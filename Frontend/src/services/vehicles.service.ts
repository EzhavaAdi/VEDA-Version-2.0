import { api } from './api'

export interface Vehicle {
  id: string; owner_phone: string; registration_number: string
  manufacturer: string; model: string; vehicle_category: string
  manufacturing_year: number; odometer_reading: number
  operating_hours: number; is_active: boolean; notes: string; created_at: string
}

export const vehiclesService = {
  list:     ()          => api.get<Vehicle[]>('/vehicles/'),
  get:      (id: string) => api.get<Vehicle>(`/vehicles/${id}/`),
  register: (data: Partial<Vehicle>) => api.post<Vehicle>('/vehicles/', data),
  update:   (id: string, data: Partial<Vehicle>) => api.patch<Vehicle>(`/vehicles/${id}/`, data),
}
