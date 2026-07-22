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
  -AgentProvider Anthropic `
  -AcceptedTypes REVIEW,REQUEST,ACTION,QUESTION,DECISION

# Any other agent CLI: it MUST read the prompt from STDIN.
powershell -ExecutionPolicy Bypass -File scripts/harness/peer_mailbox_cron.ps1 `
  -PeerId Codex -PromptFile scripts/harness/prompts/implementer.prompt.md `
  -AgentExe "C:\path\to\your-agent.exe" -AgentArgs @("run","--stdin")
```

`-AgentProvider Anthropic` resolves `claude` and uses Claude Code print mode with the
rendered prompt on STDIN. Authentication stays in local CLI state/environment and must
never be written to the repository. `-AgentProvider Codex` retains the prior default and
is the tested rollback path. A live checker cutover remains an operator action: stop the
current cron, launch the desired provider, verify its startup log, and reverse those two
steps to roll back. The runtime directory is unchanged, so seen signatures, PID guards,
locks, and leases retain their contract across provider changes.

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
- Every agent exec ends with exactly one structured line: `OUTCOME: confirmed`,
  `OUTCOME: transient`, or `OUTCOME: definitive`. Exact token equality is authoritative,
  and the token must be the last non-empty transcript line. Earlier quoted/example tokens
  do not count. Precedence is terminal token, process exit code, then peer evidence from a
  signed `runtime/state/events.jsonl` event whose `actor` equals the invoked peer and whose
  bytes were appended after the pre-exec file-length baseline. The pre-exec prefix is
  SHA-256 checked byte for byte before reading that tail; a rewrite, compaction, restoration,
  or reordering makes evidence unavailable instead of shifting the window. The evidence
  window never depends on sequence ordering. Git author names are never attribution evidence. If the
  pre-exec head is unreadable, the runner defers without invoking the agent; it never
  substitutes a sequence baseline. If no such event exists, this layer does not confirm. Free-text regexes are
  legacy fallback only and never override a token, non-zero exit, or signed own evidence.
- `seen.json` is written only after confirmed work or a definitive, principled negative.
  Transient and unconfirmed aborts stay
  unseen and use `retry.json`: three attempts by default, 30-second backoff, then a
  `RETRY_EXHAUSTED ... signal=watchdog` log record. A changed message signature resets
  the retry budget. Pre-exec defers (ledger, snapshots, residue probe, or fresh index/worktree
  residue) have their own counter and watchdog signal but consume no agent-attempt budget;
  they remain eligible and resume automatically when the environmental veto clears.
- The pre-exec residue gate uses full NUL-delimited `git status --porcelain -z`, not only the
  index. Paths with spaces or non-ASCII bytes are never quoted or escape-parsed. Fresh
  unstaged residue therefore defers with a retry signal. The probe runs inside the lock's
  cleanup path. A lock without an exec lease is
  self-healed as orphaned; the complete lock-held setup is covered by one cleanup path.
- Transient rollback snapshots the pre-exec index and restores only that index while HEAD
  is stable: it unstages to the captured HEAD, then gates `git apply --cached` by exit code.
  It never runs `git reset --hard` and never snapshots or re-applies a worktree patch, so
  concurrent tracked content remains byte-for-byte untouched. Newly created untracked files
  are moved, never deleted, into `.protocol-tmp/rollback-quarantine/`; every move has isolated
  error handling and emits `ROLLBACK_QUARANTINED path=<original> quarantine_path=<stored>`
  after success. The quarantine is retained for 30 days. Only the human operator or Arquitecto
  may remove an entry, during an explicit maintenance checkpoint and only after confirming that
  its contents have been recovered or are no longer needed; the peer loop never deletes it.
  `Area_comun/mailbox/**` and the other ledger-managed routes recognized by
  `Test-LedgerManagedPath` are never quarantined. Untracked enumeration is exit-code gated
  before any move. Ledger advancement is decided only by the shared exact event-log head
  primitive (`seq` plus last-line SHA-256), checked before the exec and before restoration.
  Rollback is conservative by default: it runs only while the ledger is
  readable and unchanged, when residue is provably local to the exec. Any signed event,
  torn tail, unreadable line at any position, or other uncertainty defers mutation and leaves
  the tree recoverable. It never decides safety from route, event-kind, or change-name lists.
  `ROLLBACK_LEDGER_PRESERVED` requires a second head read, replay-drift check, and on-disk
  fingerprint comparison for every dirty path. A failed proof reports
  `ROLLBACK_LEDGER_DRIFT`; an unreadable ledger reports `ROLLBACK_DEFER` while the retry loop
  remains alive.
- Retryable causes are temporary coordination conditions: red pre-gate, another owner's
  active claim, a peer write in flight, resource-lock contention, or dirty/staged residue
  left by an aborted exec. Non-retryable causes are principled checker NO-GO/change_required,
  explicit scope rejection, and out-of-scope refusal. These are consumed once and never
  retried automatically.
- Before a transient return, the runner unstages and restores only paths that were absent
  from the pre-exec status snapshot. Pre-existing user or peer changes are preserved.
  Staged files newer than `-AbortedResidueMinutes` are treated as live work and defer the
  exec; an older immobile staged set is reported as aborted residue. Commits, process
  existence, and CPU are not used as the live-vs-aborted discriminator.
- The hook/prune peer-gate deadlock has two coordinated exits: release the blocking peer
  claim, or make exactly one `--no-verify` commit after running the underlying validator,
  encoding, neutrality, and drift gates manually and recording that evidence. Never turn
  the bypass into a persistent config change.

## Platform note

Reference implementation is PowerShell 5.1+ (Windows). The mechanics (lock, lease, seen,
STDIN exec) are platform-neutral by design; a POSIX/Python port is future work and must keep
the same runtime-state contract so watchdogs stay compatible.
