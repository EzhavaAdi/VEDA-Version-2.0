/**
 * VEDA V2 — ProtectedRoute
 * Redirects unauthenticated users to /login.
 * Optionally enforces a required role.
 */
import { Navigate } from 'react-router-dom'
import { useAuth, type UserRole } from '../features/authentication/AuthContext'
import { LoadingState } from '../components/common/LoadingState'
import type { ReactNode } from 'react'

interface Props {
  children:     ReactNode
  requireRole?: UserRole
}

export function ProtectedRoute({ children, requireRole }: Props) {
  const { user, isLoading, hasRole } = useAuth()

  if (isLoading) return <LoadingState message="Authenticating..." />
  if (!user)     return <Navigate to="/login" replace />
  if (requireRole && !hasRole(requireRole)) return <Navigate to="/unauthorized" replace />

  return <>{children}</>
}
