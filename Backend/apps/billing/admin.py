"""VEDA V2 — billing admin"""
from django.contrib import admin
from .models import Invoice, Payment

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display  = ["invoice_number", "service_order", "total_amount", "invoice_status", "generated_at"]
    list_filter   = ["invoice_status"]
    readonly_fields = ["id", "generated_at", "updated_at"]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ["transaction_reference", "invoice", "amount", "payment_status", "paid_at"]
    list_filter   = ["payment_status", "payment_provider"]
    readonly_fields = ["id", "created_at"]
