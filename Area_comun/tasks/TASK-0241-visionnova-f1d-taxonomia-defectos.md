---
task_id: TASK-0241
title: "[VISION-NOVA][F1.4] Taxonomia de defectos D1-D4 ampliada + severidad del checker + subconteo declarado"
type: docs
status: proposed
owner: Arquitecto
phase: P2
priority: medium
created_at: 2026-07-02
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [GOAL-VISION-NOVA-001]
linked_decisions: [DECISION-0083]
linked_reqs: [GOAL-VISION-NOVA-001]
file: Area_comun/tasks/TASK-0241-visionnova-f1d-taxonomia-defectos.md
---

# TASK-0241 - [VISION-NOVA][F1.4] Taxonomia de defectos + severidad del checker

Owner: Arquitecto (doc) + Analista (gate adversarial). Codex no requerido. Paralelo, no bloquea a Codex.

## Alcance
Doc versionado con subcategorias que cubren los 6 huecos del veredicto (requisito mal
entendido, deuda de arquitectura, performance no testeada, UX/soporte, integracion externa,
conciliacion tardia) + seccion de SUBCONTEO ESPERADO (defectos que el estudio declara que NO
capta). Adopta la severidad del checker CRITICAL / WARNING-real / WARNING-theoretical /
SUGGESTION con la regla "si el uso normal lo dispara, es real" (cosecha gentle-ai).

## DoD (testable)
1. Doc en Area_comun/protocol/ (o anexo del pre-registro) commiteado, ASCII.
2. Prompt del checker (Analista) actualizado con la escala de severidad.
3. Prueba de mesa: 10 defectos historicos del repo re-clasificados sin residuo; anexada.
4. GO adversarial del Analista sobre la taxonomia.
