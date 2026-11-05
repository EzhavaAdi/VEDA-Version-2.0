"""VEDA V2 — estimates views"""
from decimal import Decimal
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsOwner, IsWorkshopMember

from . import services
from .serializers import (
    RepairEstimateSerializer, CreateEstimateSerializer,
    AddEstimateItemSerializer, ItemDecisionSerializer,
)


class EstimateListCreateView(APIView):
    """
    GET  /api/v1/service-orders/<order_id>/estimates/
    POST /api/v1/service-orders/<order_id>/estimates/  — mechanic creates estimate
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, order_id: str) -> Response:
        try:
            estimates = services.get_estimates_for_order(str(order_id), request.user)
        except (services.NotFoundError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        return Response(RepairEstimateSerializer(estimates, many=True).data)

    def post(self, request: Request, order_id: str) -> Response:
        ser = CreateEstimateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            estimate = services.create_estimate(
                str(order_id), request.user,
                notes=ser.validated_data.get("notes", "")
            )
        except (services.EstimateError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(RepairEstimateSerializer(estimate).data, status=status.HTTP_201_CREATED)


class EstimateDetailView(APIView):
    """GET /api/v1/estimates/<estimate_id>/"""
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, estimate_id: str) -> Response:
        try:
            estimate = services.get_estimate(str(estimate_id), request.user)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except services.PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        return Response(RepairEstimateSerializer(estimate).data)


class AddEstimateItemView(APIView):
    """POST /api/v1/estimates/<estimate_id>/items/"""
    permission_classes = [IsAuthenticated, IsWorkshopMember]

    def post(self, request: Request, estimate_id: str) -> Response:
        try:
            estimate = services.get_estimate(str(estimate_id), request.user)
        except (services.NotFoundError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        ser = AddEstimateItemSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        try:
            item = services.add_estimate_item(
                estimate, request.user,
                d["component_code"], d["description"],
                d["quantity"], Decimal(str(d["unit_price"])),
                Decimal(str(d["labour_cost"])),
                str(d["part_id"]) if d.get("part_id") else None,
            )
        except services.EstimateError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        from .serializers import EstimateItemSerializer
        return Response(EstimateItemSerializer(item).data, status=status.HTTP_201_CREATED)


class SubmitEstimateView(APIView):
    """POST /api/v1/estimates/<estimate_id>/submit/"""
    permission_classes = [IsAuthenticated, IsWorkshopMember]

    def post(self, request: Request, estimate_id: str) -> Response:
        try:
            estimate = services.get_estimate(str(estimate_id), request.user)
            estimate = services.submit_estimate(estimate, request.user)
        except (services.EstimateError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(RepairEstimateSerializer(estimate).data)


class ItemDecisionView(APIView):
    """
    POST /api/v1/estimate-items/<item_id>/decide/

    Owner-only: approve, reject, or request clarification on one line item.
    """
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request: Request, item_id: str) -> Response:
        ser = ItemDecisionSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            item = services.owner_decide_item(
                str(item_id), request.user,
                ser.validated_data["decision"],
                ser.validated_data.get("note", ""),
            )
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except (services.PermissionError, services.ApprovalError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        from .serializers import EstimateItemSerializer
        return Response(EstimateItemSerializer(item).data)
