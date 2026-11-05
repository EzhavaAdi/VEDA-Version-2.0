"""VEDA V2 — estimates serializers"""
from rest_framework import serializers
from .models import RepairEstimate, EstimateItem, ApprovalStatus


class EstimateItemSerializer(serializers.ModelSerializer):
    component_code = serializers.CharField(source="component.component_code", read_only=True)
    component_name = serializers.CharField(source="component.component_name", read_only=True)
    part_name      = serializers.CharField(source="part.part_name",   read_only=True, allow_null=True)
    part_number    = serializers.CharField(source="part.part_number", read_only=True, allow_null=True)
    line_total     = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model  = EstimateItem
        fields = [
            "id", "component_code", "component_name",
            "part_name", "part_number",
            "description", "quantity", "unit_price", "labour_cost", "line_total",
            "approval_status", "clarification_note",
            "owner_decision_at",
        ]
        read_only_fields = ["id", "component_code", "component_name",
                            "part_name", "part_number", "line_total",
                            "approval_status", "clarification_note", "owner_decision_at"]


class RepairEstimateSerializer(serializers.ModelSerializer):
    items = EstimateItemSerializer(many=True, read_only=True)
    created_by_phone = serializers.CharField(source="created_by.phone_number", read_only=True, allow_null=True)

    class Meta:
        model  = RepairEstimate
        fields = [
            "id", "revision_number", "estimate_status",
            "labour_total", "parts_total", "grand_total",
            "notes", "created_by_phone", "items", "created_at",
        ]
        read_only_fields = fields


class CreateEstimateSerializer(serializers.Serializer):
    notes = serializers.CharField(required=False, allow_blank=True)


class AddEstimateItemSerializer(serializers.Serializer):
    component_code = serializers.CharField(max_length=50)
    description    = serializers.CharField(min_length=3, max_length=500)
    quantity       = serializers.IntegerField(min_value=1)
    unit_price     = serializers.DecimalField(max_digits=12, decimal_places=2)
    labour_cost    = serializers.DecimalField(max_digits=12, decimal_places=2)
    part_id        = serializers.UUIDField(required=False, allow_null=True)


class ItemDecisionSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=ApprovalStatus.choices)
    note     = serializers.CharField(required=False, allow_blank=True)
