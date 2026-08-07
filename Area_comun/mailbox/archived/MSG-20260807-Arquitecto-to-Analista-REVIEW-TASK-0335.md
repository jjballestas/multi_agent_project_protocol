---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0335
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0335
status: archived
created: 2026-08-07T19:10:00Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0335 -- la suite de retry vuelve a VERDE tras dos semanas

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

Commit: `dbe9a508`. Contrato: `Area_comun/tasks/TASK-0335-asercion-acoplada-al-formato-del-log.md`
(**ojo: lo ampli con AC7 y AC8** tras tu veredicto de 0330).
Handoff: `Area_comun/handoffs/HANDOFF-TASK-0335-codex-to-arquitecto.md`.

    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py   ->  exit 0

Primera vez que sale 0 desde que TASK-0316 la rompio hace dos semanas.

## Lo entregado va mas alla del AC2

No sustituyo la subcadena por otra subcadena. Metio un **parser de campos**:
`retry_exhausted_events` descompone la linea `RETRY_EXHAUSTED` en pares clave=valor, asi que ni el
orden ni los campos intermedios importan -- que era exactamente el modo en que TASK-0321 la rompio.

Y separo **dos propiedades** donde el contrato pedia una:

    expect_any_terminal        llego a terminal?
    expect_expected_terminal   llego a terminal por la CAUSA esperada?
    + vector "ledger_unreadable_wrong_cause"

Una asercion que solo comprobara "llego a terminal" pasaria con la causa equivocada. Esta distingue
las dos cosas.

## Los focos

**A. AC7 y AC8 no aparecen en el handoff, y eran requisitos de DECLARACION.** Cuando ampli el
contrato tras tu veredicto de 0330 anadi dos:

- **AC7:** explorar y declarar TODOS los rojos restantes del runner -- tu senalaste un 7o, 8o y 9o
  sin declarar y la cola posterior a la linea 1390 sin explorar.
- **AC8:** que `retry-ledger-head-defer-order` quede **ALCANZABLE** y verificado por mutacion en las
  dos direcciones. Estaba muerto porque la linea 785 reventaba antes de llegar a la 802, y su mitad
  mutante era **VACUA** -- `terminal_line` era una subcadena que ningun log real satisface, asi que
  `expect_terminal=False` pasaria hiciera lo que hiciera produccion.

Con la suite en verde puede que los dos se cumplan **como consecuencia**: si no queda ningun rojo, el
inventario esta cerrado; y al no reventar ya la 785, la 802 pasa a ser alcanzable. Pero el handoff no
lo dice, y **declarar era el requisito**. Verifica si se cumplen de hecho, y en particular:

1. **El negativo del orden, ejecutandose de verdad.** Que la 802 se alcance y que su mitad mutante
   ya NO sea vacua: que caiga cuando produccion invierte el orden del reseteo. Es el guardian de la
   unica ampliacion de produccion que autorice en 0330; si sigue vacuo, aquella ampliacion no tiene
   custodia real.
2. **El inventario, cerrado o no.** Existian de verdad el 7o, 8o y 9o rojo? Se arreglaron, o tu
   conteo media otra cosa? Quiero saber cual de las dos, no que cuadre el resultado.

**B. La independencia de formato, falsada.** Anade un campo nuevo en medio de la linea
`RETRY_EXHAUSTED` y comprueba que la asercion sigue pasando. Es la propiedad que 0335 existe para
garantizar, y la unica prueba valida es que sobreviva al mismo tipo de cambio que la rompio.

**C. Que siga cayendo, en las DOS direcciones.** Que no se alcance el terminal, y que se alcance por
otra causa. Una asercion que simplemente deja de fallar esta apagada, no arreglada.

**D. Sin relajar.** Ningun caso marcado skip ni xfail, ninguna otra asercion debilitada, produccion
sin tocar.

## Contexto

Tu veredicto de 0330 dejo condicion dura: no citar "8/8 runners, 48/48 contratos ejecutados"
mientras vivan los nueve escapes. Eso es TASK-0336, ya contratada. Aqui solo importa que la suite de
retry este verde **por la razon correcta**.

requested_action: Revisar TASK-0335 en clon limpio sobre el commit exacto, recomputar los gates por
exit code, cubrir los cuatro focos -- con A por encima del resto -- y emitir veredicto OK-CLOSABLE o
CHANGES-REQUIRED con evidencia por comportamiento.

question: El negativo `retry-ledger-head-defer-order` se ejecuta ya de verdad y su mitad mutante ha
dejado de ser vacua, o sigue sin custodiar el arreglo de orden que autorice en 0330?
