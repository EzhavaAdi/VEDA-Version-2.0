import { NavLink } from 'react-router-dom'
import { useAuth } from '../../features/authentication/AuthContext'

interface NavItem { label: string; path: string; icon: string }

const ownerNav: NavItem[] = [
  { label: 'Overview',     path: '/owner',           icon: '◈' },
  { label: 'My Vehicles',  path: '/owner/vehicles',  icon: '⊡' },
  { label: 'Service Orders', path: '/owner/orders',  icon: '⊞' },
  { label: 'Approvals',    path: '/owner/approvals', icon: '✓' },
  { label: 'History',      path: '/owner/history',   icon: '◷' },
]

const mechanicNav: NavItem[] = [
  { label: 'My Orders',    path: '/workshop',              icon: '◈' },
  { label: 'Inspections',  path: '/workshop/inspections',  icon: '⊡' },
  { label: 'Estimates',    path: '/workshop/estimates',    icon: '⊞' },
  { label: '3D Viewer',    path: '/viewer',                icon: '◉' },
]

const workshopAdminNav: NavItem[] = [
  { label: 'Overview',     path: '/workshop',              icon: '◈' },
  { label: 'Service Orders', path: '/workshop/orders',     icon: '⊞' },
  { label: 'Mechanics',    path: '/workshop/mechanics',    icon: '⊡' },
  { label: 'Inventory',    path: '/workshop/inventory',    icon: '◫' },
  { label: 'Estimates',    path: '/workshop/estimates',    icon: '✓' },
]

export function Sidebar() {
  const { primaryRole } = useAuth()

  const navItems =
    primaryRole === 'OWNER'          ? ownerNav :
    primaryRole === 'WORKSHOP_ADMIN' ? workshopAdminNav :
    primaryRole === 'MECHANIC'       ? mechanicNav : []

  return (
    <nav style={{ padding: '1rem 0.5rem' }}>
      {navItems.map(item => (
        <NavLink
          key={item.path}
          to={item.path}
          end={item.path.split('/').length <= 2}
          style={({ isActive }) => ({
            display: 'flex', alignItems: 'center', gap: '0.6rem',
            padding: '0.55rem 0.75rem', borderRadius: '6px',
            marginBottom: '0.15rem', textDecoration: 'none',
            color: isActive ? '#F4F4F0' : '#858A7E',
            background: isActive ? '#10110F' : 'transparent',
            fontSize: '0.85rem', fontWeight: isActive ? 600 : 400,
            borderLeft: isActive ? '2px solid #B8E36A' : '2px solid transparent',
          })}
        >
          <span style={{ fontFamily: 'DM Mono, monospace', fontSize: '0.8rem', width: '16px' }}>
            {item.icon}
          </span>
          {item.label}
        </NavLink>
      ))}
    </nav>
  )
}
