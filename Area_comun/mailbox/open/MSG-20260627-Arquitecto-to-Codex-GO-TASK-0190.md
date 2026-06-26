---
message_id: MSG-20260627-Arquitecto-to-Codex-GO-TASK-0190
task_id: TASK-0190
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
requested_action: "GO a TASK-0190 (core: submit_intent firma actor_auth Ed25519, Camino B del cutover A2, off-by-default; ready). DECISION-0065 accepted. Reclamala -> in_progress y entrega a in_review cuando este verde. Repo = PROTOCOLO core (runtime/). CONSTRUIR OFF-BY-DEFAULT: con flag event_state.actor_auth_enforce ON, submit_intent firma actor_auth={method:ed25519,keyid,sig} con la privada Ed25519 del --actor-id (de D:/Agentes/protocol-secrets, path-safe, fail-closed; reusar la cripto existente de llm_turn_wrapper/attestation, sin duplicar ni meter secretos al repo). Flag OFF en el config versionado. validate/replay: aceptar not_enforced_phase2 (previos) + ed25519 (nuevos), verificar con la publica, RECHAZAR atribucion cruzada (prueba negativa permanente). CUIDADO MAXIMO: el camino OFF lo usan TODOS los agentes; debe quedar byte-identico (un bug ahi rompe el ledger vivo). NO tocar genesis/#4/config pinned; la activacion viva (flip) NO es esta tarea. DoD = SPEC-0103 AC1-AC6; correr validate con y sin secretos en clon limpio. maker=Codex / checker=Arquitecto. rr=false."
one_line_summary: "GO TASK-0190: submit_intent firma actor_auth Ed25519 (A2 vivo Camino B), off-by-default, camino OFF byte-identico, prueba negativa atribucion-cruzada, secret-indep."
context_refs:
  - Area_comun/decisions/DECISION-0065-actor-auth-ed25519-submit-intent.md
  - Area_comun/specs/SPEC-0103-actor-auth-ed25519-submit-intent.md
  - Area_comun/tasks/TASK-0190-codex-actor-auth-ed25519-submit-intent.md
---

# GO -- TASK-0190 (submit_intent firma actor_auth Ed25519, Camino B)

DECISION-0065 accepted (operador eligio Camino B). Cablear la firma Ed25519 por agente al camino de escritura real,
**off-by-default**. Repo = **protocolo core** (`runtime/`). Anclaje: SPEC-0103 AC1-AC6.

Construir:
- Con flag `event_state.actor_auth_enforce` ON: `submit_intent` firma `actor_auth={method:"ed25519",keyid,sig}` con
  la privada Ed25519 del `--actor-id` (de `protocol-secrets`, path-safe, fail-closed). Reusar la cripto existente
  (`llm_turn_wrapper`/`attestation_signing_payload`); cero secretos al repo.
- Flag **OFF** por defecto en el config versionado.
- validate/replay: acepta `not_enforced_phase2` (previos) + `ed25519` (nuevos); verifica con la **publica**;
  **RECHAZA atribucion cruzada** (prueba negativa permanente, vectores + golden).
- Golden `examples/actor_auth_ed25519_cases` + CI.

Invariantes (condicion de cierre):
- **Camino OFF byte-identico** al actual (lo usan todos los agentes; un bug rompe el ledger vivo). Test no-regresion.
- **Secret-independiente** (DECISION-0046): clon limpio solo-publicas valida exit 0; firmar sin la privada
  falla-closed.
- **NO** tocar genesis/#4/config pinned; `genesis = canonical_hash(config)` intacto; drift 0.
- La **activacion viva (flip del flag) NO es esta tarea** (es ventana del operador).

Gates: validate exit 0 **con y sin secretos** en clon limpio; golden en CI; encoding/neutralidad exit 0; Co-Author.
Entrega a in_review; yo re-checo clon limpio (`git -c core.longpaths=true`), verificando OFF byte-identico + ON
firma/verifica/rechaza-cruzada/secret-indep. rr=false.
