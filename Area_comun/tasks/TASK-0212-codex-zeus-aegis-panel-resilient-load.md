---
task_id: TASK-0212
title: "Zeus-Aegis: carga resiliente del panel governance (por-endpoint, tolerante a fallos de endpoints no-governance) (DECISION-0064)"
type: product
status: in_review
owner: Codex
phase: P2
priority: high
created_at: 2026-06-29
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064]
file: Area_comun/tasks/TASK-0212-codex-zeus-aegis-panel-resilient-load.md
---

# TASK-0212 -- Carga resiliente del panel governance

## Contexto (defecto pre-existente confirmado por el checker)
En un dev server SIN gateway (hermes-agent no instalado), el panel `/governance` muestra los chips
**Validator/Drift/Verified = `unknown`** y todas las secciones/dashboard en **0**, AUNQUE los 10 endpoints
`/api/governance/*` responden 200 con datos reales (verificado con curl + fetch in-page). Causa raiz: el
`load()` de `governance.tsx` es **todo-o-nada** -- hace `Promise.all` de los fetches y, si algo falla (p.ej.
las llamadas NO-governance `/api/auth-check` y `/api/provider-usage` dan 503 sin gateway, o un endpoint cold
hace timeout), lanza `Governance read failed` y NINGUN chip/seccion se puebla. Verificado vs HEAD~1: es
PRE-EXISTENTE (no lo introdujeron TASK-0209/0210). En el entorno del operador CON gateway los datos cargan;
pero el panel debe ser robusto y pintar lo que SI puede leer del ledger canonico, sin depender de subsistemas
ajenos (chat/gateway).

## Objetivo
El panel governance pinta la salud y los datos governance que puede leer, AUNQUE fallen endpoints
no-governance o falle algun endpoint governance puntual. Un fallo aislado degrada SOLO su propia
seccion/chip, no toda la pagina.

## Alcance (solo `governance.tsx` y, si aplica, el desacople del panel del shell de chat; READ-ONLY)
1. **Diagnostico breve:** confirmar la causa (load todo-o-nada via Promise.all + `if (!ok) throw`, y/o
   dependencia del WorkspaceShell/auth global). Dejar la causa en el handoff.
2. **Carga por-endpoint resiliente:** reemplazar el `Promise.all` todo-o-nada por `Promise.allSettled` (o
   try/catch por fetch) de modo que cada chip/seccion se setee con su propio resultado; un endpoint que falla
   deja SU seccion en estado vacio/no-disponible claro, sin blanquear el resto.
3. **Chip de salud independiente:** si `/api/governance/health` responde 200, los chips Validator/Drift/Verified
   muestran el valor REAL (verde/rojo derivado, honestidad de SPEC-0086 intacta); solo si ESE endpoint falla el
   chip va a `unknown`. El fallo de endpoints NO-governance (auth-check/provider-usage) NO debe afectar a los chips.
4. No depender de subsistemas de chat/gateway para renderizar governance (el panel-first bypass ya existe;
   completar si el shell sigue forzando una dependencia).

## Fuera de alcance
NO operar/escribir (read-only, F2 gateado post-TFM); NO tocar el binario hermes/HERMES_API_*; NO core ni baseline TFM.

## Criterios de aceptacion (verificar con RENDER HEADLESS en condicion SIN gateway)
- **AC1:** en un dev server sin gateway (auth-check/provider-usage 503), el panel muestra **Validator/Drift verdes
  reales** (no unknown) y **Seq/Version/Active tasks/Dashboard con datos reales** del ledger canonico.
- **AC2:** las 6 secciones pueblan sus conteos y listas reales (Backlog/Mailbox/Artifacts/Decisiones/Ledger/Handoffs
  con N>0 cuando hay datos), preservando lo de TASK-0210 (acordeones colapsados + filtros + recientes).
- **AC3:** un fallo inyectado en UN endpoint governance degrada SOLO su seccion (las demas siguen pintando);
  el chip de salud sigue honesto (tri-estado, derivado de exit real, no hardcodeado).
- **AC4:** read-only preservado (sin writer-path); `pnpm governance:smoke` PASS; f0-test verde.
- **AC5:** checker (Arquitecto) reproduce con RENDER HEADLESS en su clon SIN gateway + SCREENSHOT que evidencia
  chips verdes + datos != 0 (hoy salen unknown/0; el fix debe corregirlo).

## DoD
AC1-AC5 verdes; handoff `in_review` con la causa raiz + screenshots antes/despues (unknown/0 -> verde/datos).
Commit Zeus-Aegis como Arquitecto + Co-Authored-By Codex. Lecciones [[checker-verify-rendered-not-just-text]] +
[[checker-clean-clone-no-residual-artifacts]] aplican (screenshot obligatorio; gate reproducible).
