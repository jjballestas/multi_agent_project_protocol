---
decision_id: DECISION-0081
title: "Ruta unica de memoria = REQ-MEMORIA-HIBRIDA-DB-ARCHIVO-FRIO v0.3.0; linea Engram CERRADA por completo (capability OFF permanente, tareas ENG-* sin efecto); supersede DECISION-0071"
status: accepted
date: 2026-07-02
deciders: [operador humano (aprobado por escrito 2026-07-02), Arquitecto]
supersedes: [DECISION-0071]
superseded_by: []
relates_to: [DECISION-0016, DECISION-0020, DECISION-0022, DECISION-0026, DECISION-0040, DECISION-0050, DECISION-0071]
phase: P2
capability_state: engram OFF (permanente; mecanismo nunca merged; no se activa ni Tier 0 ni Tier 1)
approval_ref: personal/operador/DECISION-OPERADOR-20260702-ruta-unica-memoria-hibrida.md
related_context:
  - "personal/operador/requerimientos-futuros/memoria-hibrida-db-archivo-frio/REQ-MEMORIA-HIBRIDA-DB-ARCHIVO-FRIO.md (v0.3.0)"
  - "personal/Arquitecto/DRAFT-DECISION-engram-memory-backend.md (historico, RUTA CERRADA)"
  - "personal/Arquitecto/DRAFT-DECISION-engram-memory-backend-v2.md (historico, RUTA CERRADA)"
---

# DECISION-0081 - Ruta unica de memoria; linea Engram cerrada (supersede DECISION-0071)

> Aprobacion por escrito del operador: `personal/operador/DECISION-OPERADOR-20260702-ruta-unica-memoria-hibrida.md`
> (document_type: operator_directive, status: approved, autoridad delegada por escrito en la sesion asesor del
> 2026-07-02). Esta DECISION ejecuta el mandato de ledger de esa directiva. Cambio de gobierno, neutral de dominio
> en el Core; no toca #4, pineados, ni el dataset sellado del TFM.

## Contexto

DECISION-0071 dejo a Engram como backend de memoria/recall con capability OFF by default (mecanismo especificado,
no merged), tras tres rondas adversariales (TASK-0219 NO-GO, TASK-0220 NO-GO, TASK-0221 GO-PROMOVER-OFF). En
paralelo maduro el requerimiento `REQ-MEMORIA-HIBRIDA-DB-ARCHIVO-FRIO` (repo caliente + archivo frio verificable +
DB derivada), cuya seccion 26 absorbe como requisitos normativos las lecciones del analisis adversarial de Engram.
El asesor del operador constato que ambas rutas se solapaban en el centro (tabla de memoria por agente / recall),
que mantener las dos creaba doble backend con drift, y que Engram incumplia el principio 2 del propio REQ
(reconstruibilidad demostrada) al no existir importador markdown->Engram. El operador resolvio la ambiguedad de
doble ruta por escrito.

## Decision

1. La **ruta unica** de memoria del sistema es `REQ-MEMORIA-HIBRIDA-DB-ARCHIVO-FRIO` **v0.3.0**. Su decision formal
   de activacion + SPEC mantienen su propio gate y se registraran **post cola REQ-ZEUS** (no ahora); esta DECISION
   solo cierra la ambiguedad de doble ruta, no arranca implementacion.
2. La **linea Engram queda CERRADA por completo**: no avanza ni Tier 0 (cache personal) ni Tier 1 (memoria
   compartida via submit_intent). La capability asociada permanece **OFF de forma permanente**.
3. Las tareas **ENG-*** documentadas dentro de DECISION-0071 (FLAG-WIRING, OUTBOX/BRIDGE/RECONCILE,
   ACTORAUTH-ATTEST, IMPORT, TOPICKEY-PII, MERGE-SEMANTIC, REGENESIS-RUNBOOK y demas) quedan **sin efecto**. Si una
   necesidad reaparece, se re-expresa en los terminos de la ruta hibrida; no se reactiva la ENG-*.
4. Los drafts de Engram en `personal/Arquitecto/` se conservan como **analisis historico** (provenance de la
   seccion 26 del REQ), marcados RUTA CERRADA. No son ruta viva.
5. DECISION-0071 pasa a `superseded_by: [DECISION-0081]` y deja de ser gobierno vivo. Su contenido y su audit trail
   adversarial (0219/0220/0221) se preservan como historia.

## Consecuencias

- Las tareas de gate adversarial de Engram (TASK-0219, TASK-0220, TASK-0221) que quedaron en `ready` con veredicto
  entregado se **cancelan** citando esta DECISION (los veredictos permanecen como artefactos historicos).
- Ninguna capability nueva se enciende; no hay re-genesis; el epoch 1.14.0 y los 5 pineados no se tocan.
- Neutralidad de dominio intacta: esta decision vive en `Area_comun/decisions/` (instancia), no en el Core ni en
  los `*.template.*`.

## Aprobacion

Operador humano (John Ballestas), por escrito, 2026-07-02 -- directiva
`personal/operador/DECISION-OPERADOR-20260702-ruta-unica-memoria-hibrida.md`. Arquitecto ejecuta el registro.
