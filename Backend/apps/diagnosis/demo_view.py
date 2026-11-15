"""
VEDA V2 — Public APS demo inference endpoint.
No authentication required — for demonstration only.
Accepts a CSV file (one data row) or raw JSON features and returns the APS prediction.
"""

import csv
import io
import json
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as drf_status

from ai_engine.inference.aps_inference import run_inference, get_feature_names, get_metadata


class APSDemoInferenceView(APIView):
    """
    POST /api/v1/diagnosis/demo/

    Accepts either:
      - multipart file upload: a CSV file with one header row + one data row
      - JSON body: { "features": { "aa_000": 1234, "ab_000": 0, ... } }

    Returns the APS prediction result.
    """
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """Return model info and expected feature list."""
        meta = get_metadata()
        features = get_feature_names()
        return Response({
            "model_name":    meta["model_name"],
            "model_version": meta["model_version"],
            "feature_count": len(features),
            "feature_names": features[:10],  # first 10 as sample
            "scope_warning": meta["scope_warning"],
            "metrics": {
                "precision": meta["test_precision"],
                "recall":    meta["test_recall"],
                "f1":        meta["test_f1"],
                "roc_auc":   meta["test_roc_auc"],
            }
        })

    def post(self, request: Request) -> Response:
        raw_features = {}

        # ── Option 1: CSV file upload ──────────────────────────────────────
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
            try:
                content = csv_file.read().decode('utf-8', errors='replace')
                reader  = csv.DictReader(io.StringIO(content))
                rows    = list(reader)
                if not rows:
                    return Response(
                        {"error": "CSV file is empty or has no data rows."},
                        status=drf_status.HTTP_400_BAD_REQUEST
                    )
                row = rows[0]
                # Convert values to float where possible, skip 'class' column
                for k, v in row.items():
                    if k.lower() == 'class':
                        continue
                    try:
                        raw_features[k.strip()] = float(v)
                    except (ValueError, TypeError):
                        pass  # leave as missing — imputer handles it
            except Exception as e:
                return Response(
                    {"error": f"Could not parse CSV: {str(e)}"},
                    status=drf_status.HTTP_400_BAD_REQUEST
                )

        # ── Option 2: JSON body ────────────────────────────────────────────
        elif request.data.get('features'):
            try:
                feats = request.data['features']
                if isinstance(feats, str):
                    feats = json.loads(feats)
                for k, v in feats.items():
                    try:
                        raw_features[k] = float(v)
                    except (ValueError, TypeError):
                        pass
            except Exception as e:
                return Response(
                    {"error": f"Could not parse features: {str(e)}"},
                    status=drf_status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {"error": "Send a CSV file (field: 'file') or JSON body with 'features' dict."},
                status=drf_status.HTTP_400_BAD_REQUEST
            )

        # ── Run inference ──────────────────────────────────────────────────
        result = run_inference(raw_features)

        # Build a clean response
        response = {
            "status":               result["status"],
            "model_name":           result["model_name"],
            "model_version":        result["model_version"],
            "predicted_class":      result["predicted_class"],
            "predicted_label":      None,
            "probability_positive": result["probability_positive"],
            "feature_coverage":     result["feature_coverage"],
            "scope_warning":        result["scope_warning"],
            "error_message":        result.get("error_message", ""),
        }

        if result["predicted_class"] == "pos":
            response["predicted_label"] = "APS FAILURE DETECTED"
        elif result["predicted_class"] == "neg":
            response["predicted_label"] = "NO APS FAILURE"
        elif result["status"] == "insufficient_data":
            response["predicted_label"] = "INSUFFICIENT DATA"

        # Silent background logging
        try:
            from apps.inventory.shop_models import APSPredictionLog
            APSPredictionLog.objects.create(
                session_id=request.META.get('HTTP_X_SESSION_ID', ''),
                filename=csv_file.name if 'file' in request.FILES else '',
                predicted_class=result.get('predicted_class') or 'skipped',
                probability_pos=result.get('probability_positive'),
                feature_coverage=result.get('feature_coverage', 0),
            )
        except Exception:
            pass  # never break the response for logging

        return Response(response)