---
task_id: TASK-0190
title: "Core: submit_intent firma actor_auth Ed25519 (A2 vivo, Camino B) off-by-default + golden + prueba negativa atribucion-cruzada + secret-indep (SPEC-0103, DECISION-0065)"
type: protocol
status: in_progress
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0103
created_at: 2026-06-27
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
origin: DECISION-0065 (A2 vivo, Camino B; cutover gateado del TFM)
reuses: []
linked_decisions: [DECISION-0065, DECISION-0039, DECISION-0046, DECISION-0029]
file: Area_comun/tasks/TASK-0190-codex-actor-auth-ed25519-submit-intent.md
---

# TASK-0190 - submit_intent firma actor_auth Ed25519 (Camino B), off-by-default

> maker=Codex / checker=Arquitecto. Repo = **PROTOCOLO core** (`runtime/`). **CONSTRUIR OFF-BY-DEFAULT**: el camino
> vivo (que usan TODOS los agentes para escribir el ledger) debe quedar **byte-identico** con el flag OFF. NO tocar
> genesis/#4/config pinned. La ACTIVACION viva (flip) es ventana del operador, NO esta tarea.

## Alcance (SPEC-0103 AC1-AC6)
- `submit_intent`/`eventlog`: con flag `event_state.actor_auth_enforce` ON, `append_event` recibe
  `actor_auth={method:"ed25519",keyid,sig}` firmado con la privada Ed25519 del `--actor-id` (de
  `D:/Agentes/protocol-secrets/`, path-safe, fail-closed). Reusar cripto existente (`llm_turn_wrapper`/sign Ed25519
  / `attestation_signing_payload`); NO duplicar ni meter secretos al repo.
- Flag OFF por defecto en el config versionado.
- validate/replay: aceptar `not_enforced_phase2` (previos) + `ed25519` (nuevos); verificar con la publica; rechazar
  firma invalida / keyid no registrado / atribucion cruzada.
- Golden `examples/actor_auth_ed25519_cases` + CI.

## DoD (= SPEC-0103 AC1-AC6)
- AC1 firma viva verificable con la publica del actor (flag ON).
- AC2 off-by-default: camino OFF byte-identico al actual (HMAC intacto); flag no commiteado en ON. Test no-regresion.
- AC3 atribucion cruzada RECHAZADA (prueba negativa PERMANENTE; vectores fijos + golden).
- AC4 secret-independiente (DECISION-0046): clon limpio solo-publicas valida exit 0; firmar sin privada falla-closed.
- AC5 ledger vivo intacto: replay acepta previos+nuevos; drift 0; chain/anchor/HMAC verdes; genesis/config intactos.
- AC6 gates: validate exit 0 (con/sin secretos) clon limpio; golden en CI; encoding/neutralidad exit 0; Co-Author.

## Fuera de alcance
- real_invoker/SA/Camino A; activacion viva (flip = operador presente); tocar append_agent_attestation; generar/medir dataset.

## Notas
- Cuidado MAXIMO con el camino OFF: es el que usan todos los agentes; un bug ahi rompe el ledger vivo. El checker
  verifica OFF byte-identico + ON firma/verifica/rechaza-cruzada/secret-indep, desde clon limpio CON y SIN secretos
  (`git -c core.longpaths=true`). Reusar cripto; cero secretos al repo.
