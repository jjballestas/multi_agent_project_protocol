---
message_id: MSG-20260619-Arquitecto-to-Operador-carril-A-GO-encendido-ack
task_id: TASK-0117
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: false
response_owner: none
one_line_summary: GO de encendido recibido. Fase 1 en marcha: Codex provisiona + corre el PILOTO (AC2 N=20/AC3/AC5 rollback); yo verifico maker!=checker y hago el flip permanente de #4 contigo presente solo si VERDE. Dependencia: anchor remoto real (AC1).
requested_action: none
context_refs:
  - Area_comun/mailbox/open/MSG-20260619-Arquitecto-to-Codex-carril-A-GO-encendido-fase1.md
---

# Ack GO encendido #4 + plan Fase 1

Operador: recibido. Mantengo Codex y mi cron activos. Ejecuto Fase 1 con la secuencia de menor riesgo:

1. **Codex provisiona** (AC1): su Ed25519 publica + `event_auth.keys` + anchor remoto/proof real; privadas
   FUERA del repo.
2. **Codex corre el PILOTO** en ventana acotada (enciende temporal, mide, **rollback ensayado**): AC2
   manipulation-check N=20 >=99% (denominador del event log), AC3 6 vectores, AC5 rollback byte-equivalente.
3. **Yo verifico** el piloto maker!=checker (reproduzco AC2/AC3/AC5 + sin secretos en repo) y, **contigo
   presente**, hago el **flip PERMANENTE** de #4 (chain+agent_signatures+anchor+event_auth) + SemVer MINOR +
   CHANGELOG + cierro TASK-0117. **Solo si el piloto sale VERDE.** Si no, no enciendo, diagnostico y reporto.

**Una dependencia externa real (te la flag):** AC1 exige un **anchor remoto/proof REAL**
(`anchor_config.remote_url`). Necesito un target independiente (remoto git aparte / branch de auditoria /
bare repo local). Le pedi a Codex que proponga uno o reporte blocked; si prefieres un target concreto,
dimelo. Sin eso, el primer anclaje falla y el piloto no puede salir 100% verde.

**Limites:** no enciendo nada mas alla de #4; no combino con SA.4/authoritative-teeth/subagents/Capa C;
DEF-PII (TASK-0118) sigue diferida; la DB de Budget no se toca (corte limpio); s.9 read-only del satelite
intacto. Reporto al cerrar Fase 1 (piloto, #4 ON?, version, drift 0). Luego Fase 2 (Carril B) y Fase 3
(primer handoff = T0).
