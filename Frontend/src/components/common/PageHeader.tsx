import type { ReactNode } from 'react'

interface Props {
  title:    string
  subtitle?: string
  action?:  ReactNode
}

export function PageHeader({ title, subtitle, action }: Props) {
  return (
    <div style={{
      display: 'flex', justifyContent: 'space-between',
      alignItems: 'flex-start', marginBottom: '1.5rem',
    }}>
      <div>
        <h1 style={{ color: '#F4F4F0', fontSize: '1.25rem', fontWeight: 700,
          letterSpacing: '-0.02em', margin: 0 }}>{title}</h1>
        {subtitle && <p style={{ color: '#858A7E', fontSize: '0.8rem', margin: '0.25rem 0 0' }}>{subtitle}</p>}
      </div>
      {action}
    </div>
  )
}
