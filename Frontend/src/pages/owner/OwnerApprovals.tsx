/**
 * VEDA V2 — Owner Approvals
 * Shows all AWAITING_APPROVAL orders with itemised estimate decisions.
 */
import { useEffect, useState } from 'react'
import { AppShell }   from '../../components/layout/AppShell'
import { PageHeader } from '../../components/common/PageHeader'
import { StatusBadge } from '../../components/common/StatusBadge'
import { LoadingState, EmptyState, ErrorState } from '../../components/common/LoadingState'
import { serviceOrdersService, type ServiceOrder } from '../../services/service-orders.service'
import { estimatesService, type Estimate } from '../../services/estimates.service'

export function OwnerApprovals() {
  const [orders,  setOrders]  = useState<ServiceOrder[]>([])
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState('')
  const [deciding, setDeciding] = useState<string | null>(null)
  const [estimates, setEstimates] = useState<Record<string, Estimate[]>>({})

  useEffect(() => {
    serviceOrdersService.listOwner()
      .then(all => {
        const pending = all.filter(o => o.status === 'AWAITING_APPROVAL')
        setOrders(pending)
        // Fetch estimates for each pending order
        return Promise.all(pending.map(o =>
          estimatesService.list(o.id).then(ests => ({ orderId: o.id, ests }))
        ))
      })
      .then(results => {
        const map: Record<string, Estimate[]> = {}
        results.forEach(r => { map[r.orderId] = r.ests })
        setEstimates(map)
      })
      .catch(() => setError('Failed to load approvals.'))
      .finally(() => setLoading(false))
  }, [])

  async function decide(itemId: string, decision: string, note = '') {
    setDeciding(itemId)
    try {
      await estimatesService.decideItem(itemId, decision, note)
      // Refresh estimates
      const updated = await Promise.all(orders.map(o =>
        estimatesService.list(o.id).then(ests => ({ orderId: o.id, ests }))
      ))
      const map: Record<string, Estimate[]> = {}
      updated.forEach(r => { map[r.orderId] = r.ests })
      setEstimates(map)
    } catch {
      alert('Failed to record decision.')
    } finally {
      setDeciding(null)
    }
  }

  return (
    <AppShell title="Approvals">
      <PageHeader title="Pending Approvals"
        subtitle="Review and approve repair estimate items" />

      {loading && <LoadingState />}
      {error   && <ErrorState message={error} />}
      {!loading && !error && orders.length === 0 && (
        <EmptyState message="No estimates awaiting your approval." />
      )}

      {!loading && !error && orders.map(order => {
        const ests = estimates[order.id] ?? []
        const submitted = ests.find(e => e.estimate_status === 'SUBMITTED')
        if (!submitted) return null

        return (
          <div key={order.id} style={card}>
            {/* Order header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <div>
                <p style={label}>Vehicle</p>
                <p style={value}>{order.vehicle_reg} — {order.vehicle_make}</p>
              </div>
              <div>
                <p style={label}>Service Centre</p>
                <p style={value}>{order.centre_name}</p>
              </div>
              <div>
                <p style={label}>Estimate Total</p>
                <p style={{ ...value, color: '#B8E36A', fontSize: '1.1rem' }}>
                  ₹{parseFloat(submitted.grand_total).toLocaleString('en-IN')}
                </p>
              </div>
            </div>

            {/* Line items */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {submitted.items.map(item => (
                <div key={item.id} style={itemRow}>
                  <div style={{ flex: 1 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.2rem' }}>
                      <span style={{ color: '#F4F4F0', fontSize: '0.875rem', fontWeight: 500 }}>
                        {item.description}
                      </span>
                      <StatusBadge status={item.approval_status} />
                    </div>
                    <p style={{ color: '#858A7E', fontSize: '0.75rem', margin: 0, fontFamily: 'DM Mono, monospace' }}>
                      {item.component_code}
                      {item.part_name ? ` · Part: ${item.part_name}` : ''}
                      {' · '}Qty {item.quantity}
                      {' · '}Parts ₹{parseFloat(item.unit_price).toLocaleString('en-IN')}
                      {' · '}Labour ₹{parseFloat(item.labour_cost).toLocaleString('en-IN')}
                    </p>
                  </div>
                  {item.approval_status === 'PENDING' && (
                    <div style={{ display: 'flex', gap: '0.5rem', flexShrink: 0 }}>
                      <button
                        disabled={deciding === item.id}
                        onClick={() => decide(item.id, 'APPROVED')}
                        style={approveBtn}>
                        {deciding === item.id ? '...' : 'Approve'}
                      </button>
                      <button
                        disabled={deciding === item.id}
                        onClick={() => decide(item.id, 'REJECTED')}
                        style={rejectBtn}>
                        Reject
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )
      })}
    </AppShell>
  )
}

const card: React.CSSProperties = {
  background: '#1A1D18', border: '1px solid #2a2d26',
  borderRadius: '8px', padding: '1.25rem', marginBottom: '1rem',
}
const itemRow: React.CSSProperties = {
  display: 'flex', alignItems: 'center', gap: '1rem',
  background: '#10110F', borderRadius: '6px', padding: '0.75rem 1rem',
}
const label: React.CSSProperties = { color: '#858A7E', fontSize: '0.7rem', textTransform: 'uppercase', letterSpacing: '0.08em', margin: '0 0 0.2rem', fontFamily: 'DM Mono, monospace' }
const value: React.CSSProperties = { color: '#F4F4F0', fontSize: '0.875rem', fontWeight: 500, margin: 0 }
const approveBtn: React.CSSProperties = { background: '#91B95722', border: '1px solid #91B95744', color: '#91B957', borderRadius: '5px', padding: '0.3rem 0.75rem', fontSize: '0.75rem', cursor: 'pointer', fontWeight: 600 }
const rejectBtn:  React.CSSProperties = { background: '#B9685922', border: '1px solid #B9685944', color: '#B96859', borderRadius: '5px', padding: '0.3rem 0.75rem', fontSize: '0.75rem', cursor: 'pointer', fontWeight: 600 }
