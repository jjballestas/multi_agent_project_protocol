---
task_id: TASK-0186
title: "Consola del Arquitecto pieza 2: UI conversacional + streaming en el front (consume el puente; routeada, honesta, no-bypass) (SPEC-0099, DECISION-0062)"
type: product
status: in_review
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0099
created_at: 2026-06-26
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin: TASK-0178 / DECISION-0062 (consola del Arquitecto; pieza 2)
reuses: [TASK-0185]
linked_decisions: [DECISION-0062, DECISION-0050, DECISION-0040]
file: Area_comun/tasks/TASK-0186-codex-consola-arquitecto-ui-pieza2.md
---

# TASK-0186 - Consola del Arquitecto, pieza 2 (UI + streaming)

> maker=Codex / checker=Arquitecto. Repo = Zeus-protocol (producto). Consume el proceso-puente de TASK-0185
> (endpoints /api/protocol/architect-bridge). Off-by-default lo gatea el puente. NO toca #4/config.

## Alcance (SPEC-0099 AC1-AC6)
- **Vista "Consola Arquitecto"** routeada (nav-item que renderiza SOLO su vista): conversacion (operador + salida
  del Arquitecto en streaming) + control abrir/estado/**finalizar** + indicador de estado DERIVADO del status real.
- **Transporte streaming** cliente: consume el SSE de `/stream` y renderiza incremental; `/send`, `/stop`, `GET`.
- La UI llama SOLO a los endpoints gobernados del puente; sin ruta nueva de escritura.

## DoD (= SPEC-0099 AC1-AC6)
- AC1 vista routeada + conformidad-diseno (PERMANENTE AC12/AC13).
- AC2 solo endpoints gobernados, no-bypass (sin writeFile/ledger directo en cliente).
- AC3 estado honesto regresion-proof (PERMANENTE AC11): disabled -> UI honesta (no consola fantasma).
- AC4 sesion unica reflejada + finalizar -> dormant reflejado.
- AC5 streaming incremental + sin fuga de PII (read-only sobre el trabajo).
- AC6 gates: npm test rapido verde + caso en test:ci; protocolo validate exit 0 (con/sin secretos), drift 0,
  encoding/neutralidad exit 0; config/genesis intactos; Co-Authored-By Codex.

## Fuera de alcance
- Cambios al proceso-puente (pieza 1) salvo ajuste menor de contrato cliente<->endpoint.
- Auditoria endurecida (pieza 3); consolas para Codex/Analista; NOVA; multi-tenant; RF-9.
- Escritura directa al ledger desde la consola (prohibida).

## Notas
- La consola muestra/dirige; no actua por el Arquitecto. Reusa los endpoints de TASK-0185. Checker (Arquitecto)
  re-verifica desde clon limpio (`git -c core.longpaths=true`).
