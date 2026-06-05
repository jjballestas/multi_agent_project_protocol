---
decision_id: DECISION-0007
title: Claim antes de cualquier borrador en rutas compartidas
status: accepted
date: 2026-06-05
ratified_at: 2026-06-05
deciders: [operador humano, Codex]
supersedes: []
superseded_by: []
relates_to: [DECISION-0005, DECISION-0006, TASK-0020]
phase: P2
---

# DECISION-0007 - Claim antes de cualquier borrador en rutas compartidas

## Contexto

Durante la coordinacion de TASK-0017, TASK-0018 y TASK-0019 aparecio un archivo nuevo en una ruta
compartida (`scripts/upgrade_instance.py`) antes de que el ownership quedara claro para todos los
agentes. La comunicacion compacta evito una colision real, pero evidencio una regla operativa que
debe quedar explicita.

## Decision

Todo agente debe crear o actualizar un claim activo **antes** de crear, modificar o dejar un
borrador en una ruta compartida.

Esto aplica tambien a:

- archivos nuevos;
- borradores parciales;
- scripts o fixtures temporales que quedan en el workspace;
- ediciones de estado compartido;
- rutas que "no colisionan" tecnicamente pero pertenecen al scope de una tarea.

La unica excepcion son borradores privados dentro del area privada del agente, cuando esa area no
esta cubierta por el claim activo de otro propietario.

## Regla operativa

1. Leer `TASK_INDEX.json`, `CLAIMS.json` y `mailbox/open/`.
2. Si la ruta que se va a tocar es compartida, crear o actualizar claim activo con esa ruta en
   `scope`.
3. Solo despues crear o editar archivos.
4. Si se descubre trabajo no reclamado en una ruta compartida, no se pisa: se abre un mensaje de
   mailbox con una sola pregunta de ownership.
5. El handoff debe mencionar cualquier borrador previo reutilizado o preservado.

## Consecuencias

- Reduce carreras entre agentes y archivos "huerfanos" sin ownership.
- Hace visible el trabajo incluso cuando aun es un borrador.
- Mantiene la comunicacion compacta: si hay duda, una pregunta concreta en mailbox.
- Es aditivo y no rompe tareas historicas.
