# VEDA V2
### Vehicle Evaluation Diagnostic Agents

**An AI-assisted heavy vehicle inspection, diagnostics and service management platform.**

VEDA V2 aims to connect heavy vehicle owners with registered service centres through an intelligent platform that combines AI-assisted diagnostics, mechanic inspections, interactive vehicle visualisation, spare-parts recommendations and transparent repair management.

---

## 1. Project Overview

Heavy commercial vehicles require regular inspection and maintenance. Identifying potential faults, communicating inspection findings, sourcing compatible spare parts and managing repair approvals can be fragmented across different service providers.

VEDA V2 aims to bring these activities into one integrated platform.

The platform combines:

- AI-assisted failure prediction.
- Manual mechanic inspection and verification.
- Component-level diagnostic evidence.
- Interactive 2D and 3D vehicle visualisation.
- Service-centre spare-parts inventory.
- Transparent repair estimates.
- Owner-controlled repair approvals.
- Service history and repair tracking.

VEDA is designed as a decision-support platform. It does not replace professional mechanical inspection.

## 2. Core Users

### Vehicle Owners
- Register and manage vehicles.
- Submit service requests.
- View inspection findings.
- Review diagnostic evidence.
- Explore suspected components.
- Review repair estimates.
- Approve or reject individual repair items.
- Track repair progress and invoices.

### Service Centres
- Register and manage their service centre.
- Manage mechanics and inventory.
- Receive service requests.
- Prepare estimates.
- Track repair operations.
- Maintain service records.

### Mechanics
- Inspect assigned vehicles.
- Enter inspection findings.
- Record suspected faults.
- Review AI-generated evidence.
- Recommend repairs and spare parts.
- Update repair progress.
- Complete final inspection records.

### Administrators
- Manage users and service centres.
- Monitor platform activity.
- Maintain component catalogues.
- Review system operations and reports.

## 3. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Vite |
| UI | Tailwind CSS / Custom CSS |
| Routing | React Router |
| 3D Visualisation | Three.js, React Three Fiber, Drei |
| Charts | Recharts |
| Backend | Python, Django, Django REST Framework |
| Database | PostgreSQL |
| AI/ML | Python, pandas, NumPy, scikit-learn, XGBoost, PyTorch where required |
| Model Persistence | Joblib where appropriate |
| Version Control | Git and GitHub |

The architecture is modular so additional AI models and vehicle systems can be integrated progressively.

## 4. Diagnostic Workflow

```text
Vehicle Owner
     |
     v
Service Request
     |
     v
Registered Service Centre
     |
     v
Mechanic Inspection
     |
     +-------------------+
     |                   |
     v                   v
Manual Findings     AI Predictions
     |                   |
     +---------+---------+
               |
               v
     Diagnostic Evidence
               |
               v
     Suspected Components
               |
               v
    Spare Parts & Estimate
               |
               v
      Owner Approval
               |
               v
       Repair Process
               |
               v
    Final Inspection
               |
               v
      Invoice & Payment
```

AI predictions and mechanic findings are maintained as separate evidence sources.

## 5. AI Scope

### Initial AI Proof of Concept

The Scania APS Failure dataset will be used for the initial APS-related failure classification task.

Important limitations:

- APS failure classification is not universal vehicle diagnosis.
- Predictions do not independently prove an exact component failure.
- Mechanic inspection and additional evidence are required.
- Remaining Useful Life (RUL) will only be implemented when an appropriate dataset and validated model are available.

Future versions may incorporate additional vehicle fault datasets and diagnostic models.

## 6. 3D Vehicle Visualisation

VEDA includes an interactive vehicle visualisation layer.

Initial asset collection:

| Asset | File |
|---|---|
| Main truck candidate | `Kenwood.max` |
| Refuse collection truck | `refuse-collection-truck.glb` |
| Trailer | `truck-trailer.glb` |
| Engine candidate | `engine.max` |
| Brake component | `caliper.obj` |

These assets are initial candidates, not verified engineering models. Their licences, mesh structures, conversion compatibility and performance must be checked before production use.

Future versions may include more detailed chassis, suspension, drivetrain and component assemblies.

## 7. Project Structure

```text
VEDA-V2/
│
├── Backend/
│
├── Frontend/
│
├── 3-D model/
│   ├── caliper.obj
│   ├── engine.max
│   ├── Kenwood.max
│   ├── refuse-collection-truck.glb
│   └── truck-trailer.glb
│
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── RULES.md
│   ├── DESIGN.md
│   ├── TASKS.md
│   └── MEMORY.md
│
├── Steering/
│
├── CHECKPOINTS_TEMPLATE.md
├── FIRST_PROMPT_FOR_KIRO.md
└── README.md
```

Additional folders for datasets, processed models, images and diagrams may be introduced as development progresses.

## 8. Development Setup

Development will initially run locally.

### Prerequisites

- Python
- Node.js and npm
- PostgreSQL
- Git
- A code editor such as Kiro

### Backend

The backend will use a dedicated Python virtual environment.

```bash
cd Backend

python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install project dependencies using the backend dependency file once it has been created.

### Frontend

```bash
cd Frontend
npm install
npm run dev
```

The exact commands and environment variables will be documented as implementation progresses.

Do not commit `.env` files, passwords, API keys or private credentials.

## 9. Development Roadmap

| Phase | Focus |
|---|---|
| 0 | Repository inspection and environment setup |
| 1 | Authentication and user roles |
| 2 | Service centres, vehicles and components |
| 3 | Service requests and mechanic inspection |
| 4 | APS AI integration |
| 5 | 2D and 3D vehicle visualisation |
| 6 | Inventory and repair approvals |
| 7 | Repair workflow, invoices and mock payments |
| 8 | Dashboards and notifications |
| 9 | Testing, security and MVP release |

Refer to `docs/TASKS.md` for the detailed task breakdown.

## 10. Documentation

The `docs/` directory contains the primary project specifications:

- `PRD.md` — Product requirements.
- `ARCHITECTURE.md` — System architecture.
- `RULES.md` — Development constraints.
- `DESIGN.md` — Design system and UI direction.
- `TASKS.md` — Development roadmap.
- `MEMORY.md` — Persistent project decisions.

`CHECKPOINTS_TEMPLATE.md` defines the version-control and recovery process.

## 11. Version Control

Git and GitHub are used to maintain project history.

Development must follow these principles:

- Meaningful commits.
- Annotated phase tags.
- Tested checkpoints.
- No force-pushing.
- No accidental deletion or overwriting of user work.
- No committing secrets or private datasets.
- Documented rollback procedures.

## 12. Current Status

**Version:** 2.0  
**Stage:** Pre-development preparation

Documentation and initial 3D asset collection have been prepared. Repository inspection, local environment setup, implementation and AI integration remain to be completed.

Features documented in the roadmap must not be considered implemented until they have been developed and tested.

---

**VEDA V2 — Evidence-driven diagnostics. Transparent repairs. Smarter vehicle maintenance.**