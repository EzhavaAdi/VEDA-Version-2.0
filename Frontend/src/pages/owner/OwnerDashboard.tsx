/**
 * VEDA V2 — Owner Dashboard Overview
 * Shows summary stats + recent service orders.
 */
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { AppShell }   from '../../components/layout/AppShell'
import { PageHeader } from '../../components/common/PageHeader'
import { StatusBadge } from '../../components/common/StatusBadge'
import { LoadingState, EmptyState, ErrorState } from '../../components/common/LoadingState'
import { serviceOrdersService, type ServiceOrder } from '../../services/service-orders.service'
import { vehiclesService, type Vehicle } from '../../services/vehicles.service'

export function OwnerDashboard() {
  const [orders,   setOrders]   = useState<ServiceOrder[]>([])
  const [vehicles, setVehicles] = useState<Vehicle[]>([])
  const [loading,  setLoading]  = useState(true)
  const [error,    setError]    = useState('')

  useEffect(() => {
    Promise.all([
      serviceOrdersService.listOwner(),
      vehiclesService.list(),
    ])
      .then(([o, v]) => { setOrders(o); setVehicles(v) })
      .catch(() => setError('Failed to load dashboard data.'))
      .finally(() => setLoading(false))
  }, [])

  const pending = orders.filter(o => o.status === 'AWAITING_APPROVAL').length
  const active  = orders.filter(o => !['VEHICLE_DELIVERED','CANCELLED','REJECTED'].includes(o.status)).length

  return (
    <AppShell title="Owner Dashboard">
      <PageHeader
        title="My Dashboard"
        subtitle="Overview of your vehicles and service activity"
        action={
          <Link to="/owner/vehicles" style={linkBtnStyle}>
            Register Vehicle
          </Link>
        }
      />

      {loading && <LoadingState />}
      {error   && <ErrorState message={error} />}

      {!loading && !error && (
        <>
          {/* Stats */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
            {[
              { label: 'Vehicles',         value: vehicles.length,    accent: false },
              { label: 'Active Services',  value: active,             accent: active > 0 },
              { label: 'Pending Approvals',value: pending,            accent: pending > 0 },
              { label: 'Total Orders',     value: orders.length,      accent: false },
            ].map(stat => (
              <div key={stat.label} style={statCard}>
                <p style={{ color: '#858A7E', fontSize: '0.7rem', textTransform: 'uppercase',
                  letterSpacing: '0.08em', margin: '0 0 0.5rem', fontFamily: 'DM Mono, monospace' }}>
                  {stat.label}
                </p>
                <p style={{ color: stat.accent ? '#B8E36A' : '#F4F4F0',
                  fontSize: '1.75rem', fontWeight: 700, margin: 0 }}>
                  {stat.value}
                </p>
              </div>
            ))}
          </div>

          {/* Recent orders */}
          <h2 style={sectionTitle}>Recent Service Orders</h2>
          {orders.length === 0
            ? <EmptyState message="No service orders yet. Find a service centre to get started." />
            : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {orders.slice(0, 8).map(order => (
                  <Link
                    key={order.id}
                    to={`/owner/orders/${order.id}`}
                    style={orderRow}
                  >
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <p style={{ color: '#F4F4F0', fontWeight: 600, margin: 0, fontSize: '0.875rem' }}>
                        {order.vehicle_reg} — {order.vehicle_make}
                      </p>
                      <p style={{ color: '#858A7E', fontSize: '0.75rem', margin: '0.1rem 0 0',
                        overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {order.centre_name} · {order.service_description.slice(0, 60)}
                      </p>
                    </div>
                    <div style={{ flexShrink: 0, display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
                      <StatusBadge status={order.status} />
                      <span style={{ color: '#858A7E', fontSize: '0.7rem', fontFamily: 'DM Mono, monospace' }}>
                        {new Date(order.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            )}
        </>
      )}
    </AppShell>
  )
}

const statCard: React.CSSProperties = {
  background: '#1A1D18', border: '1px solid #2a2d26',
  borderRadius: '8px', padding: '1rem 1.25rem',
}
const sectionTitle: React.CSSProperties = {
  color: '#F4F4F0', fontSize: '0.875rem', fontWeight: 600,
  textTransform: 'uppercase', letterSpacing: '0.08em',
  margin: '0 0 0.75rem',
}
const orderRow: React.CSSProperties = {
  display: 'flex', alignItems: 'center', gap: '1rem',
  background: '#1A1D18', border: '1px solid #2a2d26',
  borderRadius: '8px', padding: '0.75rem 1rem',
  textDecoration: 'none', transition: 'border-color 150ms',
}
const linkBtnStyle: React.CSSProperties = {
  background: '#B8E36A', color: '#10110F', borderRadius: '6px',
  padding: '0.5rem 1rem', fontWeight: 700, fontSize: '0.8rem',
  textDecoration: 'none',
}
