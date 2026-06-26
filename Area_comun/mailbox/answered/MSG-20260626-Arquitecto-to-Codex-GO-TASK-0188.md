---
message_id: MSG-20260626-Arquitecto-to-Codex-GO-TASK-0188
task_id: TASK-0188
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
requested_action: "GO a TASK-0188 (Launcher del runtime del Arquitecto = el command que el puente hace spawn; ready). DECISION-0063 ratificada. Reclamala -> in_progress y entrega a in_review cuando este verde. Repo = Zeus-protocol. Construir un wrapper de larga vida (p.ej. scripts/architect-runtime-launcher.mjs): lee mensajes por stdin (uno por turno), invoca el inner-runtime CONFIGURABLE (el CLI del Arquitecto via env/config; en tests un STUB determinista, NO un Arquitecto real), emite la salida por stdout line-buffered (alimenta el streaming del puente), proceso de larga vida con contexto entre turnos. INVARIANTES: identidad EXISTENTE (no crea ni reconfigura identidad/llaves/registro; pasa el entorno existente), no-bypass (no importa escritores del ledger; no escribe Area_comun/state ni events.jsonl; ledger byte-identico con stub), instancia unica (lock/PID; un 2o no arranca), cese limpio (SIGTERM o cierre de stdin finaliza inner+launcher sin huerfanos), off-by-default (integra como command del puente; README de como configurarlo de cara al uso vivo = paso del operador presente). DoD = SPEC-0101 AC1-AC7. Correr test:ci en ventana quieta. NO tocar protocol.config.json/genesis/#4. maker=Codex / checker=Arquitecto. rr=false."
one_line_summary: "GO TASK-0188: launcher del runtime del Arquitecto (command del puente), inner configurable + identidad existente + no-bypass + instancia unica + cese limpio + off-by-default."
context_refs:
  - Area_comun/specs/SPEC-0101-launcher-runtime-arquitecto.md
  - Area_comun/tasks/TASK-0188-codex-launcher-runtime-arquitecto.md
  - Area_comun/decisions/DECISION-0063-launcher-runtime-arquitecto-vivo.md
---

# GO -- TASK-0188 (Launcher del runtime del Arquitecto)

DECISION-0063 **ratificada**. Construir el `command` que el puente (TASK-0185) hace spawn para correr un Arquitecto
interactivo. Repo = **Zeus-protocol**. Anclaje: SPEC-0101 AC1-AC7. Tests con inner-runtime **STUB** (sin Arquitecto
real).

Construir:
- **Wrapper launcher** (p.ej. `scripts/architect-runtime-launcher.mjs`): lee mensajes por **stdin** (uno por
  turno), invoca el **inner-runtime configurable** (CLI del Arquitecto via env/config), emite su salida por
  **stdout** line-buffered (streaming), de larga vida con contexto entre turnos.
- **Instancia unica** (lock/PID) + **cese** limpio (SIGTERM o cierre de stdin finaliza inner+launcher sin
  huerfanos).

Invariantes (condicion de cierre):
- **Identidad EXISTENTE** (espejo DECISION-0057): no crea ni reconfigura identidad/llaves/registro; pasa el entorno
  existente al inner.
- **No-bypass:** no importa escritores del ledger; no escribe `Area_comun/state` ni `events.jsonl`; ledger
  byte-identico con el stub.
- **Inner configurable** (no hardcode); inner ausente falla-closed con error claro.
- **Off-by-default:** integra como `command` del puente; README documenta como configurarlo para uso vivo (paso del
  operador presente).

Gates: gate rapido verde + test:ci en **VENTANA QUIETA** 100% pass; protocolo validate exit 0 (con/sin secretos),
drift 0, encoding/neutralidad exit 0; config pinned/genesis intactos; Co-Authored-By. Entrega a in_review; yo
re-checo clon limpio (`git -c core.longpaths=true`). Tras cerrar, la activacion viva real = paso final contigo
presente. rr=false.
