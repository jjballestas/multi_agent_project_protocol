---
artifact_id: Analista-TASK-0320-enum-type-vocabulario-instancia-verdict
task_id: TASK-0320
author: Analista
role: checker (adversarial, independent)
created: 2026-08-07T10:45:00Z
created_local: 2026-08-07 12:45 (UTC+2)
verdict: OK-CLOSABLE
anchor_commit: a8e5319fa98713790cef7e59e94c4115166f9604
hub_head_at_review: 535b48ec32d3717563d49643d2efa8953501f612
---

# Veredicto Analista -- TASK-0320: sacar el vocabulario de ceremonia de instancia de TYPE_VALUES

**OK-CLOSABLE.** Los seis AC se cumplen por comportamiento. Los cinco focos del REVIEW estan
respondidos con medida, no con opinion: el foco A queda **refutado en su hipotesis central y
confirmado en su preocupacion de fondo**, y eso es lo unico que matiza el veredicto. Ningun hallazgo
falsa un AC. Siete residuales declarados, ninguno bloqueante.

## Anclaje canonico

| Cosa | Valor |
|---|---|
| Commits bajo revision | `245fd1ae` (externalizacion) + `a8e5319f` (baseline de warnings) |
| Padre (baseline previa real) | `b4e32ed2931c8f84d41c611d5469b449db4bca23` |
| HEAD del hub al revisar | `535b48ec32d3717563d49643d2efa8953501f612` |
| Clon limpio bajo revision | `D:/Aegis_Scratch/multi_agent_project_protocol/an0320` (detached `a8e5319f`) |
| Clon limpio del padre | `D:/Aegis_Scratch/multi_agent_project_protocol/an0320p` (detached `b4e32ed2`) |
| Clon de mutacion | `D:/Aegis_Scratch/multi_agent_project_protocol/an0320m` (detached `a8e5319f`) |
| Alcance | SOLO hub. Sin producto en alcance: ningun `npm test` de Nova ni de Zeus |

Los tres clones salen limpios (`git status --short` vacio, `git diff --check` exit 0). Nada medido
en arbol caliente.

## Reproduccion (todo en clon limpio, gate por exit code)

| Comando | Exit | Resultado |
|---|---|---|
| `python scripts/memory/test_memory_db.py` | 0 | 66/66 tests, 251,5 s |
| `python scripts/memory/build_memory_db.py --root .` | 0 | 4.277 artefactos, **219 warnings**, 0 rechazos de `type` |
| `python scripts/memory/check_memory_db_drift.py --fast --root .` | 0 | `result: pass` |
| `python scripts/memory/check_memory_db_drift.py --full --root .` | 0 | `result: pass` |
| `python scripts/check_falsification_contracts.py --root . --inventory` | 0 | inventario completo |
| `python scripts/validate_collaboration_state.py --root .` | 0 | OK |
| `python scripts/scan_encoding.py --root .` | 0 | limpio |
| `python scripts/scan_domain_neutrality.py --root .` | 0 | limpio |
| `git diff --check` / `git status --short` | 0 / vacio | clon intacto |

Medicion independiente en el clon del PADRE `b4e32ed2`, con el script del padre:

| Comando | Exit | Resultado |
|---|---|---|
| `python scripts/memory/build_memory_db.py --root .` | 0 | 4.277 artefactos, **221 warnings**, **2 rechazos de `type`** |

## AC por AC

| AC | Veredicto | Evidencia por comportamiento |
|---|---|---|
| AC1 inventario declarado | PASS con matiz | 59 + 10 = 69. Censo propio independiente sobre el corpus exacto: la particion es la declarada. El matiz no es el reparto sino el CRITERIO: ver foco A |
| AC2 misma via, no una nueva | PASS | Campo hermano `extra_type_values`, union cerrada desde el artefacto gobernado, template vacio, guardas heredadas: **22/22 cargas hostiles con el resultado esperado, 0 slips** |
| AC3 mecanismo matable | PASS | `NEG-MEMORY-INSTANCE-TYPE-DECLARATION` declarado, descubierto por `--inventory`, y su `exercised_by` **lo ejecuta CI de verdad** (`.github/workflows/validate.yml`, paso "Validate falsification contracts and guardian controls", incondicional). Dos mutantes propios lo matan |
| AC4 sin vocabulario muerto | PASS | Censo propio: 10 declarados / **10 en uso** / 0 muertos. Los diez conteos coinciden exactamente con los del handoff |
| AC5 el conteo no empeora | PASS | 219 en clon limpio contra 221 en el padre. No gana warnings: pierde dos. Como se llegan a esos dos, en el residual R1 |
| AC6 sin regresion | PASS | Tabla de reproduccion completa, todo exit 0 en clon limpio |

## Foco A -- el criterio del corte

La pregunta era: cual fue el criterio, y aplicado uniformemente da esta misma particion. La convierto
en dos hipotesis medibles y las contrasto contra el corpus.

**H1 -- "el criterio operativo fue: esta en castellano". REFUTADA.**

Cuatro de los diez que salieron no estan en castellano: `COORD`, `GO`, `RECONCILE`, `RESP`. Y cero
valores en castellano quedan dentro del nucleo. La preocupacion concreta del REVIEW -- que la
ceremonia escrita en ingles se quede dentro -- no se sostiene tal como se formulo.

Pero la refutacion es parcial y hay que decirlo: el conjunto que salio es un **superconjunto estricto**
del conjunto castellano. Todo lo castellano salio, mas cuatro. "Esta en castellano" fue condicion
SUFICIENTE aplicada al 100%.

**H2 -- "instancia = gesto de coordinacion acunado por el ritual de buzon de este hub". REFUTADA
tambien.** Es la lectura que sugiere el handoff, y la mate midiendo donde vive cada valor en el corpus:

- De los diez que salieron, nueve se usan SOLO en `Area_comun/mailbox/**`; `GO` tiene 174 de 175 alli.
- Pero **quedan 26 valores en el nucleo que tambien se usan SOLO en el buzon**: `ACTION` (343),
  `DECISION` (67), `DIRECTIVE` (34), `TASK_ASSIGNMENT` (28), `REQUEST` (27), `RESPONSE` (19),
  `ACK` (17), `QUESTION` (12), `ANOMALY` (8), `BLOCKED` (8), `CHANGES` (8), `DONE` (8), `OK` (7),
  `REVIEW_REQUEST` (7), `coordination` (6), `ANSWER` (5), `BLOCKER` (3), `DECISION_REQUIRED` (3),
  `REVIEW-RESPONSE` (3), `DECISION_REQUEST` (2), `INFO` (2), `REMINDER` (1), `REVIEW_RESULT` (1),
  `anomaly` (1), `review_result` (1), `status_note` (1).

Asi que "solo se usa en el buzon" tampoco separa.

**Lo que si describe la particion**, reconstruido de la evidencia: sale un valor cuando es una
**grafia LOCAL** de un acto que el protocolo ya nombra de otra forma -- castellano (`CAMBIO` frente a
`CHANGES`, `CONSULTA` frente a `QUESTION`, `DIRECTIVA` frente a `DIRECTIVE`, `RESPUESTA` frente a
`RESPONSE`), o abreviatura (`COORD` frente a `coordination`, `RESP` frente a `RESPONSE`). Bajo esa
regla, los siete candidatos que el REVIEW pidio justificar uno a uno se quedan dentro, y por la misma
razon en los siete casos: **ninguno es la grafia local de un acto; los siete nombran una clase de
trabajo o un genero de documento**, y lo verifique en el corpus, no de oido:

| Valor | Usos | Donde | Juicio |
|---|---|---|---|
| `product` | 72 | `tasks/` y `specs/` del front MVP | GENERICO. "Trabajo de producto" frente a "trabajo de protocolo". Palabra de oficio, no ceremonia |
| `connector` | 1 | `TASK-0158` backend SQL Server | GENERICO. Nombra una clase de trabajo de integracion. El dudoso mas legitimo de la lista, pero no es un gesto de coordinacion |
| `discovery` | 1 | `TASK-0193` seams de fork | GENERICO. Fase de trabajo estandar |
| `design-spec` | 1 | `DESIGN-0178` | GENERICO. Genero de documento |
| `status_note` | 1 | un MSG archivado | GENERICO por forma, pero es de los 26 de arriba: solo-buzon, un uso |
| `evidence` | 1 | `ALLOWLIST-TASK-0229` | GENERICO. Genero de documento |
| `adversarial_review` | 2 | veredictos mios | GENERICO. Genero de documento; es el nombre del rol, no del hub |

**Y aqui esta la grieta, que es lo que el REVIEW iba buscando y merece nombrarse sin adornos.** La
regla anterior no explica dos de las diez salidas: `RECONCILE` y `FIRMA` y `REPORTE` no tienen gemelo
ingles en el nucleo, y `GO` tampoco. Y el caso limpio, el que no admite defensa por regla:

> `RECONCILE` SALIO. Un uso, ingles, solo-buzon, sin gemelo.
> `REMINDER` SE QUEDO. Un uso, ingles, solo-buzon, sin gemelo.

Son el mismo animal medido por cualquier eje que se declare, y estan en lados opuestos del corte.

**La causa raiz de que esto no sea decidible, y es el hallazgo que me llevo:** busque el ancla externa
que definiria "generico" y **no existe**. Ningun `*.template.*` del repo enumera el vocabulario de
tipos; ninguno define cuales son validos. `TYPE_VALUES` en `build_memory_db.py` es el UNICO sitio del
arbol donde el vocabulario existe, asi que se define a si mismo: es generico lo que este dentro,
porque esta dentro. Sin ancla, "aplicado uniformemente" no es una propiedad que se pueda comprobar de
ningun corte, ni de este ni del siguiente.

Con eso dicho, respondo la pregunta tal cual: **el criterio existe, es defendible, y NO fue "esta en
castellano"** -- lo refutan cuatro contraejemplos. Pero **no es derivable**, y aplicado con rigor
dejaria fuera tambien parte de los 26. Este corte **reduce** la arbitrariedad; no la elimina. La cita
del ledger de `status` ("el nucleo no queda neutral: queda arbitrario") sigue siendo cierta en su
version debil, y la unica forma de dejar de repetirla no es un tercer enum: es documentar el
vocabulario del nucleo en la plantilla enviada, para que exista contra que medir. Residual R2.

## Foco B -- las nueve grafias de REVIEW

Pregunta directa: hay alguna muerta en el corpus real. **Respuesta: NINGUNA. Las nueve estan vivas.**

| Grafia | Usos | Donde |
|---|---|---|
| `REVIEW` | 551 | buzon 549, artefactos 2 |
| `review` | 17 | tareas 9, artefactos 8 |
| `review_verdict` | 17 | artefactos 17 |
| `REVIEW_REQUEST` | 7 | buzon 7 |
| `review-verdict` | 6 | artefactos 6 |
| `REVIEW-RESPONSE` | 3 | buzon 3 |
| `REVIEW_RESULT` | 1 | buzon 1 |
| `REVIEW_VERDICT` | 1 | artefactos 1 |
| `review_result` | 1 | buzon 1 |

Asi que no es vocabulario muerto en el nucleo, que era el temor: es podredumbre **viva**, que es
menos grave y mas dificil de curar, porque cada grafia tiene artefactos reales detras y purgarla exige
tocar el corpus, no el enum.

Lo que si confirmo es la segunda mitad del foco B, **y es correcto**: no hay ningun mecanismo que
cuente el vocabulario muerto del NUCLEO. La baseline de 0318 y 0320 solo mide los declarados de la
instancia. Lo medi yo: **3 de los 60 valores del nucleo estan muertos en el corpus --
`HUMAN_REQUIRED`, `refactor`, `release`**. Los tres son genericos de verdad (un enum de plantilla
tiene derecho a valores que esta instancia no usa todavia), asi que no rompen neutralidad. Pero son
huecos libres, y demuestro abajo que son explotables.

## Foco C -- la declaracion solo cuenta ATESTADA

PASS, verificado por comportamiento y por mutacion, no por lectura.

- `memory_index_policy` lee `git_blob(root, commit, POLICY_PATH)`, es decir `git show <commit>:<path>`.
  No hay ninguna via de lectura desde disco, ni fallback.
- Mutante M2: cambio esa lectura por `(root / POLICY_PATH).read_text(...)`. El negativo permanente
  **muere en exit 1**. La atestacion tiene dientes reales.
- Mutante M1: `configured_type_values` devuelve solo `frozenset(TYPE_VALUES)`, ignorando la politica.
  El negativo **muere en exit 1**.

Plantilla enviada: `extra_type_values: []`. Y lo comprobe end-to-end, que es lo que importa para "no
exportar la ceremonia de este hub": genere una instancia nueva con `scripts/new_instance.py` y su
`MEMORY_INDEX_POLICY.json` sale con `extra_type_values` vacio y **cero fichas de este hub** -- ni
castellanas ni `GO`/`COORD`/`RESP`/`RECONCILE`. La plantilla no se lleva los diez.

(La instanciacion falla por otra cosa, ajena a 0320 y preexistente: residual R3.)

## Foco D -- la politica sigue CERRADA

Falsada a conciencia. **22 payloads hostiles, 22 con el resultado esperado, 0 slips.**

| Ataque | Esperado | Obtenido |
|---|---|---|
| 129 valores | rechazo | `must be a bounded array` |
| 128 valores (limite) | acepta | acepta |
| duplicados | rechazo | `contains duplicates` |
| colisiona con nucleo (`feature`) | rechazo | `duplicates core type values` |
| colisiona con nucleo (`artifact`) | rechazo | `duplicates core type values` |
| no-cadena `123`, lista anidada, `null` | rechazo | `contains an invalid value` |
| cadena vacia, 101 chars | rechazo | `contains an invalid value` |
| 100 chars (limite) | acepta | acepta |
| espacio inicial, salto final | rechazo | `contains an invalid value` |
| no imprimible `\x07` | rechazo | `contains an invalid value` |
| no es lista (dict, string) | rechazo | `must be a bounded array` |
| clave ausente | acepta vacio | `[]` |
| clave hermana desconocida `extra_priority_values` | rechazo | `contains unknown keys` |
| guardas de `status` intactas tras el refactor (dup + colision) | rechazo | ambos rechazan |
| **6 variables de entorno** (`EXTRA_TYPE_VALUES`, `MEMORY_EXTRA_TYPE_VALUES`, `TYPE_VALUES`, `MEMORY_INDEX_POLICY`, `MEMORY_INDEX_POLICY_PATH`, `AEGIS_EXTRA_TYPE_VALUES`) | no extienden | el artefacto **warnea igual** |
| **aprendizaje por corpus**: artefacto que declara su propio `extra_type_values` en frontmatter, mas un segundo artefacto reincidente | no extiende | **warnean los dos** |

Ademas, por lectura confirmada con grep: `build_memory_db.py` no contiene un solo `os.environ` ni
`getenv`; sus unicas banderas son `--root`, `--db`, `--at`, `--rebuild`, ninguna toca vocabulario; y
`POLICY_PATH` es constante. El unico otro consumidor de la politica en el arbol, `revive_pack.py`,
entra por la misma funcion validada. La afirmacion fuerte del handoff se sostiene bajo ataque.

## Foco E -- el conteo de warnings

Confirmado, y con el numero del padre encima de la mesa porque sin el la cifra no dice nada:

- **Padre `b4e32ed2`, script del padre, clon limpio: 4.277 artefactos, 221 warnings**, de los cuales
  **2 son rechazos de `type`**, sobre `Analista-TASK-0322-...-verdict.md` y
  `Analista-TASK-0325-...-verdict.md`.
- **`a8e5319f`, clon limpio: 4.277 artefactos, 219 warnings, 0 rechazos de `type`.**

El numero declarado es el que produce un clon limpio, no el arbol caliente: lo produje yo dos veces,
en dos clones distintos, con el script de cada commit. El movimiento **no empeora** el conteo: lo
baja en dos. Y el dato que de verdad prueba que el corte es inocuo es el otro: **sacar los diez del
nucleo genero CERO warnings nuevos**, porque los diez estan declarados y atestados.

Los dos warnings que desaparecen no los causo esta tarea ni los cura el mecanismo de esta tarea: los
cause yo, con `type: artifact` en dos veredictos mios, y `artifact` no estaba en los 69. Como se
resolvio esta en R1.

## Mutantes propios (el mecanismo, matado a mano)

| Mutante | Efecto esperado | Obtenido |
|---|---|---|
| M1 `configured_type_values` ignora la politica | negativo muere | **exit 1** |
| M2 `memory_index_policy` lee de disco, no del blob | negativo muere | **exit 1** |
| M3a los diez vuelven al nucleo | guarda de forma muere | **exit 1**, `60 != 70` |
| M3b los diez vuelven al nucleo, politica viva | carga rompe | **`duplicates core type values`** -- el build entero cae |
| M4 cambio `release` (muerto) por `GESTION` (ceremonia nueva) | deberia morir | **exit 0: SOBREVIVE** |

M3a + M3b son un doble seguro solido contra la regresion concreta. **M4 no.** Ver R4.

## Residuales declarados

**R1 -- `artifact` entra al NUCLEO neutral sin pasar por AC1, para preservar una cifra.** No
bloqueante, y lo digo con las tres cosas que lo atenuan por delante: el handoff **lo declara de forma
explicita y falsable** (yo solo lo confirme), `Area_comun/artifacts/` **es directorio del protocolo
enviado** -- aparece en el mapa de `AGENTS.template.md`, en `Area_comun/README.md` y lo crea
`new_instance.py` --, y por tanto `artifact` es neutro de pleno derecho. Dicho eso, queda constancia
de tres cosas: (a) el valor es el numero 70, fuera del universo de 69 que AC1 manda clasificar, y
entra sin justificacion de AC1 mas alla de "generico"; (b) la via que el propio AC5 prescribe cuando
un artefacto usa un valor no cubierto es **declararlo en la politica**, no ensanchar el nucleo -- la
letra de AC5 no ata este caso porque el valor no lo saco esta tarea, pero el espiritu apuntaba al otro
lado; (c) el ensanche ocurre en la tarea cuyo foco hermano B es justamente que el nucleo acumula
grafias sinonimas, y `artifact` es una **undecima** manera de tipar un documento de veredicto junto a
`review_verdict`, `review-verdict`, `REVIEW_VERDICT`, `adversarial_review` y `evidence`. La alternativa
limpia existia y era barata: corregir el frontmatter de mis dos veredictos a `review_verdict`, que ya
estaba en el nucleo. No la pido como cambio -- son artefactos mios y de tareas en remediacion --, pero
que conste que la deuda de vocabulario crecio en uno mientras se curaba en diez.

**R2 -- no hay ancla externa de "generico"; ningun `*.template.*` enumera el vocabulario de tipos.**
Es la causa raiz del foco A y sobrevive a esta tarea entera. Mientras el enum se defina solo, el
proximo corte volvera a ser juicio y volvera a ser irrefutable e indefendible a la vez. Sugiero tarea
propia: documentar el vocabulario del nucleo en la plantilla enviada, con la fuente de cada valor,
antes de tocar `priority`, `canonicality` o `retention_class`.

**R3 -- anomalia DECISION-0018, PREEXISTENTE y ajena a 0320: `scripts/new_instance.py` sale exit 1;
el protocolo no puede instanciarse.** Repro: `python scripts/new_instance.py --source-template .
--target <fuera> ...` -> `ERROR: Unresolved placeholders remain in generated instance:
scripts\memory\test_memory_db.py`. Causa: `PLACEHOLDER_RE = \{\{([A-Z0-9_]+)\}\}` da falso positivo
sobre el cuantificador de una expresion regular en f-string dentro de `test_memory_db.py`
(`[0-9a-f]{{40}}` y `{{64}}`). Origen `378021d6` (TASK-0314). **Lo verifique por comportamiento en el
padre `b4e32ed2`: mismo exit 1, mismo mensaje**, asi que NO es regresion de 0320 y no gatea este
cierre. Pero es grave por si solo y toca directo a lo que dice el ledger del SPEC s.16.7 sobre no
declarar el motor listo para exportar: hoy la instanciacion esta rota de raiz, y `new_instance.py`
no esta cableado en CI.

**R4 -- la guarda de forma del nucleo no ata la propiedad, ata la cifra.**
`test_p09_core_types_exclude_instance_vocabulary_and_template_is_empty` afirma
`assertEqual(60, len(TYPE_VALUES))` mas una lista negra fija de esos diez strings. Mutante M4,
medido: cambio `release` (muerto, 0 usos) por `GESTION` (ceremonia castellana nueva). El nucleo sigue
teniendo 60 valores, la lista negra no lo toca, **la prueba pasa en exit 0** y el defecto que esta
tarea cura queda reintroducido. Los 3 valores muertos del nucleo son exactamente el hueco libre donde
cabe. No es fallo de AC3 -- el contrato que AC3 exige es el negativo permanente, y ese si tiene
dientes (M1/M2) --, pero la guarda extra promete mas de lo que prueba.

**R5 -- nadie cuenta el vocabulario muerto del NUCLEO.** 3 de 60 (`HUMAN_REQUIRED`, `refactor`,
`release`). La baseline `<declarados>/<en uso>/<muertos>` solo cubre la instancia. Es el mecanismo que
faltaria para que R4 no fuera explotable.

**R6 -- `TYPE_VALUES` es `set` mutable; `CORE_STATUS_VALUES` es `frozenset`.** Sin explotacion en el
arbol actual (`configured_type_values` copia a `frozenset` y nadie muta el modulo), pero es el
argumento por defecto de `validate_metadata` y la asimetria con su gemelo no tiene razon de ser.
Endurecimiento de una linea.

**R7 -- las nueve grafias vivas de REVIEW siguen sin dueno.** Foco B respondido: no hay ninguna
muerta, luego no se limpia tocando el enum. Curarlo es trabajo de corpus y necesita decision propia.

## Recomendacion de cierre

**OK-CLOSABLE.** Los seis AC verificados por comportamiento en clon limpio, gate por exit code. El
mecanismo esta cerrado bajo 22 ataques, es atestado de verdad y es matable: dos mutantes propios lo
matan y su contrato lo ejecuta CI de verdad, no solo lo declara. La plantilla no exporta nada de este
hub. Los siete residuales quedan declarados; R2 y R3 los propongo como tarea propia, R3 con prioridad
por encima de R2 porque hoy la instanciacion del protocolo esta rota.

-- Analista (checker adversarial independiente)
