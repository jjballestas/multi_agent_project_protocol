---
spec_id: SPEC-0105
task_id: TASK-0192
type: security
status: accepted
linked_decisions:
  - DECISION-0067
  - DECISION-0065
  - DECISION-0047
  - DECISION-0046
created_at: 2026-06-27
updated_at: 2026-06-27
author: Arquitecto
---

# SPEC-0105 - actor_auth_enforce/actor_auth_config a runtime override (corrige TASK-0190)

## Context

DECISION-0067: el flag A2 debe vivir en un runtime override FUERA de `protocol.config.json` (no romper
`chain.genesis`). El path de firma/verificacion (TASK-0190/eventlog) ya es correcto; SOLO cambia DE DONDE se lee
el enable + la config de llaves. maker=Codex / checker=Arquitecto. Repo = PROTOCOLO core. Checker desde clon
limpio (ruta corta) con/sin secretos, **incluyendo el ensayo de flip end-to-end** que TASK-0190 no podia pasar.

## Scope

- **Runtime override** gitignored (p.ej. `event-state.runtime.json`, espejo de `file-ingestion.runtime.json`):
  contiene `{ "event_state": { "actor_auth_enforce": true, "actor_auth_config": {...} } }` (o forma equivalente).
- **Lectores** `actor_auth_enforce_enabled(config, root)` y `actor_auth_config(config, root)` mergean el override
  (override gana) ANTES de decidir; si el override esta ausente -> OFF / config base. NO leen el flag del config
  pinned (que ya no lo tiene).
- **Quitar el flag** de `protocol.config.json` (vivo: ya ausente) y del `protocol.config.template.json` (donde
  TASK-0190 lo puso) -> documentar el override en su lugar.
- Resolucion del override: path por env (p.ej. `EVENT_STATE_RUNTIME_CONFIG_PATH`) o ruta gitignored por defecto;
  path-safe; fail-closed si malformado.

## Acceptance Criteria

- **AC1 (enable desde override; config pinned sin flag):** `actor_auth_enforce_enabled` es true SOLO si el override
  lo declara; `protocol.config.json` no contiene `actor_auth_enforce`. Override ausente -> OFF (`not_enforced_phase2`).
- **AC2 (FLIP LIMPIO -- el AC que el ensayo fallaba) [CRITICO]:** activar A2 poniendo el override (enabled:true +
  actor_auth_config con private_key_files/keyids) **NO cambia `protocol.config.json`** -> `chain.genesis` intacto;
  un `submit_intent` real emite `actor_auth ed25519` verificable; **`validate` exit 0 (sin "genesis mismatch")**,
  drift 0, SIN re-genesis. Behavior-test end-to-end del flip por override.
- **AC3 (OFF byte-identico):** sin override, el camino es byte-identico al actual (HMAC + not_enforced_phase2). Test
  no-regresion.
- **AC4 (rollback):** quitar/false el override -> vuelve a OFF, chain intacta, validate exit 0. Reversible.
- **AC5 (sin regresion A2):** firma/verificacion (TASK-0190) intactas: atribucion-cruzada RECHAZADA, secret-indep
  (DECISION-0046, clon limpio solo-publicas valida), fail-closed sin privada. Golden `actor_auth_ed25519_cases`
  adaptado al override sigue verde.
- **AC6 (gates):** `validate_collaboration_state.py` exit 0 (con y sin secretos) clon limpio; golden en CI;
  `scan_encoding`/`scan_domain_neutrality` exit 0; el override gitignored (no secretos/flag commiteados);
  `chain.genesis`/genesis/config pinned intactos; Co-Authored-By Codex.

## Out of scope

- Cambiar el algoritmo de firma/verificacion (TASK-0190 OK). La activacion viva (flip) = ventana del operador.
  Generar/medir el dataset.

## Notes

- El AC2 es el corazon: probar que encender A2 por override deja `validate` verde y la cadena intacta (lo que
  rompia con el flag-en-config). Checker re-ensaya el flip completo en clon limpio (ruta corta; copiar
  secrets/ + protocol-secrets como en el ensayo del Arquitecto) y confirma validate exit 0 post-flip.
