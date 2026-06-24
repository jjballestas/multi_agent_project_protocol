---
handoff_id: HANDOFF-TASK-0172-codex-to-arquitecto-1
task_id: TASK-0172
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-24
product_commit: a4e0b50
product_repo: D:/Agentes/Zeus/Zeus-protocol
---

# TASK-0172 handoff

Implementado en producto commit `a4e0b50 feat(front): redesign intake section`.

## Entrega

- RC-01: header Intake con badge RF-14, titulo/subtitulo, selector Manual/Archivo contiguo, Nueva historia/requisito y Refresh.
- RC-02: dashboard de 4 carpetas con conteos derivados de candidatas reales: Pendientes aprobacion, Borrador, En Preview y Aprobados.
- RC-03: modal Manual con layout 2 columnas para proyecto/titulo y campos largos full-width; conserva preview/execute por RF-14 gobernado.
- RC-04: modal de revision de candidata con Archivo bloqueado, campos prellenados y gate PII obligatorio antes de aprobar.
- RC-05: modal Archivo solo-uploader, estados de procesamiento/OK/error y Aceptar habilitado solo con OK+candidatas; extractor sigue off-by-default.
- RC-06: vista standalone de extraccion sin radios de modo y sin lista inline de candidatas; destino declarado: Pendientes.

## Fronteras

- No se agrego ruta directa de escritura al ledger ni nuevo bypass; el front sigue usando `/api/protocol/actions/submit`.
- El gate PII de aprobacion de candidatas permanece en `submitCandidateApproval`.
- La carga por archivo conserva el mensaje OFF-by-default y depende de `fileIngestion.enabled`.
- No hubo cambios en `src/server.js`, `protocol.config.json`, runtime state ni configuracion #4.

## Evidencia

- `node --check public/app.js src/server.js tests/staticContract.test.js`: PASS.
- `git diff --check`: PASS.
- `node --test --test-name-pattern "TASK-0172" tests/staticContract.test.js`: PASS 7/7.
- `node --test --test-name-pattern "AC48|AC55|AC59|TASK-0172" tests/staticContract.test.js`: PASS 10/10.
- `npm test`: PASS 81/81.
- Clean clone `npm test`: PASS 81/81.
- Smoke local puerto 4234: `/healthz` OK y `/api/protocol/observe` OK.

## Notas de revision

Foco recomendado: no-bypass, gate PII en modal de candidata, extractor off-by-default, y que la reorganizacion visual no sugiera escritura directa fuera del flujo gobernado.
