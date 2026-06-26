---
spec_id: SPEC-0103
task_id: TASK-0190
type: security
status: accepted
linked_decisions:
  - DECISION-0065
  - DECISION-0039
  - DECISION-0046
  - DECISION-0029
created_at: 2026-06-27
updated_at: 2026-06-27
author: Arquitecto
---

# SPEC-0103 - submit_intent firma actor_auth Ed25519 (A2 vivo, Camino B), off-by-default

## Context

DECISION-0065 (accepted): cablear la firma Ed25519 por agente al camino de escritura real (`submit_intent`) para
que el dataset del TFM lleve A2 no-repudiable. Off-by-default; activacion = ventana de riesgo aparte. NO toca
genesis/#4/config pinned. Repo = core (`runtime/`). maker=Codex / checker=Arquitecto. Checker desde clon limpio
CON y SIN secretos.

## Scope

- **`runtime/submit_intent.py` + `runtime/eventlog.py`:** cuando el flag de actor-auth este ON, `append_event`
  recibe un `actor_auth = {method:"ed25519", keyid, sig}` firmado con la **privada Ed25519 del actor** (cargada de
  `protocol-secrets`, path-safe, fail-closed). Reusar la primitiva de firma existente (`llm_turn_wrapper`/`sign`
  Ed25519) o `attestation_signing_payload`; NO duplicar cripto.
- **Flag** `event_state.actor_auth_enforce` (o equivalente) **OFF** por defecto en el config pinned.
- **Verificacion** (validate/replay): aceptar eventos `not_enforced_phase2` (previos) y `ed25519` (nuevos);
  verificar Ed25519 con la **publica** de `signature_config.public_keys`; rechazar firma invalida / keyid no
  registrado / atribucion cruzada.
- **Golden** `examples/actor_auth_ed25519_cases` + CI.

## Acceptance Criteria

- **AC1 (firma viva):** con el flag ON y la privada disponible, un evento emitido por `submit_intent --actor-id X`
  lleva `actor_auth={method:"ed25519", keyid:X, sig}` **verificable con la publica de X**. Behavior-test.
- **AC2 (off-by-default, OFF byte-identico):** sin el flag, el evento lleva `actor_auth:"not_enforced_phase2"` y el
  comportamiento es **byte-identico al actual** (HMAC `event_auth` intacto). El flag esta OFF en el config
  versionado; no se commitea ON. Test de no-regresion del camino OFF.
- **AC3 (no-repudio / atribucion cruzada RECHAZADA, prueba negativa PERMANENTE):** un evento atribuido a otro agente
  sin su privada (firma forjada / keyid ajeno / sig que no verifica con la publica del actor declarado) es
  **rechazado** por validate/replay. Vectores fijos, golden por vector.
- **AC4 (secret-independiente, DECISION-0046):** clon limpio SOLO con publicas -> `validate` exit 0 y mismo
  veredicto/hash (verifica sin secretos); FIRMAR sin la privada **falla-closed** (no escribe evento). El hash
  canonico no depende de secretos.
- **AC5 (ledger vivo intacto):** replay acepta los eventos previos (`not_enforced_phase2`) y los nuevos
  (`ed25519`); **drift 0**; chain/anchor/HMAC siguen verdes; `genesis = canonical_hash(config)` intacto;
  `protocol.config.json` (epoca 1.14.0) sin cambio.
- **AC6 (gates):** `validate_collaboration_state.py` exit 0 (con y sin secretos) desde clon limpio; golden
  `examples/actor_auth_ed25519_cases` en CI; `scan_encoding`/`scan_domain_neutrality` exit 0; Co-Authored-By Codex.

## Out of scope

- real_invoker / supervised_autonomy / Camino A (orquestador). La ACTIVACION viva (flip del flag) = ventana del
  operador, no esta tarea. Tocar `append_agent_attestation` existente. Generar/medir el dataset.

## Notes

- El BUILD es off-by-default: no enciende nada en el vivo. El checker (Arquitecto) verifica especialmente que el
  camino OFF queda byte-identico (no romper el ledger que usan todos los agentes) y que el camino ON firma+verifica
  + rechaza atribucion cruzada + es secret-independiente. Reusar cripto existente; no introducir secretos al repo.
