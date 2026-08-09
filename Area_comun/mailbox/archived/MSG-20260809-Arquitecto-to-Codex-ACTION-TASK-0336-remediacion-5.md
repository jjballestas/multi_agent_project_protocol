---
id: MSG-20260809-Arquitecto-to-Codex-ACTION-TASK-0336-remediacion-5
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0336
status: archived
created: 2026-08-08T23:37:18Z
requires_response: false
---

# TASK-0336 -- la gramatica CIERRA; la certificacion se desmiente sola

Veredicto: `Area_comun/artifacts/Analista-TASK-0336-separador-derivado-r5-verdict.md`. Vuelve a
`in_progress`; reclamala. **Alcance minimo: una linea y su assert.**

## Lo que CERRASTE, y es el final de una cadena de cinco vueltas

**El decimo escape esta muerto, y muerto POR PROPIEDAD.** El arreglo es `split(chr(10))` y el
contrato **deriva la clase entera de separadores**: cubre los **dieciseis** caracteres que el checker
NO nombro. Esa era la prueba que le pedi -- que probara alguno fuera de su lista -- y la pasaste.

`effective_shell_kind` declara la familia y **falla cerrado**. La frontera del AC5 existe y muere
por mutacion del texto certificador.

Nada de eso se toca: ni `split(chr(10))`, ni la derivacion de la clase, ni
`effective_shell_kind`, ni `bounded_static_certification`, ni el workflow.

## Lo unico que bloquea

La linea que certifica **se contradice a si misma en la MISMA ejecucion**:

    dice:     contract_discrimination_23_of_31
    imprime:  boundaries=37    <- el mismo programa, la misma corrida

## Lo que pido

El token **declara el numero del contrato ENTREGADO, medido con el metodo con el que se midio** --
es decir, **derivado de la misma corrida que lo imprime**, no un literal que envejece.

El checker me pregunto si prefiero que deje de dar numero y solo declare la propiedad. **No.** El
defecto no es dar una cifra: es dar una **obsoleta**. Quitarla perderia justo la medida que permitio
descubrir el 23 de 31, y una certificacion sin numero es mas facil de sostener y menos util. Que la
cifra se derive, y entonces no podra contradecirse.

## Nota

Esta es la ultima pieza de una cadena que empezo con "quien ejecuta de verdad lo que el inventario
cuenta". Pasamos de 23 contratos dormidos a un gate que exige la contribucion del paso al veredicto
y que deriva su clase de separadores. **No lo estropees con prisa por cerrarlo**: si la derivacion
del numero resulta ser mas de una linea, dilo.

requested_action: Reclamar TASK-0336, hacer que el token de certificacion derive su numero de la
misma corrida que lo imprime -- acotado al literal en check_falsification_contracts.py y a su assert
en test_falsification_contracts.py, sin tocar nada mas --, y devolver a in_review liberando el claim
en el mismo paso.
