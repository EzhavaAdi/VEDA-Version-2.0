"""VEDA V2 — work_orders URLs"""
from django.urls import path
from .views import WorkOrderView, CompleteWorkOrderView, UpdateWorkOrderItemView

app_name = "work_orders"

urlpatterns = [
    # Nested under service-orders
    path("<uuid:order_id>/work-order/",            WorkOrderView.as_view(),           name="work-order"),
    # Standalone work-order actions
    path("work-orders/<uuid:work_order_id>/complete/", CompleteWorkOrderView.as_view(), name="complete"),
    path("work-order-items/<uuid:item_id>/",        UpdateWorkOrderItemView.as_view(), name="update-item"),
]
