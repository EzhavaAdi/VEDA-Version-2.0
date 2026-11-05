"""VEDA V2 — organizations serializers"""

from rest_framework import serializers
from .models import ServiceCentre, WorkshopMembership, VerificationStatus


class ServiceCentreSerializer(serializers.ModelSerializer):
    registered_by_phone = serializers.CharField(
        source="registered_by.phone_number", read_only=True
    )

    class Meta:
        model  = ServiceCentre
        fields = [
            "id", "name", "address", "city", "state",
            "contact_number", "email",
            "verification_status", "is_active",
            "registered_by_phone", "created_at",
        ]
        read_only_fields = ["id", "verification_status", "registered_by_phone", "created_at"]


class ServiceCentreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ServiceCentre
        fields = ["name", "address", "city", "state", "contact_number", "email"]

    def validate_contact_number(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Contact number is required.")
        return value


class WorkshopMembershipSerializer(serializers.ModelSerializer):
    user_phone  = serializers.CharField(source="user.phone_number", read_only=True)
    user_name   = serializers.CharField(source="user.full_name", read_only=True)
    centre_name = serializers.CharField(source="service_centre.name", read_only=True)

    class Meta:
        model  = WorkshopMembership
        fields = [
            "id", "user_phone", "user_name",
            "centre_name", "designation", "is_active", "joined_at",
        ]
        read_only_fields = fields


class AddMemberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    designation  = serializers.ChoiceField(choices=["ADMIN", "MECHANIC", "STAFF"])
