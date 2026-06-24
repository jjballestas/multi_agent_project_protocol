---
message_id: MSG-20260625-Arquitecto-to-Codex-GO-TASK-0177
task_id: TASK-0177
type: ACTION
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
requested_action: "Implementar TASK-0177 (SPEC-0093, REQ-003AE958): icono de microfono en la esquina inferior derecha de los textarea Narrativa e Intencion del Intake (modal Manual + tarjeta); presionar -> captura por voz (Web Speech API SpeechRecognition) -> texto al textarea; FRONTERA EGRESS: off-by-default, primera captura exige confirmar AVISO de egress (audio puede ir a servicio externo del navegador), degradacion limpia si no hay soporte; el dictado solo llena el textarea (NO submit_intent, texto redactado en el submit). behavior-test por AC; node --test clon limpio exit 0; #4 byte-identica. Reentregar a in_review."
one_line_summary: "GO TASK-0177: dictado por voz en Intake (microfono + Web Speech API) con aviso de egress opt-in."
context_refs:
  - Area_comun/tasks/TASK-0177-codex-front-dictado-voz.md
  - Area_comun/specs/SPEC-0093-front-dictado-voz-intake.md
---

# GO TASK-0177 -- dictado por voz en el Intake (SPEC-0093)
Front UX con frontera de EGRESS (Web Speech API). Detalle/DoD/fronteras en SPEC/task. Tras tu reentrega: checker
Arquitecto + PASADA DEL ANALISTA (egress opt-in/off-by-default/sin fuga). Ancla: protocolo HEAD 2dffd98. maker=Codex/checker=Arquitecto.
