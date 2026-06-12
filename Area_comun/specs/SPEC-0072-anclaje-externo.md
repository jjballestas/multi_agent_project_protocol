---
spec_id: SPEC-0072
title: "Anclaje externo periódico de la cadena (DECISION-0029 pieza 2c)"
status: proposed
date_created: 2026-06-13
date_updated: 2026-06-13
authored_by: Claude (architect)
task_id: TASK-0103
related_decisions: [DECISION-0029, DECISION-0023, DECISION-0019]
---

# SPEC-0072 — Anclaje externo periódico de la cadena

**Pieza 2c de DECISION-0029:** El digest de cabeza de la cadena (prev_hash + firmas por agente) se publica periódicamente en al menos un medio fuera del control de escritura del runtime. Backend configurable, vendor-neutral. Off-by-default.

---

## 1. Resumen

El eventlog del runtime es la fuente de verdad local. Sin anclaje externo, un adversario que controle el runtime podría:
- Fabricar eventos (A3 sin mitigación)
- Reescribir historia anclada (A3 sin mitigación)

**SPEC-0072** ancla el digest de cabeza periódicamente en **medios ajenos al runtime**, detectables post-hoc:

- **Git remoto independiente:** push del HEAD hash a un branch de auditoría en un repo separado (ej. GitHub organización auditora)
- **Log de transparencia:** append del HEAD hash a un log público (ej. Rekor, protocolo CT, o log privado auditable)
- **Sellado RFC 3161:** timestamping criptográfico por autoridad externa (TSA)

**Propiedad objetivo:** Detecta reescritura de historia que ya fue anclada (A3-restringido). RIESGO RESIDUAL: omisión de eventos aún no anclados (ventanas cortas mitigan).

---

## 2. Diseño Técnico

### 2.1 Estructura del anclaje

Cada anclaje se registra como evento `chain.anchor` en el eventlog:

```json
{
  "seq": 150,
  "timestamp": "2026-06-13T12:30:00Z",
  "type": "chain.anchor",
  "actor_id": "runtime",
  "head_digest": "sha256:abc123def456...",
  "head_seq": 149,
  "prev_hash_chain": "sha256:xyz...",
  "anchor_backend": "git-remote" | "transparency-log" | "rfc3161-tsa",
  "anchor_config": {
    "backend": "git-remote",
    "remote_url": "https://github.com/audit-org/eventlog-anchors.git",
    "branch": "audits/multi_agent_protocol",
    "identity": "runtime-anchor-key-20260101"
  },
  "anchor_evidence": {
    "git_commit": "fc7d3a2b1e...",
    "git_timestamp": "2026-06-13T12:30:15Z",
    "proof": "base64-encoded-receipt"
  },
  "prev_hash": "sha256:prev_hash_n-1"
}
```

### 2.2 Algoritmo de anclaje periódico

```python
def periodic_anchor_if_due(
    log_path: str,
    config: dict,
    interval_seconds: int = 3600,
    last_anchor_timestamp: Optional[str] = None
) -> Optional[dict]:
    """
    Ancla el HEAD de la cadena si ha pasado interval_seconds desde el último anclaje.
    
    Args:
        log_path: ruta al eventlog
        config: event_state.anchor_config (backend, remote_url, etc.)
        interval_seconds: segundos entre anclajes (default 1 hora)
        last_anchor_timestamp: timestamp del último anclaje registrado
    
    Returns:
        Evento chain.anchor si se ejecutó anclaje, None si no estaba vencido
    """
    if not config.get("enabled", False):
        return None
    
    # Leer HEAD del log
    head_event = read_last_event(log_path)
    head_digest = canonical_hash(head_event)
    
    # Verificar si está vencido
    now = datetime.utcnow()
    if last_anchor_timestamp:
        elapsed = (now - parse_iso_timestamp(last_anchor_timestamp)).total_seconds()
        if elapsed < interval_seconds:
            return None  # No vencido, skip
    
    # Ejecutar anclaje según backend
    backend = config.get("backend", "git-remote")
    
    if backend == "git-remote":
        proof = anchor_to_git_remote(
            head_digest=head_digest,
            remote_url=config["remote_url"],
            branch=config.get("branch", "audits/default"),
            identity=config.get("identity")
        )
    elif backend == "transparency-log":
        proof = anchor_to_transparency_log(
            head_digest=head_digest,
            log_endpoint=config["log_endpoint"],
            identity=config.get("identity")
        )
    elif backend == "rfc3161-tsa":
        proof = anchor_via_rfc3161(
            head_digest=head_digest,
            tsa_url=config["tsa_url"],
            hash_algo=config.get("hash_algo", "sha256")
        )
    else:
        raise ValueError(f"Unknown anchor backend: {backend}")
    
    # Crear evento chain.anchor
    anchor_event = {
        "type": "chain.anchor",
        "actor_id": "runtime",
        "head_digest": head_digest,
        "head_seq": head_event["seq"],
        "anchor_backend": backend,
        "anchor_config": {k: v for k, v in config.items() if k != "tsa_url"},  # sin secretos
        "anchor_evidence": proof,
        "timestamp": now.isoformat() + "Z",
        "prev_hash": canonical_hash(head_event)  # cadena continúa
    }
    
    return anchor_event
```

### 2.3 Backend: Git remoto independiente

```python
def anchor_to_git_remote(
    head_digest: str,
    remote_url: str,
    branch: str,
    identity: str
) -> dict:
    """
    Ancla el HEAD digest en un branch de un repo git externo.
    
    Estructura en el repo remoto:
    
        audits/multi_agent_protocol/
            HEAD
            anchors.log
    
    HEAD: archivo plain text con el último digest anclado
    anchors.log: log append-only de todos los anclajes (timestamp + digest + commit_hash_origen)
    """
    import subprocess
    
    # Clone o fetch del remoto
    tmpdir = mkdtemp()
    subprocess.run(
        ["git", "clone", "-b", branch, remote_url, tmpdir],
        check=True,
        capture_output=True
    )
    
    # Actualizar HEAD y anchors.log
    head_file = Path(tmpdir) / "HEAD"
    anchors_log = Path(tmpdir) / "anchors.log"
    
    now_iso = datetime.utcnow().isoformat() + "Z"
    head_file.write_text(head_digest)
    
    with open(anchors_log, "a") as f:
        f.write(f"{now_iso} {head_digest} {identity}\n")
    
    # Commit y push
    subprocess.run(["git", "config", "user.email", "runtime@local"], cwd=tmpdir, check=True)
    subprocess.run(["git", "config", "user.name", "Runtime"], cwd=tmpdir, check=True)
    subprocess.run(["git", "add", "HEAD", "anchors.log"], cwd=tmpdir, check=True)
    subprocess.run(
        ["git", "commit", "-m", f"Anchor: {head_digest[:12]}... at {now_iso}"],
        cwd=tmpdir,
        check=True
    )
    commit_hash = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=tmpdir,
        text=True
    ).strip()
    
    subprocess.run(["git", "push", "origin", branch], cwd=tmpdir, check=True)
    
    # Limpiar
    shutil.rmtree(tmpdir)
    
    return {
        "backend": "git-remote",
        "git_commit": commit_hash,
        "git_timestamp": now_iso,
        "proof": f"branch={branch}, commit={commit_hash}"
    }
```

### 2.4 Verificación de anclaje (validación offline)

Nueva función en `protocol_replay.py`:

```python
def verify_anchor_monotonicity(
    log_path: str,
    anchor_backend_config: dict,
    enabled: bool = False
) -> Tuple[bool, List[dict]]:
    """
    Verifica que los anclajes sean monótonos (ningún reordenamiento).
    
    Si anchor_backend=git-remote, fetch el remoto y verifica que:
    - anchors.log sea append-only
    - cada hash esté en el orden correcto (seq ascendente)
    - ningún hash esté en el log local pero ausente del remoto (omisión)
    
    Returns:
        (ok: bool, findings: List[{seq, error}])
    """
    if not enabled:
        return True, []
    
    findings = []
    last_seq = -1
    
    with open(log_path) as f:
        for line in f:
            event = json.loads(line)
            if event.get("type") != "chain.anchor":
                continue
            
            seq = event["seq"]
            if seq <= last_seq:
                findings.append({
                    "seq": seq,
                    "error": "anchor_reordered"
                })
            last_seq = seq
    
    # Si backend=git-remote, fetch y verifica monotonía remota
    if anchor_backend_config.get("backend") == "git-remote":
        remote_ok = verify_git_anchor_monotonicity(
            log_path=log_path,
            remote_url=anchor_backend_config["remote_url"],
            branch=anchor_backend_config.get("branch")
        )
        if not remote_ok:
            findings.append({
                "seq": None,
                "error": "remote_anchor_not_monotonic"
            })
    
    return len(findings) == 0, findings
```

### 2.5 Config en protocol.config.json

```json
{
  "event_state": {
    "chain_enabled": false,
    "agent_signatures_enabled": false,
    "anchor_enabled": false,
    "anchor_config": {
      "backend": "git-remote",
      "remote_url": "https://github.com/audit-org/eventlog-anchors.git",
      "branch": "audits/multi_agent_protocol",
      "identity": "runtime-anchor-key-20260101",
      "interval_seconds": 3600,
      "retry_max_attempts": 3,
      "retry_backoff_seconds": 10
    }
  }
}
```

---

## 3. Acceptance Criteria

**AC1:** Flag `event_state.anchor_enabled` (default false) apagado; byte-equivalente sin flag.

**AC2:** Evento `chain.anchor` valida contra schema; campos obligatorios: seq, type, head_digest, head_seq, anchor_backend, anchor_evidence, prev_hash.

**AC3:** Backend git-remote implementado; clona remoto, actualiza HEAD + anchors.log, pushea.

**AC4:** Backend rfc3161-tsa implementado (futuro, puede ser stub); mantiene signature_backend compatible.

**AC5:** `periodic_anchor_if_due()` respeta `interval_seconds`; no ancla si no está vencido.

**AC6:** Verificador `verify_anchor_monotonicity()` detecta reordenamiento (seq no-ascendente) en el log.

**AC7:** Git remoto: push falla → evento no se crea, retry configurable (no corrompe el log local).

**AC8:** Sin secretos en config; TSA URL es pública; identidad puede ser nombre (no credencial).

**AC9:** Cambios aditivos (nuevos eventos, config, validador); turnos/cadena/firmas existentes SIN cambios.

**AC10:** Encoding ASCII en metadatos (backend, branch, identity); sin UTF-8 extendido.

---

## 4. Golden Cases

### GC-1: Anclaje desactivado (off-by-default)
Ejecutar runtime con `anchor_enabled: false`. Verificar:
- Sin eventos `chain.anchor` en el log
- `verify_anchor_monotonicity(enabled=False)` retorna (True, [])
- Byte-equivalente a run sin este módulo

### GC-2: Anclaje a git-remote exitoso (happy path)
Ejecutar anclaje a repo de prueba local. Verificar:
- Evento `chain.anchor` creado con proof válido
- Git remoto: HEAD contiene el hash correcto
- anchors.log registra el anclaje
- `head_seq` coincide con seq del último evento anterior

### GC-3: Remoto inaccesible, sin corrupción local
Simular remoto down (network error). Verificar:
- Evento `chain.anchor` NO se crea
- Log local intacto (sin evento fallido)
- Retry se ejecuta según config
- Eventual anclaje exitoso cuando remoto vuelve

### GC-4: Intervalo no vencido, skip anclaje
Ejecutar `periodic_anchor_if_due()` dos veces en <interval_seconds. Verificar:
- Primera ejecución: anclaje exitoso, evento creado
- Segunda ejecución: skip (retorna None), sin evento duplicado

### GC-5: Reordenamiento detectado
Modificar manualmente el log: cambiar seq de dos eventos `chain.anchor` (invertir orden). Ejecutar `verify_anchor_monotonicity()`. Verificar:
- Retorna ok=false
- Findings contiene {"seq": X, "error": "anchor_reordered"}

### GC-6: Precedencia: prev_hash + firma + anclaje
Ejecutar 3 turnos; cada uno: produce evento, se firma, se ancla. Verificar:
- SPEC-0070 chain válida (prev_hash correcto)
- SPEC-0071 signatures válidas (firmas verificables)
- SPEC-0072 anchors válidos (monotonía, git proof)
- Las tres validaciones pasan juntas

### GC-7: Git remoto: anchors.log es append-only
Ejecutar 5 anclajes secuenciales. Verificar:
- anchors.log contiene 5 líneas (append, no sobrescribe)
- Cada línea: timestamp + hash + identity
- Hashes en orden (primero al último)

### GC-8: Determinismo de prueba
Ejecutar mismo anclaje 2 veces en repo limpio. Verificar:
- Git commit hash idéntico (timestamp canonicalizado, sin random)
- HEAD contenido exacto

### GC-9: Turnos legados (sin anclaje)
Log histórico sin eventos `chain.anchor`. Ejecutar `verify_anchor_monotonicity(enabled=True)`. Verificar:
- Retorna (True, []) (no hay anclajes, no es error)

### GC-10: Activación post-hoc
Inicializar con `anchor_enabled: false`. Luego flip true. Ejecutar anclaje. Verificar:
- Nuevos anclajes se crean
- Log anterior sin anclajes: validador los ignora (backward-compatible)

---

## 5. Plan de Prueba

### Unidad
- `test_periodic_anchor_if_due` (8 tests):
  - enabled=false returns None
  - enabled=true, vencido: ejecuta anclaje
  - enabled=true, no vencido: skip (retorna None)
  - interval_seconds=0: siempre ancla
  - retry_max_attempts: reintentos en error de red

- `test_verify_anchor_monotonicity` (6 tests):
  - eventos en orden: ok=true
  - seq reordenado: detectado
  - anchor remoto monotónico: ok
  - anchors.log append-only: verificado

### Integración (golden cases)
- `examples/anchor_cases/`:
  - caso1_off_by_default.json (run sin anchors, enabled=false)
  - caso2_git_remote_ok.json (anclaje a repo local exitoso)
  - caso3_remote_down.json (remoto inaccesible, retry)
  - caso4_interval_not_due.json (skip segundo anclaje)
  - caso5_reorder_detected.json (seq invertido, error detectado)
  - caso6_chain_sig_anchor.json (prev_hash + firma + anclaje juntos)
  - caso7_git_log_append.json (5 anclajes secuenciales, log append-only)
  - caso8_determinismo.json (replay idéntico)
  - caso9_legacy_no_anchors.json (log viejo sin anchors, validador ok)
  - caso10_enable_post_hoc.json (flag flip backward-compat)

- Runner: `run_anchor_cases.py` (determinista, git reset entre casos, snapshot comparison)

### Regresión
- `runtime_loop_cases` (existentes): pasan iguales (off-by-default)
- `runtime_protocol_replay_cases` (SPEC-0070/0071): corren junto a SPEC-0072; pasan juntas

### Determinismo
- `--check` en protocol_replay: timestamp canonicalizado (no dinámico), git commit reproducible

---

## 6. Cambios en Archivos

### runtime/orchestrator.py

**Nueva función:**
```python
def anchor_if_due() -> Optional[dict]:
    """Ancla HEAD si está vencido; retorna evento o None."""
```

**Integración en main loop:**
- Post-commit: call `anchor_if_due()`
- Si retorna evento: append al log + trace

### runtime/protocol_replay.py

**Nueva función:**
```python
def verify_anchor_monotonicity(
    log_path: str,
    anchor_backend_config: dict,
    enabled: bool = False
) -> Tuple[bool, List[dict]]:
    """Verifica que anclajes sean monótonos."""
```

**Integración:**
- `validate_protocol_state()`: call si `event_state.anchor_enabled`

### protocol.config.json + protocol.config.template.json

**Nuevos campos en `event_state`:**
```json
{
  "anchor_enabled": false,
  "anchor_config": {
    "backend": "git-remote",
    "remote_url": "https://github.com/audit-org/eventlog-anchors.git",
    "branch": "audits/multi_agent_protocol",
    "identity": "runtime-anchor-key-20260101",
    "interval_seconds": 3600,
    "retry_max_attempts": 3,
    "retry_backoff_seconds": 10
  }
}
```

### Area_comun/protocol/N_AGENT_RUNTIME.md

**Sección nueva:** "External Anchoring & Tamper-Evidence"
- Explicar que anclaje es auditable post-hoc
- Monotonía = reordenamiento detectado
- Ventanas de riesgo: eventos no anclados aún

---

## 7. Notas de Implementación

- **Sin auth en runtime:** el runtime NO posee credenciales del remoto. Config proporciona remote_url pública; push requiere que la máquina tenga SSH key o token en `~/.git-credentials` (fuera del repo, bajo control del operador).
- **Backward-compatible:** flag off-by-default; sin cambios a logs existentes.
- **Determinismo:** timestamps canonicalizados; no hay random en proof.
- **Neutralidad:** predicado genérico, sin términos de negocio; backends agnósticos del dominio.

---

## 8. Futuro: Otros Backends

- **Rekor (sigstore transparency log):** append el HEAD hash a log público sigstore; no requiere repo git; prueba criptográfica.
- **RFC 3161 TSA:** timestamping criptográfico por autoridad externa; signature verificable offline.
- **IPFS:** hash + publish a IPFS; contenido replicado peer-to-peer.

---

## 9. Referencias

- DECISION-0029: "Firmantes cruzados sin consenso"
- RFC 3161: Timestamp Protocol (https://tools.ietf.org/html/rfc3161)
- Sigstore Rekor: https://github.com/sigstore/rekor
- SPEC-0070: prev_hash encadenado
- SPEC-0071: firma por agente
- DECISION-0023 (firma de releases): análogo backend configurable

