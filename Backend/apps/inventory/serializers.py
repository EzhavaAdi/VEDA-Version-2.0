"""VEDA V2 — inventory serializers"""
from rest_framework import serializers
from .models import PartCatalog, PartCompatibility, WorkshopInventory


class PartCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PartCatalog
        fields = ["id", "part_name", "part_number", "manufacturer", "description"]
        read_only_fields = fields


class PartCompatibilitySerializer(serializers.ModelSerializer):
    part_name   = serializers.CharField(source="part.part_name",   read_only=True)
    part_number = serializers.CharField(source="part.part_number", read_only=True)

    class Meta:
        model  = PartCompatibility
        fields = [
            "id", "part_name", "part_number",
            "vehicle_manufacturer", "compatible_model",
            "compatibility_source", "verification_status",
        ]
        read_only_fields = fields


class WorkshopInventorySerializer(serializers.ModelSerializer):
    part_name   = serializers.CharField(source="part.part_name",   read_only=True)
    part_number = serializers.CharField(source="part.part_number", read_only=True)

    class Meta:
        model  = WorkshopInventory
        fields = ["id", "part_name", "part_number", "quantity_available", "unit_price", "updated_at"]
        read_only_fields = fields


class AddStockSerializer(serializers.Serializer):
    part_id    = serializers.UUIDField()
    quantity   = serializers.IntegerField(min_value=0)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)
