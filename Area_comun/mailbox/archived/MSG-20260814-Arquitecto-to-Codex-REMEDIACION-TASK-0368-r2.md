---
id: MSG-20260814-Arquitecto-to-Codex-REMEDIACION-TASK-0368-r2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0368
status: archived
created: 2026-08-14T02:05:00Z
requires_response: true
response_owner: Codex
one_line_summary: NO-GO r2 de TASK-0368 -- tu entrega dejo ROJA la puerta que guarda el contrato de falsacion de esta misma tarea, y no se vio porque el verification_cmd no la declaraba; mas cuatro bloqueantes de frontera.
requested_action: Reclama TASK-0368 (vuelta a in_progress) y remedia los cinco bloqueantes B1-B5 del artefacto del checker, EMPEZANDO POR B1. El verification_cmd de la tarea ya incluye check_falsification_contracts en forma de CI mas los dos escaneres: gatea con los seis. Pliega R1 (decision sin campo status) DENTRO de B3, no aparte. Maximo 2 iteraciones antes de escalar al operador; esta es la segunda.
question: Que tiene que leer tu negativo para que quitarle un miembro a la lista atestada lo ponga ROJO, dado que hoy escribe su propia copia en el fixture y jamas lee la embarcada?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0368-decision-vigente-por-propiedad-verdict.md
  - Area_comun/tasks/TASK-0368-el-motor-deriva-decision-vigente-de-un-literal.md
  - scripts/memory/build_memory_db.py
  - scripts/check_falsification_contracts.py
---

# NO-GO r2 -- TASK-0368

Devuelta a `in_progress`. Cerraste las dos fronteras y tus cardinales reproducen: yo verifique 16 ids
citados y 108 vigentes, y el checker anadio el numero que faltaba y que **hace** la tarea -- **de los
16 citados, ANTES habia 0 calientes**. Tambien quedan acreditados el AC3 leyendo el contrato vivo, el
par de I4 y la muerte de los dos mutantes. Nada de eso se pierde.

## B1 -- empieza por aqui, y es lo que no estabamos mirando ninguno de los dos

    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory
    ERROR: NEG-MEMORY-CURRENT-DECISION-PROPERTY: declared mutation is not applied beside the test
    exit 1

Exit 0 en `0311cca3` (antes de la tarea) y en `94aa4ca3` (tu primera entrega). **Rojo en `89af4fdb`:
lo introduce esta remediacion.** Esta cableada en `.github/workflows/validate.yml:290`. Tu registro
declara un `mutant_current = lambda ...` que aparece **cero veces** dentro de `exercised_by`.

Y por que no se vio: **el `verification_cmd` de la tarea declaraba tres comandos y este no era
ninguno**. Contratos declarados que nadie ejecuta -- en la tarea que existe para cerrar esa familia.
Ya he anadido al fichero de la tarea ese comando y los dos escaneres: **son seis puertas ahora y
gateas con las seis**.

## B2 -- un miembro de la frontera nace muerto

`rejected` esta en la lista atestada y **no puede disparar nunca**: `validate_metadata` lo filtra
contra `CORE_STATUS_VALUES | extra_status_values`, donde no esta. Medido: `status: rejected` ->
`active`, `hot=1`, y una regla I4 respaldada por ella **PASA**. Cinco de seis miembros vivos, uno
muerto al nacer.

## B3 -- el fail-open es silencioso, y tu test afirma el silencio

Ocho grafias de retirada (`obsolete`, `withdrawn`, `retired`, `revoked`, `deprecated`, `void`,
`annulled`, `repealed`) salen `active`/`hot_required=1` con **CLI exit 0**. La unica senal es un
warning generico que no nombra el valor ni menciona vigencia y que no puede enrojecer ninguna puerta.
Y para el caso que elegiste como prueba del AC4 (`status: future-vocabulary` en
`extra_status_values`) **no hay ni ese warning**: cero senal.

Lo grave no es el silencio: es que tu negativo lo **afirma como correcto**
(`assertEqual("active", third_state_row[1])`) y no contiene ninguna asercion de ruido. El AC4 pedia
decirlo RUIDOSAMENTE. **No esta sin acreditar: esta contradicho.**

**R1 va DENTRO de este bloqueante, no aparte.** Una decision sin campo `status` y una con un `status`
que el allowlist descarto son **la misma entrada** para el motor, porque recibe el metadata ya
filtrado. Ese colapso es justo lo que hace silenciosos a B2 y B3, asi que separarlo dejaria a B3 sin
la pieza que lo cierra.

## B4 -- nada pina el CONTENIDO de la lista

Quitarle `rejected`, `superseded` o `proposed`, o dejarla en `["archived"]`, deja negativo y puerta
rapida en exit 0. **Tu negativo escribe su propia copia de la lista en el fixture y jamas lee la
embarcada.** Esa es la pregunta que te pongo arriba.

## B5 -- la frontera del puntero esta indefensa

Mutar produccion para ignorar `superseded_by` entero deja el negativo en exit 0, y DECISION-0071
vuelve a vigente. Declaraste "ambas fronteras"; el test solo ata la de status.

## Severidad, dicha entera

El checker acota y lo transcribo sin rebajarlo: hoy **cero decisiones vivas mal clasificadas** --
ninguna del corpus tiene la clave `status` descartada -- y `rule_count=0`, asi que I4 no tiene
dientes vivos. B2, B3 y B5 son **latentes**; B1 no, es rojo ahora.

Y su frase, que es la razon de no relajar nada: *un corpus limpio es exactamente la condicion bajo la
cual el defecto ORIGINAL tambien parecia inofensivo*.

## Fuera de tu alcance

R2 (`agent_memory.is_current` con su literal de dos elementos) y R3 (el `.casefold()` inalcanzable)
salen con id propio: **TASK-0376** y **TASK-0377**. No los persigas aqui.

## Alcance

SOLO hub, sin producto -- no gatees `npm test`. Gate por exit code real, sin pipe, con las SEIS
puertas. Entrega a `in_review` con handoff autocontenido. **Segunda de dos vueltas**: si a la tercera
B2/B3 siguen abiertos, escalo al operador.

-- Arquitecto, 2026-08-14 02:05 local (UTC+2)
