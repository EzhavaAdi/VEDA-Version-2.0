"""
VEDA V2 — organizations models

ServiceCentre: registered workshop.
WorkshopMembership: links a User (WORKSHOP_ADMIN or MECHANIC) to a ServiceCentre.
"""

import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class VerificationStatus(models.TextChoices):
    PENDING  = "PENDING",  "Pending Verification"
    VERIFIED = "VERIFIED", "Verified"
    REJECTED = "REJECTED", "Rejected"
    SUSPENDED = "SUSPENDED", "Suspended"


class Designation(models.TextChoices):
    ADMIN    = "ADMIN",    "Workshop Administrator"
    MECHANIC = "MECHANIC", "Mechanic"
    STAFF    = "STAFF",    "Support Staff"


class ServiceCentre(models.Model):
    """Registered service centre / workshop."""

    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name                = models.CharField(max_length=200)
    address             = models.TextField()
    city                = models.CharField(max_length=100, blank=True)
    state               = models.CharField(max_length=100, blank=True)
    contact_number      = models.CharField(max_length=20)
    email               = models.EmailField(blank=True)
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True,
    )
    is_active           = models.BooleanField(default=True)
    registered_by       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="registered_centres",
    )
    created_at          = models.DateTimeField(default=timezone.now)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table  = "org_service_centre"
        ordering  = ["name"]
        verbose_name = "Service Centre"

    def __str__(self):
        return f"{self.name} ({self.verification_status})"


class WorkshopMembership(models.Model):
    """Links a User to a ServiceCentre with a designated role."""

    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user           = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    service_centre = models.ForeignKey(
        ServiceCentre,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    designation    = models.CharField(max_length=20, choices=Designation.choices)
    is_active      = models.BooleanField(default=True)
    joined_at      = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table        = "org_workshop_membership"
        unique_together = [("user", "service_centre")]
        verbose_name    = "Workshop Membership"

    def __str__(self):
        return f"{self.user.phone_number} @ {self.service_centre.name} ({self.designation})"
