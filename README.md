--Yes, Yes, stole from left right and centre--

# Super ADHD Child

Super ADHD Child is a dependency-free Codex plugin combining the Superpowers
software-development methodology with optional ADHD divergent ideation. The
runtime boundary is skills and documentation only: no hooks, MCP servers,
apps, CLI packages, external services, or installation-time dependencies.

## Routing

Ordinary planning, TDD, debugging, review, verification, and branch finishing
remain governed by the Superpowers skills. ADHD is manual-first and activates
only when the user explicitly asks for ADHD mode, divergent ideation, parallel
cognitive frames, or trap-focused exploration. A selected ADHD direction is
handed to `super-adhd-child:brainstorming`; ADHD does not approve or implement
the direction.

This plugin contains skills and does not register a host-level `/adhd`
command. The portable invocation is:

> Use ADHD mode on: how should we design this?

If a particular Codex surface documents `/adhd` as a textual trigger, that
surface may accept it, but it is not supplied by this plugin's manifest.

An explicit ADHD run uses five isolated divergent frame roles followed by
three isolated deepening roles. The root orchestrator scores, labels traps,
clusters, ranks, and selects candidates inline after divergence; it does not
dispatch separate scoring or clustering roles.

## Installation and duplicate installations

Use the Codex host's verified plugin installation mechanism for the repository;
there is no portable installer command in this project. The manifest exposes
only `skills: "./skills/"`, so installation must not be inferred from a slash
command. When this combined plugin is active, disable separate standalone ADHD
and Superpowers installations to prevent duplicate triggers. Do not remove,
overwrite, or modify those installations automatically.

## Local validation and packaging

From any current working directory, invoke the scripts with the repository
path (replace the placeholder with the checkout path):

```bash
python3 /path/to/Super-ADHD-Child/scripts/validate_repo.py /path/to/Super-ADHD-Child
python3 /path/to/Super-ADHD-Child/scripts/package_plugin.py /path/to/Super-ADHD-Child
python3 /path/to/Super-ADHD-Child/scripts/package_plugin.py /path/to/Super-ADHD-Child --check
```

Run the test suite from the repository root with
`python3 -m unittest discover -s tests -v`.

The validator runs the official Codex plugin validator when it is discoverable
through `CODEX_OFFICIAL_VALIDATOR`, `CODEX_HOME`, or the standard user Codex
skills path. Use `--skip-official` in offline CI when it is unavailable. The
packager validates source first, writes a stable archive with normalized ZIP
metadata, and replaces `skill.zip` only after validation succeeds. The archive
is committed; `--check` proves it is fresh without modifying it.
Inventory-declared runtime exclusions and namespaced skill references are
machine-checked, so reintroduced excluded files or references to unshipped
skills fail validation before packaging.

For the locally verified official audit, run:

```bash
python3 <local-root>/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

## Upstream maintenance

`UPSTREAM_INVENTORY.json` records repositories, pinned commits, vendored paths,
namespace transformations, exclusions, and local modifications. Check for
read-only drift with:

```bash
python3 scripts/check_upstream_drift.py
```

The drift checker may report a newer upstream commit or an inventory mismatch;
it never updates vendored files. Refreshing upstream material is deliberate:
review the new source, update the inventory and notices, reapply the local
namespace/routing changes, run the full validation suite, and rebuild the
archive. Do not rewrite historical design or implementation documents to make
them match a later implementation.

## Contribution workflow

Create a feature branch, preserve unrelated work, write failing tests before
changing behavior-shaping skills, make the smallest passing change, and review
the diff for accidental vendored-content changes. Run validation, tests,
syntax checks, archive freshness, and `git diff --check` before requesting
review. Keep runtime changes inside this repository's documented boundary.

See `THIRD_PARTY_NOTICES.md` for attribution and pinned source SHAs. See
`CHANGELOG.md` for release-level changes.
