"""
VEDA V2 — pytest conftest.py
Shared fixtures for the entire test suite.
"""

import pytest
from decimal import Decimal
from django.utils import timezone
from apps.accounts.models import User, Role, UserRole
from apps.organizations.models import ServiceCentre, WorkshopMembership, Designation
from apps.vehicles.models import Vehicle, VehicleCategory
from apps.components.models import Component, VehicleSystem
from apps.service_orders.models import ServiceOrder, ServiceOrderStatus
from apps.inspections.models import Inspection
from apps.inventory.models import PartCatalog, WorkshopInventory
from apps.estimates.models import RepairEstimate, EstimateItem


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_user(phone: str, role: str = None) -> User:
    user, _ = User.objects.get_or_create(
        phone_number=phone,
        defaults={"full_name": f"Test {phone[-4:]}"}
    )
    if role:
        Role.objects.get_or_create(user=user, role=role)
    return user


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

@pytest.fixture
def owner_user(db):
    return make_user("+919100000001", UserRole.OWNER)


@pytest.fixture
def mechanic_user(db):
    return make_user("+919100000002", UserRole.MECHANIC)


@pytest.fixture
def admin_user(db):
    return make_user("+919100000003", UserRole.WORKSHOP_ADMIN)


@pytest.fixture
def other_owner(db):
    return make_user("+919100000099", UserRole.OWNER)


# ---------------------------------------------------------------------------
# Service Centre
# ---------------------------------------------------------------------------

@pytest.fixture
def service_centre(db, admin_user):
    centre = ServiceCentre.objects.create(
        name="Test Workshop",
        address="1 Test Street",
        contact_number="+910000000000",
        registered_by=admin_user,
    )
    WorkshopMembership.objects.create(
        user=admin_user, service_centre=centre, designation=Designation.ADMIN
    )
    return centre


@pytest.fixture
def centre_with_mechanic(db, service_centre, mechanic_user):
    WorkshopMembership.objects.get_or_create(
        user=mechanic_user, service_centre=service_centre,
        defaults={"designation": Designation.MECHANIC}
    )
    return service_centre


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------

@pytest.fixture
def aps_component(db):
    comp, _ = Component.objects.get_or_create(
        component_code="APS",
        defaults={
            "component_name": "Air Pressure System",
            "vehicle_system": VehicleSystem.AIR_SYSTEM,
        }
    )
    return comp


@pytest.fixture
def brake_component(db):
    comp, _ = Component.objects.get_or_create(
        component_code="BRAKES",
        defaults={
            "component_name": "Brake System",
            "vehicle_system": VehicleSystem.BRAKES,
        }
    )
    return comp


# ---------------------------------------------------------------------------
# Vehicle
# ---------------------------------------------------------------------------

@pytest.fixture
def vehicle(db, owner_user):
    return Vehicle.objects.create(
        owner=owner_user,
        registration_number="MH01TEST01",
        manufacturer="Tata",
        model="Prima",
        vehicle_category=VehicleCategory.SEMI_TRAILER,
        manufacturing_year=2021,
    )


@pytest.fixture
def other_vehicle(db, other_owner):
    return Vehicle.objects.create(
        owner=other_owner,
        registration_number="MH01TEST99",
        manufacturer="Ashok Leyland",
        model="U-Truck",
        vehicle_category=VehicleCategory.RIGID_TRUCK,
        manufacturing_year=2020,
    )


# ---------------------------------------------------------------------------
# Service Order
# ---------------------------------------------------------------------------

@pytest.fixture
def service_order(db, vehicle, service_centre, owner_user):
    return ServiceOrder.objects.create(
        vehicle=vehicle,
        service_centre=service_centre,
        owner=owner_user,
        service_description="Test service request.",
        status=ServiceOrderStatus.REQUESTED,
    )


@pytest.fixture
def accepted_order(db, service_order, admin_user):
    from apps.service_orders.services import transition_order
    transition_order(service_order, ServiceOrderStatus.ACCEPTED, admin_user)
    return service_order


@pytest.fixture
def order_with_mechanic(db, accepted_order, mechanic_user, centre_with_mechanic, admin_user):
    from apps.service_orders.services import transition_order, assign_mechanic
    transition_order(accepted_order, ServiceOrderStatus.VEHICLE_RECEIVED, admin_user)
    assign_mechanic(accepted_order, mechanic_user, admin_user)
    return accepted_order


@pytest.fixture
def completed_inspection(db, order_with_mechanic, mechanic_user, aps_component):
    from apps.inspections.services import (
        start_inspection, add_inspection_item, complete_inspection
    )
    insp = start_inspection(order_with_mechanic, mechanic_user)
    add_inspection_item(
        insp, mechanic_user, aps_component.component_code,
        "APS compressor bearing failure.", "HIGH"
    )
    complete_inspection(insp, mechanic_user)
    return insp


# ---------------------------------------------------------------------------
# Inventory + Estimate
# ---------------------------------------------------------------------------

@pytest.fixture
def aps_part(db):
    return PartCatalog.objects.create(
        part_name="APS Compressor Unit",
        part_number="APS-COMP-TEST",
        manufacturer="Knorr-Bremse",
    )


@pytest.fixture
def workshop_inventory(db, service_centre, aps_part):
    return WorkshopInventory.objects.create(
        service_centre=service_centre,
        part=aps_part,
        quantity_available=5,
        unit_price=Decimal("4500.00"),
    )


@pytest.fixture
def submitted_estimate(db, completed_inspection, mechanic_user, aps_component, aps_part):
    from apps.estimates.services import (
        create_estimate, add_estimate_item, submit_estimate
    )
    order = completed_inspection.service_order
    est = create_estimate(str(order.id), mechanic_user)
    add_estimate_item(
        est, mechanic_user,
        aps_component.component_code,
        "Replace APS compressor", 1,
        Decimal("4500.00"), Decimal("900.00"),
        str(aps_part.id),
    )
    submit_estimate(est, mechanic_user)
    return est
