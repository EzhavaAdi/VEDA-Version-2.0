"""
VEDA V2 — accounts service layer

All business logic lives here. Views call services — never direct ORM.

Responsibilities:
- Request OTP (create user if new, generate and deliver OTP)
- Verify OTP (validate, issue JWT tokens)
- Refresh token handling delegated to simplejwt views
- Role management helpers
"""

import logging
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTP, Role, User, UserRole

logger = logging.getLogger("veda.accounts")


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class AuthError(Exception):
    """Base authentication error."""
    pass

class OTPRateLimitError(AuthError):
    """Too many OTP requests in a short window."""
    pass

class OTPInvalidError(AuthError):
    """OTP code is wrong."""
    pass

class OTPExpiredError(AuthError):
    """OTP has expired."""
    pass

class OTPMaxAttemptsError(AuthError):
    """Too many failed verification attempts."""
    pass

class OTPAlreadyUsedError(AuthError):
    """OTP has already been consumed."""
    pass


# ---------------------------------------------------------------------------
# OTP delivery
# ---------------------------------------------------------------------------

def _deliver_otp(phone_number: str, raw_code: str) -> None:
    """
    Deliver OTP to the user.
    CONSOLE provider: print to stdout (development only).
    SMS provider: integrate a real SMS gateway in production.
    Never enable CONSOLE in production.
    """
    provider = getattr(settings, "OTP_PROVIDER", "CONSOLE")

    if provider == "CONSOLE":
        # Development-only — visible in runserver terminal
        logger.info("=" * 50)
        logger.info(f"[DEV OTP] Phone: {phone_number}  Code: {raw_code}")
        logger.info("=" * 50)
    else:
        # Production: integrate SMS provider here (Phase 9+)
        raise NotImplementedError(
            f"SMS OTP provider '{provider}' is not yet implemented. "
            "Configure OTP_PROVIDER=CONSOLE for local development."
        )


# ---------------------------------------------------------------------------
# Request OTP
# ---------------------------------------------------------------------------

@transaction.atomic
def request_otp(phone_number: str) -> dict:
    """
    Step 1 of authentication.

    - Creates a new User if the phone number is not registered.
    - Invalidates any existing active OTP for this user.
    - Generates a new 6-digit OTP.
    - Hashes and stores it.
    - Delivers it via the configured provider.

    Returns:
        {"phone_number": str, "is_new_user": bool}
    """
    phone_number = phone_number.strip().replace(" ", "").replace("-", "")

    user, created = User.objects.get_or_create(
        phone_number=phone_number,
        defaults={"full_name": ""},
    )

    if not user.is_active:
        raise AuthError("This account has been deactivated.")

    # Invalidate all existing unused OTPs for this user
    OTP.objects.filter(user=user, is_used=False).update(is_used=True)

    # Generate and store new OTP
    raw_code = OTP.generate_code()
    otp = OTP.objects.create(
        user=user,
        code_hash=OTP.hash_code(raw_code),
    )

    logger.info(f"OTP created for {phone_number} (new_user={created}, otp_id={otp.id})")

    # Deliver
    _deliver_otp(phone_number, raw_code)

    return {
        "phone_number": phone_number,
        "is_new_user": created,
        "expires_in_seconds": getattr(settings, "OTP_EXPIRY_SECONDS", 300),
    }


# ---------------------------------------------------------------------------
# Verify OTP
# ---------------------------------------------------------------------------

@transaction.atomic
def verify_otp(phone_number: str, raw_code: str) -> dict:
    """
    Step 2 of authentication.

    - Finds the most recent active OTP for this phone number.
    - Validates expiry and attempt count before checking the code.
    - On success: returns JWT access + refresh tokens and user data.
    - On failure: raises a descriptive AuthError subclass.

    Returns:
        {
            "access": str,
            "refresh": str,
            "user": {id, phone_number, full_name, roles},
            "is_new_user": bool,
        }
    """
    phone_number = phone_number.strip().replace(" ", "").replace("-", "")

    try:
        user = User.objects.get(phone_number=phone_number, is_active=True)
    except User.DoesNotExist:
        raise AuthError("No account found for this phone number.")

    # Find the latest unused OTP
    otp = (
        OTP.objects
        .filter(user=user, is_used=False)
        .order_by("-created_at")
        .first()
    )

    if otp is None:
        raise AuthError("No active OTP found. Please request a new one.")

    if otp.is_expired():
        raise OTPExpiredError("OTP has expired. Please request a new one.")

    max_attempts = getattr(settings, "OTP_MAX_ATTEMPTS", 5)
    if otp.attempt_count >= max_attempts:
        raise OTPMaxAttemptsError("Too many failed attempts. Please request a new OTP.")

    # Verify — this increments attempt_count internally
    if not otp.verify(raw_code):
        remaining = max_attempts - otp.attempt_count
        raise OTPInvalidError(
            f"Incorrect code. {remaining} attempt{'s' if remaining != 1 else ''} remaining."
        )

    # Issue JWT tokens
    refresh = RefreshToken.for_user(user)

    roles = user.get_roles()
    is_new_user = not bool(user.full_name)

    logger.info(f"OTP verified for {phone_number} (user_id={user.id})")

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": str(user.id),
            "phone_number": user.phone_number,
            "full_name": user.full_name,
            "roles": roles,
            "is_new_user": is_new_user,
        },
    }


# ---------------------------------------------------------------------------
# Profile update
# ---------------------------------------------------------------------------

@transaction.atomic
def update_profile(user: User, full_name: str) -> User:
    """Update the user's full name (called during onboarding)."""
    if not full_name or not full_name.strip():
        raise AuthError("Full name cannot be empty.")
    user.full_name = full_name.strip()
    user.save(update_fields=["full_name", "updated_at"])
    logger.info(f"Profile updated for user {user.id}")
    return user


# ---------------------------------------------------------------------------
# Role management
# ---------------------------------------------------------------------------

@transaction.atomic
def assign_role(user: User, role: str) -> Role:
    """Assign a role to a user. Idempotent."""
    if role not in UserRole.values:
        raise AuthError(f"Invalid role: {role}")
    role_obj, created = Role.objects.get_or_create(user=user, role=role)
    if created:
        logger.info(f"Role {role} assigned to user {user.id}")
    return role_obj


@transaction.atomic
def remove_role(user: User, role: str) -> None:
    """Remove a role from a user."""
    Role.objects.filter(user=user, role=role).delete()
    logger.info(f"Role {role} removed from user {user.id}")


def get_user_by_id(user_id: str) -> User:
    try:
        return User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist:
        raise AuthError("User not found.")
