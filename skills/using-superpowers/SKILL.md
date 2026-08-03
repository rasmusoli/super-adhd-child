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

Before changing this guidance, use local read-only checks such as
`codex --version`, the available collaboration capability, and the current
repository branch/worktree state.

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
