"""VEDA V2 — components URLs"""

from django.urls import path
from .views import ComponentListView, ComponentDetailView

app_name = "components"

urlpatterns = [
    path("",             ComponentListView.as_view(),  name="list"),
    path("<str:code>/",  ComponentDetailView.as_view(), name="detail"),
]
