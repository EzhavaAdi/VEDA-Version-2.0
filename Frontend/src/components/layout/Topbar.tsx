import { useAuth } from '../../features/authentication/AuthContext'
import { useNavigate } from 'react-router-dom'

export function Topbar({ title }: { title?: string }) {
  const { user, logout, primaryRole } = useAuth()
  const navigate = useNavigate()

  const roleLabel: Record<string, string> = {
    OWNER: 'Vehicle Owner', WORKSHOP_ADMIN: 'Workshop Admin',
    MECHANIC: 'Mechanic', VEDA_ADMIN: 'VEDA Admin',
  }

  return (
    <div style={{
      height: '56px', background: '#1A1D18',
      borderBottom: '1px solid #2a2d26',
      display: 'flex', alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 1.5rem',
    }}>
      {/* Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#B8E36A' }} />
        <span style={{ color: '#F4F4F0', fontWeight: 800, fontSize: '1rem', letterSpacing: '-0.02em' }}>
          VEDA
        </span>
        {title && (
          <>
            <span style={{ color: '#2a2d26', fontSize: '0.875rem' }}>/</span>
            <span style={{ color: '#858A7E', fontSize: '0.875rem' }}>{title}</span>
          </>
        )}
      </div>
      {/* User */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <span style={{ color: '#858A7E', fontSize: '0.75rem', fontFamily: 'DM Mono, monospace' }}>
          {primaryRole ? roleLabel[primaryRole] : ''}
        </span>
        <span style={{ color: '#F4F4F0', fontSize: '0.8rem' }}>
          {user?.full_name || user?.phone_number}
        </span>
        <button
          onClick={() => { logout(); navigate('/login') }}
          style={{
            background: 'none', border: '1px solid #3a3d36',
            color: '#858A7E', borderRadius: '5px', padding: '0.3rem 0.75rem',
            fontSize: '0.75rem', cursor: 'pointer',
          }}>
          Sign Out
        </button>
      </div>
    </div>
  )
}
