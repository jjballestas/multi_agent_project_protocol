# Codex Memory

Last updated: 2026-06-15 Europe/Madrid, after trio stand-down.

## Current Repository State

- Latest observed HEAD before mailbox hygiene: `2e1515a chore(personal): higieniza personal/Claude + actualiza MEMORY/STARTUP_PROMPT a v1.6.0`.
- v1.6.0 is published by Claude: cost-attribution #3 is activated, TASK-0111 is done, and TASK-0113 is done.
- Claude's stand-down FYI was archived after explicit operator request to hygiene Codex mailbox:
  `Area_comun/mailbox/archived/MSG-20260614-Claude-to-Codex-stand-down-cron.md`.
- Expected open mailbox after this hygiene: `.gitkeep` only, unless new messages arrive.
- Coordination after operator request:
  - Codex sent `Area_comun/mailbox/open/MSG-20260614-Codex-to-Claude-coord-next-work.md` asking Claude
    whether there is a new GO or Codex remains in stand-down.
  - Codex answered `Area_comun/mailbox/answered/MSG-20260614-Claude-to-Codex-gate-coupling-readonly-s9.md`.
    ACK: Codex owns the future read-only invariant verification for `protocol_research` coupling/exporters
    post-GATE-DATASET, before any live Core read. No action now; current work remains gate-only/stub-only.
- Operator reactivated Codex for the OFF-PILOT trio and asked for a 5-minute coordination cron with Claude.
  Local monitor is running from `personal/Codex/coord_cron.ps1` every 300 seconds, logging to
  `personal/Codex/coord_cron.log`; stop it by creating `personal/Codex/coord_cron.stop`.
- TASK-0100 is implemented and in `in_review` under DECISION-0037 option A. Scope is future releases:
  `.gitattributes` added for LF checkouts, `dist/v1.1.0/KNOWN_LIMITATIONS.md` documents v1.1.0 as
  pre-normalization with 616 LF / 127 CRLF / 14 no-EOL, `SPEC-0075` has a rescope amendment, and
  `scripts/verify_release.py` emits a visible `release_scope` note for v1.1.0 without suppressing failures.
  Handoff: `Area_comun/handoffs/HANDOFF-TASK-0100-codex-to-claude-1.md`.
  Evidence: release verify harness OK (7 cases), clean HEAD renormalize guard staged only `.gitattributes`,
  validator/encoding/neutrality/drift green. v1.1.0 manifest/signature were not regenerated or edited.
- TASK-0100 was later closed by Claude in v1.9.1. TASK-0095 is now implemented and in `in_review`:
  `runtime/apply.py` derives task markdown paths mutated by turn transitions and includes them in
  `commit_turn`; `examples/runtime_apply_cases` now proves the task `.md` is committed even when omitted
  from `changed_paths`. Handoff:
  `Area_comun/handoffs/HANDOFF-TASK-0095-codex-to-claude-1.md`. Evidence: runtime_apply OK (4),
  runtime_loop OK (15), runtime_real_adapter OK (4), intent_flow OK (11), validator/encoding/neutrality/drift
  green. No active Codex claims expected.
- DECISION-0038 is accepted by operator order: minimal narration is now a primordial rule. AGENTS.md,
  AGENTS.template.md, personal/Codex/STARTUP_PROMPT.md, and personal/Claude/STARTUP_PROMPT.md were hardened:
  no visible process narration, no step announcements/recaps, no non-actionable periodic progress. Only final
  report/handoff, real blocking question, actionable coordination result, or substantive reasoning-as-deliverable.
- TASK-0096 is implemented and in `in_review`: real subprocess invoker runs require an explicit fresh
  `--run-id`; existing `runtime/runs/<run_id>.jsonl` is rejected before invoker execution to avoid run-log
  accumulation and cross-run metrics. Handoff: `Area_comun/handoffs/HANDOFF-TASK-0096-codex-to-claude-1.md`.
  Evidence: llm_adapter OK (6), runtime_real_adapter OK (5), supervised_autonomy OK (10), runtime_loop OK
  (15), runtime_budget OK (5), runtime_observability OK (5), runtime_cost_attribution OK (11),
  validator/encoding/neutrality/drift green. No active Codex claims expected.
- Delivery coordination for TASK-0096 was sent to Claude:
  `Area_comun/mailbox/open/MSG-20260615-Codex-to-Claude-TASK0096-delivery-coordination.md`.
  Commit `3add1c9` remains the implementation commit. Drift stayed 0; no active Codex claims. Validator is
  blocked in the live working tree by an unrelated peer mailbox anomaly:
  `Area_comun/mailbox/open/MSG-20260615-Claude-analista-to-Claude-sync-coordinacion.md` has `status:
  answered` while sitting in `open/`.
- The peer mailbox anomaly was notified to Claude in
  `Area_comun/mailbox/open/MSG-20260615-Codex-to-Claude-mailbox-anomaly-sync-coordinacion.md`. Codex did not
  edit the peer-owned anomalous message.
- Codex mailbox hygiene archived the non-response TASK-0096 delivery FYI:
  `Area_comun/mailbox/archived/MSG-20260615-Codex-to-Claude-TASK0096-delivery-coordination.md`. Validator
  is OK with one unrelated warning for `MSG-20260615-Claude-to-ClaudeAnalista-sync-reply.md`; drift 0 and
  no active Codex claims.
- Claude closed the OFF-PILOT trio and sent Codex stand-down:
  `Area_comun/mailbox/archived/MSG-20260615-Claude-to-Codex-trio-cerrado-standdown.md`. Codex mailbox is
  clean for Codex; only non-Codex open mailbox remains. Local coordination cron was stopped (PID 80672) and
  `personal/Codex/coord_cron.stop` was created locally. Do not take new tasks until operator reactivation.
- Expected active claims: none for Codex.
- Remaining Codex-relevant trio tasks after Claude review are TASK-0095 then TASK-0096, but order is strict.
  Do not claim either without a fresh GO and a mailbox/claims check.
- Runtime flags to preserve: `chain_enabled=false`, `agent_signatures_enabled=false`, `anchor_enabled=false`,
  subagents off, SA.4 not fired. Do not enable #4/chain/auth/anchor without the TASK-0113/#4 gate sequence and
  explicit operator/architect GO.

## Personal Area Hygiene

- `personal/Codex/` is the only Codex private area. Do not use legacy `Codex/`.
- Old root-level intent/claim JSON envelopes were moved to `personal/Codex/archive/intents/` during this refresh.
  They are retained for traceability but should not clutter cold-start reading.
- Root of `personal/Codex/` should stay small: `README.md`, `Memory.md`, `STARTUP_PROMPT.md`, durable reports, and
  archive folders.
- Do not touch `personal/Claude/` or `personal/operador/` unless the operator explicitly asks.

## Operating Rules

- Read `AGENTS.md` first on every cold start, then this memory and `personal/Codex/STARTUP_PROMPT.md`.
- Shared state is runtime-authoritative. Never edit `Area_comun/state/*.json` by hand; use `runtime/submit_intent.py`
  or `runtime/ledger_ops.py --submit`.
- Before editing shared routes, including mailbox, create or update an active claim that covers the route.
- Release a claim when moving work to `in_review`/`done` or when a hygiene step is finished.
- After every Codex commit, update this memory so the next cold start reflects the committed state.
- Stage explicit paths only. Leave unrelated dirty worktree changes alone.

## Known Dirty-Tree Caution

- The worktree may contain unrelated deletions under `personal/Claude/` and untracked `personal/operador/`.
  Treat them as peer/operator state and do not revert or stage them.

## Useful Fresh-Session Commands

```powershell
git status --short
git log -5 --oneline
Get-ChildItem -File Area_comun\mailbox\open | Select-Object -ExpandProperty Name
python scripts\validate_collaboration_state.py --root .
python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), indent=2, ensure_ascii=False))"
```

If a Windows sandbox tempfile test fails with `WinError 5` / `PermissionError`, remember the known inherited-ACL
issue. Re-run only the necessary evidence path and record the caveat.
