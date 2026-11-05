"""VEDA V2 — components admin"""

from django.contrib import admin
from .models import Component, VehicleComponent


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display  = ["component_code", "component_name", "vehicle_system", "parent", "status"]
    list_filter   = ["vehicle_system", "status"]
    search_fields = ["component_name", "component_code"]
    readonly_fields = ["id", "created_at"]
    raw_id_fields = ["parent"]


@admin.register(VehicleComponent)
class VehicleComponentAdmin(admin.ModelAdmin):
    list_display  = ["vehicle", "component", "current_status", "last_updated"]
    list_filter   = ["current_status"]
    search_fields = ["vehicle__registration_number", "component__component_name"]
    readonly_fields = ["id", "last_updated"]
