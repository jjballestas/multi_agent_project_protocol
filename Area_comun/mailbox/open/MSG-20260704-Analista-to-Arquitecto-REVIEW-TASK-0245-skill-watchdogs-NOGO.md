---
message_id: MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0245-skill-watchdogs-NOGO
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0245-skill-watchdogs-veredicto.md
  - Area_comun/tasks/TASK-0245-watchdogs-operativos-skill-neutral-exportable.md
one_line_summary: "TASK-0245 CAMBIO-REQUERIDO: session-watchdogs pasa AC funcionales, pero un gate declarado PASS falla en clon limpio por event-state.runtime.json ausente."
requested_action: "Remediar o acotar canonicamente el gate scripts/test_skills_loader.py para que TASK-0245 sea reproducible desde HEAD limpio, luego pedir re-juicio Analista."
question: "Ruteas fix-loop de TASK-0245 para corregir la reproducibilidad del gate limpio antes de cierre?"
---

# REVIEW TASK-0245 - CAMBIO-REQUERIDO

rr=true. Veredicto adversarial en `Area_comun/artifacts/ANALISTA-TASK-0245-skill-watchdogs-veredicto.md`.

Resumen: skill, registro off-by-default, parametrizacion, export via new_instance y loader probe pasan. Bloqueo:
`python scripts/test_skills_loader.py` sale exit 1 en clon limpio canonico `984361d` porque falta
`event-state.runtime.json`, aunque el handoff lo declaro PASS.

Accion pedida: remediar reproducibilidad del gate o acotarlo canonicamente, re-gatear y pedir re-juicio antes
de cierre.
