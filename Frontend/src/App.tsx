import { Routes, Route } from 'react-router-dom'
import { lazy, Suspense } from 'react'

const DiagnosisViewerDemo = lazy(() =>
  import('./pages/diagnosis/DiagnosisViewerDemo').then(m => ({ default: m.DiagnosisViewerDemo }))
)

/**
 * VEDA V2 — Root Application Router
 * Phase 0: Placeholder landing + Phase 5: 3D viewer demo route
 */
function App() {
  return (
    <Routes>
      <Route path="/" element={<VedaPlaceholder />} />
      <Route
        path="/viewer"
        element={
          <Suspense fallback={<PageLoader />}>
            <DiagnosisViewerDemo />
          </Suspense>
        }
      />
    </Routes>
  )
}

function PageLoader() {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: '#10110F', color: '#858A7E',
      fontFamily: 'DM Mono, monospace', fontSize: '0.75rem',
    }}>
      Loading...
    </div>
  )
}

function VedaPlaceholder() {
  return (
    <main style={{
      minHeight: '100vh',
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      background: '#10110F', color: '#F4F4F0',
      fontFamily: 'Manrope, sans-serif', gap: '1.5rem', padding: '2rem',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#B8E36A' }} />
        <span style={{ color: '#B8E36A', fontSize: '0.75rem', letterSpacing: '0.15em', textTransform: 'uppercase' }}>
          Phase 5 — Digital Twin Active
        </span>
      </div>
      <h1 style={{ fontSize: 'clamp(2rem,6vw,4rem)', fontWeight: 800, letterSpacing: '-0.02em', textAlign: 'center', margin: 0 }}>
        VEDA
      </h1>
      <p style={{ color: '#858A7E', fontSize: '0.875rem', textAlign: 'center', maxWidth: '400px', lineHeight: 1.6, margin: 0 }}>
        Vehicle Evaluation Diagnostic Agents
      </p>
      <a
        href="/viewer"
        style={{
          background: '#B8E36A', color: '#10110F',
          padding: '0.6rem 1.5rem', borderRadius: '6px',
          fontWeight: 700, fontSize: '0.875rem', textDecoration: 'none',
          display: 'inline-flex', alignItems: 'center', gap: '0.5rem',
        }}
      >
        Open 3D Viewer
      </a>
      <div style={{
        background: '#1A1D18', border: '1px solid #2a2d26', borderRadius: '8px',
        padding: '1rem 1.5rem', fontFamily: 'DM Mono, monospace',
        fontSize: '0.75rem', color: '#858A7E', textAlign: 'left', minWidth: '280px',
      }}>
        <div>React 18 ✓ | TypeScript ✓ | Vite ✓</div>
        <div>Three.js {'{'}0.170{'}'} ✓ | R3F ✓ | Drei ✓</div>
        <div>Django 5.1.4 ✓ | PostgreSQL 18.6 ✓</div>
        <div>XGBoost APS Model ✓ (F1=0.853)</div>
        <div style={{ marginTop: '0.5rem', color: '#B8E36A' }}>Stack: Fully Operational</div>
      </div>
    </main>
  )
}

export default App
