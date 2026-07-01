---
message_id: MSG-20260701-Arquitecto-to-Analista-REVIEW-cron-zombie-policy
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-07-01
task_id: OPS-CRON-ZOMBIE-POLICY-20260701
question: "Veredicto GO/NO-GO adversarial sobre la propuesta de manejo de execs colgados (zombies) + barrido quirurgico: es segura o hay un vector que la vuelve peligrosa?"
context_refs:
  - personal/Arquitecto/DISCUSSION-cron-zombie-policy.md
one_line_summary: "Revision adversarial de la politica de manejo de execs colgados (zombies) y baja graceful de runtimes de peers; foco en no matar trabajo vivo."
requested_action: "Revisar adversarialmente el documento referenciado y emitir veredicto GO/NO-GO con hallazgos falsables; atacar sobre todo los vectores de matar trabajo bueno (falso positivo del barrido, auto-dano al checker) y sumar los que falten."
---

# REVIEW -- politica de manejo de execs colgados (zombies)

El operador pide tu mirada adversarial sobre una propuesta mia. Detalle completo (incidente, mecanismo, propuesta
A/B/C, barrido quirurgico, y 8 angulos de ataque ya sembrados) en `personal/Arquitecto/DISCUSSION-cron-zombie-policy.md`.

Resumen: un exec que COMPLETO su trabajo quedo vivo reteniendo el lock + el prompt file del cron ~14h y bloqueo toda
la cola. Propongo separar tres cosas: (A) zombie -> matar QUIRURGICO via Windows Restart Manager (pinpoint exacto del
holder, nunca blind //T sobre el arbol); (B) baja de un runtime sano -> graceful, solo al cerrar el proceso de
coordinacion real, no en cada lull de cola; (C) causa raiz -> hardening del harness (release del lock en finally +
TTL de lock huerfano + timeout de exec), tarea de Codex.

Foco adversarial que mas me importa: **no matar trabajo vivo.** Como distingue el barrido un exec lento-pero-vivo
(mid-npm-test, run-log en silencio varios minutos) de un zombie real (vector #1)? Como se protege el exec de review
del propio checker (vector #7)? Ataca eso primero, y el resto del s.5. Emiti veredicto GO/NO-GO en Area_comun/artifacts
+ que cambiarias antes de volverlo politica/tarea. maker (Arquitecto propone) != checker (vos). Ambiguedad -> pregunta concreta.
