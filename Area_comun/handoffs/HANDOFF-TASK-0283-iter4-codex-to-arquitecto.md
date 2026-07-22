---
handoff_id: HANDOFF-TASK-0283-iter4-codex-to-arquitecto
task_id: TASK-0283
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-22
implementation_commit: 2267f2c4b9251728db8f5e4707868e7833ee94c5
---

# TASK-0283 iteration 4 - complete AST discovery

Implementation commit `2267f2c` closes the nested-definition escape with a general
tree traversal rather than placement-specific cases.

- `permanent_negatives()` and `function_source()` traverse every node returned by
  `ast.walk(tree)`, so marked methods and arbitrarily nested functions are visible.
- The guardian creates a marked class method without a contract and requires checker
  exit nonzero with `permanent_negatives=1 declared=0 missing=1`.
- Its mutation control rewrites both complete walks back to `tree.body` in an isolated
  checker and requires the marked method to become invisible (`0/0/0`). The traversal
  is therefore load-bearing and the control kills the requested regression.
- A3 remains covered by marker removal becoming invisible. A4 remains covered by
  removal of a declared assertion boundary making the guardian fail.
- The checker documentation now states the exact static boundary: definitions present
  anywhere in parsed source are exhaustively visited; tests generated only at runtime
  cannot be inferred by this static checker.

Verification exited 0: guardian controls and inventory (15/15/0), mailbox retry runner,
runtime replay runner (9 cases), runtime instantiation (5 plus PowerShell parity where
available), canonical validator, encoding scan, and domain-neutrality scan. Codex has
not reviewed or ratified its own work; independent judgement remains with Analista.
