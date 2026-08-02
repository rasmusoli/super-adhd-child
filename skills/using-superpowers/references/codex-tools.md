## Codex collaboration capability reference

Use this reference when a workflow needs isolated subagents, parallel
branches, continuation, or cleanup. Capability names are host-specific and
must be checked in the current Codex surface before dispatching.

### Detect before dispatch

- If the current surface exposes isolated subagents, use that capability and
  read its actual concurrency limit. Run independent branches in
  capacity-sized batches; never assume five workers are available.
- If isolated subagents are unavailable, say so. A sequential root-context
  simulation does not preserve an isolation invariant. Stop or offer a
  clearly labeled degraded workflow; do not pretend it is equivalent.
- Keep branch prompts independent. Do not pass one branch's output to another.

The local Codex desktop surface verified while maintaining this plugin exposed
the `multi_agent_v1` spawn and wait operations. Treat those names as an
observation for that surface, not as a portable plugin API. Other Codex
surfaces may expose different operation names or no isolated-subagent support.

### Model policy

Inherit the current model by default. Specify a model override only when the
current environment supports it and user/platform policy permits it. Never
invent model names or override an explicit user constraint. Use task
complexity to choose among permitted options, not to force a model selection.

### Lifecycle and cleanup

Use the currently exposed operations for dispatch, waiting, continuation, and
cleanup. Do not document or call a fixed cleanup operation name.
If the current surface exposes cleanup, use it after the relevant branch or
review completes. If it does not, wait for completion and let finished work
terminate naturally, recording the limitation rather than editing Codex
configuration.

### Local verification

Before changing this guidance, verify the local surface with read-only checks
such as `codex --version`, the available collaboration capability, and the
current repository branch/worktree state. Do not ask users to edit Codex
configuration unless a setting is verified locally and is necessary for the
requested workflow.
