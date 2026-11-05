"""VEDA V2 — billing views"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsOwner, IsWorkshopMember

from . import services
from .serializers import InvoiceSerializer, ProcessPaymentSerializer


class InvoiceView(APIView):
    """
    GET  /api/v1/service-orders/<order_id>/invoice/  — get invoice
    POST /api/v1/service-orders/<order_id>/invoice/  — generate invoice (workshop)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, order_id: str) -> Response:
        try:
            invoice = services.get_invoice(str(order_id), request.user)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except services.PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        return Response(InvoiceSerializer(invoice).data)

    def post(self, request: Request, order_id: str) -> Response:
        try:
            invoice = services.generate_invoice(str(order_id), request.user)
        except services.BillingError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except services.PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(InvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)


class ProcessPaymentView(APIView):
    """POST /api/v1/invoices/<invoice_id>/pay/  — owner initiates payment"""
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request: Request, invoice_id: str) -> Response:
        ser = ProcessPaymentSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ref = ser.validated_data.get("transaction_reference") or None
        try:
            payment = services.process_payment(str(invoice_id), request.user, ref)
        except services.PaymentError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except services.PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except services.NotFoundError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        from .serializers import PaymentSerializer
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)


class DeliverVehicleView(APIView):
    """POST /api/v1/service-orders/<order_id>/deliver/"""
    permission_classes = [IsAuthenticated, IsWorkshopMember]

    def post(self, request: Request, order_id: str) -> Response:
        try:
            order = services.deliver_vehicle(str(order_id), request.user)
        except services.BillingError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (services.PermissionError, services.NotFoundError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        from apps.service_orders.serializers import ServiceOrderSerializer
        return Response(ServiceOrderSerializer(order).data)
