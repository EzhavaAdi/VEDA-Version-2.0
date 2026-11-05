"""
VEDA V2 — APS inference engine

Loads model + preprocessor artifacts once (module-level singleton).
run_inference() accepts a dict of raw feature values and returns
a structured prediction result.

RULES:
- Never re-train at inference time.
- Never invent confidence scores.
- Store every inference result with model version and input snapshot.
- Report INSUFFICIENT_DATA when required features are entirely absent.
"""

import json
import logging
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np

from ai_engine.preprocessing.pipeline import (
    load_pipeline,
    transform_for_inference,
)

logger = logging.getLogger("veda.ai.inference")

ARTIFACT_DIR   = Path(__file__).resolve().parent.parent / "models" / "aps_v1"
MODEL_VERSION  = "v1.0.0"
PREPROCESSING_VERSION = "v1.0.0"

# Minimum fraction of features that must be non-null for a valid prediction
MIN_FEATURE_COVERAGE = 0.10  # at least 17/170 features must have real values


# ---------------------------------------------------------------------------
# Artifact loading — loaded once per process
# ---------------------------------------------------------------------------

_pipeline      = None
_feature_names = None
_classifier    = None
_metadata      = None


def _load_artifacts():
    global _pipeline, _feature_names, _classifier, _metadata
    if _classifier is not None:
        return

    if not (ARTIFACT_DIR / "aps_classifier.joblib").exists():
        raise FileNotFoundError(
            f"APS model artifacts not found at {ARTIFACT_DIR}. "
            "Run ai_engine/models/train_aps.py first."
        )

    logger.info(f"Loading APS artifacts from {ARTIFACT_DIR}")
    _pipeline, _feature_names = load_pipeline(ARTIFACT_DIR)
    _classifier = joblib.load(ARTIFACT_DIR / "aps_classifier.joblib")

    with open(ARTIFACT_DIR / "model_metadata.json") as f:
        _metadata = json.load(f)

    logger.info(
        f"APS model loaded: {_metadata['model_name']} {_metadata['model_version']} "
        f"(F1={_metadata['test_f1']}, ROC-AUC={_metadata['test_roc_auc']})"
    )


def get_metadata() -> dict:
    _load_artifacts()
    return _metadata


def get_feature_names() -> list[str]:
    _load_artifacts()
    return _feature_names


# ---------------------------------------------------------------------------
# Core inference
# ---------------------------------------------------------------------------

def run_inference(raw_features: dict) -> dict:
    """
    Run APS failure prediction on a dict of raw feature values.

    Args:
        raw_features: {feature_name: numeric_value, ...}
                      Missing features default to NaN (median-imputed).

    Returns:
        {
          "status": "completed" | "insufficient_data" | "error",
          "model_name": str,
          "model_version": str,
          "preprocessing_version": str,
          "predicted_class": "pos" | "neg" | None,
          "predicted_class_int": 1 | 0 | None,
          "probability_positive": float | None,
          "feature_coverage": float,    # fraction of non-null features provided
          "input_snapshot": dict,       # sanitised feature values used
          "scope_warning": str,
          "error_message": str,
        }
    """
    _load_artifacts()

    scope_warning = _metadata.get("scope_warning", "")

    # Check feature coverage
    provided = {k: v for k, v in raw_features.items()
                if k in _feature_names and v is not None}
    coverage = len(provided) / len(_feature_names)

    if coverage < MIN_FEATURE_COVERAGE:
        logger.warning(
            f"APS inference skipped: only {coverage:.1%} feature coverage "
            f"(minimum {MIN_FEATURE_COVERAGE:.0%} required)."
        )
        return {
            "status": "insufficient_data",
            "model_name": _metadata["model_name"],
            "model_version": MODEL_VERSION,
            "preprocessing_version": PREPROCESSING_VERSION,
            "predicted_class": None,
            "predicted_class_int": None,
            "probability_positive": None,
            "feature_coverage": round(coverage, 4),
            "input_snapshot": provided,
            "scope_warning": scope_warning,
            "error_message": (
                f"Insufficient input: {coverage:.1%} feature coverage. "
                f"At least {MIN_FEATURE_COVERAGE:.0%} required for a valid prediction."
            ),
        }

    try:
        X = transform_for_inference(raw_features, _pipeline, _feature_names)
        pred_int   = int(_classifier.predict(X)[0])
        pred_class = "pos" if pred_int == 1 else "neg"
        proba      = float(_classifier.predict_proba(X)[0][1])

        logger.info(
            f"APS inference: {pred_class} (prob_pos={proba:.4f}, coverage={coverage:.1%})"
        )

        return {
            "status": "completed",
            "model_name": _metadata["model_name"],
            "model_version": MODEL_VERSION,
            "preprocessing_version": PREPROCESSING_VERSION,
            "predicted_class": pred_class,
            "predicted_class_int": pred_int,
            "probability_positive": round(proba, 6),
            "feature_coverage": round(coverage, 4),
            "input_snapshot": provided,
            "scope_warning": scope_warning,
            "error_message": "",
        }

    except Exception as exc:
        logger.error(f"APS inference error: {exc}", exc_info=True)
        return {
            "status": "error",
            "model_name": _metadata["model_name"],
            "model_version": MODEL_VERSION,
            "preprocessing_version": PREPROCESSING_VERSION,
            "predicted_class": None,
            "predicted_class_int": None,
            "probability_positive": None,
            "feature_coverage": round(coverage, 4),
            "input_snapshot": provided,
            "scope_warning": scope_warning,
            "error_message": str(exc),
        }
