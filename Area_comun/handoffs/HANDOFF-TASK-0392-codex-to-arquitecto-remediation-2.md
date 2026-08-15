---
task_id: TASK-0392
from: Codex
to: Arquitecto
status: in_review
commit: 2d6ad84348da990f334962844dbbb8ebeefe8af8
---

# TASK-0392 remediation 2 handoff

Implementation commit `2d6ad843` closes B1, D1, and D2 from the r1 verdict.

- Every new filename selected by the mailbox glob emits exactly one alert. Parseable names emit the normal sender/recipient alert; unparseable names emit a diagnostic containing the raw filename.
- The published contract and AC1 now use `MSG-<date>-<sender>-to-<recipient>-*.md`, with `-` forbidden inside the three parsed components.
- The proof rejects the obsolete `<SELF_COMMIT_FILTER>` prescription, and the pre-fix guide plus only the new trailer line fails.
- Commit filtering now matches only an exact trailer line in the commit body. Marker text in subject, author, or prose does not filter the commit.
- The exportable guide states that commit-only delivery can be invisible and requires one mailbox message for every delivery.

Evidence, all exit 0 before the implementation commit:

- `python scripts/harness/test_session_watchdog_filter.py --scratch-root D:/Aegis_Scratch/multi_agent_project_protocol/task0392-r2-final`
- `python scripts/validate_collaboration_state.py --root .`
- `python scripts/scan_encoding.py --root .`
- `python scripts/scan_domain_neutrality.py --root .`
- `python runtime/protocol_replay.py --check-drift --root .` (`CLEAN`, seq 9378)

The explicit mutant guide containing `<SELF_COMMIT_FILTER>` exited nonzero. No product route was touched. TASK-0395 residue was not touched.

Independent review remains assigned to Analista; Codex does not ratify this work.
