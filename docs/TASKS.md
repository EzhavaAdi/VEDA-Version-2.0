# VEDA V2 — Development Roadmap and Task Management

**Version:** 2.0  
**Development Environment:** Local  
**IDE:** Kiro  
**Methodology:** Incremental, milestone-based development

# 1. Development Philosophy

VEDA V2 must be developed incrementally.

Kiro must not attempt to build the complete application in one execution.

Every phase must:
1. Have clearly defined objectives.
2. Have identified dependencies.
3. Be implemented independently where possible.
4. Include relevant tests.
5. Pass build and validation checks.
6. Be documented.
7. Receive a Git checkpoint.
8. Be approved before major subsequent phases.

Tasks must only be marked complete after implementation and verification.

# 2. Phase 0 — Project Foundation

## Objectives

Establish the development environment and repository structure.

## Tasks

- [ ] Inspect the existing repository.
- [ ] Inspect existing frontend starter code.
- [ ] Initialize Git if required.
- [ ] Create `.gitignore`.
- [ ] Create root documentation structure.
- [ ] Create Python `.venv`.
- [ ] Create `.env.example`.
- [ ] Create local `.env` without overwriting existing values.
- [ ] Configure Django settings.
- [ ] Configure PostgreSQL.
- [ ] Install backend dependencies.
- [ ] Install frontend dependencies.
- [ ] Verify React and Vite.
- [ ] Verify Django startup.
- [ ] Verify PostgreSQL connection.
- [ ] Create README with setup instructions.
- [ ] Create CHECKPOINTS.md.
- [ ] Configure GitHub remote after receiving confirmation and repository URL.
- [ ] Create initial Git checkpoint.

## Completion Criteria

Frontend and backend must start locally.

Environment configuration must work.

Secrets must be excluded from Git.

Git checkpoint must be created.

**Checkpoint:** `v2.0.0-foundation`

# 3. Phase 1 — Backend Foundation and Authentication

## Objectives

Build the core backend and secure user authentication.

## Tasks

- [ ] Create Django project structure.
- [ ] Configure Django REST Framework.
- [ ] Configure PostgreSQL.
- [ ] Create custom User model.
- [ ] Implement phone-number authentication.
- [ ] Implement OTP generation.
- [ ] Implement OTP verification.
- [ ] Implement OTP expiry.
- [ ] Implement OTP hashing.
- [ ] Implement verification attempt limits.
- [ ] Implement development-only console OTP.
- [ ] Create role management.
- [ ] Implement OWNER role.
- [ ] Implement WORKSHOP_ADMIN role.
- [ ] Implement MECHANIC role.
- [ ] Implement VEDA_ADMIN role.
- [ ] Implement authentication permissions.
- [ ] Implement protected API endpoints.
- [ ] Write authentication tests.
- [ ] Write role-permission tests.

## Completion Criteria

Users must be able to authenticate using phone number and OTP.

Backend permissions must enforce role restrictions.

**Checkpoint:** `v2.0.1-auth`

# 4. Phase 2 — Service Centres and Vehicle Management

## Objectives

Implement the relationship between vehicle owners and registered service centres.

## Tasks

- [ ] Implement service-centre model.
- [ ] Implement service-centre registration.
- [ ] Implement centre verification status.
- [ ] Implement workshop membership.
- [ ] Implement mechanic management.
- [ ] Implement owner vehicle registration.
- [ ] Implement vehicle editing.
- [ ] Implement vehicle identification.
- [ ] Implement manufacturer and model fields.
- [ ] Implement vehicle-system catalogue.
- [ ] Implement component catalogue.
- [ ] Implement vehicle-component association.
- [ ] Implement service-centre search.
- [ ] Implement vehicle listing.
- [ ] Implement owner data isolation.
- [ ] Write relevant tests.

## Completion Criteria

An owner can register vehicles.

A service centre can manage its authorized mechanics.

Owners can access only their own vehicle records.

**Checkpoint:** `v2.0.2-vehicles-centres`

# 5. Phase 3 — Service Orders and Mechanic Inspection

## Objectives

Implement the core service workflow.

## Tasks

- [ ] Create service-order model.
- [ ] Implement service request creation.
- [ ] Implement service-centre acceptance.
- [ ] Implement vehicle-received status.
- [ ] Implement mechanic assignment.
- [ ] Implement service-order lifecycle.
- [ ] Implement mechanic inspection interface.
- [ ] Implement component inspection checklist.
- [ ] Implement manual observation entry.
- [ ] Implement symptom recording.
- [ ] Implement numeric measurement entry.
- [ ] Implement measurement units.
- [ ] Implement mechanic notes.
- [ ] Implement inspection evidence attachments.
- [ ] Implement inspection completion.
- [ ] Implement inspection history.
- [ ] Implement service tracking.
- [ ] Write state-transition tests.
- [ ] Write access-control tests.

## Completion Criteria

An owner can submit a service request.

A service centre can accept it and assign a mechanic.

A mechanic can complete and save an inspection.

**Checkpoint:** `v2.0.3-inspection-workflow`

# 6. Phase 4 — AI Diagnostic Engine

## Objectives

Integrate the Scania APS predictive model into VEDA.

This is a critical technical phase.

## Tasks

### Dataset Preparation

- [ ] Confirm dataset source and usage terms.
- [ ] Obtain the complete Scania APS Failure dataset.
- [ ] Inspect dataset structure.
- [ ] Inspect feature definitions.
- [ ] Inspect missing values.
- [ ] Analyze class imbalance.
- [ ] Define training and validation strategy.
- [ ] Prevent data leakage.
- [ ] Document preprocessing.

### Model Development

- [ ] Implement preprocessing pipeline.
- [ ] Train or integrate the selected APS classifier.
- [ ] Evaluate model performance.
- [ ] Generate confusion matrix.
- [ ] Calculate precision.
- [ ] Calculate recall.
- [ ] Calculate F1-score.
- [ ] Calculate ROC-AUC where appropriate.
- [ ] Record model execution time.
- [ ] Record model artifact size.
- [ ] Save model artifact.
- [ ] Save preprocessing configuration.
- [ ] Document model limitations.

### Backend Integration

- [ ] Create AI model registry.
- [ ] Create AI execution records.
- [ ] Implement inference service.
- [ ] Validate input schema.
- [ ] Validate feature ordering.
- [ ] Implement model loading.
- [ ] Implement prediction API.
- [ ] Store prediction output.
- [ ] Store model version.
- [ ] Store execution metadata.
- [ ] Implement AI error handling.

### Diagnostic Reasoning

- [ ] Implement diagnostic evidence aggregation.
- [ ] Implement initial validated diagnostic rules.
- [ ] Separate AI predictions from mechanic observations.
- [ ] Generate component candidates only when supported by evidence.
- [ ] Allow mechanic verification.
- [ ] Allow mechanic rejection.
- [ ] Support insufficient-data status.

### Important Limitation

The Scania APS dataset supports APS failure classification.

It does not independently identify every faulty truck component.

Do not present the model as a universal vehicle diagnosis system.

Do not calculate remaining useful life using this binary classifier.

## Completion Criteria

The supported APS input must generate a reproducible prediction.

Predictions must be traceable to the model version and input.

The mechanic must be able to verify or reject diagnostic findings.

**Checkpoint:** `v2.0.4-aps-diagnosis`

# 7. Phase 5 — Digital Twin and Vehicle Visualization

## Objectives

Develop VEDA's signature interactive vehicle visualization feature.

## Tasks

### Asset Preparation

- [ ] Find legally usable generic heavy-truck 3D models.
- [ ] Verify asset licensing.
- [ ] Download suitable GLB/GLTF assets.
- [ ] Inspect mesh hierarchy.
- [ ] Identify component meshes.
- [ ] Separate components where technically and legally permitted.
- [ ] Record asset attribution.
- [ ] Find suitable 2D technical diagrams.
- [ ] Verify diagram licensing.
- [ ] Define shared component identifiers.

### 3D Development

- [ ] Integrate Three.js.
- [ ] Integrate React Three Fiber.
- [ ] Implement GLB/GLTF loading.
- [ ] Implement truck viewer.
- [ ] Implement camera rotation.
- [ ] Implement zoom.
- [ ] Implement camera reset.
- [ ] Implement component selection.
- [ ] Implement mesh highlighting.
- [ ] Implement component information panel.
- [ ] Implement visual status states.

### 2D Development

- [ ] Implement SVG diagram viewer.
- [ ] Implement component selection.
- [ ] Implement component highlighting.
- [ ] Implement diagram labels.
- [ ] Implement status legend.

### Synchronization

- [ ] Synchronize 2D component selection with 3D where mappings exist.
- [ ] Synchronize diagnostic status.
- [ ] Implement unmapped-component handling.
- [ ] Test component selection accuracy.

## Completion Criteria

A supported vehicle model must load successfully.

Mapped components must be selectable and accurately highlighted.

2D and 3D views must remain synchronized where both mappings exist.

**Checkpoint:** `v2.0.5-digital-twin`

# 8. Phase 6 — Inventory, Spare Parts and Owner Approvals

## Objectives

Connect mechanic recommendations with service-centre inventory and owner decisions.

## Tasks

### Spare Parts

- [ ] Create part catalogue.
- [ ] Implement part numbers.
- [ ] Implement part descriptions.
- [ ] Implement component compatibility.
- [ ] Implement compatibility evidence.
- [ ] Implement part photographs.
- [ ] Implement workshop inventory.
- [ ] Implement stock quantities.
- [ ] Implement workshop-specific pricing.
- [ ] Implement inventory movements.
- [ ] Implement stock reservation.

### Estimates

- [ ] Implement repair estimates.
- [ ] Implement estimate items.
- [ ] Implement labour costs.
- [ ] Implement spare-part costs.
- [ ] Implement quantity calculations.
- [ ] Implement estimate totals.
- [ ] Implement estimate revisions.
- [ ] Implement estimated completion duration.

### Owner Approval

- [ ] Implement individual item approval.
- [ ] Implement individual item rejection.
- [ ] Implement clarification requests.
- [ ] Record owner decisions.
- [ ] Prevent unauthorized repairs.
- [ ] Convert approved items into work-order items.

### Inventory Integrity

- [ ] Implement transaction-safe stock operations.
- [ ] Prevent invalid stock deductions.
- [ ] Maintain inventory audit history.
- [ ] Test concurrent inventory operations.

## Completion Criteria

The mechanic can recommend compatible parts from recorded inventory.

The owner can approve or reject individual items.

Only approved items can proceed to repair.

**Checkpoint:** `v2.0.6-inventory-approvals`

# 9. Phase 7 — Repair Tracking, Invoices and Payments

## Objectives

Complete the servicing and payment workflow.

## Tasks

- [ ] Implement work-order creation.
- [ ] Implement approved repair items.
- [ ] Implement repair status.
- [ ] Implement mechanic progress updates.
- [ ] Implement completion evidence.
- [ ] Implement final inspection.
- [ ] Implement invoice generation.
- [ ] Implement invoice itemization.
- [ ] Implement tax configuration where applicable.
- [ ] Implement payment records.
- [ ] Implement local mock payment provider.
- [ ] Implement payment status.
- [ ] Implement payment idempotency.
- [ ] Implement payment failure handling.
- [ ] Implement service completion.
- [ ] Implement vehicle delivery.
- [ ] Implement service history.

## Completion Criteria

The complete service journey must work using local mock payments.

A service order can be closed only after its required workflow conditions are met.

**Checkpoint:** `v2.0.7-repair-billing`

# 10. Phase 8 — Dashboards and Notifications

## Objectives

Complete the role-specific frontend experiences.

## Owner Dashboard

- [ ] Overview.
- [ ] Vehicle cards.
- [ ] Service requests.
- [ ] Diagnosis reports.
- [ ] Approval centre.
- [ ] Repair tracking.
- [ ] Invoices.
- [ ] Service history.

## Mechanic Dashboard

- [ ] Assigned vehicles.
- [ ] Inspection queue.
- [ ] Inspection workspace.
- [ ] AI diagnosis.
- [ ] Component visualization.
- [ ] Estimates.
- [ ] Repair progress.

## Service Centre Dashboard

- [ ] Workshop overview.
- [ ] Customer management.
- [ ] Vehicle queue.
- [ ] Mechanic management.
- [ ] Inventory.
- [ ] Estimates.
- [ ] Invoices.
- [ ] Reports.

## Administrator Dashboard

- [ ] User management.
- [ ] Service-centre verification.
- [ ] Platform overview.
- [ ] Model registry.
- [ ] Audit records.
- [ ] System monitoring.

## Notifications

- [ ] Service request notifications.
- [ ] Inspection notifications.
- [ ] Diagnosis notifications.
- [ ] Estimate notifications.
- [ ] Approval notifications.
- [ ] Repair progress notifications.
- [ ] Invoice notifications.

## Completion Criteria

All role-specific dashboards must display real backend data.

No fake demo values may be presented as actual business records.

**Checkpoint:** `v2.0.8-dashboards`

# 11. Phase 9 — Testing, Security and MVP Release

## Objectives

Prepare the platform for a complete local demonstration.

## Tasks

- [ ] Run backend test suite.
- [ ] Run frontend tests.
- [ ] Run TypeScript checks.
- [ ] Run production frontend build.
- [ ] Test complete owner workflow.
- [ ] Test complete mechanic workflow.
- [ ] Test complete service-centre workflow.
- [ ] Test administrator permissions.
- [ ] Test AI inference.
- [ ] Test component mapping.
- [ ] Test inventory consistency.
- [ ] Test approval workflow.
- [ ] Test payment workflow.
- [ ] Test responsive layouts.
- [ ] Test accessibility.
- [ ] Review authentication security.
- [ ] Review authorization.
- [ ] Review environment configuration.
- [ ] Review dependency vulnerabilities.
- [ ] Review audit logging.
- [ ] Update README.
- [ ] Update architecture documentation.
- [ ] Prepare demonstration data.
- [ ] Prepare final demonstration instructions.

## Completion Criteria

The complete VEDA service journey must work locally.

No critical authorization, data-integrity or workflow defects may remain.

**Checkpoint:** `v2.0.9-mvp-release`

# 12. Development Execution Rules

Kiro must follow these rules throughout implementation:

1. Implement only the current approved phase.
2. Never mark unimplemented functionality complete.
3. Never replace working code unnecessarily.
4. Never use fabricated data as real AI output.
5. Never skip tests to save time.
6. Never proceed silently after a failed build.
7. Never skip a required Git checkpoint.
8. Never overwrite existing environment files.
9. Never push without confirming the configured remote and successful authentication.
10. Never force-push.
11. Ask for approval before major architectural changes.
12. Update documentation after meaningful changes.

# 13. Phase Completion Report

At the end of every phase, provide:

- Phase name.
- Tasks completed.
- Files created.
- Files modified.
- Dependencies installed.
- Tests executed.
- Test results.
- Build results.
- Known issues.
- Remaining tasks.
- Git commit hash.
- Git tag.
- GitHub push status.
- Rollback instructions.

Do not claim a phase is complete if acceptance criteria are not satisfied.

# 14. Development Priority

Priority order:

1. Reliable foundation.
2. Secure authentication.
3. Owner and service-centre workflows.
4. Mechanic inspection.
5. AI integration.
6. Digital twin.
7. Inventory and approvals.
8. Repair and payment.
9. Dashboards and notifications.
10. Quality assurance.

# 15. Final Roadmap Principle

VEDA must be built as a complete and reliable vehicle-service ecosystem.

Each phase must create a stable foundation for the next.

**A working, tested and recoverable implementation is more valuable than a large unfinished codebase.**