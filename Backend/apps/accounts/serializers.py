"""
VEDA V2 — accounts serializers

Input validation and output representation for all auth endpoints.
All validation happens here — views stay thin.
"""

import re
from rest_framework import serializers
from .models import User, UserRole


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PHONE_RE = re.compile(r"^\+?[1-9]\d{6,14}$")


def validate_phone(value: str) -> str:
    cleaned = value.strip().replace(" ", "").replace("-", "")
    if not PHONE_RE.match(cleaned):
        raise serializers.ValidationError(
            "Enter a valid phone number (e.g. +919876543210)."
        )
    return cleaned


# ---------------------------------------------------------------------------
# Request OTP
# ---------------------------------------------------------------------------

class RequestOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)

    def validate_phone_number(self, value):
        return validate_phone(value)


# ---------------------------------------------------------------------------
# Verify OTP
# ---------------------------------------------------------------------------

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    code         = serializers.CharField(min_length=6, max_length=6)

    def validate_phone_number(self, value):
        return validate_phone(value)

    def validate_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must be a 6-digit number.")
        return value


# ---------------------------------------------------------------------------
# Profile setup (onboarding)
# ---------------------------------------------------------------------------

class ProfileSetupSerializer(serializers.Serializer):
    full_name = serializers.CharField(min_length=2, max_length=150)

    def validate_full_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Full name cannot be blank.")
        return value


# ---------------------------------------------------------------------------
# User output
# ---------------------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model  = User
        fields = ["id", "phone_number", "full_name", "roles", "is_active", "created_at"]
        read_only_fields = fields

    def get_roles(self, obj):
        return obj.get_roles()


# ---------------------------------------------------------------------------
# Token response (used internally by verify_otp view)
# ---------------------------------------------------------------------------

class TokenResponseSerializer(serializers.Serializer):
    access   = serializers.CharField(read_only=True)
    refresh  = serializers.CharField(read_only=True)
    user     = UserSerializer(read_only=True)
