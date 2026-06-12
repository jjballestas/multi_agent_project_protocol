# Startup Prompt For Next Session

You are Codex in `d:\Agentes\multi_agent_project_protocol`.

Read first:

1. `AGENTS.md`
2. `personal/Codex/Memory.md`
3. `Area_comun/state/PROJECT_STATE.json`
4. `Area_comun/state/TASK_INDEX.json`
5. `Area_comun/state/CLAIMS.json`
6. `Area_comun/mailbox/open/`

Then run:

```powershell
Write-Output SANDBOX_OK
git status --short
git log -5 --oneline
Get-ChildItem -File Area_comun\mailbox\open | Select-Object -ExpandProperty Name
python scripts\validate_collaboration_state.py --root .
python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), indent=2, ensure_ascii=False))"
```

If the first command fails with `windows sandbox: spawn setup refresh`, the running app-server probably has not
reloaded the fixed Windows sandbox config yet, or the fallback setup is still failing. Current expected user config:

```toml
[windows]
sandbox = "unelevated"
```

This setting lives in `C:\Users\johnb\.codex\config.toml`, outside the repo, and is shared by the CLI and the
extension app-server. It was changed after the CLI install/update caused the config to use `elevated`, which needs
administrator-approved setup and failed in background app-server contexts. Official Codex docs say `elevated` is
preferred on Windows, but `unelevated` is the documented fallback when elevated setup fails.

If the sandbox still fails after restart, collect `C:\Users\johnb\.codex\.sandbox\sandbox.log`, use only necessary
escalated commands, and do not re-fire SA.4.

Current expected state when this prompt was written:

- Latest observed committed HEAD before the current uncommitted delivery: `6a9b21e chore(personal): checkpoint Claude pre-restart (sandbox unelevated fix + TASK-0093 in_review mid-ratificacion)`.
- `TASK-0093` is `in_review`, with
  `Area_comun/handoffs/HANDOFF-TASK-0093-codex-to-claude-2.md`; claims
  `CLAIM-20260609-task0093-codex` and `CLAIM-20260609-task0093-fix-rejection-codex` are released.
  Claude should ratify the release-on-rejection fix next.
- `TASK-0092` is `done`; its old GO has been archived. Do not claim it.
- `TASK-0091` is `ready` in the ledger, but it is the SA.4 pilot target. SA.4 is currently de-armed after the
  pilot was rejected by the gate (`no active claim`), so do not manually claim/run it without a fresh
  architect/operator GO.
- `TASK-0087` remains proposed for Claude.
- `protocol_version=1.1.0`, `runtime_version=0.11.0`.
- `event_state.enabled/materialize/enforce/authoritative` are all `true`.
- Drift expected: `has_drift=false`, last observed `up_to_seq=187`.
- `runtime.real_invoker.enabled=false` and `runtime.supervised_autonomy.enabled=false`; do not re-arm or run SA.4
  without explicit GO.
- Active claims expected: none.
- Expected mailbox/open includes Claude's TASK-0092 anomaly-resolution FYI and Codex's sandbox FYI. Both are
  `requires_response: false` hygiene warnings only.
- Expected mailbox/open also includes Claude's liveness/sandbox response, Claude's root-cause response, the old
  TASK-0093 GO, Claude's TASK-0093 changes_requested review, Codex's answered liveness/root-cause requests, and
  Codex's new `MSG-20260609-Codex-to-Claude-request-tempfile-acl-sandbox.md`.
- Codex sent `MSG-20260609-Codex-to-Claude-request-tempfile-acl-sandbox.md`; wait for Claude to verify whether the
  Python `tempfile` ACL failure reproduces under Windows sandbox `unelevated` on his side, then decide runbook vs
  hardening task.
- Sandbox root cause/fix status: correlation with the Codex CLI install/update was verified enough for operation.
  `C:\Users\johnb\.codex\config.toml` is shared by CLI and extension and now sets `[windows] sandbox = "unelevated"`.
  Basic sandbox commands now work, but Python `tempfile.TemporaryDirectory()` / `os.mkdir(..., 0o700)` can create
  directories inaccessible to the sandboxed process (`WinError 5` / `PermissionError`). Suites using tempdirs may
  need an escalated rerun until Claude and Codex agree on a runbook or hardening task.

Rules to keep front of mind:

- Golden memory rule: after every commit, update `personal/Codex/Memory.md`.
- Do not edit `Area_comun/state/*.json` by hand; use `submit_intent` / `ledger_ops --submit`.
- Before shared edits, check TASK_INDEX, CLAIMS, PROJECT_STATE, and mailbox/open.
- Claim before editing any shared route, including mailbox; release the claim when done.
- Do not touch `personal/Claude/` or `personal/operador/` unless explicitly asked.
- Do not revert unrelated dirty work.

Copy-paste instruction for another session:

```text
Lee AGENTS.md y personal/Codex/Memory.md. Luego revisa PROJECT_STATE, TASK_INDEX, CLAIMS y mailbox/open. Ejecuta Write-Output SANDBOX_OK, git status --short, git log -5 --oneline, el validador y el drift check. Estado esperado: TASK-0093 in_review con handoff 2 a Claude y claim liberado, TASK-0092 done, TASK-0091 ready pero reservado como objetivo del piloto SA.4, SA.4 disabled, authoritative true, sin claims activos, drift 0 up_to_seq 187. Sandbox Windows: ~/.codex/config.toml debe tener [windows] sandbox = "unelevated"; si suites Python con tempfile fallan sandboxed con WinError 5/PermissionError, reintenta fuera del sandbox y espera la coordinacion con Claude en MSG-20260609-Codex-to-Claude-request-tempfile-acl-sandbox.md. No rearmes SA.4 ni corras piloto.
```

Update after commit `18d8162 fix(runtime): harden temp ACL write path`: TASK-0094 is now `in_review` with
`Area_comun/handoffs/HANDOFF-TASK-0094-codex-to-claude-1.md`; all TASK-0094 claims are released; drift was 0 at
seq 211 after release. The Windows temp ACL rule is posture B: not in `AGENTS.md`, documented in
`Area_comun/protocol/RUNBOOK-windows-sandbox-temp-acl.md`. Runtime write-path temp dirs use
`runtime/temp_paths.py`. TASK-0093 v2 leftovers remain separate in the worktree and must not be folded into
TASK-0094.

Update after commit `9076528 feat(P2): TASK-0098 human guide generator`: TASK-0098 is `in_review` with
`Area_comun/handoffs/HANDOFF-TASK-0098-codex-to-claude-1.md`; Codex claims are released; latest observed drift
was 0 at seq 268. The generator lives in `scripts/generate_human_guide.py` plus `.ps1`, with golden cases in
`examples/human_guide_cases/`, generated template HTML at `Area_comun/protocol/HUMAN_GUIDE.template.html`, and
CI/pre-commit checks wired. Claude already applied the prune as orchestrator; Codex must not run
`protocol_prune` as itself. Wait for Claude to ratify/close TASK-0098 and then TASK-0037. Do not re-arm SA.4,
do not run a pilot, and do not touch personal/Claude, personal/operador, or `.claude/scheduled_tasks.lock`.
