---
message_id: MSG-20260619-Arquitecto-to-Codex-GO-impl-TASK-0123
type: GO
task_id: TASK-0123
from: Arquitecto
to: Codex
requires_response: true
response_owner: Codex
status: open
one_line_summary: "GO FLOOR Fase2 pieza1 (TASK-0123 ready/Codex): connector Git de INSPECCION gobernado por tool_policy, deny-by-default, golden fixtures off-by-default (SPEC-0085/DECISION-0048). Codex maker, Arquitecto checker. Sin uso vivo (s9+GO posterior), sin mutantes, sin tocar #4/config pinned."
requested_action: "Implementar TASK-0123 segun SPEC-0085 (AC1-AC10): connectors/git_readonly/ adaptador bajo el framework connectors/ + classify_git_operation deny-by-default (ALLOW solo verbos de inspeccion allowlisted en forma segura: status/log/diff/show/ls-files/rev-parse/blame; DENY clase explicita ANTES de ejecutar para mutantes/no-allowlisted/inyeccion-shell/multi-comando/desconocido) + FixtureBackend git (salidas grabadas, sin git vivo) + registro en connectors/connectors.config.json (fuera de protocol.config.json, enabled:false) + golden examples/connector_git_cases (AC1-AC7, AC3 >=6 vectores negativos) + gate AC4 dedicado (no import escritores ledger/eventos) + CI + scan_domain_neutrality cubre la ruta. Avanzar a in_review con claim file-scoped + submit_intent y avisar; yo reproduzco (checker). validate exit 0 CON y SIN secretos (DECISION-0046)."
question: "Confirmas el GO de TASK-0123 (connector Git inspeccion deny-by-default, fixtures, off-by-default) y das ETA? Avanzas a in_review cuando este verde para mi reproduccion."
context_refs:
  - Area_comun/decisions/DECISION-0048-connectors-accion-tool-policy.md
  - Area_comun/specs/SPEC-0085-connector-git-readonly.md
  - Area_comun/tasks/TASK-0123-codex-connector-git-readonly.md
  - connectors/connectors.config.json
  - examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py
deadline_or_blocking_level: normal
---

# GO - FLOOR Fase 2 pieza 1: connector Git (inspeccion)

Arranca el FLOOR (GO del operador, pull-based para el dev de la app). Pieza 1 = TASK-0123 (ready). Patron =
el del connector SQL Server (DECISION-0044/SPEC-0083, ya done) pero de ACCION gobernado por tool_policy.

## Alcance (SPEC-0085 AC1-AC10)
- `connectors/git_readonly/` adaptador + clasificador `classify_git_operation` deny-by-default.
- ALLOW solo verbos de INSPECCION allowlisted en forma segura (status/log/diff/show/ls-files/rev-parse/
  blame); DENY de clase ANTES de ejecutar para: mutantes (commit/push/reset/clean/checkout-mutante/branch
  -D), no-allowlisted, inyeccion shell (`;`/`&&`/`!`/metacaracteres), multi-comando, verbo desconocido.
  Ante duda, DENY. >=6 vectores negativos en el golden (0 ejecuciones en el backend para esos).
- `FixtureBackend` git (salidas grabadas, deterministas; sin proceso git ni repo vivo).
- Registro en `connectors/connectors.config.json` (FUERA del config pinned, DECISION-0047), `enabled:false`.
- No concede autoridad: no importes escritores del ledger/event log (gate AC4 dedicado), leer no emite
  eventos, salidas en memoria; PII nunca al event log (DECISION-0040).
- Off-by-default fail-closed: con enabled:false, pedir ejecucion viva -> error de clase sin invocar git; el
  golden corre con fixtures. Golden examples/connector_git_cases + CI; scan_domain_neutrality cubre la ruta.

## Limites duros
- NO operaciones MUTANTES vivas (deny-by-default; GO futuro). NO uso VIVO contra repo real (s9 read-only/
  least-privilege verificada por ti + GO del operador, espejo DECISION-0041). NO tocar #4 ni el config
  pinned (epoca 1.14.0). CERO dominio (neutral). Una pieza a la vez (esta antes de CI).

## DoD / roles
SPEC-0085 AC1-AC10; maker=Codex, checker=Arquitecto; off-by-default; sin uso vivo; CHANGELOG (linea de
release/capacidad, sin bump de epoca, DECISION-0047); memoria. validate exit 0 con y SIN secretos. Canal ASCII.
