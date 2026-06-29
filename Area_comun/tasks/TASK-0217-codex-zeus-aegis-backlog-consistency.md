---
task_id: TASK-0217
title: "Zeus-Aegis: Backlog muestra 0 pese a Dashboard Tasks>0 -- fuente inconsistente (slim vs full) + render del backlog (DECISION-0064)"
type: product
status: ready
owner: Codex
phase: P2
priority: high
created_at: 2026-06-29
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064]
file: Area_comun/tasks/TASK-0217-codex-zeus-aegis-backlog-consistency.md
---

# TASK-0217 -- Backlog 0 vs Dashboard Tasks>0 (inconsistencia de fuente)

## Contexto (diagnostico del checker)
El operador reporto: el Dashboard muestra `Tasks 11` (done 7, ready 4) pero la seccion **Backlog muestra 0**
("0 visible tasks"). Causa raiz en `vendor/hermes-2.3.0/src/server/governance-readonly.ts`:
- `getGovernanceBacklog()` lee **`Area_comun/state/TASK_INDEX.slim.json`** (p.ej. 2 proposed + 7 ready).
- `getGovernanceMetrics()` (Dashboard) lee **`Area_comun/state/TASK_INDEX.json`** (full) -> cuenta distinto.
Dos fuentes distintas -> los conteos NUNCA cuadran; y el Backlog puede salir 0 aunque haya tareas ready/proposed.

## Objetivo
Backlog y Dashboard coherentes: misma fuente canonica de tareas; el Backlog PINTA las tareas ready/proposed que
existen (conteo del badge == tareas mostrables); read-only preservado.

## Alcance (solo governance read seam / governance.tsx; READ-ONLY)
1. Unificar la fuente de tareas: backlog y metrics derivan del MISMO archivo canonico (decidir slim vs full de
   forma consistente; recomendado: el conjunto que el panel quiere mostrar como backlog = ready/proposed, y que el
   Dashboard cuente del MISMO universo o se documente la diferencia explicita "backlog activo" vs "total").
2. Asegurar que el view de Backlog renderiza las tareas recibidas (revisar el path resiliente de carga de
   TASK-0212 `readEndpoint('backlog')`/`valueOf`/`setBacklog` por si deja `backlog.tasks` vacio cuando hay datos).
3. Preservar acordeones/filtros/recientes de TASK-0210.

## Criterios de aceptacion (verificar con RENDER HEADLESS)
- **AC1:** con tareas ready/proposed en el estado, el Backlog muestra N>0 y el badge == nro de tareas filtrables;
  coherente con el Dashboard (mismo universo o diferencia documentada/etiquetada en la UI).
- **AC2:** sin regresion read-only; `pnpm governance:smoke` PASS; f0-test verde.
- **AC3:** checker (Arquitecto) reproduce con RENDER HEADLESS + SCREENSHOT que el Backlog ya NO sale 0 cuando hay
  ready/proposed.

## DoD
AC1-AC3 verdes; handoff in_review con screenshot del Backlog poblado + la fuente unificada. Commit Zeus-Aegis como
Arquitecto + Co-Authored-By Codex. NO toca core ni baseline TFM. Leccion [[checker-verify-rendered-not-just-text]].
