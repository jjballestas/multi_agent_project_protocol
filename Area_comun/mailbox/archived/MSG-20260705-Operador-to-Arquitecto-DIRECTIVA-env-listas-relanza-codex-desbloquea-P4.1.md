---
message_id: MSG-20260705-Operador-to-Arquitecto-DIRECTIVA-env-listas-relanza-codex-desbloquea-P4.1
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - MSG-20260705-Operador-to-Arquitecto-FYI-reset-sandbox-entregado-desbloquea-F-NOVA-01 (el reset)
  - MSG-20260705-Codex-to-Arquitecto-TASK-0253-remediation-1-in-review (el block de F-NOVA-01)
one_line_summary: "AMBAS variables del harness ya estan configuradas en el ENTORNO DE USUARIO DE WINDOWS (el secreto vive SOLO ahi, no en archivos del repo ni auxiliares). NOVA_BUDGET_PARITY_CONNECTION_STRING (Server=localhost,1433; Database=DbsFinanciero_SANDBOX; User Id=nova_budget_verifier; Encrypt=True; TrustServerCertificate=True) + NOVA_BUDGET_SANDBOX_RESET_SQL (EXEC Budget.Reset_Sandbox_Mutator_Baseline @task_id=@taskId). VALIDADO por el DBA con el login de bajo privilegio: conexion OK + dry_run del reset con SESSION_CONTEXT tenant_id=1 -> conteos en cero, sin mutar. CUIDADO OPERATIVO: los procesos ya abiertos NO recargan las env vars de usuario -> hay que RELANZAR el proceso/scheduler de Codex para que el cron las vea. ACCION: relanza el cron de Codex -> DESBLOQUEA TASK-0253 (blocked->in_progress) -> Codex corre F-NOVA-01 (8 criterios + THROW re-verificados contra el proc desplegado, reset por task_id entre corridas, sesion con ANSI_NULLS/QUOTED_IDENTIFIER ON + tenant_id) -> P4.1 cierra con fila CLOSE + tokens (--corpus explicito). El secreto no se entrega en ningun reporte; solo se confirma presencia."
requested_action: "[DIRECTIVA] Se resolvio la OTRA mitad del block de F-NOVA-01: el DBA del Operador configuro AMBAS variables del harness en el ENTORNO DE USUARIO DE WINDOWS (el secreto vive SOLO en esa env var; NO en archivos del repo ni auxiliares; no se registra el valor en ningun reporte/mailbox). VARIABLES: (1) NOVA_BUDGET_PARITY_CONNECTION_STRING -> Server=localhost,1433; Database=DbsFinanciero_SANDBOX; User Id=nova_budget_verifier; Password=*** (solo en la env var de usuario); Encrypt=True; TrustServerCertificate=True; Application Name=NOVA Budget Parity Harness. (2) NOVA_BUDGET_SANDBOX_RESET_SQL -> 'EXEC Budget.Reset_Sandbox_Mutator_Baseline @task_id = @taskId;'. VALIDACION del DBA (login de bajo privilegio nova_budget_verifier): conexion OK contra DbsFinanciero_SANDBOX; dry_run del reset con SESSION_CONTEXT('tenant_id')=1 -> respondio con conteos en cero, SIN mutar datos. ACCIONES: (1) CUIDADO OPERATIVO -- los procesos ya abiertos NO recargan las variables de entorno de usuario de Windows; RELANZA el proceso/scheduler/cron de Codex para que las recoja (si el relanzamiento del cron tiene gate de permisos, pidelo). (2) DESBLOQUEA TASK-0253 (blocked -> in_progress) para que Codex corra la verificacion F-NOVA-01 en vivo: los 8 criterios Given/When/Then de SPEC-NOVA-P4-001 s.7 contra DbsFinanciero_SANDBOX + cada THROW (50230-50243, 50212, 50065) re-verificado falsable contra OBJECT_DEFINITION del proc DESPLEGADO; el harness debe setear ANSI_NULLS ON + QUOTED_IDENTIFIER ON + SESSION_CONTEXT tenant_id, y llamar Budget.Reset_Sandbox_Mutator_Baseline @task_id=... ENTRE corridas (repetibilidad). (3) Al cerrar P4.1: CAPTURA la fila CLOSE con tokens_total_atribuibles (del err.log ANTES de rotar) via medicion_ledger.py --corpus EXPLICITO -- NO repetir el hueco; el patron de la familia ajustes se congela al arrancar PAR-1. SEGURIDAD: el secreto solo vive en la env var de usuario de Windows (canal acordado para evitar archivos con credenciales); Codex/tu NO manejan el valor, solo confirman presencia; nada de secretos al repo/mailbox. NOTA menor: TrustServerCertificate=True es aceptable SOLO por ser localhost/sandbox (no es patron de prod). RESPONDE con: (a) cron de Codex relanzado (recoge las env vars); (b) TASK-0253 desbloqueada -> in_progress; (c) resultado de F-NOVA-01 (8 criterios + THROW) y si P4.1 cerro con su fila CLOSE + tokens."
question: ""
---

# DIRECTIVA - Env vars listas -> relanza Codex -> desbloquea P4.1

Se resolvio la otra mitad del block. El DBA configuro **ambas variables en el entorno de usuario de
Windows** (el secreto vive SOLO ahi; no en archivos del repo ni auxiliares; no se registra el valor).

## Variables (validadas por el DBA)
- `NOVA_BUDGET_PARITY_CONNECTION_STRING` -> `localhost,1433 / DbsFinanciero_SANDBOX / nova_budget_verifier / Encrypt=True / TrustServerCertificate=True`.
- `NOVA_BUDGET_SANDBOX_RESET_SQL` -> `EXEC Budget.Reset_Sandbox_Mutator_Baseline @task_id = @taskId;`.
- Validacion: conexion OK (login bajo privilegio) + dry_run del reset con `tenant_id=1` -> conteos en cero, **sin mutar**.

## Acciones
1. **CUIDADO OPERATIVO:** los procesos abiertos NO recargan env vars de usuario -> **RELANZA el cron/scheduler de Codex** para que las vea (si el relanzamiento tiene gate de permisos, pidelo).
2. **DESBLOQUEA TASK-0253** (blocked -> in_progress) -> Codex corre **F-NOVA-01** (8 criterios + THROW re-verificados contra el proc desplegado; sesion con `ANSI_NULLS/QUOTED_IDENTIFIER ON` + `tenant_id`; reset por task_id **entre corridas**).
3. Al cerrar P4.1: **captura la fila CLOSE con tokens** (err.log antes de rotar) via `medicion_ledger.py --corpus` explicito; congela el patron ajustes para PAR-1.

## Seguridad
El secreto vive SOLO en la env var de usuario de Windows (canal acordado). Codex/tu **no manejan el valor**, solo confirman presencia. Nada al repo/mailbox. `TrustServerCertificate=True` aceptable SOLO por localhost/sandbox.

## Responde
(a) cron de Codex relanzado; (b) TASK-0253 -> in_progress; (c) resultado F-NOVA-01 + P4.1 cerro con CLOSE + tokens?
