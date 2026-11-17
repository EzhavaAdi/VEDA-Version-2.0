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
    <div style={{ background: '#F2EDE4', minHeight: '100vh', fontFamily: 'Manrope, sans-serif', color: '#0F1319' }}>
      <Navbar setPage={setPage} activePage={page} />
      {page === 'home'      && <HomePage />}
      {page === 'shop'      && <ShopPage />}
      {page === 'platform'  && <PlatformPage />}
      {page === 'developer' && <DeveloperPage />}
    </div>
  )
}

/* ❬❬ Navbar ❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬ */
function Navbar({ setPage, activePage }: { setPage: (p: string) => void; activePage: string }) {
  return (
    <nav style={{
      position: 'fixed', top: 0, left: 0, right: 0, zIndex: 999,
      height: '64px',
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '0 40px',
      background: activePage === 'home' ? 'rgba(242,237,228,0.92)' : 'rgba(15,19,25,0.95)',
      backdropFilter: 'blur(14px)',
      borderBottom: `1px solid ${activePage === 'home' ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.06)'}`,
      transition: 'background 400ms, border-color 400ms',
    }}>
      <button onClick={() => setPage('home')} style={{ ...logoBtn, color: activePage === 'home' ? '#0F1319' : '#FAF8F4' }}>
        <span>VE</span><span style={{ color: '#B8E36A' }}>DA</span>
      </button>
      <div style={{ display: 'flex', gap: '28px', alignItems: 'center' }}>
        {[
          { id: 'home',      label: 'Home'      },
          { id: 'shop',      label: 'Shop'      },
          { id: 'platform',  label: 'Platform'  },
          { id: 'developer', label: 'Developer' },
        ].map(item => (
          <button
            key={item.id}
            onClick={() => setPage(item.id)}
            className={`nav-link${activePage === item.id ? ' active' : ''}`}
            style={{
              color: activePage === 'home'
                ? (activePage === item.id ? '#0F1319' : '#6A6058')
                : (activePage === item.id ? '#FAF8F4' : '#8A9099'),
            }}
          >
            {item.label}
            <style>{`
              .nav-link::after {
                background: ${activePage === 'home' ? '#0F1319' : '#B8E36A'};
              }
            `}</style>
          </button>
        ))}
      </div>
    </nav>
  )
}

const logoBtn: React.CSSProperties = {
  background: 'none', border: 'none', cursor: 'pointer',
  color: '#F4F4F0', fontSize: '1.4rem', fontWeight: 800,
  letterSpacing: '0.18em', fontFamily: 'Manrope, sans-serif', padding: 0,
}
/* ── Kenwood truck 3D model ──────────────────────────────── *//* ❬❬ Kenwood truck 3D model ❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬ */
function RefuseTruckModel() {
  const { scene } = useGLTF('/models/refuse-collection-truck.glb')
  const box    = new THREE.Box3().setFromObject(scene)
  const center = new THREE.Vector3()
  box.getCenter(center)
  return (
    <group>
      <primitive object={scene} position={[-center.x, -center.y, -center.z]} />
    </group>
  )
}

/* ❬❬ Home page ⬝ full scroll cinematic ❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬ */

/* ❬❬ Scattered image style helper ❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬ */
function si(w: number, h: number): React.CSSProperties {
  return { width: `${w}px`, height: `${h}px`, objectFit: 'cover', display: 'block', boxShadow: '0 6px 24px rgba(15,19,25,0.14)' }
}

/* ❬❬ Home page ⬝ cinematic scroll ❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬ */
function HomePage() {
  const containerRef = useRef<HTMLDivElement>(null)
  const [scrollY, setScrollY]     = useState(0)
  const [maxScroll, setMaxScroll] = useState(1)

  useEffect(() => {
    const el = containerRef.current
    if (!el) return
    const fn = () => { setScrollY(el.scrollTop); setMaxScroll(el.scrollHeight - el.clientHeight || 1) }
    el.addEventListener('scroll', fn)
    return () => el.removeEventListener('scroll', fn)
  }, [])

  // p = 0 ⠙ 1 over total scroll
  const p = Math.min(Math.max(scrollY / Math.max(maxScroll, 1), 0), 1)

  // Phase 1 ⬝ 0⠙0.20 ⬝ scattered images fly up and vanish
  const ph1          = Math.min(p / 0.20, 1)
  const imgOpacity   = Math.max(0, 1 - ph1 * 2.5)
  const imgTranslate = ph1 * -140

  // Phase 2 ⬝ 0.20⠙0.65 ⬝ VE/DA split open, truck grows in between
  const ph2  = Math.min(Math.max((p - 0.15) / 0.60, 0), 1)
  const shift = ph2 * 320          // VE moves left, DA moves right

  // Truck: starts growing at ph2=0.1, full at ph2=0.8
  const truckPh = Math.min(Math.max((ph2 - 0.18) / 0.82, 0), 1)
  // canvas is sized relative to viewport so it always fills the gap

  // Phase 3 ⬝ 0.65⠙0.82 ⬝ whole hero flies up and out
  const ph3           = Math.min(Math.max((p - 0.78) / 0.12, 0), 1)
  const heroTranslate = ph3 * -180
  const heroOpacity   = Math.max(0, 1 - ph3 * 1.8)

  // Phase 4 ⬝ 0.82⠙1.0 ⬝ "understand the machine" fades in
  const ph4          = Math.min(Math.max((p - 0.86) / 0.14, 0), 1)
  const ctaOpacity   = ph4
  const ctaTranslate = (1 - ph4) * 50

  return (
    <div ref={containerRef} style={{ height: '100vh', overflowY: 'scroll', scrollbarWidth: 'none', background: '#F2EDE4' }}>
      {/* tall canvas ⬝ 500vh gives lots of scroll travel */}
      <div style={{ height: '700vh' }}>
        <div style={{ position: 'sticky', top: 0, height: '100vh', overflow: 'hidden', background: '#F2EDE4' }}>

          {/* ❬❬ LAYER 1: scattered photos ❬❬ */}
          <div style={{ position: 'absolute', inset: 0, opacity: imgOpacity, transform: `translateY(${imgTranslate}px)`, transition: 'opacity 0.05s linear, transform 0.05s linear', pointerEvents: 'none', zIndex: 1 }}>
            <div style={{ position: 'absolute', top: '78px',   left: '20px'              }}><img src="/home/truck-india.jpg" alt="" style={si(210,275)} /></div>
            <div style={{ position: 'absolute', top: '195px',  left: '108px'             }}><img src="/home/truck-07.webp"   alt="" style={si(170,210)} /></div>
            <div style={{ position: 'absolute', bottom: '65px',left: '45px'              }}><img src="/home/truck-06.webp"   alt="" style={si(180,220)} /></div>
            <div style={{ position: 'absolute', top: '70px',   left: '50%', transform:'translateX(-55px)' }}><img src="/home/truck-03.jpg" alt="" style={si(200,245)} /></div>
            <div style={{ position: 'absolute', top: '82px',   right:'28px'              }}><img src="/home/truck-04.jpg"   alt="" style={si(195,250)} /></div>
            <div style={{ position: 'absolute', top: '228px',  right:'136px'             }}><img src="/home/truck-05.jpg"   alt="" style={si(160,200)} /></div>
            <div style={{ position: 'absolute', bottom:'70px', right:'52px'              }}><img src="/home/truck-02.jpg"   alt="" style={si(190,235)} /></div>
          </div>

          {/* ❬❬ LAYER 2: VE/DA + truck ❬❬ */}
          <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', opacity: heroOpacity, transform: `translateY(${heroTranslate}px)`, transition: 'transform 0.05s linear, opacity 0.05s linear', zIndex: 5 }}>

            <div style={{ position: 'relative', width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', height: 'clamp(130px, 24vw, 260px)' }}>

              {/* VE slides left */}
              <span style={{
                position: 'absolute',
                fontSize: 'clamp(7rem, 22vw, 18rem)', fontWeight: 900, letterSpacing: '-0.04em', lineHeight: 1,
                color: '#0F1319', userSelect: 'none', whiteSpace: 'nowrap',
                transform: `translateX(calc(-50% - ${shift}px))`,
                transition: 'transform 0.05s ease-out',
              }}>VE</span>

              {/* Kenwood truck ⬝ grows in the gap */}
              <div style={{
                  position: 'absolute', zIndex: 4,
                  width: '22vw', height: '13vw',
                  top: '50%', left: '50%',
                  transformOrigin: 'center center',
                  transform: `translate(-50%, -50%) scale(${truckPh * 2})`,
                  opacity: Math.min(truckPh * 2.5, 1),
                  transition: 'transform 0.06s ease-out, opacity 0.06s linear',
                }}>
                  <Canvas camera={{ position: [3, 1.0, 7], fov: 50 }} style={{ background: 'transparent', width: '100%', height: '100%' }}>
                    <ambientLight intensity={0.75} />
                    <directionalLight position={[8, 10, 6]}  intensity={1.6} color="#fff8e8" />
                    <directionalLight position={[-5, 3, -4]} intensity={0.4} />
                    <Suspense fallback={null}>
                      <RefuseTruckModel />
                      <Environment preset="dawn" />
                    </Suspense>
                    <OrbitControls enableZoom={false} enablePan={false} autoRotate autoRotateSpeed={0.5} />
                  </Canvas>
                </div>

              {/* DA slides right */}
              <span style={{
                position: 'absolute',
                fontSize: 'clamp(7rem, 22vw, 18rem)', fontWeight: 900, letterSpacing: '-0.04em', lineHeight: 1,
                color: '#B8E36A', userSelect: 'none', whiteSpace: 'nowrap',
                transform: `translateX(calc(50% + ${shift}px))`,
                transition: 'transform 0.05s ease-out',
              }}>DA</span>
            </div>

            {/* scroll hint ⬝ vanishes as scroll starts */}
            <div style={{ marginTop: '28px', opacity: Math.max(0, 1 - p * 8), display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '0.72rem', letterSpacing: '0.28em', textTransform: 'uppercase', color: '#8A8070', fontFamily: 'DM Mono, monospace' }}>SCROLL</span>
              <div style={{ width: '1px', height: '44px', background: 'linear-gradient(to bottom, #8A8070, transparent)' }} />
            </div>
          </div>

          {/* ❬❬ LAYER 3: "Understand the machine" ❬❬ */}
          <div style={{
            position: 'absolute', inset: 0, zIndex: 7,
            display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
            textAlign: 'center', padding: '0 32px',
            background: `rgba(15,19,25,${ph4 * 0.72})`,
            opacity: ctaOpacity, transform: `translateY(${ctaTranslate}px)`,
            transition: 'opacity 0.05s linear, transform 0.05s linear',
            pointerEvents: ctaOpacity > 0.5 ? 'auto' : 'none',
          }}>
            <span style={{ fontSize: '0.8rem', letterSpacing: '0.3em', textTransform: 'uppercase', color: '#D4C9A8', fontFamily: 'DM Mono, monospace', marginBottom: '24px' }}>DIAGNOSE · VISUALISE · MAINTAIN</span>
            <h2 style={{ fontSize: 'clamp(2.5rem, 7vw, 5.5rem)', fontWeight: 800, color: '#FAF8F4', lineHeight: 1.08, letterSpacing: '-0.02em', margin: 0, maxWidth: '860px' }}>
              UNDERSTAND THE MACHINE.<br />BEFORE IT STOPS.
            </h2>
          </div>

        </div>
      </div>

      {/* ⢐⢐⢐⢐ REST OF PAGE ⢐⢐⢐⢐ */}

      {/* Full-bleed hero image */}
      <section style={{ position: 'relative', height: '90vh', overflow: 'hidden' }}>
        <img src="/home/truck-01.jpg" alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block', filter: 'brightness(0.5)' }} />
        <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '0 32px' }}>
          <span style={{ fontSize: '0.8rem', letterSpacing: '0.3em', textTransform: 'uppercase', color: '#D4C9A8', fontFamily: 'DM Mono, monospace', marginBottom: '24px' }}>DIAGNOSE · VISUALISE · MAINTAIN</span>
          <h2 style={{ fontSize: 'clamp(2.5rem, 6vw, 5rem)', fontWeight: 800, color: '#FAF8F4', lineHeight: 1.08, letterSpacing: '-0.02em', margin: 0, maxWidth: '860px' }}>UNDERSTAND THE MACHINE.<br />BEFORE IT STOPS.</h2>
        </div>
      </section>

      {/* Editorial ⬝ cream */}
      <section style={{ background: '#FAF8F4', padding: '100px 80px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <h2 style={{ fontSize: 'clamp(1.8rem, 3.5vw, 3rem)', fontWeight: 800, letterSpacing: '-0.02em', lineHeight: 1.12, color: '#0F1319', textAlign: 'center', maxWidth: '800px', margin: '0 auto 56px' }}>
            A PLATFORM FOR THOSE WHO DEMAND TRANSPARENCY IN EVERY REPAIR
          </h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '48px' }}>
            <p style={{ fontSize: '1.05rem', lineHeight: 1.85, color: '#4A4438' }}>VEDA connects heavy vehicle owners with registered service centres and mechanics through an AI-assisted, evidence-driven diagnostic platform. Every finding is traceable. Every repair decision belongs to the owner.</p>
            <p style={{ fontSize: '1.05rem', lineHeight: 1.85, color: '#8A8070' }}>The Air Pressure System classifier ⬝ trained on 60,000 real Scania truck sensor records ⬝ achieves a ROC-AUC of 0.995. It never fabricates a result. When data is insufficient, it says so.</p>
          </div>
        </div>
      </section>

      {/* Three pillars ⬝ dark navy */}
      <section style={{ background: '#0F1319', padding: '100px 80px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <span style={{ fontSize: '0.78rem', letterSpacing: '0.3em', textTransform: 'uppercase', color: '#B8E36A', fontFamily: 'DM Mono, monospace', display: 'block', marginBottom: '56px', textAlign: 'center' }}>THE PLATFORM</span>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '2px' }}>
            {[
              { n: '01', t: 'DIAGNOSE', d: 'AI-powered APS failure detection trained on real Scania sensor data. F1-score 0.853. ROC-AUC 0.995. Mechanic observations recorded as independent evidence.', i: '/home/truck-05.jpg' },
              { n: '02', t: 'VISUALISE', d: 'Interactive 3D truck model with 289 individually named mesh components. Diagnostic colour states applied in real time ⬝ NORMAL, SUSPECTED, VERIFIED, REPAIRED.', i: '/home/truck-06.webp' },
              { n: '03', t: 'MAINTAIN', d: 'Transparent estimates. Owner-controlled approvals per line item. Work orders, invoices and payment records ⬝ all in one connected workflow.', i: '/home/truck-07.webp' },
            ].map(x => (
              <div key={x.n} style={{ background: '#161C24', overflow: 'hidden' }}>
                <div style={{ height: '230px', overflow: 'hidden' }}><img src={x.i} alt={x.t} style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block', filter: 'brightness(0.75)' }} /></div>
                <div style={{ padding: '32px 28px' }}>
                  <span style={{ fontSize: '0.72rem', letterSpacing: '0.2em', color: '#B8E36A', fontFamily: 'DM Mono, monospace', display: 'block', marginBottom: '10px' }}>{x.n}</span>
                  <h3 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#FAF8F4', margin: '0 0 14px', letterSpacing: '0.03em' }}>{x.t}</h3>
                  <p style={{ fontSize: '0.95rem', lineHeight: 1.75, color: '#8A9099', margin: 0 }}>{x.d}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Split ⬝ mechanic */}
      <section style={{ background: '#F2EDE4' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', minHeight: '65vh' }}>
          <div style={{ padding: '90px 72px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <span style={{ fontSize: '0.78rem', letterSpacing: '0.25em', textTransform: 'uppercase', color: '#8A8070', fontFamily: 'DM Mono, monospace', marginBottom: '20px', display: 'block' }}>THE MECHANIC</span>
            <h2 style={{ fontSize: 'clamp(1.8rem, 3vw, 2.6rem)', fontWeight: 800, color: '#0F1319', letterSpacing: '-0.02em', lineHeight: 1.12, margin: '0 0 20px' }}>WHERE INSPECTION BECOMES EVIDENCE</h2>
            <p style={{ fontSize: '1rem', lineHeight: 1.85, color: '#6A6058', marginBottom: '32px' }}>Enter brake pad thickness, oil pressure, bearing noise, suspension travel. The AI maps your readings to a component. The 3D model appears in the colour of its condition. Red is critical. Yellow is watch it. Green is clear.</p>
            <span style={{ fontSize: '0.78rem', letterSpacing: '0.2em', textTransform: 'uppercase', color: '#0F1319', fontFamily: 'DM Mono, monospace', borderBottom: '1px solid #0F1319', paddingBottom: '2px', width: 'fit-content', cursor: 'pointer' }}>EXPLORE PLATFORM ⠙</span>
          </div>
          <div style={{ overflow: 'hidden' }}><img src="/home/truck-india.jpg" alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }} /></div>
        </div>
      </section>

      {/* Stats */}
      <section style={{ background: '#FAF8F4', padding: '90px 80px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1px', background: '#E8E0D0' }}>
          {[
            { n: '0.995', l: 'ROC-AUC', s: 'APS failure classifier ⬝ verified on 16,000 real sensor records' },
            { n: '289',   l: 'Named Mesh Components', s: 'Individually selectable on the interactive 3D truck viewer' },
            { n: '67',    l: 'Tests Passing', s: 'Auth, isolation, state machine, AI integrity, financial accuracy' },
          ].map(s => (
            <div key={s.l} style={{ background: '#FAF8F4', padding: '52px 44px' }}>
              <p style={{ fontSize: 'clamp(2.5rem, 5vw, 4rem)', fontWeight: 800, color: '#0F1319', margin: '0 0 8px', letterSpacing: '-0.03em' }}>{s.n}</p>
              <p style={{ fontSize: '0.8rem', letterSpacing: '0.15em', textTransform: 'uppercase', color: '#B8E36A', fontFamily: 'DM Mono, monospace', margin: '0 0 10px' }}>{s.l}</p>
              <p style={{ fontSize: '0.92rem', lineHeight: 1.65, color: '#8A8070', margin: 0 }}>{s.s}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Split ⬝ shop */}
      <section style={{ background: '#F2EDE4' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', minHeight: '60vh' }}>
          <div style={{ overflow: 'hidden' }}><img src="/home/truck-04.jpg" alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }} /></div>
          <div style={{ padding: '90px 72px', display: 'flex', flexDirection: 'column', justifyContent: 'center', background: '#0F1319' }}>
            <span style={{ fontSize: '0.78rem', letterSpacing: '0.25em', textTransform: 'uppercase', color: '#B8E36A', fontFamily: 'DM Mono, monospace', marginBottom: '20px', display: 'block' }}>THE SHOP</span>
            <h2 style={{ fontSize: 'clamp(1.8rem, 3vw, 2.5rem)', fontWeight: 800, color: '#FAF8F4', letterSpacing: '-0.02em', lineHeight: 1.15, margin: '0 0 20px' }}>SPARE PARTS.<br />RIGHT PART. RIGHT PRICE.</h2>
            <p style={{ fontSize: '1rem', lineHeight: 1.85, color: '#8A9099', marginBottom: '32px' }}>27 OEM-compatible spare parts across 6 categories ⬝ APS, brakes, engine, suspension, tyres and electrical.</p>
            <span style={{ fontSize: '0.78rem', letterSpacing: '0.2em', textTransform: 'uppercase', color: '#B8E36A', fontFamily: 'DM Mono, monospace', borderBottom: '1px solid #B8E36A', paddingBottom: '2px', width: 'fit-content', cursor: 'pointer' }}>BROWSE SHOP ⠙</span>
          </div>
        </div>
      </section>

      {/* Closing CTA */}
      <section style={{ position: 'relative', height: '65vh', overflow: 'hidden' }}>
        <img src="/home/truck-02.jpg" alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block', filter: 'brightness(0.4)' }} />
        <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '0 32px' }}>
          <h2 style={{ fontSize: 'clamp(2rem, 5vw, 3.8rem)', fontWeight: 800, color: '#FAF8F4', letterSpacing: '-0.02em', margin: '0 0 28px', maxWidth: '780px', lineHeight: 1.1 }}>THE FUTURE OF VEHICLE MAINTENANCE STARTS HERE.</h2>
          <span style={{ fontSize: '0.82rem', letterSpacing: '0.25em', textTransform: 'uppercase', color: '#FAF8F4', fontFamily: 'DM Mono, monospace', border: '1px solid rgba(255,255,255,0.4)', padding: '13px 34px', cursor: 'pointer' }}>ENTER VEDA</span>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ background: '#0F1319', padding: '44px 72px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{ fontSize: '1.1rem', fontWeight: 800, letterSpacing: '0.15em', color: '#FAF8F4' }}><span>VE</span><span style={{ color: '#B8E36A' }}>DA</span></span>
        <span style={{ fontSize: '0.82rem', color: '#4A5260', fontFamily: 'DM Mono, monospace' }}>Vehicle Evaluation Diagnostic Agents · v2.0</span>
        <span style={{ fontSize: '0.82rem', color: '#4A5260', fontFamily: 'DM Mono, monospace' }}>Adhish Prasad · Harsh Barbhaya</span>
      </footer>

    </div>
  )
}


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

/* Auto-fitting camera for any GLB ⬝ positions itself based on bounding box */
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

  // Return inside a group that offsets by negative center ⬝ brings model to origin
  return (
    <group scale={scale}>
      <primitive object={obj} position={[-center.x, -center.y, -center.z]} />
    </group>
  )
}

/* ❬❬ Visual Diagnosis Overlay ❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬ */
/* ── Types + constants needed by mechanic section ─────────── */
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
        background: 'rgba(15,19,25,0.97)',
backdropFilter: 'blur(14px)',
borderBottom: '1px solid #2A2E38',
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
          background: 'none', border: '1px solid #3A3E48', color: '#9A9EA8',
          borderRadius: '6px', padding: '6px 16px', cursor: 'pointer',
          fontSize: '0.8rem', fontFamily: 'Manrope, sans-serif',
        }}>
          Close ⓢ
        </button>
      </div>

      <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '40px 24px 80px' }}>

        {/* Legend */}
        <div style={{ display: 'flex', gap: '24px', marginBottom: '36px', justifyContent: 'center', flexWrap: 'wrap' }}>
          {[
            { colour: '#FF3B3B', label: 'CRITICAL ⬝ Needs immediate replacement' },
            { colour: '#FFB347', label: 'WARNING ⬝ Monitor closely' },
            { colour: '#4ADE80', label: 'GOOD ⬝ No action needed' },
          ].map(l => (
            <div key={l.label} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: l.colour, boxShadow: `0 0 8px ${l.colour}88`, flexShrink: 0 }} />
              <span style={{ color: '#858A7E', fontSize: '0.78rem', fontFamily: 'DM Mono, monospace' }}>{l.label}</span>
            </div>
          ))}
        </div>

        {/* Main layout: 3D model left, component cards right */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', alignItems: 'start' }}>

          {/* 3D model ⬝ predicted component with health colour glow */}
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
                background: '#1A1E28',
border: '1px solid #FF3B3B55',
borderRadius: '12px', overflow: 'hidden',
boxShadow: '0 0 40px #FF3B3B1A',
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
            <div style={{ marginTop: '16px', background: '#FAF8F4', border: '1px solid #E0D8CC', borderRadius: '8px', padding: '16px 18px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ color: '#8A8070', fontSize: '0.82rem', fontFamily: 'DM Mono, monospace' }}>AI Confidence</span>
                <span style={{ color: '#FF3B3B', fontWeight: 700, fontFamily: 'DM Mono, monospace', fontSize: '0.82rem' }}>
                  {(result.confidence * 100).toFixed(1)}%
                </span>
              </div>
              <div style={{ background: '#E8E0D0', borderRadius: '4px', height: '6px', overflow: 'hidden' }}>
                <div style={{ width: `${result.confidence * 100}%`, height: '100%', background: '#FF3B3B', borderRadius: '4px', boxShadow: '0 0 8px #FF3B3B88', transition: 'width 0.5s ease' }} />
              </div>
            </div>
          </div>

          {/* Component health cards */}
          <div>
            <p style={{ color: '#6A7080', fontSize: '0.75rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.1em', margin: '0 0 14px' }}>
              All Component Health Status
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {sorted.map(([key, label]) => {
                const h = health[key] ?? { health_score: 85, condition: 'GOOD', colour: '#4ADE80' }
                const isPredicted = key === result.predicted_component
                return (
                  <div key={key} style={{
                    background: isPredicted ? `${h.colour}15` : '#1A1E28',
border: `1px solid ${isPredicted ? h.colour + '66' : '#2A2E38'}`,
                    borderRadius: '8px', padding: '12px 16px',
                    transition: 'all 200ms',
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: h.colour, boxShadow: `0 0 6px ${h.colour}88`, flexShrink: 0 }} />
                        <span style={{ color: isPredicted ? '#FAF8F4' : '#B0B4BC', fontSize: '0.9rem', fontWeight: isPredicted ? 700 : 400 }}>
                          {label}
                          {isPredicted && <span style={{ color: h.colour, fontSize: '0.7rem', fontFamily: 'DM Mono, monospace', marginLeft: '8px' }}>⠐ PREDICTED FAULT</span>}
                        </span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{ color: h.colour, fontSize: '0.72rem', fontFamily: 'DM Mono, monospace', fontWeight: 700 }}>{h.condition}</span>
                        <span style={{ color: '#555', fontSize: '0.72rem', fontFamily: 'DM Mono, monospace' }}>{h.health_score}</span>
                      </div>
                    </div>
                    {/* Health bar */}
                    <div style={{ background: '#0F1319', borderRadius: '3px', height: '5px', overflow: 'hidden' }}>
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

/* ❬❬ Tinted 3D models for visual diagnosis ❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬ */
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

/* ❬❬ Shop Page ❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬ */
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
    <div style={{ paddingTop: '64px', minHeight: '100vh', background: '#F2EDE4' }}>

      {/* Shop header */}
      <div style={{ background: '#FAF8F4', borderBottom: '1px solid #E0D8CC', padding: '32px 48px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '20px' }}>
        <div>
          <h1 style={{ color: '#0F1319', fontSize: '2.2rem', fontWeight: 800, margin: 0, letterSpacing: '-0.03em' }}>
            Spare Parts Store
          </h1>
          <p style={{ color: '#6A6058', fontSize: '0.95rem', fontFamily: 'DM Mono, monospace', margin: '6px 0 0' }}>
            {allProducts.length} verified parts · Fast delivery to your workshop
          </p>
        </div>
        {/* Cart */}
        {totalItems > 0 && (
          <div style={{ background: '#0F1319', border: '1px solid rgba(184,227,106,0.3)', borderRadius: '10px', padding: '12px 20px', display: 'flex', alignItems: 'center', gap: '16px', boxShadow: '0 4px 14px rgba(15,19,25,0.1)' }}>
            <span style={{ color: '#B8E36A', fontSize: '0.98rem', fontWeight: 700, fontFamily: 'DM Mono, monospace' }}>
              Cart: {totalItems} {totalItems > 1 ? 'items' : 'item'}
            </span>
            <span style={{ color: '#FAF8F4', fontWeight: 800, fontSize: '1.15rem', fontFamily: 'DM Mono, monospace' }}>
              Rs {totalPrice.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
            </span>
            <button style={{ background: '#B8E36A', color: '#0F1319', border: 'none', borderRadius: '6px', padding: '8px 18px', fontWeight: 800, fontSize: '0.92rem', cursor: 'pointer', fontFamily: 'Manrope, sans-serif' }}>
              Checkout
            </button>
          </div>
        )}
      </div>

      {/* Search + category filter */}
      <div style={{ padding: '20px 48px', display: 'flex', gap: '16px', alignItems: 'center', flexWrap: 'wrap', borderBottom: '1px solid #E0D8CC', background: '#FAF8F4' }}>
        <input
          type="text" placeholder="Search parts, brands, part numbers..."
          value={search} onChange={e => setSearch(e.target.value)}
          style={{ flex: 1, minWidth: '240px', background: '#F2EDE4', border: '1px solid #C8C0B0', borderRadius: '8px', padding: '14px 20px', color: '#0F1319', fontSize: '1.05rem', fontFamily: 'Manrope, sans-serif', outline: 'none' }}
        />
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
          {[{ slug: 'all', name: 'All' }, ...categories].map(cat => (
            <button key={'slug' in cat ? cat.slug : 'all'} onClick={() => setActivecat('slug' in cat ? cat.slug : 'all')}
              style={{
                background: activecat === ('slug' in cat ? cat.slug : 'all') ? '#0F1319' : '#FAF8F4',
                color: activecat === ('slug' in cat ? cat.slug : 'all') ? '#B8E36A' : '#5A5048',
                border: `1px solid ${ activecat === ('slug' in cat ? cat.slug : 'all') ? '#0F1319' : '#C8C0B0'}`,
                borderRadius: '8px', padding: '10px 20px', fontSize: '0.98rem', cursor: 'pointer',
                fontFamily: 'Manrope, sans-serif', fontWeight: activecat === ('slug' in cat ? cat.slug : 'all') ? 700 : 500,
                whiteSpace: 'nowrap', transition: 'all 150ms ease',
              }}>
              {cat.name}
            </button>
          ))}
        </div>
      </div>

      {/* Products */}
      <div style={{ padding: '36px 48px 80px' }}>
        {loading && <p style={{ color: '#8A8070', textAlign: 'center', fontFamily: 'DM Mono, monospace', fontSize: '1.1rem', padding: '40px 0' }}>Loading parts catalogue...</p>}

        {!loading && (search !== '' ? (
          // Search results
          <div>
            <p style={{ color: '#6A6058', fontSize: '0.95rem', fontFamily: 'DM Mono, monospace', marginBottom: '20px' }}>{filtered.length} results for "{search}"</p>
            <ProductGrid products={filtered} cart={cart} onAdd={addToCart} onRemove={removeFromCart} />
          </div>
        ) : (
          // Category rows
          displayCats.map(cat => (
            <div key={cat.id} style={{ marginBottom: '48px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px', paddingBottom: '10px', borderBottom: '1px solid #E0D8CC' }}>
                <h2 style={{ color: '#0F1319', fontSize: '1.5rem', fontWeight: 800, margin: 0, letterSpacing: '-0.02em' }}>
                  {cat.name}
                </h2>
                <span style={{ color: '#8A8070', fontSize: '0.9rem', fontFamily: 'DM Mono, monospace' }}>{cat.products.length} products</span>
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
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(230px, 1fr))', gap: '18px' }}>
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
    <div style={{ background: '#FAF8F4', border: `1px solid ${qty > 0 ? '#B8E36A' : '#E0D8CC'}`, borderRadius: '12px', padding: '18px 16px', display: 'flex', flexDirection: 'column', gap: '10px', transition: 'border-color 150ms, box-shadow 150ms', boxShadow: qty > 0 ? '0 4px 16px rgba(184,227,106,0.15)' : 'none' }}>
      {/* Image */}
      <div style={{ width: '100%', aspectRatio: '1', background: '#E8E0D0', borderRadius: '10px', overflow: 'hidden', marginBottom: '4px', position: 'relative' }}>
        {p.image_path ? (
          <img
            src={`/shop/${p.image_path}`}
            alt={p.name}
            style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
            onError={e => { (e.target as HTMLImageElement).style.display = 'none' }}
          />
        ) : (
          <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#E8E0D0' }}>
            <span style={{ color: '#8A8070', fontSize: '0.85rem', fontFamily: 'DM Mono, monospace', letterSpacing: '0.08em', textTransform: 'uppercase' }}>No image</span>
          </div>
        )}
        {p.discount_percent > 0 && (
          <div style={{ position: 'absolute', top: '8px', left: '8px', background: '#0F1319', color: '#B8E36A', borderRadius: '4px', padding: '4px 8px', fontSize: '0.78rem', fontWeight: 700, fontFamily: 'DM Mono, monospace', letterSpacing: '0.05em' }}>
            {p.discount_percent}% OFF
          </div>
        )}
        {!p.in_stock && (
          <div style={{ position: 'absolute', inset: 0, background: 'rgba(242,237,228,0.85)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ color: '#8A8070', fontSize: '0.85rem', fontFamily: 'DM Mono, monospace', letterSpacing: '0.1em', textTransform: 'uppercase', fontWeight: 700 }}>Out of Stock</span>
          </div>
        )}
      </div>
      {/* Details */}
      <div>
        <p style={{ color: '#8A8070', fontSize: '0.82rem', fontFamily: 'DM Mono, monospace', margin: '0 0 4px', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 600 }}>{p.brand}</p>
        <p style={{ color: '#0F1319', fontSize: '1.05rem', fontWeight: 700, margin: '0 0 4px', lineHeight: 1.4, fontFamily: 'Manrope, sans-serif' }}>{p.name}</p>
        <p style={{ color: '#9A9080', fontSize: '0.82rem', fontFamily: 'DM Mono, monospace', margin: 0 }}>{p.part_number}</p>
      </div>
      {/* Price + Add */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 'auto', paddingTop: '12px', borderTop: '1px solid #E8E0D0' }}>
        <div>
          <p style={{ color: '#0F1319', fontWeight: 800, fontSize: '1.2rem', margin: 0, fontFamily: 'DM Mono, monospace' }}>
            Rs {parseFloat(p.price).toLocaleString('en-IN')}
          </p>
          {p.original_price && (
            <p style={{ color: '#9A9080', fontSize: '0.85rem', textDecoration: 'line-through', margin: '2px 0 0', fontFamily: 'DM Mono, monospace' }}>
              Rs {parseFloat(p.original_price).toLocaleString('en-IN')}
            </p>
          )}
        </div>
        {p.in_stock ? (
          qty === 0 ? (
            <button onClick={onAdd} style={{
              background: '#0F1319', border: 'none',
              color: '#B8E36A', borderRadius: '6px',
              padding: '10px 22px', fontWeight: 700, fontSize: '0.92rem',
              cursor: 'pointer', fontFamily: 'DM Mono, monospace',
              letterSpacing: '0.08em', transition: 'background 150ms',
            }}>
              ADD
            </button>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', background: '#0F1319', borderRadius: '6px', padding: '6px 14px' }}>
              <button onClick={onRemove} style={{ background: 'none', border: 'none', color: '#B8E36A', fontWeight: 800, fontSize: '1.2rem', cursor: 'pointer', lineHeight: 1, padding: '0', fontFamily: 'DM Mono, monospace' }}>-</button>
              <span style={{ color: '#FAF8F4', fontWeight: 700, fontSize: '1.05rem', minWidth: '20px', textAlign: 'center', fontFamily: 'DM Mono, monospace' }}>{qty}</span>
              <button onClick={onAdd} style={{ background: 'none', border: 'none', color: '#B8E36A', fontWeight: 800, fontSize: '1.2rem', cursor: 'pointer', lineHeight: 1, padding: '0', fontFamily: 'DM Mono, monospace' }}>+</button>
            </div>
          )
        ) : (
          <button disabled style={{ background: '#E8E0D0', border: '1px solid #C8C0B0', color: '#8A8070', borderRadius: '6px', padding: '9px 16px', fontSize: '0.85rem', cursor: 'not-allowed', fontFamily: 'DM Mono, monospace', letterSpacing: '0.06em' }}>
            SOLD OUT
          </button>
        )}
      </div>
    </div>
  )
}


/* ❬❬ About (kept for Developer page reference) ❬❬❬❬❬❬❬❬❬❬❬❬❬ */
/* ❬❬ Platform ⬝ APS AI Demo ❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬ */

/* ❬❬ Platform Page ❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬ */
function PlatformPage() {
  const [file,    setFile]    = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result,  setResult]  = useState<ApsResult | null>(null)
  const [error,   setError]   = useState('')
  const inputRef = useRef<HTMLInputElement>(null)

  async function runAPS() {
    if (!file) return
    setLoading(true); setResult(null); setError('')
    try {
      const form = new FormData()
      form.append('file', file)
      const res  = await fetch('http://localhost:8000/api/v1/diagnosis/demo/', { method: 'POST', body: form })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error ?? 'Request failed')
      setResult(data)
    } catch (e: unknown) { setError(e instanceof Error ? e.message : 'Something went wrong.') }
    finally { setLoading(false) }
  }

  const isPos       = result?.predicted_class === 'pos'
  const isNeg       = result?.predicted_class === 'neg'
  const resultColor = isPos ? '#B96859' : isNeg ? '#5A8A5A' : '#8A7A50'

  return (
    <div style={{ background: '#F2EDE4', minHeight: '100vh', fontFamily: 'Manrope, sans-serif', color: '#0F1319' }}>

      {/* ❬❬ APS SECTION ❬❬ */}
      <div style={{ maxWidth: '760px', margin: '0 auto', padding: '100px 32px 80px' }}>

        {/* Label */}
        <p style={{ fontSize: '0.82rem', letterSpacing: '0.2em', textTransform: 'uppercase', color: '#8A8070', fontFamily: 'DM Mono, monospace', marginBottom: '12px' }}>
          APS Diagnostic AI
        </p>

        {/* Heading */}
        <h1 style={{ fontSize: 'clamp(2rem, 4vw, 3rem)', fontWeight: 800, letterSpacing: '-0.03em', lineHeight: 1.1, color: '#0F1319', margin: '0 0 16px' }}>
          Air Pressure System<br />Failure Detection
        </h1>

        {/* Description */}
        <p style={{ fontSize: '1.05rem', lineHeight: 1.8, color: '#6A6058', marginBottom: '48px', maxWidth: '580px' }}>
          Upload a CSV file containing Scania APS sensor data. The AI classifier ⬝ trained on 60,000 real truck records ⬝ predicts whether an APS failure is present. The model achieves an F1-score of 0.853 and ROC-AUC of 0.995.
        </p>

        {/* Upload box */}
        <div
          onClick={() => inputRef.current?.click()}
          style={{
            border: `2px dashed ${file ? '#B8E36A' : '#C8C0B0'}`,
            borderRadius: '8px', padding: '48px 32px',
            textAlign: 'center', cursor: 'pointer',
            background: file ? 'rgba(184,227,106,0.05)' : '#FAF8F4',
            transition: 'all 200ms', marginBottom: '16px',
          }}>
          <input ref={inputRef} type="file" accept=".csv" style={{ display: 'none' }}
            onChange={e => { const f = e.target.files?.[0]; if (f) { setFile(f); setResult(null); setError('') } }} />
          {file ? (
            <>
              <p style={{ fontSize: '1.1rem', fontWeight: 700, color: '#5A8A50', margin: '0 0 6px' }}>𸜞 {file.name}</p>
              <p style={{ color: '#8A8070', fontSize: '0.9rem', margin: 0 }}>Click to change file</p>
            </>
          ) : (
            <>
              <p style={{ fontSize: '1.1rem', fontWeight: 700, color: '#0F1319', margin: '0 0 6px' }}>⬠  Upload CSV file</p>
              <p style={{ color: '#8A8070', fontSize: '0.9rem', margin: 0 }}>One header row + one data row with 170 APS sensor features</p>
            </>
          )}
        </div>

        {/* Sample download */}
        <a href="/sample_aps_data.csv" download style={{ color: '#8A8070', fontSize: '0.85rem', fontFamily: 'DM Mono, monospace', letterSpacing: '0.08em', textDecoration: 'underline', display: 'block', marginBottom: '24px' }}>
          Download sample CSV ⠙
        </a>

        {/* Run button */}
        <button onClick={runAPS} disabled={!file || loading} style={{
          background: file && !loading ? '#0F1319' : '#C8C0B0',
          color: '#FAF8F4', border: 'none', borderRadius: '8px',
          padding: '16px 56px', fontSize: '1rem', fontWeight: 700,
          cursor: file && !loading ? 'pointer' : 'not-allowed',
          fontFamily: 'Manrope, sans-serif', letterSpacing: '0.03em',
          transition: 'all 200ms', marginBottom: '32px',
        }}>
          {loading ? 'Running Analysis...' : 'Run APS Diagnosis'}
        </button>

        {/* Error */}
        {error && (
          <div style={{ background: '#F8E8E0', border: '1px solid #D09080', borderRadius: '8px', padding: '16px 20px', color: '#8A3020', fontSize: '1rem', marginBottom: '24px' }}>
            {error}
          </div>
        )}

        {/* Result */}
        {result && (
          <div style={{ background: '#FAF8F4', border: `2px solid ${resultColor}`, borderRadius: '12px', padding: '36px', marginBottom: '0' }}>
            {/* Verdict */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '28px', paddingBottom: '28px', borderBottom: '1px solid #E8E0D0' }}>
              <div style={{ width: '14px', height: '14px', borderRadius: '50%', background: resultColor, flexShrink: 0 }} />
              <div>
                <p style={{ fontSize: '1.4rem', fontWeight: 800, color: resultColor, margin: '0 0 4px', letterSpacing: '-0.01em' }}>
                  {result.predicted_label ?? 'INSUFFICIENT DATA'}
                </p>
                {result.probability_positive != null && (
                  <p style={{ color: '#8A8070', fontSize: '0.95rem', margin: 0 }}>
                    Probability of APS failure: <strong style={{ color: '#0F1319' }}>{(result.probability_positive * 100).toFixed(1)}%</strong>
                  </p>
                )}
                {result.status === 'insufficient_data' && (
                  <p style={{ color: '#8A8070', fontSize: '0.95rem', margin: '6px 0 0' }}>
                    Not enough sensor features were provided to make a reliable prediction.
                  </p>
                )}
              </div>
            </div>

            {/* Detail rows */}
            {[
              ['Model',            result.model_name],
              ['Version',          result.model_version],
              ['Feature coverage', `${(result.feature_coverage * 100).toFixed(1)}% of 170 APS features`],
              ['Inference status', result.status],
            ].map(([k, v]) => (
              <div key={k} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0', borderBottom: '1px solid #E8E0D0' }}>
                <span style={{ color: '#8A8070', fontSize: '0.92rem', fontFamily: 'DM Mono, monospace' }}>{k}</span>
                <span style={{ color: '#0F1319', fontSize: '0.95rem', fontWeight: 600 }}>{v}</span>
              </div>
            ))}

            {/* Scope */}
            <div style={{ marginTop: '20px', background: '#F2EDE4', border: '1px solid #E0D8CC', borderRadius: '6px', padding: '14px 18px' }}>
              <p style={{ color: '#8A8070', fontSize: '0.75rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.1em', margin: '0 0 6px' }}>Scope</p>
              <p style={{ color: '#8A8070', fontSize: '0.9rem', lineHeight: 1.65, margin: 0 }}>{result.scope_warning}</p>
            </div>
          </div>
        )}
      </div>

      {/* Divider */}
      <div style={{ height: '1px', background: '#E0D8CC', maxWidth: '760px', margin: '0 auto' }} />

      {/* ❬❬ MECHANIC SECTION ❬❬ */}
      <MechanicDiagnosticSection />
    </div>
  )
}

function MechanicDiagnosticSection() {
  const [vals,    setVals]    = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(false)
  const [result,  setResult]  = useState<MechanicResult | null>(null)
  const [error,   setError]   = useState('')
  const [showVisual, setShowVisual] = useState(false)

  const fields = [
    { key: 'brake_pad_mm',                      label: 'Brake Pad Thickness',         unit: 'mm',  min: 1,  max: 15,  step: 0.1,  placeholder: '3⬜15' },
    { key: 'tyre_tread_mm',                     label: 'Tyre Tread Depth',            unit: 'mm',  min: 1,  max: 12,  step: 0.1,  placeholder: '1⬜12' },
    { key: 'engine_oil_temp_c',                 label: 'Engine Oil Temperature',      unit: 'Â°C',  min: 60, max: 160, step: 1,    placeholder: '80⬜110 normal' },
    { key: 'engine_oil_pressure_bar',           label: 'Engine Oil Pressure',         unit: 'bar', min: 0.5,max: 6,   step: 0.1,  placeholder: '3⬜6 normal' },
    { key: 'suspension_travel_mm',              label: 'Suspension Travel',           unit: 'mm',  min: 10, max: 120, step: 1,    placeholder: '50⬜100 normal' },
    { key: 'wheel_bearing_noise',               label: 'Wheel Bearing Noise',         unit: '0⬜10',min: 0,  max: 10,  step: 1,    placeholder: '0=silent 10=loud' },
    { key: 'chassis_cracks',                    label: 'Chassis Cracks Visible',      unit: '0/1', min: 0,  max: 1,   step: 1,    placeholder: '0=no 1=yes' },
    { key: 'compactor_hydraulic_pressure_bar',  label: 'Compactor Hydraulic Pressure',unit: 'bar', min: 50, max: 300, step: 1,    placeholder: '180⬜280 normal' },
    { key: 'body_damage_score',                 label: 'Body Damage Score',           unit: '0⬜10',min: 0,  max: 10,  step: 1,    placeholder: '0=none 10=severe' },
    { key: 'fuel_pressure_bar',                 label: 'Fuel Line Pressure',          unit: 'bar', min: 1,  max: 8,   step: 0.1,  placeholder: '3⬜7 normal' },
  ]

  // Presets ⬝ example readings for each component
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
    <div style={{ width: '100%', maxWidth: '760px', margin: '0 auto', paddingTop: '72px', padding: '72px 32px 80px' }}>

      <p style={{ ...mono, textAlign: 'center' }}>Mechanic Component Diagnosis</p>
      <h2 style={{ fontSize: 'clamp(1.8rem, 3vw, 2.6rem)', fontWeight: 800, letterSpacing: '-0.03em', lineHeight: 1.1, color: '#0F1319', textAlign: 'center', margin: '0 0 12px' }}>Which part needs replacing?</h2>
      <p style={{ color: '#6A6058', fontSize: '1rem', textAlign: 'center', marginBottom: '36px', lineHeight: 1.7, maxWidth: '520px', margin: '0 auto 36px' }}>
        Enter the inspection readings. The AI predicts which component is likely faulty and shows its 3D model.
      </p>

      {/* Preset selector */}
      <div style={{ marginBottom: '20px' }}>
        <p style={{ color: '#555', fontSize: '0.7rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.08em', margin: '0 0 10px' }}>
          Quick presets ⬝ load example readings for each component:
        </p>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
          {Object.entries(COMPONENT_LABELS).map(([key, label]) => (
            key !== 'tyres' ? (
              <button
                key={key}
                onClick={() => { setVals(PRESETS[key] ?? {}); setResult(null) }}
                style={{
                  background: '#FAF8F4', border: '1px solid #C8C0B0',
                  borderRadius: '6px', padding: '7px 14px',
                  color: '#5A5248', fontSize: '0.75rem', cursor: 'pointer',
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
          <div key={f.key} style={{ background: '#FAF8F4', border: '1px solid #E0D8CC', borderRadius: '8px', padding: '16px 18px' }}>
            <p style={{ color: '#6A6058', fontSize: '0.82rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.07em', margin: '0 0 6px' }}>
              {f.label} <span style={{ color: '#B0A890' }}>({f.unit})</span>
            </p>
            <input
              type="number" min={f.min} max={f.max} step={f.step}
              placeholder={f.placeholder}
              value={vals[f.key] ?? ''}
              onChange={e => setVals(prev => ({ ...prev, [f.key]: e.target.value }))}
              style={{
                width: '100%', background: 'transparent', border: 'none',
                borderBottom: `2px solid ${vals[f.key] ? '#B8E36A' : '#C8C0B0'}`,
                color: '#0F1319', fontSize: '1.15rem', fontFamily: 'DM Mono, monospace',
                padding: '6px 0', outline: 'none', boxSizing: 'border-box',
              }}
            />
          </div>
        ))}
      </div>

      <p style={{ color: '#8A8070', fontSize: '0.88rem', textAlign: 'center', marginBottom: '20px', fontFamily: 'DM Mono, monospace' }}>
        {filled}/{fields.length} fields filled ⬝ empty fields use default normal values
      </p>

      <button onClick={runMechanicAI} disabled={loading} style={{
        display: 'block', width: '100%', background: '#0F1319', color: '#FAF8F4',
        border: 'none', borderRadius: '8px', padding: '16px', fontSize: '0.95rem',
        fontWeight: 700, cursor: loading ? 'not-allowed' : 'pointer',
        fontFamily: 'Manrope, sans-serif', marginBottom: '32px', opacity: loading ? 0.6 : 1,
      }}>
        {loading ? 'Analysing...' : 'Diagnose Component'}
      </button>

      {error && <div style={{ background: '#B9685911', border: '1px solid #B9685944', borderRadius: '8px', padding: '12px 20px', color: '#B96859', fontSize: '0.85rem', textAlign: 'center', marginBottom: '24px' }}>{error}</div>}

      {/* Result */}
      {result && (
        <div style={{ background: '#FAF8F4', border: `1px solid ${accent}`, borderTop: `4px solid ${accent}`, borderRadius: '12px', padding: '28px' }}>

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
            <p style={{ color: '#6A7080', fontSize: '0.75rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.1em', margin: '0 0 12px' }}>Top predictions</p>
            {result.top_3.map((t, i) => (
              <div key={t.component} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid #E0D8CC', background: '#FAF8F4' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ color: '#333', fontFamily: 'DM Mono, monospace', fontSize: '0.72rem' }}>#{i + 1}</span>
                  <span style={{ color: i === 0 ? '#0F1319' : '#8A8070', fontSize: '0.85rem', fontWeight: i === 0 ? 600 : 400 }}>
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
              <p style={{ color: '#6A7080', fontSize: '0.75rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.1em', margin: '0 0 12px' }}>
                3D Model ⬝ {COMPONENT_LABELS[result.predicted_component]}
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
            <p style={{ color: '#8A8070', fontSize: '0.75rem', fontFamily: 'DM Mono, monospace', textTransform: 'uppercase', letterSpacing: '0.1em', margin: '0 0 6px' }}>Scope</p>
            <p style={{ color: '#6A6058', fontSize: '0.9rem', lineHeight: 1.7, margin: 0 }}>{result.scope_warning}</p>
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
            View Visual Diagnosis ⠙
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

/* ❬❬ Developer ❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬❬ */
interface TomatoSplat {
  id: number
  x: number
  y: number
}

function DeveloperPage() {
  const [adhishSplats, setAdhishSplats] = useState<TomatoSplat[]>([])
  const [harshSplats, setHarshSplats]   = useState<TomatoSplat[]>([])

  const totalTomatoes = adhishSplats.length + harshSplats.length

  function handleThrowBoth() {
    const timestamp = Date.now()
    const newAdhish: TomatoSplat = {
      id: timestamp + Math.floor(Math.random() * 10000),
      x: 25 + Math.random() * 50,
      y: 25 + Math.random() * 50,
    }
    const newHarsh: TomatoSplat = {
      id: timestamp + Math.floor(Math.random() * 10000) + 1,
      x: 25 + Math.random() * 50,
      y: 25 + Math.random() * 50,
    }
    setAdhishSplats(prev => [...prev, newAdhish])
    setHarshSplats(prev => [...prev, newHarsh])
  }

  function handlePhotoClick(e: React.MouseEvent<HTMLDivElement>, target: 'adhish' | 'harsh') {
    const rect = e.currentTarget.getBoundingClientRect()
    const x = Math.max(10, Math.min(90, ((e.clientX - rect.left) / rect.width) * 100))
    const y = Math.max(10, Math.min(90, ((e.clientY - rect.top) / rect.height) * 100))
    const newSplat: TomatoSplat = {
      id: Date.now() + Math.floor(Math.random() * 10000),
      x,
      y,
    }
    if (target === 'adhish') {
      setAdhishSplats(prev => [...prev, newSplat])
    } else {
      setHarshSplats(prev => [...prev, newSplat])
    }
  }

  function handleCeasefire() {
    setAdhishSplats([])
    setHarshSplats([])
  }

  return (
    <div style={{ paddingTop: '64px', maxWidth: '980px', margin: '0 auto', padding: '90px 32px 80px' }}>
      
      {/* Header + Action Buttons */}
      <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', marginBottom: '36px', flexWrap: 'wrap', gap: '20px' }}>
        <div>
          <span style={mono}>The Creators</span>
          <h2 style={{ ...heading, margin: 0 }}>Built by</h2>
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px', flexWrap: 'wrap' }}>
          {totalTomatoes > 0 && (
            <span style={{
              color: '#FF3B3B',
              fontFamily: 'DM Mono, monospace',
              fontSize: '0.98rem',
              fontWeight: 700,
              background: 'rgba(255,59,59,0.1)',
              padding: '10px 18px',
              borderRadius: '8px',
              border: '1px solid rgba(255,59,59,0.3)',
              letterSpacing: '0.03em',
            }}>
              {totalTomatoes} {totalTomatoes === 1 ? 'Tomato' : 'Tomatoes'} Splattered
            </span>
          )}

          <button
            onClick={handleThrowBoth}
            style={{
              background: '#0F1319',
              color: '#FAF8F4',
              border: 'none',
              borderRadius: '8px',
              padding: '14px 28px',
              fontSize: '1.05rem',
              fontWeight: 700,
              cursor: 'pointer',
              fontFamily: 'Manrope, sans-serif',
              display: 'inline-flex',
              alignItems: 'center',
              boxShadow: '0 4px 14px rgba(15,19,25,0.12)',
              transition: 'transform 100ms ease, background 200ms',
              letterSpacing: '0.01em',
            }}
            onMouseDown={e => { (e.currentTarget as HTMLElement).style.transform = 'scale(0.96)' }}
            onMouseUp={e => { (e.currentTarget as HTMLElement).style.transform = 'scale(1)' }}
          >
            Throw Tomato on Dev
          </button>

          {totalTomatoes > 0 && (
            <button
              onClick={handleCeasefire}
              style={{
                background: '#FAF8F4',
                color: '#0F1319',
                border: '1px solid #C8C0B0',
                borderRadius: '8px',
                padding: '14px 22px',
                fontSize: '1.05rem',
                fontWeight: 700,
                cursor: 'pointer',
                fontFamily: 'Manrope, sans-serif',
                display: 'inline-flex',
                alignItems: 'center',
                boxShadow: '0 2px 8px rgba(0,0,0,0.05)',
                transition: 'all 150ms ease',
                letterSpacing: '0.01em',
              }}
              onMouseEnter={e => { (e.currentTarget as HTMLElement).style.background = '#F2EDE4' }}
              onMouseLeave={e => { (e.currentTarget as HTMLElement).style.background = '#FAF8F4' }}
            >
              Ceasefire on Dev
            </button>
          )}
        </div>
      </div>

      {/* Adhish Prasad */}
      <div style={{
        background: '#FAF8F4',
        border: adhishSplats.length > 0 ? '1px solid rgba(255,59,59,0.4)' : '1px solid #E0D8CC',
        borderRadius: '16px',
        padding: '40px',
        marginBottom: '32px',
        display: 'flex',
        gap: '40px',
        alignItems: 'center',
        flexWrap: 'wrap',
        transition: 'border-color 300ms',
        boxShadow: adhishSplats.length > 0 ? '0 4px 24px rgba(255,59,59,0.08)' : 'none',
      }}>
        {/* Big Photo Container */}
        <div
          onClick={e => handlePhotoClick(e, 'adhish')}
          style={{
            position: 'relative',
            width: '270px',
            height: '335px',
            borderRadius: '12px',
            overflow: 'hidden',
            border: '1px solid #E0D8CC',
            flexShrink: 0,
            boxShadow: '0 8px 24px rgba(15,19,25,0.08)',
            cursor: 'crosshair',
            userSelect: 'none',
          }}
          title="Click to throw a tomato right here!"
        >
          <img
            src="/developer/adhish.jpg"
            alt="Adhish Prasad"
            style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
          />

          {/* Every single throw gets its own animated GIF landing precisely where clicked */}
          {adhishSplats.map((splat, idx) => (
            <div
              key={splat.id}
              style={{
                position: 'absolute',
                left: `${splat.x}%`,
                top: `${splat.y}%`,
                transform: 'translate(-50%, -50%)',
                width: '560px',
                height: '315px',
                pointerEvents: 'none',
                zIndex: 10 + idx,
              }}
            >
              <img
                src={`/developer/tomato.gif?throw=${splat.id}`}
                alt="Throwing Tomato Animation"
                style={{
                  width: '100%',
                  height: '100%',
                  maxWidth: 'none',
                  maxHeight: 'none',
                  objectFit: 'contain',
                  display: 'block',
                }}
              />
            </div>
          ))}
        </div>

        <div style={{ flex: '1 1 380px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px', margin: '0 0 8px' }}>
            <h3 style={{ color: '#0F1319', fontSize: '1.95rem', fontWeight: 800, margin: 0, letterSpacing: '-0.02em' }}>Adhish Prasad</h3>
            {adhishSplats.length > 0 && (
              <span style={{ fontSize: '0.95rem', color: '#FF3B3B', fontFamily: 'DM Mono, monospace', fontWeight: 700, background: 'rgba(255,59,59,0.1)', padding: '3px 10px', borderRadius: '6px', border: '1px solid rgba(255,59,59,0.25)' }}>
                ×{adhishSplats.length}
              </span>
            )}
          </div>
          <p style={{ color: '#5A6478', fontSize: '0.92rem', fontFamily: 'DM Mono, monospace', margin: '0 0 20px', letterSpacing: '0.06em' }}>Backend Developer · AI Engine · System Architecture · VEDA V2</p>
          <p style={{ color: '#5A5048', fontSize: '1.14rem', lineHeight: 1.88, margin: 0 }}>Designed and built the full backend architecture ⬝ Django REST API, PostgreSQL database, APS AI diagnostic engine (XGBoost, F1=0.853), mechanic component classifier, service order state machine, and all data models across 12 application modules.</p>
        </div>
      </div>

      {/* Harsh Barbhaya */}
      <div style={{
        background: '#FAF8F4',
        border: harshSplats.length > 0 ? '1px solid rgba(255,59,59,0.4)' : '1px solid #E0D8CC',
        borderRadius: '16px',
        padding: '40px',
        marginBottom: '32px',
        display: 'flex',
        gap: '40px',
        alignItems: 'center',
        flexWrap: 'wrap',
        transition: 'border-color 300ms',
        boxShadow: harshSplats.length > 0 ? '0 4px 24px rgba(255,59,59,0.08)' : 'none',
      }}>
        {/* Big Photo Container */}
        <div
          onClick={e => handlePhotoClick(e, 'harsh')}
          style={{
            position: 'relative',
            width: '270px',
            height: '335px',
            borderRadius: '12px',
            overflow: 'hidden',
            border: '1px solid #E0D8CC',
            flexShrink: 0,
            boxShadow: '0 8px 24px rgba(15,19,25,0.08)',
            cursor: 'crosshair',
            userSelect: 'none',
          }}
          title="Click to throw a tomato right here!"
        >
          <img
            src="/developer/harsh.png"
            alt="Harsh Barbhaya"
            style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
          />

          {/* Every single throw gets its own animated GIF landing precisely where clicked */}
          {harshSplats.map((splat, idx) => (
            <div
              key={splat.id}
              style={{
                position: 'absolute',
                left: `${splat.x}%`,
                top: `${splat.y}%`,
                transform: 'translate(-50%, -50%)',
                width: '560px',
                height: '315px',
                pointerEvents: 'none',
                zIndex: 10 + idx,
              }}
            >
              <img
                src={`/developer/tomato.gif?throw=${splat.id}`}
                alt="Throwing Tomato Animation"
                style={{
                  width: '100%',
                  height: '100%',
                  maxWidth: 'none',
                  maxHeight: 'none',
                  objectFit: 'contain',
                  display: 'block',
                }}
              />
            </div>
          ))}
        </div>

        <div style={{ flex: '1 1 380px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px', margin: '0 0 8px' }}>
            <h3 style={{ color: '#0F1319', fontSize: '1.95rem', fontWeight: 800, margin: 0, letterSpacing: '-0.02em' }}>Harsh Barbhaya</h3>
            {harshSplats.length > 0 && (
              <span style={{ fontSize: '0.95rem', color: '#FF3B3B', fontFamily: 'DM Mono, monospace', fontWeight: 700, background: 'rgba(255,59,59,0.1)', padding: '3px 10px', borderRadius: '6px', border: '1px solid rgba(255,59,59,0.25)' }}>
                ×{harshSplats.length}
              </span>
            )}
          </div>
          <p style={{ color: '#5A6478', fontSize: '0.92rem', fontFamily: 'DM Mono, monospace', margin: '0 0 20px', letterSpacing: '0.06em' }}>Frontend Developer · 3D Visualisation · UI/UX · VEDA V2</p>
          <p style={{ color: '#5A5048', fontSize: '1.14rem', lineHeight: 1.88, margin: 0 }}>Built the frontend platform ⬝ React Three Fiber 3D truck viewer with component highlighting, mechanic diagnostic interface, spare parts shop, visual diagnosis overlay, and the animated VEDA landing page.</p>
        </div>
      </div>

    </div>
  )
}

const mono:    React.CSSProperties = { color: '#8A8070', fontSize: '0.95rem', letterSpacing: '0.18em', textTransform: 'uppercase', fontFamily: 'DM Mono, monospace', marginBottom: '14px', display: 'block' }
const heading: React.CSSProperties = { fontSize: 'clamp(2.4rem, 4.5vw, 3.5rem)', fontWeight: 800, letterSpacing: '-0.03em', margin: '0 0 28px', lineHeight: 1.1, color: '#0F1319' }

