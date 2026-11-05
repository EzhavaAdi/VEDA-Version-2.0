/**
 * VEDA V2 — Digital Twin TypeScript types
 */

export type VisualState =
  | 'NORMAL'
  | 'SUSPECTED'
  | 'MECHANIC_VERIFIED'
  | 'REPAIRED'
  | 'UNMAPPED'

export interface MeshMapping {
  id: string
  component_code: string
  component_name: string
  vehicle_system: string
  mesh_name: string
  mesh_identifier: string
}

export interface Asset3D {
  id: string
  asset_name: string
  asset_format: string
  asset_path: string
  license_info: string
  attribution: string
  version: string
  mesh_mappings: MeshMapping[]
}

export interface SceneMeshState {
  component_code: string
  component_name: string
  visual_state: VisualState
}

export interface SceneState {
  asset_id: string
  scene: Record<string, SceneMeshState>   // mesh_identifier -> state
}

export const VISUAL_STATE_COLOURS: Record<VisualState, string> = {
  NORMAL:           '#829B75',
  SUSPECTED:        '#C89B4B',
  MECHANIC_VERIFIED:'#B96859',
  REPAIRED:         '#91B957',
  UNMAPPED:         '#858A7E',
}

export const VISUAL_STATE_LABELS: Record<VisualState, string> = {
  NORMAL:           'Normal',
  SUSPECTED:        'Suspected Fault',
  MECHANIC_VERIFIED:'Mechanic Verified',
  REPAIRED:         'Repaired',
  UNMAPPED:         'Unmapped',
}
