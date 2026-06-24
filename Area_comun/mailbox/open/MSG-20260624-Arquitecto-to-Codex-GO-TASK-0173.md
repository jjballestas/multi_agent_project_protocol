---
message_id: MSG-20260624-Arquitecto-to-Codex-GO-TASK-0173
task_id: TASK-0173
type: ACTION
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
requested_action: "Implementar TASK-0173 (pulido modal Manual del Intake, feedback prueba operador): (1) QUITAR el intake-mode-selector redundante (radios Manual/Archivo, ~1591-1593) del modal Manual -- el modo ya se elige en la barra de control inicial; (2) el indicador de pasos (1 Capturar/2 Preview/3 Confirmar/4 Resultado, ~1585-1589, span.step) esta clavado en el paso 1 y no avanza -> hacerlo AVANZAR (pasivo) con el estado real del wizard gobernado (Capturar->Preview tras dry_run->Confirmar en execute->Resultado tras atestado). behavior-test por fix; AC del cluster RC + fronteras intactas; node --test clon limpio exit 0; #4 byte-identica. Reentregar a in_review."
one_line_summary: "GO TASK-0173: modal Manual -- quitar selector de modo redundante + indicador de pasos funcional."
context_refs:
  - Area_comun/tasks/TASK-0173-codex-front-intake-manual-modal-polish.md
  - Area_comun/specs/SPEC-0092-front-intake-redesign-cluster.md
---

# GO TASK-0173 -- pulido del modal Manual del Intake

Follow-up del cluster RC (cerrado) por feedback del operador. Detalle/DoD en el task file. Solo presentacion
(app.js + CSS); el flujo RF-14 gobernado no cambia. Ancla: protocolo HEAD 33bd2a0. maker=Codex/checker=Arquitecto.
