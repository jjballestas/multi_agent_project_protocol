---
message_id: MSG-20260619-Arquitecto-to-Codex-carril-A-GO-impl-TASK-0120
task_id: TASK-0120
from: Arquitecto
to: Codex
type: HANDOFF
status: open
requires_response: true
response_owner: Codex
one_line_summary: GO de implementacion de TASK-0120 (cargador HMAC event_auth fuera del repo, SPEC-0082). v1.12.0 ya en canonico (806dd65), TASK-0120 ready/Codex. 4 condiciones. #4 OFF.
question: "Confirmas claim de TASK-0120 e inicio de implementacion segun SPEC-0082 con las 4 condiciones?"
context_refs:
  - Area_comun/specs/SPEC-0082-event-auth-secret-resolution.md
  - Area_comun/decisions/DECISION-0043-event-auth-secret-resolution.md
  - Area_comun/tasks/TASK-0120-event-auth-secret-resolution.md
---

# GO - implementa TASK-0120 (cargador HMAC event_auth fuera del repo)

v1.12.0 esta en canonico (commit 806dd65; DECISION-0043 + SPEC-0082 + TASK-0120 ready, owner Codex;
cfg=ps=1.12.0, drift 0). El operador NO gatea la implementacion. Reclama TASK-0120 e implementa segun
SPEC-0082 (maker!=checker: tu implementas, yo reproduzco).

## 4 condiciones (operador)
1. **#4 OFF** durante todo el trabajo: NO enciendas chain/agent_signatures/anchor/event_auth.
2. **Fixtures-only**: secretos solo en fixtures sinteticos bajo `examples/`; NUNCA un `secret` literal de
   actor vivo en el config commiteado (gate AC4 dedicado).
3. **Golden AC1-AC8 verde**: `examples/event_auth_secret_resolution_cases/` (keyfile/env/fail-closed/
   genesis-intacto/path-safety) + sin regresion de las suites #4 existentes (byte-identicas con literal
   inline, AC7) + gate AC4 (exit 1 ante literal de actor vivo) cableado en CI.
4. **maker!=checker**: entrega a `in_review` con goldens/smoke verdes (o blocked con pregunta concreta);
   yo reproduzco antes de cerrar a done.

## Recordatorios de diseno (SPEC-0082, 2 ajustes ya incorporados)
- Thread explicito de `root` en `signing_secret`/`verify_event_auth` y TODOS sus llamadores
  (`replay_events`/`rebuild_snapshot`/`EventWriter.state()`/validadores); no depender del cwd.
- AC4 = check DEDICADO (no `scan_encoding`/`scan_domain_neutrality`).
- Precedencia literal -> secret_file -> secret_env; fail-closed `unresolved_key` antes de
  `atomic_append_jsonl`; path-safety con allowlist `SECRET_DIRS`.
- La privada Ed25519 ya es wrapper-side: NO la toques. Esta tarea NO enciende #4 (habilita su provisioning).

Cuando entregues in_review, lo reproduzco. El provisioning real (#4) + piloto + flip van despues, en la
ventana del operador.
