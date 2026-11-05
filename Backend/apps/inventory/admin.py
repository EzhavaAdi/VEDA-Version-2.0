"""VEDA V2 — inventory admin"""
from django.contrib import admin
from .models import PartCatalog, PartCompatibility, WorkshopInventory, InventoryMovement

@admin.register(PartCatalog)
class PartCatalogAdmin(admin.ModelAdmin):
    list_display  = ["part_number", "part_name", "manufacturer", "is_active"]
    search_fields = ["part_name", "part_number"]
    readonly_fields = ["id", "created_at"]

@admin.register(PartCompatibility)
class PartCompatibilityAdmin(admin.ModelAdmin):
    list_display  = ["part", "component", "verification_status"]
    list_filter   = ["verification_status"]
    readonly_fields = ["id"]

@admin.register(WorkshopInventory)
class WorkshopInventoryAdmin(admin.ModelAdmin):
    list_display  = ["service_centre", "part", "quantity_available", "unit_price", "updated_at"]
    readonly_fields = ["id"]

@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display  = ["inventory", "movement_type", "quantity", "created_at"]
    list_filter   = ["movement_type"]
    readonly_fields = ["id", "created_at"]
