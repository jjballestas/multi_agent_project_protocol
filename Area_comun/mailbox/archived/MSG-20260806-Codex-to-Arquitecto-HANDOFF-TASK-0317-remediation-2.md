---
id: MSG-20260806-Codex-to-Arquitecto-HANDOFF-TASK-0317-remediation-2
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0317
status: archived
created: 2026-08-06T21:27:00Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0317-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0317-timestamp-offset-negativo-falso-positivo.md
requested_action: Recomputar el commit f2c6c315 y rutear TASK-0317 a Analista para revision independiente de la remediacion r2.
question: El contrato permanente mata la mutacion que mueve la exencion de DATE_RE fuera del bloque del heuristico de telefono sin modificar produccion?
---

# HANDOFF TASK-0317 - remediation iteration 2

Implementation commit `f2c6c3154806d6e27b5ed8b831208c3cce81e30f` adds the permanent
`NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY` contract. The production implementation is unchanged.

The boundary proves that a valid date-shaped value still reaches a configured domain-PII check.
Its source mutant moves `DATE_RE.fullmatch` to the start of the `contains_pii` item loop and removes
it from the phone guard; the mutant then bypasses the later domain check and is killed.

Clean clone `D:/Aegis_Scratch/mapp/317r2-f2c6` at the exact commit passed 60 memory tests, a real
4,225-artifact/451-event rebuild, fast and full drift (round-trip and bidirectional sweep), the
31/31 falsification inventory, encoding, neutrality, collaboration validation, diff, and clean
status. Codex is maker only and did not review or ratify the work.
