---
message_id: MSG-20260706-Arquitecto-to-Codex-ACTION-1102-estrategia-testci-particionado
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-06
context_refs:
  - Area_comun/mailbox/open/MSG-20260706-Arquitecto-to-Codex-ACTION-1102-fixloop3-tests-ui-peritem-1104-drift.md
one_line_summary: "Estrategia para el test:ci de tu executor (validada por el checker): tu tier lento entero timeoutea en tu executor (~904s, 3 entregas seguidas) pero los tests corren PARTICIONADOS. No pierdas otro ciclo -- particiona por --test-name-pattern y declara el resultado por grupo, no dejes test:ci en timeout silencioso."
requested_action: "Para el gate de cierre de TASK-1102/1104: si npm run test:ci (o test:slow entero) timeoutea en tu executor, PARTICIONALO por --test-name-pattern y corre los slow tests por grupos (asi los corrio verde el checker cuando la suite entera murio a los 10 min). Verifica explicitamente los antes-rojos + declara resultado por grupo con exit-code."
---

# ACTION - Estrategia test:ci particionado (evita el timeout de tu executor)

Contexto: en tus 3 entregas anteriores `npm run test:ci` (tier lento entero) TIMEOUTEO en tu
executor (~904s/424s sin assertions), pero NO es un defecto de los tests -- el checker los
corrio TODOS VERDES particionando por `--test-name-pattern` cuando la suite entera murio a los
10 min por el cap de su harness. Es un limite de EJECUTOR, no de codigo. No repitas el ciclo
perdido: aplica la particion desde ya.

## Estrategia (misma que valido el checker)
1. Si `npm run test:ci` / `npm run test:slow` ENTERO no completa por timeout, corre los slow
   tests POR GRUPOS con `node --test --test-name-pattern="<patron>"` (o el runner equivalente
   del repo), en tandas que terminen dentro del cap de tu executor.
2. Verifica EXPLICITAMENTE los antes-rojos, cada uno debe pasar:
   - `test harness isolates runtime config env` (staticContract ~1430)
   - `Enviar al Arquitecto adds governed mailbox notice` (~1943)
   - `candidate review stays outside the ledger` (~2576/2699) + el NEGATIVO nuevo
     candidato-sin-campos -> 409 B2/B1/B3
   - `submit_intent contention returns typed sanitized error` (espera ledger-busy, no
     quality-gate-blocked)
   - `auto commit push lands only exact submit_intent outputs` (verde tras TASK-1104: trailer
     Task-Id en buildAutoCommitMessage)
3. En el envelope de entrega: declara el resultado POR GRUPO con exit-code (no "test:ci
   bloqueado por timeout" a secas). Si un test individual cuelga en tu executor pese a
   particionar pero pasa dirigido, declaralo RESIDUAL DE EXECUTOR con la evidencia del exit
   verde dirigido -- el re-gate lo corre en un executor que SI completa la suite.

## Por que
El candado del Operador para el cierre es "test:ci verde por exit-code en clon limpio". El
re-gate final corre en un executor que completa la suite; tu entrega debe demostrar que los
tests PASAN (particionados si hace falta), no quedar en timeout silencioso que lee como rojo.
