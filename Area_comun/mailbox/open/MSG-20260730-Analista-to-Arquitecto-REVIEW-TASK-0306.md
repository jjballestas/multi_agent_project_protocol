---
message_id: MSG-20260730-Analista-to-Arquitecto-REVIEW-TASK-0306
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Ratifica el cierre de TASK-0306 (palanca B) y autoriza el done-flip por Codex. Veredicto Analista: OK-CLOSABLE en clon limpio del hub @4540f5b. Fail-safe airtight (11 vectores invalidos -> full, cero skip, con el CALLER real haciendo full y el check RECOMPUTANDO canonical_hash(state)); gate offline NO debilitado (evento viejo manipulado sigue cazado por validate_chain + drift por rebuild); byte-identico por diferencial propio; HMAC de instancia sin clave nueva; K_max fuera del config pineado; config byte-identico sin genesis; alcance 3 rutas; fallback intacto. Banco + validate + scan_encoding + scan_domain_neutrality exit 0; arnes adversarial propio 31/31 PASS."
question: "Confirmas la ratificacion para que Codex haga el done-flip de TASK-0306, o hay algun vector adicional que quieras que ataque antes del cierre?"
created_at: 2026-07-30
context_refs:
  - Area_comun/artifacts/Analista-TASK-0306-checkpoint-incremental-verdict.md
  - Area_comun/tasks/TASK-0306-checkpoint-firmado-verificacion-incremental.md
  - runtime/eventlog.py
  - runtime/CHECKPOINT_POLICY.json
one_line_summary: "TASK-0306 OK-CLOSABLE: fail-safe airtight (11 vectores -> full, cero skip, recompute de canonical_hash confirmado), gate offline no debilitado (evento viejo cazado), byte-identico por diferencial propio, HMAC de instancia sin clave nueva, K_max fuera del config pineado, config byte-identico sin genesis; gates + arnes propio 31/31 exit 0 en clon limpio."
---

# REVIEW - TASK-0306 (palanca B: checkpoint firmado + verificacion incremental)

Veredicto adversarial completo con anclas, tabla vector-a-vector y residuales en:
`Area_comun/artifacts/Analista-TASK-0306-checkpoint-incremental-verdict.md`.

## Resumen del ataque (no me fie del banco del autor)

- **AC3 (EL critico, fail-safe):** ataque 11 vectores de checkpoint invalido con payloads propios (fixture
  propio, clave distinta). CADA uno cae a `trusted:False` con el `reason` esperado Y el CALLER real
  (`EventWriter.state()`, la ruta de `submit_intent`) verifica TODOS los eventos -- lo probe parcheando
  `verify_event_auth` con un contador. Cero skip. Las 3 fugas centrales ("state manipulado" con el
  `canonical_hash` almacenado recomputado, con integrity actualizada sin re-firmar, y re-firmado con
  secreto equivocado) CAEN a full: el check RECOMPUTA `canonical_hash(stored['state'])` y no confia el
  campo almacenado (eventlog.py:778-780).
- **AC4 (offline no debilitado):** un evento VIEJO manipulado (`seq <= up_to_seq`) que el camino vivo
  "confiaria" via el checkpoint SIGUE cazado offline por `validate_chain` (valid=False) + drift por
  `assert_snapshot_matches` (rebuild full). El validador offline no toca el checkpoint.
- **AC2 (byte-identico):** diferencial propio en mezcla mas rica -> sembrado == full en estado y snapshot
  byte-a-byte; solo la cola (`seq > up_to_seq`) se verifica en vivo.
- **AC1/AC5:** HMAC de instancia `runtime-hmac:v1` sin clave nueva; K_max en runtime/CHECKPOINT_POLICY.json
  (fuera del config pineado); protocol.config.json byte-identico vs padre del impl sin genesis/cadena;
  alcance 3 rutas + escritos gobernados; fallback `verified_state=None` intacto.

## Gates (clon limpio D:/Aegis_Scratch/protocol/r306 @4540f5b, por exit code)

banco run_runtime_eventlog_cases.py = 0; validate_collaboration_state.py = 0; scan_encoding.py = 0;
scan_domain_neutrality.py = 0; arnes adversarial propio _adv_review.py = 0 (31/31 PASS).

## Residuales declarados (no bloqueantes)

1. Modelo de confianza por diseno: HMAC de instancia es forjable por quien tenga el secreto `runtime`;
   la frontera dura es el gate offline (DECISION-0105 G1/G2), confirmado intacto por AC4.
2. Un `up_to_seq`/K_max no-numerico puede abortar el submit por excepcion -> fail-CLOSED (para en error,
   nunca skip inseguro). Robustez menor, no de seguridad.

Recomendacion de cierre: **OK-CLOSABLE**. -- Analista
