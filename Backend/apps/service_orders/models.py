"""
VEDA V2 — service_orders models

ServiceOrder: the central workflow record connecting owner, vehicle,
service centre, and mechanic through a validated state machine.

All state transitions are enforced by the service layer — never set
status directly outside of the transition methods.
"""

import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class ServiceOrderStatus(models.TextChoices):
    REQUESTED              = "REQUESTED",              "Service Requested"
    ACCEPTED               = "ACCEPTED",               "Accepted by Centre"
    REJECTED               = "REJECTED",               "Rejected by Centre"
    VEHICLE_RECEIVED       = "VEHICLE_RECEIVED",       "Vehicle Received"
    INSPECTION_IN_PROGRESS = "INSPECTION_IN_PROGRESS", "Inspection In Progress"
    AI_DIAGNOSIS           = "AI_DIAGNOSIS",           "AI Diagnosis Running"
    ESTIMATE_READY         = "ESTIMATE_READY",         "Estimate Ready"
    AWAITING_APPROVAL      = "AWAITING_APPROVAL",      "Awaiting Owner Approval"
    APPROVED               = "APPROVED",               "Approved"
    PARTIALLY_APPROVED     = "PARTIALLY_APPROVED",     "Partially Approved"
    REPAIR_IN_PROGRESS     = "REPAIR_IN_PROGRESS",     "Repair In Progress"
    FINAL_INSPECTION       = "FINAL_INSPECTION",       "Final Inspection"
    INVOICED               = "INVOICED",               "Invoiced"
    PAYMENT_PENDING        = "PAYMENT_PENDING",        "Payment Pending"
    PAID                   = "PAID",                   "Paid"
    VEHICLE_DELIVERED      = "VEHICLE_DELIVERED",      "Vehicle Delivered"
    CANCELLED              = "CANCELLED",              "Cancelled"
    ON_HOLD                = "ON_HOLD",                "On Hold"
    REVISION_REQUESTED     = "REVISION_REQUESTED",     "Revision Requested"


# ---------------------------------------------------------------------------
# Allowed transitions — backend enforces these, frontend cannot bypass
# ---------------------------------------------------------------------------
ALLOWED_TRANSITIONS: dict[str, list[str]] = {
    ServiceOrderStatus.REQUESTED: [
        ServiceOrderStatus.ACCEPTED,
        ServiceOrderStatus.REJECTED,
        ServiceOrderStatus.CANCELLED,
    ],
    ServiceOrderStatus.ACCEPTED: [
        ServiceOrderStatus.VEHICLE_RECEIVED,
        ServiceOrderStatus.CANCELLED,
        ServiceOrderStatus.ON_HOLD,
    ],
    ServiceOrderStatus.VEHICLE_RECEIVED: [
        ServiceOrderStatus.INSPECTION_IN_PROGRESS,
        ServiceOrderStatus.ON_HOLD,
    ],
    ServiceOrderStatus.INSPECTION_IN_PROGRESS: [
        ServiceOrderStatus.AI_DIAGNOSIS,
        ServiceOrderStatus.ESTIMATE_READY,   # Skip AI if not applicable
        ServiceOrderStatus.ON_HOLD,
    ],
    ServiceOrderStatus.AI_DIAGNOSIS: [
        ServiceOrderStatus.ESTIMATE_READY,
        ServiceOrderStatus.ON_HOLD,
    ],
    ServiceOrderStatus.ESTIMATE_READY: [
        ServiceOrderStatus.AWAITING_APPROVAL,
        ServiceOrderStatus.REVISION_REQUESTED,
    ],
    ServiceOrderStatus.AWAITING_APPROVAL: [
        ServiceOrderStatus.APPROVED,
        ServiceOrderStatus.PARTIALLY_APPROVED,
        ServiceOrderStatus.REVISION_REQUESTED,
        ServiceOrderStatus.CANCELLED,
    ],
    ServiceOrderStatus.APPROVED: [
        ServiceOrderStatus.REPAIR_IN_PROGRESS,
    ],
    ServiceOrderStatus.PARTIALLY_APPROVED: [
        ServiceOrderStatus.REPAIR_IN_PROGRESS,
    ],
    ServiceOrderStatus.REPAIR_IN_PROGRESS: [
        ServiceOrderStatus.FINAL_INSPECTION,
        ServiceOrderStatus.ON_HOLD,
    ],
    ServiceOrderStatus.FINAL_INSPECTION: [
        ServiceOrderStatus.INVOICED,
    ],
    ServiceOrderStatus.INVOICED: [
        ServiceOrderStatus.PAYMENT_PENDING,
    ],
    ServiceOrderStatus.PAYMENT_PENDING: [
        ServiceOrderStatus.PAID,
    ],
    ServiceOrderStatus.PAID: [
        ServiceOrderStatus.VEHICLE_DELIVERED,
    ],
    ServiceOrderStatus.ON_HOLD: [
        ServiceOrderStatus.INSPECTION_IN_PROGRESS,
        ServiceOrderStatus.REPAIR_IN_PROGRESS,
        ServiceOrderStatus.CANCELLED,
    ],
    ServiceOrderStatus.REVISION_REQUESTED: [
        ServiceOrderStatus.ESTIMATE_READY,
        ServiceOrderStatus.CANCELLED,
    ],
    # Terminal states — no further transitions
    ServiceOrderStatus.VEHICLE_DELIVERED: [],
    ServiceOrderStatus.REJECTED: [],
    ServiceOrderStatus.CANCELLED: [],
}


class ServiceOrder(models.Model):
    """
    Central workflow record.
    State transitions are validated against ALLOWED_TRANSITIONS.
    """

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle         = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.PROTECT,
        related_name="service_orders",
    )
    service_centre  = models.ForeignKey(
        "organizations.ServiceCentre",
        on_delete=models.PROTECT,
        related_name="service_orders",
    )
    owner           = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="service_orders_as_owner",
    )
    assigned_mechanic = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_orders_as_mechanic",
    )
    status              = models.CharField(
        max_length=30,
        choices=ServiceOrderStatus.choices,
        default=ServiceOrderStatus.REQUESTED,
        db_index=True,
    )
    service_description = models.TextField(help_text="Owner's description of the issue")
    rejection_reason    = models.TextField(blank=True)
    received_at         = models.DateTimeField(null=True, blank=True)
    completed_at        = models.DateTimeField(null=True, blank=True)
    created_at          = models.DateTimeField(default=timezone.now)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table  = "service_order"
        ordering  = ["-created_at"]
        verbose_name = "Service Order"

    def __str__(self):
        return f"SO-{str(self.id)[:8]} | {self.vehicle.registration_number} | {self.status}"

    def can_transition_to(self, new_status: str) -> bool:
        return new_status in ALLOWED_TRANSITIONS.get(self.status, [])


class ServiceOrderEvent(models.Model):
    """Immutable audit log of every status transition on a service order."""

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_order = models.ForeignKey(
        ServiceOrder,
        on_delete=models.CASCADE,
        related_name="events",
    )
    from_status  = models.CharField(max_length=30)
    to_status    = models.CharField(max_length=30)
    triggered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    notes        = models.TextField(blank=True)
    created_at   = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "service_order_event"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.from_status} → {self.to_status} by {self.triggered_by}"
