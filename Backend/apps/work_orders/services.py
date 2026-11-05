"""
VEDA V2 — work_orders service layer

create_work_order()     — builds work order from all APPROVED estimate items
update_item_progress()  — mechanic marks a work order item started/completed
complete_work_order()   — all items done, transitions order to FINAL_INSPECTION
"""

import logging
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User
from apps.estimates.services import get_approved_items
from apps.organizations.models import WorkshopMembership
from apps.service_orders.models import ServiceOrder, ServiceOrderStatus
from apps.service_orders.services import transition_order
from .models import WorkOrder, WorkOrderItem, WorkStatus, ItemCompletionStatus

logger = logging.getLogger("veda.work_orders")


class WorkOrderError(Exception):
    pass

class NotFoundError(WorkOrderError):
    pass

class PermissionError(WorkOrderError):
    pass


def _assert_workshop_member(user: User, order: ServiceOrder) -> None:
    if not WorkshopMembership.objects.filter(
        user=user, service_centre=order.service_centre, is_active=True
    ).exists():
        raise PermissionError("Only workshop members can manage work orders.")


# ---------------------------------------------------------------------------
# Create work order from approved estimate items
# ---------------------------------------------------------------------------

@transaction.atomic
def create_work_order(order_id: str, created_by: User) -> WorkOrder:
    """
    Creates a WorkOrder with one WorkOrderItem per APPROVED EstimateItem.
    Only called after owner approval (APPROVED or PARTIALLY_APPROVED status).
    """
    try:
        order = ServiceOrder.objects.select_related("service_centre").get(id=order_id)
    except ServiceOrder.DoesNotExist:
        raise NotFoundError("Service order not found.")

    _assert_workshop_member(created_by, order)

    if order.status not in (ServiceOrderStatus.APPROVED, ServiceOrderStatus.PARTIALLY_APPROVED):
        raise WorkOrderError(
            f"Work order can only be created when order is APPROVED or PARTIALLY_APPROVED. "
            f"Current status: {order.status}"
        )

    if hasattr(order, "work_order"):
        raise WorkOrderError("A work order already exists for this service order.")

    approved_items = get_approved_items(order_id)
    if not approved_items:
        raise WorkOrderError("No approved estimate items found.")

    work_order = WorkOrder.objects.create(
        service_order=order,
        created_by=created_by,
    )

    for item in approved_items:
        WorkOrderItem.objects.create(
            work_order=work_order,
            estimate_item=item,
        )

    # Transition to REPAIR_IN_PROGRESS
    transition_order(order, ServiceOrderStatus.REPAIR_IN_PROGRESS, created_by,
                     f"Work order created with {len(approved_items)} approved item(s).")

    work_order.work_status = WorkStatus.IN_PROGRESS
    work_order.started_at  = timezone.now()
    work_order.save(update_fields=["work_status", "started_at", "updated_at"])

    logger.info(f"WorkOrder {work_order.id} created for order {order_id} "
                f"({len(approved_items)} items)")
    return work_order


# ---------------------------------------------------------------------------
# Update item progress
# ---------------------------------------------------------------------------

@transaction.atomic
def update_item_progress(item_id: str, mechanic: User,
                          status: str, notes: str = "") -> WorkOrderItem:
    try:
        item = WorkOrderItem.objects.select_related(
            "work_order__service_order__service_centre"
        ).get(id=item_id)
    except WorkOrderItem.DoesNotExist:
        raise NotFoundError("Work order item not found.")

    _assert_workshop_member(mechanic, item.work_order.service_order)

    valid = [v[0] for v in ItemCompletionStatus.choices]
    if status not in valid:
        raise WorkOrderError(f"Invalid status '{status}'.")

    item.completion_status = status
    item.mechanic_notes    = notes.strip()
    if status == ItemCompletionStatus.COMPLETED:
        item.completed_at = timezone.now()
    item.save(update_fields=["completion_status", "mechanic_notes", "completed_at", "updated_at"])
    return item


# ---------------------------------------------------------------------------
# Complete work order → FINAL_INSPECTION
# ---------------------------------------------------------------------------

@transaction.atomic
def complete_work_order(work_order_id: str, mechanic: User) -> WorkOrder:
    try:
        wo = WorkOrder.objects.select_related(
            "service_order__service_centre"
        ).prefetch_related("items").get(id=work_order_id)
    except WorkOrder.DoesNotExist:
        raise NotFoundError("Work order not found.")

    _assert_workshop_member(mechanic, wo.service_order)

    pending = wo.items.filter(
        completion_status__in=[ItemCompletionStatus.PENDING, ItemCompletionStatus.STARTED]
    ).count()
    if pending:
        raise WorkOrderError(
            f"{pending} item(s) are not yet completed. Mark all items completed or skipped first."
        )

    wo.work_status  = WorkStatus.COMPLETED
    wo.completed_at = timezone.now()
    wo.save(update_fields=["work_status", "completed_at", "updated_at"])

    transition_order(wo.service_order, ServiceOrderStatus.FINAL_INSPECTION, mechanic,
                     "All repair items completed. Ready for final inspection.")
    return wo


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------

def get_work_order(order_id: str, user: User) -> WorkOrder:
    try:
        order = ServiceOrder.objects.get(id=order_id)
    except ServiceOrder.DoesNotExist:
        raise NotFoundError("Service order not found.")

    is_owner  = order.owner_id == user.id
    is_member = WorkshopMembership.objects.filter(
        user=user, service_centre=order.service_centre, is_active=True
    ).exists()
    if not (is_owner or is_member):
        raise PermissionError("Access denied.")

    try:
        return WorkOrder.objects.prefetch_related(
            "items__estimate_item__component",
            "items__estimate_item__part"
        ).get(service_order=order)
    except WorkOrder.DoesNotExist:
        raise NotFoundError("No work order found for this service order.")
