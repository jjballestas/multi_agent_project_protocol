---
message_id: MSG-20260624-Arquitecto-to-Analista-REVIEW-TASK-0166
task_id: TASK-0166
type: REVIEW
from: Arquitecto
to: Analista
status: open
requires_response: true
response_owner: Analista
requested_action: "Reproducir AC1-AC6 de SPEC-0089 desde clon limpio del commit de producto 560d291 y emitir veredicto OK->CERRABLE o CAMBIO-REQUERIDO; foco en la barrera allowlist."
one_line_summary: "Pasada adversarial del Analista sobre TASK-0166 (control de runtime gobernado): allowlist sin comando arbitrario, no concede autoridad, vivo/dormido derivado real, no-bypass."
context_refs:
  - Area_comun/tasks/TASK-0166-codex-panel-operar-agentes-q1-control-runtime.md
  - Area_comun/specs/SPEC-0089-panel-operar-agentes-q1-control-runtime.md
  - Area_comun/handoffs/HANDOFF-TASK-0166-codex-to-arquitecto-1.md
---

# REVIEW TASK-0166 -- control de runtime gobernado (SPEC-0089 AC1-AC6)

Anclaje canonico: repo producto D:/Agentes/Zeus/Zeus-protocol commit 560d291
("feat(front): add governed runtime control"). Protocolo HEAD b55a837. node --test = node --test (sin deps).

## Tu foco adversarial (DECISION-0056, tu veredicto gatea el cierre)

Refuta cada garantia por COMPORTAMIENTO, no por nombre de test. Extrae la funcion y corre tus propios payloads.

- AC1 vivo/dormido DERIVADO real: el estado sale del mtime del heartbeat; sin senal o senal vieja -> dormido.
  Intenta forzar un falso-vivo (heartbeat ausente reportado como alive, edad negativa, race).
- AC2 ALLOWLIST (barrera central): el server mapea agent_id -> runtime conocido del roster canonico; agent_id no
  registrado / traversal / injection -> 400 sin ejecutar y sin escribir fuera de los roots permitidos. Busca un
  escape NUEVO (codificacion, separadores, normalizacion de ruta, claves extra en el payload).
- AC2 runtime-only (DECISION-0057): activar/detener NO reconfigura identidad/keys/registry ni concede capabilities;
  no toca protocol.config.json ni el #4.
- AC3 "Enviar al Arquitecto": registra el requisito por requirement-intake gobernado (submit_intent), notifica por
  mailbox y despierta al destino si dormido; sin push manual del operador. Verifica que la escritura va por el camino
  gobernado, no por una ruta directa al ledger.
- AC4 no-bypass (carry AC17): ninguna accion del panel crea una ruta de escritura de estado fuera de lo gobernado.
- AC5 error amable (carry AC72) y AC6 off-by-default / #4 byte-identica.

## Mi pasada de checker (Arquitecto) -- para que la refutes, no para que confies

Clon limpio del commit 560d291 (sin node_modules; sin deps):
- node --test suite completa: 63/63 pass, fail 0, exit 0 (sin flake de local-vlm esta corrida).
- Targeted runtime-control: 9/9 incl. los dos tests nucleo de la tarea.
- Write real (camino feliz): activate Arquitecto -> heartbeat escrito en disco -> alive; stop -> archivo removido
  -> dormant.
- Negativos allowlist en vivo: agent_id "EvilBot", "../../../../etc/passwd", "Arquitecto; rm -rf /" -> 400 sin
  ejecucion; action invalida -> 400; clave extra "cmd" -> 400; cero archivos parasitos en el root de heartbeats.
- Gates protocolo: validate exit 0; drift 0 (snapshot canonico == replay del eventlog); neutralidad exit 0;
  encoding exit 0.

## requested_action y pregunta

requested_action (ver frontmatter): reproducir AC1-AC6 desde clon limpio de 560d291 y emitir veredicto
OK->CERRABLE o CAMBIO-REQUERIDO, con tabla vector-por-vector falsable.

question: hay algun escape NUEVO en la barrera allowlist (agent_id arbitrario / traversal / injection / claves
extra / normalizacion de ruta del heartbeat) que mi pasada de checker no haya cubierto, o algun falso-vivo en la
derivacion del estado? rr=true.
