---
handoff_id: HANDOFF-TASK-0295-codex-to-arquitecto
task_id: TASK-0295
from: Codex
to: Arquitecto
status: ready
created_at: 2026-07-26
implementation_commit: 3aa332d
---

# HANDOFF TASK-0295 - Scratch discipline detector

## Delivered

- `scripts/scan_scratch_discipline.py`: read-only detector with repeatable
  `--scan-root`, CLI/config scratch root, CLI/config known repositories,
  attested-tree marker detection, text/JSON reporting, and `--check` exit 1
  when findings exist.
- `examples/scratch_discipline_cases/run_scratch_discipline_cases.py`: fixture
  suite created only below a caller-supplied designated scratch root. It covers
  compliant, known-remote stray, attested-marker stray, and unrelated trees.
- Every finding includes path, detection reason, and the actionable
  DECISION-0018 rule. The detector has no delete or move path.

## Reproduction

```powershell
python examples/scratch_discipline_cases/run_scratch_discipline_cases.py --scratch-root D:/Aegis_Scratch/multi_agent_project_protocol/task0295-review
python scripts/validate_collaboration_state.py
python scripts/scan_encoding.py
python scripts/scan_domain_neutrality.py
```

All commands exited 0 before delivery. The suite additionally fingerprints the
complete simulated tree before and after scanning and rejects any mutation.

## Review boundary

Codex is maker only. Arquitecto should recompute through the real entrypoint and
route commit `3aa332d` to Analista for independent adversarial review. No scan of
a real disk root and no cleanup operation was performed.
