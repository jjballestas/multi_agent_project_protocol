# ANALISTA VEREDICTO - TASK-0252 remediation 1

Firma: Analista

## Veredicto

OK / CERRABLE.

Ancla canonica revisada:
- Protocolo HEAD/instruccion: 0ca771fa0d02a268f7dc50adcd6b4dfdc13ef4a5.
- Instruccion REVIEW: Area_comun/mailbox/open/MSG-20260705-Codex-to-Analista-REVIEW-TASK-0252-remediation-1.md.
- Handoff: Area_comun/handoffs/HANDOFF-TASK-0252-codex-to-arquitecto-2.md.
- Producto Nova-Budget: 5ccb82cea3a3f6761f2f598f83a8152da3165735.
- Tarea: Area_comun/tasks/TASK-0252-harness-paridad-exec-vs-endpoint-sandbox.md.

La remediacion cierra los tres bloqueantes previos: el harness valida el rol SQL via `IS_ROLEMEMBER`,
compara la base contra el nombre canonico exacto `DbsFinanciero_SANDBOX` antes de reset/exec/endpoint,
y el gate front queda reproducible desde clon limpio con `npm ci` + `npm test`.

## Reproduccion

Producto, clon limpio:

| Gate | Comando | Exit | Resultado |
|---|---|---:|---|
| checkout | git clone D:/Agentes/Zeus/NOVA/Nova-Budget %TEMP%/nova-budget-analista-0252-r1-*; git checkout 5ccb82c | 0 | HEAD 5ccb82cea3a3f6761f2f598f83a8152da3165735 |
| dotnet | dotnet test NOVA.sln | 0 | 29 tests pass; warning NU1903 Microsoft.OpenApi |
| npm ci | npm ci --prefix apps/nova-web | 0 | 56 packages installed, 0 vulnerabilities |
| npm test | npm test --prefix apps/nova-web | 0 | typecheck pass; vitest 1/1 pass |
| adversarial | dotnet test tests/NOVA.IntegrationTests/NOVA.IntegrationTests.csproj --filter FullyQualifiedName~BudgetParityHarnessAnalistaAdversarialTests | 0 | 8/8 pass |

Protocolo:

| Gate | Exit | Resultado |
|---|---:|---|
| python scripts/validate_collaboration_state.py (vivo, con secretos locales) | 0 | OK |
| python scripts/validate_collaboration_state.py --root clean-clone | 0 | OK |
| python scripts/scan_encoding.py --root . | 0 | OK |
| python scripts/scan_encoding.py --root clean-clone | 0 | OK |
| python scripts/scan_domain_neutrality.py (vivo y clean-clone) | 0 | sin hallazgos |
| drift vivo | 0 | has_drift false, up_to_seq 3996, entries [] |
| #4 byte-identica | 0 | protocol.config.json sin diff; sha256 2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354 |

## Tabla vector por vector

| Vector / AC | Estado | Evidencia |
|---|---|---|
| F-0252-01 rol `budget_sandbox_verifier` verificado por comportamiento | PASA | `SqlBudgetSandboxDatabase.GetExecutionContextAsync` consulta `IS_ROLEMEMBER(@requiredRole)` y `RunAsync` falla cerrado si no devuelve 1. Payloads `false` y `null` lanzan excepcion antes de side effects. |
| F-0252-02 guard exacto de `DbsFinanciero_SANDBOX` | PASA | `RunAsync` usa `string.Equals(..., StringComparison.Ordinal)` contra `CanonicalSandboxDatabaseName`. Payloads `DbsFinanciero`, `DbsFinanciero_PRODUCTION_SANDBOX_COPY`, trailing-space, case variant y empty fallan antes de reset/exec/endpoint. |
| F-0252-03 gate npm reproducible | PASA | En clon limpio, `npm ci --prefix apps/nova-web` exit 0 seguido por `npm test --prefix apps/nova-web` exit 0. |
| `paridad_exec_vs_endpoint` pass/fail/NA | PASA | Tests existentes cubren pass y NA; payload propio con filas divergentes devuelve `fail`. |
| Reset entre brazos | PASA | Orden observado en pass y fail: `reset`, `exec:Budget.Get_Budget_Execution_Report`, `reset`, `endpoint:/api/budget/execution-report`. |
| Sin side effects antes de guard | PASA | En todos los negativos de base y rol, `database.Calls` queda vacio. |
| Annul_* fuera de alcance | PASA | Solo aparecen como exclusion documental; no estan en la superficie ejecutada del harness. |
| Sin secretos commiteados | PASA | El codigo usa `NOVA_BUDGET_PARITY_CONNECTION_STRING` y `NOVA_BUDGET_SANDBOX_RESET_SQL`; no hay connection string concreta en los cambios revisados. |
| Live SQL contra sandbox real | RIESGO DECLARADO | No ejecutado por falta de secretos y reset SQL; el resultado vivo queda correctamente declarado como pendiente/NA, no como prueba de paridad real. |

## Residuales

- La paridad viva contra `DbsFinanciero_SANDBOX` sigue pendiente hasta que el operador provea
  `NOVA_BUDGET_PARITY_CONNECTION_STRING` y `NOVA_BUDGET_SANDBOX_RESET_SQL`.
- Warning NU1903 en Microsoft.OpenApi sigue presente y no bloquea este cierre.
- La recomendacion DBA documental conserva el patron `IF DB_NAME() NOT LIKE '%SANDBOX%' THROW`, que esta en el AC original como relay fuera del hub. No la cuento como guard de la aplicacion; el harness ya exige exactitud.

## Recomendacion

OK / CERRABLE. El fix-loop de TASK-0252 remediation 1 puede cerrarse si Arquitecto ratifica el alcance y mantiene el
residual de live SQL como pendiente hasta tener secretos.

task_id: TASK-0252
status: OK/CERRABLE
executive_summary: La remediacion cierra los tres bloqueantes previos: rol SQL real validado, base exacta antes de side effects y gate npm reproducible en clon limpio.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0252-remediation-1-veredicto.md; prueba adversarial temporal BudgetParityHarnessAnalistaAdversarialTests.cs en clon limpio
gates: dotnet test exit 0; npm ci exit 0; npm test exit 0; adversarial payloads exit 0; protocolo validate/encoding/domain/drift/#4 exit 0
next_recommended: Arquitecto puede cerrar TASK-0252 dejando live SQL como residual pendiente de secretos.
risks: Live SQL parity no fue ejecutada; si el operador entrega secretos/reset SQL, requiere corrida viva antes de usar el harness como evidencia de paridad real.
