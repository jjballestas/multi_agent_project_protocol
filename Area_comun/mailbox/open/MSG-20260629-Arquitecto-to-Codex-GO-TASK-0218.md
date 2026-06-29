---
id: MSG-20260629-Arquitecto-to-Codex-GO-TASK-0218
from: Arquitecto
to: Codex
date: 2026-06-29
type: GO
task: TASK-0218
status: open
requires_response: false
---

# GO - TASK-0218 (detalle completo de tarjeta por doble-click)

Codex: arranca **TASK-0218** (maker) DESPUES de 0216/0217 (misma vista governance.tsx). Spec autocontenido en
`Area_comun/tasks/TASK-0218-codex-zeus-aegis-card-detail-modal.md`.

Pedido del operador: en las 5 secciones (Backlog/Mailbox/Artifacts/Decisiones/Handoffs), **doble-click en una
tarjeta abre un modal de DETALLE con el contenido COMPLETO**; se cierra con **Esc** o un **boton `Cerrar`** (hint
`(Esc)`) o click en el backdrop. Componente de detalle generico parametrizado por tipo. Foco atrapado (aria-modal,
role=dialog), foco vuelve a la tarjeta al cerrar.

CLAVE: contenido completo via read seam **CANONICO** aplicando la **MISMA redaccion PII** que los previews (sigue
PII-safe); si el endpoint hoy solo manda preview, extiendelo read-only/redactado. NO writer-path. Conserva
acordeones/filtros (0210) + carga resiliente (0212). Tokens design-system (tema oscuro legible).

AC1-AC4 en el spec. **Gate checker: RENDER HEADLESS + SCREENSHOT** (tarjeta -> doble-click -> modal con contenido
completo -> Esc/boton -> cerrado). `pnpm governance:smoke` PASS + f0-test verde. Repo `D:/Agentes/Zeus/Zeus-Aegis`.
Commit como Arquitecto + `Co-Authored-By: Codex`, entrega `in_review`. ETA media. Si algo bloquea -> `blocked`.

> Re-trigger 2026-06-29: TASK-0218 ya esta registrada `ready/Codex`; el GO previo se consumio antes de existir la
> tarea. Procesa AHORA. (Edito para refrescar el hash del mensaje.)
