/**
 * VEDA V2 — Central API client with auth header injection.
 * All service modules import from here.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

export interface ApiError {
  status:  number
  message: string
  detail?: unknown
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  // Inject JWT token
  const token = localStorage.getItem('veda_access')
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> ?? {}),
  }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers })

  if (!response.ok) {
    let detail: unknown
    try { detail = await response.json() } catch { detail = response.statusText }
    throw { status: response.status, message: `API error ${response.status}`, detail } as ApiError
  }

  if (response.status === 204) return {} as T
  return response.json() as Promise<T>
}

export const api = {
  get:    <T>(ep: string, opts?: RequestInit) => request<T>(ep, { method: 'GET', ...opts }),
  post:   <T>(ep: string, body: unknown, opts?: RequestInit) =>
    request<T>(ep, { method: 'POST', body: JSON.stringify(body), ...opts }),
  patch:  <T>(ep: string, body: unknown, opts?: RequestInit) =>
    request<T>(ep, { method: 'PATCH', body: JSON.stringify(body), ...opts }),
  put:    <T>(ep: string, body: unknown, opts?: RequestInit) =>
    request<T>(ep, { method: 'PUT', body: JSON.stringify(body), ...opts }),
  delete: <T>(ep: string, opts?: RequestInit) => request<T>(ep, { method: 'DELETE', ...opts }),
}
