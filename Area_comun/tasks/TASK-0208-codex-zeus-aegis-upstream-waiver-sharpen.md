---
task_id: TASK-0208
title: "Zeus-Aegis: afinar el waiver de los 24 fallos upstream (per-archivo, justificado, enforced) (DECISION-0064)"
type: product
status: done
owner: Codex
phase: P2
priority: medium
created_at: 2026-06-28
maker: Codex
checker: Arquitecto
adversarial_reviewer: Analista
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064]
file: Area_comun/tasks/TASK-0208-codex-zeus-aegis-upstream-waiver-sharpen.md
---

# TASK-0208 — Afinar el waiver de los 24 fallos upstream

## Contexto y decision
`zeus-aegis-f0-test.mjs` excluye 11 archivos de test upstream (`excludedUpstreamFiles`) que tienen
**24 fallos** en clon limpio Windows; el waiver vive en `docs/SEAMS.md` §"F0 Test Waiver" pero es un
**blanket bounded-a-F0**. Decision del operador (2026-06-28, tras triage del Arquitecto): **NO
arreglar los 24** (son test-rot upstream en superficies no-panel) ni podar ahora — **re-waive afinado**:
convertir el waiver en uno **por-archivo, justificado y enforced**.

## Evidencia del triage (Arquitecto, data real de hoy; usar tal cual)
- Corrida de los 11 excluidos: **24 failed / 44 passed (68)**. Desglose por archivo:
  kanban-backend 4 · mcp/-hub-search 4 · chat-message-list 3 · -context-usage 3 · swarm-memory 2 ·
  mcp-presets-store 2 · -models 2 · local-provider-discovery 1 · swarm2-screen 1 ·
  chat-composer-context-controls 1 · i18n 1.
- Causa dominante: `mock` + `is not a function` (12+10) = **test/code skew upstream** (los tests
  mockean funciones que cambiaron en el tag v2.3.0); + YAML.parse/CLAUDE_HOME (6+4, config provider/
  model); + 2 EPERM (Windows-only filesystem).
- **El panel governance NO depende de ninguna de las 11 superficies:** `src/routes/api/governance.*.ts`,
  `src/routes/governance.tsx`, `src/server/governance-readonly.ts`, `src/server/governance-security.ts`
  no importan swarm/kanban/mcp/hub-search/context-usage/i18n/local-provider/models/chat. Verificado por grep.

## Objetivo
El waiver deja de ser blanket: cada archivo excluido queda con su razon y la independencia del panel
queda **enforced por un test** (no solo documentada).

## Alcance
1. **Reescribir `docs/SEAMS.md` §"F0 Test Waiver"** como tabla **por-archivo** (los 11): archivo →
   nº de fallos → categoria (`upstream-test-skew` | `provider/model-config (YAML/CLAUDE_HOME)` |
   `windows-only (EPERM)` | `non-panel-surface`) → nota de independencia. Total declarado = 24/68.
   Afirmar explicitamente: el panel governance (F1/F2) no importa ninguna de estas superficies, por lo
   que el waiver no toca ninguna garantia de gobernanza. Listar los **triggers de re-evaluacion**: (a) si
   el panel llega a depender de una superficie waiveada, (b) en una poda de bloat que las elimine, (c) en
   un upstream sync. Conservar la nota historica de que F1a no usa estas superficies.
2. **Anotar `excludedUpstreamFiles`** en `zeus-aegis-f0-test.mjs` con un comentario inline por archivo
   (la categoria), para que el codigo case con el doc. La lista sigue siendo exactamente los 11 (no
   agregar ni quitar superficies en silencio).
3. **Guard enforced (regresion-proof):** agregar un test (incluido en el run f0 verde, NO en los
   excluidos) que **falle si cualquier archivo del panel governance importa una de las 11 superficies
   waiveadas** (o su modulo). Es decir, convertir la justificacion central del waiver ("el panel no
   depende de esto") en un invariante que falla cerrado. Implementacion a discrecion (p.ej. escanear los
   imports de `governance.*`/`governance-readonly`/`governance-security` contra una lista de modulos
   waiveados derivada de `excludedUpstreamFiles`).

## Fuera de alcance
NO arreglar los 24 tests; NO podar/borrar superficies (eso es la otra pieza, "retirar bloat"); NO tocar
el panel ni `HERMES_API_*`/binario hermes; NO F2/write-path; NO core del protocolo ni baseline TFM.

## Criterios de aceptacion
- **AC1:** `docs/SEAMS.md` §F0 Test Waiver es una tabla por-archivo (11 filas, conteos = 24 total,
  categoria, nota independencia) + triggers de re-evaluacion. Sin blanket.
- **AC2:** `excludedUpstreamFiles` anotado por archivo; la lista sigue siendo los mismos 11 (diff no
  agrega/quita superficies).
- **AC3 (guard):** existe un test en el run f0 verde que falla si el panel governance importa una
  superficie waiveada; pasa hoy (el panel no las importa) y fallaria si alguien las cableara. Incluir en
  el handoff la salida que demuestra el fail-closed (forzar un import de prueba y mostrar que el guard
  rompe, luego revertir).
- **AC4:** `node scripts/zeus-aegis-f0-test.mjs` EXIT 0, 546 pass (+ el guard nuevo), sin regresion.
- **AC5:** delta documentado en SEAMS; clon limpio valida.

## Revision adversarial (Analista) — gate
Un re-waive es una decision de **NO arreglar**: alto riesgo de enmascarar un defecto real. Por eso, antes
del cierre, el **Analista** hace una pasada adversarial que debe intentar **refutar** la justificacion:
(a) ¿algun fallo es realmente relevante al panel (no "non-panel") o a una garantia de gobernanza/seguridad?
(b) ¿el guard de imports es genuino y fail-closed, o se puede rodear (re-export, import dinamico, alias)?
(c) ¿la categorizacion "test-rot" oculta un bug de producto en una superficie que igual se sirve al usuario?
(d) ¿el conteo 24/68 y la lista de 11 siguen casando? El Analista entrega veredicto (refutado/sostenido +
hallazgos) a Arquitecto; el cierre a `done` requiere su pasada ademas del checker.

## Definition of Done
AC1-AC5 verdes; handoff autocontenido `in_review` a Arquitecto con: tabla SEAMS, diff del array anotado,
el guard + su prueba de fail-closed, salida de f0-test EXIT 0. Revision adversarial del Analista sostenida
(o hallazgos resueltos). Commit en Zeus-Aegis como Arquitecto con `Co-Authored-By: Codex`.
