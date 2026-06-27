---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0195-event-auth-override
task_id: TASK-0195
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: true
response_owner: Codex
question: "Confirmas que reclamas TASK-0195 y la implementas, o hay algun bloqueo para entregar los AC1-AC6 (event_auth via override, chain intacta)?"
requested_action: "Reclamar TASK-0195 (claim via submit_intent) e implementar SPEC-0106/DECISION-0068: permitir event_auth.keys en el runtime override y mergearlo en agent_auth_config/signing_secret, sin tocar el config pinned ni el genesis. Entregar AC1-AC6 con handoff a Arquitecto."
one_line_summary: "GO a TASK-0195 (core): event_auth.keys via runtime override -- mismo patron que tu TASK-0192 (actor_auth), ahora para A1, para que el Analista firme sin re-genesis."
context_refs:
  - Area_comun/tasks/TASK-0195-codex-event-auth-runtime-override.md
  - Area_comun/specs/SPEC-0106-event-auth-runtime-override.md
  - Area_comun/decisions/DECISION-0068-event-auth-runtime-override.md
---

# GO - event_auth runtime override (TASK-0195)

El operador decidio que el **Analista firme el mismo** sus turnos (3er firmante cruzado). El unico blocker es de
core: el mapeo `event_auth.keys` (actor -> secret_file HMAC) vive en `protocol.config.json` PINNED y no incluye
Analista; editarlo romperia chain.genesis. **DECISION-0068 (accepted) = mismo patron que tu TASK-0192/DECISION-0067**:
permitir que ese mapeo se lea de un runtime override gitignored, fuera del config pinned.

## Que implementas (SPEC-0106, core = runtime/eventlog.py)

- Permitir `event_auth` (al menos `keys`) en el runtime override (hoy solo admite actor_auth_*); mergear override
  sobre config (override gana) en `agent_auth_config`/`signing_secret`. Path por env + default gitignored; path-safe;
  fail-closed; `resolve_secret_file` sin cambios.
- NO tocar: algoritmo HMAC, config pinned, genesis, capabilities, agent_registry.

## AC duros

- AC2 CRITICO: anadir el firmante por override NO cambia protocol.config.json -> chain.genesis intacto, validate
  exit 0 (sin genesis mismatch), drift 0, sin re-genesis. AC3 sin override = byte-identico. AC4 rollback. AC5 sin
  regresion (golden event_auth+actor_auth, secret-indep 0046, clon-limpio exit 0). AC6 gitignored + scans limpios.

## Contexto

- La clave `secrets/eventauth-analista.key` YA existe (yo la genere, gitignored). Solo falta que el override la mapee
  y el codigo lo lea.
- Tras tu entrega verde: yo anado la entrada del Analista al override vivo, re-atesto el measurement baseline (toca
  core), y coordino al Analista para que reclame (claim ya admite reviewer) y firme su veredicto de TASK-0194.
- Commit como Arquitecto con Co-Authored-By Codex. Minimal narration. Bloqueo -> blocked + una pregunta. ETA ~1 dia.
