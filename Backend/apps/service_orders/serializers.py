"""VEDA V2 — service_orders serializers"""

from rest_framework import serializers
from .models import ServiceOrder, ServiceOrderEvent, ServiceOrderStatus


class ServiceOrderSerializer(serializers.ModelSerializer):
    vehicle_reg      = serializers.CharField(source="vehicle.registration_number", read_only=True)
    vehicle_make     = serializers.SerializerMethodField()
    centre_name      = serializers.CharField(source="service_centre.name", read_only=True)
    owner_phone      = serializers.CharField(source="owner.phone_number", read_only=True)
    mechanic_phone   = serializers.CharField(
        source="assigned_mechanic.phone_number", read_only=True, allow_null=True
    )
    mechanic_name    = serializers.CharField(
        source="assigned_mechanic.full_name", read_only=True, allow_null=True
    )

    class Meta:
        model  = ServiceOrder
        fields = [
            "id", "vehicle_reg", "vehicle_make", "centre_name",
            "owner_phone", "mechanic_phone", "mechanic_name",
            "status", "service_description", "rejection_reason",
            "received_at", "completed_at", "created_at",
        ]
        read_only_fields = fields

    def get_vehicle_make(self, obj):
        return f"{obj.vehicle.manufacturer} {obj.vehicle.model}"


class ServiceOrderCreateSerializer(serializers.Serializer):
    vehicle_id          = serializers.UUIDField()
    service_centre_id   = serializers.UUIDField()
    service_description = serializers.CharField(min_length=10, max_length=2000)


class TransitionSerializer(serializers.Serializer):
    """Generic transition request — used for accept, reject, receive, etc."""
    status            = serializers.ChoiceField(choices=ServiceOrderStatus.choices)
    notes             = serializers.CharField(required=False, allow_blank=True)
    rejection_reason  = serializers.CharField(required=False, allow_blank=True)
    mechanic_id       = serializers.UUIDField(required=False, allow_null=True)


class AssignMechanicSerializer(serializers.Serializer):
    mechanic_id = serializers.UUIDField()


class ServiceOrderEventSerializer(serializers.ModelSerializer):
    triggered_by_phone = serializers.CharField(
        source="triggered_by.phone_number", read_only=True, allow_null=True
    )

    class Meta:
        model  = ServiceOrderEvent
        fields = ["id", "from_status", "to_status", "triggered_by_phone", "notes", "created_at"]
        read_only_fields = fields
