---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0191
task_id: TASK-0191
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
answered_by: Codex
answered_at: 2026-06-27
requested_action: "GO a TASK-0191 (harness de experimento H1-H3 del TFM; ready). DECISION-0066 accepted. Reclamala -> in_progress y entrega a in_review cuando este verde. Repo = PROTOCOLO, tooling de investigacion en research/experiment_h1h3/ (neutral). Construir el aparato reproducible que mide H1-H3: inyeccion deterministica (seeded, parametrizada K) de A1 (alterar/borrar/insertar/reordenar) + A2 (atribucion cruzada) + A3 (rollback/equivocacion ancla) reusando examples/attestation_negative_cases + actor_auth_ed25519_cases; medicion de deteccion(TPR)/FPR/salud-AC2 + sobrecoste con-#4 vs sin-#4 + verificador externo solo-publicas (clon limpio, DECISION-0046); reporte estructurado mapeado a los umbrales del pre-registro v2.0. FRONTERA DURA (AC1 CRITICO): opera SOLO sobre copia desechable/tmp, NUNCA el runtime/state/events.jsonl VIVO (DECISION-0045); guard + prueba negativa de que el root vivo queda byte-identico tras una corrida. Construye+prueba sobre fixtures/copias (sin secretos en CI; firmas de prueba como en actor_auth_ed25519_cases); NO requiere el flip A2 ni el dataset real. Windows: tmp en RUTA CORTA / tolerar MAX_PATH (leccion TASK-0190). NO tocar core/genesis/#4. DoD = SPEC-0104 AC1-AC7. maker=Codex / checker=Arquitecto. rr=false."
one_line_summary: "GO TASK-0191 consumido: entregado a in_review con handoff HANDOFF-TASK-0191-codex-to-arquitecto-1."
context_refs:
  - Area_comun/decisions/DECISION-0066-harness-experimento-h1h3.md
  - Area_comun/specs/SPEC-0104-harness-experimento-h1h3.md
  - Area_comun/tasks/TASK-0191-codex-harness-experimento-h1h3.md
  - Area_comun/handoffs/HANDOFF-TASK-0191-codex-to-arquitecto-1.md
---

# GO -- TASK-0191 (harness de experimento H1-H3)

Consumido por Codex. Resultado: TASK-0191 entregada a `in_review`.
