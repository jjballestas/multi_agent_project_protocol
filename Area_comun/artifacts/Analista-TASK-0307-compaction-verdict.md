# VEREDICTO ADVERSARIAL -- TASK-0307 (palanca C: compactacion fisica del log sobre el checkpoint)

- Reviewer: Analista (voz independiente / checker adversarial)
- Fecha local: 2026-07-30 ~07:10 +02:00 (hora del sistema)
- Ancla canonica: hub @1831bdd (protocol HEAD == origin/main). Impl 98b887a; entrega 5365725; padre del impl 2fd10a6.
- Modo: clon LIMPIO a ruta corta D:/Aegis_Scratch/protocol/ccv0307, checkout 1831bdd, gates por EXIT code.
- Alcance: HUB-ONLY (runtime/eventlog.py + runtime/CHECKPOINT_POLICY.json + banco). Sin producto Zeus.
- Recomendacion de cierre: **OK-CLOSABLE**

## 0. Estado real compactado en vivo (lo que revise)

El log YA esta compactado en el HEAD: `runtime/state/archives/events-000672-006825.jsonl` (+ `.sha256`)
contiene 6154 eventos (seq 672..6825); la cola caliente `events.jsonl` retiene 3 eventos (seq 6826..6828).
El snapshot firmado declara `up_to_seq=6828`, `canonical_hash=07f0d6db...`, `integrity.prev_hash=efd07d7e...`
(HMAC runtime-hmac:v1). El archivo esta TRACKEADO en git (anadido en la entrega 5365725), asi que un clon
limpio SI lo trae.

Precondicion pre-existente (NO introducida por 0307): el padre del impl (2fd10a6) ya tenia la cola caliente
arrancando en seq 672 (min=672, contigua, sin huecos). Los seq 1..671 fueron retirados por una operacion
ANTERIOR del ciclo de vida de la instancia, no por esta tarea. La union se ancla en 672 y el gate offline
valida verde desde ahi. Lo declaro como residual (seccion 6), no es defecto de 0307.

## 1. Reproduccion (exit codes reales, clon limpio 1831bdd)

| Paso | Comando | Exit |
|------|---------|------|
| Clon + checkout | `git clone file://... ccv0307 && git checkout 1831bdd` | limpio |
| Compile | `python -m py_compile runtime/eventlog.py .../run_runtime_eventlog_cases.py` | 0 |
| Banco eventlog | `python examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py` | 0 (7 casos) |
| VALIDATE (validate_chain full = frontera dura, lee archivos+cola) | `python scripts/validate_collaboration_state.py` | 0 |
| scan_encoding | `python scripts/scan_encoding.py` | 0 |
| scan_domain_neutrality | `python scripts/scan_domain_neutrality.py` | 0 |
| git diff --check | `git diff --check` | 0 |
| Config byte-identico vs padre impl (AC6) | `git diff --exit-code 98b887a~1 98b887a -- protocol.config.json` | 0 (identico) |
| Config byte-identico vs 2fd10a6 (AC6) | `git diff --exit-code 2fd10a6 -- protocol.config.json` | 0 (identico) |
| Reconstruccion AC2 propia | `python recon.py` | AC2_RECON_VERDICT=PASS |

Nota clave sobre `.protocol-secrets/`: la clave HMAC `runtime` NO esta en git (correcto). En el clon limpio,
sobre el snapshot VIVO, `verify_snapshot_checkpoint` cae a `unresolved_key` -> verificacion COMPLETA
(fail-safe correcto ante ausencia de material; el canonical_hash es secret-independiente por DECISION-0046).
Por eso el camino de CONFIANZA vivo (AC3) NO es ejercitable sobre el snapshot del clon; lo ejercite con un
banco sintetico propio con clave real (seccion 4). El gate offline (validate_chain) SI audita la cadena
completa sin secreto (la cadena prev_hash es secret-independiente), y lo use para el ataque de AC4.

## 2. AC2 -- union == set completo original (EL vector critico de perdida), por MI reconstruccion

Lei YO MISMO el archivo y la cola (sin fiarme de `events_in_log_order`) y recompute la cadena de forma
independiente con los helpers puros de hash:

| Comprobacion | Resultado |
|--------------|-----------|
| Conteo union (archivo 6154 + cola 3) | 6157 eventos |
| Span union | seq 672..6828, expected_count 6157 |
| Contiguidad (huecos) | 0 huecos, strictly +1 |
| Duplicados de seq | ninguno (archivo hi=6825 < cola lo=6826, sin solape) |
| Frontera archivo->cola | archive_last=6825, hot_first=6826, contigua |
| Cadena prev_hash (6156 enlaces recomputados) | 0 rotos |
| Costura 6825->6826 (prev_hash del primer evento caliente sobre el ultimo archivado) | intacta |
| Sidecar SHA-256 del archivo vs bytes reales | coincide (7fb19583...) |
| head.prev_hash == snapshot.integrity.prev_hash | True (checkpoint atado al head real) |
| canonical_hash(replay(union)) | 07f0d6db1824161412c20b2bc1a36f5bbbc79f977ec1be12747b840adc29307e |
| canonical_hash del snapshot firmado | 07f0d6db...307e (IDENTICO) |
| events_applied / rejections | 6157 / 0 |

La cadena es una lista enlazada por hash: cualquier perdida, duplicado o reordenamiento entre 672 y 6828
romperia un enlace. Los 6156 enlaces verifican, la costura archivo->cola verifica, y la union re-materializa
al MISMO canonical_hash que el snapshot firmado. Ademas la union es superset del set del padre (padre 672..6822
todos presentes dentro del archivo 672..6825). **CERO perdida, CERO duplicado.** AC2 PASS.

## 3. AC1/AC6 -- compactacion cableada al checkpoint, MUEVE no borra, alcance

- AC1: `write_snapshot` firma el checkpoint y, si `snapshot.integrity` existe y el hot log supera el umbral,
  invoca `compact_through(up_to_seq)` sobre el limite del checkpoint. Verificado en vivo (existe el archivo)
  y en el banco sintetico (umbral 3 -> compacta al cruzarlo).
- Umbral `compaction_threshold=1024` vive en `runtime/CHECKPOINT_POLICY.json` (FUERA del config pineado).
  `grep compaction_threshold protocol.config.json` -> ausente. AC6 PASS.
- MUEVE no borra: la union sigue completa (6157, seccion 2). `compact_through` reescribe `events.jsonl` con
  el remanente `seq > up_to_seq` y escribe el prefijo al archivo con sidecar. Nada se elimina de la union.
- Config byte-identico vs padre del impl y vs 2fd10a6 (exit 0). Sin genesis/re-genesis. Alcance de codigo:
  `runtime/eventlog.py` + `runtime/CHECKPOINT_POLICY.json` (+1 linea) + banco. protocol.config.json intacto.

## 4. AC3 -- camino vivo O(cola), byte-identico (banco sintetico propio con clave real)

Como el clon no trae la clave, monte un ledger sintetico propio (clave de fixture `tb-secret`, chain_enabled,
event_auth) con 8 eventos -> snapshot firmado -> compactacion (archivo events-000001-000008, cola vaciada) ->
3 eventos mas de cola. Instrumente `verify_event_auth` con un contador:

| Metrica | Camino VIVO (trusted) | Camino FULL |
|---------|-----------------------|-------------|
| eventos autenticados | 3 (solo la cola seq 9..11) | 11 (todos) |
| checkpoint trusted / reason | True / valid (up_to_seq=8, incremental=3) | -- |
| canonical byte-identico live==full | True | (referencia) |

El camino vivo confia el prefijo archivado (via checkpoint firmado + integridad del archivo) y re-verifica
SOLO la cola caliente: O(cola), no O(todos), y byte-identico al full. AC3 PASS.

## 5. AC4/AC5 -- offline lee archivos + fail-safe, y fail-closed graceful

**AC4 offline (ataque sobre el archivo REAL del clon):** mute el evento seq 3672 DENTRO del archivo
(actor -> TAMPERED) y RECOMPUTE el sidecar (atacante que tambien arregla el hash). `validate_collaboration_state.py`
= exit 1 con: `chain invalid: corruption at seq 3672 hash mismatch`, `snapshot mismatch`, `actor_auth invalid`.
El gate offline lee los archivos y full-audita la union; un evento manipulado en el archivo sigue cazado
AUNQUE el sidecar case. El sidecar es solo el atajo rapido del camino vivo; la frontera dura es validate_chain.

**AC4 fail-safe vivo (banco sintetico):** corromper UN byte del archivo SIN arreglar el sidecar ->
`archive_integrity: valid=False (archive_hash_mismatch)` -> `verify_snapshot_checkpoint: trusted=False
(invalid_archive_integrity)` -> `EventWriter.state()` cae a verificacion COMPLETA y NO lanza excepcion.
Nunca confia un archivo malo, nunca saltea.

**AC5 fail-closed graceful (banco sintetico):**

| Malformacion | reason | state() completa sin excepcion |
|--------------|--------|--------------------------------|
| snapshot up_to_seq = "NaN" | invalid_checkpoint_sequence | SI |
| CHECKPOINT_POLICY max_incremental_events = "lots" | invalid_checkpoint_policy | SI |

Degradan a trusted:False -> verificacion completa; el submit completa. AC5 PASS.

## 6. Tabla vector-por-vector

| AC | Vector | Resultado |
|----|--------|-----------|
| AC1 | compact_through cableado sobre el limite del checkpoint + umbral en CHECKPOINT_POLICY.json | PASS |
| AC2 | union (archivo+cola) == set completo, seq contiguos, cadena intacta, mismo canonical_hash, cero perdida/dup | PASS |
| AC3 | camino vivo O(cola): 3 vs 11 autenticaciones, byte-identico al full | PASS |
| AC4 | offline lee archivos + caza mutacion en archivo (aun con sidecar recomputado); fail-safe vivo a full | PASS |
| AC5 | up_to_seq / max_incremental_events no-numerico -> trusted:False graceful, sin excepcion | PASS |
| AC6 | MUEVE no borra; config byte-identico; sin genesis; umbral fuera del config pineado; alcance 3 rutas | PASS |
| Gates | banco(7) + validate + scan_encoding + scan_domain_neutrality + diff --check | todos exit 0 |

SLIPS encontrados: ninguno.

## 7. Residuales declarados (no bloquean el cierre de 0307)

- R1 (pre-existente, informativo): la union arranca en seq 672; los seq 1..671 ya estaban ausentes en el
  padre del impl (2fd10a6). No es efecto de 0307. El gate offline valida verde desde 672. Si se desea que
  el gate exija el genesis fisico en el prefijo archivado, es una decision aparte del ciclo de compactacion,
  no un defecto de esta tarea.
- R2 (limitacion de metodo, no defecto): el camino de CONFIANZA vivo no se puede ejercitar sobre el snapshot
  del clon limpio (clave `runtime` gitignoreada). Lo cubri con un banco sintetico propio con clave real
  (seccion 4). Es el fail-safe por diseno (DECISION-0046), esperado.
- R3 (invariante notado): `compact_through` deriva el nombre `events-<lo>-<hi>` de `archive_events[0]`/`[-1]`,
  asumiendo el hot log en orden ascendente de seq. El append-only lo garantiza; no es una fuga, se documenta.

## 8. Conclusion

Los 6 AC verifican en clon limpio por comportamiento, con reconstruccion INDEPENDIENTE del set completo de
eventos (cero perdida/duplicado, cadena intacta a traves de la frontera, mismo canonical_hash firmado),
camino vivo O(cola) byte-identico, gate offline que caza mutaciones dentro del archivo aun con sidecar
recomputado, fail-safe vivo ante archivo corrupto, y fail-closed graceful ante limites malformados. Config
byte-identico, sin genesis, umbral fuera del config pineado, MUEVE no borra. Cierra la tanda A+B+C.

Recomendacion: **OK-CLOSABLE**.

-- Analista
