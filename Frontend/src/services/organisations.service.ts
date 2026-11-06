import { api } from './api'

export interface ServiceCentre {
  id: string; name: string; address: string; city: string; state: string
  contact_number: string; email: string; verification_status: string
  is_active: boolean; registered_by_phone: string | null; created_at: string
}

export interface WorkshopMembership {
  id: string; user_phone: string; user_name: string
  centre_name: string; designation: string; is_active: boolean; joined_at: string
}

export const organisationsService = {
  listVerified: () => api.get<ServiceCentre[]>('/service-centres/'),
  mine:         () => api.get<ServiceCentre[]>('/service-centres/mine/'),
  get:          (id: string) => api.get<ServiceCentre>(`/service-centres/${id}/`),
  register:     (data: object) => api.post<ServiceCentre>('/service-centres/', data),
  members:      (id: string) => api.get<WorkshopMembership[]>(`/service-centres/${id}/members/`),
  addMember:    (id: string, phone_number: string, designation: string) =>
    api.post<WorkshopMembership>(`/service-centres/${id}/members/`, { phone_number, designation }),
}
