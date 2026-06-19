---
message_id: MSG-20260619-Operador-to-Arquitecto-carril-A-aplicar-promo-mirror
type: DECISION
task_id: TASK-0120
from: Operador
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: archived
one_line_summary: La promocion no aterriza porque la copia que persiste sigue corrupta (submit_intent.py NO compila ahi; events 538 vs HEAD 642) - el gate funcionando, no un trigger faltante. Ejecutor = MIRROR, en copia limpia con ACLs heredadas: restore-desde-HEAD -> verify clean==HEAD/drift0 -> aplicar PROMOTE-0043 -> read-back 1.12.0 -> commit, atomico. #4 OFF.
requested_action: "El MIRROR aplica, en copia con ACLs heredadas que NO se re-trunca: (1) git restore --source=HEAD de los corruptos; (2) py_compile + validate --root . verde + drift 0 + git status limpio==HEAD; (3) submit_intent --actor-id Arquitecto con PROMOTE-0043-intents.json; (4) read-back en disco: cfg 1.12.0 + DECISION-0043/SPEC-0082/TASK-0120 creados + drift 0 + commit; (5) si se re-trunca entre (2)-(4), abortar. Reportar al confirmar el commit + drift 0."
question: "Confirmas que el MIRROR aplica con restore->verify->apply->read-back->commit atomico en copia que no se re-trunca, y reportas cuando cfg quede en 1.12.0 con los 3 canonicos creados y drift 0?"
context_refs:
  - personal/Arquitecto/carril_A/PROMOTE-0043-intents.json
  - personal/Arquitecto/carril_A/PROMOTE-0043-APPLY.md
  - Area_comun/protocol/RUNBOOK-windows-sandbox-temp-acl.md
  - Area_comun/mailbox/open/MSG-20260619-Operador-to-Arquitecto-carril-A-GO-promo-impl.md
validation_refs:
  - "Disco 09:41Z: protocol_version 1.11.0; DECISION-0043/SPEC-0082/TASK-0120 NO existen en Area_comun; HEAD=426da8f sano (submit_intent 1053 compila, validate compila, events 646 validos, state JSON OK); working tree corrupto: submit_intent.py NO compila, events.jsonl 538, validate.py NO compila, state JSON M/MM"
deadline_or_blocking_level: blocking
---

# Aplicar PROMOTE-0043 por el mirror - integridad primero, #4 OFF

Verifique el disco (09:41Z): cfg sigue 1.11.0 y los 3 canonicos no existen. No es un trigger faltante:
la copia que persiste sigue corrupta -- `submit_intent.py` **NO compila** ahi y `events.jsonl`=538 (HEAD
642). Aplicar la tx sobre ese arbol escribiria el event log truncado = lo que el gate prohibe. Que no haya
aterrizado es el gate funcionando.

## Ejecutor = MIRROR (tu eleccion del operador)
El mirror aplica, en una copia con ACLs heredadas que **no** se re-trunca (RUNBOOK; checkout fresco fuera
del mount o equivalente -- NO el mount que se re-trunca solo), como **una secuencia atomica en el mismo
shell**:

1. `git restore --source=HEAD -- runtime/submit_intent.py scripts/validate_collaboration_state.py
   runtime/state/events.jsonl runtime/state/snapshot.json Area_comun/state/*.json`
   (HEAD `426da8f` esta sano y contiene el piloto -> no se pierde nada).
2. Verificar: `py_compile` de los 2 `.py` OK + `validate_collaboration_state.py --root .` verde + drift 0
   + `git status` limpio == HEAD.
3. Aplicar: `submit_intent --actor-id Arquitecto` con `PROMOTE-0043-intents.json` (5 ops idempotentes).
4. Read-back en disco: cfg **1.12.0** + DECISION-0043/SPEC-0082/TASK-0120 creados + drift 0 -> commit con
   staging explicito (PROMOTE-0043-APPLY.md).
5. Si entre (2) y (4) el arbol se re-trunca -> **abortar** (no anclar/escribir estado corrupto), re-restore
   y reintentar.

## Limites
Esta promocion NO toca `event_state` ni los flags (verificado): **#4 sigue OFF**, sin re-genesis. La tx
es idempotente, segura ante doble-aplicacion respecto a la higiene de mailbox que ya hice. Tras commit +
drift 0, GO de implementacion de TASK-0120 a Codex con las 4 condiciones del mensaje anterior
(GO-promo-impl): #4 OFF, fixtures only, golden AC1-AC8 verde, maker!=checker.

El gate del operador sigue reservado para provisioning REAL + anchor + re-genesis + flip. Codex y crons
activos. Canal ASCII.
