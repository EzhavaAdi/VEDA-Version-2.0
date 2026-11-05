"""VEDA V2 — diagnosis serializers"""

from rest_framework import serializers
from .models import (
    AIModel, AIRun, AIPrediction, DiagnosisCase,
    DiagnosisEvidence, MechanicVerification,
)


class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AIModel
        fields = [
            "id", "model_name", "model_version", "model_type",
            "dataset_reference", "preprocessing_version", "active_status",
            "test_precision", "test_recall", "test_f1", "test_roc_auc",
            "scope_warning", "created_at",
        ]
        read_only_fields = fields


class AIPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AIPrediction
        fields = [
            "id", "predicted_class", "predicted_class_int",
            "probability_positive", "prediction_metadata", "created_at",
        ]
        read_only_fields = fields


class AIRunSerializer(serializers.ModelSerializer):
    model_name    = serializers.CharField(source="model.model_name", read_only=True)
    model_version = serializers.CharField(source="model.model_version", read_only=True)
    prediction    = AIPredictionSerializer(read_only=True)
    scope_warning = serializers.CharField(source="model.scope_warning", read_only=True)

    class Meta:
        model  = AIRun
        fields = [
            "id", "model_name", "model_version", "scope_warning",
            "execution_status", "error_message",
            "started_at", "completed_at", "prediction",
        ]
        read_only_fields = fields


class DiagnosisEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DiagnosisEvidence
        fields = [
            "id", "evidence_type", "evidence_reference",
            "evidence_description", "source_timestamp",
        ]
        read_only_fields = fields


class DiagnosisCaseSerializer(serializers.ModelSerializer):
    component_code = serializers.CharField(source="component.component_code", read_only=True)
    component_name = serializers.CharField(source="component.component_name", read_only=True)
    vehicle_system = serializers.CharField(source="component.vehicle_system", read_only=True)
    evidence       = DiagnosisEvidenceSerializer(many=True, read_only=True)

    class Meta:
        model  = DiagnosisCase
        fields = [
            "id", "component_code", "component_name", "vehicle_system",
            "diagnosis_status", "mechanic_verification",
            "final_notes", "evidence", "created_at", "updated_at",
        ]
        read_only_fields = fields


class RunDiagnosisSerializer(serializers.Serializer):
    """Request body for triggering APS diagnosis — no required fields
    (features come from the inspection's sensor readings)."""
    pass


class VerifyDiagnosisSerializer(serializers.Serializer):
    verification = serializers.ChoiceField(choices=MechanicVerification.choices)
    notes        = serializers.CharField(required=False, allow_blank=True)
