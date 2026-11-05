"""VEDA V2 — inventory URLs"""
from django.urls import path
from .views import PartListView, CompatiblePartsView, WorkshopInventoryView

app_name = "inventory"

urlpatterns = [
    path("",                                       PartListView.as_view(),         name="parts"),
    path("compatible/<str:component_code>/",       CompatiblePartsView.as_view(),  name="compatible"),
    path("centres/<uuid:centre_id>/inventory/",    WorkshopInventoryView.as_view(), name="workshop-inventory"),
]
