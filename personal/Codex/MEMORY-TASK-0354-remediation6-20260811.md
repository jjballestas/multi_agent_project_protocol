# TASK-0354 remediation 6

- Implementation commit `cf918584` preserves invocation kind and rejects only discovered script
  targets that do not resolve to repository files; `python -m` module targets remain exempt.
- The intact extracted workflow gate exits 0 with `invocations=73 referenced=72`.
- Under one common in-memory instrument, the exact pre-fix gate exited 0 for all cases. The new
  gate exits 1 for N1, N11, N2, N13, N9, N6, N3, N4, N5, B2, and B3. N8 (`$BASE`), N10
  (`find -exec`), and N14 (`bash -c`) remain exit 0 and are declared residuals in the task file.
- Collaboration, encoding, Python and PowerShell neutrality, drift through seq 8872, 74/74
  falsification inventory, and diff gates exited 0 before the implementation commit.
- Exact implementation `cf918584` passed the intact dependency gate, collaboration, encoding,
  Python neutrality, clean drift through seq 8872, diff checks, and empty tracked status in a
  detached worktree. Delivery commit `10e08a45` moves TASK-0354 to `in_review`, releases every
  maker claim, and publishes the self-contained Arquitecto handoff. Live delivery gates passed
  collaboration, encoding, Python and PowerShell neutrality, and clean drift through seq 8876.
  Independent Analista re-review is required; Codex has not reviewed or ratified the change.
