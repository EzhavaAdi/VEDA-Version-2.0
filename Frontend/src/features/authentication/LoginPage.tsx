/**
 * VEDA V2 — Login Page
 *
 * Two-step: phone number → OTP → JWT issued → role redirect.
 * Matches DESIGN.md: minimal layout, Carbon Black background.
 */

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from './AuthContext'
import { authService } from '../../services/auth.service'

type Step = 'phone' | 'otp' | 'profile'

export function LoginPage() {
  const { setTokens } = useAuth()
  const navigate      = useNavigate()

  const [step,       setStep]       = useState<Step>('phone')
  const [phone,      setPhone]      = useState('')
  const [otp,        setOtp]        = useState('')
  const [fullName,   setFullName]   = useState('')
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState('')

  // ── Step 1: Request OTP ────────────────────────────────────────────────
  async function handleRequestOtp(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await authService.requestOtp(phone)
      setStep('otp')
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Failed to send OTP.')
    } finally {
      setLoading(false)
    }
  }

  // ── Step 2: Verify OTP ─────────────────────────────────────────────────
  async function handleVerifyOtp(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const res = await authService.verifyOtp(phone, otp)
      setTokens(res.access, res.refresh, res.user)

      if (res.user.is_new_user || !res.user.full_name) {
        setStep('profile')
        return
      }
      redirectByRole(res.user.roles)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Invalid OTP.')
    } finally {
      setLoading(false)
    }
  }

  // ── Step 3: Profile setup (new users) ─────────────────────────────────
  async function handleProfileSetup(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const user = await authService.updateProfile(fullName)
      setTokens(
        localStorage.getItem('veda_access') ?? '',
        localStorage.getItem('veda_refresh') ?? '',
        { ...user, roles: user.roles ?? [] }
      )
      redirectByRole(user.roles ?? [])
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Profile update failed.')
    } finally {
      setLoading(false)
    }
  }

  function redirectByRole(roles: string[]) {
    if (roles.includes('VEDA_ADMIN'))     navigate('/admin')
    else if (roles.includes('WORKSHOP_ADMIN') || roles.includes('MECHANIC'))
      navigate('/workshop')
    else if (roles.includes('OWNER'))     navigate('/owner')
    else navigate('/role-select')
  }

  return (
    <div style={s.page}>
      <div style={s.card}>
        {/* Logo */}
        <div style={s.logo}>
          <div style={s.dot} />
          <span style={s.logoText}>VEDA</span>
        </div>
        <p style={s.tagline}>Vehicle Evaluation Diagnostic Agents</p>

        {/* Step: phone */}
        {step === 'phone' && (
          <form onSubmit={handleRequestOtp} style={s.form}>
            <p style={s.stepLabel}>Enter your phone number</p>
            <input
              style={s.input}
              type="tel"
              placeholder="+91 98765 43210"
              value={phone}
              onChange={e => setPhone(e.target.value)}
              required
              autoFocus
            />
            {error && <p style={s.error}>{error}</p>}
            <button style={s.btn} type="submit" disabled={loading}>
              {loading ? 'Sending...' : 'Send OTP'}
            </button>
          </form>
        )}

        {/* Step: OTP */}
        {step === 'otp' && (
          <form onSubmit={handleVerifyOtp} style={s.form}>
            <p style={s.stepLabel}>Enter the 6-digit OTP sent to</p>
            <p style={s.phoneDisplay}>{phone}</p>
            <input
              style={{ ...s.input, textAlign: 'center', letterSpacing: '0.4em', fontSize: '1.25rem' }}
              type="text"
              inputMode="numeric"
              maxLength={6}
              placeholder="000000"
              value={otp}
              onChange={e => setOtp(e.target.value.replace(/\D/g, ''))}
              required
              autoFocus
            />
            {error && <p style={s.error}>{error}</p>}
            <button style={s.btn} type="submit" disabled={loading || otp.length !== 6}>
              {loading ? 'Verifying...' : 'Verify OTP'}
            </button>
            <button type="button" style={s.linkBtn} onClick={() => setStep('phone')}>
              Change number
            </button>
          </form>
        )}

        {/* Step: profile setup */}
        {step === 'profile' && (
          <form onSubmit={handleProfileSetup} style={s.form}>
            <p style={s.stepLabel}>Welcome to VEDA! Set your name</p>
            <input
              style={s.input}
              type="text"
              placeholder="Your full name"
              value={fullName}
              onChange={e => setFullName(e.target.value)}
              required
              autoFocus
              minLength={2}
            />
            {error && <p style={s.error}>{error}</p>}
            <button style={s.btn} type="submit" disabled={loading}>
              {loading ? 'Saving...' : 'Continue'}
            </button>
          </form>
        )}
      </div>
    </div>
  )
}

const s: Record<string, React.CSSProperties> = {
  page:        { minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#10110F', padding: '1rem' },
  card:        { background: '#1A1D18', border: '1px solid #2a2d26', borderRadius: '12px', padding: '2.5rem', width: '100%', maxWidth: '380px' },
  logo:        { display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' },
  dot:         { width: '10px', height: '10px', borderRadius: '50%', background: '#B8E36A' },
  logoText:    { color: '#F4F4F0', fontSize: '1.5rem', fontWeight: 800, letterSpacing: '-0.02em' },
  tagline:     { color: '#858A7E', fontSize: '0.75rem', marginBottom: '2rem', fontFamily: 'DM Mono, monospace' },
  form:        { display: 'flex', flexDirection: 'column', gap: '0.75rem' },
  stepLabel:   { color: '#F4F4F0', fontSize: '0.875rem', fontWeight: 500, margin: 0 },
  phoneDisplay:{ color: '#B8E36A', fontFamily: 'DM Mono, monospace', fontSize: '0.875rem', margin: 0 },
  input:       { background: '#10110F', border: '1px solid #3a3d36', borderRadius: '6px', padding: '0.7rem 0.9rem', color: '#F4F4F0', fontSize: '0.95rem', fontFamily: 'Manrope, sans-serif', outline: 'none', width: '100%', boxSizing: 'border-box' },
  btn:         { background: '#B8E36A', color: '#10110F', border: 'none', borderRadius: '6px', padding: '0.75rem', fontWeight: 700, fontSize: '0.875rem', cursor: 'pointer', marginTop: '0.25rem' },
  linkBtn:     { background: 'none', border: 'none', color: '#858A7E', fontSize: '0.8rem', cursor: 'pointer', textDecoration: 'underline', padding: 0, textAlign: 'center' },
  error:       { color: '#B96859', fontSize: '0.8rem', margin: 0 },
}
