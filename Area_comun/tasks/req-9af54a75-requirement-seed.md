---
task_id: "REQ-9AF54A75"
title: "UX: Filtros en Ledger #4 por actor y tipo de evento"
type: "requirement"
status: proposed
owner: "Operador"
phase: "P2"
priority: "normal"
project: "Zeus-protocol"
author: "Operador"
relayed_by: "Arquitecto"
endorsement: "none"
sdd_role: "seed_only_architect_authors_spec"
---

# REQ-9AF54A75 - UX: Filtros en Ledger #4 por actor y tipo de evento

## Narrativa

Como operador quiero poder filtrar los eventos del Ledger #4 por actor (Arquitecto, Codex, Operador) y por tipo de evento (intent.applied, etc.) para encontrar eventos especificos sin hacer scroll manual entre mas de 900 entradas.

## Intencion de aceptacion

Deberia ver controles de filtro (desplegable de actor, desplegable de tipo de evento) en la cabecera del Ledger. Al seleccionar un filtro la lista de eventos se reduce mostrando solo los que coinciden. Tambien deberia haber paginacion o carga progresiva para no renderizar 900+ eventos a la vez.

## PII guard

- mode: structural
- channel: ascii
- free_text_public_plane: redacted
- warning_acknowledged: true
- redactions: 0

## Accountability

- author: Operador
- relayed_by: Arquitecto
- endorsement: none
