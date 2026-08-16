# TASK-0378 remediation 4 -- 2026-08-16

- Implementation commit: `36bbf90e` (`fix(TASK-0378): align no-repository claim gate contract`).
- Chosen policy: claim enforcement is inapplicable outside a Git work tree because no commit can
  be created there; inside a work tree it remains fail-closed when Git cannot supply an actor.
- Gate and inventory case moved together. The inventory case configures its synthetic actor and
  includes a mutation negative that forces applicability outside a repository and must fail.
- Local evidence: commit-msg tests green; full-mode inventory green including absent non-reviewed
  deliverable and mutation negative; collaboration validator, encoding scan, and neutrality scan
  exit 0.
- TASK-0378 remains maker-owned until the delivery transaction moves it to `in_review`, releases
  the maker claim, and publishes the r4 handoff. Independent review remains required.
