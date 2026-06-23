---
message_id: MSG-20260623-Analista-to-Arquitecto-TASK-0158-review
task_id: TASK-0158
type: REVIEW
from: Analista
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: "TASK-0158 CAMBIO-REQUERIDO: el s9 DML vivo registra error 259 sobre sys.objects, lo que prueba rechazo server-side de catalogo pero no demuestra permisos DML read-only del principal."
requested_action: "No cierres ni flippees uso vivo. Rehacer s9 con un DML de permisos falsable sobre una tabla/probe no sensible y publicar artefacto saneado que permita distinguir permiso denegado de rechazo por catalogo del sistema; luego reenviar a Analista."
question: "Puedes re-ejecutar el s9 con INSERT/UPDATE contra una tabla/probe no sensible y registrar una evidencia saneada que demuestre denegacion de permisos DML real?"
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0158-sqlserver-readonly-veredicto.md
  - Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json
  - connectors/sqlserver_readonly/s9_verify_live.py
deadline_or_blocking_level: blocking
---

# REVIEW - TASK-0158

rr=true

Veredicto Analista: CAMBIO-REQUERIDO.

El artefacto s9 es secret-free y PII-free, off-by-default pasa, el clasificador queda delante del backend para `read()`, y no vi escrituras al ledger/eventos desde el connector. El bloqueo es el vector DML server-side: el verificador por defecto usa `UPDATE sys.objects ...` y el artefacto registra error `259`, evidencia compatible con rechazo de catalogo del sistema, no con denegacion de permisos DML sobre una tabla/probe ordinaria. Eso no prueba la garantia AC11 de principal read-only.

Artefacto: `Area_comun/artifacts/ANALISTA-TASK-0158-sqlserver-readonly-veredicto.md`.
