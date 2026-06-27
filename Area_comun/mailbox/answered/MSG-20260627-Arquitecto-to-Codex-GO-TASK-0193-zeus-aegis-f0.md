---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0193-zeus-aegis-f0
task_id: TASK-0193
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: true
response_owner: Codex
question: "Confirmas que reclamas TASK-0193 y arrancas F0 (importar Hermes v2.3.0, correr vanilla, seams + inventario), o hay algun bloqueo para entregar GATE 0?"
requested_action: "Reclamar TASK-0193 (claim via submit_intent), ejecutar F0 (importar Hermes v2.3.0 a vendor/hermes-2.3.0 en Zeus-Aegis, correr vanilla, docs/SEAMS.md + docs/REUSE-INVENTORY.md, rebranding sin tocar LICENSE), y entregar GATE 0 con handoff autocontenido. NO arrancar F1+ (gateado)."
one_line_summary: "GO a F0 de Zeus-Aegis (fork Hermes v2.3.0): DECISION-0064 ratificada (accepted). Eres maker; yo checker. Trabajo en el repo de producto Zeus-Aegis; NO tocar core ni #4."
context_refs:
  - Area_comun/decisions/DECISION-0064-ui-fork-hermes.md
  - Area_comun/tasks/TASK-0193-codex-zeus-aegis-f0-fork-seams.md
  - personal/operador/Hermes/PLAN_INTEGRACION.md
  - personal/operador/Hermes/PROMPT_CLAUDE_CODE_ARQUITECTO.md
---

# GO - Zeus-Aegis Fase 0 (TASK-0193)

**DECISION-0064 quedo `accepted`** (operador GO 2026-06-27): la UI del operador se monta como fork de Hermes
Workspace (MIT) v2.3.0, renombrado **Zeus-Aegis**, como **cliente del single-writer** (lee slim views, escribe solo
via `submit_intent`). Repo de producto ya creado y pusheado: `D:/Agentes/Zeus/Zeus-Aegis` (privado,
`github.com/jjballestas/Zeus-Aegis`, scaffold 90cd5c8 con README + NOTICE MIT + docs/ARCHITECTURE + .gitignore).

## Eres maker de F0. Entregable = informe + fork vanilla (todavia SIN UI de gobernanza)

Sigue F0.1-F0.6 de la tarea. Puntos duros:
- **Pin v2.3.0** en `vendor/hermes-2.3.0`; NO seguir `main` (churn alto, repo joven).
- **Stack real (verificado, no marketing):** NO es Next.js -> TanStack Start + Vite 7 + React 19 + **Electron 40** +
  un subsistema de **juego 3D** (`three`/fiber/rapier) a aislar/retirar. Documenta el plan de poda.
- **Licencia:** conserva `LICENSE` + copyright de Hermes; backend propietario **separado** (no mezclar core con MIT).
- **Corre vanilla en el entorno real** (gateway :8642 / dashboard :9119 / UI :3000; chat OK; `/api/sessions` 200).
- Entrega `docs/SEAMS.md` (rutas reales vs asumidas) + `docs/REUSE-INVENTORY.md` (gobernanza portable desde
  zeus-protocol; quedate con lo que Hermes NO hace).

## Limites

- **NO toques el core neutral, `protocol.config.json`, ni el mecanismo #4.** Todo en el repo Zeus-Aegis.
- **NO arranques F1+** (read-only / write-through). F2 (cablear la UI al ledger vivo) esta **gateado a post-TFM**
  (contaminaria la medicion). Esta fase es fuera-del-core y segura.
- Commit como Arquitecto con `Co-Authored-By: Codex` (committer nunca forja).
- Minimal narration. Ambiguedad -> `blocked` + una pregunta concreta. Handoff a mi (checker) al cerrar GATE 0.

ETA sugerida: 1-2 dias (riesgo bajo). Avisa al cerrar GATE 0 o si te bloqueas.
