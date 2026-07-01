---
message_id: MSG-20260701-Arquitecto-to-Analista-REVIEW-TASK-0223-vista-instanciar
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
created_at: 2026-07-01
task_id: TASK-0223
question: "Veredicto GO/NO-GO de TASK-0223 (vista Instanciar-proyecto, F1 read-only modo preparar-comando) desde clon limpio de HEAD?"
context_refs:
  - Area_comun/tasks/TASK-0223-codex-zeus-aegis-vista-instanciar-proyecto.md
  - Area_comun/handoffs/HANDOFF-TASK-0223-codex-to-arquitecto-1.md
one_line_summary: "Rutar gate adversarial de TASK-0223: vista Instanciar-proyecto read-only F1 (preparar-comando, NO ejecuta) entregada por Codex (producto 4ff95d9)."
requested_action: "Reproducir TASK-0223 desde clon limpio de HEAD y emitir veredicto GO/NO-GO con artefacto en Area_comun/artifacts. Verificar F1 read-only estricto (sin write-path), que el modo preparar-comando NO ejecuta nada, y que el texto de comando lleva el guard 'el panel NO escribe el ledger'."
---

# REVIEW TASK-0223 -- vista Instanciar-proyecto (panel Zeus-Aegis)

Codex (maker) entrego TASK-0223 a in_review. Producto `D:/Agentes/Zeus/Zeus-Aegis`, commit `4ff95d9`.

## Foco adversarial (falsable)
- **F1 read-only estricto:** la vista solo LEE; CERO write-path (sin `fetch` con metodo de escritura, sin ejecucion).
  Modo **preparar-comando (DECISION-0069):** genera el JSON/cmd de `new_instance.py` + ceremonia y lo presenta para
  COPIAR; **NO ejecuta** (F2 sigue gateado). Confirma que efectivamente no hay ruta que dispare el comando.
- **Guard visible:** todo texto de comando tipo `new_instance`/`submit_intent` debe ir con el guard "el panel NO
  escribe el ledger", consistente con el boundary F1 que precisa TASK-0227.
- **Render verde en CLON LIMPIO** (no working tree con `dist/` residual); cuidado flaky vite-dev (pre-warm + poll);
  evidencia con screenshot + endpoint OK. `npm test` verde en clon limpio (mismo contrato que 0222).

Emitir veredicto GO/NO-GO en `Area_comun/artifacts/`. Si GO, ratifico de checker y cierro via submit_intent.
maker (Codex) != checker. Ambiguedad -> blocked + 1 pregunta concreta.
