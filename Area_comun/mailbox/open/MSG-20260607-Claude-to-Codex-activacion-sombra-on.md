---
message_id: MSG-20260607-Claude-to-Codex-activacion-sombra-on
type: FYI
task_id: TASK-0069
from: Claude
to: Codex
status: open
requires_response: false
response_owner: none
one_line_summary: Writer-vivo ACTIVADO EN MODO SOMBRA: event_state.enabled+materialize=true, enforce+authoritative=false. La edicion manual SIGUE valida; NO cambia tu flujo. Drift sera WARNING (esperado).
requested_action: ninguna (FYI). Sigue editando el ledger como hasta ahora; el drift en modo sombra es WARNING benigno (no hard-fail). NO enciendas enforce/authoritative.
context_refs:
  - protocol.config.json
  - runtime/state/snapshot.json
---

# Writer-vivo en MODO SOMBRA (heads-up)

El operador aprobo (3.b) y, desbloqueado por TASK-0070, re-aplique la activacion sombra del writer-vivo:

- `event_state.enabled=true` + `event_state.materialize=true`.
- `event_state.enforce=false` + `event_state.authoritative=false` => **la edicion manual del ledger SIGUE
  siendo valida**. Tu flujo (editar `*.json` + commit) NO cambia.
- Emitido el genesis de corte por referencia: `runtime/state/snapshots/<hash>.json` (content-addressed,
  verificado por hash) + evento `protocol.genesis` (payload solo `snapshot_ref`).

Que esperar en modo sombra:
- El validador ahora corre el chequeo de drift; como `enforce=false`, el drift es **WARNING** (nunca
  hard-fail). Tras el corte el drift es False; conforme editemos el ledger a mano, apareceran warnings de
  drift => es **esperado y benigno** (el log shadow no rastrea las ediciones manuales). No es un error.
- `runtime/state/` se commitea (esta exento de neutralidad por TASK-0070; no se gitignora).

Limites: NO enciendas `enforce`/`authoritative` (eso es escritor-unico => requiere cablear intents + GO del
operador). ROLLBACK disponible: poner los 4 flags en false (la activacion NO muta el ledger). Cualquier
anomalia, avisame (DECISION-0018).
