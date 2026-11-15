"""
VEDA V2 — Mechanic Component Diagnostic Model
Generates a synthetic dataset and trains a Random Forest classifier.

Components (9 classes):
  0  wheels          → axle_wheels.glb
  1  suspension      → axle_suspension.glb
  2  engine          → engine.glb
  3  cab             → cab_assembly.glb
  4  chassis         → chassis.glb
  5  rear_compactor  → rear_compactor.glb
  6  refuse_body     → refuse_body.glb
  7  brake_caliper   → caliper.obj  (OBJ)
  8  tyres           → (no 3D model — text only)

Input features (10):
  brake_pad_mm         Brake pad thickness in mm         (1–15)
  tyre_tread_mm        Tyre tread depth in mm            (1–12)
  engine_oil_temp_c    Engine oil temperature °C         (60–160)
  engine_oil_pressure  Engine oil pressure bar           (0.5–6)
  suspension_travel_mm Suspension travel mm              (10–120)
  wheel_bearing_noise  Mechanic rating 0–10              (0–10)
  chassis_cracks       Visual check 0=no 1=yes           (0 or 1)
  compactor_pressure   Hydraulic pressure bar            (50–300)
  body_damage_score    Visual damage rating 0–10         (0–10)
  fuel_pressure_bar    Fuel line pressure bar            (1–8)

Run: python ai_engine/models/train_mechanic.py
"""

import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
log = logging.getLogger("veda.mechanic_model")

ARTIFACT_DIR = Path(__file__).resolve().parent / "mechanic_v1"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

COMPONENTS = [
    "wheels",
    "suspension",
    "engine",
    "cab",
    "chassis",
    "rear_compactor",
    "refuse_body",
    "brake_caliper",
    "tyres",
]

# 3D model mapping — None means no model available
MODEL_3D_MAP = {
    "wheels":         {"file": "components/axle_wheels.glb",    "type": "glb"},
    "suspension":     {"file": "components/axle_suspension.glb","type": "glb"},
    "engine":         {"file": "engine.glb",                    "type": "glb"},
    "cab":            {"file": "components/cab_assembly.glb",   "type": "glb"},
    "chassis":        {"file": "components/chassis.glb",        "type": "glb"},
    "rear_compactor": {"file": "components/rear_compactor.glb", "type": "glb"},
    "refuse_body":    {"file": "components/refuse_body.glb",    "type": "glb"},
    "brake_caliper":  {"file": "caliper.obj",                   "type": "obj"},
    "tyres":          None,  # no separate 3D model
}

N_SAMPLES = 6000
rng = np.random.default_rng(42)

def generate_dataset():
    rows = []
    labels = []

    per_class = N_SAMPLES // len(COMPONENTS)

    for cls_idx, component in enumerate(COMPONENTS):
        for _ in range(per_class):
            # Base: all readings normal
            brake_pad       = rng.uniform(8,  15)
            tyre_tread      = rng.uniform(5,  12)
            oil_temp        = rng.uniform(80, 110)
            oil_pressure    = rng.uniform(3,   6)
            susp_travel     = rng.uniform(50, 100)
            bearing_noise   = rng.uniform(0,   3)
            chassis_cracks  = 0.0
            compactor_press = rng.uniform(180, 280)
            body_damage     = rng.uniform(0,   3)
            fuel_pressure   = rng.uniform(3,   7)

            # Inject fault signal for the target component
            if component == "wheels":
                bearing_noise  = rng.uniform(7, 10)
                tyre_tread     = rng.uniform(1, 4)

            elif component == "suspension":
                susp_travel    = rng.uniform(10, 30)
                bearing_noise  = rng.uniform(5, 8)

            elif component == "engine":
                oil_temp       = rng.uniform(140, 160)
                oil_pressure   = rng.uniform(0.5, 1.8)
                fuel_pressure  = rng.uniform(1,   2.5)

            elif component == "cab":
                body_damage    = rng.uniform(7, 10)
                chassis_cracks = rng.choice([0.0, 1.0], p=[0.3, 0.7])

            elif component == "chassis":
                chassis_cracks = 1.0
                susp_travel    = rng.uniform(10, 25)

            elif component == "rear_compactor":
                compactor_press = rng.uniform(50, 110)
                body_damage     = rng.uniform(5, 8)

            elif component == "refuse_body":
                body_damage     = rng.uniform(6, 10)
                chassis_cracks  = rng.choice([0.0, 1.0], p=[0.4, 0.6])

            elif component == "brake_caliper":
                brake_pad       = rng.uniform(1, 4)
                bearing_noise   = rng.uniform(6, 9)

            elif component == "tyres":
                tyre_tread      = rng.uniform(1, 3)
                brake_pad       = rng.uniform(2, 6)

            # Add small noise to all features
            noise = rng.normal(0, 0.05, 10)
            row = np.array([
                brake_pad, tyre_tread, oil_temp, oil_pressure,
                susp_travel, bearing_noise, chassis_cracks,
                compactor_press, body_damage, fuel_pressure
            ]) + noise

            # Clip to valid ranges
            row[0]  = np.clip(row[0],  1,   15)   # brake_pad
            row[1]  = np.clip(row[1],  1,   12)   # tyre_tread
            row[2]  = np.clip(row[2],  60, 160)   # oil_temp
            row[3]  = np.clip(row[3],  0.5, 6)    # oil_pressure
            row[4]  = np.clip(row[4],  10, 120)   # susp_travel
            row[5]  = np.clip(row[5],  0,   10)   # bearing_noise
            row[6]  = np.clip(row[6],  0,    1)   # chassis_cracks
            row[7]  = np.clip(row[7],  50, 300)   # compactor_press
            row[8]  = np.clip(row[8],  0,   10)   # body_damage
            row[9]  = np.clip(row[9],  1,    8)   # fuel_pressure

            rows.append(row)
            labels.append(cls_idx)

    X = np.array(rows)
    y = np.array(labels)
    return X, y


def main():
    log.info("=== VEDA Mechanic Component Diagnostic Model ===")

    log.info("[1/3] Generating synthetic dataset...")
    X, y = generate_dataset()
    log.info(f"  Samples: {len(X)}, Features: {X.shape[1]}, Classes: {len(COMPONENTS)}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    log.info("[2/3] Training Random Forest classifier...")
    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    log.info("[3/3] Evaluating on test set...")
    y_pred = clf.predict(X_test)
    acc    = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=COMPONENTS)
    log.info(f"\n{report}")
    log.info(f"Overall accuracy: {acc:.4f}")

    # Save artifacts
    joblib.dump(clf, ARTIFACT_DIR / "mechanic_classifier.joblib")

    feature_names = [
        "brake_pad_mm", "tyre_tread_mm", "engine_oil_temp_c",
        "engine_oil_pressure_bar", "suspension_travel_mm",
        "wheel_bearing_noise", "chassis_cracks",
        "compactor_hydraulic_pressure_bar", "body_damage_score",
        "fuel_pressure_bar",
    ]

    metadata = {
        "model_name":    "mechanic_component_classifier",
        "model_version": "v1.0.0",
        "model_type":    "RandomForestClassifier",
        "components":    COMPONENTS,
        "model_3d_map":  MODEL_3D_MAP,
        "feature_names": feature_names,
        "feature_count": len(feature_names),
        "n_train":       len(X_train),
        "n_test":        len(X_test),
        "test_accuracy": round(float(acc), 4),
        "scope_warning": (
            "This model is trained on synthetic data for demonstration purposes. "
            "It should not be used for real vehicle diagnostics without validation "
            "against real inspection records."
        ),
    }

    with open(ARTIFACT_DIR / "mechanic_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    with open(ARTIFACT_DIR / "feature_names.json", "w") as f:
        json.dump(feature_names, f, indent=2)

    log.info(f"\nArtifacts saved to: {ARTIFACT_DIR}")
    log.info(f"Accuracy: {acc:.4f}")
    return metadata


if __name__ == "__main__":
    main()
