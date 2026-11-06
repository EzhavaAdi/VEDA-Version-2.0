import { api } from './api'

export interface ServiceOrder {
  id: string; vehicle_reg: string; vehicle_make: string
  centre_name: string; owner_phone: string
  mechanic_phone: string | null; mechanic_name: string | null
  status: string; service_description: string
  rejection_reason: string; received_at: string | null
  completed_at: string | null; created_at: string
}

export interface ServiceOrderEvent {
  id: string; from_status: string; to_status: string
  triggered_by_phone: string | null; notes: string; created_at: string
}

export const serviceOrdersService = {
  listOwner:    ()            => api.get<ServiceOrder[]>('/service-orders/'),
  get:          (id: string)  => api.get<ServiceOrder>(`/service-orders/${id}/`),
  create:       (data: { vehicle_id: string; service_centre_id: string; service_description: string }) =>
                               api.post<ServiceOrder>('/service-orders/', data),
  transition:   (id: string, status: string, notes = '') =>
                               api.post<ServiceOrder>(`/service-orders/${id}/transition/`, { status, notes }),
  assignMechanic: (id: string, mechanic_id: string) =>
                               api.post<ServiceOrder>(`/service-orders/${id}/assign-mechanic/`, { mechanic_id }),
  events:       (id: string)  => api.get<ServiceOrderEvent[]>(`/service-orders/${id}/events/`),

  listForCentre:  (centreId: string) =>
                               api.get<ServiceOrder[]>(`/service-centres/${centreId}/orders/`),
  listForMechanic: ()          => api.get<ServiceOrder[]>('/service-orders/mechanic/'),
}
