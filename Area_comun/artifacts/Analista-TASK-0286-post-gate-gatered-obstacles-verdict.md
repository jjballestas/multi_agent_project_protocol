---
artifact_id: Analista-TASK-0286-post-gate-gatered-obstacles-verdict
reviewer: Analista
task_id: TASK-0286
verdict: OK-CLOSABLE
created_at: 2026-07-23
implementation_commit: e7feb7771870254d946bb8bcc6d83af0b3da7970
protocol_head: b961724
scope: no product in scope (governance/runtime only)
---

# VERDICT - TASK-0286, C3/E7 gate-red objetivo post-gate -> obstacles: OK-CLOSABLE

Voice: Analista (independent adversarial checker). This verdict gates the closure of
TASK-0286. Sin producto en alcance.

## Canonical anchor

- Implementation commit under review: `e7feb7771870254d946bb8bcc6d83af0b3da7970` ("feat(TASK-0286):
  enforce post-gate obstacle evidence").
- Protocol HEAD at review time: `b961724`.
- Method: clean clone to `D:/ccv286`, `git checkout e7feb777`, gates run THERE by exit code; plus
  my own adversarial payloads driven through the REAL `RunLog.append` entrypoint. Canonical state
  green before review (`validate_collaboration_state.py` exit 0).

## Reproduction (clean clone e7feb777, gate by exit code)

```
EXIT=0 :: python examples/runtime_turn_cases/run_post_gate_obstacle_cases.py
EXIT=0 :: python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py
EXIT=0 :: python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py
EXIT=0 :: python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
EXIT=0 :: python scripts/check_falsification_contracts.py --inventory   (permanent_negatives=26 declared=26 missing=0)
EXIT=0 :: python scripts/test_falsification_contracts.py
EXIT=0 :: python scripts/validate_collaboration_state.py
EXIT=0 :: python scripts/scan_encoding.py
EXIT=0 :: python scripts/scan_domain_neutrality.py
PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=6112
```

Note N1 (task doc, non-blocking): the task `verification_cmd[0]` cites
`examples/runtime_turn_cases/run_runtime_turn_cases.py`, which does NOT exist and never has
(git history over that path is empty; grep finds no reference in code). The real runners are the
four decomposed ones above (schema/semantic/obstacle/post-gate), all exit 0. The behavioral
coverage the acceptance demands is fully met; only the umbrella filename in the intake is stale.

## Vector-by-vector

| # | Vector | Result | Evidence |
|---|--------|--------|----------|
| 1 | Entrypoint REAL (red/empty rejected via `RunLog.append`, no unit shortcut) | PASS | The guard `validate_post_gate_obstacles(entry)` is the FIRST line of `RunLog.append` (runlog.py:25), before the file write. All 17 run-log writes in orchestrator.py route through `runlog.append`; the only `open("a")` on `runtime/runs/*.jsonl` is inside `append` itself (runlog.py:27). No bypass path exists. My own payloads driven through the real `append` reject red/absent and red/empty. |
| 2 | `gate_green` is the OBJECTIVE gate result, not a relabel-able report field | PASS | orchestrator.py:1123 sets `gate_green=result.get("green")` where `result = apply_gate_and_commit(...)`. `turn_entry` takes `gate_green` as a separate kwarg and does NOT read it from `report`. Probe #6: an agent report with `gate_green:True` while the objective gate is `False` is still REJECTED. Every one of the 7 `apply_gate_and_commit` return paths yields a strict Python bool `green` (True/False); the final `except` re-raises. So `is False` is sound for the real path. |
| 3 | Anti-theater: `gate_green:true` does NOT require obstacles | PASS | Guard only fires on `gate_green is False`. Probe: green/absent ACCEPTED. Mirror of 0259; no prose forced. |
| 4 | Negative with mutation NEG-POST-GATE-RED-OBSTACLES (26/26, 0 missing) | PASS | `check_falsification_contracts --inventory`: permanent_negatives=26 declared=26 missing=0. `test_falsification_contracts.py` exit 0: the mutation `source.replace("        validate_post_gate_obstacles(entry)\n","")` is REAL (asserts `mutant != source`), removing the call makes red/empty ACCEPTED, and the clean impl rejects it with the actionable error. Not a bounce-noop. |
| 5 | E7 limit documented (objective here; auto-declarables in 0259) | PASS | README (examples/runtime_turn_cases/README.md:22-25): "The post-gate runner covers the objective C3/E7 boundary after the gate result... Self-declared transition and revert signals remain in `turn_validate.py`." Task/intake also states the split. |
| 6 | Does NOT touch turn_validate.py or the schema | PASS | Diff of e7feb777 = state files + task files + README + `run_post_gate_obstacle_cases.py` + `runlog.py` + runtime/state. No `turn_validate.py`, no `turn_schema`. Confirmed by diff-stat, grep, and history. Matches Arquitecto recompute. |

## Independent adversarial payloads through the REAL append (results)

```
REJECTED :: red/absent  (gate_green=False, no obstacles)
REJECTED :: red/empty-list  (gate_green=False, obstacles=[])
REJECTED :: agent report claims gate_green=True but objective gate_green=False
ACCEPTED :: green/absent  (anti-theater)
ACCEPTED :: red-as-None (gate_green=None)         -> see R1
ACCEPTED :: red-as-int-0 / red-as-str-false (raw)  -> see R1 (unreachable in real orchestrator)
ACCEPTED :: red + obstacles=[''] / ' ' / [{}]      -> see R2
```

## Declared residuals (non-blocking)

- R1 (boundary/robustness, NOT a live escape): the strict `entry.get("gate_green") is False` check
  is sound ONLY because the upstream contract guarantees `gate_green` is a strict Python bool. I
  verified this holds across all `apply_gate_and_commit` return paths, and `turn_entry` passes it
  through untouched, so a red gate ALWAYS arrives as `False` in the real orchestrator. The
  `None`/`0`/`"false"` ACCEPTs above are hand-crafted dicts that the real path never produces
  (`None` means "gate did not run", the correct semantics for pre-gate/rejected/human/budget
  entries). Recommendation, optional: a future change that made `green` a non-bool truthy/falsy
  value would silently disable the guard; a one-line normalization (`gate_green in (False,)` is
  fine as-is, or coerce) or a comment pinning the invariant would harden it. Low risk today.

- R2 (anti-theater residual, matches the literal criterion): the guard enforces PRESENCE /
  non-emptiness of `obstacles`, not content quality. `obstacles=['']`, `' '`, `[{}]` are truthy and
  pass. This is symmetric with the deliberate anti-theater stance (review item 3: green does not
  force prose) and matches the acceptance wording ("obstacles vacio/ausente" = falsy). Policing
  content would invert anti-theater. Documented as a residual, not a defect.

- N1 (task doc nit): `verification_cmd[0]` names a non-existent runner (see Reproduction). Suggest
  the Arquitecto correct the task's `verification_cmd` to the four real runners. Does not gate
  closure.

## Closure recommendation

OK-CLOSABLE. The core guarantee (review item 1) holds by BEHAVIOR through the real
`RunLog.append`: an objective red gate (`gate_green:false` from `apply_gate_and_commit`) with
empty/absent obstacles is rejected with an actionable error, the agent cannot relabel the
objective result, green stays narration-free, the mutation is real and the falsification inventory
is 26/26 with 0 missing, the E7 boundary is documented, and neither `turn_validate.py` nor the
schema is touched. All cited gates exit 0 in the clean clone; drift CLEAN. Residuals R1/R2/N1 are
declared and non-blocking. Cierre a discrecion del Arquitecto (done-flip).

-- Analista
