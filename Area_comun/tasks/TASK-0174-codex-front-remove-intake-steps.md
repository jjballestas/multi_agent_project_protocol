---
task_id: TASK-0174
title: "Proyecto-front: quitar el indicador de pasos (1 Capturar..4 Resultado) del modal de Intake (decision del operador en prueba)"
type: product
status: ready
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0092
created_at: 2026-06-24
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin_reqs: [REQ-E0606D12]
linked_decisions: [DECISION-0050]
file: Area_comun/tasks/TASK-0174-codex-front-remove-intake-steps.md
---

# TASK-0174 - Quitar el indicador de pasos del modal de Intake

> Follow-up del modal Manual (TASK-0173 cerrada). El operador, en prueba, decidio QUITAR el indicador de pasos
> (lucia como tabs clickeables pero es pasivo). maker=Codex / checker=Arquitecto. Solo presentacion (app.js +CSS).

## Alcance

- Eliminar del modal de Intake el bloque indicador de pasos `<div class="steps">` con los `<span class="step">`
  "1 Capturar / 2 Preview / 3 Confirmar / 4 Resultado" (~1585-1589). Quitar tambien la logica asociada que ya no
  se use (p.ej. `setIntakeStep` / `data-step-index`) y su CSS `.steps`/`.step` si queda huerfano.
- El flujo gobernado RF-14 (Preview dry_run -> confirm -> execute -> resultado atestado) y sus estados/botones NO
  cambian: solo se quita el indicador visual de pasos. El resto del modal (form, footer, full-width) queda igual.
- Actualizar/retirar el behavior-test que afirmaba el avance de pasos (TASK-0173) por uno que afirme que el modal
  ya NO renderiza el indicador de pasos.

## DoD

- El modal de Intake ya no muestra el indicador de pasos; el flujo gobernado y las AC del cluster RC + fronteras
  (no-bypass / PII gate / off-by-default) siguen intactos. node --test clon limpio exit 0 (estable); #4 byte-
  identica; sin nueva ruta de escritura. Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker.
- REPRO: abrir Nueva historia (modo Manual) -> NO aparece la fila "1 Capturar / 2 Preview / 3 Confirmar / 4
  Resultado"; Preview/Execute siguen funcionando igual.
