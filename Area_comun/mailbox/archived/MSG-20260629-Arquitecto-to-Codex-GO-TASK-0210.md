---
id: MSG-20260629-Arquitecto-to-Codex-GO-TASK-0210
from: Arquitecto
to: Codex
date: 2026-06-29
type: GO
task: TASK-0210
status: archived
requires_response: false
---

# GO - TASK-0210 (UX de las vistas del panel governance)

Codex: arranca **TASK-0210** (maker). TASK-0209 (performance) ya cerro DONE. Spec autocontenido en
`Area_comun/tasks/TASK-0210-codex-zeus-aegis-panel-views-ux.md`.

Encargo (feedback del operador, todo READ-ONLY, no contamina TFM): el panel `/governance` es usable para
OBSERVAR.
- **Acordeones colapsados por defecto:** las 6 secciones (Backlog, Mailbox, Artifacts, Decisiones,
  Ledger/atestacion, Handoffs) son desplegables con header (titulo + conteo + chevron), COLAPSADAS por
  defecto; persistir abierto/cerrado por sesion (localStorage) es deseable.
- **Recientes + Mostrar mas:** cada seccion lista solo los N mas recientes (p.ej. 10, fecha/seq desc) +
  boton "Mostrar mas". No volcar todo de golpe.
- **Filtros legibles (tema oscuro):** los `<select>` nativos salen texto gris ilegible -> estilizarlos con
  tokens del design-system (fondo panel, texto ink, hover accent) para contraste suficiente.
- **Mailbox con filtros** (paridad con Backlog: carpeta open/answered/archived, from/to, tipo, texto).
- **Artifacts con combo por TIPO** (handoff/review/report/...) ademas del campo de texto.

Fuera de alcance: NO operar/escribir (F2 gateado post-TFM); NO tocar el binario hermes/HERMES_API_*; NO core
ni baseline TFM. AC1-AC6 en el spec; `pnpm governance:smoke` PASS + f0-test verde.

**Gate de cierre del checker (Arquitecto): RENDER HEADLESS + SCREENSHOT** (Playwright + chrome del sistema via
NODE_PATH al vendor) que evidencie: colapsado-por-defecto, un combo legible en tema oscuro, y filtros de
Mailbox/Artifacts. Lecciones: verifica en clon limpio sin dist residual; el screenshot es obligatorio.

Repo `D:/Agentes/Zeus/Zeus-Aegis`. Reclama via submit_intent (Ed25519), commit como Arquitecto +
`Co-Authored-By: Codex`, entrega `in_review`. ETA: media. Si algo bloquea -> `blocked` + una pregunta.

Nota (opcional, NO bloqueante): el chip de salud sale `unknown` cuando endpoints NO-governance
(/api/auth-check, /api/provider-usage) dan 503 por el load() todo-o-nada; si es barato, que el panel pinte la
salud governance aunque fallen endpoints ajenos. Si no, queda como follow-up.
