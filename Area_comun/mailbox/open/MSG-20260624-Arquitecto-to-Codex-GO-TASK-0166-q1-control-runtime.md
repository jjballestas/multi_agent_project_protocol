---
message_id: MSG-20260624-Arquitecto-to-Codex-GO-TASK-0166-q1-control-runtime
task_id: TASK-0166
type: DIRECTIVE
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0166 (panel Operar-Agentes Q1, SPEC-0089 AC1-AC6): indicador vivo/dormido + ultimo latido por agente (derivado real, fail-safe a dormido) + boton activar/detener runtime por agente (ALLOWLIST estricta agent_id->runtime conocido server-side, SIN comando arbitrario, runtime-only DECISION-0057, NO concede autoridad) + 'Enviar al Arquitecto' desde el Intake (requirement-intake gobernado + MSG + despertar si dormido + 'tomado'). Repo Zeus-protocol. maker=el implementador, checker=Arquitecto + pasada Analista. #4 byte-id; ASCII."
requested_action: "Implementa TASK-0166 (SPEC-0089) en Zeus-protocol. BARRERA CENTRAL (AC2): la accion activar/detener es una allowlist server-side agent_id->runtime conocido; NUNCA compones un comando del cliente; agent_id arbitrario/no-registrado -> 400 sin ejecutar (behavior-test negativo obligatorio). AC1 vivo/dormido DERIVADO de senal real (mtime de heartbeat/runtime log por agente o proceso), fail-safe a dormido (nunca falso-vivo). AC3 'Enviar al Arquitecto' reusa requirement-intake gobernado + notifica + despierta (AC2) + marca 'tomado'. AC4 activar NO concede autoridad (carry AC17). AC5 error amable (AC72). AC6 #4 byte-id (no tocar protocol.config.json). Entrega in_review con node --test clon limpio exit 0 + gates (validate con/sin secretos, encoding, neutralidad). Commit como Arquitecto con Co-Authored-By el implementador (no forjar)."
context_refs:
  - Area_comun/specs/SPEC-0089-panel-operar-agentes-q1-control-runtime.md
  - Area_comun/tasks/TASK-0166-codex-panel-operar-agentes-q1-control-runtime.md
  - Area_comun/tasks/req-885632826e-requirement-seed.md
  - Area_comun/tasks/req-9442785dd6-requirement-seed.md
deadline_or_blocking_level: normal
---

# GO - TASK-0166: Panel Operar-Agentes Q1 (control de runtime)

Segunda pieza del panel "Operar Agentes" (SPEC-0089), aprobada por el operador (REQ-885632826E + REQ-9442785DD6).
Q2 (consola de prompts) ya cerro; esta pieza agrega el CONTROL de runtime y el despertar-al-destino que Q2 difirio.

## Lo critico
- **AC2 ALLOWLIST** es la barrera de seguridad: el server mapea `agent_id -> runtime conocido` (set cerrado del
  agent_registry); NUNCA ejecuta un comando arbitrario del cliente. El Analista probara con un agent_id arbitrario:
  debe dar 400 sin ejecutar nada. runtime-only (DECISION-0057): no reconfigura identidad/keys/registry, no concede
  capabilities.
- **AC1** vivo/dormido + ultimo latido DERIVADO de senal real, fail-safe a "dormido" (jamas un verde falso).
- **AC3** "Enviar al Arquitecto" en el Intake: requirement-intake gobernado (ya existe) + MSG al Arquitecto + despertar
  su runtime si dormido + el front marca "tomado". Sin push manual.
- **AC4/AC6** no-bypass / no-autoridad / #4 byte-id.

## Gates de entrega
node --test clon limpio exit 0; validate con/sin secretos exit 0; encoding 0; neutralidad 0; #4 byte-identica.
Behavior-tests deterministas (incl. el negativo de allowlist). Entrega a in_review con FYI; yo checker + pasada Analista.
