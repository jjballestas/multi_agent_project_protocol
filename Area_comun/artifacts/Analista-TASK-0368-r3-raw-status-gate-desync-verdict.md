---
artifact_id: Analista-TASK-0368-r3-raw-status-gate-desync-verdict
task_id: TASK-0368
type: adversarial_review
author: Analista
status: final
created: 2026-08-14
verdict: CHANGE-REQUIRED
---

# Veredicto adversarial -- TASK-0368 remediacion 3 (leer el status crudo)

**CHANGE-REQUIRED.** Un bloqueante nuevo, introducido por el fix 1.

Empiezo por tu pregunta, porque la respuesta tiene dos mitades y la segunda es el veredicto.

**Mitad buena, y la verifique, no la herede.** Leer el `status` crudo aguas arriba del allowlist **no
admite nada**. El valor crudo se consume SOLO en la comparacion de la puerta y se tira: los cinco
sitios que escriben la columna `status` en la DB siguen leyendo `metadata.get("status")`, o sea el
valor ya filtrado (`build_memory_db.py:1348, 1387, 1405`, y `decision_policy_state` en `1192`). Medi
la familia entera que te preocupaba -- PII, longitud, inyeccion, formas raras -- y ninguna entra:

    caso                          puerta        policy_state   valor almacenado
    PII email en status           warn-missing  active         None
    PII IBAN en status            warn-missing  active         None
    status de 2000 caracteres     RAISE         --             None
    inyeccion con salto de linea  RAISE         --             None
    inyeccion SQL                 RAISE         --             None
    cadena vacia                  RAISE         --             None
    homoglifo unicode invisible   RAISE         --             None

La afirmacion del maker -- *"structural PII status rejection remains green"* -- es **cierta**, y la
doy por verificada: `contains_pii(raw_status, ..., coordinate="status")` se evalua ANTES de aceptar
el crudo, y si dispara, el valor cae al camino filtrado. No cambiamos un fail-open de vocabulario por
una entrada sin filtrar. Esa sospecha tuya queda descartada por medicion.

**Mitad mala, y es un bloqueante.** El fix no admite contenido nuevo; lo que hace es **desincronizar
la puerta del clasificador**. Desde r3 los dos miran valores distintos con reglas distintas:

    puerta (load_artifacts:971-982)   valor CRUDO   +  casefold  +  pertenencia a `classified`
    clasificador (decision_policy_state)  valor del ALLOWLIST  +  igualdad EXACTA (`value in status_values`)

Todo lo que caiga en la grieta entre esas dos reglas **pasa la puerta en silencio y aterriza como
vigente**. La grieta tiene habitantes obvios: las variantes de mayusculas de los seis estados no
vigentes. `Superseded`, `Proposed`, `REJECTED`, `Archived`, `Cancelled`, `Draft`. Su `casefold()`
esta en `classified`, asi que la puerta no levanta el `raise`; y su forma exacta no esta en
`status_values`, asi que el allowlist la descarta y el clasificador recibe `None` y devuelve
`mapping["current"]`.

Y aqui esta lo que convierte esto en regresion y no en un residual heredado: **antes de r3 esa misma
entrada emitia el aviso explicito de vigencia. Ahora no emite ninguno.** El fix 1 se llevo por
delante la unica huella que tenia esa familia.

---

## 1. Ancla canonica y reproduccion

| Elemento | Valor |
|---|---|
| Commit bajo revision | `4b7d42b6fc1884498526246f64923964eef1711c` |
| HEAD del protocolo al revisar | `bb7cf203` (origin/main) |
| Linea base para medir las dos direcciones | `7980bfcd` (pre-r3) |
| Alcance | SOLO hub (protocolo). Sin producto: no gateo `npm test`. |
| Clon limpio | `git clone -s -n <repo> <dst> && git checkout 4b7d42b6` |
| Raiz de scratch | `D:/Aegis_Scratch/mapp/` (DECISION-0104) |
| Hora | 2026-08-14 12:02 local (UTC+2) |

### Las SEIS puertas del `verification_cmd`, por exit code, en clon limpio

| # | Comando | Exit |
|---|---|---|
| 1 | `python scripts/memory/check_memory_db_drift.py --root . --fast` | **0** |
| 2 | `python scripts/memory/test_memory_db.py` | **0** |
| 3 | `python scripts/validate_collaboration_state.py --root .` | **0** |
| 4 | `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` | **0** |
| 5 | `python scripts/scan_encoding.py --root .` | **0** |
| 6 | `python scripts/scan_domain_neutrality.py --root .` | **0** |

Seis de seis en verde. La puerta 4 declara `NEG-MEMORY-CURRENT-DECISION-PROPERTY boundaries=10`,
igual que la vuelta pasada.

Censo re-derivado por mi con las funciones de produccion sobre `4b7d42b6`: **112 ficheros de
decision, `active=110`, `superseded=2`**, un unico aviso de vigencia (DECISION-0059, la que no
declara `status`) entre 231 avisos totales. Coherente con lo que declara la tarea una vez sumadas
DECISION-0113 y 0114.

---

## 2. Tus tres criterios de mi seccion 6 de r2: los TRES estan cerrados

Los ejecute yo, sobre PRODUCCION, contra el runner declarado
(`test_current_decision_is_attested_property_not_status_literal`).

| Mutante sobre produccion | Exit | Resultado |
|---|---|---|
| M0 control, sin mutar | 0 | verde |
| M1 clase de estado ignorada (motor pointer-only) | **1** | MUERE |
| **M2 puntero de supersesion ignorado** (quitar `value_list(metadata.get("superseded_by")) or`) | **1** | **MUERE** |
| M3 vocabulario no clasificado aceptado en silencio (`raise` de `decision_policy_state`) | 0 | SOBREVIVE (ver 4.1) |
| **M7 ausente pasa a NO vigente** | **1** | **MUERE** |
| **M8 `raise` del fix 1 neutralizado en `load_artifacts`** | **1** | **MUERE** |

- **Mi criterio 1 (3.1 de r2) -- CERRADO.** La prueba de aceptacion que declare era el probe e2e
  sobre el corpus real. Ejecutado: anado `Area_comun/decisions/DECISION-9999-probe-retired.md` con
  `status: retired`, lo commiteo, y

      python scripts/memory/check_memory_db_drift.py --root . --fast   exit 1
      ERROR: Area_comun/decisions/DECISION-9999-probe-retired.md: decision currentness status
             'retired' is not classified by Area_comun/protocol/MEMORY_INDEX_POLICY.json

  Ruta y valor, como pedia. La familia de vocabulario **no registrado en ninguna superficie** ya no
  pasa: `retired`, `obsolete`, `withdrawn` -- las tres mueren donde antes entraban calientes.

- **Mi criterio 2 (3.2 de r2) -- CERRADO, y no es una tautologia nueva.** M2 muere en
  `test_memory_db.py:3109`, `self.assertEqual("superseded", rows["DECISION-OLD"][1])`, con
  `'superseded' != 'active'`. La fixture es la correcta: `DECISION-OLD` lleva `status: accepted`
  (vigente por estado) **y** `superseded_by: DECISION-ACCEPTED` (no vigente por puntero), asi que la
  unica cosa que puede sostener el aserto es que produccion mire el puntero. Los dos lados salen de
  `rows`, la misma poblacion. El aserto de union (`production_hot | {"DECISION-OLD"}`, linea 3114) es
  un segundo guardian redundante pero tambien discriminante: si el mutante mete `DECISION-OLD` en
  `production_hot`, la union deja de diferir y el `assertNotEqual` cae. Miraste bien: pedir que sea
  la misma poblacion era lo que faltaba, y esta.

- **Mi criterio 3 (3.3 de r2) -- CERRADO por conducta.** M7 muere. `missing_status` ya se
  desreferencia y la fixture `DECISION-MISSING-STATUS` lo fija con
  `assertEqual("active", rows["DECISION-MISSING-STATUS"][1])`.

Tenias razon en que los dos mutantes de produccion en exit 1 eran la diferencia entre una puerta y
un adorno. Lo son, y cambian de signo de verdad.

---

## 3. El bloqueante nuevo: la grieta entre la puerta y el clasificador

### 3.1 Mecanismo

`load_artifacts:971-982` decide con el crudo y `casefold()`; `validate_metadata:860` acepta con
`value in status_values`, igualdad **exacta**. Simulacion con las funciones de produccion y la
politica atestada real:

    grafia cruda    puerta    policy_state   avisos emitidos
    superseded      silent    superseded     []
    proposed        silent    superseded     []
    Superseded      silent    active         ['rejected frontmatter key status']
    SUPERSEDED      silent    active         ['rejected frontmatter key status']
    Proposed        silent    active         ['rejected frontmatter key status']
    REJECTED        silent    active         ['rejected frontmatter key status']
    Archived        silent    active         ['rejected frontmatter key status']
    Cancelled       silent    active         ['rejected frontmatter key status']
    Draft           silent    active         ['rejected frontmatter key status']
    sUpErSeDeD      silent    active         ['rejected frontmatter key status']

`silent` significa literalmente eso: ni `raise`, ni el aviso de vigencia. El unico rastro es el aviso
generico de allowlist, que dice "rejected frontmatter key status" y **no menciona la vigencia**; hay
231 avisos en el corpus real y ese canal ya es ruido de fondo.

### 3.2 Las dos direcciones, medidas contra la linea base

Corri la MISMA simulacion contra `7980bfcd` (pre-r3), cambiando solo el bloque que r3 toca:

    grafia          pre-r3 (7980bfcd)                       r3 (4b7d42b6)
    retired         warn-missing -> active   (fuga)         RAISE            <- GANADO
    obsolete        warn-missing -> active   (fuga)         RAISE            <- GANADO
    withdrawn       warn-missing -> active   (fuga)         RAISE            <- GANADO
    Superseded      warn-missing -> active   (avisado)      silent -> active <- PERDIDO
    Proposed        warn-missing -> active   (avisado)      silent -> active <- PERDIDO
    REJECTED        warn-missing -> active   (avisado)      silent -> active <- PERDIDO

r3 gana la familia no registrada y **pierde la senal** de la familia registrada-en-otra-caja. El
`elif` nuevo se come el `if status is None` para exactamente esas entradas. Esto no es un residual
heredado: es una senal que existia el 13 de agosto y no existe el 14.

### 3.3 Extremo a extremo sobre el corpus real, con un solo caracter

No uso fixture. Sobre el clon limpio de `4b7d42b6`, cambio **una letra** en un fichero real:
`Area_comun/decisions/DECISION-0078-medicion-peones-ab-c-sandbox.md`, `status: proposed` ->
`status: Proposed`, y lo commiteo con su trailer:

    antes:   check_memory_db_drift --fast   exit 0   active_decision_count = 110
    despues: check_memory_db_drift --fast   exit 0   active_decision_count = 111
             validate_collaboration_state    exit 0   OK: collaboration state is valid.
             scan_encoding                   exit 0
    unico rastro:
      Area_comun/decisions/DECISION-0078-...: rejected frontmatter key status

Una decision `proposed` -- no vigente por la politica atestada, y no vigente por su propia letra --
pasa a **vigente y caliente** por escribirse con mayuscula inicial, con las puertas protocolares en
verde y sin un solo aviso de vigencia.

### 3.4 Por que lo cuento como bloqueante y no como residual

Por el AC4 de la propia tarea, no por una regla mia: *"si el criterio la clasifica mal, tiene que
decirlo RUIDOSAMENTE, no en silencio: la cara fail-open es la que este bloqueante existe para
cerrar"*. `Proposed` con mayuscula es una grafia que **hoy no existe en el corpus** (las 112 estan en
minuscula), el criterio la clasifica mal, y lo hace en silencio. Es la letra del AC4.

Y es la forma del defecto original una vuelta mas: el instrumento decide por pertenencia a un
conjunto, y lo que el conjunto no contiene entra por la puerta buena. r1 fallaba con el literal
`active`; r2 con el vocabulario no registrado; r3 con la caja de las letras. Cada vuelta estrecha el
dano sin cambiar la clase. Lo digo sin dramatizar: **el criterio de AC1 sigue siendo el correcto y
sigue bien implementado**; lo que falla es, otra vez, la frontera por donde entra el vocabulario.

---

## 4. Tabla vector por vector

| Vector | Lo que declara la entrega | Veredicto | Evidencia |
|---|---|---|---|
| **Fix 1** cierra la fuga de vocabulario no registrado | fixture e2e con `retired` falla con ruta y valor | **PASS** | probe e2e sobre corpus real: exit 1 con ruta y valor; M8 mata al mutante que neutraliza el `raise` |
| **Fix 1** no admite nada por saltar el allowlist | (implicito) | **PASS** | PII/longitud/inyeccion/vacio/homoglifo: ninguno se almacena; los 5 escritores de la columna usan `metadata` |
| **Fix 1** variantes de caja | no declarado | **SLIP -- BLOQUEANTE** | `Proposed` -> `active`, silencioso; e2e sobre DECISION-0078 real: 110 -> 111 activas, seis puertas verdes |
| **Fix 1** senal preexistente conservada | no declarado | **SLIP -- REGRESION** | pre-r3 emitia el aviso de vigencia para esa familia; r3 no emite ninguno |
| **Fix 2** puntero, misma poblacion | quitar el termino pone el runner en exit 1 | **PASS** | M2 exit 1 en `test_memory_db.py:3109`; fixture `DECISION-OLD` = accepted + superseded_by |
| **Fix 3** `missing_status` desreferenciado | invertir la conducta pone el runner en exit 1 | **PASS** | M7 exit 1 |
| **AC1** criterio, no lista | no se toco | **PASS** | intacto; sigue siendo la propiedad correcta |
| **AC5** el positivo de I4 sigue muriendo | -- | **PASS** | boundary `assertRaisesRegex(ValueError, "absent or inactive")` viva; M1 exit 1 |
| **AC6** censo | 110/2 | **PASS** | re-derivado por mi: 112 ficheros, active=110, superseded=2 |

---

## 5. Residuales declarados (no bloqueantes, no los cuento en el veredicto)

- **M3 sobrevive: guardian muerto.** El `raise` interno de `decision_policy_state`
  (`build_memory_db.py:1199`) ya no lo mata nadie, porque el `raise` del fix 1 dispara antes en los
  dos unicos llamantes (`policy_row:1217` y `check_memory_db_drift.py:34`), que le pasan
  `artifact.metadata` post-`load_artifacts`. Defensa en profundidad que dejo de ser falsable. No es
  fail-open; lo anoto para que nadie lo cuente como puerta.
- **El inventario declarado sigue nombrando la tautologia de r2.** `boundaries=10` no cambio, y entre
  esos diez sigue estando `self.assertNotEqual(hot, mutant_hot)`, el aserto de poblaciones distintas
  que documente en r2 seccion 3.2. Los dos asertos que de verdad matan a M2 -- `assertEqual("superseded",
  rows["DECISION-OLD"][1])` y el de la union -- **no estan declarados**. La conducta esta defendida;
  la DECLARACION esta obsoleta. Tenias razon en no fiarte de la cuenta: los diez de hoy no son los
  diez que defienden. Corregirlo es gratis y va en la misma vuelta.
- **`status` no-cadena** (`status: 2026`, `status: [superseded]`, `status: {}`, booleano de YAML):
  cae al camino filtrado, produce el aviso de vigencia y clasifica como `active`. Fail-open **con
  aviso**, identico a pre-r3. No lo introduce r3 y no lo cuento aqui.
- **`build_memory_db.py:1405`**: `int(metadata.get("status") not in {"superseded", "archived"})`
  deriva vigencia de dos literales cableados para las filas de `agent_memory`. Es la misma familia de
  defecto que TASK-0368, pero sobre otro tipo de artefacto y fuera del `scope_routes` declarado.
  Tarea aparte; no lo meto en este veredicto.
- 231 avisos en el corpus real. Cualquier senal nueva por ese canal nace enterrada.
- No corri `check_memory_db_drift --full`: no esta en el `verification_cmd` de la tarea.

---

## 6. Veredicto y lazo de correccion

**CHANGE-REQUIRED.** Un bloqueante (3.x). Los tres que abri en r2 estan cerrados y verificados por mi.

Lo que aceptaria como cerrado, por conducta y no por forma:

1. **La puerta y el clasificador deben juzgar el MISMO valor con la MISMA regla.** El mecanismo es
   del maker -- normalizar una sola vez y que las dos superficies consuman esa normalizacion es lo
   evidente, pero no me corresponde disenarlo. Lo que no acepto es una lista de variantes de caja
   anadida al allowlist: es la misma lista con mas elementos, y la siguiente decision escrita
   `SuperSeded ` con un espacio vuelve a romperlo.
   **Prueba de aceptacion:** el probe de 3.3 -- cambiar `status: proposed` a `status: Proposed` en un
   fichero real de decision -- debe poner en exit distinto de 0 alguna de las seis puertas, y en
   ningun caso incrementar `active_decision_count` en silencio.
2. **La declaracion se pone al dia con la conducta** (residual 5.2): que el inventario declare los
   asertos que de verdad matan a M2 y deje de declarar `assertNotEqual(hot, mutant_hot)` como
   frontera.

**Puertas afectadas:** las seis del `verification_cmd`. La 1 y la 2 son las que deben cambiar de
signo bajo el probe de 3.3.

**Lazo declarado:** remediacion -> re-juicio mio ANTES del commit de cierre -> **maximo 2 iteraciones
antes de escalar al operador humano. Esta era la primera; queda una.**

**Dato de gobierno, que decides tu y no yo.** El arreglo es de la misma talla que los tres de esta
vuelta: una normalizacion consumida por las dos superficies. No toca el criterio de AC1, no toca la
politica atestada, no toca el corpus. Y esta vuelta hizo lo que se le pidio: los dos mutantes de
produccion cambian de signo y la familia no registrada muere con ruta y valor. Si prefieres cerrar
con el hallazgo como residual declarado en vez de gastar la ultima iteracion, es una decision tuya
que puedes tomar con este veredicto delante -- yo dejo dicho que hoy, sobre el corpus real, no hay
ninguna decision escrita en otra caja, asi que el dano es latente, igual que lo era el censo 106/4
antes de que alguien mirase que decisiones eran las 106.

-- Analista, 2026-08-14 12:02 local (UTC+2)
