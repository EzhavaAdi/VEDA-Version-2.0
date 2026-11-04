# VEDA V2 — Kiro Development Rules

**Version:** 2.0  
**Project:** VEDA Vehicle Intelligence Platform  
**Priority:** Mandatory

These rules apply to every implementation, modification, debugging session and development phase.

Kiro must follow these instructions unless the user explicitly approves a change.

# 1. General Development Principles

1. Read the project documentation before implementing any feature.
2. Treat PRD.md as the product requirements source of truth.
3. Treat ARCHITECTURE.md as the technical architecture source of truth.
4. Treat DESIGN.md as the visual design source of truth.
5. Treat TASKS.md as the development roadmap.
6. Treat MEMORY.md as the persistent project decision log.
7. Never invent requirements or silently change approved decisions.
8. Ask the user when an important requirement is ambiguous.
9. Work incrementally rather than generating the entire application at once.
10. Prioritize maintainability, security, correctness and reliability.

# 2. Mandatory Planning Before Implementation

Before implementing a major feature:

1. Inspect the existing code.
2. Read the relevant documentation.
3. Identify dependencies.
4. Explain the implementation approach.
5. Identify files that will be created or modified.
6. Identify possible risks.
7. Implement only after the approach is clear.

Do not make unnecessary changes to unrelated modules.

Do not rewrite working code simply because another implementation style is preferred.

# 3. Environment Management

Creating the development environment is mandatory.

## Backend

- Use Python virtual environment named `.venv`.
- Install dependencies inside `.venv`.
- Maintain a requirements file.
- Configure Django using environment variables.
- Create `.env.example`.
- Create `.env` locally if it does not exist.
- Never overwrite existing environment secrets.
- Validate required environment variables.
- Configure PostgreSQL.
- Document migration and startup commands.

## Frontend

- Use Node.js and the existing React + TypeScript + Vite setup.
- Preserve the package lockfile.
- Install dependencies using the package manager indicated by the lockfile.
- Maintain a frontend environment example if required.
- Never expose private backend secrets through VITE environment variables.

## Environment Protection

The following must be ignored by Git:

- `.env`
- `.env.local`
- `.venv/`
- `node_modules/`
- `__pycache__/`
- `.pytest_cache/`
- Build output.
- Local databases.
- Private datasets.
- Private model artifacts.
- Uploaded private documents.
- Logs containing sensitive information.

Never commit credentials, private API keys or personal information.

# 4. Git and GitHub Rules

Git is mandatory throughout the project.

## Repository Setup

- Inspect the existing Git repository before initializing another one.
- Never overwrite an existing Git configuration.
- Create `.gitignore` before staging project files.
- Inspect the configured remote before adding a new one.
- Ask the user for the GitHub repository URL if it is unavailable.
- Use SSH, GitHub CLI or Git Credential Manager for authentication.
- Never request that the user paste passwords or access tokens into source files.

## Commit Rules

Every meaningful development phase must have a checkpoint commit.

Commit messages should be descriptive.

Examples:

```bash
git commit -m "feat: implement phone OTP authentication"

git commit -m "feat: implement vehicle registration"

git commit -m "feat: integrate APS inference engine"

git commit -m "feat: implement interactive truck viewer"
```

## GitHub Push Rules

- Push completed checkpoints to the configured GitHub repository.
- Push corresponding annotated tags.
- Check Git status before every commit.
- Review changes before staging.
- Never force-push.
- Never rewrite shared Git history.
- Never delete existing remote branches without permission.
- Never claim a push succeeded unless Git confirms it.

# 5. Checkpoint and Rollback Rules

This project must maintain recoverable checkpoints.

Before every major phase:

1. Check Git status.
2. Commit or otherwise safely preserve existing work.
3. Create a checkpoint branch when appropriate.
4. Implement the new phase.
5. Run tests and builds.
6. Review the Git diff.
7. Commit the completed work.
8. Create an annotated Git tag.
9. Update CHECKPOINTS.md.
10. Push commits and tags when GitHub is configured.

Suggested checkpoints:

- v2.0.0-foundation
- v2.0.1-auth
- v2.0.2-vehicles-centres
- v2.0.3-inspection-workflow
- v2.0.4-aps-diagnosis
- v2.0.5-digital-twin
- v2.0.6-inventory-approvals
- v2.0.7-repair-billing
- v2.0.8-mvp

## Rollback

Prefer:

```bash
git revert <commit-hash>
```

To inspect an earlier version:

```bash
git switch --detach <checkpoint-tag>
```

To create a recovery branch:

```bash
git switch -c recovery/<name> <checkpoint-tag>
```

Never execute the following without explicit user approval after explaining the consequences:

```bash
git reset --hard
git clean -fd
git push --force
```

Never discard uncommitted user changes.

# 6. Frontend Development Rules

- Use React and TypeScript.
- Use reusable components.
- Keep components focused on their responsibilities.
- Separate API communication from presentation.
- Maintain consistent naming conventions.
- Avoid unnecessarily large components.
- Use proper loading, empty, error and success states.
- Ensure forms have validation.
- Ensure buttons perform their advertised actions.
- Do not use fake backend responses as real production data.
- Make the application responsive.
- Respect accessibility requirements.
- Respect reduced-motion preferences.

## Design Consistency

Follow DESIGN.md.

The VEDA identity must remain:

- Premium.
- Minimalist.
- Automotive.
- Technologically advanced.
- Professional.

Do not turn the platform into a generic admin template.

Do not introduce unrelated colour schemes or inconsistent UI components.

# 7. Backend Development Rules

- Use Django and Django REST Framework.
- Keep the modular monolith architecture.
- Use PostgreSQL.
- Use Django migrations for schema changes.
- Use serializers for input validation.
- Use service modules for business logic.
- Use permissions for authorization.
- Use transactions for sensitive operations.
- Use Decimal for financial calculations.
- Use UUID identifiers where appropriate.
- Add indexes for frequently queried fields.
- Document important API contracts.

Never place all application logic inside views.

Never trust frontend validation as a replacement for backend validation.

# 8. Authentication and Authorization

- Use phone-number-based OTP authentication.
- Hash OTP values before storage.
- Set OTP expiry.
- Limit verification attempts.
- Implement rate limiting.
- Use a development-only console/mock OTP provider.
- Disable development bypasses in production.
- Enforce backend permissions for every protected resource.

Owners must only access their own vehicles and associated records.

Workshop administrators must only access records belonging to their service centre.

Mechanics must only access authorized workshop resources and assigned service orders.

VEDA administrators must have explicit administrative permissions.

# 9. AI and Machine Learning Rules

These rules are critical.

## Dataset Integrity

- Never invent training data.
- Never fabricate dataset labels.
- Record dataset source and version.
- Check dataset licensing and usage terms.
- Preserve original data where appropriate.
- Document preprocessing.
- Prevent train/test leakage.
- Use appropriate validation and test splits.
- Track model versions and evaluation metrics.

## Scania APS Model

The Scania APS Failure dataset is initially used for APS-related failure classification.

It must not be represented as:
- A complete truck-health model.
- A universal component-diagnosis model.
- An engine-damage prediction model.
- A remaining-useful-life model.

Do not claim exact component identification from APS predictions alone.

## Prediction Integrity

Every AI prediction must preserve:

- Model name.
- Model version.
- Preprocessing version.
- Input reference.
- Prediction output.
- Probability or confidence where supported.
- Execution timestamp.
- Execution status.

Never invent confidence scores.

Never replace missing model outputs with fabricated predictions.

## Mechanic Data Separation

Mechanic findings must be recorded separately from AI predictions.

Do not use post-prediction mechanic-confirmed labels as input features when evaluating the predictive model for the same diagnosis.

Avoid target leakage.

Mechanic data can be used as additional evidence in the diagnostic reasoning stage.

## Diagnostic Integrity

Distinguish:

1. AI-predicted fault.
2. Rule-based inference.
3. Mechanic observation.
4. Mechanic-verified diagnosis.

When evidence is insufficient, explicitly report insufficient data.

# 10. Diagnostic and Component Rules

- Use a controlled component catalogue.
- Maintain component hierarchy.
- Maintain component-to-system relationships.
- Use validated diagnostic rules.
- Record evidence supporting component recommendations.
- Never invent component compatibility.
- Never claim a component is definitely faulty based on unsupported inference.
- Allow mechanics to verify, reject or request additional inspection.

# 11. Remaining Useful Life Rules

Remaining useful life must be handled separately from failure classification.

- Do not calculate RUL using the binary Scania APS classifier.
- Require a suitable degradation/time-series dataset.
- Require a separately trained and validated RUL model.
- Account for available operating conditions.
- Display estimates with appropriate limitations.
- Display insufficient data when a validated estimate is unavailable.

Never manufacture a lifespan number to make the interface appear complete.

# 12. 3D and 2D Visualization Rules

- Use Three.js and React Three Fiber.
- Support GLB/GLTF assets.
- Support 2D SVG technical diagrams.
- Use actual mesh mappings.
- Use stable component identifiers.
- Synchronize 2D and 3D selection where mappings exist.
- Support rotation, zoom and camera reset.
- Maintain a component status legend.

Visualization states:

- NORMAL
- SUSPECTED
- MECHANIC_VERIFIED
- REPAIRED
- UNMAPPED

Never highlight an unrelated mesh to simulate a diagnosis.

Never assume a downloaded model has separately selectable components.

Check asset licensing and attribution.

# 13. Spare Parts and Inventory Rules

- Maintain a structured parts catalogue.
- Record compatibility evidence.
- Maintain centre-specific inventory.
- Track stock movements.
- Use transactions for stock reservations and deductions.
- Prevent negative stock unless explicitly supported by a documented business rule.
- Use Decimal for prices.
- Do not invent spare-part prices.
- Do not recommend incompatible parts.
- Maintain inventory audit records.

# 14. Estimates and Owner Approval Rules

- Estimates must be itemized.
- Separate labour and spare-part costs.
- Support estimate revisions.
- Support individual item approval and rejection.
- Record owner decisions and timestamps.
- Only approved items can enter authorized work orders.
- Mechanics cannot approve items on behalf of owners.
- Record clarification requests.

# 15. Repair and Payment Rules

- Maintain repair progress records.
- Record completed work.
- Perform final inspection.
- Generate invoices from authorized completed work.
- Use mock payments in local development.
- Verify production payment callbacks.
- Implement idempotent payment processing.
- Never store card information.
- Never treat frontend success as proof of payment.
- Never invent payment completion.

# 16. Data and File Management

- Store relational business data in PostgreSQL.
- Store uploaded files in controlled file storage.
- Store large model artifacts outside the database.
- Do not commit private datasets.
- Do not commit large model files without explicit approval.
- Consider Git LFS only after explaining its storage implications.
- Maintain dataset and asset provenance.

# 17. Testing Rules

Every major feature must include relevant tests.

Prioritize tests for:

- Authentication.
- Role permissions.
- Owner data isolation.
- Service-centre data isolation.
- Service-order state transitions.
- Inspection validation.
- AI input validation.
- AI inference output.
- Diagnostic evidence handling.
- Component mapping.
- Inventory stock updates.
- Estimate approvals.
- Payment verification.

Run relevant tests before marking a task complete.

Fix regressions before proceeding.

# 18. Documentation Rules

Whenever important changes are made:

- Update MEMORY.md.
- Update TASKS.md.
- Update ARCHITECTURE.md if architecture changes.
- Update PRD.md if product scope changes.
- Update DESIGN.md if design decisions change.
- Update CHECKPOINTS.md after checkpoints.

Never leave documentation describing functionality that does not exist.

Clearly distinguish completed, partial, mocked and planned functionality.

# 19. User Collaboration Rules

- Ask before making major architectural changes.
- Ask before introducing a new major dependency.
- Ask before replacing existing working modules.
- Explain significant technical tradeoffs.
- Do not assume unavailable credentials.
- Do not invent user or business details.
- Do not proceed past a major phase without reporting its results.
- Preserve existing work.

# 20. Final Development Principle

VEDA must be built as a reliable commercial vehicle-maintenance platform, not as a collection of disconnected demonstrations.

Correctness, traceability, security, maintainability and user trust take priority over development speed.

**Never sacrifice the integrity of the platform merely to make a feature look complete.**