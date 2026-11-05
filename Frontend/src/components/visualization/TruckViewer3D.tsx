/**
 * VEDA V2 — TruckViewer3D
 *
 * Loads a GLB model via React Three Fiber and highlights meshes
 * according to their diagnostic visual state.
 *
 * RULES:
 * - Only mapped components are highlighted — unmapped meshes stay grey.
 * - Visual states come from the backend; never inferred client-side.
 * - Camera, lighting and materials are performance-conscious.
 */

import { Suspense, useRef, useMemo, useCallback } from 'react'
import { Canvas, useFrame, ThreeEvent } from '@react-three/fiber'
import { useGLTF, OrbitControls, Environment, Html } from '@react-three/drei'
import * as THREE from 'three'
import type { SceneState, VisualState } from '../../types/digital-twin'
import { VISUAL_STATE_COLOURS } from '../../types/digital-twin'

// ---------------------------------------------------------------------------
// Colour constants
// ---------------------------------------------------------------------------
const UNSELECTED_COLOUR  = new THREE.Color('#2a2d26')  // dark graphite
const SELECTED_COLOUR    = new THREE.Color('#B8E36A')   // industrial lime
const HOVER_COLOUR       = new THREE.Color('#d4ff88')

const stateColour = (state: VisualState): THREE.Color =>
  new THREE.Color(VISUAL_STATE_COLOURS[state] ?? VISUAL_STATE_COLOURS.NORMAL)

// ---------------------------------------------------------------------------
// Inner scene — loaded inside <Suspense>
// ---------------------------------------------------------------------------
interface TruckSceneProps {
  modelUrl:         string
  sceneState:       SceneState | null
  selectedMesh:     string | null
  onMeshClick:      (meshId: string | null, componentCode: string | null) => void
}

function TruckScene({ modelUrl, sceneState, selectedMesh, onMeshClick }: TruckSceneProps) {
  const { scene } = useGLTF(modelUrl)
  const hoveredRef = useRef<string | null>(null)

  // Build a map of mesh name -> colour based on current scene state
  const colourMap = useMemo(() => {
    const map: Record<string, THREE.Color> = {}
    if (!sceneState) return map
    for (const [meshId, meshState] of Object.entries(sceneState.scene)) {
      map[meshId] = stateColour(meshState.visual_state as VisualState)
    }
    return map
  }, [sceneState])

  // Apply colours to all meshes
  useFrame(() => {
    scene.traverse((child) => {
      if (!(child instanceof THREE.Mesh)) return
      const name = child.name

      const isSelected = name === selectedMesh
      const isHovered  = name === hoveredRef.current
      const mappedColour = colourMap[name]

      const mat = child.material as THREE.MeshStandardMaterial
      if (!mat || typeof mat.color === 'undefined') return

      if (isSelected) {
        mat.color.copy(SELECTED_COLOUR)
        mat.emissive?.copy(SELECTED_COLOUR).multiplyScalar(0.3)
      } else if (isHovered) {
        mat.color.copy(HOVER_COLOUR)
        mat.emissive?.copy(HOVER_COLOUR).multiplyScalar(0.15)
      } else if (mappedColour) {
        mat.color.copy(mappedColour)
        mat.emissive?.set(0, 0, 0)
      } else {
        mat.color.copy(UNSELECTED_COLOUR)
        mat.emissive?.set(0, 0, 0)
      }
    })
  })

  const handlePointerOver = useCallback((e: ThreeEvent<PointerEvent>) => {
    e.stopPropagation()
    const name = (e.object as THREE.Mesh).name
    if (sceneState?.scene[name]) {
      hoveredRef.current = name
      document.body.style.cursor = 'pointer'
    }
  }, [sceneState])

  const handlePointerOut = useCallback((_e: ThreeEvent<PointerEvent>) => {
    hoveredRef.current = null
    document.body.style.cursor = 'default'
  }, [])

  const handleClick = useCallback((e: ThreeEvent<MouseEvent>) => {
    e.stopPropagation()
    const name = (e.object as THREE.Mesh).name
    if (sceneState?.scene[name]) {
      const meshState = sceneState.scene[name]
      onMeshClick(name, meshState.component_code)
    } else {
      onMeshClick(null, null)
    }
  }, [sceneState, onMeshClick])

  return (
    <primitive
      object={scene}
      scale={0.8}
      position={[0, -1, 0]}
      onPointerOver={handlePointerOver}
      onPointerOut={handlePointerOut}
      onClick={handleClick}
    />
  )
}

// ---------------------------------------------------------------------------
// Loading overlay
// ---------------------------------------------------------------------------
function LoadingOverlay() {
  return (
    <Html center>
      <div style={{
        color: '#B8E36A',
        fontFamily: 'DM Mono, monospace',
        fontSize: '0.75rem',
        letterSpacing: '0.1em',
        textTransform: 'uppercase',
      }}>
        Loading 3D Model...
      </div>
    </Html>
  )
}

// ---------------------------------------------------------------------------
// Status legend
// ---------------------------------------------------------------------------
function StatusLegend() {
  const states: [VisualState, string][] = [
    ['NORMAL',           'Normal'],
    ['SUSPECTED',        'Suspected Fault'],
    ['MECHANIC_VERIFIED','Mechanic Verified'],
    ['REPAIRED',         'Repaired'],
    ['UNMAPPED',         'Unmapped'],
  ]
  return (
    <div style={{
      position: 'absolute',
      bottom: '1rem',
      left: '1rem',
      background: 'rgba(26,29,24,0.92)',
      border: '1px solid #2a2d26',
      borderRadius: '6px',
      padding: '0.75rem 1rem',
      display: 'flex',
      flexDirection: 'column',
      gap: '0.4rem',
      pointerEvents: 'none',
    }}>
      {states.map(([state, label]) => (
        <div key={state} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div style={{
            width: '10px', height: '10px', borderRadius: '50%',
            background: VISUAL_STATE_COLOURS[state],
            flexShrink: 0,
          }} />
          <span style={{
            fontSize: '0.7rem', color: '#858A7E',
            fontFamily: 'DM Mono, monospace',
          }}>{label}</span>
        </div>
      ))}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Public component
// ---------------------------------------------------------------------------
export interface TruckViewer3DProps {
  modelUrl:         string
  sceneState:       SceneState | null
  selectedMesh?:    string | null
  onMeshClick?:     (meshId: string | null, componentCode: string | null) => void
  height?:          string
}

export function TruckViewer3D({
  modelUrl,
  sceneState,
  selectedMesh = null,
  onMeshClick = () => {},
  height = '480px',
}: TruckViewer3DProps) {
  return (
    <div style={{ position: 'relative', width: '100%', height, background: '#10110F', borderRadius: '8px', overflow: 'hidden' }}>
      <Canvas
        camera={{ position: [6, 3, 8], fov: 45 }}
        gl={{ antialias: true, alpha: false }}
        shadows={false}
      >
        <ambientLight intensity={0.8} />
        <directionalLight position={[5, 10, 5]} intensity={1.2} />
        <directionalLight position={[-5, 5, -5]} intensity={0.4} />
        <Suspense fallback={<LoadingOverlay />}>
          <TruckScene
            modelUrl={modelUrl}
            sceneState={sceneState}
            selectedMesh={selectedMesh}
            onMeshClick={onMeshClick}
          />
          <Environment preset="warehouse" />
        </Suspense>
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minDistance={2}
          maxDistance={20}
          target={[0, 0, 0]}
        />
      </Canvas>
      <StatusLegend />
    </div>
  )
}

// Preload the GLB for faster initial render
useGLTF.preload('/models/refuse-collection-truck.glb')
