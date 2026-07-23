---
handoff_id: HANDOFF-TASK-0264-codex-to-arquitecto
task_id: TASK-0264
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-23
implementation_commit: a079bca
---

# TASK-0264 delivery

task_id: TASK-0264
status: in_review
executive_summary: The written DECISION-0103 C1 plan-approval rule is published in the canonical task lifecycle and mirrored in the born-operational agent template.
artifacts: `Area_comun/protocol/TASK_PROTOCOL.md`, `AGENTS.template.md`, and `Area_comun/mailbox/open/MSG-20260723-Codex-to-Asesor-FYI-TASK-0264-regla-C1-publicada.md`.
gates: `validate_collaboration_state.py`, `scan_encoding.py`, and `scan_domain_neutrality.py` exited 0.
next_recommended: Route implementation commit `a079bca` to Analista for independent review against DECISION-0103 C1 and TASK-0264 acceptance.
risks: Low. This task documents the rule only; TASK-0260 owns mechanical turn-zero enforcement.

The canonical rule blocks the first execution turn until the human has seen and approved a plan
row for every governed unit with `id`, `goal`, `acceptance`, `verification_cmd`,
`required_capability`, `risk`, and `estimate`. Approval must be recorded in a signed event log or
signed mailbox. Adding a unit or materially changing acceptance or risk requires re-approval.
The DECISION-0103 E1 remediation carve-out is preserved.

The same contract is mirrored under the lifecycle section of `AGENTS.template.md`, so new
instances receive it through the born-operational template. The FYI informs Asesor of publication
without editing any private area. Codex did not implement or alter the TASK-0260 enforcement and
has not reviewed or ratified this work.

