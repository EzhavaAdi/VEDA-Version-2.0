"""
VEDA V2 — vehicles models

Vehicle: registered heavy vehicle owned by a User with OWNER role.
VehicleDocument: photos and documents attached to a vehicle.
"""

import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class VehicleCategory(models.TextChoices):
    RIGID_TRUCK      = "RIGID_TRUCK",      "Rigid Truck"
    SEMI_TRAILER     = "SEMI_TRAILER",     "Semi-Trailer"
    TIPPER           = "TIPPER",           "Tipper / Dump Truck"
    TANKER           = "TANKER",           "Tanker"
    REFUSE_TRUCK     = "REFUSE_TRUCK",     "Refuse Collection Truck"
    FLATBED          = "FLATBED",          "Flatbed"
    REFRIGERATED     = "REFRIGERATED",     "Refrigerated Truck"
    CONCRETE_MIXER   = "CONCRETE_MIXER",   "Concrete Mixer"
    CRANE_TRUCK      = "CRANE_TRUCK",      "Crane Truck"
    OTHER            = "OTHER",            "Other"


class Vehicle(models.Model):
    """
    A heavy vehicle registered by an owner.
    Owners may only access their own vehicles — enforced at the service layer.
    """

    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner               = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vehicles",
        db_index=True,
    )
    registration_number = models.CharField(max_length=50, unique=True, db_index=True)
    manufacturer        = models.CharField(max_length=100)
    model               = models.CharField(max_length=100)
    vehicle_category    = models.CharField(
        max_length=30,
        choices=VehicleCategory.choices,
        default=VehicleCategory.OTHER,
    )
    manufacturing_year  = models.PositiveSmallIntegerField()
    vin                 = models.CharField(max_length=17, blank=True)  # Vehicle Identification Number
    odometer_reading    = models.PositiveIntegerField(default=0, help_text="Kilometres")
    operating_hours     = models.PositiveIntegerField(default=0, help_text="Engine hours")
    is_active           = models.BooleanField(default=True)
    notes               = models.TextField(blank=True)
    created_at          = models.DateTimeField(default=timezone.now)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table  = "vehicle"
        ordering  = ["-created_at"]
        verbose_name = "Vehicle"

    def __str__(self):
        return f"{self.registration_number} — {self.manufacturer} {self.model} ({self.manufacturing_year})"


class DocumentType(models.TextChoices):
    PHOTOGRAPH       = "PHOTOGRAPH",       "Vehicle Photograph"
    REGISTRATION     = "REGISTRATION",     "Registration Certificate"
    INSURANCE        = "INSURANCE",        "Insurance Document"
    INSPECTION_CERT  = "INSPECTION_CERT",  "Inspection Certificate"
    OTHER            = "OTHER",            "Other"


class VehicleDocument(models.Model):
    """Photos and documents attached to a vehicle."""

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle     = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    document_type = models.CharField(max_length=30, choices=DocumentType.choices)
    file          = models.FileField(upload_to="vehicles/documents/%Y/%m/")
    description   = models.CharField(max_length=200, blank=True)
    uploaded_at   = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "vehicle_document"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.vehicle.registration_number} — {self.document_type}"
