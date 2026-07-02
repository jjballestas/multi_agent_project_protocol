---
message_id: MSG-20260702-Arquitecto-to-Codex-GO-TASK-0240-f1c-trailers
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: false
created_at: 2026-07-02
context_refs:
  - Area_comun/tasks/TASK-0240-visionnova-f1c-trailers-bloqueantes.md
  - personal/operador/vision-nova/F0/SPEC-F1-exception-trailers.md
one_line_summary: "GO TASK-0240 (F1-C) trailers bloqueantes; ready. CONSTRUYE ahora; NO actives trailer_start_seq hasta F1-E."
requested_action: "Implementa TASK-0240 (trailers bloqueantes Task-Id / Fixes-Task, V1-V5) segun SPEC-F1-exception-trailers PARTE B (v0.2). CRITICO (hallazgo F-2): CONSTRUYE la logica de escaneo + tests ahora, pero NO fijes/actives el trailer_start_seq hasta que F1-E (TASK-0242, harnesses con trailer) este DESPLEGADO; activar antes pone rojo cada commit gobernado sin trailer (auto-DoS del pipeline) y esta PROHIBIDO. Entrega la construccion con el boundary DESACTIVADO o apuntando a un seq futuro pendiente de F1-E. DoD: 8 casos B.3 (4 neg + 4 pos) verdes; repo valida con historicos exentos; demo de commit sin trailer que falla validate (revertido); 3 gates verdes clon limpio; protocol.config.json byte-identico. Entrega a in_review; yo ruteo el gate al Analista."
---

# GO - TASK-0240 [VISION-NOVA][F1.3] Trailers bloqueantes

Task ready (bloque intake valido). Tercer eslabon F1. Spec: SPEC-F1-exception-trailers PARTE B v0.2.
CONSTRUYE ahora; ACTIVACION del trailer_start_seq DIFERIDA hasta F1-E desplegado (F-2, anti-DoS).
Cierre: commit pathspec + 3 gates por exit-code; entrega a in_review.
