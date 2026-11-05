/**
 * VEDA V2 — DiagnosisViewer
 *
 * Two-panel diagnostic workspace:
 * - Left:  component list with visual state badges + evidence summary
 * - Right: interactive 3D truck viewer
 * - Below: component detail panel when a component is selected
 *
 * Data comes from the backend via the digital-twin and diagnosis APIs.
 */

import { useState, useEffect, useCallback } from 'react'
import { TruckViewer3D } from '../../components/visualization/TruckViewer3D'
import { digitalTwinService } from '../../services/digital-twin.service'
import type { SceneState, MeshMapping } from '../../types/digital-twin'
import { VISUAL_STATE_COLOURS, VISUAL_STATE_LABELS } from '../../types/digital-twin'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------
interface DiagnosisCase {
  id: string
  component_code: string
  component_name: string
  vehicle_system: string
  diagnosis_status: string
  mechanic_verification: string
  final_notes: string
  evidence: Array<{ evidence_type: string; evidence_description: string }>
}

interface Props {
  assetId:  string
  orderId?: string
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------
export function DiagnosisViewer({ assetId, orderId }: Props) {
  const [sceneState,    setSceneState]    = useState<SceneState | null>(null)
  const [meshMappings,  setMeshMappings]  = useState<MeshMapping[]>([])
  const [selectedMesh,  setSelectedMesh]  = useState<string | null>(null)
  const [selectedCode,  setSelectedCode]  = useState<string | null>(null)
  const [diagCases,     setDiagCases]     = useState<DiagnosisCase[]>([])
  const [loading,       setLoading]       = useState(true)
  const [error,         setError]         = useState<string | null>(null)

  // Fetch asset mesh mappings and scene state
  useEffect(() => {
    setLoading(true)
    Promise.all([
      digitalTwinService.getAsset(assetId),
      digitalTwinService.getSceneState(assetId, orderId),
    ])
      .then(([asset, scene]) => {
        setMeshMappings(asset.mesh_mappings)
        setSceneState(scene)
        setError(null)
      })
      .catch(() => setError('Failed to load 3D asset data.'))
      .finally(() => setLoading(false))
  }, [assetId, orderId])

  // Fetch diagnosis cases if orderId provided
  useEffect(() => {
    if (!orderId) return
    // Fetch via the diagnosis API (requires auth token — handled by api.ts interceptor in Phase 1+)
    import('../../services/api').then(({ api }) =>
      api.get<{ diagnosis_cases: DiagnosisCase[] }>(`/service-orders/${orderId}/diagnosis/`)
        .then(data => setDiagCases(data.diagnosis_cases ?? []))
        .catch(() => {}) // silent — diagnosis may not exist yet
    )
  }, [orderId])

  const handleMeshClick = useCallback((meshId: string | null, code: string | null) => {
    setSelectedMesh(meshId)
    setSelectedCode(code)
  }, [])

  // Find selected component's diagnosis case
  const selectedCase = diagCases.find(c => c.component_code === selectedCode)
  const selectedMapping = meshMappings.find(m => m.mesh_identifier === selectedMesh)

  // Visual state for selected component
  const visualState = selectedMesh && sceneState?.scene[selectedMesh]
    ? sceneState.scene[selectedMesh].visual_state
    : 'NORMAL'

  if (loading) return (
    <div style={styles.container}>
      <div style={styles.loadingText}>Loading visualization...</div>
    </div>
  )
  if (error) return (
    <div style={styles.container}>
      <div style={styles.errorText}>{error}</div>
    </div>
  )

  // Build unique component list from mappings + diagnosis cases
  const allComponents = [
    ...meshMappings.map(m => ({
      code: m.component_code,
      name: m.component_name,
      system: m.vehicle_system,
      meshId: m.mesh_identifier,
    })),
    ...diagCases
      .filter(c => !meshMappings.find(m => m.component_code === c.component_code))
      .map(c => ({
        code: c.component_code,
        name: c.component_name,
        system: c.vehicle_system,
        meshId: null,
      })),
  ]
  // Deduplicate by component code
  const uniqueComponents = Array.from(
    new Map(allComponents.map(c => [c.code, c])).values()
  )

  return (
    <div style={styles.wrapper}>
      {/* Left panel — component list */}
      <div style={styles.leftPanel}>
        <h3 style={styles.panelTitle}>Components</h3>
        <div style={styles.componentList}>
          {uniqueComponents.length === 0 && (
            <p style={styles.emptyText}>No components mapped for this vehicle.</p>
          )}
          {uniqueComponents.map(comp => {
            const meshState = comp.meshId && sceneState?.scene[comp.meshId]
              ? sceneState.scene[comp.meshId].visual_state
              : 'UNMAPPED'
            const diagCase = diagCases.find(c => c.component_code === comp.code)
            const isSelected = comp.code === selectedCode
            return (
              <button
                key={comp.code}
                onClick={() => {
                  setSelectedCode(comp.code)
                  setSelectedMesh(comp.meshId ?? null)
                }}
                style={{
                  ...styles.componentItem,
                  background: isSelected ? '#1e2219' : 'transparent',
                  borderColor: isSelected ? '#B8E36A' : '#2a2d26',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{
                    width: '8px', height: '8px', borderRadius: '50%',
                    background: VISUAL_STATE_COLOURS[meshState as keyof typeof VISUAL_STATE_COLOURS] ?? '#858A7E',
                    flexShrink: 0,
                  }} />
                  <span style={styles.compName}>{comp.name}</span>
                </div>
                <span style={styles.compSystem}>{comp.system.replace('_', ' ')}</span>
                {diagCase && (
                  <span style={{
                    fontSize: '0.65rem',
                    color: VISUAL_STATE_COLOURS[meshState as keyof typeof VISUAL_STATE_COLOURS],
                    marginTop: '0.15rem',
                  }}>
                    {diagCase.diagnosis_status.replace(/_/g, ' ')}
                  </span>
                )}
              </button>
            )
          })}
        </div>
      </div>

      {/* Right panel — 3D viewer */}
      <div style={styles.rightPanel}>
        <TruckViewer3D
          modelUrl="/models/refuse-collection-truck.glb"
          sceneState={sceneState}
          selectedMesh={selectedMesh}
          onMeshClick={handleMeshClick}
          height="460px"
        />

        {/* Component info panel */}
        {selectedCode && (
          <div style={styles.infoPanel}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <h4 style={styles.infoTitle}>
                  {selectedMapping?.component_name ?? selectedCode}
                </h4>
                <span style={styles.infoCode}>{selectedCode}</span>
              </div>
              <span style={{
                fontSize: '0.7rem',
                padding: '0.2rem 0.6rem',
                borderRadius: '999px',
                background: VISUAL_STATE_COLOURS[visualState as keyof typeof VISUAL_STATE_COLOURS] + '22',
                color:      VISUAL_STATE_COLOURS[visualState as keyof typeof VISUAL_STATE_COLOURS],
                border: `1px solid ${VISUAL_STATE_COLOURS[visualState as keyof typeof VISUAL_STATE_COLOURS]}44`,
              }}>
                {VISUAL_STATE_LABELS[visualState as keyof typeof VISUAL_STATE_LABELS]}
              </span>
            </div>

            {selectedCase ? (
              <div style={{ marginTop: '0.75rem' }}>
                <p style={styles.infoLabel}>Mechanic Verification</p>
                <p style={styles.infoValue}>{selectedCase.mechanic_verification.replace(/_/g, ' ')}</p>
                {selectedCase.final_notes && (
                  <>
                    <p style={styles.infoLabel}>Notes</p>
                    <p style={styles.infoValue}>{selectedCase.final_notes}</p>
                  </>
                )}
                {selectedCase.evidence.length > 0 && (
                  <>
                    <p style={styles.infoLabel}>Evidence ({selectedCase.evidence.length})</p>
                    {selectedCase.evidence.slice(0, 3).map((ev, i) => (
                      <div key={i} style={styles.evidenceItem}>
                        <span style={styles.evidenceType}>{ev.evidence_type.replace(/_/g, ' ')}</span>
                        <p style={styles.evidenceDesc}>{ev.evidence_description}</p>
                      </div>
                    ))}
                  </>
                )}
              </div>
            ) : (
              <p style={{ ...styles.infoValue, marginTop: '0.5rem', color: '#858A7E' }}>
                {selectedMesh
                  ? 'No diagnosis case recorded for this component.'
                  : 'Component not mapped in 3D model (UNMAPPED).'}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Styles
// ---------------------------------------------------------------------------
const styles: Record<string, React.CSSProperties> = {
  wrapper: {
    display: 'grid',
    gridTemplateColumns: '260px 1fr',
    gap: '1rem',
    height: '100%',
    fontFamily: 'Manrope, sans-serif',
  },
  container: {
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    height: '400px', background: '#10110F', borderRadius: '8px',
  },
  loadingText: { color: '#858A7E', fontFamily: 'DM Mono, monospace', fontSize: '0.75rem' },
  errorText:   { color: '#B96859', fontSize: '0.875rem' },
  leftPanel: {
    background: '#1A1D18',
    border: '1px solid #2a2d26',
    borderRadius: '8px',
    overflow: 'hidden',
    display: 'flex',
    flexDirection: 'column',
  },
  panelTitle: {
    color: '#F4F4F0', fontSize: '0.75rem', fontWeight: 600,
    letterSpacing: '0.1em', textTransform: 'uppercase',
    padding: '0.75rem 1rem',
    borderBottom: '1px solid #2a2d26',
    margin: 0,
  },
  componentList: { overflowY: 'auto', flex: 1, padding: '0.25rem' },
  componentItem: {
    width: '100%', textAlign: 'left', cursor: 'pointer',
    border: '1px solid transparent', borderRadius: '6px',
    padding: '0.5rem 0.75rem',
    marginBottom: '0.25rem',
    display: 'flex', flexDirection: 'column', gap: '0.1rem',
    transition: 'background 150ms, border-color 150ms',
  },
  compName:   { color: '#F4F4F0', fontSize: '0.8rem', fontWeight: 500 },
  compSystem: { color: '#858A7E', fontSize: '0.65rem', fontFamily: 'DM Mono, monospace' },
  emptyText:  { color: '#858A7E', fontSize: '0.8rem', padding: '1rem', textAlign: 'center' },
  rightPanel: { display: 'flex', flexDirection: 'column', gap: '1rem' },
  infoPanel: {
    background: '#1A1D18', border: '1px solid #2a2d26',
    borderRadius: '8px', padding: '1rem',
  },
  infoTitle: { color: '#F4F4F0', fontSize: '0.95rem', fontWeight: 600, margin: 0 },
  infoCode:  { color: '#858A7E', fontSize: '0.7rem', fontFamily: 'DM Mono, monospace' },
  infoLabel: { color: '#858A7E', fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.08em', margin: '0.5rem 0 0.15rem' },
  infoValue: { color: '#F4F4F0', fontSize: '0.85rem', margin: 0 },
  evidenceItem: { background: '#10110F', borderRadius: '4px', padding: '0.5rem', marginBottom: '0.35rem' },
  evidenceType: { color: '#B8E36A', fontSize: '0.65rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase' },
  evidenceDesc: { color: '#858A7E', fontSize: '0.75rem', margin: '0.15rem 0 0' },
}
