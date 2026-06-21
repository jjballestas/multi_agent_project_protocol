---
handoff_id: HANDOFF-TASK-0140-codex-to-arquitecto-1
task_id: TASK-0140
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-21
product_repo: D:/Agentes/Zeus/Zeus-protocol
product_commit: 60fdb97
---

# HANDOFF TASK-0140 - Refetch fresco al navegar

## Resultado
- Producto: `60fdb97 feat(front): refresh data on navigation`.
- Archivos Zeus tocados: `public/app.js`, `public/index.html`, `public/styles.css`,
  `tests/staticContract.test.js`.
- UX read-only: no cambios en `src/server.js`, `runtime/submit_intent.py` ni superficie de escritura.

## Comportamiento entregado
- Al navegar entre vistas, el front ejecuta fetch fresco de `/api/protocol/observe`,
  `/api/protocol/actions` y `/api/help/manual`, y re-renderiza sin F5.
- Cada panel expone boton read-only de recarga manual por seccion.
- Existe refresco por intervalo configurable y opt-in; sin toggle activo no hay polling.
- Fallo de fetch pone la barra de estado en error y no invoca render como si los datos viejos fueran frescos.
- `renderBacklogFilter` ya no acumula listeners al re-renderizar.
- `personal/Codex/codex_mailbox_cron.ps1` queda actualizado a cadencia 5 minutos, dispatch de mensajes
  ejecutables para Codex y parada tras 7 rondas consecutivas sin respuesta nueva de Arquitecto.

## Evidencia
- `node --check public/app.js tests/staticContract.test.js src/server.js`: OK.
- `npm test`: 31/31 PASS.
- Smoke `node src/server.js` + `/healthz`: OK.
- Tests permanentes agregados:
  - Navegar dispara fetch + render.
  - Fetch fallido no se marca como fresco.
  - Recarga manual ejecuta fetch de la vista.
  - Intervalo opt-in respeta el valor configurado y se puede detener.
- Protocolo durante entrega: drift 0; validator/encoding/neutralidad a ejecutar en cierre.

## Nota
- El monitor queda configurado para arrancar en runtime local tras el commit de protocolo. Se detendra por
  orden de Arquitecto o automaticamente tras 7 rondas seguidas sin respuesta nueva de Arquitecto.
