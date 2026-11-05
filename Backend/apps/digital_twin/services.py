"""VEDA V2 — digital_twin service layer"""

from .models import Asset3D, ComponentMeshMapping, Diagram2D


def get_active_assets():
    return Asset3D.objects.filter(is_active=True).order_by("asset_name")


def get_asset_with_mappings(asset_id: str) -> Asset3D:
    try:
        return Asset3D.objects.prefetch_related(
            "mesh_mappings__component"
        ).get(id=asset_id, is_active=True)
    except Asset3D.DoesNotExist:
        raise ValueError("Asset not found.")


def get_mesh_mappings_for_asset(asset_id: str) -> list:
    """Return all mesh mappings for an asset, keyed by component_code."""
    mappings = ComponentMeshMapping.objects.filter(
        asset_id=asset_id
    ).select_related("component")
    return list(mappings)


def get_component_visual_state(component_code: str, diagnosis_cases: list) -> str:
    """
    Given a component code and a list of diagnosis case dicts,
    return the appropriate visual state string.
    """
    for case in diagnosis_cases:
        if case.get("component_code") == component_code:
            status = case.get("diagnosis_status", "")
            verification = case.get("mechanic_verification", "UNREVIEWED")
            if status == "MECHANIC_VERIFIED":
                return "MECHANIC_VERIFIED"
            if status == "MECHANIC_REJECTED":
                return "NORMAL"
            if status == "RESOLVED":
                return "REPAIRED"
            if status == "SUSPECTED":
                return "SUSPECTED"
    return "NORMAL"


def build_scene_state(asset_id: str, diagnosis_cases: list) -> dict:
    """
    Build the complete scene state dict for the frontend viewer.
    Returns mesh_identifier -> visual_state for all mapped meshes.
    """
    mappings = get_mesh_mappings_for_asset(asset_id)
    scene = {}
    for m in mappings:
        state = get_component_visual_state(m.component.component_code, diagnosis_cases)
        scene[m.mesh_identifier] = {
            "component_code": m.component.component_code,
            "component_name": m.component.component_name,
            "visual_state":   state,
        }
    return scene
