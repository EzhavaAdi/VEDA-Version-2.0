"""VEDA V2 — estimates admin"""
from django.contrib import admin
from .models import RepairEstimate, EstimateItem

@admin.register(RepairEstimate)
class RepairEstimateAdmin(admin.ModelAdmin):
    list_display  = ["id", "service_order", "revision_number", "estimate_status", "grand_total", "created_at"]
    list_filter   = ["estimate_status"]
    readonly_fields = ["id", "created_at", "updated_at"]

@admin.register(EstimateItem)
class EstimateItemAdmin(admin.ModelAdmin):
    list_display  = ["estimate", "component", "description", "quantity", "unit_price", "labour_cost", "approval_status"]
    list_filter   = ["approval_status"]
    readonly_fields = ["id", "created_at", "updated_at"]
