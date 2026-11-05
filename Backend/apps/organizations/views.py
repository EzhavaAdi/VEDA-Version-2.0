"""VEDA V2 — organizations views"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsWorkshopAdmin, IsVedaAdmin

from . import services
from .serializers import (
    ServiceCentreSerializer,
    ServiceCentreCreateSerializer,
    WorkshopMembershipSerializer,
    AddMemberSerializer,
)


class ServiceCentreListView(APIView):
    """
    GET  /api/v1/service-centres/          — Public list of verified centres
    POST /api/v1/service-centres/          — Register a new service centre
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request: Request) -> Response:
        centres = services.get_verified_centres()
        return Response(ServiceCentreSerializer(centres, many=True).data)

    def post(self, request: Request) -> Response:
        serializer = ServiceCentreCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            centre = services.register_service_centre(request.user, serializer.validated_data)
        except services.OrganizationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ServiceCentreSerializer(centre).data, status=status.HTTP_201_CREATED)


class MyCentresView(APIView):
    """
    GET /api/v1/service-centres/mine/  — Centres the current user belongs to
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        centres = services.get_user_centres(request.user)
        return Response(ServiceCentreSerializer(centres, many=True).data)


class ServiceCentreDetailView(APIView):
    """
    GET   /api/v1/service-centres/<id>/   — Centre detail (member access)
    PATCH /api/v1/service-centres/<id>/   — Update centre (VEDA admin only for now)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, centre_id: str) -> Response:
        try:
            centre = services.get_centre_for_member(centre_id, request.user)
        except services.CentreNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(ServiceCentreSerializer(centre).data)


class WorkshopMemberListView(APIView):
    """
    GET  /api/v1/service-centres/<id>/members/  — List members
    POST /api/v1/service-centres/<id>/members/  — Add a member
    """
    permission_classes = [IsAuthenticated, IsWorkshopAdmin]

    def get(self, request: Request, centre_id: str) -> Response:
        try:
            centre = services.get_centre_for_admin(centre_id, request.user)
        except services.CentreNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        members = services.get_centre_members(centre)
        return Response(WorkshopMembershipSerializer(members, many=True).data)

    def post(self, request: Request, centre_id: str) -> Response:
        try:
            centre = services.get_centre_for_admin(centre_id, request.user)
        except services.CentreNotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            membership = services.add_member(
                centre,
                request.user,
                serializer.validated_data["phone_number"],
                serializer.validated_data["designation"],
            )
        except services.MembershipError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(WorkshopMembershipSerializer(membership).data, status=status.HTTP_201_CREATED)
