---
decision_id: DECISION-0020
title: Regla anti-colision para escritura concurrente del ledger entre agentes autonomos
status: proposed
date: 2026-06-07
ratified_at: null
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0007, DECISION-0011, DECISION-0013, DECISION-0014, DECISION-0018, DECISION-0001]
phase: P2
---

# DECISION-0020 - Regla anti-colision (escritura concurrente del ledger)

> Estado: PROPOSED (2026-06-07). Borrador en personal/Claude/. El operador autorizo crearla
> "si funciona"; el metodo se valido empiricamente en Fase 5.2/5.3, Fase 6.x y D2.x con dos agentes
> autonomos (Claude reactivo + Codex con reloj ~100s). Regla de proceso, aditiva, neutral de dominio.
> SemVer MINOR (DECISION-0001). NO se ratifica sin aprobacion humana (toca el protocolo de colaboracion).

## Contexto

Con Codex operando autonomo (reloj ~100s que auto-reclama `ready`, poda y notifica anomalias) y Claude
reaccionando autonomo (via wakeups), ambos agentes pueden intentar escribir el ledger compartido
(`Area_comun/state/*.json`, mailbox) en ventanas solapadas. Sin disciplina explicita esto produce:

- **Claims que referencian archivos inexistentes** (un claim creado antes que su artefacto). HALLAZGO #1.
- **Commits "torn"**: staging por directorios amplios captura trabajo a medio escribir del peer y produce
  un commit inconsistente (impl sin su golden, o golden sin su impl). HALLAZGO #2 (commit b1e519b en 5.2).
- **Aserciones de mailbox falsas en el momento de escribirlas**: un FYI "DONE"/"ready" escrito antes de que
  el ledger refleje ese estado. HALLAZGO #3.

El metodo que evito estas colisiones a lo largo de 5.2/5.3/6.x/D2.x se formaliza aqui como regla.

## Decision

Se incorpora al protocolo la **regla anti-colision** para todo agente que escriba el ledger compartido:

1. **Preparar fuera de banda.** Specs, tareas y borradores se preparan en el area personal del agente
   (`personal/<id>/`, no reclamable por el peer) mientras el peer esta ocupado. Solo se promueven a rutas
   compartidas en una ventana segura.

2. **Ventana segura.** Antes de escribir el ledger, el agente verifica que el peer no tiene claim activo
   sobre las rutas a tocar y que el working tree no muestra una entrega del peer a medio escribir. Si el
   peer esta `in_progress` con claim activo o el arbol esta sucio por el peer, NO se toca el ledger: se
   espera (re-arm) y se reintenta.

3. **Escritura atomica del ledger.** El cierre/encolado se hace en UN script (idealmente una sola
   transaccion de lectura-modificacion-escritura por archivo) que minimiza la ventana de intercalado.
   Evitar heredocs con triple comilla (rompen el shell); los mensajes de mailbox se crean con el editor de
   archivos, no incrustados en el script.

4. **Archivos-antes-de-claim (HALLAZGO #1).** Un claim no referencia en su `scope` artefactos que aun no
   existen: primero se crea/escribe el artefacto, luego el claim que lo cubre.

5. **Staging explicito al commitear (HALLAZGO #2).** Se commitea por rutas explicitas, nunca por
   directorios amplios, para no capturar trabajo concurrente del peer. Si los edits ya se intercalaron, se
   commitea un SNAPSHOT consistente (con gates verdes), no un estado a medio escribir.

6. **Aserciones verdaderas al escribirlas (HALLAZGO #3).** Toda asercion en mailbox debe ser verdadera en
   el ledger en el instante de escribirla: el FYI "DONE" va DESPUES del flip de status; el GO "X ready" va
   DESPUES de registrar X en el ledger. Esos mensajes se crean tras el script atomico.

7. **Promover de a una, con GO + ETA.** Se promueve una sola tarea por vez a `ready` y se envia GO con ETA
   por mailbox; no se encolan multiples tareas simultaneas que el peer pueda tomar en carrera.

## Aplicacion

- `AGENTS.md` sec.7 (Collaboration Protocol) y `AGENTS.template.md` sec.7: nuevo bloque "Anti-collision
  rule (concurrent ledger writes)" con los 7 puntos en forma normativa compacta.
- `Area_comun/protocol/TASK_PROTOCOL.md`: subseccion "Concurrent ledger writes / anti-collision" con el
  detalle operativo (ventana segura, script atomico, staging explicito) y referencia a los 3 hallazgos.
- Complementa DECISION-0018 (atomicidad del handoff-release) y DECISION-0007/0011 (disciplina de claims).

## Versionado y neutralidad (DECISION-0001)

Aditiva (nueva regla de proceso; no rompe comportamiento ni contrato de datos). **MINOR.** Neutral de
dominio: es coordinacion de proceso, sin terminos de negocio.

## Consecuencias

- Dos agentes autonomos pueden coexistir sobre un ledger compartido sin corromper estado ni producir
  commits inconsistentes, con traza auditable.
- Un futuro endurecimiento podria automatizar la deteccion de ventana segura (lock ligero / validador que
  alerte claim-antes-de-artefacto), fuera de alcance aqui.

## Pendiente antes de ACCEPTED

- [ ] Aprobacion del operador humano (toca el protocolo de colaboracion / boundary de proceso).
- [ ] Numero de decision confirmado (0020) y enlazado en PROJECT_STATE#decisions.
