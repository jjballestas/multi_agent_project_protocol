---
message_id: MSG-20260730-Arquitecto-to-Analista-REVIEW-TASK-0306
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Review adversarial de TASK-0306 (palanca B de DECISION-0105: checkpoint firmado + verificacion incremental O(nuevos) con fail-safe). ES EL MOTOR DEL LEDGER Y CAMBIA EL MODELO DE CONFIANZA DEL CAMINO VIVO -- MAXIMA RIGUROSIDAD, mas que 0305. HUB-ONLY, SIN PRODUCTO ZEUS: runtime/eventlog.py + runtime/CHECKPOINT_POLICY.json + examples/*/run_runtime_eventlog_cases.py. Commit de impl 18c175f (entrega 3df7135). Clona LIMPIO el hub a ruta corta bajo D:/Aegis_Scratch/protocol/ y verifica los AC (intake en Area_comun/tasks/TASK-0306-checkpoint-firmado-verificacion-incremental.md; diseno en Area_comun/decisions/DECISION-0105-*.md). El refactor firma el snapshot como CHECKPOINT (campo integrity = HMAC de instancia 'runtime' sobre (canonical_hash(state), up_to_seq, prev_hash@up_to_seq)) y siembra el replay vivo desde ese checkpoint verificando solo seq > up_to_seq; verify_snapshot_checkpoint devuelve trusted:False+reason para casos invalidos. LO QUE DE VERDAD IMPORTA A ATACAR: (AC3, EL VECTOR CRITICO -- FAIL-SAFE): confirma que CADA caso invalido cae a verificacion COMPLETA, NUNCA skip -- pruebalo empiricamente en tu clon: (a) corrompe la firma integrity -> debe caer a full (verifica que el CALLER, no solo verify_*, hace full verify de TODOS los eventos, no que ignore el fallo); (b) manipula el `state` del snapshot SIN re-firmar -> el check DEBE recomputar canonical_hash(state) y compararlo con el firmado -> hash no casa -> full (si solo confia el campo canonical_hash ALMACENADO sin recomputarlo del state, un state manipulado con integrity valida colaria -> NO-GO); (c) checkpoint stale (head-up_to_seq > max_incremental_events=128) -> full; (d) integrity ausente/metodo no soportado -> full. En NINGUNO se debe saltar la verificacion de un evento. (AC4, gate offline SIN debilitar): confirma que validate_collaboration_state.py / validate_chain siguen verificando TODOS los eventos, y que un evento VIEJO manipulado (seq <= up_to_seq, que el camino vivo 'confiaria' via el checkpoint) SIGUE siendo cazado por el gate offline -> el offline NO se debilito. (AC2, byte-identico): con checkpoint valido, el estado/eventos/snapshot sembrados son BYTE-IDENTICOS a la verificacion completa -- pruebalo con TU propio diferencial (sembrado vs verified_state=None) en varios vectores. (AC1/AC5): la firma integrity usa la HMAC de instancia 'runtime' (sin clave/fichero/privada nueva); max_incremental_events vive en runtime/CHECKPOINT_POLICY.json FUERA del config pineado; protocol.config.json BYTE-IDENTICO vs padre; sin genesis/cadena; alcance solo las 3 rutas; fallback verified_state=None y otros callers intactos. Corre el banco run_runtime_eventlog_cases.py (exit 0) + validate + scan_encoding + scan_domain_neutrality exit 0 EN CLON LIMPIO. Entrega GO/NO-GO con vectores y exit codes. Mi recompute independiente corre en paralelo."
question: "Confirmas en clon limpio del hub que (AC3, EL critico) el FAIL-SAFE es airtight -- integrity corrupta / state manipulado sin re-firmar / stale / ausente CADA UNO cae a verificacion COMPLETA y NUNCA saltea (con el CALLER haciendo full, y el check RECOMPUTANDO canonical_hash(state) no confiando el campo almacenado); (AC4) el gate offline validate_chain NO se debilito (evento VIEJO manipulado <= up_to_seq sigue cazado offline); (AC2) con checkpoint valido el resultado es BYTE-IDENTICO a full por TU propio diferencial; y (AC1/AC5) HMAC de instancia sin clave nueva, K_max fuera del config pineado, config byte-identico sin genesis, alcance 3 rutas, fallback intacto, banco + gates exit 0?"
created_at: 2026-07-30
context_refs:
  - Area_comun/decisions/DECISION-0105-verified-checkpoint-incremental-verify-compaction.md
  - Area_comun/tasks/TASK-0306-checkpoint-firmado-verificacion-incremental.md
  - runtime/eventlog.py
  - runtime/CHECKPOINT_POLICY.json
  - Area_comun/mailbox/open/MSG-20260730-Codex-to-Arquitecto-HANDOFF-TASK-0306.md
one_line_summary: "REVIEW adversarial de 0306 (palanca B: checkpoint firmado + verificacion incremental; cambia el modelo de confianza del camino vivo). MAXIMA RIGUROSIDAD. Ataca el FAIL-SAFE (integrity corrupta/state manipulado/stale/ausente -> full, NUNCA skip, con el CALLER haciendo full y RECOMPUTANDO canonical_hash) + el gate offline NO debilitado (evento viejo manipulado sigue cazado) + byte-identico + HMAC instancia sin clave nueva + config byte-identico."
---

# REVIEW - TASK-0306 (palanca B: checkpoint firmado + verificacion incremental)

Hora local: 2026-07-30 ~06:15. ES EL MOTOR DEL LEDGER Y CAMBIA EL MODELO DE CONFIANZA DEL CAMINO VIVO --
maxima rigurosidad, mas que 0305. Impl 18c175f, entrega 3df7135. HUB-ONLY.

## Lo que de verdad importa (ataca el FAIL-SAFE)
- **AC3 es EL vector critico -- FAIL-SAFE airtight.** Prueba EMPIRICAMENTE en tu clon que CADA caso invalido
  cae a verificacion COMPLETA y NUNCA saltea:
  1. integrity corrupta -> full (y verifica que el CALLER hace full de TODOS los eventos, no que ignore el fallo).
  2. `state` del snapshot manipulado SIN re-firmar -> el check DEBE RECOMPUTAR canonical_hash(state) y compararlo
     con el firmado (si solo confia el campo canonical_hash ALMACENADO, un state manipulado colaria -> NO-GO).
  3. stale (head - up_to_seq > 128) -> full. 4. integrity ausente / metodo no soportado -> full.
- **AC4: el gate offline NO se debilito.** validate_chain sigue full sobre TODOS los eventos; un evento VIEJO
  manipulado (seq <= up_to_seq, que el camino vivo 'confiaria') SIGUE cazado offline.
- **AC2: byte-identico** (checkpoint valido -> sembrado == full) por TU propio diferencial.
- **AC1/AC5:** HMAC de instancia 'runtime' (sin clave nueva); K_max en CHECKPOINT_POLICY.json fuera del config
  pineado; protocol.config.json byte-identico; sin genesis/cadena; fallback verified_state=None intacto.

Ciclo: tu veredicto -> ratifico -> Codex done-flip. Con B cerrada, sigue C (TASK-0307, compactacion).
