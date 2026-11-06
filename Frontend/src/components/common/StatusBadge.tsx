/** VEDA V2 — Status badge for service order states, approval states, etc. */

interface Props { status: string; size?: 'sm' | 'md' }

const STATUS_COLOURS: Record<string, { bg: string; text: string }> = {
  // Service order
  REQUESTED:              { bg: '#66869B22', text: '#66869B' },
  ACCEPTED:               { bg: '#B8E36A22', text: '#B8E36A' },
  VEHICLE_RECEIVED:       { bg: '#B8E36A22', text: '#B8E36A' },
  INSPECTION_IN_PROGRESS: { bg: '#C89B4B22', text: '#C89B4B' },
  ESTIMATE_READY:         { bg: '#C89B4B22', text: '#C89B4B' },
  AWAITING_APPROVAL:      { bg: '#C89B4B22', text: '#C89B4B' },
  APPROVED:               { bg: '#91B95722', text: '#91B957' },
  PARTIALLY_APPROVED:     { bg: '#91B95722', text: '#91B957' },
  REPAIR_IN_PROGRESS:     { bg: '#B8E36A22', text: '#B8E36A' },
  FINAL_INSPECTION:       { bg: '#B8E36A22', text: '#B8E36A' },
  INVOICED:               { bg: '#66869B22', text: '#66869B' },
  PAYMENT_PENDING:        { bg: '#C89B4B22', text: '#C89B4B' },
  PAID:                   { bg: '#91B95722', text: '#91B957' },
  VEHICLE_DELIVERED:      { bg: '#829B7522', text: '#829B75' },
  CANCELLED:              { bg: '#B9685922', text: '#B96859' },
  REJECTED:               { bg: '#B9685922', text: '#B96859' },
  // Approval
  PENDING:                { bg: '#C89B4B22', text: '#C89B4B' },
  // Generic
  COMPLETED:              { bg: '#91B95722', text: '#91B957' },
  FAILED:                 { bg: '#B9685922', text: '#B96859' },
  VERIFIED:               { bg: '#91B95722', text: '#91B957' },
}

export function StatusBadge({ status, size = 'sm' }: Props) {
  const c = STATUS_COLOURS[status] ?? { bg: '#85807E22', text: '#858A7E' }
  return (
    <span style={{
      display: 'inline-block',
      background: c.bg, color: c.text,
      borderRadius: '999px',
      padding: size === 'sm' ? '0.15rem 0.6rem' : '0.25rem 0.8rem',
      fontSize: size === 'sm' ? '0.65rem' : '0.75rem',
      fontWeight: 600, fontFamily: 'DM Mono, monospace',
      letterSpacing: '0.04em', textTransform: 'uppercase', whiteSpace: 'nowrap',
    }}>
      {status.replace(/_/g, ' ')}
    </span>
  )
}
