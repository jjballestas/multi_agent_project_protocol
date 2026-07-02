---
id: DECISION-OPERADOR-20260702-RUTA-UNICA-MEMORIA-HIBRIDA
title: "Directiva del Operador: ruta unica de memoria = REQ-MEMORIA-HIBRIDA; linea Engram cerrada; superseder DECISION-0071"
status: approved
author: Operador (John Ballestas)
prepared_by: Asesor del Operador (sesion asesor 2026-07-02, autoridad delegada por escrito en esa sesion)
created_at: 2026-07-02
document_type: operator_directive
requires_ledger_action: true
ledger_action_owner: Arquitecto
related_context:
  - "personal/operador/requerimientos-futuros/memoria-hibrida-db-archivo-frio/REQ-MEMORIA-HIBRIDA-DB-ARCHIVO-FRIO.md (v0.3.0)"
  - "Area_comun/decisions/DECISION-0071-engram-memory-backend.md"
  - "personal/Arquitecto/DRAFT-DECISION-engram-memory-backend.md (historico)"
  - "personal/Arquitecto/DRAFT-DECISION-engram-memory-backend-v2.md (historico)"
---

# Directiva del Operador: ruta unica de memoria

## 1. Decision del Operador (aprobacion por escrito)

1. La **ruta unica** de memoria del sistema es el requerimiento
   `REQ-MEMORIA-HIBRIDA-DB-ARCHIVO-FRIO` **v0.3.0** (repo caliente + archivo frio verificable + DB derivada),
   cuya seccion 26 absorbe como requisitos normativos las lecciones del analisis adversarial de Engram.
2. La **linea Engram queda CERRADA por completo**: no avanza ni Tier 0 (cache personal) ni Tier 1 (memoria
   compartida via submit_intent). La capability asociada permanece **OFF de forma permanente**.
3. Las ~10 tareas ENG-* documentadas dentro de DECISION-0071 (FLAG-WIRING, OUTBOX/BRIDGE/RECONCILE,
   ACTORAUTH-ATTEST, IMPORT, TOPICKEY-PII, MERGE-SEMANTIC, REGENESIS-RUNBOOK, etc.) quedan **sin efecto**;
   si alguna necesidad reaparece, se re-expresa con los terminos de la ruta hibrida, no se reactiva la ENG-*.
4. Los drafts de Engram en `personal/Arquitecto/` se conservan como analisis historico (provenance de la
   seccion 26 del REQ), marcados RUTA CERRADA. No son ruta viva.
5. La implementacion de la ruta hibrida NO arranca ahora: mantiene su gate propio (decision formal + SPEC,
   post cola REQ-ZEUS), segun el propio REQ. Esta directiva solo cierra la ambiguedad de doble ruta.

## 2. Mandato al Arquitecto (accion de ledger requerida)

Registrar via `submit_intent` una DECISION nueva que **supersede DECISION-0071** con el contenido del punto 1-4,
actualizar `superseded_by` en DECISION-0071, y commitear esta directiva + la decision + el estado en un solo
commit gateado por exit-code (validate + scan_encoding + neutralidad), en ventana segura. La decision nueva debe
citar esta directiva como aprobacion escrita del operador.

## 3. Provenance

- Veredicto del asesor (sesion 2026-07-02): el REQ hibrido y Engram se solapaban en el centro (tabla
  agent_memory / recall per-agente); mantener ambos creaba doble backend con drift. Engram ademas incumplia el
  principio 2 del propio REQ (reconstruibilidad demostrada) al no existir importador markdown->Engram.
- Autoridad: el operador delego por escrito en la sesion asesor del 2026-07-02 la redaccion de esta directiva
  ("te doy autoridad para escribir como operador para resolver que queda pendiente de gobierno").
