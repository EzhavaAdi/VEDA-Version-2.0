/**
 * VEDA V2 — Auth Context
 *
 * Provides current user, roles, JWT tokens and auth actions to the whole app.
 * Tokens are stored in localStorage (access + refresh).
 * The api.ts interceptor reads the token here for every request.
 */

import {
  createContext, useContext, useState, useEffect, useCallback,
  type ReactNode,
} from 'react'

export type UserRole = 'OWNER' | 'WORKSHOP_ADMIN' | 'MECHANIC' | 'VEDA_ADMIN'

export interface AuthUser {
  id: string
  phone_number: string
  full_name: string
  roles: UserRole[]
  is_new_user?: boolean
}

interface AuthState {
  user:      AuthUser | null
  accessToken: string | null
  isLoading:  boolean
}

interface AuthContextValue extends AuthState {
  setTokens:  (access: string, refresh: string, user: AuthUser) => void
  logout:     () => void
  hasRole:    (role: UserRole) => boolean
  primaryRole: UserRole | null
}

const AuthContext = createContext<AuthContextValue | null>(null)

const ACCESS_KEY  = 'veda_access'
const REFRESH_KEY = 'veda_refresh'
const USER_KEY    = 'veda_user'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({
    user:        null,
    accessToken: null,
    isLoading:   true,
  })

  // Restore from localStorage on mount
  useEffect(() => {
    const access  = localStorage.getItem(ACCESS_KEY)
    const userStr = localStorage.getItem(USER_KEY)
    if (access && userStr) {
      try {
        const user = JSON.parse(userStr) as AuthUser
        setState({ user, accessToken: access, isLoading: false })
      } catch {
        localStorage.clear()
        setState({ user: null, accessToken: null, isLoading: false })
      }
    } else {
      setState(s => ({ ...s, isLoading: false }))
    }
  }, [])

  const setTokens = useCallback((access: string, refresh: string, user: AuthUser) => {
    localStorage.setItem(ACCESS_KEY,  access)
    localStorage.setItem(REFRESH_KEY, refresh)
    localStorage.setItem(USER_KEY,    JSON.stringify(user))
    setState({ user, accessToken: access, isLoading: false })
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(ACCESS_KEY)
    localStorage.removeItem(REFRESH_KEY)
    localStorage.removeItem(USER_KEY)
    setState({ user: null, accessToken: null, isLoading: false })
  }, [])

  const hasRole = useCallback((role: UserRole) =>
    state.user?.roles.includes(role) ?? false,
  [state.user])

  // Role priority: VEDA_ADMIN > WORKSHOP_ADMIN > MECHANIC > OWNER
  const primaryRole: UserRole | null = (() => {
    const roles = state.user?.roles ?? []
    if (roles.includes('VEDA_ADMIN'))     return 'VEDA_ADMIN'
    if (roles.includes('WORKSHOP_ADMIN')) return 'WORKSHOP_ADMIN'
    if (roles.includes('MECHANIC'))       return 'MECHANIC'
    if (roles.includes('OWNER'))          return 'OWNER'
    return null
  })()

  return (
    <AuthContext.Provider value={{ ...state, setTokens, logout, hasRole, primaryRole }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

/** Read the current access token (used by api.ts) */
export function getStoredToken(): string | null {
  return localStorage.getItem(ACCESS_KEY)
}

export function getStoredRefresh(): string | null {
  return localStorage.getItem(REFRESH_KEY)
}
