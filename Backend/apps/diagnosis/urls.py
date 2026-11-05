"""VEDA V2 — diagnosis URLs"""

from django.urls import path
from .views import AIModelListView, RunDiagnosisView, DiagnosisResultView, VerifyDiagnosisCaseView

app_name = "diagnosis"

urlpatterns = [
    # AI model registry
    path("models/",                              AIModelListView.as_view(),         name="models"),

    # Per-service-order diagnosis
    path("<uuid:order_id>/diagnosis/",           DiagnosisResultView.as_view(),     name="result"),
    path("<uuid:order_id>/diagnosis/run/",       RunDiagnosisView.as_view(),        name="run"),

    # Mechanic verification
    path("cases/<uuid:case_id>/verify/",         VerifyDiagnosisCaseView.as_view(), name="verify"),
]
