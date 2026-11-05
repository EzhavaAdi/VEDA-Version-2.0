"""VEDA V2 — vehicles admin"""

from django.contrib import admin
from .models import Vehicle, VehicleDocument


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display  = ["registration_number", "manufacturer", "model", "owner", "vehicle_category", "is_active", "created_at"]
    list_filter   = ["vehicle_category", "is_active", "manufacturing_year"]
    search_fields = ["registration_number", "manufacturer", "model", "owner__phone_number"]
    readonly_fields = ["id", "created_at", "updated_at"]
    raw_id_fields = ["owner"]


@admin.register(VehicleDocument)
class VehicleDocumentAdmin(admin.ModelAdmin):
    list_display  = ["vehicle", "document_type", "uploaded_at"]
    list_filter   = ["document_type"]
