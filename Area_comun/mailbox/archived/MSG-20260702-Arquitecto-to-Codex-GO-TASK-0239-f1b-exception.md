---
message_id: MSG-20260702-Arquitecto-to-Codex-GO-TASK-0239-f1b-exception
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: false
created_at: 2026-07-02
context_refs:
  - Area_comun/tasks/TASK-0239-visionnova-f1b-exception-recorded.md
  - personal/operador/vision-nova/F0/SPEC-F1-exception-trailers.md
one_line_summary: "GO TASK-0239 (F1-B) evento firmado exception.recorded; ready. Implementa SPEC PARTE A."
requested_action: "Implementa TASK-0239 (evento firmado exception.recorded) segun SPEC-F1-exception-trailers.md PARTE A. Alcance: intent exception en submit_intent + schema A.1 (enums cerrados, ASCII, sin PII) + doctrina U1-U3 en TASK_PROTOCOL.md (y template). Firmado ed25519, entra a la cadena atestada. NOTA: budget_overrun queda SOLO como kind/evento (el auto-pause es Carril B, fuera de F1). Este evento HABILITA el R5 fail-closed de 0238: intake_exempt podra validar cuando exista un exception.recorded kind=intake_exempt. DoD: 4 tests negativos (kind fuera de enum / summary no-ASCII / exception_id duplicado / task_id inexistente); round-trip de 2 eventos reales (assist + arbitration) con replay drift 0 y listables por task_id; U2 documentada; 3 gates + scan_encoding verdes en clon limpio; protocol.config.json byte-identico. Entrega a in_review con commit; yo ruteo el gate al Analista. F1-C (0240) va despues."
---

# GO - TASK-0239 [VISION-NOVA][F1.2] Evento firmado exception.recorded

Task ready (proposed->ready registrado; bloque intake valido). Segundo eslabon de la cadena F1.

Spec: personal/operador/vision-nova/F0/SPEC-F1-exception-trailers.md PARTE A (v0.2).
Cierre: commit pathspec + 3 gates por exit-code ANTES de pedir review; entrega a in_review.
F1-C (0240 trailers) NO se activa hasta que F1-E (0242) despliegue los harnesses con trailer.
