# SPEC-NOVA-P4-005 - Annul_Availability_Certificate (anulacion de CDP, brecha B-04/RN-08) [miembro de PAR-2, isomorfo con P4-006]

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Miembro de PAR-2 (par
> CONFIRMADO, sello s.13, isomorfo con Annul_Commitment / SPEC-NOVA-P4-006). Sorteo del sello s.23:
> `Annul_Availability_Certificate` = BASELINE; `Annul_Commitment` = GOBERNADO (Sprint 1). El proc es
> HARDENING (construido por el DBA, fuera del estudio medido, regla 8); esta SPEC cubre SOLO la
> superficie C#/API sobre el proc, que SI es la unidad medida. Preparada por el Arquitecto FUERA de la
> ventana medida. Fuente: NOVA-PRES-08 (Reversos y Anulaciones, B-04/RN-08) + NOVA-PRES-04 (CDP) +
> `DRAFT-SPEC-hardening-annul-cdp-compromiso.md` (diseno del Asesor) + FYI-PAR2-hardening-entregado.

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P4-005 - task_id (hub): asignado al registrar la tarea de superficie
- owner_maker: agente desarrollador de la instancia; repo producto Nova-Budget
- checker: adversarial informal de 12 puntos en **SESION SEPARADA / contexto limpio** (dev != adversarial;
  checker_formal=0 en el brazo baseline).
- arm: **PAR-2 BASELINE** (sorteo del sello s.23, empate resuelto por orden alfabetico del nombre real
  del proc SQL) - unit: Annul_Availability_Certificate (anulacion de CDP)
- q4_membership: **DENTRO** (miembro de par del contraste; criticidad media; proc de hardening ya
  existente y verificado por el DBA -- 10/10 pruebas OK).
- **isolation: CRITICA (PAR-2).** Isomorfo con Annul_Commitment. leyo_codigo_hermano = **NO**: esta SPEC
  se redacta SOLO de NOVA-PRES-08/04 + el draft de diseno del Asesor (documento de proceso compartido,
  no implementacion); NO se lee la implementacion del hermano ni su repo. Manifiesto de archivos leidos:
  NOVA-PRES-08/04 + `DRAFT-SPEC-hardening-annul-cdp-compromiso.md` + patron congelado de P4.1/P4.2 (Apply
  atomico, THROW->ProblemDetails, saldo por vista, guard de procedencia). Riesgo: implementar la anulacion
  de Compromiso "de paso" = CONTAMINACION intra-par -> par CONTAMINADO fuera del confirmatorio.
- **PRECONDICION: READY, preflight AMPLIADO YA HECHO.** El proc de hardening YA EXISTE y esta VERIFICADO
  por el DBA (10/10 pruebas en `DbsFinanciero_SANDBOX`: existencia, guarda bloqueante hijos-vivos,
  camino feliz con cuadre CDP, idempotencia, rollback forzado, `SESSION_CONTEXT` faltante). GRANT EXECUTE
  ya concedido. **Preflight ampliado completado (adelantado, ambos miembros del par):** `VIEW DEFINITION`
  sobre `Annul_Availability_Certificate` + `Annul_Commitment` + las 4 tablas de reverso; `SELECT` sobre
  13 tablas base (`Availability_Certificate`+`_Line`+`_Line_Adjustment` + 2 reverso; `Commitment`+
  `_Line`+`_Line_Adjustment` + 2 reverso; `Obligation`; `Core.Fiscal_Year`; `Core.Internal_Catalog`;
  `Security.[User]`). Sin TVP (no requiere `EXECUTE ON TYPE`); sin triggers en las tablas de reverso.
  Smoke real (ROLLBACK, CDP 30/RP 87) confirma procedencia sin errores de permiso. **F-NOVA-01 puede
  proceder sin round-trips** (leccion de TASK-0254 aplicada preventivamente por el DBA).
- **measurement:** cache-confound -> mismo runtime que su pareja de par o declarar; captura de tokens en
  err.log; checker_formal=0 en el brazo baseline.
- **F-NOVA-01 (re-verificacion, CRITICA -- precedente F-0246-02, P4.1, P4.2):** preflight AMPLIADO YA
  HECHO por el DBA (VIEW DEFINITION sobre ambos Annul + 4 tablas de reverso; SELECT sobre 13 tablas base;
  smoke real con ROLLBACK OK, CDP 30/RP 87, 0 residuos) -- **F-NOVA-01 puede proceder sin round-trips de
  permisos.** El `OBJECT_DEFINITION` (leido por el DBA) revela el set REAL, MAS RICO que el smoke/encargo
  original (2a vez que esto pasa -- refuerza la tesis de falsabilidad F-0246-02): **set completo de
  `Annul_Availability_Certificate` = 50100, 50280, 50281, 50282, 50283, 50284, 50285, 50286, 50287** (9
  codigos). El maker RE-CONFIRMA estos 9 contra `OBJECT_DEFINITION` al construir (ya tiene VIEW
  DEFINITION) -- no asumir que son exactamente estos sin re-verificar, pero SON el punto de partida real,
  no un rango documentado sin base.
- **GUARD DE PROCEDENCIA (adoptado tras TASK-0253, sello s.15):** la evidencia F-NOVA-01 debe versionarse
  con una clase SQL real (gateada por env vars, NA limpio sin credenciales) -- NINGUN mock/Recording*
  in-memory con resultados hardcodeados puede sustituirla. El checker adversarial lo verifica
  explicitamente.
- db_verified_at: proc + tablas de reverso verificados por el DBA en `DbsFinanciero_SANDBOX`
  (10/10 pruebas, ver `MSG-20260705-Operador-to-Arquitecto-FYI-PAR2-hardening-entregado-confirmado`
  archivado); el maker RE-VERIFICA contra la BD desplegada (F-NOVA-01) para el set exacto de THROW.
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL
  Server 2025 via gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS:
  WebForms/PageMethods, DataTable entre capas, DLLs manuales, capa DATABASE generica, secretos en .config,
  centinelas -99.

## 1. Objetivo definido
El usuario anula un CDP (Certificado de Disponibilidad Presupuestal) existente mediante una llamada
ATOMICA a `Budget.Annul_Availability_Certificate` (proc de hardening, controlado), que: (a) valida que
NO existan compromisos (RP) activos sobre ese CDP (guarda bloqueante); (b) si pasa la guarda, libera el
monto del CDP de vuelta a la apropiacion vigente, marca el CDP en estado 'A' (anulado, vía MERGE), y
genera el reverso documental/contable correspondiente. Sin reimplementar la guarda ni el reverso de saldo
en C#.
- Fuente: NOVA-PRES-08 (patron RN-08: 3 efectos coordinados + guarda bloqueante) + NOVA-PRES-04 (saldos
  de CDP) + `DRAFT-SPEC-hardening-annul-cdp-compromiso.md` s.3.
- Calidad: falsable. Bien: "anular un CDP que tiene un RP activo encima devuelve ProblemDetails del THROW
  de guarda bloqueante (dentro del set real 50100/50280-50287, RE-CONFIRMAR cual exacto) y NO libera saldo
  ni cambia el estado del CDP".

## 2. Usuario objetivo definido
Rol **Gestion de presupuesto (anulaciones de cadena)**: revisa el CDP a anular (motivo, usuario real,
correlation-id/task_id para auditoria) y confirma la anulacion. Supuesto temporal: usuario autenticado
con rol presupuesto; policy por operacion via BR-C4 post-Sprint-1 (mismo supuesto DD-01 que el resto de
la familia).

## 3. Alcance definido
Un contrato de mutacion atomico (anulacion) + su preparacion:
- **Guarda bloqueante (RN-08):** el proc rechaza la anulacion si el CDP tiene compromisos (RP) activos
  encima -> uno de los THROW del set real (50100/50280-50287, RE-CONFIRMAR el codigo exacto de esta
  guarda contra `OBJECT_DEFINITION`). La aplicacion NO debe permitir ni siquiera intentar la llamada sin
  que el usuario vea la previsualizacion del estado (RP activos) primero, pero la guarda AUTORITATIVA
  vive en el proc, no en C#.
- **Efecto presupuestal:** libera el monto del CDP de vuelta a la apropiacion vigente (el saldo
  disponible de la apropiacion sube); se lee de la vista de saldo, NO recalculado en C#.
- **Efecto documental:** el CDP pasa a estado 'A' (anulado) via MERGE (idempotente: anular dos veces no
  doble-restaura, ver s.6 restriccion (c)).
- **Efecto contable:** comprobante inverso si el CDP original tuvo comprobante (NOTA DE DOMINIO
  confirmada por el DBA: en CDP/RP el tramo contable es NO-OP -- correcto, CDP/RP es reserva
  presupuestal, no movimiento contable; el comprobante inverso real solo aplica de Obligacion/Pago hacia
  abajo). La superficie NO debe fingir un posteo contable que el proc no hace.
- Tenant/auditoria: `SESSION_CONTEXT('tenant_id')` obligatorio (THROW de tenant faltante, RE-VERIFICAR
  numero exacto); usuario real + correlation-id/task_id en cada anulacion.

## 4. Fuera de alcance definido
- **Anulacion de COMPROMISO** (`Annul_Commitment`, P4-006, hermano de par): territorio del miembro
  GOBERNADO -> FUERA (AISLAMIENTO PAR-2).
- **Crear/aprobar un CDP** (`Approve_Availability_Certificate_Draft`, P3.2) o ajustarlo
  (`Apply_Availability_Adjustment`, P4.2, TASK-0254 ya cerrada): FUERA, son otras unidades.
- **Construir o modificar el proc de hardening:** el proc YA EXISTE (construido por el DBA); esta unidad
  NUNCA toca su definicion SQL, solo consume el contrato via la superficie C#/API.
- Contabilidad real (el tramo es NO-OP para CDP/RP, confirmado; no reimplementar un posteo que el proc no
  hace).

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada; F-NOVA-01):**
  - Proc: `Budget.Annul_Availability_Certificate` (hardening, verificado 10/10 por el DBA). Firma EXACTA
    (parametros, tipos) **NO documentada en el hub -- el maker la extrae de `OBJECT_DEFINITION` al
    construir**, no debe asumirse igual a `Apply_Availability_Adjustment`.
  - Tablas de reverso: `Budget.Availability_Certificate_Reversal` + `Budget.Availability_Certificate_Reversal_Line`
    (creadas por el DBA junto con el proc). Estado del CDP anulado: `'A'` via `MERGE` (no INSERT/UPDATE
    directo desde C#).
  - Vistas de saldo/validacion existentes de la familia CDP (`Budget.vw_Availability_Certificate_Balance`,
    `Budget.vw_Commitment_Availability_Validation` -- confirmar cual aplica al saldo POST-anulacion contra
    el proc real, no asumir).
- **THROW (set REAL leido de `OBJECT_DEFINITION` por el DBA -- RE-CONFIRMAR al construir, NO un rango
  documentado sin base): 50100, 50280, 50281, 50282, 50283, 50284, 50285, 50286, 50287** (9 codigos). El
  maker mapea cada uno a su regla de negocio (tenant faltante, guarda bloqueante RP-activo, no-existe,
  ya-anulado/idempotencia, etc.) confirmando el texto real del proc -- la asignacion codigo-regla exacta
  se determina al leer `OBJECT_DEFINITION`, no se asume por analogia con otros procs de la familia.
- **API:** `POST /api/budget/availability-certificates/{id}/annul` (body = motivo + usuario/correlation
  ya derivados del contexto de auth); ProblemDetails por THROW; devuelve el estado resultante del CDP +
  el saldo de apropiacion post-anulacion (por vista).
- **UI (apps/nova-web):** flujo de anulacion -- selecciona CDP, muestra estado actual (RP activos si los
  hay, para que el usuario entienda POR QUE podria fallar antes de intentar), campo de motivo, confirma;
  muestra el ProblemDetails si el proc rechaza.
- **Capa Application:** `NOVA.Application/Budget/AvailabilityCertificateAnnulment/` (mapea la solicitud,
  traduce THROW, NO reimplementa la guarda ni el reverso de saldo).
- **Referencias:** NOVA-PRES-08 (patron RN-08), NOVA-PRES-04 (CDP), `DRAFT-SPEC-hardening-annul-cdp-compromiso.md`
  (diseno completo del proc), patron congelado de P4.1/P4.2 (Apply/Annul atomico, THROW->ProblemDetails,
  guard de procedencia). (NO se lee el hermano P4-006 ni su implementacion -- aislamiento PAR-2.)

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 (React nunca SQL; MCP nunca SQL; C# no reimplementa
  saldos/guardas/numeracion; gateways tipados; cero DataTable) + stack + patron congelado de P4.1/P4.2.
- Propias:
  - (a) Mutacion SOLO por `Annul_Availability_Certificate`; jamas DML directo sobre las tablas de CDP o
    de reverso, ni recalculo de saldo/guarda en C#.
  - (b) **GUARDA BLOQUEANTE (RN-08):** el proc, NO la aplicacion, decide si hay RP activos que bloqueen la
    anulacion; la app puede PREVISUALIZAR (leer si hay RP activos) para UX, pero la decision autoritativa
    es del proc (uno de los THROW del set real 50100/50280-50287, RE-VERIFICAR cual).
  - (c) **IDEMPOTENCIA:** anular un CDP ya anulado no debe doble-restaurar saldo -- verificar contra el
    proc real (puede ser no-op o THROW controlado, RE-VERIFICAR cual).
  - (d) Saldo leido de la vista correspondiente, NUNCA recalculado en C#.
  - (e) DTOs 1:1; THROW->ProblemDetails (cada codigo alcanzable, RE-VERIFICADO); correlation id + task_id +
    usuario real en cada anulacion.
  - (f) **GUARD DE PROCEDENCIA:** el harness de evidencia F-NOVA-01 usa una clase SQL real, gateada por env
    vars, NA limpio sin credenciales -- jamas un mock/Recording* in-memory (precedente TASK-0253).
  - (g) **AISLAMIENTO PAR-2:** NO tocar/leer `Annul_Commitment` (hermano, P4-006) ni su implementacion.

## 7. Criterios de aceptacion definidos (Given/When/Then; +un negativo por THROW ALCANZABLE, re-verificado)
> F-NOVA-01: cada negativo cita el THROW conocido o recien confirmado contra `OBJECT_DEFINITION`; el
> maker CONFIRMA los 9 codigos reales (50100, 50280-50287) contra OBJECT_DEFINITION antes de fijar los criterios finales.
> Los tests de mutacion corren en el SANDBOX sellado.
1. **Dado** un CDP existente SIN compromisos (RP) activos, **cuando** anulo, **entonces** el proc libera
   el monto a la apropiacion vigente, el CDP queda en estado 'A' (verificable via MERGE/lectura), y el
   saldo de apropiacion sube por el monto liberado (verificable en la vista, antes y despues).
2. **Dado** un CDP CON un compromiso (RP) activo encima, **entonces** ProblemDetails del THROW de guarda
   bloqueante (dentro del set real 50100/50280-50287, RE-CONFIRMAR cual) y el CDP/saldo NO cambian.
3. **Dado** una anulacion sin `SESSION_CONTEXT('tenant_id')`, **entonces** ProblemDetails del THROW de
   tenant faltante (RE-VERIFICAR numero exacto).
4. **Dado** un CDP ya anulado, **cuando** se intenta anular de nuevo, **entonces** comportamiento
   idempotente verificado contra el proc real (no-op controlado o THROW, sin doble-restaurar saldo).
5. **Dado** un CDP que NO existe, **entonces** ProblemDetails del THROW correspondiente (RE-VERIFICAR).
6. **Dado** cualquier anulacion exitosa, **entonces** la auditoria queda con usuario real + motivo +
   correlation-id/task_id (verificable en la tabla de reverso o el log de auditoria del proc).
7. **Dado** cualquier caso, **entonces** el saldo se lee de la vista (NO recalculado en C#, verificable en
   el diff); NO toca `Annul_Commitment` ni tipos de compromiso (aislamiento PAR-2, verificable en el diff).
8. **Dado** el harness de evidencia F-NOVA-01, **entonces** usa una clase SQL real (gateada por env vars,
   NA limpio sin credenciales) -- sin ningun mock/Recording* sustituyendo la evidencia.

## 8. Pruebas / gates definidos
- **Unit:** mapeo de la solicitud de anulacion; traduccion THROW->ProblemDetails; enforcement de que la
  guarda/saldo/idempotencia NO se recalculan en C#.
- **Architecture tests:** Api sin SQL directo; React sin SQL; Mcp sin SQL; cero DataTable; **test de
  aislamiento PAR-2: ningun archivo de esta unidad referencia `Annul_Commitment` ni tipos de compromiso**
  (mismo patron mecanico que el test de aislamiento de TASK-0254).
- **Integracion vs DbsFinanciero_SANDBOX (EXECUTE via GRANT, ya concedido):** criterio 1 (happy, delta de
  saldo real), un caso por THROW ALCANZABLE (de los 9 reales: 50100 + 50280-50287 -- guarda, tenant, no-existe, idempotencia)
  RE-VERIFICADO contra `OBJECT_DEFINITION`, criterio 7 (saldo por vista + aislamiento). **PRECONDICION:
  GRANT VIEW DEFINITION + SELECT sobre tablas base pendiente de preflight ampliado (ver DoR) antes de
  construir el harness de evidencia.**
- **Gate final:** APROBADO del adversarial informal en SESION SEPARADA (baseline, checker_formal=0) + arch
  tests + CI + **F-NOVA-01: cada THROW verificado contra el proc desplegado** + guard de procedencia
  (evidencia SQL real, sin mock) + verificacion de AISLAMIENTO PAR-2 + DoD con evidencia real + gates del
  hub verdes + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Asumir el set de THROW sin re-confirmar contra el proc desplegado | Criterio falso, THROW no alcanzable no detectado (F-0246-02, ya paso 2 veces en este proyecto) | F-NOVA-01: RE-CONFIRMAR los 9 codigos (50100, 50280-50287) contra OBJECT_DEFINITION antes de fijar los criterios finales |
| Repetir la saga de permisos de P4.1/P4.2 (VIEW DEFINITION, SELECT sobre tablas base no anticipadas) | Bloqueo F-NOVA-01 en vivo, ciclos de retry | Preflight AMPLIADO pedido ANTES del GO (VIEW DEFINITION + SELECT sobre tablas base, no solo vistas) |
| Mock/fixture in-memory disfrazado de evidencia F-NOVA-01 real | Criterio falso-verde no detectado (precedente TASK-0250/0253) | Guard de procedencia (restriccion 6f): clase SQL real, NA limpio, sin credenciales -- checker lo verifica explicitamente |
| Implementar Annul_Commitment "de paso" | CONTAMINACION intra-par PAR-2 | Restriccion 6g + architecture test de aislamiento mecanico |
| Reimplementar la guarda RN-08 o el saldo en C# | Divergencia con la BD (RN-08) | Restricciones 6a/6b/6d; adversarial punto especifico |
| Fingir un posteo contable que el proc no hace (CDP/RP es NO-OP contable, confirmado) | Criterio falso, contradice la nota de dominio del DBA | s.3: efecto contable documentado como NO-OP para CDP/RP, no reimplementar |
| adversarial en la misma sesion del maker | Contaminacion (tokens no separables) | DoR: adversarial en SESION SEPARADA |

## 10. Prioridad definida
**GOAL-P4** (anulaciones de cadena, brecha B-04/RN-08 cerrada por hardening), miembro de **PAR-2** (par
CONFIRMADO s.13, isomorfo con Annul_Commitment). **Pertenencia Q4: DENTRO** (miembro de par del
contraste; criticidad media; proc de hardening ya verificado 10/10). Severidad: mutador de anulacion de
CDP (libera saldo presupuestal). Dependencias: GOAL-P1 + patron congelado de P4.1/P4.2 + proc de
hardening (existe, verificado por el DBA) + **preflight ampliado de permisos (VIEW DEFINITION + SELECT
sobre tablas base) pendiente antes de construir**. AISLAMIENTO PAR-2: leyo_codigo_hermano=NO; el sorteo
(sello s.23) ya asigno baseline/gobernado; violacion de aislamiento = par CONTAMINADO. Desbloquea: el
ciclo completo de anulaciones de la cadena presupuestal (CDP hoy; Compromiso en Sprint 1).
