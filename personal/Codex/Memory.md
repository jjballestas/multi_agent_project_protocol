# Codex Memory

Last updated: 2026-06-13 Europe/Madrid, after delivering TASK-0106 context compaction.

## Repository

`multi_agent_project_protocol` is the canonical, domain-neutral repository for the reusable multi-agent
software project protocol. It dogfoods itself.

Private area: `personal/Codex/` (DECISION-0016). Do not create or use legacy `Codex/`. Do not touch
`personal/Claude/` or `personal/operador/` unless explicitly asked.

## Current Expected State

- Latest Codex delivery commit: `38a48fe feat(runtime): add context compaction policy`.
- TASK-0106 is `in_review`; Codex claim `CLAIM-20260613-task0106-codex` is released. Handoff:
  `Area_comun/handoffs/HANDOFF-TASK-0106-codex-to-claude-1.md`.
- Runtime drift after handoff-release: `has_drift=false`, `up_to_seq=401`.
- TASK-0106 implemented the minimum safe SPEC-0078/DECISION-0031 scope:
  `runtime.context_policy` off by default, compact turn context, tool-result clearing via runlog summaries,
  deterministic warning/fallback, close-summary gate only when compaction is enabled, `delegate_subagent`
  isolated and off by default, and measured context-cost baseline.
- Baseline artifact: `Area_comun/artifacts/baseline-context-20260613.json`.
  Cold-start slim/full: `9346`/`19676` tokens; turn-context compact/full: `22092`/`42752`; delta: `20660`.
- TASK-0106 gates run before commit: py_compile OK; context_policy GC-1..GC-9 OK; context_cost cases OK;
  runtime_loop 15 OK; runtime_budget 5 OK with elevation due sandbox temp ACL; llm_adapter 6 OK with elevation
  due sandbox temp ACL; domain neutrality OK; collaboration validator OK; drift 0. Encoding scan still fails on
  historical mailbox messages not touched by TASK-0106.
- Open mailbox after this delivery should still include operator/current coordination messages; Claude owns review
  closure for TASK-0106.
- Current TASK-0093 delivery is re-entered after Claude's `changes_requested` review:
  - Claude rejected the first TASK-0093 handoff because release-on-rejection was missing for pre-apply rejection
    paths. Mailbox finding: `MSG-20260609-Claude-to-Codex-task0093-changes-requested.md`.
  - Codex acquired `CLAIM-20260609-task0093-fix-rejection-codex`, implemented cleanup for orchestrator-acquired
    claims on pre-apply stops, added runtime_loop goldens, delivered
    `Area_comun/handoffs/HANDOFF-TASK-0093-codex-to-claude-2.md`, moved TASK-0093 back to `in_review`, and
    released the claim.
- Sandbox/tempfile coordination:
  - Codex opened `MSG-20260609-Codex-to-Claude-request-tempfile-acl-sandbox.md` for Claude to verify whether the
    Windows sandbox `unelevated` + Python `tempfile` ACL failure reproduces on his side and to decide runbook vs
    hardening task.
- Important recent commits:
  - `6a9b21e`: Claude personal checkpoint after sandbox unelevated fix and TASK-0093 mid-ratification.
  - `720b417`: Claude root-caused the sandbox failure to Windows `sandbox="elevated"` / os error 740 and
    documented the `unelevated` fix.
  - `8d2734f`: after TASK-0093 checkpoint, Codex asked Claude to verify the operator hypothesis that the
    sandbox failures may correlate with Codex CLI installation; temporary maintenance claim was acquired/released,
    mailbox request opened, drift 0 at seq 172.
  - `d6569f4`: TASK-0093 first delivery to `in_review`; orchestrator acquires routed owner claims before adapter,
    terminal outcomes release claims automatically, runtime_loop goldens cover missing-claim/pre-claim/conflict,
    handoff created, claim released, drift 0 at seq 170.
  - `88e8ea5`: TASK-0092 done, executed by Claude while Codex agent was down; codex invoker implementer and
    full-turn prompt contract integrated.
  - `79814ff`: Claude acknowledged Codex's anomaly report; changes were authorized and normalized; anomaly reply
    opened for Codex.
  - `8926f39`: SA.4 was re-armed and TASK-0091 moved blocked->ready for the codex-invoker pilot.
  - `4923c62`: stale TASK-0092 GO was archived after TASK-0092 was already done.
  - `89d140b`: SA.4 was de-armed again after the pilot was rejected by the gate (`no active claim`).
  - `b04b791`: Claude's startup prompt was refreshed for the post-pilot state.
- `protocol_version=1.1.0`, `runtime_version=0.11.0`.
- `event_state.enabled=true`, `materialize=true`, `enforce=true`, `authoritative=true`.
- Runtime drift last observed after tempfile coordination: `has_drift=false`, `up_to_seq=187`,
  hash `e63a17339195733d454c0d7a8c36440c4e45b6a0b566ef3de0898d157e1314f9`.
- `runtime.real_invoker.enabled=false` and `runtime.supervised_autonomy.enabled=false`. Do not re-arm or run the
  SA.4 pilot without explicit operator/Claude GO.
- `TASK-0092` is `done`; its stale GO has been archived. Do not claim it.
- `TASK-0091` is `ready` in the ledger, but it is the SA.4 pilot target. Because SA.4 is de-armed after the
  `no active claim` gate rejection, do not manually claim/run it without a fresh architect/operator GO.
- `TASK-0093` is `in_review`; latest handoff:
  `Area_comun/handoffs/HANDOFF-TASK-0093-codex-to-claude-2.md`. Claims
  `CLAIM-20260609-task0093-codex` and `CLAIM-20260609-task0093-fix-rejection-codex` are released.
- `TASK-0087` remains proposed for Claude.
- Active claims expected: none.

## Open Mailbox To Expect

- `MSG-20260609-Claude-to-Codex-anomalia-task0092-resuelta.md`
  - FYI, no response required; explains TASK-0092 changes were authorized and normalized.
- `MSG-20260609-Codex-to-Claude-fyi-sandbox-spawn-setup-refresh.md`
  - FYI from Codex to Claude about the sandbox failure pattern.
- `MSG-20260609-Claude-to-Codex-response-liveness-sandbox.md`
  - Claude response: Codex in VS Code is push-driven; checkpoint/commit before restart; then restart app-server or
    VS Code; later create shared runbook.
- `MSG-20260609-Claude-to-Codex-task0093-changes-requested.md`
  - Review finding for TASK-0093. Codex responded by implementing release-on-rejection and re-delivering handoff 2;
    Claude still needs to ratify and archive/close as appropriate.
- `MSG-20260609-Codex-to-Claude-request-tempfile-acl-sandbox.md`
  - Codex request to Claude: verify whether the Python tempfile ACL issue reproduces under sandbox unelevated and
    choose runbook vs hardening task.

The old TASK-0092 GO is no longer open; it was archived in `4923c62`.

Validators warn when FYI/no-response messages remain in `open/`; that is hygiene debt, not a hard failure.

## Sandbox Diagnosis And Fix

The Windows sandbox failed in this session before some commands executed:

`windows sandbox: spawn setup refresh`

Confirmed findings:

- In this running session, `Write-Output SANDBOX_OK` still failed inside the sandbox but worked with escalation.
- The failure happens without `workdir`, so it is not caused by this repo or `D:\Agentes`.
- TEMP is writable and disk space is fine.
- Re-running the same commands with `sandbox_permissions: require_escalated` works.
- The validator and drift check can still succeed sandboxed; treat isolated `spawn setup refresh` failures as
  environment noise and re-run only the needed command with approval.
- A separate `codex exec -s read-only` run from this repo confirmed it is a separate session that can see
  TASK-0093/claim state from disk, but it also reproduced `windows sandbox: spawn setup refresh` for some reads.
- Claude's root-cause hypothesis was verified against official docs and local state: the Codex CLI install/update
  rewrote shared user config under `C:\Users\johnb\.codex`. `config.toml` was written on 2026-06-09 03:23 and
  `.codex-global-state.json`/`.bak` on 2026-06-09 03:14. That user config is shared by CLI and extension.
- Local config previously had `[windows] sandbox = "elevated"`. Official Codex docs say `elevated` is preferred on
  Windows, but `unelevated` is the documented fallback when elevated/admin setup fails.
- The operator applied the fix: `C:\Users\johnb\.codex\config.toml` now has:

```toml
[windows]
sandbox = "unelevated"
```

Operational next step: restart VS Code / the Codex app-server so the running process reloads `~/.codex/config.toml`.
This current session may continue to fail until restart because it likely loaded the old sandbox configuration.

Post-restart verification passed for the basic sandbox path:

1. `Write-Output SANDBOX_OK` without escalation -> OK.
2. `Get-Content`/state reads generally work without escalation again.
3. `python scripts\validate_collaboration_state.py --root .` without escalation -> OK.
4. Drift check -> false.

Remaining sandbox caveat: Python `tempfile.TemporaryDirectory()` creates directories with restrictive mode
(`0o700`); under Windows sandbox `unelevated`, those directories can become unreadable/unwritable to the sandboxed
process. Suites using `%TEMP%` may fail sandboxed with `WinError 5` / `PermissionError` and pass outside the
sandbox. This affected `runtime_real_adapter`, `llm_adapter`, `intent_flow`, and sometimes `scan_encoding`.

If sandbox still fails after restart, collect `C:\Users\johnb\.codex\.sandbox\sandbox.log` and compare whether the
failure is now from `unelevated` setup rather than elevated UAC/error 740. Do not re-fire SA.4 while sandbox health
is red; the pilot invokes `codex exec` non-interactively and may hit the same setup path.

## Hygiene / Golden Rules Notes

- Operator golden rule (DECISION-0026): after every commit, each agent updates its own memory. For Codex, update
  this file after any Codex commit and after observing a peer commit that materially changes the expected state.
- Observation from golden-rule verification: Claude's personal memory files looked stale versus recent commits
  (`personal/Claude/MEMORY.md` still dated 2026-06-05; startup prompt still old). Do not edit Claude's memory.
- Shared-state mode is authoritative. Never edit `Area_comun/state/*.json` by hand. Use
  `runtime/submit_intent.py` or `runtime/ledger_ops.py --submit`.
- Before shared edits: read `TASK_INDEX.json`, `CLAIMS.json`, `PROJECT_STATE.json`, and `mailbox/open/`.
- Create/update an active claim before editing shared routes, including mailbox. Release it when done.
- If an anomaly is detected, notify via `Area_comun/mailbox/open/` with one concrete actionable question.

## Hygiene Verification Snapshot

Recent checks:

- `python scripts\validate_collaboration_state.py --root .` -> OK with warnings for FYI/no-response messages in
  `mailbox/open/`.
- `protocol_state_drift(Path('.'))` -> `has_drift=false`, latest observed `up_to_seq=187`, hot hash equals replay hash.
- PowerShell validator -> OK with the same warnings.
- `examples\mailbox_status_cases` -> OK.
- `examples\compact_comms_validation_cases` -> OK.
- `examples\mailbox_hygiene_cases` failed: its legacy expectation treats resolved messages in `open/` as warnings,
  but the newer status-folder gate makes `status: answered` in `open/` a hard mismatch. Treat as a likely obsolete
  harness needing triage, not as proof the live repo is invalid.

## Dirty Worktree Caution

Expected dirty/untracked areas after this refresh:

- `.claude/scheduled_tasks.lock` deleted; leave it alone unless the operator asks.
- `personal/Codex/Memory.md` and `personal/Codex/STARTUP_PROMPT.md` from this refresh/update.
- `personal/Codex/REPORT-20260609-sandbox-spawn-setup-refresh.md` untracked.
- `personal/operador/` may remain untracked; leave it alone.

Do not revert unrelated changes or peer/operator work.

## Useful Fresh-Session Commands

```powershell
Write-Output SANDBOX_OK
git status --short
git log -5 --oneline
Get-ChildItem -File Area_comun\mailbox\open | Select-Object -ExpandProperty Name
python scripts\validate_collaboration_state.py --root .
python scripts\prune_state.py --root . --check
python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), indent=2, ensure_ascii=False))"
```

If the first command fails with `windows sandbox: spawn setup refresh`, the sandbox is still broken; escalate only
when needed and ask the operator to restart Codex/app-server if the `unelevated` config has not yet been loaded.

## 2026-06-09 - TASK-0094 tempfile/ACL hardening committed

- Commit `18d8162 fix(runtime): harden temp ACL write path` formalized TASK-0094 and moved it to `in_review`.
- TASK-0094 posture B was ratified by the operator: the temp ACL rule is not in `AGENTS.md`; it lives in
  `Area_comun/protocol/RUNBOOK-windows-sandbox-temp-acl.md`.
- Runtime write-path hardening now uses `runtime/temp_paths.py` for repo-local inherited-ACL temp dirs:
  `runtime/protocol_replay.py` materialization staging, `runtime/submit_intent.py` runtime-state backups, and
  `runtime/apply.py` runtime-state backups no longer use OS `%TEMP%` helpers.
- Harnesses requested by the GO were hardened where needed so they pass inside the Codex Windows sandbox:
  `runtime_protocol_replay_cases`, `runtime_protocol_materialize_cases`, `materialize_cross_fs_cases`,
  `intent_flow_cases`, and `runtime_real_adapter_cases`.
- Evidence before commit/release: materialize 7 OK, cross-FS 2 OK, replay 6 OK, intent_flow 11 OK,
  runtime_loop 15 OK, runtime_real_adapter 4 OK, validator OK, neutrality OK, encoding OK.
- Post-release drift: `has_drift=false`, `up_to_seq=211`; TASK-0094 claims released; handoff:
  `Area_comun/handoffs/HANDOFF-TASK-0094-codex-to-claude-1.md`.
- Do not include TASK-0093 v2 leftovers in TASK-0094 follow-up commits: `runtime/orchestrator.py`,
  `examples/runtime_loop_cases/run_runtime_loop_cases.py`, and
  `Area_comun/handoffs/HANDOFF-TASK-0093-codex-to-claude-2.md` remain separate worktree changes for Claude's
  TASK-0093 closure path.

## 2026-06-10 - TASK-0098 human guide generator committed

- Commit `9076528 feat(P2): TASK-0098 human guide generator` delivered the deterministic HUMAN_GUIDE renderer:
  `scripts/generate_human_guide.py`, `scripts/generate_human_guide.ps1`,
  `Area_comun/protocol/HUMAN_GUIDE.template.html`, `examples/human_guide_cases/run_human_guide_cases.py`,
  CI wiring, pre-commit hook, TASK-0098 handoff, mailbox unblock/blocker audit, and materialized runtime state.
- TASK-0098 is `in_review`; Codex claim `CLAIM-20260610-task0098-resume-codex` is released. Latest observed drift
  before commit was `has_drift=false`, `up_to_seq=268`.
- Claude applied the required prune as `orchestrator` before Codex resumed; `python scripts/prune_state.py --root .
  --check` was green (`cold_start_tokens` around 16k). Codex does not have `orchestrator` and must not run
  `protocol_prune` as itself.
- Gates run by Codex before delivery: human guide cases OK, template `--check` OK, prune check OK, collaboration
  validator OK, domain neutrality 0, encoding clean, drift 0.
- Open mailbox after the commit may still contain the original TASK-0098 GO, Claude's unblock response, and Codex's
  prune blocker audit. They are related to the TASK-0098 review/closure path; let Claude ratify and close/archive
  them unless the operator asks for hygiene.
- SA.4/Capa C stayed off; no pilot was run.

## 2026-06-10 - TASK-0099 external-command signing backend accepted

- Claude committed `aeaa12c feat(P2): TASK-0099 done - backend de firma external-command configurable
  (DECISION-0023 sec.4)`.
- TASK-0099 is `done`; Claude ratified the external-command backend adversarially:
  vendor-neutral, no secrets, `subject_digest == manifest.sbom_hash` binding before backend execution, fixture
  HMAC byte-equivalent, deterministic goldens, and `.py/.ps1` parity.
- Open FYI `MSG-20260610-Claude-to-Codex-task0099-accept-done.md` was archived by Codex under
  `CLAIM-20260610-task0099-accept-fyi-archive-codex`; claim released. Drift after archive release:
  `has_drift=false`, `up_to_seq=288`.
- Current hygiene caveat: two Codex-owned blocked claims remain intentionally not released because releasing them
  may raise released-claim ratio and trigger `protocol_prune`: `CLAIM-20260610-task0098-codex` and
  `CLAIM-20260610-task0099-prune-blocker-codex`. Let Claude/orchestrator decide prune+cleanup timing.
- Latest observed checks after FYI archive: collaboration validator OK, mailbox/open only `.gitkeep`, drift 0.
- SA.4/Capa C stayed off; no pilot was run.

## 2026-06-13 - Mailbox coordination hygiene committed

- Commit `6a31345 chore: archive consumed mailbox coordination` archived consumed mailbox messages and the
  Codex/Claude commit-boundary exchange, plus persisted Codex personal intent traces.
- Boundary confirmed by Claude before commit: leave `Area_comun/specs/SPEC-0078-compaction-y-subagentes.md`,
  `Area_comun/tasks/TASK-0106-codex-compaction-subagentes.md`, `personal/Claude/pending_intents/*`, and
  `__sync_probe__.txt` out of Codex staging. TASK-0106 remains gated pending operator GO/review.
- Open mailbox after the commit should contain only `MSG-20260613-Operador-GO-DECISION-0014-0030.md` unless
  newer messages arrive.
- Pre-memory-update checks: collaboration validator OK; runtime drift `has_drift=false`, `up_to_seq=385`; no active
  claims after releasing `CLAIM-20260613-coord-boundary-archive-codex`.

## 2026-06-13 - TASK-0106 GO acknowledged

- Commit `dccb447 chore: acknowledge task0106 go` moved
  `MSG-20260613-Claude-to-Codex-GO-TASK-0106.md` from `mailbox/open/` to `mailbox/answered/` and added Codex's
  explicit ACK.
- Codex confirmed to Claude: run `scripts/measure_context_cost --baseline` before freezing DELTA-1/2/4
  thresholds or cadences; AC7/AC8/GC-8/GC-9 must use measured values or remain null/provisional.
- Codex confirmed DELTA-3 stays outside TASK-0106 and any future implementation must go through `submit_intent`;
  `subagents_enabled` stays off without explicit operator GO.
- Runtime state stayed authoritative and clean before commit: validator OK, drift `has_drift=false`,
  `up_to_seq=395`. Claim `CLAIM-20260613-task0106-go-ack-codex` was acquired and released.
- Next TASK-0106 implementation must start with a fresh claim and measurement baseline, then implement only the
  minimum safe scope from SPEC-0078/DECISION-0031.

## 2026-06-13 - TASK-0106 baseline tooling clarification acknowledged

- Commit `02b3f92 chore: acknowledge baseline tooling clarification` answered Claude's reminder
  `MSG-20260613-Claude-to-Codex-clarif-baseline-tooling.md`.
- Important correction: current `scripts/measure_context_cost.py` does not have `--baseline`; first TASK-0106
  measurement can use `python scripts/measure_context_cost.py --root . --json` and persist that output as the
  baseline artifact before freezing thresholds/cadences.
- Adding a `--baseline` mode remains optional/clean as part of TASK-0106 deliverables if it fits SPEC-0078.
- Runtime stayed clean before commit: validator OK, drift `has_drift=false`, `up_to_seq=397`. Claim
  `CLAIM-20260613-task0106-baseline-clarif-ack-codex` was acquired and released.
