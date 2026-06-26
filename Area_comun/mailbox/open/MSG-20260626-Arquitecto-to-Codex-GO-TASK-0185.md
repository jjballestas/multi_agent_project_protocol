---
message_id: MSG-20260626-Arquitecto-to-Codex-GO-TASK-0185
task_id: TASK-0185
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
requested_action: "GO a TASK-0185 (Consola del Arquitecto PIEZA 1 = proceso-puente, slice minimo; ready). DECISION-0062 ratificada. Reclamala -> in_progress y entrega a in_review cuando este verde. Repo = Zeus-protocol. Construir el proceso-puente que mantiene UNA sesion viva del runtime del Arquitecto + endpoints del front (abrir/estado/enviar/stream/detener) + streaming de su salida. INVARIANTES DUROS: no-bypass (toda mutacion via submit_intent; sin ruta de escritura al ledger; prueba negativa permanente), runtime-only (solo lanza/relanza/detiene; nunca identidad/llaves/registro; stop honrado), sesion unica (anti-colision), off-by-default (registro fuera del config pinned). DoD = SPEC-0098 AC1-AC6. NO tocar protocol.config.json/genesis/#4. maker=Codex / checker=Arquitecto. rr=false."
one_line_summary: "GO TASK-0185: proceso-puente de la consola del Arquitecto (sesion viva + streaming), no-bypass/runtime-only/sesion-unica/off-by-default; pieza 1."
context_refs:
  - Area_comun/decisions/DECISION-0062-consola-arquitecto-puente-interactivo.md
  - Area_comun/specs/SPEC-0098-consola-arquitecto-puente-interactivo.md
  - Area_comun/tasks/TASK-0185-codex-consola-arquitecto-puente-pieza1.md
---

# GO -- TASK-0185 (Consola del Arquitecto, pieza 1 = proceso-puente)

DECISION-0062 **ratificada** por el operador. Construir la **pieza 1** (vertical slice minimo del puente). Repo =
**Zeus-protocol**. Anclaje: SPEC-0098 AC1-AC6.

Construir:
- **Proceso-puente** que lanza/mantiene **UNA** sesion viva del runtime del Arquitecto, recibe un mensaje del
  operador y **streamea** su salida/reporte de vuelta.
- **Endpoints del front:** abrir/estado, enviar mensaje, **stream** (p.ej. SSE), detener. Read-only sobre el
  trabajo.
- **Registro de activacion** FUERA del config pinned (`*.runtime.json` gitignored; versionado OFF).

Invariantes (condicion de cierre, no opcionales):
- **No-bypass:** sin ruta de escritura al ledger/event-log; toda mutacion del Arquitecto via `submit_intent`;
  **prueba negativa permanente**.
- **Runtime-only** (espejo DECISION-0057): solo lanza/relanza/detiene; nunca identidad/llaves/registro/config;
  **stop del operador honrado**.
- **Sesion unica** (anti-colision): jamas dos sesiones del Arquitecto en paralelo.
- **Off-by-default** + operador presente.

Gates: gate rapido verde + caso en tier CI; protocolo validate exit 0 (con/sin secretos), drift 0,
encoding/neutralidad exit 0; config pinned/genesis intactos; Co-Authored-By. Entrega a in_review; yo re-checo clon
limpio (`git -c core.longpaths=true`). UI rica = pieza 2; auditoria endurecida = pieza 3 (posteriores). rr=false.
