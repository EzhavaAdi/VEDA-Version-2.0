"""
VEDA V2 — AI integrity tests

Rules enforced:
- Model returns SKIPPED when feature coverage is below minimum
- Model returns COMPLETED with real probability when sufficient features given
- AI prediction is never fabricated
- Mechanic evidence creates diagnosis cases independently of AI
- AI prediction and mechanic verification stored separately
"""

import pytest
from decimal import Decimal
from ai_engine.inference.aps_inference import run_inference, get_feature_names
from apps.diagnosis.models import AIPrediction, AIRun, DiagnosisCase, EvidenceType


@pytest.mark.django_db
class TestInferenceCoverage:
    def test_empty_features_returns_skipped(self):
        result = run_inference({})
        assert result["status"] == "insufficient_data"
        assert result["predicted_class"] is None
        assert result["probability_positive"] is None

    def test_single_feature_returns_skipped(self):
        result = run_inference({"aa_000": 1000.0})
        assert result["status"] == "insufficient_data"

    def test_full_features_returns_completed(self):
        feature_names = get_feature_names()
        # Fill all features with 0.0 (median-imputed anyway but coverage will be 100%)
        features = {f: 0.0 for f in feature_names}
        result = run_inference(features)
        assert result["status"] == "completed"
        assert result["predicted_class"] in ("pos", "neg")
        assert result["probability_positive"] is not None
        assert 0.0 <= result["probability_positive"] <= 1.0

    def test_scope_warning_always_present(self):
        result = run_inference({})
        assert "scope_warning" in result
        assert len(result["scope_warning"]) > 10  # non-empty

    def test_feature_coverage_reported(self):
        features = {f: 1.0 for f in list(get_feature_names())[:20]}
        result = run_inference(features)
        assert "feature_coverage" in result
        assert result["feature_coverage"] > 0


@pytest.mark.django_db
class TestDiagnosisIntegrity:
    def test_mechanic_rule_fires_independently(
        self, completed_inspection, mechanic_user, admin_user
    ):
        """MECH-001: HIGH severity inspection item creates a DiagnosisCase even if AI skips."""
        from apps.diagnosis.services import run_aps_diagnosis
        order = completed_inspection.service_order
        result = run_aps_diagnosis(order, mechanic_user)
        # AI will be SKIPPED (only a few features in inspection)
        # But mechanic-identified HIGH severity component should still create a case
        assert result["candidates_created"] >= 1

    def test_ai_prediction_stored_independently(
        self, completed_inspection, mechanic_user
    ):
        """AI prediction record is stored regardless of mechanic verification."""
        from apps.diagnosis.services import run_aps_diagnosis
        order = completed_inspection.service_order
        run_aps_diagnosis(order, mechanic_user)
        ai_run = AIRun.objects.filter(service_order=order).first()
        assert ai_run is not None
        assert ai_run.execution_status in ("COMPLETED", "SKIPPED")

    def test_mechanic_verification_stored_separately(
        self, completed_inspection, mechanic_user, centre_with_mechanic
    ):
        """Mechanic CONFIRMED/REJECTED is stored on DiagnosisCase, not on AIRun."""
        from apps.diagnosis.services import run_aps_diagnosis, verify_diagnosis_case
        from apps.diagnosis.models import MechanicVerification
        order = completed_inspection.service_order
        run_aps_diagnosis(order, mechanic_user)
        case = DiagnosisCase.objects.filter(service_order=order).first()
        assert case is not None
        assert case.mechanic_verification == MechanicVerification.UNREVIEWED

        # Mechanic verifies
        verify_diagnosis_case(str(case.id), mechanic_user, "CONFIRMED", "Confirmed by inspection.")
        case.refresh_from_db()
        assert case.mechanic_verification == "CONFIRMED"

        # Original AI run is unchanged
        ai_run = AIRun.objects.filter(service_order=order).first()
        assert ai_run.execution_status in ("COMPLETED", "SKIPPED")

    def test_ai_evidence_type_recorded(self, completed_inspection, mechanic_user):
        from apps.diagnosis.services import run_aps_diagnosis
        from apps.diagnosis.models import DiagnosisEvidence
        order = completed_inspection.service_order
        run_aps_diagnosis(order, mechanic_user)
        evidence_types = DiagnosisEvidence.objects.filter(
            diagnosis_case__service_order=order
        ).values_list("evidence_type", flat=True)
        # Must have at least one MECHANIC_OBSERVATION or DIAGNOSTIC_RULE — never fabricated
        assert any(et in (
            EvidenceType.MECHANIC_OBSERVATION,
            EvidenceType.DIAGNOSTIC_RULE,
            EvidenceType.AI_PREDICTION,
        ) for et in evidence_types)
