# VEDA V2 — Development Checkpoint Template

This document defines the mandatory checkpoint procedure for VEDA V2.

Every development phase must be reviewed, tested, documented, and committed before moving to the next phase.

---

## 1. Checkpoint Information

| Field | Details |
|---|---|
| Project | VEDA V2 |
| Phase Number | `[PHASE_NUMBER]` |
| Phase Name | `[PHASE_NAME]` |
| Date | `[YYYY-MM-DD]` |
| Developer / Agent | Kiro |
| Git Branch | `[BRANCH_NAME]` |
| Commit Hash | `[COMMIT_HASH]` |
| Git Tag | `[ANNOTATED_TAG]` |
| Status | `[IN_PROGRESS / COMPLETED / BLOCKED]` |

## 2. Work Completed

List all implemented features, modifications, and completed tasks.

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3
- [ ] Task 4

Describe significant implementation decisions:

`[ADD DETAILS]`

## 3. Files Created or Modified

| File / Directory | Action | Purpose |
|---|---|---|
| `[PATH]` | Created / Modified / Deleted | `[DESCRIPTION]` |
| `[PATH]` | Created / Modified / Deleted | `[DESCRIPTION]` |

Record deletions explicitly. Never hide or silently discard existing user work.

## 4. Testing and Validation

| Test | Result | Notes |
|---|---|---|
| Backend tests | PASS / FAIL / N/A | |
| Frontend tests | PASS / FAIL / N/A | |
| API integration | PASS / FAIL / N/A | |
| Database tests | PASS / FAIL / N/A | |
| AI tests | PASS / FAIL / N/A | |
| Security checks | PASS / FAIL / N/A | |
| Build verification | PASS / FAIL / N/A | |

Only mark a test as PASS when it has actually been executed successfully.

List outstanding failures and known limitations:

`[ADD DETAILS]`

## 5. Git Checkpoint

Before creating a checkpoint:

1. Check the current branch.
2. Review `git status`.
3. Inspect the changes using `git diff`.
4. Check for accidental secrets, private datasets and generated files.
5. Run relevant tests.
6. Stage only the intended files.
7. Create a descriptive commit.
8. Create an annotated Git tag for the completed phase.
9. Push the branch and tag to GitHub only after repository access and push permissions are confirmed.

Suggested commit format:

`feat(phase-X): description of completed work`

Suggested tag format:

`v2.0.X-phase-name`

Example:

`v2.0.1-auth`

Never force-push or rewrite published Git history.

## 6. GitHub Synchronisation

| Check | Status |
|---|---|
| Local commit created | YES / NO |
| Commit hash recorded | YES / NO |
| Annotated tag created | YES / NO |
| Branch pushed | YES / NO |
| Tag pushed | YES / NO |
| Remote verified | YES / NO |

If GitHub synchronisation fails, preserve the valid local checkpoint and report the error. Do not claim that the work was backed up remotely.

## 7. Rollback Information

**Checkpoint commit:** `[COMMIT_HASH]`

**Checkpoint tag:** `[TAG_NAME]`

**Previous stable checkpoint:** `[PREVIOUS_TAG]`

Preferred rollback method for already-published changes:

`git revert <commit-hash>`

For a sequence of commits, review the range and determine the appropriate revert strategy before executing it.

Do not use destructive commands such as `git reset --hard`, `git clean -fd`, or force-push without explicit user approval.

## 8. Known Issues and Pending Work

- [ ] Pending task 1
- [ ] Pending task 2
- [ ] Known issue 1
- [ ] Known issue 2

Additional notes:

`[ADD DETAILS]`

## 9. Next Phase

**Next phase number:** `[PHASE_NUMBER]`

**Next phase name:** `[PHASE_NAME]`

**Prerequisites:**

- [ ] Current phase reviewed.
- [ ] Required tests passed.
- [ ] Checkpoint committed.
- [ ] Documentation updated.
- [ ] User approval received where required.

## 10. Completion Approval

| Approval | Status |
|---|---|
| Implementation reviewed | YES / NO |
| Testing reviewed | YES / NO |
| Git checkpoint verified | YES / NO |
| Documentation updated | YES / NO |
| Ready for next phase | YES / NO |

**Final notes:**

`[ADD SUMMARY]`

---

## Mandatory Rules

1. Never begin a new development phase while the previous phase has unresolved critical failures.
2. Never mark incomplete functionality as complete.
3. Never claim a GitHub push succeeded without verifying it.
4. Never commit secrets, credentials, private datasets or local environment files.
5. Never overwrite user-created files without reviewing them.
6. Preserve a clear history of all major architectural and implementation changes.
7. Update `MEMORY.md`, `TASKS.md` and other relevant documentation when important decisions or progress change.
8. Obtain user approval before proceeding whenever the project rules require it.

**VEDA V2 principle: Every stable phase must be recoverable, traceable and verifiable.**