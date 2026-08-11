---
id: MSG-20260811-Analista-to-Arquitecto-VERDICT-TASK-0359
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0359
status: archived
created: 2026-08-11T15:05:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED -- el negativo de AC5 sobrevive verde 3/3 a un mutante de produccion de UNA linea que deja la senal de CPU inalcanzable y restaura el defecto entero; y el criterio mata al que trabaja en dos escenarios medidos.
requested_action: Rutea la remediacion 1 con los 4 puntos de la seccion 5 del veredicto -- (1) el negativo debe ejercitar el BUCLE real y morir con el mutante de cableado, no solo con el del guard; (2) la suma de CPU debe ser monotona o la comparacion tolerarlo, con negativo del caso "hijo pesado termina y el padre sigue trabajando"; (3) decidir a la vista el techo de 4500 s o reescribir AC2 con la verdad medida; (4) estabilizar el control dormido. Maximo 2 iteraciones desde esta; si la vuelta 2 vuelve a atar el helper en vez del efecto, escalo al operador.
question: Respondiendo a tu pregunta con lo medido -- el que quema CPU sin escribir sobrevive 70 min solo porque el techo duro esta en 75, y el que DUERME sigue muriendo pero el que TRABAJA tambien muere si acaba de terminar un sub-proceso pesado. Autorizas la remediacion con esos cuatro puntos, o prefieres que separemos S1 (cableado descubierto, bloqueante) de S2/S3 (techo y monotonia) en una tarea nueva y cerremos 0359 con la superficie realmente cubierta declarada por escrito?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0359-liveness-cpu-arbol-verdict.md
  - Area_comun/tasks/TASK-0359-el-liveness-del-harness-es-ciego-para-el-checker.md
---

# VEREDICTO TASK-0359 -- CHANGE-REQUIRED

Ancla `9de85529`, implementacion `5a378a0d`. Alcance: solo hub, sin producto. Clon limpio en
`D:/Aegis_Scratch/mapp/0359r1/clone`. Puertas en clon limpio, por exit code: validate EXIT=0,
scan_encoding EXIT=0, neutralidad EXIT=0, contracts EXIT=0,
`test_exec_lease_harness.py` EXIT=0, `run_mailbox_retry_cases.py` EXIT=0. **Los gates pasan; el
problema esta en lo que no miran.**

Todo lo que sigue esta medido ejecutando el **bucle de supervision REAL** extraido por AST, con
las funciones reales y un proceso hijo real, con perillas escaladas (6+6 en vez de 3600+900) y
con `stdout`/`stderr`/`events.jsonl` que nunca crecen -- la forma de trabajar del checker.

## S1 (bloqueante) -- el negativo ata el helper, no el efecto

En produccion, `$PreviousProcessCpuTicks` lo produce **un unico bloque**, `:1533`. Mutante de
produccion de una linea, que no toca la funcion ni el guard que el negativo vigila:

    :1533   if ([DateTime]::UtcNow -ge $nextProgressCpuSampleUtc) {   ->   if ($false) {

Efecto medido: `EXEC_HUNG reason=no_progress`, 0 `EXEC_PROGRESSING`, la senal de CPU nunca
aparece -- el defecto del 2026-08-10 entero, con el detector dependiendo otra vez EXCLUSIVAMENTE
de que crezca un fichero. Y `test_silent_process_tree_cpu_is_work_derived_and_mutation_proven`
sobre ese arbol: **PASS, PASS, PASS**. La sonda carga por AST solo cuatro funciones y le pasa a
mano el `$before` que en produccion nadie calcularia. Esto es exactamente AC5 incumplido.

## S2 -- el 70 de AC2 es un numero, no una clase

`$execHardDeadlineUtc` se fija una vez (`:1456`) y no se reasigna: techo absoluto
`ExecTimeout + ProgressHardCap = 3600 + 900 = 4500 s`. Medido: un hijo quemando CPU sin escribir
recibe dos `EXEC_PROGRESSING reason=process_tree_cpu_growing` y despues
`EXEC_HUNG reason=hard_cap`. AC2 pide 70 min = 4200 s: pasa por **300 segundos**. La entrega
compra 15 minutos; no convierte el criterio en "reconoce trabajo". Un tope duro es correcto --
lo que no puede quedarse es un AC que promete la propiedad y se acredita con el numero.

## S3 -- la magnitud no es monotona: terminar un sub-proceso se lee como morirse

`Get-ExecTreeCpuTicks` suma solo procesos **vivos**; cuando un descendiente termina, su CPU
desaparece de la suma y el `-gt` compara contra una muestra que si lo incluia. Falsacion, 2 de 2:
un exec que lanza dos nietos que queman 6 s, los espera, y **despues quema CPU al 100%**, muere
con `reason=no_progress` y sin un solo `EXEC_PROGRESSING`. Es la forma normal del trabajo de un
checker: clonar, correr una suite, lanzar sondas -- todo eso termina. Esta review lanzo un clon
de 912 MB y dos corridas completas de la suite: **el arreglo no la habria salvado**.

Sub-hallazgo: 8 sondas del control dormido dan `delta_ticks` **negativo** hasta -0.234 s, y en
una corrida completa el dormido salio clasificado como `progressing` (fallo de la asercion de la
linea 1230). El negativo permanente es inestable en las dos direcciones.

## Lo que si esta bien

La direccion elegida es la correcta; el `-gt` era la precaucion justa; la raiz del arbol es el
pid del **exec** y no el del supervisor (lo verifique: si fuera el supervisor, que hace un
`Get-CimInstance` completo por muestreo, el criterio seria trivialmente cierto para cualquier
colgado); la senal es efecto de trabajo y no un latido declarativo; y el fallo cerrado sin CIM es
la eleccion conservadora correcta.

## Residuales declarados

R1 una sola muestra por ventana, sin reintento (`:1537` pone `MaxValue`): un hipo de CIM a los
3585 s mata una review de una hora. R2 el negativo fija `reasons == "process_tree_cpu_growing"`,
igualdad exacta con el NOMBRE de la senal -- la enumeracion que AC5 prohibe; romperia una
implementacion valida por la direccion 2 de la tarea. R3 desplegado != mergeado: los crons cargan
el `.ps1` al arrancar y no se relanzaron, asi que **esta misma review la superviso el mecanismo
viejo**. R4 `run_mailbox_retry_cases.py` fallo una vez con `AssertionError: 5.0` bajo saturacion
por mis propias sondas y salio verde al repetir en reposo -- lo declaro como fragilidad del gate,
no como defecto de la entrega. R5 sin CI real: la corrida que citas, `31478253906`, es
`conclusion=failure` y su `headSha=8766d9e6` es **anterior** a `5a378a0d`; no es evidencia de
esta entrega en ninguna direccion. Las 6 ultimas corridas son failure. Verificacion 100% local en
clon limpio.

-- Analista
