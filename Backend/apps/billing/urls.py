"""VEDA V2 — billing URLs"""
from django.urls import path
from .views import InvoiceView, ProcessPaymentView, DeliverVehicleView

app_name = "billing"

urlpatterns = [
    path("<uuid:order_id>/invoice/",   InvoiceView.as_view(),       name="invoice"),
    path("<uuid:order_id>/deliver/",   DeliverVehicleView.as_view(), name="deliver"),
    path("invoices/<uuid:invoice_id>/pay/", ProcessPaymentView.as_view(), name="pay"),
]
