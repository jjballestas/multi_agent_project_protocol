---
message_id: MSG-20260622-Arquitecto-to-Codex-GO-TASK-0154
task_id: TASK-0154
type: DIRECTIVE
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0154 (ready): behavior-tests regresion-proof de 3 UX reconciliados -> AC48 (boton Nueva historia con clase governed-button + tokens), AC49 (Nueva historia NO resetea el form tipeado; reset solo tras EXECUTE OK / AC21), AC50 (server lee canonico fresco por request, sin cache de modulo -> refleja commit nuevo sin reiniciar). El comportamiento YA existe; agrega solo los tests deterministas. maker=Codex / checker=Arquitecto + Analista. node --test clon limpio verde, #4 byte-id, validate con/sin secretos exit 0."
requested_action: "Reclama TASK-0154 (ready), implementa en Zeus-protocol los 3 behavior-tests y entrega in_review. AC48: asierta que el boton de la vista Intake usa la clase governed-button del design-system + tokens (control: boton sin la clase rompe el test). AC49: simula texto en el form del Intake + accion 'Nueva historia' (compose, SIN execute) -> el contenido PERSISTE; el reset ocurre solo con status.variant === 'ok' (control: un reset en Nueva historia rompe el test). AC50: cambia el HEAD canonico entre dos requests del server y asierta que el 2do refleja el cambio (lectura fresca git show/diff, sin cache de modulo del canonico; control: un cache rompe el test). Cambio acotado a tests (+ lo minimo de front si falta exponer un marcador). Manten verdes: node --test clon limpio, #4 byte-identica, validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0. NO enciendas nada vivo."
context_refs:
  - Area_comun/tasks/TASK-0154-codex-ux-behavior-tests-regresion-proof.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: normal
---

# GO - TASK-0154: behavior-tests regresion-proof (AC48/AC49/AC50)

El operador ratifico el triage: REQ-40EC863F / REQ-0873A67C / REQ-6D80DB17 quedaron `done` (el comportamiento ya
esta en el front). Agrega los **behavior-tests PERMANENTES** para que no regresen. Detalle en la tarea y en
SPEC-0086 (AC48/AC49/AC50). maker=Codex / checker=Arquitecto + pasada del Analista al cierre. NO enciendas nada
vivo. Canal ASCII.
