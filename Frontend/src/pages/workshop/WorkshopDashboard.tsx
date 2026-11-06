/**
 * VEDA V2 — Workshop Admin Dashboard
 * Shows service order queue, centre info, quick actions.
 */
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AppShell }    from '../../components/layout/AppShell'
import { PageHeader }  from '../../components/common/PageHeader'
import { StatusBadge } from '../../components/common/StatusBadge'
import { LoadingState, EmptyState, ErrorState } from '../../components/common/LoadingState'
import { organisationsService, type ServiceCentre } from '../../services/organisations.service'
import { serviceOrdersService, type ServiceOrder } from '../../services/service-orders.service'

export function WorkshopDashboard() {
  const [centre,  setCentre]  = useState<ServiceCentre | null>(null)
  const [orders,  setOrders]  = useState<ServiceOrder[]>([])
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState('')
  const [acting,  setActing]  = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    organisationsService.mine()
      .then(centres => {
        if (centres.length === 0) {
          setLoading(false)
          return
        }
        const c = centres[0]
        setCentre(c)
        return serviceOrdersService.listForCentre(c.id)
      })
      .then(o => o && setOrders(o))
      .catch(() => setError('Failed to load workshop data.'))
      .finally(() => setLoading(false))
  }, [])

  async function acceptOrder(orderId: string) {
    setActing(orderId)
    try {
      await serviceOrdersService.transition(orderId, 'ACCEPTED', 'Accepted by workshop.')
      setOrders(prev => prev.map(o => o.id === orderId ? { ...o, status: 'ACCEPTED' } : o))
    } catch { alert('Failed to accept order.') }
    finally { setActing(null) }
  }

  const incoming   = orders.filter(o => o.status === 'REQUESTED')
  const active     = orders.filter(o => !['VEHICLE_DELIVERED','CANCELLED','REJECTED','REQUESTED'].includes(o.status))
  const awaiting   = orders.filter(o => o.status === 'AWAITING_APPROVAL')

  return (
    <AppShell title="Workshop">
      <PageHeader
        title={centre?.name ?? 'Workshop Dashboard'}
        subtitle={centre ? `${centre.city} · ${centre.verification_status}` : ''}
        action={
          <button onClick={() => navigate('/workshop/orders')}
            style={{ background: '#B8E36A', color: '#10110F', border: 'none', borderRadius: '6px',
              padding: '0.5rem 1rem', fontWeight: 700, fontSize: '0.8rem', cursor: 'pointer' }}>
            View All Orders
          </button>
        }
      />

      {loading && <LoadingState />}
      {error   && <ErrorState message={error} />}

      {!loading && !error && (
        <>
          {/* Stats */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
            {[
              { label: 'Incoming',           value: incoming.length,  accent: incoming.length > 0 },
              { label: 'Active Jobs',        value: active.length,    accent: false },
              { label: 'Awaiting Approval',  value: awaiting.length,  accent: awaiting.length > 0 },
              { label: 'Total Orders',       value: orders.length,    accent: false },
            ].map(s => (
              <div key={s.label} style={statCard}>
                <p style={statLabel}>{s.label}</p>
                <p style={{ ...statVal, color: s.accent ? '#C89B4B' : '#F4F4F0' }}>{s.value}</p>
              </div>
            ))}
          </div>

          {/* Incoming requests */}
          {incoming.length > 0 && (
            <>
              <h2 style={sectionTitle}>Incoming Requests</h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '1.5rem' }}>
                {incoming.map(order => (
                  <div key={order.id} style={orderRow}>
                    <div style={{ flex: 1 }}>
                      <p style={{ color: '#F4F4F0', fontWeight: 600, margin: 0, fontSize: '0.875rem' }}>
                        {order.vehicle_reg} — {order.vehicle_make}
                      </p>
                      <p style={{ color: '#858A7E', fontSize: '0.75rem', margin: '0.1rem 0 0' }}>
                        Owner: {order.owner_phone} · {order.service_description.slice(0, 60)}
                      </p>
                    </div>
                    <button
                      disabled={acting === order.id}
                      onClick={() => acceptOrder(order.id)}
                      style={{ background: '#91B95722', border: '1px solid #91B95744', color: '#91B957',
                        borderRadius: '5px', padding: '0.35rem 0.9rem', fontSize: '0.75rem',
                        cursor: 'pointer', fontWeight: 600, flexShrink: 0 }}>
                      {acting === order.id ? '...' : 'Accept'}
                    </button>
                  </div>
                ))}
              </div>
            </>
          )}

          {/* Active jobs */}
          <h2 style={sectionTitle}>Active Jobs</h2>
          {active.length === 0
            ? <EmptyState message="No active jobs right now." />
            : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {active.slice(0, 10).map(order => (
                  <div key={order.id} style={{ ...orderRow, cursor: 'pointer' }}
                    onClick={() => navigate(`/workshop/orders/${order.id}`)}>
                    <div style={{ flex: 1 }}>
                      <p style={{ color: '#F4F4F0', fontWeight: 600, margin: 0, fontSize: '0.875rem' }}>
                        {order.vehicle_reg} — {order.vehicle_make}
                      </p>
                      <p style={{ color: '#858A7E', fontSize: '0.75rem', margin: '0.1rem 0 0' }}>
                        Mechanic: {order.mechanic_name ?? order.mechanic_phone ?? '— unassigned'}
                      </p>
                    </div>
                    <StatusBadge status={order.status} />
                  </div>
                ))}
              </div>
            )}
        </>
      )}
    </AppShell>
  )
}

const statCard:  React.CSSProperties = { background: '#1A1D18', border: '1px solid #2a2d26', borderRadius: '8px', padding: '1rem 1.25rem' }
const statLabel: React.CSSProperties = { color: '#858A7E', fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.08em', margin: '0 0 0.5rem', fontFamily: 'DM Mono, monospace' }
const statVal:   React.CSSProperties = { fontSize: '1.75rem', fontWeight: 700, margin: 0 }
const sectionTitle: React.CSSProperties = { color: '#F4F4F0', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', margin: '0 0 0.75rem' }
const orderRow:  React.CSSProperties = { display: 'flex', alignItems: 'center', gap: '1rem', background: '#1A1D18', border: '1px solid #2a2d26', borderRadius: '8px', padding: '0.75rem 1rem' }
