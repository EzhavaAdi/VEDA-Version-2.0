"""VEDA V2 — service_orders admin"""
from django.contrib import admin
from .models import ServiceOrder, ServiceOrderEvent

@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display  = ["id", "vehicle", "service_centre", "status", "assigned_mechanic", "created_at"]
    list_filter   = ["status"]
    search_fields = ["vehicle__registration_number", "owner__phone_number"]
    readonly_fields = ["id", "created_at", "updated_at"]

@admin.register(ServiceOrderEvent)
class ServiceOrderEventAdmin(admin.ModelAdmin):
    list_display  = ["service_order", "from_status", "to_status", "triggered_by", "created_at"]
    readonly_fields = ["id", "created_at"]
