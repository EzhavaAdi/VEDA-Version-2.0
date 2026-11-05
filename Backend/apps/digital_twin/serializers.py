"""VEDA V2 — digital_twin serializers"""

from rest_framework import serializers
from .models import Asset3D, ComponentMeshMapping


class ComponentMeshMappingSerializer(serializers.ModelSerializer):
    component_code = serializers.CharField(source="component.component_code", read_only=True)
    component_name = serializers.CharField(source="component.component_name", read_only=True)
    vehicle_system = serializers.CharField(source="component.vehicle_system", read_only=True)

    class Meta:
        model  = ComponentMeshMapping
        fields = ["id", "component_code", "component_name", "vehicle_system",
                  "mesh_name", "mesh_identifier"]
        read_only_fields = fields


class Asset3DSerializer(serializers.ModelSerializer):
    mesh_mappings = ComponentMeshMappingSerializer(many=True, read_only=True)

    class Meta:
        model  = Asset3D
        fields = ["id", "asset_name", "asset_format", "asset_path",
                  "asset_source", "license_info", "attribution",
                  "version", "mesh_mappings"]
        read_only_fields = fields
