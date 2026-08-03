# Super ADHD Child Plugin Design

## Goal

Create one self-contained, installable Codex plugin named `super-adhd-child` that combines the current Superpowers development workflow with ADHD divergent ideation while keeping ADHD manual-first and dependency-free.

## Source snapshots

- Superpowers: `https://github.com/obra/superpowers`, `main` at `44c9b2d6e889982ac18c27d05a19fefe335194e1`.
- ADHD: `https://github.com/UditAkhourii/adhd`, `main` at `eaeba4e98b388b8d1d31a31572d91ff989e04c00`.
- The source SHAs will be recorded in `THIRD_PARTY_NOTICES.md` so the vendored content is traceable.

## Architecture

The plugin root contains a minimal Codex manifest, documentation, license notices, and a `skills/` tree. The 14 requested Superpowers skill directories are copied with their nested references, scripts, examples, and diagrams so internal workflow links continue to work. Only the skill content is vendored; Superpowers repository hooks, tests, package metadata, and other harness integrations are excluded.

The ADHD source is included only as `skills/adhd-ideation/SKILL.md`. Its CLI, TypeScript library, package files, tests, and Agent SDK-related material are not copied. A new `using-super-adhd-child` skill documents routing and handoff policy without introducing a runtime component.

## Skill routing and namespacing

`adhd-ideation` keeps the upstream two-phase divergent-then-focus process, including isolated frame generation, scoring, clustering, trap detection, and deepening. Its frontmatter is narrowed to:

> Use when the user explicitly requests ADHD mode, divergent ideation, parallel cognitive frames, or trap-focused exploration.

The skill body retains the explicit `/adhd` opt-in. The router explains that genuinely open-ended ideation can use ADHD when breadth is the actual request, while ordinary feature design, planning, TDD, debugging, review, and delivery continue through Superpowers. ADHD output does not silently start implementation; a selected direction is handed to `super-adhd-child:brainstorming` for an approved design.

Every internal skill identifier that currently uses the `superpowers:` namespace is rewritten to `super-adhd-child:`. Skill directory names and the Superpowers prose branding remain unchanged except where a namespace must resolve inside the combined plugin. No references to the standalone `adhd` skill remain after the rename.

The `using-super-adhd-child` description is narrow enough to avoid competing with the upstream `using-superpowers` bootstrap on every ordinary request. It is intended for combined-plugin routing, explicit ADHD requests, and duplicate-installation guidance.

## Plugin manifest

`.codex-plugin/plugin.json` will:

- use `name: "super-adhd-child"` and strict semantic version `1.0.0`;
- point `skills` to `./skills/`;
- use MIT metadata and a neutral placeholder for repository/homepage fields;
- provide a clear `Super ADHD Child` interface description and starter prompts;
- contain no `hooks`, MCP, app, or unsupported manifest fields.

The manifest will not reference assets that are not shipped. A root `LICENSE` will carry the combined package's MIT license, while upstream license text and attribution will be preserved in `THIRD_PARTY_NOTICES.md`.

## Documentation and attribution

`README.md` will describe installation, the normal Superpowers workflow, explicit ADHD invocation, the handoff from ADHD to brainstorming, and how to avoid duplicate triggers. It will instruct users to disable separate standalone ADHD and Superpowers installations while using this combined plugin; it will not uninstall or modify those installations.

`THIRD_PARTY_NOTICES.md` will identify both upstream repositories and commit SHAs, include their MIT license attribution, and list local changes: the ADHD skill rename and trigger isolation, the namespace adaptation, the added router, and the exclusion of runtime code.

## Validation and delivery

Validation will combine the plugin-creator validator with repository-specific checks:

1. Validate `.codex-plugin/plugin.json` using the official validator from the local Codex installation.
2. Verify all 16 expected skills have frontmatter and `SKILL.md` files.
3. Verify every nested relative reference used by the vendored skills exists.
4. Verify no manifest placeholder marker, stale `superpowers:` namespace, standalone `adhd` skill directory, ADHD package/runtime file, or Anthropic SDK dependency is present.
5. Confirm Superpowers workflow identifiers and required support files remain present.
6. Review the final diff and status, commit as `feat: create combined super-adhd-child plugin`, and publish the selected branch without force-pushing.

The final report will include the branch, commit, push result, validator output, source SHAs, and the remaining instruction to disable duplicate standalone installations.

## Alternatives considered

### SKILL.md-only bundle

This reduces the package size but loses supporting references such as test-writing guidance, debugging references, review prompts, and brainstorming companion files. It would make the Superpowers workflow less faithful and is rejected.

### Upstream repositories or submodules inside the plugin

This preserves upstream layout but makes installation depend on repository nesting or submodule retrieval. It also risks shipping unrelated runtime code and duplicate plugin metadata. It is rejected because the requested result is one self-contained, skill-first plugin.

### Clean vendored skill bundle

Copying the selected skill directories and adapting only namespacing and trigger policy preserves the workflow while keeping the package installable and dependency-free. This is the selected approach.
