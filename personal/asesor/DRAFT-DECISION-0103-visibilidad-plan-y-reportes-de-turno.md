---
decision_id: DRAFT-DECISION-0103
title: "Visibilidad obligatoria del trabajo gobernado: plan aprobado antes del primer turno, reporte de asignacion, y reporte de entrega con obstaculos y soluciones"
status: draft
date: 2026-07-19
author: Asesor
approved_by: "PENDIENTE DE FIRMA DEL OPERADOR"
relates_to: [DECISION-0009, DECISION-0099, DECISION-0100, DECISION-0101]
---

# DRAFT-DECISION-0103 - Visibilidad del trabajo gobernado

> Redactada por el Asesor a peticion del Operador (19-jul-2026). El Asesor NO firma:
> esto es cambio de protocolo y requiere firma soberana. Correcciones bienvenidas
> antes de firmar; una vez firmada, la implementacion es trabajo de maker gateado.

## Contexto (verificado en codigo, no opinion)

La metodologia garantiza que el trabajo sea ATESTADO, pero no que sea VISIBLE para el
humano que lo encarga. Tres huecos verificados el 19-jul-2026:

1. **No hay vista del plan.** `runtime/orchestrator.py --plan` imprime el PROXIMO turno,
   no el conjunto de unidades. Las unidades existen en disco (`Area_comun/tasks/TASK-*.md`
   + `TASK_INDEX.json`) pero nadie las presenta al humano antes de ejecutar. El humano
   aprueba una conversacion, no una lista.
2. **El runtime es mudo durante la ejecucion.** `orchestrator.py` tiene exactamente dos
   `print()`: el de `--plan` y el del resultado final. Todo lo demas se escribe a
   `runtime/runs/RUN-<id>.jsonl` (completo: agente, changed_paths, commit, gate_green,
   traza de 9 etapas, y el `routing_decision` con el porque de la eleccion de agente).
   Es decir: **el problema es de VISTA, no de datos.** Los datos ya estan emitidos y
   atestados.
3. **Los obstaculos se pierden.** `runtime/turn_schema.json` exige
   `turn_id, task_id, agent, outcome, summary, changed_paths, commit_message` y admite
   `tools, actions, decision_refs, transitions, gate, next_hint`. **Cero campos para
   obstaculos, causa raiz o solucion.** Grep de `lessons|problemas|handoff_note` en
   `scripts/` y `runtime/`: 0 hits. Cuando un agente pelea contra un error y lo resuelve,
   esa solucion muere con su contexto: el commit guarda QUE quedo, nadie guarda CONTRA QUE
   se peleo.

Evidencia de que el hueco 3 es caro: todas las lecciones duras vigentes de esta
metodologia (Ops-Reason <=120 medido en paso separado; commits path-limited por indice
compartido; `requires_response` exige `question` + `requested_action`; `codex exec` no
emite JSON puro y necesita wrapper) nacieron de que un agente se estrello y **alguien las
transcribio a mano** a su ESTADO. El bucle de aprendizaje existe, pero es artesanal, solo
cubre al agente que se estrello, y solo si se acuerda.

## Decision

### Clausula 1 - PLAN APROBADO antes del primer turno (gate duro)

Ningun conjunto de unidades gobernadas se ejecuta sin que el humano que lo encarga haya
visto y aprobado la LISTA. El plan presentado incluye, por unidad:

`id | goal | acceptance | verification_cmd | required_capability | risk | estimate`

(los campos ya son obligatorios: son el intake DoR que valida
`scripts/validate_collaboration_state.py`, campos `type, goal, acceptance,
verification_cmd, scope_routes, out_of_scope, risk, estimate`).

- Es un **checkpoint de turno 0**: aprueba el CONJUNTO, no un turno. Distinto de
  `supervised_autonomy.human_checkpoint_every_k`, que solo pausa entre turnos.
- La aprobacion se registra (no es un "ok" de chat que se pierde): referencia al plan
  aprobado en el event log / mailbox firmado.
- Si el plan cambia materialmente durante la ejecucion (unidades nuevas, cambio de
  acceptance, cambio de riesgo), **se re-aprueba**; no se amplia en silencio.

### Clausula 2 - REPORTE DE ASIGNACION

Cuando una unidad se asigna a un agente, se reporta al humano: unidad, agente,
y **por que ese agente**. El dato ya existe: `routing_decision` del run-log registra
`required_capability`, `load_score`, candidatos y metricas. Esta clausula solo obliga a
presentarlo. Coste marginal ~0.

### Clausula 3 - REPORTE DE ENTREGA con obstaculos (el corazon de la decision)

Al entregar una unidad, el reporte incluye un bloque estructurado:

```
obstacles:
  - what: <con que se choco>
    root_cause: <por que pasaba>
    resolution: <como se resolvio>
    recurrence_risk: low | medium | high
```

Reglas anti-teatro (sin esto el campo se degrada a "sin problemas" y el humano deja de
leerlo en dos semanas):

- **Lista vacia es respuesta legitima.** No se fuerza prosa donde no hubo friccion.
- **Pero NO puede ir vacia si el turno tuvo friccion**, y la friccion es mecanicamente
  detectable: `gate_green: false`, `attempt > 1` / bounce, o revert. En esos casos el
  agente no puede escaparse con silencio.
- Estructurado, no prosa libre: el objetivo es que sea **consultable**, no legible una vez.

Proposito declarado: los obstaculos son la materia prima para crear skills y endurecer el
protocolo. Un obstaculo con `recurrence_risk: high` es un candidato explicito a skill o a
regla nueva.

### Clausula 4 - DOS CARRILES (o cubre solo una fraccion)

La mayor parte del trabajo NO pasa por el runtime: Arquitecto, Codex por cron y Analista
trabajan en sesion. Por tanto las clausulas 2 y 3 se implementan en **ambos** portadores,
con el MISMO bloque `obstacles`:

- carril runtime: campo en `runtime/turn_schema.json` (+ validacion en `turn_validate`);
- carril sesion: mensaje `type: REPORTE` por mailbox, con el bloque en el cuerpo.

### Clausula 5 - ALCANCE

Capa HUB (metodologia), con espejo en el export born-operational (DECISION-0096): toda
instancia presente y futura, incluida cualquier instancia de terceros (p.ej. Julian).

## Lo que esta decision NO hace (limites explicitos)

- **No convierte el runtime en un stream de consola.** El Operador rechazo explicitamente
  el "mostrar todo lo que hacen". Los reportes son por EVENTO (asignacion / entrega), no
  continuos, y son ARTEFACTOS releibles, no scroll.
- **No debilita DECISION-0009.** Los ficheros atestados siguen siendo la fuente de verdad;
  cualquier vista es una PROYECCION de los ficheros, nunca al reves. Si vista y commit
  discrepan, gana el commit.
- **No toca maker != checker** (DECISION-0099 / DECISION-0101). El Asesor sigue sin poder
  ser maker: presenta el plan y los reportes, no los ejecuta.
- **No enciende `supervised_autonomy`** ni el invoker real: son gates independientes.

## Implementacion (trabajo gobernado tras la firma; NO del Asesor)

| # | unidad | carril | capability |
|---|---|---|---|
| 1 | anadir bloque `obstacles[]` a `runtime/turn_schema.json` | runtime | implementer |
| 2 | validacion condicional (obligatorio si gate rojo / attempt>1 / revert) en `turn_validate` | runtime | implementer |
| 3 | vista de plan (`--plan-all` o render de TASK_INDEX) + gate de aprobacion turno 0 | runtime | implementer |
| 4 | plantilla de REPORTE de mailbox con bloque `obstacles` | sesion | (doc) |
| 5 | regla de arranque del Asesor: nunca ejecutar sin plan aprobado | doc | (doc) |
| 6 | revision adversarial de 1-3 por checker de proveedor diverso | gate | reviewer |

Nota de secuencia: esta decision deberia ir ANTES del pipeline maker->checker multi-turno.
Multi-turno sin reporte de entrega es exactamente la ceguera que motiva esta decision,
multiplicada por N turnos.

## Paradoja de arranque (declarada honestamente)

Si esta decision se implementa CON el runtime, ese trabajo no puede beneficiarse de la
clausula 1 (el gate de plan aun no existe). Sustituto para esa primera vez: el Asesor
presenta el plan a mano y el Operador lo aprueba por mailbox firmado antes del turno 1.
A partir de la segunda vez, el gate es del sistema, no de la buena voluntad del Asesor.

-- Asesor, 19-jul-2026. Pendiente de firma del Operador.
