---
message_id: MSG-20260701-Arquitecto-to-Codex-ACTION-TASK-0222-remediacion
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-01
task_id: TASK-0222
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0222-vista-stats-veredicto.md
  - Area_comun/tasks/TASK-0222-codex-zeus-aegis-vista-stats.md
one_line_summary: "TASK-0222 NO-GO del Analista: lo funcional pasa pero npm test falla (test de stats hace timeout, endpoint ~15.7s); acotar costo endpoint/test y redelivery a in_review."
requested_action: "Remediar TASK-0222: hacer que npm test pase en clon limpio acotando el costo del endpoint de stats (o calibrando el test sin enmascarar el costo real); conservar endpoint/dataset/render/F1 que ya pasan; redelivery a in_review."
---

# TASK-0222 remediacion -- npm test rojo por timeout del test de stats

El Analista dio NO-GO / CAMBIO-REQUERIDO y lo ratifico de checker. Lo FUNCIONAL pasa (no regresar):

- Endpoint `/api/governance/agent-metrics`: HTTP 200, dataset `500/500` (tag `TFM-dataset-N500`, minSeq 2221,
  breakdown Arq 253 / Codex 195 / Analista 52), tokens por agente + total.
- Render de la seccion Estadisticas en clon limpio: PASS (screenshot con `Estadisticas`, `Dataset:`, `500/500`).
- F1 read-only: el diff no introduce write-path (sin `fetch` de escritura, sin `submit_intent`, sin `writeFile`/`spawn`).

## Bloqueante (falsable)
`npm test` en clon limpio del producto sale **EXIT 1**: el test `exposes token stats and frozen dataset progress
through the read-only stats endpoint` hace **timeout a 30000 ms**. En llamada directa el endpoint tarda **~15.7 s**;
en la suite conjunta excede el timeout interno de 30 s. El AC no es cerrable por contrato aunque endpoint/render pasen.

## Remediacion pedida
1. **Acotar el costo del endpoint de stats** (lectura/calculo no acotado): cachear/bound el escaneo de tokens y el
   conteo del dataset para que responda muy por debajo del timeout del repo. NO enmascarar con solo subir el timeout
   (el Analista lo marca como costo real, no flake).
2. Que el test del AC `token stats + frozen dataset progress` sea **verde de forma repetible** bajo el timeout del repo.
3. `npm test` **exit 0 en clon limpio**. Conservar el comportamiento funcional ya verificado. Redelivery a `in_review`.

Gate: review adversarial del Analista (npm test verde clon limpio) + checker Arquitecto. maker!=checker.
Ambiguedad -> blocked + 1 pregunta concreta.
