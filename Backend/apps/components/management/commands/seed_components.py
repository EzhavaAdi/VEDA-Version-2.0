"""
VEDA V2 — management command to seed the initial component catalogue.

Run: python manage.py seed_components

Idempotent — uses get_or_create so safe to run multiple times.
This seeds components relevant to Phase 4 (Scania APS) and general truck systems.
"""

from django.core.management.base import BaseCommand
from apps.components.models import Component, VehicleSystem


COMPONENTS = [
    # -------------------------------------------------------------------------
    # Air Pressure System (APS) — Scania APS dataset scope
    # -------------------------------------------------------------------------
    {
        "code": "APS",
        "name": "Air Pressure System",
        "system": VehicleSystem.AIR_SYSTEM,
        "description": "Generates and distributes pressurised air for braking, gear changes and other pneumatic functions.",
        "parent": None,
    },
    {
        "code": "APS_COMPRESSOR",
        "name": "Air Compressor",
        "system": VehicleSystem.AIR_SYSTEM,
        "parent": "APS",
        "description": "Compresses air for the pneumatic system.",
    },
    {
        "code": "APS_DRYER",
        "name": "Air Dryer",
        "system": VehicleSystem.AIR_SYSTEM,
        "parent": "APS",
        "description": "Removes moisture from compressed air.",
    },
    {
        "code": "APS_RESERVOIR",
        "name": "Air Reservoir / Tank",
        "system": VehicleSystem.AIR_SYSTEM,
        "parent": "APS",
        "description": "Stores compressed air.",
    },
    {
        "code": "APS_GOVERNOR",
        "name": "Pressure Governor",
        "system": VehicleSystem.AIR_SYSTEM,
        "parent": "APS",
        "description": "Regulates system pressure.",
    },
    {
        "code": "APS_VALVE",
        "name": "Air Control Valve",
        "system": VehicleSystem.AIR_SYSTEM,
        "parent": "APS",
        "description": "Controls air flow within the pneumatic system.",
    },
    # -------------------------------------------------------------------------
    # Brake System
    # -------------------------------------------------------------------------
    {
        "code": "BRAKES",
        "name": "Brake System",
        "system": VehicleSystem.BRAKES,
        "parent": None,
        "description": "Complete braking system including pneumatic and friction components.",
    },
    {
        "code": "BRAKE_DISC",
        "name": "Brake Disc / Rotor",
        "system": VehicleSystem.BRAKES,
        "parent": "BRAKES",
    },
    {
        "code": "BRAKE_PAD",
        "name": "Brake Pad",
        "system": VehicleSystem.BRAKES,
        "parent": "BRAKES",
    },
    {
        "code": "BRAKE_CALIPER",
        "name": "Brake Caliper",
        "system": VehicleSystem.BRAKES,
        "parent": "BRAKES",
    },
    {
        "code": "BRAKE_DRUM",
        "name": "Brake Drum",
        "system": VehicleSystem.BRAKES,
        "parent": "BRAKES",
    },
    # -------------------------------------------------------------------------
    # Engine
    # -------------------------------------------------------------------------
    {
        "code": "ENGINE",
        "name": "Engine",
        "system": VehicleSystem.ENGINE,
        "parent": None,
        "description": "Diesel engine assembly.",
    },
    {
        "code": "ENGINE_TURBO",
        "name": "Turbocharger",
        "system": VehicleSystem.ENGINE,
        "parent": "ENGINE",
    },
    {
        "code": "ENGINE_COOLING",
        "name": "Engine Cooling System",
        "system": VehicleSystem.COOLING,
        "parent": None,
        "description": "Radiator, coolant circuit and thermostat.",
    },
    # -------------------------------------------------------------------------
    # Transmission
    # -------------------------------------------------------------------------
    {
        "code": "TRANSMISSION",
        "name": "Transmission / Gearbox",
        "system": VehicleSystem.TRANSMISSION,
        "parent": None,
    },
    # -------------------------------------------------------------------------
    # Suspension
    # -------------------------------------------------------------------------
    {
        "code": "SUSPENSION",
        "name": "Suspension System",
        "system": VehicleSystem.SUSPENSION,
        "parent": None,
    },
    {
        "code": "SUSPENSION_LEAF_SPRING",
        "name": "Leaf Spring",
        "system": VehicleSystem.SUSPENSION,
        "parent": "SUSPENSION",
    },
    # -------------------------------------------------------------------------
    # Steering
    # -------------------------------------------------------------------------
    {
        "code": "STEERING",
        "name": "Steering System",
        "system": VehicleSystem.STEERING,
        "parent": None,
    },
    # -------------------------------------------------------------------------
    # Axle
    # -------------------------------------------------------------------------
    {
        "code": "AXLE",
        "name": "Axle Assembly",
        "system": VehicleSystem.AXLE,
        "parent": None,
    },
    {
        "code": "AXLE_DIFF",
        "name": "Differential",
        "system": VehicleSystem.AXLE,
        "parent": "AXLE",
    },
    # -------------------------------------------------------------------------
    # Tyres and Wheels
    # -------------------------------------------------------------------------
    {
        "code": "TYRES",
        "name": "Tyres and Wheels",
        "system": VehicleSystem.TYRES,
        "parent": None,
    },
    {
        "code": "TYRE_FRONT",
        "name": "Front Tyre",
        "system": VehicleSystem.TYRES,
        "parent": "TYRES",
    },
    {
        "code": "TYRE_REAR",
        "name": "Rear Tyre",
        "system": VehicleSystem.TYRES,
        "parent": "TYRES",
    },
    # -------------------------------------------------------------------------
    # Body and Cab
    # -------------------------------------------------------------------------
    {
        "code": "BODY",
        "name": "Body and Cab",
        "system": VehicleSystem.BODY,
        "parent": None,
        "description": "Vehicle body, cab structure, doors and glazing.",
    },
    {
        "code": "ELECTRICAL",
        "name": "Electrical System",
        "system": VehicleSystem.ELECTRICAL,
        "parent": None,
    },
    {
        "code": "ELEC_BATTERY",
        "name": "Battery",
        "system": VehicleSystem.ELECTRICAL,
        "parent": "ELECTRICAL",
    },
    {
        "code": "ELEC_ALTERNATOR",
        "name": "Alternator",
        "system": VehicleSystem.ELECTRICAL,
        "parent": "ELECTRICAL",
    },
]


class Command(BaseCommand):
    help = "Seed the initial VEDA component catalogue."

    def handle(self, *args, **options):
        # First pass: create root components
        code_map = {}
        created_count = 0
        existing_count = 0

        for spec in COMPONENTS:
            if spec.get("parent") is None:
                obj, created = Component.objects.get_or_create(
                    component_code=spec["code"],
                    defaults={
                        "component_name": spec["name"],
                        "vehicle_system": spec["system"],
                        "description": spec.get("description", ""),
                    },
                )
                code_map[spec["code"]] = obj
                if created:
                    created_count += 1
                else:
                    existing_count += 1

        # Second pass: create children
        for spec in COMPONENTS:
            if spec.get("parent") is not None:
                parent = code_map.get(spec["parent"])
                if not parent:
                    try:
                        parent = Component.objects.get(component_code=spec["parent"])
                    except Component.DoesNotExist:
                        self.stderr.write(f"Parent '{spec['parent']}' not found for {spec['code']}")
                        continue
                obj, created = Component.objects.get_or_create(
                    component_code=spec["code"],
                    defaults={
                        "component_name": spec["name"],
                        "vehicle_system": spec["system"],
                        "parent": parent,
                        "description": spec.get("description", ""),
                    },
                )
                code_map[spec["code"]] = obj
                if created:
                    created_count += 1
                else:
                    existing_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Component catalogue: {created_count} created, {existing_count} already existed. "
                f"Total: {Component.objects.count()} components."
            )
        )
