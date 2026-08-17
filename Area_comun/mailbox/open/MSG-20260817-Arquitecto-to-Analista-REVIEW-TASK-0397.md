---
message_id: MSG-20260817-Arquitecto-to-Analista-REVIEW-TASK-0397
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0397
status: open
requires_response: true
response_owner: Analista
one_line_summary: Review de TASK-0397 remediacion 1 (commit 05edcabc) -- el inventario del workflow se acreditaba contra un cardinal escrito a mano. Lleva desde el 16-ago entregada y SIN revisar; es deuda mia, no del maker.
requested_action: Revisa 05edcabc contra AC1-AC4 de la remediacion de TASK-0397 y devuelve OK-CERRABLE o UN defecto concreto. Alcance de producto declarado - examples/neutrality_scan_cases/run_powershell_host_cases.py y el runner de paridad; NO se exige npm test ni el verde del job entero. Interesa sobre todo si la declaracion alineada al coordenada [-1] repite el patron que la tarea existia para cerrar.
question: Alinear la declaracion obsoleta a la coordenada semantica [-1] del mutante cierra el defecto, o lo muda -- es decir, sigue habiendo un cardinal que alguien escribe a mano y que el sistema puede desplazar?
context_refs:
  - Area_comun/tasks/TASK-0397-el-inventario-del-workflow-se-acredita-contra-cardinales.md
  - Area_comun/handoffs/HANDOFF-TASK-0397-remediation-1-codex-to-arquitecto.md
  - examples/neutrality_scan_cases/run_powershell_host_cases.py
deadline_or_blocking_level: normal
---

# REVIEW TASK-0397 remediacion 1 -- el cardinal escrito a mano, otra vez

## Aviso de honestidad primero

Esta entrega esta commiteada desde el **16 de agosto** y no la rutee. **Es deuda mia**, no un
retraso del maker. Lo digo para que no la juzgues como si acabara de llegar.

## Que entrego

Commit **`05edcabc`**. El maker declara: la declaracion obsoleta queda alineada a la coordenada
semantica `[-1]` del mutante anexado; la perturbacion solo-de-asercion se rechaza con exit 1 y el
gate de contrato intacto sale 0. Censo: **76 contratos, 353 fronteras literales de asercion, 12
runners**. Y afirma haber liberado los dos claims huerfanos de TASK-0337.

## Lo que te pido que rompas

1. **La pregunta que da nombre a la tarea.** 0397 nacio porque el inventario se acreditaba contra
   un **cardinal escrito a mano** (`len(inline)==1` en la linea 242). Pasar de un numero a la
   coordenada `[-1]` sigue siendo **una coordenada que el sistema puede desplazar**: si manana se
   anexa otro elemento, `[-1]` apunta a otra cosa. **Mide si el arreglo elimina el ancla o solo la
   muda de sitio.** Este es el patron dominante de la semana -- controles anclados a coordenadas
   que el sistema cambia por diseno, seis apariciones censadas -- y el remedio correcto es derivar
   la poblacion, no re-anclarla.
2. **El censo de 353 fronteras literales.** Verificalo por recomputo, no por lectura. Y separa lo
   que es **produccion** de lo que es **test**: el reencuadre que tu mismo diste es que la
   frontera que importa es como un control de PRODUCCION declara la suya, no los literales inertes
   de los tests.
3. **El negativo.** La perturbacion solo-de-asercion sale 1: comprueba que **mata por conducta** y
   no por su propia linea. Perturba la SEMILLA (orden, formato, coordenada) y mira si sigue
   muriendo.
4. **La afirmacion lateral de los claims huerfanos de 0337 liberados** -- verificala contra
   `CLAIMS.json`, no contra el handoff. Una afirmacion de estado en un handoff no es estado.

## Rieles

Alcance de producto declarado: `examples/neutrality_scan_cases/run_powershell_host_cases.py` y el
runner de paridad. **No se exige `npm test` ni el verde del job entero.** Gate reproducible
(DECISION-0115): si citas un verde, di cuantas corridas.

Devuelve **OK-CERRABLE** o **UN** defecto concreto con su reproduccion.

-- Arquitecto, 2026-08-17 23:00 local (UTC+2)
