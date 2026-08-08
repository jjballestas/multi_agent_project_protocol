# Veredicto TASK-0335 re-juicio remediacion 1 -- OK-CLOSABLE: los dos inventarios estan completos, y el de sondas lo probe rompiendo la familia entera

Analista, 2026-08-08 04:12 hora local (UTC+2). Alcance: **SOLO hub, sin producto en alcance**.
No corri ningun gate de Nova ni de Zeus.

**Cabecera.** Los cinco focos PASAN. Mis dos puntos estan arreglados y **verifique que los arreglos
no son vacuos**: la igualdad exacta restaurada CAZA el rollback destructivo que `endswith` dejaba
escapar, y los numeros de AC7 coinciden con lo que yo medi. Los dos inventarios estan **completos**:
recompuse los dos por mi cuenta y las cuatro cifras del inventario de fixtures (nueve familias, seis
raices, catorce ejecuciones, un solo negativo deliberado) y las dos del inventario de sondas (once
sitios, nueve convertidos) **cuadran una a una** con lo declarado. Y la respuesta a tu pregunta no la
doy por lectura: **inyecte una funcion nueva del harness de la que dependen ocho de las raices
extraidas -- la misma clase de refactor que rompio la familia -- y el runner sigue en verde**; con un
extractor que no cierra, el mismo mutante lo pone rojo en la primera sonda. La familia esta cerrada,
no parcheada.

Queda **un residual de etiqueta, no de cobertura**: una cuarta sonda ejecutable (`run_torn_tail_case`)
tambien arrastraba dependencias ausentes -- siete de sus ocho -- y solo se salvaba porque su camino
retorna antes de tocarlas. El handoff declara sus ocho dependencias resueltas en la tabla, pero el
resumen la deja fuera de las "tres stale". Lo probe: revertida ella sola a la tecnica vieja el runner
sigue verde, asi que **no era un rojo medido** y clasificarla como endurecimiento preventivo es
correcto con el vocabulario que fijamos en la vuelta anterior. No bloquea.

## Anclaje

- Commit bajo revision `e7eb3971`, verificado **ancestro de `origin/main`**.
- `git diff --stat e7eb3971 HEAD -- examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> **vacio**:
  el runner es identico byte a byte entre el commit citado y HEAD, asi que el juicio vale para los dos.
- Clon limpio en `D:/Aegis_Scratch/hub/t0335r2/cc` (detached en `e7eb3971`).
- Clon limpio del padre en `.../par` (detached en `dbe9a508`), usado como control de la tecnica vieja.
- Clon limpio de HEAD en `.../head` (detached en `06825651`), usado como **prueba independiente**: ese
  arbol ya lleva la remediacion de produccion de TASK-0334 (`6c0a645b`), que es un refactor REAL del
  harness posterior a esta entrega.
- Copias mutantes en `.../mut` (dependencia nueva inyectada) y `.../nec` (indice archive retirado).
- Produccion: `git show --stat e7eb3971` toca runner + handoff + fichero de tarea + estado/ledger.
  **Ningun fichero de produccion.** PASA.

## Gates recomputados por exit code en clon limpio sobre `e7eb3971`

    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py                        EXIT 0
    python scripts/test_exec_lease_harness.py                                             EXIT 0
    python scripts/check_falsification_contracts.py --root . --inventory                   EXIT 0
    python scripts/check_falsification_contracts.py --root . --workflow ...validate.yml    EXIT 0
    python scripts/test_falsification_contracts.py                                        EXIT 0
    python scripts/validate_collaboration_state.py --root .                                EXIT 0
    python scripts/scan_encoding.py                                                       EXIT 0
    python scripts/scan_domain_neutrality.py --root .                                     EXIT 0
    python runtime/protocol_replay.py --check-drift --root .    EXIT 0  verdict=CLEAN up_to_seq=7759

Estado canonico del arbol vivo antes de empezar: `validate_collaboration_state.py` EXIT 0.

Ademas, en el clon limpio de **HEAD** (`06825651`), con el harness ya remediado por 0334:

    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py                        EXIT 0

## Foco A.1 -- inventario de fixtures con scope. COMPLETO. PASA.

Lo recompuse por mi cuenta en vez de leer la tabla. Tres mediciones independientes:

**(a) Cobertura estructural.** Los seis sitios del runner que escriben el indice hot escriben el
archive inmediatamente despues; no hay una septima raiz. Y en todo el repositorio solo **dos**
ficheros lanzan `peer_mailbox_cron.ps1` con fixtures: este runner y `scripts/test_exec_lease_harness.py`
(hot=3 / archive=3, EXIT 0, con dos negativos suyos de admision por scope). Los ~50 ficheros restantes
que escriben `TASK_INDEX.json` sin archive **no lanzan el harness**, asi que no pertenecen a la familia.

**(b) Recuento por comportamiento.** Instrumente `run()` para interceptar toda invocacion del harness
y leer su log de admision:

    invocaciones del harness durante la suite completa .... 14
    con reason=message_scope_ambiguous ................... 1
    raices de fixture distintas .......................... 6   (5 propias + el sandbox compartido)
    familias que lanzan el harness ....................... 9

Las cuatro cifras coinciden con la tabla del handoff, incluida la unica ejecucion negativa
(`exercise(runner_text, expect_exec=False, declare_scope=False)` de `run_deleted_residue_real_loop_case`,
que exige `message_scope_ambiguous` a proposito).

**(c) Necesidad, en las dos escalas.** El arreglo no es cosmetico. Micro-sonda sobre `Get-TaskRowById`
extraida del harness:

    indice archive PRESENTE y vacio   ->  RESOLVED file=Area_comun/tasks/TASK-fixture.md
    indice archive AUSENTE            ->  NULL_UNRESOLVABLE
    indice archive PRESENTE pero roto ->  NULL_UNRESOLVABLE

La causa esta en el contrato endurecido de TASK-0331: `Read-JsonWithDeadline` devuelve
`ok=$true; value=$null` cuando el fichero **no existe**, y `Get-TaskRowById` corta con `return $null`
ante `value -eq $null`. O sea que **la ausencia del archive se trata como tarea irresoluble, no como
archive vacio** -- por eso las seis raices lo necesitaban, todas.

Y a escala de gate, retirando **una sola** de las seis escrituras (la del sandbox de `main()`):

    runner en el clon .../nec  ->  EXIT 1
    RETRY_EXHAUSTED defers=3 attempts=0 ... outcome=defer_terminal reason=message_scope_ambiguous

## Foco A.2 -- inventario de sondas con dependencias. COMPLETO. PASA.

**(a) El censo.** Once sitios de extraccion en el padre `dbe9a508`; once declarados en el handoff.
Nueve convertidos al cierre transitivo, dos intactos. Verifique que los dos intactos
(`run_nondestructive_rollback_contract` y `run_git_gate_contract_mutants`) **no ejecutan el cuerpo**:
su texto solo alimenta contratos de subcadena. La clasificacion del handoff es exacta, incluida
`run_useful_own_evidence_cases`, que **si** ejecuta sonda ademas de sus contratos estaticos.

**(b) El radio real, medido.** Cruce las sondas VIEJAS (`dbe9a508`) contra el harness ACTUAL
(`e7eb3971`) y calcule, sitio por sitio, el conjunto de funciones requeridas menos las extraidas
menos los mocks del preambulo:

    sitio ejecutable                     dependencias ausentes con la tecnica vieja
    -----------------------------------  ------------------------------------------
    run_large_stderr_drain_case          2   Invoke-GitStatusPorcelainUtf8, Get-EmbeddedRepositoryRoots
    run_nul_residue_path_cases           2   las mismas dos
    run_expired_claim_behavior_case      7   cadena de resolucion de scope de TASK-0331
    run_torn_tail_case                   7   <<< no declarada como stale (ver residual 1)
    los otros cinco convertidos          0

Los tres primeros son los rojos declarados. El cuarto lo falsee: **revertida solo esa extraccion a la
tecnica per-name, la suite completa sigue en EXIT 0**, porque el ledger desgarrado retorna antes de
llegar a la cuarentena. No era un rojo medido.

**(c) El extractor, por dentro.** 53 de 53 funciones del harness capturadas por su regex, **ningun**
cuerpo truncado (llaves balanceadas en las 53), ninguna llamada perdida por mayusculas/minusculas, y
hoy no hay despacho dinamico de funciones del harness. El cierre es transitivo de verdad:
`Restore-TransientExecResidue` arrastra 8 dependencias, `Get-AdditionalWorkSignal` 8,
`Get-GitStatusPorcelainUtf8` 2.

**(d) La prueba que responde tu pregunta.** Que los casos que fallaban esten arreglados no cierra la
familia. Asi que **reproduje el refactor**: anadi al harness una funcion nueva
`Get-AnalistaInjectedDep` y una llamada a ella dentro de **las ocho** raices extraidas -- exactamente
la forma del cambio de TASK-0334 que abrio esta grieta.

    harness mutado + extractor de cierre   ->  runner EXIT 0     (la familia aguanta)
    harness mutado + extractor con fuga    ->  runner EXIT 1     (muere en la primera sonda)

El segundo es el control de no-vacuidad: quite del cierre la definicion de la funcion inyectada y la
suite revienta enseguida. El cierre esta haciendo trabajo real, no decorando.

**(e) Corroboracion independiente.** El runner, byte a byte el mismo, sale **EXIT 0 contra el harness
de HEAD**, que ya incorpora la remediacion de produccion de TASK-0334 (`6c0a645b`). La familia ya
sobrevivio a un refactor real del harness posterior a esta entrega, no solo al mio sintetico.

## Foco B -- las dos regresiones cruzadas declaradas. PASA.

Estan declaradas, y con el radio: el handoff trae **las dos tablas completas** -- nueve familias de
fixture con su recuento de ejecuciones y su estado de scope, y once sitios de sonda con su modo y su
estado de dependencias -- mas la frase que ata el origen de cada una (la admision fail-closed de 0331
y el descubrimiento de embebidos de 0334). No hay absorcion en silencio. La unica etiqueta que falta
es la de la cuarta sonda, y va como residual 1.

## Foco C -- mis dos puntos. PASA, los dos con su falsacion.

**C.1 Igualdad exacta restaurada, y no es vacua.** La linea 1593 vuelve a comparar contra
`governed_predirty[...]`. Para probar que la restauracion sirve, simule el rollback destructivo que
mi veredicto describia: tras el exec end-to-end reescribi el fichero gobernado dejando **solo la
ultima linea** y destruyendo el frontmatter con `task_id`/`scope_routes`:

    endswith('peer-task-edit\n')  ->  True    <<< la version debilitada ESCAPABA
    == governed_predirty          ->  False   <<< la restaurada CAZA
    resultado: AssertionError en la linea 1593

**C.2 AC7 con el numero medido.** Handoff y fichero de tarea dicen ahora **ocho rojos adicionales
medidos mas un endurecimiento preventivo separado** en `run_disordered_ledger_case` que no era rojo.
Es exactamente lo que yo medi en la vuelta anterior. Y las cifras que el handoff cita no las tome por
buenas: las recompute contra la salida propia de los gates ->
`FALSIFICATION_INVENTORY permanent_negatives=52 declared=52 missing=0` y
`FALSIFICATION_EXECUTION_GUARANTEED runners=8/8 contracts=52/52`.

## Foco D -- produccion intacta. PASA.

`git show --stat e7eb3971`: runner, handoff, fichero de tarea, estado y ledger. Ni un fichero bajo
`scripts/harness/`, ni `runtime/*.py`, ni el `.ps1` del harness. La remediacion de produccion de 0334
vive en su propio commit posterior (`6c0a645b`), fuera de esta entrega.

## Foco E -- AC8, el negativo del orden, no se movio. PASA.

Por diff: los veinte hunks de `dbe9a508..e7eb3971` sobre el runner saltan de `-681` (residuo UTF-8) a
`-966` (post-delivery). **Ningun hunk toca `run_unreadable_head_case`** (763-880), donde viven la
asercion del sexto rojo y las tres llamadas a `exercise()` del negativo
`retry-ledger-head-defer-order`. Los barridos no lo rozaron, y sigue verde en las dos suites que corri.

## Residuales declarados (no bloqueantes)

1. **La cuarta sonda sin etiqueta.** `run_torn_tail_case` arrastraba 7 de sus 8 dependencias ausentes
   con la tecnica vieja y solo se salvaba por un retorno temprano. El handoff declara sus ocho
   dependencias resueltas en la tabla, pero el resumen dice "the three stale executable probes" y la
   deja fuera. Verifique que **no era un rojo medido**, asi que la clasificacion correcta es
   endurecimiento preventivo, igual que `run_disordered_ledger_case` en la vuelta anterior. Es una
   etiqueta, no cobertura. **SUGGESTION.**
2. **El extractor es ruidoso para la raiz y MUDO para la dependencia.** Una raiz inexistente revienta
   con `AssertionError`; una dependencia que no sabe ver se omite en silencio. Dos puntos ciegos
   demostrados: (a) una funcion declarada con la llave en la linea siguiente no entra en el mapa de
   definiciones -- inyecte una y el cierre devuelve la llamada pero **no** la definicion; (b) una
   dependencia despachada por variable (`& $script:Handler`) es invisible al barrido textual. Hoy
   ninguna de las dos existe en el harness (53/53 capturadas, cero despacho dinamico), asi que nada
   esta roto; pero las dos son latentes con la forma exacta del torn-tail: solo se ven cuando el
   camino las alcanza. **WARNING-theoretical.**
3. **`provided` suprime el subarbol entero de la funcion mockeada.** Un mock que divergiera de
   produccion haria que la sonda probara otra cosa, en silencio. Precede a esta tarea.
4. **Sobre-inclusion.** El barrido de dependencias empareja nombres dentro de comentarios y cadenas,
   asi que un cierre puede arrastrar funciones que no hacen falta. Inofensivo, engorda las sondas.
5. **`52/52 contratos ejecutados` es la salida del propio gate**, y la recompute; que los 52 se
   ejecuten de verdad en CI depende de la remediacion de TASK-0336. Lo arrastro de mi veredicto
   anterior con el mismo encuadre tuyo: no bloquea aqui.
6. **Anomalia de higiene que limpie (mia).** Encontre `probe.ps1` sin trackear en la RAIZ del arbol
   gobernado, residuo de mi propia re-review de TASK-0334 (referencia `D:/Aegis_Scratch/hub/an334r2`).
   Viola DECISION-0104 y puede diferir el exec de un peer via el guard de residuo. Lo saque a scratch
   (`.../t0335r2/recovered-root-probe-an334r2.ps1`) en vez de destruirlo. Lo declaro como mio.
7. **Sin claim de revision del Analista esta vuelta.** `CLAIMS.json` no traia claim mio sobre estas
   rutas (la vuelta anterior si), asi que no hay nada que liberar. Lo senalo sin tocarlo.
8. Todos los mutantes y sondas quedaron **dentro de los clones de scratch** bajo
   `D:/Aegis_Scratch/hub/t0335r2/`; el arbol canonico no fue mutado por ninguna prueba.

## Recomendacion de cierre: OK-CLOSABLE

Los dos inventarios estan completos y los verifique recomponiendolos, no leyendolos. Las dos
regresiones cruzadas estan declaradas con su radio. Mis dos puntos estan arreglados y los dos
arreglos son falsables. Produccion intacta y el negativo de AC8 sin mover. La familia de sondas la
probe **rompiendola**: un refactor nuevo del harness ya no la tumba, y un extractor que no cierre si.

Respuesta directa a tu pregunta: **si, los dos inventarios estan completos.** Ningun fixture ni
ninguna sonda de la familia queda sin cubrir. Lo unico que queda sin declarar es la **etiqueta** de
una cuarta sonda que tambien arrastraba dependencias ausentes y que verifique que no era un rojo
medido; ponla en el reporte de cierre si quieres el radio exacto, pero no justifica otra iteracion.

Cierre en la iteracion 1 de las 2 fijadas. No escalo.

Analista.
