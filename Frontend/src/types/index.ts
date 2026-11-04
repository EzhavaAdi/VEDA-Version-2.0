/**
 * VEDA V2 — Shared TypeScript Types
 *
 * Phase 0: Core type stubs.
 * Full domain types (Vehicle, ServiceOrder, Diagnosis, etc.) added in Phase 1+.
 */

// ---------------------------------------------------------------------------
// API
// ---------------------------------------------------------------------------
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// ---------------------------------------------------------------------------
// User and Roles
// ---------------------------------------------------------------------------
export type UserRole = 'OWNER' | 'WORKSHOP_ADMIN' | 'MECHANIC' | 'VEDA_ADMIN'

export interface User {
  id: string
  phone_number: string
  full_name: string
  is_active: boolean
  created_at: string
}

export interface AuthUser extends User {
  roles: UserRole[]
}

// ---------------------------------------------------------------------------
// Component Visualization States
// ---------------------------------------------------------------------------
export type ComponentVisualState =
  | 'NORMAL'
  | 'SUSPECTED'
  | 'MECHANIC_VERIFIED'
  | 'REPAIRED'
  | 'UNMAPPED'

// ---------------------------------------------------------------------------
// Service Order States
// ---------------------------------------------------------------------------
export type ServiceOrderStatus =
  | 'REQUESTED'
  | 'ACCEPTED'
  | 'VEHICLE_RECEIVED'
  | 'INSPECTION_IN_PROGRESS'
  | 'AI_DIAGNOSIS'
  | 'ESTIMATE_READY'
  | 'AWAITING_OWNER_APPROVAL'
  | 'APPROVED'
  | 'PARTIALLY_APPROVED'
  | 'REPAIR_IN_PROGRESS'
  | 'FINAL_INSPECTION'
  | 'INVOICED'
  | 'PAYMENT_PENDING'
  | 'PAID'
  | 'VEHICLE_DELIVERED'
  | 'CANCELLED'
  | 'REJECTED'
  | 'ON_HOLD'
  | 'REVISION_REQUESTED'

// ---------------------------------------------------------------------------
// Estimate Approval States
// ---------------------------------------------------------------------------
export type ApprovalStatus =
  | 'PENDING'
  | 'APPROVED'
  | 'REJECTED'
  | 'CLARIFICATION_REQUESTED'

// ---------------------------------------------------------------------------
// Diagnostic Evidence Types
// ---------------------------------------------------------------------------
export type EvidenceType =
  | 'AI_PREDICTION'
  | 'MECHANIC_OBSERVATION'
  | 'SENSOR_READING'
  | 'DIAGNOSTIC_RULE'
  | 'EXTERNAL_REFERENCE'
