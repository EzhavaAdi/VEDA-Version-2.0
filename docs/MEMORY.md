# VEDA V2 — Project Memory

## 1. Project Identity

**Project:** VEDA V2  
**Full Form:** Vehicle Evaluation Diagnostic Agents  
**Purpose:** An AI-assisted heavy-vehicle inspection, diagnosis, repair estimation, and service management platform.

VEDA connects heavy-vehicle owners with registered service centres. It combines AI-generated diagnostic evidence with mechanic inspections to support transparent repair decisions.

## 2. Locked Product Decisions

- Target vehicles: Heavy vehicles and logistics trucks.
- Service providers: Registered service centres and their onboarded mechanics.
- Owners can register vehicles and track service requests.
- Mechanics manually enter inspection findings.
- AI predictions and mechanic findings must remain separate evidence sources.
- Diagnosis should identify suspected components only when supported by available evidence.
- The platform must not claim certainty beyond model capabilities.
- Both 2D technical diagrams and 3D vehicle visualisation are required.
- Spare parts must come from the selected service centre's inventory.
- Estimates must be itemised.
- Owners can approve or reject individual estimate items.
- Repairs must follow the owner's approvals.
- Service centres complete repairs and final inspection.
- Invoices and payment records are maintained through the platform.

## 3. Technology Stack

### Frontend
- React
- TypeScript
- Vite
- React Router
- Tailwind CSS or an organised custom CSS design system
- Three.js
- React Three Fiber
- Drei
- Recharts
- Lucide icons

### Backend
- Python
- Django
- Django REST Framework
- Modular monolithic architecture

### Database
- PostgreSQL

### AI
- Python
- pandas
- NumPy
- scikit-learn
- XGBoost
- PyTorch when justified
- Joblib for suitable model persistence

### Development
- Local development first
- Git and GitHub for version control
- Python virtual environment
- `.env` for local secrets
- `.env.example` for environment documentation

## 4. AI Scope and Restrictions

### Scania APS Failure Dataset

The Scania APS Failure dataset is the initial AI proof-of-concept dataset.

Important limitations:

- It concerns APS-related failure classification.
- It does not represent every heavy-vehicle component or failure type.
- It does not independently establish an exact faulty component.
- It does not provide a validated Remaining Useful Life prediction.
- It must not be presented as a universal truck-diagnostics model.

### AI Evidence Rules

- Preserve model predictions and mechanic findings separately.
- Do not use mechanic verification as an input to the same pre-inspection prediction.
- Avoid data leakage.
- Record model version, prediction, confidence where meaningful, and supporting evidence.
- Provide an insufficient-data outcome when evidence is inadequate.
- Never fabricate model accuracy or diagnostic certainty.

### Remaining Useful Life

RUL functionality is conditional.

Only implement RUL predictions when a suitable degradation/time-series dataset and a validated RUL model are available. Otherwise, display that there is insufficient data for an RUL estimate.

## 5. Digital Twin and Visualisation

- Support 2D technical diagrams and 3D truck visualisation.
- Prefer a generic heavy-truck model initially.
- Verify the model's licence before use.
- Inspect the GLB/GLTF/FBX model hierarchy before implementing component highlighting.
- Map visible meshes to a controlled VEDA component catalogue.
- Never assume that a 3D model contains independently selectable components.
- Keep the component catalogue independent of any one 3D asset.
- Show clear visual indicators for suspected components and their evidence status.

## 6. Service Centre and Inventory Rules

- Mechanics belong to registered service centres.
- Service centres manage their own inventory.
- Parts recommendations must be based on available inventory.
- Compatibility must be supported by recorded vehicle/component information.
- Do not invent stock quantities, prices, or compatibility.
- Estimates must show parts, labour, quantities, and applicable charges separately.
- Owners must approve or reject individual estimate lines.
- Only approved work may proceed.

## 7. Authentication and Payments

### Authentication
- Phone number and OTP authentication.
- OTP must expire.
- OTP storage must be secure.
- Apply rate limiting and verification protections.
- Enforce role-based permissions.

### Payments
- Use a mock payment provider during local development.
- Never treat a frontend success message as proof of payment.
- Production payments require a suitable compliant payment provider.
- Verify payment callbacks and transaction status on the backend.
- Never store sensitive payment credentials directly.

## 8. Design Direction

VEDA should have a premium, modern, industrial automotive identity.

### Core colours
- Carbon Black: `#10110F`
- Graphite: `#1A1D18`
- Warm White: `#F4F4F0`
- Industrial Lime: `#B8E36A`

Use amber, red, and blue for meaningful status indicators.

### Design principles
- Premium minimalist interface.
- Strong typography and generous spacing.
- Clear data hierarchy.
- Cinematic automotive imagery where appropriate.
- Functional dashboards rather than decorative dashboards.
- Consistent owner, mechanic, and service-centre experiences.
- Responsive and accessible components.

Refer to `DESIGN.md` for the complete design specification.

## 9. Development and Repository Rules

- Inspect the existing repository before changing files.
- Preserve existing user work.
- Never overwrite an existing `.env`.
- Never commit secrets, private datasets, or credentials.
- Never force-push.
- Never perform destructive Git operations without approval.
- Use meaningful commits and annotated phase tags.
- Maintain `CHECKPOINTS.md`.
- Run relevant tests before marking a phase complete.
- Update documentation whenever architecture or product decisions change.

## 10. Project Documentation

The following files are the primary project references:

- `PRD.md` — Product requirements and scope.
- `ARCHITECTURE.md` — System architecture and technical structure.
- `RULES.md` — Mandatory development rules.
- `DESIGN.md` — Visual identity and UI/UX direction.
- `TASKS.md` — Development phases and task checklist.
- `MEMORY.md` — Persistent project context and locked decisions.

If two documents appear inconsistent, do not silently invent a decision. Identify the conflict and ask for clarification.

## 11. Current Development Status

**Documentation preparation:** In progress.

The six core documentation files are being prepared before the first Kiro implementation prompt.

No application feature should be considered implemented merely because it appears in a documentation file.

After documentation is complete:

1. Review all six files for consistency.
2. Prepare `FIRST_PROMPT_FOR_KIRO.md`.
3. Ask Kiro to inspect the existing workspace.
4. Establish the local development environment.
5. Set up Git checkpoints.
6. Complete Phase 0 before proceeding to Phase 1.

## 12. Future Enhancements

Potential future features include:

- YouTube repair and component explanation recommendations.
- Advanced AI diagnosis across additional vehicle systems.
- Validated RUL prediction.
- More detailed component-level digital twins.
- Service-centre analytics.
- Notifications and repair progress tracking.
- Production payment gateway integration.
- Cloud deployment and scalable AI inference.

These are future enhancements, not automatically part of the initial MVP.

## 13. Most Important Principle

**VEDA must be evidence-driven, transparent, and safe.**

AI should assist mechanics and vehicle owners, not replace professional inspection or make unsupported claims. Every diagnosis, recommendation, estimate, approval, and repair action must be traceable.
