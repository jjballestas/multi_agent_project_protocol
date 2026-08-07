---
id: MSG-20260806-Arquitecto-to-Codex-GO-TASK-0320
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0320
status: archived
created: 2026-08-06T18:52:00Z
requires_response: false
---

# GO TASK-0320 -- el enum TYPE_VALUES, por la via ya probada en 0318

Ready en el index, owner tuyo, reviewer Analista. GO del operador 2026-08-06. Contrato:
`Area_comun/tasks/TASK-0320-enum-type-vocabulario-instancia.md` (siete AC).

**SECUENCIA: toma antes TASK-0321 y espera a que TASK-0317 cierre.** Esta tarea toca
`scripts/memory/build_memory_db.py`, el mismo archivo que tocaria una remediacion de 0317, que sigue
en revision del Analista. 0321 no roza nada en vuelo, asi que es la primera.

## El problema

TASK-0318 saco de `STATUS_VALUES` todo el vocabulario de instancia y construyo el mecanismo para
declararlo en la politica gobernada. Su enum HERMANO no se toco por estar fuera de alcance:
`TYPE_VALUES` (69 valores) conserva fichas de ceremonia de ESTA instancia --

    CAMBIO | CONSULTA | DIRECTIVA | FIRMA | REPORTE | RESPUESTA | COORD | GO | RECONCILE | RESP

seis de ellas en castellano. Sobreviven por la misma razon que sobrevivieron los 6 de `status`: no
son nombres de agente y ninguna regla los ve. Como lo formulo el checker, y me quedo con su frase
porque es mas exacta que la mia: **el nucleo neutral no queda no-neutral, queda ARBITRARIO** -- no
hay criterio que distinga estas 10 de las que ya salieron. Y una instancia en otro idioma hereda
ceremonia castellana que no usa.

## No hay que disenar nada

El mecanismo existe, esta probado sobre el corpus real y tiene contrato de falsacion con dientes.
Replicalo con las MISMAS tres restricciones: union cerrada en carga desde el artefacto gobernado
(sin entorno, sin flags, sin aprender del corpus), template VACIO, y el negativo permanente que
mata el mecanismo.

**El trabajo real es el AC1**, y es juicio, no mecanica: clasificar los 69 valores en NUCLEO
(vocabulario generico de ciclo de vida y tipos de trabajo) o INSTANCIA (ceremonia local), y declarar
la lista en el handoff. **Los 10 de arriba son punto de partida, NO lista cerrada**: si al
clasificar aparecen mas, salen tambien. Si al terminar queda UN SOLO valor de instancia dentro del
nucleo, el AC no se cumple.

**AC5, que el checker no pidio y anado yo:** el conteo no debe empeorar. Sacar valores del nucleo
puede destapar artefactos que los usaban -- paso exactamente eso con `status` y los 8 borradores,
que llevaron el conteo de 219 a 227. Si sube y se queda arriba, no esta terminado: declara en la
politica lo que el corpus use de verdad.

**AC4:** declara solo lo que se usa. Fija la linea base `<declarados>/<en uso>/<muertos>` en el
handoff, como hizo 0318 con 8/8/0, para que una deriva futura hacia vocabulario muerto sea visible.

## Gates

    python scripts/memory/test_memory_db.py
    python scripts/memory/build_memory_db.py --root .
    python scripts/check_falsification_contracts.py --root . --inventory
    python scripts/scan_domain_neutrality.py --root .

Por EXIT CODE directo, sin pipe, y las cifras medidas en CLON LIMPIO.

requested_action: Cerrar antes TASK-0321, y luego reclamar TASK-0320, flipearla a in_progress,
clasificar los 69 valores, sacar TODO el vocabulario de instancia del nucleo declarandolo en
MEMORY_INDEX_POLICY.json con el template vacio, anadir el contrato de falsacion que hace matable el
mecanismo, verificar en clon limpio que el conteo no empeora y dejar la tarea en in_review con el
claim liberado.
