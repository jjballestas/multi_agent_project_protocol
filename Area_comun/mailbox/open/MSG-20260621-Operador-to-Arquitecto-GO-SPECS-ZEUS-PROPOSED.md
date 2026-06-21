---
message_id: MSG-20260621-Operador-to-Arquitecto-GO-SPECS-ZEUS-PROPOSED
task_id: none
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Autorar las SPECs (DECISION->SPEC con AC+test_plan, modelo SDD) de los 9 requisitos en PROPOSED del proyecto Zeus-protocol, listados abajo. Los quiero TODOS; tu propones el orden de ejecucion. Para REQ-31100EAF (carga por archivo) planifica que es superficie de ingestion de archivos -> probable pasada del Analista (ingestion/egress) al cierre, y nace OFF/gateada si abre superficie nueva. Reporta el plan/orden y los drafts en canonico por el camino gobernado."
question: "Autorizo que autores las SPECs de los 9 requisitos PROPOSED de Zeus-protocol (los quiero todos). Procedes y me propones el orden de ejecucion?"
one_line_summary: "GO para autorar SPECs de los 9 requisitos PROPOSED de Zeus-protocol (8 UX + carga por archivo). Los quiero todos; el Arquitecto propone orden. REQ-31100EAF es superficie de ingestion -> Analista al cierre. nova.budget es OTRO proyecto (NOVA), no entra en este batch."
context_refs:
  - Area_comun/tasks/req-31100eaf-requirement-seed.md
  - Area_comun/tasks/req-c1976857-requirement-seed.md
  - Area_comun/tasks/req-547c6c54-requirement-seed.md
  - Area_comun/tasks/req-3e31293f-requirement-seed.md
  - Area_comun/tasks/req-d2c6579f-requirement-seed.md
  - Area_comun/tasks/req-28118fc3-requirement-seed.md
  - Area_comun/tasks/req-b97838c6-requirement-seed.md
  - Area_comun/tasks/req-9af54a75-requirement-seed.md
  - Area_comun/tasks/req-4120b017-requirement-seed.md
deadline_or_blocking_level: normal
---

# GO - autorar SPECs de los 9 requisitos PROPOSED de Zeus-protocol

Doy GO para que autores las SPECs (SDD: DECISION -> SPEC con AC + test_plan) de TODOS los
requisitos que estan en PROPOSED del proyecto Zeus-protocol. No priorizo uno: los quiero todos.
Tu propones el orden de ejecucion.

Los 9:
- REQ-31100EAF - carga de requerimiento por archivo
- REQ-C1976857 - UX: Refrescar datos automaticamente al navegar entre secciones sin recargar
- REQ-547C6C54 - UX: Indicador de ultima actualizacion y estado de refresco de datos
- REQ-3E31293F - UX: Tooltips en codigos RF-N y acronimos tecnicos en todas las vistas
- REQ-D2C6579F - UX: Renderizar diagramas Mermaid en la vista Help
- REQ-28118FC3 - UX: Jerarquia tipografica en vistas Mailbox y Backlog
- REQ-B97838C6 - UX: Backlog Kanban - colapsar columnas vacias y mostrar contenido de done
- REQ-9AF54A75 - UX: Filtros en Ledger #4 por actor y tipo de evento
- REQ-4120B017 - UX: Tooltips explicativos en badges de la barra de integridad

Nota REQ-31100EAF: es superficie de ingestion de archivos (tipo/tamano, path traversal, PII,
contenido nunca ejecutado). Disenala OFF/gateada si abre superficie nueva y cuenta con pasada
del Analista (ingestion/egress) al cierre.

Fuera de este batch: nova.budget es de OTRO proyecto (NOVA), no de Zeus-protocol. Canal ASCII.
