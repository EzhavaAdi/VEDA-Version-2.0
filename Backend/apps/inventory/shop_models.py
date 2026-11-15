"""
VEDA V2 — Shop and AI prediction logging models.
These operate silently in the background — not exposed in the main frontend.
"""
import uuid
from django.db import models
from django.utils import timezone


# ---------------------------------------------------------------------------
# Spare Parts Shop
# ---------------------------------------------------------------------------

class ShopCategory(models.Model):
    id   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, blank=True, help_text="Emoji icon")
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "shop_category"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class ShopProduct(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category        = models.ForeignKey(ShopCategory, on_delete=models.CASCADE, related_name="products")
    name            = models.CharField(max_length=200)
    brand           = models.CharField(max_length=100, blank=True)
    description     = models.TextField(blank=True)
    part_number     = models.CharField(max_length=100, blank=True)
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    original_price  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock           = models.PositiveIntegerField(default=0)
    unit            = models.CharField(max_length=30, default="piece")
    image_emoji     = models.CharField(max_length=10, default="🔧", help_text="Emoji used as placeholder image")
    image_path      = models.CharField(max_length=200, blank=True, help_text="Filename in /shop/ folder e.g. BRAKES.webp")
    compatible_with = models.CharField(max_length=300, blank=True, help_text="Comma-separated component codes")
    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "shop_product"
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.part_number})"

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            return int((1 - self.price / self.original_price) * 100)
        return 0

    @property
    def in_stock(self):
        return self.stock > 0


class ShopCartEvent(models.Model):
    """Silent tracking of add-to-cart events."""
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product    = models.ForeignKey(ShopProduct, on_delete=models.CASCADE, related_name="cart_events")
    session_id = models.CharField(max_length=64, blank=True)
    quantity   = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "shop_cart_event"
        ordering = ["-created_at"]


# ---------------------------------------------------------------------------
# AI Prediction Logging (silent — not shown in frontend)
# ---------------------------------------------------------------------------

class APSPredictionLog(models.Model):
    """Every APS inference on the demo endpoint is logged here."""
    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id       = models.CharField(max_length=64, blank=True)
    filename         = models.CharField(max_length=200, blank=True)
    predicted_class  = models.CharField(max_length=10)   # pos / neg / skipped
    probability_pos  = models.FloatField(null=True, blank=True)
    feature_coverage = models.FloatField(default=0)
    created_at       = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "aps_prediction_log"
        ordering = ["-created_at"]

    def __str__(self):
        return f"APS {self.predicted_class} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class MechanicPredictionLog(models.Model):
    """Every mechanic component inference is logged here."""
    id                   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id           = models.CharField(max_length=64, blank=True)
    predicted_component  = models.CharField(max_length=50)
    confidence           = models.FloatField(default=0)
    input_values         = models.JSONField(default=dict)
    component_health     = models.JSONField(default=dict)
    created_at           = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "mechanic_prediction_log"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Mechanic → {self.predicted_component} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
