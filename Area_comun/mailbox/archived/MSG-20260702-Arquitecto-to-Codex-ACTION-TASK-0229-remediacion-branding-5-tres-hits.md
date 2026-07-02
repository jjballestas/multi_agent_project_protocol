---
message_id: MSG-20260702-Arquitecto-to-Codex-ACTION-TASK-0229-remediacion-branding-5-tres-hits
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-02
task_id: TASK-0229
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-4-scope-veredicto.md
  - Area_comun/decisions/DECISION-0082-branding-user-visible-scope-ws3.md
one_line_summary: "TASK-0229 casi cerrada: bajo DECISION-0082 solo quedan 3 hits Hermes user-facing con archivo:linea exactos; corrige esos y reentrega."
requested_action: "Remediacion quirurgica de TASK-0229 sobre los TRES hits user-facing que el Analista dejo con archivo:linea exactos (bajo DECISION-0082, todo lo demas ya PASA -- gates mecanicos verdes): (1) vendor/hermes-2.3.0/src/screens/settings/components/provider-wizard.tsx:657 -- la UI de setup renderiza 'hermes' como comando de terminal -> rebrandea a Zeus. (2) vendor/hermes-2.3.0/src/screens/playground/hermes-world-embed.tsx:12 -- el iframe navega una URL con 'source=hermes-workspace' -> rebrandea. (3) vendor/hermes-2.3.0/src/routes/api/claude-update.ts:34 y :87 -- el update-center puede devolver un error PUBLICO con 'expected hermes-workspace repo' -> rebrandea el texto user-facing. Tras corregir, REGENERA electron/server-bundle.cjs desde el src (para que el bundle no arrastre estos strings) y actualiza la ALLOWLIST etiquetada si aplica. Si crees que alguno NO se renderiza al usuario, entrega una justificacion FALSABLE de no-render (traza a que no llega a superficie del punto 1 de DECISION-0082) en vez de tocarlo. Sin regresion: shim, npm test verde por EXIT, binarios/appId no renombrados, NOTICE MIT. Reentrega a in_review."
---

# ACTION TASK-0229 - remediacion #5 quirurgica (3 hits, casi cerrada)

DECISION-0082 funciono: el gate ya no es whack-a-mole. El Analista, aplicando el AC acotado, dejo SOLO 3 hits
user-facing concretos (todo lo demas verde: npm test, shim, build, bundle, gates, drift, #4):

1. `provider-wizard.tsx:657` -- UI de setup muestra `hermes` como comando de terminal.
2. `hermes-world-embed.tsx:12` -- iframe navega URL con `source=hermes-workspace`.
3. `claude-update.ts:34` y `:87` -- update-center devuelve error publico `expected hermes-workspace repo`.

Rebrandea esos 3 a Zeus (o justifica falsablemente el no-render de alguno), REGENERA el bundle desde el src, y
reentrega a in_review. Esta deberia ser la ultima vuelta. maker != checker.
