---
message_id: MSG-20260703-Operador-to-Arquitecto-ACTION-dor-v2-en-0243
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-03
context_refs:
  - personal/operador/vision-nova/CHECKLIST-DEFINITION-OF-READY-V2.md
  - Area_comun/tasks/TASK-0243 (proposed)
one_line_summary: "Al promover TASK-0243: la mini-DECISION incluye el anexo Definition-of-Ready (checklist 10 puntos del Operador); F2.1 extendera el template de instancia con intake v2 por tipo."
requested_action: "[DIRECTIVA] (1) Cuando promuevas TASK-0243 (mini-DECISION anti-vibecoding), su alcance INCLUYE anexar la Definition of Ready del Operador (los 10 puntos, ver checklist referenciado) como doctrina: la interrogacion de requisitos existe justamente con el fin de llenar esos 10 puntos antes de que una tarea sea ready. (2) Anota en el cuerpo de TASK-0230/F2.1 que el TASK_TEMPLATE de la instancia nova-budget extiende el bloque intake con los campos v2 del checklist s.3 (target_user, functional_scope, assets_inputs, tech_constraints, risks_list, priority) obligatorios para type feature/product, con la regla anti-vacio (ninguno explicito vale, ausente no). (3) NO se reabre TASK-0238 ni se toca el validador del hub en F1: el enforcement estructural de los campos v2 es de la instancia o de v1.19 (decision futura). [RECOMENDACION] El encaje exacto de campos/enums es tuyo y de Codex; el requisito duro son los 10 puntos cubiertos en tareas de producto."
question: ""
---

# ACTION - Definition of Ready v2 en TASK-0243 + template de instancia (F2.1)

El Operador pregunto si la metodologia quedara preparada con su checklist de 10
puntos (objetivo, usuario objetivo, alcance, fuera de alcance, contenido/assets,
restricciones tecnicas, criterios de aceptacion, pruebas/gates, riesgos,
prioridad). Respuesta del analisis: el intake v1 (0238) cubre 6/10; los 4
faltantes (usuario objetivo, assets, restricciones tecnicas, prioridad) son
campos de PRODUCTO y aterrizan sin reabrir nada: doctrina en 0243 + template
extendido en la instancia (F2.1). Detalle completo y mapa de cobertura en
personal/operador/vision-nova/CHECKLIST-DEFINITION-OF-READY-V2.md.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
