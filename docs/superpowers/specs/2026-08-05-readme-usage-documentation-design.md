# README Usage Documentation Design

## Goal

Make the repository README a reliable starting point for installing and using
the Super ADHD Child plugin, with examples that match the shipped v1.4.0
skills and manifest.

## Scope

- Replace the stray opening text in `README.md` with a clear introduction.
- Add a concise quick-start section explaining that installation uses the
  host's verified plugin mechanism and that this repository has no portable
  installer command.
- Add concrete prompt examples for ordinary Superpowers work, explicit ADHD
  divergent ideation, and handing a selected direction back to planning/TDD.
- Keep the manual-first ADHD boundary, duplicate-installation warning, and
  validation commands accurate.
- Commit and push the README change to the repository's default branch after
  fresh validation.

## Non-goals

- Do not add a host-level `/adhd` command.
- Do not invent an installer command or alter marketplace configuration.
- Do not change plugin runtime behavior, vendored skills, or standalone
  installations.

## Acceptance checks

- README examples use only documented prompts and commands.
- README explicitly distinguishes ordinary workflows from explicit ADHD mode.
- README explains the lack of a portable installer and the duplicate-install
  boundary.
- `python3 scripts/validate_repo.py .` passes.
- `python3 -m unittest discover -s tests -v` passes.
- `python3 scripts/package_plugin.py . --check` passes.
- `python3 scripts/check_upstream_drift.py . --offline` passes.
- `git diff --check` passes.

