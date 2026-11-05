"""
VEDA V2 — digital_twin models

Asset3D:              registered 3D model asset (GLB/GLTF)
ComponentMeshMapping: maps a VEDA component code to a named mesh in an asset
Diagram2D:            registered 2D SVG technical diagram
ComponentDiagramMapping: maps a VEDA component code to an SVG element ID

RULES:
- Never assume a model has selectable components — only mapped ones are highlighted.
- mesh_identifier must exactly match the anatomical_id in the GLB extras.
- UNMAPPED status is shown when no mapping exists for a component.
"""

import uuid
from django.db import models
from django.utils import timezone


class AssetFormat(models.TextChoices):
    GLB  = "GLB",  "GLB (Binary glTF)"
    GLTF = "GLTF", "GLTF (Text)"
    OBJ  = "OBJ",  "Wavefront OBJ"


class Asset3D(models.Model):
    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_name       = models.CharField(max_length=200)
    asset_format     = models.CharField(max_length=10, choices=AssetFormat.choices)
    asset_path       = models.CharField(max_length=500, help_text="Path relative to public/models/")
    asset_source     = models.CharField(max_length=500, blank=True)
    license_info     = models.TextField(blank=True)
    attribution      = models.TextField(blank=True)
    version          = models.CharField(max_length=20, default="1.0")
    is_active        = models.BooleanField(default=True)
    created_at       = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table   = "asset_3d"
        verbose_name = "3D Asset"

    def __str__(self):
        return f"{self.asset_name} ({self.asset_format})"


class ComponentMeshMapping(models.Model):
    """Maps one VEDA component code to one mesh in a 3D asset."""

    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset            = models.ForeignKey(
        Asset3D, on_delete=models.CASCADE, related_name="mesh_mappings"
    )
    component        = models.ForeignKey(
        "components.Component", on_delete=models.CASCADE, related_name="mesh_mappings"
    )
    mesh_name        = models.CharField(max_length=300, help_text="Human-readable mesh label")
    mesh_identifier  = models.CharField(
        max_length=300,
        help_text="Exact anatomical_id value from GLB node extras — must match perfectly"
    )

    class Meta:
        db_table        = "component_mesh_mapping"
        unique_together = [("asset", "component", "mesh_identifier")]
        verbose_name    = "Component Mesh Mapping"

    def __str__(self):
        return f"{self.component.component_code} -> {self.mesh_identifier}"


class Diagram2D(models.Model):
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diagram_name = models.CharField(max_length=200)
    diagram_path = models.CharField(max_length=500, help_text="Path relative to public/diagrams/")
    vehicle_system = models.CharField(max_length=30, blank=True)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table   = "diagram_2d"
        verbose_name = "2D Diagram"

    def __str__(self):
        return self.diagram_name


class ComponentDiagramMapping(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diagram       = models.ForeignKey(
        Diagram2D, on_delete=models.CASCADE, related_name="component_mappings"
    )
    component     = models.ForeignKey(
        "components.Component", on_delete=models.CASCADE, related_name="diagram_mappings"
    )
    svg_element_id = models.CharField(max_length=200)

    class Meta:
        db_table        = "component_diagram_mapping"
        unique_together = [("diagram", "component")]
        verbose_name    = "Component Diagram Mapping"

    def __str__(self):
        return f"{self.component.component_code} -> #{self.svg_element_id}"
