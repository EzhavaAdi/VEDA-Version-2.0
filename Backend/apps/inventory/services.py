"""VEDA V2 — inventory service layer

All stock mutations go through reserve_stock() and consume_stock().
Negative stock is prevented at service level.
Every movement creates an InventoryMovement audit record.
"""

import logging
from decimal import Decimal
from django.db import transaction

from apps.accounts.models import User
from apps.organizations.models import ServiceCentre
from .models import (
    PartCatalog, PartCompatibility, WorkshopInventory,
    InventoryMovement, MovementType, CompatibilityStatus,
)

logger = logging.getLogger("veda.inventory")


class InventoryError(Exception):
    pass

class InsufficientStockError(InventoryError):
    pass

class NotFoundError(InventoryError):
    pass


# ---------------------------------------------------------------------------
# Part catalogue
# ---------------------------------------------------------------------------

def get_parts(search: str = None):
    qs = PartCatalog.objects.filter(is_active=True)
    if search:
        qs = qs.filter(part_name__icontains=search) | qs.filter(part_number__icontains=search)
    return qs.order_by("part_name")


def get_compatible_parts(component_code: str):
    """Return parts compatible with a component, verified first."""
    return PartCompatibility.objects.filter(
        component__component_code=component_code,
        part__is_active=True,
    ).select_related("part").order_by("-verification_status")


# ---------------------------------------------------------------------------
# Workshop inventory
# ---------------------------------------------------------------------------

def get_inventory(centre: ServiceCentre, in_stock_only: bool = False):
    qs = WorkshopInventory.objects.filter(service_centre=centre).select_related("part")
    if in_stock_only:
        qs = qs.filter(quantity_available__gt=0)
    return qs.order_by("part__part_name")


@transaction.atomic
def add_or_update_stock(centre: ServiceCentre, part_id: str,
                         quantity: int, unit_price: Decimal,
                         added_by: User) -> WorkshopInventory:
    if quantity < 0:
        raise InventoryError("Quantity must be non-negative.")
    try:
        part = PartCatalog.objects.get(id=part_id, is_active=True)
    except PartCatalog.DoesNotExist:
        raise NotFoundError("Part not found.")

    inv, created = WorkshopInventory.objects.get_or_create(
        service_centre=centre, part=part,
        defaults={"quantity_available": 0, "unit_price": unit_price},
    )
    if not created:
        inv.unit_price = unit_price
        inv.save(update_fields=["unit_price", "updated_at"])

    if quantity > 0:
        inv.quantity_available += quantity
        inv.save(update_fields=["quantity_available", "updated_at"])
        InventoryMovement.objects.create(
            inventory=inv, movement_type=MovementType.RECEIVED,
            quantity=quantity, created_by=added_by,
            reference=f"Stock added by {added_by.phone_number}",
        )
    return inv


@transaction.atomic
def reserve_stock(inv: WorkshopInventory, quantity: int,
                  service_order, reserved_by: User) -> WorkshopInventory:
    """
    Reserve stock for a service order.
    Raises InsufficientStockError if not enough available.
    """
    inv = WorkshopInventory.objects.select_for_update().get(pk=inv.pk)
    if inv.quantity_available < quantity:
        raise InsufficientStockError(
            f"Insufficient stock for '{inv.part.part_name}'. "
            f"Available: {inv.quantity_available}, requested: {quantity}."
        )
    inv.quantity_available -= quantity
    inv.save(update_fields=["quantity_available", "updated_at"])
    InventoryMovement.objects.create(
        inventory=inv, movement_type=MovementType.RESERVED,
        quantity=-quantity, service_order=service_order,
        created_by=reserved_by,
        reference=f"Reserved for order {service_order.id}",
    )
    return inv


@transaction.atomic
def consume_stock(inv: WorkshopInventory, quantity: int,
                  service_order, consumed_by: User) -> WorkshopInventory:
    """Mark stock as actually used (called after repair completes)."""
    inv = WorkshopInventory.objects.select_for_update().get(pk=inv.pk)
    InventoryMovement.objects.create(
        inventory=inv, movement_type=MovementType.USED,
        quantity=-quantity, service_order=service_order,
        created_by=consumed_by,
        reference=f"Used in order {service_order.id}",
    )
    return inv


@transaction.atomic
def cancel_reservation(inv: WorkshopInventory, quantity: int,
                       service_order, cancelled_by: User) -> WorkshopInventory:
    inv = WorkshopInventory.objects.select_for_update().get(pk=inv.pk)
    inv.quantity_available += quantity
    inv.save(update_fields=["quantity_available", "updated_at"])
    InventoryMovement.objects.create(
        inventory=inv, movement_type=MovementType.CANCELLED,
        quantity=quantity, service_order=service_order,
        created_by=cancelled_by,
        reference=f"Reservation cancelled for order {service_order.id}",
    )
    return inv
