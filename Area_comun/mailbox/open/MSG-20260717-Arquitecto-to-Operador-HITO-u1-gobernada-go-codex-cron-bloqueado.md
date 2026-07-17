---
message_id: MSG-20260717-Arquitecto-to-Operador-HITO-u1-gobernada-go-codex-cron-bloqueado
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Operador-to-Arquitecto-RESP-ack-plan-f1-y-anomalia-trailer.md
one_line_summary: "HITO U1: TASK-0001 gobernada READY en el ledger de Nova-Payroll + GO a Codex commiteado (local c9a3555, gates 0/0/0). Carril: cron Analista (reviewer) VIVO; cron Codex (implementer) BLOQUEADO por el classifier del harness -> necesito que corras TU la linea exacta (abajo) o autorices el relanzamiento. Sin eso, U1 tiene maker registrado pero sin runtime."
requested_action: "Correr en PowerShell (o autorizar en settings del harness y avisarme): powershell -NoProfile -File D:\\Agentes\\NOVA-Suite\\Nova-Payroll\\Aegis\\scripts\\harness\\peer_mailbox_cron.ps1 -PeerId Codex -Root D:\\Agentes\\NOVA-Suite\\Nova-Payroll\\Aegis -PromptFile D:\\Agentes\\NOVA-Suite\\Nova-Payroll\\Aegis\\scripts\\harness\\prompts\\implementer.prompt.md"
question: "Corres tu la linea del cron Codex de Nova-Payroll o me autorizas el relanzamiento (regla de permiso) para que lo haga yo?"
---

# HITO - U1 gobernada + GO; carril a medio activar (cron Codex bloqueado)

## Hecho (Nova-Payroll, commit local c9a3555; sin remoto por orden)
- TASK-0001 [F1-U1] registrada con intake DoR completo y promovida a READY (submit_intent seq 2-5,
  claim setup adquirido y liberado; validate/encoding/neutralidad = 0/0/0).
- GO a Codex en su mailbox (intake autocontenido: DDL v1 15 tablas + indexador read-only port del
  memdb de Zeus-protocol-Aegis con diff documentado + mapeo s.5.1b tal cual + I9 cero-inferencias +
  PII NEG de nomina + .gitignore/scan). Fix menor de nacimiento: .ledger.lock estaba tracked ->
  untracked + gitignored (gap del export a anotar en 0096).
- Cron ANALISTA (reviewer) de la instancia: VIVO (pid nuevo, heartbeat 03:07, effort medium).

## Bloqueo (necesito accion tuya)
El classifier del harness DENEGO lanzar el cron CODEX (implementer) de la instancia -- si permitio
el del Analista (mismo comando, otro PeerId). Por regla no rodeo el deny: te paso la linea exacta
(requested_action). Opciones: (a) la corres tu; (b) autorizas la regla de permiso y me avisas para
lanzarlo yo. En cuanto el cron viva, Codex tomara el GO de la cola automaticamente.

## Siguiente
Al arrancar Codex: monitor read-only sobre la instancia armado; veredicto del Analista tras la
entrega; mail de hito al in_review y al done de U1. U2 se registra al ratificar U1.

-- Arquitecto. Hora local 05:10 (UTC+2). Fondo: N=500, 2E35F26E, 1.14.0 intactos.
