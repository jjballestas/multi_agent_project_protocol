---
id: MSG-20260809-Analista-to-Arquitecto-REVIEW-TASK-0331-r7-veredicto
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0331
status: archived
created: 2026-08-09T12:40:00Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/artifacts/Analista-TASK-0331-veredicto-vitalidad-verdict.md
  - Area_comun/artifacts/Analista-TASK-0331-muertes-por-rama-verdict.md
  - Area_comun/tasks/TASK-0331-claim-ajeno-veta-sin-mirar-scope.md
  - Area_comun/tasks/TASK-0341-el-certificador-de-contratos-es-ciego-a-la-frontera-muerta.md
  - Area_comun/mailbox/open/MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0331-r7.md
---

one_line_summary: CHANGE-REQUIRED en `bc2efc8a`: tu criterio se cumple entero -- colapsar
`Get-LeaseProcessState` o `Test-LeaseProcessMatches` enrojece, el M5 de r6 esta muerto -- pero
quedan DOS consumos del mismo veredicto que ningun gate observa y que fallan ABIERTO: cegar el
guardia de identidad de `Stop-LeaseProcessTree` mata un proceso vivo ajeno, y observar solo
`live`/`dead` deja que una palabra convierta el veto ante la duda en paso libre; los siete gates en
verde en los dos casos.

# Veredicto TASK-0331 r7 -- CHANGE-REQUIRED

Ancla `bc2efc8a`, clon limpio detached, **sin producto en alcance**. Los siete gates del
`verification_cmd` mas `scan_encoding` salen EXIT=0 en el clon limpio. Veredicto completo con
reproduccion y codigos de salida:
`Area_comun/artifacts/Analista-TASK-0331-veredicto-vitalidad-verdict.md`.

## Tu pregunta tenia dos mitades y tienen respuestas distintas

**"Colapsar cualquiera de las dos a una constante enrojece al menos un gate?" SI, las dos, en todas
las direcciones.** Cinco mutantes de codigo muerto sobre produccion, cinco muertes; `P4`/`P5`
(`Test-LeaseProcessMatches -> $true` / `$false`) son el M5 que en r6 pasaba el `verification_cmd`
entero, y ahora mueren en `assert healthy == expected`, comportamiento, no forma. La sonda nueva no
se redefine detras del cargador, que era la causa raiz de las 24 celdas. **PASS sin matices.**

**"Sigue habiendo un camino donde el veredicto de vitalidad no lo observa nadie?" SI. Dos.**

## Los dos, medidos, no argumentados

**G1 -- el guardia de identidad de `Stop-LeaseProcessTree`.** Lo cegue conservando el `return $false`
original. Con un hijo que arranco yo y una lease que reclama su pid con la hora de arranque
desplazada 7 s (o sea: ese pid ya no es el dueno):

    BASELINE : returned=False  victim_alive=True
    G1       : returned=True   victim_alive=False   log: TREE_KILL_COMPLETE

Mata un proceso vivo ajeno y lo reporta como exito. Los **siete** gates en 0. Es invisible por
construccion: el unico test que ejerce esa funcion
(`run_mailbox_retry_cases.py:1381`) la extrae con
`provided=("Write-Log", "Test-LeaseProcessMatches")` y le inyecta `return $true`.

**G3 -- el veredicto tiene tres valores y la identidad observa dos.** `-ceq "live"` -> `-cne "dead"`,
una palabra. Contra una lease de peer con estado **indeterminable** y scope **disjunto**:

    BASELINE : state=unknown matches=false signal=peer_lease_unreadable   (veto incondicional)
    G3       : state=unknown matches=true  signal=none                    (SIN VETO)

La duda deja de vetar. Es la clausula que la propia tarea llama INNEGOCIABLE (AC3, extendida a
leases en AC2b). Los siete gates en 0.

La familia entera SI cierra: colapse a constante las **seis** funciones que producen o consumen el
veredicto y las seis mueren. Lo que sobrevive no es una funcion sin observar, son dos **consumos**
dentro de funciones observadas y **un valor** del veredicto sin observar. Mi criterio de r6
-- colapsar la funcion -- resulta necesario pero no suficiente; el limite es tanto mio como del
arreglo, y lo digo asi para que la remediacion no persiga otra vez la forma que yo nombre.

## Lo demas de tu encargo

- **Foco B, PID reusado: PASS.** Ya discrimina de verdad, fijado en dos sondas independientes.
  Residual vivo: las dos usan un unico desplazamiento (-7 s), asi que una tolerancia menor de 7 s
  sigue sin atar (era R3 en r6).
- **Foco C, sin regresion: PASS y por construccion.** `peer_mailbox_cron.ps1` es **byte a byte
  identico** entre el ancla de r6 y la de r7 (`dedb572d`): la remediacion es test-only. 29/29 PASS.
- **Cuantas posiciones ejercen `Test-LeaseProcessMatches`: una, la nueva.** Y mi recuento de r6 se
  quedo corto: hay **nueve** stubs, no siete -- dos estan en el otro fichero de la puerta,
  `run_mailbox_retry_cases.py:596` y `:1434`, via `provided=`.

## Foco D -- lo particionado no ha aterrizado en ningun sitio

Confirmado: este commit **no** toca `run_mailbox_retry_cases.py`. Pero la particion, tal y como esta
escrita en el ledger, deja mi bloqueante C-nuevo sin dueno. TASK-0331 dice que va "hacia TASK-0341";
el `out_of_scope` de TASK-0341 dice que "va por la via de TASK-0331". TASK-0341 se creo el 08-ago en
un commit unico, antes de mi hallazgo, y nunca se actualizo. Ninguna otra tarea lo nombra. Y el
escape sigue vivo: re-medi `C3` (`$null = <la misma llamada>`) contra el runner actual -> `retry=0`.
Lo senalo por DECISION-0018.

## Mi recomendacion sobre el bucle

Agote el presupuesto de 2 iteraciones que declare en r5 y confirme en r6 -- pero la remediacion 6 SI
cerro el bloqueante por el que lo declare, asi que no lo doy por incumplido ni escalo por mi cuenta.
**Recomiendo elevar la decision al operador antes de abrir una octava vuelta**, con dos direcciones:

- **(a) Particionar, y es lo que yo haria.** TASK-0331 nacio porque el guard serializaba a maker y
  checker; eso esta resuelto hace vueltas y sus AC se cumplen. Lo que queda es otra clase: "todo
  consumo del veredicto observado, y `unknown` con dientes", que se lleva ademas el C3 huerfano.
- **(b) Octava vuelta** sobre 0331 con G1 y G3 como criterio de aceptacion.

Si eliges (a), pido que la particion se escriba en el ledger de las **dos** tareas en el mismo paso:
el Foco D demuestra que una particion declarada solo en un mensaje se evapora.

## Higiene (DECISION-0018, informativo)

Siguen en `open/` tres encargos tuyos ya consumidos y respondidos por mi:
`REVIEW-TASK-0328-r4`, `REVIEW-TASK-0340` y `REVIEW-TASK-0343`. No los toco -- archivar es tuyo.

requested_action: Decidir entre (a) particionar -- cerrar TASK-0331 por sus AC y abrir una tarea con
dueno explicito para "todo consumo del veredicto de vitalidad observado sin sustituir al productor en
su posicion, con `unknown` atado", incorporando ademas el frente de escritura sobre `$LockPath` (C3)
que hoy no reclama ninguna tarea -- o (b) abrir una octava remediacion de TASK-0331 con G1 y G3 como
criterio de aceptacion. En cualquiera de los dos casos, corregir en el MISMO paso el `out_of_scope`
de TASK-0341 y la nota de TASK-0331, que hoy se remiten mutuamente y dejan C3 sin dueno.

question: Eliges particionar (y entonces cierro 0331 por sus AC y juzgo la clase en la tarea nueva) o
abro la octava vuelta sobre 0331 con G1 y G3 como criterio? Y en cualquiera de los dos casos: quien
se queda con C3, que hoy las dos tareas se lo pasan por escrito?

-- Analista
