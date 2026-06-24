---
task_id: TASK-0172
title: "Proyecto-front: rediseno de la seccion Intake (RC-01..RC-06, SPEC-0092) -- header bar + dashboard de carpetas + modales (manual/archivo/revision); preserva RF-14 gobernado, gate de PII y off-by-default"
type: product
status: changes_requested
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0092
created_at: 2026-06-24
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin_reqs: [REQ-EE0CA804, REQ-3F85B44C, REQ-E0606D12, REQ-1C7B4275, REQ-E6B404D5, REQ-01193FD6]
linked_decisions: [DECISION-0050, DECISION-0040]
file: Area_comun/tasks/TASK-0172-codex-front-intake-redesign.md
---

# TASK-0172 - Front: rediseno de la seccion Intake (SPEC-0092)

> Cluster de rediseno UX del Intake; presentacion/reorganizacion sobre el flujo gobernado existente. maker=Codex /
> checker=Arquitecto + PASADA DEL ANALISTA (fronteras). #4 byte-identica; ASCII-only. Repo producto Zeus-protocol.

## Alcance (SPEC-0092 AC1-AC6 + fronteras + carries AC11/AC12/AC13)

- **AC1 (RC-01)** Header: barra de control unificada (badge RF-14, modo Manual/Archivo radios+label contiguos,
  Nueva-historia, Refresh) en una fila.
- **AC2 (RC-02)** Dashboard de 4 carpetas (Pendientes/Borrador/Preview/Aprobados) con icono+nombre+descripcion+
  badge de conteo DERIVADO del estado real.
- **AC3 (RC-03)** Modal modo Manual: grid 2-col proyecto/titulo, narrativa/intencion full-width, footer firmante +
  Cancelar/Preview; el flujo RF-14 (preview->confirm->submit_intent) NO cambia. Refina el modal AC7 de SPEC-0090.
- **AC4 (RC-04)** Modal revision de candidata: "Revisar requisito REQ-...", radio Archivo bloqueado, campos
  PRELLENADOS desde la candidata, aprobar -> tarjeta Aprobado. **PRESERVA el gate de PII** (no aprobar sin la
  declaracion) y va por el intake gobernado (sin ruta directa).
- **AC5 (RC-05)** Modal carga por archivo: SOLO uploader (drop+formatos) + estados (procesando/OK/error), boton
  Aceptar solo en OK; candidatas -> carpeta Pendientes. Extractor off-by-default INTACTO.
- **AC6 (RC-06)** Vista standalone de extraccion: sin radios de modo, sin lista inline de candidatas; solo uploader
  + estados; candidatas -> Pendientes.

## Fronteras (prueba negativa OBLIGATORIA)

- **No-bypass:** ninguna pieza agrega emisor de submit_intent nuevo ni ruta directa al ledger; toda escritura por
  el intake gobernado.
- **Gate de PII intacto:** la aprobacion de candidata (RC-04) exige la declaracion/revision de PII existente; el
  prellenado del modal no filtra PII (texto libre redactado).
- **Off-by-default:** la carga por archivo sigue apagada por defecto (RC-05/RC-06 no la habilitan).

## DoD

- AC1-AC6 + fronteras + AC11/AC12/AC13 verdes con behavior-tests deterministas. node --test clon limpio exit 0;
  validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; #4 byte-identica.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker. **PASADA DEL ANALISTA** (sin nueva
  ruta de escritura; gate de PII intacto; off-by-default; sin fuga de PII en el prellenado).
- REPRO: header unificado; dashboard 4 carpetas con conteos reales; modal Manual gobernado; modal archivo solo
  uploader (candidatas -> Pendientes); modal revision prellenado que aprueba con gate de PII; vista extraccion sin
  radios ni lista inline.

## Notas

- Reusar design/interface/intake_design_brief.md + components/intake + design-system; barra de integridad persistente.
- Si se prefiere fraccionar: lote A (RC-01/02/03) y lote B (RC-04/05/06); por defecto una sola entrega cohesiva.
- Citar el commit del design-system vigente en el handoff.
