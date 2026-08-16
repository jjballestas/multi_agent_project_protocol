---
decision_id: DECISION-0117
title: El actor de gobierno se declara en el commit -- trailer Governed-By obligatorio en rutas gobernadas
status: accepted
date: 2026-08-16
author: Arquitecto
approved_by: operador humano
supersedes: []
superseded_by: []
related:
  - TASK-0386
  - DECISION-0020
  - Area_comun/protocol/COMMIT_TRAILERS.json
  - personal/Analista/drafts/PROPUESTA-20260816-eficiencia-coordinacion-v3-FINAL.md
---

# DECISION-0117 -- la identidad de gobierno se declara, no se infiere

## Que se decide

Todo commit que toque rutas gobernadas declara su **actor de gobierno** en un trailer explicito
(`Governed-By: <actor>`), verificado por `scripts/check_commit_trailers.py` contra el
`agent_registry`. **El actor de gobierno deja de inferirse de `git config user.name` y deja de
inferirse del subject.**

## Por que, con los tres hechos que lo fuerzan

**1. `%an` no es identidad de gobierno.** Medido el 2026-08-16 en este arbol: conviven TRES
identidades -- `Arquitecto|arquitecto@local.invalid`, `Arquitecto|codex@local.invalid` y
`Codex|codex@local.invalid` -- porque el `user.name` del repo es `Codex` y lo comparten los tres
agentes. Un commit de coordinacion del Arquitecto entro firmado como `Codex` ese mismo dia.

**2. El subject tampoco basta.** Medido sobre los ultimos 60 commits: **13 de 60** (22 %) permiten
derivar el actor. El 78 % restante nombra la TAREA (`review(TASK-0396)`, `tasks(TASK-0397)`,
`fix(...)`), no al actor. Y una heuristica por verbo **misatribuye justo los casos que importan**:
`state(memoria): commiteo el fichero de memoria de Codex` lo hizo el Arquitecto, y cualquier
derivacion por subject lo leeria como Codex.

**3. El especimen vivo es de HOY, y es el peor posible.** El commit `04679824` de Codex absorbio dos
ficheros de veredicto del checker que estaban staged. El contenido quedo integro y firmado por
dentro, pero **publicado con autoria de MAKER y con `Task-Id` de otra tarea**. Es decir: el
veredicto del checker aterrizo en un commit del maker. **Lo que hace verificable este dataset es que
maker != checker se pueda comprobar EN EL LEDGER**, y ese dia no se podia.

La ironia que cierra el argumento: el commit que rompio la atribucion del checker era el handoff de
**TASK-0378**, que es precisamente la tarea sobre responsabilidad a nivel de commit.

## Alcance y limites

- Aplica a commits que tocan rutas gobernadas, igual que el gate de trailers existente.
- **No sustituye la atestacion criptografica** (`actor_auth`, ed25519). Es la capa de DECLARACION
  legible; la firma sigue siendo la capa de prueba. Un trailer se puede escribir mal; por eso se
  verifica contra `agent_registry` y por eso esta DECISION no cierra TASK-0386, solo le quita su
  agujero mas barato.
- **No exige cambiar `git config`** -- que es compartido y cuyo cambio romperia a los peers.

## El negativo que la acredita

Un commit sobre ruta gobernada **sin** `Governed-By`, o con un actor que no esta en el
`agent_registry`, **debe ser RECHAZADO** con la causa nombrada. Acreditacion **por mutacion**: quitar
la comprobacion hace fallar el caso. Un gate que nunca ha dicho que no no esta demostrado.

## Lo que NO se decide aqui

La atribucion retroactiva de commits ya publicados. El de hoy queda explicado en el cierre de
TASK-0409, que **cita la absorcion**: la traza la explica el ledger, no se reescribe la historia.
