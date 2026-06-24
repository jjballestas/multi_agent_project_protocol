---
task_id: TASK-0173
title: "Proyecto-front: pulido del modal Manual del Intake -- quitar selector de modo redundante + indicador de pasos funcional (feedback prueba operador)"
type: product
status: in_review
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
file: Area_comun/tasks/TASK-0173-codex-front-intake-manual-modal-polish.md
---

# TASK-0173 - Pulido del modal Manual del Intake (SPEC-0092 addendum)

> Follow-up del cluster RC (TASK-0172 cerrada) por feedback del operador en prueba. Solo public/app.js (+CSS).
> maker=Codex / checker=Arquitecto. #4 byte-identica; sin nueva ruta de escritura.

## Alcance (2 fixes)

- **Fix 1 (selector de modo redundante en el modal Manual).** El modal Manual (intake-wizard intake-modal, ~1584)
  repite un `intake-mode-selector` con radios Manual/Archivo (~1591-1593). Es REDUNDANTE: el modo ya se eligio en
  la barra de control del panel inicial (RC-01) antes de abrir el modal. QUITAR ese `intake-mode-selector` del
  modal Manual (el modal ya ES la captura manual). Behavior-test: el modal Manual NO contiene radios de modo
  Manual/Archivo.
- **Fix 2 (indicador de pasos no funcional).** Los pasos "1 Capturar / 2 Preview / 3 Confirmar / 4 Resultado"
  (`<span class="step ...">`, ~1585-1589) son ESTATICOS: el "on" esta fijo en el paso 1 y nunca avanza; parecen
  tabs clickeables pero no hacen nada. Hacer que el indicador AVANCE con el estado real del wizard gobernado:
  Capturar (form) -> Preview (tras Preview dry_run) -> Confirmar (en la confirmacion del execute) -> Resultado
  (tras el execute atestado). El paso activo refleja donde esta el flujo; el indicador es PASIVO (no navega/no
  es un boton que rompa el flujo gobernado). Behavior-test: el paso activo cambia segun el estado del wizard
  (al menos Capturar->Preview->Resultado), no queda clavado en 1.

## DoD

- Fix 1 y Fix 2 verdes con behavior-tests; las AC del cluster RC (TASK-0172) y las fronteras (no-bypass / PII gate /
  off-by-default) siguen intactas. node --test clon limpio exit 0 (estable); #4 byte-identica; sin nueva ruta de
  escritura. Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker.
- REPRO: abrir el modo Manual -> el modal NO muestra radios de modo; al hacer Preview dry_run y luego Execute, el
  indicador de pasos avanza (Capturar -> Preview -> ... -> Resultado).

## Notas

- El resto del modal Manual (form proyecto/titulo/narrativa/intencion, footer firmante + Preview/Execute, full-
  width) queda igual. Solo se quita el selector de modo y se hace funcional el indicador de pasos.
