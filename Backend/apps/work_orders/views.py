"""VEDA V2 — work_orders views"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsWorkshopMember

from . import services
from .serializers import WorkOrderSerializer, UpdateItemSerializer


class WorkOrderView(APIView):
    """
    GET  /api/v1/service-orders/<order_id>/work-order/  — get work order
    POST /api/v1/service-orders/<order_id>/work-order/  — create from approved items
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, order_id: str) -> Response:
        try:
            wo = services.get_work_order(str(order_id), request.user)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except services.PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        return Response(WorkOrderSerializer(wo).data)

    def post(self, request: Request, order_id: str) -> Response:
        try:
            wo = services.create_work_order(str(order_id), request.user)
        except services.WorkOrderError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except services.PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(WorkOrderSerializer(wo).data, status=status.HTTP_201_CREATED)


class CompleteWorkOrderView(APIView):
    """POST /api/v1/work-orders/<work_order_id>/complete/"""
    permission_classes = [IsAuthenticated, IsWorkshopMember]

    def post(self, request: Request, work_order_id: str) -> Response:
        try:
            wo = services.complete_work_order(str(work_order_id), request.user)
        except (services.WorkOrderError, services.PermissionError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(WorkOrderSerializer(wo).data)


class UpdateWorkOrderItemView(APIView):
    """PATCH /api/v1/work-order-items/<item_id>/"""
    permission_classes = [IsAuthenticated, IsWorkshopMember]

    def patch(self, request: Request, item_id: str) -> Response:
        ser = UpdateItemSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            item = services.update_item_progress(
                str(item_id), request.user,
                ser.validated_data["status"],
                ser.validated_data.get("notes", ""),
            )
        except services.WorkOrderError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except services.PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        from .serializers import WorkOrderItemSerializer
        return Response(WorkOrderItemSerializer(item).data)
