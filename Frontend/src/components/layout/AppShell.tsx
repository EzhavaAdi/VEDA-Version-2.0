/**
 * VEDA V2 — AppShell
 * Wraps authenticated pages: Sidebar + main content area.
 */
import type { ReactNode } from 'react'
import { Sidebar } from './Sidebar'
import { Topbar }  from './Topbar'

interface Props { children: ReactNode; title?: string }

export function AppShell({ children, title }: Props) {
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: '220px 1fr',
      gridTemplateRows: '56px 1fr',
      minHeight: '100vh',
      background: '#10110F',
    }}>
      {/* Top bar — spans both columns */}
      <div style={{ gridColumn: '1 / -1' }}>
        <Topbar title={title} />
      </div>
      {/* Sidebar */}
      <div style={{
        background: '#1A1D18',
        borderRight: '1px solid #2a2d26',
        height: 'calc(100vh - 56px)',
        overflow: 'hidden auto',
        position: 'sticky',
        top: '56px',
      }}>
        <Sidebar />
      </div>
      {/* Main content */}
      <main style={{
        padding: '1.5rem',
        overflowY: 'auto',
        height: 'calc(100vh - 56px)',
      }}>
        {children}
      </main>
    </div>
  )
}
