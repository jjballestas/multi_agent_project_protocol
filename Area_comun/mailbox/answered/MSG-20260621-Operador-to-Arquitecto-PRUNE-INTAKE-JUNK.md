---
message_id: MSG-20260621-Operador-to-Arquitecto-PRUNE-INTAKE-JUNK
task_id: none
type: DECISION
from: Operador
to: Arquitecto
status: answered
requires_response: false
response_owner: Arquitecto
requested_action: "Prunear (gobernado) 2 entradas de PROPOSED de Zeus-protocol que NO son requerimientos validos: (1) REQ-984A85C6 'Conciliar saldos por cuenta al cierre mensual' = fantasma de un bug del front (placeholder/ejemplo persistido como requerimiento; narrativa e intencion de aceptacion vacias; yo no lo file; no hay trabajo para NOVA). (2) duplicado del fix de estilo del boton: conservar REQ-40EC863F (mas completo) y prunear REQ-829CBFCE. Root cause lo filo aparte como defecto por el Intake."
question: "Pruneas REQ-984A85C6 (fantasma) y REQ-829CBFCE (duplicado), dejando solo REQ-40EC863F del fix del boton?"
one_line_summary: "Limpieza de PROPOSED: REQ-984A85C6 es un fantasma de bug del front (placeholder vacio, no es de NOVA) y REQ-829CBFCE duplica a REQ-40EC863F (fix de estilo del boton). Pido prune gobernado de los 2; conservar REQ-40EC863F. El bug raiz lo filo como defecto aparte."
context_refs:
  - Area_comun/tasks/req-984a85c6-requirement-seed.md
  - Area_comun/tasks/req-829cbfce-requirement-seed.md
  - Area_comun/tasks/req-40ec863f-requirement-seed.md
deadline_or_blocking_level: normal
---

# Prune de basura del Intake (2 entradas)

Dos entradas en PROPOSED de Zeus-protocol que no deben quedarse:

1. REQ-984A85C6 "Conciliar saldos por cuenta al cierre mensual": fantasma. El front dejo un
   texto generico/de ejemplo y lo persistio como requerimiento (narrativa e intencion de
   aceptacion = vacias). Yo no lo file y NO hay requerimientos para NOVA. Prune.
2. Duplicado del fix de estilo del boton "Nueva historia/requisito": REQ-829CBFCE y
   REQ-40EC863F son el mismo. Conservar REQ-40EC863F (mas detallado); prune REQ-829CBFCE.

El bug que genero el fantasma lo filo como defecto por el Intake (req aparte) para que tenga
SPEC + fix. Canal ASCII.
