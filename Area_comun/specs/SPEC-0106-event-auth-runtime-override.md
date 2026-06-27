---
spec_id: SPEC-0106
title: event_auth.keys legibles desde runtime override (anadir firmante sin re-genesis)
status: ready
phase: P2
linked_decisions: [DECISION-0068, DECISION-0067, DECISION-0066]
owner: Codex
checker: Arquitecto
created_at: 2026-06-27
---

# SPEC-0106 - event_auth.keys via runtime override

> Implementa DECISION-0068. Espejo de SPEC-0105/TASK-0192 (que hizo lo mismo para actor_auth). Core =
> `runtime/eventlog.py`. NO tocar el algoritmo HMAC ni el config pinned ni el genesis.

## Cambio

Hoy `agent_auth_config(config, actor)` (eventlog.py ~504) lee el mapeo event_auth de `config["event_auth"]["keys"]`
(que vive en `protocol.config.json` PINNED). Extender para que **mergee un override gitignored** (mismo archivo /
mecanismo que el actor_auth override de DECISION-0067, `event-state.runtime.json`), de modo que `event_auth.keys`
(y campos event_auth por actor) puedan provenir del override y GANEN sobre el config, sin leer el mapeo del config
cuando el override lo provea.

- Ampliar el conjunto de claves permitidas del override para incluir `event_auth` (al menos su subclave `keys`).
  Hoy el validador del override rechaza claves != {actor_auth_enforce, actor_auth_config} (eventlog.py ~255).
- `signing_secret` / `agent_auth_config` resuelven el secret_file del actor con el mapeo mergeado; `resolve_secret_file`
  sigue exigiendo ruta relativa, sin traversal, dentro de SECRET_DIRS, no vacia (sin cambios).
- Path del override por env (mismo que actor_auth) + default gitignored; path-safe; fail-closed.

## DoD = AC

- **AC1** Con el override proveyendo `event_auth.keys.Analista = {key_id, secret_file: secrets/eventauth-analista.key}`,
  `signing_secret(config, "Analista")` resuelve la clave y un `submit_intent` con actor Analista produce un evento
  con `event_auth` (HMAC) valido + `actor_auth` Ed25519 valido.
- **AC2 (CRITICO)** Anadir el firmante por override NO cambia `protocol.config.json` -> `chain.genesis` intacto;
  `validate` exit 0 (SIN "genesis mismatch"), drift 0, SIN re-genesis. Behavior-test e2e.
- **AC3** Sin la entrada en el override, comportamiento byte-identico al actual (Analista -> "event auth signing key
  missing"; Arquitecto/Codex sin cambio).
- **AC4** Rollback: quitar la entrada del override -> Analista deja de firmar, cadena intacta, validate exit 0.
- **AC5** Sin regresion: Arquitecto/Codex siguen firmando event_auth+actor_auth; golden de event_auth y actor_auth
  verdes; verificacion secret-independiente (DECISION-0046) intacta; clon-limpio-sin-secretos valida exit 0.
- **AC6** Override gitignored; sin secretos al repo; scan_domain_neutrality + scan_encoding limpios.
