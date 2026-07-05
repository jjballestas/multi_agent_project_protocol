---
message_id: MSG-20260705-Operador-to-Arquitecto-FYI-reset-sandbox-entregado-desbloquea-F-NOVA-01
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - "D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/DATA/sandbox-reset-mutator-baseline.sql"
  - "D:/Agentes/Zeus/NOVA/Nova-Budget/docs/budget-parity-harness.md"
  - MSG-20260705-Codex-to-Arquitecto-TASK-0253-remediation-1-in-review (el block de F-NOVA-01)
one_line_summary: "El Operador entrego el RESET no-admin del harness (Budget.Reset_Sandbox_Mutator_Baseline) = la pieza NOVA_BUDGET_SANDBOX_RESET_SQL que TASK-0253 (P4.1) necesitaba. Revision del Asesor: PASA (guard DB_NAME 51011, non-admin corre como budget_sandbox_verifier, SESSION_CONTEXT tenant obligatorio 50100, scoped por task_id/prefix, restaura a estado PREVIO via previous_* -- determinista, @dry_run, sin secretos; cuadre validado: RP 491 + CDP 436 -> 'G', is_active=1, saldo 2950000.0000, sin filas de reverso). Grant surface ahora 108 (18 EXECUTE + 90 SELECT; +1 el Reset). ACCION: (1) registra la ENMIENDA FECHADA del grant (+1 Reset). (2) el harness de paridad debe setear ANSI_NULLS ON + QUOTED_IDENTIFIER ON + SESSION_CONTEXT tenant_id, y llamar el reset POR task_id ENTRE corridas (aislamiento determinista). (3) VERIFICA la OTRA mitad del block: esta NOVA_BUDGET_PARITY_CONNECTION_STRING (login nova_budget_verifier) en el entorno de Codex? Si ambas estan -> DESBLOQUEA TASK-0253 (blocked->in_progress) para que Codex corra F-NOVA-01 y cierre P4.1; si falta la connection string, ese es el gap restante del operador."
requested_action: "[DIRECTIVA/FYI] El Operador entrego el RESET no-admin que faltaba para F-NOVA-01: Budget.Reset_Sandbox_Mutator_Baseline (desplegado en DbsFinanciero_SANDBOX). Es la pieza NOVA_BUDGET_SANDBOX_RESET_SQL que Codex pidio para desbloquear TASK-0253 (P4.1). REVISION DEL ASESOR (study-integrity + diseno): PASA. Verificado: (a) guard DB_NAME() NOT LIKE '%SANDBOX%' -> THROW 51011 (fail-closed, no corre en prod); (b) NON-ADMIN: corre como budget_sandbox_verifier (mismo rol restringido del harness, no admin); (c) SESSION_CONTEXT('tenant_id') obligatorio -> THROW 50100; (d) SCOPED por @task_id / @task_id_prefix / @artifact_code_prefix -> revierte SOLO lo que ese task_id toco (aislamiento, no arrasa el sandbox); (e) restaura a estado PREVIO via columnas previous_* (previous_is_active/previous_updated_at/previous_movement_status_catalog_id) -> reset DETERMINISTA, no reactivate ciego; (f) @dry_run=1 soportado; (g) SIN secretos en el script (escaneado); (h) ANSI_NULLS ON + QUOTED_IDENTIFIER ON al crear el proc (fix del bloqueo por columnas computadas/indices). VALIDACION del operador (non-admin, nova_budget_verifier): anulo RP 491 + CDP 436 -> reset por task_id -> ambos a 'G', is_active=1, saldo 2950000.0000, lineas activas restauradas, cero filas de reverso para el task_id. NOTA de disciplina: el operador limpio el acto de anulacion de su primera prueba USANDO EL RESET (no intervencion manual sobre tablas) -> respeta 'toda mutacion via proc gobernado'. ACCIONES: (1) REGISTRA la ENMIENDA FECHADA del grant surface del sandbox (+1 EXECUTE: Reset_Sandbox_Mutator_Baseline; total 108) -- misma via que los Annul (sello s.5). (2) HARNESS: cuando Codex cablee/corra la paridad, la sesion debe setear ANSI_NULLS ON + QUOTED_IDENTIFIER ON (para casar con el proc y evitar el mismo fallo) + SESSION_CONTEXT tenant_id, y llamar Budget.Reset_Sandbox_Mutator_Baseline @task_id=... ENTRE corridas de paridad (asegura repetibilidad; una corrida no contamina a la otra). Uso documentado en NOVA/Nova-Budget/docs/budget-parity-harness.md. (3) VERIFICA LA OTRA MITAD DEL BLOCK: Codex pidio DOS cosas -- el RESET (ya entregado) y NOVA_BUDGET_PARITY_CONNECTION_STRING (login nova_budget_verifier). Confirma si esa connection string esta ahora en el ENTORNO de Codex (env/secret store, NUNCA el repo). SI AMBAS estan presentes -> DESBLOQUEA TASK-0253 (blocked -> in_progress) para que Codex corra F-NOVA-01 (los 8 criterios + THROW re-verificados contra el proc desplegado) y cierre P4.1 con su fila CLOSE + tokens. SI la connection string sigue ausente -> ese es el unico gap restante y es del operador (avisale por el resumen *-to-Operador-*). FRONTERA: el Reset es TEST-INFRA (fuera del estudio medido, como el harness), no una unidad medida ni un proc de producto. RESPONDE con: (a) enmienda fechada del grant (+1 Reset) registrada; (b) esta la connection string en el entorno de Codex? (c) TASK-0253 desbloqueada o queda el gap de la connection string."
question: ""
---

# FYI/DIRECTIVA - Reset no-admin del harness entregado (desbloquea F-NOVA-01 de P4.1)

El Operador entrego la pieza que faltaba para F-NOVA-01: **`Budget.Reset_Sandbox_Mutator_Baseline`**
(desplegado en `DbsFinanciero_SANDBOX`), el `NOVA_BUDGET_SANDBOX_RESET_SQL` que Codex pidio para
desbloquear TASK-0253 (P4.1).

## Revision del Asesor: PASA
- Guard `DB_NAME()` -> THROW 51011 (fail-closed) | **non-admin** (corre como `budget_sandbox_verifier`).
- `SESSION_CONTEXT('tenant_id')` obligatorio (THROW 50100) | **scoped por task_id** (aisla, no arrasa).
- Restaura a estado **PREVIO** via `previous_*` (determinista, no reactivate ciego) | `@dry_run` | **sin secretos**.
- `ANSI_NULLS/QUOTED_IDENTIFIER ON` (fix del bloqueo por columnas computadas).
- **Validado** (non-admin): RP 491 + CDP 436 -> 'G', is_active=1, saldo 2950000.0000, sin filas de reverso.
- El operador limpio su prueba **con el reset**, no manual -> respeta 'toda mutacion via proc gobernado'.

## Acciones
1. **Enmienda fechada** del grant surface: +1 EXECUTE (`Reset_Sandbox_Mutator_Baseline`), total **108**.
2. **Harness:** setear `ANSI_NULLS ON` + `QUOTED_IDENTIFIER ON` + `SESSION_CONTEXT tenant_id`; llamar el reset **por task_id ENTRE corridas** de paridad. Uso en `NOVA/Nova-Budget/docs/budget-parity-harness.md`.
3. **Verifica la otra mitad:** esta `NOVA_BUDGET_PARITY_CONNECTION_STRING` (login `nova_budget_verifier`) en el **entorno de Codex**? Si ambas estan -> **DESBLOQUEA TASK-0253** (blocked->in_progress) para F-NOVA-01 + cierre de P4.1. Si falta -> gap del operador.

## Frontera
El Reset es **test-infra** (fuera del estudio medido, como el harness), no unidad medida ni proc de producto.

## Responde
(a) enmienda fechada (+1 Reset) registrada; (b) connection string en entorno de Codex?; (c) TASK-0253 desbloqueada o queda el gap.
