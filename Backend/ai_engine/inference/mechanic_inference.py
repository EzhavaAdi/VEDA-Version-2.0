"""VEDA V2 — Mechanic component inference engine."""
import json
import logging
from pathlib import Path

import joblib
import numpy as np

log = logging.getLogger("veda.mechanic_inference")

ARTIFACT_DIR = Path(__file__).resolve().parent.parent / "models" / "mechanic_v1"

_clf      = None
_metadata = None
_features = None


def _load():
    global _clf, _metadata, _features
    if _clf is not None:
        return
    _clf = joblib.load(ARTIFACT_DIR / "mechanic_classifier.joblib")
    with open(ARTIFACT_DIR / "mechanic_metadata.json") as f:
        _metadata = json.load(f)
    with open(ARTIFACT_DIR / "feature_names.json") as f:
        _features = json.load(f)
    log.info(f"Mechanic model loaded — accuracy={_metadata['test_accuracy']}")


def get_metadata():
    _load()
    return _metadata


# ---------------------------------------------------------------------------
# Health scoring — maps each reading to a 0–100 health score
# 100 = perfect, 0 = critical failure
# ---------------------------------------------------------------------------
HEALTH_RULES = {
    # (feature_key, bad_direction, bad_threshold, warn_threshold)
    # bad_direction: 'low' means low values are bad, 'high' means high is bad
    "brake_pad_mm":                     ("low",  3.0,   5.0),
    "tyre_tread_mm":                    ("low",  2.0,   4.0),
    "engine_oil_temp_c":                ("high", 140.0, 120.0),
    "engine_oil_pressure_bar":          ("low",  1.5,   2.5),
    "suspension_travel_mm":             ("low",  25.0,  40.0),
    "wheel_bearing_noise":              ("high", 7.0,   5.0),
    "chassis_cracks":                   ("high", 1.0,   0.5),
    "compactor_hydraulic_pressure_bar": ("low",  100.0, 150.0),
    "body_damage_score":                ("high", 7.0,   5.0),
    "fuel_pressure_bar":                ("low",  1.5,   2.5),
}

# Which features map to which component
FEATURE_COMPONENT_MAP = {
    "brake_pad_mm":                     ["brake_caliper", "wheels"],
    "tyre_tread_mm":                    ["tyres", "wheels"],
    "engine_oil_temp_c":                ["engine"],
    "engine_oil_pressure_bar":          ["engine"],
    "suspension_travel_mm":             ["suspension", "chassis"],
    "wheel_bearing_noise":              ["wheels", "brake_caliper"],
    "chassis_cracks":                   ["chassis", "refuse_body", "cab"],
    "compactor_hydraulic_pressure_bar": ["rear_compactor"],
    "body_damage_score":                ["cab", "refuse_body"],
    "fuel_pressure_bar":                ["engine"],
}


def _score_feature(key: str, value: float) -> int:
    """Return 0–100 health score for a single feature reading."""
    if key not in HEALTH_RULES:
        return 100
    direction, bad_thresh, warn_thresh = HEALTH_RULES[key]
    if direction == "low":
        if value <= bad_thresh:
            return max(0, int((value / bad_thresh) * 30))
        elif value <= warn_thresh:
            return int(30 + ((value - bad_thresh) / (warn_thresh - bad_thresh)) * 40)
        else:
            return min(100, int(70 + ((value - warn_thresh) / (warn_thresh * 0.5)) * 30))
    else:  # high
        if value >= bad_thresh:
            return max(0, int(30 - ((value - bad_thresh) / (bad_thresh * 0.1)) * 30))
        elif value >= warn_thresh:
            return int(30 + ((bad_thresh - value) / (bad_thresh - warn_thresh)) * 40)
        else:
            return 100


def _condition(score: int) -> str:
    if score <= 35:
        return "CRITICAL"
    elif score <= 65:
        return "WARNING"
    return "GOOD"


def _colour(condition: str) -> str:
    return {"CRITICAL": "#FF3B3B", "WARNING": "#FFB347", "GOOD": "#4ADE80"}[condition]


def _build_component_health(values: dict, feature_names: list) -> dict:
    """
    Returns health score for every component based on the input readings.
    Components not covered by any input default to GOOD.
    """
    all_components = [
        "wheels", "suspension", "engine", "cab", "chassis",
        "rear_compactor", "refuse_body", "brake_caliper", "tyres"
    ]
    comp_scores: dict[str, list[int]] = {c: [] for c in all_components}

    for feat, val in values.items():
        if val is None:
            continue
        try:
            fval = float(val)
        except (ValueError, TypeError):
            continue
        score = _score_feature(feat, fval)
        for comp in FEATURE_COMPONENT_MAP.get(feat, []):
            comp_scores[comp].append(score)

    result = {}
    for comp in all_components:
        scores = comp_scores[comp]
        avg    = int(sum(scores) / len(scores)) if scores else 85
        cond   = _condition(avg)
        result[comp] = {
            "health_score": avg,
            "condition":    cond,
            "colour":       _colour(cond),
        }
    return result


# ---------------------------------------------------------------------------
# Main inference
# ---------------------------------------------------------------------------

def run_mechanic_inference(values: dict) -> dict:
    _load()

    row = []
    missing = []
    for name in _features:
        v = values.get(name)
        if v is None:
            missing.append(name)
            row.append(np.nan)
        else:
            try:
                row.append(float(v))
            except (ValueError, TypeError):
                row.append(np.nan)
                missing.append(name)

    row = np.array(row)
    medians = np.array([7, 6, 95, 4, 70, 2, 0, 200, 2, 4], dtype=float)
    for i, v in enumerate(row):
        if np.isnan(v):
            row[i] = medians[i]

    X = row.reshape(1, -1)
    pred_idx   = int(_clf.predict(X)[0])
    proba      = _clf.predict_proba(X)[0]
    confidence = float(proba[pred_idx])
    component  = _metadata["components"][pred_idx]
    model_3d   = _metadata["model_3d_map"].get(component)

    top3_idx = np.argsort(proba)[::-1][:3]
    top3 = [
        {"component": _metadata["components"][int(i)], "probability": round(float(proba[i]), 4)}
        for i in top3_idx
    ]

    # Build component health map for visual diagnosis
    component_health = _build_component_health(values, _features)

    # Force the predicted component to CRITICAL if confidence is high
    if confidence > 0.6 and component in component_health:
        component_health[component]["health_score"] = min(
            component_health[component]["health_score"], 25
        )
        component_health[component]["condition"] = "CRITICAL"
        component_health[component]["colour"]    = "#FF3B3B"

    return {
        "status":               "completed",
        "predicted_component":  component,
        "confidence":           round(confidence, 4),
        "top_3":                top3,
        "model_3d":             model_3d,
        "component_health":     component_health,
        "scope_warning":        _metadata["scope_warning"],
        "missing_features":     missing,
    }
