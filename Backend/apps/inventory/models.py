"""
VEDA V2 — inventory models

PartCatalog:       master parts catalogue
PartCompatibility: which components a part is compatible with
WorkshopInventory: centre-specific stock (quantity + price)
InventoryMovement: audit trail for every stock change

RULES:
- All financial values use DecimalField.
- Stock operations must use database transactions.
- Negative stock is prevented at the service layer.
- Never invent compatibility — record evidence source.
"""

import uuid
from django.db import models
from django.utils import timezone


class CompatibilityStatus(models.TextChoices):
    VERIFIED   = "VERIFIED",   "Verified"
    PROBABLE   = "PROBABLE",   "Probable (unverified)"
    DEPRECATED = "DEPRECATED", "Deprecated"


class MovementType(models.TextChoices):
    RECEIVED  = "RECEIVED",  "Stock Received"
    RESERVED  = "RESERVED",  "Reserved for Order"
    USED      = "USED",      "Used in Repair"
    RETURNED  = "RETURNED",  "Returned to Stock"
    ADJUSTED  = "ADJUSTED",  "Manual Adjustment"
    CANCELLED = "CANCELLED", "Reservation Cancelled"


class PartCatalog(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    part_name   = models.CharField(max_length=200)
    part_number = models.CharField(max_length=100, unique=True, db_index=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    description  = models.TextField(blank=True)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "part_catalog"
        ordering = ["part_name"]
        verbose_name = "Part"

    def __str__(self):
        return f"{self.part_number} — {self.part_name}"


class PartCompatibility(models.Model):
    """Records that a part is compatible with a component."""

    id                   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    part                 = models.ForeignKey(
        PartCatalog, on_delete=models.CASCADE, related_name="compatibilities"
    )
    component            = models.ForeignKey(
        "components.Component", on_delete=models.CASCADE, related_name="compatible_parts"
    )
    vehicle_manufacturer = models.CharField(max_length=100, blank=True)
    compatible_model     = models.CharField(max_length=100, blank=True)
    compatibility_source = models.CharField(max_length=300, blank=True,
        help_text="Source of this compatibility record (e.g. OEM catalogue, mechanic note)")
    verification_status  = models.CharField(
        max_length=15, choices=CompatibilityStatus.choices,
        default=CompatibilityStatus.PROBABLE
    )

    class Meta:
        db_table        = "part_compatibility"
        unique_together = [("part", "component")]
        verbose_name    = "Part Compatibility"

    def __str__(self):
        return f"{self.part.part_number} ↔ {self.component.component_code}"


class WorkshopInventory(models.Model):
    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_centre = models.ForeignKey(
        "organizations.ServiceCentre",
        on_delete=models.CASCADE, related_name="inventory"
    )
    part           = models.ForeignKey(
        PartCatalog, on_delete=models.CASCADE, related_name="inventory_entries"
    )
    quantity_available = models.PositiveIntegerField(default=0)
    unit_price         = models.DecimalField(max_digits=12, decimal_places=2)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        db_table        = "workshop_inventory"
        unique_together = [("service_centre", "part")]
        verbose_name    = "Workshop Inventory"

    def __str__(self):
        return f"{self.service_centre.name} — {self.part.part_number} x{self.quantity_available}"


class InventoryMovement(models.Model):
    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inventory      = models.ForeignKey(
        WorkshopInventory, on_delete=models.CASCADE, related_name="movements"
    )
    movement_type  = models.CharField(max_length=15, choices=MovementType.choices)
    quantity       = models.IntegerField(help_text="Positive = stock in, negative = stock out")
    service_order  = models.ForeignKey(
        "service_orders.ServiceOrder",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    reference      = models.CharField(max_length=200, blank=True)
    created_by     = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True
    )
    created_at     = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "inventory_movement"
        ordering = ["-created_at"]
        verbose_name = "Inventory Movement"

    def __str__(self):
        return f"{self.movement_type} {self.quantity:+d} × {self.inventory.part.part_number}"
