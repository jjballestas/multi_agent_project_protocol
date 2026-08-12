---
artifact_id: Analista-TASK-0365-spec-memoria-hibrida-review-formal-verdict
task_id: TASK-0365
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-08-12T18:15:00Z
anchor_commit: 694bd7e4b74731a737e916c4d93e9d4934cfe6b6
verdict: CHANGE-REQUIRED
iteration: 1
---

# Veredicto TASK-0365 -- review FORMAL de SPEC-MEMORIA-HIBRIDA v0.3.0

Voz del Analista. Yo no implemento, no promuevo, no cierro. Este veredicto gatea el cierre.

Respuesta corta a la pregunta del encargo: **puedo romper I7, y el mutante es de un campo.**
Dos reglas hot/cold identicas salvo su `created_by_decision` -- una respaldada por DECISION-0026
(`status: accepted`, la regla de memoria dorada que AGENTS.md s.7 cita como vinculante hoy) y otra
por DECISION-0099 (`status: active`) -- hacen que el gate rapido falle nombrando **solo** a
DECISION-0026 como "absent or inactive". El motor deriva "decision activa" del literal
`status == "active"`, y este hub escribe `accepted`: **106 de 110 decisiones indexadas quedan
`policy_state='historical'` con `hot_required=0`**. I7 esta bien escrito; el motor no lo cumple.
La correccion va al MOTOR.

## Anclaje canonico

- Commit bajo revision: `694bd7e4b74731a737e916c4d93e9d4934cfe6b6`
  (`coord(TASK-0365): la review formal de la SPEC va numerada...`), que era HEAD y `origin/main`
  al abrir la revision.
- Durante la revision `origin/main` avanzo a `4a29aa8a` (192c5dea + 4a29aa8a, TASK-0350).
  Verificado por exit code que **el motor y la SPEC son byte a byte identicos entre los dos
  commits**: `git diff --quiet 694bd7e4 4a29aa8a -- scripts/memory/ Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md Area_comun/protocol/MEMORY_INDEX_POLICY.json` -> exit 0.
  Toda medicion de este veredicto vale igual en HEAD.
- Metodo: **dos clones limpios** bajo `D:/Aegis_Scratch/protocol/t0365/` (DECISION-0104),
  `git clone -s -n` + `checkout 694bd7e4`. Ninguna puerta se corrio en el arbol caliente.
- Alcance: SOLO hub. Sin producto en alcance, `npm test` no gateado, conforme al encargo.

## Reproduccion, por exit code

| Comando (clon limpio, raiz del clon) | Exit | Salida relevante |
|---|---|---|
| `python scripts/validate_collaboration_state.py --root .` | **0** | `OK: collaboration state is valid.` |
| `python scripts/scan_encoding.py --root .` | **0** | -- |
| `python scripts/scan_domain_neutrality.py --root .` | **0** | -- |
| `python scripts/memory/test_memory_db.py` | **0** | `Ran 72 tests in 321.940s` / `OK` (72/72) |
| `python scripts/memory/build_memory_db.py --root .` | **0** | 4797 artefactos, 95 eventos, 15 tablas, `schema_version` 1, `foreign_keys` 1, 228 warnings |
| `python scripts/memory/build_memory_db.py --root . --rebuild` | **0** | mismo censo |
| `python scripts/memory/dump_memory_db.py` (A y B) | **0** | 8 942 429 bytes, sha256 `1615731d...c387f` en AMBOS |
| `python scripts/memory/check_memory_db_drift.py --root . --fast` | **0** | `result: pass`, `database_read: false` |
| `python scripts/memory/check_memory_db_drift.py --root . --full` | **0** | `result: pass`, `round_trip: pass`, `sweep: bidirectional-pass`, `database_written: false` |
| `python scripts/memory/revive_pack.py <agente>` x3 | **0** | 115 293 / 114 504 / 50 119 bytes |
| `check_memory_db_drift --fast` sobre el MUTANTE de reglas | **1** | `hot/cold rule references an absent or inactive decision: DECISION-0026` |

Las tres primeras puertas se corrieron **con la DB ausente** (`runtime/memory/` inexistente): es la
medicion de I5, no una formalidad.

## Veredicto invariante por invariante

Ninguno se declara cumplido sin haber intentado romperlo. La columna "ataque" dice que se intento.

| Inv | Ataque ejecutado | Resultado |
|---|---|---|
| **I1** | build A incremental -> dump; `--rebuild` desde cero -> dump; comparacion **byte a byte** en clon limpio | **PASS.** `cmp` identico, sha256 `1615731d...` en ambos dumps de 8 942 429 bytes |
| **I2** | `git status --porcelain` antes del build, tras el build y tras el `--rebuild` | **PASS.** 0 lineas en los tres puntos, incluidos untracked (`runtime/memory/` gitignored, linea 12) |
| **I3** | censo de las 4797 filas + familia propia de cargas contra `contains_pii` | **PASS con SLIPS.** 0 excerpts no nulos, 0 `public_plane_allowed=1`, 0 `is_pii_safe=1`, 0 `redaction_state != unclassified`; unica fuente de `search_terms` = `metadata_allowlist`. Slips S2/S3/S4 abajo |
| **I4** | fichero canonico de reglas plantado y **commiteado** con dos reglas habilitadas | **PASS por forma, mal calibrado.** El cargador falla cerrado (`enabled hot/cold rule requires created_by_decision`), pero el gate rechaza la regla respaldada por una decision `accepted`. Mismo defecto que B1 |
| **I5** | borrar la DB y correr los flujos vivos + censo de lectores en el arbol trackeado | **PASS con residual.** validate/encoding/neutralidad exit 0 sin DB; cero referencias a la DB en `runtime/`, en `scripts/harness/peer_mailbox_cron.ps1` ni en los workflows. Residual R-A abajo |
| **I6** | `revive_pack` de un agente contra las areas ajenas + superficie de CLI | **PASS.** Los 5 `agent_id` del indice salen del path (`Analista, Arquitecto, Codex, asesor, operador`); el pack de Codex trae 98 rutas `personal/Codex/` y ninguna fuente ajena (la unica mencion de `personal/Arquitecto` es texto citado dentro del cuerpo de una tarea). No hay flag que fuerce `agent_id` |
| **I7** | **mutante de un campo** sobre el fichero canonico de reglas + censo de `policy_status` | **FAIL. Ver B1** |
| **I8** | **arbol de trabajo saboteado**: append de contenido en un fichero y conversion integra a CRLF en otro, y build encima | **PASS.** Build exit 0; `artifacts.sha256` y `content_sha256` iguales al **blob de git** en los dos ficheros, distintos de la copia de trabajo. El `--full` tampoco falso-alarmo |
| **I9** | censo de aristas por tipo + tabla de productores + `validate_f1_edge_type` + inyeccion de lista mixta | **PASS con SLIP.** Todo `edge_type` producido esta en `EDGE_PRODUCERS`; los reservados no se escriben; ninguna arista nace del cuerpo. Slip S1 abajo |

## B1 -- BLOQUEANTE: I7 se cumple por su LETRA y se rompe por su NOMBRE

**Que promete I7.** "Decision activa jamas invisible": `policy_status.hot_required=1` obliga a que
el .md completo este hot o exista stub verificado, y `check_memory_db_drift` falla si no.

**Que hace el motor.** `policy_row()` en `build_memory_db.py:1110` deriva el estado de politica de
una comparacion literal:

    if status == "active":      policy_state = "active"      # hot_required = 1
    elif status == "superseded": policy_state = "superseded"
    else:                        policy_state = "historical"  # hot_required = 0

y `_active_decisions()` en `check_memory_db_drift.py:27` usa el mismo literal.

**Que escribe este hub.** Censo del corpus de `Area_comun/decisions/` en clon limpio:
**104 `accepted`, 4 `active`, 1 `proposed`.**

**Consecuencia medida sobre la DB construida** (4797 artefactos, clon limpio @694bd7e4):

    policy_state=historical  hot_required=0   n=106
    policy_state=active      hot_required=1   n=4

Las cuatro `active` son DECISION-0099, 0100, 0101 y 0103, las mas recientes. Todo lo demas es
"historia" para el indice. Entre ese 96,4 por ciento estan, con `hot_required=0`, decisiones que
**AGENTS.md cita nominalmente como vinculantes hoy**:

| Decision | `status` en frontmatter | Como la clasifica el indice | Citada en AGENTS.md |
|---|---|---|---|
| DECISION-0026 (regla de memoria dorada) | `accepted` | `historical`, `hot_required=0` | s.7 |
| DECISION-0020 (anti-colision de ledger) | `accepted` | `historical`, `hot_required=0` | s.7 |
| DECISION-0038 (regla primordial de narracion) | `accepted` | `historical`, `hot_required=0` | s.7 |
| DECISION-0104 (disciplina de scratch, "inquebrantable") | `accepted` | `historical`, `hot_required=0` | s.4 |
| DECISION-0018 (notificacion de anomalia) | `accepted` | `historical`, `hot_required=0` | s.7 (x2) |
| DECISION-0016 (area personal) | `accepted` | `historical`, `hot_required=0` | s.7 |
| DECISION-0022 (modo runtime-autoritativo) | `accepted` | `historical`, `hot_required=0` | s.7 |
| DECISION-0081 (`derives_from` de esta misma SPEC) | `accepted` | `historical`, `hot_required=0` | -- |

**El mutante, de un campo.** Escribi `Area_comun/protocol/MEMORY_HOT_COLD_RULES.json` en el clon
de scratch con dos reglas habilitadas identicas salvo su respaldo, y lo **commitee** (el motor lee
el blob, no la copia de trabajo):

    R-ACCEPTED-BACKED  created_by_decision: DECISION-0026   (status accepted)
    R-ACTIVE-BACKED    created_by_decision: DECISION-0099   (status active)

    $ python scripts/memory/check_memory_db_drift.py --root . --fast
    ERROR: hot/cold rule references an absent or inactive decision: DECISION-0026
    exit 1

El gate nombra **solo** a DECISION-0026. La unica diferencia entre las dos reglas es el valor de un
campo. Es un test de dos puntos que discrimina: no estoy leyendo codigo, estoy viendo el
comportamiento invertirse.

**El defecto tiene dos caras y solo una es segura.**

- Cara fail-CLOSED (I4): una regla legitimamente respaldada por una decision en vigor no puede
  habilitarse. Molesto, pero no peligroso.
- Cara fail-OPEN (I7 y s.8 Q3): 106 decisiones en vigor llevan `hot_required=0`, de modo que
  cuando F2/F3 enciendan el enfriado, `--propose-cold` y el gate de drift trataran como historia
  archivable sin stub a la practica totalidad de la politica vigente del protocolo, **y I7 no
  dira nada**. La garantia sera cierta porque su antecedente casi nunca se cumple, no porque
  proteja.

**Por que esto es del port y no del corpus.** El port calibro al vocabulario del hub los enums de
ACEPTACION (P8 identidades, P9 `status`/`type`) sacandolos a `MEMORY_INDEX_POLICY.json`. Pero
`accepted` ya estaba en `CORE_STATUS_VALUES`: se indexa perfectamente. Lo que nunca se calibro es
el **mapeo a estado de politica**, que esta cableado en `policy_row` y **no tiene superficie de
configuracion ninguna**. Anadir `accepted` a `extra_status_values` no arregla nada. Es la misma
clase de hallazgo que P8/P9, en el unico sitio donde el port no miro.

**Direccion de la correccion: al MOTOR.** I7 y s.8 Q3 estan bien escritos. La salida facil seria
reescribir el texto o renombrar 104 ficheros gobernados a `status: active`; ambas contradicen la
regla del propio port (s.16.3: se amplia el conjunto de valores ACEPTADOS conservando la validacion
por VALOR). Lo que toca es exponer el mapeo de estado de politica al mismo mecanismo atestado que
ya cura los enums, con enum finito y por valor.

**Por que bloquea salir de `draft-reviewed-informal`.** Hoy el dano es latente
(`cold_pack_count: 0`, `rule_count: 0`, F2/F3 apagadas). Eso es precisamente lo que lo hace
peligroso: la SPEC saldria de draft certificando una garantia cuya implementacion esta apagada para
el 96 por ciento del corpus, y nadie lo notaria hasta el dia en que se encienda el enfriado, que es
el dia en que I7 es lo unico que separa la politica vigente de la carpeta de historia.

## B2 -- BLOQUEANTE: la s.7 normativa contradice al motor que se acaba de portar

I3 remite explicitamente a la s.7 ("Frontmatter indexado por ALLOWLIST DE CLAVES con validacion por
VALOR (s.7)"). Comparada la s.7 con `build_memory_db.py` del mismo commit:

| s.7 dice | El motor hace | Origen |
|---|---|---|
| allowlist v1 de **20** claves, enumeradas | **21** claves: la s.7 no incluye `applies_to`, que el motor si indexa y sobre la que se apoya `policy_status.applies_to` de la s.5.5 | nunca declarado |
| `title` = "**ASCII imprimible**" | `title_is_safe` acepta UTF-8 imprimible: `title_is_safe("...evaluacion SOTA o<acento>")` -> True | autorizado por P7, s.7 no actualizada |
| `title` longitud "**<= 200**" | `TITLE_MAX_LENGTH = 500` | autorizado por P7, s.7 no actualizada |

Los dos ultimos son contradicciones **internas** de la SPEC: la s.16.3 autoriza el cambio y la s.7
sigue afirmando la regla vieja. El primero es peor: el motor indexa una clave que la allowlist
normativa no autoriza. Una allowlist es un contrato de superficie; si la lista publicada y la
efectiva difieren, deja de ser allowlist. **Direccion: al TEXTO**, como edicion gobernada de la
SPEC (la s.5.1b ya declara que cambiar estas tablas es edicion gobernada, nunca decision del
implementador), salvo que se decida que `applies_to` no debe indexarse, en cuyo caso va al motor.

## AC4 -- la neutralizacion del lexico de PII quedo POR LISTA, en los dos lados

El encargo pedia determinar si quedo por CRITERIO de pertenencia o por LISTA. Medido:

1. **El nucleo si quedo neutro de nomina.** `contains_payroll_pii` es hoy `contains_pii`, y el
   lexico salio: `contains_pii("salario bruto anual", [])` -> **False**;
   `contains_pii("nombre del agente", [])` -> **False** (el falso positivo de P1 murio).
2. **El mecanismo compensatorio es un ALLOWLIST DECLARADO, y solo surte efecto ATESTADO.** Lo
   verifique yo, no lo relayo: edite `MEMORY_INDEX_POLICY.json` en la copia de trabajo poniendo
   `domain_pii_terms: ["salario","empleado"]` y el motor siguio leyendo `[]`, porque
   `memory_index_policy()` va por `git_blob`. Declarado y commiteado, funciona
   (`contains_pii("salario bruto", ["salario"])` -> True). La politica esta acotada (<=128 terminos,
   <=100 caracteres, sin duplicados, imprimibles). Esto es lo que convierte la declaracion en
   validacion y no en documentacion.
3. **Pero el nucleo conserva una LISTA de dominio, no un criterio.** `STRUCTURAL_PII_PATTERNS[2]`
   es literalmente `\b(?:NIF|NIE|NIT|DNI|SSN)\b`: cinco siglas fiscales de jurisdicciones
   concretas (ES / LatAm / US). Medido con mis propias cargas:

        "el NIF del titular"                    -> True
        "el CPF del titular"        (Brasil)    -> False
        "el RFC del titular"        (Mexico)    -> False
        "the NINO of the worker"    (UK)        -> False
        "il codice fiscale ..."     (Italia)    -> False

   La s.16.3 P1 autorizo "palabras clave de id fiscal" en el nucleo, asi que **el motor cumple
   P1**; pero P1 pidio "patrones ESTRUCTURALES" y esto no lo es: es una lista de cinco terminos sin
   criterio de pertenencia declarado ni jurisdicciones nombradas. **Respuesta a AC4: por lista.**
   Es la clase que esta instancia lleva semanas desterrando, y la declaro como tal. No la hago
   bloqueante porque su correccion es acotada (o pasar esas siglas al mismo mecanismo atestado que
   ya existe, o declarar por escrito el criterio y las jurisdicciones cubiertas), y porque el email,
   el identificador de cuenta con digito de control y el telefono si son estructurales.

## AC5 -- la regla del port, verificada hallazgo por hallazgo

"Ningun hallazgo se resuelve relajando una garantia; se amplia el conjunto de valores ACEPTADOS
conservando la validacion por VALOR. Nunca texto libre en el indice."

| P | Estado medido | Conserva validacion por VALOR? |
|---|---|---|
| P1 lexico de nomina en el nucleo | **CUMPLIDO con matiz** (ver AC4): lexico fuera, funcion renombrada, `domain_pii_terms: []` por defecto | Si: allowlist acotada y atestada, no texto libre. Unico sitio donde una garantia se ESTRECHA -- exigido por la frontera de neutralidad, con mecanismo compensatorio declarado y verificado |
| P2 literal `"Nova-Payroll"` | **CUMPLIDO.** `SELECT DISTINCT project FROM artifacts` -> `multi_agent_project_protocol`, derivado de `protocol.config.json` | Si: `project_name` validado (no vacio, imprimible, <=200) |
| P3 `DUMP_FORMAT` | **CUMPLIDO.** `protocol-memory-derived-v1` | n/a |
| P4 docstrings con marca de producto | **INCUMPLIDO PARCIAL.** `build_memory_db.py:9` conserva "No migration of a **Zeus** DB is attempted". `scan_domain_neutrality.py` sale 0: ningun gate lo caza | n/a |
| P5 telefono vs ids con marca de tiempo | **CUMPLIDO.** `contains_pii("MSG-20260619-092823-Codex-to-Arquitecto-x", coordinate="message_id")` -> False; el telefono desnudo sigue cazado | Si: por sobre de identidad anclado, no por desactivar el patron. Slip S4 |
| P6 `ID_RE` sin punto | **CUMPLIDO.** `^[A-Z]+-[0-9A-Za-z._-]+$`, ancla de prefijo en mayusculas conservada | Si: regex anclada |
| P7 titulos con tilde / >200 | **CUMPLIDO EN CODIGO, texto sin actualizar** (ver B2) | Si: sigue pasando el scan PII por valor |
| P8 identidades | **CUMPLIDO.** `configured_agents` = registry UNION `human_owner` UNION `identity_aliases` (10 alias declarados) | Si: pertenencia a conjunto finito, jamas texto libre |
| P9 enums `type`/`status` | **CUMPLIDO.** `extra_status_values` (8) y `extra_type_values` (10) en la politica atestada | Si: enums finitos |
| P10 `*_TEMPLATE.*` | **CUMPLIDO.** `is_excluded` con `(?:^|_)template(?:\.|$)`; ademas ids con `XXXX` ignorados. El build de 4797 artefactos no aborta por colision | n/a |
| P11 tope de `revive_pack` | **CUMPLIDO.** Arquitecto **115 293** bytes contra `max_bytes` 131 072 (era 1 535 306: reduccion 13,3x), con `omitted_bytes_total: 1394955`, `omitted_entries_total: 296` y `token_estimate: 28817` declarados dentro del pack | Si: resumen determinista de metadata |
| P12 `supersedes: []` | **CUMPLIDO.** Lista vacia aceptada sin arista; `""` sigue rechazado | Si: el rechazo se reserva a malformados |

**Conclusion de AC5: la regla se cumplio.** Ninguno de P5-P9 ni P12 relajo nada; todos ampliaron el
dominio de valores aceptados por enum finito, regex anclada o allowlist atestada, y no entro texto
libre en el indice (lo confirma el censo: unica fuente de `search_terms` = `metadata_allowlist`).
El unico incumplimiento es **P4**, y es de neutralidad, no de garantia.

## Slips y residuales declarados (no bloqueantes)

- **S1 -- las 222 aristas `implements` no resuelven ninguna.** Censo sobre la DB construida:

        mentions      total=1262  to_id resuelve=862
        decision_for  total=971   to_id resuelve=970
        implements    total=222   to_id resuelve=0
        supersedes    total=3     to_id resuelve=3

  La causa es estructural: `file_target_id` sintetiza `artifact:<ruta>`, pero el artefacto que vive
  en esa ruta tiene id **intrinseco** (`TASK-XXXX`), nunca `artifact:Area_comun/tasks/...`. La
  s.5.1b promete "from=task, to=artefacto entregable"; el tipo de arista es hoy inerte al 100 por
  cien. No viola I9 (la arista SI se extrae de una clave allowlisted), pero el grafo no une lo que
  la SPEC dice que une. **Correccion al MOTOR** (normalizar el destino al id intrinseco cuando la
  ruta resuelve a un artefacto indexado). Las 400 `mentions` colgantes son el caso declarado y
  tolerado del DDL (sin FK a proposito); las 222 `implements` no son ese caso: son el 100 por cien.
- **S2 -- deteccion de id fiscal por lista de 5 siglas** (AC4 punto 3).
- **S3 -- la deteccion de identificador de cuenta AGRUPADO esta atada a una clase de 7
  separadores.** El residual R2 del ledger dice "IBAN solo forma contigua", y eso subestima al
  motor y a la vez oculta donde esta el hueco. Medido con un IBAN valido agrupado de 4 en 4:

        espacio, punto, guion, barra, guion_bajo, nbsp, thin-space  -> True
        coma, punto_y_coma, dos_puntos, barra_vertical, mas         -> False

  La agrupacion por coma es la forma humana mas comun despues del espacio. **Correccion al MOTOR**,
  y de paso corregir la redaccion de R2 en la s.16.7, que hoy describe mal el comportamiento real.
- **S4 -- la exencion `REQ-[0-9A-F]{8,}` no tiene tope de longitud.** Los sobres
  `(?:TASK|DECISION|SPEC)-\d{4}` son exactos; el de `REQ` es abierto por arriba. Medido:
  `REQ-6001234567890123456789012345678901234567` (40 digitos) pasa `ID_RE` y da `contains_pii` ->
  False, mientras la misma cadena desnuda da True. Es la clase declarada en R1, pero R1 no dice que
  la exencion sea **ilimitada**; con un tope se cerraria sin perder el arreglo de P5.
- **S5 -- `events.jsonl` es fuente declarada del `--rebuild` (s.6) y el motor solo la cuenta.**
  `read_events_torn_safe` se invoca en `build_memory_db.py:1182` y su resultado se usa
  exclusivamente en `event_count` (linea 1381): ninguna fila derivada de eventos entra en la DB.
  Ademas es la unica fuente que se lee del **arbol de trabajo**, no del blob (lo que no rompe I8
  porque nada de ella se hashea ni se atesta, pero es la excepcion y conviene que este escrita).
  La s.6 deberia decir que en F1 los eventos no contribuyen a la particion derivada.
- **S6 -- el rechazo por clave es todo-o-nada y tira ids validos.** Verificado:
  `relates_to: [PACKAGE_VERSIONING, SPEC-0043]` (caso real, `Area_comun/specs/SPEC-0057-fase7-release-engineering.md`)
  rechaza la clave entera y pierde tambien la arista valida a SPEC-0043. La s.7 lo autoriza
  ("si no valida, la clave NO se indexa"), asi que no es incumplimiento; lo declaro porque el efecto
  sobre el grafo es silencioso (solo warning) y contraintuitivo para quien lea I9.
- **S7 -- P4 sin cerrar** (marca de producto en el docstring del nucleo, ningun gate la caza).
- **S8 -- el cardinal "219 warnings" de la s.16.7 no se re-deriva sin nombrar su poblacion.**
  Medido en clon limpio: **228 en total, de los cuales 219 sobre `Area_comun/`** (gobernado) y 9
  sobre `personal/`. Las dos lecturas dan numeros distintos y la SPEC no dice cual es. Una linea
  base de deriva que no nombra su unidad no sirve de linea base.
- **S9 -- `scope='compartido'` de I6 es inalcanzable.** `agent_memory.scope` se inserta con el
  literal `'personal'` y el tipo `memory` solo nace de `personal/`. La frase de I6 sobre fuentes
  bajo `Area_comun/` no describe nada que el motor produzca.

## Lo que NO pude medir, y por que (AC6)

- **R-A: el camino de ESCRITURA de `submit_intent` con la DB ausente.** En clon limpio llega hasta
  la resolucion de firma y para: `ERROR: event auth signing key missing for actor: Analista` (y,
  antes, `lacks required capability: orchestrator` para `task_upsert`). Es decir: el flujo recorre
  parseo, validacion, lectura de config y autorizacion **sin tocar la DB**, y falla por ausencia de
  claves, que no estan en el arbol. No corri el camino de escritura en el arbol vivo porque mutaria
  el ledger canonico y yo soy checker. Lo que si acredito por censo del arbol trackeado: **cero
  referencias** a `index.db`, `runtime/memory` o a los scripts del motor en `runtime/`, en
  `scripts/harness/peer_mailbox_cron.ps1` (el arnes de los peones, que si esta trackeado) o en los
  workflows; las unicas menciones en `scripts/` son de EXCLUSION (`scan_encoding`,
  `scan_domain_neutrality`) y de EXPORTACION (`new_instance.py`). I5 lo doy por PASS con este
  residual escrito.
- **I7 en su cara de stubs, y I4 en su cara de movimiento fisico, no tienen corpus.**
  `cold_pack_count: 0`, `rule_count: 0`, y `Area_comun/protocol/MEMORY_HOT_COLD_RULES.json` **no
  existe en el arbol** (es entregable de F2). Todo lo que afirmo sobre esos caminos sale del
  mutante que yo plante y commitee, no de datos reales. Es exactamente por eso que B1 importa: el
  unico ejercicio que ha tenido ese camino es el mio.
- **DoD 8 (export a instancias)**: existe el test
  `test_new_instance_exports_complete_memory_toolchain` y esta verde dentro de los 72. No medi el
  instanciador de punta a punta porque TASK-0350 ya lo tiene censado; no encontre indicio de que sea
  mas ancho que su titulo, pero tampoco lo busque activamente: quedaba fuera del encargo.
- No corri `npm test` ni nada de producto: el encargo declaro alcance solo hub.

## Recomendacion de cierre

**CHANGE-REQUIRED.** La SPEC **no** puede salir hoy de `status: draft-reviewed-informal`.

Siete de los nueve invariantes resisten los ataques, y tres de ellos (I1+I8 round-trip byte a byte,
I2 read-only, I3 plano publico cerrado sobre 4797 filas) lo hacen con margen. El motor es solido y
el port cumplio su regla. Lo que impide el cambio de estado son dos cosas concretas:

1. **B1**, que hay que corregir en el **MOTOR**: exponer el mapeo de estado de politica al mismo
   mecanismo atestado que ya cura los enums, de modo que el vocabulario de decisiones en vigor de
   esta instancia (`accepted`) produzca `policy_state='active'` y `hot_required=1`. Con un test que
   fije la propiedad -- no el conteo --: *toda decision que el contrato vigente cita como vinculante
   tiene `hot_required=1`*. Un test sobre "4 activas" volveria a estar verde el dia que el mapeo se
   rompa de otra forma.
2. **B2**, que hay que corregir en el **TEXTO**, como edicion gobernada: alinear la s.7 con el motor
   en las tres divergencias, o retirar `applies_to` del motor si la decision es no indexarla.

Los slips S1-S9 no bloquean el cambio de estado, pero S1 y S3 son correcciones al motor que
conviene no dejar sin tarea, y S8 es una linea base que hoy no cumple su funcion.

## Bucle de correccion esperado

- **Remediacion**: B1 al maker (Codex) como cambio de motor + test de propiedad; B2 al Arquitecto
  como edicion gobernada de la SPEC. Son independientes y pueden ir en paralelo.
- **Puertas afectadas** en el re-juicio: `validate_collaboration_state.py`, `scan_encoding.py`,
  `scan_domain_neutrality.py`, `scripts/memory/test_memory_db.py`, build normal + `--rebuild` con
  round-trip byte a byte, `check_memory_db_drift --fast` y `--full`, todo en clon limpio y por exit
  code. Anado como puerta del re-juicio la **repeticion de mi mutante de dos reglas**: tras el
  arreglo, la regla respaldada por una decision `accepted` debe pasar y el censo de `policy_status`
  debe dejar de decir 106/4.
- **Re-juicio antes del commit de cierre**, siempre. Maximo **2 iteraciones**; si a la tercera
  sigue abierto, escalo al operador humano.

-- Analista, 2026-08-12 20:15 local (UTC+2)
