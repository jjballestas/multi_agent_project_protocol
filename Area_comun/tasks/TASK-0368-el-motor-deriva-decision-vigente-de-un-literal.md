---
id: TASK-0368
title: El motor deriva "decision vigente" de un literal que este corpus casi no usa, y deja 106 de 110 politicas invisibles
status: in_progress
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
created: 2026-08-12
intake:
  type: fix
  goal: >
    Bloqueante B1 del veredicto formal de TASK-0365. El motor de memoria decide si una decision esta
    vigente comparando su `status` con el literal `"active"` (`policy_row` y `_active_decisions` en
    `scripts/memory/build_memory_db.py`). Este corpus escribe `accepted`: censo medido 104
    `accepted`, 4 `active`, 1 `proposed`, 1 sin campo. Resultado en la DB construida:
    `historical`/`hot_required=0` para 106, `active`/`hot_required=1` para 4 -- y entre las 106
    invisibles estan DECISION-0026 (memoria dorada), 0020 (anti-colision), 0038 (narracion minima),
    0104 (scratch inquebrantable), 0016, 0018 y 0022, todas citadas NOMINALMENTE por AGENTS.md como
    vinculantes hoy, mas DECISION-0081, el `derives_from` de la propia SPEC. Falsado con un mutante
    de UN campo: dos reglas identicas salvo su respaldo, y el gate rechaza solo la respaldada por
    `accepted` (`ERROR: hot/cold rule references an absent or inactive decision: DECISION-0026`).
    Tiene dos caras y solo una es segura: fail-CLOSED para I4 (una regla legitima no puede
    habilitarse) y fail-OPEN para I7 y s.8 Q3 (cuando F2/F3 enciendan el enfriado, casi toda la
    politica vigente sera archivable sin stub y el gate callara). El invariante I7 esta bien escrito:
    se cumple por su LETRA y se rompe por su NOMBRE. La correccion va al MOTOR, no al texto y no al
    corpus.
  acceptance:
    - "AC1 (criterio, no lista de literales): el motor deja de preguntar `status == \"active\"` y pasa
      a preguntar por la PROPIEDAD `esta decision sigue vigente`. Anadir `accepted` junto a `active`
      NO acredita: es la misma lista con un elemento mas, y la siguiente decision escrita con una
      tercera grafia vuelve a romperlo. Se declara el criterio y por que separa vigente de no
      vigente. Dato medido que lo informa: de 110 decisiones, exactamente UNA tiene `superseded_by`
      no vacio (DECISION-0071 -> DECISION-0081)."
    - "AC2 (la superficie es la atestada, no el codigo): el mapeo a estado de politica se expone al
      MISMO mecanismo atestado de `MEMORY_INDEX_POLICY.json` que ya cura los enums de P9 -- hoy esta
      cableado y sin ninguna superficie de configuracion. Se acredita como se acredito P9: editar la
      politica SIN commitear no surte efecto (el motor lee el blob de git)."
    - "AC3 (test de PROPIEDAD, no de conteo): negativo permanente que fije `toda decision que el
      contrato vigente cita como vinculante tiene hot_required=1`, con la poblacion DERIVADA de las
      citas de AGENTS.md y no escrita a mano. Un test que afirme `hot_required=1 para n=110` no
      acredita: pasa por casualidad el dia que el censo coincide y no dice nada el dia que no."
    - "AC4 (superviviencia a la tercera grafia): el test de AC3 sigue vivo si manana una decision
      nace con un `status` que hoy no existe en el corpus. Se acredita introduciendo una y midiendo
      -- si el criterio la clasifica mal, tiene que decirlo RUIDOSAMENTE, no en silencio: la cara
      fail-open es la que este bloqueante existe para cerrar."
    - "AC5 (el positivo de I4 sigue muriendo): una regla que referencia una decision realmente
      ausente o realmente no vigente sigue rechazandose con exit distinto de 0. Se acredita con el
      PAR, repitiendo el mutante de dos reglas del checker: la respaldada por una decision `accepted`
      vigente debe PASAR, y la respaldada por una ausente debe MORIR. Un cambio que arregle la
      primera y ademas deje pasar la segunda no acredita nada."
    - "AC6 (el censo deja de decir 106/4): se reporta el censo de `policy_status` antes y despues,
      derivado de una construccion real de la DB, con las dos direcciones -- ninguna decision pasa a
      vigente sin que el criterio de AC1 lo explique, y ninguna deja de serlo."
  verification_cmd:
    - "python scripts/memory/check_memory_db_drift.py --root . --fast"
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/check_memory_db_drift.py
    - scripts/memory/test_memory_db.py
    - Area_comun/protocol/MEMORY_INDEX_POLICY.json
  out_of_scope:
    - "Renombrar el vocabulario de `status` del corpus de decisiones: contradice la regla del propio
      port (s.16.3, se amplia el conjunto de valores ACEPTADOS, no se reescribe el corpus), reescribe
      104 ficheros para que encajen en el instrumento, y no arregla nada duradero -- la siguiente
      decision escrita con otra grafia vuelve a romperlo. Descartado con razon declarada."
    - "Las tres divergencias entre la s.7 de la SPEC y el motor: son TASK-0369, del lado del TEXTO."
    - "Las 222 aristas `implements` que no resuelven ninguna, el alcance de la deteccion agrupada de
      IBAN y las siglas de id fiscal por lista: residuales censados del mismo veredicto, no
      bloqueantes, con tarea aparte."
  risk: medium
  estimate: M
---

# TASK-0368 -- vigente por nombre, no por literal

## El mutante que lo mato

Dos reglas habilitadas, identicas salvo su respaldo:

    R-ACCEPTED-BACKED  created_by_decision: DECISION-0026   (status: accepted)
    R-ACTIVE-BACKED    created_by_decision: DECISION-0099   (status: active)

    $ python scripts/memory/check_memory_db_drift.py --root . --fast
    ERROR: hot/cold rule references an absent or inactive decision: DECISION-0026
    exit 1

El gate nombra **solo** a DECISION-0026: la regla de memoria dorada que AGENTS.md s.7 cita como
vinculante hoy.

## Por que no es del corpus

Las cuatro decisiones que el motor ve vigentes son 0099, 0100, 0101 y 0103. No son las mas recientes
ni las mas importantes: DECISION-0104 -- la regla de scratch que AGENTS.md s.4 llama inviolable --
esta entre las 106 invisibles. El corpus usa `accepted` y `active` sin distinguirlos; el motor eligio
uno de los dos y se quedo con el 4 por ciento.

Reescribir 104 ficheros para que encajen en la comparacion es rehacer la historia a medida del
instrumento. Es la misma familia de defecto que esta instancia lleva semanas desterrando, y ademas no
dura: basta que la 111 nazca con una tercera grafia.

## Implementacion Codex

El criterio implementado es una propiedad de dos fronteras: una decision sigue vigente mientras no
declare un `superseded_by` no vacio Y no declare un estado de no-vigencia. La politica atestada contiene
el conjunto cerrado `archived/cancelled/draft/proposed/rejected/superseded`; el motor y el gate rapido
consumen la misma funcion. Una grafia futura que no se declare no vigente permanece vigente, mientras
que `proposed` y `superseded` quedan fuera aun sin puntero.

El negativo permanente deriva su poblacion de las citas `DECISION-####` del `AGENTS.md` vivo y copia
esas decisiones reales al corpus de prueba. Ademas mata por separado el mutante literal y el mutante
que solo mira `superseded_by`; prueba una tercera grafia futura, `proposed`, `superseded` sin puntero y
el par completo de I4: respaldo vigente pasa, respaldo ausente, propuesto o retirado muere. Un cambio
no commiteado de la politica sigue sin afectar al blob atestado.

Censo previo re-derivado por el checker desde una construccion real de `94aa4ca3~1`:
`active=4`, `historical=106`, `superseded=0`; `hot_required=1` para 4 y `hot_required=0` para 106.
Censo posterior de la reconstruccion real del candidato de remediacion: `active=108`,
`superseded=2`, `historical=0`; `hot_required=1` para 108 y `hot_required=0` para 2.
DECISION-0071 pasa de `historical` a `superseded` por su puntero a DECISION-0081;
DECISION-0078 pasa de `historical` a `superseded` porque declara `status: proposed`. Las cuatro
decisiones vigentes previas permanecen vigentes.

## Por que no basta con anadir `accepted`

P8 y P9 calibraron los enums de ACEPTACION sacandolos a `MEMORY_INDEX_POLICY.json`, pero `accepted`
ya se indexaba sin problema. Lo que nunca se calibro es el **mapeo a estado de politica**: esta
cableado y no tiene superficie de configuracion. Anadir un literal a una lista deja la lista.
