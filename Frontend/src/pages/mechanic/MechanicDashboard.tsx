/**
 * VEDA V2 — Mechanic Dashboard
 * Shows assigned service orders with action buttons for each stage.
 */
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AppShell }    from '../../components/layout/AppShell'
import { PageHeader }  from '../../components/common/PageHeader'
import { StatusBadge } from '../../components/common/StatusBadge'
import { LoadingState, EmptyState, ErrorState } from '../../components/common/LoadingState'
import { serviceOrdersService, type ServiceOrder } from '../../services/service-orders.service'
import { inspectionsService } from '../../services/inspections.service'

export function MechanicDashboard() {
  const [orders,  setOrders]  = useState<ServiceOrder[]>([])
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState('')
  const [acting,  setActing]  = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    serviceOrdersService.listForMechanic()
      .then(setOrders)
      .catch(() => setError('Failed to load assigned orders.'))
      .finally(() => setLoading(false))
  }, [])

  async function startInspection(orderId: string) {
    setActing(orderId)
    try {
      await inspectionsService.start(orderId)
      navigate(`/workshop/inspect/${orderId}`)
    } catch (err: unknown) {
      const e = err as { detail?: string }
      alert(e?.detail ?? 'Failed to start inspection.')
    } finally {
      setActing(null)
    }
  }

  const nextAction = (order: ServiceOrder) => {
    if (order.status === 'VEHICLE_RECEIVED')         return { label: 'Start Inspection', action: () => startInspection(order.id) }
    if (order.status === 'INSPECTION_IN_PROGRESS')   return { label: 'Continue Inspection', action: () => navigate(`/workshop/inspect/${order.id}`) }
    if (order.status === 'ESTIMATE_READY')            return { label: 'Prepare Estimate', action: () => navigate(`/workshop/estimate/${order.id}`) }
    if (order.status === 'REPAIR_IN_PROGRESS')        return { label: 'Update Repair', action: () => navigate(`/workshop/repair/${order.id}`) }
    return null
  }

  return (
    <AppShell title="My Orders">
      <PageHeader title="Assigned Orders"
        subtitle="Vehicles assigned to you for inspection and repair" />

      {loading && <LoadingState />}
      {error   && <ErrorState message={error} />}
      {!loading && !error && orders.length === 0 && (
        <EmptyState message="No orders assigned to you." />
      )}

      {!loading && !error && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {orders.map(order => {
            const action = nextAction(order)
            return (
              <div key={order.id} style={card}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div style={{ flex: 1 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
                      <span style={{ color: '#F4F4F0', fontWeight: 600, fontSize: '0.95rem' }}>
                        {order.vehicle_reg}
                      </span>
                      <span style={{ color: '#858A7E', fontSize: '0.8rem' }}>{order.vehicle_make}</span>
                      <StatusBadge status={order.status} />
                    </div>
                    <p style={{ color: '#858A7E', fontSize: '0.8rem', margin: 0 }}>
                      {order.centre_name} · {order.service_description.slice(0, 80)}
                    </p>
                  </div>
                  {action && (
                    <button
                      disabled={acting === order.id}
                      onClick={action.action}
                      style={actionBtn}>
                      {acting === order.id ? '...' : action.label} →
                    </button>
                  )}
                </div>
                <div style={{ display: 'flex', gap: '1.5rem', marginTop: '0.75rem',
                  paddingTop: '0.75rem', borderTop: '1px solid #2a2d26' }}>
                  {[
                    ['Owner',   order.owner_phone],
                    ['Centre',  order.centre_name],
                    ['Received', order.received_at ? new Date(order.received_at).toLocaleDateString() : '—'],
                    ['Order ID', order.id.slice(0, 8) + '...'],
                  ].map(([k, v]) => (
                    <div key={k as string}>
                      <p style={{ color: '#858A7E', fontSize: '0.65rem', textTransform: 'uppercase',
                        letterSpacing: '0.08em', margin: 0, fontFamily: 'DM Mono, monospace' }}>{k}</p>
                      <p style={{ color: '#F4F4F0', fontSize: '0.8rem', margin: '0.1rem 0 0',
                        fontFamily: 'DM Mono, monospace' }}>{v}</p>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </AppShell>
  )
}

const card: React.CSSProperties = {
  background: '#1A1D18', border: '1px solid #2a2d26',
  borderRadius: '8px', padding: '1.25rem',
}
const actionBtn: React.CSSProperties = {
  background: '#B8E36A', color: '#10110F', border: 'none',
  borderRadius: '6px', padding: '0.5rem 1rem', fontWeight: 700,
  fontSize: '0.8rem', cursor: 'pointer', flexShrink: 0, marginLeft: '1rem',
}
