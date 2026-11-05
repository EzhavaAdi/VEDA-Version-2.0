"""VEDA V2 — vehicles service layer

Owner isolation: every method that retrieves a vehicle requires the requesting
user, and raises VehicleNotFoundError if the vehicle does not belong to them.
Workshop users may also access vehicles on their assigned service orders —
that cross-access is handled at the service_orders layer in Phase 3.
"""

from django.db import transaction
from .models import Vehicle, VehicleDocument


class VehicleError(Exception):
    pass

class VehicleNotFoundError(VehicleError):
    pass

class VehiclePermissionError(VehicleError):
    pass


@transaction.atomic
def register_vehicle(owner, data: dict) -> Vehicle:
    reg = data.get("registration_number", "").strip().upper()
    if Vehicle.objects.filter(registration_number=reg).exists():
        raise VehicleError(
            f"Registration number '{reg}' is already registered on VEDA."
        )
    vehicle = Vehicle.objects.create(
        owner=owner,
        registration_number=reg,
        manufacturer=data["manufacturer"],
        model=data["model"],
        vehicle_category=data.get("vehicle_category", "OTHER"),
        manufacturing_year=data["manufacturing_year"],
        vin=data.get("vin", ""),
        odometer_reading=data.get("odometer_reading", 0),
        operating_hours=data.get("operating_hours", 0),
        notes=data.get("notes", ""),
    )
    return vehicle


def get_owner_vehicles(owner, active_only: bool = True):
    qs = Vehicle.objects.filter(owner=owner)
    if active_only:
        qs = qs.filter(is_active=True)
    return qs.order_by("-created_at")


def get_vehicle_for_owner(vehicle_id: str, owner) -> Vehicle:
    """Retrieve a vehicle, enforcing ownership."""
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id, is_active=True)
    except Vehicle.DoesNotExist:
        raise VehicleNotFoundError("Vehicle not found.")
    if vehicle.owner_id != owner.id:
        raise VehiclePermissionError("You do not have access to this vehicle.")
    return vehicle


@transaction.atomic
def update_vehicle(vehicle: Vehicle, data: dict) -> Vehicle:
    allowed = ["odometer_reading", "operating_hours", "notes", "vin"]
    for field in allowed:
        if field in data:
            setattr(vehicle, field, data[field])
    vehicle.save(update_fields=allowed + ["updated_at"])
    return vehicle


@transaction.atomic
def deactivate_vehicle(vehicle: Vehicle) -> Vehicle:
    vehicle.is_active = False
    vehicle.save(update_fields=["is_active", "updated_at"])
    return vehicle
