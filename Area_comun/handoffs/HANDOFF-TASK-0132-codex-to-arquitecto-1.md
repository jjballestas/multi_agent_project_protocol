---
handoff_id: HANDOFF-TASK-0132-codex-to-arquitecto-1
task_id: TASK-0132
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-20T12:05:00Z
---

# HANDOFF TASK-0132 - Front etapa 6.1

## Entrega

- Producto: `D:/Agentes/Zeus/Zeus-protocol`
- Commit producto: `a4acb68 feat(front): align selector and backlog with design`
- Insumos de diseno usados: `design/interface/components/selector/index.html`, `design/interface/components/kanban/index.html`, `design/interface/design-system/tokens.css`.

## Cambios

- Backlog ahora es kanban read-only con columnas `proposed`, `ready`, `in_progress`, `in_review`, `done`, filtro por agente y badges de claim activo.
- Projects ahora consume entidades `{id,name,kind,source,state}` y no rutas; la fuente actual es `zeus-product-root` bajo `D:/Agentes/Zeus`.
- Selector Projects incluye tarjetas de entidad y tarjeta `Add project` cableada a la accion gobernada RF-10 `project-kickoff-t0`.
- El selector no crea repos ni ejecuta `git init`; la escritura sigue pasando por `runtime/submit_intent.py`.
- PII: `renderEvent` fuerza `safePayloadPreview`, de modo que texto libre no se pinta crudo en la vista.
- `public/styles.css` adopta familias de tokens `--font-*`, `--fs-*`, `--sp-*`, `--radius*` del design system.

## Evidencia

- `npm test` PASS: 19 tests.
- `node --check public/app.js`, `node --check src/server.js`: OK.
- Smoke local en `http://127.0.0.1:4176`: `/healthz` OK, `/api/protocol/observe` 200, HTML con 7 paneles, filtro backlog y Projects.
- `python scripts/scan_encoding.py --root .`: OK.
- `python scripts/scan_domain_neutrality.py --root .`: OK.
- `python scripts/validate_collaboration_state.py --root .`: OK antes del cierre de la tarea.
- Drift: `has_drift=false`, `up_to_seq=806` antes del cierre.

## Caveats

- `design/front_pipeline.html` estaba dirty antes y no fue tocado.
- El smoke uso puerto 4176 para no interferir con procesos previos; fue detenido.
