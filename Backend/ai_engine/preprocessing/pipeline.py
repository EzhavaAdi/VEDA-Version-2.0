"""
VEDA V2 — APS preprocessing pipeline

Responsibilities:
- Load raw CSV (train or single-row inference)
- Encode class label (pos=1, neg=0)
- Median imputation (fit on train, apply on inference)
- StandardScaler (fit on train, apply on inference)
- Preserve and enforce exact feature column order

The fitted pipeline is saved as a joblib artifact and reloaded at
inference time. Never re-fit on new data at inference.

RULES (from RULES.md):
- Never invent training data.
- Preserve train/test split — no leakage.
- Document preprocessing version.
- Feature order must match training order exactly at inference.
"""

import json
import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger("veda.ai.preprocessing")

PREPROCESSING_VERSION = "v1.0.0"
CLASS_COLUMN = "class"
POSITIVE_LABEL = "pos"
NEGATIVE_LABEL = "neg"


# ---------------------------------------------------------------------------
# Build and fit the pipeline on training data
# ---------------------------------------------------------------------------

def build_and_fit(train_path: str | Path) -> tuple[Pipeline, list[str], dict]:
    """
    Load training CSV, fit the preprocessing pipeline.

    Returns:
        pipeline  — fitted sklearn Pipeline (imputer + scaler)
        feature_names — ordered list of 170 feature column names
        stats     — dict of class counts and version metadata
    """
    logger.info(f"Loading training data from {train_path}")
    df = pd.read_csv(train_path, na_values="na")

    if CLASS_COLUMN not in df.columns:
        raise ValueError(f"Expected '{CLASS_COLUMN}' column not found.")

    # Separate features and labels
    y = (df[CLASS_COLUMN] == POSITIVE_LABEL).astype(int)
    X = df.drop(columns=[CLASS_COLUMN])
    feature_names = list(X.columns)

    logger.info(f"Features: {len(feature_names)}, Samples: {len(X)}")
    logger.info(f"Class distribution: pos={y.sum()}, neg={(y==0).sum()}")

    # Verify all features are numeric
    non_numeric = X.select_dtypes(exclude=[np.number]).columns.tolist()
    if non_numeric:
        raise ValueError(f"Non-numeric features found: {non_numeric}")

    # Build pipeline: median imputation then standard scaling
    pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler",  StandardScaler()),
    ])
    pipeline.fit(X)

    stats = {
        "preprocessing_version": PREPROCESSING_VERSION,
        "n_features": len(feature_names),
        "n_train_samples": len(X),
        "n_positive": int(y.sum()),
        "n_negative": int((y == 0).sum()),
        "imbalance_ratio": round(float((y==0).sum() / y.sum()), 2),
        "feature_names": feature_names,
    }

    logger.info("Preprocessing pipeline fitted successfully.")
    return pipeline, feature_names, y, stats


# ---------------------------------------------------------------------------
# Save / load artifacts
# ---------------------------------------------------------------------------

def save_artifacts(pipeline: Pipeline, feature_names: list[str],
                   stats: dict, artifact_dir: str | Path) -> None:
    artifact_dir = Path(artifact_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(pipeline, artifact_dir / "preprocessor.joblib")

    with open(artifact_dir / "feature_names.json", "w") as f:
        json.dump(feature_names, f, indent=2)

    with open(artifact_dir / "preprocessing_stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    logger.info(f"Preprocessing artifacts saved to {artifact_dir}")


def load_pipeline(artifact_dir: str | Path) -> tuple[Pipeline, list[str]]:
    artifact_dir = Path(artifact_dir)
    pipeline = joblib.load(artifact_dir / "preprocessor.joblib")
    with open(artifact_dir / "feature_names.json") as f:
        feature_names = json.load(f)
    return pipeline, feature_names


# ---------------------------------------------------------------------------
# Transform a single inference row
# ---------------------------------------------------------------------------

def transform_for_inference(raw: dict, pipeline: Pipeline,
                             feature_names: list[str]) -> np.ndarray:
    """
    Transform a raw dict of {feature_name: value} for inference.

    Missing features default to NaN (the imputer handles them).
    Extra features in raw are ignored — only training features are used.
    Feature order is enforced exactly.
    """
    row = {col: raw.get(col, np.nan) for col in feature_names}
    X = pd.DataFrame([row], columns=feature_names)
    return pipeline.transform(X)


def get_y_for_training(train_path: str | Path) -> np.ndarray:
    """Load labels only (for use with already-fitted pipeline)."""
    df = pd.read_csv(train_path, na_values="na")
    return (df[CLASS_COLUMN] == POSITIVE_LABEL).astype(int).values
