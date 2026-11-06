import { Routes, Route, Navigate } from 'react-router-dom'
import { lazy, Suspense }          from 'react'
import { AuthProvider, useAuth }   from './features/authentication/AuthContext'
import { ProtectedRoute }          from './routes/ProtectedRoute'
import { LoadingState }            from './components/common/LoadingState'

// ── Lazy pages ──────────────────────────────────────────────────────────────
const LoginPage           = lazy(() => import('./features/authentication/LoginPage').then(m => ({ default: m.LoginPage })))
const OwnerDashboard      = lazy(() => import('./pages/owner/OwnerDashboard').then(m => ({ default: m.OwnerDashboard })))
const OwnerApprovals      = lazy(() => import('./pages/owner/OwnerApprovals').then(m => ({ default: m.OwnerApprovals })))
const MechanicDashboard   = lazy(() => import('./pages/mechanic/MechanicDashboard').then(m => ({ default: m.MechanicDashboard })))
const WorkshopDashboard   = lazy(() => import('./pages/workshop/WorkshopDashboard').then(m => ({ default: m.WorkshopDashboard })))
const DiagnosisViewerDemo = lazy(() => import('./pages/diagnosis/DiagnosisViewerDemo').then(m => ({ default: m.DiagnosisViewerDemo })))

function PageLoader() {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center',
      justifyContent: 'center', background: '#10110F' }}>
      <LoadingState message="Loading..." />
    </div>
  )
}

// Role-based root redirect
function RoleRedirect() {
  const { user, primaryRole, isLoading } = useAuth()
  if (isLoading) return <PageLoader />
  if (!user) return <Navigate to="/login" replace />
  if (primaryRole === 'OWNER')          return <Navigate to="/owner"    replace />
  if (primaryRole === 'WORKSHOP_ADMIN') return <Navigate to="/workshop" replace />
  if (primaryRole === 'MECHANIC')       return <Navigate to="/workshop" replace />
  if (primaryRole === 'VEDA_ADMIN')     return <Navigate to="/admin"    replace />
  return <Navigate to="/role-select" replace />
}

// Landing (unauthenticated)
function Landing() {
  const { user } = useAuth()
  if (user) return <Navigate to="/" replace />
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center', background: '#10110F',
      color: '#F4F4F0', fontFamily: 'Manrope, sans-serif', gap: '1.5rem', padding: '2rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#B8E36A' }} />
        <span style={{ color: '#B8E36A', fontSize: '0.75rem', letterSpacing: '0.15em', textTransform: 'uppercase' }}>
          Vehicle Intelligence Platform
        </span>
      </div>
      <h1 style={{ fontSize: 'clamp(2.5rem,7vw,5rem)', fontWeight: 800,
        letterSpacing: '-0.03em', margin: 0, textAlign: 'center' }}>
        UNDERSTAND THE MACHINE.<br />BEFORE IT STOPS.
      </h1>
      <p style={{ color: '#858A7E', maxWidth: '440px', textAlign: 'center',
        lineHeight: 1.7, fontSize: '0.95rem', margin: 0 }}>
        Intelligent diagnostics, transparent maintenance and connected service management
        for the next generation of heavy vehicles.
      </p>
      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', justifyContent: 'center' }}>
        <a href="/login" style={{ background: '#B8E36A', color: '#10110F', padding: '0.75rem 2rem',
          borderRadius: '6px', fontWeight: 700, fontSize: '0.9rem', textDecoration: 'none' }}>
          Enter VEDA
        </a>
        <a href="/viewer" style={{ background: 'transparent', color: '#F4F4F0',
          padding: '0.75rem 2rem', borderRadius: '6px', fontWeight: 600, fontSize: '0.9rem',
          textDecoration: 'none', border: '1px solid #3a3d36' }}>
          View 3D Demo
        </a>
      </div>
    </div>
  )
}

function Unauthorized() {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center',
      justifyContent: 'center', background: '#10110F', flexDirection: 'column', gap: '1rem' }}>
      <p style={{ color: '#B96859', fontSize: '1rem' }}>Access denied.</p>
      <a href="/" style={{ color: '#858A7E', fontSize: '0.85rem' }}>← Go back</a>
    </div>
  )
}

function RoleSelect() {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center',
      justifyContent: 'center', background: '#10110F', flexDirection: 'column', gap: '1rem' }}>
      <p style={{ color: '#F4F4F0' }}>No role assigned yet.</p>
      <p style={{ color: '#858A7E', fontSize: '0.85rem', maxWidth: '360px', textAlign: 'center' }}>
        Ask a VEDA administrator or workshop admin to assign you a role.
      </p>
      <a href="/login" style={{ color: '#858A7E' }}>Sign out</a>
    </div>
  )
}

// ── Router ──────────────────────────────────────────────────────────────────
export default function App() {
  return (
    <AuthProvider>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          {/* Public */}
          <Route path="/landing" element={<Landing />} />
          <Route path="/login"   element={<LoginPage />} />
          <Route path="/viewer"  element={<DiagnosisViewerDemo />} />
          <Route path="/unauthorized" element={<Unauthorized />} />
          <Route path="/role-select"  element={<RoleSelect />} />

          {/* Role redirect from root */}
          <Route path="/" element={<ProtectedRoute><RoleRedirect /></ProtectedRoute>} />

          {/* Owner */}
          <Route path="/owner" element={
            <ProtectedRoute requireRole="OWNER"><OwnerDashboard /></ProtectedRoute>
          } />
          <Route path="/owner/approvals" element={
            <ProtectedRoute requireRole="OWNER"><OwnerApprovals /></ProtectedRoute>
          } />
          <Route path="/owner/orders"    element={
            <ProtectedRoute requireRole="OWNER"><OwnerDashboard /></ProtectedRoute>
          } />
          <Route path="/owner/vehicles"  element={
            <ProtectedRoute requireRole="OWNER"><OwnerDashboard /></ProtectedRoute>
          } />
          <Route path="/owner/history"   element={
            <ProtectedRoute requireRole="OWNER"><OwnerDashboard /></ProtectedRoute>
          } />

          {/* Workshop (Admin + Mechanic) */}
          <Route path="/workshop" element={
            <ProtectedRoute><WorkshopDashboard /></ProtectedRoute>
          } />
          <Route path="/workshop/orders" element={
            <ProtectedRoute><WorkshopDashboard /></ProtectedRoute>
          } />
          <Route path="/workshop/inspections" element={
            <ProtectedRoute requireRole="MECHANIC"><MechanicDashboard /></ProtectedRoute>
          } />
          <Route path="/workshop/estimates" element={
            <ProtectedRoute><MechanicDashboard /></ProtectedRoute>
          } />

          {/* Mechanic */}
          <Route path="/workshop/inspect/:orderId" element={
            <ProtectedRoute requireRole="MECHANIC"><MechanicDashboard /></ProtectedRoute>
          } />

          {/* Catch-all */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Suspense>
    </AuthProvider>
  )
}
