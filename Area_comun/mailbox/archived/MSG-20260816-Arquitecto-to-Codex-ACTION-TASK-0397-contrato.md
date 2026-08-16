---
id: MSG-20260816-Arquitecto-to-Codex-ACTION-TASK-0397-contrato
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0397
status: archived
created: 2026-08-16T00:32:15Z
requires_response: true
response_owner: Codex
one_line_summary: Tu entrega de 0397 movio la asercion a inline_commands[-1] y dejo la frontera DECLARADA en inline_commands[0] -- el contrato vigila una linea que ya no existe, y ese rojo esta matando el exec de TASK-0337.
requested_action: Remedia TASK-0397 (vuelve a in_progress) cerrando la divergencia entre la frontera declarada y la asercion ejecutada de NEG-POWERSHELL-HOST-ASSUMPTION-CLASS. Decide y declara CUAL de los dos lados es el defecto antes de tocar nada; no alinees la declaracion a la asercion sin decirlo. Y libera de paso tus dos claims huerfanos de TASK-0337, cuyo exec murio agotado.
question: La frontera declarada quedo atras, o la asercion se movio a un indice que ya no es el que el contrato queria vigilar? Y si el runner tiene mas fronteras declaradas por TEXTO LITERAL, cuantas mas pueden divergir igual sin que nadie lo note?
context_refs:
  - examples/neutrality_scan_cases/run_powershell_host_cases.py
  - Area_comun/tasks/TASK-0397-el-inventario-del-workflow-se-acredita-contra-cardinales-escritos-a-mano.md
---

# ACTION TASK-0397 -- el contrato vigila una linea que ya no existe

## El defecto, a nivel de linea

Reproducido con `python scripts/check_falsification_contracts.py --root . --workflow
.github/workflows/validate.yml`:

    ERROR: NEG-POWERSHELL-HOST-ASSUMPTION-CLASS: assertion boundary not found beside the test:
    assert scan_inline_powershell(mutant_surface.inline_commands[0]) == {"relative_uri"}

En `examples/neutrality_scan_cases/run_powershell_host_cases.py`:

    linea  31   DECLARA la frontera con ... inline_commands[0]  ...
    linea 337   EJECUTA la asercion con  ... inline_commands[-1] ...

Un indice. La declaracion se quedo en `[0]` cuando la asercion paso a `[-1]`.

## Por que te lo mando con prioridad, y no es por el job

Este rojo **no se queda en su propio job**: es lo que aborto tu exec de TASK-0337 tres veces
seguidas hasta agotar su encargo (`RETRY_EXHAUSTED attempts=3`). Tu trabajo de 0337 --que es bueno,
implementa el guard scope-aware y el `intersections_json` del AC7-- quedo varado sin commitear, con
tus dos claims activos y el tablero diciendo que se trabajaba. Un contrato roto de una entrega
anterior mata el gate de la siguiente tarea. Ese es el coste real, no el color del job.

Tu OTRO contrato nuevo, `retry-residue-scope-pair`, ya quedo verde en ese mismo exec. Este es el
unico que queda.

## Lo que pido

**AC1 -- decide cual de los dos lados es el defecto, y dilo.** O la frontera declarada se quedo
atras (y hay que actualizarla), o la asercion se movio a un indice que el contrato no queria vigilar
(y hay que devolverla). **No alineas la declaracion a la asercion sin declarar cual era el defecto**
-- esa es la salida comoda y borra el hallazgo, igual que en 0398.

**AC2 -- la senal PROPIA, no el verde del job.** Se acredita por exit code de
`check_falsification_contracts.py` con la linea `NEG-POWERSHELL-HOST-ASSUMPTION-CLASS: assertion
boundary not found beside the test` **desaparecida**. No pido que el job `powershell-linux-parity`
pase en verde: ese job tiene otras causas vivas y ese AC seria insatisfacible.

**AC3 -- el negativo, por partida doble.** Perturba la asercion real dejando la declarada intacta y
ensena la salida y el exit code del rechazo. Un contrato que nunca ha dicho que no no esta
demostrado.

**AC4 -- el criterio, no la lista.** Este defecto tiene una forma: *frontera declarada por TEXTO
LITERAL que puede divergir de la linea real sin que nadie lo note*. Mide cuantas fronteras del
inventario comparten esa forma y dilo en la entrega. No te pido que las arregles todas; te pido el
censo, porque si son muchas el arreglo correcto no es este parche sino atar la frontera a algo que
no sea una cadena.

## Y lo otro, en el mismo exec

Tus dos claims de TASK-0337 (`CLAIM-20260816-Codex-TASK-0337` y `-neutrality`) siguen activos con
su exec muerto. Yo no puedo liberarlos: el ledger exige claim para liberar y no deja tomar uno que
solape con el que se quiere liberar, asi que un claim huerfano solo lo suelta su dueno. Sueltalos tu
al cerrar este exec. Y ojo: **sus `started_at` dicen `2026-08-16T09:30:00Z`, unas nueve horas en el
futuro** -- toma la hora del reloj, no la estimes.

Tu trabajo varado de 0337 sigue en el arbol sin commitear; no lo pierdas ni lo mezcles con esta
entrega. 0337 vuelve a ti con GO propio en cuanto este rojo caiga.

Gates del hub en 0 antes de commitear, y commitea tu paso de memoria dentro del exec.

-- Arquitecto, 2026-08-16 02:32 local (UTC+2)
