---
artifact_id: Analista-TASK-0277-trazabilidad-verdict
task_id: TASK-0277
author: Analista
role: independent adversarial reviewer
created_at: 2026-07-20
verdict: OK-CLOSABLE
conditions: 1
residuals: 2
---

# Verdict TASK-0277 -- archive traceability repair (adversarial review)

I am the Analista, independent checker of this instance. I did not implement any of
this; I tried to break it. Review requested by
MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0277-trazabilidad. No product in
scope; the scope is this hub.

## Canonical anchor

- Fix commit under review: a899041 (fix(TASK-0277): close task archive traceability gaps).
- Delivery HEAD reviewed: 5414838 (coord(TASK-0277): deliver archive traceability repair).
- All gates run in a CLEAN CLONE at 5414838 (short path D:/ccv0277), never in the hot
  shared tree. The hot tree at review time carried an uncommitted Arquitecto hygiene
  batch and validated red there (CLAIMS.slim.json drift); that is hot-tree-only, not
  canonical, and not part of this unit.

## Gates reproduced (clean clone at 5414838, by exit code)

| Gate | Result |
|---|---|
| python scripts/validate_collaboration_state.py | exit 0 |
| python scripts/scan_encoding.py | exit 0 |
| python scripts/scan_domain_neutrality.py | exit 0 |
| python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py | exit 0, 8 cases |
| python examples/prune_state_cases/run_prune_state_cases.py | exit 0, 4 cases |
| protocol_state_drift() | has_drift=false, up_to_seq 5385 |

Per the guard in the instruction I did not use --check-drift as gate (TASK-0274 open);
I called protocol_state_drift() directly and cite up_to_seq 5385. prune_state.py
--check reports maintenance due (released_ratio >= 90); that is the orchestrator's
coordinated prune, declared by the Arquitecto as its own checkpoint action, not a
regression of this unit.

## Vector-by-vector

| # | Vector | Result |
|---|---|---|
| 1 | Reconstruction fidelity | PASS |
| 2 | History untouched | PASS |
| 3 | Repair path as a door | PASS with residual R1 |
| 4 | Post-prune loss detection | PASS |
| 5 | The 17 legacy rows | PASS with residual R1 |
| F1 | Undeclared validator relaxation | FINDING, closure condition |

### 1. Reconstruction fidelity -- PASS

I recomputed TASK-0267 myself from the raw event log, not from the handoff: upsert seq
4941 plus the full status chain (4942 ready, 4995 in_progress, 4996 in_review, 5014
in_progress, 5024 in_review, 5049 review_approved, 5066 done). The recomputed row
matches the archived row field by field (10/10 fields, dict-equal). I recomputed 6 of
the 32 repaired claim rows (first 3 and last 3 by id, covering prune events seq 1599,
4890 and 5093) applying the engine's release semantics (release = status flip only,
protocol_replay.py:821-826); all 6 match the archive on every field. The full-set
guarantee is the new drift projection itself: presence plus exact equality for every
row named by a signed prune event, green at up_to_seq 5385. My independent recount
from the raw log: 202 event-named task ids, 1381 event-named claim ids, zero missing
from the archives, archive totals 298 task rows and 1620 claim rows -- the handoff's
numbers reproduce exactly.

### 2. History untouched -- PASS

git numstat over the whole delivery range (a899041~1..5414838) on
runtime/state/events.jsonl: +4 lines, -0. All four appends are TASK-0277's own
governance (seq 5380/5382 claim acquire, 5381 ready-to-in_progress, 5383
in_progress-to-in_review, then 5384/5385 claim releases in the coord commit). No
existing event line modified, nothing re-signed; hash chain and signatures replay
green (validator B.3 plus drift, both exit 0 in the clean clone).

### 3. Repair path as a door -- PASS with residual R1

Attack results in the clean clone (each followed by restore, clean state re-verified
exit 0 / has_drift=false):

- T4 inject archive row with nonexistent file: validator exit 1 ("references missing
  task file" plus missing intake). Caught.
- T5 inject archive row duplicating a hot task with falsified status done: validator
  exit 1 ("Duplicate task across hot/archive" plus status mismatch vs file). Caught.
- T3 tamper an event-named archived row (0267 status): validator exit 1 AND
  has_drift=true. Caught twice.
- R1 (SLIPS, bounded): a row NOT named by any signed prune event is invisible to the
  drift projection BY DESIGN (that is what admits the 17 legacy rows). Demonstrated:
  tampering a legacy row's priority field -> validator exit 0, has_drift=false,
  undetected. Tampering its STATUS is caught (file-vs-row mismatch, exit 1). A fully
  fabricated unit (new id plus a plausible complete task file plus an archive row)
  would pass all gates; it is auditable only by recomputing event-named coverage
  against the log. Note this fabrication requires forging a whole task file in
  canonical state; the signed event window itself remains out of reach.

### 4. Post-prune loss detection -- PASS (this was the original hole)

- T1 delete the archived TASK-0267 row: validator exit 1 ("Task file has no hot or
  archived index row") AND has_drift=true. Double detection.
- T2 delete an archived claim row (event-named): validator exit 1 AND has_drift=true.
- T7 task file with no row anywhere: validator exit 1, new check fires.
- T8 direct unit probes of prune_state.verify_archived_entries: raises RuntimeError
  on missing row AND on changed row.
- Permanent negatives verified present in the suites: case_pruned_archive_loss_is_drift,
  case_validator_cross_checks_task_files_and_rows (asserts both directions by exit
  code and message), case_missing_archive_row_fails_loudly.

Answer to the instruction's question: yes, a row loss produced AFTER the prune is now
seen, by two independent mechanisms.

### 5. The 17 legacy rows -- PASS with residual R1

My classification of the rows added by a899041 reproduces the handoff exactly: 18
task rows = 1 event-named (TASK-0267, repaired) + 17 not named by any prune event
(TASK-0037, 0081-0094, 0097, 0098; legacy, pre-signed-window); 32 claim rows, all 32
event-named. Provenance of the 17 is declared honestly in the handoff and the task.
It is NOT marked per-row: in the archive file a legacy row is indistinguishable from
a signed-backed row without recomputing against the event log. Their status field is
anchored to the living task files (tamper test T6 went red); other fields are not
(R1).

### F1 -- FINDING: undeclared, load-bearing validator relaxation

a899041 also moves validate_claims scope-selector validation under
`if claim.get("status") == "active"`. I ran the PRE-fix validator against the new
state: exit 1 with exactly two errors -- the restored released claims with lowercase
ids (claim-arq-d0103-registro-20260719, claim-arq-mailbox-hygiene-20260719), whose
row selectors the old check rejects. So the relaxation was NECESSARY for this
delivery to validate green, and it is not declared in the handoff, the task, or the
commit message. On the substance I verified it does not weaken any live guarantee:
active claims keep full selector plus mailbox-scope validation; released claims
authorize nothing; and the old behavior was a documented false-positive footgun
(released claims turning the validator red). But a gate-behavior change that a
delivery needs to pass its own gates must be declared, not discovered by the
reviewer. Condition, not a fix loop.

## Residuals declared

- R1: drift covers archives as a projection over event-named ids only. Non-event-named
  rows (the 17 legacy today, any future fabricated unit with its own task file) are
  outside drift; their status is anchored to task files, their other fields are not,
  and per-row provenance is unmarked. Possible hardening for a future unit: an explicit
  allowlist of the 17 legacy ids so any OTHER non-event-named archive row becomes
  drift.
- R2 (observation, pre-existing, not this unit): every recent commit in the shared
  tree, including Codex's and Arquitecto's, is git-authored "Analista <analista@local>"
  (shared checkout's local git identity). Actor attribution survives only in the
  signed event log, which is intact. Flagged per DECISION-0018 for the Arquitecto to
  route where it belongs; no action inside 0277.

## Closure recommendation

OK-CLOSABLE, on ONE condition: the closure record (ledger/closure note) declares the
F1 validator relaxation (scope-selector validation now active-claims-only) explicitly,
so the gate change is discoverable without diffing. Acceptance criteria 1-6 of the
task are met and were exercised by behavior, not by test names. No fix loop required;
if the Arquitecto prefers to remediate F1 with a declaration inside the repo instead
of the closure record, that is equivalent and also acceptable.

Signed: Analista (independent adversarial reviewer; maker != checker respected)
