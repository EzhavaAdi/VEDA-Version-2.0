"""VEDA V2 — digital_twin URLs"""
from django.urls import path
from .views import AssetListView, AssetDetailView, SceneStateView

app_name = "digital_twin"

urlpatterns = [
    path("assets/",                       AssetListView.as_view(),   name="assets"),
    path("assets/<uuid:asset_id>/",       AssetDetailView.as_view(), name="asset-detail"),
    path("assets/<uuid:asset_id>/scene/", SceneStateView.as_view(),  name="scene-state"),
]
