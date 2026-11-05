"""VEDA V2 — inspections views"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsMechanic, IsWorkshopMember
from apps.service_orders.services import get_order_for_centre, get_order_for_owner

from . import services
from .serializers import (
    InspectionSerializer,
    InspectionUpdateSerializer,
    InspectionItemSerializer,
    InspectionItemCreateSerializer,
    SensorReadingSerializer,
    SensorReadingCreateSerializer,
)


def _resolve_order(order_id, user):
    """Resolve a service order for either a workshop member or owner."""
    try:
        return get_order_for_centre(str(order_id), user)
    except Exception:
        pass
    try:
        return get_order_for_owner(str(order_id), user)
    except Exception:
        return None


class InspectionView(APIView):
    """
    POST /api/v1/service-orders/<order_id>/inspection/   — Start inspection
    GET  /api/v1/service-orders/<order_id>/inspection/   — Get inspection
    PATCH /api/v1/service-orders/<order_id>/inspection/  — Update general observations
    """
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, order_id: str) -> Response:
        order = _resolve_order(order_id, request.user)
        if not order:
            return Response({"detail": "Service order not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            inspection = services.start_inspection(order, request.user)
        except (services.InspectionError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(InspectionSerializer(inspection).data, status=status.HTTP_201_CREATED)

    def get(self, request: Request, order_id: str) -> Response:
        try:
            inspection = services.get_inspection_for_member(str(order_id), request.user)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except services.PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        return Response(InspectionSerializer(inspection).data)

    def patch(self, request: Request, order_id: str) -> Response:
        try:
            inspection = services.get_inspection_for_mechanic(str(order_id), request.user)
        except (services.NotFoundError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        ser = InspectionUpdateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            inspection = services.update_general_observations(
                inspection, request.user,
                ser.validated_data.get("general_observations", ""),
            )
        except (services.InspectionError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(InspectionSerializer(inspection).data)


class CompleteInspectionView(APIView):
    """POST /api/v1/service-orders/<order_id>/inspection/complete/"""
    permission_classes = [IsAuthenticated, IsMechanic]

    def post(self, request: Request, order_id: str) -> Response:
        try:
            inspection = services.get_inspection_for_mechanic(str(order_id), request.user)
        except (services.NotFoundError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            inspection = services.complete_inspection(inspection, request.user)
        except (services.InspectionError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(InspectionSerializer(inspection).data)


class InspectionItemListView(APIView):
    """
    GET  /api/v1/service-orders/<order_id>/inspection/items/
    POST /api/v1/service-orders/<order_id>/inspection/items/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, order_id: str) -> Response:
        try:
            inspection = services.get_inspection_for_member(str(order_id), request.user)
        except (services.NotFoundError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        items = services.get_inspection_items(inspection)
        return Response(InspectionItemSerializer(items, many=True).data)

    def post(self, request: Request, order_id: str) -> Response:
        try:
            inspection = services.get_inspection_for_mechanic(str(order_id), request.user)
        except (services.NotFoundError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        ser = InspectionItemCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        try:
            item = services.add_inspection_item(
                inspection, request.user,
                d["component_code"], d["observed_condition"],
                d["severity"], d.get("mechanic_notes", ""),
            )
        except (services.InspectionError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(InspectionItemSerializer(item).data, status=status.HTTP_201_CREATED)


class SensorReadingListView(APIView):
    """
    GET  /api/v1/service-orders/<order_id>/inspection/readings/
    POST /api/v1/service-orders/<order_id>/inspection/readings/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, order_id: str) -> Response:
        try:
            inspection = services.get_inspection_for_member(str(order_id), request.user)
        except (services.NotFoundError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        readings = services.get_sensor_readings(inspection)
        return Response(SensorReadingSerializer(readings, many=True).data)

    def post(self, request: Request, order_id: str) -> Response:
        try:
            inspection = services.get_inspection_for_mechanic(str(order_id), request.user)
        except (services.NotFoundError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        ser = SensorReadingCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        try:
            reading = services.add_sensor_reading(
                inspection, request.user,
                d["parameter_name"], d["parameter_value"],
                d.get("unit", ""),
                d.get("component_code", "") or None,
                d.get("notes", ""),
            )
        except (services.InspectionError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(SensorReadingSerializer(reading).data, status=status.HTTP_201_CREATED)
