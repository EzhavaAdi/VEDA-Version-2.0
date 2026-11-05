"""
VEDA V2 — work_orders models

WorkOrder:     one work order per service order (created from approved estimate items)
WorkOrderItem: one item per approved EstimateItem — tracks completion

RULES:
- Work orders can only be created from APPROVED estimate items.
- Mechanics update item completion; service centre does final inspection.
- The service order transitions through REPAIR_IN_PROGRESS -> FINAL_INSPECTION.
"""

import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class WorkStatus(models.TextChoices):
    PENDING     = "PENDING",     "Pending"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED   = "COMPLETED",   "Completed"
    ON_HOLD     = "ON_HOLD",     "On Hold"


class ItemCompletionStatus(models.TextChoices):
    PENDING   = "PENDING",   "Pending"
    STARTED   = "STARTED",   "Started"
    COMPLETED = "COMPLETED", "Completed"
    SKIPPED   = "SKIPPED",   "Skipped"


class WorkOrder(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_order = models.OneToOneField(
        "service_orders.ServiceOrder",
        on_delete=models.CASCADE, related_name="work_order"
    )
    work_status   = models.CharField(
        max_length=15, choices=WorkStatus.choices, default=WorkStatus.PENDING
    )
    started_at    = models.DateTimeField(null=True, blank=True)
    completed_at  = models.DateTimeField(null=True, blank=True)
    created_by    = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at    = models.DateTimeField(default=timezone.now)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table   = "work_order"
        verbose_name = "Work Order"

    def __str__(self):
        return f"WO-{str(self.id)[:8]} [{self.work_status}]"


class WorkOrderItem(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_order    = models.ForeignKey(
        WorkOrder, on_delete=models.CASCADE, related_name="items"
    )
    estimate_item = models.OneToOneField(
        "estimates.EstimateItem",
        on_delete=models.PROTECT, related_name="work_order_item"
    )
    completion_status = models.CharField(
        max_length=15, choices=ItemCompletionStatus.choices,
        default=ItemCompletionStatus.PENDING
    )
    mechanic_notes = models.TextField(blank=True)
    completed_at   = models.DateTimeField(null=True, blank=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "work_order_item"
        verbose_name = "Work Order Item"

    def __str__(self):
        return f"{self.estimate_item.component.component_code} [{self.completion_status}]"
