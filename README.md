# VEDA V2
### Vehicle Evaluation Diagnostic Agents

**An AI-assisted heavy vehicle inspection, diagnostics and service management platform.**

> **Current Status:** MVP complete (v2.0.9). All 9 development phases delivered and tested locally.

---

## What Is VEDA?

VEDA connects heavy vehicle owners with registered service centres through a platform that combines AI-assisted diagnostics, mechanic inspections, interactive 3D vehicle visualisation, spare-parts inventory, transparent repair estimates, owner-controlled approvals, and integrated payment records.

VEDA is a decision-support platform. It does not replace professional mechanical inspection. Every diagnostic finding, recommendation and repair action is traceable.

---

## What Is Actually Built (MVP)

### Backend — Python / Django / PostgreSQL

| Area | Status | Details |
|---|---|---|
| Authentication | ✅ Complete | Phone OTP (6-digit, SHA-256 hashed, 5-min expiry, attempt limiting), JWT access + refresh tokens |
| User Roles | ✅ Complete | OWNER, WORKSHOP_ADMIN, MECHANIC, VEDA_ADMIN — role-based permission classes on every endpoint |
| Vehicles | ✅ Complete | Owner-isolated vehicle registration, update, deactivation |
| Service Centres | ✅ Complete | Registration, membership management, workshop admin access control |
| Component Catalogue | ✅ Complete | Hierarchical catalogue (27 components), `component_code` stable identifiers |
| Service Orders | ✅ Complete | 18-state machine (REQUESTED → VEHICLE_DELIVERED), validated transitions, immutable audit trail |
| Mechanic Inspection | ✅ Complete | Per-component observations, severity ratings, numeric sensor readings |
| AI Engine — APS | ✅ Complete | Scania APS failure classifier (XGBoost, F1=0.853, ROC-AUC=0.995), honest SKIPPED when data insufficient |
| Diagnostic Rules | ✅ Complete | APS-001 (AI prediction), MECH-001 (HIGH/CRITICAL observation), SENS-001 (out-of-range readings) |
| Digital Twin — Backend | ✅ Complete | Asset3D registry, 25 verified mesh mappings from GLB `anatomical_id` values |
| Inventory | ✅ Complete | Part catalogue, compatibility records, workshop stock, `select_for_update()` reservations |
| Estimates | ✅ Complete | Versioned repair estimates, Decimal totals, mechanics cannot approve on behalf of owners |
| Owner Approvals | ✅ Complete | Per-item approve/reject/clarify, auto-transition to APPROVED/PARTIALLY_APPROVED |
| Work Orders | ✅ Complete | Built from APPROVED items only, item progress tracking |
| Invoices | ✅ Complete | Sequential invoice numbers, tax-aware, Decimal throughout |
| Payments | ✅ Complete | MOCK provider (dev), idempotent by `transaction_reference` |
| Vehicle Delivery | ✅ Complete | PAID → VEHICLE_DELIVERED terminal state |

### Frontend — React / TypeScript / Vite

| Area | Status | Details |
|---|---|---|
| Authentication UI | ✅ Complete | Phone → OTP → profile setup → role-based redirect |
| Auth Context | ✅ Complete | JWT storage, role detection, `primaryRole`, protected routes |
| Owner Dashboard | ✅ Complete | Stats, recent orders, vehicle list — real API data |
| Owner Approvals | ✅ Complete | Itemised estimate decisions with approve/reject per line |
| Mechanic Dashboard | ✅ Complete | Assigned orders, context-aware next-action buttons |
| Workshop Admin Dashboard | ✅ Complete | Incoming queue, one-click accept, active job list |
| 3D Truck Viewer | ✅ Complete | React Three Fiber, GLB loading, per-mesh colour by diagnostic status |
| Status Legend | ✅ Complete | NORMAL / SUSPECTED / MECHANIC_VERIFIED / REPAIRED / UNMAPPED |
| API Service Layer | ✅ Complete | 7 typed service modules covering all backend endpoints |
| Landing Page | ✅ Complete | "UNDERSTAND THE MACHINE. BEFORE IT STOPS." — DESIGN.md hero |

### Tests

| Suite | Count | Result |
|---|---|---|
| Auth (OTP, JWT, roles) | 28 | ✅ Pass |
| Data isolation (owner, workshop) | 11 | ✅ Pass |
| State machine (transitions, audit) | 13 | ✅ Pass |
| AI integrity (coverage, honesty) | 9 | ✅ Pass |
| Estimates / inventory | 9 | ✅ Pass |
| **Total** | **67** | **✅ All pass** |

---

## Technology Stack

| Layer | Technology | Version |
|---|---|---|
| Backend | Python, Django, Django REST Framework | 3.11.9 / 5.1.4 / 3.15.2 |
| Auth | djangorestframework-simplejwt | 5.3.1 |
| Database | PostgreSQL | 18.6 |
| AI/ML | XGBoost, scikit-learn, pandas, NumPy | 2.1.3 / 1.5.2 / 2.2.3 / 2.1.3 |
| Frontend | React, TypeScript, Vite | 18.3 / 5.6 / 6.0 |
| 3D Viewer | Three.js, React Three Fiber, Drei | 0.170 / 8.17 / 9.117 |
| Testing | pytest-django, factory-boy | 4.9.0 / 3.3.1 |
| Version Control | Git / GitHub | — |

---

## Local Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (tested on 18.6)
- Git

### Backend

```powershell
cd Backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1       # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env — set DB_PASSWORD and DJANGO_SECRET_KEY

# Database setup (run in psql as postgres superuser)
# CREATE DATABASE veda_v2_dev;
# CREATE USER veda_user WITH PASSWORD 'your_password';
# GRANT ALL PRIVILEGES ON DATABASE veda_v2_dev TO veda_user;
# GRANT ALL ON SCHEMA public TO veda_user;

# Run migrations
python manage.py migrate

# Seed component catalogue and 3D asset mappings
python manage.py seed_components
python manage.py seed_digital_twin

# Train the APS classifier (required before AI diagnosis works)
python ai_engine/models/train_aps.py

# Start development server
python manage.py runserver
```

Backend runs at `http://localhost:8000`

OTP codes print to the terminal (CONSOLE provider — development only).

### Frontend

```powershell
cd Frontend

npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

### Run Tests

```powershell
cd Backend
python -m pytest tests/ -v
```

---

## API Overview

Base URL: `http://localhost:8000/api/v1/`

| Group | Prefix |
|---|---|
| Authentication | `/auth/` |
| Vehicles | `/vehicles/` |
| Service Centres | `/service-centres/` |
| Components | `/components/` |
| Service Orders | `/service-orders/` |
| Diagnosis | `/diagnosis/` |
| Digital Twin | `/digital-twin/` |
| Parts Catalogue | `/parts/` |
| Invoices / Payments | `/invoices/` |

All endpoints require JWT Bearer authentication except public read-only endpoints (component catalogue, verified service centres, 3D asset metadata, parts catalogue).

---

## AI Scope — Important Limitations

VEDA's initial AI model uses the **Scania APS Failure dataset** (GPL v3, Scania CV AB 2016) for APS-related failure classification only.

**This model does not:**
- Diagnose all truck component failures
- Independently identify a specific faulty component
- Provide Remaining Useful Life estimates
- Replace professional mechanic inspection

The model returns `SKIPPED` (not a fabricated prediction) when fewer than 10% of the 170 input features are present. Every AI response includes a scope warning.

**Verified test metrics (held-out test set):**

| Metric | Value |
|---|---|
| Precision | 0.853 |
| Recall | 0.853 |
| F1-score | 0.853 |
| ROC-AUC | 0.995 |
| Business cost (FP×10 + FN×500) | 28,050 |

---

## 3D Assets

| Asset | Format | License | Mesh Components |
|---|---|---|---|
| `refuse-collection-truck.glb` | GLB (glTF 2.0) | CC0 1.0 (Innerscene Corp) | 289 named meshes, 25 mapped to VEDA component codes |
| `truck-trailer.glb` | GLB (glTF 2.0) | CC0 1.0 (grab3d.com) | 7 nodes (body + wheels) |
| `caliper.obj` | Wavefront OBJ | License unverified | Single mesh |
| `engine.max` | 3ds Max binary | License unverified — not committed | N/A |
| `Kenwood.max` | 3ds Max binary | License unverified — not committed | N/A |

Components without a verified mesh mapping display as **UNMAPPED** rather than highlighting incorrect geometry.

---

## Development Roadmap

| Phase | Focus | Tag |
|---|---|---|
| 0 | Repository setup, environment, scaffolding | `v2.0.0-foundation` |
| 1 | Phone OTP authentication, JWT, roles | `v2.0.1-auth` |
| 2 | Service centres, vehicles, component catalogue | `v2.0.2-vehicles-centres` |
| 3 | Service orders state machine, mechanic inspection | `v2.0.3-inspection-workflow` |
| 4 | APS AI diagnostic engine, rule engine | `v2.0.4-aps-diagnosis` |
| 5 | Digital twin, 3D viewer, mesh mappings | `v2.0.5-digital-twin` |
| 6 | Inventory, spare parts, owner approvals | `v2.0.6-inventory-approvals` |
| 7 | Work orders, invoices, mock payments, delivery | `v2.0.7-repair-billing` |
| 8 | Frontend dashboards (Owner, Mechanic, Workshop) | `v2.0.8-dashboards` |
| 9 | Tests, security review, MVP release | `v2.0.9-mvp-release` |

---

## Security Notes

- OTP codes are stored as SHA-256 hashes only — the raw code is never persisted
- JWT tokens are stateless; refresh tokens rotate on use
- All secrets are read from `.env` — never hardcoded
- `.env`, `.venv/`, datasets and model binaries are all gitignored
- MOCK payment provider and CONSOLE OTP must never be enabled in production
- Each role class is applied at the view level — backend enforces all access control

---

## Repository

**GitHub:** https://github.com/EzhavaAdi/VEDA-Version-2.0

---

*VEDA V2 — Evidence-driven diagnostics. Transparent repairs. Smarter vehicle maintenance.*
