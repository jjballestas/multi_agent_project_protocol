# Analista verdict -- TASK-0290 (R-A1: prune --check nombra *_ARCHIVE.json malformados)

- Reviewer: Analista (independent adversarial checker; provider-diverse; maker != checker).
- Verdict: **OK-CLOSABLE (GO)**.
- Emitted: 2026-07-23 20:36 local (UTC+0200).

## Canonical anchor

- Repo under review: multi_agent_project_protocol (protocol hub; NO product in scope).
- origin/main HEAD: `b993acd49d5fdf3876f61191da6672f6c55f6b12`.
- Impl commit: `535dd67` (Codex). Confirmed `scripts/prune_state.py` and
  `examples/malformed_json_cases/run_malformed_json_cases.py` are BYTE-IDENTICAL at HEAD to `535dd67`
  (no later commit touched the code under review).
- Method: CLEAN CLONE of origin/main into `/d/ccv0290`, checkout `b993acd`, gates run THERE by EXIT code.
  Behavior tested by extracting the real entrypoint and running my OWN payloads (whole family, not the
  given example), plus a before/after comparison against the pre-fix blob to prove the fix is not theater.

## What the change is (audited, not trusted)

`scripts/prune_state.py`, function `run_check`: +2 lines add
`Area_comun/state/TASK_INDEX_ARCHIVE.json` and `Area_comun/state/CLAIMS_ARCHIVE.json` to the preflight
tuple already read via `read_json` (return value discarded). `read_json` returns `{}` for a missing
file and raises `InvalidJsonError` (subclass of ValueError) on `json.JSONDecodeError`/`UnicodeError`;
that exception is caught in `main()` -> prints `ERROR: invalid JSON in <path>` to stderr -> exit 2.
`assess()`/`measure()` do NOT read the archives, so reading them in the preflight is a pure decodability
probe: a no-op on valid input, a graceful named failure on malformed input. Diff scope confirmed:
`scripts/prune_state.py` +2 (preflight only), `examples/` +23 (regression). `.githooks/`, the validator,
the apply/`--apply` path, thresholds and config are UNTOUCHED.

## Reproduction (exit codes, clean clone /d/ccv0290 @ b993acd)

Protocol gates:
- `python scripts/validate_collaboration_state.py --root .` -> exit 0 (OK: collaboration state is valid).
- `python scripts/scan_encoding.py` -> exit 0 (OK: encoding scan is clean).
- `python examples/malformed_json_cases/run_malformed_json_cases.py` -> exit 0
  ("OK: clean, malformed validate/prune, semantic rejection, and full-hook C5 cases.").

Canonical in-place validate (HEAD b993acd): exit 0. drift: coordination-tier instance (manual ledger);
validate green is authoritative; no runtime drift enforcement active.

Independent behavior probe (my payloads, whole family):

| # | Vector | Result | PASS/SLIP |
|---|--------|--------|-----------|
| Baseline | valid state -> --check | exit 0, "prune not due (cold_start_tokens=12076)" | PASS |
| V1 | TASK_INDEX_ARCHIVE.json = `{` -> --check | exit 2, NAMES TASK_INDEX_ARCHIVE.json, no Traceback | PASS |
| V2 | CLAIMS_ARCHIVE.json = `not json` -> --check | exit 2, NAMES CLAIMS_ARCHIVE.json, no Traceback | PASS |
| V3 | TASK_INDEX_ARCHIVE.json = invalid UTF-8 bytes -> --check | exit 2, NAMES file (UnicodeError path), no Traceback | PASS |
| V4 (escape) | TASK_INDEX_ARCHIVE.json DELETED -> --check | exit 0 no-op (read_json returns {}); NO FileNotFoundError/crash | PASS |
| V5 (no-reg) | HOT TASK_INDEX.json = `{` -> --check | exit 2, NAMES file, graceful | PASS |
| V6 | archive = valid JSON, different shape -> --check | exit 0 no-op (not-due unchanged) | PASS |

Before/after (fix is NOT theater), pre-fix = `535dd67~1` blob run in-place (sibling import intact):
- PRE-FIX valid -> exit 0 not-due (cold_start_tokens=12076).
- PRE-FIX malformed TASK_INDEX_ARCHIVE `{` -> exit 0 "prune not due", does NOT name the archive, no traceback (INVISIBLE).
- PRE-FIX malformed CLAIMS_ARCHIVE `{` -> exit 0, does NOT name it.
- POST-FIX same inputs -> exit 2 naming the archive. Valid-state assessment identical before and after
  (12076 tokens, not-due) -> ZERO semantic/threshold change. This exactly matches the task's premise
  ("hoy da exit 0 not-due sin nombrarlo").

## Acceptance criteria (vector-by-vector)

1. Malformed `TASK_INDEX_ARCHIVE.json` / `CLAIMS_ARCHIVE.json` -> --check -> non-zero graceful naming,
   no traceback: PASS (V1/V2/V3 + shipped test + before/after delta).
2. No-regression: valid -> --check normal (not-due correct, tokens identical); hot malformed still
   named+graceful (V5); no threshold changed (pre vs post valid assessment identical): PASS.
3. Domain neutrality of the core script: PASS (the +2 lines are literal `Area_comun/state/*_ARCHIVE.json`
   paths; scan_encoding exit 0; no business/domain terms).

## Declared residuals (non-blocking, NOT slips)

- R-obs1: `--check` flags a MALFORMED archive but a DELETED/absent archive stays a no-op (exit 0), by
  `read_json`'s `if not path.exists(): return {}`. Correct-by-design: an absent archive is a legitimate
  empty state for a fresh instance; malformed vs missing are intentionally different. Within task scope.
- R-obs2: the regression fixture's internal overlay-commit is still labeled `TASK-0288` (shared fixture
  across the 0288/0290 malformed-JSON family). Cosmetic; does not affect what is exercised (exit 0).

## Closure recommendation

**OK-CLOSABLE (GO).** The +2-line preflight addition makes `prune --check` name a malformed
`*_ARCHIVE.json` gracefully (exit 2, no traceback) where it previously swallowed it silently as
"not due", with zero change to semantics, thresholds, the apply path, or the untouchable fondo. All
protocol gates green in a clean clone; the whole guarantee family holds under independent payloads;
no new escape found. Fit to close TASK-0290 (maker Codex does not ratify its own work).

-- Analista
