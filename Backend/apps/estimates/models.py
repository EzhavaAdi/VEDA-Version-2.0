"""
VEDA V2 — estimates models

RepairEstimate: the overall estimate for a service order (versioned)
EstimateItem:   one line item — component, part, labour, qty, owner approval

RULES:
- All financial values use DecimalField.
- Mechanics cannot approve items on behalf of owners.
- Only APPROVED items can enter authorized repair work.
- Owner decisions and timestamps are recorded immutably.
- Estimates support revisions (revision_number increments).
"""

import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class EstimateStatus(models.TextChoices):
    DRAFT     = "DRAFT",     "Draft"
    SUBMITTED = "SUBMITTED", "Submitted to Owner"
    REVISED   = "REVISED",   "Revision Requested"
    ACCEPTED  = "ACCEPTED",  "Accepted"
    REJECTED  = "REJECTED",  "Rejected"


class ApprovalStatus(models.TextChoices):
    PENDING               = "PENDING",               "Pending"
    APPROVED              = "APPROVED",              "Approved"
    REJECTED              = "REJECTED",              "Rejected"
    CLARIFICATION_REQUESTED = "CLARIFICATION_REQUESTED", "Clarification Requested"


class RepairEstimate(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_order   = models.ForeignKey(
        "service_orders.ServiceOrder",
        on_delete=models.CASCADE, related_name="estimates"
    )
    revision_number = models.PositiveSmallIntegerField(default=1)
    labour_total    = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    parts_total     = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total     = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estimate_status = models.CharField(
        max_length=15, choices=EstimateStatus.choices, default=EstimateStatus.DRAFT
    )
    notes           = models.TextField(blank=True)
    created_by      = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at      = models.DateTimeField(default=timezone.now)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table        = "repair_estimate"
        unique_together = [("service_order", "revision_number")]
        ordering        = ["-revision_number"]
        verbose_name    = "Repair Estimate"

    def __str__(self):
        return f"Estimate #{self.revision_number} for {self.service_order_id} [{self.estimate_status}]"

    def recalculate_totals(self):
        """Recompute totals from active line items and save."""
        from decimal import Decimal
        items = self.items.all()
        self.labour_total = sum(i.labour_cost for i in items)
        self.parts_total  = sum(i.unit_price * i.quantity for i in items)
        self.grand_total  = self.labour_total + self.parts_total
        self.save(update_fields=["labour_total", "parts_total", "grand_total", "updated_at"])


class EstimateItem(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estimate    = models.ForeignKey(
        RepairEstimate, on_delete=models.CASCADE, related_name="items"
    )
    component   = models.ForeignKey(
        "components.Component", on_delete=models.PROTECT, related_name="estimate_items"
    )
    part        = models.ForeignKey(
        "inventory.PartCatalog",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="estimate_items"
    )
    description     = models.CharField(max_length=500)
    quantity        = models.PositiveSmallIntegerField(default=1)
    unit_price      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    labour_cost     = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    approval_status = models.CharField(
        max_length=25, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING
    )
    # Owner decision audit
    owner_decision_at  = models.DateTimeField(null=True, blank=True)
    owner_decision_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="estimate_decisions"
    )
    clarification_note = models.TextField(blank=True)
    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "estimate_item"
        ordering = ["component__vehicle_system", "description"]
        verbose_name = "Estimate Item"

    def __str__(self):
        return f"{self.component.component_code} — {self.description} [{self.approval_status}]"

    @property
    def line_total(self):
        return self.unit_price * self.quantity + self.labour_cost
