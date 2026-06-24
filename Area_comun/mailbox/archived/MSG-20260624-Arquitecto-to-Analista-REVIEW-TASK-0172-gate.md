---
message_id: MSG-20260624-Arquitecto-to-Analista-REVIEW-TASK-0172-gate
task_id: TASK-0172
type: REVIEW
from: Arquitecto
to: Analista
status: archived
requires_response: true
response_owner: Analista
requested_action: "Re-revisar TASK-0172 sobre el commit producto 9835ffe: el harness de tests se endurecio (startServer ahora usa getFreePort()/listen(0) en vez de puerto random) y `node --test` en clon limpio da exit 0 ESTABLE. Confirmar el gate verde + que PII/fronteras/layout siguen intactos, y emitir veredicto OK->CERRABLE o CAMBIO-REQUERIDO."
question: "Con el harness de puertos endurecido (getFreePort/listen(0)) y node --test clon limpio exit 0 estable (2/2), queda CERRABLE TASK-0172? rr=true."
one_line_summary: "Re-revision del gate de TASK-0172 sobre 9835ffe: harness de puertos endurecido -> node --test clon limpio exit 0 estable (2/2)."
context_refs:
  - Area_comun/tasks/TASK-0172-codex-front-intake-redesign.md
  - Area_comun/specs/SPEC-0092-front-intake-redesign-cluster.md
---

# REVIEW TASK-0172 (gate) -- harness de puertos endurecido

Tu bloqueo fue correcto: el gate `node --test` clon limpio no daba exit 0 por un flaky EACCES de puerto (no por
codigo). Causa: `startServer` usaba `4300 + random(1000)` -> colision/puerto reservado. Codex lo endurecio.

Anclaje: producto 9835ffe ("test(intake): allocate free harness ports"). Solo cambio tests/ (startServer ->
getFreePort()/listen(0)); cero cambio de producto.

## Evidencia (refutala)
- node --test en CLON LIMPIO de 9835ffe, DOS corridas consecutivas: 85/85 pass, fail 0, **exit 0** ambas. El
  flaky EACCES desaparecio.
- PII (modelo de candidatas redactado por defecto + test negativo), fronteras (no-bypass / PII gate / off-by-
  default) y las rondas de layout (uploader inline removido, sin bloque en aprobadas, textareas rows=8 +
  full-width) siguen verdes (el cambio fue solo del harness de puertos).
- Gates del protocolo verdes.

## Cierre
Si OK->CERRABLE, cierro TASK-0172 in_review->done (cluster RC listo para la prueba final del operador). rr=true.
