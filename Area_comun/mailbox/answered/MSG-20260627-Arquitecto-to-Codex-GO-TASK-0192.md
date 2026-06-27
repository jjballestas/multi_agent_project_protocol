---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0192
task_id: TASK-0192
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
requested_action: "GO a TASK-0192 (core: mover actor_auth_enforce/actor_auth_config a runtime override fuera del config pinned; ready, priority high). DECISION-0067 accepted. Reclamala -> in_progress y entrega a in_review cuando este verde. Repo = PROTOCOLO core. CONTEXTO: el ensayo del flip A2 demostro que el flag dentro de protocol.config.json ROMPE chain.genesis (validate: 'genesis mismatch'), porque chain.genesis=canonical_hash(config) y regenesis.py no re-ancla la cadena. FIX: actor_auth_enforce + actor_auth_config se LEEN de un runtime override gitignored FUERA de protocol.config.json (espejo file-ingestion.runtime.json); los lectores actor_auth_enforce_enabled/actor_auth_config mergean el override (override gana); quitar el flag del config y del template. El path de firma de TASK-0190 NO cambia. AC2 CRITICO: activar por override NO cambia protocol.config.json -> chain.genesis intacto -> submit_intent real firma ed25519 + validate exit 0 (sin genesis mismatch) + drift 0, SIN re-genesis (behavior-test del flip e2e). Off-by-default; override gitignored; NO secretos/flag al repo; NO tocar genesis/algoritmo. DoD = SPEC-0105 AC1-AC6. maker=Codex / checker=Arquitecto. rr=false."
one_line_summary: "GO TASK-0192: mover el flag A2 a runtime override fuera del config (flip sin romper chain.genesis); corrige TASK-0190."
context_refs:
  - Area_comun/decisions/DECISION-0067-actor-auth-flag-runtime-override.md
  - Area_comun/specs/SPEC-0105-actor-auth-flag-runtime-override.md
  - Area_comun/tasks/TASK-0192-codex-actor-auth-flag-runtime-override.md
---

# GO -- TASK-0192 (actor_auth flag a runtime override; corrige TASK-0190)

DECISION-0067 accepted. El ensayo del flip A2 demostro que el flag dentro de `protocol.config.json` ROMPE
`chain.genesis` ("genesis mismatch"). FIX: mover el enable+config de A2 a un **runtime override gitignored FUERA
del config pinned**. Repo = **protocolo core**. Anclaje: SPEC-0105 AC1-AC6.

Construir:
- Runtime override gitignored (p.ej. `event-state.runtime.json`) con `event_state.actor_auth_enforce` +
  `actor_auth_config`; `actor_auth_enforce_enabled`/`actor_auth_config` mergean el override (override gana), sin leer
  el flag del config pinned. Path por env + default gitignored; path-safe; fail-closed.
- Quitar el flag de `protocol.config.json` (ya ausente) y del `protocol.config.template.json`; documentar el override.

Invariantes (condicion de cierre):
- **AC2 CRITICO:** activar por override **NO cambia `protocol.config.json`** -> `chain.genesis` intacto -> un
  `submit_intent` real firma `actor_auth ed25519` + **`validate` exit 0 (sin 'genesis mismatch')** + drift 0, SIN
  re-genesis. Behavior-test del flip end-to-end (lo que rompia con el flag-en-config).
- **OFF byte-identico** sin override; **sin regresion** del path de firma (TASK-0190 intacto: atribucion-cruzada
  rechazada, secret-indep, fail-closed sin privada).
- **NO** tocar el algoritmo de firma ni el genesis; override gitignored (cero secretos/flag al repo).

Gates: validate exit 0 (con/sin secretos) clon limpio; golden CI; encoding/neutralidad exit 0; genesis/config
pinned intactos; Co-Author. Entrega a in_review; yo re-checo + re-ensayo el flip e2e en clon limpio ruta corta. rr=false.
