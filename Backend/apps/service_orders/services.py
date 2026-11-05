"""
VEDA V2 — service_orders service layer

All state transitions go through transition_order().
No view may set status directly on the model.
"""

import logging
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User, UserRole
from apps.organizations.models import ServiceCentre, WorkshopMembership
from apps.vehicles.models import Vehicle
from .models import ServiceOrder, ServiceOrderEvent, ServiceOrderStatus, ALLOWED_TRANSITIONS

logger = logging.getLogger("veda.service_orders")


class ServiceOrderError(Exception):
    pass

class TransitionError(ServiceOrderError):
    pass

class PermissionError(ServiceOrderError):
    pass

class NotFoundError(ServiceOrderError):
    pass


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _record_event(order: ServiceOrder, from_status: str, to_status: str,
                  user: User, notes: str = "") -> ServiceOrderEvent:
    return ServiceOrderEvent.objects.create(
        service_order=order,
        from_status=from_status,
        to_status=to_status,
        triggered_by=user,
        notes=notes,
    )


def _assert_can_transition(order: ServiceOrder, target: str) -> None:
    if not order.can_transition_to(target):
        allowed = ALLOWED_TRANSITIONS.get(order.status, [])
        raise TransitionError(
            f"Cannot move from '{order.status}' to '{target}'. "
            f"Allowed transitions: {allowed or ['none (terminal state)']}."
        )


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

@transaction.atomic
def create_service_order(owner: User, vehicle_id: str,
                         centre_id: str, description: str) -> ServiceOrder:
    """Owner submits a service request."""
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id, owner=owner, is_active=True)
    except Vehicle.DoesNotExist:
        raise NotFoundError("Vehicle not found or does not belong to you.")

    try:
        centre = ServiceCentre.objects.get(id=centre_id, is_active=True)
    except ServiceCentre.DoesNotExist:
        raise NotFoundError("Service centre not found.")

    if centre.verification_status not in ("VERIFIED", "PENDING"):
        raise ServiceOrderError("This service centre is not currently accepting requests.")

    order = ServiceOrder.objects.create(
        vehicle=vehicle,
        service_centre=centre,
        owner=owner,
        service_description=description.strip(),
        status=ServiceOrderStatus.REQUESTED,
    )
    _record_event(order, "", ServiceOrderStatus.REQUESTED, owner, "Service request submitted.")
    logger.info(f"ServiceOrder {order.id} created by owner {owner.id}")
    return order


# ---------------------------------------------------------------------------
# State transitions
# ---------------------------------------------------------------------------

@transaction.atomic
def transition_order(order: ServiceOrder, new_status: str,
                     triggered_by: User, notes: str = "", **kwargs) -> ServiceOrder:
    """
    Central transition method. All status changes go through here.
    kwargs carry transition-specific data (mechanic_id, rejection_reason, etc.)
    """
    _assert_can_transition(order, new_status)
    old_status = order.status
    order.status = new_status

    # Transition-specific side effects
    if new_status == ServiceOrderStatus.VEHICLE_RECEIVED:
        order.received_at = timezone.now()

    if new_status == ServiceOrderStatus.REJECTED:
        order.rejection_reason = kwargs.get("rejection_reason", "")

    if new_status == ServiceOrderStatus.VEHICLE_DELIVERED:
        order.completed_at = timezone.now()

    order.save(update_fields=["status", "rejection_reason", "received_at",
                               "completed_at", "updated_at"])
    _record_event(order, old_status, new_status, triggered_by, notes)
    logger.info(f"ServiceOrder {order.id}: {old_status} -> {new_status} by {triggered_by.id}")
    return order


@transaction.atomic
def assign_mechanic(order: ServiceOrder, mechanic: User, admin: User) -> ServiceOrder:
    """Assign a mechanic to the order (workshop admin action)."""
    # Verify mechanic belongs to this centre
    if not WorkshopMembership.objects.filter(
        user=mechanic,
        service_centre=order.service_centre,
        is_active=True,
    ).exists():
        raise ServiceOrderError("This mechanic does not belong to the assigned service centre.")

    if not mechanic.has_role(UserRole.MECHANIC):
        raise ServiceOrderError("The selected user does not have the MECHANIC role.")

    order.assigned_mechanic = mechanic
    order.save(update_fields=["assigned_mechanic", "updated_at"])
    _record_event(order, order.status, order.status, admin,
                  f"Mechanic {mechanic.phone_number} assigned.")
    logger.info(f"Mechanic {mechanic.id} assigned to order {order.id}")
    return order


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

def get_order_for_owner(order_id: str, owner: User) -> ServiceOrder:
    try:
        return ServiceOrder.objects.select_related(
            "vehicle", "service_centre", "assigned_mechanic"
        ).get(id=order_id, owner=owner)
    except ServiceOrder.DoesNotExist:
        raise NotFoundError("Service order not found.")


def get_orders_for_owner(owner: User):
    return ServiceOrder.objects.filter(owner=owner).select_related(
        "vehicle", "service_centre"
    ).order_by("-created_at")


def get_order_for_centre(order_id: str, user: User) -> ServiceOrder:
    """Return order if user is an active member of the order's service centre."""
    try:
        order = ServiceOrder.objects.select_related(
            "vehicle", "owner", "assigned_mechanic", "service_centre"
        ).get(id=order_id)
    except ServiceOrder.DoesNotExist:
        raise NotFoundError("Service order not found.")

    if not WorkshopMembership.objects.filter(
        user=user, service_centre=order.service_centre, is_active=True
    ).exists():
        raise PermissionError("Access denied.")
    return order


def get_orders_for_centre(centre_id: str, user: User):
    """All orders for a service centre (workshop member access)."""
    if not WorkshopMembership.objects.filter(
        user=user, service_centre_id=centre_id, is_active=True
    ).exists():
        raise PermissionError("You are not a member of this service centre.")
    return ServiceOrder.objects.filter(
        service_centre_id=centre_id
    ).select_related("vehicle", "owner", "assigned_mechanic").order_by("-created_at")


def get_orders_for_mechanic(mechanic: User):
    return ServiceOrder.objects.filter(
        assigned_mechanic=mechanic
    ).select_related("vehicle", "service_centre").order_by("-created_at")


def get_order_events(order_id: str, user: User):
    """Return audit trail — accessible to owner and workshop members."""
    try:
        order = ServiceOrder.objects.get(id=order_id)
    except ServiceOrder.DoesNotExist:
        raise NotFoundError("Service order not found.")

    is_owner = order.owner_id == user.id
    is_member = WorkshopMembership.objects.filter(
        user=user, service_centre=order.service_centre, is_active=True
    ).exists()
    if not (is_owner or is_member):
        raise PermissionError("Access denied.")

    return order.events.select_related("triggered_by").order_by("created_at")
