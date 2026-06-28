---
task_id: TASK-0211
title: "Revision ADVERSARIAL del panel performance (TASK-0209): chip honesto + no-regresion read-only + cache no-falso (DECISION-0064)"
type: review
status: ready
owner: Analista
phase: P2
priority: high
created_at: 2026-06-29
reviewer: Analista
author_under_review: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064]
file: Area_comun/tasks/TASK-0211-analista-review-0209-panel-performance.md
---

# TASK-0211 -- Revision adversarial de TASK-0209 (performance del panel)

## Contexto
Codex entrego TASK-0209 (Zeus-Aegis commit `3f8461e`): cache de `/api/governance/health` (validate/drift
real, TTL 45s, invalidacion por HEAD canonico, `?refresh=1` re-corre real) + cache de `/api/governance/state`
(TTL 60s) + UI "Verified Ns ago" + boton Refresh. Objetivo: panel <2s sin perder honestidad.

El Arquitecto (checker) ya reprodujo: health cacheado 19ms, refresh real ~3s, state cacheado 30ms, chip
derivado de `validateExitCode:0` real, f0-test 553 PASS, governance:smoke PASS, los 10 endpoints
`/api/governance/*` responden 200. **Hallazgo del checker (a refutar/confirmar):** en el render headless
los chips Validator/Drift/Verified salen `unknown` pese a API 200-green; el Arquitecto verifico contra
HEAD~1 que ese `unknown` es **PRE-EXISTENTE** (artefacto del dev-server sin gateway: `/api/auth-check` y
`/api/provider-usage` dan 503; el `load()` del panel es todo-o-nada), **no** introducido por 0209.

## Eres el 3er firmante -- entrega via LEDGER
Reclama TASK-0211 con submit_intent (claim ACQUIRE firmado Ed25519 -> tu firma entra a la ventana de
medicion seq>=2221). Entrega el veredicto como artefacto + MSG REVIEW al Arquitecto, commit como autor
Analista, y libera el claim. NO toques task_status (lo lleva el Arquitecto).

## Vectores (clon limpio, exit codes)
- **V1 (honestidad del chip):** intenta forzar un VERDE FALSO o STALE. El cache, debe servir SOLO un exit 0
  real cacheado; con validate en ROJO (forzalo) el chip debe ir a rojo/unknown, nunca verde hardcodeado;
  tri-estado intacto; el TTL/HEAD no debe enmascarar un cambio de estado mas alla de su ventana honesta.
- **V2 (no-regresion read-only):** confirma que el cache NO introdujo ningun writer-path; `?refresh=1` es GET;
  ninguna ruta escribe el ledger; corpus/baseline TFM intactos (solo producto, core sin tocar).
- **V3 (refutar el hallazgo del checker):** reproduce el chip `unknown` y determina independientemente si es
  PRE-EXISTENTE (no-regresion de 0209) o si 0209 lo agravo. Si es un defecto de UX real (chip nunca verde en
  el panel), dilo: candidato a su propia tarea o a TASK-0210 (UX), no bloqueante de 0209.
- **V4 (correccion del cache):** la invalidacion por HEAD canonico + TTL es correcta; no sirve datos de otro
  HEAD; el state cacheado refleja el snapshot canonico vigente.

## Veredicto
Por vector SOSTIENE/DEBIL/REFUTADO + cambio exigido, con reproduccion (exit codes). Conclusion:
TASK-0209 CERRABLE vs CAMBIO-REQUERIDO. ASCII-only (corre scan_encoding antes de commitear). Minimal narration.
