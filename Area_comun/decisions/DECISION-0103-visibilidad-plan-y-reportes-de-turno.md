---
decision_id: DECISION-0103
title: "Visibilidad obligatoria del trabajo gobernado: plan aprobado antes del primer turno, reporte de asignacion, y reporte de entrega con obstaculos y soluciones"
status: active
date: 2026-07-19
author: Asesor
approved_by: "Operador (firma directa al Arquitecto en sesion 2026-07-19: 'FIRMO la DECISION-0103 tal cual'; draft del Asesor en commit 68bb6e0; formalizada por el Arquitecto)"
relates_to: [DECISION-0009, DECISION-0096, DECISION-0099, DECISION-0100, DECISION-0101]
---

# DECISION-0103 - Visibilidad del trabajo gobernado

> Redactada por el Asesor a peticion del Operador (19-jul-2026) como
> DRAFT-DECISION-0103 (personal/asesor/, commit 68bb6e0). Firmada TAL CUAL por el
> Operador el 2026-07-19 en orden directa al Arquitecto, que la formaliza aqui.
> La implementacion es trabajo de maker gateado (unidades TASK-0257..TASK-0265).

## Motivo del Operador (registrado con la firma, en sus palabras)

El trabajo gobernado es ATESTADO pero no es VISIBLE. El Operador ve comandos y luego
nada hasta el reporte final. Quiere (a) ver el plan antes de que arranque, (b) saber
a quien se asigna y por que, y (c) que al entregar se reporte contra que se peleo el
agente y como lo resolvio -- eso es la materia prima para crear skills y que el error
no se repita.

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

### Clausula 3-bis - OFERTA DE MEJORA (no automatismo)

Registrar el obstaculo no basta: el reporte debe **cerrar el bucle de aprendizaje**.

- Cuando un obstaculo tenga `recurrence_risk: high`, o cuando el mismo `root_cause`
  aparezca en dos o mas entregas, el reporte **OFRECE al humano** crear/actualizar la
  skill o la regla, **con la propuesta ya redactada** (borrador del cambio concreto, no
  un "convendria mejorar esto").
- **Ofrece, no crea.** La creacion de skills y de reglas es decision humana; ningun
  agente modifica el protocolo ni una skill por su cuenta a partir de un obstaculo.
- El humano puede aceptar, rechazar o parquear; el rechazo tambien queda registrado
  (evita que la misma propuesta se re-ofrezca en bucle en cada entrega).

Racional: el valor no esta en tener la lista de obstaculos, esta en que la lista
**produzca cambios**. Sin esta clausula, `obstacles[]` es un archivo que nadie relee.

### Clausula 4 - DOS CARRILES (o cubre solo una fraccion)

La mayor parte del trabajo NO pasa por el runtime: Arquitecto, Codex por cron y Analista
trabajan en sesion. Por tanto las clausulas 2, 3 y 3-bis se implementan en **ambos**
portadores, con el MISMO bloque `obstacles`:

- carril runtime: campo en `runtime/turn_schema.json` (+ validacion en `turn_validate`);
- carril sesion: mensaje `type: REPORTE` por mailbox, con el bloque en el cuerpo.

**Ambos carriles son exigibles por validador** (verificado 19-jul): `validate_mailbox`
(`scripts/validate_collaboration_state.py:1041`) ya falla en ROJO por estructura de
frontmatter -- coherencia status/carpeta, `response_owner`, `requested_action`, `question`.
Exigir `obstacles` alli es del mismo tipo de regla, no es cuestion de disciplina.

Limite honesto -- **presencia vs veracidad**: el validador puede forzar que el bloque
EXISTA y este bien formado (duro, automatico, ambos carriles); no puede saber si un
agente que peleo lo REPORTO. La diferencia entre carriles es el sensor de friccion:

- runtime: la friccion es mecanicamente detectable (`gate_green: false`, `attempt > 1`,
  revert) -> el validador puede cruzar "gate rojo + obstacles vacio = FAIL".
- sesion: **no existe sensor de friccion**. Por eso esta decision obliga al REPORTE de
  sesion a declarar un contador minimo de friccion (reintentos / rechazos de gate /
  correcciones del checker) que haga cruzable la misma regla. Sin ese contador, la
  completitud del carril sesion queda expuesta y se declara como tal.

### Clausula 5 - ARMAR EL HARNESS (una regla que hay que acordarse de correr no es una regla)

Hallazgo del 19-jul que motiva esta clausula: **el harness existe pero no esta armado**.
`git config core.hooksPath` esta VACIO, `.git/hooks/` no tiene ningun hook activo (solo
`.sample`), y `.githooks/pre-commit` -- aunque se cableara -- **no invoca
`validate_collaboration_state`** (0 hits): solo corre `prune_state --check` y el drift de
la guia HTML. Hoy el validador se ejecuta porque los agentes lo invocan a mano o porque lo
llama el cron.

Por tanto:

1. `core.hooksPath` se cablea a `.githooks/` (hub y export born-operational, mas
   instruccion de cableado en el arranque de cada instancia y cada clone nuevo).
2. `.githooks/pre-commit` invoca `validate_collaboration_state` y **falla el commit** si
   el estado colaborativo esta en rojo.
3. Se declara y se mide el coste: si el validador completo hace el pre-commit demasiado
   lento, se corre en modo acotado a las rutas tocadas -- pero **no se desactiva**.

Racional: las clausulas 1-4 no valen nada si dependen de que alguien se acuerde de correr
el validador. Una regla no exigible es una sugerencia.

### Clausula 6 - ALCANCE

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

| # | unidad | clausula | carril | capability | task |
|---|---|---|---|---|---|
| 1 | cablear `core.hooksPath` a `.githooks/` + `pre-commit` invoca `validate_collaboration_state` y falla en rojo | C5 | harness | implementer | TASK-0257 |
| 2 | anadir bloque `obstacles[]` a `runtime/turn_schema.json` | C3 | runtime | implementer | TASK-0258 |
| 3 | validacion condicional en `turn_validate` (obligatorio si `gate_green:false` / `attempt>1` / revert) | C3 | runtime | implementer | TASK-0259 |
| 4 | vista de plan (`--plan-all` o render de TASK_INDEX) + gate de aprobacion turno 0 | C1 | runtime | implementer | TASK-0260 |
| 5 | `validate_mailbox`: exigir `obstacles` + contador de friccion en `type: REPORTE` | C3/C4 | sesion | implementer | TASK-0261 |
| 6 | plantilla de REPORTE de mailbox con bloque `obstacles` + reporte de asignacion | C2/C4 | sesion | (doc) | TASK-0262 |
| 7 | mecanismo de oferta de mejora (deteccion `recurrence_risk: high` o `root_cause` repetido -> propuesta redactada al humano; registro de rechazos) | C3-bis | ambos | implementer | TASK-0263 |
| 8 | regla de arranque del Asesor: nunca ejecutar sin plan aprobado | C1 | doc | (doc) | TASK-0264 |
| 9 | revision adversarial del conjunto por checker de proveedor diverso | gate | gate | reviewer | TASK-0265 |

**Orden sugerido: la unidad 1 va PRIMERA.** Armar el harness antes de escribir reglas
nuevas garantiza que las reglas nuevas nazcan ya exigidas, y ademas la propia
implementacion de 2-9 queda validada por el hook desde el primer commit.

Nota de secuencia: esta decision deberia ir ANTES del pipeline maker->checker multi-turno.
Multi-turno sin reporte de entrega es exactamente la ceguera que motiva esta decision,
multiplicada por N turnos.

## Paradoja de arranque (declarada honestamente)

Si esta decision se implementa CON el runtime, ese trabajo no puede beneficiarse de la
clausula 1 (el gate de plan aun no existe). Sustituto para esa primera vez: el plan se
presenta a mano y el Operador lo aprueba por mailbox firmado antes del turno 1. A partir
de la segunda vez, el gate es del sistema, no de la buena voluntad de quien presenta.

## Enmiendas (2026-07-19, firma del Operador en orden directa al Arquitecto, con el OK de arranque del plan)

### E1 - Carve-out de remediacion en C1 (resuelve la nota de diseno N1)

Una unidad de remediacion nacida de un rechazo del checker queda cubierta por la
aprobacion original del plan SOLO si conserva el MISMO acceptance, el MISMO scope_routes
y el MISMO risk que la unidad padre, y referencia el id de la unidad padre. Si el risk
sube, se re-aprueba. Racional del Operador: C3 ya da la visibilidad (un rechazo del
checker es friccion, luego obstacles[] es obligatorio y se ve en el reporte de entrega);
el gate de turno 0 no es necesario para enterarse.

### E2 - Gate propio inmediato para la unidad de harness

TASK-0257 se revisa EN CUANTO ATERRIZA, con gate propio (checker de proveedor diverso),
ANTES de arrancar TASK-0258. Motivo: es la unidad de mayor radio de explosion (toca el
pre-commit de todos los agentes); no se construyen ocho unidades encima de un harness
sin revisar.

### E3 - Procedimiento de desarme del hook

TASK-0257 entrega ademas el procedimiento de DESARME: el comando exacto para desconectar
el hook en 30 segundos si bloquea al equipo, documentado en la propia tarea. No debilita
C5: el enforcement duro sigue en CI (el workflow corre validate en cada push y PR, hub e
instancia, desde clon limpio). Es la salida de emergencia.

### E4 - Conjunto adoptable (2026-07-19, firma Operador via MSG-20260719-Operador-to-Arquitecto-ENMIENDA-E4-E5-adoptable-githooks)

`.githooks/**` entra al conjunto adoptable de `upgrade_instance.py` (via
`DEFAULT_ADOPTABLE_GLOBS` o via `upgrade.adoptable_globs` en `protocol.config.json`, lo
que resulte mas limpio). Motivo: sin esto, C5 seria la UNICA clausula de la 0103 que no
viaja a instancias EXISTENTES (NOVA incluida); el resto viaja solo por los globs ya
presentes (scripts/*.py, runtime/**, el workflow de CI). Verificacion: upgrade_instance
contra una instancia real reporta el delta de `.githooks/` como adoptable.

### E5 - Cableado en la instanciacion (misma firma que E4)

`new_instance.py` cablea `core.hooksPath` al instanciar. Copiar `.githooks/` sin
configurar el path deja el hook igual de muerto que estaba en el hub: es el mismo error
que motivo la propia C5, un nivel mas arriba. Verificacion: instancia nueva en sandbox
con `git config core.hooksPath` devolviendo la ruta sin paso manual y prueba negativa
abortando el commit.

Ruteo de E4/E5 (delegado por el Operador al Arquitecto, preferencia declarada por unidad
hermana): **unidad hermana TASK-0266**, para no cargar el fix-loop de TASK-0257 (tope 2
iteraciones) con alcance ajeno a sus defectos; ademas, plegarlas cambiaria el acceptance
de 0257 a mitad de fix-loop, rompiendo la cobertura del carve-out E1 (exige MISMO
acceptance) y forzando re-aprobacion.

### E6 - Reparto de coste del harness (2026-07-20, firma del Operador en orden directa: "acepto tu recomendacion / GO A / luego GO C")

El enforcement de C5 se reparte por capas segun coste medido (serie v1 11.5->42.9s; v2
por materializacion 51.5-53.3s; suelo del validador ~12.5s):

- **A (inmediato)**: en LOCAL el hook corre el modo ACOTADO por defecto (~0.4s) para
  todo commit, incluido el gobernado; el modo COMPLETO local queda disponible solo bajo
  flag explicito (p.ej. pre-push voluntario). El CI conserva la validacion COMPLETA
  desde clon limpio en cada push/PR (ya existente) + el paso de existencia/SHA del hook
  (E4' de la C2 de O1). El CI es el enforcement duro; el hook es la primera linea. El
  riesgo asumido y declarado: ventanas de HEAD rojo transitorio hasta que el CI las
  caza, mitigadas por la disciplina de gates pre-push de los harnesses.
- **C (siguiente)**: unidad de optimizacion que materializa SOLO las rutas que el
  validador lee (no el arbol entero) y mide; si el completo v2 baja a un coste que no
  duele (~15s o menos), el Operador re-decide si reactivar el completo-local con esa
  cifra en la mano. B (completo local a 51s) queda descartado a ese precio.

Implementacion: TASK-0268 (A) y TASK-0269 (C), secuenciadas tras el veredicto de
TASK-0267 (comparten .githooks/pre-commit).

**Criterio EX-ANTE de la re-decision post-C (2026-07-20, firma del Operador en orden
directa: "si sellalo asi"; fijado ANTES de conocer la cifra de C, misma disciplina de
umbrales pre-declarados que este protocolo exige a sus mediciones):**

- Si el modo completo con materializacion parcial (TASK-0269) mide **<= 15s**: se
  REACTIVA el completo-local SOLO para commits que tocan estado/ledger
  (Area_comun/state/**, runtime/state/**), manteniendo el acotado para el resto
  (mailbox y demas rutas gobernadas de alta frecuencia). Reparto HIBRIDO: la garantia
  "nunca se commitea estado roto" donde mas importa, sin gravar cada mensaje. Esta
  reactivacion queda PRE-AUTORIZADA: se ejecuta como ajuste menor del hook contra este
  criterio, sin nuevo gate del Operador.
- Si mide **> 15s**: E6-A queda permanente (acotado local; completo en CI y bajo flag
  voluntario); C se paga igual abaratando el flag y potencialmente el CI.
- La cifra que decide es la del handoff de TASK-0269 verificada por el checker en su
  re-juicio (frio y caliente; decide la CALIENTE por ser la del flujo real). Contexto
  del dato al sellar: v2 actual 45.8-53.3s (maker y checker); suelo del validador
  ~12.5s. La decision se ejecuta contra el umbral SIN re-litigarse.

## Nota de ejecucion de esta primera tanda (orden del Operador, 2026-07-19)

- Ejecucion por el flujo gobernado NORMAL (cron/sesion + submit_intent), NO por el
  runtime orchestrator: el runtime quedo validado end-to-end en instancia scratch pero
  nunca corrio en el hub, y el hub esta vivo y compartido.
- maker = Codex (implementer); checker = proveedor diverso (DECISION-0101).
- Gate de turno 0 A MANO esta primera vez (paradoja de arranque): tabla por mailbox y
  ningun arranque sin OK explicito del Operador.
