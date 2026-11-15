const API = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

export interface ShopProduct {
  id: string; name: string; brand: string; description: string
  part_number: string; price: string; original_price: string | null
  discount_percent: number; stock: number; in_stock: boolean
  unit: string; image_emoji: string; image_path: string
  compatible_with: string; category_name: string; category_icon: string
}

export interface ShopCategory {
  id: string; name: string; slug: string; icon: string
  products: ShopProduct[]
}

export const shopService = {
  list: (component?: string): Promise<ShopCategory[]> => {
    const url = component
      ? `${API}/shop/?component=${encodeURIComponent(component)}`
      : `${API}/shop/`
    return fetch(url).then(r => r.json())
  },

  logCart: (product_id: string, quantity: number, session_id: string) => {
    return fetch(`${API}/shop/cart/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id, quantity, session_id }),
    }).catch(() => {}) // silent
  },
}
