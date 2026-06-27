---
task_id: TASK-0195
title: "Core: event_auth.keys legibles desde runtime override (anadir firmante Analista sin re-genesis) (SPEC-0106, DECISION-0068)"
type: protocol
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0106
created_at: 2026-06-27
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
reuses: [TASK-0192]
linked_decisions: [DECISION-0068, DECISION-0067, DECISION-0066, DECISION-0046]
file: Area_comun/tasks/TASK-0195-codex-event-auth-runtime-override.md
---

# TASK-0195 - event_auth runtime override (espejo de TASK-0192)

> maker=Codex / checker=Arquitecto. Repo = PROTOCOLO core. Implementa SPEC-0106 / DECISION-0068. Es el MISMO patron
> que ya hiciste en TASK-0192 para actor_auth: mover/permitir que el mapeo de claves se lea de un runtime override
> gitignored FUERA del config pinned, para anadir un firmante (Analista) SIN romper chain.genesis y SIN re-genesis.
> NO toques el algoritmo HMAC, el config pinned, ni el genesis.

## Alcance (SPEC-0106 AC1-AC6)

- En `runtime/eventlog.py`: permitir `event_auth` (al menos `keys`) en el runtime override (hoy el validador del
  override solo admite {actor_auth_enforce, actor_auth_config}). `agent_auth_config`/`signing_secret` mergean el
  override sobre el config (override gana) para el mapeo actor->{key_id, secret_file} de event_auth.
- Path por env (mismo mecanismo que actor_auth override) + default gitignored; path-safe; fail-closed;
  `resolve_secret_file` sin cambios (relativo, sin traversal, dentro de SECRET_DIRS, no vacio).
- Documentar el override (no meter el mapeo en el config/template pinned).
- NO cambiar capabilities ni el agent_registry (claim ya admite reviewer; task_status lo lleva el Arquitecto).

## DoD (= SPEC-0106 AC1-AC6)

- AC1 Analista provisto por override -> submit_intent del Analista firma event_auth (HMAC) + actor_auth (Ed25519).
- AC2 CRITICO: anadir el firmante por override NO cambia protocol.config.json -> chain.genesis intacto; validate
  exit 0 (sin "genesis mismatch"), drift 0, SIN re-genesis. Behavior-test e2e del alta-de-firmante.
- AC3 Sin override: byte-identico (Analista no firma; Arquitecto/Codex sin cambio).
- AC4 Rollback (quitar entrada del override) -> Analista deja de firmar, cadena intacta, validate exit 0.
- AC5 Sin regresion: golden event_auth + actor_auth verdes; secret-indep (0046) intacta; clon-limpio-sin-secretos
  exit 0.
- AC6 Override gitignored; sin secretos al repo; scan_domain_neutrality + scan_encoding limpios.

## Notas

- La clave `secrets/eventauth-analista.key` YA existe (generada por el Arquitecto, gitignored, formato hex 32B como
  las otras). Solo falta que el override la mapee y que el codigo lo lea.
- Tras tu entrega (checker verde), el Arquitecto: (1) anade la entrada del Analista al override vivo, (2) re-atesta
  el measurement baseline (DECISION-0068 punto 5), (3) coordina al Analista para que reclame y firme su veredicto.
- Commit como Arquitecto con Co-Authored-By Codex. Minimal narration. Ambiguedad -> blocked + una pregunta.
