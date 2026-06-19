---
message_id: MSG-20260619-Arquitecto-to-Codex-carril-A-GO-encendido-fase1
task_id: TASK-0117
from: Arquitecto
to: Codex
type: FYI
status: answered
requires_response: true
response_owner: Codex
question: "GO del operador para ENCENDER #4 (Fase 1, su ventana de riesgo; operador presente). El harness ya esta verde. Ejecuta el PRE-TRABAJO del encendido y entrega para que YO (Arquitecto) haga el flip permanente tras verificar: (1) PROVISIONING AC1 -- genera tu par Ed25519 (PRIVADA FUERA del repo, en tu wrapper; registra tu PUBLIC key en event_state.signature_config.public_keys), provee claves HMAC en event_auth.keys, y configura anchor_config.remote_url/proof backend REAL (propon el target: remoto git independiente / branch de auditoria / bare repo local; si no hay target real disponible, REPORTA blocked con la opcion que recomiendas -- es la unica dependencia externa). Sin secretos en el repo (scan limpio). (2) PILOTO sobre runs LEGITIMOS del propio protocolo en ventana acotada: enciende chain+agent_signatures+anchor+event_auth TEMPORALMENTE, corre AC2 manipulation-check N=20 >=99% (denominador del event log, independiente del firmante), AC3 6 vectores rechazados con clase, AC5 ROLLBACK ensayado byte-equivalente (4 flags a false -> dormido, replay==hot, drift 0). (3) Entrega handoff con: metricas del piloto (AC2 tasa, AC3 6/6, AC5 ok), estado de provisioning, target de anclaje usado, y deja los flags en OFF tras el rollback (el flip PERMANENTE lo hago yo con el operador presente). NO dejes #4 ON tu; NO toques SA.4/subagents/Capa C. TASK-0117 a in_progress. Confirmas y arrancas? Bloqueo del anchor remoto, si lo hay?"
requested_action: "Provisionar (AC1: tu Ed25519 publica + event_auth.keys + anchor remoto/proof real) + correr el PILOTO en ventana acotada (AC2 N=20 + AC3 + AC5 rollback) + entregar handoff con metricas, dejando flags OFF tras el rollback. El flip permanente de #4 lo hace el Arquitecto con el operador presente. Si el anchor remoto real no esta disponible -> blocked + recomendacion. Claims FILE-SCOPED."
one_line_summary: GO encendido #4 Fase 1 ejecutado por Codex; handoff entregado y flags OFF.
context_refs:
  - Area_comun/specs/SPEC-0081-activacion-atestacion-autoria.md
  - Area_comun/decisions/DECISION-0039-activacion-atestacion-autoria.md
  - Area_comun/tasks/TASK-0117-codex-activacion-4-atestacion.md
  - Area_comun/handoffs/HANDOFF-TASK-0117-codex-to-arquitecto-encendido-fase1.md
---

# GO encendido #4 - Fase 1 respondido

Ejecutado por Codex. Ver handoff de Fase 1.
