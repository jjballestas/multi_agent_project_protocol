---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0193-fix-build
task_id: TASK-0193
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
question: "Confirmas que arreglas el build de Zeus-Aegis hasta npm test exit 0 en clon limpio, o hay un bloqueo que reportar?"
requested_action: "TASK-0193 esta en changes_requested: la revision adversarial del Analista (TASK-0194, V6) reprodujo que Gate 0 NO esta verde -- en clon limpio del commit entregado, npm test del vendor Hermes sale exit 1 con 24 fallos (Windows; dashboard real pendiente; TypeScript rojo). Arreglar el entorno/suite de Zeus-Aegis hasta npm test exit 0 reproducible en CLON LIMPIO, re-handoff a Arquitecto. Si algun fallo es ajeno al fork y no corregible, documentarlo y proponer waiver acotado."
one_line_summary: "GO: arreglar build de Zeus-Aegis hasta npm test exit 0 en clon limpio (Gate 0 no verde, hallazgo V6 del Analista). TASK-0193 changes_requested."
context_refs:
  - Area_comun/tasks/TASK-0193-codex-zeus-aegis-f0-fork-seams.md
  - Area_comun/artifacts/ANALISTA-TASK-0194-veredicto.md
---

# GO - Arreglar build de Zeus-Aegis hasta verde (TASK-0193)

La revision adversarial del Analista (TASK-0194, recomendacion CAMBIO-REQUERIDO) reprodujo el hallazgo **V6**: el
**Gate 0 de Zeus-Aegis NO esta verde**. Evidencia del Analista en clon limpio del commit F0 (f87317c):

- `npm test` en `vendor/hermes-2.3.0` sin deps -> exit 1 (`vitest` no reconocido).
- `corepack pnpm install --frozen-lockfile; npm test` -> exit 1; install reporta ignored builds; vitest corre pero
  deja **24 fallos** (Windows; dashboard real pendiente; TypeScript rojo).
- Root de Zeus-Aegis sin `package.json` testeable.

Bajo la regla "gatear por exit code", F0 no es cerrable como verde. **TASK-0193 -> changes_requested.**

## Que arreglas

- Dejar `npm test` (o el runner que corresponda) **exit 0 reproducible en CLON LIMPIO** del commit de Zeus-Aegis,
  desde el entorno real (no sandbox stale). Resolver los 24 fallos de vitest / TypeScript / el approve-builds de
  pnpm en Windows.
- Si un subconjunto de fallos es estructural del upstream Hermes y NO corregible sin salir del pin v2.3.0, NO lo
  escondas: documentalo en `docs/SEAMS.md` y propon un **waiver acotado** (que exactamente queda fuera y por que),
  para que el operador decida.
- Re-handoff a Arquitecto (checker) con la evidencia de exit 0 (o el waiver propuesto).

## Limites

- Solo repo PRODUCTO Zeus-Aegis. NO tocar el core del protocolo, #4, ni el baseline (esto es producto, no aparato).
- Pin Hermes v2.3.0; no perseguir main. Commit como Arquitecto con Co-Authored-By Codex. Minimal narration.
- Bloqueo -> blocked + una pregunta concreta.
