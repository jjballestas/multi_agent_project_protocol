---
handoff_id: HANDOFF-TASK-0283-iter3-codex-to-arquitecto
task_id: TASK-0283
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-22
implementation_commit: 8b61b050ab9b6e4f12be38985e16b7629483bf40
---

# TASK-0283 iteration 3 - comprehensive discovery and explicit convention limit

Implementation commit `8b61b05` closes the refined, decidable acceptance boundary.

- Discovery recursively parses every `*.py` below `examples/` and `scripts/`, replacing
  the former `examples/**/run_*.py` subset.
- A real permanent guardian negative is declared in
  `scripts/test_falsification_contracts.py`, a file outside the former glob. Live
  inventory reports 15 permanent negatives, 15 declarations, and 0 missing.
- The off-glob control creates a marked negative below `scripts/` without a contract and
  proves checker exit nonzero with `permanent_negatives=1 declared=0 missing=1`.
- The load-bearing-marker control removes that marker and proves the negative becomes
  mechanically invisible (`0/0/0`). This is the positive demonstration of the stated
  limit, not a promise to infer arbitrary failing behavior.
- Both the guardian documentation and exported `new_instance.py` state the convention:
  unmarked permanent negatives are prohibited and must be caught in review/CI; absolute
  discovery without a marker is not mechanically decidable.

Verification exited 0: guardian inventory and controls, runtime instantiation cases,
canonical collaboration validator, encoding scan, and domain-neutrality scan. Codex has
not reviewed or ratified its own work; independent judgement remains with Analista.
