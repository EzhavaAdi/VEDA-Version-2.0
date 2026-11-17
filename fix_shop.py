path = r"C:\VEDA_2.0\Frontend\src\App.tsx"
with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# Replace entire ProductCard function (lines 800-869, 0-indexed 799-868)
new_card = r"""function ProductCard({ product: p, qty, onAdd, onRemove }: {
  product: import('./services/shop.service').ShopProduct
  qty: number; onAdd: () => void; onRemove: () => void
}) {
  return (
    <div style={{ background: '#FAF8F4', border: `1px solid ${qty > 0 ? '#B8E36A' : '#E0D8CC'}`, borderRadius: '10px', padding: '16px 14px', display: 'flex', flexDirection: 'column', gap: '8px', transition: 'border-color 150ms' }}>
      {/* Image */}
      <div style={{ width: '100%', aspectRatio: '1', background: '#E8E0D0', borderRadius: '8px', overflow: 'hidden', marginBottom: '4px', position: 'relative' }}>
        {p.image_path ? (
          <img
            src={`/shop/${p.image_path}`}
            alt={p.name}
            style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
            onError={e => { (e.target as HTMLImageElement).style.display = 'none' }}
          />
        ) : (
          <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#E8E0D0' }}>
            <span style={{ color: '#8A8070', fontSize: '0.75rem', fontFamily: 'DM Mono, monospace', letterSpacing: '0.08em', textTransform: 'uppercase' }}>No image</span>
          </div>
        )}
        {p.discount_percent > 0 && (
          <div style={{ position: 'absolute', top: '6px', left: '6px', background: '#0F1319', color: '#B8E36A', borderRadius: '4px', padding: '3px 7px', fontSize: '0.68rem', fontWeight: 700, fontFamily: 'DM Mono, monospace', letterSpacing: '0.05em' }}>
            {p.discount_percent}% OFF
          </div>
        )}
        {!p.in_stock && (
          <div style={{ position: 'absolute', inset: 0, background: 'rgba(242,237,228,0.82)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ color: '#8A8070', fontSize: '0.72rem', fontFamily: 'DM Mono, monospace', letterSpacing: '0.1em', textTransform: 'uppercase' }}>Out of Stock</span>
          </div>
        )}
      </div>
      {/* Details */}
      <div>
        <p style={{ color: '#8A8070', fontSize: '0.72rem', fontFamily: 'DM Mono, monospace', margin: '0 0 4px', textTransform: 'uppercase', letterSpacing: '0.08em' }}>{p.brand}</p>
        <p style={{ color: '#0F1319', fontSize: '0.9rem', fontWeight: 600, margin: '0 0 2px', lineHeight: 1.4, fontFamily: 'Manrope, sans-serif' }}>{p.name}</p>
        <p style={{ color: '#B0A890', fontSize: '0.72rem', fontFamily: 'DM Mono, monospace', margin: 0 }}>{p.part_number}</p>
      </div>
      {/* Price + Add */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 'auto', paddingTop: '8px', borderTop: '1px solid #E8E0D0' }}>
        <div>
          <p style={{ color: '#0F1319', fontWeight: 800, fontSize: '1rem', margin: 0, fontFamily: 'DM Mono, monospace' }}>
            Rs {parseFloat(p.price).toLocaleString('en-IN')}
          </p>
          {p.original_price && (
            <p style={{ color: '#B0A890', fontSize: '0.72rem', textDecoration: 'line-through', margin: '1px 0 0', fontFamily: 'DM Mono, monospace' }}>
              Rs {parseFloat(p.original_price).toLocaleString('en-IN')}
            </p>
          )}
        </div>
        {p.in_stock ? (
          qty === 0 ? (
            <button onClick={onAdd} style={{
              background: '#0F1319', border: 'none',
              color: '#B8E36A', borderRadius: '6px',
              padding: '8px 18px', fontWeight: 700, fontSize: '0.82rem',
              cursor: 'pointer', fontFamily: 'DM Mono, monospace',
              letterSpacing: '0.08em', transition: 'background 150ms',
            }}>
              ADD
            </button>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', background: '#0F1319', borderRadius: '6px', padding: '6px 12px' }}>
              <button onClick={onRemove} style={{ background: 'none', border: 'none', color: '#B8E36A', fontWeight: 800, fontSize: '1.1rem', cursor: 'pointer', lineHeight: 1, padding: '0', fontFamily: 'DM Mono, monospace' }}>-</button>
              <span style={{ color: '#FAF8F4', fontWeight: 700, fontSize: '0.9rem', minWidth: '18px', textAlign: 'center', fontFamily: 'DM Mono, monospace' }}>{qty}</span>
              <button onClick={onAdd} style={{ background: 'none', border: 'none', color: '#B8E36A', fontWeight: 800, fontSize: '1.1rem', cursor: 'pointer', lineHeight: 1, padding: '0', fontFamily: 'DM Mono, monospace' }}>+</button>
            </div>
          )
        ) : (
          <button disabled style={{ background: '#E8E0D0', border: '1px solid #C8C0B0', color: '#8A8070', borderRadius: '6px', padding: '7px 14px', fontSize: '0.78rem', cursor: 'not-allowed', fontFamily: 'DM Mono, monospace', letterSpacing: '0.06em' }}>
            SOLD OUT
          </button>
        )}
      </div>
    </div>
  )
}
"""

before = lines[:799]  # 0-indexed line 799 = line 800
after  = lines[869:]  # 0-indexed line 869 = line 870 (after closing brace)

combined = before + [new_card + '\n'] + after
with open(path, 'w', encoding='utf-8') as f:
    f.writelines(combined)

print(f"Done. Total lines: {len(combined)}")
