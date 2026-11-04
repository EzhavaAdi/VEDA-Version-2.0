import { Routes, Route } from 'react-router-dom'

/**
 * VEDA V2 — Root Application Router
 *
 * Routes are registered here as each phase delivers its pages.
 * Phase 0: Placeholder landing page confirming the frontend is running.
 * Phase 1+: Authentication, dashboards, and feature pages.
 */
function App() {
  return (
    <Routes>
      <Route path="/" element={<VedaPlaceholder />} />
    </Routes>
  )
}

/**
 * Temporary placeholder — replaced by the real landing page in Phase 1.
 * Confirms the React + Vite + TypeScript stack is working correctly.
 */
function VedaPlaceholder() {
  return (
    <main
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#10110F',
        color: '#F4F4F0',
        fontFamily: 'Manrope, sans-serif',
        gap: '1.5rem',
        padding: '2rem',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div
          style={{
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            background: '#B8E36A',
          }}
        />
        <span style={{ color: '#B8E36A', fontSize: '0.75rem', letterSpacing: '0.15em', textTransform: 'uppercase' }}>
          Phase 0 — Foundation Active
        </span>
      </div>

      <h1
        style={{
          fontSize: 'clamp(2rem, 6vw, 4rem)',
          fontWeight: 800,
          letterSpacing: '-0.02em',
          textAlign: 'center',
          margin: 0,
        }}
      >
        VEDA
      </h1>

      <p
        style={{
          color: '#858A7E',
          fontSize: '0.875rem',
          textAlign: 'center',
          maxWidth: '400px',
          lineHeight: 1.6,
          margin: 0,
        }}
      >
        Vehicle Evaluation Diagnostic Agents
        <br />
        Frontend scaffold operational. Backend and feature implementation begins in Phase 1.
      </p>

      <div
        style={{
          background: '#1A1D18',
          border: '1px solid #2a2d26',
          borderRadius: '8px',
          padding: '1rem 1.5rem',
          fontFamily: 'DM Mono, monospace',
          fontSize: '0.75rem',
          color: '#858A7E',
          textAlign: 'left',
          minWidth: '280px',
        }}
      >
        <div>React 18 ✓</div>
        <div>TypeScript ✓</div>
        <div>Vite ✓</div>
        <div>React Router ✓</div>
        <div style={{ marginTop: '0.5rem', color: '#B8E36A' }}>Stack: Operational</div>
      </div>
    </main>
  )
}

export default App
