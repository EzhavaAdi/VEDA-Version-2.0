"""VEDA V2 — diagnosis admin"""
from django.contrib import admin
from .models import AIModel, AIRun, AIPrediction, DiagnosisCase, DiagnosisEvidence

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ["model_name", "model_version", "model_type", "active_status",
                    "test_f1", "test_roc_auc", "created_at"]
    readonly_fields = ["id", "created_at"]

@admin.register(AIRun)
class AIRunAdmin(admin.ModelAdmin):
    list_display = ["id", "service_order", "model", "execution_status", "started_at"]
    list_filter  = ["execution_status"]
    readonly_fields = ["id", "started_at"]

@admin.register(AIPrediction)
class AIPredictionAdmin(admin.ModelAdmin):
    list_display = ["ai_run", "predicted_class", "probability_positive", "created_at"]
    readonly_fields = ["id", "created_at"]

@admin.register(DiagnosisCase)
class DiagnosisCaseAdmin(admin.ModelAdmin):
    list_display = ["service_order", "component", "diagnosis_status", "mechanic_verification"]
    list_filter  = ["diagnosis_status", "mechanic_verification"]
    readonly_fields = ["id", "created_at", "updated_at"]

@admin.register(DiagnosisEvidence)
class DiagnosisEvidenceAdmin(admin.ModelAdmin):
    list_display = ["diagnosis_case", "evidence_type", "source_timestamp"]
    list_filter  = ["evidence_type"]
    readonly_fields = ["id"]
