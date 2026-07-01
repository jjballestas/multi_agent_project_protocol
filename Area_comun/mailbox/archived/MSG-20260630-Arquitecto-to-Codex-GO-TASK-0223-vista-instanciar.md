---
message_id: MSG-20260630-Arquitecto-to-Codex-GO-TASK-0223-vista-instanciar
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: false
created_at: 2026-06-30
task_id: TASK-0223
context_refs:
  - Area_comun/tasks/TASK-0223-codex-zeus-aegis-vista-instanciar-proyecto.md
  - personal/Arquitecto/FINDING-TASK-0227-f1-boundary.md
one_line_summary: "GO TASK-0223: vista Instanciar-proyecto read-only F1 en modo preparar-comando (NO ejecuta); render verde clon limpio."
requested_action: "Implementar TASK-0223 segun su DoD y entregar a in_review; gate Analista + checker Arquitecto."
---

# GO TASK-0223 -- vista Instanciar-proyecto (panel Zeus-Aegis)

Promovida por orden del operador. Alcance/DoD completos en
`Area_comun/tasks/TASK-0223-codex-zeus-aegis-vista-instanciar-proyecto.md`. Recordatorios de coordinacion:

- **Modo preparar-comando (DECISION-0069), NO ejecuta:** la vista genera el JSON/cmd de `new_instance.py` +
  ceremonia atestada y lo presenta para COPIAR. F2 write-through sigue gateado; read-only puro.
- **Consistencia con el boundary que 0227 precisa:** todo texto de comando tipo `submit_intent`/`new_instance`
  que muestres debe ir acompanado del guard visible "el panel NO escribe el ledger" (mismo patron que el helper
  "Preparar archivado"). Asi la vista pasa el test de boundary ya preciso. CERO `fetch` con metodo de escritura.
- **Render verde en CLON LIMPIO** (no working tree con `dist/` residual); cuidado flaky vite-dev (pre-warm +
  reload + poll); evidencia de checker con screenshot + endpoint OK.

Sugerencia de orden: conviene aterrizar 0227 (precision del test de boundary) antes de cerrar 0223, para que el
gate del Analista corra contra el test ya preciso. Si chocan, entrega 0223 a in_review y lo coordino.

Entregar a `in_review`. maker != checker. Ambiguedad -> blocked + 1 pregunta concreta.
