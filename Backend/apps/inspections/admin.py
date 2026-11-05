"""VEDA V2 — inspections admin"""
from django.contrib import admin
from .models import Inspection, InspectionItem, SensorReading

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display  = ["service_order", "mechanic", "inspection_status", "inspection_date"]
    list_filter   = ["inspection_status"]
    readonly_fields = ["id", "created_at", "updated_at"]

@admin.register(InspectionItem)
class InspectionItemAdmin(admin.ModelAdmin):
    list_display  = ["inspection", "component", "severity"]
    list_filter   = ["severity"]
    readonly_fields = ["id"]

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display  = ["inspection", "parameter_name", "parameter_value", "unit", "recorded_at"]
    readonly_fields = ["id", "recorded_at"]
