---
spec_id: SPEC-0107
title: Zeus-Aegis F1 - panel de gobernanza SOLO-LECTURA (contrato /api/governance/* + vistas)
status: ready
phase: P2
linked_decisions: [DECISION-0064, DECISION-0050, DECISION-0022, DECISION-0040]
owner: Codex
checker: Arquitecto
created_at: 2026-06-27
---

# SPEC-0107 - Zeus-Aegis F1 (panel read-only)

> Implementa la Fase 1 de DECISION-0064 sobre el fork Zeus-Aegis (producto). **SOLO LECTURA**: la UI LEE slim views
> y NO escribe estado. El writer-path (F2) sigue GATEADO post-TFM. Genera dataset elegible (gobernanza de
> construirlo, seq >= 2221), NO toca el aparato congelado ni el core del protocolo.

## Contrato (lectura, read-only)

`GET /api/governance/health`    -> { validator: green|red, drift, version } (DERIVADO de la verificacion real)
`GET /api/governance/state`     -> PROJECT_STATE.slim.json
`GET /api/governance/backlog`   -> TASK_INDEX.slim.json (+ filtros)
`GET /api/governance/mailbox`   -> Area_comun/mailbox/open/*
`GET /api/governance/decisions` -> indice de Area_comun/decisions/
`GET /api/governance/handoffs`  -> indice de Area_comun/handoffs/
`GET /api/governance/ledger`    -> ultimos N eventos atestados

## Reglas duras

- **Read-only:** ningun endpoint muta estado; NO hay ruta a submit_intent desde la UI todavia (eso es F2). Ningun
  camino Node escribe Area_comun/state/*.json.
- **Fuente CANONICA:** leer el estado canonico (via slim views / `git show` del HEAD canonico), NO el working tree
  crudo (leccion zeus-protocol etapa2).
- **Salud DERIVADA:** el indicador validador/drift se deriva de la verificacion real (validate exit + drift), nunca
  verde hardcodeado; fail-safe a no-verde.
- **PII (DECISION-0040):** texto libre redactado; export PII-free.
- **Producto:** todo en repo Zeus-Aegis; NO tocar core del protocolo, #4, ni el baseline congelado. Pin Hermes v2.3.0.
- **Waiver F0 (pre-F1):** los 24 fallos upstream waivados en F0 (chat/swarm/mcp/i18n/kanban) que F1 NO use quedan
  waivados con justificacion; los que F1 SI toque deben quedar verdes. Declararlo en docs/SEAMS.md.

## Entrega por increments (cada uno = un caso; tras cerrar, actualizar pipeline.html)

- **F1a (TASK-0196):** contrato + endpoints health/state/backlog/mailbox; vista Estado + header de salud
  (validador/drift DERIVADO); vista Backlog (filtros texto/estado/owner); vista Mailbox. node --test verde.
- **F1b (follow):** vistas Decisiones + Ledger/atestacion + Handoffs.
- **F1c (follow):** migrar componentes de gobernanza reutilizables de zeus-protocol (REUSE-INVENTORY F0.6).
- **GATE 1:** el operador ve el estado real del protocolo en la UI, solo lectura, sin riesgo de drift.

## DoD F1a (= AC)

- AC1 endpoints health/state/backlog/mailbox sirven slim views read-only (sin ruta de escritura).
- AC2 header de salud DERIVADO de validate/drift reales (tri-estado; fail-safe no-verde; nunca hardcoded).
- AC3 vistas Estado/Backlog(filtros)/Mailbox renderizan desde el canonico; PII redactada.
- AC4 prueba negativa: no existe superficie de escritura directa al ledger desde la UI (test).
- AC5 node --test verde; el gate F0 (npm test) sigue exit 0; waiver F0 revisado en SEAMS.md.
- AC6 core protocolo intacto; handoff a Arquitecto (checker).
