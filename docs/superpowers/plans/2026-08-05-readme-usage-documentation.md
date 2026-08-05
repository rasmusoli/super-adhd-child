# README Usage Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use super-adhd-child:subagent-driven-development (recommended) or super-adhd-child:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the README with accurate installation guidance and practical examples for ordinary Superpowers workflows, explicit ADHD ideation, and handoff into tested planning.

**Architecture:** Keep the change documentation-only. The README will mirror the existing manifest and skill contracts, using prompt examples rather than claiming a portable CLI or host-level command.

**Tech Stack:** Markdown, Python repository validation scripts, unittest, deterministic ZIP packaging.

## Global Constraints

- Preserve the dependency-free runtime boundary.
- Keep ADHD manual-first and separate from ordinary Superpowers routing.
- Do not invent a portable installer or host-level `/adhd` command.
- Do not modify standalone ADHD or Superpowers installations.
- Publish to the existing default branch `codex/super-adhd-child`.

---

### Task 1: Publish README usage guidance

**Files:**
- Modify: `README.md`
- Verify: `scripts/validate_repo.py`, `scripts/package_plugin.py`, `scripts/check_upstream_drift.py`, `tests/`

**Interfaces:**
- Consumes: Existing plugin manifest and skill contracts.
- Produces: README sections titled `Quick start`, `Usage examples`, and accurate installation/duplicate-installation guidance.

- [ ] **Step 1: Replace the stray opening line and add the quick start.**

  The README introduction must identify the plugin as dependency-free. The quick start must say to use the host's verified plugin installation mechanism and must not show an invented install command.

- [ ] **Step 2: Add usage examples that reflect the routing contract.**

  Include these concrete prompts:

  ```text
  Let's build this with Superpowers.
  Use ADHD mode on: generate unconventional directions for this open-ended design problem.
  Take the selected direction and turn it into a tested implementation plan.
  ```

  Explain that ADHD activates only after an explicit request and that selected directions return to Superpowers for planning, TDD, implementation, review, and verification.

- [ ] **Step 3: Preserve operational guidance.**

  Keep the no-portable-installer statement, the no-host-level-`/adhd` statement, the duplicate-installation warning, and the documented validation commands. Ensure examples do not imply that this plugin registers a slash command.

- [ ] **Step 4: Run the authoritative repository gate.**

  Run from the repository root:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_repo.py .
  PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
  PYTHONDONTWRITEBYTECODE=1 python3 scripts/package_plugin.py . --check
  PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_upstream_drift.py . --offline
  git diff --check
  ```

  Expected: every command exits zero; the unittest suite reports zero failures; the package check reports a fresh archive; the drift check reports offline PASS.

- [ ] **Step 5: Commit and push the scoped documentation change.**

  Stage only `README.md`, commit with `docs: clarify plugin usage`, and push the current branch with tracking already established:

  ```bash
  git add README.md
  git commit -m "docs: clarify plugin usage"
  git push origin codex/super-adhd-child
  ```

