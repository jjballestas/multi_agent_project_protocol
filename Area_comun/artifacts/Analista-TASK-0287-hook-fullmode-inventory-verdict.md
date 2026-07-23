# VERDICT - TASK-0287 (F1/DECISION-0103): hook full-mode inventory omits task deliverables -> false rejection

Reviewer: Analista (independent adversarial checker, diverse provider). Maker: Codex (does not
ratify own work). This artifact is my gate for the closure of TASK-0287.

## Closure recommendation: OK-CLOSABLE (GO)

## Canonical anchor

- Repo under review: multi_agent_project_protocol (protocol hub). Scope: PROTOCOL ONLY; no
  product (Nova-Budget/Zeus) in scope -- product tests not run, by instruction.
- Implementation commit: `cd6bcfc` ("fix(TASK-0287): include task deliverables in full hook snapshot").
- Delivery commit: `6759fd8`. HEAD origin/main at review time: `144491d` (== local HEAD; cd6bcfc is
  an ancestor, verified with `git merge-base --is-ancestor`).
- CLEAN CLONE: `git clone --no-hardlinks` to `/d/ccv287`, `git checkout 144491d`, tree confirmed
  clean (`git status --short` empty). All gates run THERE, gated by exit code, not in the hot tree.

## What the fix does (audited, not trusted)

The full-mode local hook (`HOOK_FULL=1` / `git config hook.full true`) materializes a PARTIAL
snapshot of the staged index into a temp dir and runs `validate_collaboration_state.py --root .`
inside it. The validator merges hot TASK_INDEX + TASK_INDEX_ARCHIVE (validate_collaboration_state.py
line 1455 merge_by_array_field) and, for reviewed tasks, checks deliverable EXISTENCE
(lines 1049-1054). Two archived deliverables resolve OUTSIDE the pre-fix inventory:
TASK-0037 -> `HUMAN_GUIDE.md`, TASK-0084 -> `personal/Codex/STARTUP_PROMPT.md`. The pre-fix partial
inventory materialized neither, so a CLEAN tree was rejected in false with 'deliverable missing'.

`cd6bcfc` adds exactly two entries (`personal`, `HUMAN_GUIDE.md`) to `snapshot_inventory` plus a
comment. The validator invocation is unchanged; `scripts/validate_collaboration_state.py` is NOT in
the diff. It is a READ-SET extension, not a behavior change.

## Reproduction (clean clone /d/ccv287 @ 144491d, exit codes real)

```
# Gates
python scripts/validate_collaboration_state.py --root .   -> exit 0  (OK: collaboration state is valid.)
python scripts/scan_encoding.py                           -> exit 0  (OK: encoding scan is clean.)
python scripts/scan_domain_neutrality.py                  -> exit 0
sha256sum .githooks/pre-commit
  90685654449cb364995cd8362150411992dc6d173cf6f77acbb974d6b9a7f90f  (== pin in .github/workflows/validate.yml)

# Positive (the fix)
HOOK_FULL=1 HOOK_SNAPSHOT_MODE=partial sh .githooks/pre-commit  -> exit 0  (OK: collaboration state is valid.)

# Pre-fix demonstration (fix is load-bearing, not a no-op)
# old hook from cd6bcfc~1 on the SAME clean tree:
HOOK_FULL=1 HOOK_SNAPSHOT_MODE=partial sh <old-pre-commit>      -> exit 1  (FALSE reject):
  - Task TASK-0037 deliverable missing: HUMAN_GUIDE.md
  - Task TASK-0084 deliverable missing: personal/Codex/STARTUP_PROMPT.md

# Negative A (C5, parse-broken governed state): TASK_INDEX.json = '{' + git add
HOOK_FULL=1 ... sh .githooks/pre-commit  -> exit 1
  rejection message: "collaboration state in staged snapshot is invalid; commit rejected"
  attributed to scripts/validate_collaboration_state.py (its nonzero exit drives the reject)

# Negative B (masking probe): git rm --cached HUMAN_GUIDE.md (staged deletion of a NOW-inventoried deliverable)
HOOK_FULL=1 ... sh .githooks/pre-commit  -> exit 1
  - Task TASK-0037 deliverable missing: HUMAN_GUIDE.md  (STILL bites)

# Negative C (masking probe): git rm --cached personal/Codex/STARTUP_PROMPT.md
HOOK_FULL=1 ... sh .githooks/pre-commit  -> exit 1
  - Task TASK-0084 deliverable missing: personal/Codex/STARTUP_PROMPT.md  (STILL bites)

# Negative D (graceful semantic break, valid JSON): flip a task status to mismatch its markdown
HOOK_FULL=1 ... sh .githooks/pre-commit  -> exit 1
  - Task REQ-829CBFCE status mismatch: index='ZZZ_BOGUS' file='cancelled'  (graceful validate.fail, no crash)

# Regression (shipped)
python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py  -> exit 0
```

## Vector-by-vector (against the REVIEW's four questions)

| # | Claim to refute | Test (by behavior, real entrypoint) | Result |
|---|-----------------|-------------------------------------|--------|
| 1 | Positive: clean tree + HOOK_FULL=1 -> exit 0 (was false exit 1) | real hook on clean clone; pre-fix hook shown to reject in false | PASS |
| 2 | Negative/C5 intact: genuinely broken governed state STILL rejects, reason = validate ('...invalid; commit rejected'), NOT an unrelated crash | Neg A (parse break) + Neg D (graceful status mismatch) both reject via validate; Neg B/C prove deliverable check still bites | PASS |
| 3 | Fix ONLY extends inventory/read-set; validator behavior unchanged | diff cd6bcfc = comment + 2 inventory lines; validator invocation identical; validate_collaboration_state.py not in diff | PASS |
| 4 | CI parity: hook SHA-256 pin updated + matches; regression added | sha256sum == pin 9068..f90f; validate.yml adds "Run full-mode hook inventory cases" step; full-tree validate step unchanged | PASS |

Masking angle (the reviewer's central worry): does copying MORE into the snapshot swallow a real
inconsistency? NO. The snapshot is materialized from `git ls-files -z` over the STAGED index, so a
staged deletion of a newly-inventoried deliverable is faithfully ABSENT from the snapshot and the
validator flags it missing (Neg B and Neg C, both exit 1). The extension only makes PRESENT files
present; it cannot fabricate a deleted file. The gate still bites.

## Declared residuals (NON-blocking, out of TASK-0287 scope)

- R1 (pre-existing, unchanged by this fix): on a PARSE-broken governed state (Neg A, '{'),
  `scripts/prune_state.py --check` AND `validate_collaboration_state.py` both raise an uncaught
  `json.decoder.JSONDecodeError` traceback rather than a graceful `validation.fail`. This does NOT
  weaken C5: the prune crash is on the NON-BLOCKING warning path (hook prints WARNING and continues),
  and the actual rejection is validate's nonzero exit -> "collaboration state in staged snapshot is
  invalid; commit rejected". Neg D confirms the gate ALSO bites GRACEFULLY (no crash) on a
  valid-JSON semantic break, so attribution to the validator is clean and the 0266 trap
  (reject-for-the-wrong-reason) does not apply. Error-handling hygiene of prune/validate on
  malformed JSON is out of scope here (the fix does not touch it) and identical pre-fix.
- R2: the partial full-mode snapshot now materializes all of `personal/**` (hundreds of files),
  increasing local full-hook latency (a single full-mode run over the current tree is visibly
  slower). Acceptable: full mode is opt-in/local and CI clean-clone is the hard boundary; worth
  watching if `personal/` grows unbounded, but not a correctness issue for TASK-0287.

## Bottom line

The bug is real (pre-fix hook rejects a clean tree in false), the fix is load-bearing and minimal
(read-set only), the security intent C5 is intact (four independent genuine breaks still reject, the
reason attributable to the validator), and CI parity holds (pin matches, regression wired). No new
escape found.

Recommendation: OK-CLOSABLE. Closure (done-flip) is the Architect's call; I do not close.

-- Analista
