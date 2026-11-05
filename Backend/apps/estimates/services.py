"""
VEDA V2 — estimates service layer

Mechanics create and submit estimates.
Owners approve or reject individual items.
Only APPROVED items can proceed to work orders.
Mechanics cannot approve items on behalf of owners.
"""

import logging
from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User, UserRole
from apps.components.models import Component
from apps.organizations.models import WorkshopMembership
from apps.service_orders.models import ServiceOrder, ServiceOrderStatus
from apps.service_orders.services import transition_order
from .models import (
    RepairEstimate, EstimateItem,
    EstimateStatus, ApprovalStatus,
)

logger = logging.getLogger("veda.estimates")


class EstimateError(Exception):
    pass

class NotFoundError(EstimateError):
    pass

class PermissionError(EstimateError):
    pass

class ApprovalError(EstimateError):
    pass


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _assert_mechanic_or_admin(user: User, order: ServiceOrder) -> None:
    if not WorkshopMembership.objects.filter(
        user=user, service_centre=order.service_centre, is_active=True
    ).exists():
        raise PermissionError("Only workshop members can manage estimates.")


def _assert_owner(user: User, order: ServiceOrder) -> None:
    if order.owner_id != user.id:
        raise PermissionError("Only the vehicle owner can approve or reject estimate items.")


def _get_order(order_id: str) -> ServiceOrder:
    try:
        return ServiceOrder.objects.select_related(
            "service_centre", "owner", "vehicle"
        ).get(id=order_id)
    except ServiceOrder.DoesNotExist:
        raise NotFoundError("Service order not found.")


# ---------------------------------------------------------------------------
# Create estimate
# ---------------------------------------------------------------------------

@transaction.atomic
def create_estimate(order_id: str, mechanic: User, notes: str = "") -> RepairEstimate:
    order = _get_order(order_id)
    _assert_mechanic_or_admin(mechanic, order)

    # Determine next revision number
    last = RepairEstimate.objects.filter(service_order=order).order_by("-revision_number").first()
    revision = (last.revision_number + 1) if last else 1

    estimate = RepairEstimate.objects.create(
        service_order=order,
        revision_number=revision,
        estimate_status=EstimateStatus.DRAFT,
        notes=notes,
        created_by=mechanic,
    )
    logger.info(f"Estimate #{revision} created for order {order_id}")
    return estimate


# ---------------------------------------------------------------------------
# Add / update estimate items
# ---------------------------------------------------------------------------

@transaction.atomic
def add_estimate_item(
    estimate: RepairEstimate,
    mechanic: User,
    component_code: str,
    description: str,
    quantity: int,
    unit_price: Decimal,
    labour_cost: Decimal,
    part_id: str = None,
) -> EstimateItem:
    _assert_mechanic_or_admin(mechanic, estimate.service_order)

    if estimate.estimate_status not in (EstimateStatus.DRAFT, EstimateStatus.REVISED):
        raise EstimateError("Cannot add items to a submitted or accepted estimate.")

    try:
        component = Component.objects.get(component_code=component_code)
    except Component.DoesNotExist:
        raise EstimateError(f"Component '{component_code}' not found.")

    part = None
    if part_id:
        from apps.inventory.models import PartCatalog
        try:
            part = PartCatalog.objects.get(id=part_id, is_active=True)
        except PartCatalog.DoesNotExist:
            raise EstimateError("Part not found.")

    item = EstimateItem.objects.create(
        estimate=estimate,
        component=component,
        part=part,
        description=description,
        quantity=quantity,
        unit_price=unit_price,
        labour_cost=labour_cost,
    )
    estimate.recalculate_totals()
    return item


# ---------------------------------------------------------------------------
# Submit estimate to owner
# ---------------------------------------------------------------------------

@transaction.atomic
def submit_estimate(estimate: RepairEstimate, mechanic: User) -> RepairEstimate:
    _assert_mechanic_or_admin(mechanic, estimate.service_order)

    if estimate.estimate_status not in (EstimateStatus.DRAFT, EstimateStatus.REVISED):
        raise EstimateError("Only DRAFT or REVISED estimates can be submitted.")
    if not estimate.items.exists():
        raise EstimateError("Cannot submit an estimate with no line items.")

    estimate.recalculate_totals()
    estimate.estimate_status = EstimateStatus.SUBMITTED
    estimate.save(update_fields=["estimate_status", "updated_at"])

    # Transition service order to AWAITING_APPROVAL
    order = estimate.service_order
    if order.can_transition_to(ServiceOrderStatus.AWAITING_APPROVAL):
        transition_order(
            order, ServiceOrderStatus.AWAITING_APPROVAL, mechanic,
            f"Estimate #{estimate.revision_number} submitted for owner approval."
        )

    logger.info(f"Estimate #{estimate.revision_number} submitted for order {order.id}")
    return estimate


# ---------------------------------------------------------------------------
# Owner approves / rejects individual items
# ---------------------------------------------------------------------------

@transaction.atomic
def owner_decide_item(
    item_id: str, owner: User,
    decision: str, note: str = ""
) -> EstimateItem:
    """
    Owner approves, rejects, or requests clarification on a single line item.
    Mechanics cannot call this function — enforced by _assert_owner().
    """
    try:
        item = EstimateItem.objects.select_related(
            "estimate__service_order__owner"
        ).get(id=item_id)
    except EstimateItem.DoesNotExist:
        raise NotFoundError("Estimate item not found.")

    _assert_owner(owner, item.estimate.service_order)

    if item.estimate.estimate_status != EstimateStatus.SUBMITTED:
        raise ApprovalError("Items can only be approved on a SUBMITTED estimate.")

    valid_decisions = [v[0] for v in ApprovalStatus.choices]
    if decision not in valid_decisions:
        raise ApprovalError(f"Invalid decision '{decision}'.")

    item.approval_status      = decision
    item.owner_decision_at    = timezone.now()
    item.owner_decision_by    = owner
    item.clarification_note   = note.strip()
    item.save(update_fields=[
        "approval_status", "owner_decision_at",
        "owner_decision_by", "clarification_note", "updated_at"
    ])

    # After every decision, check if all items have been reviewed
    _check_estimate_completion(item.estimate, owner)

    logger.info(
        f"Owner {owner.phone_number} set item {item_id} -> {decision}"
    )
    return item


def _check_estimate_completion(estimate: RepairEstimate, owner: User) -> None:
    """
    After owner decisions, transition the order if all items are decided.
    """
    items = estimate.items.all()
    pending = items.filter(approval_status=ApprovalStatus.PENDING).count()
    if pending > 0:
        return  # still waiting for more decisions

    approved_count = items.filter(approval_status=ApprovalStatus.APPROVED).count()
    rejected_count = items.filter(approval_status=ApprovalStatus.REJECTED).count()
    order = estimate.service_order

    if approved_count == 0:
        estimate.estimate_status = EstimateStatus.REJECTED
        estimate.save(update_fields=["estimate_status", "updated_at"])
        if order.can_transition_to(ServiceOrderStatus.REVISION_REQUESTED):
            transition_order(order, ServiceOrderStatus.REVISION_REQUESTED, owner,
                             "All estimate items rejected by owner.")
    elif rejected_count == 0:
        estimate.estimate_status = EstimateStatus.ACCEPTED
        estimate.save(update_fields=["estimate_status", "updated_at"])
        if order.can_transition_to(ServiceOrderStatus.APPROVED):
            transition_order(order, ServiceOrderStatus.APPROVED, owner,
                             "All estimate items approved by owner.")
    else:
        estimate.estimate_status = EstimateStatus.ACCEPTED
        estimate.save(update_fields=["estimate_status", "updated_at"])
        if order.can_transition_to(ServiceOrderStatus.PARTIALLY_APPROVED):
            transition_order(order, ServiceOrderStatus.PARTIALLY_APPROVED, owner,
                             f"{approved_count} items approved, {rejected_count} rejected.")


# ---------------------------------------------------------------------------
# Read operations
# ---------------------------------------------------------------------------

def get_estimates_for_order(order_id: str, user: User) -> list:
    order = _get_order(order_id)
    is_owner = order.owner_id == user.id
    is_member = WorkshopMembership.objects.filter(
        user=user, service_centre=order.service_centre, is_active=True
    ).exists()
    if not (is_owner or is_member):
        raise PermissionError("Access denied.")
    return list(
        RepairEstimate.objects.filter(service_order=order)
        .prefetch_related("items__component", "items__part")
        .order_by("-revision_number")
    )


def get_estimate(estimate_id: str, user: User) -> RepairEstimate:
    try:
        estimate = RepairEstimate.objects.prefetch_related(
            "items__component", "items__part"
        ).get(id=estimate_id)
    except RepairEstimate.DoesNotExist:
        raise NotFoundError("Estimate not found.")

    order = estimate.service_order
    is_owner = order.owner_id == user.id
    is_member = WorkshopMembership.objects.filter(
        user=user, service_centre=order.service_centre, is_active=True
    ).exists()
    if not (is_owner or is_member):
        raise PermissionError("Access denied.")
    return estimate


def get_approved_items(order_id: str) -> list:
    """Return all APPROVED estimate items for an order — used by work order creation."""
    return list(
        EstimateItem.objects.filter(
            estimate__service_order_id=order_id,
            approval_status=ApprovalStatus.APPROVED,
        ).select_related("component", "part")
    )
