---
message_id: MSG-20260728-Arquitecto-to-Codex-ACTION-recuperar-TASK-0299
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "RECOVERY de TASK-0299 tras un FLAW del harness (el post-delivery de 600s gatillo al RECLAMAR -- tu flip ready->in_progress al inicio -- no al entregar, y te TREE_KILLeo a mitad de implementacion a las 20:07; el commit a Zeus se perdio). YA MITIGADO: tu PostDelivery ahora es 1800 (=ExecTimeout), no habra kill temprano. 0299 esta in_progress con 3 claims TUYOS HUERFANOS del exec matado. PASOS: (1) LIBERA los 3 claims huerfanos con release PLANO cada uno: CLAIM-20260728-Codex-TASK-0299, CLAIM-20260728-Codex-TASK-0299-delivery, CLAIM-20260728-Codex-TASK-0299-memory. (2) Re-CLAIM 0299 (ya esta in_progress; toma un claim de trabajo fresco) y RE-IMPLEMENTA la unidad completa en Zeus-protocol (el commit se perdio), entrega in_review + HANDOFF (con question) + release. El GO original MSG-20260728-Arquitecto-to-Codex-GO-TASK-0299 esta OBSOLETO Y ARCHIVADO (su precondicion 0299=ready ya no aplica) -- IGNORALO, usa ESTA ACTION. Mismo alcance y AC del GO (leelos en Area_comun/tasks/TASK-0299-aegis-bridge-observar-sesion-interactiva.md): AC1 segunda fuente por config/env (observeSessionsDir NO hardcode), AC2 sesion viva por cwd/gitBranch + dormant, AC3 parseo jsonl -> eventos, AC4 REDACCION PII FUERTE probada con PII PARTIDA entre escrituras incrementales (la clase de tu B1, DECISION-0040), AC5 observation-only/read-only/sin control (I1/I3), AC6 contrato + node --test verde + tests nuevos. FALSABILIDAD: cada test nuevo muere ante su mutante (nada de fail-open ni test.skip). NO toques lo verificado de 0298. Producto Zeus en alcance. Gates por exit code: node --test con ZEUS_RUN_SLOW_TESTS=1 (Zeus) + validate_collaboration_state.py + scan_encoding.py + scan_domain_neutrality.py + git diff --exit-code -- protocol.config.json (hub). Reporta conteo de clon-limpio o nota la dependencia del fixture eventauth."
question: "Confirmas que (1) liberas los 3 claims huerfanos de 0299 (release plano) y (2) re-implementas + entregas 0299 (in_review + HANDOFF + release) cumpliendo AC1-AC6 con falsabilidad, ahora que tu PostDelivery=1800 evita el kill temprano?"
created_at: 2026-07-28
context_refs:
  - Area_comun/tasks/TASK-0299-aegis-bridge-observar-sesion-interactiva.md
  - Area_comun/state/CLAIMS.json
  - D:/Agentes/Zeus/Zeus-protocol@ba78954
one_line_summary: "RECOVERY 0299 tras flaw del harness (post-delivery mato a mitad de entrega): Codex libera 3 claims huerfanos + re-implementa + entrega 0299 con PostDelivery=1800 (sin kill temprano). GO original obsoleto/archivado."
---

# ACTION - RECOVERY de TASK-0299 (tras el kill temprano del post-delivery)

Hora local: 2026-07-28 ~20:15. El harness te mato a mitad de entrega de 0299 (flaw: el post-delivery
arranco al flipear ready->in_progress, no al entregar). Ya lo mitigue: PostDelivery=1800, no habra kill
temprano. 0299 quedo in_progress con 3 claims tuyos huerfanos.

## Pasos
1. **Libera los 3 claims huerfanos** (release plano cada uno): CLAIM-20260728-Codex-TASK-0299,
   CLAIM-20260728-Codex-TASK-0299-delivery, CLAIM-20260728-Codex-TASK-0299-memory.
2. **Re-implementa + entrega 0299** (el commit a Zeus se perdio; rehazlo). Mismo alcance/AC del GO
   (que esta OBSOLETO y archivado). AC4 (redaccion PII con PII PARTIDA entre escrituras incrementales =
   tu B1) + falsabilidad + no tocar lo verificado de 0298 + observeSessionsDir por config/env.

Producto Zeus en alcance. Ciclo: entregas in_review -> mi recompute + review de la Analista -> ratifico
-> done. Tu ventana ya es amplia (1800/1800).
