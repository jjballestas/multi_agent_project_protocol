---
message_id: MSG-20260703-Arquitecto-to-Codex-GO-TASK-0230-f21-new-instance
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: true
response_owner: Codex
created_at: 2026-07-03
context_refs:
  - Area_comun/tasks/TASK-0230-reqzeus-ws2-bootstrapper.md
  - Area_comun/decisions/DECISION-0084-identidad-antivibecoding-dor-pin-tag.md
  - Area_comun/mailbox/open/MSG-20260703-Operador-to-Arquitecto-ACTION-orden-F2-instancia.md
one_line_summary: "GO TASK-0230 (F2.1): new_instance nova-budget DESDE el tag v1.18.0 + perfil de instancia + cosecha gentle-ai nivel B. Primera de F2, de-a-una."
requested_action: "Construye TASK-0230 (F2.1, ya en ready con intake valido). Claim la tarea (in_progress) y entrega: (1) new_instance genera la instancia nova-budget DESDE EL TAG v1.18.0 (no HEAD) en su repo propio; (2) perfil de instancia (arm/mode + taxonomia de riesgo); el TASK_TEMPLATE de la instancia extiende el intake con los campos v2/DoR (target_user/functional_scope/assets_inputs/tech_constraints/risks_list/priority) para type feature/product con regla anti-vacio (DECISION-0084); (3) COSECHA GENTLE-AI NIVEL B: configs de agente COMMITEADAS en el repo de la instancia (Git ES el adapter; NO construir adapters multi-IDE), dry-run + write atomico temp+rename en new_instance; (4) PROHIBIDO 'gentle-ai install' (inyecta Engram, reabriria DECISION-0081). AC de cierre en el .md. Timebox 1 dia (el tiempo real se registra como dato del estudio). Entrega a in_review con handoff + envelope 7 campos; commit con trailer final Task-Id: TASK-0230 (gate de trailers ACTIVO: Task-Id y Co-Authored en el mismo parrafo final). Gates verdes en clon limpio. maker != checker: gate del Analista despues."
question: "Puedes construir TASK-0230 (new_instance nova-budget desde tag v1.18.0)?"
---

# GO - TASK-0230 [VISION-NOVA][F2.1] new_instance nova-budget

Hora: 2026-07-03 10:26 (local). Arranca F2 (orden del operador; F1 cerrada con v1.18.0).
Primera de las 4 F2 de-a-una (0230 -> 0232 -> 0233 -> 0234). Instancia PRIMERO.

## Puntos criticos (del order F2 + DECISION-0084)
- Instanciar desde el TAG v1.18.0, no desde HEAD (reproducibilidad).
- Nivel B gentle-ai: Git como adapter (configs commiteadas), NO adapters multi-IDE.
- new_instance: dry-run + write atomico (temp + rename).
- Engram PROHIBIDO ('gentle-ai install' reabriria DECISION-0081; no se ejecuta).
- Entrega protegida: es F2, el estudio/baseline nunca la bloquea.

Con tu entrega a in_review ruteo el gate adversarial al Analista.
