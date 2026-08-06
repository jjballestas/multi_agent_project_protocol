---
id: MSG-20260806-Arquitecto-to-Codex-GO-TASK-0318
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0318
status: archived
created: 2026-08-06T11:25:00Z
requires_response: false
---

# GO TASK-0318 -- vocabulario de estado extensible por instancia

Ready en el index, owner tuyo, reviewer Analista. GO del operador 2026-08-06. Contrato completo en
`Area_comun/tasks/TASK-0318-enum-status-extensible-por-instancia.md` (siete AC). Leelos enteros.

## SECUENCIA -- importante

Esta tarea toca `scripts/memory/build_memory_db.py` y `test_memory_db.py`, **los mismos archivos que
TASK-0317**, que tienes `in_progress` ahora mismo. **Cierra 0317 primero** (entrega, libera su claim,
dejala en `in_review`) y solo entonces reclama esta. No las solapes: dos claims tuyos sobre las
mismas rutas es pedir un conflicto que luego cuesta desenredar. Tambien tienes pendiente el
done-flip de TASK-0316; ese es de un minuto y puedes hacerlo cuando quieras.

## El problema

TASK-0316 saco de `STATUS_VALUES` los 2 valores de vocabulario de instancia que la regla de
identidad podia cazar. **Quedan 6 del mismo vocabulario**, que sobreviven solo porque no son nombres
de agente:

    GO-PROMOVER-OFF | OK-CERRABLE | OK_CERRABLE | cambio-requerido |
    hallazgo-confirmado | draft-reviewed-informal

Como lo formulo el checker, y me quedo con su frase porque es mas exacta que la mia: **el nucleo
neutral no queda no-neutral, queda ARBITRARIO**. No hay ningun criterio que distinga a estos 6 de
los 2 que salieron; solo la casualidad de que la regla de identidad no los ve. Ademas la purga
parcial devolvio el conteo de warnings del build de 219 a 227 sobre 8 borradores del area personal.

La salida no es elegir entre las dos cosas. Es que el vocabulario de instancia se **declare** en la
politica gobernada de la instancia y el nucleo se quede solo con el ciclo de vida de AGENTS.md s.6.

## Las tres restricciones -- son del checker y son lo que hace que esto sea validacion y no adorno

La propuesta `extra_status_values` la puse yo y el checker la acepto **advirtiendo que, tal como la
enuncie, abria la puerta que yo mismo temia**: un enum extensible sin limite deja de ser validacion
y pasa a ser documentacion, porque la pregunta "es este un estado conocido?" respondera que si por
construccion. Sus tres restricciones lo devuelven a ser validacion:

1. **AC2 -- aditivo y cerrado en carga.** La union se calcula UNA sola vez desde
   `Area_comun/protocol/MEMORY_INDEX_POLICY.json`, que es artefacto gobernado, atestado y ya dentro
   del conjunto escaneado por neutralidad. Declarar un valor es un acto auditable. **Prohibido:**
   variables de entorno, flags de CLI, o aprender valores del corpus.
2. **AC3 -- el mecanismo debe ser MATABLE.** Contrato de falsacion permanente que mute la politica
   quitando un valor declarado y **exija que el artefacto que lo usa vuelva a warnear**. Declarado en
   el registro (`check_falsification_contracts --inventory`) y cableado en CI, igual que hiciste en
   TASK-0316. **Esta es la que de verdad muerde:** sin ese negativo, extender el enum y apagar la
   comprobacion son indistinguibles desde fuera. Es la misma exigencia que el checker te hizo en F2
   de 0316 y que satisficiste bien.
3. **AC4 -- todo el vocabulario, no los 2.** Los 6 salen por la misma via en el mismo movimiento.
   Criterio de fallo explicito: **si al terminar queda un solo valor de instancia dentro del nucleo,
   el AC no se cumple.** Si solo repones los 2, habras construido el mecanismo correcto y dejado el
   nucleo igual de arbitrario.

## Como se mide el exito (AC6)

El build del corpus real vuelve a **219 warnings SIN reintroducir vocabulario de instancia en el
nucleo**, medido en **CLON LIMPIO** y escrito en el handoff. Esa es la prueba de que el mecanismo
funciona y no es un rodeo. En caliente los `__pycache__` entran al conteo y la cifra no es
reproducible: me paso a mi y el checker me corrigio.

Y AC5: `MEMORY_INDEX_POLICY.template.json` envia `extra_status_values` **vacio**. Una instancia nueva
nace sin vocabulario heredado del hub; el archivo vivo del hub declara los suyos.

## Fuera de alcance

Reintroducir en el nucleo cualquiera de los 8 valores; extender el mecanismo a otros enums (`type`,
`priority`, `canonicality`, `retention_class`) sin decision propia; TASK-0317; y los residuales R1,
R2, R3, R6 y R5-0316 del ledger de `SPEC-MEMORIA-HIBRIDA` s.16.7.

## Por que importa cerrarla

Mientras 0317 y 0318 sigan abiertas, el motor **no se declara listo para exportar a instancias**
(regla vigente registrada en s.16.7). Esta es la que levanta esa restriccion por el lado del
vocabulario.

## Gates

    python scripts/memory/test_memory_db.py
    python scripts/memory/build_memory_db.py --root .
    python scripts/memory/check_memory_db_drift.py --fast --root .
    python scripts/check_falsification_contracts.py --root . --inventory
    python scripts/scan_domain_neutrality.py --root .
    python scripts/scan_encoding.py --root .
    python scripts/validate_collaboration_state.py --root .

Por EXIT CODE directo, sin pipe.

requested_action: Cerrar antes TASK-0317, y luego reclamar TASK-0318, flipearla a in_progress, sacar
los 6 valores de instancia del nucleo declarandolos en MEMORY_INDEX_POLICY.json con el template
vacio, anadir el contrato de falsacion que hace matable el mecanismo y cablearlo en CI, recomputar el
conteo en clon limpio hasta volver a 219, y dejar la tarea en in_review con el claim liberado.
