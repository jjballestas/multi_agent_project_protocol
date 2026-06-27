---
task_id: TASK-0192
title: "Core: mover actor_auth_enforce/actor_auth_config a un runtime override fuera del config pinned (flip A2 sin romper chain.genesis) (SPEC-0105, DECISION-0067)"
type: protocol
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0105
created_at: 2026-06-27
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
origin: ensayo del flip A2 (Arquitecto) -> el flag-en-config rompe la cadena; DECISION-0067 corrige TASK-0190
reuses: [TASK-0190]
linked_decisions: [DECISION-0067, DECISION-0065, DECISION-0047, DECISION-0046]
file: Area_comun/tasks/TASK-0192-codex-actor-auth-flag-runtime-override.md
---

# TASK-0192 - actor_auth flag a runtime override (corrige TASK-0190)

> maker=Codex / checker=Arquitecto. Repo = PROTOCOLO core. Corrige el error: el flag estaba en
> `protocol.config.json` y encenderlo ROMPE `chain.genesis` (ensayo del Arquitecto: "genesis mismatch"). Mover el
> enable+config de A2 a un **runtime override gitignored FUERA del config pinned** (espejo file-ingestion.runtime.json).
> El path de firma (TASK-0190) NO cambia; solo DE DONDE se lee el enable. NO tocar el algoritmo ni el genesis.

## Alcance (SPEC-0105 AC1-AC6)
- Runtime override gitignored (p.ej. `event-state.runtime.json`) con `event_state.actor_auth_enforce` +
  `actor_auth_config`; lectores `actor_auth_enforce_enabled`/`actor_auth_config` mergean el override (override gana),
  sin leer el flag del config pinned. Path por env + default gitignored; path-safe; fail-closed.
- Quitar el flag de `protocol.config.json` (ya ausente) y del `protocol.config.template.json` (TASK-0190 lo puso);
  documentar el override.

## DoD (= SPEC-0105 AC1-AC6)
- AC1 enable desde override; config pinned sin el flag; override ausente -> OFF (not_enforced_phase2).
- AC2 CRITICO: activar por override NO cambia protocol.config.json -> chain.genesis intacto; submit_intent real
  firma ed25519; **validate exit 0 (sin "genesis mismatch"), drift 0, SIN re-genesis**. Behavior-test del flip e2e.
- AC3 OFF byte-identico (sin override).
- AC4 rollback (quitar override) -> OFF, chain intacta, validate exit 0.
- AC5 sin regresion A2: atribucion-cruzada rechazada, secret-indep (0046), fail-closed sin privada; golden adaptado verde.
- AC6 gates: validate exit 0 (con/sin secretos) clon limpio; golden CI; encoding/neutralidad exit 0; override
  gitignored (sin secretos/flag commiteados); genesis/config pinned intactos; Co-Author.

## Fuera de alcance
- Cambiar firma/verificacion (TASK-0190 OK); activacion viva (flip=operador); generar/medir dataset.

## Notas
- AC2 es el corazon (probar que encender por override deja validate verde + cadena intacta -- lo que rompia el
  flag-en-config). Checker re-ensaya el flip e2e en clon limpio RUTA CORTA (copiar secrets/ + protocol-secrets como
  el ensayo del Arquitecto). Cero secretos/flag al repo.
