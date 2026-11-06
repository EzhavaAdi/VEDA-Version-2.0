"""
VEDA V2 — Data isolation tests

Critical security tests:
- Owner can only access their own vehicles
- Owner cannot access another owner's vehicles
- Workshop members can only access their centre's orders
- Non-members are blocked from workshop data
"""

import pytest
from apps.vehicles.services import (
    get_vehicle_for_owner, VehiclePermissionError, VehicleNotFoundError
)
from apps.service_orders.services import (
    get_order_for_owner, get_order_for_centre, get_orders_for_centre,
    NotFoundError, PermissionError
)


@pytest.mark.django_db
class TestOwnerVehicleIsolation:
    def test_owner_can_access_own_vehicle(self, vehicle, owner_user):
        v = get_vehicle_for_owner(str(vehicle.id), owner_user)
        assert v.id == vehicle.id

    def test_owner_cannot_access_other_vehicle(self, other_vehicle, owner_user):
        with pytest.raises((VehiclePermissionError, VehicleNotFoundError)):
            get_vehicle_for_owner(str(other_vehicle.id), owner_user)

    def test_other_owner_cannot_access_first_owner_vehicle(self, vehicle, other_owner):
        with pytest.raises((VehiclePermissionError, VehicleNotFoundError)):
            get_vehicle_for_owner(str(vehicle.id), other_owner)

    def test_nonexistent_vehicle_raises_not_found(self, owner_user):
        import uuid
        with pytest.raises((VehiclePermissionError, VehicleNotFoundError)):
            get_vehicle_for_owner(str(uuid.uuid4()), owner_user)


@pytest.mark.django_db
class TestServiceOrderOwnerIsolation:
    def test_owner_can_access_own_order(self, service_order, owner_user):
        order = get_order_for_owner(str(service_order.id), owner_user)
        assert order.id == service_order.id

    def test_other_owner_blocked_from_order(self, service_order, other_owner):
        with pytest.raises(NotFoundError):
            get_order_for_owner(str(service_order.id), other_owner)

    def test_mechanic_blocked_from_owner_endpoint(self, service_order, mechanic_user):
        with pytest.raises(NotFoundError):
            get_order_for_owner(str(service_order.id), mechanic_user)


@pytest.mark.django_db
class TestWorkshopAccessIsolation:
    def test_member_can_access_centre_order(self, service_order, admin_user):
        order = get_order_for_centre(str(service_order.id), admin_user)
        assert order.id == service_order.id

    def test_non_member_blocked_from_centre_order(self, service_order, other_owner):
        with pytest.raises(PermissionError):
            get_order_for_centre(str(service_order.id), other_owner)

    def test_non_member_blocked_from_centre_order_list(self, service_centre, other_owner):
        with pytest.raises(PermissionError):
            list(get_orders_for_centre(str(service_centre.id), other_owner))

    def test_mechanic_member_can_access_centre_order(
        self, service_order, mechanic_user, centre_with_mechanic
    ):
        order = get_order_for_centre(str(service_order.id), mechanic_user)
        assert order.id == service_order.id
