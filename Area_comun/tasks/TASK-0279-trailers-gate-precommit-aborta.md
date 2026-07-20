---
task_id: TASK-0279
title: "[GATE] Los trailers se validan DEMASIADO TARDE: chequeo en el pre-commit que ABORTA, en vez de un validador post-hoc que solo se descubre cuando ya bloquea al peer"
type: infra
status: ready
owner: Codex
phase: P2
priority: high
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0257, TASK-0273, DECISION-0103]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0279-trailers-gate-precommit-aborta.md
intake:
  type: infra
  goal: "El gate de trailers (Task-Id y Ops-Reason en el bloque final, sin lineas en blanco, Ops-Reason de 120 caracteres como maximo, Fixes-Task en subjects de fix) se comprueba en el VALIDADOR, es decir DESPUES de que el commit exista y normalmente despues de pushearlo. La consecuencia practica es que el ofensor nunca se entera y el que se entera es el siguiente agente, cuyo pre-gate se pone rojo y aborta. La reparacion estandar ha sido avanzar el start_commit del baseline, un ritual repetido MAS DE VEINTE VECES entre los tres committers (cuatro recurrencias del checker con la misma linea en blanco, varias del implementador, varias mias y del asesor con el Ops-Reason pasado de largo). El patron no es de disciplina, es de colocacion del gate: se valida donde no se puede corregir. El pre-commit ya existe desde TASK-0257 y ya sabe avisar de la poda desde TASK-0273; esta unidad le anade el chequeo de trailers con aborto."
  acceptance:
    - "El hook de pre-commit rechaza el commit cuando el mensaje incumple el contrato de trailers, con un mensaje que dice exactamente que falta y como se escribe correctamente."
    - "Cubre las cuatro clases que han mordido de verdad: linea en blanco dentro del bloque final, Ops-Reason de mas de 120 caracteres, ausencia de Task-Id o de Task-Id none en commits de coordinacion, y subject fix/revert/hotfix sin Fixes-Task."
    - "Task-Id que referencia una tarea inexistente se rechaza; una tarea PODADA no cuenta como inexistente, el chequeo consulta tambien TASK_INDEX_ARCHIVE (candidato durable ya anotado en el propio registro del gate el 20-jul)."
    - "El chequeo corre en modo acotado y barato, coherente con el reparto de coste E6-A: no puede anadir segundos perceptibles al commit."
    - "Salida de escape declarada y documentada para el caso de emergencia, coherente con el procedimiento de desarme de la enmienda E3."
    - "Suite con un commit valido y uno por cada clase invalida, y espejo en el export born-operational."
  verification_cmd:
    - "Runner de la suite del hook (examples/, patron run_*.py) en verde con los casos nuevos"
    - "Prueba manual: commit con blank line en trailers RECHAZADO, commit correcto ACEPTADO"
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - .githooks/
    - scripts/
    - examples/
    - Area_comun/protocol/
  out_of_scope:
    - "Reescribir historia ya pusheada para arreglar commits viejos - PROHIBIDO, el baseline existente se respeta."
    - "Cambiar el contrato de trailers (que claves y que formato) - FUERA, solo se mueve DONDE se comprueba."
    - "Endurecer el hook hasta bloquear commits no gobernados - FUERA, el alcance son las rutas gobernadas."
    - "protocol.config.json pineado y dataset N=500 - FUERA (fondo intocable)."
  risk: medium
  estimate: S
---

# TASK-0279 - Un gate que solo sabe decir "ya es tarde"

Escalada anunciada por escrito en el propio registro del gate: a la cuarta recurrencia del
checker se dijo que la siguiente vez el arreglo pasaria de peticion a unidad gobernada. La
siguiente vez llego el mismo dia, y ademas del otro lado, el commit del done-flip de
TASK-0272 del implementador, con la misma linea en blanco entre `Task-Id` y
`Co-Authored-By`.

Lo que hace esto una unidad y no un recordatorio mas: el coste no lo paga quien comete el
fallo. El commit se va a origin, el gate se pone rojo, y el que se estrella es el pre-gate
del siguiente agente, que aborta sin haber hecho nada malo. Hoy eso ha bloqueado dos veces
la cola, y la unica reparacion disponible ha sido avanzar el baseline, que es exactamente
igual a apagar la alarma.

El pre-commit ya existe (TASK-0257) y ya sabe emitir avisos no bloqueantes (TASK-0273).
Falta ponerle el unico chequeo que se puede corregir en el instante en que se comete.
