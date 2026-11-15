import { useState, useEffect, useRef, Suspense } from 'react'
import { Canvas, useThree } from '@react-three/fiber'
import { useGLTF, OrbitControls, Environment } from '@react-three/drei'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js'
import { useLoader } from '@react-three/fiber'
import * as THREE from 'three'

interface ApsResult {
  status: string
  model_name: string
  model_version: string
  predicted_class: string | null
  predicted_label: string | null
  probability_positive: number | null
  feature_coverage: number
  scope_warning: string
  error_message: string
}

export default function App() {
  const [page, setPage] = useState('home')

  return (
    <div style={{ background: '#0A0A0A', minHeight: '100vh', fontFamily: 'Manrope, sans-serif', color: '#F4F4F0' }}>
      <Navbar setPage={setPage} activePage={page} />
      {page === 'home'      && <HomePage />}
      {page === 'shop'      && <ShopPage />}
      {page === 'platform'  && <PlatformPage />}
      {page === 'developer' && <DeveloperPage />}
    </div>
  )
}

/* ── Navbar ──────────────────────────────────────────────── */
function Navbar({ setPage, activePage }: { setPage: (p: string) => void; activePage: string }) {
  return (
    <nav style={{
      position: 'fixed', top: 0, left: 0, right: 0, zIndex: 999,
      height: '56px',
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '0 40px',
      background: 'rgba(10,10,10,0.85)',
      backdropFilter: 'blur(14px)',
      borderBottom: '1px solid rgba(255,255,255,0.05)',
    }}>
      <button onClick={() => setPage('home')} style={logoBtn}>VEDA</button>
      <div style={{ display: 'flex', gap: '4px' }}>
        {[
          { id: 'home',      label: 'Home'      },
          { id: 'shop',      label: 'Shop'      },
          { id: 'platform',  label: 'Platform'  },
          { id: 'developer', label: 'Developer' },
        ].map(item => (
          <button key={item.id} onClick={() => setPage(item.id)} style={{
            background: activePage === item.id ? '#B8E36A' : 'transparent',
            color:      activePage === item.id ? '#0A0A0A'  : '#858A7E',
            border: 'none', borderRadius: '6px', padding: '6px 16px',
            fontSize: '0.83rem', fontWeight: activePage === item.id ? 700 : 400,
            cursor: 'pointer', fontFamily: 'Manrope, sans-serif', transition: 'all 180ms',
          }}>{item.label}</button>
        ))}
      </div>
    </nav>
  )
}

const logoBtn: React.CSSProperties = {
  background: 'none', border: 'none', cursor: 'pointer',
  color: '#F4F4F0', fontSize: '1.1rem', fontWeight: 800,
  letterSpacing: '0.18em', fontFamily: 'Manrope, sans-serif', padding: 0,
}

/* ── Truck 3D model ──────────────────────────────────────── */
function TruckModel() {
  const { scene } = useGLTF('/models/refuse-collection-truck.glb')
  return <primitive object={scene} scale={0.6} position={[0, -0.8, 0]} rotation={[0, 0.4, 0]} />
}

/* ── Home page — scroll split + truck reveal ─────────────── */
function HomePage() {
  const containerRef = useRef<HTMLDivElement>(null)
  const [scrollY, setScrollY] = useState(0)
  const [maxScroll, setMaxScroll] = useState(1)

  useEffect(() => {
    const el = containerRef.current
    if (!el) return
    const onScroll = () => {
      setScrollY(el.scrollTop)
      setMaxScroll(el.scrollHeight - el.clientHeight || 1)
    }
    el.addEventListener('scroll', onScroll)
    return () => el.removeEventListener('scroll', onScroll)
  }, [])

  // 0 → 1 as you scroll down, back to 0 as you scroll up
  const progress = Math.min(Math.max(scrollY / (maxScroll * 0.65), 0), 1)

  // VE moves left, DA moves right
  const shift = progress * 320

  // Truck scales from 0 → full as VE/DA split
  // starts appearing at progress 0.2, full size at progress 1
  const truckProgress = Math.max(0, (progress - 0.15) / 0.85)
  const truckScale    = truckProgress          // 0 → 1
  const truckOpacity  = truckProgress

  // Canvas size: starts at 0, grows to fill the gap (600px wide at full)
  const canvasSize = Math.round(truckScale * 580)

  return (
    <div
      ref={containerRef}
      style={{ height: '100vh', overflowY: 'scroll', paddingTop: '56px', scrollbarWidth: 'none' }}
    >
      {/* Tall area to allow scroll */}
      <div style={{ height: '320vh' }}>

        {/* Sticky hero */}
        <div style={{
          position: 'sticky', top: '56px',
          height: 'calc(100vh - 56px)',
          display: 'flex', flexDirection: 'column',
          alignItems: 'center', justifyContent: 'center',
          overflow: 'hidden',
        }}>

          {/* VEDA split row */}
          <div style={{
            position: 'relative',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            width: '100%', height: 'clamp(100px, 20vw, 220px)',
          }}>

            {/* VE — slides left */}
            <span style={{
              fontSize: 'clamp(5rem, 18vw, 15rem)',
              fontWeight: 800, letterSpacing: '-0.02em', lineHeight: 1,
              color: '#F4F4F0',
              position: 'absolute',
              transform: `translateX(calc(-50% - ${shift}px))`,
              transition: 'transform 0.08s ease-out',
              whiteSpace: 'nowrap',
            }}>VE</span>

            {/* Truck canvas — appears in the gap */}
            {canvasSize > 10 && (
              <div style={{
                position: 'absolute',
                width:   `${canvasSize}px`,
                height:  `${canvasSize * 0.62}px`,
                opacity: truckOpacity,
                transition: 'opacity 0.08s ease-out',
                zIndex: 2,
                pointerEvents: truckScale > 0.95 ? 'auto' : 'none',
              }}>
                <Canvas camera={{ position: [3, 1.5, 5], fov: 42 }} style={{ background: 'transparent' }}>
                  <ambientLight intensity={0.9} />
                  <directionalLight position={[5, 8, 5]} intensity={1.4} />
                  <Suspense fallback={null}>
                    <TruckModel />
                    <Environment preset="warehouse" />
                  </Suspense>
                  {truckScale > 0.95 && <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.6} />}
                </Canvas>
              </div>
            )}

            {/* DA — slides right */}
            <span style={{
              fontSize: 'clamp(5rem, 18vw, 15rem)',
              fontWeight: 800, letterSpacing: '-0.02em', lineHeight: 1,
              color: '#B8E36A',
              position: 'absolute',
              transform: `translateX(calc(50% + ${shift}px))`,
              transition: 'transform 0.08s ease-out',
              whiteSpace: 'nowrap',
            }}>DA</span>
          </div>

          {/* Tagline — fades in near the end */}
          <p style={{
            marginTop: '24px',
            color: '#858A7E',
            fontSize: 'clamp(0.8rem, 1.5vw, 0.95rem)',
            fontFamily: 'DM Mono, monospace',
            letterSpacing: '0.1em',
            opacity: Math.max(0, (progress - 0.7) / 0.3),
            transition: 'opacity 0.04s linear',
            textAlign: 'center',
          }}>
            Vehicle Evaluation Diagnostic Agents
          </p>

          {/* About text — fades in after progress 0.85 */}
          <div style={{
            marginTop: '20px',
            maxWidth: '500px',
            textAlign: 'center',
            opacity: Math.max(0, (progress - 0.82) / 0.18),
            transition: 'opacity 0.04s linear',
            padding: '0 24px',
          }}>
            <p style={{ color: '#555', fontSize: 'clamp(0.78rem, 1.3vw, 0.88rem)', lineHeight: 1.75, margin: 0 }}>
              AI-assisted diagnostics for heavy vehicles.
            </p>
            <p style={{ color: '#555', fontSize: 'clamp(0.78rem, 1.3vw, 0.88rem)', lineHeight: 1.75, margin: '4px 0 0' }}>
              Connecting owners, mechanics and service centres
              through transparent, evidence-driven repairs.
            </p>
          </div>

          {/* Scroll hint */}
          <div style={{
            position: 'absolute', bottom: '28px',
            opacity: Math.max(0, 1 - progress * 5),
            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px',
          }}>
            <span style={{ color: '#333', fontSize: '0.65rem', letterSpacing: '0.14em', textTransform: 'uppercase', fontFamily: 'DM Mono, monospace' }}>scroll</span>
            <div style={{ width: '1px', height: '28px', background: 'linear-gradient(to bottom, #333, transparent)' }} />
          </div>

        </div>
      </div>
    </div>
  )
}

/* ── 3D model viewers ────────────────────────────────────── */
function GLBModel({ path, scale }: { path: string; scale: number }) {
  const { scene } = useGLTF(path)

  const box    = new THREE.Box3().setFromObject(scene)
  const center = new THREE.Vector3()
  box.getCenter(center)

  return (
    <group scale={scale}>
      <primitive object={scene} position={[-center.x, -center.y, -center.z]} />
    </group>
  )
}

/* Auto-fitting camera for any GLB — positions itself based on bounding box */
function AutoCamera({ path }: { path: string }) {
  const { scene } = useGLTF(path)
  const { camera } = useThree()

  useEffect(() => {
    const box  = new THREE.Box3().setFromObject(scene)
    const size = new THREE.Vector3()
    box.getSize(size)
    const maxDim  = Math.max(size.x, size.y, size.z)
    const fov     = (camera as THREE.PerspectiveCamera).fov * (Math.PI / 180)
    const dist    = (maxDim / 2) / Math.tan(fov / 2) * 1.6
    camera.position.set(dist * 0.6, dist * 0.4, dist)
    camera.near = dist * 0.001
    camera.far  = dist * 10
    camera.updateProjectionMatrix()
  }, [scene, camera])

  return null
}

function OBJModel({ path, scale }: { path: string; scale: number }) {
  const obj = useLoader(OBJLoader, path)

  // Apply material to all meshes
  obj.traverse((child) => {
    if (child instanceof THREE.Mesh) {
      child.material = new THREE.MeshStandardMaterial({
        color: '#a8a8a8', metalness: 0.75, roughness: 0.25,
        side: THREE.DoubleSide,
      })
    }
  })

  // Compute bounding box and center offset
  const box    = new THREE.Box3().setFromObject(obj)
  const center = new THREE.Vector3()
  box.getCenter(center)

  // Return inside a group that offsets by negative center — brings model to origin
  return (
    <group scale={scale}>
      <primitive object={obj} position={[-center.x, -center.y, -center.z]} />
    </group>
  )
}

/* ── Visual Diagnosis Overlay ────────────────────────────── */
function VisualDiagnosisOverlay({
  result, onClose,
}: {
  result: MechanicResult
  onClose: () => void
}) {
  const health = result.component_health ?? {}
  const model3d = result.model_3d

  // Sort: CRITICAL first, then WARNING, then GOOD
  const order = { CRITICAL: 0, WARNING: 1, GOOD: 2 }
  const sorted = Object.entries(COMPONENT_LABELS).sort(([a], [b]) => {
    const ca = order[health[a]?.condition as keyof typeof order] ?? 2
    const cb = order[health[b]?.condition as keyof typeof order] ?? 2
    return ca - cb
  })

  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 9999,
      background: 'rgba(5,5,5,0.97)',
      backdropFilter: 'blur(8px)',
      overflowY: 'auto',
      fontFamily: 'Manrope, sans-serif',
    }}>
      {/* Header */}
      <div style={{
        position: 'sticky', top: 0,
        background: 'rgba(10,10,10,0.95)',
        backdropFilter: 'blur(12px)',
        borderBottom: '1px solid #1e1e1e',
        padding: '0 32px',
        height: '56px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        zIndex: 10,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#FF3B3B', boxShadow: '0 0 8px #FF3B3B' }} />
          <span style={{ color: '#F4F4F0', fontWeight: 700, fontSize: '0.95rem', letterSpacing: '-0.01em' }}>
            Visual Diagnosis Report
          </span>
        </div>
        <button onClick={onClose} style={{
          background: 'none', border: '1px solid #2a2a2a', color: '#858A7E',
          borderRadius: '6px', padding: '6px 16px', cursor: 'pointer',
          fontSize: '0.8rem', fontFamily: 'Manrope, sans-serif',
        }}>
          Close ✕
        </button>
      </div>

      <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '40px 24px 80px' }}>

        {/* Legend */}
        <div style={{ display: 'flex', gap: '24px', marginBottom: '36px', justifyContent: 'center', flexWrap: 'wrap' }}>
          {[
            { colour: '#FF3B3B', label: 'CRITICAL — Needs immediate replacement' },
            { colour: '#FFB347', label: 'WARNING — Monitor closely' },
            { colour: '#4ADE80', label: 'GOOD — No action needed' },
          ].map(l => (
            <div key={l.label} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: l.colour, boxShadow: `0 0 8px ${l.colour}88`, flexShrink: 0 }} />
              <span style={{ color: '#858A7E', fontSize: '0.78rem', fontFamily: 'DM Mono, monospace' }}>{l.label}</span>
            </div>
          ))}
        </div>

        {/* Main layout: 3D model left, component cards right */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', alignItems: 'start' }}>

          {/* 3D model — predicted component with health colour glow */}
          <div>
            <p style={{ color: '#555', fontSize: '0.7rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.08em', margin: '0 0 10px' }}>
              Predicted Faulty Component
            </p>
            <h3 style={{ color: '#FF3B3B', fontSize: '1.1rem', fontWeight: 700, margin: '0 0 16px', letterSpacing: '-0.01em' }}>
              {COMPONENT_LABELS[result.predicted_component] ?? result.predicted_component}
            </h3>

            {model3d ? (
              <div style={{
                width: '100%', height: '360px',
                background: '#080808',
                border: '1px solid #FF3B3B44',
                borderRadius: '12px', overflow: 'hidden',
                boxShadow: '0 0 60px #FF3B3B22',
              }}>
                <Canvas camera={{ position: [4, 2, 7], fov: 50 }} style={{ background: 'transparent' }}>
                  <ambientLight intensity={0.6} />
                  <directionalLight position={[5, 8, 5]} intensity={1.5} color="#FF3B3B" />
                  <directionalLight position={[-4, 2, -3]} intensity={0.5} />
                  <Suspense fallback={null}>
                    {model3d.type === 'glb'
                      ? <GLBModelTinted path={`/models/${model3d.file}`} colour="#FF3B3B" />
                      : <OBJModelTinted path={`/models/${model3d.file}`} colour="#FF3B3B" />
                    }
                    {model3d.type === 'glb' && <AutoCamera path={`/models/${model3d.file}`} />}
                    <Environment preset="warehouse" />
                  </Suspense>
                  <OrbitControls enableZoom autoRotate autoRotateSpeed={1.2} target={[0,0,0]} />
                </Canvas>
              </div>
            ) : (
              <div style={{ background: '#111', border: '1px solid #FF3B3B33', borderRadius: '12px', padding: '48px', textAlign: 'center' }}>
                <p style={{ color: '#FF3B3B', fontWeight: 700, fontSize: '1rem', margin: '0 0 8px' }}>CRITICAL</p>
                <p style={{ color: '#858A7E', fontSize: '0.85rem', margin: 0 }}>No 3D model for {COMPONENT_LABELS[result.predicted_component]}</p>
              </div>
            )}

            {/* Confidence bar */}
            <div style={{ marginTop: '16px', background: '#111', border: '1px solid #1e1e1e', borderRadius: '8px', padding: '14px 16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ color: '#555', fontSize: '0.72rem', fontFamily: 'DM Mono, monospace' }}>AI Confidence</span>
                <span style={{ color: '#FF3B3B', fontWeight: 700, fontFamily: 'DM Mono, monospace', fontSize: '0.82rem' }}>
                  {(result.confidence * 100).toFixed(1)}%
                </span>
              </div>
              <div style={{ background: '#1a1a1a', borderRadius: '4px', height: '6px', overflow: 'hidden' }}>
                <div style={{ width: `${result.confidence * 100}%`, height: '100%', background: '#FF3B3B', borderRadius: '4px', boxShadow: '0 0 8px #FF3B3B88', transition: 'width 0.5s ease' }} />
              </div>
            </div>
          </div>

          {/* Component health cards */}
          <div>
            <p style={{ color: '#555', fontSize: '0.7rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.08em', margin: '0 0 12px' }}>
              All Component Health Status
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {sorted.map(([key, label]) => {
                const h = health[key] ?? { health_score: 85, condition: 'GOOD', colour: '#4ADE80' }
                const isPredicted = key === result.predicted_component
                return (
                  <div key={key} style={{
                    background: isPredicted ? `${h.colour}0d` : '#111',
                    border: `1px solid ${isPredicted ? h.colour + '55' : '#1e1e1e'}`,
                    borderRadius: '8px', padding: '12px 16px',
                    transition: 'all 200ms',
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: h.colour, boxShadow: `0 0 6px ${h.colour}88`, flexShrink: 0 }} />
                        <span style={{ color: isPredicted ? '#F4F4F0' : '#D0D0C8', fontSize: '0.85rem', fontWeight: isPredicted ? 700 : 400 }}>
                          {label}
                          {isPredicted && <span style={{ color: h.colour, fontSize: '0.7rem', fontFamily: 'DM Mono, monospace', marginLeft: '8px' }}>← PREDICTED FAULT</span>}
                        </span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ color: h.colour, fontSize: '0.72rem', fontFamily: 'DM Mono, monospace', fontWeight: 700 }}>{h.condition}</span>
                        <span style={{ color: '#555', fontSize: '0.72rem', fontFamily: 'DM Mono, monospace' }}>{h.health_score}</span>
                      </div>
                    </div>
                    {/* Health bar */}
                    <div style={{ background: '#1a1a1a', borderRadius: '3px', height: '4px', overflow: 'hidden' }}>
                      <div style={{
                        width: `${h.health_score}%`, height: '100%',
                        background: h.colour,
                        borderRadius: '3px',
                        boxShadow: `0 0 6px ${h.colour}66`,
                        transition: 'width 0.6s ease',
                      }} />
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

/* ── Tinted 3D models for visual diagnosis ───────────────── */
function GLBModelTinted({ path, colour }: { path: string; colour: string }) {
  const { scene } = useGLTF(path)
  const col = new THREE.Color(colour)

  const box    = new THREE.Box3().setFromObject(scene)
  const center = new THREE.Vector3()
  box.getCenter(center)

  scene.traverse(child => {
    if (child instanceof THREE.Mesh) {
      child.material = new THREE.MeshStandardMaterial({
        color: col, metalness: 0.6, roughness: 0.3,
        emissive: col, emissiveIntensity: 0.15,
      })
    }
  })

  return (
    <group>
      <primitive object={scene} position={[-center.x, -center.y, -center.z]} />
    </group>
  )
}

function OBJModelTinted({ path, colour }: { path: string; colour: string }) {
  const obj = useLoader(OBJLoader, path)
  const col = new THREE.Color(colour)

  const box    = new THREE.Box3().setFromObject(obj)
  const center = new THREE.Vector3()
  box.getCenter(center)

  obj.traverse(child => {
    if (child instanceof THREE.Mesh) {
      child.material = new THREE.MeshStandardMaterial({
        color: col, metalness: 0.65, roughness: 0.3, side: THREE.DoubleSide,
        emissive: col, emissiveIntensity: 0.15,
      })
    }
  })

  return (
    <group>
      <primitive object={obj} position={[-center.x, -center.y, -center.z]} scale={0.8} />
    </group>
  )
}

/* ── Shop Page ───────────────────────────────────────────── */
function ShopPage() {
  const [categories, setCategories] = useState<import('./services/shop.service').ShopCategory[]>([])
  const [loading,    setLoading]    = useState(true)
  const [cart,       setCart]       = useState<Record<string, number>>({})
  const [search,     setSearch]     = useState('')
  const [activecat,  setActivecat]  = useState('all')
  const sessionId = useState(() => Math.random().toString(36).slice(2))[0]

  useEffect(() => {
    import('./services/shop.service').then(({ shopService }) =>
      shopService.list().then(data => { setCategories(data); setLoading(false) })
    )
  }, [])

  function addToCart(product: import('./services/shop.service').ShopProduct) {
    setCart(prev => ({ ...prev, [product.id]: (prev[product.id] ?? 0) + 1 }))
    import('./services/shop.service').then(({ shopService }) =>
      shopService.logCart(product.id, 1, sessionId)
    )
  }

  function removeFromCart(id: string) {
    setCart(prev => {
      const next = { ...prev }
      if ((next[id] ?? 0) > 1) next[id]--
      else delete next[id]
      return next
    })
  }

  const totalItems = Object.values(cart).reduce((a, b) => a + b, 0)
  const totalPrice = categories
    .flatMap(c => c.products)
    .reduce((acc, p) => acc + (cart[p.id] ?? 0) * parseFloat(p.price), 0)

  const allProducts = categories.flatMap(c => c.products)
  const filtered = allProducts.filter(p => {
    const matchSearch = search === '' ||
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      p.brand.toLowerCase().includes(search.toLowerCase()) ||
      p.part_number.toLowerCase().includes(search.toLowerCase())
    const matchCat = activecat === 'all' || categories.find(c => c.slug === activecat)?.products.some(cp => cp.id === p.id)
    return matchSearch && matchCat
  })
  const displayCats = activecat === 'all'
    ? categories
    : categories.filter(c => c.slug === activecat)

  return (
    <div style={{ paddingTop: '56px', minHeight: '100vh', background: '#0A0A0A' }}>

      {/* Shop header */}
      <div style={{ background: '#111', borderBottom: '1px solid #1e1e1e', padding: '20px 32px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <h1 style={{ color: '#F4F4F0', fontSize: '1.3rem', fontWeight: 800, margin: 0, letterSpacing: '-0.02em' }}>
            Spare Parts Store
          </h1>
          <p style={{ color: '#555', fontSize: '0.75rem', fontFamily: 'DM Mono, monospace', margin: '4px 0 0' }}>
            {allProducts.length} parts · Fast delivery to your workshop
          </p>
        </div>
        {/* Cart */}
        {totalItems > 0 && (
          <div style={{ background: '#1A1A1A', border: '1px solid #B8E36A44', borderRadius: '10px', padding: '10px 16px', display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ color: '#B8E36A', fontSize: '0.85rem', fontWeight: 600 }}>
              🛒 {totalItems} item{totalItems > 1 ? 's' : ''}
            </span>
            <span style={{ color: '#F4F4F0', fontWeight: 700, fontFamily: 'DM Mono, monospace' }}>
              ₹{totalPrice.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
            </span>
            <button style={{ background: '#B8E36A', color: '#0A0A0A', border: 'none', borderRadius: '6px', padding: '6px 14px', fontWeight: 700, fontSize: '0.8rem', cursor: 'pointer', fontFamily: 'Manrope, sans-serif' }}>
              Checkout
            </button>
          </div>
        )}
      </div>

      {/* Search + category filter */}
      <div style={{ padding: '16px 32px', display: 'flex', gap: '12px', alignItems: 'center', flexWrap: 'wrap', borderBottom: '1px solid #1a1a1a' }}>
        <input
          type="text" placeholder="Search parts, brands, part numbers..."
          value={search} onChange={e => setSearch(e.target.value)}
          style={{ flex: 1, minWidth: '200px', background: '#111', border: '1px solid #2a2a2a', borderRadius: '8px', padding: '10px 16px', color: '#F4F4F0', fontSize: '0.875rem', fontFamily: 'Manrope, sans-serif', outline: 'none' }}
        />
        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
          {[{ slug: 'all', name: 'All', icon: '🔍' }, ...categories].map(cat => (
            <button key={'slug' in cat ? cat.slug : 'all'} onClick={() => setActivecat('slug' in cat ? cat.slug : 'all')}
              style={{ background: activecat === ('slug' in cat ? cat.slug : 'all') ? '#B8E36A' : '#111', color: activecat === ('slug' in cat ? cat.slug : 'all') ? '#0A0A0A' : '#858A7E', border: `1px solid ${ activecat === ('slug' in cat ? cat.slug : 'all') ? '#B8E36A' : '#2a2a2a'}`, borderRadius: '6px', padding: '6px 12px', fontSize: '0.78rem', cursor: 'pointer', fontFamily: 'Manrope, sans-serif', fontWeight: activecat === ('slug' in cat ? cat.slug : 'all') ? 700 : 400, whiteSpace: 'nowrap' }}>
              {'icon' in cat ? cat.icon : ''} {'name' in cat ? cat.name : ''}
            </button>
          ))}
        </div>
      </div>

      {/* Products */}
      <div style={{ padding: '24px 32px' }}>
        {loading && <p style={{ color: '#555', textAlign: 'center', fontFamily: 'DM Mono, monospace', fontSize: '0.8rem' }}>Loading...</p>}

        {!loading && (search !== '' ? (
          // Search results
          <div>
            <p style={{ color: '#555', fontSize: '0.75rem', fontFamily: 'DM Mono, monospace', marginBottom: '16px' }}>{filtered.length} results for "{search}"</p>
            <ProductGrid products={filtered} cart={cart} onAdd={addToCart} onRemove={removeFromCart} />
          </div>
        ) : (
          // Category rows
          displayCats.map(cat => (
            <div key={cat.id} style={{ marginBottom: '40px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                <h2 style={{ color: '#F4F4F0', fontSize: '1rem', fontWeight: 700, margin: 0 }}>
                  {cat.icon} {cat.name}
                </h2>
                <span style={{ color: '#555', fontSize: '0.72rem', fontFamily: 'DM Mono, monospace' }}>{cat.products.length} products</span>
              </div>
              <ProductGrid products={cat.products} cart={cart} onAdd={addToCart} onRemove={removeFromCart} />
            </div>
          ))
        ))}
      </div>
    </div>
  )
}

function ProductGrid({ products, cart, onAdd, onRemove }: {
  products: import('./services/shop.service').ShopProduct[]
  cart: Record<string, number>
  onAdd: (p: import('./services/shop.service').ShopProduct) => void
  onRemove: (id: string) => void
}) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '12px' }}>
      {products.map(p => (
        <ProductCard key={p.id} product={p} qty={cart[p.id] ?? 0} onAdd={() => onAdd(p)} onRemove={() => onRemove(p.id)} />
      ))}
    </div>
  )
}

function ProductCard({ product: p, qty, onAdd, onRemove }: {
  product: import('./services/shop.service').ShopProduct
  qty: number; onAdd: () => void; onRemove: () => void
}) {
  return (
    <div style={{ background: '#111', border: `1px solid ${qty > 0 ? '#B8E36A44' : '#1e1e1e'}`, borderRadius: '10px', padding: '16px 14px', display: 'flex', flexDirection: 'column', gap: '8px', transition: 'border-color 150ms' }}>
      {/* Image */}
      <div style={{ width: '100%', aspectRatio: '1', background: '#1A1A1A', borderRadius: '8px', overflow: 'hidden', marginBottom: '4px', position: 'relative' }}>
        {p.image_path ? (
          <img
            src={`/shop/${p.image_path}`}
            alt={p.name}
            style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
            onError={e => { (e.target as HTMLImageElement).style.display = 'none' }}
          />
        ) : (
          <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '2.5rem' }}>
            {p.image_emoji}
          </div>
        )}
        {p.discount_percent > 0 && (
          <div style={{ position: 'absolute', top: '6px', left: '6px', background: '#B8E36A', color: '#0A0A0A', borderRadius: '4px', padding: '2px 6px', fontSize: '0.65rem', fontWeight: 700 }}>
            {p.discount_percent}% OFF
          </div>
        )}
        {!p.in_stock && (
          <div style={{ position: 'absolute', inset: 0, background: 'rgba(10,10,10,0.7)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ color: '#555', fontSize: '0.7rem', fontFamily: 'DM Mono, monospace' }}>OUT OF STOCK</span>
          </div>
        )}
      </div>
      {/* Details */}
      <div>
        <p style={{ color: '#858A7E', fontSize: '0.65rem', fontFamily: 'DM Mono, monospace', margin: '0 0 3px', textTransform: 'uppercase', letterSpacing: '0.06em' }}>{p.brand}</p>
        <p style={{ color: '#F4F4F0', fontSize: '0.82rem', fontWeight: 500, margin: 0, lineHeight: 1.4 }}>{p.name}</p>
        <p style={{ color: '#444', fontSize: '0.68rem', fontFamily: 'DM Mono, monospace', margin: '2px 0 0' }}>{p.part_number}</p>
      </div>
      {/* Price + Add */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 'auto' }}>
        <div>
          <p style={{ color: '#F4F4F0', fontWeight: 700, fontSize: '0.95rem', margin: 0, fontFamily: 'DM Mono, monospace' }}>
            ₹{parseFloat(p.price).toLocaleString('en-IN')}
          </p>
          {p.original_price && (
            <p style={{ color: '#444', fontSize: '0.72rem', textDecoration: 'line-through', margin: '1px 0 0', fontFamily: 'DM Mono, monospace' }}>
              ₹{parseFloat(p.original_price).toLocaleString('en-IN')}
            </p>
          )}
        </div>
        {p.in_stock ? (
          qty === 0 ? (
            <button onClick={onAdd} style={{ background: 'transparent', border: '1px solid #B8E36A', color: '#B8E36A', borderRadius: '6px', padding: '6px 14px', fontWeight: 700, fontSize: '0.8rem', cursor: 'pointer', fontFamily: 'Manrope, sans-serif' }}>
              ADD
            </button>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: '#B8E36A', borderRadius: '6px', padding: '4px 8px' }}>
              <button onClick={onRemove} style={{ background: 'none', border: 'none', color: '#0A0A0A', fontWeight: 800, fontSize: '1rem', cursor: 'pointer', lineHeight: 1, padding: '0 2px' }}>−</button>
              <span style={{ color: '#0A0A0A', fontWeight: 700, fontSize: '0.85rem', minWidth: '16px', textAlign: 'center' }}>{qty}</span>
              <button onClick={onAdd}    style={{ background: 'none', border: 'none', color: '#0A0A0A', fontWeight: 800, fontSize: '1rem', cursor: 'pointer', lineHeight: 1, padding: '0 2px' }}>+</button>
            </div>
          )
        ) : (
          <button disabled style={{ background: '#1a1a1a', border: '1px solid #2a2a2a', color: '#333', borderRadius: '6px', padding: '6px 14px', fontSize: '0.8rem', cursor: 'not-allowed' }}>
            SOLD OUT
          </button>
        )}
      </div>
    </div>
  )
}

/* ── About (kept for Developer page reference) ───────────── */
/* ── Platform — APS AI Demo ──────────────────────────────── */
function PlatformPage() {
  const [file,     setFile]     = useState<File | null>(null)
  const [loading,  setLoading]  = useState(false)
  const [result,   setResult]   = useState<ApsResult | null>(null)
  const [error,    setError]    = useState('')
  const inputRef = useRef<HTMLInputElement>(null)

  async function runInference() {
    if (!file) return
    setLoading(true); setResult(null); setError('')
    try {
      const form = new FormData()
      form.append('file', file)
      const res  = await fetch('http://localhost:8000/api/v1/diagnosis/demo/', { method: 'POST', body: form })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error ?? 'Request failed')
      setResult(data)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Something went wrong.')
    } finally { setLoading(false) }
  }

  const isPos       = result?.predicted_class === 'pos'
  const isNeg       = result?.predicted_class === 'neg'
  const isInsuf     = result?.status === 'insufficient_data'
  const resultColor = isPos ? '#B96859' : isNeg ? '#91B957' : '#C89B4B'

  return (
    <div style={{ paddingTop: '56px', minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '100px 24px 80px' }}>

      {/* ── SECTION 1: APS AI ── */}
      <p style={mono}>APS Diagnostic AI</p>
      <h2 style={{ ...heading, textAlign: 'center', marginBottom: '8px' }}>Air Pressure System Failure Detection</h2>
      <p style={{ color: '#858A7E', fontSize: '0.85rem', textAlign: 'center', marginBottom: '40px', maxWidth: '480px', lineHeight: 1.6 }}>
        Upload a CSV file with Scania APS sensor data. The model classifies whether an APS failure is present.
      </p>

      <div onClick={() => inputRef.current?.click()} style={{
        width: '100%', maxWidth: '480px', border: `2px dashed ${file ? '#B8E36A' : '#2a2a2a'}`,
        borderRadius: '12px', padding: '40px 24px', textAlign: 'center', cursor: 'pointer',
        background: file ? 'rgba(184,227,106,0.04)' : '#111', transition: 'all 200ms', marginBottom: '16px',
      }}>
        <input ref={inputRef} type="file" accept=".csv" style={{ display: 'none' }}
          onChange={e => { const f = e.target.files?.[0]; if (f) { setFile(f); setResult(null); setError('') } }} />
        {file ? (
          <><div style={{ fontSize: '2rem', marginBottom: '8px' }}>📄</div>
            <p style={{ color: '#B8E36A', fontWeight: 600, margin: '0 0 4px' }}>{file.name}</p>
            <p style={{ color: '#858A7E', fontSize: '0.8rem', margin: 0 }}>Click to change</p></>
        ) : (
          <><div style={{ fontSize: '2rem', marginBottom: '10px' }}>⬆</div>
            <p style={{ color: '#F4F4F0', fontWeight: 600, margin: '0 0 4px' }}>Upload CSV file</p>
            <p style={{ color: '#555', fontSize: '0.8rem', margin: 0 }}>One header row + one data row — 170 APS features</p></>
        )}
      </div>

      <a href="/sample_aps_data.csv" download style={{ color: '#555', fontSize: '0.73rem', textDecoration: 'underline', marginBottom: '20px', fontFamily: 'DM Mono, monospace' }}>
        Download sample CSV
      </a>

      <button onClick={runInference} disabled={!file || loading} style={{
        background: file && !loading ? '#B8E36A' : '#1e1e1e', color: file && !loading ? '#0A0A0A' : '#444',
        border: 'none', borderRadius: '8px', padding: '13px 44px', fontSize: '0.9rem', fontWeight: 700,
        cursor: file && !loading ? 'pointer' : 'not-allowed', fontFamily: 'Manrope, sans-serif', marginBottom: '36px',
      }}>
        {loading ? 'Running...' : 'Run APS Diagnosis'}
      </button>

      {error && <div style={{ background: '#B9685911', border: '1px solid #B9685944', borderRadius: '8px', padding: '12px 20px', color: '#B96859', fontSize: '0.85rem', maxWidth: '480px', width: '100%', textAlign: 'center', marginBottom: '20px' }}>{error}</div>}

      {result && (
        <div style={{ width: '100%', maxWidth: '520px', background: '#111', border: `1px solid ${resultColor}44`, borderTop: `4px solid ${resultColor}`, borderRadius: '12px', padding: '28px', marginBottom: '0' }}>
          <div style={{ textAlign: 'center', marginBottom: '24px' }}>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '10px', background: `${resultColor}18`, borderRadius: '999px', padding: '9px 22px', marginBottom: '10px' }}>
              <div style={{ width: '9px', height: '9px', borderRadius: '50%', background: resultColor, boxShadow: `0 0 8px ${resultColor}` }} />
              <span style={{ color: resultColor, fontWeight: 800, fontSize: '0.95rem', letterSpacing: '0.08em' }}>{result.predicted_label ?? 'INSUFFICIENT DATA'}</span>
            </div>
            {result.probability_positive != null && (
              <p style={{ color: '#858A7E', fontSize: '0.83rem', margin: 0, fontFamily: 'DM Mono, monospace' }}>
                Probability: <strong style={{ color: '#F4F4F0' }}>{(result.probability_positive * 100).toFixed(1)}%</strong>
              </p>
            )}
            {isInsuf && <p style={{ color: '#858A7E', fontSize: '0.82rem', margin: '8px 0 0' }}>Not enough features for a reliable prediction.</p>}
          </div>
          {[['Model', result.model_name], ['Version', result.model_version], ['Coverage', `${(result.feature_coverage * 100).toFixed(1)}% of 170`], ['Status', result.status]].map(([k, v]) => (
            <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #1e1e1e' }}>
              <span style={{ color: '#555', fontSize: '0.76rem', fontFamily: 'DM Mono, monospace' }}>{k}</span>
              <span style={{ color: '#D0D0C8', fontSize: '0.82rem', fontWeight: 600 }}>{v}</span>
            </div>
          ))}
          <div style={{ marginTop: '16px', background: '#1a1a1a', borderRadius: '6px', padding: '10px 14px' }}>
            <p style={{ color: '#444', fontSize: '0.72rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.08em', margin: '0 0 4px' }}>Scope</p>
            <p style={{ color: '#444', fontSize: '0.76rem', lineHeight: 1.6, margin: 0 }}>{result.scope_warning}</p>
          </div>
        </div>
      )}

      {/* ── SECTION 2: Mechanic Component Diagnosis ── */}
      <MechanicDiagnosticSection />
    </div>
  )
}

/* ── Mechanic component types ────────────────────────────── */
interface MechanicResult {
  status: string
  predicted_component: string
  confidence: number
  top_3: Array<{ component: string; probability: number }>
  model_3d: { file: string; type: string } | null
  component_health: Record<string, { health_score: number; condition: string; colour: string }>
  scope_warning: string
}

const COMPONENT_LABELS: Record<string, string> = {
  wheels:        'Wheels & Hubs',
  suspension:    'Suspension & Axle',
  engine:        'Engine',
  cab:           'Cab Assembly',
  chassis:       'Chassis & Frame',
  rear_compactor:'Rear Compactor',
  refuse_body:   'Refuse Body',
  brake_caliper: 'Brake Caliper',
  tyres:         'Tyres',
}

const COMPONENT_COLOUR: Record<string, string> = {
  wheels: '#B8E36A', suspension: '#C89B4B', engine: '#B96859',
  cab: '#66869B', chassis: '#829B75', rear_compactor: '#C89B4B',
  refuse_body: '#66869B', brake_caliper: '#B96859', tyres: '#91B957',
}

function MechanicDiagnosticSection() {
  const [vals,    setVals]    = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)
  const [result,  setResult]  = useState<MechanicResult | null>(null)
  const [error,   setError]   = useState('')
  const [showVisual, setShowVisual] = useState(false)

  const fields = [
    { key: 'brake_pad_mm',                      label: 'Brake Pad Thickness',         unit: 'mm',  min: 1,  max: 15,  step: 0.1,  placeholder: '3–15' },
    { key: 'tyre_tread_mm',                     label: 'Tyre Tread Depth',            unit: 'mm',  min: 1,  max: 12,  step: 0.1,  placeholder: '1–12' },
    { key: 'engine_oil_temp_c',                 label: 'Engine Oil Temperature',      unit: '°C',  min: 60, max: 160, step: 1,    placeholder: '80–110 normal' },
    { key: 'engine_oil_pressure_bar',           label: 'Engine Oil Pressure',         unit: 'bar', min: 0.5,max: 6,   step: 0.1,  placeholder: '3–6 normal' },
    { key: 'suspension_travel_mm',              label: 'Suspension Travel',           unit: 'mm',  min: 10, max: 120, step: 1,    placeholder: '50–100 normal' },
    { key: 'wheel_bearing_noise',               label: 'Wheel Bearing Noise',         unit: '0–10',min: 0,  max: 10,  step: 1,    placeholder: '0=silent 10=loud' },
    { key: 'chassis_cracks',                    label: 'Chassis Cracks Visible',      unit: '0/1', min: 0,  max: 1,   step: 1,    placeholder: '0=no 1=yes' },
    { key: 'compactor_hydraulic_pressure_bar',  label: 'Compactor Hydraulic Pressure',unit: 'bar', min: 50, max: 300, step: 1,    placeholder: '180–280 normal' },
    { key: 'body_damage_score',                 label: 'Body Damage Score',           unit: '0–10',min: 0,  max: 10,  step: 1,    placeholder: '0=none 10=severe' },
    { key: 'fuel_pressure_bar',                 label: 'Fuel Line Pressure',          unit: 'bar', min: 1,  max: 8,   step: 0.1,  placeholder: '3–7 normal' },
  ]

  // Presets — example readings for each component
  const PRESETS: Record<string, Record<string, string>> = {
    'wheels': {
      brake_pad_mm: '8', tyre_tread_mm: '2', engine_oil_temp_c: '92',
      engine_oil_pressure_bar: '4', suspension_travel_mm: '75',
      wheel_bearing_noise: '9', chassis_cracks: '0',
      compactor_hydraulic_pressure_bar: '220', body_damage_score: '1', fuel_pressure_bar: '4',
    },
    'suspension': {
      brake_pad_mm: '9', tyre_tread_mm: '7', engine_oil_temp_c: '90',
      engine_oil_pressure_bar: '4', suspension_travel_mm: '15',
      wheel_bearing_noise: '6', chassis_cracks: '0',
      compactor_hydraulic_pressure_bar: '210', body_damage_score: '2', fuel_pressure_bar: '4.5',
    },
    'engine': {
      brake_pad_mm: '10', tyre_tread_mm: '8', engine_oil_temp_c: '155',
      engine_oil_pressure_bar: '1.2', suspension_travel_mm: '70',
      wheel_bearing_noise: '1', chassis_cracks: '0',
      compactor_hydraulic_pressure_bar: '230', body_damage_score: '1', fuel_pressure_bar: '1.8',
    },
    'cab': {
      brake_pad_mm: '9', tyre_tread_mm: '7', engine_oil_temp_c: '91',
      engine_oil_pressure_bar: '4', suspension_travel_mm: '72',
      wheel_bearing_noise: '1', chassis_cracks: '1',
      compactor_hydraulic_pressure_bar: '215', body_damage_score: '8', fuel_pressure_bar: '4.5',
    },
    'chassis': {
      brake_pad_mm: '9', tyre_tread_mm: '7', engine_oil_temp_c: '90',
      engine_oil_pressure_bar: '4', suspension_travel_mm: '20',
      wheel_bearing_noise: '2', chassis_cracks: '1',
      compactor_hydraulic_pressure_bar: '220', body_damage_score: '3', fuel_pressure_bar: '4.5',
    },
    'rear_compactor': {
      brake_pad_mm: '9', tyre_tread_mm: '7', engine_oil_temp_c: '92',
      engine_oil_pressure_bar: '4', suspension_travel_mm: '70',
      wheel_bearing_noise: '1', chassis_cracks: '0',
      compactor_hydraulic_pressure_bar: '75', body_damage_score: '7', fuel_pressure_bar: '4.5',
    },
    'refuse_body': {
      brake_pad_mm: '9', tyre_tread_mm: '7', engine_oil_temp_c: '91',
      engine_oil_pressure_bar: '4', suspension_travel_mm: '70',
      wheel_bearing_noise: '1', chassis_cracks: '1',
      compactor_hydraulic_pressure_bar: '210', body_damage_score: '9', fuel_pressure_bar: '4.5',
    },
    'brake_caliper': {
      brake_pad_mm: '2', tyre_tread_mm: '7', engine_oil_temp_c: '92',
      engine_oil_pressure_bar: '4', suspension_travel_mm: '70',
      wheel_bearing_noise: '8', chassis_cracks: '0',
      compactor_hydraulic_pressure_bar: '220', body_damage_score: '1', fuel_pressure_bar: '4.5',
    },
    'tyres': {
      brake_pad_mm: '5', tyre_tread_mm: '1.5', engine_oil_temp_c: '91',
      engine_oil_pressure_bar: '4', suspension_travel_mm: '70',
      wheel_bearing_noise: '2', chassis_cracks: '0',
      compactor_hydraulic_pressure_bar: '220', body_damage_score: '1', fuel_pressure_bar: '4.5',
    },
  }

  async function runMechanicAI() {
    setLoading(true); setResult(null); setError('')
    try {
      const payload: Record<string, number> = {}
      for (const f of fields) {
        const v = parseFloat(vals[f.key])
        if (!isNaN(v)) payload[f.key] = v
      }
      const res  = await fetch('http://localhost:8000/api/v1/diagnosis/mechanic-demo/', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error ?? 'Request failed')
      setResult(data)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Something went wrong.')
    } finally { setLoading(false) }
  }

  const filled = fields.filter(f => vals[f.key] !== undefined && vals[f.key] !== '').length
  const accent = result ? (COMPONENT_COLOUR[result.predicted_component] ?? '#B8E36A') : '#B8E36A'
  const model3d = result?.model_3d ?? null

  return (
    <div style={{ width: '100%', maxWidth: '680px', marginTop: '72px', paddingTop: '56px', borderTop: '1px solid #1e1e1e' }}>

      <p style={{ ...mono, textAlign: 'center' }}>Mechanic Component Diagnosis</p>
      <h2 style={{ ...heading, textAlign: 'center', marginBottom: '8px' }}>Which part needs replacing?</h2>
      <p style={{ color: '#858A7E', fontSize: '0.85rem', textAlign: 'center', marginBottom: '40px', lineHeight: 1.6, maxWidth: '500px', margin: '0 auto 40px' }}>
        Enter the inspection readings. The AI predicts which component is likely faulty and shows its 3D model.
      </p>

      {/* Preset selector */}
      <div style={{ marginBottom: '20px' }}>
        <p style={{ color: '#555', fontSize: '0.7rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.08em', margin: '0 0 10px' }}>
          Quick presets — load example readings for each component:
        </p>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {Object.entries(COMPONENT_LABELS).map(([key, label]) => (
            key !== 'tyres' ? (
              <button
                key={key}
                onClick={() => { setVals(PRESETS[key] ?? {}); setResult(null) }}
                style={{
                  background: '#111', border: '1px solid #2a2a2a',
                  borderRadius: '6px', padding: '5px 12px',
                  color: '#858A7E', fontSize: '0.75rem', cursor: 'pointer',
                  fontFamily: 'DM Mono, monospace',
                  transition: 'all 150ms',
                }}
                onMouseEnter={e => { (e.target as HTMLElement).style.borderColor = '#B8E36A'; (e.target as HTMLElement).style.color = '#B8E36A' }}
                onMouseLeave={e => { (e.target as HTMLElement).style.borderColor = '#2a2a2a'; (e.target as HTMLElement).style.color = '#858A7E' }}
              >
                {label}
              </button>
            ) : null
          ))}
          <button
            onClick={() => { setVals(PRESETS['tyres'] ?? {}); setResult(null) }}
            style={{ background: '#111', border: '1px solid #2a2a2a', borderRadius: '6px', padding: '5px 12px', color: '#858A7E', fontSize: '0.75rem', cursor: 'pointer', fontFamily: 'DM Mono, monospace' }}
          >
            Tyres
          </button>
        </div>
      </div>

      {/* Input grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '28px' }}>
        {fields.map(f => (
          <div key={f.key} style={{ background: '#111', border: '1px solid #1e1e1e', borderRadius: '8px', padding: '14px 16px' }}>
            <p style={{ color: '#858A7E', fontSize: '0.7rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.07em', margin: '0 0 6px' }}>
              {f.label} <span style={{ color: '#333' }}>({f.unit})</span>
            </p>
            <input
              type="number" min={f.min} max={f.max} step={f.step}
              placeholder={f.placeholder}
              value={vals[f.key] ?? ''}
              onChange={e => setVals(prev => ({ ...prev, [f.key]: e.target.value }))}
              style={{
                width: '100%', background: 'transparent', border: 'none',
                borderBottom: `1px solid ${vals[f.key] ? '#B8E36A44' : '#2a2a2a'}`,
                color: '#F4F4F0', fontSize: '1.05rem', fontFamily: 'DM Mono, monospace',
                padding: '4px 0', outline: 'none', boxSizing: 'border-box',
              }}
            />
          </div>
        ))}
      </div>

      <p style={{ color: '#333', fontSize: '0.75rem', textAlign: 'center', marginBottom: '20px', fontFamily: 'DM Mono, monospace' }}>
        {filled}/{fields.length} fields filled — empty fields use default normal values
      </p>

      <button onClick={runMechanicAI} disabled={loading} style={{
        display: 'block', width: '100%', background: '#B8E36A', color: '#0A0A0A',
        border: 'none', borderRadius: '8px', padding: '14px', fontSize: '0.95rem',
        fontWeight: 700, cursor: loading ? 'not-allowed' : 'pointer',
        fontFamily: 'Manrope, sans-serif', marginBottom: '32px', opacity: loading ? 0.6 : 1,
      }}>
        {loading ? 'Analysing...' : 'Diagnose Component'}
      </button>

      {error && <div style={{ background: '#B9685911', border: '1px solid #B9685944', borderRadius: '8px', padding: '12px 20px', color: '#B96859', fontSize: '0.85rem', textAlign: 'center', marginBottom: '24px' }}>{error}</div>}

      {/* Result */}
      {result && (
        <div style={{ background: '#111', border: `1px solid ${accent}44`, borderTop: `4px solid ${accent}`, borderRadius: '12px', padding: '28px' }}>

          {/* Verdict */}
          <div style={{ textAlign: 'center', marginBottom: '24px' }}>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '10px', background: `${accent}18`, borderRadius: '999px', padding: '10px 24px', marginBottom: '10px' }}>
              <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: accent, boxShadow: `0 0 10px ${accent}` }} />
              <span style={{ color: accent, fontWeight: 800, fontSize: '1rem', letterSpacing: '0.06em', textTransform: 'uppercase' }}>
                {COMPONENT_LABELS[result.predicted_component] ?? result.predicted_component}
              </span>
            </div>
            <p style={{ color: '#858A7E', fontSize: '0.83rem', margin: 0, fontFamily: 'DM Mono, monospace' }}>
              Confidence: <strong style={{ color: '#F4F4F0' }}>{(result.confidence * 100).toFixed(1)}%</strong>
            </p>
          </div>

          {/* Top 3 */}
          <div style={{ marginBottom: '24px' }}>
            <p style={{ color: '#333', fontSize: '0.7rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.08em', margin: '0 0 10px' }}>Top predictions</p>
            {result.top_3.map((t, i) => (
              <div key={t.component} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid #1a1a1a' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ color: '#333', fontFamily: 'DM Mono, monospace', fontSize: '0.72rem' }}>#{i + 1}</span>
                  <span style={{ color: i === 0 ? '#F4F4F0' : '#858A7E', fontSize: '0.85rem', fontWeight: i === 0 ? 600 : 400 }}>
                    {COMPONENT_LABELS[t.component] ?? t.component}
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <div style={{ width: `${Math.round(t.probability * 80)}px`, height: '4px', background: i === 0 ? accent : '#2a2a2a', borderRadius: '2px', minWidth: '4px' }} />
                  <span style={{ color: '#555', fontSize: '0.72rem', fontFamily: 'DM Mono, monospace', width: '36px', textAlign: 'right' }}>
                    {(t.probability * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>

          {/* 3D Model */}
          {model3d ? (
            <div>
              <p style={{ color: '#333', fontSize: '0.7rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.08em', margin: '0 0 10px' }}>
                3D Model — {COMPONENT_LABELS[result.predicted_component]}
              </p>
              <div style={{ width: '100%', height: '320px', background: '#0d0d0d', border: `1px solid ${accent}33`, borderRadius: '10px', overflow: 'hidden', boxShadow: `0 0 40px ${accent}11` }}>
                <Canvas camera={{ position: [4, 2, 7], fov: 50 }} style={{ background: 'transparent' }}>
                  <ambientLight intensity={0.8} />
                  <directionalLight position={[5, 8, 5]} intensity={1.3} />
                  <directionalLight position={[-4, 2, -3]} intensity={0.4} />
                  <Suspense fallback={null}>
                    {model3d.type === 'glb'
                      ? <GLBModel path={`/models/${model3d.file}`} scale={1} />
                      : <OBJModel path={`/models/${model3d.file}`} scale={0.8} />
                    }
                    {model3d.type === 'glb' && <AutoCamera path={`/models/${model3d.file}`} />}
                    <Environment preset="warehouse" />
                  </Suspense>
                  <OrbitControls enableZoom autoRotate autoRotateSpeed={0.8} target={[0, 0, 0]} />
                </Canvas>
              </div>
              <p style={{ color: '#333', fontSize: '0.7rem', textAlign: 'center', marginTop: '8px', fontFamily: 'DM Mono, monospace' }}>Drag · Scroll · Auto-rotating</p>
            </div>
          ) : (
            <div style={{ background: '#1a1a1a', borderRadius: '8px', padding: '16px', textAlign: 'center' }}>
              <p style={{ color: '#555', fontSize: '0.83rem', margin: 0 }}>No 3D model available for <strong style={{ color: '#858A7E' }}>{COMPONENT_LABELS[result.predicted_component]}</strong></p>
            </div>
          )}

          {/* Scope */}
          <div style={{ marginTop: '20px', background: '#1a1a1a', borderRadius: '6px', padding: '10px 14px' }}>
            <p style={{ color: '#333', fontSize: '0.72rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.08em', margin: '0 0 4px' }}>Scope</p>
            <p style={{ color: '#333', fontSize: '0.76rem', lineHeight: 1.6, margin: 0 }}>{result.scope_warning}</p>
          </div>

          {/* Visual Diagnosis button */}
          <button
            onClick={() => setShowVisual(true)}
            style={{
              display: 'block', width: '100%', marginTop: '16px',
              background: 'transparent',
              border: '1px solid #FF3B3B88',
              borderRadius: '8px', padding: '13px',
              color: '#FF3B3B', fontSize: '0.9rem', fontWeight: 700,
              cursor: 'pointer', fontFamily: 'Manrope, sans-serif',
              transition: 'all 200ms',
            }}
            onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = '#FF3B3B11' }}
            onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = 'transparent' }}
          >
            View Visual Diagnosis →
          </button>
        </div>
      )}

      {/* Visual overlay */}
      {showVisual && result && (
        <VisualDiagnosisOverlay result={result} onClose={() => setShowVisual(false)} />
      )}
    </div>
  )
}

/* ── Developer ───────────────────────────────────────────── */
function DeveloperPage() {
  return (
    <div style={{ paddingTop: '56px', maxWidth: '720px', margin: '0 auto', padding: '120px 32px 80px' }}>
      <p style={mono}>Developer</p>
      <h2 style={heading}>Built by</h2>
      <div style={{ background: '#111', border: '1px solid #1e1e1e', borderRadius: '12px', padding: '32px', marginBottom: '28px' }}>
        <h3 style={{ color: '#F4F4F0', fontSize: '1.4rem', fontWeight: 800, margin: '0 0 4px' }}>Harshu</h3>
        <p style={{ color: '#B8E36A', fontSize: '0.75rem', fontFamily: 'DM Mono, monospace', margin: '0 0 20px', letterSpacing: '0.08em' }}>Lead Developer · VEDA V2</p>
        <p style={{ color: '#B0B0A8', fontSize: '0.95rem', lineHeight: 1.75, margin: 0 }}>Designed and built VEDA V2 — a full-stack AI-assisted heavy vehicle diagnostics platform, covering backend API design, AI model integration, 3D visualisation, and role-based dashboards.</p>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
        {[
          ['Backend',   'Python · Django · DRF'],
          ['Frontend',  'React · TypeScript · Vite'],
          ['Database',  'PostgreSQL 18.6'],
          ['AI Engine', 'XGBoost · scikit-learn'],
          ['3D Viewer', 'Three.js · React Three Fiber'],
          ['Tests',     '67 tests — all passing'],
          ['GitHub',    'EzhavaAdi / VEDA-Version-2.0'],
          ['Version',   'v2.0.9 — MVP Release'],
        ].map(([k, v]) => (
          <div key={k} style={{ background: '#111', border: '1px solid #1e1e1e', borderRadius: '8px', padding: '12px 16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ color: '#555', fontSize: '0.72rem', fontFamily: 'DM Mono, monospace' }}>{k}</span>
            <span style={{ color: '#D0D0C8', fontSize: '0.82rem', fontWeight: 600 }}>{v}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

/* ── Shared styles ───────────────────────────────────────── */
const mono:      React.CSSProperties = { color: '#B8E36A', fontSize: '0.72rem', letterSpacing: '0.12em', textTransform: 'uppercase', fontFamily: 'DM Mono, monospace', marginBottom: '16px' }
const heading:   React.CSSProperties = { fontSize: 'clamp(1.8rem,4vw,3rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 28px', lineHeight: 1.1 }
useGLTF.preload('/models/refuse-collection-truck.glb')
