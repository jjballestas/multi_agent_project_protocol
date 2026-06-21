---
message_id: MSG-20260621-Operador-to-Arquitecto-DEFECTO-INTAKE-FANTASMA
task_id: none
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Registrar (gobernado, capability orchestrator) este DEFECTO como requerimiento de Zeus-protocol y encolarlo (tu decides el orden respecto al batch). Lo registro por mailbox y no por el Intake a proposito: el bug ESTA en el Intake (genero el fantasma REQ-984A85C6 ya cancelado). Contenido del seed abajo (narrativa + intencion de aceptacion). Autoras la SPEC como con los demas."
question: "Registras este defecto del Intake como REQ (Zeus-protocol) y lo encolas para SPEC+fix?"
one_line_summary: "DEFECTO Zeus-protocol: el Intake persiste texto de ejemplo/placeholder como requerimiento fantasma (caso real: REQ-984A85C6, narrativa/intencion vacias, proyecto defaulteado a Zeus-protocol). Pido registrarlo gobernado como REQ + SPEC/fix. Lo mando por mailbox porque el bug esta en el propio Intake."
context_refs:
  - Area_comun/tasks/req-984a85c6-requirement-seed.md
deadline_or_blocking_level: normal
---

# DEFECTO - el Intake crea un requerimiento fantasma desde texto de ejemplo/placeholder

Registralo como requerimiento de Zeus-protocol (gobernado) para que tenga SPEC + fix. Seed:

## Titulo
Bug: el Intake crea un requerimiento fantasma desde texto de ejemplo/placeholder

## Narrativa
Como operador no quiero que el Intake persista textos de ejemplo/placeholder como
requerimientos reales. Aparecio REQ-984A85C6 "Conciliar saldos por cuenta al cierre mensual"
con narrativa e intencion de aceptacion vacias, que yo no escribi: un mensaje generico de
ejemplo que no deberia convertirse en requerimiento (ya cancelado por prune).

## Intencion de aceptacion
El Intake nunca debe crear un requerimiento a partir de texto placeholder/ejemplo. Un EXECUTE
solo procede con narrativa e intencion de aceptacion reales y no vacias (validacion que rechaza
campos vacios o iguales al placeholder, sin preview-as-green). Ademas el proyecto destino debe
elegirse explicitamente y no defaultear a Zeus-protocol.

Canal ASCII.
