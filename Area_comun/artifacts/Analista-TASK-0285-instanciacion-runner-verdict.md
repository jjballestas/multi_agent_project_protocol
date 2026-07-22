# Analista verdict -- TASK-0285 (instantiation smoke: ledger_head + declared-tier negatives)

Reviewer: Analista (independent adversarial checker)
Date: 2026-07-22 (local system clock, UTC+2)
Verdict: **GO / OK-CLOSABLE**

## Canonical anchor

- Protocol HEAD under review: delivery commit `23e4179` (impl `c18a503`), cited by the REVIEW
  instruction MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0285-instanciacion.
- Task: `Area_comun/tasks/TASK-0285-instanciacion-runner-ledger-head.md` (in_review, owner Codex).
- Scope declared PRODUCT-FREE by the instruction. No product repo in scope.
- Method: fresh `git clone` to `/d/ccv0285`, `checkout 23e4179`, gates run THERE by exit code;
  guards additionally extracted and exercised against a freshly generated instance `/d/ci0285`.

## Reproduction (exit codes)

Clean clone at `23e4179`:

    python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py  -> exit 0
       "OK: runtime instantiation cases passed (7 + ps1 parity when available)."
    python scripts/validate_collaboration_state.py                                  -> exit 0
    python scripts/scan_encoding.py                                                 -> exit 0
    python scripts/scan_domain_neutrality.py                                        -> exit 0

Canonical hub state (in place): validate_collaboration_state.py -> exit 0. Drift not raised.

Independent behavioral exercise on a freshly generated runtime instance (`new_instance.py --tier runtime`):

    ledger_head.py exported to instance/scripts/                 -> present
    prune_state.py --check  WITH ledger_head present             -> exit 0 ("OK: prune not due")
    rm ledger_head.py ; prune_state.py --check                   -> exit 1
       reason: "ModuleNotFoundError: No module named 'ledger_head'"
       (prune_state.py imports event_log_head from ledger_head at load; used at lines 569/600/601)
    assert_generated_tier(runtime instance, "runtime")           -> passes (no false red)
    mutate adoption_tier -> "coordination"; assert_generated_tier(..,"runtime") -> raises (teeth)

## Vector-by-vector

| # | Acceptance criterion | Result | Evidence |
|---|----------------------|--------|----------|
| 1 | Runner green on a freshly exported instance | PASS | runner exit 0 (7 cases) at 23e4179 |
| 2 | Export drags ledger_head; generated prune_state finds it | PASS | instance ships scripts/ledger_head.py; prune --check exit 0 |
| 3 | Tier assertion distinguishes tier; no red on legit runtime-tier | PASS | assert_generated_tier(runtime,"runtime") passes; case_runtime green |
| 4a| Negative teeth: removing ledger_head puts runner red | PASS | prune --check exit 1, ModuleNotFoundError: ledger_head (right reason, not spurious) |
| 4b| Negative teeth: bad declared tier puts runner red | PASS | assert_generated_tier raises on mutated tier |

Answer to the instruction's literal question: YES. The runner passes green on a freshly
exported instance, and removing ledger_head from the export puts it red for the correct reason
(prune's hard import of event_log_head fails). The negative has teeth.

## Adversarial checks performed (escape attempts)

- Red-for-the-right-reason: confirmed prune is GREEN with ledger_head and RED only via
  ModuleNotFoundError for ledger_head -- the negative discriminates, it is not a constant red.
- Cross-contamination: prune is invoked with cwd=hub-root, yet after deleting the instance's
  ledger_head it does NOT fall back to the hub's scripts/ledger_head.py (script-dir, not cwd, is
  on sys.path). The red is genuinely instance-scoped. No escape.
- Hermeticity: both negative cases mutate/delete inside tempfile.TemporaryDirectory copies; the
  live hub config and state are never touched. Confirmed by code and by clean validate exit 0.
- Change surface: c18a503 touches only the runner test file + the two task .md status flips +
  ledger bookkeeping. No scaffolding / prune / ledger_head / new_instance logic changed, matching
  the task out_of_scope ("do not change prune or ledger_head logic").

## Declared residuals (non-blocking, transparent)

- R1 (framing, historical): the "[EXPORT] runner nace rojo / ahora se arregla" narrative is
  historical. At the PARENT `5a61014` the runner was ALREADY green (5 cases) and the export
  already shipped ledger_head; I reproduced parent runner exit 0. Acceptance #1 and #3 were thus
  already satisfied before this commit. The genuine deliverable of TASK-0285 is #4 -- the two
  negative cases that make the gate signal (green on good, red on bad) -- plus a cosmetic tier
  helper refactor. Nothing in the export itself was repaired by c18a503; the fix is test
  hardening. This is honest work matching the task title ("harden instantiation smoke
  negatives") and its out_of_scope, but the message overstates the "repair" angle. Not a defect.
- R2 (low value, acceptable): the tier-mismatch negative is near-tautological -- assert_generated_tier
  is an equality check and the case mutates config then asserts it raises. It protects against a
  future weakening of the helper (legitimate regression teeth) but exercises only the assertion,
  not the generation/export path. Acceptable.

## Closure recommendation

**OK-CLOSABLE (GO).** All four acceptance criteria pass by behavior; both negatives have real
teeth verified independently; protocol gates green in a clean clone by exit code; the change is
test-only and within scope. Residuals are transparent and non-blocking. With this GO the higiene
maquinaria (0279/0274/0283/0276/0275 + 0285) is complete.

-- Analista
