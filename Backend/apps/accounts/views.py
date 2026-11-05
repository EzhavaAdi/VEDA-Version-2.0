"""
VEDA V2 — accounts views

Thin API views — all logic delegated to services.py.
Views handle HTTP concerns only: request parsing, response formatting, error mapping.

Endpoints:
    POST /api/v1/auth/request-otp/     — Step 1: request OTP
    POST /api/v1/auth/verify-otp/      — Step 2: verify OTP, receive JWT
    POST /api/v1/auth/token/refresh/   — Refresh access token (simplejwt)
    GET  /api/v1/auth/me/              — Current user profile
    PATCH /api/v1/auth/me/             — Update profile (onboarding)
"""

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services
from .serializers import (
    RequestOTPSerializer,
    VerifyOTPSerializer,
    ProfileSetupSerializer,
    UserSerializer,
)

logger = logging.getLogger("veda.accounts")


# ---------------------------------------------------------------------------
# Request OTP
# ---------------------------------------------------------------------------

class RequestOTPView(APIView):
    """
    POST /api/v1/auth/request-otp/

    Accepts a phone number, creates the user if new, generates and
    delivers a 6-digit OTP via the configured provider.

    Body: { "phone_number": "+919876543210" }
    """
    permission_classes = [AllowAny]
    throttle_scope     = "otp_request"

    def post(self, request: Request) -> Response:
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]

        try:
            result = services.request_otp(phone_number)
        except services.AuthError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except NotImplementedError as e:
            logger.error(f"OTP delivery not implemented: {e}")
            return Response(
                {"detail": "OTP delivery is not configured on this server."},
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )

        return Response(
            {
                "detail": "OTP sent successfully.",
                "phone_number": result["phone_number"],
                "is_new_user": result["is_new_user"],
                "expires_in_seconds": result["expires_in_seconds"],
            },
            status=status.HTTP_200_OK,
        )


# ---------------------------------------------------------------------------
# Verify OTP
# ---------------------------------------------------------------------------

class VerifyOTPView(APIView):
    """
    POST /api/v1/auth/verify-otp/

    Verifies the OTP and returns JWT access + refresh tokens.

    Body: { "phone_number": "+919876543210", "code": "123456" }

    Response:
    {
        "access": "...",
        "refresh": "...",
        "user": { id, phone_number, full_name, roles, is_new_user }
    }
    """
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        code         = serializer.validated_data["code"]

        try:
            result = services.verify_otp(phone_number, code)
        except services.OTPExpiredError as e:
            return Response({"detail": str(e)}, status=status.HTTP_410_GONE)
        except services.OTPMaxAttemptsError as e:
            return Response({"detail": str(e)}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except services.OTPInvalidError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except services.AuthError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# Current user — GET and PATCH
# ---------------------------------------------------------------------------

class MeView(APIView):
    """
    GET  /api/v1/auth/me/   — Return current user profile.
    PATCH /api/v1/auth/me/  — Update full_name (profile onboarding).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request) -> Response:
        serializer = ProfileSetupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = services.update_profile(
                user=request.user,
                full_name=serializer.validated_data["full_name"],
            )
        except services.AuthError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
