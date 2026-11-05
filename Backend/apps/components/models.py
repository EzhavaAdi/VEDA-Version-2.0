"""
VEDA V2 — components models

Component: hierarchical catalogue of vehicle components (system → subsystem → part).
VehicleComponent: links a specific component instance to a vehicle.

The catalogue is independent of any single vehicle or 3D asset.
Component IDs are stable — 3D mesh mappings reference these IDs.
"""

import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class VehicleSystem(models.TextChoices):
    ENGINE          = "ENGINE",          "Engine"
    AIR_SYSTEM      = "AIR_SYSTEM",      "Air Pressure System (APS)"
    BRAKES          = "BRAKES",          "Brake System"
    TRANSMISSION    = "TRANSMISSION",    "Transmission"
    SUSPENSION      = "SUSPENSION",      "Suspension"
    STEERING        = "STEERING",        "Steering"
    ELECTRICAL      = "ELECTRICAL",      "Electrical System"
    COOLING         = "COOLING",         "Cooling System"
    FUEL            = "FUEL",            "Fuel System"
    EXHAUST         = "EXHAUST",         "Exhaust System"
    BODY            = "BODY",            "Body and Cab"
    AXLE            = "AXLE",            "Axles and Drivetrain"
    TYRES           = "TYRES",           "Tyres and Wheels"
    HYDRAULICS      = "HYDRAULICS",      "Hydraulics"
    OTHER           = "OTHER",           "Other"


class ComponentStatus(models.TextChoices):
    ACTIVE      = "ACTIVE",      "Active"
    DEPRECATED  = "DEPRECATED",  "Deprecated"


class Component(models.Model):
    """
    A vehicle component in the VEDA catalogue.

    Hierarchical — a component may have a parent (e.g. Air Compressor → APS).
    component_code is a stable identifier used for mesh mappings and diagnostic rules.
    """

    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component_name   = models.CharField(max_length=200)
    component_code   = models.CharField(max_length=50, unique=True, db_index=True)
    vehicle_system   = models.CharField(
        max_length=30,
        choices=VehicleSystem.choices,
        db_index=True,
    )
    parent           = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    description      = models.TextField(blank=True)
    maintenance_info = models.TextField(blank=True, help_text="General maintenance notes")
    status           = models.CharField(
        max_length=15,
        choices=ComponentStatus.choices,
        default=ComponentStatus.ACTIVE,
    )
    created_at       = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table  = "component"
        ordering  = ["vehicle_system", "component_name"]
        verbose_name = "Component"

    def __str__(self):
        parent_str = f" > {self.parent.component_name}" if self.parent else ""
        return f"[{self.component_code}] {self.component_name}{parent_str}"

    def get_ancestors(self):
        """Return list of ancestor components from root down."""
        ancestors = []
        node = self.parent
        while node:
            ancestors.insert(0, node)
            node = node.parent
        return ancestors


class VehicleComponentStatus(models.TextChoices):
    NORMAL    = "NORMAL",    "Normal"
    SUSPECTED = "SUSPECTED", "Suspected Fault"
    FAULTY    = "FAULTY",    "Confirmed Fault"
    REPAIRED  = "REPAIRED",  "Repaired"
    REPLACED  = "REPLACED",  "Replaced"
    UNKNOWN   = "UNKNOWN",   "Unknown"


class VehicleComponent(models.Model):
    """
    An instance of a Component installed on a specific Vehicle.
    Tracks current condition and installation details.
    """

    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle          = models.ForeignKey(
        "vehicles.Vehicle",
        on_delete=models.CASCADE,
        related_name="components",
    )
    component        = models.ForeignKey(
        Component,
        on_delete=models.PROTECT,
        related_name="vehicle_instances",
    )
    current_status   = models.CharField(
        max_length=15,
        choices=VehicleComponentStatus.choices,
        default=VehicleComponentStatus.UNKNOWN,
    )
    installation_date = models.DateField(null=True, blank=True)
    notes            = models.TextField(blank=True)
    last_updated     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table        = "vehicle_component"
        unique_together = [("vehicle", "component")]
        verbose_name    = "Vehicle Component"

    def __str__(self):
        return f"{self.vehicle.registration_number} — {self.component.component_name} ({self.current_status})"
