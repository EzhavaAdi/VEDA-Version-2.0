"""VEDA V2 — work_orders serializers"""
from rest_framework import serializers
from .models import WorkOrder, WorkOrderItem, ItemCompletionStatus


class WorkOrderItemSerializer(serializers.ModelSerializer):
    component_code = serializers.CharField(
        source="estimate_item.component.component_code", read_only=True)
    component_name = serializers.CharField(
        source="estimate_item.component.component_name", read_only=True)
    description    = serializers.CharField(
        source="estimate_item.description", read_only=True)
    unit_price     = serializers.DecimalField(
        source="estimate_item.unit_price", max_digits=12, decimal_places=2, read_only=True)
    labour_cost    = serializers.DecimalField(
        source="estimate_item.labour_cost", max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model  = WorkOrderItem
        fields = [
            "id", "component_code", "component_name", "description",
            "unit_price", "labour_cost",
            "completion_status", "mechanic_notes", "completed_at",
        ]
        read_only_fields = ["id", "component_code", "component_name",
                            "description", "unit_price", "labour_cost", "completed_at"]


class WorkOrderSerializer(serializers.ModelSerializer):
    items = WorkOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model  = WorkOrder
        fields = ["id", "work_status", "started_at", "completed_at", "items", "created_at"]
        read_only_fields = fields


class UpdateItemSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=ItemCompletionStatus.choices)
    notes  = serializers.CharField(required=False, allow_blank=True)
