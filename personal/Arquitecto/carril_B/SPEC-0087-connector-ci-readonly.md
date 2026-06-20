---
spec_id: SPEC-0087
task_id: TASK-0125
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

# SPEC-0087 - Connector CI (lectura de corridas) gobernado por tool_policy, deny-by-default

## Context

DECISION-0048: connectors de accion gobernados por tool_policy, deny-by-default, no conceden autoridad,
off-by-default, uso vivo gateado (s9+GO). FLOOR Fase 2 pieza 2 = connector CI de LECTURA (estado/resultado
de corridas), prerequisito de "el codigo que compila/testea" del proyecto-front. Patron = connector Git
(SPEC-0085). maker=Codex, checker=Arquitecto. Fixtures-only (sin CI vivo).

## Scope

- `connectors/ci_readonly/`: adaptador bajo el framework `connectors/` + clasificador deny-by-default de
  operaciones CI gobernado por tool_policy. Framework neutral (CI-system-agnostico); primer adaptador =
  GitHub Actions (lo que ya usa el protocolo); el backend de fixtures es agnostico.
- Allowlist de LECTURA: estado/resultado de corridas -- list runs, get run/job status, get conclusion
  (success/failure), logs/summary de una corrida identificada. Forma acotada/parametrizada.
- DENY de clase ANTES de ejecutar para: DISPARAR/re-ejecutar/cancelar corridas, aprobar deployments,
  mutar secrets/variables/workflows, cualquier verbo mutante o no-allowlisted, inyeccion/multi-comando,
  verbo desconocido. Ante duda, DENY.
- `FixtureBackend` CI (respuestas grabadas: run status/conclusion/jobs/summary; sin red ni CI vivo).
- Registro en `connectors/connectors.config.json` (FUERA de protocol.config.json), default `enabled:false`.
- Golden `examples/connector_ci_cases/` + CI; `scan_domain_neutrality` cubre la ruta.

## Out Of Scope

- Disparar/mutar corridas (deny-by-default; GO futuro); uso VIVO contra un CI real (s9+GO, DECISION-0041);
  tocar #4 / config pinned; dominio; el pipeline CI del producto front (eso es codigo en Zeus-protocol que
  USA este connector).

## Diseno

`classify_ci_operation(op, args, policy) -> ALLOW(read) | DENY(reason_class)` antes de ejecutar:
- ALLOW: verbo de lectura allowlisted (list_runs, run_status, run_conclusion, job_status, run_summary) con
  args en forma segura (run/job id, repo/workflow ref; sin flags peligrosos, sin shell-metacaracteres).
- DENY (clase, sin ejecutar): dispatch/rerun/cancel, approve, set-secret/variable, edit-workflow, verbo
  mutante, no-allowlisted, desconocido, inyeccion/multi-comando.
El connector NO concede autoridad: solo expone lo allowlisted; no importa escritores del ledger/event log;
leer no emite eventos; salidas en memoria (no persistidas). Off-by-default: con `enabled:false`, pedir
ejecucion VIVA -> error de clase sin tocar el CI (fail-closed); el golden usa fixtures.

## acceptance_criteria

- **AC1 - trust_boundary + allowlist deny-by-default.** Connector declarado con trust_boundary (read_only,
  grants_no_authority, persists_outputs:false, allowlist de verbos de lectura). Verbo/arg fuera del
  allowlist -> denegado. Golden.
- **AC2 - Lectura (positivo).** Un verbo allowlisted (p.ej. run_status/run_conclusion) contra fixtures
  devuelve el estado/resultado grabado (evidencia en memoria). Golden.
- **AC3 - Deny-by-default (prueba negativa OBJETIVA, >=6 vectores).** Rechazo de clase ANTES de ejecutar,
  golden negativo por vector, >=6: dispatch (disparar), rerun, cancel, set-secret/variable, edit-workflow/
  approve, inyeccion/multi-comando o verbo desconocido. NUNCA se ejecuta el CI para esos vectores (el
  backend registra 0 ejecuciones).
- **AC4 - No concede autoridad / no escribe (gate dedicado + behavioral).** El modulo no importa escritores
  del ledger/event log ni expone API de mutacion; leer produce 0 eventos nuevos y 0 cambios de estado.
- **AC5 - Off-by-default + fail-closed (vivo).** Default `enabled:false`; pedir ejecucion viva -> error de
  clase sin invocar el CI. Golden corre con fixtures sin importar el flag.
- **AC6 - Genesis/drift intactos.** Registro en connectors.config.json (fuera de protocol.config.json);
  aterrizar no cambia genesis ni drift; validate exit 0 (con y SIN secretos, DECISION-0046).
- **AC7 - Frontera de datos / PII.** Salidas no persisten al event log/estado; un campo PII-like de un
  fixture leido -> 0 escritura al event log (DECISION-0040). Golden.
- **AC8 - Precondicion de uso vivo (s9, espejo DECISION-0041), NO ejercida.** Documentada + fail-closed: el
  uso vivo exige identidad/token de minimo privilegio (read-only, sin permiso de disparar/mutar) + prueba
  negativa objetiva registrada por Codex (s9) + GO del operador. En esta pieza la ruta viva esta cerrada.
- **AC9 - Neutralidad.** Cero dominio en `connectors/ci*` ni golden; framework CI-agnostico;
  scan_domain_neutrality limpio.
- **AC10 - Gates.** validate (--root . con y sin secretos) + scan_encoding + scan_domain_neutrality + el
  nuevo `connector_ci_cases` en CI.

## test_plan

- `examples/connector_ci_cases/run_connector_ci_cases.py`: AC1 allowlist/trust_boundary; AC2 lectura de
  estado/resultado contra fixtures; AC3 >=6 vectores negativos (rechazo de clase, 0 ejecuciones); AC4 gate
  no-import-escritores + 0 eventos; AC5 off-by-default fail-closed; AC7 fila PII-like; reporte JSON
  determinista, exit 0/1.
- Sin regresion: connector_git_cases + connector_sqlserver_readonly_cases + suites existentes verdes.

## closure_criteria

- AC1-AC10; maker=Codex / checker=Arquitecto; off-by-default; sin uso vivo; sin tocar #4/config; CHANGELOG
  (linea de release/capacidad, DECISION-0047, sin bump de epoca); memoria.

## Risks

- **Parser de args evadible / inyeccion.** Mitigacion: deny-by-default + allowlist estricto + rechazo de
  metacaracteres/multi-comando; prueba negativa por vector; uso vivo agrega token read-only de minimo
  privilegio (s9).
- **Confundir "leer corrida" con "disparar corrida".** Mitigacion: dispatch/rerun/cancel son DENY duros
  (vectores AC3); el connector del floor es SOLO lectura.

## Traceability

| Requirement | Task | Test | Closure |
|-------------|------|------|---------|
| trust_boundary + allowlist deny-by-default | TASK-0125 | connector_ci_cases AC1 | AC1 |
| Lectura de estado/resultado contra fixtures | TASK-0125 | golden AC2 | AC2 |
| Deny-by-default >=6 vectores (incl dispatch/cancel) | TASK-0125 | goldens negativos | AC3 |
| No concede autoridad / no escribe | TASK-0125 | gate AC4 + behavioral | AC4 |
| Off-by-default fail-closed | TASK-0125 | golden flag | AC5 |
| Genesis/drift intactos | TASK-0125 | validate con/sin secretos | AC6 |
| Neutralidad CI-agnostica | TASK-0125 | scan_domain | AC9 |
