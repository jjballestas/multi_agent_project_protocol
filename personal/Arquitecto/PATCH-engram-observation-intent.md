# PATCH SPEC — intent `engram_observation` (submit_intent.py + protocol_replay.py)

> Autor: Arquitecto · Estado: DRAFT para Codex · No toca ledger al redactarse (vive en `personal/`).
> Depende de: DRAFT-DECISION-engram-memory-backend (capability OFF by default).
> Alcance EXACTO del parche: `runtime/submit_intent.py` + `runtime/protocol_replay.py` + tests.
> NO incluye el `engram_bridge` (el `mem_save` real a Engram) — eso es tarea aparte (ver §7).

## 0. Qué se quiere lograr (intención, leer antes de tocar código)

Añadir un tipo de intent `engram_observation` que permita **atestar en el ledger #4 que un
agente registró una memoria**, SIN:
- mutar el state materializado (`CLAIMS.json` / `TASK_INDEX.json` / `PROJECT_STATE.json`),
- meter el CUERPO de la memoria (texto libre) en el event log,
- romper single-writer ni la atomicidad de `submit_intent --intents`.

El ledger lleva solo **metadato + `content_sha256`** (mismo principio "sujeto por hash" de
DECISION-0040, plano estructural). El cuerpo vive en Engram, fuera de banda. La capacidad nace
**APAGADA** (gate `event-state.runtime.json -> engram.enabled`, default `false`) para garantizar
cero impacto en el dataset del TFM hasta que el operador la active tras sellar el dataset.

## 1. Invariantes de aceptación (definition of done)

- **I1 (gate):** con `engram.enabled` ausente/`false`, un `engram_observation` se **rechaza**
  (`IntentValidationError`, exit ≠ 0). No se escribe ningún evento.
- **I2 (cero drift):** con la capacidad ON, aplicar un `engram_observation` válido deja
  `CLAIMS.json`, `TASK_INDEX.json`, `PROJECT_STATE.json` **byte-idénticos** antes/después. El
  hard-gate B.3 de drift sigue verde.
- **I3 (replay no-op):** re-ejecutar el event log que incluya `engram_observation` reproduce el
  mismo state materializado (es no-op puro sobre el state).
- **I4 (cero cuerpo / PII):** en `events.jsonl` solo aparecen `topic_key`, `title`, `mem_type`,
  `memory_project`, `content_sha256` (+ opcional `task_id`, `supersedes`). **Nunca** el cuerpo.
- **I5 (idempotencia):** misma `(actor, memory_project, topic_key, content_sha256)` ⇒ idempotente
  (no duplica evento), vía el `idempotency_key` existente.
- **I6 (atomicidad):** un `engram_observation` dentro de una transacción `--intents` hace rollback
  con el resto si cualquier intent falla (usa el camino transaccional existente, sin cambios).

## 2. `runtime/submit_intent.py`

### 2.1 — Añadir el tipo a `INTENT_TYPES` (línea 84)
```python
# ANTES
INTENT_TYPES = {"task_status", "task_upsert", "claim", "decision", "project_narrative", "protocol_prune", "mailbox_archive"}
# DESPUÉS
INTENT_TYPES = {"task_status", "task_upsert", "claim", "decision", "project_narrative", "protocol_prune", "mailbox_archive", "engram_observation"}
```

### 2.2 — Constantes nuevas (insertar tras `MAILBOX_MESSAGE_ID_RE`, ~línea 86)
```python
ENGRAM_MEM_TYPES = {"decision", "architecture", "bugfix", "pattern", "config", "discovery", "learning"}
ENGRAM_PROJECT_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")     # p.ej. map-arquitecto / map-codex / map-shared
ENGRAM_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ENGRAM_TOPIC_KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,127}$")  # slug, no prosa libre
```

### 2.3 — Gate de capacidad (función nueva, top-level; insertar tras `restore_files`, ~línea 216)
```python
def engram_capability_enabled(root: Path) -> bool:
    """Tier-1 gate. La emisión de `engram_observation` está APAGADA por defecto
    (DRAFT-DECISION-engram). Lee <root>/event-state.runtime.json -> {"engram": {"enabled": bool}}.
    Archivo o clave ausente => False (desactivado)."""
    config_path = root / "event-state.runtime.json"
    if not config_path.exists():
        return False
    try:
        config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return False
    engram = config.get("engram") if isinstance(config, dict) else None
    if not isinstance(engram, dict):
        return False
    return bool(engram.get("enabled", False))
```
> Nota Codex: si existe un loader central de `event-state.runtime.json`, reusarlo en vez de releer
> el archivo; el contrato (default `false`) no cambia.

### 2.4 — Rama de normalización en `normalize_intent`
Insertar **ANTES** del fall-through de `decision` (actualmente líneas 386–389; la rama final sin
`if kind == ...` ES el caso decision). Colocar justo después del bloque `mailbox_archive`
(tras la línea 384):
```python
    if kind == "engram_observation":
        topic_key = require_text(payload, "topic_key")
        if not ENGRAM_TOPIC_KEY_RE.fullmatch(topic_key):
            raise IntentValidationError("engram_observation.topic_key must be a slug (no spaces/free prose)")
        title = require_text(payload, "title")
        mem_type = require_text(payload, "mem_type")
        if mem_type not in ENGRAM_MEM_TYPES:
            raise IntentValidationError(
                f"engram_observation.mem_type must be one of: {', '.join(sorted(ENGRAM_MEM_TYPES))}"
            )
        memory_project = require_text(payload, "memory_project")
        if not ENGRAM_PROJECT_RE.fullmatch(memory_project):
            raise IntentValidationError("engram_observation.memory_project must be a safe slug (e.g. map-arquitecto)")
        content_sha256 = require_text(payload, "content_sha256").lower()
        if not ENGRAM_SHA256_RE.fullmatch(content_sha256):
            raise IntentValidationError("engram_observation.content_sha256 must be a 64-char hex sha256")
        # PROHIBIDO el cuerpo en el ledger (I4): rechazar campos que parezcan llevar texto largo.
        for forbidden in ("content", "body", "message", "observation", "text"):
            if forbidden in payload:
                raise IntentValidationError(
                    f"engram_observation must NOT carry the memory body ('{forbidden}'); pass content_sha256 only"
                )
        normalized = {
            **common,
            "topic_key": topic_key,
            "title": title,
            "mem_type": mem_type,
            "memory_project": memory_project,
            "content_sha256": content_sha256,
            "scope": (str(payload.get("scope") or "project").strip() or "project"),
        }
        task_id = str(payload.get("task_id") or "").strip()
        if task_id:
            normalized["task_id"] = task_id
        supersedes = str(payload.get("supersedes") or "").strip()
        if supersedes:
            normalized["supersedes"] = supersedes
        return normalized
```

### 2.5 — `aggregate_id_for` (línea 399): agrupar por proyecto+topic
Insertar antes del bucle `for key in (...)`:
```python
    if normalized.get("kind") == "engram_observation":
        return f"engram:{normalized.get('memory_project')}:{normalized.get('topic_key')}"
```

### 2.6 — `event_payload_for` (línea 411): serializar la transición
Insertar como `elif` tras el bloque `mailbox_archive` (antes de `return payload`, línea 462):
```python
    elif kind == "engram_observation":
        observation = {
            "topic_key": normalized["topic_key"],
            "title": normalized["title"],
            "mem_type": normalized["mem_type"],
            "memory_project": normalized["memory_project"],
            "content_sha256": normalized["content_sha256"],
            "scope": normalized.get("scope", "project"),
        }
        if normalized.get("supersedes"):
            observation["supersedes"] = normalized["supersedes"]
        payload["transitions"]["engram_observation"] = observation
```
> `task_id` ya se incluye arriba (líneas 419–420) si `normalized` lo trae. El cuerpo NO se incluye.

### 2.7 — Enforcement del gate (camino de aplicación)
En el paso donde se itera la lista de intents normalizados ANTES de emitir eventos (la pasada de
validación contra el state donde `root` está en scope — single y `--intents`), añadir:
```python
    if normalized["kind"] == "engram_observation" and not engram_capability_enabled(root):
        raise IntentValidationError(
            "engram_observation capability is OFF (DRAFT-DECISION-engram). "
            "Set event-state.runtime.json -> engram.enabled=true to activate (gated by GATE-DATASET)."
        )
```
> Debe ejecutarse para CADA intent de la transacción, de modo que un `engram_observation` apagado
> aborte toda la transacción `--intents` (I1 + I6). NO ponerlo dentro de `normalize_intent`
> (normalize no debe leer config).

## 3. `runtime/protocol_replay.py` — `apply_intent_event`

Añadir rama **explícita no-op** al final del bloque `if isinstance(transitions, dict):`
(tras el bloque `prune_transition`, ~línea 930):
```python
        # engram_observation: la MEMORIA NO es state de protocolo. El evento intent.applied del
        # ledger ATESTA que se registró una memoria (topic_key + content_sha256); el cuerpo vive en
        # Engram, fuera de banda. Replaying NO debe mutar el state materializado row-scoped
        # (CLAIMS/TASK_INDEX/PROJECT_STATE) -> no-op INTENCIONAL y explícito para auditoría
        # (no borrar: el silencio aquí parecería un caso olvidado). Garantiza I2/I3 (cero drift).
        engram_transition = transitions.get("engram_observation")
        if isinstance(engram_transition, dict):
            pass
```
> No tocar `replay_protocol_state` (línea 965 ya enruta `intent.applied` -> `apply_intent_event`).

## 4. Forma de uso (cómo lo invocará un agente cuando esté ON)
```bash
python runtime/submit_intent.py --intent '{
  "type": "engram_observation",
  "topic_key": "task/TASK-0218/learning",
  "title": "modal doble-click: Esc cierra y restaura foco",
  "mem_type": "learning",
  "memory_project": "map-arquitecto",
  "content_sha256": "<sha256 del cuerpo que el bridge guardará en Engram>",
  "task_id": "TASK-0218"
}'
```

## 5. Tests (añadir junto a los tests de runtime existentes)
- `test_engram_observation_rejected_when_disabled`: sin flag ⇒ `IntentValidationError`, sin evento nuevo (I1).
- `test_engram_observation_accepted_when_enabled`: con `engram.enabled=true` ⇒ 1 evento `intent.applied`
  con `transitions.engram_observation`; payload **sin** cuerpo (I4).
- `test_engram_observation_zero_drift`: hash de `CLAIMS/TASK_INDEX/PROJECT_STATE` idéntico antes/después (I2).
- `test_engram_observation_replay_noop`: `replay_protocol_state` con el evento ⇒ state == baseline (I3).
- `test_engram_observation_validation`: `mem_type` inválido, `content_sha256` no-hex, `memory_project`
  con mayúsculas/espacios, `topic_key` con espacios, presencia de `content`/`body` ⇒ todos rechazados.
- `test_engram_observation_idempotent`: dos envíos idénticos ⇒ un solo evento (I5).
- `test_engram_observation_rollback_in_tx`: `--intents` con [claim válido, engram_observation con
  capacidad OFF] ⇒ rollback total; el claim NO se aplica (I6).

## 6. Gates a correr
`validate_collaboration_state.ps1` verde + suite de runtime + verificación de drift (B.3) +
domain-neutrality scan (los identificadores `map-*` son neutrales; no introducir términos de dominio).

## 7. Fuera de este parche (tareas siguientes, NO hacer aquí)
- `runtime/engram_bridge.py`: tras commitear la transacción, lee los `engram_observation` aplicados y
  hace el `mem_save` real en el proyecto Engram `memory_project`, verificando que `sha256(cuerpo)==content_sha256`.
- Wiring del flag `engram.enabled` en `event-state.runtime.json` + doc.
- Validador anti-PII sobre `title`/`topic_key` antes de habilitar Tier-1 en vivo (plano disciplinario → estructural).
