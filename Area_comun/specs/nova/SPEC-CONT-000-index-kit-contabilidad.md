# SPEC-CONT-000 - Indice del kit SPEC-CONT de Contabilidad (PREP, patron NOVA-SPEC-T-001 / Presupuesto)

> Kit de SPECs de superficie del modulo Contabilidad de la suite Nova, instanciado por el Arquitecto FUERA de la
> ventana medida como PREP de Sprint 1 (DIRECTIVA Operador 2026-07-11, GO commit 9d10d86 via Asesor: "escribir NO
> construir"). Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084), mismo patron congelado que
> las SPEC-NOVA-P4-00x de Presupuesto (referencia de forma: SPEC-NOVA-P4-006). Fuente design-source
> (D:/Agentes/Ingenas, FUERA del hub): WS1 (accounting_ws1_base_solida.html, F-NOVA-01 re-verificado 2026-07-10) +
> SDD (accounting_module_requirements.html). Las SPEC-CONT NO se implementan antes del 30-jul.

## Frontera (recordatorio duro)
- **PREP / design-source.** Este kit SE ESCRIBE, no se construye. NO promueve tareas de build; NO activa
  SESSION_CONTEXT desde la API; NO toca el estudio medido, el baseline congelado ni el core pineado del hub
  (epoch 1.14.0). Los procs de hardening (schema/010-028) YA EXISTEN, desplegados + verificados por el DBA en las
  3 BD (DbsFinanciero, DbsFinanciero_SANDBOX, SNJDC); cada SPEC-CONT cubre SOLO la superficie C#/API(+UI) sobre el
  proc, que es la unidad medida.
- **BUILD gobernado gated** por (Julian onboardeado + base promovida al hub/instancia + calendario Sprint 1
  post-30-jul). Nota: el onboarding nominal de Julian (re-genesis A2 de Aegis) esta en BLOCKER tecnico separado
  (ver MSG-BLOCKER-regenesis-A2-chain-reanchor); no afecta a este kit PREP.
- **Colocacion:** hub `Area_comun/specs/nova/` (junto a las SPEC-NOVA-P4-00x de Presupuesto; la gobernanza/SPECs
  viven en el hub, DECISION-0050 #1). El build de producto ira al repo de la instancia cuando abra.

## Slices (mapa R1-R8 del SDD dado por el operador; 6C es frontera del modulo fuente)

| Slice | SPEC-CONT | Unidad | Objeto(s) NOVA principal(es) | THROW real (F-NOVA-01, seccion D WS1) | schema | Estado SPEC |
|---|---|---|---|---|---|---|
| S1 | SPEC-CONT-S1 | Reportes y consultas RO | 11 `Get_*_Report` + `Get_Bank_Retention_Crossing_Report` | 52700-707, 52800-810, 52900-908, 53000-005, 53100-110, 53200-206, 53300-306, 53400-406, 53500-506, 53600-607, 53700-708; 51000-004 (modelado) | reports/025-035, reports/020 | ESCRITA |
| S2 | SPEC-CONT-S2 | Comprobante manual + correcciones | `Post_Voucher`/`Post_Voucher_Draft` (12 triggers), `Reverse_Voucher`, `Get_Next_Accounting_Source_Number` | Post_Voucher 52230-247,52252; Draft 52250-251; trg_validate 52200-204; Reverse 52600-607; terceros 52300-321; fuente 52100-102 | 015,024,010,021 | PEND |
| S3 | SPEC-CONT-S3 | Cierre/apertura mensual (P03-P07) | `Validate/Close/Open_Accounting_Period`, `trg_voucher__date_controls` | 53800-804, 53820-826, 53840-844, 53860-867; date controls 52510-514 | 025,023 | PEND |
| S4 | SPEC-CONT-S4 | Saldos iniciales de vigencia | `Create/Validate/Approve/Import_Opening_Balance_Draft`, `Convert_Auxiliary_To_Major` | 52400-452 (52420-21, 52430-37, 52440-43, 52450-52); 52300-313 | 022,021 | PEND |
| S5 | SPEC-CONT-S5 | CHIP contingencia | `Create_Chip_Report_Balance_Batch`, `Get_Chip_Reconciliation_Difference`, `Post_Chip_Adjustment_Voucher` | 53900-910, 53920-923, 53940-953 | 026 | PEND |
| S6A | SPEC-CONT-S6A | Informe trimestral CGN/CHIP | `Import_Cgn_Chip_Valid_Account_Catalog`, `Create/Get/Confirm_Cgn_Chip_Quarterly_Report` | 54400-413, 54420-441, 54450-451, 54452-457 (P05) | 027 | PEND |
| S6B | SPEC-CONT-S6B | Cierre anual | `Close_Annual_Accounting_Period` (annual_close via Post_Voucher + saldos iniciales sig. vigencia + P07) | 54460-487 (54480-487 reserva legal privada opcional) | 028 | PEND |
| S6C | SPEC-CONT-S6C | Causacion ingresos/CxC (FRONTERA modulo fuente) | `income_accrual` / `accounts_receivable_accrual` | (build del modulo fuente, NO Contabilidad) | -- | PEND (spec-frontera) |

## Preambulo compartido (aplica a toda SPEC-CONT; cada slice lo particulariza)
- **Superficie-sobre-proc:** cada unidad es superficie C#/API(+UI) sobre un proc de hardening; C# NO reimplementa
  validacion / saldo / guarda / numeracion / reverso. El proc es autoritativo.
- **F-NOVA-01:** el maker RE-CONFIRMA el set REAL de THROW de cada proc contra `OBJECT_DEFINITION` del proc
  DESPLEGADO (las 3 BD) al construir; los codigos de la seccion D del WS1 (re-verificados 2026-07-10) son el punto
  de partida real, no un rango documentado sin base. Cada criterio negativo cita un THROW ALCANZABLE.
- **Guard de procedencia:** la evidencia F-NOVA-01 se versiona con una clase SQL real, gateada por env vars, NA
  limpio sin credenciales; NINGUN mock/`Recording*` in-memory la sustituye. Checker formal (Analista) + adversarial
  informal lo verifican (guard cazado ya 2x: TASK-0250, TASK-0253).
- **Aislamiento intra-par/familia:** manifiesto explicito de archivos leidos en el DoD; el maker de una unidad no
  lee la implementacion de una hermana isomorfa. Aplica si Contabilidad se mide como pares.
- **Auth real desde el arranque gobernado:** rol + `[Authorize]`/`RequireAuthorization` real (no el supuesto DD-01
  del baseline), heredado del patron gobernado P4-006 (s.6h). Los endpoints MUTADORES exigen rol; sin sesion/rol
  valido, 401/403 ANTES de tocar el proc. Los endpoints RO exigen autenticacion + aislamiento de tenant.
- **Stack obligatorio + anti-patrones PROHIBIDOS:** React+TS+Vite (front sin SQL) / ASP.NET Core .NET en capas +
  NOVA.Mcp / SQL Server via gateways tipados / OpenTelemetry / ProblemDetails. PROHIBIDO: WebForms/PageMethods,
  DataTable entre capas, DLLs manuales, capa DATABASE generica, secretos en `.config`, centinelas -99.
- **Gates (verdes por exit-code):** `dotnet build` limpio + `dotnet test` (unit + arch tests: capas, sin DataTable
  entre capas, front sin SQL, gateway tipado, aislamiento) + integracion HTTP en CLON LIMPIO + F-NOVA-01 real
  (>=1 negativo por THROW alcanzable, clase SQL real) + neutralidad/`scan_encoding` del artefacto. Checker: Analista
  adversarial FORMAL (contexto limpio: SPEC + diff + BD readonly, no la conversacion del maker) + adversarial
  informal en sesion separada.
- **Tenant/auditoria (hallazgo #14, seguridad ALTA):** `SESSION_CONTEXT('tenant_id')` obligatorio + aislamiento de
  tenant DEMOSTRABLE en toda lectura de gateway (filtro explicito `WHERE tenant_id=@tenant_id`, O vista/RLS que
  consuma `SESSION_CONTEXT('tenant_id')` verificado contra `OBJECT_DEFINITION` + `SECURITY POLICY`). NO basta
  `sp_set_session_context` si el objeto leido no lo consume. Usuario real del contexto de auth + correlation-id/
  task_id en cada operacion.

## INVARIANTE DE INTEGRIDAD (escotilla de periodo cerrado -- NO RELAJAR EN NINGUNA SPEC)
El UNICO bypass permitido del control de periodo cerrado es la escotilla `SESSION_CONTEXT('accounting_annual_close')=1`
que SOLO activa `Accounting.Close_Annual_Accounting_Period` (set antes de `Post_Voucher`, reset despues y en CATCH).
Las 3 guardas la aplican con `AND NOT (item='annual_close' AND COALESCE(TRY_CONVERT(int,
SESSION_CONTEXT('accounting_annual_close')),0)=1)`:
- `52204` `trg_voucher__validate_insert`
- `52512` `trg_voucher__date_controls`
- `Post_Voucher` (guarda del set 52230-52247; RE-CONFIRMAR el codigo EXACTO contra `OBJECT_DEFINITION`, propuesto
  ~52233) + `52252` bloquea la captura MANUAL con tipos proc-only como `annual_close`.
Ninguna SPEC-CONT expone, parametriza ni activa esta escotilla desde la API/UI; es INTERNA del proc de cierre anual
(S6B). La captura manual (S2) NUNCA puede fijar `source_type` proc-only (`annual_close`) -> `52252`. Las SPEC de
S2/S3/S6B DECLARAN esta invariante y la verifican con un negativo (captura manual con `annual_close` -> `52252`;
comprobante fuera de periodo sin escotilla -> `52204`/`52512`). El fix de integridad quedo verificado
estaticamente en el design-source; las SPEC lo PRESERVAN, no lo relajan.

## FOLLOW-UP DE ENDURECIMIENTO (declarado, no bypass; backlog PREP-CONTABILIDAD s.4)
Endurecer que la captura manual FIJE `source_module_code='accounting'` para que el `52252` no sea esquivable a
nivel BD (hoy `Post_Voucher_Draft` lo lee del draft). El bypass de periodo cerrado NO depende de esto (lo cubre la
escotilla independientemente). Se instancia como hardening DECLARADO (unidad/criterio en S2) cuando abra el build;
NO como bypass, NO reabre el sello ni el baseline.

## Estado del kit
- ESCRITAS: **S1** (SPEC-CONT-S1-reportes-consultas-ro.md). PEND: S2, S3, S4, S5, S6A, S6B, S6C.
- Se entregan **por slice** (DIRECTIVA operador). Ninguna registrada como tarea de build (PREP). Cuando abra el
  build gobernado, cada SPEC-CONT-Sx se registra como tarea de superficie en el ledger de la instancia (no el hub).
