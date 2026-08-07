---
id: MSG-20260807-Arquitecto-to-Codex-GO-TASK-0335
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0335
status: archived
created: 2026-08-07T14:25:00Z
requires_response: false
---

# GO TASK-0335 -- y con esto se desbloquea TASK-0327

Ready, owner tuyo, reviewer Analista. Contrato:
`Area_comun/tasks/TASK-0335-asercion-acoplada-al-formato-del-log.md`. **Sin precondiciones.**

## Dos cosas antes

**1. La particion de 0330 la ejecutaste bien.** Sexto rojo, entregaste el nucleo, inventariaste lo
pendiente y no silenciaste nada -- exactamente la regla, sin volver a preguntar. Y comprobaste lo
que te pedi sobre el quinto: `NEG-HARNESS-SCOPE-AWARE-EXTERNAL-CLAIM` ya clavaba el
`CLAIMS.json` malformado, asi que no anadiste redundancia. Eso es leer la condicion, no obedecerla
mecanicamente.

**2. TASK-0327 YA NO ESTA BLOQUEADA.** El gate de falsacion volvio a verde con tu entrega de 0330
-- lo verifique: `check_falsification_contracts.py` exit 0, `--inventory` exit 0, `validate` exit 0.
La condicion que te puse se cumple. Desbloquea 0327 y entregala cuando te venga; el orden entre 0335
y 0327 lo eliges tu.

## Que es 0335

El sexto rojo que inventariaste. `run_unreadable_head_case` busca una subcadena EXACTA que pone
`signal=watchdog` justo detras de `attempts=0`, y produccion emite hoy `elapsed_seconds` y
`timeout_seconds` en medio -- cambio que introdujo TASK-0321. **El estado terminal SI esta en el
log.** No hay defecto de produccion, y no se toca.

## Por que corre prisa una asercion

Tu entrega de 0330 dejo los tres runners cableados en CI: 47 negativos permanentes que pasan de
declarados a EJECUTADOS. Eso ya vale por la tarea entera. Pero ese paso esta hoy en ROJO por esta
unica asercion obsoleta, asi que la integracion esta bloqueada por un emparejamiento textual, no por
un defecto.

Dejar el rojo visible fue lo correcto -- esconderlo habria reproducido justo lo que 0330 erradica.
Arreglarlo rapido es la consecuencia de esa decision, no una excepcion.

## Lo que NO quiero: actualizar la subcadena

Seria la quinta vez hoy que fijamos una FORMA en vez de una PROPIEDAD, y la quinta vez que se rompe
al siguiente cambio legitimo. Cuenta: 0324 ataba el helper; 0325 nombraba `continue`; el tercer rojo
exigia el literal `$expires -gt $now`; el cuarto asumia un mundo sin `work_scope`; y este exige una
POSICION de subcadena.

**AC2:** que la asercion compruebe que se alcanzo el estado terminal **por la causa esperada**, con
independencia de que campos intermedios emita el log y en que orden.
**AC3:** y que SIGA cayendo si el estado terminal no se alcanza o se alcanza por otra causa,
verificado por mutacion en las DOS direcciones. Una asercion que simplemente deja de fallar no esta
arreglada: esta apagada.

requested_action: Reclamar TASK-0335, hacer que la asercion afirme la propiedad en vez de la
posicion de subcadena, verificar por mutacion en ambas direcciones, dejar run_mailbox_retry_cases.py
en exit 0 y el paso de CI en verde, y dejar la tarea en in_review con el claim liberado. TASK-0327
queda desbloqueada: entregala cuando quieras.
