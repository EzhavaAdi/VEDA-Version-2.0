"""
VEDA V2 — inspections models

Inspection: the mechanic's formal inspection record for a service order.
InspectionItem: per-component observations.
SensorReading: numeric measurements (pressure, temperature, etc.).
"""

import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class InspectionStatus(models.TextChoices):
    STARTED   = "STARTED",   "Started"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"


class Severity(models.TextChoices):
    NONE     = "NONE",     "No Issue"
    LOW      = "LOW",      "Low"
    MEDIUM   = "MEDIUM",   "Medium"
    HIGH     = "HIGH",     "High"
    CRITICAL = "CRITICAL", "Critical"


class Inspection(models.Model):
    """
    One inspection record per service order.
    A mechanic may update it incrementally until marked COMPLETED.
    """

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_order   = models.OneToOneField(
        "service_orders.ServiceOrder",
        on_delete=models.CASCADE,
        related_name="inspection",
    )
    mechanic        = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="inspections",
    )
    inspection_date      = models.DateField(default=timezone.localdate)
    general_observations = models.TextField(blank=True)
    inspection_status    = models.CharField(
        max_length=15,
        choices=InspectionStatus.choices,
        default=InspectionStatus.STARTED,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inspection"
        verbose_name = "Inspection"

    def __str__(self):
        return f"Inspection for {self.service_order} [{self.inspection_status}]"


class InspectionItem(models.Model):
    """
    A mechanic's observation for one specific component.
    Multiple items per inspection — one per component examined.
    """

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inspection  = models.ForeignKey(
        Inspection,
        on_delete=models.CASCADE,
        related_name="items",
    )
    component   = models.ForeignKey(
        "components.Component",
        on_delete=models.PROTECT,
        related_name="inspection_items",
    )
    observed_condition = models.TextField(help_text="Mechanic's description of what was observed")
    severity           = models.CharField(
        max_length=10,
        choices=Severity.choices,
        default=Severity.NONE,
    )
    mechanic_notes = models.TextField(blank=True)
    created_at     = models.DateTimeField(default=timezone.now)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table        = "inspection_item"
        unique_together = [("inspection", "component")]
        verbose_name    = "Inspection Item"

    def __str__(self):
        return f"{self.component.component_code} — {self.severity}"


class SensorReading(models.Model):
    """
    A numeric measurement recorded during the inspection.
    Examples: air pressure (bar), brake pad thickness (mm), coolant temp (°C).
    """

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inspection      = models.ForeignKey(
        Inspection,
        on_delete=models.CASCADE,
        related_name="sensor_readings",
    )
    parameter_name  = models.CharField(max_length=100)
    parameter_value = models.DecimalField(max_digits=12, decimal_places=4)
    unit            = models.CharField(max_length=30, blank=True, help_text="e.g. bar, mm, °C, kPa")
    component       = models.ForeignKey(
        "components.Component",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sensor_readings",
    )
    recorded_at = models.DateTimeField(default=timezone.now)
    notes       = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "sensor_reading"
        ordering = ["recorded_at"]
        verbose_name = "Sensor Reading"

    def __str__(self):
        return f"{self.parameter_name}: {self.parameter_value} {self.unit}"
