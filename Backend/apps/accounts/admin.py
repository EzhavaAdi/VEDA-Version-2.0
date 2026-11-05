"""
VEDA V2 — accounts Django admin registration
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import OTP, Role, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ["phone_number", "full_name", "is_active", "is_staff", "created_at"]
    list_filter   = ["is_active", "is_staff"]
    search_fields = ["phone_number", "full_name"]
    ordering      = ["-created_at"]
    readonly_fields = ["id", "created_at", "updated_at"]

    fieldsets = (
        (None, {"fields": ("id", "phone_number", "password")}),
        ("Personal", {"fields": ("full_name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "full_name", "password1", "password2", "is_staff", "is_active"),
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display  = ["user", "role", "assigned_at"]
    list_filter   = ["role"]
    search_fields = ["user__phone_number", "user__full_name"]
    readonly_fields = ["id", "assigned_at"]


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display  = ["user", "is_used", "attempt_count", "expires_at", "created_at"]
    list_filter   = ["is_used"]
    search_fields = ["user__phone_number"]
    readonly_fields = ["id", "code_hash", "created_at"]
    # Never expose raw codes — only hashes are stored
