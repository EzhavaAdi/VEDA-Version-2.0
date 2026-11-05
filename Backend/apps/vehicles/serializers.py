"""VEDA V2 — vehicles serializers"""

from rest_framework import serializers
from .models import Vehicle, VehicleDocument, VehicleCategory
from django.utils import timezone


class VehicleSerializer(serializers.ModelSerializer):
    owner_phone = serializers.CharField(source="owner.phone_number", read_only=True)

    class Meta:
        model  = Vehicle
        fields = [
            "id", "owner_phone", "registration_number",
            "manufacturer", "model", "vehicle_category",
            "manufacturing_year", "vin",
            "odometer_reading", "operating_hours",
            "is_active", "notes", "created_at",
        ]
        read_only_fields = ["id", "owner_phone", "created_at"]


class VehicleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Vehicle
        fields = [
            "registration_number", "manufacturer", "model",
            "vehicle_category", "manufacturing_year", "vin",
            "odometer_reading", "operating_hours", "notes",
        ]

    def validate_manufacturing_year(self, value):
        current_year = timezone.now().year
        if value < 1950 or value > current_year + 1:
            raise serializers.ValidationError(
                f"Manufacturing year must be between 1950 and {current_year + 1}."
            )
        return value

    def validate_registration_number(self, value):
        return value.strip().upper()


class VehicleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Vehicle
        fields = ["odometer_reading", "operating_hours", "notes", "vin"]


class VehicleDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = VehicleDocument
        fields = ["id", "document_type", "file", "description", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]
