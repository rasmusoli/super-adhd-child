# Third-Party Notices

Super ADHD Child combines and adapts skill documentation from the following MIT-licensed projects. The source snapshots are pinned so the vendored content can be audited and refreshed deliberately.

## Superpowers

- Repository: https://github.com/obra/superpowers
- Source branch: `main`
- Source commit: `44c9b2d6e889982ac18c27d05a19fefe335194e1`
- License: MIT
- Copyright notice: Copyright (c) 2025 Jesse Vincent

The following is the license text from the pinned Superpowers source:

```text
MIT License

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## ADHD

- Repository: https://github.com/UditAkhourii/adhd
- Source branch: `main`
- Source commit: `eaeba4e98b388b8d1d31a31572d91ff989e04c00`
- License: MIT
- Copyright notice: Copyright (c) 2026 ADHD contributors

The following is the license text from the pinned ADHD source:

```text
MIT License

Copyright (c) 2026 ADHD contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

## Local modifications

The combined plugin makes these changes to the upstream skill material:

1. Renames the ADHD skill directory and frontmatter from `adhd` to `adhd-ideation`.
2. Narrows ADHD activation to explicit ADHD/divergent-ideation requests and adds a handoff to `super-adhd-child:brainstorming`.
3. Rewrites internal `superpowers:` skill identifiers to the combined `super-adhd-child:` namespace.
4. Adds the `using-super-adhd-child` routing skill.
5. Excludes upstream hooks, plugin manifests, package files, CLI/library code, tests, and runtime dependencies.

6. Adds a compact cross-cutting operational-patterns reference for objective-first execution, evidence-led action, conditional automation, operational fit, proportional communication, and applied learning.

7. Keeps skill frontmatter limited to `name` and `description` while preserving the vendored skill inventory.
8. Adds capability-aware ADHD execution guidance: isolated-subagent detection, capacity-sized batching, inherited model policy, and estimate-only timing/cost language.
9. Clarifies that `/adhd` is not registered by this skills-only plugin and documents the portable explicit invocation.

10. Consolidates Codex collaboration capability, model, lifecycle, and local-verification guidance into `skills/using-superpowers/SKILL.md`; removes the redundant platform-reference bootstrap step.
11. Keeps ADHD-specific isolation in `skills/adhd-ideation/SKILL.md` while moving scoring, trap detection, clustering, ranking, and selection inline to the orchestrator; the default accounting is five divergent roles plus three deepening roles.
12. Removes five excluded debugging development files, records their exact paths in `UPSTREAM_INVENTORY.json`, and enforces the exclusion during validation, offline inventory checks, and deterministic packaging.
13. Removes invalid skill references and redundant dispatch-skill worked examples while preserving the operative workflow gates and review contracts.
14. Corrects the executing-plans host-reference note and documents how Codex maps the generic subagent template to its built-in agents.
15. Replaces unconditional activation delegation with economics-based routing: proactively evaluate delegation, use the cheapest sufficient topology, wait efficiently, and resolve relevant documentation contradictions while preserving manual-first ADHD ideation and high-assurance review gates.

The plugin does not include the ADHD CLI/library or Anthropic Agent SDK dependencies. It also does not remove, alter, or uninstall any standalone ADHD or Superpowers installation.
