---
task_id: TASK-0306
file: Area_comun/tasks/TASK-0306-checkpoint-firmado-verificacion-incremental.md
title: "Palanca B (DECISION-0105): checkpoint firmado + verificacion incremental entre submits (O(nuevos)) con fail-safe"
status: review_approved
type: infra
owner: Codex
reviewer: Analista
priority: normal
depends_on:
  - TASK-0305
relates_to:
  - DECISION-0105
created_at: 2026-07-30
intake:
  type: infra
  goal: >
    Implementar la palanca B de DECISION-0105: firmar el snapshot como CHECKPOINT VERIFICADO y sembrar el replay
    vivo desde ese checkpoint de confianza, verificando SOLO los eventos con seq > up_to_seq. Hoy cada submit
    re-verifica las firmas del log ENTERO (O(n)); esto lo hace O(nuevos). El snapshot.json gana un campo `integrity`:
    HMAC-SHA256 con la clave de INSTANCIA (runtime-hmac:v1, la misma clase que event_auth; SIN clave/fichero/privada
    nueva) sobre la tupla canonica (canonical_hash(state), up_to_seq, prev_hash del evento @up_to_seq). El replay
    vivo confia en el checkpoint como base SOLO si su integrity verifica + hash casa + coherencia con el head del log;
    si NO (ausente/invalido/manipulado/stale con head-up_to_seq > K_max) cae a verificacion COMPLETA (fail-safe,
    nunca skip). K_max vive en un registro FUERA del config pineado (patron COMMIT_TRAILERS.json). El resultado es
    byte-identico a la verificacion completa; el gate offline (validate_chain) sigue full sobre todos los eventos.
  acceptance:
    - "AC1 (checkpoint firmado): snapshot.json gana un campo `integrity` = HMAC-SHA256 con la clave de instancia sobre (canonical_hash(state), up_to_seq, prev_hash@up_to_seq); un helper lo verifica (firma + hash + coherencia con el evento @up_to_seq del log). La firma usa la HMAC de instancia existente -- SIN clave/fichero/privada nueva."
    - "AC2 (O(nuevos) + byte-identico): el replay vivo siembra base_state desde el checkpoint de confianza y verifica SOLO seq > up_to_seq; un test diferencial prueba que el estado/eventos/snapshot resultantes son BYTE-IDENTICOS a la verificacion completa. Medir: el coste de verificacion de un submit sobre el log grande cae a O(nuevos) (ya no re-verifica todos los eventos). Reportar antes/despues."
    - "AC3 (FAIL-SAFE, EL vector critico): checkpoint ausente / integrity invalido / state manipulado / stale (head-up_to_seq > K_max) -> cae a verificacion COMPLETA, NUNCA skip. Tests: (a) corromper la firma integrity -> no se confia -> full verify; (b) manipular el state del snapshot sin re-firmar -> hash no casa -> full verify; (c) un checkpoint stale (> K_max) -> full verify. En ninguno se salta la verificacion de eventos."
    - "AC4 (gate offline SIN debilitar): validate_collaboration_state.py / validate_chain siguen verificando TODOS los eventos (firmas + cadena); un evento VIEJO manipulado (que el checkpoint del camino vivo 'confiaria') SIGUE siendo cazado por el gate offline. Demostrar que el offline no se debilito."
    - "AC5 (seguridad/alcance): integrity con la HMAC de instancia (sin clave nueva); K_max en registro fuera del config pineado; protocol.config.json BYTE-IDENTICO; sin genesis/re-genesis; sin cambio en la cadena #4 ni en QUE se verifica de los eventos nuevos. Alcance: runtime/eventlog.py (+ helper/registro + test). Fallback verified_state=None y otros callers intactos."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
  scope_routes:
    - runtime/eventlog.py
  out_of_scope: >
    Palanca C (compactacion fisica del log / compact_through) -- es TASK-0307, tras esta. Cualquier cambio en
    protocol.config.json o el genesis. Cambiar QUE se verifica de los eventos nuevos. La firma ed25519 (se decidio
    HMAC de instancia). Producto Zeus.
  risk: high
  estimate: M
notes: >
  Palanca B de DECISION-0105 (operador aprobo B+C en la misma tanda, firma HMAC). RIESGO ALTO: cambia el modelo de
  confianza del camino VIVO (de 'verifico todo' a 'confio en un checkpoint firmado y verifico la cola'). La seguridad
  esta en las 2 guardas: G1 fail-safe (checkpoint invalido -> full, nunca skip) y G2 el gate offline sigue full. El
  gate de la tarea debe atacar sobre todo AC3 (fail-safe) y AC4 (offline no debilitado), ademas del diferencial
  byte-identico. Tras esta, TASK-0307 (palanca C) cablea compact_through sobre el mismo limite de checkpoint.
---

# TASK-0306 - Palanca B: checkpoint firmado + verificacion incremental (DECISION-0105)

## Contexto
DECISION-0105 introduce el checkpoint verificado firmado. TASK-0305 (palanca A) ya quito el multiplicador
intra-submit; esta hace O(nuevos) el caso general sembrando desde el checkpoint. El snapshot ya tiene
up_to_seq + canonical_hash; falta la firma integrity + la siembra condicional con fail-safe.

## Que hacer
1. Firmar el snapshot: campo `integrity` = HMAC de instancia sobre (canonical_hash(state), up_to_seq,
   prev_hash@up_to_seq). Helper de verificacion.
2. Sembrar el replay vivo desde el checkpoint de confianza; verificar solo seq > up_to_seq; cap K_max (registro
   fuera del config pineado).
3. Fail-safe: checkpoint ausente/invalido/manipulado/stale -> verificacion COMPLETA.

## Como probarlo (lo critico)
- Diferencial byte-identico (con y sin siembra IDENTICO).
- FAIL-SAFE (AC3): corromper firma / manipular state / stale -> cae a full, nunca skip.
- Gate offline (AC4): evento viejo manipulado SIGUE cazado por validate_chain.

## No hacer
Palanca C (compactacion) es TASK-0307. Sin tocar config/genesis/cadena. HMAC de instancia (no ed25519, no clave
nueva). Fondo intocable.
