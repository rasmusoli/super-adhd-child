# Super ADHD Child Delegation Economics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use super-adhd-child:subagent-driven-development (recommended) or super-adhd-child:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace unconditional delegation-on-activation with evidence-based cheapest-sufficient routing while preserving manual-first ADHD ideation and high-assurance Superpowers workflows.

**Architecture:** Keep one authoritative policy in `skills/using-superpowers/SKILL.md`. Add only the activation boundary to `skills/using-super-adhd-child/SKILL.md`, protect the semantics with repository contract tests, update release attribution, and regenerate the deterministic archive.

**Tech Stack:** Markdown skill documentation, Python `unittest` contract tests, repository validation and packaging scripts, shell/JavaScript syntax checks, and deterministic ZIP packaging.

## Global Constraints

- Delegation requires independent separability, a meaningful benefit, and expected benefit greater than coordination and execution costs.
- Direct execution remains valid for trivial, tightly coupled, highly context-dependent, or faster-inline work.
- Use one Reader or one Builder when sufficient; add review only for justified risk or explicit independent verification.
- Full subagent-driven development remains the high-assurance path for approved multi-task plans and retains review gates, repair loops, ledgers, and final review.
- Waiting is capability-aware and event-driven; do not hard-code lifecycle names, poll with short waits, or request evidence-free updates.
- Related multi-agent work must resolve material documentation or contract contradictions at coordinator level before delegation.
- ADHD remains manual-first and is not activated by ordinary delegation.
- Do not add fixed models, worker counts, lifecycle names, global configuration, dependencies, or automatic commits.
- Preserve unrelated work and modify no standalone installations.

## File Map

- Modify `skills/using-superpowers/SKILL.md`: authoritative collaboration economics, topology ladder, waiting, handoff, and consistency gate.
- Modify `skills/using-super-adhd-child/SKILL.md`: delegation-versus-ADHD boundary wording if needed after the authoritative policy update.
- Modify `tests/test_repo_tools.py`: semantic contract tests replacing the obsolete unconditional-default assertion.
- Modify `THIRD_PARTY_NOTICES.md`: record the corrected local policy adaptation.
- Modify `CHANGELOG.md`: add the smallest appropriate release entry after inspecting version conventions.
- Modify `.codex-plugin/plugin.json`: bump version only if repository convention requires a release for this behavior change.
- Regenerate `skill.zip`: deterministic archive produced only after source validation passes.
- Remove the superseded untracked activation-delegation design and plan documents via recoverable trash cleanup.

### Task 1: Replace the collaboration policy

**Files:**
- Modify: `skills/using-superpowers/SKILL.md`
- Modify: `skills/using-super-adhd-child/SKILL.md` only if its boundary wording needs alignment

**Interfaces:**
- Consumes: current capability-aware collaboration policy and current manual-first ADHD router.
- Produces: one authoritative, platform-neutral delegation decision policy.

- [ ] **Step 1: Rewrite the activation paragraph**

Replace the unconditional “delegation as the default” behavior with wording
that proactively evaluates delegation but requires independent separability,
meaningful benefit, and expected benefit above assignment, handoff, waiting,
review, repair, context-reconstruction, and wall-clock costs. Do not require
numeric calculations.

- [ ] **Step 2: Add the lightest-sufficient topology ladder**

Document direct execution, one Reader, one Builder, justified independent
review, selective parallel workers, and full SDD. Explicitly say not to add
Reader/Builder/Tester/Reviewer/documentation workers automatically and not to
spawn ceremonial agents.

- [ ] **Step 3: Add waiting and handoff limits**

State that the current host’s native blocking wait, completion event, or
equivalent should be used when available; capability names must be detected;
short polling, routine status prompts, and evidence-free check-ins are
forbidden. Resume on completion, blocker, defect, meaningful timeout, or user
intervention. Retain file-based concise task briefs and evidence-driven
reports.

- [ ] **Step 4: Add the documentation-consistency preflight**

Require inspection of the smallest relevant set of requirements, plans,
durable documentation, interfaces, tests, and current behavior before related
multi-step delegation. Resolve material contradictions at coordinator level and
avoid repository-wide audits.

- [ ] **Step 5: Align the ADHD boundary**

Ensure `using-super-adhd-child` says ordinary delegation does not activate ADHD
and that ADHD remains manual-first.

### Task 2: Update semantic contract tests

**Files:**
- Modify: `tests/test_repo_tools.py`

**Interfaces:**
- Consumes: the policy and router text from Task 1.
- Produces: regression coverage for the new economics, waiting, consistency,
  and preserved-safety semantics.

- [ ] **Step 1: Remove the obsolete unconditional-default assertion**

Replace the marker requiring `capability-aware subagent delegation as the
default` with semantic markers for proactive evaluation, cost threshold,
direct execution, lightest topology, justified review, high-assurance SDD, and
ceremonial-agent prohibition.

- [ ] **Step 2: Add waiting-policy assertions**

Assert markers for native efficient waiting, capability-aware naming, no live
monitoring, no repeated short polling, no evidence-free check-ins, and the
completion/blocker/defect/timeout/user-intervention resume events.

- [ ] **Step 3: Add documentation-consistency assertions**

Assert relevant-source preflight, coordinator conflict resolution, and the
explicit prohibition on unnecessary repository-wide audits.

- [ ] **Step 4: Preserve existing safety assertions**

Keep tests for manual-first ADHD routing, no fixed operation/model/worker-count
assumptions, inline trivial work, full SDD review gates, file-based handoffs and
ledgers, valid namespace references, excluded runtime files, and deterministic
archives.

### Task 3: Update release records and clean superseded artifacts

**Files:**
- Modify: `CHANGELOG.md` if the version convention requires a release entry
- Modify: `THIRD_PARTY_NOTICES.md`
- Modify: `.codex-plugin/plugin.json` only if a version bump is required
- Remove recoverably: `docs/superpowers/specs/2026-08-03-subagent-delegation-on-plugin-activation-design.md`
- Remove recoverably: `docs/superpowers/plans/2026-08-03-subagent-delegation-on-plugin-activation.md`

**Interfaces:**
- Consumes: verified policy and tests from Tasks 1–2.
- Produces: release metadata that describes the corrected behavior without
  rewriting historical documents.

- [ ] **Step 1: Inspect release conventions**

Use current metadata, changelog, and recent history to select the smallest
appropriate version bump; do not hard-code a version from the request.

- [ ] **Step 2: Record the local policy adaptation**

Describe economics-based routing, efficient waiting, and consistency gates as
local changes while preserving manual-first ADHD ideation and high-assurance
workflow gates.

- [ ] **Step 3: Remove superseded untracked documents**

Move only the two named obsolete documents to the desktop trash so cleanup is
recoverable. Leave all checked-in historical plans and unrelated user changes
untouched.

### Task 4: Rebuild and validate the distributable

**Files:**
- Modify: `skill.zip`

**Interfaces:**
- Consumes: validated source tree and release metadata.
- Produces: fresh deterministic archive matching the source.

- [ ] **Step 1: Run focused policy tests**

Run the new contract tests and confirm they pass against the updated text.

- [ ] **Step 2: Run repository validation and package build**

Run `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_repo.py . --skip-official`
and `PYTHONDONTWRITEBYTECODE=1 python3 scripts/package_plugin.py . --skip-official`.

- [ ] **Step 3: Run complete verification**

Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`,
`python3 scripts/package_plugin.py . --check`,
`PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_upstream_drift.py . --offline`,
shell syntax checks for tracked `.sh` files, JavaScript syntax checks for
tracked `.js`/`.cjs` files, and `git diff --check`.

- [ ] **Step 4: Inspect final scope and evidence**

Review `git status --short --branch`, the final diff, archive contents, and
version metadata. Confirm no caches, vendored upstream rewrites, standalone
installation changes, or unrelated files were introduced.

## Validation Scenarios

Use the final policy to confirm: trivial work stays direct; bounded read-only
work may use one Reader without an automatic Builder; bounded implementation
may use one Builder or direct execution; security-sensitive changes justify
independent review; approved multi-task plans retain full SDD; long-running
workers use event-based waiting; contradictory project sources are resolved
before worker assignment; correct user approaches are not challenged
artificially; risky premises get a read-only discriminating test; repeated
manual work may receive a small reusable automation; and no efficiency claim is
made without measurement.

## No Automatic Commit

Do not create commits or push changes in this task. The user explicitly
requested implementation while the prompt forbids automatic commits; leave the
final working tree and evidence ready for deliberate review.
