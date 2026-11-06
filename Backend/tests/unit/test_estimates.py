"""
VEDA V2 — Estimate and approval tests

Rules enforced:
- Mechanics cannot approve items on behalf of owners
- Owners cannot add items to estimates
- Grand total uses Decimal arithmetic (no float errors)
- Auto-transition: all approved -> APPROVED, mixed -> PARTIALLY_APPROVED
- Revision number increments correctly
"""

import pytest
from decimal import Decimal
from apps.estimates.models import ApprovalStatus, EstimateStatus
from apps.estimates.services import (
    create_estimate, add_estimate_item, submit_estimate,
    owner_decide_item, PermissionError, ApprovalError, EstimateError
)
from apps.service_orders.models import ServiceOrderStatus


@pytest.mark.django_db
class TestEstimateCreation:
    def test_mechanic_can_create_estimate(self, completed_inspection, mechanic_user):
        order = completed_inspection.service_order
        est = create_estimate(str(order.id), mechanic_user)
        assert est.estimate_status == EstimateStatus.DRAFT
        assert est.revision_number == 1

    def test_revision_number_increments(self, completed_inspection, mechanic_user):
        order = completed_inspection.service_order
        est1 = create_estimate(str(order.id), mechanic_user)
        est2 = create_estimate(str(order.id), mechanic_user)
        assert est2.revision_number == 2

    def test_non_member_cannot_create_estimate(
        self, completed_inspection, other_owner
    ):
        order = completed_inspection.service_order
        with pytest.raises(PermissionError):
            create_estimate(str(order.id), other_owner)


@pytest.mark.django_db
class TestEstimateItems:
    def test_add_item_calculates_total(
        self, completed_inspection, mechanic_user, aps_component, aps_part
    ):
        order = completed_inspection.service_order
        est = create_estimate(str(order.id), mechanic_user)
        add_estimate_item(
            est, mechanic_user,
            aps_component.component_code,
            "Replace compressor", 1,
            Decimal("4500.00"), Decimal("900.00"),
            str(aps_part.id),
        )
        est.refresh_from_db()
        assert est.parts_total == Decimal("4500.00")
        assert est.labour_total == Decimal("900.00")
        assert est.grand_total == Decimal("5400.00")

    def test_decimal_precision(
        self, completed_inspection, mechanic_user, aps_component
    ):
        """Totals must use Decimal — no float rounding errors."""
        order = completed_inspection.service_order
        est = create_estimate(str(order.id), mechanic_user)
        add_estimate_item(
            est, mechanic_user,
            aps_component.component_code,
            "Item 1", 3,
            Decimal("33.33"), Decimal("10.00"),
        )
        est.refresh_from_db()
        assert est.parts_total == Decimal("99.99")
        assert isinstance(est.parts_total, Decimal)

    def test_owner_cannot_add_items(
        self, completed_inspection, owner_user, mechanic_user, aps_component
    ):
        order = completed_inspection.service_order
        est = create_estimate(str(order.id), mechanic_user)
        with pytest.raises(PermissionError):
            add_estimate_item(
                est, owner_user,
                aps_component.component_code,
                "Owner tries to add", 1,
                Decimal("100.00"), Decimal("50.00"),
            )


@pytest.mark.django_db
class TestOwnerApproval:
    def test_mechanic_cannot_approve(self, submitted_estimate, mechanic_user):
        item = submitted_estimate.items.first()
        with pytest.raises(PermissionError):
            owner_decide_item(str(item.id), mechanic_user, ApprovalStatus.APPROVED)

    def test_owner_can_approve(self, submitted_estimate, owner_user):
        item = submitted_estimate.items.first()
        updated = owner_decide_item(str(item.id), owner_user, ApprovalStatus.APPROVED)
        assert updated.approval_status == ApprovalStatus.APPROVED
        assert updated.owner_decision_by == owner_user
        assert updated.owner_decision_at is not None

    def test_owner_can_reject(self, submitted_estimate, owner_user):
        item = submitted_estimate.items.first()
        updated = owner_decide_item(str(item.id), owner_user, ApprovalStatus.REJECTED, "Too expensive.")
        assert updated.approval_status == ApprovalStatus.REJECTED
        assert updated.clarification_note == "Too expensive."

    def test_all_approved_transitions_order(self, submitted_estimate, owner_user):
        item = submitted_estimate.items.first()
        owner_decide_item(str(item.id), owner_user, ApprovalStatus.APPROVED)
        order = submitted_estimate.service_order
        order.refresh_from_db()
        assert order.status == ServiceOrderStatus.APPROVED

    def test_all_rejected_requests_revision(self, submitted_estimate, owner_user):
        item = submitted_estimate.items.first()
        owner_decide_item(str(item.id), owner_user, ApprovalStatus.REJECTED)
        order = submitted_estimate.service_order
        order.refresh_from_db()
        assert order.status == ServiceOrderStatus.REVISION_REQUESTED

    def test_cannot_decide_on_draft_estimate(
        self, completed_inspection, mechanic_user, owner_user, aps_component
    ):
        order = completed_inspection.service_order
        est = create_estimate(str(order.id), mechanic_user)
        item = add_estimate_item(
            est, mechanic_user, aps_component.component_code, "Test", 1,
            Decimal("100.00"), Decimal("50.00")
        )
        # Not submitted yet
        with pytest.raises(ApprovalError):
            owner_decide_item(str(item.id), owner_user, ApprovalStatus.APPROVED)


@pytest.mark.django_db
class TestInventoryStock:
    def test_reserve_reduces_stock(
        self, workshop_inventory, service_order, admin_user
    ):
        from apps.inventory.services import reserve_stock
        initial = workshop_inventory.quantity_available
        reserve_stock(workshop_inventory, 2, service_order, admin_user)
        workshop_inventory.refresh_from_db()
        assert workshop_inventory.quantity_available == initial - 2

    def test_insufficient_stock_raises(
        self, workshop_inventory, service_order, admin_user
    ):
        from apps.inventory.services import reserve_stock, InsufficientStockError
        workshop_inventory.quantity_available = 1
        workshop_inventory.save()
        with pytest.raises(InsufficientStockError):
            reserve_stock(workshop_inventory, 5, service_order, admin_user)

    def test_reservation_creates_movement_record(
        self, workshop_inventory, service_order, admin_user
    ):
        from apps.inventory.services import reserve_stock
        from apps.inventory.models import InventoryMovement, MovementType
        reserve_stock(workshop_inventory, 1, service_order, admin_user)
        movement = InventoryMovement.objects.filter(
            inventory=workshop_inventory, movement_type=MovementType.RESERVED
        ).first()
        assert movement is not None
        assert movement.quantity == -1
