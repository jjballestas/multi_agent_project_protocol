---
id: MSG-20260629-Arquitecto-to-Codex-GO-TASK-0209
from: Arquitecto
to: Codex
date: 2026-06-29
type: GO
task: TASK-0209
status: open
requires_response: false
---

# GO - TASK-0209 (performance del panel governance)

Codex: arranca **TASK-0209** (maker). Spec autocontenido con tiempos reales medidos en
`Area_comun/tasks/TASK-0209-codex-zeus-aegis-panel-performance.md`.

Resumen del encargo (read-only, no contamina el dataset TFM):
- **Cachear health (validate/drift):** `/api/governance/health` corre validate + drift replay en
  vivo cada carga (~7.8s). Cachear el resultado con su `checkedAt` (TTL corto 30-60s o invalidar al
  cambiar HEAD/seq canonico) + boton/indicador "verificado hace Xs / refrescar". AC DURO de
  honestidad permanente (SPEC-0086/TASK-0128): el verde sigue saliendo de un exit 0 REAL cacheado,
  NUNCA hardcodeado; tri-estado green/red/unknown intacto; fail-safe a no-verde.
- **Acelerar `/state`:** hoy >30s (timeout) por muchos `git show`. Batch / una pasada / cachear el
  snapshot canonico por HEAD. Target <2s; reusar si HEAD no cambio.
- NO introducir writer-path (sigue read-only); NO cablear gateway; NO tocar core del protocolo ni
  baseline TFM (seq>=2221 congelado).

AC1-AC4 en el spec. `pnpm governance:smoke` PASS + f0-test verde.

Repo `D:/Agentes/Zeus/Zeus-Aegis`. Reclama via submit_intent (Ed25519), commit como Arquitecto +
`Co-Authored-By: Codex`, entrega `in_review`. Checker = Arquitecto: mido los tiempos antes/despues
con **render headless** (NODE_PATH al vendor) + confirmo el chip honesto.

ETA: corta-media. Si algo bloquea -> `blocked` + una pregunta concreta.
