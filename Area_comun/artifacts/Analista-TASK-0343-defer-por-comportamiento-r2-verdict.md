# Veredicto TASK-0343 r2 -- el contrato dejo de mirar el nombre y dejo de mirar

reviewer: Analista
task_id: TASK-0343
verdict: CHANGE-REQUIRED
iteracion: 2 de 2 -- presupuesto agotado, recomiendo escalar al operador humano
fecha: 2026-08-09 (hora local del sistema, UTC+2)

## Ancla canonica

    commit bajo revision      4cded4c4  fix(TASK-0343): bind rollback checks to behavior
    commit de la r1           26b33967  fix(TASK-0343): assert rollback ledger preservation
    HEAD canonico             2415b55d  (origin/main al abrir la revision)
    instruccion               MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0343-r2
    veredicto previo          Area_comun/artifacts/Analista-TASK-0343-asercion-rollback-contadores-verdict.md

Alcance respetado: SOLO el hub, sin producto. Todas las mutaciones se aplican sobre PRODUCCION
(`scripts/harness/peer_mailbox_cron.ps1` y el helper `ledger_preservation_holds` de
`examples/mailbox_retry_cases/run_mailbox_retry_cases.py`), nunca sobre los mutantes que el propio
runner se escribe.

## Reproduccion

Tres clones limpios en `D:/Aegis_Scratch/multi_agent_project_protocol/an0343r2{,b,c}/hub`, los tres en
detached `4cded4c4` con `git status --short` vacio. Gate por exit code, nunca por texto:

    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py   -> 0   (1m53s)
    python scripts/check_falsification_contracts.py --root .         -> 0
    python scripts/validate_collaboration_state.py --root .          -> 0
    python scripts/scan_encoding.py --root .                         -> 0
    python scripts/scan_domain_neutrality.py --root .                -> 0
    protocol_state_drift(Path("."))["has_drift"]                     -> False

CI real (`gh api .../actions/runs/<id>/jobs`), leido por PASO, no por job:

    31310469089  4cded4c4  falsification-runners  success
                           STEP "Execute mailbox retry falsification runner"  success
                 4cded4c4  validate               failure
                           STEP "Run runtime concurrency simulation cases"  failure  (ajeno a 0343,
                           el mismo paso que ya declare en la r1)

AC5 vuelve a estar cubierto: el paso que abrio la tarea sale success en Actions sobre el commit exacto.

## Vector por vector

Cada linea es el runner COMPLETO en clon limpio. Donde hay varias corridas es porque el resultado no
es estable, y esa inestabilidad es parte del hallazgo.

| # | Vector (mutacion sobre PRODUCCION) | Direccion pedida | Medido | Veredicto |
|---|------------------------------------|------------------|--------|-----------|
| mp4 | borrar `and after_claims == before_claims` de `ledger_preservation_holds` | 0 -> 1 | exit **1**, linea 199, `('claims_changed', True, False)` | **PASA** |
| mp5 | borrar `bool(before_events) and` | 0 -> 1 | exit **1**, linea 199, `('empty_prestate', True, False)` | **PASA** |
| mp6 | renombrar `reason=ledger_unreadable_after_exec` -> `reason=ledger_head_unreadable_after_exec` (misma rama, mismo `return`, mismo efecto) | 1 -> 0 | 4 corridas: **1, 0, 0, 1** | **SLIP** |
| mp8 | `Set-Content Area_comun/state/CLAIMS.json '{"seq":0,"claims":[]}'` justo antes de `ROLLBACK_LEDGER_PRESERVED` | sigue en 1 | exit **1**, linea 1719, la asercion de la propiedad | **PASA** (no regresion) |
| mp13 | quitar el defer conservador (sin `return`) dejando una linea que el predicado SI acepta | sigue en 1 | exit **1**, linea 1747, `ROLLBACK_LEDGER_DRIFT` | **PASA** por cascada |
| mp9 | borrar SOLO el `Write-Log` del defer guardado, conservando el `return` (el efecto sigue intacto) | deberia ser 1 | 4 corridas: **0, 0, 1, 0** | **NUEVO ESCAPE** |
| mp11 | renombrar la razon a `x` | -- | exit **0** | coherente con mp9 |
| mp14 | renombrar la razon a `ledger-unreadable-after-exec` (guiones: el regex NO puede casarla) | -- | 3 corridas: **1, 0, 0** | **NUEVO ESCAPE** |
| base | ninguna | 0 | 4 corridas: **0, 0, 0, 0** | PASA |

Control cruzado sobre el commit anterior, misma mutacion, mismo clon:

    mp9 sobre 26b33967 (pre-remediacion)   2 de 2 corridas exit 1, deterministas,
                                           "AssertionError: seen state missing"

## Lo que la remediacion si consigue

**mp4 y mp5 mueren, y mueren bien.** El negativo permanente paso de dos casos con claims identicos a
cuatro (`events_lost`, `claims_changed`, `empty_prestate`, `preserved`) y de dos mutantes a tres. Las
dos mitades de la propiedad que en la r1 sobrevivian -- la comparacion de claims y la guarda de
no-vacuidad -- ahora estan cubiertas, y lo estan de forma DETERMINISTA: ambos fallan dentro de
`run_rollback_ledger_preservation_property`, que es aritmetica pura sobre diccionarios sinteticos y no
depende de ninguna carrera. Esa parte del encargo esta cumplida.

**mp8 sigue muriendo por la asercion instalada**, no por cascada: la destruccion real de `CLAIMS.json`
en la rama que declara preservacion cae en la linea 1719 con el diagnostico exacto de before/after. No
hay regresion (foco B, PASA).

**mp13 tambien muere**: eliminar el defer conservador de verdad -- dejando la rama sin `return`, de modo
que el rollback continua -- pone rojo el runner. La muerte es por `ROLLBACK_LEDGER_DRIFT`, es decir por
cascada y no por el guardian nuevo, pero el criterio "una mutacion que elimine el defer conservador debe
seguir poniendolo rojo" se cumple.

**El foco A esta atendido en la forma pedida.** El `or` de dos razones de la vieja linea 1712 y la barrera
de reparacion con `-SimpleMatch` de una sola razon estan sustituidos por un criterio de pertenencia. El
barrido AST propio, con el mismo predicado en los tres commits, mide la tendencia correcta:

    071b5a1a (pre-arreglo)  23 aserciones atadas a subcadenas literales del log
    26b33967 (r1)           22
    4cded4c4 (r2)           21

**El foco C esta limpio.** mp1 no se toca aqui: `run_rollback_ledger_preservation_property()` sigue
invocada desde `main()` (linea 1631), `scripts/check_falsification_contracts.py` no aparece en el diff de
`4cded4c4`, y TASK-0341 (proposed, owner Codex) lleva la clase de la frontera muerta. Nada en este commit
cambia el estado de mp1.

Y la frase del DIAG que en la r1 no sostenia su evidencia esta corregida: ahora declara que el barrido
no cubria literales ejecutables fuera de aserciones y nombra el `csc.exe` como residual R5 explicito.

## F-0343-04 -- el criterio nuevo se satisface con una linea de otro intento, tres intentos antes

Esta es la razon del CHANGE-REQUIRED y responde tu pregunta.

Volque el log completo del escenario desde un clon instrumentado (`an0343r2c`, la corrida entera sale
exit 0). El escenario emite **dos** `ROLLBACK_DEFER`, y no en el mismo intento:

    17:51:11  ROLLBACK_DEFER reason=head_changed                 <- intento 1
    17:51:13  ROLLBACK_QUARANTINED path=residue.txt              <- intento 2
    17:51:15  ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=3 <- intento 3
    17:51:17  EVIDENCE_UNAVAILABLE reason=ledger_not_pure_append <- intento 4, el escenario bajo prueba
    17:51:17  ROLLBACK_DEFER reason=ledger_unreadable_after_exec <- intento 4, la linea guardada

`conservative_rollback_defer_observed(log)` recorre el log ENTERO. La linea del intento 1 lo satisface
para siempre. La consecuencia es que la asercion de la linea 1743 **no puede fallar nunca por lo que
ocurra en el intento 4**, que es exactamente el unico intento que la tarea investiga.

Falsacion, no opinion, en dos direcciones independientes:

1. **mp9.** Borro en produccion unicamente el `Write-Log` del defer guardado y conservo el `return`: el
   efecto conservador sigue ahi, pero la linea que la asercion fue reescrita para observar desaparece.
   El runner sale **0 en 3 de 4 corridas**. Sobre `26b33967`, la misma mutacion salia **1 en 2 de 2**,
   determinista. La remediacion no cambio un literal estrecho por una propiedad: cambio un rojo
   determinista por un verde.
2. **mp14.** Renombro la razon a `ledger-unreadable-after-exec`. El regex es
   `ROLLBACK_DEFER reason=[A-Za-z0-9_]+(?:\s|$)`, asi que ante `reason=ledger-unreadable-...` casa
   `ledger` y despues exige espacio o fin de linea, encuentra un guion y **no casa**. El predicado no
   reconoce la razon renombrada en absoluto, y aun asi el runner sale **0 en 2 de 3 corridas**. Lo que
   lo aprueba no es la razon renombrada: es `head_changed`.

Nota de clase: el predicado sigue atado a una FORMA, solo que a una mas ancha. Antes eran dos nombres
literales; ahora es "un nombre de razon compuesto exclusivamente por `[A-Za-z0-9_]`, seguido de espacio o
fin de linea". Un renombrado legitimo con guion, punto o dos puntos lo vuelve a romper. Es la misma
familia que ya adjudicamos en TASK-0328: la exencion validaba un juego de caracteres en vez de la cosa.

## F-0343-05 -- la barrera de reparacion dejo de ser una barrera

El mismo ensanchado se aplico al `Select-String` del fixture (linea 1609), y ahi hace mas dano porque no
es una asercion sino un PRIMITIVO DE SINCRONIZACION. El script de reparacion se lanza en el intento 4
(`$count -eq 4`, 17:51:16). Para entonces `ROLLBACK_DEFER reason=head_changed` lleva **cinco segundos** en
el log. El nuevo `-Pattern 'ROLLBACK_DEFER reason=[A-Za-z0-9_]+' -Quiet` casa en el PRIMER sondeo, antes
de que el rollback del intento 4 haya observado nada. La barrera ya no espera: dispara de inmediato y la
restauracion de `events.jsonl` pasa a competir con el rollback en vez de secuenciarse detras de el.

Eso es lo que hace inestables a mp6, mp9 y mp14: la misma mutacion sobre el mismo commit sale 1 o 0 segun
como caiga la carrera. Es medible en la tabla -- mp6 da 1, 0, 0, 1 -- y no es un artefacto de mi entorno:
el baseline sale 0 en 4 de 4, o sea que el runner sin mutar es estable hoy y lo que se volvio no
determinista es la RESPUESTA DEL GATE A UNA MUTACION. Un gate que responde a la misma mutacion con
resultados distintos no es un gate; y el mecanismo que lo produce (una barrera que ya no bloquea)
tambien puede poner en falso verde al escenario sin mutar cuando la maquina de CI vaya mas cargada que
la mia.

## Respuesta literal a tu pregunta

    mp6  debe pasar de exit 1 a exit 0   ->  NO: 4 corridas dan 1, 0, 0, 1
    mp4  debe pasar de exit 0 a exit 1   ->  SI, determinista
    mp5  debe pasar de exit 0 a exit 1   ->  SI, determinista

"mp6 deja de dar rojo falso, o el contrato sigue mirando el nombre en vez del efecto?" Ninguna de las
dos. El contrato dejo de mirar el nombre, pero no paso a mirar el efecto: paso a mirar el log entero, y
en el log entero siempre hay un `ROLLBACK_DEFER` de otro intento. Y mp6 sigue dando rojo la mitad de las
veces, no porque el contrato lea el nombre, sino porque la barrera que se ensancho a la vez volvio racy
al fixture.

## Residuales declarados (no bloquean)

- **R1 (de la r1, vivo).** mp2: la asercion de `main()` sigue siendo borrable con todos los gates verdes.
  Clase de TASK-0341.
- **R2.** La `mutation` declarada del contrato sigue siendo una linea del propio mutante del runner
  (`'"claims_ignored": lambda before, after, before_claims, after_claims:'`), no de produccion. El
  certificador comprueba que el texto EXISTE, no que mate nada. Clase de TASK-0341.
- **R3.** Queda una asercion atada a una razon literal en el fichero, fuera del camino tocado: linea 351,
  `assert "ROLLBACK_DEFER reason=ledger_torn_tail" in output` dentro de `run_torn_tail_case`.
- **R4.** El negativo declara `("reason_with_context", "... reason=quarantine_move_failed ...", True)`, es
  decir consagra como "defer conservador" una razon que en produccion (linea 1240) se emite en un `catch`
  DENTRO del bucle y **sin `return`**: ahi el rollback continua. El predicado acepta como prueba de defer
  una linea que por control de flujo no lo es.
- **R5.** `scope_routes` de la tarea nombra `Area_comun/protocol/FALSIFICATION_CONTRACTS.json`, que no
  existe en el arbol; los contratos viven inline en cada runner.
- **R6 (de la r1, vivo).** El literal `csc.exe` de la linea 535, ya declarado en el DIAG.

## Recomendacion de cierre

**CHANGE-REQUIRED.**

Lo que hay que cambiar, en este orden y sin ensanchar nada mas:

1. **Acotar la ventana, no el vocabulario.** La asercion debe mirar el tramo del log que corresponde al
   intento bajo prueba (el ultimo `EXEC_START`/`EXEC_EXIT`, o el tramo posterior a
   `EVIDENCE_UNAVAILABLE`), no el log completo. Criterio de aceptacion POR COMPORTAMIENTO: **mp9 debe
   volver a exit 1 en 3 de 3 corridas** y **mp14 debe salir exit 0 en 3 de 3**. Si solo se toca el regex,
   no se ha arreglado nada.
2. **Devolver la barrera a su trabajo.** El `Select-String` del fixture tiene que volver a bloquear hasta
   el punto de sincronizacion real del intento 4. Criterio: **mp6 exit 0 en 3 de 3 corridas** y el
   baseline **exit 0 en 3 de 3**. Un unico resultado verde no cuenta: esta clase de defecto se esconde
   detras de una sola corrida afortunada.
3. **Retirar el caso `quarantine_move_failed` del negativo** o justificar por escrito por que una rama que
   no hace `return` cuenta como defer conservador (R4).

Gates afectados: `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`,
`scripts/harness/peer_mailbox_cron.ps1`, `scripts/check_falsification_contracts.py`, y el paso `Execute
mailbox retry falsification runner` en Actions, con **run REAL citado**.

**Presupuesto agotado.** Declare maximo 2 iteraciones en el veredicto r1 y esta es la segunda. La decision
de gastar una tercera no me corresponde: recomiendo **escalar al operador humano** con las dos opciones
sobre la mesa -- (a) remediacion 3 acotando la ventana y restaurando la barrera, o (b) cerrar 0343 por sus
AC medibles (AC1, AC2, AC4, AC5, AC6 estan cumplidos; mp4 y mp5 mueren) y particionar F-0343-04 y F-0343-05
a una tarea nueva, porque son un defecto del FIXTURE de reintentos (ventana de observacion y barrera de
sincronizacion) y no de la asercion de contadores que abrio esta tarea.

Si se elige (b), la tarea nueva no puede heredar el encuadre de esta: su criterio no es "que el gate
reconozca cualquier razon", sino "que el gate observe la ventana del intento que dice observar".

-- Analista
