---
spec_id: SPEC-0071
title: Firma por agente - Atestación de autoría en el eventlog (in-toto compatible, off-by-default)
status: proposed
date: 2026-06-13
author: Claude (architect)
relates_to: [DECISION-0029, TASK-0102, SPEC-0070, DECISION-0015, DECISION-0023]
phase: P2
priority: high
sdd_required: true
---

# SPEC-0071 — Firma por agente

**Pieza 2b de DECISION-0029:** Atestación de autoría mediante firma criptográfica por cada agente (no consenso). Cada turno relevante lleva atestación firmada del productor; la revisión se registra como atestación del revisor (maker ≠ checker). Backend configurable, vendor-neutral. Apagado por defecto.

## 1. Resumen

El eventlog actual autentica con HMAC simétrico controlado por el runtime, sin evidencia criptográfica de quién produjo cada artefacto. **SPEC-0071** agrega firma asimétrica por agente:

- Cada agente del `agent_registry` posee material de firma propio (Ed25519 local o identidad keyless)
- Los turnos y handoffs llevan atestación firmada por el agente productor (sujeto: hash del artefacto; predicado: agente, modelo-versión, tarea, decision habilitante, trust_boundary)
- Formato compatible in-toto (Statement + Predicate, sig verificable externamente)
- Runtime almacena y encadena atestaciones pero NO las produce
- Revisión critic (maker ≠ checker) registrada como atestación del revisor firmada
- Flag `event_state.agent_signatures_enabled` off-by-default; opt-in por instancia

**Propiedades objetivo:** Detecta suplantación de autoría entre agentes (A2), complementa prev_hash (A1) y anclaje externo (A3-restringido).

---

## 2. Diseño Técnico

### 2.1 Estructura del evento atestación

Cada evento `agent.attestation` (nuevo tipo de evento) contiene:

```json
{
  "seq": 42,
  "timestamp": "2026-06-13T12:00:00Z",
  "type": "agent.attestation",
  "actor_id": "Codex",
  "agent_id": "Codex",
  "subject_digest": "sha256:abc123...",
  "subject_reference": "TASK-0101.md",
  "predicate": {
    "agent_id": "Codex",
    "agent_model": "claude-opus-4-8",
    "task_id": "TASK-0101",
    "decision_id": "DECISION-0029",
    "role": "implementer",
    "inputs_trust_boundary": "public",
    "outputs_scope": "runtime/eventlog.py, protocol_replay.py, examples/",
    "timestamp_claimed": "2026-06-13T12:00:00Z",
    "turn_index": 3,
    "human_checkpoint": false
  },
  "signature": {
    "keyid": "codex-ed25519-20260101",
    "sig": "base64-encoded-signature",
    "algorithm": "rsa-pkcs1v15-sha256" | "ed25519" | "ecdsa-sha256" | "keyless-oidc"
  },
  "verification_backend": "local-ed25519" | "keyless-oidc-google" | "external-command",
  "prev_hash": "sha256:prev_hash_n-1"
}
```

### 2.2 Sujeto (subject_digest)

La firma cubre el **hash SHA256 canónico** del artefacto producido:
- Turno: hash del turnReport JSON + timestamp_canonical (sin microsegundos)
- Handoff: hash del archivo HANDOFF .md con lf+utf-8, sin BOM
- Evento de estado (task_status, claim, decision): hash JSON canónico del evento autorizado

```
subject_digest = SHA256(canonical_json(artefacto) | canonical_timestamp)
```

### 2.3 Predicado (in-toto compatible)

La estructura `predicate` es un subconjunto de in-toto v1 Statement, ampliado:

- `agent_id`: identificador único del agente (de `agent_registry`)
- `agent_model`: versión del modelo/invoker usado (ej. "claude-opus-4-8", "codex-v1.2")
- `task_id`: ID de tarea ejecutada (del eventlog/TASK_INDEX)
- `decision_id`: decisión habilitante (ej. DECISION-0029)
- `role`: capacidad bajo la cual se produjo (implementer, reviewer, qa, architect)
- `inputs_trust_boundary`: "public" | "internal" | "secret" (marca si el turno procesa insumos clasificados)
- `outputs_scope`: rutas afectadas (del report `changed_paths`)
- `timestamp_claimed`: timestamp que el agente afirma (para detectar clock-skew)
- `turn_index`: índice del turno en el lazo (1, 2, 3...; 0 si no aplica)
- `human_checkpoint`: true si requirió parada humana

### 2.4 Firma (signature)

- **keyid**: identificador público de la clave (ej. "codex-ed25519-20260101", "claude-keyless-google-2026")
- **sig**: firma en base64 de `subject_digest || canonical_json(predicate)`
- **algorithm**: "rsa-pkcs1v15-sha256", "ed25519", "ecdsa-sha256", "keyless-oidc" (registrado en config)

**Sin secretos en el repo:** la clave privada vive fuera (en wrapper del agente); al repo solo entran claves públicas y firmas verificables.

### 2.5 Backend de firma (configurable, vendor-neutral)

```json
{
  "event_state": {
    "agent_signatures_enabled": false,
    "signature_backend": "local-ed25519" | "keyless-oidc-google" | "external-command",
    "signature_config": {
      "backend": "keyless-oidc-google",
      "issuer": "https://accounts.google.com",
      "identity_claim": "email",
      "timeout_seconds": 30
    }
  }
}
```

- **local-ed25519**: clave privada en `~/.agent_keys/` (local, solo dev/testing)
- **keyless-oidc-google**: (futuro) OIDC de Google sin clave privada en disco
- **external-command**: (futuro) comando externo configurable (análogo a DECISION-0023)

### 2.6 Validación de firma en protocol_replay.py

Nueva función `validate_agent_signatures`:

```python
def validate_agent_signatures(
    log_path: str,
    agent_registry: dict,
    enabled: bool = False,
    backend_config: dict = None
) -> Tuple[bool, List[dict]]:
    """
    Valida firmas de atestaciones en el eventlog.
    
    Args:
        enabled: si False, retorna (True, []) (sin validacion, compatible backward)
        backend_config: config de verificacion (keyids publicas, issuer, etc.)
    
    Returns:
        (ok: bool, findings: List[{seq, agent_id, error}])
    """
    if not enabled:
        return True, []
    
    findings = []
    with open(log_path) as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("type") != "agent.attestation":
                continue
            
            agent_id = event["agent_id"]
            agent = agent_registry.get(agent_id)
            if not agent:
                findings.append({
                    "seq": event["seq"],
                    "agent_id": agent_id,
                    "error": "unknown_agent"
                })
                continue
            
            # Reconstruir subject_digest y verificar firma
            # (pseudocodigo; detalles segun backend)
            ok = verify_signature(
                subject_digest=event["subject_digest"],
                predicate=event["predicate"],
                signature=event["signature"],
                backend=event["verification_backend"],
                agent_keyid=agent["public_key_id"]
            )
            
            if not ok:
                findings.append({
                    "seq": event["seq"],
                    "agent_id": agent_id,
                    "error": "signature_invalid"
                })
    
    return len(findings) == 0, findings
```

### 2.7 Ciclo de vida de una firma

1. **Producción (en el agente, FUERA del runtime):**
   - Agente produce artefacto (turn report, handoff .md, etc.)
   - Agente calcula `subject_digest = SHA256(canonical_json(artefacto))`
   - Agente firma con su clave privada: `sig = Sign(subject_digest || canonical_json(predicate))`
   - Agente incluye `signature` en el report entregado al runtime

2. **Almacenamiento (en el runtime):**
   - `submit_intent.py` recibe report con firma
   - Crea evento `agent.attestation` con toda la info
   - Append al eventlog (sin validar la firma; solo estructura)
   - Encadena con `prev_hash` (SPEC-0070)

3. **Validación (offline, en protocol_replay):**
   - `validate_agent_signatures(enabled=True)` lee el log
   - Reconstruye `subject_digest` y `predicate` desde el evento
   - Verifica firma contra la clave pública del agente
   - Reporta firmas inválidas (agent no registrado, sig fallida, etc.)

### 2.8 Attestaciones de revisor (maker ≠ checker)

Cuando Claude revisa y aprueba el trabajo de Codex:

```json
{
  "seq": 100,
  "type": "agent.attestation",
  "actor_id": "Claude",
  "agent_id": "Claude",
  "subject_digest": "sha256:hash-de-handoff-de-codex",
  "subject_reference": "HANDOFF-TASK-0101-codex-to-claude-1.md",
  "predicate": {
    "agent_id": "Claude",
    "role": "reviewer",
    "reviewed_work_agent": "Codex",
    "reviewed_task": "TASK-0101",
    "verdict": "approved" | "changes_requested" | "rejected",
    "findings": [
      { "category": "correctness", "severity": "none" },
      { "category": "security", "severity": "none" }
    ],
    "turn_index": 42
  },
  "signature": {...}
}
```

El runtime **no produce esta firma** (Claude la genera offline en su wrapper); el runtime solo la almacena y encadena.

---

## 3. Acceptance Criteria

**AC1:** Flag `event_state.agent_signatures_enabled` (default false) apagado; byte-equivalente sin flag encendido.

**AC2:** Estructura JSON del evento `agent.attestation` valida contra schema (seq, type, agent_id, subject_digest, predicate, signature, prev_hash obligatorios).

**AC3:** Nueva función `validate_agent_signatures(enabled, backend_config)` en `protocol_replay.py` implementada; si enabled=false retorna (True, []) sin validar (backward-compatible).

**AC4:** Backend "local-ed25519" implementado; puede verificar firmas Ed25519 desde keyid registrado en config (clave pública, no privada, en repo como config).

**AC5:** Firma cubre `subject_digest || canonical_json(predicate)` determinista (sin timestamp dinámico, sin random).

**AC6:** Revisor (maker ≠ checker) puede producir atestación independiente; runtime solo almacena/encadena, NO valida autoría del revisor (confianza delegada al backend externo).

**AC7:** Cambios aditivos en eventlog.py (tipos nuevos), protocol_replay.py (validacion), config (flags, backend); turnos/handoffs existentes SIN cambios (off-by-default).

**AC8:** Neutralidad domain: cero términos de negocio/trading; formato in-toto agnóstico del dominio.

**AC9:** Encoding ASCII en predicados (JSON + metadatos); sin UTF-8 extendido en nombres de agente/role.

---

## 4. Golden Cases

### GC-1: Turnos sin firma (off-by-default)
Ejecutar un turno normal con `agent_signatures_enabled: false`. Verificar:
- Event log sin eventos `agent.attestation`
- `validate_agent_signatures(enabled=False)` retorna (True, [])
- Byte-equivalente a turno sin este módulo

### GC-2: Turno con firma Ed25519 local (happy path)
Ejecutar turno con `agent_signatures_enabled: true, backend: local-ed25519`. Agente Codex firma su turn report. Verificar:
- Evento `agent.attestation` creado con firma válida
- `subject_digest` coincide con hash del artefacto
- `validate_agent_signatures(enabled=True)` ok=true, findings=[]
- Firma verificable offline con clave pública de config

### GC-3: Falsificación detectada (firmas inválidas)
Modificar manualmente `sig` en evento `agent.attestation` (cambiar 1 byte). Ejecutar `validate_agent_signatures(enabled=True)`. Verificar:
- Retorna ok=false
- Findings contiene {"seq": X, "agent_id": "Codex", "error": "signature_invalid"}

### GC-4: Agente no registrado
Crear evento `agent.attestation` con `agent_id: "UnknownAgent"` (no en `agent_registry`). Ejecutar validación. Verificar:
- Finding: {"error": "unknown_agent"}

### GC-5: Atestación de revisor (maker ≠ checker)
Codex produce turno; Claude revisa y firma atestación separada con role="reviewer". Verificar:
- Evento `agent.attestation` de Claude con `reviewed_work_agent: Codex`
- `verdict` aprobado/rechazado registrado
- Firma del revisor verificable independientemente

### GC-6: Predicado incompleto
Crear evento sin campo `task_id` en predicado. Ejecutar validación de schema. Verificar:
- Falla con "missing predicate field"

### GC-7: Precedencia: prev_hash + firma
Encadenar dos turnos; el segundo tiene prev_hash Y firma. Ejecutar SPEC-0070 + SPEC-0071 juntas. Verificar:
- Ambas validaciones pasan (prev_hash chain ok, signatures ok)
- Hash anterior enlaza correctamente

### GC-8: Determinismo de firma
Ejecutar mismo turno dos veces (replay). Verificar:
- subject_digest idéntico (no timestamp en el sujeto)
- Firma reproduce con seed fijo (no hay random en construcción de sig)

### GC-9: Turnos legados (pre-signatures)
Log histórico sin eventos `agent.attestation`. Ejecutar `validate_agent_signatures(enabled=True)`. Verificar:
- Retorna (True, []) (no hay firmas para validar, no es error)

### GC-10: Migracion: encender flag post-hoc
Inicializar log sin firmas. Luego flip `agent_signatures_enabled: false -> true`. Replay. Verificar:
- Eventos previos sin firma: validador los ignora (backward-compatible)
- Nuevos eventos requieren firma si enabled=true

---

## 5. Plan de Prueba

### Unidad
- `test_validate_agent_signatures` (10 tests):
  - enabled=false returns (True, [])
  - ed25519 sig válida verifica ok
  - sig alterada rechazada
  - agent no registrado detectado
  - predicado incompleto flagged
  - hash subject reconstructible determinista

### Integración (golden cases)
- `examples/agent_signature_cases/`:
  - caso1_off_by_default.json (turno sin sigs, enabled=false)
  - caso2_ed25519_valid.json (turno con sig válida)
  - caso3_sig_invalid.json (sig alterada)
  - caso4_unknown_agent.json (agent_id no registrado)
  - caso5_reviewer_attestation.json (revisor firma por separado)
  - caso6_predicate_incomplete.json (schema fail)
  - caso7_prev_hash_and_sig.json (SPEC-0070 + SPEC-0071 juntas)
  - caso8_determinismo.json (replay identico)
  - caso9_legacy_no_sigs.json (log viejo sin firmas)
  - caso10_enable_post_hoc.json (flag flip backward-compat)

- Runner: `run_agent_signature_cases.py` (determinista, replay validation, golden snapshot comparison)

### Regresion
- `runtime_loop_cases` (existentes, sin agent_signatures): pasan iguales (off-by-default)
- `runtime_protocol_replay_cases` (SPEC-0070 validation): corren junto a SPEC-0071 validation; pasan juntas

### Determinismo
- `--check` en protocol_replay (sigs no usan timestamp dinámico, random):
  - Calcular hash canonical_json(predicate) dos veces -> identico
  - Verificar sig con replay determinista (sin network, sin random)

---

## 6. Cambios en Archivos

### runtime/eventlog.py

**Nuevas funciones:**
```python
def append_agent_attestation(
    log_path: str,
    agent_id: str,
    subject_digest: str,
    subject_reference: str,
    predicate: dict,
    signature: dict,
    prev_hash: str,
    timestamp: Optional[str] = None
) -> int:
    """Append evento agent.attestation."""

def compute_agent_attestation_sig(
    subject_digest: str,
    predicate: dict,
    backend: str,
    private_key_path: Optional[str] = None
) -> dict:
    """Compute firma Ed25519 / keyless / external."""
```

**Cambios existentes:**
- `append_event()`: add tipo "agent.attestation" a tipos permitidos (aditivo)
- `protocol.config.json`: nuevo flag `event_state.agent_signatures_enabled: false` + `signature_backend` + `signature_config`

### runtime/protocol_replay.py

**Nueva función:**
```python
def validate_agent_signatures(
    log_path: str,
    agent_registry: dict,
    enabled: bool = False,
    backend_config: dict = None
) -> Tuple[bool, List[dict]]:
    """Valida firmas de agente en eventlog."""
```

**Integración:**
- `validate_protocol_state()`: call `validate_agent_signatures` si config.event_state.agent_signatures_enabled
- Reportar findings en return dict

### runtime/llm_turn_wrapper.py

**Cambios aditivos:**
- Función `sign_turn_report(turn_report: dict, agent_id: str, signature_backend: str) -> dict` que retorna `signature` dict para incluir en el report
- Wrapper de agente llama esta función ANTES de enviar report al runtime
- Runtime recibe report con campo `signature` y lo pasa a `agent.attestation` event

### protocol.config.json + protocol.config.template.json

**Nuevos campos en `event_state`:**
```json
{
  "event_state": {
    "chain_enabled": false,
    "agent_signatures_enabled": false,
    "signature_backend": "local-ed25519",
    "signature_config": {
      "backend": "local-ed25519",
      "keyids_public": {
        "Claude": "claude-ed25519-20260101",
        "Codex": "codex-ed25519-20260101"
      },
      "keydir": "~/.agent_keys"
    }
  }
}
```

### Area_comun/protocol/N_AGENT_RUNTIME.md

**Sección nueva:** "Agent Attestation & Maker ≠ Checker"
- Explicar que revisor produce atestación independiente
- Ejemplo de flujo: Codex produce turno con sig; Claude revisa y firma atestación de aprobación
- Verificación offline: `python -m runtime.protocol_replay validate-sigs`

---

## 7. Notas de Implementación

- **Sin producción de firmas en runtime:** el runtime NO invoca ninguna clave privada. Las firmas las produce el wrapper del agente (fuera del repo, bajo control de cada participante).
- **Backward-compatible:** flag off-by-default; sin cambios a turnos existentes; validación es opt-in por instancia.
- **Determinismo:** no se usan timestamps en `subject_digest` o predicado; solo canonical_json + hash.
- **Neutralidad:** predicado genérico, sin términos de negocio; in-toto schema agnóstico del dominio.

---

## 8. Decisión: Clave Privada Fuera del Repo

Se respeta DECISION-0029 sec.5 "Sin secretos en el repo":
- Claves privadas viven en wrapper del agente (usuario home, vault, etc.)
- Repo solo contiene claves públicas (en config) y firmas verificables
- No hay arch secreto

---

## 9. Referencias

- DECISION-0029: "Firmantes cruzados sin consenso"
- in-toto Statement v1: https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md
- SPEC-0070: prev_hash encadenado
- SPEC-0023 (DECISION-0023): Firma de releases (análogo backend configurable)

