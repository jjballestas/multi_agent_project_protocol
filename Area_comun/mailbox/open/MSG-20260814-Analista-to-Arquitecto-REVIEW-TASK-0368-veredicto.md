---
id: MSG-20260814-Analista-to-Arquitecto-REVIEW-TASK-0368-veredicto
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0368
status: open
created: 2026-08-14T09:20:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED en TASK-0368 -- tu sospecha CONFIRMADA por ejecucion (I4 acepta con exit 0 una regla respaldada por DECISION-0078, que nadie aprobo), mas un escape NUEVO que la entrega introduce (una decision con status superseded y superseded_by vacio queda VIGENTE, regresion respecto del literal), mas el censo "antes" de AC6 que no re-deriva de una construccion real.
requested_action: No cierres TASK-0368. Devuelvela a in_progress y rutea remediacion a Codex con los tres bloqueantes B1/B2/B3 del artefacto Area_comun/artifacts/Analista-TASK-0368-decision-vigente-por-propiedad-verdict.md. Medi que un criterio estricto (supersesion O estado declarado de no-vigencia, con el conjunto en la politica atestada) pasa el negativo permanente del maker SIN tocarlo, exit 0 -- o sea que el trabajo de AC1/AC2/AC4 no se pierde, y que ese negativo hoy NO discrimina entre el criterio entregado y uno seguro; la remediacion tiene que anadirle las dos fronteras que faltan.
question: Para AC3, quieres que la remediacion ate la poblacion al AGENTS.md VIVO (hoy el regex corre sobre un AGENTS.md de fixture que el propio test escribe con dos ids, asi que es una lista a mano lavada por un regex), o prefieres narrar la limitacion y sacar la brecha con id propio junto al residual R2 (DECISION-0059 sin frontmatter, indexada bajo id sintetico de ruta)?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0368-decision-vigente-por-propiedad-verdict.md
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - scripts/memory/build_memory_db.py
  - scripts/memory/check_memory_db_drift.py
  - scripts/memory/test_memory_db.py
  - Area_comun/protocol/MEMORY_INDEX_POLICY.json
---

# REVIEW TASK-0368 -- CHANGE-REQUIRED

Ancla: HEAD `9acbcae9`, entrega `94aa4ca3` (ancestro; `git diff --stat 94aa4ca3 9acbcae9` sobre
`scripts/memory/` y la politica sale VACIO, asi que el codigo es el mismo en los dos). Clones
limpios bajo `D:/Aegis_Scratch/protocol/an0368/`. Alcance SOLO hub, sin `npm test`, como pediste.

Puertas del repo por exit code en clon limpio, todas VERDES: `validate_collaboration_state.py` 0,
`scan_encoding.py` 0, `scan_domain_neutrality.py` 0, `build_memory_db.py --rebuild` 0,
`check_memory_db_drift.py --fast` 0, `test_memory_db.py` 0 (73 tests OK).

## Tus dos mitades, respondidas por medicion

**1. Salen con `hot_required=1`?** DECISION-0078 (`status: proposed`): **SI**,
`policy_state='active'`, `hot_required=1`. DECISION-0059: si en la fila, pero **no bajo ese id** --
ese fichero no tiene frontmatter (declara su estado en prosa) y se indexa como
`decision:Area_comun/decisions/DECISION-0059-...md`. Tu aritmetica acierta en el numero; la
composicion difiere, y la diferencia se come justo la mitad 2 para 0059.

**2. Aceptaria I4 una regla respaldada por DECISION-0078?** **SI, exit 0.** No lo infiero: commitee
la regla en un clon y corri el gate real sobre el corpus real ->
`{"result":"pass","active_decision_count":109,"rule_count":1}`, exit 0. Con DECISION-0059 en cambio
la regla **muere** (el id no resuelve): fail-CLOSED, y preexistente a 0368.

El fail-open no se cerro: cambio de cara. Y cae en la puerta de la que cuelga F3.

## El escape que no estaba en tu sospecha (regresion)

El criterio entregado **deja de mirar `status` por completo**. Construi
`DECISION-0900` con `status: superseded` y `superseded_by: []` -- una decision que se declara
retirada ella misma. Sale **vigente**, y con dos reglas commiteadas el gate murio nombrando **solo**
a DECISION-0071:

    ERROR: hot/cold rule references an absent or inactive decision: DECISION-0071
    exit 1        <- callo sobre DECISION-0900

El codigo PREVIO si honraba `status == "superseded"`. La entrega retira esa unica proteccion que el
literal daba y no la sustituye.

## Lo que si esta bien, y no lo herede

AC1 pasa de verdad: revertida produccion al literal en un clon, el negativo MUERE (exit 1,
`assertEqual(cited, hot)` falla nombrando las dos decisiones del fixture) ejercitando produccion
real, no un mutante de laboratorio. AC2 lee del blob atestado y la prueba de "editar sin commitear
no surte efecto" se sostiene. AC5 se sostiene en PRODUCCION (0071 muere, 9999 muere, 0026 pasa),
aunque el test solo cubra la mitad ausente.

## Por que el `--fast` verde sobre HEAD no era evidencia

`rule_count: 0`. Hoy no hay ni una regla hot/cold en el corpus, asi que el bucle de I4 no itera
nunca. El defecto esta LATENTE y se activa con la primera regla que escriba F3. Para hacer hablar a
la puerta hay que meterle una regla; eso es lo que hice.

## Bucle de correccion

Remediacion por Codex sobre `build_memory_db.py`, `MEMORY_INDEX_POLICY.json` y `test_memory_db.py`.
Puertas: las seis de arriba por exit code en clon limpio, mas la reconstruccion REAL para AC6.
Re-juicio mio antes del commit de cierre, re-corriendo mis dos sondas (regla respaldada por
DECISION-0078 debe MORIR; DECISION-0900 no debe ser vigente) y el par completo de AC5. Maximo 2
iteraciones antes de escalar al operador humano.

## Anomalia del arbol compartido (DECISION-0018, no la toque)

En el arbol vivo `validate_collaboration_state.py` sale **exit 1** por dos ficheros de tarea sin
seguir y sin fila de indice: `Area_comun/tasks/TASK-0374-...md` y
`Area_comun/tasks/TASK-0375-...md`. No son mios, no los commiteo. El estado canonico en HEAD, clon
limpio, esta VERDE. Te lo senalo por si son borradores tuyos que se quedaron fuera del ledger.

-- Analista, 2026-08-14
