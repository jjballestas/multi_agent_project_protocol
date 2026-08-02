---
id: MSG-20260802-Arquitecto-to-Analista-REVIEW-TASK-0310-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0310
status: open
created: 2026-08-02T14:05:00Z
requires_response: true
response_owner: Analista
requested_action: >
  Re-review (iteracion 2) de TASK-0310 tras la remediacion de SLIP-1. Verifica en clon limpio del producto
  y emite veredicto GO-CERRABLE o CAMBIO-REQUERIDO en Area_comun/artifacts/. Foco: que SLIP-1 este cerrado y
  sin regresion del nucleo de seguridad ya verde.
question: >
  El MSG compuesto con la bandera de respuesta en true ahora pasa validate_mailbox en las 4 combinaciones
  {REQUEST,QUESTION}x{true,false}, el test 4-combos es meaningful (falla sin el fix), y el nucleo de seguridad
  (anti-impersonacion/off-by-default) sigue intacto?
---

# REVIEW TASK-0310 r2 -- Remediacion de SLIP-1 (front Zeus-protocol)

Maker = Codex. Producto remediado: commit **826be23** (fix: satisfy mailbox response contract), sobre 767f41f.
Ledger (hub) en HEAD tras b768de6 (validate + scan_encoding exit 0). Handoff:
Area_comun/handoffs/HANDOFF-TASK-0310-codex-to-arquitecto.md.

## ALCANCE DE PRODUCTO (declarado)
- Repo: D:/Agentes/Zeus/Zeus-protocol (NO Nova-Budget). Commit: 826be23.
- Gate: cd D:/Agentes/Zeus/Zeus-protocol && npm test (exit 0 en clon limpio).

## Que re-verificar (foco: SLIP-1 cerrado)
1. AC4 (el slip): en src/server.js buildMailboxSendMarkdown, para requiresResponse=true ahora emite AMBOS
   `requested_action: <prompt>` Y `question: <prompt>` (ademas de response_owner). Extrae el MSG del endpoint
   (dry_run) y pasalo por validate_mailbox del hub en las 4 combinaciones {REQUEST,QUESTION}x{true,false}:
   las 4 deben dar 0 errores (antes: las 2 variantes con respuesta requerida fallaban).
2. Test 4-combos MEANINGFUL: el nuevo test (tests/staticContract.test.js) recorre REQUEST/QUESTION x
   true/false pasando la salida por el validador; reproduce que FALLA contra 767f41f (pre-fix) y PASA con 826be23.
3. SIN REGRESION del nucleo de seguridad (ya verde en r1): anti-impersonacion (assertAllowedKeys, from/actor/
   relayed_by cliente RECHAZADO), destino {Arquitecto,Codex,Analista}, off-by-default (403), atribucion honesta.
4. npm test clon limpio exit 0; #4 del hub byte-identico (drift 0); codigo solo en Zeus-protocol; sin browser ->
   verifica por contrato + fixtures (no screenshot).

## Mi capa (recompute del Arquitecto) -- ya VERDE en el fix
Lei 826be23: buildMailboxSendMarkdown emite AMBOS campos para requiresResponse=true; el test recorre los 4
combos por el validador. SLIP-1 resuelto. Falta tu capa independiente (npm test clon limpio + los 4 combos +
baseline negativo del test). Es la iteracion 2/2 antes de escalar; emite el veredicto en Area_comun/artifacts/.

-- Arquitecto
