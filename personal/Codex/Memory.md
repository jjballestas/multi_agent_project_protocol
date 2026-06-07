# Codex Memory

Last updated: 2026-06-07 Europe/Madrid, after TASK-0063 was delivered to in_review.

## Repository

`multi_agent_project_protocol` is the canonical, domain-neutral repository for the reusable
multi-agent software project protocol. It dogfoods itself.

Current private area: `personal/Codex/` (DECISION-0016). Do not create or use legacy `Codex/`.

## Current State

- Live protocol/runtime version: `0.10.0`.
- v1.0 track is in progress. Functional blocks are complete through the wrapper LLM real.
- Active claims: none.
- `TASK-0061`: done, accepted by Claude.
- `TASK-0062`: done, accepted by Claude. This closed the last functional block before docs/SemVer.
- `TASK-0063`: in_review, owned by Codex, awaiting Claude ratification.
- `python runtime\orchestrator.py --plan` currently returns:
  - `action: answer_mailbox`
  - `task_id: TASK-0063`
  - `owner: Claude`
  - reason: pending response to `MSG-20260607-Codex-to-Claude-anomalia-task0063-go-ledger`
- No ready or in_progress task is currently available to Codex.

## Open Mailbox To Watch

Open messages at refresh included:

- `MSG-20260607-Codex-to-Claude-task0063-in-review.md`
  - requires Claude response.
  - handoff for TASK-0063 docs.
- `MSG-20260607-Codex-to-Claude-anomalia-task0063-go-ledger.md`
  - requires Claude response.
  - materially resolved by later ledger reconciliation, but still open; orchestrator points Claude to it.
- `MSG-20260607-Claude-to-Codex-task0062-accepted.md`
  - FYI, no response required.
- `MSG-20260607-Claude-to-Codex-task0060-accepted.md`
  - FYI, no response required.
- `MSG-20260607-Claude-to-Codex-respuesta-anomalia-task0060.md`
  - answer/FYI, no action required.

Do not claim a new task until TASK_INDEX/PROJECT_STATE show a ready task for Codex and no active claim
conflicts. If Claude answers the TASK-0063 anomaly and/or accepts TASK-0063, re-read the ledger before acting.

## Completed This Session

### TASK-0062 - Wrapper LLM real

Implemented and delivered; Claude accepted it as done.

Key changes:

- `runtime/adapters/llm_adapter.py`
  - command/preset resolver;
  - `runtime.llm_cli_presets`;
  - `runtime.real_invoker` activation check.
- `runtime/orchestrator.py`
  - added `--llm-preset`;
  - real subprocess invoker now requires `--once`, `--allow-real-invoker`, command/preset, and local activation registration.
- `protocol.config.json` and `protocol.config.template.json`
  - `runtime.real_invoker.enabled:false`;
  - example presets `claude` and `codex`.
- `examples/runtime_real_adapter_cases/`
  - deterministic golden cases for activation gates, replay comparison, limits, and presets.
- `.github/workflows/validate.yml`
  - added the real adapter activation cases.
- Minimal docs in `runtime/README.md` and `README_INSTANCIACION.md`.

Validation before handoff included:

- py_compile for touched Python.
- `examples/llm_adapter_cases` 6/6.
- `examples/runtime_real_adapter_cases` 4/4.
- Full runtime suite green.
- validators, encoding, neutrality, prune, and `git diff --check` green.

### TASK-0063 - Docs de adopcion

Implemented and delivered to in_review.

Key changes:

- `README_INSTANCIACION.md`
  - tiers `coordination` and `runtime`;
  - how to instantiate via `new_instance.py --tier`;
  - tier-aware upgrade via `upgrade_instance.py`;
  - safe operation of real agents via DECISION-0021 and wrapper flags;
  - links to runtime docs and N-agent docs.
- `Area_comun/protocol/N_AGENT_RUNTIME.md`
  - registry/capabilities;
  - routing;
  - Review/QA states;
  - claims and handoffs;
  - guardrails/security;
  - observability/event log/replay;
  - budget/deadlines;
  - adoption checklist.
- Handoff:
  - `Area_comun/handoffs/HANDOFF-TASK-0063-codex-to-claude-1.md`
- Review message:
  - `Area_comun/mailbox/open/MSG-20260607-Codex-to-Claude-task0063-in-review.md`

Validation after handoff:

- `python scripts\validate_collaboration_state.py --root .` -> OK, FYI warnings only.
- PowerShell validator -> OK, same FYI warnings.
- encoding scan -> OK.
- neutrality scan -> OK.
- `python scripts\prune_state.py --root . --check` -> OK.
- `git diff --check` -> OK, only CRLF warnings.

## Anomalies / Process Notes

- A TASK-0063 GO appeared before TASK_INDEX/PROJECT_STATE had TASK-0063 and while TASK-0062 was still
  in_review. Codex waited briefly, then sent:
  `MSG-20260607-Codex-to-Claude-anomalia-task0063-go-ledger.md`.
- Claude later reconciled the ledger, accepted TASK-0062, and registered TASK-0063 ready. Codex then
  claimed TASK-0063 normally.
- Keep applying DECISION-0018: notify anomalies via mailbox; do not silently fix another owner's closure.
- Handoff-release must be atomic: task status, handoff, review message, GO archive, and claim release
  should land in the same coordination step.

## Dirty Worktree Caution

The worktree is intentionally dirty with shared task deliverables and Claude coordination changes.
Do not revert unrelated files. Notable dirty/untracked areas seen at refresh:

- Shared deliverables for TASK-0062 and TASK-0063.
- Mailbox moves/archives and handoffs.
- `Area_comun/state/*` hot/archive updates.
- `Area_comun/protocol/N_AGENT_RUNTIME.md`.
- `examples/runtime_real_adapter_cases/`.
- `.claude/settings.json` changed by another participant/tooling; do not touch unless asked.
- `personal/Claude/*` untracked; do not touch.
- `personal/Codex/Memory.md` and `personal/Codex/STARTUP_PROMPT.md` are intentionally updated by this refresh.

Claude usually commits accepted Codex deliverables. Do not commit unless the user asks.

## Working Rules

- Before any shared edit: read `TASK_INDEX.json`, `CLAIMS.json`, and `mailbox/open/`.
- Create/update an active claim before editing shared routes.
- Do not edit routes under another owner's active claim.
- Release claim when moving a task to `in_review` or `done`.
- If a message says DONE but ledger disagrees, wait/recheck briefly; if persistent, notify via mailbox.
- Private notes under `personal/Codex/` do not need a shared claim.

## Useful Fresh-Session Commands

```powershell
git status --short
python runtime\orchestrator.py --plan
python scripts\validate_collaboration_state.py --root .
python scripts\prune_state.py --root . --check
python scripts\scan_encoding.py --root .
python scripts\scan_domain_neutrality.py --root .
```

## Next Session Rule

Start in monitoring/coordination mode. First expected action belongs to Claude: answer/close the open
TASK-0063 anomaly message and review TASK-0063. If Claude accepts TASK-0063 and enqueues D2.4, inspect
GO/spec/task/ledger and claims before claiming.
