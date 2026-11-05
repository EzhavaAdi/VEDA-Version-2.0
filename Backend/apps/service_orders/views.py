"""VEDA V2 — service_orders views"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import IsOwner, IsWorkshopAdmin, IsMechanic, IsWorkshopMember

from . import services
from .serializers import (
    ServiceOrderSerializer,
    ServiceOrderCreateSerializer,
    TransitionSerializer,
    AssignMechanicSerializer,
    ServiceOrderEventSerializer,
)


# ---------------------------------------------------------------------------
# Owner views
# ---------------------------------------------------------------------------

class OwnerServiceOrderListView(APIView):
    """
    GET  /api/v1/service-orders/          — Owner's orders
    POST /api/v1/service-orders/          — Submit a new service request
    """
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request: Request) -> Response:
        orders = services.get_orders_for_owner(request.user)
        return Response(ServiceOrderSerializer(orders, many=True).data)

    def post(self, request: Request) -> Response:
        ser = ServiceOrderCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        try:
            order = services.create_service_order(
                request.user,
                str(d["vehicle_id"]),
                str(d["service_centre_id"]),
                d["service_description"],
            )
        except (services.NotFoundError, services.ServiceOrderError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ServiceOrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OwnerServiceOrderDetailView(APIView):
    """GET /api/v1/service-orders/<id>/"""
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request: Request, order_id: str) -> Response:
        try:
            order = services.get_order_for_owner(order_id, request.user)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(ServiceOrderSerializer(order).data)


# ---------------------------------------------------------------------------
# Workshop views
# ---------------------------------------------------------------------------

class CentreServiceOrderListView(APIView):
    """GET /api/v1/service-centres/<id>/orders/"""
    permission_classes = [IsAuthenticated, IsWorkshopMember]

    def get(self, request: Request, centre_id: str) -> Response:
        try:
            orders = services.get_orders_for_centre(str(centre_id), request.user)
        except services.PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        return Response(ServiceOrderSerializer(orders, many=True).data)


class CentreServiceOrderDetailView(APIView):
    """
    GET   /api/v1/service-centres/<id>/orders/<order_id>/
    PATCH /api/v1/service-centres/<id>/orders/<order_id>/transition/  (via action)
    """
    permission_classes = [IsAuthenticated, IsWorkshopMember]

    def get(self, request: Request, centre_id: str, order_id: str) -> Response:
        try:
            order = services.get_order_for_centre(order_id, request.user)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except services.PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        return Response(ServiceOrderSerializer(order).data)


class TransitionOrderView(APIView):
    """
    POST /api/v1/service-orders/<id>/transition/

    Accessible to: workshop members for workshop-side transitions,
    owners for approval transitions (APPROVED / PARTIALLY_APPROVED).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, order_id: str) -> Response:
        ser = TransitionSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        new_status = d["status"]

        # Resolve the order — try owner first, then workshop member
        order = None
        try:
            order = services.get_order_for_owner(order_id, request.user)
        except services.NotFoundError:
            pass

        if order is None:
            try:
                order = services.get_order_for_centre(order_id, request.user)
            except (services.NotFoundError, services.PermissionError):
                return Response({"detail": "Service order not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            order = services.transition_order(
                order, new_status, request.user,
                notes=d.get("notes", ""),
                rejection_reason=d.get("rejection_reason", ""),
            )
        except services.TransitionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ServiceOrderSerializer(order).data)


class AssignMechanicView(APIView):
    """POST /api/v1/service-orders/<id>/assign-mechanic/"""
    permission_classes = [IsAuthenticated, IsWorkshopAdmin]

    def post(self, request: Request, order_id: str) -> Response:
        ser = AssignMechanicSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        try:
            order = services.get_order_for_centre(order_id, request.user)
        except (services.NotFoundError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        try:
            mechanic = User.objects.get(id=ser.validated_data["mechanic_id"], is_active=True)
        except User.DoesNotExist:
            return Response({"detail": "Mechanic not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            order = services.assign_mechanic(order, mechanic, request.user)
        except services.ServiceOrderError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(ServiceOrderSerializer(order).data)


class ServiceOrderEventsView(APIView):
    """GET /api/v1/service-orders/<id>/events/"""
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, order_id: str) -> Response:
        try:
            events = services.get_order_events(order_id, request.user)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except services.PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        return Response(ServiceOrderEventSerializer(events, many=True).data)


class MechanicOrderListView(APIView):
    """GET /api/v1/mechanic/orders/"""
    permission_classes = [IsAuthenticated, IsMechanic]

    def get(self, request: Request) -> Response:
        orders = services.get_orders_for_mechanic(request.user)
        return Response(ServiceOrderSerializer(orders, many=True).data)
