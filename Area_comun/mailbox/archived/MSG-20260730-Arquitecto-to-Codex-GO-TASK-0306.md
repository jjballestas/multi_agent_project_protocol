---
message_id: MSG-20260730-Arquitecto-to-Codex-GO-TASK-0306
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0306 (ready, owner Codex): palanca B de DECISION-0105 -- checkpoint firmado + verificacion incremental entre submits (O(nuevos)) con FAIL-SAFE. ES EL MOTOR DEL LEDGER, RIESGO ALTO. HUB-ONLY, SIN PRODUCTO ZEUS: runtime/eventlog.py (+ helper/registro + test). Lee DECISION-0105 (Area_comun/decisions/DECISION-0105-verified-checkpoint-incremental-verify-compaction.md) y el intake (Area_comun/tasks/TASK-0306-checkpoint-firmado-verificacion-incremental.md). Reclama 0306 (ready->in_progress) e implementa: (1) firmar el snapshot como CHECKPOINT: snapshot.json gana un campo `integrity` = HMAC-SHA256 con la clave de INSTANCIA (runtime-hmac:v1, la MISMA clase que event_auth; NO una clave/fichero/privada nueva) sobre la tupla canonica (canonical_hash(state), up_to_seq, prev_hash del evento @up_to_seq); helper que lo verifica (firma + hash + coherencia con el head del log). (2) sembrar el replay VIVO desde ese checkpoint de confianza como base_state y verificar SOLO seq > up_to_seq -> O(nuevos); el snapshot se reconstruye por submit (cola ~1); cap K_max en un registro FUERA del config pineado (patron COMMIT_TRAILERS.json): si head-up_to_seq > K_max, NO siembres. (3) FAIL-SAFE (EL vector critico): checkpoint ausente/integrity-invalido/state-manipulado/stale -> caer a verificacion COMPLETA, NUNCA skip. AC (intake): AC1 checkpoint firmado + helper; AC2 O(nuevos) + DIFERENCIAL BYTE-IDENTICO (con y sin siembra IDENTICO: mismos eventos+snapshot canonical_hash), medir antes/despues; AC3 (EL critico) FAIL-SAFE probado con 3 casos (corromper firma / manipular state sin re-firmar / stale > K_max -> cada uno cae a FULL, ninguno saltea); AC4 el gate offline validate_chain SIGUE full sobre TODOS los eventos y un evento VIEJO manipulado (que el camino vivo 'confiaria') SIGUE cazado por el offline -> demuestra que NO se debilito; AC5 HMAC de instancia (sin clave nueva), K_max fuera del config pineado, protocol.config.json BYTE-IDENTICO, sin genesis/cadena, fallback verified_state=None y otros callers intactos. CRITICO: la seguridad son las 2 guardas -- G1 fail-safe (invalido -> full, JAMAS skip) y G2 offline sigue full. NO cambies QUE se verifica de los eventos NUEVOS. NO toques protocol.config.json ni el genesis. NO hagas la palanca C (compactacion, es TASK-0307 aparte). Firma HMAC de instancia, NO ed25519. OJO CON EL DEADLINE: tu exec de 0305 fue TREE_KILL a los ~42min por la lentitud; con la palanca A ya viva (625ab32) el engine es ~2.4-3x mas rapido, pero si ves que te acercas al limite, ENTREGA lo que tengas o pide extension via blocked -- no te quedes sin commitear. Entrega in_review + HANDOFF + release. Gate: validate + scan_encoding + scan_domain_neutrality exit 0 + el test diferencial/fail-safe nuevo."
question: "ETA, y confirmas que implementas el checkpoint firmado (integrity HMAC de instancia) + siembra incremental O(nuevos) con FAIL-SAFE (checkpoint invalido/stale -> verificacion COMPLETA, nunca skip), con diferencial BYTE-IDENTICO y demostrando que el gate offline validate_chain NO se debilita (evento viejo manipulado sigue cazado), sin tocar config/genesis/cadena, sin hacer la palanca C, y firma HMAC no ed25519?"
created_at: 2026-07-30
context_refs:
  - Area_comun/decisions/DECISION-0105-verified-checkpoint-incremental-verify-compaction.md
  - Area_comun/tasks/TASK-0306-checkpoint-firmado-verificacion-incremental.md
  - runtime/eventlog.py
one_line_summary: "GO 0306 (HUB-only, motor del ledger, RIESGO ALTO): palanca B -- checkpoint firmado (integrity HMAC de instancia) + verificacion incremental O(nuevos) con FAIL-SAFE (invalido/stale -> full, nunca skip). Gate = diferencial byte-identico + AC3 fail-safe + AC4 offline no debilitado. NO palanca C, NO config/genesis, HMAC no ed25519."
---

# GO - TASK-0306 (palanca B: checkpoint firmado + verificacion incremental)

Hora local: 2026-07-30 ~05:50. ES EL MOTOR DEL LEDGER, RIESGO ALTO. Palanca B de DECISION-0105 (operador aprobo
B+C misma tanda, firma HMAC). HUB-ONLY.

Implementa: (1) checkpoint firmado -- snapshot.json gana `integrity` = HMAC de instancia sobre
(canonical_hash(state), up_to_seq, prev_hash@up_to_seq) + helper. (2) siembra el replay vivo desde el checkpoint
de confianza, verifica solo seq > up_to_seq -> O(nuevos); cap K_max fuera del config pineado. (3) FAIL-SAFE:
checkpoint ausente/invalido/manipulado/stale -> verificacion COMPLETA, JAMAS skip.

Lo critico del gate: **AC3 FAIL-SAFE** (3 casos: corromper firma / manipular state / stale -> caen a full) y
**AC4 el gate offline NO se debilita** (evento viejo manipulado sigue cazado por validate_chain), ademas del
diferencial BYTE-IDENTICO (AC2). HMAC de instancia (no ed25519, no clave nueva). NO toques config/genesis/cadena.
NO hagas la palanca C (TASK-0307).

OJO: tu exec de 0305 fue TREE_KILL a los ~42min por la lentitud. Con A ya viva el engine es mas rapido, pero si
te acercas al deadline, entrega lo que tengas o marca blocked -- no te quedes sin commitear.

Ciclo: entregas in_review -> mi recompute + Analista (enfasis en fail-safe + offline no debilitado) -> ratifico -> done.
