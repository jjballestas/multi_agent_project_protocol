---
id: TASK-0125
title: Connector CI (lectura de corridas) gobernado por tool_policy, deny-by-default + golden off-by-default (DECISION-0048 / SPEC-0087)
type: security
status: ready
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0087
linked_decisions: [DECISION-0048, DECISION-0044, DECISION-0041, DECISION-0047]
created_at: 2026-06-19
---

# TASK-0125 - Connector CI (lectura) deny-by-default

## Objective

FLOOR Fase 2 pieza 2: connector CI de LECTURA (estado/resultado de corridas) bajo `connectors/`, gobernado
por tool_policy deny-by-default, no concede autoridad, off-by-default, golden con fixtures (sin CI vivo).
Prerequisito del codigo del proyecto-front que compila/testea. Ver SPEC-0087 (AC1-AC10). maker=Codex,
checker=Arquitecto. NO disparar/mutar corridas (deny-by-default). NO uso vivo (s9+GO posterior). NO tocar
#4/config pinned.

## Alcance (SPEC-0087)

- `connectors/ci_readonly/` adaptador + `classify_ci_operation` deny-by-default (ALLOW solo verbos de
  lectura allowlisted: list_runs/run_status/run_conclusion/job_status/run_summary; DENY clase explicita
  ANTES de ejecutar para dispatch/rerun/cancel/approve/set-secret/edit-workflow/inyeccion/desconocido).
  Framework CI-agnostico; primer adaptador = GitHub Actions.
- `FixtureBackend` CI (respuestas grabadas; sin red ni CI vivo).
- Registro en `connectors/connectors.config.json` (FUERA de protocol.config.json), default `enabled:false`.
- Golden `examples/connector_ci_cases/` (AC1-AC7, AC3 >=6 vectores incl dispatch/cancel) + gate AC4 dedicado
  (no import de escritores ledger/eventos) + CI; `scan_domain_neutrality` cubre la ruta.

## DoD

SPEC-0087 AC1-AC10; maker=Codex / checker=Arquitecto; off-by-default; sin uso vivo; sin tocar #4/config;
CHANGELOG (linea de release/capacidad); memoria. validate exit 0 con y SIN secretos (DECISION-0046), drift 0.

## Verification

- `python examples\connector_ci_cases\run_connector_ci_cases.py` (AC1-AC7)
- gate AC4 (no import escritores); `scan_domain_neutrality` cubre connectors/ci*
- `validate_collaboration_state.py --root .` (con y sin secretos) + `scan_encoding.py`
