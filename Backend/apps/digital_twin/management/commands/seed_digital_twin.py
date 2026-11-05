"""
VEDA V2 — seed_digital_twin management command

Seeds the Asset3D record for refuse-collection-truck.glb and creates
ComponentMeshMapping entries for all components that have verified mesh names.

ONLY components with confirmed anatomical_id values in the GLB are mapped.
Components with no matching mesh are intentionally left unmapped (UNMAPPED state).

Run: python manage.py seed_digital_twin
Idempotent — safe to run multiple times.
"""

from django.core.management.base import BaseCommand
from apps.components.models import Component
from apps.digital_twin.models import Asset3D, ComponentMeshMapping


# ---------------------------------------------------------------------------
# Asset registration
# ---------------------------------------------------------------------------
ASSET = {
    "asset_name":   "Refuse Collection Truck (Generic)",
    "asset_format": "GLB",
    "asset_path":   "models/refuse-collection-truck.glb",
    "asset_source": "Innerscene Corp (innerscene.com)",
    "license_info": "CC0 1.0 Universal — Public Domain Dedication. "
                    "https://creativecommons.org/publicdomain/zero/1.0/",
    "attribution":  "Authored by Innerscene Corp. No attribution required under CC0.",
    "version":      "1.0",
}

# ---------------------------------------------------------------------------
# Verified mesh mappings — anatomical_id values confirmed from GLB JSON chunk
# Format: (component_code, mesh_name_label, anatomical_id_in_glb)
# Multiple rows per component_code are allowed (one entry per mesh)
# ---------------------------------------------------------------------------
MAPPINGS = [
    # Axle / Drivetrain
    ("AXLE",                "Axle 1 — Housing",         "axle_1_through_housing"),
    ("AXLE",                "Axle 2 — Housing",         "axle_2_through_housing"),
    ("AXLE_DIFF",           "Axle 1 — Differential",    "axle_1_differential_case"),
    ("AXLE_DIFF",           "Axle 2 — Differential",    "axle_2_differential_case"),

    # Suspension — leaf springs (axle 1)
    ("SUSPENSION_LEAF_SPRING", "Leaf Spring A1-1 (0)", "axle_1_seated_leaf_spring_1_0"),
    ("SUSPENSION_LEAF_SPRING", "Leaf Spring A1-1 (1)", "axle_1_seated_leaf_spring_1_1"),
    ("SUSPENSION_LEAF_SPRING", "Leaf Spring A1-1 (2)", "axle_1_seated_leaf_spring_1_2"),
    ("SUSPENSION_LEAF_SPRING", "Leaf Spring A1-1 (3)", "axle_1_seated_leaf_spring_1_3"),
    ("SUSPENSION_LEAF_SPRING", "Leaf Spring A1--1 (0)","axle_1_seated_leaf_spring_-1_0"),
    ("SUSPENSION_LEAF_SPRING", "Leaf Spring A1--1 (1)","axle_1_seated_leaf_spring_-1_1"),

    # Suspension — spring saddles
    ("SUSPENSION",          "Spring Saddle A1 L",       "axle_1_spring_saddle_1"),
    ("SUSPENSION",          "Spring Saddle A1 R",       "axle_1_spring_saddle_-1"),

    # Tyres and wheels (front axle wheel disc)
    ("TYRE_FRONT",          "Front Wheel Disc L",       "axle_1_wheel_1_pressed_wheel_disc_with_ventilation_apertures"),
    ("TYRE_FRONT",          "Front Wheel Disc R",       "axle_1_wheel_-1_pressed_wheel_disc_with_ventilation_apertures"),
    ("TYRE_REAR",           "Rear Wheel Disc A2 L",     "axle_2_wheel_1_pressed_wheel_disc_with_ventilation_apertures"),
    ("TYRE_REAR",           "Rear Wheel Disc A2 R",     "axle_2_wheel_-1_pressed_wheel_disc_with_ventilation_apertures"),
    ("TYRES",               "Front Bearing Hub L",      "axle_1_wheel_1_bearing_hub"),
    ("TYRES",               "Front Bearing Hub R",      "axle_1_wheel_-1_bearing_hub"),

    # Steering
    ("STEERING",            "Steering Wheel Rim",       "steering_wheel_closed_rim"),
    ("STEERING",            "Steering Wheel Hub",       "steering_wheel_hub"),
    ("STEERING",            "Steering Column",          "steering_column_attached_to_dashboard"),

    # Body / Cab
    ("BODY",                "Cab Front Grille Bar 0",   "cab_front_grille_raised_bar_0"),
    ("BODY",                "Cab Entry Step L",         "cab_entry_nonslip_step_1"),
    ("BODY",                "Cab Entry Step R",         "cab_entry_nonslip_step_-1"),

    # Chassis
    ("ELECTRICAL",          "Instrument Bridge",        "cab_full_width_instrument_bridge"),
]


class Command(BaseCommand):
    help = "Seed Asset3D and ComponentMeshMapping records for refuse-collection-truck.glb"

    def handle(self, *args, **options):
        # Register asset
        asset, created = Asset3D.objects.get_or_create(
            asset_path=ASSET["asset_path"],
            defaults=ASSET,
        )
        action = "Created" if created else "Already exists"
        self.stdout.write(f"{action}: Asset3D '{asset.asset_name}'")

        # Build mappings
        mapped = 0
        skipped = 0
        for comp_code, mesh_label, mesh_id in MAPPINGS:
            try:
                component = Component.objects.get(component_code=comp_code)
            except Component.DoesNotExist:
                self.stderr.write(f"Component '{comp_code}' not found — skipping.")
                skipped += 1
                continue

            _, created_m = ComponentMeshMapping.objects.get_or_create(
                asset=asset,
                component=component,
                mesh_identifier=mesh_id,
                defaults={"mesh_name": mesh_label},
            )
            if created_m:
                mapped += 1

        total = ComponentMeshMapping.objects.filter(asset=asset).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Mesh mappings: {mapped} new, {skipped} skipped. "
                f"Total for this asset: {total}"
            )
        )
        self.stdout.write(
            "Note: APS, Engine, Brakes have no mesh in this asset and will show as UNMAPPED."
        )
