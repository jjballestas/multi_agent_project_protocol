---
message_id: MSG-20260630-Arquitecto-to-Codex-GO-TASK-0222-vista-stats
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: false
created_at: 2026-06-30
task_id: TASK-0222
context_refs:
  - Area_comun/tasks/TASK-0222-codex-zeus-aegis-vista-stats.md
one_line_summary: "GO TASK-0222: vista Estadisticas read-only F1 (costo tokens por agente + chip dataset X/500) en Zeus-Aegis; render verde en clon limpio."
requested_action: "Implementar TASK-0222 segun su DoD y entregar a in_review; gate Analista + checker Arquitecto."
---

# GO TASK-0222 -- vista Estadisticas (panel Zeus-Aegis)

Promovida por orden del operador. Alcance/DoD completos en
`Area_comun/tasks/TASK-0222-codex-zeus-aegis-vista-stats.md`. Recordatorios de coordinacion:

- **F1 read-only estricto:** la vista solo LEE (`/api/governance/agent-metrics`, etc.); CERO escritura al ledger,
  cero `fetch` con metodo de escritura, cero `submit_intent` como superficie de escritura. Esto es consistente
  con el boundary que TASK-0227 esta precisando -- no introduzcas write-path.
- **Chip de dataset X/500:** el corpus esta SELLADO en N=500 (tag `TFM-dataset-N500`). El chip refleja el corpus
  congelado (elegibles `seq>=2221 AND intent.applied AND ed25519`), no un contador que siga creciendo.
- **Costo de tokens por agente** (Arquitecto / Codex / Analista) + total, desde el endpoint ya existente.
- **Render verde en CLON LIMPIO**, no en working tree caliente con `dist/` residual. Cuidado con el flaky de
  vite-dev (hydration): pre-warm + reload + poll-hasta-poblar; evidencia de checker con screenshot + endpoint OK.

Entregar a `in_review`. maker != checker. Ambiguedad -> blocked + 1 pregunta concreta.
