---
spec_id: SPEC-0085
task_id: TASK-0123
type: security
status: accepted
linked_decisions:
  - DECISION-0048
  - DECISION-0044
  - DECISION-0041
  - DECISION-0047
created_at: 2026-06-19
updated_at: 2026-06-19
author: Arquitecto
---

# SPEC-0085 - Connector Git (inspeccion) gobernado por tool_policy, deny-by-default

## Context

DECISION-0048: connectors de accion gobernados por tool_policy, deny-by-default, allowlist de inspeccion,
no conceden autoridad, off-by-default, uso vivo gateado (s9+GO). Esta SPEC fija el primer adaptador: Git de
INSPECCION (read-only), con backend de fixtures. Pieza 1 del floor Fase 2. maker=Codex, checker=Arquitecto.

## Scope

- `connectors/git_readonly/` (o `connectors/git/`): adaptador bajo el framework `connectors/` (DECISION-0044)
  + clasificador deny-by-default de operaciones git gobernado por tool_policy.
- Allowlist de INSPECCION: `status`, `log`, `diff`, `show`, `ls-files`, `rev-parse`, `blame` (forma
  acotada/parametrizada; sin flags arbitrarios que muten). Todo lo demas (commit/push/reset/clean/checkout-
  mutante/fetch/pull/tag/branch-d, EXEC de hooks, comandos shell arbitrarios) -> DENY de clase explicita
  ANTES de ejecutar.
- `FixtureBackend` (salidas git grabadas, deterministas; sin repo vivo ni proceso git).
- Registro en `connectors/connectors.config.json` (FUERA de protocol.config.json), default `enabled:false`.
- Golden `examples/connector_git_cases/` + CI; `scan_domain_neutrality` cubre la nueva ruta.

## Out Of Scope

- Operaciones git MUTANTES (deny-by-default; GO futuro); uso VIVO contra repo real (s9+GO, DECISION-0041);
  CI connector (SPEC-0086, pieza 2); tocar #4 / config pinned; dominio.

## Diseno

`classify_git_operation(op, args, policy) -> ALLOW(read) | DENY(reason_class)` antes de cualquier ejecucion:
- ALLOW: verbo en el allowlist de inspeccion + args en forma segura (sin `-x`/`!`/redireccion/`;`/`&&`/
  subcomando que mute; sin `--upload-pack`/`-c core.*=` peligrosos).
- DENY (clase, sin ejecutar): verbo mutante, verbo no allowlisted, verbo desconocido, args con inyeccion/
  shell-metacaracteres, multi-comando. Ante duda, DENY.
El connector NO concede autoridad: solo expone lo allowlisted por tool_policy; no importa escritores del
ledger/event log; leer no emite eventos; salidas en memoria (no persistidas). Off-by-default: con
`enabled:false`, pedir ejecucion VIVA -> error de clase sin tocar git (fail-closed); el golden usa fixtures.

## acceptance_criteria

- **AC1 - trust_boundary + allowlist deny-by-default.** Connector declarado con trust_boundary (read_only,
  grants_no_authority, persists_outputs:false, allowlist de verbos de inspeccion). Verbo/arg fuera del
  allowlist -> denegado. Golden.
- **AC2 - Inspeccion (positivo).** Un verbo allowlisted (p.ej. `git log`/`git diff` parametrizado) contra
  fixtures devuelve la salida grabada (evidencia en memoria). Golden.
- **AC3 - Deny-by-default (prueba negativa OBJETIVA, >=6 vectores).** Rechazo de clase ANTES de ejecutar,
  golden negativo por vector, >=6: commit, push, reset --hard, clean -fd, checkout-mutante (o branch -D),
  EXEC/shell-injection (`log; rm -rf`), verbo desconocido. NUNCA se ejecuta git para esos vectores
  (FixtureBackend registra 0 ejecuciones).
- **AC4 - No concede autoridad / no escribe (gate dedicado + behavioral).** El modulo no importa escritores
  del ledger/event log y no expone API de mutacion; ejecutar inspeccion produce 0 eventos nuevos y 0
  cambios de estado. Gate dedicado (no delegado en scans).
- **AC5 - Off-by-default + fail-closed (vivo).** Default `enabled:false`; pedir ejecucion viva -> error de
  clase sin invocar git. Golden corre con fixtures sin importar el flag.
- **AC6 - Genesis/drift intactos.** Registro en connectors.config.json (fuera de protocol.config.json);
  aterrizar no cambia genesis ni drift; validate exit 0 (con y sin secretos, DECISION-0046).
- **AC7 - Frontera de datos / PII.** Salidas no persisten al event log/estado; PII-like de un fixture leida
  -> 0 escritura al event log (DECISION-0040). Golden.
- **AC8 - Precondicion de uso vivo (s9, espejo DECISION-0041), NO ejercida.** Documentada + fail-closed: el
  uso vivo exige identidad sin permiso de mutacion + prueba negativa objetiva registrada por Codex (s9) +
  GO del operador. En esta pieza la ruta viva esta cerrada por flag.
- **AC9 - Neutralidad.** Cero dominio en `connectors/git*` ni golden; scan_domain_neutrality limpio.
- **AC10 - Gates.** validate (--root . con y sin secretos) + scan_encoding + scan_domain_neutrality + el
  nuevo `connector_git_cases` en CI.

## test_plan

- `examples/connector_git_cases/run_connector_git_cases.py`: AC1 allowlist/trust_boundary; AC2 inspeccion
  contra fixtures; AC3 >=6 vectores negativos (rechazo de clase, 0 ejecuciones en el backend); AC4 gate
  no-import-escritores + 0 eventos; AC5 off-by-default fail-closed; AC7 fila PII-like; reporte JSON
  determinista, exit 0/1.
- Sin regresion: connector_sqlserver_readonly_cases + suites existentes verdes.

## closure_criteria

- AC1-AC10; maker=Codex / checker=Arquitecto; off-by-default; sin uso vivo; sin tocar #4/config; CHANGELOG
  (linea de release/capacidad, DECISION-0047; sin bump de epoca). memoria.

## Risks

- **Parser de args evadible (inyeccion).** Mitigacion: deny-by-default + allowlist estricto de verbos +
  rechazo de metacaracteres/multi-comando; prueba negativa por vector; uso vivo agrega least-privilege s9.
- **Falsa sensacion de seguridad.** El read-only real para el VIVO exige identidad sin mutacion server/repo-
  side (s9), no solo el clasificador.

## Traceability

| Requirement | Task | Test | Closure |
|-------------|------|------|---------|
| trust_boundary + allowlist deny-by-default | TASK-0123 | connector_git_cases AC1 | AC1 |
| Inspeccion read contra fixtures | TASK-0123 | golden AC2 | AC2 |
| Deny-by-default >=6 vectores | TASK-0123 | goldens negativos | AC3 |
| No concede autoridad / no escribe | TASK-0123 | gate AC4 + behavioral | AC4 |
| Off-by-default fail-closed | TASK-0123 | golden flag | AC5 |
| Genesis/drift intactos | TASK-0123 | validate con/sin secretos | AC6 |
| PII fuera del event log | TASK-0123 | golden fila PII | AC7 |
| Neutralidad | TASK-0123 | scan_domain | AC9 |
