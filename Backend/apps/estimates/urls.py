"""VEDA V2 — estimates URLs"""
from django.urls import path
from .views import (
    EstimateListCreateView, EstimateDetailView,
    AddEstimateItemView, SubmitEstimateView, ItemDecisionView,
)

app_name = "estimates"

urlpatterns = [
    # Nested under service-orders
    path("<uuid:order_id>/estimates/",              EstimateListCreateView.as_view(), name="list-create"),
    # Standalone estimate access
    path("estimates/<uuid:estimate_id>/",            EstimateDetailView.as_view(),    name="detail"),
    path("estimates/<uuid:estimate_id>/items/",      AddEstimateItemView.as_view(),   name="add-item"),
    path("estimates/<uuid:estimate_id>/submit/",     SubmitEstimateView.as_view(),    name="submit"),
    # Owner item decision
    path("estimate-items/<uuid:item_id>/decide/",    ItemDecisionView.as_view(),      name="decide"),
]
