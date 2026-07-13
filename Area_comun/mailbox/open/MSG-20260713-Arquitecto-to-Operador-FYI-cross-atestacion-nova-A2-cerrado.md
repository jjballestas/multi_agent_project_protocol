---
message_id: MSG-20260713-Arquitecto-to-Operador-FYI-cross-atestacion-nova-A2-cerrado
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: false
created_at: 2026-07-13
context_refs:
  - Area_comun/artifacts/CROSS-ATESTACION-hub-nova-registro.md
  - Area_comun/artifacts/CROSS-ATESTACION-hub-aegis-registro.md
one_line_summary: "1a CROSS-ATESTACION NOVA<->hub ANCLADA (Entrada 0, hub commit f23ec3e). A2-nominal NOVA CERRADO. NOVA = instancia 2.A independiente (genesis fresco, 5 firmantes). El hub NO se toco. Hora: 2026-07-13 ~15:40 local (UTC+2)."
---

# FYI - Cross-atestacion NOVA<->hub anclada; A2-nominal NOVA CERRADO (2026-07-13 ~15:40 local, UTC+2)

## Que se hizo
- Ancle en el HUB la **1a cross-atestacion de la instancia NOVA**: nuevo registro
  `Area_comun/artifacts/CROSS-ATESTACION-hub-nova-registro.md` (Entrada 0), commit hub **f23ec3e** (=origin).
  Con esto el **A2-nominal NOVA queda CERRADO**.
- Mecanismo = el mismo del registro Aegis (DECISION-0088 p.5 / 0093 / 0050 p.5), pero NOVA tiene su **PROPIO
  registro** por ser instancia independiente 2.A. Es un commit de artefacto con trailers (Task-Id: none),
  NO un submit_intent (el artefacto no es state file; precedente Entrada 3 Aegis = commit e22e9f3).

## Ancla (verificable re-computando contra NOVA.git/main@5ca2e5c)
- nova_repo: github.com/jjballestas/NOVA.git (main); nova_commit: **5ca2e5c**
- head_seq: **4**; head_prev_hash: 4728a8f1...; sha256 events.jsonl: **4f69a3dc...**; sha256_head_line: d2c1a06b...
- event_count: **4 (seq 1..4)** = **genesis FRESCO e independiente** (NO continuacion del hub; a diferencia de
  Aegis que forkeaba la cadena del hub). config-epoch sha8 NOVA: **5679362F**.
- 5 firmantes ed25519: arquitecto/codex/analista:v1 (trio) + jheredia:v1 (Julian) + jball:v1 (John).
- Re-verificado por mi sobre clon NOVA.git/main@5ca2e5c: **validate 0, scan_encoding 0, neutralidad 0**,
  local HEAD == origin/main.

## Frontera dos-trios respetada
- Yo (hub-Arquitecto) SOLO LEI NOVA (git fetch read-only) para anclar aqui; NO escribi el ledger de NOVA
  (lo escribe su propio trio). No pushee nada a NOVA.

## Fondo intocable (HUB) -- confirmado NO tocado
- config **2E35F26E / epoch 1.14.0** PINNED, dataset TFM **N=500** SELLADO, sello pre-registro **N=6**
  (DECISION-0094, sha256 28fd963b) -- todo INTACTO.

## Estado
- **STANDBY / cola del operador.** Nada pendiente corto.
- Pendientes que esperan tu GO: (1) sellar la topologia dos-trios/2.A como DECISION consolidada (enmienda
  DECISION-0050); (2) Zeus-protocol vs Zeus-Aegis (panel); (3) build-open post-30-jul (promover TASK-9310 +
  6 unidades medidas de Contabilidad).

-- Arquitecto
