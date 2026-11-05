"""VEDA V2 — digital_twin admin"""
from django.contrib import admin
from .models import Asset3D, ComponentMeshMapping, Diagram2D, ComponentDiagramMapping

@admin.register(Asset3D)
class Asset3DAdmin(admin.ModelAdmin):
    list_display = ["asset_name", "asset_format", "version", "is_active"]
    readonly_fields = ["id", "created_at"]

@admin.register(ComponentMeshMapping)
class ComponentMeshMappingAdmin(admin.ModelAdmin):
    list_display  = ["asset", "component", "mesh_identifier"]
    search_fields = ["mesh_identifier", "component__component_code"]
    readonly_fields = ["id"]

@admin.register(Diagram2D)
class Diagram2DAdmin(admin.ModelAdmin):
    list_display = ["diagram_name", "vehicle_system", "is_active"]
    readonly_fields = ["id", "created_at"]

@admin.register(ComponentDiagramMapping)
class ComponentDiagramMappingAdmin(admin.ModelAdmin):
    list_display  = ["diagram", "component", "svg_element_id"]
    readonly_fields = ["id"]
