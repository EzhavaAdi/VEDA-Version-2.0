"""VEDA V2 — vehicles URLs"""

from django.urls import path
from .views import VehicleListCreateView, VehicleDetailView, VehicleComponentListView

app_name = "vehicles"

urlpatterns = [
    path("",                         VehicleListCreateView.as_view(),  name="list-create"),
    path("<uuid:vehicle_id>/",       VehicleDetailView.as_view(),      name="detail"),
    path("<uuid:vehicle_id>/components/", VehicleComponentListView.as_view(), name="components"),
]
