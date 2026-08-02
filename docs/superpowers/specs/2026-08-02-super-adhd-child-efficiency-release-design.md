# Super ADHD Child Efficiency and Consistency Release Design

## Goal

Release a surgical `1.3.0` update that removes excluded runtime material,
eliminates the universal Codex policy round trip, keeps ADHD evaluation inline
in the orchestrator, removes invalid skill references, and shortens hot-path
dispatch skills without weakening any safety or development gates.

## Boundaries

- ADHD remains manual-first and selected directions still hand off to
  `super-adhd-child:brainstorming`.
- Ordinary planning, TDD, debugging, review, verification, and delivery remain
  Superpowers workflows.
- Runtime remains skills-and-documentation-only, with no hooks, apps, MCP
  servers, external services, or package dependencies.
- Pinned upstream commits, licenses, attribution, namespace conversion,
  historical documents, and unrelated work remain unchanged.
- Work is local only: no commit, push, publication, installation, marketplace
  update, or standalone-plugin mutation.

## Design

### 1. One inventory policy for validation and packaging

Add machine-readable excluded path patterns to each applicable upstream entry
in `UPSTREAM_INVENTORY.json`. The Superpowers entry will identify the five
development-only debugging files by exact relative path and retain the broader
descriptive exclusion. Repository validation will parse and validate these
patterns, reject any matching source path beneath the runtime tree, and reject
invalid or non-matching patterns. Archive-member discovery will apply the same
policy before producing entries, while packaging will continue to validate the
source first; therefore an invalid source cannot be packaged or replace the
existing archive.

Offline drift validation will use the same structured exclusion checks. Fixture
tests will copy the repository, reintroduce one excluded file, and prove both
repository validation and packaging reject it. Archive tests will prove removed
runtime files cannot enter the deterministic archive.

### 2. Consolidated collaboration policy

Move the compact Codex collaboration rules from the obsolete platform
reference into the universal
`skills/using-superpowers/SKILL.md`: capability detection, capacity-sized
batching, degraded behavior, independent branches, inherited-model defaults,
lifecycle detection, and local read-only verification. Remove the platform
adaptation lookup and delete the obsolete Codex reference file; update
`writing-skills` and inventory/notices so no broken reference or duplicate
policy remains.

The conditional `operational-patterns.md` lookup remains conditional and is not
promoted into the universal bootstrap.

### 3. ADHD orchestration and reference consistency

Replace the duplicated ADHD model/lifecycle section with a single reference to
the authoritative universal policy plus ADHD-specific isolation rules. Phase 2
will explicitly state that the orchestrator scores novelty, viability, and fit,
labels traps, clusters by angle, computes weighted ranking, and selects the top
three inline after all five divergent results return. It will dispatch only the
three deepening roles, making the default accounting exactly eight isolated
roles: five divergent frames and three deepeners.

All namespaced references will be checked against the shipped skill directory.
Missing unshipped design and builder skill references will be removed or
replaced with shipped skills, preserving brainstorming's hard gate that
`writing-plans` is the only transition after an approved specification.

### 4. Hot-path reduction and release metadata

Trim the duplicated opening rationale from each dispatch skill to its own
decision rule. Remove the redundant closing worked examples rather than adding
another mandatory reference file. Preserve operative diagrams, prompt
contracts, ledgers, review loops, fix-round limits, and verification rules.

Bump the manifest to `1.3.0`, document the user-visible changes in the
changelog and README, update attribution and inventory local-modification
records, and rebuild `skill.zip` only after source validation passes.

## Test and verification design

Tests will be added before production edits and run in RED. They will cover
inventory exclusions, archive exclusion, one authoritative Codex policy,
bootstrap lookup removal, inline ADHD accounting and evaluation, named-skill
resolution, hot-path example removal with valid conditional references,
manual-first routing, brainstorming handoff, deterministic packaging, and
offline inventory validation. GREEN verification will run the official and
repository validators, full unittest suite, archive freshness, offline drift,
shell and JavaScript syntax checks, fence-aware link checks, `git diff --check`,
and targeted searches for every requested invariant.
