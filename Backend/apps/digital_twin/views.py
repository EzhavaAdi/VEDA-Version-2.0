"""VEDA V2 — digital_twin views"""

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from . import services
from .serializers import Asset3DSerializer


class AssetListView(APIView):
    """GET /api/v1/digital-twin/assets/ — list all active 3D assets"""
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        assets = services.get_active_assets()
        return Response(Asset3DSerializer(assets, many=True).data)


class AssetDetailView(APIView):
    """GET /api/v1/digital-twin/assets/<id>/ — asset with mesh mappings"""
    permission_classes = [AllowAny]

    def get(self, request: Request, asset_id: str) -> Response:
        try:
            asset = services.get_asset_with_mappings(str(asset_id))
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(Asset3DSerializer(asset).data)


class SceneStateView(APIView):
    """
    GET /api/v1/digital-twin/assets/<id>/scene/?order_id=<uuid>

    Returns mesh_identifier -> visual_state for all mapped meshes,
    applying diagnosis case states where available.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, asset_id: str) -> Response:
        order_id = request.query_params.get("order_id")
        diagnosis_cases = []

        if order_id:
            from apps.diagnosis.services import get_diagnosis_for_order
            from apps.diagnosis.services import PermissionError, NotFoundError
            try:
                data = get_diagnosis_for_order(order_id, request.user)
                diagnosis_cases = [
                    {
                        "component_code":      c.component.component_code,
                        "diagnosis_status":    c.diagnosis_status,
                        "mechanic_verification": c.mechanic_verification,
                    }
                    for c in data["cases"]
                ]
            except (PermissionError, NotFoundError):
                pass

        try:
            scene = services.build_scene_state(str(asset_id), diagnosis_cases)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response({"asset_id": str(asset_id), "scene": scene})
