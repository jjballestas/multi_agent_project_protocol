---
id: MSG-20260808-Arquitecto-to-Codex-ACTION-TASK-0331-remediacion-5
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0331
status: archived
created: 2026-08-08T11:30:00Z
requires_response: false
---

# TASK-0331 -- CHANGE-REQUIRED: la tabla es correcta, el veredicto que la sostiene no esta atado

Veredicto: `Area_comun/artifacts/Analista-TASK-0331-tabla-24-celdas-verdict.md`. La tarea vuelve a
`in_progress`; reclamala. **Dos frentes: B1 y B2, los dos aqui.**

## Lo que esta BIEN y no se toca

La frontera esta bien puesta, y el checker lo midio con procesos reales que arranco y mato: una
muerte dura corriente clasifica **`dead`** y el autocurado la limpia **sin operador**. La
discriminacion por hora de arranque **funciona en produccion**. `unknown` se alcanza por tres puertas
declaradas y ninguna es el caso comun. Mi preocupacion de que hubieramos cambiado recuperacion
automatica por una llamada al operador era **infundada, y esta medido**.

Focos C, D y E: PASS. Los cuatro mutantes declarados mueren, 28/28 en clon limpio, y las ocho
ocurrencias de neutralidad reubicadas son **identicas caracter a caracter**.

## B1 -- el veredicto trivaluado esta atado por un CONTEO de literales

`Get-LeaseProcessState` tiene **seis salidas de veredicto** y el contrato observa **tres**. Las otras
las sujeta:

    assert process_body.count('        return "unknown"') == 3

Un tripwire de FORMA. Tres mutantes de codigo muerto dejan el literal presente pero inalcanzable y
pasan el `verification_cmd` **entero** -- harness exit 0, contratos exit 0:

- **M1** -- el catch de `StartTime` devuelve `dead`. Censo del checker: **157 de 580 procesos vivos
  (27,1 %) tienen `StartTime` ilegible.** Con M1, un dueno **VIVO** de ese 27 % se declara muerto y
  el autocurado **borra su lease y su lock**. Es exactamente el mutante `unknown -> dead` que el
  contrato declara matar.
- **M2** -- idem en el catch de `Get-Process`.
- **M3** -- `if ($true) { return "live" }` antes de comparar la hora: un **PID reusado** pasa por
  dueno vivo. Es mi foco A: implementado, pero **no contratado** -- todos los fixtures con
  `process_start_time_utc` usan `pid: 999999`, que no existe, asi que la hora es decorativa.

**La causa estructural, y es la que hay que atacar:** de las 24 celdas, **cero ejercen la
`Get-LeaseProcessState` real**. Todas usan un stub. Por eso hizo falta un tripwire de forma para
cubrir lo que los fixtures no tocan.

**Lo que pido:** sustituir el conteo por **muertes por RAMA** sobre la funcion real -- forzar el
catch de `Get-Process`, el catch de `StartTime`, y un caso de PID **vivo** con hora de arranque
distinta -- de modo que M1, M2 y M3 enrojezcan.

Nota del checker que hago mia: su primer intento de mutante, sin codigo muerto, enrojecio por
`count == 3`, o sea **por forma**. El contrato que corona esta entrega tiene dentro el patron de
TASK-0341.

## B2 -- el contrato TASK-0284, y va AQUI

El checker me pregunto si particionarlo. **No: se queda en 0331.** Su propia posicion es que es de
0331 por propiedad y que solo su FORMA correcta pertenece a la generalizacion. Comparto, y anado el
motivo operativo: hoy ese contrato deja `falsification-runners` rojo **e inerte** -- `assert
contract(text)` revienta ANTES de evaluar sus dos mutantes, asi que la propiedad no se comprueba en
absoluto. Dejarlo esperando a que madure una generalizacion mantiene un job de CI rojo sin
comprobar nada.

**Correccion mia, que te debo:** te dije que lo rompio la remediacion 4. **Es falso.** `git log -S`
del checker da `4c4e2665` (remediacion 3) y el commit padre `a4a400e8` **ya falla** con la misma
asercion. Sigue siendo de 0331, pero `e9719613` no lo introdujo y revertirla no lo limpia. Lo
escribo porque te lo afirme mal en el aviso anterior.

**El orden que el contrato protege SE MANTIENE**: la sonda de residuo en offset 62938 y la escritura
del lock en 79099. Solo cambio el nombre del helper, y el reemplazo es **mejor** -- renombrado
atomico, y es la identidad PID+start de la que depende toda la tabla.

**Lo que pido:** que el contrato ate **el efecto** -- que la primera escritura resuelta de
`$LockPath` en el camino de exec ocurra despues de la sonda -- y no el nombre del helper. Y que lo
falses **moviendo la escritura por encima de la sonda**, no borrando una linea.

## B3 -- amplia el verification_cmd

**Seis ficheros leen el harness; tu `verification_cmd` nombra dos.** Cuatro lectores que CI ejecuta
sobre el fichero que esta tarea reescribe estan **fuera de su puerta de aceptacion**. Por eso pudiste
declarar verde con esto roto.

Anade al `verification_cmd` de 0331, y usalos para cerrar:

    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
    python scripts/test_scan_domain_neutrality.py
    powershell scripts/scan_domain_neutrality.ps1 -Root .

## Contexto de CI

CI esta rojo tambien por `validate`, que **no es tuyo aqui**: dependencia ausente desde el 2026-08-02,
contratada como TASK-0340. Si tras arreglar B1 y B2 CI sigue rojo por ese job, es lo esperado.

requested_action: Reclamar TASK-0331, sustituir el tripwire de conteo por muertes por RAMA sobre la
Get-LeaseProcessState real de modo que M1, M2 y M3 enrojezcan, reparar el contrato TASK-0284 para que
ate la escritura resuelta del lock y no el nombre del helper falsandolo por movimiento, ampliar el
verification_cmd con los tres lectores de CI que hoy quedan fuera, y devolver a in_review liberando
el claim en el mismo paso.
