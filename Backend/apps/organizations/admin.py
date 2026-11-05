"""VEDA V2 — organizations admin"""

from django.contrib import admin
from .models import ServiceCentre, WorkshopMembership


@admin.register(ServiceCentre)
class ServiceCentreAdmin(admin.ModelAdmin):
    list_display  = ["name", "city", "contact_number", "verification_status", "is_active", "created_at"]
    list_filter   = ["verification_status", "is_active"]
    search_fields = ["name", "city", "contact_number"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(WorkshopMembership)
class WorkshopMembershipAdmin(admin.ModelAdmin):
    list_display  = ["user", "service_centre", "designation", "is_active", "joined_at"]
    list_filter   = ["designation", "is_active"]
    search_fields = ["user__phone_number", "service_centre__name"]
    readonly_fields = ["id", "joined_at"]
