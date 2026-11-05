"""VEDA V2 — components views (read-only catalogue)"""

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services
from .serializers import ComponentSerializer, ComponentTreeSerializer


class ComponentListView(APIView):
    """
    GET /api/v1/components/
    Query params:
        system=ENGINE|AIR_SYSTEM|...
        tree=1  — include children
    """
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        system   = request.query_params.get("system")
        use_tree = request.query_params.get("tree") == "1"

        if use_tree:
            components = services.get_root_components(system=system)
            return Response(ComponentTreeSerializer(components, many=True).data)

        components = services.get_catalogue(system=system)
        return Response(ComponentSerializer(components, many=True).data)


class ComponentDetailView(APIView):
    """
    GET /api/v1/components/<code>/
    """
    permission_classes = [AllowAny]

    def get(self, request: Request, code: str) -> Response:
        try:
            component = services.get_component_by_code(code)
        except services.ComponentError as e:
            from rest_framework import status
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(ComponentSerializer(component).data)
