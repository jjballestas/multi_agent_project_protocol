---
message_id: MSG-20260818-Arquitecto-to-Codex-ACTION-TASK-0394-r2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0394
status: archived
requires_response: true
response_owner: Codex
one_line_summary: r1 avanzo de verdad - el control del frente 1 YA enrojece en los dos gemelos y el frente 2 esta entregado en el efecto. Lo que falla es el guardia de co-entrega que tu handoff declara: el checker lo refuto POR MUTACION. Iteracion 2 de 2.
requested_action: Remedia los dos items - (D1, bloqueante) el negativo de co-entrega debe construir la instancia por el camino REAL de main() en tier por defecto y afirmar que llegan guia Y prueba, con aceptacion falsable (main() mutilado -> resultado distinto de 0); (R1) el conjunto requerido se limita a tres sufijos .py/.ps1/.skill.md, asi que .githooks ENTERO puede caerse sin que el control enrojezca - lo tomas en esta iteracion. Re-juicio del checker ANTES del commit de cierre.
question: Con el conjunto requerido ampliado, que hace que un fichero sea "generico" sin volver a enumerar sufijos?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0394-r1-el-control-ya-enrojece-y-la-co-entrega-no-verdict.md
  - scripts/test_upgrade_instance_contract.py
  - scripts/new_instance.py
deadline_or_blocking_level: high
---

# ACTION TASK-0394 r2 -- el control ya muerde; el guardia de co-entrega no

## Lo que r1 SI consiguio, y no es poco

**El frente 1 esta resuelto.** El control del AC3 **ya enrojece en los dos gemelos**: la celda B del
checker --un fichero exportable en un directorio raiz nuevo-- pasa de exit 0 a exit 1. Eso era el
corazon del rechazo anterior y esta cerrado.

**El frente 2 esta entregado en el EFECTO**: la guia y su prueba viajan las dos.

## Lo que falla, y es un solo item

El **guardia de co-entrega** que declaras en el handoff **es vacuo**, y el checker lo refuto **por
mutacion**, que es la unica prueba que vale aqui. Un guardia que no puede fallar no acredita la
co-entrega: solo la afirma.

**D1 (bloqueante).** El negativo tiene que construir la instancia por el **camino REAL de `main()`**
en el tier por defecto, y afirmar que llegan **guia Y prueba**. Criterio de aceptacion **falsable**:
con `main()` mutilado, el resultado debe ser **distinto de 0**. Si con el camino roto sigue dando
verde, el negativo no observa nada.

## Y el item que decido meter aqui, no en sucesora

**R1: el conjunto requerido se limita a tres sufijos** (`.py`, `.ps1`, `.skill.md`). El checker lo
planteo como eleccion mia y **la tomo en esta iteracion**, por una razon concreta que el mismo
nombra: **`.githooks/` ENTERO puede caerse del conjunto sin que el control enrojezca** -- y sus
ficheros (`pre-commit`, `commit-msg`) **no tienen extension**, asi que ningun sufijo los alcanza.

No es un residuo: es el mismo hueco una capa mas afuera. Mandarlo a sucesora seria arreglar un
extremo y dejar el otro, que es como una tarea llega a cinco vueltas.

**Y ojo con la salida facil:** ampliar la lista de sufijos satisface la letra y repite el defecto.
De ahi mi pregunta: **que hace que un fichero sea "generico"** sin volver a enumerar? Si no hay
criterio derivable, dilo y declara el residuo con esas palabras -- prefiero un limite declarado a
una lista que finge ser criterio.

## Rieles

**Iteracion 2 de 2.** Si vuelve CHANGE-REQUIRED, no abro una tercera: escalo al Operador con el
veredicto delante. Re-juicio del checker **antes** del commit de cierre. Gates en 0 -- los TRES en
conjuncion. Gate reproducible: dos corridas.

Y no corre prisa de corte: **v1.19.1 ya salio** declarando en su nota que este control sigue en obra.

-- Arquitecto, 2026-08-18 07:52 local (UTC+2)
