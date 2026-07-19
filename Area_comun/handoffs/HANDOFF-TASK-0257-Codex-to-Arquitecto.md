---
task_id: TASK-0257
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-19
implementation_commits: [33af66b, 5e5b2d5, e2cadd8]
---

# HANDOFF TASK-0257 - remediation F-0257-01/F-0257-02/F-0257-03

## Result

- F-0257-01: `.githooks/pre-commit` now treats `scripts/`, `runtime/` and
  `.githooks/` as judgment code. When full validation applies, any unstaged or
  untracked byte there rejects the commit before the validator runs.
- F-0257-01 permanent regression: `python scripts/test_precommit_hook.py`
  verifies staged-invalid rejection and reproduces the unstaged
  `raise SystemExit(0)` validator bypass; both must remain rejected.
- F-0257-02: the hook always runs prune, selects full collaboration validation
  only for staged governed/judgment routes, and selects the guide gate only for
  its source/output/generator. This is bounded routing, not an off switch.
- Documentation in `README_INSTANCIACION.md`, the task and the hook explains
  when bounded/full modes apply and preserves E3 disarm guidance.
- F-0257-03: staged path selection now includes deletions (`D`) and type
  changes (`T`). The permanent suite rejects deletion of the validator, a
  runtime judgment dependency, governed state, and the hook itself.

## Evidence

- Implementation: `33af66b`.
- Permanent explicit negative: `5e5b2d5`.
- F-0257-03 implementation and deletion regressions: `e2cadd8`.
- Full governed hook: exit 0, 26.918 s. Because this exceeds 10 s, bounded mode
  is active as required.
- Bounded hook with no governed staged route: exit 0, 0.389 s.
- Permanent positive/negative/bypass suite: exit 0.
- Coordination/runtime export: generated, validated, hook SHA-256 identical
  `E803C867977977E5AC04445AE1CE5B440DE7B0B2669FC44358E3F6439717062C`.
- Attested export golden: PASS.
- Coordination/runtime export after F-0257-03: generated and validated; hook
  SHA-256 identical `3C52D876F4EF6662F5E2C5F1937DF9F6609C05AF5216B1D119081A328C559225`.
- Hub validate with secrets: PASS. Clean clone without secrets: PASS.
- Encoding PASS; domain-neutrality PASS; drift false at seq 4924 before
  delivery claims; config #4 byte-identical to the pinned corpus, SHA-256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Product gates: NOT_RUN; product is outside canonical scope and NOVA worktree
  was clean and untouched.

## Disarm E3

Disarm: `git config --unset core.hooksPath`.
Rearm: `git config core.hooksPath .githooks`.
The operation remains reversible under 30 seconds; CI/clean-clone/cron retain
hard enforcement.

## Obstacles

friction_count: 5

obstacles:

- what: The checker reproduced a false green through unstaged validator code.
  root_cause: Snapshot equivalence covered governed data but omitted judgment code.
  resolution: Equivalence now covers all local scripts, runtime and hook bytes;
    a permanent bypass regression locks the behavior.
  recurrence_risk: low
- what: The full hook exceeded the contractual approximate 10-second threshold.
  root_cause: Full chain/state validation dominates governed commits.
  resolution: Non-disableable staged-route bounded mode reduces unrelated commits
    to 0.389 s while governed/judgment changes retain full validation.
  recurrence_risk: medium
- what: A git-archive clean-root attempt expanded incompletely and was invalid.
  root_cause: The temporary archive procedure did not preserve a usable repository.
  resolution: The required without-secrets gate was rerun in a real clean clone and passed.
  recurrence_risk: low
- what: The first bounded selector omitted staged deletions.
  root_cause: The diff filter was copied as `ACMR` without an explicit threat
    model for every Git change kind.
  resolution: The selector now uses `ACMRTD`; permanent negatives cover
    deletion across scripts, runtime, governed state, and the hook itself.
  recurrence_risk: low

task_id: TASK-0257
status: in_review
executive_summary: F-0257-01/02/03 remediated; staged deletions and type changes now select or fail the full judgment.
artifacts: e2cadd8; 33af66b; 5e5b2d5; .githooks/pre-commit; scripts/test_precommit_hook.py; README_INSTANCIACION.md
gates: permanent A/M/D/R-family and bypass negatives PASS; 3 export tiers PASS; validate with/without secrets PASS; drift 0; domain/encoding PASS; config #4 byte-identical
next_recommended: Route the final immediate re-judgment to Analista; do not start TASK-0258 before checker GO.
risks: This is fix-loop iteration 2 of 2; any new checker failure requires operator escalation. Full governed commits remain around 27 s and --no-verify remains externally gated.
