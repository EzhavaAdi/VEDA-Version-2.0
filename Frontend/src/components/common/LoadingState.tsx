export function LoadingState({ message = 'Loading...' }: { message?: string }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: '3rem', color: '#858A7E',
      fontFamily: 'DM Mono, monospace', fontSize: '0.8rem',
    }}>
      {message}
    </div>
  )
}

export function EmptyState({ message }: { message: string }) {
  return (
    <div style={{
      background: '#1A1D18', border: '1px dashed #2a2d26',
      borderRadius: '8px', padding: '2.5rem',
      textAlign: 'center', color: '#858A7E', fontSize: '0.875rem',
    }}>
      {message}
    </div>
  )
}

export function ErrorState({ message }: { message: string }) {
  return (
    <div style={{
      background: '#B9685911', border: '1px solid #B9685933',
      borderRadius: '8px', padding: '1rem 1.25rem',
      color: '#B96859', fontSize: '0.875rem',
    }}>
      {message}
    </div>
  )
}
