---
message_id: MSG-20260625-Arquitecto-to-Codex-GO-TASK-0182
task_id: TASK-0182
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
requested_action: "GO a TASK-0182 (deuda tecnica, ready). Reclamala -> in_progress y entrega a in_review cuando este verde. Objetivo: el gate full `node --test` de Zeus completa exit 0 en < 300s wall-clock reproducible en clon limpio, atacando la causa (tests de subproceso lentos), SIN bajar cobertura ni subir mas timeouts. Ver DoD AC1-AC4 en la tarea. maker=Codex / checker=Arquitecto. rr=false."
one_line_summary: "GO TASK-0182: robustecer la duracion del full-suite de Zeus (<300s, atacar causa, no subir timeouts)."
context_refs:
  - Area_comun/tasks/TASK-0182-codex-zeus-fullsuite-duration-hardening.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
---

# GO -- TASK-0182 (deuda tecnica del full-suite)

El operador autorizo arrancar **TASK-0182**. Reclamala y trabajala en el repo producto Zeus-protocol.

Objetivo (DoD en la tarea, AC1-AC4):
- **AC1:** `node --test` (gate por defecto, clon limpio) completa **exit 0 en < 300s** wall-clock, reproducible
  (>=3 corridas) y bajo carga moderada. Documenta la duracion observada.
- **AC2:** ataca la CAUSA -- los tests de subproceso que dominan el wall-clock (auto-commit-push, local-vlm
  extractor, candidate-review). Opciones validas: paralelizar (`--test-concurrency`), aislar un tier lento en script
  aparte (p.ej. `npm run test:slow`) ejecutable y documentado fuera del gate por defecto, mockear/acelerar el
  subproceso con fixtures deterministas, o acotar a un caso representativo. **NO subir mas los timeouts.**
- **AC3:** sin perdida de cobertura ni de comportamiento (mantener AC3-bis/AC3-ter PII, no-bypass, no-egress,
  off-by-default). `git diff` no toca produccion (server.js/app.js) salvo refactor de testabilidad justificado.
- **AC4:** clon limpio valida exit 0 (con y sin secretos), drift 0, scan_encoding/scan_domain_neutrality exit 0;
  Co-Authored-By Codex en el commit de producto.

Entrega a in_review con evidencia de duracion + corridas. Yo soy checker (clon limpio). rr=false.
