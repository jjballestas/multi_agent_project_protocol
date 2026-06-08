# Supervised autonomy

> Operational guide for the supervised-autonomy envelope introduced by
> `DECISION-0024` and specified in `SPEC-0064`. This document describes the
> SA.1-SA.3 envelope that already exists. It does not activate SA.4, does not
> enable real multi-turn agents, and does not change runtime defaults.

## Purpose

Supervised autonomy lets the runtime observe and bound a multi-turn loop with
explicit stops, audit output and reversible configuration. The envelope is
domain-neutral and off by default.

The implemented scope is:

- SA.1: activation registry, `caps.max_turns` and `*.runreport.md`.
- SA.2: pause sentinel `runtime/state/PAUSE` and wall-clock cap
  `caps.wall_clock_ms`.
- SA.3: human checkpoint through `caps.human_checkpoint_every_k` or repeated
  review/QA fix-cycles.

SA.4, the real subprocess invoker running for more than one turn under this
envelope, remains gated. It requires an explicit operator GO, a registered
activation and a rehearsed rollback. Until that separate step lands, the real
subprocess invoker still requires `--once`.

## Configuration

The runtime block is present in `protocol.config.json` and template instances,
but it is disabled by default:

```json
{
  "runtime": {
    "supervised_autonomy": {
      "enabled": false,
      "activation_decision": "",
      "approved_by": "",
      "approved_at": "",
      "caps": {
        "max_turns": 5,
        "human_checkpoint_every_k": 2,
        "wall_clock_ms": 300000
      }
    }
  }
}
```

The runtime accepts supervised autonomy only when all of these are true:

- The caller passes `--allow-supervised-autonomy`.
- `runtime.supervised_autonomy.enabled` is `true`.
- `activation_decision`, `approved_by` and `approved_at` are non-empty.
- `caps.max_turns` is an integer `>= 1`.
- `caps.wall_clock_ms` is an integer `>= 0`.
- `caps.human_checkpoint_every_k` is an integer `>= 1`.

If any registry field or cap is missing, the run fails closed with an activation
error. If the flag is omitted, the runtime behaves as the regular loop and does
not apply the supervised caps or write a supervised run report.

## Running recorded turns

The safe exercised path is the recorded invoker. It is deterministic, uses local
transcripts and needs no network or credentials:

```powershell
python runtime\orchestrator.py --run `
  --adapter llm `
  --llm-invoker recorded `
  --replay-report <transcript-or-dir> `
  --max-iter 5 `
  --allow-supervised-autonomy
```

Tests may pass `--clock-fixed <ms>` to make wall-clock behavior deterministic.
The cap `max_turns` still bounds the effective loop even if `--max-iter` is
higher.

## Hard stops

Every stop is explicit in the run log. Ambiguity stops closed rather than
continuing silently.

| Stop | Trigger | Outcome | Resume rule |
|---|---|---|---|
| Turn cap | `caps.max_turns` reached while more input remains | `max_turns_reached` | Human starts a new run if appropriate. |
| Pause sentinel | File `runtime/state/PAUSE` exists before the next turn | `paused` | Remove the sentinel and start a new run. |
| Wall-clock cap | Accumulated duration would exceed `caps.wall_clock_ms` before the next turn | `wallclock_exhausted` | Human reviews and starts a new run if appropriate. |
| Human checkpoint | `caps.human_checkpoint_every_k` turns complete while work remains | `human_checkpoint` with `human_required:true` | Human review required; no auto-resume. |
| Fix-cycle checkpoint | Repeated review or QA cycles reach `quality_policy.max_review_cycles` or `quality_policy.max_qa_cycles` | `human_checkpoint` with `human_required:true` | Human review required; no auto-resume. |

All pre-existing runtime stops still apply: pre-gate failures, routing escalation
to a human, task deadlines, budget limits, schema errors, human outcomes,
undeclared dirty worktree changes and post-gate failures.

## Pause sentinel

The pause sentinel is an operational kill-switch between turns. Create the file
before the next turn should stop:

```powershell
New-Item -ItemType Directory -Path runtime\state -Force
New-Item -ItemType File -Path runtime\state\PAUSE -Force
```

To allow a later run, remove the sentinel:

```powershell
Remove-Item -LiteralPath runtime\state\PAUSE
```

The sentinel is not a task artifact. It is an operator control file and should
not be committed as protocol source.

## Run report

When supervised autonomy is active for a run, the orchestrator writes:

- `runtime/runs/RUN-<id>.jsonl`
- `runtime/runs/RUN-<id>.summary.json`
- `runtime/runs/RUN-<id>.runreport.md`

The human-readable `*.runreport.md` includes:

- final outcome.
- turns recorded.
- total declared token cost.
- total duration in milliseconds.
- activation decision, approver and approval date.
- `caps.max_turns`, `caps.wall_clock_ms` and
  `caps.human_checkpoint_every_k`.
- per-turn task, outcome, reason, cost, commit and validation errors.

Use the report as the review surface before starting any follow-up run. A run
ending in `human_checkpoint`, `paused`, `wallclock_exhausted` or
`max_turns_reached` is not an automatic failure; it is the envelope stopping at
an intentional boundary.

## Real invoker boundary

The real CLI wrapper and supervised autonomy are separate gates:

- `runtime.real_invoker` controls whether a subprocess LLM can be called at all.
- `runtime.supervised_autonomy` controls the multi-turn supervision envelope.

In the current implemented state, SA.1-SA.3 do not lift the real-invoker
`--once` lock. A real subprocess command still needs:

```powershell
python runtime\orchestrator.py --run `
  --adapter llm `
  --llm-invoker subprocess `
  --once `
  --allow-real-invoker `
  --llm-preset codex
```

SA.4 is the only step that may allow a real subprocess loop to run for more than
one turn, and it remains blocked until the operator gives explicit GO plus a
rollback rehearsal. This document is not that GO.

## Safe operation checklist

1. Keep `runtime.supervised_autonomy.enabled:false` until the local operator
   approves activation.
2. Record the activation decision, approver and date in the local instance.
3. Set conservative caps before the first run.
4. Use recorded transcripts for tests and CI.
5. Use `runtime/state/PAUSE` to stop before the next turn.
6. Treat `human_checkpoint` as a hard boundary; do not auto-resume.
7. Review `*.runreport.md` before any follow-up run.
8. Keep credentials and real CLI auth outside the repository.

## References

- `Area_comun/decisions/DECISION-0024-autonomia-supervisada.md`
- `Area_comun/specs/SPEC-0064-autonomia-supervisada.md`
- `Area_comun/protocol/N_AGENT_RUNTIME.md`
- `runtime/orchestrator.py`
- `runtime/supervised_autonomy.py`
- `examples/supervised_autonomy_cases/`
