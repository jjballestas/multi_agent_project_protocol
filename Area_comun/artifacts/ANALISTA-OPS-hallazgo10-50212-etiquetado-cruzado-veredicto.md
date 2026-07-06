# Veredicto Analista - Hallazgo #10 THROW 50212 etiquetado cruzado

Firma: Analista
Fecha: 2026-07-07
Ancla protocolo revisada: `d33f005b4f8e973d78de4e3f0080292c97213fa0`
Commit protocolo que introdujo la instruccion: `a2657d548b89bde064d6456f18e55aeb743e88b9`
Ancla producto revisada: `edbc037be8ce8297fbf308f611eef8c84aeccbf0`
Instruccion: `Area_comun/mailbox/open/MSG-20260706-Arquitecto-to-Analista-ACTION-hallazgo10-50212-etiquetado-cruzado.md`

## Veredicto

CONFIRMADO con una salvedad canonica. El hallazgo #10 es real como QA no-bloqueante: `BudgetProcedureProblemDetails.Map` es un switch unico usado por las tres superficies revisadas, `50212` cae en `RN-A01` disponibilidad, y `RN-01` apropiacion solo contiene `50230 or 50231`. Si `POST /api/budget/appropriation-modifications/` recibe un `BudgetProcedureException` numero `50212`, la respuesta conserva HTTP 409 y `sqlErrorNumber=50212`, pero devuelve titulo y `businessRule` de disponibilidad.

Cambio requerido acotado: no confirmo la afirmacion "ya documentado con transparencia total" en el ancla canonica del producto, porque `docs/documentacion-tecnica/diccionario-datos.html` y `docs/documentacion-tecnica/log-cambios.html` no existen en `git ls-tree -r HEAD` del clon limpio `edbc037b`. Si esos HTML son generados o locales, no quedan atestados por el commit citado.

Recomendacion de cierre: CAMBIO-REQUERIDO para la asercion documental canonica, pero CERRABLE para registrar el hallazgo #10 como QA no-bloqueante. No lo trato como bloqueo de una tarea de implementacion en curso: el defecto confirmado afecta etiquetado legible/businessRule, no status HTTP ni numero SQL crudo.

## Reproduccion

| Comando | Resultado |
|---|---:|
| `git fetch origin` en protocolo | 0 |
| `git status --short` en protocolo | 0 para lectura; arbol local con cambios ajenos no tocados |
| `python scripts/validate_collaboration_state.py` en protocolo vivo | 0 |
| `git clone D:/Agentes/Zeus/NOVA/Nova-Budget <tmp>` | 0 |
| `git -C <tmp> checkout edbc037be8ce8297fbf308f611eef8c84aeccbf0` | 0 |
| `npm test` en raiz del clon producto | 1, npm errno `-4058`, no existe `package.json` raiz |
| `dotnet test tests/NOVA.ArchitectureTests` en clon producto | 0, 10/10 |
| Probe propio por reflexion de `BudgetProcedureProblemDetails.Map` | 0 |
| `git ls-tree -r HEAD` buscando `docs/documentacion-tecnica/*.html` | 0, sin hits |
| `python scripts/validate_collaboration_state.py` vivo | 0 |
| `python scripts/validate_collaboration_state.py` en clon limpio sin `secrets/` | 0 |
| `python scripts/scan_domain_neutrality.py` vivo y clon limpio | 0 |
| `python scripts/scan_encoding.py` vivo y clon limpio | 0 |
| `python -m runtime.protocol_replay --check` vivo y clon limpio | 0 |
| Drift runtime | 0 drift, `up_to_seq=4395` |
| Chain runtime | valida, `checked_events=3723` |
| `protocol.config.json` byte-identico | sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vector por vector

| Vector / AC a refutar | Evidencia independiente | Resultado |
|---|---|---|
| Switch unico compartido por las tres superficies | `Program.cs` llama `BudgetProcedureProblemDetails.Map(exception.Number)` en `appropriation-modifications` linea 198, `availability-adjustments` linea 254 y `availability-certificates/annul` linea 312. | PASA |
| `50212` solo esta en `RN-A01` | La unica ocurrencia productiva de `50212` en `Program.cs` es linea 500: `50250 or 50251 or 50212 => ... RN-A01 ... 409`. | PASA |
| `RN-01` ya no incluye `50212` | Linea 513: `50230 or 50231 => ... RN-01 ... 409`; no incluye `50212`. | PASA |
| Comportamiento real de `Map(50212)` | Probe por reflexion sobre `NOVA.Api` devuelve `50212|Fiscal year is not open for availability adjustment|RN-A01|409`. | SLIPS confirmado |
| Familia de codigos vecinos conserva su etiqueta esperada | Probe propio: `50230` y `50231` devuelven `RN-01`; `50250` y `50251` devuelven `RN-A01`; `50282` devuelve `RN-08-YEAR`; `50100` devuelve `TENANT`; desconocido devuelve `UNKNOWN`. | PASA |
| Arquitectura con build limpio | `dotnet test tests/NOVA.ArchitectureTests` recompila/restaura y termina con 10 superados, 0 fallidos. | PASA |
| `npm test` raiz obligatorio transversal | Falla por ausencia de `package.json`; no refuta el hallazgo C#/API, pero el gate transversal no queda verde. | RIESGO DECLARADO |
| Asercion "ya documentado en HTML" | En clon limpio del commit citado no existen `docs/documentacion-tecnica/diccionario-datos.html` ni `docs/documentacion-tecnica/log-cambios.html`; `git ls-tree -r HEAD` no muestra esas rutas. | SLIPS documental |

## Clasificacion

- Tipo: QA / etiquetado de error cruzado entre superficies.
- Severidad: WARNING-real no bloqueante. El uso normal que dispare `50212` desde apropiacion muestra etiqueta/titulo equivocado, pero mantiene HTTP 409 y `sqlErrorNumber` correcto.
- No lo clasifico como seguridad.
- No cierro ninguna tarea: este veredicto registra el hallazgo y pide correccion documental o ancla canonica si la documentacion existe fuera del commit revisado.

## Residuales

- No ejecute una llamada HTTP real contra SQL Server: la instruccion pedia lectura/probe del mapper y test de arquitectura; no habia credenciales ni fixture canonico para forzar el trigger `50212` desde apropiacion.
- `npm test` raiz sigue siendo un gate transversal no reproducible en este producto porque no hay `package.json` raiz.
- Si los HTML existen como artefactos generados no versionados, deben publicarse o citarse por hash/ruta canonica antes de usarlos como atenuante.

## Envelope

task_id: OPS-HALLAZGO-10
status: CONFIRMADO-CAMBIO-REQUERIDO-DOCUMENTAL
executive_summary: Hallazgo #10 confirmado como QA no-bloqueante; `50212` mapea a `RN-A01` disponibilidad aunque puede emerger por apropiacion, pero la documentacion HTML citada no existe en el commit producto canonico.
artifacts: Area_comun/artifacts/ANALISTA-OPS-hallazgo10-50212-etiquetado-cruzado-veredicto.md
gates: validate vivo 0; validate sin secretos 0; domain 0; encoding 0; drift 0 up_to_seq=4395; chain valid checked_events=3723; protocol.config byte-identico; producto dotnet ArchitectureTests 0 10/10; producto npm raiz 1 errno -4058 residual.
next_recommended: Registrar #10 como QA no-bloqueante y remediar/canonizar la evidencia documental; fix sugerido: separar `50212` en rama neutral o mapear por superficie antes de publicar el cierre documental.
risks: Sin prueba HTTP+SQL real del trigger; docs HTML pueden existir fuera de git pero no estan atestadas por el commit citado; root npm test no aplica hasta definir gate canonico para este repo.
