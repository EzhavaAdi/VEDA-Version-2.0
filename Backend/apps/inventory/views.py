"""VEDA V2 — inventory views"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsWorkshopAdmin, IsWorkshopMember
from apps.organizations.services import get_centre_for_member, CentreNotFoundError

from . import services
from .serializers import (
    PartCatalogSerializer, PartCompatibilitySerializer,
    WorkshopInventorySerializer, AddStockSerializer,
)


class PartListView(APIView):
    """GET /api/v1/parts/?search=<term>"""
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        parts = services.get_parts(search=request.query_params.get("search"))
        return Response(PartCatalogSerializer(parts, many=True).data)


class CompatiblePartsView(APIView):
    """GET /api/v1/parts/compatible/<component_code>/"""
    permission_classes = [AllowAny]

    def get(self, request: Request, component_code: str) -> Response:
        compat = services.get_compatible_parts(component_code)
        return Response(PartCompatibilitySerializer(compat, many=True).data)


class WorkshopInventoryView(APIView):
    """
    GET  /api/v1/service-centres/<id>/inventory/
    POST /api/v1/service-centres/<id>/inventory/  — add / update stock (admin only)
    """
    permission_classes = [IsAuthenticated, IsWorkshopMember]

    def get(self, request: Request, centre_id: str) -> Response:
        try:
            centre = get_centre_for_member(str(centre_id), request.user)
        except CentreNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        in_stock = request.query_params.get("in_stock") == "1"
        inv = services.get_inventory(centre, in_stock_only=in_stock)
        return Response(WorkshopInventorySerializer(inv, many=True).data)

    def post(self, request: Request, centre_id: str) -> Response:
        from apps.accounts.permissions import IsWorkshopAdmin
        if not request.user.has_role("WORKSHOP_ADMIN"):
            return Response({"detail": "Workshop admin required."}, status=status.HTTP_403_FORBIDDEN)
        try:
            from apps.organizations.services import get_centre_for_admin
            centre = get_centre_for_admin(str(centre_id), request.user)
        except CentreNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        ser = AddStockSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        d = ser.validated_data
        try:
            inv = services.add_or_update_stock(
                centre, str(d["part_id"]), d["quantity"], d["unit_price"], request.user
            )
        except (services.InventoryError, services.NotFoundError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(WorkshopInventorySerializer(inv).data, status=status.HTTP_201_CREATED)
