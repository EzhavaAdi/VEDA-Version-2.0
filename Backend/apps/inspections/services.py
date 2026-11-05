"""VEDA V2 — inspections service layer"""

import logging
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User, UserRole
from apps.components.models import Component
from apps.organizations.models import WorkshopMembership
from apps.service_orders.models import ServiceOrder, ServiceOrderStatus
from apps.service_orders.services import transition_order
from .models import Inspection, InspectionItem, SensorReading, InspectionStatus

logger = logging.getLogger("veda.inspections")


class InspectionError(Exception):
    pass

class NotFoundError(InspectionError):
    pass

class PermissionError(InspectionError):
    pass


def _assert_mechanic_on_order(mechanic: User, order: ServiceOrder) -> None:
    if order.assigned_mechanic_id != mechanic.id:
        raise PermissionError("You are not the assigned mechanic for this service order.")


# ---------------------------------------------------------------------------
# Inspection lifecycle
# ---------------------------------------------------------------------------

@transaction.atomic
def start_inspection(order: ServiceOrder, mechanic: User) -> Inspection:
    """
    Mechanic starts the inspection.
    Transitions the service order to INSPECTION_IN_PROGRESS.
    Creates the Inspection record.
    """
    _assert_mechanic_on_order(mechanic, order)

    if hasattr(order, "inspection"):
        raise InspectionError("An inspection already exists for this service order.")

    if order.status == ServiceOrderStatus.VEHICLE_RECEIVED:
        transition_order(
            order,
            ServiceOrderStatus.INSPECTION_IN_PROGRESS,
            mechanic,
            "Mechanic started inspection.",
        )
    elif order.status != ServiceOrderStatus.INSPECTION_IN_PROGRESS:
        raise InspectionError(
            f"Cannot start inspection — order is in '{order.status}' state."
        )

    inspection = Inspection.objects.create(
        service_order=order,
        mechanic=mechanic,
    )
    logger.info(f"Inspection {inspection.id} started for order {order.id}")
    return inspection


def get_inspection_for_mechanic(order_id: str, mechanic: User) -> Inspection:
    try:
        order = ServiceOrder.objects.get(id=order_id)
    except ServiceOrder.DoesNotExist:
        raise NotFoundError("Service order not found.")
    _assert_mechanic_on_order(mechanic, order)
    try:
        return Inspection.objects.get(service_order=order)
    except Inspection.DoesNotExist:
        raise NotFoundError("No inspection found for this order.")


def get_inspection_for_member(order_id: str, user: User) -> Inspection:
    """Any active workshop member can read the inspection."""
    try:
        order = ServiceOrder.objects.get(id=order_id)
    except ServiceOrder.DoesNotExist:
        raise NotFoundError("Service order not found.")
    is_member = WorkshopMembership.objects.filter(
        user=user, service_centre=order.service_centre, is_active=True
    ).exists()
    is_owner = order.owner_id == user.id
    if not (is_member or is_owner):
        raise PermissionError("Access denied.")
    try:
        return Inspection.objects.get(service_order=order)
    except Inspection.DoesNotExist:
        raise NotFoundError("No inspection found for this order.")


@transaction.atomic
def update_general_observations(inspection: Inspection, mechanic: User,
                                  text: str) -> Inspection:
    if inspection.mechanic_id != mechanic.id:
        raise PermissionError("Only the assigned mechanic can update this inspection.")
    if inspection.inspection_status == InspectionStatus.COMPLETED:
        raise InspectionError("Cannot modify a completed inspection.")
    inspection.general_observations = text
    inspection.inspection_status = InspectionStatus.IN_PROGRESS
    inspection.save(update_fields=["general_observations", "inspection_status", "updated_at"])
    return inspection


@transaction.atomic
def complete_inspection(inspection: Inspection, mechanic: User) -> Inspection:
    """Mark inspection complete and transition order to ESTIMATE_READY pathway."""
    if inspection.mechanic_id != mechanic.id:
        raise PermissionError("Only the assigned mechanic can complete this inspection.")
    if inspection.inspection_status == InspectionStatus.COMPLETED:
        raise InspectionError("Inspection is already completed.")

    inspection.inspection_status = InspectionStatus.COMPLETED
    inspection.save(update_fields=["inspection_status", "updated_at"])

    # Transition order — mechanic may go straight to ESTIMATE_READY
    # (skipping AI_DIAGNOSIS if not running the AI engine)
    order = inspection.service_order
    if order.can_transition_to(ServiceOrderStatus.ESTIMATE_READY):
        transition_order(
            order,
            ServiceOrderStatus.ESTIMATE_READY,
            mechanic,
            "Inspection completed. Estimate to be prepared.",
        )

    logger.info(f"Inspection {inspection.id} completed")
    return inspection


# ---------------------------------------------------------------------------
# Inspection items (per-component observations)
# ---------------------------------------------------------------------------

@transaction.atomic
def add_inspection_item(inspection: Inspection, mechanic: User,
                        component_code: str, condition: str,
                        severity: str, notes: str = "") -> InspectionItem:
    if inspection.mechanic_id != mechanic.id:
        raise PermissionError("Only the assigned mechanic can add observations.")
    if inspection.inspection_status == InspectionStatus.COMPLETED:
        raise InspectionError("Cannot add items to a completed inspection.")

    try:
        component = Component.objects.get(component_code=component_code)
    except Component.DoesNotExist:
        raise InspectionError(f"Component '{component_code}' not found.")

    item, created = InspectionItem.objects.update_or_create(
        inspection=inspection,
        component=component,
        defaults={
            "observed_condition": condition,
            "severity": severity,
            "mechanic_notes": notes,
        },
    )
    return item


def get_inspection_items(inspection: Inspection):
    return inspection.items.select_related("component").order_by("component__vehicle_system")


# ---------------------------------------------------------------------------
# Sensor readings (numeric measurements)
# ---------------------------------------------------------------------------

@transaction.atomic
def add_sensor_reading(inspection: Inspection, mechanic: User,
                       parameter_name: str, value, unit: str,
                       component_code: str = None, notes: str = "") -> SensorReading:
    if inspection.mechanic_id != mechanic.id:
        raise PermissionError("Only the assigned mechanic can record measurements.")
    if inspection.inspection_status == InspectionStatus.COMPLETED:
        raise InspectionError("Cannot add readings to a completed inspection.")

    component = None
    if component_code:
        try:
            component = Component.objects.get(component_code=component_code)
        except Component.DoesNotExist:
            raise InspectionError(f"Component '{component_code}' not found.")

    reading = SensorReading.objects.create(
        inspection=inspection,
        parameter_name=parameter_name,
        parameter_value=value,
        unit=unit,
        component=component,
        notes=notes,
    )
    return reading


def get_sensor_readings(inspection: Inspection):
    return inspection.sensor_readings.select_related("component").order_by("recorded_at")
