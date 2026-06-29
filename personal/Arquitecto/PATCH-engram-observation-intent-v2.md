# PATCH SPEC v3 -- intent `engram_observation` (submit_intent.py + protocol_replay.py)

> Autor: Arquitecto - Estado: SPEC para Codex (NO implementado: `grep engram_* runtime/*.py` = 0 hits;
> tests §5 a escribir, no ejecutados) - v3 tras la VERIFICACION ADVERSARIAL de v2 (corrige overclaims y el
> fix real de B: 3 campos admitidos -- scope/task_id/supersedes -- aun admitian prosa).
> No toca ledger al redactarse (vive en `personal/`). Nada aqui se declara "cerrado" ni "probado".
> Depende de: DRAFT-DECISION-engram-memory-backend (capability OFF by default).
> Alcance EXACTO del parche: `runtime/submit_intent.py` + `runtime/protocol_replay.py` +
> `scripts/validate_collaboration_state.ps1` (espejo del guard) + tests.
> NO incluye `engram_bridge`/outbox/ack/reconciliador (tarea aparte ENG-BRIDGE/ENG-RECONCILE, ver §8).
>
> **Anclas verificadas contra HEAD (`submit_intent.py`):** `INTENT_TYPES` linea 84; `normalize_intent`
> 317-389 (la rama `decision` es el fall-through final 386-389); `required_scopes` 592-621;
> `validate_scope_authority` 645-659; `validate_intent` 662-746; `binding_slug` 755-760;
> `aggregate_id_for` 399-408; `event_payload_for` 411-462; camino single valida en `validate_intent`
> (linea 999) y la transaccion en `validate_transaction` que **llama `validate_intent` por intent**
> (linea 524-539, llamada en 536); `ensure_event_state_config_valid` 810-814. `apply_intent_event`
> 881-930; routing replay 965-966.
> **Anclas verificadas contra HEAD (`protocol_replay.py`):** `event_state_*_enabled` 100-122;
> `event_state_config_error` 125-152; `validate_chain` / genesis-hash mismatch 155-171.
> **Anclas verificadas contra HEAD (`eventlog.py`):** `compute_genesis_prev_hash` 185-189;
> `event_state_runtime_override` allowlist estricta 243-277 (solo
> `event_state.{actor_auth_enforce, actor_auth_config, event_auth}`).

## 0. Que se quiere lograr (intencion, leer antes de tocar codigo)

Anadir el intent `engram_observation` que **atesta en el ledger #4 el COMPROMISO durable y ordenado de
registrar una memoria** (consistencia eventual, NO existencia inmediata en Engram), SIN:
- mutar el state materializado (`CLAIMS.json`/`TASK_INDEX.json`/`PROJECT_STATE.json`),
- meter el CUERPO ni el `title` (texto libre) de la memoria en el event log,
- romper single-writer ni la atomicidad de `submit_intent --intents`,
- aceptar un `memory_project` que no corresponda al actor firmado,
- permitir que la activacion de Tier 1 sea un toggle local silencioso no atestado.

El ledger lleva solo **metadato de allowlist (slug + enum) + `content_sha256`**, NUNCA texto libre. El
cuerpo Y el `title` viven en Engram, fuera de banda. El evento `intent.applied` resultante ES el registro
**outbox** que un `engram_bridge` idempotente consume con **ACK** fuera de banda, y un reconciliador healer
cierra el lazo (ver §8). El ledger NO afirma que el cuerpo ya este en Engram.

### 0.1 -- Arquitectura del enforcement frente a v1 (cierra blockers H, A, B)

Tres correcciones de arquitectura frente a v1:

1. **Chokepoint unico (H):** v1 ponia el gate en una "pasada de aplicacion" separada y NO lo mostraba en
   ambos caminos. v2 mueve TODO el enforcement (gate de capacidad + identidad + scope) DENTRO de
   `validate_intent`, unico punto que cubre el camino single (linea 999) y el `--intents`
   (`validate_transaction` lo llama por intent, linea 536). `validate_intent(root, actor_id, normalized,
   ...)` ya recibe `root` (para el gate) y `actor_id` (la identidad firmada): no hace falta cablear nada
   nuevo y un `engram_observation` con la capacidad OFF aborta toda la transaccion por rollback existente
   (I1 + I6).
2. **Flag en el plano ATESTADO (A):** v1 leia `event-state.runtime.json -> {engram:{enabled}}` con un
   reader paralelo (`engram_capability_enabled` ad-hoc). Eso es un **gate roto**: el loader central
   `event_state_runtime_override` (`eventlog.py:243-277`) aplica un **allowlist estricto** y rechaza
   cualquier clave que no sea `event_state.{actor_auth_enforce, actor_auth_config, event_auth}`; meter
   `engram` ahi lo deja IGNORADO o ROMPE el runtime. v2 ata el flag a `protocol.config.json ->
   event_state.engram.enabled`, que esta hasheado en el `prev_hash` del genesis #4
   (`compute_genesis_prev_hash`, `eventlog.py:185-189`); encenderlo MUTA el hash y ROMPE la cadena salvo
   re-genesis coordinado -> **el flip es atestado por construccion, no editable a mano** (5.2 de la
   DECISION).
3. **Allowlist, no blacklist; `title` ELIMINADO (B):** v1 conservaba `title` como texto libre y "protegia"
   con una blacklist (`content/body/...`) burlable. v2 ELIMINA `title` del evento y valida por **allowlist
   de campos** (se rechaza CUALQUIER campo fuera del conjunto cerrado) -> el evento no contiene NINGUN
   campo de texto libre: cero-PROSA **estructural** (no disciplinaria).

## 1. Invariantes de aceptacion (definition of done)

- **I1 (gate ESTRUCTURAL):** con `event_state.engram.enabled` ausente/`false`, un `engram_observation` se
  **rechaza** (`IntentValidationError`, exit != 0). Ningun evento escrito. Cubre single y `--intents`.
- **I2 (cero drift ESTRUCTURAL):** con la capacidad ON, aplicar un `engram_observation` valido deja
  `CLAIMS/TASK_INDEX/PROJECT_STATE` **byte-identicos**. El hard-gate B.3 sigue verde (`has_drift=false`).
- **I3 (replay no-op ESTRUCTURAL):** re-ejecutar el event log con `engram_observation` reproduce el mismo
  state (no-op puro sobre el state).
- **I4 (cero texto libre ESTRUCTURAL):** en `events.jsonl` solo aparecen `topic_key`, `mem_type`,
  `memory_project`, `content_sha256`, `scope` (+ opcional `task_id`, `supersedes`). **`title` NO existe en
  el evento.** Control por **allowlist de campos** (rechaza todo campo no listado), no blacklist; Y CADA
  campo admitido esta regimentado por valor: `topic_key`/`memory_project`/`supersedes` slugs por regex,
  `mem_type` enum, `content_sha256` hex, **`scope` enum {project, personal}**, **`task_id` regex
  `^TASK-[0-9]+$`**. Ningun campo admite prosa libre por valor (cierra el contraejemplo
  `scope="persona@example.com NIT 900123456"`). **Nunca** el cuerpo ni prosa.
- **I5 (idempotencia):** misma `(actor, memory_project, topic_key, content_sha256)` => idempotente, via
  `idempotency_key` existente.
- **I6 (atomicidad):** un `engram_observation` dentro de `--intents` hace rollback con el resto si cualquier
  intent falla (camino transaccional existente).
- **I7 (identidad enforced ESTRUCTURAL, cierra E):** `memory_project` DEBE ser `"map-" + binding_slug(actor_id)`;
  cualquier otro valor se rechaza, **salvo** `map-shared`, que requiere la capability `engram_shared`.
- **I8 (sin claim espurio, corrige bug latente):** `engram_observation` NO requiere ningun claim activo
  sobre rutas del ledger (no toca rutas row-scoped). Un actor sin claims activos puede emitirlo (§2.6).
- **I9 (precondicion dataset_seal ESTRUCTURAL, cierra A):** `event_state.engram.enabled=true` solo es config
  valida si existe `event_state.engram.dataset_seal` = objeto con `{seal_commit, seal_event_seq, sealed_at}`
  no vacios; si no, `event_state_config_error` != None y NINGUN intent corre.
- **I10 (flip atestado ESTRUCTURAL, cierra A):** editar `event_state.engram.enabled` a mano (sin re-genesis)
  invalida el genesis (`validate_chain` reporta hash mismatch). Bajo `chain_enabled=false` esta garantia es
  disciplinaria (declarado).

## 2. `runtime/submit_intent.py`

### 2.1 -- Anadir el tipo a `INTENT_TYPES` (linea 84)
```python
# ANTES
INTENT_TYPES = {"task_status", "task_upsert", "claim", "decision", "project_narrative", "protocol_prune", "mailbox_archive"}
# DESPUES
INTENT_TYPES = {"task_status", "task_upsert", "claim", "decision", "project_narrative", "protocol_prune", "mailbox_archive", "engram_observation"}
```

### 2.2 -- Constantes nuevas (insertar tras `MAILBOX_MESSAGE_ID_RE`, ~linea 86)
```python
ENGRAM_MEM_TYPES = {"decision", "architecture", "bugfix", "pattern", "config", "discovery", "learning"}
ENGRAM_PROJECT_RE = re.compile(r"^map-[a-z0-9][a-z0-9-]{0,62}$")   # map-arquitecto / map-codex / map-shared
ENGRAM_SHARED_PROJECT = "map-shared"
ENGRAM_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ENGRAM_TOPIC_KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,127}$")   # slug, NO prosa libre
ENGRAM_SCOPE_VALUES = {"project", "personal"}                              # enum CERRADO, no prosa
ENGRAM_TASK_ID_RE = re.compile(r"^TASK-[0-9]{1,8}$")                        # id estructurado, no prosa
# supersedes: o un topic_key (slug) o un id de observacion (hex/uuid corto). NUNCA prosa.
ENGRAM_SUPERSEDES_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/:-]{0,127}$")
# allowlist CERRADA de campos del payload: cualquier otro campo => rechazo (I4 estructural).
ENGRAM_ALLOWED_FIELDS = {"type", "kind", "topic_key", "mem_type", "memory_project", "content_sha256", "scope", "task_id", "supersedes", "idempotency_key"}
```
> Decision de diseno (corrige B en su totalidad): v1 dejaba `title` libre y protegia con blacklist. v2
> ELIMINO `title` del evento (vive solo en Engram, junto al cuerpo). Pero la verificacion adversarial cazo
> que con la allowlist sola, 3 campos restantes (`scope`, `task_id`, `supersedes`) AUN admitian prosa libre
> -- contraejemplo intacto: `scope="persona@example.com NIT 900123456"` pasaba la allowlist y aterrizaba en
> `events.jsonl`. v3 cierra el hueco validando los tres por enum/regex (ver §2.4): `scope` ENUM
> {project, personal}; `task_id` regex `^TASK-[0-9]+$`; `supersedes` slug topic_key o id de observacion.
> SOLO con esto "cero-PROSA en el evento" es **ESTRUCTURAL** (allowlist de campos + valor regimentado en
> cada campo, no solo en `topic_key`/`memory_project`). El residual de PII semantica corta dentro de un slug
> acotado (p.ej. un NIT como token en `topic_key`/`supersedes`) es **DISCIPLINARIO** y se cubre con
> ENG-TOPICKEY-PII (opcional, defensa en profundidad; NO bloqueante).

### 2.3 -- Gate de capacidad atado al PLANO ATESTADO (funcion nueva; insertar tras `ensure_event_state_config_valid`, ~linea 815)
```python
def engram_capability_enabled(root: Path) -> bool:
    """Tier-1 gate (DECISION-engram v3). El flag vive en el plano ATESTADO
    protocol.config.json -> event_state.engram.enabled (ausente => False), de modo que encenderlo
    muta el hash del genesis #4 y exige re-genesis coordinado (no editable a mano). NO se lee de
    event-state.runtime.json (su loader tiene allowlist estricta que no admite la clave engram).
    EXIGE ADEMAS adoption_tier=='runtime': el guard dataset_seal (I9) vive en event_state_config_error,
    que retorna None si adoption_tier!='runtime' (protocol_replay.py:127) -> en coordination-tier ese
    guard es INERTE; por eso aqui se exige el mismo tier, para que el cierre estructural de A/seal valga
    SOLO en runtime-tier. En coordination-tier la capacidad permanece OFF estructuralmente."""
    config_path = root.resolve() / "protocol.config.json"
    if not config_path.exists():
        return False
    try:
        config = read_json(config_path)
    except (OSError, ValueError):
        return False
    if not isinstance(config, dict) or config.get("adoption_tier") != "runtime":
        return False
    event_state = config.get("event_state")
    engram = event_state.get("engram") if isinstance(event_state, dict) else None
    return bool(isinstance(engram, dict) and engram.get("enabled") is True)
```
> Por que aqui y no en `event-state.runtime.json`: el override gitignored pasa por
> `event_state_runtime_override` (`eventlog.py:243-277`), cuya allowlist estricta solo admite
> `actor_auth_enforce/actor_auth_config/event_auth` y rechaza cualquier otra clave. El flag DEBE vivir en
> la config commiteada y hasheada en el genesis para que la activacion sea un cambio atestado y visible
> (coherente con DECISION-0022 cutover coordinado), no un toggle local silencioso.
> **Precondicion de tier (cierra el hueco D/H):** sin el chequeo `adoption_tier=='runtime'`, este gate
> leeria el flag de forma tier-agnostica mientras que su precondicion `dataset_seal` (en
> `event_state_config_error`) es INERTE en coordination-tier (short-circuit `protocol_replay.py:127`). El
> chequeo de tier evita ese desajuste: la capacidad solo puede encenderse donde el guard del seal tiene
> dientes. En coordination-tier el cierre de A/seal baja a **DISCIPLINARIO** y la capacidad queda OFF.

### 2.4 -- Rama de normalizacion en `normalize_intent` (insertar tras el bloque `mailbox_archive`, tras linea 384, ANTES del fall-through de `decision` de la 386). ALLOWLIST + sin `title`
```python
    if kind == "engram_observation":
        unsupported = sorted(k for k in payload if k not in ENGRAM_ALLOWED_FIELDS)
        if unsupported:
            raise IntentValidationError(
                f"engram_observation contains unsupported fields (memory body/title must NOT be in the ledger): {', '.join(unsupported)}"
            )
        topic_key = require_text(payload, "topic_key")
        if not ENGRAM_TOPIC_KEY_RE.fullmatch(topic_key):
            raise IntentValidationError("engram_observation.topic_key must be a slug (no spaces/free prose)")
        mem_type = require_text(payload, "mem_type")
        if mem_type not in ENGRAM_MEM_TYPES:
            raise IntentValidationError(
                f"engram_observation.mem_type must be one of: {', '.join(sorted(ENGRAM_MEM_TYPES))}"
            )
        memory_project = require_text(payload, "memory_project")
        if not ENGRAM_PROJECT_RE.fullmatch(memory_project):
            raise IntentValidationError("engram_observation.memory_project must match ^map-[a-z0-9-]+$")
        content_sha256 = require_text(payload, "content_sha256").lower()
        if not ENGRAM_SHA256_RE.fullmatch(content_sha256):
            raise IntentValidationError("engram_observation.content_sha256 must be a 64-char hex sha256")
        # scope: enum CERRADO, no prosa (cierra el contraejemplo scope="persona@example.com NIT ...").
        scope = (str(payload.get("scope") or "project").strip() or "project")
        if scope not in ENGRAM_SCOPE_VALUES:
            raise IntentValidationError(
                f"engram_observation.scope must be one of: {', '.join(sorted(ENGRAM_SCOPE_VALUES))} (no free prose)"
            )
        normalized = {
            **common,
            "topic_key": topic_key,
            "mem_type": mem_type,
            "memory_project": memory_project,
            "content_sha256": content_sha256,
            "scope": scope,
        }
        # task_id: opcional, pero si viene DEBE ser un id estructurado, nunca prosa.
        task_id = str(payload.get("task_id") or "").strip()
        if task_id:
            if not ENGRAM_TASK_ID_RE.fullmatch(task_id):
                raise IntentValidationError("engram_observation.task_id must match ^TASK-[0-9]+$ (no free prose)")
            normalized["task_id"] = task_id
        # supersedes: opcional; si viene DEBE ser slug topic_key o id de observacion, nunca prosa.
        supersedes = str(payload.get("supersedes") or "").strip()
        if supersedes:
            if not ENGRAM_SUPERSEDES_RE.fullmatch(supersedes):
                raise IntentValidationError(
                    "engram_observation.supersedes must be a topic_key slug or an observation id (no free prose)"
                )
            normalized["supersedes"] = supersedes
        return normalized
```
> La ALLOWLIST de campos (rechaza TODO campo no listado, incluido `title`/`content`/`body`/`note`/`summary`/
> `detail`) NO basta por si sola: 3 de los campos admitidos (`scope`, `task_id`, `supersedes`) AUN dejarian
> entrar prosa por valor. v3 los regimenta por enum/regex aqui mismo, de modo que NINGUN campo del evento
> admite texto libre -> I4 (cero-PROSA) pasa a ser **ESTRUCTURAL** de verdad. La blacklist de v1
> (`content/body/...`) se ELIMINA por incompleta. `normalize_intent` NO lee config ni conoce `actor_id`: la
> identidad (I7) y el gate (I1/I9) se validan en `validate_intent` (§2.5), donde viven `root` y `actor_id`.

### 2.5 -- Enforcement en `validate_intent` (gate + identidad). Rama `elif kind == "engram_observation":` justo antes del `elif kind == "claim":` (linea 724)
```python
    elif kind == "engram_observation":
        # I1: gate de capacidad atado al plano atestado. Cubre single (999) y --intents (validate_transaction -> 536).
        if not engram_capability_enabled(root):
            raise IntentValidationError(
                "engram_observation capability is OFF (DECISION-engram v2). "
                "Activation requires a coordinated re-genesis that sets "
                "protocol.config.json -> event_state.engram.enabled=true with a dataset_seal; "
                "it cannot be hand-edited without breaking the #4 chain."
            )
        # I7: identidad de autor enforced en el borde. map-<slug-del-actor-firmado>, no convencion.
        memory_project = str(normalized.get("memory_project") or "")
        if memory_project == ENGRAM_SHARED_PROJECT:
            if not actor_has_any(registry, actor_id, {"engram_shared"}):
                raise IntentValidationError(
                    f"actor {actor_id} lacks capability 'engram_shared' required to write {ENGRAM_SHARED_PROJECT}"
                )
        else:
            expected = f"map-{binding_slug(actor_id)}"
            if memory_project != expected:
                raise IntentValidationError(
                    f"engram_observation.memory_project must be '{expected}' for actor {actor_id} "
                    f"(or '{ENGRAM_SHARED_PROJECT}' with the engram_shared capability); got '{memory_project}'"
                )
```
> Por que aqui y no en una pasada aparte (cierra H): `validate_intent` es el UNICO punto que ambos caminos
> atraviesan. `registry` ya esta cargado al inicio de `validate_intent` (linea 663) y `binding_slug` ya
> existe (linea 755). Cero wiring nuevo de identidad: se reusa el `actor_id` firmado que
> `submit_intent`/`submit_intents` ya pasan. I9 (dataset_seal) NO se valida aqui sino en
> `event_state_config_error` (§3b), que corre ANTES via `ensure_event_state_config_valid`.

### 2.6 -- `required_scopes` y `validate_scope_authority`: eximir a `engram_observation` del claim (I8, corrige bug latente)
`required_scopes` (linea 592) cae al `return []` final para `engram_observation` (correcto: no toca rutas
row-scoped). PERO `validate_scope_authority` (lineas 654-656) exige **al menos un claim activo del actor**
aunque `required` este vacio -> bloquearia espuriamente a un agente sin claims. Anadir el bypass explicito
al inicio de `validate_scope_authority` (tras la rama de `claim acquire` que ya retorna en :651, antes de
`required = required_scopes(...)` en :653):
```python
    if normalized["kind"] == "engram_observation":
        # engram_observation no escribe rutas del ledger (required_scopes == []); no exige claim activo.
        return
```
> Sin esto, `test_engram_observation_accepted_when_enabled` (actor sin claim) fallaria. La exencion es
> intencional y se cubre con `test_engram_observation_no_claim_required` (§5).

### 2.7 -- `aggregate_id_for` (linea 399): agrupar por proyecto+topic
Insertar antes del bucle `for key in (...)` (linea 404):
```python
    if normalized.get("kind") == "engram_observation":
        return f"engram:{normalized.get('memory_project')}:{normalized.get('topic_key')}"
```

### 2.8 -- `event_payload_for` (linea 411): serializar la transicion (SIN `title`)
Insertar como `elif` tras el bloque `mailbox_archive` (antes de `return payload`, linea 462):
```python
    elif kind == "engram_observation":
        observation = {
            "topic_key": normalized["topic_key"],
            "mem_type": normalized["mem_type"],
            "memory_project": normalized["memory_project"],
            "content_sha256": normalized["content_sha256"],
            "scope": normalized.get("scope", "project"),
        }
        if normalized.get("supersedes"):
            observation["supersedes"] = normalized["supersedes"]
        payload["transitions"]["engram_observation"] = observation
```
> `task_id` ya se incluye en lineas 419-420 si `normalized` lo trae. NI el cuerpo NI `title` se incluyen.

## 3. `runtime/protocol_replay.py` -- `apply_intent_event`

Anadir rama **explicita no-op** al final del bloque `if isinstance(transitions, dict):` (tras
`prune_transition`, linea 930):
```python
        # engram_observation: la MEMORIA NO es state de protocolo. apply_intent_event SOLO muta filas
        # para transitions.{task_status,task_upsert,claims,decision,project_narrative,protocol_prune};
        # engram_observation no aparece en ninguna -> cero-drift es ESTRUCTURAL (no hay rama que toque
        # CLAIMS/TASK_INDEX/PROJECT_STATE). El evento atesta una SOLICITUD/COMPROMISO de registrar memoria
        # (topic_key + content_sha256); el cuerpo vive en Engram y su registro real lo confirma el ACK del
        # bridge (ENG-BRIDGE), NO el replay. Rama no-op EXPLICITA solo para auditoria (I2/I3).
        engram_transition = transitions.get("engram_observation")
        if isinstance(engram_transition, dict):
            pass
```
> No tocar `replay_protocol_state` (linea 965-966 ya enruta `intent.applied` -> `apply_intent_event`).

## 3b. `runtime/protocol_replay.py` -- `event_state_config_error`: guard `dataset_seal` (I9, cierra A de forma estructural)

Anadir un accessor junto a los `event_state_*_enabled` (~linea 122):
```python
def event_state_engram_enabled(config: dict[str, Any] | None) -> bool:
    event_state = (config or {}).get("event_state")
    engram = event_state.get("engram") if isinstance(event_state, dict) else None
    return isinstance(engram, dict) and engram.get("enabled") is True
```
Dentro de `event_state_config_error` (linea 125), ANTES del `return None` final (linea 152):
```python
    engram = event_state.get("engram") if isinstance(event_state.get("engram"), dict) else None
    if isinstance(engram, dict) and engram.get("enabled") is True:
        seal = engram.get("dataset_seal")
        if not isinstance(seal, dict) or not seal:
            return (
                "event_state.engram.enabled=true requires event_state.engram.dataset_seal "
                "(object with seal_commit, seal_event_seq, sealed_at); set it via a coordinated "
                "re-genesis after the operator seals the coordination dataset, or set engram.enabled=false."
            )
        for field in ("seal_commit", "seal_event_seq", "sealed_at"):
            if not str(seal.get(field) or "").strip():
                return f"event_state.engram.dataset_seal.{field} is required when engram.enabled=true"
```
> Esto se propaga AUTOMATICAMENTE a `submit_intent.ensure_event_state_config_valid` (`submit_intent.py:810-814`),
> a `runtime/apply.py` y al validador `scripts/validate_collaboration_state.py` (que delega en
> `event_state_config_error`). Sin seal => config invalida => NINGUN intent corre (no solo el engram).
> **Honestidad:** el guard verifica que SE DECLARO un seal atestado, NO que el dataset este "realmente
> congelado/veraz" -- eso es JUICIO del operador (DISCIPLINARIO, espejo plano-1 DECISION-0040).

## 3c. Espejo PowerShell (cierra H en el segundo validador)

`scripts/validate_collaboration_state.ps1`: replicar la guardia `engram` (enabled => dataset_seal con
`{seal_commit, seal_event_seq, sealed_at}` no vacios) JUNTO a la guardia existente
`authoritative=>enforce=>materialize=>enabled` (la que TASK-0086 cableo en py/ps). Mismo mensaje de fallo
que la version python. El cierre real exige correr AMBOS validadores en clon limpio.

## 4. Forma de uso (como lo invocara un agente cuando este ON)
```bash
python runtime/submit_intent.py --intent '{
  "type": "engram_observation",
  "topic_key": "task/TASK-0218/learning",
  "mem_type": "learning",
  "memory_project": "map-arquitecto",
  "content_sha256": "<sha256 del cuerpo que el bridge guardara en Engram>",
  "task_id": "TASK-0218"
}'
```
> SIN `title` (se eliminò del evento; vive en Engram). `memory_project` DEBE ser `map-<binding_slug(actor_id)>`:
> si el actor firmado es `Arquitecto`, `binding_slug("Arquitecto") == "arquitecto"` => `map-arquitecto`.
> Cualquier otro valor se rechaza (I7). El intent solo corre si `protocol.config.json ->
> event_state.engram.enabled=true` CON `dataset_seal` (I1/I9), lo que exige re-genesis del operador (I10).

## 5. Tests (anadir junto a los tests de runtime existentes; correr en CLON LIMPIO sin dist/ residual)
- `test_engram_rejected_when_disabled` (I1, single): sin `event_state.engram` => `IntentValidationError`, 0 eventos.
- `test_engram_rejected_in_tx_rollback` (I1+I6): `--intents` [claim valido, engram_observation OFF] => rollback
  total; el claim NO se aplica (el camino transaccion que v1 no demostro).
- `test_engram_accepted_when_enabled` (I4 + I8): `engram.enabled=true` + `dataset_seal` completo => 1 evento
  `intent.applied` con `transitions.engram_observation`; el evento NO contiene clave `title` ni ningun campo
  fuera de la allowlist; actor SIN claim activo => aceptado.
- `test_engram_allowlist_rejects_body` (I4 estructural): payload con `title`/`note`/`summary`/`detail`/`body`
  => `IntentValidationError "unsupported fields"`; cubre que es ALLOWLIST, no blacklist (cierra el
  contraejemplo exacto del Analista, blocker B).
- `test_engram_rejects_prose_in_admitted_fields` (I4 estructural, cierra B residual): payload con
  `scope="persona@example.com NIT 900123456"` => rechazado; `task_id="ver bug de Juan"` => rechazado;
  `supersedes="la memoria vieja con el NIT"` => rechazado; los 3 con valores validos (`scope="personal"`,
  `task_id="TASK-0218"`, `supersedes="task/TASK-0100/learning"`) => aceptados. Prueba que NINGUN campo
  admitido deja entrar prosa por valor (el hueco que la allowlist sola no cerraba).
- `test_engram_identity_enforced` (I7): actor `Analista` con `memory_project="map-codex"` => rechazado; con
  `map-analista` => aceptado.
- `test_engram_shared_requires_capability` (I7): `memory_project="map-shared"` sin capability `engram_shared`
  => rechazado; con la capability => aceptado.
- `test_engram_no_claim_required` (I8): actor sin claim activo + `engram.enabled=true` => ACEPTADO (FALLA sin
  el bypass §2.6, PASA con el; test de regresion del bug latente de `validate_scope_authority`).
- `test_engram_enabled_without_seal_is_config_error` (I9): `event_state.engram.enabled=true` SIN `dataset_seal`
  => `event_state_config_error != None` => `submit_intent` aborta en `ensure_event_state_config_valid` para
  CUALQUIER intent (no solo engram).
- `test_engram_zero_drift` (I2): hash de `CLAIMS/TASK_INDEX/PROJECT_STATE` byte-identico antes/despues; ademas
  `drift_after.has_drift is False` (reusa el hard-gate B.3 real).
- `test_engram_replay_noop` (I3): `replay_protocol_state` con el evento => state == baseline.
- `test_engram_validation`: `mem_type` invalido, `content_sha256` no-hex, `memory_project` fuera de
  `^map-...$`, `topic_key` con espacios => todos rechazados.
- `test_engram_idempotent` (I5): dos envios identicos => un solo evento.
- `test_engram_rollback_in_tx_enabled` (I6 camino feliz+fallo): `--intents` [engram valido,
  intent_que_falla_despues] con capability ON => rollback total incluido el engram (prueba el rollback REAL,
  no solo la negativa; cierra el miss "checker prueba el write real").
- `test_config_flip_breaks_chain_without_regenesis` (I10): editar `engram.enabled` a mano (sin re-genesis) =>
  `validate_chain` reporta genesis hash mismatch (prueba estructural del flip atestado, 5.2).
- `test_engram_off_in_coordination_tier` (precondicion de tier, cierra D/H): con `adoption_tier="coordination"`
  + `event_state.engram.enabled=true`, `engram_capability_enabled` => False y el intent se RECHAZA (la
  capacidad solo enciende en runtime-tier, donde el guard `dataset_seal` tiene dientes).
- `test_decision_fallthrough_intact`: un intent `decision` valido sigue normalizando/aplicando igual (la rama
  nueva esta ANTES del fall-through; verifica que no la rompimos -- pedido explicito del Analista).

## 6. Gates a correr (en clon limpio, no en working tree caliente)
`python scripts/validate_collaboration_state.py` exit 0 + `scripts/validate_collaboration_state.ps1` verde
(con el espejo del guard §3c) + suite de runtime (los tests §5) + verificacion de drift (B.3
`has_drift=false`) + `python scripts/scan_domain_neutrality.py` exit 0 (los identificadores `map-*` y
`mem_type` son neutrales; sin terminos de dominio) + `scripts/scan_encoding.py` exit 0 (sin BOM/CRLF).
El PATCH NO se mergea sin esto. La DECISION SI se puede grabar OFF antes (separacion estructural
DECISION-vs-PATCH).

## 7. Matriz de estado por invariante (honestidad -- nada se llama "cerrado" sin codigo+tests)
> Este parche es una **SPEC**: el codigo NO esta merged (`grep engram_* runtime/*.py` = 0 hits) y los tests
> de §5 estan A ESCRIBIR, no ejecutados. Las etiquetas de abajo describen el estado de DISEÑO de cada
> invariante y su precondicion; "ESTRUCTURAL" aqui significa "estructural POR DISEÑO, PENDIENTE de
> implementacion+tests verdes en clon limpio", nunca "ya probado".

- **ESTRUCTURAL-PENDIENTE-IMPL+TESTS (diseño solido, sin codigo merged):** gate OFF-by-default atado al
  plano atestado en ambos caminos (I1/I6); cero-drift y replay no-op por construccion del replay (I2/I3);
  cero texto libre por allowlist de campos + regimentacion por valor de TODOS los campos admitidos, `title`
  eliminado (I4); precondicion `dataset_seal` como hard-gate de config (I9). Suben a ESTRUCTURAL al mergear
  el codigo con la suite §5 verde en clon limpio.
- **ESTRUCTURAL-SI-PRECONDICION (runtime-tier):** flip atestado que rompe la cadena sin re-genesis (I10)
  vale SOLO bajo `chain_enabled=true`; el gate y el guard `dataset_seal` valen SOLO bajo
  `adoption_tier=='runtime'` (en coordination-tier el guard es inerte por short-circuit
  `protocol_replay.py:127`, y `engram_capability_enabled` exige el tier por eso). Fuera de esas
  precondiciones, bajan a DISCIPLINARIO.
- **ESTRUCTURAL-SI-PRECONDICION (`actor_auth_enforce`):** la identidad de autor `memory_project==map-<actor>`
  (I7) atrapa el typo/mismatch SIEMPRE (anti-typo, estructural), PERO el binding criptografico del `actor_id`
  al keyid ed25519 (`ensure_attested_actor_key_binding`) es **no-op mientras `actor_auth_enforce` no este
  activo**, y ese flag vive en el override runtime gitignored (`eventlog.py:294-296`), NO en el
  `protocol.config.json` atestado. Por tanto HOY `--actor-id` es spoofable y I7 es **anti-typo
  (DISCIPLINARIO contra impersonacion)**. Para que I7 sea estructural contra impersonacion en Tier 1 hay que
  promover `actor_auth_enforce` al plano atestado (tarea ENG-ACTORAUTH-ATTEST, §8).
- **ESTRUCTURAL-PENDIENTE-IMPL+TESTS:** exencion de claim espurio (I8) y `map-shared` tras capability (parte
  de I7) -- diseño solido, pendientes de codigo+test.
- **ABIERTO-DIFERIDO (NO lo cierra este parche, declarado):** **atomicidad ledger<->Engram** y "memoria
  realmente registrada" -> ENG-BRIDGE outbox/ACK + ENG-RECONCILE healer; este parche solo atesta el
  COMPROMISO, no la existencia (C ABIERTO). **Hueco de diseño abierto en C:** el evento `engram_observation`
  NO lleva puntero al archivo/ancla markdown cuyo `content_sha256` atesta, asi que el bridge diferido NO
  puede localizar el cuerpo -> la spec de ENG-OUTBOX/ENG-BRIDGE debe anadir un campo `body_ref` (ruta
  repo-relativa validada como slug de path, NO prosa) o declararlo punto de diseño abierto (ver §8).
  **Reconstruccion markdown->Engram** -> ENG-IMPORT con test (D ABIERTO). **DISCIPLINARIO residual:** PII
  semantica corta dentro de un slug acotado (`topic_key`/`supersedes`) -> ENG-TOPICKEY-PII opcional, NO
  bloqueante; veracidad semantica del `dataset_seal` (JUICIO del operador, espejo plano-1 DECISION-0040).
  **Nada se sobre-afirma como cerrado ni como probado.**

## 8. Fuera de este parche (tareas siguientes, NO hacer aqui)
- **HUECO DE DISEÑO ABIERTO en C (resolver al especificar ENG-OUTBOX/ENG-BRIDGE):** el evento
  `engram_observation` lleva `content_sha256` pero NO un puntero al archivo/ancla markdown que contiene el
  cuerpo cuyo sha256 atesta. Sin ese puntero el bridge diferido no puede localizar el cuerpo para hacer el
  `mem_save` real. La spec de ENG-OUTBOX/ENG-BRIDGE debe anadir a la allowlist un campo **`body_ref`** (ruta
  repo-relativa validada como **slug de path**, NO prosa -- regex tipo `^[A-Za-z0-9][A-Za-z0-9._/-]{0,255}$`)
  que apunte al cuerpo en el markdown-en-git atestado; alternativamente declararlo punto de diseño ABIERTO y
  resolver el direccionamiento del cuerpo antes de activar Tier 1. Mientras no se resuelva, C sigue ABIERTO.
- `runtime/engram_bridge.py` (CONSUMIDOR IDEMPOTENTE DEL OUTBOX): lee los `engram_observation` aplicados
  (`applied:true`) cuyo `idempotency_key` NO este en `runtime/state/engram_ack.json`; para cada uno hace el
  `mem_save` real leyendo el CUERPO del markdown-en-git atestado **localizado via `body_ref`**, verifica
  `sha256(cuerpo)==content_sha256`, y SOLO tras exito escribe el ACK
  `{idempotency_key: {seq, content_sha256, mem_id, ts}}` (escritura atomica, fuera del ledger -> cero drift,
  I2/I8). Idempotente por `content_sha256`. NUNCA escribe el ledger.
- `ENG-ACTORAUTH-ATTEST` (precondicion para que I7 sea estructural contra impersonacion en Tier 1): promover
  `actor_auth_enforce` (hoy solo en el override runtime gitignored, `eventlog.py:294-296`) al plano atestado
  `protocol.config.json` (de modo que `ensure_attested_actor_key_binding` deje de ser no-op y `--actor-id`
  no sea spoofable). Sin esto, I7 cierra typo/mismatch (anti-typo) pero NO impersonacion.
- `runtime/engram_reconcile.py` (HEALER "atestado-pero-ausente"): detecta `engram_observation` aplicados sin
  ACK o con `content_sha256` ausente en el pool destino, reintenta con backoff, reporta irreconciliables como
  anomalia DECISION-0018.
- `runtime/state/engram_ack.json`: tabla lateral de ACK, NO commiteada (gitignore), reconstruible re-corriendo
  el bridge; NO es fuente de verdad (lo es el par event-log+Engram, y en ultima instancia el markdown-en-git).
- Wiring del flag `event_state.engram.{enabled,dataset_seal}` + capability `engram_shared` en el
  `agent_registry` de `protocol.config.json` + doc + runbook del re-genesis (ENG-REGENESIS-RUNBOOK).
- Validador anti-PII de `topic_key` (ENG-TOPICKEY-PII, opcional, defensa en profundidad).
- Importador determinista markdown->Engram (ENG-IMPORT) con test round-trip si se quiere re-afirmar
  reconstruibilidad.
