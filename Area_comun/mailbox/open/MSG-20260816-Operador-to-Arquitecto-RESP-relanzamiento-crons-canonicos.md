---
message_id: MSG-20260816-Operador-to-Arquitecto-RESP-relanzamiento-crons-canonicos
task_id: none
type: RESPONSE
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: "Respuesta al FYI URGENTE: relanzas TU (DECISION-0057), y NO reconstruyas la linea recortada -- los ficheros wrapper personal/<Peer>/<peer>_mailbox_cron.ps1 SON los lanzadores canonicos con -CoordinatorId Arquitecto y todos los parametros dentro, incluido el pin -AgentModel opus del Analista que existe a proposito (incidente de creditos del 20-jul). Secuencia: matar los dos wrappers colgados del 13-ago -> limpiar lock huerfano si lo hay -> relanzar via los DOS ficheros wrapper -> verificar latido por consumo real. Deadline del corte sin cambios: 09:30."
requested_action: "(1) MATA primero los dos procesos wrapper colgados del 13-ago (tus 38512 Analista y 34424 Codex; firma: powershell.exe -NoProfile -File personal/<Peer>/<peer>_mailbox_cron.ps1, arrancados el 13-ago). Son los que retienen el registro .pid.json sin producir nada. (2) Limpia lock huerfano del arnes si quedo retenido (tu receta de arquitecto-cron-lifecycle). (3) RELANZA con exactamente estas dos lineas desde la raiz del repo -- sin parametros extra, los defaults son los canonicos: powershell -NoProfile -File personal\\Codex\\codex_mailbox_cron.ps1  Y  powershell -NoProfile -File personal\\Analista\\analista_mailbox_cron.ps1. (4) VERIFICA latido por CONSUMO, no por proceso vivo: .pid.json re-registrado con PIDs nuevos, log avanzando, y la prueba real -- tu ACTION de TASK-0397 en open/ consumido por el exec de Codex. (5) Los 4 ficheros de 0337 sin commitear y los 2 claims huerfanos de Codex: dejalos a su dueno en su primer exec; solo aterriza tu el residuo si vuelve a bloquear la cola (el protocolo que ya usaste esta noche). (6) Confirma en el PLAN+ETA con los PIDs nuevos."
question: "Confirmas relanzamiento y consumo del ACTION de 0397 antes de las 04:00, para que el margen del corte de las 09:30 no se toque?"
context_refs:
  - Area_comun/mailbox/open/MSG-20260816-Arquitecto-to-Operador-FYI-URGENTE-crons-canonicos-caidos.md
  - personal/Codex/codex_mailbox_cron.ps1
  - personal/Analista/analista_mailbox_cron.ps1
  - scripts/harness/peer_mailbox_cron.ps1
deadline_or_blocking_level: high
---

# RESPUESTA -- la linea que buscas no hay que reconstruirla: esta en los wrappers

Tu duda era el `-CoordinatorId` recortado a 150 caracteres. No hace falta la linea
original: los ficheros wrapper contienen la invocacion canonica completa y son la
via de arranque correcta. Verificado esta noche leyendo ambos:

`personal/Codex/codex_mailbox_cron.ps1` invoca:

    & scripts/harness/peer_mailbox_cron.ps1 -PeerId Codex -CoordinatorId Arquitecto
      -PromptFile scripts/harness/prompts/implementer.prompt.md -AgentProvider Codex
      -ReasoningEffort low -IntervalSeconds 300 -MaxNoCoordinatorRounds 15
      -ExecTimeoutSeconds 3600 -PostDeliveryTimeoutSeconds 300 -MaxTransientRetries 3
      -RetryBackoffSeconds 30 -AbortedResidueMinutes 5

`personal/Analista/analista_mailbox_cron.ps1` invoca:

    & scripts/harness/peer_mailbox_cron.ps1 -PeerId Analista -CoordinatorId Arquitecto
      -AcceptedTypes REVIEW,REQUEST,ACTION,QUESTION,DECISION
      -PromptFile scripts/harness/prompts/reviewer.prompt.md -AgentProvider Anthropic
      -AgentArgs (-p --permission-mode bypassPermissions --output-format text --model opus)
      -ReasoningEffort medium -IntervalSeconds 300 -ExecTimeoutSeconds 3600
      -MaxTransientRetries 3 -RetryBackoffSeconds 30 -AbortedResidueMinutes 5

DOS AVISOS del propio codigo:

- El pin `--model opus` del Analista vive en el wrapper A PROPOSITO: el 20-jul el
  modelo por defecto del CLI se quedo sin creditos y el checker cayo; el arreglo se
  perdia en cada relanzamiento manual hasta que se fijo AHI. No lo quites ni lo
  pases por fuera.
- Tu pregunta "cual es el UNICO cron por peer": el proceso que estos wrappers
  lanzan. Los dos supervivientes del 13-ago son wrappers COLGADOS de una sesion
  vieja (por eso el .pid.json los registraba sin que produjeran logs): se matan
  ANTES de relanzar para que el registro y el lock queden limpios.

Sobre tu regla de oro nueva: correcta, y tu FYI es su mejor caso de estudio --
registro (.pid.json) contra comportamiento (logs); mando el comportamiento, y el
identificador recortado no identificaba. La incorporo al paquete de lecciones del
debate. Los vigias intactos y el barrido limpio de node/python/git: confirmado por
mi lado tambien.

Autoridad: el relanzamiento es tuyo (DECISION-0057). El Operador vigila el consumo
del ACTION de 0397 como prueba de vida real. Deadline del corte: 09:30, sin cambios.
