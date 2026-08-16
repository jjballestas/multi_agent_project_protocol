# TASK-0378 remediation 4 -- 2026-08-16

- Implementation commit: `36bbf90e` (`fix(TASK-0378): align no-repository claim gate contract`).
- Chosen policy: claim enforcement is inapplicable outside a Git work tree because no commit can
  be created there; inside a work tree it remains fail-closed when Git cannot supply an actor.
- Gate and inventory case moved together. The inventory case configures its synthetic actor and
  includes a mutation negative that forces applicability outside a repository and must fail.
- Local evidence: commit-msg tests green; full-mode inventory green including absent non-reviewed
  deliverable and mutation negative; collaboration validator, encoding scan, and neutrality scan
  exit 0.
- Governed delivery commit `ddd13482` moves TASK-0378 to `in_review`, releases both r4 maker
  claims, and publishes `MSG-20260816-Codex-to-Arquitecto-HANDOFF-TASK-0378-r4.md`. Runtime
  materialization reached seq 9569 with drift false.
- Independent Analista review remains required. Codex is maker only and did not review or ratify
  the remediation.
