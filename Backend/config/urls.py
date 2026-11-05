"""
VEDA V2 — Root URL configuration

All API endpoints are under /api/v1/
Django admin is available at /admin/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),

    # API v1 — Authentication
    path("api/v1/auth/",             include("apps.accounts.urls",      namespace="accounts")),

    # API v1 — Phase 2
    path("api/v1/vehicles/",         include("apps.vehicles.urls",      namespace="vehicles")),
    path("api/v1/service-centres/",  include("apps.organizations.urls", namespace="organizations")),
    path("api/v1/components/",       include("apps.components.urls",    namespace="components")),

    # API v1 — Phase 3
    path("api/v1/service-orders/",   include("apps.service_orders.urls", namespace="service_orders")),
    path("api/v1/service-orders/",   include("apps.inspections.urls",    namespace="inspections")),

    # API v1 — Phase 4
    path("api/v1/diagnosis/",        include("apps.diagnosis.urls",      namespace="diagnosis")),
    path("api/v1/service-orders/",   include("apps.diagnosis.urls",      namespace="diagnosis_orders")),

    # API v1 — Phase 5
    path("api/v1/digital-twin/",     include("apps.digital_twin.urls",   namespace="digital_twin")),

    # API v1 — Phase 6
    path("api/v1/parts/",            include("apps.inventory.urls",      namespace="inventory")),
    path("api/v1/service-orders/",   include("apps.estimates.urls",      namespace="estimates")),
    path("api/v1/",                  include("apps.estimates.urls",      namespace="estimates_standalone")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
