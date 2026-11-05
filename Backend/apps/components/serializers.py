"""VEDA V2 — components serializers"""

from rest_framework import serializers
from .models import Component, VehicleComponent


class ComponentSerializer(serializers.ModelSerializer):
    parent_code = serializers.CharField(
        source="parent.component_code", read_only=True, allow_null=True
    )
    parent_name = serializers.CharField(
        source="parent.component_name", read_only=True, allow_null=True
    )

    class Meta:
        model  = Component
        fields = [
            "id", "component_name", "component_code",
            "vehicle_system", "parent_code", "parent_name",
            "description", "maintenance_info", "status",
        ]
        read_only_fields = fields


class ComponentTreeSerializer(serializers.ModelSerializer):
    """Serializer that includes direct children (one level deep)."""
    children = serializers.SerializerMethodField()

    class Meta:
        model  = Component
        fields = [
            "id", "component_name", "component_code",
            "vehicle_system", "description", "children",
        ]

    def get_children(self, obj):
        return ComponentTreeSerializer(
            obj.children.filter(status="ACTIVE"), many=True
        ).data


class VehicleComponentSerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(source="component.component_name", read_only=True)
    component_code = serializers.CharField(source="component.component_code", read_only=True)
    vehicle_system = serializers.CharField(source="component.vehicle_system", read_only=True)

    class Meta:
        model  = VehicleComponent
        fields = [
            "id", "component_name", "component_code", "vehicle_system",
            "current_status", "installation_date", "notes", "last_updated",
        ]
        read_only_fields = ["id", "component_name", "component_code", "vehicle_system", "last_updated"]


class VehicleComponentCreateSerializer(serializers.Serializer):
    component_code    = serializers.CharField(max_length=50)
    installation_date = serializers.DateField(required=False, allow_null=True)
    notes             = serializers.CharField(required=False, allow_blank=True)
