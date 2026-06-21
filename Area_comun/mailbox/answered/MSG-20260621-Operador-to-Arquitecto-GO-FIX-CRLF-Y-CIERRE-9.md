---
message_id: MSG-20260621-Operador-to-Arquitecto-GO-FIX-CRLF-Y-CIERRE-9
task_id: TASK-0148
type: DECISION
from: Operador
to: Arquitecto
status: answered
requires_response: false
response_owner: Arquitecto
requested_action: "GO al fix del rojo de clon limpio que marco el Analista (ajeno a la ingestion): anadir .gitattributes eol=lf a Zeus-protocol + hacer la regex del test Mermaid tolerante a CRLF (\\r?\\n), gobernado. Re-verificar npm test 41/41 en CLON LIMPIO (gate DECISION-0037). Con eso verde + el 7/7 del Analista (ingestion OK por comportamiento): aplicar mi PRE-AUTH condicionada (dejar la carga por archivo RUNTIME-READY, versionado enabled:false OFF, encendido por env) y CERRAR TASK-0148 (#9) -> done. La logica de ingestion NO se toca."
question: "GO al fix CRLF (.gitattributes eol=lf + regex tolerante), re-verificar 41/41 en clon limpio, y con eso cerrar el #9 dejando la ingestion runtime-ready por mi pre-auth?"
one_line_summary: "GO: aplica el fix CRLF/clean-clone que marco el Analista (.gitattributes eol=lf + regex Mermaid tolerante), re-verifica 41/41 en clon limpio, y con eso + ingestion OK 7/7 cierra TASK-0148 (#9) y deja la carga por archivo runtime-ready (versionado OFF) por mi pre-auth. Ingestion sin rework."
context_refs:
  - Area_comun/artifacts/ANALISTA-REQ-31100EAF-ingestion-veredicto.md
  - Area_comun/tasks/TASK-0148-codex-front-file-ingestion.md
  - Area_comun/decisions/DECISION-0055-file-ingestion.md
deadline_or_blocking_level: normal
---

# GO - fix CRLF/clean-clone + cierre del #9

El Analista dio la ingestion **OK 7/7 por comportamiento** (bounding/PII/idempotencia/OFF-gated/honestidad/
egress/no-bypass), y marco UN cambio AJENO a la ingestion: la suite sale **roja 40/41 en clon limpio Windows**
por el test de Mermaid (CRLF en docs/MANUAL-operador.md + Zeus sin .gitattributes, core.autocrlf=true).

GO para:
1. Aplicar el fix gobernado: `.gitattributes` con `eol=lf` en Zeus-protocol + regex del test Mermaid tolerante
   a CRLF (`\r?\n`). La logica de ingestion NO se toca.
2. Re-verificar **npm test 41/41 en CLON LIMPIO** (gate DECISION-0037 eol=lf).
3. Con eso verde + el 7/7 del Analista: aplicar mi **PRE-AUTH condicionada** -> dejar la carga por archivo
   **RUNTIME-READY** (versionado enabled:false OFF, encendido por env) y **CERRAR TASK-0148 (#9) -> done**.

Con el #9 cerrado quedan los 9 servidos -> stand-down (Codex + tu cron). El defecto del Intake (REQ-643B160A)
queda para su SPEC despues, como acordamos. Canal ASCII.
