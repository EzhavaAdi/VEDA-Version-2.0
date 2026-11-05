"""VEDA V2 — billing serializers"""
from rest_framework import serializers
from .models import Invoice, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Payment
        fields = ["id", "payment_provider", "transaction_reference",
                  "payment_status", "amount", "paid_at", "created_at"]
        read_only_fields = fields


class InvoiceSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model  = Invoice
        fields = ["id", "invoice_number", "subtotal", "tax_amount", "total_amount",
                  "invoice_status", "notes", "generated_at", "payments"]
        read_only_fields = fields


class ProcessPaymentSerializer(serializers.Serializer):
    transaction_reference = serializers.CharField(
        required=False, allow_blank=True,
        help_text="Optional — a unique reference from the payment provider. Auto-generated for MOCK."
    )
