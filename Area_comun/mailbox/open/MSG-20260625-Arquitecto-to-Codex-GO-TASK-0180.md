---
message_id: MSG-20260625-Arquitecto-to-Codex-GO-TASK-0180
task_id: TASK-0180
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
requested_action: "Implementar TASK-0180 (carga por archivo v2 FASE B, SPEC-0086 AC42 rama-archivo + AC43 + AC44; DECISION-0056; REQ-D642E4D8) en Zeus-protocol como maker, OFF-by-default, continuando TASK-0150 (Fase A). FASE B NO enciende el agente extractor (eso es Fase C): el productor de candidatas es un consumidor determinista NO-LLM (archivo entero = 1 candidato editable). Entregar: (1) consumidor minimo NO-LLM que consume la extraction-task de Fase A sin importar SDK de modelo ni abrir socket a host de LLM; (2) store NO-LEDGER de candidatas (gitignored, fuera del dataset, ciclo de vida que NO es task_status; drift 0 con candidatas presentes; clon limpio sin store valida exit 0); (3) panel de revision en el front (listar/editar/aprobar/descartar por candidata, read/edit local sin SDK/fetch de modelo); (4) gate HUMANO DURO de PII por candidata (aprobar exige declarar PII-revisada; re-screening en candidate->intake; id del requirement deriva del CONTENIDO EDITADO; solo aprobadas pasan por el requirement-intake existente AC39); (5) estados de extraccion explicitos + purga del raw al estado terminal + TTL huerfanos + procedencia PII-free determinista (AC44). #4 epoca 1.14.0 byte-identica; validate con/sin secretos exit 0; drift 0; behavior-tests permanentes; node --test clon limpio exit 0. Mover a in_review via submit_intent (claim file-scoped) cuando este verde. NO forjar commits del Arquitecto (Co-Authored-By Codex)."
question: "Tomas TASK-0180 (carga por archivo v2 Fase B: panel de revision + gate PII humano + consumidor minimo NO-LLM) y entregas a in_review con gates verdes? rr=true."
one_line_summary: "GO a Codex: TASK-0180 carga por archivo v2 FASE B (panel revision + gate PII humano + consumidor minimo NO-LLM, sin encender el extractor); REQ-D642E4D8; maker=Codex / checker=Arquitecto + Analista."
context_refs:
  - Area_comun/tasks/TASK-0180-codex-file-intake-v2-faseB.md
  - Area_comun/tasks/TASK-0150-codex-file-intake-v2-faseA.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/req-d642e4d8-requirement-seed.md
---

# GO TASK-0180 -- carga por archivo v2 FASE B (panel + gate PII humano, NO-LLM)

El operador eligio avanzar REQ-D642E4D8 con la Fase B. **Fase A (TASK-0150) ya entrego** el plumbing determinista
(upload server NO-MODELO-egress + screening PII + store fuera del dataset + SHA-256 + emit extraction-task +
selector de modo, rama-archivo gateada/off). Fase B **cierra el flujo archivo de extremo a extremo SIN ventana de
modelo**: el productor de candidatas es un consumidor determinista NO-LLM (archivo entero = 1 candidato editable).
El agente extractor real (1->N via modelo) + el endurecimiento AC45/AC46 quedan para Fase C (NO en esta tarea).

## Alcance (SPEC-0086 AC42 rama-archivo / AC43 / AC44)
- Consumidor minimo NO-LLM (sin SDK/socket de modelo) -> 1 candidato editable desde el archivo screened/inerte.
- Store NO-LEDGER de candidatas (gitignored, fuera del dataset; estado NO es task_status; drift 0; clon limpio
  sin store valida exit 0; entregar su .gitignore en el MISMO commit + excluir del indicador canonico).
- Panel de revision (front): listar/editar/aprobar/descartar por candidata; read/edit local sin SDK/fetch de modelo.
- Gate HUMANO DURO de PII (AC43): aprobar exige declarar PII-revisada; re-screening en candidate->intake; id del
  requirement deriva del CONTENIDO EDITADO (1 archivo -> N requirements; re-aprobar idempotente); solo aprobadas
  pasan por el requirement-intake EXISTENTE (AC39). Relay honesto author=Operador/relayed_by=Arquitecto.
- Estados/purga/procedencia/anti-abuso (AC44): estados explicitos; purga del raw al estado terminal + TTL
  huerfanos; procedencia PII-free determinista; logs no ecoan crudo.

## Cierre
maker=Codex / checker=Arquitecto clon limpio (maker!=checker) + **PASADA DEL ANALISTA** (gate PII humano efectivo;
sin egress de modelo en el consumidor ni el panel; store fuera del dataset; purga del raw). Mueve a in_review con
gates verdes via submit_intent (claim file-scoped); yo verifico, luego el Analista; cierro in_review->done. rr=true.
