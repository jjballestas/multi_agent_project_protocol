# Peer harness -- operational layer of a protocol instance

This folder ships the **launchable runtime for peer agents** (implementer / reviewer) so an
instance is *born operational*: the governance skeleton (ledger, validators, config) plus the
mechanism that actually runs the agents. It unifies the per-peer mirror scripts the hub
instance evolved (`codex_mailbox_cron.ps1` / `analista_mailbox_cron.ps1`) into one
parameterized runner.

## Contents

- `peer_mailbox_cron.ps1` -- generic mailbox-driven cron for ONE peer agent.
- `prompts/implementer.prompt.md` -- neutral role prompt template for the maker.
- `prompts/reviewer.prompt.md` -- neutral role prompt template for the adversarial checker.

## How it works

The runner polls `Area_comun/mailbox/open/` for messages addressed `to: <PeerId>` that are
actionable (`requires_response: true`, or a non-empty `requested_action`, or `type` in the
accepted set). For each new message it renders the prompt template (substituting the runtime
tokens below), launches the agent CLI ONCE with the prompt on STDIN, and records the message
as seen (`name|length|mtime` signature -- editing a message re-triggers it).

Runtime tokens substituted into the prompt template per execution:

| Token | Value |
|---|---|
| `@@MESSAGE_PATH@@` | root-relative path of the message being processed (required in template) |
| `@@ROOT@@` | absolute path of the governance root (forward slashes) |
| `@@PEER_ID@@` | the `-PeerId` argument |
| `@@COORDINATOR_ID@@` | the `-CoordinatorId` argument (default `Arquitecto`) |

Tokens use `@@...@@` on purpose: `{{...}}` is reserved by the instancing renderer
(`new_instance.py`) and must not appear in shipped files.

## Launch examples

```powershell
# Implementer (maker) peer named Codex, reference CLI (codex) auto-discovered:
powershell -ExecutionPolicy Bypass -File scripts/harness/peer_mailbox_cron.ps1 `
  -PeerId Codex -PromptFile scripts/harness/prompts/implementer.prompt.md

# Reviewer (adversarial checker) peer named Analista, narrowed message types:
powershell -ExecutionPolicy Bypass -File scripts/harness/peer_mailbox_cron.ps1 `
  -PeerId Analista -PromptFile scripts/harness/prompts/reviewer.prompt.md `
  -AcceptedTypes REVIEW,REQUEST,ACTION,QUESTION,DECISION

# Any other agent CLI: it MUST read the prompt from STDIN.
powershell -ExecutionPolicy Bypass -File scripts/harness/peer_mailbox_cron.ps1 `
  -PeerId Codex -PromptFile scripts/harness/prompts/implementer.prompt.md `
  -AgentExe "C:\path\to\your-agent.exe" -AgentArgs @("run","--stdin")
```

Customize per instance by COPYING a template (e.g. `prompts/codex.prompt.md`) and editing:
add your product paths, your instance's decision references, your quality gates. If
`-PromptFile` is omitted the runner looks for `prompts/<peerid-lowercase>.prompt.md`.

## Runtime state (`.protocol-tmp/`) -- born at first run, never committed

The runner creates `<root>/.protocol-tmp/<peerid>_mailbox_cron/` on first start: `*.lock`
(one exec at a time), `*.pid` + `*.pid.json` (single-instance guard by PID + process start
time), `*.exec-lease.json` (heartbeated lease of the running exec, used by watchdogs and by
the self-heal), `*.seen.json` (processed-message signatures), `runs/*.{prompt.txt,out.log,err.log}`.
Keep `.protocol-tmp/` gitignored. **Do not create it by hand and do not expect it to exist
before the first run.**

## Stopping a peer

1. Stop marker: create `<runtime-dir>/<peerid>_mailbox_cron.stop` (graceful; waits for the
   current exec).
2. STOP_JOB order: a mailbox message from the coordinator to the peer whose
   `requested_action` or `one_line_summary` is EXACTLY `STOP_JOB` (case-sensitive equality;
   mere mentions of stop words never trip it).
3. Idle exit: after `-MaxNoCoordinatorRounds` rounds without coordinator activity the cron
   exits by itself.

## Safety mechanics (inherited from the hub's hardened harness)

- Single instance per peer (PID + process start time match).
- Exec lease with heartbeat; expired/orphaned execs are tree-killed EXCEPT when the child
  command line matches the deny list (ledger writes, git, test runners) -- never kill a
  ledger write in flight.
- Stale lock self-heal on start and before each exec.
- Deadline (`-ExecTimeoutSeconds`) enforced per exec.

## Watchdogs (coordinator side)

The runner is one half of the operational layer; the coordinator arms watchdogs over it
(delivery monitor, exec-health via lease+frozen-run-log, mailbox hygiene threshold). See the
methodology skills shipped with the instance (`.claude/skills/` for Claude-based
coordinators, `skills/session-watchdogs` in the neutral layer).

## Migrating from the hub's per-peer scripts

The runner keeps the same runtime-state paths (`.protocol-tmp/<peerid>_mailbox_cron/`), so
the single-instance guard works across old/new and `seen.json` is inherited without
reprocessing. Two DEFAULTS differ from the historical per-peer scripts -- pass the flags to
preserve old behavior:

- The reviewer peer historically did NOT trigger on `GO`/`HANDOFF`; the generic default
  accepts both. Narrow it: `-AcceptedTypes REVIEW,REQUEST,ACTION,QUESTION,DECISION`.
- The implementer peer historically ran `model_reasoning_effort=low`; the generic default
  is `medium`. Pass `-ReasoningEffort low` to keep the old cost/latency profile.

## Operational cautions

- **Agent path vs tree-kill deny-list:** the expired-exec tree-kill refuses to kill a
  process whose command line matches the deny list (`submit_intent`, `git `, `npm test`,
  `vitest`, `validate_collaboration_state`) -- protection against killing ledger writes.
  Do not use `-AgentExe`/`-AgentArgs` values CONTAINING those substrings (e.g. a path like
  `D:\tools\vitest-agent\agent.exe`), or an expired exec becomes unkillable by the runner.
- **Verify the resolved root:** the startup log line prints `root=...`. If you copied the
  harness into a tree without its own `protocol.config.json`, the upward walk can anchor to
  an ENCLOSING instance's config -- check that line on first launch.
- A failed exec marks the message as seen (inherited design: no retry storms). To re-trigger
  a message, edit it (the signature is name|length|mtime) or remove its entry from
  `seen.json`.

## Platform note

Reference implementation is PowerShell 5.1+ (Windows). The mechanics (lock, lease, seen,
STDIN exec) are platform-neutral by design; a POSIX/Python port is future work and must keep
the same runtime-state contract so watchdogs stay compatible.
