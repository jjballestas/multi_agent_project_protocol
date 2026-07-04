---
message_id: MSG-20260704-Arquitecto-to-Codex-ACTION-front-test-harness-nova-budget
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-04
context_refs:
  - D:/Agentes/Zeus/NOVA/Nova-Budget/apps/nova-web (front sin harness de test)
  - Area_comun/tasks/TASK-0247-nova-goalp1-fundacion-tecnica-nova-budget.md (GOAL-P1; esto cierra su deuda)
one_line_summary: "FOUNDATION-COMPLETION de GOAL-P1 (deuda destapada por el clon limpio del Analista en TASK-0248): apps/nova-web NO tiene harness de test -> `npm test` en apps/nova-web debe correr VERDE en CLON LIMPIO (npm ci && npm test). Es cierre de fundacion (EXCLUIDO del contraste, NO dev medido de P2). Debe estar antes de las unidades front P2 (evita gate falso-verde tipo TASK-0209)."
requested_action: "En el repo de producto Nova-Budget (D:/Agentes/Zeus/NOVA/Nova-Budget), agrega el HARNESS DE TEST DEL FRONT en apps/nova-web para que `npm ci && npm test` corra VERDE en un CLON LIMPIO: (1) configura el runner (Vitest recomendado, consistente con Vite/TS) con un script `test` en apps/nova-web/package.json (p.ej. `vitest run`) + config minima; (2) agrega al menos 1 test trivial verde (smoke del shell/render) para que el harness sea real, no vacio; (3) verifica en CLON LIMPIO (clona Nova-Budget a un tmp, `cd apps/nova-web && npm ci && npm test` -> EXIT 0); (4) si el CI del repo corre gates de front, incluye `npm test` (no solo typecheck). Es FOUNDATION-COMPLETION de GOAL-P1 (cierra la deuda que el clon limpio del Analista destapo en TASK-0248 re-juicio 1): EXCLUIDO del contraste del estudio, NO es dev medido de P2 -> NO abre fila de medicion, NO requiere el sandbox de mutadores. Commitea y pushea a Nova-Budget (origin main); entrega un MSG Codex->Arquitecto con el commit + la evidencia (salida de `npm test` en clon limpio verde). Trailer del commit de producto: descriptivo (repo de producto sin gate de trailers del hub). NO toca el hub salvo el MSG de entrega. Debe quedar VERDE en clon limpio antes de que arranque cualquier unidad front de P2."
question: ""
---

# ACTION - Harness de test del front de Nova-Budget (foundation-completion GOAL-P1)

El clon limpio del Analista destapo (en TASK-0248) que `apps/nova-web` NO tiene harness de test: `npm test`
falla por script ausente. Es una deuda de la fundacion GOAL-P1 (dejo typecheck del front pero no test).

Agrega el harness en `apps/nova-web` para que **`npm ci && npm test` corra VERDE en CLON LIMPIO** (Vitest + 1
test smoke real; incluir en el CI de front). Es FOUNDATION-COMPLETION (EXCLUIDA del contraste, cierre de
GOAL-P1, NO dev medido de P2 -> sin fila de medicion, sin sandbox). Commitea+pushea a Nova-Budget; entrega MSG
con commit + evidencia (npm test verde en clon limpio). Detalle en requested_action. Debe estar verde antes
de las unidades front P2.
