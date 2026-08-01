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

The plugin does not include the ADHD CLI/library or Anthropic Agent SDK dependencies. It also does not remove, alter, or uninstall any standalone ADHD or Superpowers installation.
