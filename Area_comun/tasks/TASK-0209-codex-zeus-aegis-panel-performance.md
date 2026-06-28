---
task_id: TASK-0209
title: "Zeus-Aegis: performance del panel governance (cachear validate/drift, acelerar /state) (DECISION-0064)"
type: product
status: ready
owner: Codex
phase: P2
priority: high
created_at: 2026-06-28
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064]
file: Area_comun/tasks/TASK-0209-codex-zeus-aegis-panel-performance.md
---

# TASK-0209 -- Performance del panel governance

## Contexto (medido por el Arquitecto)
El panel `/governance` carga pero es LENTO -> se siente vacio/roto los primeros segundos. Tiempos reales medidos:
- `/api/governance/health` (chips Validator/Drift): **~7.8s** (corre `validate_collaboration_state.py` + drift replay en Python EN VIVO cada carga).
- `/api/governance/state` (Version/Seq/Active tasks): **>30s (timeout)** -- lee muchos archivos canonicos via `git show`.
- `/api/governance/backlog`: responde OK.
El panel es READ-ONLY y honesto (validator/drift DERIVADOS de validacion real, no verde estatico); eso debe preservarse.

## Objetivo
El panel carga en ~1-2s la mayoria del tiempo, SIN perder la honestidad (validator/drift siguen siendo verificacion real, solo cacheada con su timestamp y refrescable).

## Alcance
1. **Cachear health (validate/drift):** guardar el resultado de `validate_collaboration_state.py` + drift con su `checkedAt` (TTL corto, p.ej. 30-60s, o invalidar cuando cambia el HEAD/seq canonico). Servir el cacheado al instante + un boton/indicador "verificado hace Xs / refrescar" que re-corre bajo demanda. El AC DURO de honestidad se mantiene: el verde sigue saliendo de un exit 0 REAL (cacheado), nunca hardcodeado; tri-estado (green/red/unknown) intacto; fail-safe a no-verde.
2. **Acelerar `/state`:** reducir el costo (batch de `git show` / leer en una pasada / cachear el snapshot canonico por HEAD). Target <2s. Si HEAD no cambio, reusar.
3. No introducir writer-path (sigue read-only); no cablear gateway; no tocar core del protocolo ni baseline TFM.

## Criterios de aceptacion
- **AC1:** health responde <500ms en caliente (cacheado) con `checkedAt`; un refresh re-corre la validacion real. El chip sigue DERIVADO de exit 0 real (no hardcodeado), tri-estado, fail-safe a no-verde (AC honestidad permanente de SPEC-0086/TASK-0128).
- **AC2:** `/state` responde <2s en caliente; sin timeout.
- **AC3:** sin regresion read-only (ninguna ruta nueva escribe el ledger); `pnpm governance:smoke` PASS; f0-test verde.
- **AC4:** checker (Arquitecto) mide los tiempos con render headless/curl y confirma <2s + chip honesto.

## DoD
AC1-AC4 verdes; handoff `in_review` con tiempos medidos (antes/despues) + evidencia del chip honesto. Commit Zeus-Aegis como Arquitecto + Co-Authored-By Codex. Checker verifica con render headless (NODE_PATH al vendor) -- ver leccion [[checker-verify-rendered-not-just-text]].
