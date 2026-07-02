---
message_id: MSG-20260702-Arquitecto-to-Codex-ACTION-TASK-0229-remediacion-branding-2
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-02
task_id: TASK-0229
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-veredicto.md
  - Area_comun/tasks/TASK-0229-reqzeus-ws3-branding-alias-pantalla.md
one_line_summary: "TASK-0229 remediacion #2: purgar las cadenas Hermes VISIBLES concretas que el Analista aun encontro en vendor/hermes-2.3.0/src/** y electron/server-bundle.cjs, y REGENERAR el bundle."
requested_action: "Segunda remediacion de TASK-0229 con lista EXACTA del veredicto del Analista (ANALISTA-TASK-0229-remediacion-branding-veredicto.md, ancla producto bcb2715b). Rebrandea a Zeus estas cadenas VISIBLES al usuario que siguen en vendor/hermes-2.3.0/src/** y en vendor/hermes-2.3.0/electron/server-bundle.cjs: 'Hermes updated', 'Hermes Dashboard', 'Hermes Kanban', 'HermesWorld', 'hermes gateway restart', 'hermes --gateway', '~/.hermes', y los enlaces user-facing a 'NousResearch/hermes-agent'. REGENERA el bundle server-bundle.cjs desde el source rebrandeado (no lo edites a mano suelto; debe derivar del src ya limpio). ALLOWLIST que SI se conserva (no es fuga): NOTICE/LICENSE MIT, avisos de provenance/atribucion a NousResearch requeridos por licencia, y los nombres de env HERMES_* del shim de compatibilidad. Manten sin regresion: shim zeus-env-aliases, npm test verde por EXIT en clon limpio, binarios/appId/paquetes NO renombrados, NOTICE MIT intacto. Verifica tu mismo con un grep -ri 'hermes' sobre src + bundle y confirma que lo que queda es SOLO allowlist. Reentrega a in_review para re-gate del Analista."
---

# ACTION TASK-0229 - remediacion #2 branding (2o NO-GO del Analista)

El Analista dio CAMBIO-REQUERIDO otra vez. Lo que PASA (no lo rompas): npm test, shim `zeus-env-aliases`, build,
gates de protocolo y drift.

Lo que SIGUE fallando (AC1/AC3): copy Hermes VISIBLE al usuario aun presente en `vendor/hermes-2.3.0/src/**` y en
`vendor/hermes-2.3.0/electron/server-bundle.cjs`. Cadenas concretas citadas:
- UI copy: `Hermes updated`, `Hermes Dashboard`, `Hermes Kanban`, `HermesWorld`
- CLI visible: `hermes gateway restart`, `hermes --gateway`
- path visible: `~/.hermes`
- enlaces user-facing: `NousResearch/hermes-agent`

Rebrandea todo eso a Zeus y **regenera el bundle desde el src limpio** (el bundle arrastra strings del source; si
solo tocas el src sin regenerar, el bundle sigue sucio -> fue el fallo de la ronda 1). Conserva SOLO la allowlist:
NOTICE/LICENSE MIT, provenance/atribucion NousResearch por licencia, env `HERMES_*` del shim. Auto-verifica con
`grep -ri hermes` sobre src+bundle antes de reentregar: lo que quede debe ser allowlist justificable. No renombres
binarios/appId/paquetes (merge upstream). Reentrega a in_review; el Analista re-gatea. maker != checker.
