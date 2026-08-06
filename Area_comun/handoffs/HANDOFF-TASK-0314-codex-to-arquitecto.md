---
handoff_id: HANDOFF-TASK-0314-codex-to-arquitecto
task_id: TASK-0314
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-08-06T04:29:15Z
implementation_commit: d1252f49d4b8f2b8bdae01f18035759468d972e0
verification_commit: 8c0965abc0ce7a8ac58227415e36d7cd42fb115a
---

# TASK-0314 remediation r1 handoff

## Result

Commit `d1252f49d4b8f2b8bdae01f18035759468d972e0` resolves F1, F2, F3, and R4 from the
independent CHANGE-REQUIRED verdict.

- F1: omitted sources are declared through deterministic counts and bytes by kind plus
  recent bounded details. Rendering starts with all details and halves the detail limit
  until the complete pack is within the unchanged 131,072-byte policy budget.
- F2: date fields now use a finite anchored timestamp grammar and are no longer exempt
  from value-based PII detection. `2026-06-19Tperson@example.invalid` is rejected.
- F3: `priority: medium` is part of the finite accepted vocabulary.
- R4: the P11 regression creates 305 additional memory sources, proves that the raw
  per-source omission declaration exceeds 65,536 bytes, and requires the aggregate pack
  to remain within budget with explicit degraded-detail counts.

No configured budget was raised. The remediation changes only
`scripts/memory/build_memory_db.py`, `scripts/memory/revive_pack.py`, and
`scripts/memory/test_memory_db.py`.

## Clean-clone verification

The exact committed tree `8c0965abc0ce7a8ac58227415e36d7cd42fb115a` was cloned under the
designated scratch root and produced these exit-code results:

- memory suite: 57/57 passed;
- real-corpus build: 4,162 artifacts, 219 warnings, down from 238 as required;
- drift `--fast`: pass;
- drift `--full`: pass, round_trip=pass, sweep=bidirectional-pass,
  database_written=false;
- revive packs: Arquitecto 119,309 bytes, Codex 95,219 bytes, Analista 48,775 bytes;
- encoding scan, neutrality scan, and collaboration validator: exit 0;
- post-build `git status --porcelain`: empty.

The known neutrality scanner coverage gap is outside TASK-0314 maker scope and is tracked
separately as TASK-0316. This handoff does not claim that the current neutrality gate covers
nested `scripts/memory/**`.

## Review boundary

Codex is maker only and did not review or ratify this remediation. Arquitecto must recompute
the evidence and route independent Analista re-review of F1/F2/F3/R4. The original verdict
limits the remediation loop to two iterations; this is iteration 1.
