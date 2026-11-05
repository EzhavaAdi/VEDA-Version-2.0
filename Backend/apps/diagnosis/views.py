"""VEDA V2 — diagnosis views"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsMechanic, IsWorkshopMember
from apps.service_orders.services import get_order_for_centre, get_order_for_owner

from . import services
from .serializers import (
    AIModelSerializer,
    AIRunSerializer,
    DiagnosisCaseSerializer,
    RunDiagnosisSerializer,
    VerifyDiagnosisSerializer,
)


def _resolve_order(order_id, user):
    try:
        return get_order_for_centre(str(order_id), user)
    except Exception:
        pass
    try:
        return get_order_for_owner(str(order_id), user)
    except Exception:
        return None


class AIModelListView(APIView):
    """GET /api/v1/diagnosis/models/ — List registered AI models (public info)."""
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        models = services.get_ai_model_info()
        return Response(AIModelSerializer(models, many=True).data)


class RunDiagnosisView(APIView):
    """
    POST /api/v1/service-orders/<order_id>/diagnosis/run/

    Triggers APS inference on the completed inspection's sensor readings,
    runs the diagnostic rule engine, and creates DiagnosisCase records.
    Only the assigned mechanic or workshop admin can trigger this.
    """
    permission_classes = [IsAuthenticated, IsWorkshopMember]

    def post(self, request: Request, order_id: str) -> Response:
        order = _resolve_order(order_id, request.user)
        if not order:
            return Response({"detail": "Service order not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            result = services.run_aps_diagnosis(order, request.user)
        except services.DiagnosisError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_201_CREATED)


class DiagnosisResultView(APIView):
    """
    GET /api/v1/service-orders/<order_id>/diagnosis/

    Returns AI runs and diagnosis cases for the order.
    Accessible to owner and workshop members.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, order_id: str) -> Response:
        try:
            data = services.get_diagnosis_for_order(str(order_id), request.user)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except services.PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        return Response({
            "ai_runs": AIRunSerializer(data["ai_runs"], many=True).data,
            "diagnosis_cases": DiagnosisCaseSerializer(data["cases"], many=True).data,
        })


class VerifyDiagnosisCaseView(APIView):
    """
    POST /api/v1/diagnosis/cases/<case_id>/verify/

    Mechanic confirms or rejects a diagnosis case.
    """
    permission_classes = [IsAuthenticated, IsMechanic]

    def post(self, request: Request, case_id: str) -> Response:
        ser = VerifyDiagnosisSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            case = services.verify_diagnosis_case(
                str(case_id),
                request.user,
                ser.validated_data["verification"],
                ser.validated_data.get("notes", ""),
            )
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except (services.PermissionError, services.DiagnosisError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(DiagnosisCaseSerializer(case).data)
