---
spec_id: SPEC-0076
title: "prev_hash encadenado en el eventlog (DECISION-0029 pieza 2a)"
status: draft
date_created: 2026-06-13
date_updated: 2026-06-13
authored_by: Claude (architect)
task_id: TASK-0101
related_decisions: [DECISION-0029, DECISION-0017, DECISION-0022, DECISION-0014]
---

# SPEC-0076 – prev_hash encadenado en el eventlog

**Resumen ejecutivo:** Implementar encadenado criptográfico (SHA256) en el eventlog sin romper
compatibilidad con el log legacy. El flag `event_state.chain_enabled` controla su activación;
off-by-default. Preservar verificabilidad bajo prune/archive versionando el hash de corte en el
archivo prunado.

---

## 1. Contexto y Justificación

Ver DECISION-0029 (pieza 2a) y DECISION-0017 para la arquitectura de eventlog.

**Problema:** Hoy `eventlog.py` (runtime v0.11.0) autentica eventos con HMAC-SHA256 simétrico
(evento aislado), sin encadenado entre eventos. Esto hace indetectable la manipulación selectiva:
un administrador o compromiso del runtime puede borrar eventos intermedios, reordenar, o insertar
sin que ninguna verificación lo detecte. El encadenado es **prerequisito** para:

- Firma por agente (TASK-0102): necesita una cadena auditable cuyas mutaciones sean demostrables.
- Anclaje externo (TASK-0103): necesita proteger la cadena contra reescritura total.

---

## 2. Diseño Técnico

### 2.1 Estructura de evento con prev_hash

Cada evento en el log incluye un nuevo campo `prev_hash` bajo el flag `event_state.chain_enabled`:

```json
{
  "seq": 123,
  "timestamp": "2026-06-13T10:30:45Z",
  "event_type": "task_status",
  "agent": "Claude",
  "payload": {...},
  "prev_hash": "sha256_del_evento_anterior_o_genesis"
}
```

**Campo `prev_hash`:**
- Tipo: string (hexadecimal SHA256, 64 caracteres).
- Valor en genesis: hash de `protocol.config.json` (curado en tiempo de creación del log).
- Valor en resto: `SHA256(canonical_json(evento_{n-1}) || prev_hash_{n-1})` en base canónica.
- Presente solo si `event_state.chain_enabled == true` (retrocompatibilidad: log existente sin
  prev_hash sigue validando en modo legacy).

**Canonical form para hash:**
```
event_canonical = JSON.stringify(evento_actual, sort_keys, ensure_ascii, separators=(",", ":"))
prev_hash_n = SHA256(event_canonical || prev_hash_{n-1})
```

El orden de inclusión es:
1. Evento canonicalizado (sin el campo `prev_hash` aún).
2. El `prev_hash` del evento anterior.

Ambos se concatenan como strings binarios (UTF-8) y se hashean.

### 2.2 Genesis

**Definición:** El primer evento de una cadena tiene `prev_hash` = `SHA256(canonical_json(protocol.config.json))`.

**Justificación (respuesta a Q1):** `protocol.config.json` es versionado, auditado y reproduce
el estado de activación de la cadena. Usar su hash como raíz permite que un validador:
- Sin acceso a la cadena previa (e.g., después de un prune), reconstruya la raíz.
- Verificar que la cadena comenzó bajo el protocolo esperado (versión, event_state flags).

**Cálculo:** 
```python
import hashlib
import json
config = json.load(open("protocol.config.json"))
genesis_prev_hash = hashlib.sha256(
    json.dumps(config, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    .encode("utf-8")
).hexdigest()
```

**Caso especial - migración:** Si se activa `event_state.chain_enabled` en un log existing
sin prev_hash:
- Registrar un evento `chain_genesis` con `prev_hash = genesis_prev_hash` y `event_type = "chain.genesis"`.
- Este evento no materializa estado; su único propósito es anclar la raíz.
- Los eventos posteriores encadenan contra este genesis.
- El validador lo detecta y valida la cadena desde ahí en adelante.

### 2.3 Cálculo de cadena

**Pseudocódigo:**

```python
def compute_chain_hash(event_dict: dict, prev_hash: str) -> str:
    """Calcula prev_hash para el siguiente evento dado este evento."""
    event_canonical = canonical_json(event_dict)
    combined = event_canonical + prev_hash
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()

def build_event_with_chain(event_payload: dict, prev_hash_of_previous: str) -> dict:
    """Construye un evento con su prev_hash."""
    event = {
        "seq": event_payload["seq"],
        "timestamp": event_payload["timestamp"],
        ...
        # todos los campos del evento
    }
    # El evento NO incluye su propio prev_hash en canonical form;
    # el prev_hash es el hash del evento anterior.
    event_dict_for_hash = deepcopy(event)
    # Calcular prev_hash como hash del evento anterior (sin prev_hash field):
    prev_hash_of_this = compute_chain_hash(event_dict_for_hash, prev_hash_of_previous)
    event["prev_hash"] = prev_hash_of_this  # Incluir para almacenamiento
    return event
```

**Nota:** El `prev_hash` de evento `n` apunta a evento `n-1`. Los campos `seq`, `timestamp`, etc.
NO cambian; solo se añade `prev_hash`.

### 2.4 Cambios en eventlog.py

**Archivos a modificar:**
- `runtime/eventlog.py` – append, read, auth functions.
- `runtime/protocol_replay.py` – validator.
- `protocol.config.json` – nuevo flag `chain_enabled` (default false).

**Cambios en eventlog.py:**

1. **Función `observability_chain_enabled(config)`:**
   ```python
   def chain_enabled(config: dict[str, Any] | None) -> bool:
       event_state = (config or {}).get("event_state") or {}
       return event_state.get("chain_enabled") is True
   ```

2. **Función `compute_genesis_prev_hash(config_path)`:**
   ```python
   def compute_genesis_prev_hash(config_path: Path = Path("protocol.config.json")) -> str:
       if not config_path.exists():
           raise EventLogError(f"Config not found: {config_path}")
       config_text = config_path.read_text(encoding="utf-8-sig")
       config = json.loads(config_text)
       return canonical_hash(config)
   ```

3. **Función `append_event()` actualizada:**
   - Si `chain_enabled`, leer el último evento del log.
   - Calcular `prev_hash` del nuevo evento.
   - Incluirlo en el evento antes de serializar.

4. **Función `read_jsonl_torn_safe()` sin cambios** (sigue leyendo eventos, incluido prev_hash
   si está presente).

**Capa de compatibilidad:**

- Los eventos sin `prev_hash` (log legacy) se consideran válidos en modo legacy (flag off).
- Al validar un log con `chain_enabled == true`, se espera que TODOS los eventos tengan
  `prev_hash` O exista un evento `chain.genesis` que los preceda.
- Un log sin genesis pero con flag on es error de validación `chain.genesis_missing`.

---

## 3. Validador de Cadena

**Ubicación:** `runtime/protocol_replay.py` (función nueva `validate_chain()` o integrada
en `validate_eventlog()`).

### 3.1 Algoritmo

```python
def validate_chain(events: list[dict], config: dict) -> tuple[bool, str]:
    """
    Valida que la cadena prev_hash sea correcta (detecta alteracion, insercion, borrado, reordenamiento).
    
    Retorna: (is_valid, reason)
    """
    if not chain_enabled(config):
        return True, "chain validation disabled"
    
    if not events:
        return True, "no events"
    
    # Buscar genesis
    genesis_idx = -1
    for i, evt in enumerate(events):
        if evt.get("event_type") == "chain.genesis":
            genesis_idx = i
            break
    
    if genesis_idx == -1:
        # Log sin genesis; si chain_enabled, error
        return False, "chain_enabled but no chain.genesis event"
    
    # Validar que genesis tiene prev_hash correcto
    expected_genesis = compute_genesis_prev_hash(Path("protocol.config.json"))
    actual_genesis = events[genesis_idx].get("prev_hash", "")
    if actual_genesis != expected_genesis:
        return False, f"genesis mismatch: expected {expected_genesis}, got {actual_genesis}"
    
    # Validar encadenado desde genesis
    prev_hash = events[genesis_idx].get("prev_hash")
    for i in range(genesis_idx + 1, len(events)):
        evt = events[i]
        evt_dict = deepcopy(evt)
        evt_dict.pop("prev_hash", None)  # Quitar prev_hash para canonical form
        
        computed = compute_chain_hash(evt_dict, prev_hash)
        actual = evt.get("prev_hash", "")
        
        if computed != actual:
            # 4 casos diagnosticables:
            # a) alteracion puntual: prev_hash incorrecto dado evento intacto
            # b) borrado/insercion: salto en seq (si no es contiguo)
            # c) reordenamiento: orden de seq no-monotono
            
            # Reporte detallado:
            if evt.get("seq") != (events[i-1].get("seq", -1) + 1):
                return False, f"gap or reorder at seq {evt.get('seq')}: expected {events[i-1].get('seq') + 1}"
            else:
                return False, f"corruption at seq {evt.get('seq')}: hash mismatch"
        
        prev_hash = actual
    
    return True, "chain valid"
```

### 3.2 Detección de las 4 manipulaciones

| Manipulación | Detección | Firma |
|---|---|---|
| **Alteración puntual** | `prev_hash` no coincide, seq contiguo | hash mismatch en evento N |
| **Inserción (evento falso)** | seq no-contiguo O cadena brinca | gap/reorder en seq |
| **Borrado (evento omitido)** | seq salta; cadena no verifica | gap en seq |
| **Reordenamiento** | seq no-monotono; cadena no verifica | seq out of order |

El validador reporta **qué tipo** de manipulación detectó basándose en el patrón seq + hash.

---

## 4. Interacción con prune/archive (Respuesta a Q2)

**Problema:** DECISION-0014 permite prune de eventos viejos al archivo. Si borramos eventos
del log principal, la cadena se rompe a menos que preservemos el punto de corte.

**Solución:**

1. **Archivo de header:** Antes de prune, escribir `runtime/state/archives/chain_manifest.json`:
   ```json
   {
     "prune_date": "2026-06-13T10:30:00Z",
     "last_seq_before_prune": 120,
     "last_event_hash": "sha256_del_evento_seq_120",
     "prev_hash_before_prune": "sha256_que_apunta_a_seq_119",
     "events_archived": "events_0-120.jsonl.gz",
     "protocol_config_hash_at_prune": "..."
   }
   ```

2. **Evento de anclaje post-prune:** Al reactivar el log después de prune, el primer evento nuevo
   es un evento especial `chain.archive_boundary`:
   ```json
   {
     "seq": 121,
     "event_type": "chain.archive_boundary",
     "timestamp": "...",
     "archive_ref": "chain_manifest.json",
     "prev_hash": "valor_replicado_desde_manifest"
   }
   ```

3. **Validador híbrido:** El validador de cadena:
   - Si encuentra `chain.archive_boundary`, valida que su `prev_hash` coincida con el registro
     en el manifest.
   - Luego valida la cadena desde ese punto en adelante.
   - Para verificabilidad completa, exige que el manifest esté versionado en git (signed).

**Nota técnica:**
- El manifest es un artefacto de prune, no parte del log principal.
- Se archiva junto con los eventos prunados en `ARCHIVE_DIR`.
- El validador puede reconstruir la cadena sin cargar todos los eventos previos si confía
  en la integridad del manifest.

**Golden case para Q2:**
```
1. Log normal: seq 0-120
2. Prune: eventos 0-110 archivados, manifest escrito
3. Reactivar: primer nuevo evento (seq 121) es chain.archive_boundary con prev_hash del 110
4. Validar: reconoce boundary, valida manifest, valida 111-120, valida 121+
5. Resultado: cadena íntegra incluso con gap de archive
```

---

## 5. Acceptance Criteria

**AC1 – Campo prev_hash bajo flag off-by-default:**
- [ ] `protocol.config.json` incluye `event_state.chain_enabled` (default: false).
- [ ] Cuando flag=false, eventos no incluyen `prev_hash`.
- [ ] Cuando flag=true, TODOS los eventos nuevos incluyen `prev_hash`.
- [ ] No hay cambios en log existente; comportamiento legacy intacto.

**AC2 – Genesis correctamente calculado:**
- [ ] Función `compute_genesis_prev_hash()` existe y es determinista.
- [ ] Genesis = SHA256(canonical_json(protocol.config.json)).
- [ ] En migración de log legacy, evento `chain.genesis` creado automáticamente con prev_hash correcto.

**AC3 – Validador detecta las 4 manipulaciones:**
- [ ] Alteración puntual: hash mismatch reportado.
- [ ] Inserción: gap en seq O hash brinca detectado.
- [ ] Borrado: seq salta (missing intermediate) reportado.
- [ ] Reordenamiento: seq no-monotono reportado como out-of-order.
- [ ] Cada manipulación tiene un golden case reproducible.

**AC4 – Compatibilidad con prune/archive:**
- [ ] Manifest creado antes de prune, archivado junto con eventos.
- [ ] Evento `chain.archive_boundary` insertado correctamente después de prune.
- [ ] Validador híbrido reconoce boundary y valida cadena post-prune.
- [ ] Golden case: cadena verifica a través del punto de prune.

**AC5 – Validador, neutralidad y encoding verdes:**
- [ ] `scripts/validate_collaboration_state.ps1` pasa (no errores de schema).
- [ ] `domain_neutrality` scan limpio (no términos de negocio en core files).
- [ ] `scan_encoding` limpio (ASCII en canal, UTF-8 en datos JSON).
- [ ] Sin secretos en repo.

**AC6 – Handoff con evidencia:**
- [ ] Versión reproducible de `eventlog.py`, `protocol_replay.py`.
- [ ] Golden cases con traces reproducibles (no aleatorios, seeds fijos si es necesario).
- [ ] Documentación de decisiones en la tarea (Q1, Q2 respondidas).

---

## 6. Test Plan y Golden Cases

### 6.1 Estructura de golden cases

Directorio: `examples/chain_cases/`

Cada caso es independiente (sin estado compartido entre casos):
- Archivo de log (`events_<caso>.jsonl`).
- Archivo de config (`config_<caso>.json`) con flags pertinentes.
- Script de validación (`test_<caso>.py` o `.sh`) que corre el validador.
- Expected output (stderr/stdout o report JSON).

### 6.2 Golden Cases

#### **GC-1: Cadena válida (happy path)**
- Input: 10 eventos secuenciales con prev_hash correcto.
- Esperado: ✓ Validación exitosa.
- Descripción: Línea base; valida que no haya falsos positivos.

#### **GC-2: Alteración puntual (evento 5 mutado)**
- Input: 10 eventos; evento seq=5 tiene un campo `payload.value` cambiado.
- Esperado: ✗ Validación falla con "corruption at seq 5: hash mismatch".
- Descripción: Demuestra que cambios en payload rompen la cadena.

#### **GC-3: Borrado de evento intermedio (seq 5 omitido)**
- Input: 10 eventos originales; evento seq=5 completamente removido → seq 4, 6, 7...
- Esperado: ✗ Validación falla con "gap at seq 6: expected 5".
- Descripción: Demuestra que omisión es detectable.

#### **GC-4: Reordenamiento (seq 7 y 8 swapped)**
- Input: 10 eventos; orden: 1,2,3,4,5,6,8,7,9,10 (7 y 8 intercambiados).
- Esperado: ✗ Validación falla con "seq out of order at position X".
- Descripción: Demuestra que el orden no puede manipularse.

#### **GC-5: Inserción de evento falso (entre 5 y 6)**
- Input: 10 eventos originales + 1 falso insertado en medio (seq 5.5 o renumerado → 11 eventos).
- Esperado: ✗ Validación falla (gap o hash mismatch).
- Descripción: Demuestra que eventos ficticios rompen la cadena.

#### **GC-6: Log legacy sin prev_hash (chain_enabled=false)**
- Input: 10 eventos antiguos sin `prev_hash`, config con `chain_enabled=false`.
- Esperado: ✓ Validación exitosa (legacy mode).
- Descripción: Compatibilidad hacia atrás.

#### **GC-7: Migración de log legacy a cadena (chain_enabled=true)**
- Input: Log legacy de 5 eventos + activar `chain_enabled=true`.
- Esperado: Genesis event creado automáticamente; 4 eventos siguientes encadenados.
- Descripción: Demuestra transición sin ruptura.

#### **GC-8: Genesis mismatch**
- Input: Cadena con `chain.genesis` cuyo `prev_hash` NO coincide con `protocol.config.json`.
- Esperado: ✗ Validación falla con "genesis mismatch".
- Descripción: Demuestra que raíz es validada.

#### **GC-9: Cadena post-prune (archive boundary)**
- Input: 20 eventos; prune a 10 (seq 0-9 archivados, manifest creado); seq 10 es
  `chain.archive_boundary` con prev_hash del seq 9; seq 11-19 encadenados contra boundary.
- Esperado: ✓ Validación exitosa (reconoce boundary, valida a través).
- Descripción: Demuestra integridad tras prune.

#### **GC-10: Boundary missing after prune**
- Input: Cadena prunada pero sin evento `chain.archive_boundary` (gap directo de seq 9 a seq 11).
- Esperado: ✗ Validación falla con "gap at seq 11: expected 10" o "archive_boundary missing".
- Descripción: Demuestra que prune mal ejecutado es detectable.

### 6.3 Ejecución de tests

Script: `examples/chain_cases/run_tests.py`

```bash
python examples/chain_cases/run_tests.py [--verbose] [--golden-case GC-1|GC-2|...]
```

Cada golden case debe:
1. Ser **reproducible**: mismas inputs → mismo resultado (no usar datetime.now(), usar
   timestamps fijos).
2. **Reportar resultado** en formato JSON:
   ```json
   {
     "case": "GC-1",
     "status": "pass",
     "message": "chain valid",
     "events_count": 10,
     "chain_hash": "abc123...",
     "timestamp": "2026-06-13T10:30:00Z"
   }
   ```
3. **Integrable en CI**: exit code 0 si pasa, 1 si falla.

---

## 7. Cambios en archivos

### 7.1 runtime/eventlog.py

**Nuevas funciones:**
- `chain_enabled(config: dict) -> bool`
- `compute_genesis_prev_hash(config_path: Path) -> str`
- `compute_event_prev_hash(event_dict: dict, prev_hash_of_previous: str) -> str`
- `ensure_chain_genesis(events: list[dict], config: dict) -> list[dict]` – crea genesis si falta

**Función `append_event()` modificada:**
- Si `chain_enabled(config)`, calcular prev_hash antes de serializar.
- Incluir en evento.

### 7.2 runtime/protocol_replay.py

**Nueva función:**
- `validate_chain(events: list[dict], config: dict) -> tuple[bool, str]`

**Integración en `validate_eventlog()`:**
- Llamar a `validate_chain()` como chequeo adicional si aplica.
- Reportar hallazgos en `validation_report`.

### 7.3 protocol.config.json

**Nuevo campo en `event_state`:**
```json
"event_state": {
  "enabled": true,
  "materialize": true,
  "enforce": true,
  "authoritative": true,
  "chain_enabled": false
}
```

### 7.4 examples/chain_cases/

- Crear directorio.
- 10 archivos de casos golden (eventos.jsonl + config.json para cada caso).
- Script `run_tests.py` que ejecuta y reporta.

---

## 8. Consideraciones de Seguridad

**Cadena de suposiciones (A1/A2/A3r del modelo DECISION-0029):**

1. **A1 (manipulación post-hoc):** prev_hash detecta cambios en evento aislado (HMAC detectaba
   esto ya); encadenado detecta borrado/reordenamiento (NUEVO).
2. **A2 (suplantación entre agentes):** Detectado por firma del agente (TASK-0102), no por
   prev_hash. prev_hash no atestigua identidad, solo integridad de cadena.
3. **A3-restringido (reescritura por runtime):** prev_hash + anclaje externo (TASK-0103)
   detectan reescritura total. Sin ancla, reescritura local es indetectable.
4. **A4 (operador malicioso):** Fuera de alcance (DECISION-0029 sec. 3).

**Riesgo residual (DECISION-0029):**
- Omisión de eventos aún no anclados (ventana entre último evento y ancla externa).
- Mitigación parcial: ventanas cortas + anclaje frecuente.

**Sin secretos:**
- prev_hash es público (hash determinista de datos públicos).
- Genesis es hash de protocol.config (público, versionado).
- Ningún material secreto entra en cálculos.

---

## 9. Definición de Listo (DoD)

- [ ] SPEC aprobada por el operador.
- [ ] Código de eventlog.py + protocol_replay.py + ejemplos merge a main.
- [ ] Golden cases run 10/10 exitosos.
- [ ] Validador, neutralidad, encoding verdes.
- [ ] Handoff autocontenido: `HANDOFF-TASK-0101-codex-to-claude-1.md` + evidencia (hashes,
      reproducibilidad).
- [ ] TASK-0101 cierra en `done`.
- [ ] TASK-0102 y TASK-0103 promovidas a `ready` (no dependen de cierre de 0101, solo de que
      esté en rama).

---

## 10. Referencias

- DECISION-0029: Firmantes cruzados sin consenso.
- DECISION-0017: Runtime observer.
- DECISION-0022: Runtime como escritor único.
- DECISION-0014: Prune y archive de eventos.
- runtime/eventlog.py: Código actual.
- runtime/protocol_replay.py: Validador actual.
