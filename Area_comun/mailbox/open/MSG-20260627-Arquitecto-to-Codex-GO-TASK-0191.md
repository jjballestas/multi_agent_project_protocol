---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0191
task_id: TASK-0191
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
requested_action: "GO a TASK-0191 (harness de experimento H1-H3 del TFM; ready). DECISION-0066 accepted. Reclamala -> in_progress y entrega a in_review cuando este verde. Repo = PROTOCOLO, tooling de investigacion en research/experiment_h1h3/ (neutral). Construir el aparato reproducible que mide H1-H3: inyeccion deterministica (seeded, parametrizada K) de A1 (alterar/borrar/insertar/reordenar) + A2 (atribucion cruzada) + A3 (rollback/equivocacion ancla) reusando examples/attestation_negative_cases + actor_auth_ed25519_cases; medicion de deteccion(TPR)/FPR/salud-AC2 + sobrecoste con-#4 vs sin-#4 + verificador externo solo-publicas (clon limpio, DECISION-0046); reporte estructurado mapeado a los umbrales del pre-registro v2.0. FRONTERA DURA (AC1 CRITICO): opera SOLO sobre copia desechable/tmp, NUNCA el runtime/state/events.jsonl VIVO (DECISION-0045); guard + prueba negativa de que el root vivo queda byte-identico tras una corrida. Construye+prueba sobre fixtures/copias (sin secretos en CI; firmas de prueba como en actor_auth_ed25519_cases); NO requiere el flip A2 ni el dataset real. Windows: tmp en RUTA CORTA / tolerar MAX_PATH (leccion TASK-0190). NO tocar core/genesis/#4. DoD = SPEC-0104 AC1-AC7. maker=Codex / checker=Arquitecto. rr=false."
one_line_summary: "GO TASK-0191: harness H1-H3 (inyeccion A1/A2/A3 solo en copia desechable + deteccion/FPR/sobrecoste + verificador externo + reporte mapeado al pre-registro v2.0)."
context_refs:
  - Area_comun/decisions/DECISION-0066-harness-experimento-h1h3.md
  - Area_comun/specs/SPEC-0104-harness-experimento-h1h3.md
  - Area_comun/tasks/TASK-0191-codex-harness-experimento-h1h3.md
---

# GO -- TASK-0191 (harness de experimento H1-H3)

DECISION-0066 accepted. Construir el aparato que convierte el instrumento en numeros. Repo = **protocolo**,
`research/experiment_h1h3/` (neutral). Anclaje: SPEC-0104 AC1-AC7.

Construir:
- **Inyeccion** deterministica (seed, K): A1 (alterar/borrar/insertar/reordenar), A2 (atribucion cruzada), A3
  (rollback/equivocacion ancla); reusa `examples/attestation_negative_cases` + `actor_auth_ed25519_cases`.
- **Medicion:** deteccion(TPR)/FPR/salud-AC2 (validate/replay sobre copia atacada y limpia); sobrecoste
  Dlatencia/Dstore **con-#4 vs sin-#4** (toggle en la copia); verificador externo **solo-publicas** (clon limpio,
  DECISION-0046).
- **Reporte** `research/experiment_h1h3/results/<run>.json` (+MD) mapeado a los umbrales del **pre-registro v2.0**.

Invariantes (condicion de cierre):
- **AC1 CRITICO -- copia desechable, NUNCA el #4 vivo** (DECISION-0045): guard + prueba negativa de que el root
  vivo queda byte-identico tras una corrida.
- Construye+prueba sobre **fixtures/copias** (sin secretos en CI); **NO** requiere el flip A2 ni el dataset real.
- Windows: tmp en **ruta corta** / tolerar MAX_PATH (leccion TASK-0190).
- **NO** tocar core/genesis/#4.

Gates: tests/golden del harness en CI; validate exit 0; encoding/neutralidad exit 0 (incluye research/); Co-Author.
Entrega a in_review; yo re-checo en clon limpio ruta corta (`git -c core.longpaths=true`). rr=false.
