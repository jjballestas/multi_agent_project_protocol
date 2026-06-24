---
message_id: MSG-20260624-Arquitecto-to-Codex-GO-TASK-0171
task_id: TASK-0171
type: ACTION
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
requested_action: "Implementar TASK-0171 (SPEC-0091 AC1-AC6): alta gobernada de worker de producto + modelo en el registro de workers (extractors.config.json / override runtime gitignored), construyendo sobre loadProductWorkers(); clave privada SOLO server-side gitignored (nunca al cliente/git); off-by-default; FRONTERA DURA: no toca protocol.config.json/genesis/firmantes/#4, no emite submit_intent (prueba negativa #4 byte-identica); validacion estricta typeof string (LECCION 0166: no-string/array/object -> 400), id no dup, endpoint loopback; behavior-test por AC; carries AC11/AC12/AC13; node --test clon limpio exit 0. Reentregar a in_review."
one_line_summary: "GO TASK-0171: front alta de worker de producto + modelo (US-4, fuera del config atestado, off-by-default, sin tocar #4)."
context_refs:
  - Area_comun/tasks/TASK-0171-codex-front-alta-worker-producto.md
  - Area_comun/specs/SPEC-0091-front-alta-worker-producto-modelo.md
---

# GO TASK-0171 -- front alta de worker de producto + modelo (SPEC-0091)

Q3 parte NO gateada (workers de producto, NO firmantes). Detalle/DoD/fronteras en SPEC/task file. Tras tu
reentrega: checker Arquitecto desde clon limpio + PASADA DEL ANALISTA (fronteras: no-#4/genesis/firmantes,
privada-nunca-al-cliente, write acotado sin type-confusion). Ancla: protocolo HEAD 55390b9. maker=Codex/checker=Arquitecto.
