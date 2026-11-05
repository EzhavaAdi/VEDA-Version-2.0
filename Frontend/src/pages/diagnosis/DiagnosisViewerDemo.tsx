/**
 * VEDA V2 — DiagnosisViewer Demo Page
 *
 * Standalone demo that loads the 3D viewer with the seeded asset.
 * Uses a hardcoded asset path (/models/refuse-collection-truck.glb)
 * with a mock scene state so the viewer works without an auth token.
 *
 * In production, assetId and orderId come from routing params.
 */

import { useState } from 'react'
import { TruckViewer3D } from '../../components/visualization/TruckViewer3D'
import type { SceneState } from '../../types/digital-twin'

const MOCK_SCENE_STATE: SceneState = {
  asset_id: 'demo',
  scene: {
    'axle_1_through_housing':           { component_code: 'AXLE',                 component_name: 'Axle Assembly',          visual_state: 'SUSPECTED' },
    'axle_1_differential_case':         { component_code: 'AXLE_DIFF',            component_name: 'Differential',           visual_state: 'SUSPECTED' },
    'axle_1_seated_leaf_spring_1_0':    { component_code: 'SUSPENSION_LEAF_SPRING', component_name: 'Leaf Spring',           visual_state: 'NORMAL' },
    'axle_1_seated_leaf_spring_1_1':    { component_code: 'SUSPENSION_LEAF_SPRING', component_name: 'Leaf Spring',           visual_state: 'NORMAL' },
    'axle_1_seated_leaf_spring_1_2':    { component_code: 'SUSPENSION_LEAF_SPRING', component_name: 'Leaf Spring',           visual_state: 'NORMAL' },
    'axle_1_seated_leaf_spring_1_3':    { component_code: 'SUSPENSION_LEAF_SPRING', component_name: 'Leaf Spring',           visual_state: 'NORMAL' },
    'axle_1_seated_leaf_spring_-1_0':   { component_code: 'SUSPENSION_LEAF_SPRING', component_name: 'Leaf Spring',           visual_state: 'NORMAL' },
    'axle_1_seated_leaf_spring_-1_1':   { component_code: 'SUSPENSION_LEAF_SPRING', component_name: 'Leaf Spring',           visual_state: 'NORMAL' },
    'axle_1_spring_saddle_1':           { component_code: 'SUSPENSION',           component_name: 'Spring Saddle',           visual_state: 'NORMAL' },
    'axle_1_spring_saddle_-1':          { component_code: 'SUSPENSION',           component_name: 'Spring Saddle',           visual_state: 'NORMAL' },
    'axle_1_wheel_1_pressed_wheel_disc_with_ventilation_apertures':  { component_code: 'TYRE_FRONT', component_name: 'Front Tyre', visual_state: 'NORMAL' },
    'axle_1_wheel_-1_pressed_wheel_disc_with_ventilation_apertures': { component_code: 'TYRE_FRONT', component_name: 'Front Tyre', visual_state: 'NORMAL' },
    'axle_2_wheel_1_pressed_wheel_disc_with_ventilation_apertures':  { component_code: 'TYRE_REAR',  component_name: 'Rear Tyre',  visual_state: 'REPAIRED' },
    'axle_2_wheel_-1_pressed_wheel_disc_with_ventilation_apertures': { component_code: 'TYRE_REAR',  component_name: 'Rear Tyre',  visual_state: 'REPAIRED' },
    'axle_1_wheel_1_bearing_hub':       { component_code: 'TYRES',               component_name: 'Bearing Hub',             visual_state: 'MECHANIC_VERIFIED' },
    'axle_1_wheel_-1_bearing_hub':      { component_code: 'TYRES',               component_name: 'Bearing Hub',             visual_state: 'MECHANIC_VERIFIED' },
    'steering_wheel_closed_rim':        { component_code: 'STEERING',            component_name: 'Steering',                visual_state: 'NORMAL' },
    'steering_wheel_hub':               { component_code: 'STEERING',            component_name: 'Steering',                visual_state: 'NORMAL' },
    'steering_column_attached_to_dashboard': { component_code: 'STEERING',       component_name: 'Steering Column',         visual_state: 'NORMAL' },
    'cab_front_grille_raised_bar_0':    { component_code: 'BODY',               component_name: 'Body / Cab',              visual_state: 'NORMAL' },
    'cab_entry_nonslip_step_1':         { component_code: 'BODY',               component_name: 'Body / Cab',              visual_state: 'NORMAL' },
    'cab_entry_nonslip_step_-1':        { component_code: 'BODY',               component_name: 'Body / Cab',              visual_state: 'NORMAL' },
    'cab_full_width_instrument_bridge': { component_code: 'ELECTRICAL',         component_name: 'Electrical System',       visual_state: 'NORMAL' },
  },
}

export function DiagnosisViewerDemo() {
  const [selected, setSelected] = useState<{ mesh: string | null; code: string | null }>({ mesh: null, code: null })

  return (
    <div style={{
      minHeight: '100vh',
      background: '#10110F',
      color: '#F4F4F0',
      fontFamily: 'Manrope, sans-serif',
      padding: '1.5rem',
    }}>
      {/* Header */}
      <div style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '1.25rem', fontWeight: 700, margin: 0, letterSpacing: '-0.02em' }}>
            VEDA — Digital Twin Viewer
          </h1>
          <p style={{ color: '#858A7E', fontSize: '0.8rem', margin: '0.25rem 0 0', fontFamily: 'DM Mono, monospace' }}>
            refuse-collection-truck.glb — Phase 5 Demo — CC0 License (Innerscene Corp)
          </p>
        </div>
        <a href="/" style={{ color: '#858A7E', fontSize: '0.8rem', textDecoration: 'none' }}>
          ← Back
        </a>
      </div>

      {/* Scope notice */}
      <div style={{
        background: '#1A1D18', border: '1px solid #C89B4B44',
        borderRadius: '6px', padding: '0.6rem 1rem',
        marginBottom: '1.25rem', fontSize: '0.75rem', color: '#C89B4B',
        fontFamily: 'DM Mono, monospace',
      }}>
        DEMO MODE — Visual states are hardcoded for demonstration. In production, states come from the diagnosis API.
      </div>

      {/* Two-panel layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '220px 1fr', gap: '1rem' }}>
        {/* Left: component list */}
        <div style={{
          background: '#1A1D18', border: '1px solid #2a2d26',
          borderRadius: '8px', overflow: 'hidden',
        }}>
          <p style={{
            margin: 0, padding: '0.75rem 1rem',
            fontSize: '0.7rem', fontWeight: 600, color: '#858A7E',
            textTransform: 'uppercase', letterSpacing: '0.1em',
            borderBottom: '1px solid #2a2d26',
          }}>Mapped Components</p>
          <div style={{ padding: '0.25rem', maxHeight: '420px', overflowY: 'auto' }}>
            {Object.entries(
              // Group by component_code
              Object.values(MOCK_SCENE_STATE.scene).reduce<Record<string, { name: string; state: string; meshId: string }>>((acc, v, i) => {
                const key = v.component_code
                if (!acc[key]) acc[key] = { name: v.component_name, state: v.visual_state, meshId: Object.keys(MOCK_SCENE_STATE.scene)[i] }
                return acc
              }, {})
            ).map(([code, info]) => (
              <button
                key={code}
                onClick={() => setSelected({ mesh: info.meshId, code })}
                style={{
                  width: '100%', textAlign: 'left', border: '1px solid',
                  borderColor: selected.code === code ? '#B8E36A' : '#2a2d26',
                  background: selected.code === code ? '#1e2219' : 'transparent',
                  borderRadius: '5px', padding: '0.45rem 0.65rem',
                  marginBottom: '0.2rem', cursor: 'pointer',
                  display: 'flex', flexDirection: 'column', gap: '0.1rem',
                }}
              >
                <span style={{ color: '#F4F4F0', fontSize: '0.78rem', fontWeight: 500 }}>{info.name}</span>
                <span style={{
                  fontSize: '0.65rem',
                  color: ({ NORMAL: '#829B75', SUSPECTED: '#C89B4B', MECHANIC_VERIFIED: '#B96859', REPAIRED: '#91B957' } as Record<string,string>)[info.state] ?? '#858A7E',
                  fontFamily: 'DM Mono, monospace',
                }}>{info.state.replace(/_/g, ' ')}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Right: 3D viewer */}
        <div>
          <TruckViewer3D
            modelUrl="/models/refuse-collection-truck.glb"
            sceneState={MOCK_SCENE_STATE}
            selectedMesh={selected.mesh}
            onMeshClick={(meshId, code) => setSelected({ mesh: meshId, code })}
            height="500px"
          />
          {selected.code && (
            <div style={{
              marginTop: '0.75rem',
              background: '#1A1D18', border: '1px solid #2a2d26',
              borderRadius: '8px', padding: '1rem',
            }}>
              <p style={{ margin: '0 0 0.25rem', color: '#858A7E', fontSize: '0.7rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase' }}>
                Selected Component
              </p>
              <h3 style={{ margin: 0, color: '#F4F4F0', fontSize: '1rem' }}>
                {MOCK_SCENE_STATE.scene[selected.mesh ?? '']?.component_name ?? selected.code}
              </h3>
              <p style={{ margin: '0.25rem 0 0', color: '#858A7E', fontSize: '0.75rem', fontFamily: 'DM Mono, monospace' }}>
                {selected.code} — mesh: {selected.mesh ?? 'none'}
              </p>
              <p style={{ margin: '0.5rem 0 0', color: '#858A7E', fontSize: '0.8rem' }}>
                Visual state:{' '}
                <strong style={{ color: '#F4F4F0' }}>
                  {MOCK_SCENE_STATE.scene[selected.mesh ?? '']?.visual_state ?? 'UNMAPPED'}
                </strong>
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
