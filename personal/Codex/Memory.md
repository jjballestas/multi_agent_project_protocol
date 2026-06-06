# Codex Memory

Last updated: 2026-06-06 Europe/Madrid

## Repository

`multi_agent_project_protocol` is the canonical, domain-neutral repository for the reusable
multi-agent software project protocol. It dogfoods itself.

Current private area: `personal/Codex/` (DECISION-0016). Do not create new files under legacy `Codex/`.

## Session Close - 2026-06-06

The N-agent program is in progress after the human owner approved/froze Phase 0:

- `DECISION-0015` is accepted.
- `SPEC-0038` is frozen with D-1..D-16, I1..I8 and addenda A1..A13.
- `TASK-0043` Phase 1 is accepted and done.
- `TASK-0044` Phase 2 is accepted and done.
- `TASK-0045` Phase 3 is ready and queued to Codex.

Open mailbox at close:

- `Area_comun/mailbox/open/MSG-20260606-Claude-to-Codex-task0044-accepted.md`
  - FYI only, no response required.
  - TASK-0044 accepted and done.
- `Area_comun/mailbox/open/MSG-20260606-Claude-to-Codex-task0045-fase3.md`
  - Requires Codex response.
  - TASK-0045 READY: N-agent Phase 3 router + fairness.

Git status was clean immediately before updating this memory and creating the startup prompt.

## Latest Completed Work

### TASK-0043 - N-agent Phase 1

Commit: `3430c2c feat(runtime): add agent registry validation`

Delivered:

- `runtime/context.py`
  - `load_agent_registry(root)` with fallback:
    `agent_registry` -> `agent_roles` -> default Claude/Codex/human triad.
  - helpers: `enabled_agents`, `agents_with_capability`, `has_capability`.
- `runtime/turn_schema.json`
  - `agent` changed from fixed enum to non-empty string.
- `runtime/turn_validate.py`
  - semantic validation for registered/enabled/capable agent.
  - preserves `claim.owner == report.agent`.
- `examples/agent_registry_cases/`
  - explicit registry, `agent_roles`, default fallback, unregistered/disabled/uncapable rejection.

Claude accepted TASK-0043.

### TASK-0044 - N-agent Phase 2

Commit: `e5faa1d feat(runtime): add event log concurrency core`

Delivered:

- `runtime/eventlog.py`
  - append-only JSONL event log under `runtime/state/events.jsonl`;
  - writer-only monotonic `seq`;
  - `event_schema_version`;
  - fsync append and torn-write-safe reader;
  - canonical snapshot/replay/hash;
  - archive compaction under `runtime/state/archives/`;
  - idempotency by tuple `actor/task/transition/attempt/fencing`;
  - duplicate intent returns existing event with no new seq, including after compaction;
  - per-aggregate fencing tokens;
  - stale-fencing rejection events without aggregate version bump;
  - negative replay helper that does not invoke external callbacks.
- `runtime/turn_schema.json`
  - optional `attempt_id`, `idempotency_key`, `aggregate_version`, `fencing_token`.
- `runtime/turn_validate.py`
  - optional semantic checks for `aggregate_version` and `fencing_token`.
- `runtime/orchestrator.py`
  - preserves optional concurrency fields in sanitized reports.
- `examples/runtime_eventlog_cases/`
  - seq/torn-write;
  - idempotency pre/post compaction;
  - lease reclaim/stale fencing;
  - snapshot hash/mismatch gate;
  - negative replay.

Claude accepted TASK-0044. Follow-up noted by Claude: when event log becomes the live writer, wire
`assert_snapshot_matches` into py/ps1 global validators as a repo-wide hard gate before writes. This does
not block Phase 3.

## Next Task

`TASK-0045` is ready:

- File: `Area_comun/tasks/TASK-0045-codex-n-agent-fase3-router.md`
- Message: `Area_comun/mailbox/open/MSG-20260606-Claude-to-Codex-task0045-fase3.md`
- Goal: N-agent Phase 3 router + fairness.

Expected scope:

- `runtime/router.py`
- `runtime/context.py` if helper tweaks are needed
- `examples/runtime_router_cases/`
- probably new fairness/routing golden cases
- protocol state/task/mailbox/handoff files for claim and handoff-release

Key requirements from Claude:

- Select by required capability and load.
- `required_capability` optional in tasks; if absent, use current owner behavior.
- Use `routing_weights` from config, not hardcoded constants.
- Exclude author in review/QA, even if author has reviewer/QA capability.
- No hidden escalation: if no eligible reviewer/QA distinct from author, escalate/blocked with reason and candidates; never self-review.
- Deterministic tiebreak:
  - stable hash of `task + transition + agent + routing_epoch`;
  - lexicographic only as final tiebreak.
- Respect `max_active_claims`.
- Add `routing_decision.explanation` with candidates, filtered reasons and score tuple.
- Fairness gate over eligible assignments:
  - 100 tasks / 3 identical agents nearly uniform;
  - weighted expected-vs-observed;
  - anti-starvation if an eligible agent gets zero after minimum sample;
  - guard denominator zero.
- Keep fallback N=2 byte-equivalent:
  - without registry, review -> Claude;
  - human gate -> `operador humano`;
  - current 5 router cases remain green.

## Validation Baseline

Before closing, these suites were green after TASK-0044:

- `python examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py` -> 5/5
- `python examples/agent_registry_cases/run_agent_registry_cases.py` -> 4/4
- `python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py` -> 5/5
- `python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py` -> 5/5
- `python examples/runtime_router_cases/run_runtime_router_cases.py` -> 5/5
- `python examples/runtime_apply_cases/run_runtime_apply_cases.py` -> 4/4
- `python examples/runtime_loop_cases/run_runtime_loop_cases.py` -> 8/8
- `python examples/runtime_observability_cases/run_runtime_observability_cases.py` -> 5/5
- `python examples/llm_adapter_cases/run_llm_adapter_cases.py` -> 6/6
- `python scripts/validate_collaboration_state.py` -> OK
- `python scripts/scan_encoding.py` -> OK
- `python scripts/scan_domain_neutrality.py` -> OK

Run these again after implementing TASK-0045, plus any new router/fairness cases.

## Protocol Reminders

- Read `AGENTS.md` first.
- Before shared edits, inspect:
  - `Area_comun/state/TASK_INDEX.json`
  - `Area_comun/state/CLAIMS.json`
  - `Area_comun/mailbox/open/`
- Create/update an active claim before editing shared routes.
- Do not edit paths covered by another active claim.
- When moving a task to `in_review`, release the active claim in the same coordination step.
- ASCII-only applies to `Area_comun/mailbox/**` and `Area_comun/state/*.json`.
- Keep protocol core domain-neutral.
- Do not introduce secrets.
- Do not change compatibility/boundaries/release policy without decision + human approval.
