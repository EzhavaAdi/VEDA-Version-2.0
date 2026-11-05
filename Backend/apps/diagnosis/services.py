"""
VEDA V2 — diagnosis service layer

Orchestrates:
1. Running APS inference on sensor readings from an inspection
2. Storing AIRun + AIPrediction records
3. Running the diagnostic rule engine
4. Creating DiagnosisCase + DiagnosisEvidence records
5. Allowing mechanic verification/rejection of findings
"""

import json
import logging
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import User
from apps.components.models import Component
from apps.inspections.models import Inspection
from apps.service_orders.models import ServiceOrder

from .models import (
    AIModel, AIRun, AIPrediction, DiagnosisCase, DiagnosisEvidence,
    ExecutionStatus, DiagnosisStatus, EvidenceType, MechanicVerification,
)

logger = logging.getLogger("veda.diagnosis")


class DiagnosisError(Exception):
    pass

class NotFoundError(DiagnosisError):
    pass

class PermissionError(DiagnosisError):
    pass


# ---------------------------------------------------------------------------
# AI Model registry helpers
# ---------------------------------------------------------------------------

def get_or_create_aps_model() -> AIModel:
    """
    Ensure the APS model is registered in the database.
    Called at inference time — idempotent.
    """
    from ai_engine.inference.aps_inference import get_metadata
    meta = get_metadata()

    model, _ = AIModel.objects.get_or_create(
        model_name=meta["model_name"],
        model_version=meta["model_version"],
        defaults={
            "model_type":             "CLASSIFIER",
            "dataset_reference":      meta["dataset_reference"],
            "artifact_location":      meta["artifact_location"],
            "preprocessing_version":  meta["preprocessing_version"],
            "active_status":          True,
            "test_precision":         meta["test_precision"],
            "test_recall":            meta["test_recall"],
            "test_f1":                meta["test_f1"],
            "test_roc_auc":           meta["test_roc_auc"],
            "scope_warning":          meta["scope_warning"],
        },
    )
    return model


# ---------------------------------------------------------------------------
# Build input features from inspection sensor readings
# ---------------------------------------------------------------------------

def _build_feature_dict(inspection: Inspection) -> dict:
    """
    Convert sensor readings to a {feature_name: value} dict
    suitable for APS inference.

    Sensor readings with parameter_name matching APS feature names
    (aa_000 … eg_000) are used directly.
    All others are ignored for the APS model.
    """
    from ai_engine.inference.aps_inference import get_feature_names
    feature_names = set(get_feature_names())

    raw = {}
    for reading in inspection.sensor_readings.all():
        if reading.parameter_name in feature_names:
            try:
                raw[reading.parameter_name] = float(reading.parameter_value)
            except (TypeError, ValueError):
                pass

    logger.info(
        f"Feature dict built from inspection {inspection.id}: "
        f"{len(raw)}/{len(feature_names)} features provided."
    )
    return raw


# ---------------------------------------------------------------------------
# Run APS inference for a service order
# ---------------------------------------------------------------------------

@transaction.atomic
def run_aps_diagnosis(service_order: ServiceOrder, triggered_by: User) -> dict:
    """
    Main entry point for APS diagnosis.

    1. Validates the inspection is completed.
    2. Registers the AIModel if needed.
    3. Creates AIRun record.
    4. Runs inference.
    5. Stores AIPrediction.
    6. Runs diagnostic rule engine.
    7. Creates DiagnosisCase + DiagnosisEvidence records.
    8. Returns structured result.
    """
    # Validate inspection
    try:
        inspection = Inspection.objects.get(service_order=service_order)
    except Inspection.DoesNotExist:
        raise DiagnosisError("No inspection found for this service order.")

    if inspection.inspection_status != "COMPLETED":
        raise DiagnosisError(
            "Inspection must be completed before running AI diagnosis."
        )

    # Register model
    ai_model = get_or_create_aps_model()

    # Create AIRun
    ai_run = AIRun.objects.create(
        service_order=service_order,
        model=ai_model,
        execution_status=ExecutionStatus.RUNNING,
    )

    try:
        # Build feature input
        raw_features = _build_feature_dict(inspection)
        ai_run.input_reference = json.dumps({"feature_count": len(raw_features)})
        ai_run.save(update_fields=["input_reference"])

        # Run inference
        from ai_engine.inference.aps_inference import run_inference
        result = run_inference(raw_features)

        # Store prediction
        status_map = {
            "completed":        ExecutionStatus.COMPLETED,
            "insufficient_data": ExecutionStatus.SKIPPED,
            "error":            ExecutionStatus.FAILED,
        }
        ai_run.execution_status = status_map.get(result["status"], ExecutionStatus.FAILED)
        ai_run.error_message    = result.get("error_message", "")
        ai_run.completed_at     = timezone.now()
        ai_run.save(update_fields=["execution_status", "error_message", "completed_at"])

        prediction = None
        if result["status"] == "completed":
            prediction = AIPrediction.objects.create(
                ai_run=ai_run,
                predicted_class=result["predicted_class"],
                predicted_class_int=result["predicted_class_int"],
                probability_positive=result.get("probability_positive"),
                prediction_metadata={
                    "feature_coverage": result["feature_coverage"],
                    "model_version":    result["model_version"],
                    "preprocessing_version": result["preprocessing_version"],
                },
            )

        # Run diagnostic rules
        inspection_items = list(inspection.items.select_related("component").values(
            "id", "component__component_code", "component__component_name",
            "observed_condition", "severity", "mechanic_notes"
        ))
        # Normalize keys for rule engine
        items_for_rules = [
            {
                "id":                item["id"],
                "component_code":    item["component__component_code"],
                "component_name":    item["component__component_name"],
                "observed_condition": item["observed_condition"],
                "severity":          item["severity"],
            }
            for item in inspection_items
        ]

        sensor_readings = list(inspection.sensor_readings.select_related("component").values(
            "id", "parameter_name", "parameter_value", "unit",
            "component__component_code", "notes"
        ))
        readings_for_rules = [
            {
                "id":             r["id"],
                "parameter_name": r["parameter_name"],
                "parameter_value": float(r["parameter_value"]),
                "unit":           r["unit"],
                "component_code": r["component__component_code"] or "",
                "notes":          r["notes"],
            }
            for r in sensor_readings
        ]

        from ai_engine.diagnosis_rules.aps_rules import run_all_rules
        candidates, extra_evidence = run_all_rules(
            result, str(ai_run.id), items_for_rules, readings_for_rules
        )

        # Persist DiagnosisCase + DiagnosisEvidence
        created_cases = []
        for candidate in candidates:
            try:
                component = Component.objects.get(component_code=candidate.component_code)
            except Component.DoesNotExist:
                logger.warning(f"Component {candidate.component_code} not in catalogue — skipping.")
                continue

            case, _ = DiagnosisCase.objects.get_or_create(
                service_order=service_order,
                component=component,
                defaults={
                    "diagnosis_status":      DiagnosisStatus.SUSPECTED,
                    "mechanic_verification": MechanicVerification.UNREVIEWED,
                    "created_by":            triggered_by,
                },
            )

            for ev in candidate.evidence:
                DiagnosisEvidence.objects.create(
                    diagnosis_case=case,
                    evidence_type=ev.evidence_type,
                    evidence_reference=ev.evidence_reference,
                    evidence_description=ev.evidence_description,
                )

            created_cases.append(case)

        logger.info(
            f"Diagnosis complete for order {service_order.id}: "
            f"{len(created_cases)} cases created, status={result['status']}"
        )

        return {
            "ai_run_id":          str(ai_run.id),
            "execution_status":   ai_run.execution_status,
            "prediction":         result,
            "candidates_created": len(created_cases),
            "cases": [
                {
                    "case_id":        str(c.id),
                    "component_code": c.component.component_code,
                    "component_name": c.component.component_name,
                    "status":         c.diagnosis_status,
                }
                for c in created_cases
            ],
        }

    except Exception as exc:
        ai_run.execution_status = ExecutionStatus.FAILED
        ai_run.error_message    = str(exc)
        ai_run.completed_at     = timezone.now()
        ai_run.save(update_fields=["execution_status", "error_message", "completed_at"])
        logger.error(f"Diagnosis failed for order {service_order.id}: {exc}", exc_info=True)
        raise DiagnosisError(f"Diagnosis failed: {exc}")


# ---------------------------------------------------------------------------
# Mechanic verification
# ---------------------------------------------------------------------------

@transaction.atomic
def verify_diagnosis_case(case_id: str, mechanic: User,
                           verification: str, notes: str = "") -> DiagnosisCase:
    try:
        case = DiagnosisCase.objects.get(id=case_id)
    except DiagnosisCase.DoesNotExist:
        raise NotFoundError("Diagnosis case not found.")

    from apps.organizations.models import WorkshopMembership
    if not WorkshopMembership.objects.filter(
        user=mechanic,
        service_centre=case.service_order.service_centre,
        is_active=True,
    ).exists():
        raise PermissionError("Only a workshop member can verify diagnosis cases.")

    valid_verifications = [v[0] for v in MechanicVerification.choices]
    if verification not in valid_verifications:
        raise DiagnosisError(f"Invalid verification value: {verification}")

    case.mechanic_verification = verification
    case.final_notes = notes.strip()

    if verification == MechanicVerification.CONFIRMED:
        case.diagnosis_status = DiagnosisStatus.MECHANIC_VERIFIED
    elif verification == MechanicVerification.REJECTED:
        case.diagnosis_status = DiagnosisStatus.MECHANIC_REJECTED

    case.save(update_fields=["mechanic_verification", "diagnosis_status",
                              "final_notes", "updated_at"])

    DiagnosisEvidence.objects.create(
        diagnosis_case=case,
        evidence_type=EvidenceType.MECHANIC_OBSERVATION,
        evidence_reference=str(mechanic.id),
        evidence_description=(
            f"Mechanic {mechanic.phone_number} set verification to '{verification}'. "
            f"Notes: {notes or 'None.'}"
        ),
    )
    return case


# ---------------------------------------------------------------------------
# Read operations
# ---------------------------------------------------------------------------

def get_diagnosis_for_order(order_id: str, user: User) -> dict:
    try:
        order = ServiceOrder.objects.get(id=order_id)
    except ServiceOrder.DoesNotExist:
        raise NotFoundError("Service order not found.")

    from apps.organizations.models import WorkshopMembership
    is_owner  = order.owner_id == user.id
    is_member = WorkshopMembership.objects.filter(
        user=user, service_centre=order.service_centre, is_active=True
    ).exists()
    if not (is_owner or is_member):
        raise PermissionError("Access denied.")

    ai_runs = order.ai_runs.select_related("model", "prediction").order_by("-started_at")
    cases   = order.diagnosis_cases.select_related(
        "component", "created_by"
    ).prefetch_related("evidence").order_by("component__vehicle_system")

    return {"ai_runs": list(ai_runs), "cases": list(cases)}


def get_ai_model_info() -> list:
    return list(AIModel.objects.filter(active_status=True).order_by("-created_at"))
