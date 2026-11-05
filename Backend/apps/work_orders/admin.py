"""VEDA V2 — work_orders admin"""
from django.contrib import admin
from .models import WorkOrder, WorkOrderItem

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display  = ["id", "service_order", "work_status", "started_at", "completed_at"]
    list_filter   = ["work_status"]
    readonly_fields = ["id", "created_at", "updated_at"]

@admin.register(WorkOrderItem)
class WorkOrderItemAdmin(admin.ModelAdmin):
    list_display  = ["work_order", "estimate_item", "completion_status", "completed_at"]
    list_filter   = ["completion_status"]
    readonly_fields = ["id", "updated_at"]
