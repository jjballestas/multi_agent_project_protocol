# TASK-0354 remediation 6

- Implementation commit `cf918584` preserves invocation kind and rejects only discovered script
  targets that do not resolve to repository files; `python -m` module targets remain exempt.
- The intact extracted workflow gate exits 0 with `invocations=73 referenced=72`.
- Under one common in-memory instrument, the exact pre-fix gate exited 0 for all cases. The new
  gate exits 1 for N1, N11, N2, N13, N9, N6, N3, N4, N5, B2, and B3. N8 (`$BASE`), N10
  (`find -exec`), and N14 (`bash -c`) remain exit 0 and are declared residuals in the task file.
- Collaboration, encoding, Python and PowerShell neutrality, drift through seq 8872, 74/74
  falsification inventory, and diff gates exited 0 before the implementation commit.
- TASK-0354 remains `in_progress` under
  `CLAIM-20260811-Codex-TASK-0354-remediation-6` pending exact-commit verification and governed
  delivery. Codex is maker only and has not reviewed or ratified the change.
