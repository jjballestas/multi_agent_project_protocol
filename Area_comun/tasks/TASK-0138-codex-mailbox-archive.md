---
task_id: TASK-0138
title: "Mailbox-archive gobernado de 1 click (RF-14): intent kind core `mailbox_archive` (aditivo, neutral) + accion de relay acotada server-side + vista Mailbox con boton archivar; anti-impersonacion y #4 byte-identica"
type: product
status: done
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0086
linked_decisions: [DECISION-0053, DECISION-0052]
created_at: 2026-06-20
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0138-codex-mailbox-archive.md
---

# TASK-0138 - Mailbox-archive gobernado de 1 click (SPEC-0086 ext5, AC24/AC25; DECISION-0053)

> maker=Codex / checker=Arquitecto. TOCA EL CORE (runtime de este repo) + producto (Zeus-protocol).
> Ratificado por el Operador (REQ-B65E7802 -> DECISION-0053 + ext5 SPEC-0086). carry AC11/AC13/AC17/AC19/AC20.
> Condicion de cierre extra: PASADA DEL ANALISTA validando bounding + neutralidad ANTES de cerrar.

## Origen
REQ-B65E7802 (semilla del operador via intake): higienizar (archivar) mensajes leidos/procesados del mailbox
con UN CLICK desde el front, sin terminal; via relay acotado, builder server-side, atestado, idempotente.

## Alcance
1. **Core runtime (`runtime/submit_intent.py` + validador):** nuevo intent kind aditivo `mailbox_archive`.
   Payload `{ message_id }`; valida existencia en `Area_comun/mailbox/open/` + ruta dentro de
   `Area_comun/mailbox/` (sin path-traversal); emite evento atestado; `apply_mailbox_side_effects` mueve
   open->archived + setea `status: archived` (ASCII); idempotente (no-op si ya archivado). Golden cases
   (camino feliz + negativos PERMANENTES). Core DOMAIN-NEUTRAL.
2. **Server (Zeus):** accion de relay `mailbox-archive` (GOVERNED_ACTIONS): builder server-side estricto desde
   `message_id` validado (sin trust de payload.actorId/intents); actor relay=Arquitecto en nombre del Operador;
   `assertAllowedKeys`; hard-gate admite EXACTAMENTE {requirement-intake, mailbox-archive}.
3. **Front (Zeus):** vista Mailbox muestra estado (open/answered/archived) + marca consumidos + boton "archivar"
   por mensaje en open/. Tras archive OK -> el mensaje pasa a archived en la UI (derivado de la respuesta real);
   fallo -> error visible, sigue en open. Read-only salvo el archive gobernado. Sin ruta directa al filesystem.

## DoD
- AC24 (archive gobernado idempotente, honesto, deja canonico verde) + AC25 (anti-impersonacion prueba negativa
  permanente; hard-gate EXACTAMENTE {requirement-intake, mailbox-archive}) verdes como tests de COMPORTAMIENTO.
  Carry AC11/AC13/AC17/AC19/AC20.
- Core: golden cases `mailbox_archive` (camino feliz + negativos: id inexistente, ruta fuera de mailbox,
  path-traversal, otro-intent-via-mailbox-archive); validate exit 0 con/sin secretos; un archive real deja el
  canonico VERDE (regresion-proof).
- Server: camino feliz WRITE REAL (archive real, no mock) + prueba negativa de impersonacion.
- #4 epoca 1.14.0 BYTE-IDENTICA (config/manifest/keys sin cambio); drift 0; node --test/CI verde; npm start
  ejecutable; neutralidad/encoding limpio.
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker. PASADA DEL ANALISTA (bounding +
  neutralidad) ANTES de cerrar (la activa el operador). Commit como Arquitecto + Co-Authored-By: Codex.
  (Core en multi_agent_project_protocol; front/server en Zeus-protocol.)

## Fuera de alcance
- Cualquier ruta de escritura directa del front al mailbox/filesystem (todo via runtime, escritor unico).
- Borrado de mensajes (solo archive open->archived; no delete).
- Politica de QUE mensajes se pueden archivar mas alla de "existe en open/" (el operador decide con el click;
  la UI puede advertir si requires_response y no answered, sin bloquear).
