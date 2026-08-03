# Super ADHD Child Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** Build and publish a self-contained Codex plugin named super-adhd-child that vendors the requested Superpowers workflow and a manual-first ADHD ideation skill.

**Architecture:** Copy only the 14 requested Superpowers skill directories and all nested support files. Add a renamed, trigger-isolated adhd-ideation skill and a narrow using-super-adhd-child router, then create a clean Codex manifest and documentation without upstream runtime code, hooks, or unsupported manifest fields.

**Tech Stack:** Markdown/YAML skill files, JSON manifest, MIT license text, Bash/Git, Python 3, and the local plugin-creator validator. No Node package installation or Agent SDK is required.

## Global Constraints

- Use the normalized plugin name super-adhd-child.
- Vendor Superpowers from commit 44c9b2d6e889982ac18c27d05a19fefe335194e1.
- Vendor ADHD from commit eaeba4e98b388b8d1d31a31572d91ff989e04c00.
- Include these Superpowers skills: brainstorming, writing-plans, test-driven-development, systematic-debugging, verification-before-completion, subagent-driven-development, executing-plans, dispatching-parallel-agents, requesting-code-review, receiving-code-review, using-git-worktrees, finishing-a-development-branch, writing-skills, and using-superpowers.
- Name the ADHD skill adhd-ideation and the router skill using-super-adhd-child.
- Use ADHD only for explicit /adhd requests or genuinely open-ended divergent ideation; ordinary Superpowers workflows remain authoritative.
- Do not include the ADHD CLI/library or Anthropic Agent SDK dependencies.
- Do not add hooks or any unsupported manifest field.
- Do not delete or uninstall standalone ADHD or Superpowers installations.
- Work on codex/super-adhd-child; never force-push.

---

### Task 1: Vendor the Superpowers skill tree

Files:
- Create: skills/brainstorming/ and the other 13 requested Superpowers skill directories, preserving each upstream directory's nested files.
- Source: `<temporary-source-root>/superpowers/` at the pinned commit, or a fresh checkout of the same commit if that temporary source is unavailable.

Interfaces:
- Consumes: the pinned Superpowers repository and the skill list in Global Constraints.
- Produces: 14 self-contained skill directories with upstream relative support-file layout and internal identifiers adapted to the combined plugin namespace.

- [ ] Step 1: Confirm the source commit before copying.

~~~bash
SOURCE_ROOT="<temporary-source-root>"
test "$(git -C "$SOURCE_ROOT/superpowers" rev-parse HEAD)" = "44c9b2d6e889982ac18c27d05a19fefe335194e1"
~~~

Expected: exit 0 with no output.

- [ ] Step 2: Copy the 14 selected skill directories, including nested support files.

~~~bash
SOURCE_ROOT="<temporary-source-root>"
skills=(
  brainstorming writing-plans test-driven-development systematic-debugging
  verification-before-completion subagent-driven-development executing-plans
  dispatching-parallel-agents requesting-code-review receiving-code-review
  using-git-worktrees finishing-a-development-branch writing-skills using-superpowers
)
mkdir -p skills
for skill in "\${skills[@]}"; do
  cp -a "$SOURCE_ROOT/superpowers/skills/$skill" "skills/$skill"
done
~~~

Expected: every listed directory exists with upstream support files such as brainstorming scripts, debugging references, review prompts, and SDD helper scripts.

- [ ] Step 3: Adapt only the internal skill namespace.

~~~bash
while IFS= read -r file; do
  sed -i 's/superpowers:/super-adhd-child:/g' "$file"
done < <(rg -l --glob '*.md' 'superpowers:' skills)
~~~

Expected: rg -n 'superpowers:' skills returns no matches, while rg -n 'super-adhd-child:' skills finds the adapted workflow references.

- [ ] Step 4: Verify the copied inventory before continuing.

~~~bash
SOURCE_ROOT="<temporary-source-root>"
skills=(
  brainstorming writing-plans test-driven-development systematic-debugging
  verification-before-completion subagent-driven-development executing-plans
  dispatching-parallel-agents requesting-code-review receiving-code-review
  using-git-worktrees finishing-a-development-branch writing-skills using-superpowers
)
for skill in "\${skills[@]}"; do
  test -f "skills/$skill/SKILL.md"
  test "$(find "$SOURCE_ROOT/superpowers/skills/$skill" -type f | wc -l)" = "$(find "skills/$skill" -type f | wc -l)"
done
git diff --check
~~~

Expected: exit 0. File counts prove nested support files were not silently dropped; content differences are limited to the planned namespace replacement.

- [ ] Step 5: Commit the vendored workflow.

~~~bash
git add skills
git commit -m "feat: vendor Superpowers workflow skills"
~~~

Expected: a commit containing only the selected Superpowers skill tree.

### Task 2: Add the ADHD skill and combined-plugin router

Files:
- Create: skills/adhd-ideation/SKILL.md
- Create: skills/using-super-adhd-child/SKILL.md
- Source: `<temporary-source-root>/adhd/skills/adhd/SKILL.md` at the pinned commit.

Interfaces:
- Consumes: the upstream ADHD skill and the namespaced Superpowers skills from Task 1.
- Produces: an explicit/manual-first ADHD skill and a policy router that hands selected ideas to super-adhd-child:brainstorming.

- [ ] Step 1: Confirm the ADHD source commit and copy only its skill document.

~~~bash
SOURCE_ROOT="<temporary-source-root>"
test "$(git -C "$SOURCE_ROOT/adhd" rev-parse HEAD)" = "eaeba4e98b388b8d1d31a31572d91ff989e04c00"
mkdir -p skills/adhd-ideation
cp "$SOURCE_ROOT/adhd/skills/adhd/SKILL.md" skills/adhd-ideation/SKILL.md
~~~

Expected: only skills/adhd-ideation/SKILL.md is added; no ADHD package, source, tests, CLI, or build files are copied.

- [ ] Step 2: Narrow the ADHD frontmatter and preserve its core loop.

The first lines must be:

~~~yaml
---
name: adhd-ideation
description: "Use when the user explicitly requests ADHD mode, divergent ideation, parallel cognitive frames, or trap-focused exploration."
license: MIT
---
~~~

Keep the upstream pre-flight gate, five-frame divergent generation, scoring, clustering, trap detection, weighted shortlist, and three-branch deepening. Replace the companion CLI install block with a sentence that this Codex plugin does not bundle or require the ADHD CLI/library. Add this after the output-shape guidance:

~~~markdown
## Handoff to Superpowers

ADHD produces candidate directions; it does not approve or implement one. When the user wants to turn a selected direction into a buildable design, continue with super-adhd-child:brainstorming. The Superpowers planning, TDD, debugging, review, and branch-finishing skills remain authoritative after that handoff.
~~~

Expected: the methodology is preserved, the trigger is manual-first, and the skill no longer instructs users to install a separate runtime for this plugin.

- [ ] Step 3: Create the router with a narrow trigger and explicit routing policy.

Create skills/using-super-adhd-child/SKILL.md with this content:

~~~markdown
---
name: using-super-adhd-child
description: "Use when the user asks how to route work through the Super ADHD Child plugin, explicitly requests ADHD mode, or needs duplicate-installation guidance."
license: MIT
---

# Using Super ADHD Child

This plugin combines the Superpowers development methodology with ADHD divergent ideation.

## Routing policy

- Use ADHD only for an explicit /adhd request, an explicit request for divergent ideation or parallel cognitive frames, or genuinely open-ended ideation where breadth is the actual need.
- Do not use ADHD automatically for ordinary feature design, implementation planning, TDD, known-root-cause debugging, code review, or branch finishing.
- ADHD performs divergent generation, scoring, clustering, trap detection, and deepening. It does not approve or implement a direction.
- After the user selects a direction, hand it to super-adhd-child:brainstorming for the approved design gate.
- super-adhd-child:writing-plans, super-adhd-child:test-driven-development, super-adhd-child:systematic-debugging, review skills, and branch-finishing skills remain authoritative for implementation and delivery.

## Duplicate installations

When this combined plugin is active, disable separate standalone ADHD and Superpowers installations to prevent duplicate triggers. Do not remove or modify those installations automatically.
~~~

Expected: the router contains the manual-first policy, handoff/authority statements, and no broad trigger that competes with ordinary Superpowers brainstorming.

- [ ] Step 4: Validate the two new skill frontmatters and policy text.

~~~bash
python3 - <<'PY'
from pathlib import Path
import yaml

expected = {
    "adhd-ideation": "Use when the user explicitly requests ADHD mode, divergent ideation, parallel cognitive frames, or trap-focused exploration.",
    "using-super-adhd-child": "Use when the user asks how to route work through the Super ADHD Child plugin, explicitly requests ADHD mode, or needs duplicate-installation guidance.",
}
for name, description in expected.items():
    path = Path("skills") / name / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---", 4)
    frontmatter = yaml.safe_load(text[4:end])
    assert frontmatter["name"] == name
    assert frontmatter["description"] == description
    assert "super-adhd-child:brainstorming" in text
assert not Path("skills/adhd").exists()
PY
! rg -n -i '@anthropic-ai/sdk|from ["'"'"']@anthropic|require\(["'"'"']@anthropic|npm install -g adhd-agent' skills/adhd-ideation
~~~

Expected: exit 0.

- [ ] Step 5: Commit the ADHD routing layer.

~~~bash
git add skills/adhd-ideation skills/using-super-adhd-child
git commit -m "feat: add manual-first ADHD ideation routing"
~~~

Expected: a commit containing the adapted ADHD skill and router only.

### Task 3: Add the manifest, license, attribution, and README

Files:
- Create: .codex-plugin/plugin.json
- Create: README.md
- Create: LICENSE
- Create: THIRD_PARTY_NOTICES.md

Interfaces:
- Consumes: the complete skill tree from Tasks 1 and 2, the two pinned upstream SHAs, and the Codex plugin manifest contract.
- Produces: an installable manifest and user-facing documentation with complete MIT attribution.

- [ ] Step 1: Create the manifest with only accepted fields.

Create .codex-plugin/plugin.json with this exact shape:

~~~json
{
  "name": "super-adhd-child",
  "version": "1.0.0",
  "description": "Superpowers development workflows with explicit ADHD divergent ideation for Codex.",
  "author": {
    "name": "Plugin Maintainers",
    "url": "https://example.invalid/super-adhd-child"
  },
  "homepage": "https://example.invalid/super-adhd-child",
  "repository": "https://example.invalid/super-adhd-child",
  "license": "MIT",
  "keywords": ["superpowers", "adhd", "ideation", "planning", "tdd", "debugging"],
  "skills": "./skills/",
  "interface": {
    "displayName": "Super ADHD Child",
    "shortDescription": "Superpowers workflows with explicit divergent ideation",
    "longDescription": "Use Super ADHD Child for disciplined brainstorming, planning, TDD, debugging, review, delivery, and optional ADHD divergent exploration that hands selected directions back to Superpowers.",
    "developerName": "Plugin Maintainers",
    "category": "Developer Tools",
    "capabilities": ["Interactive", "Read", "Write"],
    "defaultPrompt": [
      "Let's build this with Superpowers.",
      "Run /adhd on this open-ended design problem.",
      "Help me move from the selected idea to a tested plan."
    ],
    "websiteURL": "https://example.invalid/super-adhd-child",
    "screenshots": []
  }
}
~~~

Expected: no hooks, runtime component paths, or placeholder values.

- [ ] Step 2: Write README.md with this content:

~~~markdown
# Super ADHD Child

Super ADHD Child is a dependency-free Codex plugin combining the Superpowers software-development methodology with the ADHD divergent-ideation skill.

## Normal workflow

Use the Superpowers skills for ordinary work: brainstorming and design approval, implementation planning, TDD, systematic debugging, parallel execution, code review, verification, and branch finishing.

## ADHD mode

Run /adhd <problem> or explicitly ask for ADHD mode, divergent ideation, parallel cognitive frames, or trap-focused exploration. ADHD generates broadly, scores and clusters candidates, flags traps, and deepens survivors. It does not silently implement a candidate. When a direction is selected, continue with super-adhd-child:brainstorming, then use the Superpowers planning and implementation workflow.

## Installation and duplicate triggers

Install this repository as the super-adhd-child Codex plugin. When using it, disable separate standalone ADHD and Superpowers installations so their skills do not compete. This plugin never removes or changes those installations.

## Dependency boundary

The first version contains skill and documentation files only. It does not bundle the ADHD CLI/library, Anthropic Agent SDK packages, hooks, or other runtime services.

## Upstream attribution

See THIRD_PARTY_NOTICES.md for the pinned source commits, MIT notices, and local modifications.
~~~

- [ ] Step 3: Add LICENSE and THIRD_PARTY_NOTICES.md. LICENSE contains the standard MIT permission and warranty text for this combined package. THIRD_PARTY_NOTICES.md identifies both repositories and exact SHAs, reproduces the Superpowers and ADHD MIT copyright/license notices from their source LICENSE files, and lists these local modifications: the ADHD rename, manual-first trigger and handoff, namespace adaptation, added router, and exclusion of hooks, package files, CLI/library code, tests, and runtime dependencies.

- [ ] Step 4: Run manifest-level checks before committing the documentation layer.

~~~bash
Run the official plugin validator from the active Codex installation against the checkout.
git diff --check
~~~

Expected: the plugin validator passes once the skill tree is present, and git diff --check emits no whitespace errors.

- [ ] Step 5: Commit the plugin metadata and documentation.

~~~bash
git add .codex-plugin/plugin.json README.md LICENSE THIRD_PARTY_NOTICES.md
git commit -m "feat: create combined super-adhd-child plugin"
~~~

Expected: a commit containing the manifest, README, license, and notices.

### Task 4: Run complete validation and review the assembled plugin

Files:
- Test: the current plugin tree and all committed files.
- Reference: the official validator in the local Codex installation.

Interfaces:
- Consumes: the plugin assembled by Tasks 1–3.
- Produces: command evidence that every requirement is satisfied before publication.

- [ ] Step 1: Run the official plugin validator.

~~~bash
Run the official plugin validator from the active Codex installation against the checkout.
~~~

Expected: the official plugin validator reports success for the checkout.

- [ ] Step 2: Verify the complete expected skill set and frontmatter.

~~~bash
python3 - <<'PY'
from pathlib import Path
import yaml

expected = {
    "brainstorming", "writing-plans", "test-driven-development",
    "systematic-debugging", "verification-before-completion",
    "subagent-driven-development", "executing-plans",
    "dispatching-parallel-agents", "requesting-code-review",
    "receiving-code-review", "using-git-worktrees",
    "finishing-a-development-branch", "writing-skills", "using-superpowers",
    "adhd-ideation", "using-super-adhd-child",
}
actual = {path.name for path in Path("skills").iterdir() if path.is_dir() and not path.name.startswith(".")}
assert actual == expected, (sorted(actual), sorted(expected))
for name in sorted(expected):
    text = (Path("skills") / name / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\n")
    end = text.find("\n---", 4)
    frontmatter = yaml.safe_load(text[4:end])
    assert frontmatter["name"] == name
    assert isinstance(frontmatter["description"], str) and frontmatter["description"].strip()
PY
~~~

Expected: exit 0 with no assertion output.

- [ ] Step 3: Verify namespace, dependency, and source-boundary invariants.

~~~bash
! rg -n 'superpowers:' skills
! find skills/adhd-ideation -type f \( -name 'package.json' -o -name 'package-lock.json' -o -name '*.ts' \) -print -quit | grep -q .
! rg -n -i '@anthropic-ai/sdk|from ["'"'"']@anthropic|require\(["'"'"']@anthropic|anthropic-agent-sdk' skills
test ! -e skills/adhd
test ! -e package.json
test ! -e package-lock.json
test "$(find skills -mindepth 1 -maxdepth 1 -type d | wc -l)" = 16
rg -n 'super-adhd-child:(brainstorming|writing-plans|test-driven-development|systematic-debugging|verification-before-completion|subagent-driven-development|executing-plans|requesting-code-review|finishing-a-development-branch)' skills
~~~

Expected: negative checks pass, exactly 16 skill directories exist, and the final rg command prints adapted workflow references.

- [ ] Step 4: Verify support-file inventory and repository cleanliness.

~~~bash
SOURCE_ROOT="<temporary-source-root>"
skills=(
  brainstorming writing-plans test-driven-development systematic-debugging
  verification-before-completion subagent-driven-development executing-plans
  dispatching-parallel-agents requesting-code-review receiving-code-review
  using-git-worktrees finishing-a-development-branch writing-skills using-superpowers
)
for skill in "\${skills[@]}"; do
  test "$(find "$SOURCE_ROOT/superpowers/skills/$skill" -type f | wc -l)" = "$(find "skills/$skill" -type f | wc -l)"
done
git diff --check
git status --short
~~~

Expected: support-file counts match, whitespace validation passes, and only intended files are present.

- [ ] Step 5: Review the final diff before publication.

~~~bash
git log --oneline --decorate --max-count=6
git diff "$(git rev-list --max-parents=0 HEAD)" HEAD --stat
git diff "$(git rev-list --max-parents=0 HEAD)" HEAD -- .codex-plugin/plugin.json README.md THIRD_PARTY_NOTICES.md skills/adhd-ideation/SKILL.md skills/using-super-adhd-child/SKILL.md
~~~

Expected: the diff contains the manifest, docs, notices, router, adapted ADHD skill, and the complete selected Superpowers tree, with no unrelated upstream runtime repository content.

### Task 5: Commit the release state and publish the requested branch

Files:
- Modify: Git history and remote branch only.

Interfaces:
- Consumes: a clean, validated local branch.
- Produces: the selected publication branch and verifiable remote commit evidence.

- [ ] Step 1: Confirm the exact branch and clean state.

~~~bash
test "$(git branch --show-current)" = "codex/super-adhd-child"
test -z "$(git status --porcelain)"
~~~

Expected: exit 0.

- [ ] Step 2: Create the requested feature commit if any final validation changes remain.

~~~bash
git add .
git commit -m "feat: create combined super-adhd-child plugin"
~~~

Expected: commit the final implementation changes if present; if the implementation commits already contain the final state, retain the latest implementation commit instead of creating an empty commit.

- [ ] Step 3: Push without force.

~~~bash
git push -u origin codex/super-adhd-child
~~~

Expected: GitHub accepts a new branch at local HEAD without any force-push option.

- [ ] Step 4: Verify the remote branch and final commit.

~~~bash
git ls-remote --heads origin codex/super-adhd-child
gh api repos/OWNER/REPOSITORY/branches/codex/super-adhd-child --jq '.name + " " + .commit.sha'
~~~

Expected: both commands report codex/super-adhd-child and the same commit SHA as local git rev-parse HEAD.

- [ ] Step 5: Report the complete handoff.

Report the final branch, commit SHA, official validator result, custom invariant checks, upstream SHAs, push result, and the instruction to disable separate standalone ADHD and Superpowers installations while using this combined plugin.
