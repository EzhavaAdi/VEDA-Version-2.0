"""VEDA V2 — vehicles views"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsOwner
from apps.components.serializers import VehicleComponentSerializer, VehicleComponentCreateSerializer
from apps.components import services as comp_services

from . import services
from .serializers import VehicleSerializer, VehicleCreateSerializer, VehicleUpdateSerializer


class VehicleListCreateView(APIView):
    """
    GET  /api/v1/vehicles/         — List owner's vehicles
    POST /api/v1/vehicles/         — Register a new vehicle
    """
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request: Request) -> Response:
        vehicles = services.get_owner_vehicles(request.user)
        return Response(VehicleSerializer(vehicles, many=True).data)

    def post(self, request: Request) -> Response:
        serializer = VehicleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            vehicle = services.register_vehicle(request.user, serializer.validated_data)
        except services.VehicleError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(VehicleSerializer(vehicle).data, status=status.HTTP_201_CREATED)


class VehicleDetailView(APIView):
    """
    GET    /api/v1/vehicles/<id>/  — Get vehicle detail
    PATCH  /api/v1/vehicles/<id>/  — Update vehicle (odometer, notes, etc.)
    DELETE /api/v1/vehicles/<id>/  — Deactivate vehicle
    """
    permission_classes = [IsAuthenticated, IsOwner]

    def _get_vehicle(self, request, vehicle_id):
        try:
            return services.get_vehicle_for_owner(vehicle_id, request.user), None
        except services.VehicleNotFoundError:
            return None, Response({"detail": "Vehicle not found."}, status=status.HTTP_404_NOT_FOUND)
        except services.VehiclePermissionError:
            return None, Response({"detail": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request: Request, vehicle_id: str) -> Response:
        vehicle, err = self._get_vehicle(request, vehicle_id)
        if err:
            return err
        return Response(VehicleSerializer(vehicle).data)

    def patch(self, request: Request, vehicle_id: str) -> Response:
        vehicle, err = self._get_vehicle(request, vehicle_id)
        if err:
            return err
        serializer = VehicleUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        vehicle = services.update_vehicle(vehicle, serializer.validated_data)
        return Response(VehicleSerializer(vehicle).data)

    def delete(self, request: Request, vehicle_id: str) -> Response:
        vehicle, err = self._get_vehicle(request, vehicle_id)
        if err:
            return err
        services.deactivate_vehicle(vehicle)
        return Response({"detail": "Vehicle deactivated."}, status=status.HTTP_204_NO_CONTENT)


class VehicleComponentListView(APIView):
    """
    GET  /api/v1/vehicles/<id>/components/         — List components on this vehicle
    POST /api/v1/vehicles/<id>/components/         — Add a component
    """
    permission_classes = [IsAuthenticated, IsOwner]

    def _get_vehicle(self, request, vehicle_id):
        try:
            return services.get_vehicle_for_owner(vehicle_id, request.user), None
        except (services.VehicleNotFoundError, services.VehiclePermissionError) as e:
            return None, Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, vehicle_id: str) -> Response:
        vehicle, err = self._get_vehicle(request, vehicle_id)
        if err:
            return err
        components = comp_services.get_vehicle_components(vehicle)
        return Response(VehicleComponentSerializer(components, many=True).data)

    def post(self, request: Request, vehicle_id: str) -> Response:
        vehicle, err = self._get_vehicle(request, vehicle_id)
        if err:
            return err
        serializer = VehicleComponentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            vc = comp_services.add_vehicle_component(
                vehicle,
                serializer.validated_data["component_code"],
                serializer.validated_data.get("installation_date"),
                serializer.validated_data.get("notes", ""),
            )
        except comp_services.ComponentError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(VehicleComponentSerializer(vc).data, status=status.HTTP_201_CREATED)
