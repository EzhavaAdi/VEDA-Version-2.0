"""
VEDA V2 — accounts URL configuration

All auth endpoints are under /api/v1/auth/
Token refresh is handled by simplejwt's built-in view.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MeView, RequestOTPView, VerifyOTPView

app_name = "accounts"

urlpatterns = [
    # Step 1 — request OTP
    path("request-otp/", RequestOTPView.as_view(), name="request-otp"),

    # Step 2 — verify OTP, receive JWT
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),

    # Refresh access token using refresh token
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    # Authenticated user profile
    path("me/", MeView.as_view(), name="me"),
]
