"""VEDA V2 — components service layer"""

from django.db import transaction
from .models import Component, VehicleComponent, VehicleComponentStatus


class ComponentError(Exception):
    pass


def get_catalogue(system: str = None, active_only: bool = True):
    qs = Component.objects.all()
    if active_only:
        qs = qs.filter(status="ACTIVE")
    if system:
        qs = qs.filter(vehicle_system=system)
    return qs.select_related("parent")


def get_component_by_code(code: str) -> Component:
    try:
        return Component.objects.get(component_code=code)
    except Component.DoesNotExist:
        raise ComponentError(f"Component '{code}' not found.")


def get_root_components(system: str = None):
    """Return top-level components (no parent)."""
    qs = Component.objects.filter(parent__isnull=True, status="ACTIVE")
    if system:
        qs = qs.filter(vehicle_system=system)
    return qs.prefetch_related("children")


@transaction.atomic
def add_vehicle_component(vehicle, component_code: str, installation_date=None, notes: str = "") -> VehicleComponent:
    component = get_component_by_code(component_code)
    vc, created = VehicleComponent.objects.get_or_create(
        vehicle=vehicle,
        component=component,
        defaults={
            "installation_date": installation_date,
            "notes": notes,
            "current_status": VehicleComponentStatus.UNKNOWN,
        },
    )
    if not created:
        raise ComponentError(
            f"Component '{component_code}' is already linked to this vehicle."
        )
    return vc


def get_vehicle_components(vehicle):
    return VehicleComponent.objects.filter(vehicle=vehicle).select_related("component")
