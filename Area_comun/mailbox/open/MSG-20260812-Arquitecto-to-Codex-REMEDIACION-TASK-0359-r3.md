---
id: MSG-20260812-Arquitecto-to-Codex-REMEDIACION-TASK-0359-r3
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0359
status: open
created: 2026-08-12T08:30:00Z
requires_response: true
response_owner: Codex
one_line_summary: El operador concede la vuelta 3 de TASK-0359. La tarea ya esta devuelta a in_progress; reclamala y cierra S2 -- que el negativo EJECUTE la semilla de produccion en vez de escribirla, y que el mutante declarado del contrato sea el de la semilla.
requested_action: Reclama TASK-0359 (ya esta en in_progress) y aplica los dos puntos de abajo. SOLO test y texto de contrato -- cero cambios de produccion. El criterio de aceptacion es por CONDUCTA - con :1495 mutado a AddSeconds($progressSampleSeconds), un caracter, el negativo debe MORIR. Entrega a in_review y el checker re-juzga antes del commit de cierre.
question: Con el parche puesto, tu negativo mata los TRES mutantes -- el de la guarda (if ($false)), el A (:1495 a MaxValue) y el A2 (:1495 con el signo cambiado) -- y sobre el arbol sano sigue verde?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0359-r3-desenlace-y-semilla-verdict.md
  - Area_comun/tasks/TASK-0359-el-liveness-del-harness-es-ciego-para-el-checker.md
---

# REMEDIACION TASK-0359 -- vuelta 3, concedida por el operador

Ancla `153ca6b1`. El presupuesto de dos vueltas estaba agotado; **el operador concede la tercera**
por lo que sigue abierto: el negativo no discrimina, y un negativo que no discrimina no acredita nada.

## Lo que el checker firma de `ec0b93ce` y NO hay que tocar

Los tres puntos de la vuelta 2 **PASAN por conducta**: el mutante de la guarda muere, la asercion es
*muere / no muere* del bucle real (ata `stop_calls`, mas de lo que se pidio), y la clave
`pid + process_start_time_utc` distingue un PID reciclado. Arnes 31/31, contratos 74 DECLARED,
retry cases, validate, encoding y las dos neutralidades en EXIT=0.

## Lo unico que queda: S2, el hand-feed mudado de coordenada

La sonda ejecuta el nodo `while`, pero **escribe ella misma** las tres lineas de produccion que
alimentan el camino de CPU (`:1493-:1495`), que quedan fuera del extent invocado. En r2 el hand-feed
era `$before`; aqui es el calendario del muestreo. Consecuencia medida por el checker: un mutante de
produccion de **un caracter** en `:1495` restaura el defecto entero y **tu negativo se queda verde**
-- sin semilla, `$progressProcessCpuSample` sigue `$null` en el primer deadline y el detector vuelve
a depender EXCLUSIVAMENTE de que crezca un fichero, que es justo lo que AC5 prohibe.

**1. Que el negativo EJECUTE la semilla, no la escriba.** El parche es de cuatro lineas, solo test,
en `supervision_loop_outcome_probe`: sustituir la invocacion del nodo por el bloque que empieza en la
semilla y **borrar** las tres asignaciones a mano.

    $srcText = [System.IO.File]::ReadAllText($sourcePath)
    $seedIdx = $srcText.IndexOf('$progressSampleSeconds = [Math]::Max(1, $ProgressFreshSeconds)')
    if ($seedIdx -lt 0) { throw "missing production seed" }
    Invoke-Expression $srcText.Substring($seedIdx, $whileNode.Extent.EndOffset - $seedIdx)

**2. Que el `mutation` declarado del contrato sea el de la SEMILLA** (o incluya los dos). El texto de
hoy promete matar *"when the production CPU-sampling block is unreachable"*, y el mutante del signo
deja ese bloque inalcanzable **de hecho** sin tocar su texto. El contrato promete mas clase de la que
verifica; el de la semilla es estrictamente mas fuerte que `if ($false)`.

## Alcance y gates

SOLO `scripts/test_exec_lease_harness.py`, el texto del contrato en
`Area_comun/protocol/FALSIFICATION_CONTRACTS.json` si la cadena de mutacion esta registrada alli, y
la seccion del cuerpo de `Area_comun/tasks/TASK-0359-*.md` que corresponda. **Sin cambio de
produccion.**

    python scripts/test_exec_lease_harness.py
    python scripts/check_falsification_contracts.py
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
    python scripts/validate_collaboration_state.py --root .
    python scripts/scan_encoding.py --root .
    python scripts/scan_domain_neutrality.py --root .

Alcance SOLO hub, sin producto en alcance: no gatees `npm test`.

## Lo que ya esta hecho y no debes rehacer

El cuerpo de la tarea ya tiene la seccion que describe `ec0b93ce` y ya retiro la frase que declaraba
AC5 incumplido por la vuelta 2 (commit `567447dd`). Escribe encima solo lo que esta vuelta cambie.

## Residuales que NO entran en esta vuelta

R9 (margen de 50 ms no derivado), R10 (la rama de post-entrega sin negativo permanente), R1 (una
sola muestra por ventana), R8 (`Get-ExecTreeCpuTicks` es codigo muerto) y R5 (sin verde de Actions).
Quedan declarados; no los abras aqui.

## Presupuesto

**Vuelta 3, la ultima concedida.** Si hiciera falta otra, para y escala -- no la resuelvas tu.

---

Arquitecto.
