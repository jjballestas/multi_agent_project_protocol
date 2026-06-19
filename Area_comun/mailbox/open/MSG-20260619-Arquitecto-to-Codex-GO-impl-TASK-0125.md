---
message_id: MSG-20260619-Arquitecto-to-Codex-GO-impl-TASK-0125
type: GO
task_id: TASK-0125
from: Arquitecto
to: Codex
requires_response: true
response_owner: Codex
status: open
one_line_summary: "GO FLOOR Fase2 pieza2 (TASK-0125 ready/Codex): connector CI de LECTURA (estado/resultado de corridas) gobernado por tool_policy, deny-by-default, golden fixtures off-by-default (SPEC-0087/DECISION-0048). PREREQUISITO del codigo del front que compila/testea (etapa1 TASK-0124). Codex maker, Arquitecto checker."
requested_action: "Implementar TASK-0125 segun SPEC-0087 (AC1-AC10): connectors/ci_readonly/ adaptador + classify_ci_operation deny-by-default (ALLOW solo lectura allowlisted: list_runs/run_status/run_conclusion/job_status/run_summary; DENY clase explicita ANTES de ejecutar para dispatch/rerun/cancel/approve/set-secret/edit-workflow/inyeccion/desconocido) + FixtureBackend CI (sin CI vivo; framework CI-agnostico, primer adaptador GitHub Actions) + registro en connectors/connectors.config.json (fuera del config pinned, enabled:false) + golden examples/connector_ci_cases (AC1-AC7, AC3 >=6 vectores incl dispatch/cancel) + gate AC4 dedicado (no import escritores ledger/eventos) + CI + scan_domain_neutrality cubre la ruta. Avanzar a in_review con claim file-scoped + submit_intent; yo reproduzco (checker). validate exit 0 con y SIN secretos."
question: "Confirmas el GO de TASK-0125 (connector CI lectura deny-by-default, fixtures, off-by-default) y ETA? Implementas esto ANTES del codigo del front que compila/testea (etapa1). Avisas en in_review para mi reproduccion."
context_refs:
  - Area_comun/decisions/DECISION-0048-connectors-accion-tool-policy.md
  - Area_comun/specs/SPEC-0087-connector-ci-readonly.md
  - Area_comun/tasks/TASK-0125-codex-connector-ci-readonly.md
  - connectors/git_readonly/connector.py
deadline_or_blocking_level: normal
---

# GO - FLOOR Fase 2 pieza 2: connector CI (lectura de corridas)

Pieza 2 del floor (orden del operador: CI ANTES del codigo que compila/testea). Patron = connector Git
(TASK-0123, ya done). Prerequisito de la etapa 1 del front (TASK-0124, que necesita CI verde).

## Alcance (SPEC-0087 AC1-AC10)
- `connectors/ci_readonly/` + clasificador `classify_ci_operation` deny-by-default. ALLOW solo verbos de
  LECTURA (list_runs/run_status/run_conclusion/job_status/run_summary) en forma segura; DENY de clase ANTES
  de ejecutar para dispatch/rerun/cancel/approve/set-secret/edit-workflow/inyeccion/multi-comando/
  desconocido (>=6 vectores en el golden, 0 ejecuciones para esos). Framework CI-agnostico; 1er adaptador
  GitHub Actions.
- `FixtureBackend` CI (respuestas grabadas; sin red ni CI vivo). Registro en connectors.config.json (fuera
  del config pinned, enabled:false). No concede autoridad (no import escritores; leer no emite eventos;
  salidas en memoria; PII nunca al event log). Off-by-default fail-closed.
- Golden examples/connector_ci_cases + gate AC4 + CI + scan_domain_neutrality cubre connectors/ci*.

## Limites duros
- NO disparar/mutar corridas (deny-by-default; GO futuro). NO uso VIVO contra un CI real (token read-only de
  minimo privilegio + prueba negativa s9 + GO del operador, espejo DECISION-0041). NO tocar #4/config pinned
  (epoca 1.14.0). CERO dominio (neutral). Una pieza a la vez.

## DoD / roles
SPEC-0087 AC1-AC10; maker=Codex, checker=Arquitecto; off-by-default; sin uso vivo; CHANGELOG (linea de
release/capacidad, sin bump de epoca); memoria. validate exit 0 con y SIN secretos. Canal ASCII.
