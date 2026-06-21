---
message_id: MSG-20260622-Arquitecto-to-Operador-RESP-INGESTION-V2-OPCION4
task_id: none
type: DECISION
from: Arquitecto
to: Operador
status: open
requires_response: false
response_owner: Operador
one_line_summary: "Carga por archivo v2 REGISTRADA (REQ-D642E4D8, priority high, supersede REQ-31100EAF) y SPEC autorada con tu OPCION 4 (server NO-EGRESS: upload gobernado guarda en ruta acotada + PII-gate-en-ingest + emite tarea de extraccion; un AGENTE extrae candidatas en estado candidate FUERA del backlog; panel de revision; solo aprobadas -> intake gobernado AC39). DRAFT-DECISION-0056 + DRAFT-SPEC-0086-ext10 (AC40..AC43), dimensionada en FASES A/B/C. Espera ratificacion para promover. La OPCION 4 disuelve el trilema: server determinista/#4-limpio; LLM vive en los agentes; no-determinismo fuera de #4."
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0056-file-ingestion-v2.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0086-ext10-file-intake-v2.md
  - Area_comun/tasks/req-d642e4d8-requirement-seed.md
deadline_or_blocking_level: normal
---

# RESP - v2 registrada + SPEC con tu OPCION 4

Adopto tu **OPCION 4** integra (descarto la op2 = egress del server). Tu encuadre disuelve el trilema y lo
respeta todo: server **no-egress / determinista / #4-limpio**; el LLM vive donde ya vive (los agentes); el
no-determinismo del LLM queda FUERA de #4 (solo entra lo que tu apruebas, por el intake determinista).

## Registrado
**REQ-D642E4D8** (priority HIGH, `supersedes: REQ-31100EAF`) -- gobernado. NO speceo la v1 como definitiva.

## Drafts autorados (esperan tu ratificacion)
- **DRAFT-DECISION-0056** (mecanismo OPCION 4, OFF-by-default, Analista al cierre).
- **DRAFT-SPEC-0086-ext10** (AC40..AC43):
  - **AC40** Upload gobernado server-NO-EGRESS: PII-gate-en-ingest (antes de guardar/antes del agente; honesto,
    best-effort, DEF-PII sigue gate) + ruta acotada gitignored fuera del dataset + emite TAREA de extraccion; el
    server NO llama a ningun modelo (prueba negativa). #4 byte-identica.
  - **AC41** Extraccion = trabajo de AGENTE -> candidatas en estado `candidate` FUERA del backlog -> panel de
    revision -> solo APROBADAS al intake gobernado actual (AC39).
  - **AC42** Selector de modo (digitado vs archivo), validando obligatorios en AMBOS (carry AC39).
  - **AC43** Anti-abuso permanente: no-egress (falsable), ruta acotada/saneada/gitignored, contenido inerte,
    candidatas no-aprobadas no atestadas, PII-gate en ingest, #4 byte-identica.

## Dimensionamiento (FASES, de a una)
- **A (plumbing determinista):** AC40 + AC42 -- entrega ya, sin depender del agente.
- **B (candidatos + revision):** AC41 estado candidate + panel + aprobar -> intake.
- **C (loop de extraccion):** atar la tarea de extraccion a un agente (contrato de la tarea; agente LLM-backed
  de siempre). Es la pieza grande y ata a que un agente este en el loop (no instantaneo).

## Matices que recojo de tu mensaje
- Candidatas `candidate` (no PROPOSED) hasta aprobarse. Ruta de uploads acotada + limpieza/retencion (efimera,
  purga tras aprobar/descartar) -- en la SPEC. PII-gate INNEGOCIABLE en el ingest.

Si ratificas, promuevo en orden: DECISION-0056 -> ext10 -> GO Fase A a Codex. Codex en stand-down: reactivalo
para implementar. Canal ASCII.
