---
message_id: MSG-20260619-Arquitecto-to-Operador-carril-A-promocion-done
type: FYI
task_id: PROMO-20260619-CARRIL-A
from: Arquitecto
to: Operador
status: open
requires_response: false
response_owner: none
one_line_summary: Promocion Carril A HECHA. v1.10.0 (e56b027). DECISION-0039/0040/0041/0042 + SPEC-0081 + TASK-0117/0118/0119 en el ledger; drift 0; gates verdes; #4 sigue OFF; Codex queda ACTIVO.
requested_action: none
context_refs:
  - Area_comun/mailbox/answered/MSG-20260619-Operador-to-Arquitecto-carril-A-GO-promocion.md
  - Area_comun/mailbox/answered/MSG-20260619-Operador-to-Arquitecto-carril-A-coord-crons.md
---

# Promocion Carril A - HECHA (responde a GO-promocion + coord-crons)

Operador: promocion ejecutada por `submit_intent` (transaccion atomica de 10 intents) + commit/push.

- **Version:** protocol_version + PROJECT_STATE.version **1.9.3 -> 1.10.0** (SemVer MINOR). Entrada CHANGELOG anadida.
- **Decisions:** DECISION-0039 (activacion #4), DECISION-0040 (GATE-DATASET), DECISION-0041 (read-only),
  DECISION-0042 (mailbox claims file-scoped) -> en PROJECT_STATE.decisions.
- **SPEC:** SPEC-0081 (activacion #4) -> Area_comun/specs.
- **Tasks:** TASK-0117 (activacion #4, gateada) / TASK-0118 (DEF-PII, diferida) / TASK-0119 (guard mailbox),
  owner Codex, `proposed`. En TASK_INDEX.
- **Gates:** validador + encoding + neutralidad verdes; **drift 0**. HEAD e56b027 (pusheado).
- **#4 sigue OFF** (chain/agent_signatures/anchor/event_auth en false; off-by-default intacto). El encendido
  es un GO POSTERIOR tras el piloto.
- **Crons:** Codex queda **ACTIVO** (tu orden coord-crons): tiene TASK-0117 (SPEC-0081) + prueba negativa A3
  + TASK-0119 (guard) pendientes. No detuve su cron ni el mio; espero tu/asistente senal de cierre.
- **Pendiente menor (diferido):** reconciliar `agents.architect="Claude"->"Arquitecto"` no es posible por
  submit_intent (solo re-genesis); cosmetico (la capability ya sale de agent_roles). Lo dejo para una
  ventana dedicada si lo quieres.
