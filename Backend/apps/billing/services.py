"""
VEDA V2 — billing service layer

generate_invoice()   — creates Invoice from completed work order items
process_payment()    — MOCK provider only in local development
complete_delivery()  — final state: VEHICLE_DELIVERED

RULES:
- Never treat frontend payment success as verified payment.
- Never store card information.
- Use idempotent transaction references.
- MOCK provider returns success immediately — replace in production.
- Invoice is generated only after FINAL_INSPECTION status.
"""

import logging
import secrets
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.conf import settings

from apps.accounts.models import User
from apps.organizations.models import WorkshopMembership
from apps.service_orders.models import ServiceOrder, ServiceOrderStatus
from apps.service_orders.services import transition_order
from .models import Invoice, Payment, InvoiceStatus, PaymentStatus

logger = logging.getLogger("veda.billing")


class BillingError(Exception):
    pass

class NotFoundError(BillingError):
    pass

class PermissionError(BillingError):
    pass

class PaymentError(BillingError):
    pass


# ---------------------------------------------------------------------------
# Invoice number generation
# ---------------------------------------------------------------------------

def _next_invoice_number() -> str:
    from django.utils import timezone
    prefix = f"INV-{timezone.now().strftime('%Y%m')}"
    last = (
        Invoice.objects
        .filter(invoice_number__startswith=prefix)
        .order_by("-invoice_number")
        .first()
    )
    if last:
        try:
            seq = int(last.invoice_number.split("-")[-1]) + 1
        except (ValueError, IndexError):
            seq = 1
    else:
        seq = 1
    return f"{prefix}-{seq:04d}"


# ---------------------------------------------------------------------------
# Generate invoice
# ---------------------------------------------------------------------------

@transaction.atomic
def generate_invoice(order_id: str, created_by: User) -> Invoice:
    try:
        order = ServiceOrder.objects.select_related("service_centre").get(id=order_id)
    except ServiceOrder.DoesNotExist:
        raise NotFoundError("Service order not found.")

    if not WorkshopMembership.objects.filter(
        user=created_by, service_centre=order.service_centre, is_active=True
    ).exists():
        raise PermissionError("Only workshop members can generate invoices.")

    if order.status != ServiceOrderStatus.FINAL_INSPECTION:
        raise BillingError(
            f"Invoice can only be generated after FINAL_INSPECTION. "
            f"Current status: {order.status}"
        )

    if hasattr(order, "invoice"):
        raise BillingError("An invoice already exists for this service order.")

    # Sum approved work order items
    try:
        wo = order.work_order
    except Exception:
        raise BillingError("No work order found for this service order.")

    subtotal = Decimal("0.00")
    for item in wo.items.select_related(
        "estimate_item__component", "estimate_item__part"
    ).all():
        ei = item.estimate_item
        subtotal += ei.unit_price * ei.quantity + ei.labour_cost

    # Tax rate from settings (default 0 for local dev)
    tax_rate = Decimal(str(getattr(settings, "TAX_RATE_PERCENT", "0"))) / Decimal("100")
    tax_amount   = (subtotal * tax_rate).quantize(Decimal("0.01"))
    total_amount = subtotal + tax_amount

    invoice = Invoice.objects.create(
        service_order=order,
        invoice_number=_next_invoice_number(),
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        invoice_status=InvoiceStatus.ISSUED,
    )

    transition_order(order, ServiceOrderStatus.INVOICED, created_by,
                     f"Invoice {invoice.invoice_number} generated. Total: {total_amount}")

    logger.info(f"Invoice {invoice.invoice_number} generated for order {order_id}")
    return invoice


# ---------------------------------------------------------------------------
# Process payment (MOCK)
# ---------------------------------------------------------------------------

@transaction.atomic
def process_payment(invoice_id: str, owner: User,
                    transaction_reference: str = None) -> Payment:
    """
    Process payment against an invoice.

    In local development: MOCK provider — always succeeds.
    In production: verify the callback/webhook from the real payment provider
    before marking as COMPLETED. Never trust frontend success messages.
    """
    try:
        invoice = Invoice.objects.select_related(
            "service_order__owner", "service_order__service_centre"
        ).get(id=invoice_id)
    except Invoice.DoesNotExist:
        raise NotFoundError("Invoice not found.")

    if invoice.service_order.owner_id != owner.id:
        raise PermissionError("Only the vehicle owner can make payments.")

    if invoice.invoice_status == InvoiceStatus.PAID:
        # If already paid, check idempotency — same reference returns existing record
        if transaction_reference:
            existing = Payment.objects.filter(
                invoice=invoice,
                transaction_reference=transaction_reference
            ).first()
            if existing:
                return existing
        raise PaymentError("This invoice has already been paid.")

    if invoice.invoice_status == InvoiceStatus.VOID:
        raise PaymentError("Cannot pay a void invoice.")

    provider = getattr(settings, "PAYMENT_PROVIDER", "MOCK")

    # Generate idempotent reference if not provided
    if not transaction_reference:
        transaction_reference = f"MOCK-{secrets.token_hex(8).upper()}"

    # Idempotency check — prevent duplicate payments
    if Payment.objects.filter(transaction_reference=transaction_reference).exists():
        return Payment.objects.get(transaction_reference=transaction_reference)

    payment = Payment.objects.create(
        invoice=invoice,
        payment_provider=provider,
        transaction_reference=transaction_reference,
        amount=invoice.total_amount,
        payment_status=PaymentStatus.PENDING,
    )

    if provider == "MOCK":
        # Mock: immediately complete
        payment.payment_status = PaymentStatus.COMPLETED
        payment.paid_at        = timezone.now()
        payment.save(update_fields=["payment_status", "paid_at"])

        invoice.invoice_status = InvoiceStatus.PAID
        invoice.save(update_fields=["invoice_status", "updated_at"])

        order = invoice.service_order
        # INVOICED -> PAYMENT_PENDING -> PAID (state machine requires both steps)
        if order.can_transition_to(ServiceOrderStatus.PAYMENT_PENDING):
            transition_order(order, ServiceOrderStatus.PAYMENT_PENDING, owner,
                             f"Payment initiated via MOCK provider.")
        transition_order(order, ServiceOrderStatus.PAID, owner,
                         f"Payment {transaction_reference} completed via MOCK provider.")

        logger.info(f"MOCK payment {transaction_reference} completed for invoice {invoice.invoice_number}")
    else:
        # Production: payment is PENDING — webhook will confirm
        logger.info(f"Payment {transaction_reference} initiated via {provider}")

    return payment


# ---------------------------------------------------------------------------
# Deliver vehicle
# ---------------------------------------------------------------------------

@transaction.atomic
def deliver_vehicle(order_id: str, admin: User) -> ServiceOrder:
    try:
        order = ServiceOrder.objects.select_related("service_centre").get(id=order_id)
    except ServiceOrder.DoesNotExist:
        raise NotFoundError("Service order not found.")

    if not WorkshopMembership.objects.filter(
        user=admin, service_centre=order.service_centre, is_active=True
    ).exists():
        raise PermissionError("Only workshop members can mark vehicle as delivered.")

    if order.status != ServiceOrderStatus.PAID:
        raise BillingError(
            f"Vehicle can only be delivered after payment. Current status: {order.status}"
        )

    transition_order(order, ServiceOrderStatus.VEHICLE_DELIVERED, admin,
                     "Vehicle returned to owner. Service complete.")
    logger.info(f"Vehicle delivered for order {order_id}")
    return order


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------

def get_invoice(order_id: str, user: User) -> Invoice:
    try:
        order = ServiceOrder.objects.get(id=order_id)
    except ServiceOrder.DoesNotExist:
        raise NotFoundError("Service order not found.")

    is_owner  = order.owner_id == user.id
    is_member = WorkshopMembership.objects.filter(
        user=user, service_centre=order.service_centre, is_active=True
    ).exists()
    if not (is_owner or is_member):
        raise PermissionError("Access denied.")

    try:
        return Invoice.objects.prefetch_related("payments").get(service_order=order)
    except Invoice.DoesNotExist:
        raise NotFoundError("No invoice found for this service order.")
