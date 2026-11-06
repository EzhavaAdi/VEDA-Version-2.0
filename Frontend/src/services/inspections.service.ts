import { api } from './api'

export interface InspectionItem {
  id: string; component_name: string; component_code: string
  vehicle_system: string; observed_condition: string
  severity: string; mechanic_notes: string; updated_at: string
}

export interface SensorReading {
  id: string; parameter_name: string; parameter_value: string
  unit: string; component_code: string | null; notes: string; recorded_at: string
}

export interface Inspection {
  id: string; mechanic_phone: string; mechanic_name: string
  inspection_date: string; inspection_status: string
  general_observations: string
  items: InspectionItem[]; sensor_readings: SensorReading[]
  created_at: string; updated_at: string
}

export const inspectionsService = {
  get:           (orderId: string) => api.get<Inspection>(`/service-orders/${orderId}/inspection/`),
  start:         (orderId: string) => api.post<Inspection>(`/service-orders/${orderId}/inspection/`, {}),
  updateNotes:   (orderId: string, general_observations: string) =>
    api.patch<Inspection>(`/service-orders/${orderId}/inspection/`, { general_observations }),
  complete:      (orderId: string) => api.post<Inspection>(`/service-orders/${orderId}/inspection/complete/`, {}),
  addItem:       (orderId: string, data: object) =>
    api.post<InspectionItem>(`/service-orders/${orderId}/inspection/items/`, data),
  listItems:     (orderId: string) => api.get<InspectionItem[]>(`/service-orders/${orderId}/inspection/items/`),
  addReading:    (orderId: string, data: object) =>
    api.post<SensorReading>(`/service-orders/${orderId}/inspection/readings/`, data),
  listReadings:  (orderId: string) => api.get<SensorReading[]>(`/service-orders/${orderId}/inspection/readings/`),
}
