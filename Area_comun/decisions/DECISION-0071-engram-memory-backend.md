---
decision_id: DECISION-0071
title: Engram como backend de memoria/recall (capability OFF by default) - frontera ledger/memoria, namespacing por agente, single-writer preservado, activacion Tier 1 por gate atestado (estructural por diseno, valido en runtime-tier) y no-interferencia con el dataset del TFM
status: accepted
date: 2026-06-29
deciders: [operador humano (aprobado 2026-06-29), Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0016, DECISION-0020, DECISION-0022, DECISION-0026, DECISION-0040, DECISION-0050]
phase: P2
capability_state: OFF (mechanism specified, not merged; PATCH = SPEC hasta merge+tests)
canonical_protocol_commit: 77dfa0f64c738b6be5d57d89fb44de4d601c98ed
adversarial_review: [TASK-0219 NO-GO, TASK-0220 NO-GO, TASK-0221 GO-PROMOVER-OFF]
revision: v3.1 (correccion de overclaims tras verificacion adversarial de v2; matriz de estado honesta; fix real de B en scope/task_id/supersedes; engram_source_commit 44faeee; v3.1 relabel honesto de la fila B tras TASK-0220 -- B-cero-prosa-libre, PII corta = DISCIPLINARIO; drafts canonicalizados en HEAD)
---

# DECISION-0071 - Engram como backend de memoria/recall (capability OFF by default)

> DRAFT v3 del Arquitecto. v2 cerraba los bloqueantes del Analista con DISENO solido pero la verificacion
> adversarial cazo que SOBRE-AFIRMABA cierre ("cerrado/probado/estructural" sin codigo merged, sin declarar
> precondiciones, y con 3 campos -- scope/task_id/supersedes -- que aun admitian prosa). v3 corrige con
> HONESTIDAD: matriz de estado por bloqueante, fix real de B, precondiciones explicitas (runtime-tier,
> chain_enabled, actor_auth_enforce atestado), y nada llamado "cerrado". NO toca el ledger al redactarse.
> Cambio aditivo, capacidad APAGADA por defecto, neutral de dominio en el Core. La aprobacion por escrito
> del operador se registra como esta DECISION al promover (OFF, como "capacidad definida con matriz honesta").
>
> **Honestidad estructural (leccion central de DECISION-0040; v3 corrige el sobre-cierre de v2 cazado por la
> verificacion adversarial, el mismo pecado que hundio v1 y antes a 0040):** este documento NO llama
> "cerrado" ni "probado" a nada que (a) no tenga codigo merged, (b) tenga precondiciones no declaradas, o
> (c) aun admita prosa libre. Cada bloqueante lleva una **etiqueta de estado honesta** de este conjunto
> exacto: **ESTRUCTURAL | ESTRUCTURAL-PENDIENTE-IMPL+TESTS | ESTRUCTURAL-SI-PRECONDICION(<cual>) |
> DISCIPLINARIO | ABIERTO-DIFERIDO** (ver la Matriz de estado honesta v3 al final). El codigo del intent NO
> esta merged (`grep engram_* runtime/*.py` = 0 hits) y los tests son a ESCRIBIR, no ejecutados: por eso
> "estructural por diseno" no equivale a "cerrado". Esta DECISION es promovible **OFF** como "capacidad
> definida con matriz de estado honesta"; el PATCH queda como SPEC hasta que Codex implemente+pruebe.
> **Ningun bloqueante se declara cerrado. v3 NO se promueve como "Tier 1 listo".**

## Contexto

Hoy la memoria persistente de cada agente es markdown (`personal/<id>/` + runbook), gobernada por la
regla de oro post-commit (DECISION-0026). Funciona, pero el recall es manual (grep) y no detecta
memoria obsoleta/contradictoria. **Engram** (Gentleman-Programming) es un motor de memoria
agent-agnostico (Go + SQLite/FTS5 + servidor MCP, ~20 tools `mem_save`/`mem_search`/`mem_context`,
y *conflict-surfacing* `mem_judge`/`mem_compare`) que mejoraria el arranque frio y la higiene de memoria.
Hechos verificados contra la fuente primaria (`github.com/Gentleman-Programming/engram` @ `44faeee`).

**El hecho que obliga esta decision:** el modelo de concurrencia de Engram es **opuesto** al nuestro.
Su propia doc: memoria **compartida por proyecto**, *"scope is a search and filter signal, not a privacy
boundary"* (`docs/TEAM-USAGE.md:22-30`), **sin locks** y con la verdad local en un **SQLite fuera del
repo** que a git solo exporta `chunks/*.jsonl.gz` (`README.md:150-165`, `DOCS.md:1115-1138`).
Dos matices que v1 afirmo de mas y aqui se fijan EXACTOS (verificados por el Analista vs fuente
primaria, commit `44faeee`):

- **Autor (P1, exacto):** las **OBSERVACIONES** (`mem_save`) **no llevan campo de autor** -- la fila de
  observacion documenta `{session_id, type, title, content, project?, scope?, topic_key?}` sin
  author/actor (`DOCS.md:46`, `DOCS.md:136`). En cambio, **`memory_relations` SI tiene un campo
  `marked_by_actor`** (`DOCS.md:51`). Es decir: NO es cierto que "ningun registro lleve autor"; lo
  exacto es que **la unidad que escribiriamos en flujo (la observacion) no atribuye autor**, que es
  precisamente la unidad cuya identidad necesitamos para el aislamiento per-agente. Por eso el
  aislamiento per-agente **no puede descansar en "Engram no tiene autor"** sino en enforcement externo
  `actor -> memory_project` (clausula 4) y en el `actor` firmado del propio evento del ledger (clausula 4-bis).

- **Merge (P2, exacto):** Engram **SI documenta** una estrategia de sincronizacion git basada en
  **chunks append-only con "no merge conflicts"** a nivel de archivo (`README.md:150`,
  `DOCS.md:1136-1138`); tambien expone import/export JSON y sync de chunks (`DOCS.md:180-185`,
  `DOCS.md:1110-1119`). Lo que **NO** documenta -- y lo que sigue **sin resolver** para nuestro caso --
  es la **resolucion semantica de memorias CONTRADICTORIAS entre agentes** (que gana cuando dos pools
  afirman hechos incompatibles): la evitacion de merge de archivos no equivale a una politica de
  arbitraje de contenido. `mem_judge`/`mem_compare` las **SUPERFICIAN** pero no las resuelven.

Con esos dos matices fijados, el riesgo de fondo persiste: enchufar Engram ingenuamente (varios agentes
escribiendo un pool compartido de observaciones que no atribuyen autor) **reintroduce el multi-writer que
matamos con claims + `submit_intent`** (DECISION-0020), y mete texto libre en un plano que GATE-DATASET
(DECISION-0040) protege, sin que la sincronizacion append-only ofrezca arbitraje cuando dos agentes se
contradicen. Esta decision fija como adoptar Engram **sin** perder esas garantias y **sin** afectar el TFM,
distinguiendo lo estructural de lo disciplinario.

## Decision

### 1. Frontera dura: Engram != ledger. markdown-en-git = registro DURABLE; Engram = CACHE de recall. [HONESTIDAD - corrige blocker D]

El ledger atestado #4 (`Area_comun/state/*.json` via `submit_intent`) sigue siendo la **unica fuente de
verdad de gobernanza**. El **markdown-en-git** (`personal/<id>/` + runbook, regla de oro DECISION-0026) es
el **registro durable y atestable** de la memoria de cada agente. **Engram es un CACHE de recall, NO una
fuente de verdad y NO se afirma reconstruible mientras no exista importador con test.**

- **[ESTRUCTURAL]** El intent `engram_observation` es un **no-op puro** sobre el state materializado:
  `apply_intent_event` (`runtime/protocol_replay.py`) no tiene rama que mute CLAIMS/TASK_INDEX/PROJECT_STATE
  para este tipo; lo hacen cumplir el hard-gate B.3 de drift y el test de replay byte-identico (PATCH v2 sec.3).
  Engram **no puede sombrear el state de protocolo** por construccion del replay.
- **[HONESTIDAD - corrige blocker D]** v1 prometia "indice derivado **reconstruible** desde markdown". El
  Analista refuto: **no existe importador `personal/<id>/MEMORY.md` -> Engram ni esquema canonico de memoria
  en markdown** (Engram tiene import/export JSON y sync de chunks `DOCS.md:180-185,1110-1119`, no un
  importador desde nuestro markdown). v2 BAJA la afirmacion: Engram es **cache de recall NO autoritativa y
  NO reconstruible automaticamente** hoy. Si su DB local se pierde, el agente NO pierde memoria (sigue en
  markdown-en-git) pero el recall por Engram queda **degradado** hasta que se re-puebla; no hay reimport
  automatico. La reconstruibilidad markdown->Engram queda como **tarea diferida ENG-IMPORT con test
  round-trip**, NO como propiedad afirmada de esta decision. Engram no anade ninguna fuente de verdad nueva.

### 2. Capacidad APAGADA por defecto + modelo de tres niveles.

- **Tier 0 (permitido YA):** recall per-agente, DB local, **no commiteado**, fuera del ledger. Cada agente
  hace `mem_save`/`mem_search` en SU proyecto Engram. Impacto en claims/ledger/dataset = **ninguno** (vive
  fuera de rutas del repo y no emite eventos). **[ESTRUCTURAL: no toca el ledger porque no pasa por
  `submit_intent`; DISCIPLINARIO: el aislamiento entre pools Tier 0 es por DB local separada, ver 4(d).]**
- **Tier 1 (DIFERIDO en su ACTIVACION, ver clausula 5):** memoria **compartida** entre agentes, enrutada
  por `submit_intent` (intent `engram_observation`). Single-writer del ledger preservado. El **mecanismo**
  del intent se especifica y se shippea OFF (PATCH); su **activacion** pasa por un gate atestado (estructural
  por diseno, valido en runtime-tier; ver clausula 5 y la Matriz de estado).
- **Tier 2 (no recomendado / fit debil):** commitear `.engram/` a git. Solo single-writer (runtime), claim
  explicito sobre la ruta, staging explicito (DECISION-0020 #2). Caveat: chunks gzip casi binarios para
  diff y el merge SEMANTICO no esta resuelto -> preferir Tier 0 + reimport.

### 3. Namespacing por agente = proyecto Engram `map-<id>` (espejo de DECISION-0016).

`personal/Arquitecto` -> `map-arquitecto`; `Codex` -> `map-codex`; `Analista` -> `map-analista`. El
`memory_project` es **enrutado/namespacing**, NO identidad por si solo (premisa P1 corregida). La identidad
de autor es estructural y vive en el evento del ledger (clausula 4-bis) y se ENFORZA en el borde (clausula
4). Un pool compartido `map-shared` solo se escribe via Tier 1 con capability `engram_shared`.

### 4. Identidad de autor con ENFORCEMENT en el borde + cero-prosa estructural en el ledger. [ESTRUCTURAL para Tier 1 - cierra blocker E y degrada blocker B]

El Analista demostro que en Engram **proyecto/scope son seleccion/filtro, no identidad** (`DOCS.md:692`,
`docs/TEAM-USAGE.md:22-30`): `map-codex` es **mera convencion** salvo que algo imponga `actor ->
memory_project`. Engram **no lo impone**. Fix estructural en NUESTRO borde (no en Engram): `submit_intent`
ya conoce el **actor autenticado/firmado** (`actor_id`, con su binding `binding_slug(actor_id)` ->
`actor_keyid`). El intent `engram_observation` se valida server-side dentro de `validate_intent`
(`runtime/submit_intent.py:662`), unico chokepoint que cubre el camino single y el `--intents` (PATCH v2 sec.2).
Cuatro garantias:

- **(a) Escrituras per-agente enforced [ESTRUCTURAL-PENDIENTE-IMPL+TESTS; binding anti-typo, anti-impersonacion SOLO SI actor_auth_enforce atestado, ver 4-bis]:** `memory_project` **DEBE** ser exactamente
  `"map-" + binding_slug(actor_id)`; el actor `Analista` solo puede emitir a `map-analista`; cualquier otro
  valor se rechaza con `IntentValidationError`. La identidad pasa de convencion a enforcement del valor
  contra el `actor_id`. **Precondicion (4-bis):** que ese `actor_id` no sea spoofable exige
  `actor_auth_enforce=true` en el plano atestado, hoy ausente -> hoy esto atrapa el typo/mismatch
  (estructural), no la impersonacion (disciplinario). Pendiente de codigo+test (PATCH I7).
- **(b) Pool compartido gated [ESTRUCTURAL-PENDIENTE-IMPL+TESTS]:** `map-shared` requiere capability explicita `engram_shared`
  en el `agent_registry`; sin ella se rechaza. "Memoria compartida" no es free-for-all: es autorizacion
  nominal, single-writer, atestada.
- **(c) Cero PROSA en el ledger [ESTRUCTURAL-PENDIENTE-IMPL+TESTS]:** el evento `engram_observation` lleva
  UNICAMENTE campos de una allowlist cerrada, Y cada campo admitido esta regimentado por valor (enum o
  regex), no solo por nombre: `topic_key` (slug regex, NO prosa), `mem_type` (enum cerrado), `memory_project`
  (slug regex `map-*`), `content_sha256` (hex), **`scope` (enum {project, personal})**, opcional **`task_id`
  (regex `^TASK-[0-9]+$`)** y **`supersedes` (slug topic_key o id de observacion)**. El campo **`title`
  (texto libre) SE ELIMINA del evento por completo** (vive SOLO en Engram, junto al cuerpo). El control es
  por **ALLOWLIST de campos** (rechaza CUALQUIER campo fuera del conjunto), no blacklist. **Honestidad (fix
  de la verificacion adversarial):** la allowlist sola NO bastaba -- v2 dejaba `scope`/`task_id`/`supersedes`
  como strings libres, y el contraejemplo `scope="persona@example.com NIT 900123456"` con `content_sha256`
  valido AUN pasaba. v3 los regimenta por enum/regex (PATCH sec.2.2/sec.2.4), de modo que NINGUN campo admite prosa
  por valor. SOLO ENTONCES "cero-PROSA en el evento" es estructural; mientras el PATCH no este merged con su
  test `test_engram_rejects_prose_in_admitted_fields` verde, es estructural POR DISENO, PENDIENTE. El cuerpo
  se ata por hash (principio "sujeto por hash, plano estructural" de DECISION-0040). No se afirma cero-PII
  absoluto: solo cero-PROSA-LIBRE (la PII semantica corta dentro de un slug acotado queda DISCIPLINARIA, (d)).
- **(d) Honestidad de planos:** el enforcement (a)-(c) es ESTRUCTURAL para todo lo que pasa por el ledger
  (Tier 1, el plano compartido/atestado que importa). En **Tier 0** local (fuera de `submit_intent`) un
  agente puede escribir su SQLite con cualquier `memory_project`; ahi el aislamiento es **[DISCIPLINARIO]**
  (DB local separada), y asi se declara, no se disfraza. **RESIDUAL DISCIPLINARIO:** el TEXTO de `topic_key`
  (slug acotado, sin espacios/prosa) aun podria codificar un dato corto sensible (p.ej. un NIT como token);
  eso es disciplinario residual y se vuelve refuerzo defensa-en-profundidad con ENG-TOPICKEY-PII (NO
  condicion previa, porque la garantia estructural de cero-PROSA no depende de el). No se sobre-afirma
  cero-PII absoluto: solo **cero-PROSA-LIBRE estructural**.

### 4-bis. El autor que Engram no tiene en la observacion, el LEDGER si lo tiene. [ESTRUCTURAL-SI-PRECONDICION(actor_auth_enforce atestado)]

Como las observaciones `mem_save` de Engram no llevan autor (premisa P1 corregida), el autor de una memoria
compartida NO se delega a Engram: queda en el evento `intent.applied` del ledger, cuyo campo `actor`
(`runtime/submit_intent.py`) lo fija el runtime a partir de `actor_id`. El namespacing
`memory_project == "map-"+binding_slug(actor_id)` enforzado en `validate_intent` (clausula 4(a)) **SI es
estructural** y atrapa cualquier `memory_project` que no corresponda al `actor_id` declarado.

**PRECONDICION declarada (corrige el overclaim de v2):** la afirmacion "autor criptograficamente atado
(ed25519), no spoofable" es estructural **SOLO SI `actor_auth_enforce=true`**. Ese flag HOY **no esta en el
`protocol.config.json` atestado**: vive en el override runtime gitignored (`eventlog.py:294-296`,
`actor_auth_enforce_enabled` lo lee del override). Por tanto HOY `ensure_attested_actor_key_binding`
(`submit_intent.py:778-779`) hace **early-return no-op** y `--actor-id` (`submit_intent.py:1236`) es
**spoofable**. Conclusion honesta: el binding `map-<actor>` es **anti-typo/anti-mismatch (atrapa el error
honesto)**, NO anti-impersonacion, mientras `actor_auth_enforce` no este activo. Para que la autoria sea
estructural contra impersonacion en Tier 1 hay que **promover `actor_auth_enforce` al plano atestado**
(tarea ENG-ACTORAUTH-ATTEST). Hasta entonces, la atribucion firmada es **DISCIPLINARIA contra un actor
malicioso** y estructural solo contra el error de buena fe.

### 4-ter. Single-writer + consistencia eventual honesta (outbox/ack), no atomicidad ledger<->Engram. [ESTRUCTURAL en el ledger; el evento atesta SOLICITUD, no "memoria registrada" - corrige blocker C]

v1 decia que el runtime hace el `mem_save` "despues de que la transaccion aterrice". El Analista refuto:
eso preserva un solo escritor del **ledger**, pero **no la atomicidad ledger+memoria** (dos fases: ledger
OK y `mem_save` falla -> el ledger atestaria una memoria inexistente = atestacion fantasma). El ledger #4 y
el SQLite de Engram NO comparten frontera transaccional. v2 corrige la **semantica** y el **mecanismo**:

- Ningun agente escribe un pool compartido de Engram directamente; la memoria compartida pasa por
  `submit_intent` como `engram_observation`. **[ESTRUCTURAL: el ledger es single-writer, orden total.]**
- **Semantica honesta del evento:** un `engram_observation` aplicado atesta el **COMPROMISO durable y
  ordenado de registrar una memoria** (`topic_key` + `content_sha256` + metadato), **NO** que el cuerpo ya
  exista en Engram. El propio evento `intent.applied` ES el registro **outbox**: durable, secuenciado
  (`seq`), firmado y direccionado por contenido.
- **Outbox durable + ACK + reconciliador (tarea diferida ENG-BRIDGE/ENG-RECONCILE, condicion previa a
  activar Tier 1):** el `engram_bridge` es un **consumidor idempotente** del outbox que lee los
  `engram_observation` aplicados, hace el `mem_save` real leyendo el CUERPO desde el markdown-en-git
  atestado (no de buffer volatil), verifica `sha256(cuerpo)==content_sha256`, y SOLO tras exito marca el
  evento como consumido (**ACK**) en una tabla lateral FUERA del ledger atestado
  (`runtime/state/engram_ack.json`, no commiteada, reconstruible) para no introducir drift. Un
  **reconciliador** (`engram_reconcile.py`) detecta las anomalias *ledger-sin-memoria* y *memoria-sin-ledger*
  por `content_sha256`, reintenta con backoff y reporta los irreconciliables como anomalia DECISION-0018.
- **Honestidad explicita: el ledger atesta intencion/compromiso con consistencia eventual via healer, NO
  existencia inmediata en Engram.** *[ESTRUCTURAL: outbox+reconciliador garantizan convergencia bajo el
  supuesto de que Engram acaba estando disponible. DISCIPLINARIO-RESIDUAL: que un futuro doc no vuelva a
  sobre-afirmar "ya integrado".]* El bridge y el reconciliador son DIFERIDOS, por lo que **C-atomicidad
  queda ESPECIFICADO pero ABIERTO** -- no se promueve Tier 1 hasta cerrarlo.

### 5. ACTIVACION DE TIER 1 = GATE ESTRUCTURAL ATESTADO (no diferimiento documental). [corrige blocker A]

v1 dejaba el diferimiento de Tier 1 como **prosa** (clausula documental) y un "gate" que releia
`event-state.runtime.json -> {engram:{enabled}}` de forma ad-hoc. El Analista refuto: el flag no existia en
codigo, el lector paralelo bypassaba el loader atestado, no habia precondicion verificable de "dataset
sellado", y nada impedia que un agente lo encendiera durante la captura -> **diferimiento DISCIPLINARIO, no
gate real**. (Causa raiz verificada: el loader central `event_state_runtime_override`,
`runtime/eventlog.py:243-277`, aplica un **allowlist estricto** -- solo
`event_state.{actor_auth_enforce, actor_auth_config, event_auth}` -- y rechaza cualquier otra clave; meter
`engram` ahi lo deja ignorado o rompe el runtime.) v3 ata el flag al **plano atestado**
`protocol.config.json -> event_state.engram.enabled` (ausente o `false` por defecto), JUNTO a
`enabled/materialize/enforce/authoritative` y bajo su misma guardia de configuracion. El diseno es
estructuralmente solido y los anclas verifican, PERO no hay codigo merged ni tests ejecutados: lo de abajo
es **estructural POR DISENO, PENDIENTE de implementacion+tests verdes** (ver Matriz de estado y seccion H).
TRES garantias, con su etiqueta y precondicion:

- **5.1 GATE ENFORCED [ESTRUCTURAL-PENDIENTE-IMPL+TESTS; el diseno verifica, el codigo no esta merged].**
  Con el flag ausente/`false`, todo intent `engram_observation` se RECHAZA en `validate_intent`
  (`runtime/submit_intent.py:662`), que corre por-intent tanto en el camino single (`submit_intent.py:999`)
  como en cada intent de `--intents` (via `validate_transaction`, `submit_intent.py:524-539`); un
  `engram_observation` apagado dentro de una transaccion aborta TODA la transaccion (rollback existente). El
  chokepoint es unico y el ancla verifica. **Honestidad (corrige el overclaim de v2):** NO esta "probado" --
  los tests negativos del PATCH sec.5 son a ESCRIBIR; `grep engram_* runtime/*.py` = 0 hits. Sube a ESTRUCTURAL
  cuando el PATCH se mergee con esos tests verdes en clon limpio. **Precondicion de tier:** la capacidad
  exige `adoption_tier=='runtime'` (ver 5.3); en coordination-tier el gate queda OFF y el cierre baja a
  disciplinario.
- **5.2 FLIP ATESTADO, NO EDITABLE A MANO [ESTRUCTURAL-SI-PRECONDICION(chain_enabled=true); diseno verificado, impl pendiente].** Como `compute_genesis_prev_hash`
  (`runtime/eventlog.py:185-189`) hashea el `protocol.config.json` COMPLETO dentro del `prev_hash` del
  genesis #4, y `validate_chain` (`runtime/protocol_replay.py:161-171`) rechaza un genesis con hash distinto,
  encender `event_state.engram.enabled` MUTA el hash del config y ROMPE la cadena #4 salvo re-genesis
  coordinado (`runtime/regenesis.py`). El flip es atestado por construccion: un agente NO puede encenderlo
  con una edicion silenciosa sin invalidar el ledger. Reaprovecha el mecanismo existente (no inventa teeth
  nuevos), igual que el guard `authoritative=>enforce=>...` de TASK-0086. **PRECONDICION declarada:** depende
  de `chain_enabled=true` (lo esta: `protocol.config.json` verificado `chain_enabled=true`); en una instancia
  con cadena #4 apagada, editar el flag no rompe nada -> alli baja a **DISCIPLINARIA**. El ancla verifica el
  diseno; la prueba estructural (`test_config_flip_breaks_chain_without_regenesis`, PATCH I10) esta pendiente
  de escribir.
- **5.3 PRECONDICION 'DATASET SELLADO' [ESTRUCTURAL-SI-PRECONDICION(adoption_tier=='runtime'); el JUICIO del corte es DISCIPLINARIO].** Encender
  `event_state.engram.enabled=true` REQUIERE, por hard-gate de configuracion, que exista
  `event_state.engram.dataset_seal` como objeto no vacio con `{seal_commit, seal_event_seq, sealed_at}`. La
  verificacion la anade `event_state_config_error` (`runtime/protocol_replay.py:125`), que ya corre al inicio
  de cada `submit_intent` (via `ensure_event_state_config_valid`, `submit_intent.py:810`) y en los
  validadores py/ps. **PRECONDICION DE TIER no declarada en v2, ahora explicita:** `event_state_config_error`
  retorna `None` si `adoption_tier != "runtime"` (`protocol_replay.py:127`) -> el guard `dataset_seal` es
  **INERTE en coordination-tier**. Por eso `engram_capability_enabled` debe exigir tambien
  `adoption_tier=='runtime'` (PATCH sec.2.3): asi la capacidad solo enciende donde el seal tiene dientes, y el
  cierre estructural de A/seal vale **SOLO en runtime-tier** (esta instancia lo es); en coordination-tier baja
  a DISCIPLINARIO y la capacidad queda OFF. **LO QUE NO ES ESTRUCTURAL (DISCIPLINARIO, espejo DECISION-0040
  plano 1):** que el `seal_event_seq`/`seal_commit` representen un dataset N=500 congelado y veraz es JUICIO
  del operador; el gate verifica que SE DECLARO un seal atestado, no que el dataset este "realmente
  terminado". La autoridad de poblar `dataset_seal` y hacer el re-genesis es del OPERADOR (los agentes no
  tienen capability de re-genesis y un flip por edicion rompe la cadena), lo que satisface "politica de
  activacion no accesible por agentes durante la captura". Codigo+test pendientes (PATCH I9).
- **5.4 TIER 0 sin cambios:** vive fuera del ledger, no toca el dataset, permitido desde ya.

### 6. DECISION-0026 - mejora de mecanismo, regla intacta. [DISCIPLINARIO, sin cambio de garantia]

Tras cada commit, la actualizacion de memoria PUEDE registrarse ademas via Engram `mem_save` (formato
What/Why/Where/Learned; `Where` = commit SHA; `mem_type` neutral; `topic_key` estable) en el proyecto
`map-<id>` del agente. La regla de oro NO cambia; el markdown-en-git sigue siendo el registro durable. El
conflict-surfacing (`mem_judge`) ayuda a SUPERFICIAR (no resolver) la memoria obsoleta. Esto es Tier 0
(local), sin impacto en ledger/dataset.

## Alcance / No-alcance

- **En alcance (definido en esta DECISION, con matriz de estado honesta; NADA "cerrado"):** frontera
  ledger/memoria con planos estructural/disciplinario declarados; capacidad OFF by default con gate;
  **namespacing `memory_project == "map-"+binding_slug(actor_id)` en `validate_intent`** (anti-typo
  estructural; anti-impersonacion SOLO SI `actor_auth_enforce` atestado, E); `map-shared` tras capability
  `engram_shared`; `engram_observation` como via single-writer (ledger lleva slug+hash+enum, **sin `title`
  ni cuerpo**, con `scope`/`task_id`/`supersedes` regimentados -> cero-PROSA, B); **activacion de Tier 1 como
  gate de configuracion atestado por el #4, valido SOLO en runtime-tier** (A); mejora de mecanismo de
  DECISION-0026. Todos estos son **ESTRUCTURAL-PENDIENTE-IMPL+TESTS** o **ESTRUCTURAL-SI-PRECONDICION** hasta
  que el PATCH se mergee con tests verdes.
- **En alcance (ABIERTO-DIFERIDO, tarea aparte):** consistencia eventual outbox/ACK/reconciliador y el
  puntero `body_ref` al cuerpo (C); reconstruibilidad markdown->Engram con test (D); suite completa de tests
  + rollback en clon limpio + espejo PowerShell (H); promocion de `actor_auth_enforce` al plano atestado
  (precondicion de E anti-impersonacion).
- **Fuera de alcance:** activar Tier 1 ahora; afirmar reconstruibilidad automatica markdown->Engram (bajada
  a cache no autoritativa); sustituir el markdown-en-git como fuente de verdad; meter `title`/cuerpo en el
  event log; commitear `.engram/` por defecto (Tier 2); introducir terminos de dominio (los `map-*` y
  `mem_type` son neutrales); cualquier publicacion/citacion del dataset (sigue bajo GATE-DATASET + GATE-INST
  + PRE-REG).

## Consecuencias

- Se habilita YA el recall per-agente (Tier 0) sin riesgo: arranque frio con `mem_context` en vez de grep.
  Sin impacto en ledger/dataset/TFM. *[Tier 0 aislamiento = DISCIPLINARIO.]*
- El protocolo gana una via atestada, single-writer y **con namespacing de autor enforced en el borde** para
  memoria compartida cuando se active (Tier 1), con el `title` Y el cuerpo fuera del log (cero-PROSA por
  diseno). **Honestidad:** el namespacing es anti-typo estructural; contra impersonacion requiere
  `actor_auth_enforce` atestado (hoy en override gitignored -> disciplinario), declarado como precondicion.
- La activacion de Tier 1 deja de ser una promesa documental: el diseno la ata a un gate de configuracion
  atestado por el #4 (5.1-5.3), **valido SOLO en runtime-tier** (en coordination-tier el guard del seal es
  inerte). **Honestidad:** el seal verifica DECLARACION atestada, no veracidad semantica del corte del
  dataset (eso es operador, DISCIPLINARIO); y el mecanismo es diseno, no codigo merged.
- **HONESTIDAD (anti sobre-afirmacion):** este diseno NO afirma que el cache de Engram sea reconstruible hoy
  (DoD de ENG-IMPORT = test round-trip verde); ni "ya integrado"; ni "cero PII estructural total" (solo
  cero-PROSA). La unica garantia durable es markdown-en-git; Engram es recall best-effort.
- **HONESTIDAD (estado de cierre, v3):** NADA se declara cerrado. La Matriz de estado honesta v3 (al final)
  da la etiqueta exacta por bloqueante. En resumen: A/B/E/H tienen **diseno estructural verificado pero SIN
  codigo merged ni tests ejecutados** (ESTRUCTURAL-PENDIENTE-IMPL+TESTS), algunos con precondicion
  (runtime-tier para A; `chain_enabled` para el flip; `actor_auth_enforce` atestado para E
  anti-impersonacion). **C-atomicidad** (bridge/outbox/reconciliador + puntero `body_ref`) y
  **D-reconstruccion** (importador con test) quedan **ABIERTO-DIFERIDO**. **Prohibido afirmar "ya integrado",
  "cerrado" o "probado".**
- Dependencia de un binario externo (Go) acotada a una capacidad opcional; el markdown sigue como registro
  durable y atestable (Engram nunca es la verdad).

## Frontera DECISION-vs-PATCH (H = SPEC, no codigo merged)

Esta DECISION se registra con la capacidad **OFF** y NO requiere que el PATCH este implementado: grabar la
decision (capability OFF by default, con su matriz de estado honesta) es independiente de mergear el
mecanismo. El PATCH (intent `engram_observation`) solo entra a `main` cuando los tests I1..I10 esten verdes
en **clon limpio**, incluido el rollback en transaccion `--intents` (I6), el cero-drift por hash (I2) y por
replay (I3), el rechazo de prosa en `scope`/`task_id`/`supersedes` (I4), el rechazo en coordination-tier, el
espejo PowerShell del guard `dataset_seal`, y la prueba de que el flip rompe la cadena sin re-genesis (I10).
**La DECISION esta en estado "mechanism specified, not merged"; esto es coherente con que ningun bloqueante
de la Matriz se etiquete "cerrado": A/B/E/H son estructural POR DISENO y suben de nivel solo al mergear con
tests verdes. Prohibido afirmar "ya integrado", "cerrado" o "probado".**

## Tareas diferidas (condicion de activacion, NO bloqueo de promover el mecanismo INERTE)

Se registran como tareas con fecha (se formalizan en `TASK_INDEX` al promover; NO se construyen ahora). La
frontera DECISION-vs-PATCH permite registrar esta DECISION con la capacidad OFF sin que esten implementadas:

- **ENG-FLAG-WIRING (Codex):** flag en `protocol.config.json -> event_state.engram.{enabled,dataset_seal}`
  (default ausente=false) + capability `engram_shared` en el `agent_registry`; gate en `validate_intent`;
  guard `dataset_seal` en `event_state_config_error` (py) + espejo en `validate_collaboration_state.ps1` +
  tests en clon limpio. Default OFF. NO enciende nada.
- **ENG-OUTBOX / ENG-BRIDGE (bloqueante C, condicion previa a Tier 1):** `runtime/engram_bridge.py`
  consumidor idempotente del outbox; lee `engram_observation` aplicados sin ACK, hace `mem_save` real
  leyendo el CUERPO desde el markdown-en-git atestado, verifica `sha256(cuerpo)==content_sha256`, escribe
  ACK atomico en `runtime/state/engram_ack.json` solo tras exito; nunca escribe el ledger; idempotente por
  `content_sha256`. **HUECO DE DISENO ABIERTO en C:** el evento `engram_observation` NO lleva puntero al
  archivo/ancla markdown cuyo `content_sha256` atesta -> el bridge no puede localizar el cuerpo. La spec debe
  anadir a la allowlist un campo **`body_ref`** (ruta repo-relativa validada como **slug de path**, NO prosa)
  o declarar el direccionamiento del cuerpo como punto de diseno ABIERTO a resolver antes de Tier 1.
- **ENG-ACTORAUTH-ATTEST (precondicion de E anti-impersonacion):** promover `actor_auth_enforce` (hoy solo en
  el override runtime gitignored, `eventlog.py:294-296`) al plano atestado `protocol.config.json`, de modo
  que `ensure_attested_actor_key_binding` deje de ser no-op y `--actor-id` no sea spoofable. Sin esta tarea,
  el namespacing `map-<actor>` (clausula 4(a)) es anti-typo (estructural) pero NO anti-impersonacion
  (disciplinario). Condicion para que E sea estructural contra un actor malicioso en Tier 1.
- **ENG-RECONCILE (bloqueante C):** `runtime/engram_reconcile.py` healer "atestado-pero-ausente"; detecta
  `engram_observation` aplicados sin ACK o con `content_sha256` ausente en el pool destino, reintenta con
  backoff, reporta irreconciliables como anomalia DECISION-0018. Cierra el lazo de consistencia eventual.
- **ENG-ACK-GITIGNORE:** anadir `runtime/state/engram_ack.json` a `.gitignore`; documentar que es tabla
  lateral reconstruible, NO fuente de verdad ni state de protocolo (no afecta drift B.3 / I2).
- **ENG-IDENTITY (complemento de E):** enforcement server-side `actor -> memory_project` en el propio
  `engram_bridge` (que el `mem_save` real respete `map-<id>`); el namespacing en el borde ya esta enforced
  (clausula 4 (a)/(b)).
- **ENG-IMPORT / ENG-RECONSTRUCT (bloqueante D):** `runtime/engram_import.py` importador determinista
  `personal/<id>/*.md` + runbook -> Engram + esquema canonico de memoria en markdown. DoD = test round-trip
  de ACEPTACION verde. SOLO al pasar este test la DECISION puede afirmar reconstruibilidad; hasta entonces,
  clausula 1 la mantiene como "cache no autoritativa, no reconstruible automaticamente".
- **ENG-TOPICKEY-PII (refuerzo opcional, defensa en profundidad, NO bloqueante):** al eliminar `title`, el
  unico texto restante es `topic_key`, ya restringido a slug por regex (estructural). Validador adicional
  que rechace patrones tipo-identificador-sensible (NIT, secuencias numericas largas) dentro de `topic_key`.
  Los ejemplos de PII de dominio (NIT, razon social, SQL Budget) van a perfil/instancia (neutralidad del
  Core, blocker G). Reemplaza/degrada el ENG-PII de v1 que apuntaba a `title` (campo ahora eliminado).
- **ENG-MERGE-SEMANTIC (diferida, condicionada a activar `map-shared`):** politica de conciliacion de
  memorias CONTRADICTORIAS entre agentes (que Engram superficia con `mem_judge` pero no resuelve) antes de
  habilitar cualquier `map-shared` multi-escritor logico via Tier 1.
- **ENG-REGENESIS-RUNBOOK (operador):** runbook del flip Tier 1 = poblar `event_state.engram.dataset_seal`
  con `seal_commit`/`seal_event_seq`/`sealed_at` del corte real del dataset + re-genesis coordinado
  (`regenesis.py`) + rollback ensayado; documentar que en instancias con `chain_enabled=false` la garantia
  (5.2) baja a disciplinaria.
- **Re-review Analista del DRAFT v2 + PATCH v2:** verificar (a) las 2 premisas inexactas corregidas vs
  fuente primaria, (b) I4 es allowlist no blocklist y `title` eliminado, (c) la separacion DECISION-OFF vs
  PATCH-merge no sobre-afirma integracion, (d) A-activacion estructural y E-identidad enforced, (e) C/D/H
  siguen declarados abiertos.

## Alternativas consideradas

- **Dejar que los agentes escriban Engram compartido directamente.** Descartada: reintroduce multi-writer
  (viola DECISION-0020); sin autor en las observaciones, sin locks, y sin resolucion del merge de memorias
  contradictorias -> colision/divergencia silenciosa entre pools.
- **`map-<id>` solo por convencion (v1).** Descartada por el NO-GO: convencion != enforcement. v2 lo ancla
  a `"map-"+binding_slug(actor_id)` en `validate_intent`.
- **`title` libre con blacklist de cuerpo (v1, I4).** Descartada: disciplinario disfrazado de estructural;
  v3 ELIMINA `title`, usa allowlist de campos Y regimenta por valor `scope`/`task_id`/`supersedes` -> cero-prosa
  estructural por diseno (pendiente de impl+tests).
- **Afirmar reconstruibilidad markdown->Engram (v1).** Descartada: no existe el importador; v2 baja la
  afirmacion a cache no autoritativa (ENG-IMPORT diferido con test).
- **Bridge dos-fases sin outbox (v1).** Descartada: no es atomico (atestacion fantasma); v2 define
  outbox/ACK/reconciliador y semantica "compromiso, no existencia".
- **Gate de activacion como prosa/flag gitignored (v1).** Descartada: el lector paralelo de v1 sobre
  `event-state.runtime.json` bypassa el loader atestado (allowlist estricta de
  `event_state_runtime_override`, `eventlog.py:243-277`) -> flip invisible al #4, "documental, no gate
  real". v2 ata el flag al `protocol.config.json` hasheado en el genesis (estructural).
- **Meter el cuerpo en el event log.** Descartada: superficie de PII; el hash basta para atestar.
- **Sustituir el markdown por Engram como fuente de verdad.** Descartada: el DB local no esta en git.
- **Activar Tier 1 ya.** Descartada: cambia el instrumento del dataset a mitad de captura; el gate de
  activacion estructural (clausula 5) lo bloquea hasta el re-genesis con `dataset_seal` autorizado por el
  operador, y antes hay que cerrar C/D/H.

## Matriz de estado honesta v3 (respuesta a la verificacion adversarial)

> Etiquetas exactas: **ESTRUCTURAL** (enforced por codigo merged + tests verdes) | **ESTRUCTURAL-PENDIENTE-IMPL+TESTS**
> (diseno verificado por anclas, sin codigo merged ni tests ejecutados) | **ESTRUCTURAL-SI-PRECONDICION(<cual>)** |
> **DISCIPLINARIO** | **ABIERTO-DIFERIDO**. Nada se etiqueta "cerrado/probado". Codigo: `grep engram_* runtime/*.py` = 0 hits.

| Bloqueante | Etiqueta de estado | Que falta para subir de nivel | Donde |
|---|---|---|---|
| **A-activacion** (gate de activacion de Tier 1) | **ESTRUCTURAL-SI-PRECONDICION(adoption_tier=='runtime')** por diseno, **PENDIENTE-IMPL+TESTS** | Mergear el gate en `validate_intent` + el guard `dataset_seal` en `event_state_config_error` + `engram_capability_enabled` exigiendo `adoption_tier=='runtime'`; tests I1/I9 + `test_engram_off_in_coordination_tier` verdes en clon limpio. En coordination-tier el guard es inerte (`protocol_replay.py:127`) -> alli baja a DISCIPLINARIO. | Decision 5.1-5.4; PATCH sec.2.3 (gate+tier), sec.3b (seal), sec.5 |
| **A-flip** (no editable a mano) | **ESTRUCTURAL-SI-PRECONDICION(chain_enabled=true)** por diseno, **PENDIENTE-IMPL+TESTS** | Test `test_config_flip_breaks_chain_without_regenesis` (I10) verde. Bajo `chain_enabled=false` baja a DISCIPLINARIO (declarado). Ancla `compute_genesis_prev_hash` (eventlog.py:185-189) verifica el diseno. | Decision 5.2; PATCH sec.0.1(2), I10 |
| **B-cero-prosa-libre** (PII semantica corta en slug = DISCIPLINARIO; NO es "B-PII") | **ESTRUCTURAL-PENDIENTE-IMPL+TESTS** -- y SOLO cero-PROSA-LIBRE; la garantia NO cubre PII corta | FIX REAL (cierra prosa libre, NO PII corta): ademas de eliminar `title` y usar allowlist de campos, se regimentan por valor los 3 campos que aun admitian prosa -- `scope` enum {project,personal}, `task_id` regex `^TASK-[0-9]+$`, `supersedes` slug/id. Falta mergear + `test_engram_allowlist_rejects_body` y `test_engram_rejects_prose_in_admitted_fields` verdes. RESIDUAL EXPLICITO (verificacion adversarial TASK-0220): un identificador corto tipo `nit-900123456` PASA el slug regex de `topic_key`/`supersedes` -> PII semantica corta entra; eso es DISCIPLINARIO, no estructural (leccion DECISION-0040). Subir a estructural exige ENG-TOPICKEY-PII (guard de patrones PII corta), DIFERIDO. | Decision 4(c)/(d); PATCH sec.2.2, sec.2.4, I4, sec.5 |
| **C-atomicidad** | **ABIERTO-DIFERIDO** | Construir ENG-OUTBOX/ENG-BRIDGE (consumidor idempotente + ACK fuera del ledger) + ENG-RECONCILE (healer). **Hueco de diseno abierto:** el evento no lleva `body_ref` al cuerpo cuyo sha256 atesta -> el bridge no puede localizarlo; anadir `body_ref` (slug de path) o declararlo punto abierto. El ledger atesta COMPROMISO, no existencia. | Decision 4-ter; PATCH sec.7, sec.8; tareas ENG-OUTBOX/ENG-BRIDGE, ENG-RECONCILE |
| **D-reconstruccion** | **ABIERTO-DIFERIDO** | Construir ENG-IMPORT (`engram_import.py`) + esquema canonico markdown; DoD = test round-trip verde. Hasta entonces Engram es cache no autoritativa, NO reconstruible (clausula 1). | Decision clausula 1, Consecuencias; tarea ENG-IMPORT/ENG-RECONSTRUCT |
| **E-identidad** | **ESTRUCTURAL-PENDIENTE-IMPL+TESTS** (anti-typo) / **ESTRUCTURAL-SI-PRECONDICION(actor_auth_enforce atestado)** (anti-impersonacion) | El namespacing `memory_project=="map-"+binding_slug(actor_id)` en `validate_intent` es estructural por diseno (falta merge + test I7). PERO el binding ed25519 es no-op hoy: `actor_auth_enforce` vive en el override runtime gitignored (`eventlog.py:294-296`), no en el config atestado -> `--actor-id` spoofable. Promover `actor_auth_enforce` al plano atestado (ENG-ACTORAUTH-ATTEST) para que sea anti-impersonacion. | Decision 4(a)/(b), 4-bis; PATCH sec.2.5, I7; tarea ENG-ACTORAUTH-ATTEST |
| **H-parche** (suite + chokepoint unico + config) | **ESTRUCTURAL-PENDIENTE-IMPL+TESTS** | Enforcement en el chokepoint unico `validate_intent` (cubre single + `--intents`) y flag en el plano atestado: diseno verificado. Falta mergear y dejar verde toda la suite I1..I10 + espejo PowerShell del guard + scans de neutralidad/encoding en clon limpio. | Decision 5.1 + Frontera DECISION-vs-PATCH; PATCH sec.1, sec.5, sec.6, sec.7 |
| **PREMISA P1** ("sin campo de autor") | corregida (exacta vs fuente `44faeee`) | -- ya fijada: observaciones `mem_save` sin autor (`DOCS.md:46/136`); `memory_relations` con `marked_by_actor` (`DOCS.md:51`). | Contexto "Autor (P1, exacto)"; clausulas 3, 4-bis |
| **PREMISA P2** ("no documenta merge") | corregida (exacta vs fuente `44faeee`) | -- ya fijada: chunks append-only "no merge conflicts" SI documentado; lo no resuelto es el merge SEMANTICO de memorias contradictorias (ENG-MERGE-SEMANTIC). | Contexto "Merge (P2, exacto)"; Alternativas; tarea ENG-MERGE-SEMANTIC |
