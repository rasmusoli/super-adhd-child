# Super ADHD Child Efficiency and Consistency Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use super-adhd-child:subagent-driven-development (recommended) or super-adhd-child:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement and verify the local-only `1.3.0` surgical efficiency and consistency release described in the companion design.

**Architecture:** Keep policy in the universal `using-superpowers` skill, keep ADHD-specific isolation and orchestration rules in `adhd-ideation`, and enforce runtime exclusions through one inventory-aware repository validation path shared by archive discovery and packaging. Keep tests in the existing dependency-free unittest module.

**Tech Stack:** Markdown skill documents, JSON metadata, Python standard library validation and packaging, ZIP archives, and `unittest`.

## Global Constraints

- ADHD remains manual-first.
- Ordinary planning, TDD, debugging, review, and delivery continue through Superpowers.
- ADHD divergence remains isolated across cognitive-frame branches.
- Selected ADHD directions hand off to `super-adhd-child:brainstorming`.
- Do not weaken debugging, TDD, review, approval, verification, rationalization, or safety gates.
- Keep the plugin skills-and-documentation-only at runtime.
- Add no hooks, MCP servers, apps, external services, package dependencies, or unsupported manifest fields.
- Preserve pinned upstream commits, licenses, attribution, namespace conversion, intentional exclusions, unrelated work, and historical documents.
- Do not commit, push, publish, reinstall, change the marketplace, or modify standalone installations.

### Task 1: Add failing contracts

**Files:**
- Modify: `tests/test_repo_tools.py`
- Read for assertions: `UPSTREAM_INVENTORY.json`, `scripts/repo_tools.py`, and affected `skills/*/SKILL.md`

- [ ] Add fixture tests for a reintroduced excluded debugging file being rejected by `validate_repository` and `package_repository`.
- [ ] Add tests for one authoritative Codex policy, no obsolete bootstrap lookup, inline ADHD evaluation, exactly five divergent plus three deepening roles, no scoring/cluster subagents, shipped namespaced references, removed hot-path examples, preserved conditional references, manual-first routing, brainstorming handoff, and archive exclusion.
- [ ] Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`.
- [ ] Record the expected RED failures and confirm they arise from missing requested behavior rather than malformed tests.

### Task 2: Enforce structured inventory exclusions

**Files:**
- Modify: `UPSTREAM_INVENTORY.json`
- Modify: `scripts/repo_tools.py`
- Modify: `scripts/check_upstream_drift.py`
- Test: `tests/test_repo_tools.py`

- [ ] Add structured exact excluded paths for the five debugging development files under the Superpowers inventory entry.
- [ ] Add inventory parsing that validates exclusion types, paths, and nonempty matches against the declared policy without weakening existing pinned-source checks.
- [ ] Add a shared runtime-path exclusion check that reports a reintroduced excluded path as a validation error.
- [ ] Apply the same exclusion policy in `_archive_members` so an invalid excluded runtime path is never silently packaged.
- [ ] Ensure `package_repository` validates source before atomically replacing `skill.zip`.
- [ ] Re-run only the new inventory and archive tests and confirm GREEN.

### Task 3: Consolidate Codex collaboration policy

**Files:**
- Modify: `skills/using-superpowers/SKILL.md`
- Modify: `skills/writing-skills/SKILL.md`
- Delete: obsolete Codex platform reference file under `skills/using-superpowers/references/`
- Modify: `UPSTREAM_INVENTORY.json`
- Modify: `THIRD_PARTY_NOTICES.md`
- Test: `tests/test_repo_tools.py`

- [ ] Add compact universal Codex guidance for capability detection, capacity-sized batching, unavailable-isolation behavior, branch independence, inherited-model defaults, lifecycle detection, and local read-only verification.
- [ ] Remove the universal Platform Adaptation lookup and retain conditional `operational-patterns.md` behavior.
- [ ] Remove the `writing-skills` path reference to the deleted Codex reference file without introducing another universal lookup.
- [ ] Record the deletion and consolidated policy in inventory and local-modification notices.
- [ ] Run targeted bootstrap and link tests and confirm GREEN.

### Task 4: Refine ADHD orchestration and skill references

**Files:**
- Modify: `skills/adhd-ideation/SKILL.md`
- Modify: `skills/brainstorming/SKILL.md`
- Modify: `skills/using-superpowers/SKILL.md` if needed for shipped-reference consistency
- Modify: `scripts/repo_tools.py`
- Test: `tests/test_repo_tools.py`

- [ ] Replace the duplicated ADHD model/lifecycle policy with one authoritative-policy statement and local isolation rules.
- [ ] Make the orchestrator's Phase 2 inline scoring, trap labeling, clustering, weighted ranking, and top-three selection explicit.
- [ ] State exactly five divergent roles plus three deepening roles and exclude scoring/clustering from isolated dispatch accounting.
- [ ] Replace missing design and builder skill names with shipped skill references while preserving the `writing-plans` transition gate.
- [ ] Add fence-aware validation for namespaced references that resolves each referenced skill against the shipped directories and ignores generic prose or fenced examples.
- [ ] Run targeted ADHD and reference tests and confirm GREEN.

### Task 5: Reduce dispatch hot-path duplication

**Files:**
- Modify: `skills/dispatching-parallel-agents/SKILL.md`
- Modify: `skills/subagent-driven-development/SKILL.md`
- Test: `tests/test_repo_tools.py`

- [ ] Reduce the dispatching opening to independence and concurrent problem domains.
- [ ] Reduce the subagent-development opening to fresh per-task implementation and review loops.
- [ ] Remove the redundant `Real Example from Session` and `Example Workflow` closing sections.
- [ ] Preserve operative diagrams, prompt contracts, ledgers, review loops, fix-round caps, and verification requirements.
- [ ] Assert meaningful word-count reduction and valid remaining relative links.

### Task 6: Remove excluded files and update release documentation

**Files:**
- Delete: `skills/systematic-debugging/CREATION-LOG.md`
- Delete: `skills/systematic-debugging/test-academic.md`
- Delete: `skills/systematic-debugging/test-pressure-1.md`
- Delete: `skills/systematic-debugging/test-pressure-2.md`
- Delete: `skills/systematic-debugging/test-pressure-3.md`
- Preserve: `skills/systematic-debugging/root-cause-tracing.md`, `defense-in-depth.md`, and `condition-based-waiting.md`
- Modify: `.codex-plugin/plugin.json`
- Modify: `CHANGELOG.md`
- Modify: `README.md`
- Modify: `THIRD_PARTY_NOTICES.md`
- Modify: `UPSTREAM_INVENTORY.json`

- [ ] Remove only the five excluded runtime files.
- [ ] Bump the plugin version to `1.3.0`.
- [ ] Document the user-visible routing and efficiency changes without rewriting historical documents.
- [ ] Update local-modification and exclusion records while preserving both upstream SHAs and attribution.

### Task 7: Rebuild and verify the complete release

**Files:**
- Modify: `skill.zip`

- [ ] Run the official validator.
- [ ] Run the repository validator.
- [ ] Run the full unittest suite.
- [ ] Run deterministic archive freshness and offline upstream inventory checks.
- [ ] Run shell syntax checks for tracked shell scripts and CommonJS/JavaScript syntax checks for tracked scripts.
- [ ] Run fence-aware Markdown-link validation and `git diff --check`.
- [ ] Search for absent excluded files, absent obsolete Codex reference file, absent invalid skill references, eight-role ADHD accounting, inline orchestrator evaluation, one authoritative lifecycle policy, shipped namespaced references, manual-first routing, and brainstorming handoff.
- [ ] Compare before/after line counts, word counts, skill-tree size, and archive size.
- [ ] Confirm no commits, push, publication, installation, marketplace mutation, standalone-plugin mutation, caches, temporary archives, or generated test artifacts remain.
