---
handoff_id: HANDOFF-TASK-0151-codex-to-arquitecto-1
task_id: TASK-0151
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-22
product_repo: D:/Agentes/Zeus/Zeus-protocol
product_commit: 0a5e737
---

# HANDOFF TASK-0151 - File Intake V2 Phase B

## Resultado
- Producto: `0a5e737 feat(intake): add candidate review gate`.
- Alcance implementado: candidatas en store OS temp fuera del dataset, panel de revision, gate humano duro de PII por candidata, approve/discard fuera de `task_status`, re-screen candidate->intake, id derivado del contenido editado y procedencia PII-free.
- Activacion viva: OFF por defecto; no se modifico `file-ingestion.config.json` ni `protocol.config.json`.

## Rutas producto
- `D:/Agentes/Zeus/Zeus-protocol/src/server.js`
- `D:/Agentes/Zeus/Zeus-protocol/public/app.js`
- `D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js`

## Evidencia producto
- `node --check src/server.js` OK.
- `node --check public/app.js` OK.
- `node --check tests/staticContract.test.js` OK.
- `npm test` PASS 43/43.
- Clean clone Zeus `npm test` PASS 43/43.

## Garantias cubiertas
- Candidatas fuera del ledger: store `os-tmp/zeus-protocol-file-candidates`, `git ls-files` vacio para el locator, sin `type/status=candidate` en `TASK_INDEX`.
- Drift 0 con candidatas presentes.
- Aprobar sin declarar PII revisada: bloqueado.
- Editar candidata con contenido activo: rechazado.
- Candidate->intake: re-screen best-effort, redaccion de PII/SQL, relay honesto y escritura solo via `submit_intent`.
- 1 archivo -> 3 candidatas -> 3 REQ distintos; re-aprobar queda idempotente.
- Procedencia atestada sin PII: `source_file_sha256`, `extraction_task_id`, `candidate_pre_edit_hash`.

## Pendiente de checker
- Reproducir desde clon limpio.
- Pasada Analista ingest/egress/PII antes de cierre.
- Fase C sigue fuera de alcance: agente extractor, guard ampliado a todo `src/**`, purga/TTL.
