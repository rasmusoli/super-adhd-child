---
name: using-superpowers
description: Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** — including clarifying questions, exploring the codebase, or checking files. If it turns out wrong for the situation, you don't have to use it.

**Before entering plan mode:** if you haven't already brainstormed, invoke the brainstorming skill first.

Then announce "Using [skill] to [purpose]" and follow the skill exactly. If it has a checklist, create a todo per item.

## Skill Priority

When multiple skills apply, process skills come first — they set the approach, then domain skills carry it out. Brainstorming and systematic-debugging are Superpowers' most common process skills, but the rule holds for any of them.

- "Let's build X" → super-adhd-child:brainstorming first, then domain skills.
- "Fix this bug" → super-adhd-child:systematic-debugging first, then domain skills.

## Operational Defaults

For implementation, diagnosis, architecture, automation, research, documentation,
or learning tasks, read [`operational-patterns.md`](operational-patterns.md) and
apply only the relevant guidance. It is a compact decision aid, not a mandatory
workflow: simple tasks stay direct; material-risk tasks get explicit assumptions,
rollback, and verification.

## Codex collaboration policy

Proactively evaluate delegation without waiting for a second user request.
Use the cheapest sufficient execution topology. Delegation requires
independently separable work, at least one meaningful benefit (isolation,
specialization, parallelism, controller-context preservation, cheaper
execution, independent verification, or durable long-running execution), and
expected benefit that exceeds assignment cost, handoff cost, waiting cost,
review cost, likely repair cost, context reconstruction, and added wall-clock
delay. Use practical judgment; numeric token calculations are not required.

### Lightest sufficient topology

- **Direct execution:** Use the main agent for trivial, short, tightly coupled,
  highly context-dependent, clarification-heavy, or faster-inline work. One-line
  edits, small config changes, narrow command generation, and tightly coupled
  bug fixes may remain inline.
- **One Reader:** Use one read-only worker for bounded exploration when a concise
  evidence report preserves substantial controller context. Dispatch once,
  consume one final report, and do not automatically follow it with a Builder.
- **One Builder:** Use one implementation worker for a bounded scope with clear
  acceptance criteria, a bounded edit surface, and focused self-verification.
  One Builder or direct execution may be sufficient; do not automatically add
  a Reader, Builder, Tester, Reviewer, or documentation worker.
- **Builder plus independent review:** Extra review requires risk or
  verification justification, such as security, authentication or
  authorization, public contracts, migration or data integrity, concurrency,
  subtle correctness, broad integration, production impact, meaningful
  regression risk, or an explicit independent-verification requirement. The
  reviewer must add independent evidence, not repeat trustworthy unchanged
  tests.
- **Parallel workers:** Use parallel workers only for genuinely independent
  domains with no shared mutable state or overlapping files, when integration
  is safe and parallelism creates meaningful wall-clock benefit. Do not
  maximize worker count merely because capacity exists.
- **Full subagent-driven development:** Reserve the high-assurance workflow for
  approved written plans, multiple meaningful tasks, important integrations,
  broad changes, substantial context or time, or work where per-task review
  materially reduces risk. Preserve fresh per-task implementers, review gates,
  repair loops, ledgers, final whole-branch review, and
  finishing-a-development-branch. Never spawn ceremonial agents.

When a workflow needs isolated subagents, detect the capability exposed by the
current Codex surface and read its actual concurrency limit. Use independent
branches in capacity-sized batches; never assume five workers or a fixed
operation name. If isolated subagents are unavailable, say so: sequential
root-context reasoning is not equivalent isolation. Stop or offer a clearly
labeled degraded workflow, and never pretend it preserves the invariant.

On Codex, `Subagent (general-purpose):` is a cross-platform template marker:
it maps to Codex's `default` built-in agent. `worker` and `explorer` are
available for read-write and read-only splits. Dispatch by writing a direct
natural-language delegation instruction (for example, `Spawn a subagent:
<task>. Wait for it, then report back <X>.`), not a formal tool call.

Keep branch prompts independent and do not pass one branch's output to another.
Use the inherited model by default. Specify an override only when the
environment exposes it and user/platform policy permits it; never invent model
names or override an explicit constraint. Use the currently exposed operations
for dispatch, waiting, continuation, and cleanup. If cleanup is unavailable,
let completed branches terminate naturally and report that limitation.

### Waiting and handoff

After dispatch, use the current host's native blocking wait, completion event,
wait-thread, or equivalent efficient lifecycle feature when available. Detect
the capability and do not hard-code the feature name or a lifecycle operation
name. Do not use live monitoring, repeated short waits, short status polling,
filesystem polling solely to see whether work started, or evidence-free
check-ins. Resume coordination only when the worker completes, reports a
blocker or defect, a meaningful timeout expires, or the user intervenes. If
the host cannot wait efficiently, use its least expensive supported behavior
and report that limitation honestly. For external processes, use one suitable
wait or condition-based waiting when the next action depends on a real
observable condition.

Keep file-based handoffs. Give workers only the task ID, desired outcome,
assigned and protected scope, acceptance criteria, source paths, validation
expectation, and return contract. Do not paste full conversation history,
repeated summaries, old logs, completed-task history, or an entire plan when a
bounded task brief is enough. Make reports evidence-driven and detailed in a
file when necessary; do not request routine progress narration.

### Documentation-consistency preflight

Before delegating related multi-step project work, inspect the smallest
relevant set of approved requirements, active implementation plan, durable
project documentation, current interfaces and contracts, relevant tests, and
actual current code behavior. Look for material contradictions, including
conflicting APIs, stale architecture, obsolete tests, overlapping ownership,
or documentation for missing files. Resolve material contradictions at the
coordinator level before workers act; do not silently choose a source of truth.
Do not perform a repository-wide documentation audit unless the task requires
it.

Before changing this guidance, use local read-only checks such as `codex
--version`, the available collaboration capability, and the current repository
branch/worktree state.

## Red Flags

These thoughts mean STOP—you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## User Instructions

User instructions (CLAUDE.md, AGENTS.md, GEMINI.md, etc, direct requests) take precedence over skills, which in turn override default behavior. Only skip skill workflows or instructions when your human partner has explicitly told you to.
