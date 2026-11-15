"""VEDA V2 — diagnosis URLs"""

from django.urls import path
from .views import AIModelListView, RunDiagnosisView, DiagnosisResultView, VerifyDiagnosisCaseView
from .demo_view import APSDemoInferenceView
from .mechanic_demo_view import MechanicDemoView

app_name = "diagnosis"

urlpatterns = [
    path("models/",                              AIModelListView.as_view(),         name="models"),
    path("demo/",                                APSDemoInferenceView.as_view(),    name="demo"),
    path("mechanic-demo/",                       MechanicDemoView.as_view(),        name="mechanic-demo"),
    path("<uuid:order_id>/diagnosis/",           DiagnosisResultView.as_view(),     name="result"),
    path("<uuid:order_id>/diagnosis/run/",       RunDiagnosisView.as_view(),        name="run"),
    path("cases/<uuid:case_id>/verify/",         VerifyDiagnosisCaseView.as_view(), name="verify"),
]
