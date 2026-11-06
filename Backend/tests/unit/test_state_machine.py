"""
VEDA V2 — Service order state machine tests

- Valid transitions succeed
- Invalid transitions are blocked with TransitionError
- Terminal states cannot be transitioned from
- Audit events are recorded for every transition
"""

import pytest
from apps.service_orders.models import (
    ServiceOrder, ServiceOrderStatus, ServiceOrderEvent, ALLOWED_TRANSITIONS
)
from apps.service_orders.services import (
    transition_order, TransitionError, create_service_order
)


@pytest.mark.django_db
class TestStateMachineTransitions:
    def test_requested_to_accepted(self, service_order, admin_user):
        order = transition_order(
            service_order, ServiceOrderStatus.ACCEPTED, admin_user, "Accepted."
        )
        assert order.status == ServiceOrderStatus.ACCEPTED

    def test_requested_to_rejected(self, service_order, admin_user):
        order = transition_order(
            service_order, ServiceOrderStatus.REJECTED, admin_user,
            rejection_reason="Not available."
        )
        assert order.status == ServiceOrderStatus.REJECTED
        order.refresh_from_db()
        assert order.rejection_reason == "Not available."

    def test_invalid_transition_raises(self, service_order, admin_user):
        # REQUESTED -> REPAIR_IN_PROGRESS is not allowed
        with pytest.raises(TransitionError):
            transition_order(
                service_order, ServiceOrderStatus.REPAIR_IN_PROGRESS, admin_user
            )

    def test_skip_step_raises(self, accepted_order, admin_user):
        # ACCEPTED -> INSPECTION_IN_PROGRESS skips VEHICLE_RECEIVED
        with pytest.raises(TransitionError):
            transition_order(
                accepted_order, ServiceOrderStatus.INSPECTION_IN_PROGRESS, admin_user
            )

    def test_terminal_state_locked(self, service_order, admin_user):
        # Go to REJECTED (terminal)
        transition_order(service_order, ServiceOrderStatus.REJECTED, admin_user)
        with pytest.raises(TransitionError):
            transition_order(service_order, ServiceOrderStatus.ACCEPTED, admin_user)

    def test_cancelled_is_terminal(self, service_order, admin_user):
        transition_order(service_order, ServiceOrderStatus.CANCELLED, admin_user)
        with pytest.raises(TransitionError):
            transition_order(service_order, ServiceOrderStatus.ACCEPTED, admin_user)

    def test_vehicle_received_sets_timestamp(self, accepted_order, admin_user):
        order = transition_order(
            accepted_order, ServiceOrderStatus.VEHICLE_RECEIVED, admin_user
        )
        order.refresh_from_db()
        assert order.received_at is not None

    def test_delivery_sets_completed_timestamp(self, db, accepted_order, admin_user,
                                                 mechanic_user, centre_with_mechanic):
        from apps.service_orders.services import assign_mechanic
        from apps.inspections.services import start_inspection, add_inspection_item, complete_inspection
        from apps.estimates.services import create_estimate, add_estimate_item, submit_estimate, owner_decide_item
        from apps.estimates.models import ApprovalStatus
        from apps.work_orders.services import create_work_order, update_item_progress, complete_work_order
        from apps.billing.services import generate_invoice, process_payment, deliver_vehicle
        from apps.components.models import Component
        from apps.inventory.models import PartCatalog
        from decimal import Decimal

        # ACCEPTED -> VEHICLE_RECEIVED
        order = transition_order(accepted_order, ServiceOrderStatus.VEHICLE_RECEIVED, admin_user)
        assign_mechanic(order, mechanic_user, admin_user)

        comp, _ = Component.objects.get_or_create(
            component_code="APS2", defaults={
                "component_name": "APS", "vehicle_system": "AIR_SYSTEM"
            })
        part = PartCatalog.objects.create(part_name="Test Part", part_number="TP-SM-01")

        insp = start_inspection(order, mechanic_user)
        add_inspection_item(insp, mechanic_user, "APS2", "Test.", "LOW")
        complete_inspection(insp, mechanic_user)

        est = create_estimate(str(order.id), mechanic_user)
        item = add_estimate_item(est, mechanic_user, "APS2", "Fix it", 1,
                                  Decimal("100.00"), Decimal("50.00"))
        submit_estimate(est, mechanic_user)
        owner_decide_item(str(item.id), order.owner, ApprovalStatus.APPROVED)

        order.refresh_from_db()
        wo = create_work_order(str(order.id), admin_user)
        wi = wo.items.first()
        update_item_progress(str(wi.id), mechanic_user, "COMPLETED", "Done.")
        complete_work_order(str(wo.id), mechanic_user)

        order.refresh_from_db()
        invoice = generate_invoice(str(order.id), admin_user)
        process_payment(str(invoice.id), order.owner)
        order.refresh_from_db()
        deliver_vehicle(str(order.id), admin_user)
        order.refresh_from_db()

        assert order.status == ServiceOrderStatus.VEHICLE_DELIVERED
        assert order.completed_at is not None


@pytest.mark.django_db
class TestAuditTrail:
    def test_transition_creates_event(self, service_order, admin_user):
        initial_count = ServiceOrderEvent.objects.filter(service_order=service_order).count()
        transition_order(service_order, ServiceOrderStatus.ACCEPTED, admin_user, "Test note.")
        new_count = ServiceOrderEvent.objects.filter(service_order=service_order).count()
        assert new_count == initial_count + 1

    def test_event_records_correct_states(self, service_order, admin_user):
        transition_order(service_order, ServiceOrderStatus.ACCEPTED, admin_user)
        event = ServiceOrderEvent.objects.filter(service_order=service_order).last()
        assert event.from_status == ServiceOrderStatus.REQUESTED
        assert event.to_status   == ServiceOrderStatus.ACCEPTED
        assert event.triggered_by == admin_user

    def test_multiple_transitions_all_recorded(self, accepted_order, admin_user):
        transition_order(accepted_order, ServiceOrderStatus.VEHICLE_RECEIVED, admin_user)
        events = ServiceOrderEvent.objects.filter(service_order=accepted_order).order_by("created_at")
        statuses = [e.to_status for e in events]
        assert ServiceOrderStatus.ACCEPTED       in statuses
        assert ServiceOrderStatus.VEHICLE_RECEIVED in statuses


@pytest.mark.django_db
class TestCanTransitionTo:
    def test_all_allowed_transitions_pass(self):
        for from_status, targets in ALLOWED_TRANSITIONS.items():
            order = ServiceOrder.__new__(ServiceOrder)
            order.status = from_status
            for target in targets:
                assert order.can_transition_to(target), \
                    f"Expected {from_status} -> {target} to be allowed"

    def test_disallowed_transitions_fail(self):
        order = ServiceOrder.__new__(ServiceOrder)
        order.status = ServiceOrderStatus.REQUESTED
        # REQUESTED -> INVOICED should never be allowed
        assert not order.can_transition_to(ServiceOrderStatus.INVOICED)
        assert not order.can_transition_to(ServiceOrderStatus.PAID)
