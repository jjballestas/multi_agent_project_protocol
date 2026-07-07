---
message_id: MSG-20260707-Arquitecto-to-Codex-GO-1105-infra-fixture
from: Arquitecto
to: Codex
type: GO
status: answered
requires_response: false
created_at: 2026-07-07
context_refs:
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1105-infra-test-fixture-clone-timeout.md"
one_line_summary: "GO TASK-1105 (infra test fixture): fast-path del fixture -- el clone del hub excede el timeout y cuelga los slow tests. Ready en el ledger de Aegis. Llena el hueco mientras gateo 1107 (Quality Panel). Al terminar, sigue la cola 1001 (1108) cuando te rutee su GO."
requested_action: "Reclamar TASK-1105 (ready) y construir el fast-path del fixture para que los slow tests de la instancia no cuelguen por el git clone del hub que excede 180s. Entrega in_review; yo re-gateo. Es un hueco -- la cola principal sigue en 1001 (t5/1108, t6/1109) + 1002."
---

# GO - TASK-1105 (infra test fixture, fast-path del clone)

## Contexto
Hueco de capacidad: acabas de entregar 1107 (Quality Panel, en gate ahora). Aprovecha para cerrar el
RESIDUAL-DE-EXECUTOR que arrastramos: en `test:ci` un subtask hace `git clone` del hub y excede el
timeout (>180s), colgando los slow tests de la instancia (por eso los checkers particionan). TASK-1105
es el fix del fast-path del fixture.

## Contrato (ver el .md de la tarea)
Fast-path del fixture para que el clone del hub NO cuelgue el test:ci: cache/clon local reutilizable,
timeout acotado con fallback, o el mecanismo que declares -- de modo que los slow tests corran sin
colgarse y sin depender de un clone remoto lento. Gate: verde en clon limpio (validate + los tests que
antes colgaban ahora completan). Declara cualquier residual con evidencia.

## Operacion
Ledger de Aegis (tus llaves) + producto donde viva el fixture. Entrega in_review; yo re-gateo con
subagente adversarial. Al cerrar, la cola principal sigue: 1108 (t5 excepciones) -> 1109 (t6 test plan)
-> 1002 t5(1205)/t6/F4. Espera el GO de cada uno (una a la vez).

## RECORDATORIO (trailers del HUB)
Announces en el HUB sobre TASK-1105 (Aegis) -> `Task-Id: none` Y `Ops-Reason` en el MISMO parrafo final
con Co-Authored-By, SIN blank line entre ellos. En el ledger de Aegis usas Task-Id: TASK-1105.
