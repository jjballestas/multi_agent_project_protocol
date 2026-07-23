# VERDICT - TASK-0289 (R2/DECISION-0103): bound personal/** materialization in the full-hook

Reviewer: Analista (independent adversarial checker, diverse provider). Maker: Codex (does not
ratify own work). This artifact is my gate for the closure of TASK-0289.

## Closure recommendation: OK-CLOSABLE (GO)

A-SOBRE-RECHAZO adjudicated: ACCEPTABLE (fail-closed local opt-in gate), NOT a reintroduction of the
prohibited clean-tree F1. It is a real, net-new, LATENT hook>validator divergence -> filed as a
declared residual (R3) with a cheap non-blocking follow-up. Details below.

## Canonical anchor

- Repo under review: multi_agent_project_protocol (protocol hub). Scope: PROTOCOL ONLY; no product
  (Nova-Budget/Zeus) in scope -- product tests NOT run, by instruction.
- Implementation commit: `3090d5f` ("fix(TASK-0289): bound full-hook personal inventory"). Cited
  clean-clone anchor: `cf369d4` (delivery+memory head at review time). `3090d5f` verified ancestor of
  the current origin/main `f6bf963` (the coord commit that only routes this REVIEW; scope files
  identical). Maker Codex; not self-ratified.
- CLEAN CLONE: `git clone --no-hardlinks` to `/d/ccv289`, `git checkout cf369d4`, `git status --short`
  empty. All gates run THERE, gated by EXIT code, not in the hot tree.

## What the fix does (audited, not trusted)

`.githooks/pre-commit`: removes the whole `personal` tree from the static `snapshot_inventory`. After
materializing the static inventory, an inline Python block reads `TASK_INDEX.json` +
`TASK_INDEX_ARCHIVE.json` from the STAGED snapshot, extracts `deliverables` whose first part is
`personal` (anti-traversal guard: `path.parts[0]=="personal" and ".." not in path.parts and not
path.is_absolute()`), and materializes ONLY those paths via `git checkout-index --force -- <path>`.
Any checkout-index failure -> `status=1` -> "could not materialize staged snapshot; commit rejected".
`HOOK_INVENTORY_REPORT=1` prints "bounded personal deliverables: X of Y". `.github/workflows/
validate.yml`: hook SHA-256 pin updated. `scripts/` NOT touched (validator intact; confirmed by
`git diff --stat 3090d5f~1 cf369d4 -- scripts/` = empty).

## Reproduction (clean clone /d/ccv289 @ cf369d4, real exit codes)

```
# Provenance / parity
sha256sum .githooks/pre-commit  -> 66e7f3814de529e8234d745cd3e639f3cfe0432aaa9858fbd4c6a275ef76f4ed
  == pin in .github/workflows/validate.yml  (MATCH)
git diff --stat 3090d5f~1 cf369d4 -- scripts/   -> empty (validator untouched)

# 1. Positive: clean tree + HOOK_FULL=1 + report
HOOK_FULL=1 HOOK_INVENTORY_REPORT=1 sh .githooks/pre-commit  -> exit 0
  "bounded personal deliverables: 1 of 761 tracked paths"
  "OK: collaboration state is valid."
  (a non-blocking "PRUNE DUE released_ratio 90.48 >= 90" WARNING prints on the continue path; it is
   pre-existing hot-state condition, not introduced by 0289, and does not reject)

# 2. Negative (C5): parse-broken governed state ('{' into TASK_INDEX.json) + git add + HOOK_FULL=1
  -> exit 1 ; the Python block skips (except OSError/JSONDecodeError -> 0 personal), then the
     validator inside the snapshot rejects GRACEFULLY:
     "ERRORS: - Invalid JSON: ...TASK_INDEX.json :: Expecting property name..."
     "collaboration state in staged snapshot is invalid; commit rejected"   (attributed to validate)

# 3. Masking probe: git rm --cached personal/Codex/STARTUP_PROMPT.md (TASK-0084 done) + HOOK_FULL=1
  -> exit 1 ; REASON = checkout-index (earlier than 0287, which rejected via validate):
     "git checkout-index: personal/Codex/STARTUP_PROMPT.md is not in the cache"
     "could not materialize staged snapshot; commit rejected"
     Fail-CLOSED and attributable. (TASK-0084 is `done` = reviewed, so validate would ALSO reject it
     with "deliverable missing" if checkout-index tolerated the miss -> C5 for done deliverables is
     doubly covered.)

# 4. A-SOBRE-RECHAZO probe (isolated from the B.3 drift gate by extracting validate_tasks and running
#    real task files TASK-0118[cancelled] + TASK-0084[done], each listing an ABSENT personal/ ghost):
     validator: cancelled ghost -> NOT flagged ; done ghost -> "deliverable missing" (flagged)
     hook (probe on cancelled REQ-829CBFCE + absent personal/ ghost, staged):
       "git checkout-index: personal/ghost-nonexistent-0289probe.md is not in the cache"
       "could not materialize staged snapshot; commit rejected"  -> exit 1
     => DIVERGENCE CONFIRMED: for a NON-reviewed task the hook rejects an absent personal/ deliverable
        the validator TOLERATES.

# 5. Shipped regression + gates
python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py  -> exit 0
python scripts/validate_collaboration_state.py --root .  -> exit 0
python scripts/scan_encoding.py --root .                 -> exit 0
anti-traversal guard payloads (exact filter): personal/../etc, /etc/passwd, /personal/x,
  personal/a/../b, Area_comun/x  -> ALL rejected ; personal/Codex/STARTUP_PROMPT.md -> accepted
```

## Vector-by-vector (against the REVIEW's requested verifications)

| # | Claim to refute | Test (real entrypoint, by exit code) | Result |
|---|-----------------|--------------------------------------|--------|
| 1 | Clean tree + HOOK_FULL=1 still exit 0 (no F1 regression); STARTUP_PROMPT.md resolves present; reduction measurable | real hook clean clone -> exit 0, "1 of 761" | PASS |
| 2 | C5 intact: broken governed state STILL rejects via validate | parse-break -> exit 1, "...invalid; commit rejected" (validate) | PASS |
| 3 | Masking probe (staged removal of indexed deliverable) STILL bites | rm --cached STARTUP_PROMPT.md -> exit 1 (checkout-index, fail-closed) | PASS (reason shifted, see below) |
| 4 | A-SOBRE-RECHAZO: is the hook>validator strictness a defect? | isolated validate_tasks + live hook probe -> real divergence | SLIP -> declared residual R3 (non-blocking) |
| 5 | No validator changed; pin matches; CI parity; regression green | scripts/ diff empty; pin MATCH; regression exit 0; validate/scan_encoding exit 0 | PASS |

## A-SOBRE-RECHAZO adjudication (the angle the Architect asked me to rule on)

CONFIRMED it is a REAL, net-new divergence: the hook iterates `deliverables` of ALL task statuses and
`git checkout-index --force -- <path>` FAILS-HARD on an absent path, whereas the validator checks
deliverable EXISTENCE only for `REVIEWED_TASK_STATUSES = {in_review, review_approved, qa_pending,
architect_review, done}` (validate_collaboration_state.py:1048). So for NON-reviewed statuses
(cancelled/proposed/ready/claimed/in_progress/blocked) the hook is STRICTER than the validator ->
false rejection. Note the Architect's framing said "done/cancelled": for `done` there is NO divergence
(done is reviewed -> the validator ALSO rejects); the divergence is specific to NON-reviewed tasks.
This divergence did NOT exist under TASK-0287 (which included the whole `personal` tree via
`git ls-files -z -- personal`; ls-files only lists TRACKED files and never fails on an
index-listed-but-absent path). 0289 introduced it via the per-deliverable fail-hard checkout-index.

Ruling: ACCEPTABLE, does NOT reintroduce the PROHIBITED F1, for four independent reasons:
1. F1 as the task scopes/prohibits it = false rejection of a CLEAN tree with PRESENT-but-omitted
   deliverables (acceptance #1: "arbol limpio sigue en exit 0 ... deliverables antes omitidos ...
   siguen resolviendo como presentes"). The clean tree exits 0 and STARTUP_PROMPT.md resolves present.
   A-SOBRE-RECHAZO requires a DIFFERENT, non-clean, validator-tolerated state (absent deliverable on a
   non-reviewed task) that does not exist today.
2. Severity is bounded: LOCAL opt-in (HOOK_FULL / hook.full), fail-CLOSED (never accepts a bad commit),
   and NOT a CI blocker -- CI's hard boundary is the DIRECT validator on the real tree
   (validate.yml:29), which tolerates the same state; NO CI step runs the partial HOOK_FULL path over
   the real tree.
3. LATENT: the sole personal/ deliverable in the indexes is TASK-0084 [done], present. No non-reviewed
   task carries a personal/ deliverable, so the divergence is unreachable in the current tree.
4. The rejection is honest and attributable ("could not materialize staged snapshot") -- not a 0266
   reject-for-the-wrong-reason trap.

Because no acceptance criterion and no task-scoped prohibition is breached, a NO-GO here would itself
be over-rejection. I record it as a declared residual, not a blocker.

## Declared residuals (NON-blocking, out of TASK-0289 acceptance)

- R3 (net-new, adjudicated above): the full-hook is STRICTER than the authoritative validator for
  NON-reviewed tasks that list an absent personal/ deliverable (latent today; local opt-in;
  fail-closed; not a CI blocker). Minimal alignment for a follow-up so the hook stays a faithful
  materializer rather than a stricter gate: filter the extracted personal/ deliverables by the SAME
  REVIEWED_TASK_STATUSES the validator uses (only materialize deliverables of reviewed tasks), OR
  tolerate a checkout-index miss and let the validator be the authority (this matches the handoff's own
  stated philosophy, "left for the collaboration validator to reject"). Either closes the divergence.
- R4 (test-attribution weakening, minor): the shipped regression's masking case asserts only
  `returncode != 0`, not the rejection REASON. Post-0289 that case green-passes via checkout-index
  ("could not materialize"), NOT via the validator's "deliverable missing" C5 path. C5 is not weakened
  (done deliverables are doubly covered), but the test no longer PROVES the validator path bites.
  Consider asserting the reason (as the broken-state case already does) if the masking probe is meant
  to attest the C5/validator boundary specifically.

## Bottom line

The fix delivers the requested bounding (whole personal/ tree -> 1 of 761), keeps the clean tree
green (no F1 regression), keeps C5 fail-closed and attributable on genuine breaks, leaves the
validator untouched, and holds CI parity (pin MATCH, regression green). The A-SOBRE-RECHAZO angle is a
real but latent, local, fail-closed hook>validator divergence -> declared residual R3, non-blocking.
No new escape that accepts a bad commit was found.

Recommendation: OK-CLOSABLE (GO). Closure (done-flip) is the Architect's call; I do not close.

-- Analista
