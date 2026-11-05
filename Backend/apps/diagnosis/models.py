"""
VEDA V2 — diagnosis models

AIModel     — registry of trained model versions
AIRun       — one inference execution per service order
AIPrediction — the output of one AIRun
DiagnosisCase — one suspected component finding per service order
DiagnosisEvidence — one piece of evidence supporting a DiagnosisCase

RULES:
- AI prediction and mechanic verification are stored independently.
- Original prediction is never overwritten by mechanic decision.
- Evidence type clearly distinguishes AI vs mechanic vs rule sources.
"""

import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class AIModelType(models.TextChoices):
    CLASSIFIER = "CLASSIFIER", "Binary Classifier"
    REGRESSOR  = "REGRESSOR",  "Regressor"
    RUL        = "RUL",        "Remaining Useful Life"


class ExecutionStatus(models.TextChoices):
    PENDING   = "PENDING",   "Pending"
    RUNNING   = "RUNNING",   "Running"
    COMPLETED = "COMPLETED", "Completed"
    FAILED    = "FAILED",    "Failed"
    SKIPPED   = "SKIPPED",   "Skipped (insufficient input)"


class DiagnosisStatus(models.TextChoices):
    SUSPECTED           = "SUSPECTED",           "Suspected"
    MECHANIC_VERIFIED   = "MECHANIC_VERIFIED",   "Mechanic Verified"
    MECHANIC_REJECTED   = "MECHANIC_REJECTED",   "Mechanic Rejected"
    REQUIRES_INSPECTION = "REQUIRES_INSPECTION", "Requires Further Inspection"
    RESOLVED            = "RESOLVED",            "Resolved"


class EvidenceType(models.TextChoices):
    AI_PREDICTION        = "AI_PREDICTION",        "AI Prediction"
    MECHANIC_OBSERVATION = "MECHANIC_OBSERVATION", "Mechanic Observation"
    SENSOR_READING       = "SENSOR_READING",       "Sensor Reading"
    DIAGNOSTIC_RULE      = "DIAGNOSTIC_RULE",      "Diagnostic Rule"
    EXTERNAL_REFERENCE   = "EXTERNAL_REFERENCE",   "External Reference"


class MechanicVerification(models.TextChoices):
    UNREVIEWED = "UNREVIEWED", "Not Yet Reviewed"
    CONFIRMED  = "CONFIRMED",  "Confirmed by Mechanic"
    REJECTED   = "REJECTED",   "Rejected by Mechanic"
    PARTIAL    = "PARTIAL",    "Partially Confirmed"


# ---------------------------------------------------------------------------
# AIModel — registry
# ---------------------------------------------------------------------------

class AIModel(models.Model):
    id                    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model_name            = models.CharField(max_length=100)
    model_version         = models.CharField(max_length=20)
    model_type            = models.CharField(max_length=20, choices=AIModelType.choices)
    dataset_reference     = models.TextField()
    artifact_location     = models.TextField()
    preprocessing_version = models.CharField(max_length=20)
    active_status         = models.BooleanField(default=True)
    test_precision        = models.FloatField(null=True, blank=True)
    test_recall           = models.FloatField(null=True, blank=True)
    test_f1               = models.FloatField(null=True, blank=True)
    test_roc_auc          = models.FloatField(null=True, blank=True)
    scope_warning         = models.TextField(blank=True)
    created_at            = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table        = "ai_model"
        unique_together = [("model_name", "model_version")]
        verbose_name    = "AI Model"

    def __str__(self):
        return f"{self.model_name} {self.model_version}"


# ---------------------------------------------------------------------------
# AIRun — one execution per service order
# ---------------------------------------------------------------------------

class AIRun(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_order   = models.ForeignKey(
        "service_orders.ServiceOrder",
        on_delete=models.CASCADE,
        related_name="ai_runs",
    )
    model           = models.ForeignKey(
        AIModel, on_delete=models.PROTECT, related_name="runs"
    )
    execution_status = models.CharField(
        max_length=15, choices=ExecutionStatus.choices, default=ExecutionStatus.PENDING
    )
    input_reference  = models.TextField(blank=True, help_text="JSON snapshot of input features used")
    error_message    = models.TextField(blank=True)
    started_at       = models.DateTimeField(default=timezone.now)
    completed_at     = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "ai_run"
        ordering = ["-started_at"]
        verbose_name = "AI Run"

    def __str__(self):
        return f"AIRun {self.id} [{self.execution_status}] for order {self.service_order_id}"


# ---------------------------------------------------------------------------
# AIPrediction — output of one AIRun
# ---------------------------------------------------------------------------

class AIPrediction(models.Model):
    id                   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ai_run               = models.OneToOneField(
        AIRun, on_delete=models.CASCADE, related_name="prediction"
    )
    predicted_class      = models.CharField(max_length=20)   # "pos" or "neg"
    predicted_class_int  = models.SmallIntegerField()         # 1 or 0
    probability_positive = models.FloatField(null=True, blank=True)
    prediction_metadata  = models.JSONField(default=dict)
    created_at           = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "ai_prediction"
        verbose_name = "AI Prediction"

    def __str__(self):
        prob = f" ({self.probability_positive:.2%})" if self.probability_positive else ""
        return f"APS: {self.predicted_class}{prob}"


# ---------------------------------------------------------------------------
# DiagnosisCase — one suspected component finding
# ---------------------------------------------------------------------------

class DiagnosisCase(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_order   = models.ForeignKey(
        "service_orders.ServiceOrder",
        on_delete=models.CASCADE,
        related_name="diagnosis_cases",
    )
    component       = models.ForeignKey(
        "components.Component",
        on_delete=models.PROTECT,
        related_name="diagnosis_cases",
    )
    diagnosis_status     = models.CharField(
        max_length=25, choices=DiagnosisStatus.choices, default=DiagnosisStatus.SUSPECTED
    )
    mechanic_verification = models.CharField(
        max_length=15, choices=MechanicVerification.choices, default=MechanicVerification.UNREVIEWED
    )
    final_notes          = models.TextField(blank=True)
    created_by           = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    created_at           = models.DateTimeField(default=timezone.now)
    updated_at           = models.DateTimeField(auto_now=True)

    class Meta:
        db_table        = "diagnosis_case"
        unique_together = [("service_order", "component")]
        verbose_name    = "Diagnosis Case"

    def __str__(self):
        return f"{self.component.component_code} — {self.diagnosis_status}"


# ---------------------------------------------------------------------------
# DiagnosisEvidence — evidence supporting a DiagnosisCase
# ---------------------------------------------------------------------------

class DiagnosisEvidence(models.Model):
    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diagnosis_case      = models.ForeignKey(
        DiagnosisCase, on_delete=models.CASCADE, related_name="evidence"
    )
    evidence_type       = models.CharField(max_length=25, choices=EvidenceType.choices)
    evidence_reference  = models.TextField(
        blank=True, help_text="ID or identifier of source record"
    )
    evidence_description = models.TextField()
    source_timestamp    = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "diagnosis_evidence"
        ordering = ["source_timestamp"]
        verbose_name = "Diagnosis Evidence"

    def __str__(self):
        return f"{self.evidence_type}: {self.evidence_description[:60]}"
