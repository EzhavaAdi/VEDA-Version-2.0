# VEDA V2 — Development Checkpoints

This file records all development phase checkpoints for VEDA V2.

Each checkpoint represents a verified, tested and committed state of the project.

Refer to `CHECKPOINTS_TEMPLATE.md` for the checkpoint procedure.

---

## Checkpoint Index

| Phase | Name | Tag | Status | Date |
|---|---|---|---|---|
| 0 | Project Foundation | `v2.0.0-foundation` | COMPLETED | 2026-11-05 |
| 1 | Authentication | `v2.0.1-auth` | PENDING | — |
| 2 | Vehicles and Service Centres | `v2.0.2-vehicles-centres` | PENDING | — |
| 3 | Inspection Workflow | `v2.0.3-inspection-workflow` | PENDING | — |
| 4 | APS Diagnosis Engine | `v2.0.4-aps-diagnosis` | PENDING | — |
| 5 | Digital Twin and Visualization | `v2.0.5-digital-twin` | PENDING | — |
| 6 | Inventory and Approvals | `v2.0.6-inventory-approvals` | PENDING | — |
| 7 | Repair and Billing | `v2.0.7-repair-billing` | PENDING | — |
| 8 | Dashboards and Notifications | `v2.0.8-dashboards` | PENDING | — |
| 9 | MVP Release | `v2.0.9-mvp-release` | PENDING | — |

---

## Phase 0 — Project Foundation

### Checkpoint Information

| Field | Details |
|---|---|
| Project | VEDA V2 |
| Phase Number | 0 |
| Phase Name | Project Foundation |
| Date | 2026-11-05 |
| Developer / Agent | Kiro |
| Git Branch | main |
| Commit Hash | NOT YET CREATED — awaiting user approval |
| Git Tag | `v2.0.0-foundation` |
| Status | COMPLETED |

### Objectives

Establish the development environment, repository baseline, and project scaffolding.

No application features are implemented in this phase.

### Work Completed

- [x] Read and reviewed all six project documentation files (PRD.md, ARCHITECTURE.md, RULES.md, DESIGN.md, TASKS.md, MEMORY.md).
- [x] Read README.md and CHECKPOINTS_TEMPLATE.md.
- [x] Inspected full workspace structure.
- [x] Inspected Git status — workspace was NOT a Git repository; initialized in Phase 0.
- [x] Inspected 3D asset files (formats, sizes, license, mesh structure).
- [x] Inspected Backend and Frontend directories — both were empty.
- [x] Checked Python (3.11.9 ✓), Node.js (v24.13.1 ✓), npm (11.8.0 ✓), Git (2.53.0 ✓).
- [x] Confirmed PostgreSQL is NOT installed — installation required before Phase 1 DB setup.
- [x] Created `.gitignore` (excludes .env, .venv, node_modules, datasets, model artifacts, .max files).
- [x] Created `Backend/.env.example` with all required environment variables documented.
- [x] Created `CHECKPOINTS.md` (this file).
- [x] Verified `README.md` — accurate, no modifications needed.
- [x] Initialized Git repository (`git init`, branch `main`).
- [x] Created initial commit `a6d7c95` — 16 foundation files staged, no secrets, no datasets, no .max files.
- [x] Created annotated tag `v2.0.0-foundation`.
- [x] Created Python virtual environment at `Backend/.venv` (Python 3.11.9).
- [x] Installed all backend dependencies: Django 5.1.4, DRF 3.15.2, django-cors-headers 4.6.0, psycopg2-binary 2.9.10, python-dotenv 1.0.1, djangorestframework-simplejwt 5.3.1, Pillow 11.0.0, PyJWT 2.15.1, pandas 2.2.3, numpy 2.1.3, scikit-learn 1.5.2, xgboost 2.1.3, joblib 1.4.2.
- [x] Scaffolded Django project with VEDA-specific `config/settings.py` (env-driven, PostgreSQL, DRF, JWT, CORS, logging).
- [x] Created `Backend/requirements.txt` with all pinned dependencies.
- [x] Created `Backend/.env` with safe local development placeholders.
- [x] Created all `Backend/apps/` module stubs (accounts, organizations, vehicles, components, service_orders, inspections, diagnosis, digital_twin, inventory, estimates, work_orders, billing, notifications, audit).
- [x] Created all `Backend/ai_engine/` module stubs (datasets, preprocessing, models, inference, diagnosis_rules, evaluation, rul).
- [x] Verified `python manage.py check` — 0 issues.
- [x] Scaffolded React + TypeScript + Vite frontend with full directory structure (components, pages, features, services, hooks, types, utils, routes).
- [x] Created `Frontend/src/index.css` with VEDA design tokens (all colours, typography, spacing).
- [x] Created `Frontend/src/App.tsx` with Phase 0 placeholder confirming stack is operational.
- [x] Created `Frontend/src/main.tsx`, `Frontend/src/services/api.ts`, `Frontend/src/types/index.ts`.
- [x] Created `Frontend/src/vite-env.d.ts` for Vite environment type declarations.
- [x] Created `Frontend/.env.example` for frontend environment documentation.
- [x] `npm install` — 185 packages installed.
- [x] Frontend production build — 31 modules, 504ms, 0 errors.
- [x] TypeScript compilation — 0 errors.

### Files Created or Modified

| File / Directory | Action | Purpose |
|---|---|---|
| `.gitignore` | Created | Excludes secrets, venv, node_modules, datasets, model artifacts, .max files, OS files |
| `Backend/.env.example` | Created | Documents all required backend environment variables |
| `Backend/.env` | Created | Local dev environment (gitignored — never committed) |
| `Backend/config/settings.py` | Created/Replaced | VEDA-specific Django settings — env-driven, PostgreSQL, DRF, JWT, CORS, logging |
| `Backend/config/urls.py` | Created | Django URL root (generated by startproject) |
| `Backend/config/wsgi.py` | Created | WSGI entry point |
| `Backend/config/asgi.py` | Created | ASGI entry point |
| `Backend/manage.py` | Created | Django management script |
| `Backend/requirements.txt` | Created | All pinned Python dependencies |
| `Backend/apps/` | Created | 14 Django app module stubs (all with `__init__.py`) |
| `Backend/ai_engine/` | Created | 7 AI engine module stubs (datasets, preprocessing, models, inference, diagnosis_rules, evaluation, rul) |
| `Backend/media/` | Created | Local media upload directory (gitignored) |
| `CHECKPOINTS.md` | Created | This checkpoint tracking document |
| `Frontend/package.json` | Created | npm dependencies and scripts |
| `Frontend/tsconfig.json` | Created | TypeScript compiler configuration |
| `Frontend/tsconfig.node.json` | Created | TypeScript config for Vite config file |
| `Frontend/vite.config.ts` | Created | Vite config with React plugin, path alias, API proxy |
| `Frontend/index.html` | Created | HTML entry point with Manrope and DM Mono fonts |
| `Frontend/.env.example` | Created | Frontend environment variable documentation |
| `Frontend/src/main.tsx` | Created | React entry point with BrowserRouter |
| `Frontend/src/App.tsx` | Created | Root router with Phase 0 operational placeholder |
| `Frontend/src/index.css` | Created | Global CSS reset and VEDA design tokens |
| `Frontend/src/vite-env.d.ts` | Created | Vite environment type declarations |
| `Frontend/src/services/api.ts` | Created | Central API client (fetch wrapper) |
| `Frontend/src/types/index.ts` | Created | Shared TypeScript types (roles, states, evidence types) |
| `Frontend/src/` subdirectories | Created | components, pages, features, services, hooks, types, utils, routes, public |

### Environment Findings

| Component | Status | Details |
|---|---|---|
| Python | ✓ Available | 3.11.9 — suitable for Django and AI/ML work |
| python3 alias | ✗ Not mapped | Use `python` on this system |
| Node.js | ✓ Available | v24.13.1 |
| npm | ✓ Available | 11.8.0 |
| Git | ✓ Available | 2.53.0.windows.1 |
| PostgreSQL | ✗ NOT INSTALLED | Must be installed before Phase 1 database setup |
| Virtual environment | ✓ Created | `Backend/.venv` — Python 3.11.9 |
| Git repository | ✓ Initialized | `main` branch, commit `a6d7c95` |
| .gitignore | ✓ Created | Phase 0 |
| .env | ✓ Created | `Backend/.env` — local dev, gitignored |
| Backend/.env.example | ✓ Created | Phase 0 |
| requirements.txt | ✓ Created | All 13 dependencies pinned |
| Django check | ✓ PASS | `python manage.py check` — 0 issues |
| Frontend build | ✓ PASS | 31 modules, 504ms, 0 TypeScript errors |

### 3D Asset Findings

| Asset | Format | Size | Status | License | Component Granularity |
|---|---|---|---|---|---|
| `refuse-collection-truck.glb` | GLB (glTF 2.0) | 8.5 MB | ✓ Valid | CC0 1.0 (Innerscene Corp) | **289 named meshes** with `anatomical_id` — excellent for component highlighting |
| `truck-trailer.glb` | GLB (glTF 2.0) | 1.7 MB | ✓ Valid | CC0 1.0 (grab3d.com) | 7 nodes (body + 6 wheels) — low granularity, suitable as background/trailer asset |
| `caliper.obj` | OBJ (Wavefront) | 5.7 MB | ✓ Valid OBJ | Unknown — needs verification | Single component mesh, exported by Max2Obj v4.0 |
| `engine.max` | 3ds Max binary | 0.5 MB | ✗ Cannot inspect | Unknown — needs verification | Cannot determine without 3ds Max |
| `Kenwood.max` | 3ds Max binary | 138.6 MB | ✗ Cannot inspect | Unknown — needs verification | Cannot determine without 3ds Max |

**Key finding:** `refuse-collection-truck.glb` is the primary candidate for VEDA's interactive truck viewer. It has 289 individually named mesh components with `anatomical_id` extras covering axles, cab, chassis, suspension, steering, brakes and more — directly suitable for component-level highlighting in React Three Fiber.

**Important:** The `.max` files cannot be used in browser-based Three.js without conversion to GLB/GLTF. Conversion requires Autodesk 3ds Max or a compatible converter. License and attribution for these files must be verified before any conversion or production use.

### Dataset Findings

| File | Size | Notes |
|---|---|---|
| `aps_failure_training_set.csv` | 42.6 MB | Raw training data — 60,000 records |
| `aps_failure_test_set.csv` | 11.4 MB | Raw test data — 16,000 records |
| `aps_failure_training_set_processed_8bit.csv` | 97.75 MB | Preprocessed training data |
| `aps_failure_test_set_processed_8bit.csv` | 26.07 MB | Preprocessed test data |

**License:** GNU GPL v3.0 (Scania CV AB, 2016). Free to redistribute and modify under GPL terms.

All dataset files are excluded from Git by `.gitignore`.

### Testing and Validation

| Test | Result | Notes |
|---|---|---|
| Backend tests | N/A | Backend apps not yet implemented (Phase 1+) |
| Frontend tests | N/A | Test framework not yet configured (Phase 1+) |
| API integration | N/A | Not yet implemented |
| Database connection | **PASS** | PostgreSQL 18.6 connected, 18 migrations applied |
| AI tests | N/A | Model not yet trained |
| `manage.py check` | **PASS** | 0 issues, 0 silenced |
| TypeScript compilation | **PASS** | 0 errors |
| Frontend production build | **PASS** | 31 modules, 504ms, 161KB JS bundle |
| .gitignore review | **PASS** | Covers all required exclusions per RULES.md |
| .env.example review | **PASS** | All required variables documented |

### Git Checkpoint

**Status: COMPLETED**

**Initial foundation commit:**
```
a6d7c95 feat(phase-0): project foundation — documentation, gitignore, env example, 3D assets
```
Tag: `v2.0.0-foundation`

**Phase 0 completion commit:** (created in this phase — see below)

GitHub remote: `https://github.com/EzhavaAdi/VEDA-Version-2.0.git` — configured and push pending.

### GitHub Synchronisation

| Check | Status |
|---|---|
| Local commit created | YES — `a6d7c95` (foundation), `a3898bf` (scaffold) |
| Commit hash recorded | YES |
| Annotated tag created | YES — `v2.0.0-foundation` |
| Branch pushed | **BLOCKED** — authentication mismatch (see below) |
| Tag pushed | **BLOCKED** — same reason |
| Remote verified | YES — `https://github.com/EzhavaAdi/VEDA-Version-2.0.git` |

**Authentication issue:** Git is authenticated as `AdhishPrasad` but the target repository belongs to `EzhavaAdi`. To resolve, run one of the following before pushing:

```powershell
# Option A — GitHub CLI (recommended)
gh auth login
# Choose: GitHub.com → HTTPS → Login with a web browser
# Then re-authenticate as EzhavaAdi

# Option B — Git Credential Manager reset
git credential reject
# Re-enter EzhavaAdi credentials on next push

# Once authenticated correctly:
git push -u origin main
git push origin v2.0.0-foundation
```

### Known Issues and Blockers

- [x] **BLOCKER: PostgreSQL not installed.** ✅ RESOLVED — PostgreSQL 18.6 installed, `veda_v2_dev` database created, permissions granted, 18 migrations applied successfully.
- [ ] **ACTION REQUIRED: engine.max and Kenwood.max licenses.** These files are in the workspace but not committed. Their source and license must be confirmed before they can be committed to a public repository. They are currently gitignored via `3-D model/*.max`.
- [ ] **ACTION REQUIRED: caliper.obj license.** Origin unclear — verify before production use.
- [ ] **PENDING: GitHub push.** Remote `origin` will be configured and pushed once authentication is confirmed.

### Rollback Information

**Checkpoint commit:** NOT YET CREATED

**Checkpoint tag:** `v2.0.0-foundation` (proposed)

**Previous stable checkpoint:** None (this is the initial baseline)

Once the initial commit is created, the rollback reference will be:

```bash
git switch --detach v2.0.0-foundation
```

### Next Phase

**Next phase number:** 1

**Next phase name:** Backend Foundation and Authentication

**Prerequisites:**

- [x] Phase 0 reviewed and approved.
- [x] Git repository initialized and foundation commit created.
- [x] Django scaffold operational (`manage.py check` passes).
- [x] Frontend scaffold operational (build passes).
- [x] PostgreSQL installed and `veda_v2_dev` database created.
- [x] GitHub push completed and verified — `main` branch and `v2.0.0-foundation` tag on remote.
- [x] `Backend/.env` updated with real local PostgreSQL password.
- [x] `python manage.py migrate` — 18 migrations applied successfully.

### Completion Approval

| Approval | Status |
|---|---|
| Implementation reviewed | YES |
| Testing reviewed | YES |
| Git checkpoint verified | YES |
| Documentation updated | YES |
| Ready for next phase | **YES** — all Phase 0 prerequisites met |

---

*CHECKPOINTS.md is maintained throughout the entire VEDA V2 development lifecycle.*
*Each completed phase appends a new checkpoint section to this file.*
*Never mark a checkpoint complete without a verified Git commit hash.*

---

## Phase 1 — Backend Authentication

### Checkpoint Information

| Field | Details |
|---|---|
| Project | VEDA V2 |
| Phase Number | 1 |
| Phase Name | Backend Authentication |
| Date | 2026-11-06 |
| Developer / Agent | Kiro |
| Git Branch | main |
| Commit Hash | `82c6300` |
| Git Tag | `v2.0.1-auth` |
| Status | COMPLETED |

### Work Completed

- [x] Custom `User` model — UUID PK, `phone_number` (unique), `full_name`, `AbstractBaseUser`, no username field.
- [x] `Role` model — UUID PK, FK to User, choices: OWNER, WORKSHOP_ADMIN, MECHANIC, VEDA_ADMIN. Unique together constraint.
- [x] `OTP` model — UUID PK, SHA-256 hashed code, `expires_at`, `attempt_count`, `is_used`. Secure code generation via `secrets` module.
- [x] `AUTH_USER_MODEL = "accounts.User"` set in `settings.py`.
- [x] `apps.accounts` registered in `INSTALLED_APPS`.
- [x] Service layer (`services.py`): `request_otp`, `verify_otp`, `update_profile`, `assign_role`, `remove_role`. All wrapped in `@transaction.atomic`.
- [x] Typed exception hierarchy: `AuthError`, `OTPExpiredError`, `OTPInvalidError`, `OTPMaxAttemptsError`, `OTPAlreadyUsedError`.
- [x] CONSOLE OTP provider (dev only) — logs raw code to server terminal. Never enabled in production.
- [x] Serializers: `RequestOTPSerializer`, `VerifyOTPSerializer`, `ProfileSetupSerializer`, `UserSerializer`.
- [x] Views: `RequestOTPView`, `VerifyOTPView`, `MeView` (GET + PATCH).
- [x] URL routes: `/api/v1/auth/request-otp/`, `/verify-otp/`, `/token/refresh/`, `/me/`.
- [x] Root `config/urls.py` updated with API v1 prefix and future route stubs.
- [x] Permission classes: `IsOwner`, `IsWorkshopAdmin`, `IsMechanic`, `IsVedaAdmin`, `IsWorkshopMember`, `IsOwnerOrWorkshopMember`.
- [x] Django admin registered for `User`, `Role`, `OTP`.
- [x] Migration `accounts/0001_initial` created and applied.
- [x] 19 total migrations applied on clean database.

### Files Created or Modified

| File | Action |
|---|---|
| `Backend/apps/accounts/models.py` | Created |
| `Backend/apps/accounts/services.py` | Created |
| `Backend/apps/accounts/serializers.py` | Created |
| `Backend/apps/accounts/views.py` | Created |
| `Backend/apps/accounts/urls.py` | Created |
| `Backend/apps/accounts/permissions.py` | Created |
| `Backend/apps/accounts/admin.py` | Created |
| `Backend/apps/accounts/migrations/0001_initial.py` | Created |
| `Backend/config/settings.py` | Modified — AUTH_USER_MODEL, apps.accounts |
| `Backend/config/urls.py` | Modified — API v1 routes |

### Testing and Validation

| Test | Result | Notes |
|---|---|---|
| `manage.py check` | **PASS** | 0 issues |
| Migrations | **PASS** | 19 applied cleanly |
| Smoke tests | **PASS** | 8/8 — request-otp, invalid phone, wrong OTP, unauthenticated /me/, invalid refresh, missing body |
| E2E auth flow | **PASS** | 7/7 — full flow: request OTP → verify → JWT → /me/ → profile update → token refresh → reused OTP rejected |

### Git Checkpoint

| Check | Status |
|---|---|
| Commit created | YES — `82c6300` |
| Tag created | YES — `v2.0.1-auth` |
| Branch pushed | YES — `origin/main` |
| Tag pushed | YES — `origin/v2.0.1-auth` |

### Rollback

```bash
git switch --detach v2.0.1-auth    # inspect
git switch -c recovery/phase-1 v2.0.1-auth  # recover
git revert 82c6300                 # undo if needed
```

### Next Phase

**Phase 2 — Service Centres, Vehicles and Component Catalogue**

Prerequisites:
- [x] Phase 1 reviewed and approved.
- [x] Auth endpoints verified working.
- [x] JWT tokens issued and validated.
- [ ] User approval to begin Phase 2.

---

## Phase 2 — Service Centres, Vehicles and Component Catalogue

| Field | Details |
|---|---|
| Phase Number | 2 |
| Phase Name | Service Centres, Vehicles and Component Catalogue |
| Date | 2026-11-06 |
| Commit Hash | `9cf24cb` |
| Git Tag | `v2.0.2-vehicles-centres` |
| Status | COMPLETED |

### Work Completed

- [x] `ServiceCentre` model — UUID PK, VerificationStatus, registered_by FK
- [x] `WorkshopMembership` — user + centre unique, Designation choices (ADMIN, MECHANIC, STAFF)
- [x] `Vehicle` model — UUID PK, owner FK, registration_number unique, VehicleCategory, VehicleDocument
- [x] `Component` catalogue — hierarchical (parent FK), `component_code` stable identifier, VehicleSystem choices
- [x] `VehicleComponent` — links component instances to specific vehicles
- [x] 26 seed components via `seed_components` management command (APS, brakes, engine, suspension, axle, steering, tyres, electrical)
- [x] Service layers: `vehicles/services.py`, `organizations/services.py`, `components/services.py`
- [x] Serializers, views, URL routes for all three apps
- [x] Owner isolation enforced: owners access only their own vehicles
- [x] Workshop admin permission required for member management
- [x] 3 migrations applied cleanly
- [x] 21/21 smoke tests passed

### Endpoints Added

| Endpoint | Auth | Notes |
|---|---|---|
| `GET /api/v1/components/` | Public | Filter by `?system=` or `?tree=1` |
| `GET /api/v1/components/<code>/` | Public | Component by code |
| `GET /api/v1/service-centres/` | Public | Verified centres only |
| `POST /api/v1/service-centres/` | Any auth | Register + auto WORKSHOP_ADMIN role |
| `GET /api/v1/service-centres/mine/` | Auth | User's centres |
| `GET /api/v1/service-centres/<id>/` | Member | Centre detail |
| `GET/POST /api/v1/service-centres/<id>/members/` | Workshop Admin | Manage members |
| `GET/POST /api/v1/vehicles/` | Owner | List / register |
| `GET/PATCH/DELETE /api/v1/vehicles/<id>/` | Owner | Detail / update / deactivate |
| `GET/POST /api/v1/vehicles/<id>/components/` | Owner | Vehicle components |

### Next Phase: 3 — Service Orders and Mechanic Inspection

---

## Phase 3 — Service Orders and Mechanic Inspection

| Field | Details |
|---|---|
| Phase Number | 3 |
| Phase Name | Service Orders and Mechanic Inspection |
| Date | 2026-11-06 |
| Commit Hash | `fd77f54` |
| Git Tag | `v2.0.3-inspection-workflow` |
| Status | COMPLETED |

### Work Completed

- [x] `ServiceOrder` — full state machine, 18 states, `ALLOWED_TRANSITIONS` dict, `can_transition_to()` guard
- [x] `ServiceOrderEvent` — immutable audit log for every transition
- [x] `Inspection` — OneToOne to ServiceOrder, status: STARTED → IN_PROGRESS → COMPLETED
- [x] `InspectionItem` — per-component mechanic observations, Severity choices
- [x] `SensorReading` — Decimal measurements with unit and optional component link
- [x] Service layers: `transition_order`, `assign_mechanic`, `start_inspection`, `complete_inspection`, `add_inspection_item`, `add_sensor_reading`
- [x] Inspection completion auto-transitions order to `ESTIMATE_READY`
- [x] Role-based access: owner isolation, workshop member checks, mechanic assignment guard
- [x] 16/16 smoke tests passed — full workflow: submit → accept → receive → assign → inspect → observe → measure → complete → ESTIMATE_READY

### Endpoints Added

| Endpoint | Auth |
|---|---|
| `POST/GET /api/v1/service-orders/` | Owner |
| `GET /api/v1/service-orders/<id>/` | Owner |
| `POST /api/v1/service-orders/<id>/transition/` | Owner or Workshop member |
| `POST /api/v1/service-orders/<id>/assign-mechanic/` | Workshop Admin |
| `GET /api/v1/service-orders/<id>/events/` | Owner or Workshop member |
| `GET /api/v1/mechanic/orders/` | Mechanic → via `/api/v1/service-orders/mechanic/` |
| `GET /api/v1/service-centres/<id>/orders/` | Workshop member |
| `POST/GET/PATCH /api/v1/service-orders/<id>/inspection/` | Mechanic / member |
| `POST /api/v1/service-orders/<id>/inspection/complete/` | Mechanic |
| `GET/POST /api/v1/service-orders/<id>/inspection/items/` | Mechanic / member |
| `GET/POST /api/v1/service-orders/<id>/inspection/readings/` | Mechanic / member |

### Next Phase: 4 — APS AI Diagnostic Engine

---

## Phase 4 — APS AI Diagnostic Engine

| Field | Details |
|---|---|
| Phase Number | 4 |
| Phase Name | APS AI Diagnostic Engine |
| Date | 2026-11-06 |
| Commit Hash | `8774b29` |
| Git Tag | `v2.0.4-aps-diagnosis` |
| Status | COMPLETED |

### Model Performance (verified on held-out test set — not invented)

| Metric | Value |
|---|---|
| Precision | 0.853 |
| Recall | 0.853 |
| F1-score | 0.853 |
| ROC-AUC | 0.995 |
| True Negatives | 15,570 |
| False Positives | 55 |
| False Negatives | 55 |
| True Positives | 320 |
| Business cost (FP×10 + FN×500) | 28,050 |

### Scope Warning (on every AI response)

> This model classifies APS-related failures only. It does not diagnose all truck faults and must not be presented as a universal vehicle diagnostic system.

### Work Completed

- [x] Dataset inspected: 60k train / 16k test, 170 anonymised features, 59:1 imbalance
- [x] Preprocessing: `SimpleImputer(median)` + `StandardScaler`, feature order enforced
- [x] XGBoost classifier: `scale_pos_weight=59`, 200 trees, `tree_method=hist`
- [x] Model artifacts saved (binaries gitignored, JSON metadata committed)
- [x] Inference: `aps_inference.py` — singleton load, MIN_FEATURE_COVERAGE=10%, honest SKIPPED
- [x] Rule engine: APS-001, MECH-001, SENS-001 — explicit, traceable rules
- [x] Diagnosis models: AIModel, AIRun, AIPrediction, DiagnosisCase, DiagnosisEvidence
- [x] AI prediction and mechanic verification stored independently
- [x] Mechanic can confirm / reject / partial-verify each case
- [x] 6/6 smoke tests passed

### Next Phase: 5 — Digital Twin and 3D Vehicle Visualization

---

## Phase 5 — Digital Twin and 3D Vehicle Visualization

| Field | Details |
|---|---|
| Phase Number | 5 |
| Phase Name | Digital Twin and 3D Vehicle Visualization |
| Date | 2026-11-06 |
| Commit Hash | `07fc433` |
| Git Tag | `v2.0.5-digital-twin` |
| Status | COMPLETED |

### Work Completed

**Backend:**
- [x] `Asset3D`, `ComponentMeshMapping`, `Diagram2D`, `ComponentDiagramMapping` models
- [x] Digital twin service: `build_scene_state()` maps mesh_identifier → visual_state
- [x] `/api/v1/digital-twin/assets/`, `/assets/<id>/`, `/assets/<id>/scene/?order_id=`
- [x] `seed_digital_twin` command — 25 verified mappings using confirmed `anatomical_id` values from GLB
- [x] BODY component added to catalogue (27 total)
- [x] APS, Engine, Brakes correctly show as UNMAPPED (no mesh in this asset — this is honest)

**Frontend:**
- [x] Three.js 0.170, @react-three/fiber 8.17.10, @react-three/drei 9.117.3 installed
- [x] `TruckViewer3D.tsx` — GLB loading, OrbitControls, per-mesh colour by visual state
- [x] `DiagnosisViewer.tsx` — two-panel workspace (component list + 3D viewer + info panel)
- [x] `DiagnosisViewerDemo.tsx` — standalone demo at `/viewer` with mock scene state
- [x] Status legend (NORMAL/SUSPECTED/MECHANIC\_VERIFIED/REPAIRED/UNMAPPED)
- [x] Production build: 639 modules, 0 TypeScript errors

### Mesh Mapping Honesty Note

The `refuse-collection-truck.glb` is a refuse collection truck (garbage truck). It has excellent body, axle, suspension, steering, and wheel geometry (289 named meshes) but no APS, engine, or brake meshes. This is documented and honest — those components show as `UNMAPPED` rather than highlighting incorrect geometry.

### Next Phase: 6 — Inventory, Spare Parts and Owner Approvals

---

## Phase 6 — Inventory, Spare Parts and Owner Approvals

| Field | Details |
|---|---|
| Phase Number | 6 |
| Phase Name | Inventory, Spare Parts and Owner Approvals |
| Date | 2026-11-06 |
| Commit Hash | `8c301b9` |
| Git Tag | `v2.0.6-inventory-approvals` |
| Status | COMPLETED |

### Work Completed

- [x] `PartCatalog`, `PartCompatibility` (VERIFIED/PROBABLE/DEPRECATED), `WorkshopInventory`, `InventoryMovement`
- [x] `reserve_stock()`, `consume_stock()`, `cancel_reservation()` — all `select_for_update()` for concurrency safety
- [x] `RepairEstimate` (versioned, `recalculate_totals()`), `EstimateItem` (`ApprovalStatus`)
- [x] Owner decision audit: `owner_decision_by`, `owner_decision_at`, `clarification_note`
- [x] **Mechanics cannot approve items** — enforced at service layer (returns 403)
- [x] After all items decided: order auto-transitions (APPROVED / PARTIALLY\_APPROVED / REVISION\_REQUESTED)
- [x] `get_approved_items()` — gate for work order creation in Phase 7
- [x] All Decimal for financial values — no float arithmetic
- [x] 15/15 smoke tests passed

### Key rule verified in tests:
Grand total = (4500+800) + (850×2+300) = **7,300.00** ✓ Mechanic approve attempt → **403** ✓ Auto-transition to **PARTIALLY_APPROVED** after mixed owner decisions ✓

### Next Phase: 7 — Repair Tracking, Invoices and Payments

---

## Phase 7 — Repair Tracking, Invoices and Mock Payments

| Field | Details |
|---|---|
| Phase Number | 7 |
| Phase Name | Repair Tracking, Invoices and Mock Payments |
| Date | 2026-11-06 |
| Commit Hash | `b55442e` |
| Git Tag | `v2.0.7-repair-billing` |
| Status | COMPLETED |

### Complete Service Journey (14 state transitions verified)

```
REQUESTED → ACCEPTED → VEHICLE_RECEIVED → INSPECTION_IN_PROGRESS →
ESTIMATE_READY → AWAITING_APPROVAL → APPROVED → REPAIR_IN_PROGRESS →
FINAL_INSPECTION → INVOICED → PAYMENT_PENDING → PAID → VEHICLE_DELIVERED
```

### Work Completed

- [x] `WorkOrder`, `WorkOrderItem` — built from APPROVED estimate items only
- [x] Item progress: PENDING → STARTED → COMPLETED/SKIPPED
- [x] Work order completion → auto-transitions to FINAL\_INSPECTION
- [x] `Invoice` — sequential number, Decimal totals, tax-aware
- [x] `Payment` — `transaction_reference` unique (idempotency), MOCK provider
- [x] Mock payment: server-side completion, never trusts frontend
- [x] Idempotent: same reference returns existing Payment record
- [x] `deliver_vehicle()`: PAID → VEHICLE\_DELIVERED
- [x] Duplicate invoice blocked
- [x] 15/15 smoke tests passed

### Next Phase: 8 — Dashboards and Notifications (MVP completion)
