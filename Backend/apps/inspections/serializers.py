"""VEDA V2 — inspections serializers"""

from rest_framework import serializers
from .models import Inspection, InspectionItem, SensorReading, Severity


class SensorReadingSerializer(serializers.ModelSerializer):
    component_code = serializers.CharField(
        source="component.component_code", read_only=True, allow_null=True
    )

    class Meta:
        model  = SensorReading
        fields = [
            "id", "parameter_name", "parameter_value",
            "unit", "component_code", "notes", "recorded_at",
        ]
        read_only_fields = ["id", "recorded_at"]


class SensorReadingCreateSerializer(serializers.Serializer):
    parameter_name  = serializers.CharField(max_length=100)
    parameter_value = serializers.DecimalField(max_digits=12, decimal_places=4)
    unit            = serializers.CharField(max_length=30, required=False, allow_blank=True)
    component_code  = serializers.CharField(required=False, allow_blank=True)
    notes           = serializers.CharField(required=False, allow_blank=True)


class InspectionItemSerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(source="component.component_name", read_only=True)
    component_code = serializers.CharField(source="component.component_code", read_only=True)
    vehicle_system = serializers.CharField(source="component.vehicle_system", read_only=True)

    class Meta:
        model  = InspectionItem
        fields = [
            "id", "component_name", "component_code", "vehicle_system",
            "observed_condition", "severity", "mechanic_notes", "updated_at",
        ]
        read_only_fields = ["id", "component_name", "component_code", "vehicle_system", "updated_at"]


class InspectionItemCreateSerializer(serializers.Serializer):
    component_code     = serializers.CharField(max_length=50)
    observed_condition = serializers.CharField(min_length=3, max_length=2000)
    severity           = serializers.ChoiceField(choices=Severity.choices)
    mechanic_notes     = serializers.CharField(required=False, allow_blank=True)


class InspectionSerializer(serializers.ModelSerializer):
    mechanic_phone = serializers.CharField(source="mechanic.phone_number", read_only=True)
    mechanic_name  = serializers.CharField(source="mechanic.full_name", read_only=True)
    items          = InspectionItemSerializer(many=True, read_only=True)
    sensor_readings = SensorReadingSerializer(many=True, read_only=True)

    class Meta:
        model  = Inspection
        fields = [
            "id", "mechanic_phone", "mechanic_name",
            "inspection_date", "inspection_status",
            "general_observations",
            "items", "sensor_readings",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "mechanic_phone", "mechanic_name",
                            "inspection_date", "created_at", "updated_at"]


class InspectionUpdateSerializer(serializers.Serializer):
    general_observations = serializers.CharField(required=False, allow_blank=True)
