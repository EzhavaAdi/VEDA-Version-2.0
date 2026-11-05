"""
VEDA V2 — APS classifier training script

Run once to train the model and save artifacts:
    python ai_engine/models/train_aps.py

Outputs (written to ai_engine/models/aps_v1/):
    preprocessor.joblib         — fitted imputer + scaler pipeline
    feature_names.json          — ordered feature list (170 names)
    preprocessing_stats.json    — dataset metadata
    aps_classifier.joblib       — trained XGBoost classifier
    model_metadata.json         — version, metrics, training config

RULES:
- No data leakage: test set is only used for final evaluation.
- Class imbalance handled via scale_pos_weight.
- Model accuracy is recorded from actual evaluation — never invented.
- Artifacts are saved but NOT committed to Git (excluded by .gitignore).
"""

import json
import logging
import sys
from pathlib import Path

# Allow running from the Backend/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from xgboost import XGBClassifier

from ai_engine.preprocessing.pipeline import (
    build_and_fit,
    save_artifacts,
    load_pipeline,
)

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("veda.ai.training")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE          = Path(__file__).resolve().parent.parent.parent
TRAIN_PATH    = BASE.parent / "dataset" / "scania-aps" / "raw" / "aps_failure_training_set.csv"
TEST_PATH     = BASE.parent / "dataset" / "scania-aps" / "raw" / "aps_failure_test_set.csv"
ARTIFACT_DIR  = BASE / "ai_engine" / "models" / "aps_v1"

MODEL_VERSION          = "v1.0.0"
PREPROCESSING_VERSION  = "v1.0.0"


def load_test_data(test_path: Path, pipeline, feature_names: list[str]):
    df = pd.read_csv(test_path, na_values="na")
    y_test = (df["class"] == "pos").astype(int).values
    X_test = df.drop(columns=["class"])
    X_test = X_test[feature_names]          # enforce column order
    X_test_t = pipeline.transform(X_test)
    return X_test_t, y_test


def main():
    logger.info("=== VEDA APS Classifier Training ===")
    logger.info(f"Train:  {TRAIN_PATH}")
    logger.info(f"Test:   {TEST_PATH}")
    logger.info(f"Output: {ARTIFACT_DIR}")

    # ── Step 1: Fit preprocessing pipeline ─────────────────────────────────
    logger.info("\n[1/4] Fitting preprocessing pipeline...")
    pipeline, feature_names, y_train, stats = build_and_fit(TRAIN_PATH)
    save_artifacts(pipeline, feature_names, stats, ARTIFACT_DIR)

    # ── Step 2: Transform training features ────────────────────────────────
    logger.info("\n[2/4] Transforming training data...")
    df_train = pd.read_csv(TRAIN_PATH, na_values="na")
    X_train  = df_train.drop(columns=["class"])[feature_names]
    X_train_t = pipeline.transform(X_train)

    # Class imbalance: ~59:1 — use scale_pos_weight
    n_neg = int((y_train == 0).sum())
    n_pos = int(y_train.sum())
    scale_pos_weight = round(n_neg / n_pos, 2)
    logger.info(f"scale_pos_weight = {scale_pos_weight} ({n_neg} neg / {n_pos} pos)")

    # ── Step 3: Train XGBoost classifier ────────────────────────────────────
    logger.info("\n[3/4] Training XGBoost classifier...")
    clf = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1,
        tree_method="hist",
    )
    clf.fit(X_train_t, y_train)
    logger.info("Training complete.")

    # ── Step 4: Evaluate on held-out test set ───────────────────────────────
    logger.info("\n[4/4] Evaluating on test set...")
    X_test_t, y_test = load_test_data(TEST_PATH, pipeline, feature_names)
    y_pred      = clf.predict(X_test_t)
    y_pred_prob = clf.predict_proba(X_test_t)[:, 1]

    precision = round(float(precision_score(y_test, y_pred, zero_division=0)), 4)
    recall    = round(float(recall_score(y_test, y_pred, zero_division=0)),    4)
    f1        = round(float(f1_score(y_test, y_pred, zero_division=0)),        4)
    roc_auc   = round(float(roc_auc_score(y_test, y_pred_prob)),               4)
    cm        = confusion_matrix(y_test, y_pred).tolist()

    logger.info(f"\nClassification Report:\n{classification_report(y_test, y_pred, target_names=['neg','pos'])}")
    logger.info(f"Confusion Matrix:\n{np.array(cm)}")
    logger.info(f"ROC-AUC: {roc_auc}")

    # Cost metric from dataset description: FP cost=10, FN cost=500
    fp = cm[0][1]
    fn = cm[1][0]
    total_cost = fp * 10 + fn * 500
    logger.info(f"Business cost metric: FP={fp}*10 + FN={fn}*500 = {total_cost}")

    # ── Save model artifact ─────────────────────────────────────────────────
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    model_path = ARTIFACT_DIR / "aps_classifier.joblib"
    joblib.dump(clf, model_path)

    metadata = {
        "model_name":             "aps_failure_classifier",
        "model_version":          MODEL_VERSION,
        "model_type":             "XGBoostClassifier",
        "preprocessing_version":  PREPROCESSING_VERSION,
        "dataset_reference":      "Scania APS Failure Dataset (GPL v3, Scania CV AB 2016)",
        "artifact_location":      str(ARTIFACT_DIR),
        "n_estimators":           200,
        "max_depth":              6,
        "learning_rate":          0.1,
        "scale_pos_weight":       scale_pos_weight,
        "test_precision":         precision,
        "test_recall":            recall,
        "test_f1":                f1,
        "test_roc_auc":           roc_auc,
        "confusion_matrix":       cm,
        "business_cost_fp":       fp * 10,
        "business_cost_fn":       fn * 500,
        "business_total_cost":    total_cost,
        "n_train_samples":        len(y_train),
        "n_test_samples":         len(y_test),
        "feature_count":          len(feature_names),
        "predicted_classes":      {"0": "neg (no APS failure)", "1": "pos (APS failure)"},
        "scope_warning": (
            "This model classifies APS-related failures only. "
            "It does not diagnose all truck faults and must not be "
            "presented as a universal vehicle diagnostic system."
        ),
    }

    with open(ARTIFACT_DIR / "model_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"\nModel saved to: {model_path}")
    logger.info(f"Metadata saved to: {ARTIFACT_DIR / 'model_metadata.json'}")
    logger.info("\n=== Training Complete ===")
    logger.info(f"  Precision: {precision}  Recall: {recall}  F1: {f1}  ROC-AUC: {roc_auc}")
    logger.info(f"  Business cost: {total_cost}")
    return metadata


if __name__ == "__main__":
    main()
