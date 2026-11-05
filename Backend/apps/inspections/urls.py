"""VEDA V2 — inspections URLs (nested under service-orders)"""

from django.urls import path
from .views import (
    InspectionView,
    CompleteInspectionView,
    InspectionItemListView,
    SensorReadingListView,
)

app_name = "inspections"

urlpatterns = [
    path("<uuid:order_id>/inspection/",             InspectionView.as_view(),         name="inspection"),
    path("<uuid:order_id>/inspection/complete/",    CompleteInspectionView.as_view(),  name="complete"),
    path("<uuid:order_id>/inspection/items/",       InspectionItemListView.as_view(),  name="items"),
    path("<uuid:order_id>/inspection/readings/",    SensorReadingListView.as_view(),   name="readings"),
]
