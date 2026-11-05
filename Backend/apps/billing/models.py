"""
VEDA V2 — billing models

Invoice: generated from a completed work order
Payment: records a payment transaction

RULES:
- All financial values use DecimalField.
- Invoice is generated only after work order is completed and final inspection passed.
- Mock payments are used during local development.
- Never treat frontend success as proof of payment.
- Never store card numbers or sensitive credentials.
- Payment idempotency via transaction_reference uniqueness.
"""

import uuid
from django.db import models
from django.utils import timezone


class InvoiceStatus(models.TextChoices):
    DRAFT   = "DRAFT",   "Draft"
    ISSUED  = "ISSUED",  "Issued"
    PAID    = "PAID",    "Paid"
    VOID    = "VOID",    "Void"


class PaymentStatus(models.TextChoices):
    PENDING   = "PENDING",   "Pending"
    COMPLETED = "COMPLETED", "Completed"
    FAILED    = "FAILED",    "Failed"
    REFUNDED  = "REFUNDED",  "Refunded"


class Invoice(models.Model):
    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_order  = models.OneToOneField(
        "service_orders.ServiceOrder",
        on_delete=models.CASCADE, related_name="invoice"
    )
    invoice_number = models.CharField(max_length=30, unique=True, db_index=True)
    subtotal       = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount     = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount   = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    invoice_status = models.CharField(
        max_length=10, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT
    )
    notes          = models.TextField(blank=True)
    generated_at   = models.DateTimeField(default=timezone.now)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table   = "invoice"
        verbose_name = "Invoice"

    def __str__(self):
        return f"INV-{self.invoice_number} [{self.invoice_status}] {self.total_amount}"


class Payment(models.Model):
    id                    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice               = models.ForeignKey(
        Invoice, on_delete=models.PROTECT, related_name="payments"
    )
    payment_provider      = models.CharField(max_length=30, default="MOCK")
    transaction_reference = models.CharField(
        max_length=100, unique=True,
        help_text="Unique reference from payment provider — used for idempotency"
    )
    payment_status        = models.CharField(
        max_length=15, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    amount                = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at               = models.DateTimeField(null=True, blank=True)
    failure_reason        = models.CharField(max_length=300, blank=True)
    created_at            = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table   = "payment"
        verbose_name = "Payment"

    def __str__(self):
        return f"PAY-{self.transaction_reference} [{self.payment_status}] {self.amount}"
