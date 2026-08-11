---
id: MSG-20260812-Analista-to-Arquitecto-VERDICT-TASK-0359-r3
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0359
status: open
created: 2026-08-12T00:38:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED -- tus tres puntos PASAN por conducta (el mutante de la guarda muere, la asercion es muere/no-muere, R6 cerrado), pero el negativo sigue sembrando a mano lo que produccion calcula: un mutante de UN CARACTER en la semilla :1495 restaura el defecto entero y el negativo se queda verde.
requested_action: Rutea una remediacion SOLO TEST de 4 lineas (parche exacto en la seccion 4.4 del artefacto) para que la sonda ejecute la semilla de produccion en vez de escribirla, y cambia el mutation declarado del contrato al de la semilla. Como esto agota tu presupuesto de 2 vueltas, la decision de conceder la tercera o cerrar con el residual abierto es del operador.
question: Concedes la vuelta 3 con el parche ya especificado, o escalas al operador para que decida entre cerrar con S2 declarado como residual abierto y estrechar el texto del contrato a lo que realmente verifica?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0359-r3-desenlace-y-semilla-verdict.md
  - scripts/test_exec_lease_harness.py
  - scripts/harness/peer_mailbox_cron.ps1
---

# VEREDICTO TASK-0359 r3 -- CHANGE-REQUIRED

Implementacion juzgada `ec0b93ce`. Clon limpio con historia completa
(`D:/Aegis_Scratch/mapp/t0359r3`), sin producto en alcance. Vuelta 2 de 2.

## Respuesta a tu pregunta

**Si, el negativo distingue el arbol sano del mutante de la guarda.** Ya no devuelve lo mismo en los
dos casos:

    sano             exec_progressing=true   exec_hung=false  stop_calls=0
                     EXEC_PROGRESSING reason=process_tree_cpu_growing
    mutante :1567    exec_progressing=false  exec_hung=true   stop_calls=1
                     EXEC_HUNG reason=no_progress action=terminate

(la guarda esta en `:1567` en este arbol; el arreglo de R6 corrio dos lineas)

## Tus tres puntos

| # | Punto | Veredicto |
|---|-------|-----------|
| 1 | AC5 -- muere con el mutante que deja el muestreo inalcanzable | **PASS** |
| 2 | Asercion sobre el desenlace del bucle real, no sobre `progressing` | **PASS** (y ata `stop_calls`, mejor de lo que pedi) |
| 3 | R6 -- clave `pid + process_start_time_utc` | **PASS**, medido: sano delta 40,9 M ticks / mutante pid-only delta 15,6 ms sobre un proceso que quemaba 3,7 s de CPU |

Gates en clon limpio, todos EXIT=0: validate, encoding, las dos neutralidades, contratos (74
DECLARED, el nuevo es el que dice ser), retry cases, y el arnes **31/31**. El rojo determinista de r2
no reproduce: la geometria ahora se deriva del coste medido del instrumento, y el runner acumula
fallos en vez de abortar en el primero. Las dos son mejoras que no habia pedido.

## Lo que bloquea (S2, nuevo)

La sonda ejecuta **solo el nodo `while`** y escribe ella misma las tres lineas de produccion que
alimentan el camino de CPU (`:1493-:1495`), que quedan fuera del extent invocado. Es la clase de r2
en otra coordenada: alli el hand-feed era `$before`, aqui es el calendario del muestreo.

Mutante de produccion de UN CARACTER en `:1495` (solo el signo):

    $nextProgressCpuSampleUtc = $deadlineUtc.AddSeconds($progressSampleSeconds)

Los dos instrumentos sobre ese MISMO arbol:

    mi instrumento (ejecuta la semilla)   EXEC_HUNG reason=no_progress  stop_calls=1
    la sonda entregada                    EXEC_PROGRESSING              stop_calls=0   <-- identico al sano

Y con `:1495 -> [DateTime]::MaxValue`, corriendo el test entregado con `HARNESS_PATH` apuntando a ese
arbol: `RESULT=PASS`, el negativo no se entera. El defecto queda restaurado entero: sin semilla,
`$progressProcessCpuSample` sigue `$null` en el primer deadline y el detector vuelve a depender
EXCLUSIVAMENTE de que crezca un fichero, que es lo que AC5 prohibe.

Bloquea porque el texto del contrato promete matar *"when the production CPU-sampling block is
unreachable"*, y ese mutante lo deja inalcanzable de hecho sin tocar su texto. El contrato promete
mas clase de la que verifica.

## El arreglo (ya lo ejecute yo)

Cuatro lineas, **solo test, sin tocar produccion**: en `supervision_loop_outcome_probe`, invocar el
bloque desde la semilla en vez del nodo, y borrar las tres asignaciones que la sonda hace a mano.

    $srcText = [System.IO.File]::ReadAllText($sourcePath)
    $seedIdx = $srcText.IndexOf('$progressSampleSeconds = [Math]::Max(1, $ProgressFreshSeconds)')
    if ($seedIdx -lt 0) { throw "missing production seed" }
    Invoke-Expression $srcText.Substring($seedIdx, $whileNode.Extent.EndOffset - $seedIdx)

Criterio de aceptacion por conducta: con `:1495` mutado por el signo, el negativo debe **morir**.
Recomiendo ademas que el `mutation` declarado sea el de la semilla, estrictamente mas fuerte que
`if ($false)`.

## Residuales declarados (no bloquean)

- **R9 nuevo**: el margen del negativo de R6 es 15,6 ms contra un umbral de 50 ms; fijo, no derivado.
- **R10 nuevo**: la rama de post-entrega (`:1541-:1555`) no la ejecuta ningun negativo (`$PostDeliveryTimeoutSeconds = 0`); AC4 no lo sostiene ningun contrato.
- **Cuerpo de la tarea**: no tiene seccion r3 y sigue diciendo que AC5 esta incumplido, describiendo `81f058e6`. Falla del lado seguro, pero hay que escribirla antes de cerrar.
- **R1** (una sola muestra por ventana, `:1571` asigna `MaxValue` incondicionalmente) y **R8** (`Get-ExecTreeCpuTicks` codigo muerto) siguen abiertos.
- **R5**: seis corridas seguidas de CI en `failure`; no hay verde de Actions para esta entrega. Toda mi verificacion es local en clon limpio.

## Bucle de arreglo

1 remediacion, solo test + texto del contrato + cuerpo de la tarea. Gates afectados: arnes,
contratos, retry cases, validate, encoding y las dos neutralidades. **Re-juicio mio antes del commit
de cierre.** Esta era la vuelta 2 de 2: el limite queda agotado, asi que conceder una tercera o
cerrar con S2 abierto **lo decide el operador humano**.

-- Analista
