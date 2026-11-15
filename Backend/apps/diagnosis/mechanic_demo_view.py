"""VEDA V2 — Mechanic component diagnostic demo endpoint. No auth required."""
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as drf_status

from ai_engine.inference.mechanic_inference import run_mechanic_inference, get_metadata


class MechanicDemoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        meta = get_metadata()
        return Response({
            "model_name":    meta["model_name"],
            "model_version": meta["model_version"],
            "feature_names": meta["feature_names"],
            "components":    meta["components"],
            "test_accuracy": meta["test_accuracy"],
            "scope_warning": meta["scope_warning"],
        })

    def post(self, request: Request) -> Response:
        data = request.data
        if not data:
            return Response(
                {"error": "Send JSON body with feature values."},
                status=drf_status.HTTP_400_BAD_REQUEST,
            )
        result = run_mechanic_inference(data)

        # Silent background logging
        try:
            from apps.inventory.shop_models import MechanicPredictionLog
            MechanicPredictionLog.objects.create(
                session_id=request.META.get('HTTP_X_SESSION_ID', ''),
                predicted_component=result.get('predicted_component', ''),
                confidence=result.get('confidence', 0),
                input_values=data,
                component_health=result.get('component_health', {}),
            )
        except Exception:
            pass

        return Response(result)
