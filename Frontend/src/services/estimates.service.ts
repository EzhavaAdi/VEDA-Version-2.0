import { api } from './api'

export interface EstimateItem {
  id: string; component_code: string; component_name: string
  part_name: string | null; part_number: string | null
  description: string; quantity: number
  unit_price: string; labour_cost: string; line_total: string
  approval_status: string; clarification_note: string; owner_decision_at: string | null
}

export interface Estimate {
  id: string; revision_number: number; estimate_status: string
  labour_total: string; parts_total: string; grand_total: string
  notes: string; created_by_phone: string | null
  items: EstimateItem[]; created_at: string
}

export const estimatesService = {
  list:       (orderId: string) => api.get<Estimate[]>(`/service-orders/${orderId}/estimates/`),
  get:        (id: string)      => api.get<Estimate>(`/estimates/${id}/`),
  create:     (orderId: string, notes = '') =>
                                   api.post<Estimate>(`/service-orders/${orderId}/estimates/`, { notes }),
  addItem:    (estimateId: string, data: object) =>
                                   api.post<EstimateItem>(`/estimates/${estimateId}/items/`, data),
  submit:     (estimateId: string) => api.post<Estimate>(`/estimates/${estimateId}/submit/`, {}),
  decideItem: (itemId: string, decision: string, note = '') =>
                                   api.post<EstimateItem>(`/estimate-items/${itemId}/decide/`, { decision, note }),
}
