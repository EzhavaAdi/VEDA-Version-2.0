import { api } from './api'

export interface Payment {
  id: string; payment_provider: string; transaction_reference: string
  payment_status: string; amount: string; paid_at: string | null; created_at: string
}

export interface Invoice {
  id: string; invoice_number: string; subtotal: string
  tax_amount: string; total_amount: string
  invoice_status: string; notes: string
  generated_at: string; payments: Payment[]
}

export interface WorkOrderItem {
  id: string; component_code: string; component_name: string
  description: string; unit_price: string; labour_cost: string
  completion_status: string; mechanic_notes: string; completed_at: string | null
}

export interface WorkOrder {
  id: string; work_status: string
  started_at: string | null; completed_at: string | null
  items: WorkOrderItem[]; created_at: string
}

export const billingService = {
  getWorkOrder:  (orderId: string) => api.get<WorkOrder>(`/service-orders/${orderId}/work-order/`),
  createWorkOrder:(orderId: string) => api.post<WorkOrder>(`/service-orders/${orderId}/work-order/`, {}),
  updateItem:    (itemId: string, status: string, notes = '') =>
    api.patch<WorkOrderItem>(`/work-order-items/${itemId}/`, { status, notes }),
  completeWorkOrder: (woId: string) => api.post<WorkOrder>(`/work-orders/${woId}/complete/`, {}),

  getInvoice:    (orderId: string) => api.get<Invoice>(`/service-orders/${orderId}/invoice/`),
  generateInvoice:(orderId: string) => api.post<Invoice>(`/service-orders/${orderId}/invoice/`, {}),
  pay:           (invoiceId: string, transaction_reference?: string) =>
    api.post<Payment>(`/invoices/${invoiceId}/pay/`, { transaction_reference }),
  deliver:       (orderId: string) => api.post(`/service-orders/${orderId}/deliver/`, {}),
}
