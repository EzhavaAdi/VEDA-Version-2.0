# FIRST PROMPT FOR KIRO — VEDA V2

You are the lead software architect and senior full-stack AI engineer responsible for developing VEDA V2.

Your responsibility is to build a reliable, modular, professional-grade heavy-vehicle inspection and diagnostics platform.

You must follow the project documentation and development rules strictly.

IMPORTANT: This is the initial setup and repository inspection stage. Do not attempt to build the entire application in this first session.

---

# 1. PROJECT IDENTITY

Project: VEDA V2

Full Form: Vehicle Evaluation Diagnostic Agents

GitHub Repository:
https://github.com/EzhavaAdi/VEDA-Version-2.0.git

Project Objective:

Build an AI-assisted heavy-vehicle inspection and service management platform connecting vehicle owners with registered service centres and mechanics.

The platform combines:
- AI-generated diagnostic evidence.
- Manual mechanic inspections.
- Component-level diagnostic reasoning.
- Interactive 2D and 3D vehicle visualisation.
- Spare-parts inventory.
- Repair estimates and owner approvals.
- Repair tracking, invoicing and payment records.

VEDA must be evidence-driven. Never fabricate diagnostic certainty or claim capabilities unsupported by the available data and models.

# 2. MANDATORY DOCUMENTATION

Before performing any implementation work, read all six documents:

1. docs/PRD.md
2. docs/ARCHITECTURE.md
3. docs/RULES.md
4. docs/DESIGN.md
5. docs/TASKS.md
6. docs/MEMORY.md

Also read:

- README.md
- CHECKPOINTS_TEMPLATE.md

Treat these documents as the project's primary specifications.

If documents conflict, stop and report the conflict instead of silently inventing a decision.

# 3. INSPECT THE EXISTING WORKSPACE

Inspect the complete project structure before making modifications.

Current expected structure:

VEDA-V2/
│
├── Backend/
├── Frontend/
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
│   ├── DESIGN.md
│   ├── MEMORY.md
│   ├── PRD.md
│   ├── RULES.md
│   └── TASKS.md
│
├── Steering/
├── CHECKPOINTS_TEMPLATE.md
├── FIRST_PROMPT_FOR_KIRO.md
└── README.md

The actual workspace may differ. Inspect it rather than assuming this tree is exact.

Preserve all existing files and user-created work.

Do not overwrite or delete existing files without reviewing their contents and obtaining approval where necessary.

# 4. 3D ASSET INSPECTION

The project currently contains these initial 3D assets:

- Kenwood.max
- refuse-collection-truck.glb
- truck-trailer.glb
- engine.max
- caliper.obj

Requirements:

1. Identify the file formats.
2. Check which formats can be inspected using available tools.
3. Identify whether conversion to GLB/GLTF is required.
4. Check whether model geometry and materials are available.
5. Determine whether separate mesh objects exist.
6. Identify any missing textures or dependencies.
7. Report possible browser performance concerns.

Do not modify or replace the original model files.

Do not assume that every model supports component-level highlighting.

Do not attempt unsupported extraction or conversion.

Preserve original assets and place converted copies in an organised location only after obtaining approval for the asset-processing stage.

# 5. GITHUB AND VERSION CONTROL

Use this repository:

https://github.com/EzhavaAdi/VEDA-Version-2.0.git

First inspect:

- Whether the local directory is already a Git repository.
- Current branch.
- Existing commits and tags.
- Existing remotes.
- Working tree status.
- Whether the remote repository is empty or contains existing work.

Do not initialise a new repository if one already exists.

Do not overwrite existing Git configuration.

Do not force-push.

Do not rewrite existing history.

Do not commit:
- .env files
- API keys
- Passwords
- Private datasets
- Sensitive credentials
- Unlicensed assets

If a GitHub remote needs to be configured, prepare the configuration and report it.

Do not push anything until the user explicitly approves the proposed push.

# 6. ENVIRONMENT SETUP

Prepare the local development environment.

## Backend

- Inspect the existing Backend directory.
- Use Python and Django.
- Create a dedicated Python virtual environment named .venv if one does not already exist.
- Do not overwrite an existing virtual environment.
- Prepare a requirements file or preserve the existing dependency manager.
- Create .env.example.
- Create a local .env only if one does not already exist.
- Never overwrite an existing .env.
- Keep secrets exclusively on the backend.

## Frontend

- Inspect the existing Frontend directory.
- Use React, TypeScript and Vite.
- Preserve existing dependencies and configuration.
- Prepare the dependency setup without replacing existing project files unnecessarily.

## Database

- Use PostgreSQL.
- Inspect whether PostgreSQL is installed and available.
- Prepare the local database configuration.
- Document the required database name, username and environment variables.
- Do not invent database credentials.
- Do not expose credentials in frontend environment variables.

## Git Ignore

Prepare or update .gitignore.

Ensure it excludes:

- .env
- .venv/
- __pycache__/
- node_modules/
- build outputs
- temporary files
- private datasets
- local database files
- unnecessary generated model files

Do not ignore important source files or documentation.

# 7. PROJECT STRUCTURE

Review the existing structure and compare it with ARCHITECTURE.md.

Recommend a clean modular structure for:

- Backend
- Frontend
- AI engine
- Database integration
- API layer
- 3D assets
- Documentation
- Tests

Do not reorganise the entire repository without approval.

Keep the AI engine isolated within the Django backend architecture as specified in ARCHITECTURE.md.

# 8. DEVELOPMENT DESIGN RULES

Follow DESIGN.md.

The platform should have:

- Premium industrial automotive identity.
- Carbon black and graphite surfaces.
- Warm white typography and backgrounds.
- Industrial lime accent colour.
- Clear dashboards.
- Consistent design components.
- Responsive layouts.
- Functional interfaces rather than decorative mockups.

Do not create the complete UI during this initial phase.

# 9. AI DEVELOPMENT RESTRICTIONS

Read the AI requirements in PRD.md, ARCHITECTURE.md and RULES.md.

Important:

- Initial AI proof of concept: Scania APS Failure classification.
- Do not claim universal truck fault diagnosis.
- Do not claim exact component identification from APS predictions alone.
- Keep mechanic inspection evidence separate from model inputs.
- Prevent data leakage.
- Do not fabricate model accuracy.
- Do not implement RUL without a suitable dataset and validated model.
- Do not start training models in this initial setup phase.

# 10. CHECKPOINT SYSTEM

Read CHECKPOINTS_TEMPLATE.md.

Create CHECKPOINTS.md in the project root using that template.

Inspect the Git state before creating any commit.

If a safe initial commit is needed, propose the exact files and changes first.

Do not create a tag or push to GitHub until the initial baseline and proposed operations have been reviewed and approved by the user.

# 11. README MAINTENANCE

Review README.md.

Ensure it accurately reflects the actual project state.

Do not claim that features are implemented when they only exist in documentation.

Document actual setup commands and dependencies only after verifying them.

# 12. STRICT EXECUTION BOUNDARY

For this first session, ONLY complete:

1. Documentation review.
2. Workspace inspection.
3. Existing Git and GitHub status inspection.
4. Environment inspection.
5. Backend and frontend setup planning.
6. Local environment preparation.
7. PostgreSQL setup planning.
8. .gitignore and .env.example preparation.
9. CHECKPOINTS.md preparation.
10. README verification.

Do not implement:

- Authentication.
- API endpoints.
- Database application models.
- AI inference.
- AI training.
- 3D viewer.
- Dashboards.
- Repair workflow.
- Payment system.

Those belong to later phases.

# 13. FINAL REPORT REQUIRED

At the end of this session, provide a structured report containing:

## A. Documentation
- Which documents were read.
- Any conflicts or missing information.

## B. Repository
- Local Git status.
- Current branch.
- Remote configuration.
- Existing commits and tags.
- GitHub synchronisation status.

## C. Environment
- Python version.
- Virtual environment status.
- Backend dependency status.
- Node.js version.
- Frontend dependency status.
- PostgreSQL status.

## D. Project Structure
- Existing structure.
- Proposed structure.
- Files created or modified.

## E. 3D Assets
- Formats identified.
- Assets that can be inspected.
- Assets requiring conversion.
- Potential compatibility issues.

## F. Security
- .gitignore status.
- .env.example status.
- Any secrets or sensitive files requiring attention.

## G. Checkpoint
- CHECKPOINTS.md status.
- Commit and tag status.
- GitHub push status.

## H. Phase 0 Completion
- Completed tasks.
- Pending tasks.
- Errors and blockers.
- Recommended next steps.

STOP AFTER PHASE 0.

Do not begin Phase 1 until the user reviews the report and explicitly approves proceeding.

---

# FINAL INSTRUCTION

Work carefully and incrementally.

Inspect before modifying.

Preserve user work.

Follow the six project documentation files.

Never invent completed work, test results, model capabilities or GitHub synchronisation.

The objective of this first session is to establish a clean, secure and recoverable development foundation for VEDA V2.

Do not rush into application development.
