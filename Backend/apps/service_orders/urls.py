"""VEDA V2 — service_orders URLs"""

from django.urls import path
from .views import (
    OwnerServiceOrderListView,
    OwnerServiceOrderDetailView,
    CentreServiceOrderListView,
    CentreServiceOrderDetailView,
    TransitionOrderView,
    AssignMechanicView,
    ServiceOrderEventsView,
    MechanicOrderListView,
)

app_name = "service_orders"

urlpatterns = [
    # Owner
    path("",                                          OwnerServiceOrderListView.as_view(),   name="list-create"),
    path("<uuid:order_id>/",                          OwnerServiceOrderDetailView.as_view(), name="detail"),
    path("<uuid:order_id>/transition/",               TransitionOrderView.as_view(),         name="transition"),
    path("<uuid:order_id>/assign-mechanic/",          AssignMechanicView.as_view(),          name="assign-mechanic"),
    path("<uuid:order_id>/events/",                   ServiceOrderEventsView.as_view(),      name="events"),

    # Mechanic
    path("mechanic/",                                 MechanicOrderListView.as_view(),       name="mechanic-list"),
]
