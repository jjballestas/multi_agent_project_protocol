---
handoff_id: HANDOFF-TASK-0152-codex-to-arquitecto-1
task_id: TASK-0152
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-22
product_repo: D:/Agentes/Zeus/Zeus-protocol
product_commit: 63a80ee
---

# TASK-0152 - Handoff Codex -> Arquitecto

## Resultado
- Producto: `63a80ee feat(intake): add extractor loop and raw purge`.
- AC45: guard estatico ampliado a `src/**` con control positivo para `fetch`; mantiene allowlist de transporte git gobernado/read-only.
- AC45: raw upload store en os-tmp ahora tiene TTL deterministicamente barrido y purga al estado terminal de candidata (`approved`/`discarded`).
- AC41: endpoint gated `/api/protocol/intake-extractions/run` ejecuta el loop extractor off-by-default, con consentimiento `FILE_EXTRACTION_AGENT`, provider allowlisted `deterministic-local`, frontera `agent_extractor_explicit_consent`, sin network egress, leyendo el raw por sha256 y escribiendo candidatas al store no-ledger.
- Estados de extraccion externos: `running`, `completed-empty`, `completed-N`, `failed`, `timeout-released`, `no-agent-in-loop`; expuestos en `candidateReview.extractionStates`, fuera de TASK_INDEX/PROJECT_STATE.

## Archivos Producto
- `src/server.js`
- `tests/staticContract.test.js`

## Evidencia Producto
- `node --check src/server.js`
- `node --check public/app.js`
- `node --check tests/staticContract.test.js`
- `npm test`: PASS 43/43
- clean clone `npm test`: PASS 43/43
- smoke local `/healthz` + `/api/protocol/actions`: OK (`actions=7`)

## Notas De Revision
- Uso vivo de archivos reales sigue OFF-by-default y requiere GO aparte del operador.
- El loop implementado es provider local determinista para CI; no abre SDK/model endpoint ni socket de red.
- Candidatas y estados viven fuera del dataset atestado; el ledger conserva drift 0.
