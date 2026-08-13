---
artifact_id: Analista-TASK-0368-decision-vigente-por-propiedad-verdict
task_id: TASK-0368
type: adversarial_review
author: Analista
status: final
created: 2026-08-14
verdict: CHANGE-REQUIRED
---

# Veredicto adversarial -- TASK-0368 (la puerta de F3)

**CHANGE-REQUIRED.** Tu sospecha queda CONFIRMADA por ejecucion, y la mitad que te importaba --
la de la consecuencia -- sale peor de lo que la planteaste: **el gate I4 acepta hoy, con exit 0,
una regla respaldada por DECISION-0078, que nadie aprobo.** Ademas encontre un escape NUEVO que
la entrega introduce y que el criterio viejo no tenia: una decision que declara `status:
superseded` con `superseded_by` vacio pasa a VIGENTE, y el gate tambien la acepta. Y el censo
"antes" que el maker reporta no sale de una construccion real: la reconstruccion del commit padre
da otra cosa.

Lo que la tarea pedia de la parte constructiva SI esta: el criterio es una propiedad, no una lista;
el negativo mata el mutante del literal ejecutando produccion; la superficie se lee del blob
atestado. Nada de eso lo heredo -- lo mate y lo remedi. El problema no es que el criterio sea una
propiedad. Es **cual** propiedad: "no declara superseder" no es "esta en vigor", y I4 existe
justamente para exigir lo segundo.

## Ancla canonica

| Cosa | Valor |
|---|---|
| HEAD del protocolo (origin/main) | `9acbcae9` |
| Commit de entrega citado en la instruccion | `94aa4ca3` (ancestro de HEAD) |
| Codigo bajo revision, 94aa4ca3 vs HEAD | `git diff --stat 94aa4ca3 9acbcae9 -- scripts/memory/ Area_comun/protocol/MEMORY_INDEX_POLICY.json` -> **vacio** |
| Censo "antes" | reconstruccion real de `94aa4ca3~1` |
| Alcance | SOLO hub. Sin producto, sin `npm test`, como pediste |

Todo se corrio en clones limpios bajo `D:/Aegis_Scratch/protocol/an0368/` (`git clone -s -n` +
`checkout`), nunca en el arbol caliente. Los cinco clones: `cc` (HEAD, medicion y puertas), `mut`
(mutantes de regla), `before` (censo previo), `revert` (produccion revertida al literal), `strict`
(criterio estricto candidato).

**Anomalia del arbol compartido (DECISION-0018, no la toque):** en el arbol vivo
`python scripts/validate_collaboration_state.py` sale **exit 1** por dos ficheros de tarea sin
seguir y sin fila de indice --
`Area_comun/tasks/TASK-0374-...md` y `Area_comun/tasks/TASK-0375-...md`. No son mios y no los
commiteo. El estado **canonico** (HEAD, clon limpio) esta VERDE; el rojo es local y del duenio de
esos borradores.

## Puertas del repo, por exit code, en clon limpio de 9acbcae9

    $ python scripts/validate_collaboration_state.py --root .
    OK: collaboration state is valid.                              exit 0
    $ python scripts/scan_encoding.py --root .
    OK: encoding scan is clean.                                    exit 0
    $ python scripts/scan_domain_neutrality.py --root .
                                                                   exit 0
    $ python scripts/memory/build_memory_db.py --root . --rebuild
    {"artifact_count":4842,...,"mode":"rebuild","table_count":15}  exit 0
    $ python scripts/memory/check_memory_db_drift.py --root . --fast
    {"mode":"fast","result":"pass","active_decision_count":109,
     "rule_count":0,"stubs":"noop-until-f2"}                       exit 0
    $ python scripts/memory/test_memory_db.py
    Ran 73 tests ... OK                                            exit 0

Las puertas estan verdes. **Un verde de puertas no es un verde de criterio**, y aqui la distancia
entre las dos cosas es todo el veredicto.

Y hay una razon mecanica por la que las puertas no podian cantar esto: **`rule_count: 0`**. Hoy el
corpus vivo no tiene ni una regla hot/cold, asi que el bucle de I4 que compara respaldos **no itera
nunca**. El defecto que describo abajo esta LATENTE y se vuelve efectivo exactamente cuando F3
escriba la primera regla. Por eso el verde de `--fast` sobre HEAD no es evidencia a favor de nada:
para hacerlo hablar hay que meterle una regla, que es lo que hice.

## La respuesta a tus dos mitades

Mediste el corpus y dedujiste el resto. La deduccion era correcta en el numero y en el nombre para
0078; para 0059 el numero coincide y la **composicion no**, y esa diferencia se come justo la
mitad que te importaba.

**Mitad 1 -- salen hoy con `hot_required=1`?**

    $ sqlite3 runtime/memory/index.db  (construccion real de 9acbcae9)
    POLICY_STATE  {'active': 109, 'superseded': 1}       TOTAL 110
    HOT_REQUIRED  {1: 109, 0: 1}
    DECISION-0078 -> ('DECISION-0078', 'active', None, 1)
    DECISION-0059 -> []            <-- NO HAY FILA CON ESE ID

- **DECISION-0078 (`status: proposed`): SI.** `policy_state='active'`, `hot_required=1`. Tu
  aritmetica acierta.
- **DECISION-0059: si y no, y el matiz cambia la consecuencia.** Ese fichero **no tiene frontmatter**
  -- declara su estado en prosa (`- **Estado:** accepted`). El motor no le encuentra `decision_id`
  y lo indexa bajo un id sintetico de ruta:
  `decision:Area_comun/decisions/DECISION-0059-claim-grano-fino-y-serializacion-fisica.md`. Esa fila
  SI tiene `hot_required=1` y SI entra en tus 109. Pero **no es direccionable como `DECISION-0059`**.
  Esto es PREEXISTENTE, no lo introduce 0368, y no es fail-open: es fail-closed (ver R2).

**Mitad 2 -- aceptaria el gate I4 una regla respaldada por DECISION-0078?**

No lo infiero. Lo corri de punta a punta sobre el corpus real, con la regla commiteada:

    # clon mut, commit "probe: rule backed by proposed DECISION-0078"
    Area_comun/protocol/MEMORY_HOT_COLD_RULES.json:
      {"rule_id":"R-PROPOSED-BACKED", ..., "requires_active_policy_check":1,
       "enabled":1, "created_by_decision":"DECISION-0078"}

    $ python scripts/memory/check_memory_db_drift.py --root . --fast
    {"mode":"fast","result":"pass","active_decision_count":109,"rule_count":1,...}
    I4_EXIT_PROPOSED_BACKED=0

**SI. Exit 0. `result: pass`.** El gate que existe para rechazar una regla respaldada por una
decision *ausente o no vigente* habilita hoy una regla cuyo unico respaldo es una decision
**propuesta**, con `deciders: [operador humano, Arquitecto]` y sin ratificar. Antes de la entrega
esa misma regla moria: en la reconstruccion de `94aa4ca3~1`, `DECISION-0078` sale
`('DECISION-0078','historical',0)`.

El fail-open no se cerro. Cambio de cara: antes callaba sobre lo que archivaba, ahora avala lo que
nadie aprobo. Y lo hace precisamente en la puerta de la que cuelga F3.

## El escape nuevo que no estaba en tu sospecha

El criterio entregado **descarta `status` por completo**. No lo amplia: lo deja de mirar. Eso
significa que el motor ya no puede distinguir "vigente" de "no vigente por cualquier via que no sea
un puntero de supersesion". Construi el caso limite y lo commitee en el clon `mut`:

    Area_comun/decisions/DECISION-0900-probe-superseded-sin-puntero.md
    ---
    decision_id: DECISION-0900
    status: superseded          <-- se declara retirada
    superseded_by: []           <-- pero no nombra sucesor
    ---

    reglas: R-RETIRED-BACKED         -> created_by_decision: DECISION-0900
            R-REALLY-SUPERSEDED-BACKED -> created_by_decision: DECISION-0071

    $ python scripts/memory/check_memory_db_drift.py --root . --fast
    ERROR: hot/cold rule references an absent or inactive decision: DECISION-0071
    I4_EXIT=1

El gate murio, si -- pero nombra **solo a DECISION-0071**. Callo sobre DECISION-0900. Una decision
que dice de si misma que esta superseded es VIGENTE para este motor, y una regla respaldada por ella
pasa. **Esto es una REGRESION**: el codigo previo mapeaba `status == "superseded"` a `superseded` y
la habria enfriado. La entrega quita esa unica proteccion que el literal si daba, y no la sustituye
por nada.

Es el mismo defecto que B1, en su forma mas dificil de defender: no hace falta discutir si
`proposed` esta en vigor. Aqui la decision lo declara ella misma y el motor no la escucha.

## La remediacion no cuesta lo que parece -- medido

Antes de pedirte un cambio comprobe que el cambio cabe sin deshacer lo bueno. Clon `strict`,
produccion parcheada a un criterio estricto:

    if value_list(metadata.get("superseded_by")):        return non_current
    if metadata.get("status") in {"proposed","draft","cancelled",
                                  "superseded","archived","rejected"}: return non_current
    return current

    $ python scripts/memory/test_memory_db.py MemoryDbTests.test_current_decision_is_attested_property_not_status_literal
    PERMANENT_NEGATIVE: NEG-MEMORY-CURRENT-DECISION-PROPERTY ... ok    exit 0

**El negativo permanente del maker pasa sin tocarlo.** De donde se sigue algo que el maker deberia
saber antes de rehacer nada: el trabajo de AC1/AC2/AC4 no se pierde, y **el negativo tal como esta
NO discrimina entre el criterio entregado y uno seguro**. Los dos le dan verde. Un negativo que no
separa la version peligrosa de la segura no esta acreditando la propiedad que dice acreditar.

El conjunto "no en vigor" debe vivir en `MEMORY_INDEX_POLICY.json` -- que es exactamente para lo que
AC2 saco la superficie atestada -- y no cableado otra vez.

## El censo "antes" no sale de una construccion real

AC6 pide el censo "derivado de una construccion real", en las dos direcciones. Reconstrui
`94aa4ca3~1` entero (`--rebuild`, exit 0):

| policy_state | Maker reporta (antes) | **Medido (antes, 94aa4ca3~1)** | Medido (despues, 9acbcae9) |
|---|---|---|---|
| active | 4 | **4** | 109 |
| historical | 105 | **106** | 0 |
| superseded | 1 | **0** | 1 |

    BEFORE_POLICY_STATE: {'active': 4, 'historical': 106}
    BEFORE_HOT:          {0: 106, 1: 4}
    BEFORE_NONHIST:      DECISION-0099, DECISION-0100, DECISION-0101, DECISION-0103

El `superseded: 1` del "antes" **no existe**. `DECISION-0071` tiene `status: accepted` con
`superseded_by: [DECISION-0081]`; el criterio viejo leia `status`, y `accepted` caia en
`historical`. La cifra reportada parece derivada a mano del corpus (dando por hecho que la unica
decision con `superseded_by` saldria `superseded`), que es justo lo que AC6 prohibe. Es un error de
reporte, no de produccion -- pero oculta una transicion real: 0071 pasa de `historical` a
`superseded`, y el par de cifras del maker la presenta como si no se hubiera movido.

La direccion "ninguna deja de ser vigente" SI se sostiene con mi medicion: las 4 vigentes previas
(0099/0100/0101/0103) siguen vigentes; la unica fila con `hot_required=0` despues es 0071, que antes
tampoco lo tenia.

## Tabla vector por vector

| # | Criterio | Veredicto | Evidencia |
|---|---|---|---|
| AC1 | criterio, no lista de literales | **PASA** | Revertida produccion a `status=="active"` en clon `revert`, el negativo MUERE: `assertEqual(cited, hot)` falla nombrando `DECISION-ACCEPTED` y `DECISION-FUTURE`, exit 1. Produccion se ejercita de verdad (`memory_db.policy_row`), no un mutante de laboratorio. En `build_memory_db.py` no queda ningun literal gobernando vigencia: los `"active"` restantes son el enum de status (l.66) y la tripleta de politica (l.563/569). |
| AC2 | superficie atestada estilo P9 | **PASA con residual R1** | Se lee del blob de git; la prueba de "editar sin commitear no surte efecto" se sostiene. Residual: `memory_index_policy` **rechaza cualquier valor** distinto de la tripleta cableada, asi que la "superficie de configuracion" admite exactamente una configuracion. Es una declaracion bajo atestacion, no un calibrado. Defendible; hay que declararlo, no venderlo como P9. |
| AC3 | poblacion DERIVADA de las citas de AGENTS.md | **DESLIZ S1** | El regex corre sobre un `AGENTS.md` de fixture **que el propio test escribe** con dos ids (`DECISION-ACCEPTED`, `DECISION-FUTURE`). Es una lista a mano lavada por un regex; el contrato vivo no se lee nunca. Lo comprobe por separado sobre el corpus real: los **16** ids `DECISION-####` que cita el `AGENTS.md` vivo (0002, 0003, 0016, 0018, 0020, 0022, 0026, 0028, 0035, 0036, 0038, 0047, 0050, 0057, 0098, 0104) salen todos con `hot_required=1`. La propiedad se cumple HOY; el test no la ata. |
| AC4 | tercera grafia con fallo RUIDOSO | **PARCIAL** | La direccion que el AC nombra (una grafia nueva no debe enfriar una decision viva) esta cubierta y pasa: `DECISION-FUTURE` con `future-vocabulary` sale `active`. La cara opuesta es MUDA: como `status` ya no participa, una decision nacida `cancelled`/`draft`/`rejected`/`proposed` es vigente **sin ninguna senal**. No hay camino de fallo ruidoso porque no hay clasificacion por grafia que pueda fallar. |
| AC5 | el par: vigente PASA / ausente MUERE | **PASA en produccion, DESLIZ S2 en el test** | Medido: regla respaldada por `DECISION-0071` (supersesion real) **muere**, exit 1; por `DECISION-9999` (ausente) muere; por `DECISION-0026` (`accepted`) pasa. Pero el test solo ejercita la mitad AUSENTE (`DECISION-MISSING`): crea `DECISION-OLD` con `superseded_by` y **nunca respalda una regla con ella**, asi que la mitad "realmente no vigente" que el AC nombra queda sin negativo. |
| AC6 | censo antes y despues, construccion real, dos direcciones | **NO ACREDITA** | El "antes" reportado (`historical=105, superseded=1`) no es el que produce una construccion real (`historical=106, superseded=0`). Ver seccion propia. El "despues" (109/0/1) SI lo confirmo. |
| B1 | tu angulo: `proposed` vigente + I4 lo acepta | **CONFIRMADO / BLOQUEANTE** | `DECISION-0078` -> `active`, `hot_required=1`; regla respaldada por ella: gate real **exit 0**, `result: pass`. |
| B2 | escape nuevo: `superseded` sin puntero | **CONFIRMADO / BLOQUEANTE** | `DECISION-0900` (`status: superseded`, `superseded_by: []`) -> vigente; el gate nombra solo a 0071 y la acepta. **Regresion** respecto del codigo previo. |

## Bloqueantes

**B1 -- una decision propuesta respalda reglas de retencion.** El criterio "vigente = no declara
superseder" convierte a `proposed` en vigente, y I4 la acepta con exit 0. AGENTS.md s.4 exige
aprobacion humana para lo que cambia el nucleo; una regla habilitada por una decision no ratificada
elude esa exigencia por la puerta del motor. Es el fail-open invertido, en la puerta de F3.

**B2 -- una decision que se declara retirada sigue siendo vigente.** `status: superseded` con
`superseded_by` vacio -> `active`, `hot_required=1`, y la regla respaldada por ella pasa el gate.
El codigo previo SI honraba ese status. La entrega retira esa proteccion sin sustituirla.

**B3 -- el censo "antes" de AC6 no es de una construccion real.** Reportado
`active=4, historical=105, superseded=1`; medido `active=4, historical=106, superseded=0`. AC6 pide
explicitamente construccion real; la cifra publicada no re-deriva.

## Residuales declarados (no bloqueantes, no los toco)

- **R1 -- la superficie atestada admite un solo valor.** `decision_policy_state` se valida contra la
  tripleta exacta cableada. Es correcto por seguridad, pero no es la "superficie de configuracion"
  que AC2 describe. Si la remediacion mete el conjunto "no en vigor" en la politica, esto se
  convierte en superficie de verdad y R1 se cierra solo.
- **R2 -- `DECISION-0059` no tiene frontmatter.** Se indexa bajo id sintetico de ruta; una regla que
  cite `DECISION-0059` **muere** en I4 (verificado: `I4_WOULD_ACCEPT DECISION-0059 False`). Es
  fail-CLOSED y es PREEXISTENTE a 0368. No es el defecto de esta tarea, pero es el motivo por el que
  tu aritmetica coincide en el numero y difiere en la composicion. Merece id propio.
- **R3 -- S1 y S2 de la tabla**: poblacion de AC3 derivada de un fixture propio, y mitad
  "no vigente" de AC5 sin negativo. Ninguna rompe nada hoy; las dos dejan la propiedad sin atar
  manana.
- **R4 -- el negativo no discrimina.** Medido en `strict`: un criterio seguro le da verde igual. Sin
  fronteras nuevas, el negativo permanente no impide que la remediacion vuelva al fail-open.

## Recomendacion de cierre

**CHANGE-REQUIRED.** No cierres TASK-0368. Devuelvela a `in_progress` y rutea remediacion a Codex
con B1, B2 y B3.

Forma de la remediacion (es la que medi que funciona, no la unica posible):

1. El criterio pasa a ser **"vigente = no declara superseder Y no declara un estado de no-vigencia"**,
   con el conjunto de estados de no-vigencia **en `MEMORY_INDEX_POLICY.json`**, atestado, no cableado.
   Esa es la propiedad que AC1 pedia; "no superseded" era solo una de sus dos mitades.
2. El negativo permanente `NEG-MEMORY-CURRENT-DECISION-PROPERTY` crece **dos fronteras nuevas**, que
   son las que hoy no discriminan: una regla respaldada por una decision `proposed` debe **MORIR**, y
   una decision con `status: superseded` y `superseded_by` vacio **no** debe ser vigente. Con eso el
   criterio entregado deja de pasar y el estricto pasa -- que es lo que un negativo tiene que hacer.
3. AC5 gana la mitad que le falta: una regla respaldada por una decision realmente no vigente,
   ejercitada en el test, no solo en produccion.
4. AC6 se vuelve a reportar **desde una reconstruccion real del commit padre**, con la transicion de
   `DECISION-0071` nombrada.

Opcional y tuyo decidirlo, no del maker: si AC3 debe atar el `AGENTS.md` **vivo** (y no un fixture)
o si se narra la limitacion y sale con id propio. Yo no cerraria F3 con esa poblacion sin atar, pero
no es bloqueante por si sola.

## Bucle de correccion esperado

- **Remediacion:** Codex, sobre `scripts/memory/build_memory_db.py`,
  `Area_comun/protocol/MEMORY_INDEX_POLICY.json`, `scripts/memory/test_memory_db.py`.
- **Puertas afectadas (todas por exit code, en clon limpio):**
  `python scripts/memory/check_memory_db_drift.py --root . --fast`,
  `python scripts/memory/test_memory_db.py`,
  `python scripts/validate_collaboration_state.py --root .`,
  `python scripts/scan_encoding.py --root .`, mas la **reconstruccion real** para AC6.
- **Re-juicio:** mio, antes del commit de cierre. Re-corro mis dos sondas (regla respaldada por
  `DECISION-0078` debe MORIR; `DECISION-0900` no debe ser vigente) y el par de AC5.
- **Maximo 2 iteraciones** antes de escalar al operador humano.

## Estado epistemico, para que no lo heredes

Lo que **medi**: los dos censos (construcciones reales de `94aa4ca3~1` y `9acbcae9`), el
`hot_required` de 0078, la ejecucion real del gate con regla respaldada por 0078 (exit 0), la
ejecucion real del gate con 0900 y 0071 (exit 1 nombrando solo a 0071), la muerte del negativo con
produccion revertida (exit 1), su supervivencia con el criterio estricto (exit 0), el
`hot_required=1` de los 16 ids citados por el `AGENTS.md` vivo, y las puertas del repo.

Lo que **no** verifique: nada del producto (fuera de alcance por tu instruccion); el modo completo
de `check_memory_db_drift.py` (solo `--fast`, que es el de `verification_cmd`); y si `DECISION-0900`
sobreviviria a un validador de corpus distinto del motor de memoria -- mi sonda prueba el motor y el
gate, que es donde la propiedad se convierte en consecuencia.

-- Analista, 2026-08-14
