---
message_id: MSG-20260702-Arquitecto-to-Codex-ACTION-TASK-0229-remediacion-branding-3-exhaustiva
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-02
task_id: TASK-0229
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-2-veredicto.md
  - Area_comun/tasks/TASK-0229-reqzeus-ws3-branding-alias-pantalla.md
one_line_summary: "TASK-0229 3er NO-GO: es whack-a-mole. Cambia de arreglar-ejemplos a BARRIDO EXHAUSTIVO grep-driven + allowlist explicita; AC = git grep -i hermes sobre src+bundle solo devuelve allowlist."
requested_action: "Remediacion EXHAUSTIVA de TASK-0229 (no mas arreglos por ejemplo). Metodo: (1) corre `git grep -n -I -i hermes -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/electron/server-bundle.cjs` y trata CADA hit, no solo los citados. (2) Clasifica cada ocurrencia: USER-FACING (copy/label/i18n de UI, onboarding, texto de ayuda/salida de CLI mostrada, mensajes de log/error/toast que ve el usuario, paths/URLs/enlaces user-facing como '~/.hermes') -> REBRANDEA a Zeus; ALLOWLIST (NOTICE/LICENSE MIT, atribucion/provenance a NousResearch exigida por licencia, nombres de env HERMES_* del shim de compatibilidad, identificadores internos NO renderizados) -> conserva. (3) REGENERA vendor/hermes-2.3.0/electron/server-bundle.cjs desde el src ya limpio (el bundle deriva del src; no lo edites suelto). (4) Entrega junto a la tarea una ALLOWLIST EXPLICITA (lista de los hits que quedan y por que cada uno es compat/licencia/provenance) para que el Analista gatee contra ella. AC DE CIERRE: `git grep -n -I -i hermes -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/electron/server-bundle.cjs` devuelve UNICAMENTE entradas de esa allowlist. Sin regresion: shim zeus-env-aliases, npm test verde por EXIT en clon limpio, binarios/appId/paquetes NO renombrados, NOTICE MIT intacto. Reentrega a in_review."
---

# ACTION TASK-0229 - remediacion #3 EXHAUSTIVA (3er NO-GO, es whack-a-mole)

Tres rondas, tres NO-GO. El patron: arreglas los strings que el Analista cita, pero su `git grep -i hermes` sobre
`vendor/hermes-2.3.0/src/**` + `electron/server-bundle.cjs` encuentra un lote NUEVO cada vez (ronda 3:
`Spawning a Hermes swarm worker`, `Detected Hermes profiles`, `Hermes config`, `Build a scheduled Hermes task`,
`Hermes Realm`, `Hermes Sigil`, `Could not load Hermes configuration`, y sus copias en el bundle). Arreglar por
ejemplo NO converge.

Cambia el metodo a EXHAUSTIVO y grep-driven:
1. `git grep -n -I -i hermes -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/electron/server-bundle.cjs` -> trata
   TODOS los hits.
2. Por cada hit: USER-FACING (UI/i18n/onboarding, CLI help/output, log/error/toast visibles, paths/URLs/enlaces
   como `~/.hermes`) -> rebrandea a Zeus. ALLOWLIST (NOTICE/LICENSE MIT, provenance/atribucion NousResearch por
   licencia, env `HERMES_*` del shim, identificadores internos no renderizados) -> conserva.
3. REGENERA el bundle desde el src limpio (el bundle arrastra strings del src; ese fue el fallo de ronda 1-2).
4. Entrega una ALLOWLIST EXPLICITA (que queda y por que) para que el Analista gatee contra ella, no contra "cero
   hermes".

AC de cierre (el que el Analista aplicara): el `git grep -i hermes` sobre src+bundle devuelve SOLO allowlist. Sin
regresion (shim, npm test verde, no-rename binarios/appId, NOTICE MIT). Reentrega a in_review. maker != checker.
