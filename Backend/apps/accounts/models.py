"""
VEDA V2 — accounts models

Custom User model (phone-number-based, no username field) plus
role management and OTP verification tracking.

All primary keys use UUID for security and future-proofing.
"""

import uuid
import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


# ---------------------------------------------------------------------------
# Role constants
# ---------------------------------------------------------------------------

class UserRole(models.TextChoices):
    OWNER          = "OWNER",          "Vehicle Owner"
    WORKSHOP_ADMIN = "WORKSHOP_ADMIN", "Workshop Administrator"
    MECHANIC       = "MECHANIC",       "Mechanic"
    VEDA_ADMIN     = "VEDA_ADMIN",     "VEDA Administrator"


# ---------------------------------------------------------------------------
# Custom User Manager
# ---------------------------------------------------------------------------

class UserManager(BaseUserManager):
    """Manager for phone-number-based authentication."""

    def create_user(self, phone_number: str, full_name: str = "", password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required.")
        phone_number = self._normalise_phone(phone_number)
        user = self.model(phone_number=phone_number, full_name=full_name, **extra_fields)
        # VEDA uses OTP — password is unusable by default for regular users
        user.set_unusable_password()
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number: str, full_name: str = "", password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if not password:
            raise ValueError("Superuser must have a password.")
        user = self.create_user(phone_number, full_name, password=password, **extra_fields)
        # Assign VEDA_ADMIN role
        Role.objects.get_or_create(user=user, role=UserRole.VEDA_ADMIN)
        return user

    @staticmethod
    def _normalise_phone(phone: str) -> str:
        """Strip whitespace and ensure consistent storage format."""
        return phone.strip().replace(" ", "").replace("-", "")


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class User(AbstractBaseUser, PermissionsMixin):
    """
    Central user account.

    Authentication is phone-number + OTP.
    Password is set only for Django admin superusers.
    """

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number   = models.CharField(max_length=20, unique=True, db_index=True)
    full_name      = models.CharField(max_length=150, blank=True)
    is_active      = models.BooleanField(default=True)
    is_staff       = models.BooleanField(default=False)   # Django admin access
    created_at     = models.DateTimeField(default=timezone.now)
    updated_at     = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD  = "phone_number"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        db_table    = "accounts_user"
        verbose_name = "User"
        ordering    = ["-created_at"]

    def __str__(self):
        return f"{self.phone_number} ({self.full_name or 'unnamed'})"

    def get_roles(self) -> list[str]:
        return list(self.roles.values_list("role", flat=True))

    def has_role(self, role: str) -> bool:
        return self.roles.filter(role=role).exists()


# ---------------------------------------------------------------------------
# Role
# ---------------------------------------------------------------------------

class Role(models.Model):
    """
    User-role assignment.
    A user may hold multiple roles (e.g. WORKSHOP_ADMIN + MECHANIC).
    """

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="roles",
    )
    role       = models.CharField(max_length=30, choices=UserRole.choices)
    assigned_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table        = "accounts_role"
        unique_together = [("user", "role")]
        verbose_name    = "User Role"

    def __str__(self):
        return f"{self.user.phone_number} — {self.role}"


# ---------------------------------------------------------------------------
# OTP
# ---------------------------------------------------------------------------

def _otp_expiry():
    """Return the expiry timestamp based on settings."""
    expiry_seconds = getattr(settings, "OTP_EXPIRY_SECONDS", 300)
    return timezone.now() + timedelta(seconds=expiry_seconds)


class OTP(models.Model):
    """
    One-time password record.

    The raw OTP code is NEVER stored — only its SHA-256 hash.
    Expiry and attempt limits are enforced at the service layer.
    """

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user           = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="otps",
    )
    # Hashed OTP — SHA-256 of the raw 6-digit code
    code_hash      = models.CharField(max_length=64)
    expires_at     = models.DateTimeField(default=_otp_expiry)
    is_used        = models.BooleanField(default=False)
    attempt_count  = models.PositiveSmallIntegerField(default=0)
    created_at     = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table   = "accounts_otp"
        verbose_name = "OTP"
        ordering   = ["-created_at"]

    def __str__(self):
        status = "used" if self.is_used else ("expired" if self.is_expired() else "active")
        return f"OTP({self.user.phone_number}, {status})"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at

    def is_valid(self) -> bool:
        max_attempts = getattr(settings, "OTP_MAX_ATTEMPTS", 5)
        return (
            not self.is_used
            and not self.is_expired()
            and self.attempt_count < max_attempts
        )

    def verify(self, raw_code: str) -> bool:
        """
        Check raw code against stored hash.
        Increments attempt_count regardless of result.
        Marks is_used=True on success.
        """
        self.attempt_count += 1
        code_hash = hashlib.sha256(raw_code.encode()).hexdigest()
        if code_hash == self.code_hash:
            self.is_used = True
            self.save(update_fields=["attempt_count", "is_used"])
            return True
        self.save(update_fields=["attempt_count"])
        return False

    @staticmethod
    def hash_code(raw_code: str) -> str:
        return hashlib.sha256(raw_code.encode()).hexdigest()

    @staticmethod
    def generate_code() -> str:
        """Generate a cryptographically random 6-digit code."""
        return str(secrets.randbelow(900000) + 100000)  # 100000–999999
