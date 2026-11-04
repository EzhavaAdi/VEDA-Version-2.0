# VEDA V2 — System Architecture

**Version:** 2.0  
**Architecture:** Modular Monolith  
**Deployment:** Local-first  
**Status:** Initial Architecture Specification

# 1. Architecture Overview

VEDA V2 will use a modular monolithic architecture.

The platform consists of five major layers:

1. Frontend application.
2. Backend REST API.
3. Database and storage.
4. Integrated AI diagnostic engine.
5. Visualization and digital twin engine.

All modules communicate through clearly defined interfaces.

The architecture must remain modular so individual components can be improved or replaced without rewriting the entire application.

# 2. Technology Stack

## 2.1 Frontend

- React
- TypeScript
- Vite
- React Router
- Tailwind CSS or the established project CSS design system
- Lucide React
- Three.js
- React Three Fiber
- React Three Drei
- Recharts

Responsibilities:
- Public landing page.
- Owner dashboard.
- Service-centre dashboard.
- Mechanic workspace.
- Administrator dashboard.
- Vehicle management.
- Inspection forms.
- Diagnostic reports.
- Interactive 2D and 3D visualization.
- Spare-parts recommendations.
- Estimates and approvals.
- Payment interface.

## 2.2 Backend

- Python
- Django
- Django REST Framework

Responsibilities:
- Authentication.
- User and role management.
- Vehicle management.
- Service-centre management.
- Inspection records.
- AI inference orchestration.
- Diagnostic rule processing.
- Component catalogue.
- Inventory.
- Estimates and approvals.
- Repair tracking.
- Billing and payments.
- Notifications.
- Audit logs.

## 2.3 Database

Primary database: PostgreSQL.

PostgreSQL stores:
- Users.
- Vehicles.
- Service centres.
- Mechanics.
- Service orders.
- Inspection records.
- AI predictions.
- Diagnostic findings.
- Components.
- 3D asset metadata.
- Spare-parts inventory.
- Estimates.
- Approvals.
- Work orders.
- Invoices.
- Payments.
- Notifications.
- Audit records.

Use UUID identifiers for major business entities.

Use Decimal fields for financial values.

Use timezone-aware timestamps.

Use database transactions for inventory and payment-related operations.

## 2.4 AI Technologies

- Python
- pandas
- NumPy
- scikit-learn
- XGBoost
- PyTorch where justified
- Joblib for supported model serialization
- OpenCV where image processing is required

AI inference will initially be integrated into the Django backend through a dedicated AI package.

Do not create a separate microservice unless performance or deployment requirements justify it.

# 3. High-Level System Architecture

```text
              VEDA PLATFORM
                    |
       ---------------------------
       |            |            |
     OWNER       MECHANIC       ADMIN
       |            |            |
       -------- FRONTEND --------
                    |
              REST API
                    |
             DJANGO BACKEND
                    |
    -------------------------------------
    |       |       |       |           |
 ACCOUNTS VEHICLES SERVICE AI ENGINE INVENTORY
                  ORDERS
    |       |       |       |           |
    -------- POSTGRESQL DATABASE --------
                    |
           LOCAL FILE STORAGE
                    |
       ---------------------------
       |                         |
  2D DIAGRAMS                3D MODELS
       |                         |
       -------- VISUALIZATION -----
```

# 4. Frontend Architecture

Frontend directory:

```text
Frontend/
│
├── public/
│   ├── assets/
│   ├── images/
│   ├── models/
│   └── diagrams/
│
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── common/
│   │   ├── layout/
│   │   ├── dashboard/
│   │   ├── vehicles/
│   │   ├── diagnosis/
│   │   ├── inventory/
│   │   └── visualization/
│   │
│   ├── pages/
│   │   ├── landing/
│   │   ├── auth/
│   │   ├── owner/
│   │   ├── mechanic/
│   │   ├── workshop/
│   │   ├── admin/
│   │   └── diagnosis/
│   │
│   ├── features/
│   │   ├── authentication/
│   │   ├── vehicles/
│   │   ├── inspections/
│   │   ├── diagnosis/
│   │   ├── inventory/
│   │   ├── approvals/
│   │   └── payments/
│   │
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.service.ts
│   │   ├── vehicle.service.ts
│   │   └── diagnosis.service.ts
│   │
│   ├── hooks/
│   ├── types/
│   ├── utils/
│   ├── routes/
│   └── main.tsx
│
├── .env.example
├── package.json
└── vite.config.ts
```

This is the proposed target structure. Kiro must inspect and preserve existing frontend code before reorganizing it.

# 5. Backend Architecture

Backend directory:

```text
Backend/
│
├── config/
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
│
├── apps/
│   ├── accounts/
│   ├── organizations/
│   ├── vehicles/
│   ├── components/
│   ├── service_orders/
│   ├── inspections/
│   ├── diagnosis/
│   ├── digital_twin/
│   ├── inventory/
│   ├── estimates/
│   ├── work_orders/
│   ├── billing/
│   ├── notifications/
│   └── audit/
│
├── ai_engine/
│   ├── datasets/
│   ├── preprocessing/
│   ├── models/
│   ├── inference/
│   ├── diagnosis_rules/
│   ├── evaluation/
│   └── rul/
│
├── media/
├── requirements.txt
├── manage.py
└── .env.example
```

Each application must have a clear responsibility.

Avoid putting the entire business logic into Django views.

Use:
- Models for database representation.
- Serializers for validation.
- Views or ViewSets for API handling.
- Services for business logic.
- Permissions for access control.
- Tests for business rules.

# 6. Database Design

The database must support the complete service workflow.

## 6.1 Accounts and organizations

### User
- id
- phone_number
- full_name
- is_active
- created_at

### UserRole
- id
- user_id
- role

Supported roles:
- OWNER
- WORKSHOP_ADMIN
- MECHANIC
- VEDA_ADMIN

### ServiceCentre
- id
- name
- address
- contact_number
- verification_status
- created_at

### WorkshopMembership
- id
- user_id
- service_centre_id
- designation
- is_active

## 6.2 Vehicles

### Vehicle
- id
- owner_id
- registration_number
- manufacturer
- model
- vehicle_category
- manufacturing_year
- odometer_reading
- operating_hours
- created_at

### VehicleComponent
- id
- vehicle_id
- component_id
- installation_date
- current_status

## 6.3 Component catalogue

### Component
- id
- component_name
- component_code
- parent_component_id
- vehicle_system
- description
- maintenance_information

Examples:
- Engine
- Air compressor
- Air dryer
- Brake system
- Transmission
- Turbocharger
- Cooling system
- Suspension
- Electrical system

The catalogue must be hierarchical and extensible.

## 6.4 Service orders

### ServiceOrder
- id
- vehicle_id
- service_centre_id
- assigned_mechanic_id
- order_status
- service_description
- received_at
- completed_at
- created_at

### Inspection
- id
- service_order_id
- mechanic_id
- inspection_date
- general_observations
- inspection_status

### InspectionItem
- id
- inspection_id
- component_id
- observed_condition
- severity
- mechanic_notes

### SensorReading
- id
- inspection_id
- parameter_name
- parameter_value
- unit
- recorded_at

## 6.5 AI diagnosis

### AIModel
- id
- model_name
- model_version
- model_type
- dataset_reference
- artifact_location
- preprocessing_version
- active_status

### AIRun
- id
- service_order_id
- model_id
- execution_status
- input_reference
- started_at
- completed_at
- error_message

### AIPrediction
- id
- ai_run_id
- predicted_class
- probability
- prediction_metadata

### DiagnosisCase
- id
- service_order_id
- component_id
- diagnosis_status
- mechanic_verification
- final_notes

### DiagnosisEvidence
- id
- diagnosis_case_id
- evidence_type
- evidence_reference
- evidence_description
- source_timestamp

Evidence types:
- AI_PREDICTION
- MECHANIC_OBSERVATION
- SENSOR_READING
- DIAGNOSTIC_RULE
- EXTERNAL_REFERENCE

AI predictions and mechanic verification must be stored independently.

The database must preserve the original prediction even if the mechanic later rejects it.

# 7. Digital Twin and Visualization Database

### Asset3D
- id
- asset_name
- asset_format
- asset_path
- asset_source
- license_information
- attribution
- version

### ComponentMeshMapping
- id
- asset_id
- component_id
- mesh_name
- mesh_identifier

### Diagram2D
- id
- diagram_name
- diagram_path
- vehicle_system

### ComponentDiagramMapping
- id
- diagram_id
- component_id
- svg_element_id

Component visualization states:

- NORMAL
- SUSPECTED
- MECHANIC_VERIFIED
- REPAIRED
- UNMAPPED

If a component cannot be mapped accurately, show UNMAPPED instead of highlighting an incorrect part.

# 8. Spare Parts and Inventory

### PartCatalog
- id
- part_name
- part_number
- manufacturer
- description

### PartCompatibility
- id
- part_id
- component_id
- vehicle_manufacturer
- compatible_model
- compatibility_source
- verification_status

### WorkshopInventory
- id
- service_centre_id
- part_id
- quantity_available
- unit_price
- updated_at

### InventoryMovement
- id
- inventory_id
- movement_type
- quantity
- service_order_id
- reference
- created_at

Inventory operations must be transaction-safe.

# 9. Estimates and Approvals

### RepairEstimate
- id
- service_order_id
- revision_number
- labour_total
- parts_total
- grand_total
- estimate_status
- created_at

### EstimateItem
- id
- estimate_id
- component_id
- part_id
- description
- quantity
- unit_price
- labour_cost
- approval_status

Approval states:
- PENDING
- APPROVED
- REJECTED
- CLARIFICATION_REQUESTED

Owners must approve individual items.

Only approved items can enter the authorized repair workflow.

# 10. Repair and Billing

### WorkOrder
- id
- service_order_id
- work_status
- started_at
- completed_at

### WorkOrderItem
- id
- work_order_id
- estimate_item_id
- completion_status
- mechanic_notes

### Invoice
- id
- service_order_id
- invoice_number
- subtotal
- tax_amount
- total_amount
- invoice_status
- generated_at

### Payment
- id
- invoice_id
- payment_provider
- transaction_reference
- payment_status
- amount
- paid_at

Use Decimal for all financial fields.

Never treat a frontend payment-success message as verified payment.

# 11. Service Order State Machine

The backend must control service-order transitions.

```text
REQUESTED
    |
ACCEPTED
    |
VEHICLE_RECEIVED
    |
INSPECTION_IN_PROGRESS
    |
AI_DIAGNOSIS
    |
ESTIMATE_READY
    |
AWAITING_OWNER_APPROVAL
    |
APPROVED / PARTIALLY_APPROVED
    |
REPAIR_IN_PROGRESS
    |
FINAL_INSPECTION
    |
INVOICED
    |
PAYMENT_PENDING
    |
PAID
    |
VEHICLE_DELIVERED
```

Additional states:
- CANCELLED
- REJECTED
- ON_HOLD
- REVISION_REQUESTED

All state transitions must be validated on the backend.

# 12. AI Engine Architecture

The AI engine will initially run within the Django backend.

Internal pipeline:

```text
MECHANIC INSPECTION DATA
          |
     INPUT VALIDATION
          |
      PREPROCESSING
          |
    SCANIA APS MODEL
          |
    PREDICTIVE OUTPUT
          |
   DIAGNOSTIC RULE ENGINE
          |
   COMPONENT CANDIDATES
          |
  MECHANIC VERIFICATION
          |
   STRUCTURED DIAGNOSIS
```

## 12.1 Scania APS Model

Initial task:
APS-related failure classification.

The system must:
- Validate input schema.
- Preserve feature order.
- Apply training-time preprocessing.
- Load the correct model version.
- Generate predictions.
- Store inference metadata.
- Handle unsupported or missing inputs.

The model must not be represented as a complete truck diagnostic system.

## 12.2 Diagnostic Rule Engine

The rule engine combines available evidence to generate component-level candidates.

Inputs:
- AI predictions.
- Mechanic observations.
- Sensor readings.
- Component relationships.
- Validated diagnostic rules.

Outputs:
- Suspected component.
- Supporting evidence.
- Diagnostic status.
- Recommended next inspection.
- Compatible repair recommendations where validated.

Do not assign arbitrary confidence values or claim exact component faults without supporting evidence.

## 12.3 Remaining Useful Life

RUL is a separate model capability.

The APS binary failure classifier must not be used to calculate remaining useful life.

A separate validated degradation dataset and model are required.

# 13. API Architecture

Base API:

`/api/v1/`

Initial endpoint groups:

```text
/auth/
/owners/
/service-centres/
/vehicles/
/components/
/service-orders/
/inspections/
/diagnosis/
/digital-twin/
/parts/
/inventory/
/estimates/
/work-orders/
/invoices/
/payments/
/notifications/
/reports/
```

All endpoints must use serializers, permissions and backend validation.

Provide API documentation using OpenAPI/Swagger.

# 14. File Storage

During local development:

- Uploaded documents: local media directory.
- Vehicle photographs: local media directory.
- 3D models: controlled public asset directory or protected media storage as appropriate.
- 2D diagrams: controlled asset directory.
- AI models: backend model-artifact directory.

Do not store large model binaries or datasets inside PostgreSQL.

Keep private datasets and model artifacts out of normal Git commits.

# 15. Authentication and Security

- Phone-number-based OTP.
- Hashed OTP storage.
- OTP expiry.
- Verification attempt limits.
- Rate limiting.
- Role-based authorization.
- Object-level permissions.
- Secure API access.
- Environment-based secrets.
- CORS restrictions.
- Audit logging.

Development OTP bypass must never be enabled in production.

Owners must access only their own vehicle records.

Workshop users must access only records belonging to their authorized service centre.

Mechanics must access only permitted assigned jobs.

# 16. Environment Architecture

The project must support a reproducible local development environment.

Backend:
- Python virtual environment named `.venv`.
- Django dependencies.
- PostgreSQL connection.
- Environment variables from `.env`.

Frontend:
- Node.js dependencies.
- Vite development server.
- API base URL configured through a public frontend environment variable.

Create:
- `.env.example`
- `.gitignore`
- `requirements.txt`
- `package.json`
- `README.md`

Never commit `.env`, private credentials or API keys.

Never expose backend secrets through Vite environment variables.

# 17. GitHub and Checkpoint Architecture

Git is mandatory from the beginning.

Each major phase must produce:
1. Working implementation.
2. Passing relevant tests.
3. Reviewed Git changes.
4. Commit.
5. Annotated Git tag.
6. Updated CHECKPOINTS.md.
7. GitHub push after remote and authentication are configured.

Suggested tags:

- v2.0.0-foundation
- v2.0.1-auth
- v2.0.2-vehicles-centres
- v2.0.3-inspection-workflow
- v2.0.4-aps-diagnosis
- v2.0.5-digital-twin
- v2.0.6-inventory-approvals
- v2.0.7-repair-billing
- v2.0.8-mvp

Never force-push or discard uncommitted work without explicit approval.

# 18. Performance and Reliability

- Use pagination for large API lists.
- Add database indexes to frequently queried fields.
- Avoid unnecessary frontend API requests.
- Cache only where useful and safe.
- Keep AI inference isolated from normal request processing.
- Add asynchronous background execution if inference becomes slow.
- Manual mechanic workflows must remain available when AI is unavailable.
- Log errors without exposing sensitive information.

# 19. Architecture Principles

1. Modular monolith before microservices.
2. Backend is the source of truth.
3. Database integrity is mandatory.
4. AI output is evidence, not unquestionable truth.
5. Mechanic verification is a separate business event.
6. Component visualization must be based on actual asset mappings.
7. Inventory and payment operations must be auditable.
8. All critical actions must be permission-controlled.
9. Every implementation phase must have a recoverable Git checkpoint.
10. Architecture must allow future expansion to additional truck manufacturers and diagnostic models.