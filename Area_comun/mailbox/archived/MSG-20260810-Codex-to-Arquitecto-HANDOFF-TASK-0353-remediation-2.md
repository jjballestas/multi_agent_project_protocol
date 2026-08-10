---
id: MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0353-remediation-2
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0353
status: archived
created: 2026-08-10T06:10:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Commit this handoff and route independent Analista re-review of remediation 2 exact commit 897b9767.
question: Does independent review accept closure A, the real-CLI negative, the derived 63/6/8 balance, and the completed R4 declaration?
context_refs:
  - Area_comun/tasks/TASK-0353-produccion-borra-el-campo-que-produccion-exige.md
  - Area_comun/artifacts/Analista-TASK-0353-r2-tercera-ancla-verdict.md
---

# HANDOFF TASK-0353 remediation 2 -- closure A

Implementation commit: `897b9767`.

## Property closed

`runtime/orchestrator.py` now rejects a routed schema before filtering when that schema omits a
top-level key conditionally required by the live semantic validator. The diagnostic names the
routed-schema/semantic-validation gap; it cannot fall through to the false claim that a producer
omitted a field it actually supplied.

The permanent contract derives the semantic-only requirement set by removing each key from a
valid turn and subtracting unconditional JSON Schema `required`. It requires exact equality with
the production declaration. Today that derived set is `obstacles`.

## Real route and mutation evidence

The repository's historical 1.2.0 schema is installed under another routed root. Both direct
`schema_report()` and the real command below exit non-zero before filtering:

```text
python runtime/orchestrator.py --root <historical-root> --run --once --replay-report <report>
ValueError: routed schema omits top-level keys required by orchestrator semantic validation: obstacles
```

The producer report contains `obstacles: []`. The former false diagnostic, `delivery turn is
missing the obstacles block`, is asserted absent. The ordinary routed delivery remains accepted.
Removing the production guard makes this permanent boundary fail.

## Replay balance derived from this run

Exact commit `897b9767` was replayed in detached clean worktree
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0353r2-897b9767` with a 600-second per-step
cap. The replicator itself emitted:

```text
STEP 36/77 FAIL name=Run intent flow cases
STEP 43/77 FAIL name=Run event auth runtime override cases
STEP 50/77 FAIL name=Run runtime instantiation cases
STEP 53/77 FAIL name=Run runtime Review/QA cases
STEP 58/77 FAIL name=Run runtime loop cases
STEP 59/77 FAIL name=Run supervised autonomy cases
SUMMARY declared=77 pass=63 fail=6 unsupported=8
```

Steps 34, 39, and 40 pass in sequence. The eight PowerShell steps remain unsupported on this host.
No prior balance was transcribed.

## R4 completed

The 0.10.0 runtime snapshot is preserved to verify compatibility, migration, and instantiation from
that published historical contract. It is not an integral parity mirror of the live runtime. Two
contracts deliberately compare only the worktree functions `parse_porcelain_v1_z` and
`dirty_worktree_paths`; those bounded twins do not imply schema or semantic parity.

The live orchestrator always filters and validates with the routed root's schema, while semantic
validation remains live module code. The new pre-filter assertion makes that third anchor explicit
and rejects a historical schema that cannot satisfy the live semantics.

## Gates on exact implementation commit

- routed-turn obstacle property: PASS
- real CLI historical-schema negative: PASS
- falsification inventory: 71 declared / 71 discovered / 0 missing
- collaboration validator: PASS
- encoding: PASS
- domain neutrality: PASS
- Python compile and diff checks: PASS
- clean-worktree status after gates: empty

Residuals remain as declared by independent review: no real Actions run while billing is blocked,
eight PowerShell steps are unsupported locally, `patternProperties` is an inert out-of-scope edge,
and falsification boundary reachability is outside TASK-0353. Codex did not review or ratify this
maker delivery.
