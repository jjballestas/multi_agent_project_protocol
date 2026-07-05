# ANALISTA VEREDICTO - TASK-0252 harness paridad exec-vs-endpoint

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO / NO CERRABLE.

Ancla canonica revisada:
- Protocolo HEAD/instruccion: d2ab042600c54614ed42680866d69dc9d63dfa12.
- Producto Nova-Budget: dc04bd8a820069de9fcce0879010a65b50057c56.
- Tarea: Area_comun/tasks/TASK-0252-harness-paridad-exec-vs-endpoint-sandbox.md.
- Handoff: Area_comun/handoffs/HANDOFF-TASK-0252-codex-to-arquitecto-1.md.

La infraestructura basica existe y varios comportamientos pasan, pero el gate formal no cierra: el harness no
verifica de forma ejecutable que la conexion use el rol budget_sandbox_verifier y su guard de base de datos acepta
cualquier nombre que contenga SANDBOX, no el sandbox canonico DbsFinanciero_SANDBOX. Ese escape permite que una base
no canonica pase antes de ejecutar paridad.

## Reproduccion

Producto, clon limpio:

| Gate | Comando | Exit | Resultado |
|---|---:|---:|---|
| checkout | git clone D:/Agentes/Zeus/NOVA/Nova-Budget %TEMP%/nova-budget-review-0252-*; git checkout dc04bd8 | 0 | HEAD dc04bd8a820069de9fcce0879010a65b50057c56 |
| dotnet | dotnet test NOVA.sln | 0 | 26 tests pass; warning NU1903 Microsoft.OpenApi |
| npm raw | npm test --prefix apps/nova-web | 1 | falla porque tsc no esta instalado en el clon limpio |
| npm con deps | npm install --prefix apps/nova-web; npm test --prefix apps/nova-web | 0 | 1 test pass |
| adversarial | dotnet test tests/NOVA.IntegrationTests/NOVA.IntegrationTests.csproj --filter FullyQualifiedName~BudgetParityHarnessAdversarialTests | 1 | 1 pass, 1 fail: no rechazo de DbsFinanciero_PRODUCTION_SANDBOX_COPY |

Protocolo:

| Gate | Exit | Resultado |
|---|---:|---|
| python scripts/validate_collaboration_state.py (vivo, con secretos locales) | 0 | OK |
| python scripts/validate_collaboration_state.py (clon limpio sin secretos/untracked) | 0 | OK |
| python scripts/scan_domain_neutrality.py (vivo y clon limpio) | 0 | sin hallazgos impresos |
| python scripts/scan_encoding.py (vivo y clon limpio) | 0 | OK |
| drift vivo | 0 | has_drift False, up_to_seq 3986, entries 0 |
| drift clon limpio | 0 | has_drift False, up_to_seq 3986, entries 0 |
| chain vivo/clon limpio | 0 | chain valid, checked_events 3314 |
| #4 byte-identica | 0 | protocol.config.json sin diff contra HEAD, sha256 2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354 |

## Tabla vector por vector

| Vector / AC | Estado | Evidencia |
|---|---|---|
| Usa rol budget_sandbox_verifier contra DbsFinanciero_SANDBOX, nunca produccion | SLIPS | `RequiredRole` es una constante y la doc nombra el rol, pero `SqlBudgetSandboxDatabase` no consulta `IS_ROLEMEMBER`, `CURRENT_USER`, login, ni user efectivo. El harness acepta cualquier connection string si `DB_NAME()` contiene SANDBOX. |
| Guard de sandbox | SLIPS | Payload propio `DbsFinanciero_PRODUCTION_SANDBOX_COPY` no lanza excepcion. La prueba adversarial esperaba fail-closed y fallo con `Assert.Throws() Failure: No exception was thrown`. |
| Columna paridad_exec_vs_endpoint pass/fail/NA | PASA | Test existente cubre pass y NA. Payload propio con filas divergentes devuelve `fail`. |
| Reset de linea base entre brazos | PASA | Orden observado: reset, exec, reset, endpoint. |
| Annul_Availability_Certificate / Annul_Commitment ausentes | PASA | Solo aparecen como exclusion en docs; no estan en la superficie ejecutada del harness. |
| Sin secretos hardcodeados | PASA | No encontre password ni connection string concreta; usa `NOVA_BUDGET_PARITY_CONNECTION_STRING` y `NOVA_BUDGET_SANDBOX_RESET_SQL`. |
| Live SQL contra DbsFinanciero_SANDBOX | RIESGO DECLARADO | No ejecutado por falta de connection string y reset SQL secretos. Correcto declararlo como pendiente; no debe presentarse como verificado. |
| Gates producto | SLIPS | `dotnet test NOVA.sln` pasa. `npm test --prefix apps/nova-web` en clon limpio falla sin instalar dependencias; tras `npm install --prefix apps/nova-web`, pasa. |
| Gates protocolo | PASA | validate con/sin secretos, encoding, domain, drift 0, chain valid y #4 byte-identica pasan. |

## Hallazgos bloqueantes

F-0252-01 - Rol no verificado por comportamiento.

El AC dice que el harness usa el rol `budget_sandbox_verifier`. La implementacion solo devuelve ese texto en
`BudgetParityResult.RequiredRole`. No hay prueba ni consulta SQL que falle si la connection string apunta a otro
usuario con permisos mas amplios. Remediacion esperada: antes de ejecutar reset/exec/endpoint, validar el contexto SQL
real con una consulta fail-closed, por ejemplo `IS_ROLEMEMBER('budget_sandbox_verifier') = 1` y base exacta, sin exponer
secretos. Agregar negativo con conexion/abstraccion sin rol y positivo con rol.

F-0252-02 - Guard de base de datos demasiado laxo.

`RunAsync` usa `databaseName.Contains("SANDBOX", StringComparison.OrdinalIgnoreCase)`. El payload
`DbsFinanciero_PRODUCTION_SANDBOX_COPY` pasa el guard y permite seguir a reset/exec/endpoint. El intake exige
`DbsFinanciero_SANDBOX` y nunca produccion. Remediacion esperada: comparar contra el nombre canonico exacto o contra
una allowlist explicita gobernada, y agregar negativos para nombres que contienen SANDBOX pero no son el sandbox
canonico.

F-0252-03 - Gate npm no es reproducible como comando crudo de clon limpio.

`npm test --prefix apps/nova-web` salio 1 en el clon limpio porque `tsc` no existe hasta instalar dependencias. Con
`npm install --prefix apps/nova-web`, el mismo gate pasa. Remediacion esperada: documentar y usar el comando completo
reproducible (`npm ci`/`npm install` + test) o ajustar el gate esperado; no presentar el comando crudo como verde.

## Residuales

- La paridad SQL viva sigue pendiente hasta disponer de `NOVA_BUDGET_PARITY_CONNECTION_STRING` y
  `NOVA_BUDGET_SANDBOX_RESET_SQL` desde secreto. Es residual aceptable solo si queda declarado como pendiente.
- La advertencia NU1903 de Microsoft.OpenApi no bloquea este gate.

## Recomendacion

CAMBIO-REQUERIDO. Fix-loop esperado: remediar F-0252-01/F-0252-02/F-0252-03, re-ejecutar dotnet/npm en clon limpio,
gates de protocolo con/sin secretos, drift 0, scan_domain_neutrality, scan_encoding, #4 byte-identica y re-juicio
Analista previo al commit de cierre. Maximo 2 iteraciones antes de escalar al operador.

task_id: TASK-0252
status: CAMBIO-REQUERIDO
executive_summary: El harness existe, resetea entre brazos y produce pass/fail/NA, pero no verifica el rol SQL real y acepta nombres no canonicos que solo contienen SANDBOX; no es cerrable.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0252-harness-paridad-veredicto.md; prueba adversarial temporal en clon limpio BudgetParityHarnessAdversarialTests.cs
gates: dotnet test exit 0; npm raw exit 1; npm con install exit 0; adversarial exit 1; protocolo validate/encoding/domain/drift/chain/#4 exit 0
next_recommended: Remediar rol real, guard exacto de DbsFinanciero_SANDBOX y gate npm reproducible; solicitar re-juicio Analista.
risks: Live SQL no fue ejecutado por falta de secretos; no debe contarse como verificacion de paridad viva.
