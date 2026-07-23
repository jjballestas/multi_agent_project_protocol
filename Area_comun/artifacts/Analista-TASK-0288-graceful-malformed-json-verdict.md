# VERDICT - TASK-0288 (R1/DECISION-0103): graceful handling of malformed governed JSON in validate + prune

Reviewer: Analista (independent adversarial checker, diverse provider). Maker: Codex (does not
ratify own work). This artifact is my gate for the closure of TASK-0288.

## Closure recommendation: OK-CLOSABLE (GO)

One declared NON-blocking residual (R-A1), inside the A1 envelope the instruction set. No C5
weakening, no uncaught traceback on any governed file (hot or archive), no semantic/threshold change.

## Canonical anchor

- Repo under review: multi_agent_project_protocol (protocol hub). Scope: PROTOCOL ONLY; no product
  (Nova-Budget/Zeus) in scope -- product tests NOT run, by instruction.
- Implementation commits: `18b25da` ("handle malformed governed JSON gracefully") + `2959622`
  ("make clean-clone runner idempotent"). Both are ancestors of the cited delivery `50135f9`
  (verified with `git merge-base --is-ancestor`). No other commit touches
  `scripts/validate_collaboration_state.py` or `scripts/prune_state.py` in `18b25da..50135f9`.
- CLEAN CLONES: `git clone --no-hardlinks` to `/d/ccv288` and `/d/ccv288b`, `git checkout 50135f9`,
  both trees confirmed clean (`git status --short` empty). All gates and probes run THERE, gated by
  exit code, not in the hot tree.

## What the fix does (audited, not trusted)

- `scripts/prune_state.py` (+30): new `InvalidJsonError(ValueError)` carrying the source path;
  `read_json` catches `json.JSONDecodeError`/`UnicodeError` and re-raises as `InvalidJsonError`;
  `run_check` preflights 4 hot governed files (config, PROJECT_STATE, TASK_INDEX, CLAIMS); `main`
  wraps BOTH the `--check` and the apply paths in `try/except InvalidJsonError -> "ERROR: invalid
  JSON in <path>" to stderr, exit 2`.
- `scripts/validate_collaboration_state.py` (+2): after reading hot index/claims + archives, adds
  `if validation.errors: return validation` -- an early return BEFORE the merge/deliverable-check
  that previously assumed valid dicts. `read_json_file` already recorded malformed JSON as
  `validation.fail(...)` (broad `except Exception`), so this early return converts the downstream
  crash into a clean nonzero exit while preserving the rejection.
- `examples/malformed_json_cases/run_malformed_json_cases.py` (+): regression by real entrypoint.

Static guarantee I confirmed by reading the code: EVERY archive read in prune
(`apply_prune_direct` lines 395/403, and the `--check` path via `assess`) routes through the now
guarded `read_json`; `main` catches `InvalidJsonError` for both paths. Therefore NO governed JSON
(hot OR archive) can produce an uncaught traceback out of prune.

## Reproduction (clean clones @ 50135f9, real exit codes)

```
# Baseline gates (/d/ccv288)
python scripts/validate_collaboration_state.py                          -> exit 0  (OK: ... valid.)
python examples/malformed_json_cases/run_malformed_json_cases.py        -> exit 0  (OK: ... C5 cases.)
python scripts/scan_encoding.py                                         -> exit 0
python scripts/scan_domain_neutrality.py                                -> exit 0

# My own adversarial probes (/d/ccv288b), corrupt one file at a time, restore between cases:
# validate | prune --check  (checked: nonzero exit / names-file / NO "Traceback")
TASK_INDEX.json    = '{'          -> validate exit 1 (names,no-tb)  | prune exit 2 (names,no-tb)  PASS/PASS
CLAIMS.json        = '{'          -> validate exit 1 (names,no-tb)  | prune exit 2 (names,no-tb)  PASS/PASS
PROJECT_STATE.json = '{'          -> validate exit 1 (names,no-tb)  | prune exit 2 (names,no-tb)  PASS/PASS
protocol.config.json = '{'        -> validate exit 1 (names,no-tb)  | prune exit 2 (names,no-tb)  PASS/PASS
TASK_INDEX.json = '{"tasks":['    -> validate exit 1 (names,no-tb)  | prune exit 2 (names,no-tb)  PASS/PASS
TASK_INDEX.json = 'not json'      -> validate exit 1 (names,no-tb)  | prune exit 2 (names,no-tb)  PASS/PASS
TASK_INDEX.json = '' (empty)      -> validate exit 1 (names,no-tb)  | prune exit 2 (names,no-tb)  PASS/PASS
TASK_INDEX.json = invalid UTF-8   -> validate exit 1 (no-tb)        | prune exit 2 (no-tb, names) PASS/PASS
  (prune tail: "ERROR: invalid JSON in ...TASK_INDEX.json: 'utf-8' codec can't decode byte 0xff ...")

# A1 -- ARCHIVE files (NOT in prune preflight):
TASK_INDEX_ARCHIVE.json = '{'     -> validate exit 1 (names,no-tb)  | prune exit 0 "not due" (no-tb, not named)
CLAIMS_ARCHIVE.json     = '{'     -> validate exit 1 (names,no-tb)  | prune exit 0 "not due" (no-tb, not named)

# A2 -- masking / early-return:
clean state                       -> validate exit 0  (no spurious early-return)
TASK_INDEX = '{"schema_version":"1.0","tasks":[]}' (valid JSON, semantically broken)
                                  -> validate exit 1 (no-tb)  (C5 semantic reject still bites)

# C5 at the commit boundary (full-mode hook, HOOK_FULL=1, staged):
malformed HOT TASK_INDEX staged    -> hook exit 1; "Invalid JSON: ...TASK_INDEX.json"; boundary msg
                                      "collaboration state in staged snapshot is invalid; commit rejected"; NO traceback
malformed ARCHIVE staged           -> hook exit 1; "Invalid JSON: ...TASK_INDEX_ARCHIVE.json"; same boundary msg; NO traceback
```

## Vector-by-vector (against the REVIEW's four questions)

| # | Claim to refute | Test (by behavior, real entrypoint) | Result |
|---|-----------------|-------------------------------------|--------|
| 1 | Clean tree -> validate exit 0 | baseline gate + clean re-run after probes | PASS |
| 2 | Malformed governed JSON -> validate AND prune --check fail graceful (nonzero, name file, no traceback) | 4 hot files + 4 corruption variants + invalid-UTF-8: validate AND prune both nonzero, name the file, no traceback | PASS (hot); ARCHIVE = residual R-A1 (no traceback met; prune returns exit-0 not-due, does not name) |
| 3 | C5 intact: a genuinely broken governed state (valid-but-semantically-broken AND invalid JSON, incl. HOOK_FULL=1 staged) STILL rejects, reason attributable to the validator | semantic-broken reject (exit 1); full-hook rejects staged malformed HOT and ARCHIVE at the validator boundary ("...invalid; commit rejected"), no traceback | PASS |
| 4 | Fix does NOT change semantics/thresholds of validator or prune | diff = +2 in validate (early return) + error-handling-only in prune (InvalidJsonError, guarded read_json, preflight, main try/except); no rule/threshold altered; no other commit to these scripts | PASS |

## Adversarial angles (as instructed)

- **A1 (ARCHIVE coverage):** Corrupting `TASK_INDEX_ARCHIVE.json` / `CLAIMS_ARCHIVE.json` does NOT
  crash with a traceback in validate OR prune -- the A1 bar ("if a malformed archive blows up with a
  traceback, it is an R1 hole") is MET. `validate` (the real C5 gate) rejects them (exit 1, names the
  file) both directly and at the full-hook boundary. `prune --check` returns exit 0 "prune not due"
  because archives are outside the preflight tuple and are not read on the not-due path; if ever read
  on the due/apply path, `read_json` raises `InvalidJsonError` caught by `main` -> exit 2 (verified by
  static path analysis). See residual R-A1.
- **A2 (error truncation / masking):** On a CLEAN state the `if validation.errors: return validation`
  does NOT fire (validate exit 0). On a valid-JSON-but-semantically-broken state it does NOT early
  return spuriously -- the semantic rejection still fires (exit 1). The early return only short
  circuits when a governed file is unreadable, which is exactly when downstream merge would crash; it
  masks nothing that was previously reported as a distinct pass/fail (the exit stays nonzero).
- **A3 (semantics intact):** Confirmed. `validate` diff is exactly `+2` lines (early return);
  `prune` diff is exclusively error-handling (new exception type, guarded `read_json`, a 4-file
  preflight, `main` try/except). No validation rule, no prune threshold (`recent_done_tasks`,
  `recent_released_claims`, token due-threshold) changed.

## Declared residual (NON-blocking, inside the A1 envelope)

- **R-A1:** `prune_state.py --check` on a malformed `*_ARCHIVE.json` returns exit 0 ("prune not due")
  WITHOUT naming the file (the two `*_ARCHIVE.json` are not in the preflight tuple and are not read on
  the not-due path). This stays GRACEFUL (no traceback -- the A1 acceptance bar) and is within the
  task's prune acceptance ("exit non-zero OR the documented behavior"). It is NOT a C5 hole: the
  integrity gate that matters -- `validate`, directly and at the full-hook commit boundary -- rejects
  malformed archives (exit 1, names the file, no traceback). Optional hardening (NOT required for
  closure, at the Architect's discretion): add the two `*_ARCHIVE.json` to the prune preflight tuple
  so `--check` also names them.

## Protocol gates (hot canonical tree, this repo)

- `python scripts/validate_collaboration_state.py` -> exit 0. drift 0 (enforce/authoritative live
  instance healthy at cold start). Encoding scan run on this artifact + my message before commit.

## Bottom line

The R1 goal -- turn the uncaught `JSONDecodeError` into a graceful, attributable failure -- is
achieved for every governed JSON file including archives (no traceback anywhere). C5 is intact: four
independent genuine breaks (semantic mismatch, malformed hot, malformed archive at the hook boundary,
staged) all still reject, the reason attributable to the validator. The change is minimal and touches
no semantics or thresholds. One non-blocking residual (R-A1) is declared and sits inside the A1 bar.

Recommendation: OK-CLOSABLE. Closure (done-flip) is the Architect's call; I do not close.

-- Analista
