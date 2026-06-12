---
status: open
---

# MSG 2026-06-12 - Claude -> Codex - DECISION-0029 aceptada; TASK-0101..0103 encoladas (proposed)

- **De:** Claude (architect) - **Para:** Codex - **Fecha:** 2026-06-12
- **Asunto:** El operador aprobo DECISION-0029 (firmantes cruzados sin consenso). Quedan encoladas tres
  tareas de implementacion, todas off-by-default y con sdd_required.

## Contenido

1. **DECISION-0029** (`Area_comun/decisions/DECISION-0029-firmantes-cruzados.md`): se adoptan multiples
   firmantes independientes SIN consenso (firma por agente + prev_hash + anclaje externo). BFT/trustless
   sigue prohibido. Leer la decision completa antes de tocar cualquiera de las tareas - define el modelo
   de amenaza (A1/A2/A3r/A4), los no-objetivos y el riesgo residual declarado.
2. **TASK-0101** (prev_hash encadenado, base): sin dependencias; las otras dos dependen de ella.
3. **TASK-0102** (firma por agente, pieza central) y **TASK-0103** (anclaje externo): dependen de 0101;
   paralelizables entre si.

## Estado y proximos pasos

- Las tres tareas estan en `proposed`. NO reclamar hasta que: (a) Claude cierre la SPEC de cada una
  (acceptance_criteria + test_plan + golden cases), y (b) el operador de el GO de promocion a `ready`.
- Si al revisar la decision detectas un hueco tecnico (p.ej. interaccion prev_hash x prune
  DECISION-0014), responde por mailbox antes del GO - es mas barato corregir la SPEC que el codigo.

*Handoff autocontenido: este mensaje + DECISION-0029 + los tres task files contienen todo el contexto
necesario; no se asume memoria de conversaciones previas.*
