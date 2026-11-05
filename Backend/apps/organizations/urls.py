"""VEDA V2 — organizations URLs"""

from django.urls import path
from .views import (
    ServiceCentreListView,
    ServiceCentreDetailView,
    MyCentresView,
    WorkshopMemberListView,
)

app_name = "organizations"

urlpatterns = [
    path("",                              ServiceCentreListView.as_view(),   name="list-create"),
    path("mine/",                         MyCentresView.as_view(),           name="mine"),
    path("<uuid:centre_id>/",             ServiceCentreDetailView.as_view(), name="detail"),
    path("<uuid:centre_id>/members/",     WorkshopMemberListView.as_view(),  name="members"),
]
