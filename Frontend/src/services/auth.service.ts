import { api } from './api'
import type { AuthUser } from '../features/authentication/AuthContext'

interface OtpRequestResponse { phone_number: string; is_new_user: boolean; expires_in_seconds: number }
interface OtpVerifyResponse  { access: string; refresh: string; user: AuthUser }

export const authService = {
  requestOtp: (phone_number: string) =>
    api.post<OtpRequestResponse>('/auth/request-otp/', { phone_number }),

  verifyOtp: (phone_number: string, code: string) =>
    api.post<OtpVerifyResponse>('/auth/verify-otp/', { phone_number, code }),

  refreshToken: (refresh: string) =>
    api.post<{ access: string }>('/auth/token/refresh/', { refresh }),

  getMe: () => api.get<AuthUser>('/auth/me/'),

  updateProfile: (full_name: string) =>
    api.patch<AuthUser>('/auth/me/', { full_name }),
}
