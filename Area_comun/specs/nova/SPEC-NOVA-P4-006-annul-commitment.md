# SPEC-NOVA-P4-006 - Annul_Commitment (anulacion de Compromiso/RP, brecha B-04/RN-08) [miembro GOBERNADO de PAR-2, isomorfo con P4-005]

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Miembro GOBERNADO de PAR-2 (par
> CONFIRMADO, sello s.13/s.23), isomorfo con `Annul_Availability_Certificate` (baseline, SPEC-NOVA-P4-005,
> TASK-0255, DONE). El proc es HARDENING (construido por el DBA, fuera del estudio medido, regla 8); esta
> SPEC cubre SOLO la superficie C#/API sobre el proc, que SI es la unidad medida. Preparada por el
> Arquitecto FUERA de la ventana medida, como PREP de Sprint 1 (DIRECTIVA Operador 2026-07-06,
> "escribir, no construir" -- esta SPEC no se implementa antes del 30-jul). Fuente: NOVA-PRES-08 (Reversos
> y Anulaciones, B-04/RN-08) + NOVA-PRES-05 (Compromiso) + `DRAFT-SPEC-hardening-annul-cdp-compromiso.md`
> (diseno del Asesor) + FYI-PAR2-hardening-entregado + enmienda s.24/s.25 del sello (grant + THROW reales).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P4-006 - task_id (hub): asignado al registrar la tarea de superficie (Sprint 1,
  post-30-jul; NO registrar como `ready`/GO antes de esa fecha -- linea roja pool Q4/gobernado).
- owner_maker: agente desarrollador de la instancia gobernada (Sprint 1); repo producto Nova-Budget.
- checker: **Analista (adversarial FORMAL, contexto limpio, estructuralmente independiente; recibe SPEC +
  diff + BD readonly, NO la conversacion del maker)** -- a diferencia del hermano baseline (P4-005,
  checker_formal=0), este miembro GOBERNADO lleva checker formal ADEMAS del adversarial informal (mismo
  patron que P4-003/P3-001).
- arm: **PAR-2 GOBERNADO** (sorteo del sello s.23, empate resuelto por orden alfabetico del nombre real
  del proc SQL) - unit: Annul_Commitment (anulacion de Compromiso/RP).
- q4_membership: **DENTRO** (miembro de par del contraste; criticidad media; proc de hardening ya
  existente y verificado por el DBA -- 10/10 pruebas OK, mismo lote que su hermano baseline).
- **isolation: CRITICA (PAR-2).** Isomorfo con `Annul_Availability_Certificate` (P4-005, YA CONSTRUIDA Y
  CERRADA como `done`). leyo_codigo_hermano = **NO**: esta SPEC se redacta SOLO de NOVA-PRES-08/05 + el
  draft de diseno del Asesor (documento de proceso compartido, no implementacion) + el patron congelado de
  P4.1/P4.2/P4-005 (documentado, no el codigo fuente de P4-005). El MAKER de esta unidad, al construirla en
  Sprint 1, **NO debe leer el repo/implementacion de `Annul_Availability_Certificate`** (commits `9aff84d`/
  `edbc037` en Nova-Budget) pese a estar ya mergeada en el mismo repo producto -- manifiesto de archivos
  leidos explicito en el DoD; violacion = par CONTAMINADO fuera del confirmatorio. Riesgo: reusar "de paso"
  el gateway/test/UI de CDP para Compromiso = CONTAMINACION intra-par.
- **PRECONDICION: READY, preflight AMPLIADO YA HECHO (adelantado, ambos miembros del par, sello s.24).**
  El proc de hardening YA EXISTE y esta VERIFICADO por el DBA (10/10 pruebas en `DbsFinanciero_SANDBOX`).
  GRANT EXECUTE ya concedido. `VIEW DEFINITION` sobre `Annul_Commitment` + 2 de las 4 tablas de reverso
  (`Commitment_Reversal`/`_Line`); `SELECT` sobre las 13 tablas base ya concedidas para el par completo
  (ver s.24 del sello). Sin TVP; sin triggers en reverso. Smoke real (ROLLBACK, RP 87) confirma
  procedencia sin errores de permiso. **F-NOVA-01 puede proceder sin round-trips** cuando se construya.
- **measurement:** cache-confound -> mismo runtime que su pareja de par o declarar; captura de tokens en
  err.log; checker_formal cuenta (a diferencia del baseline) -- separar tokens_adversarial_informal de
  tokens_checker_formal en el journal.
- **F-NOVA-01 (re-verificacion, CRITICA -- precedente F-0246-02, P4.1, P4.2, P4-005):** preflight AMPLIADO
  YA HECHO por el DBA (VIEW DEFINITION + SELECT ya concedidos, sello s.24). El `OBJECT_DEFINITION` (leido
  por el DBA) revela el set REAL: **`Annul_Commitment` = 50100, 50290, 50291, 50292, 50293, 50294, 50295,
  50296, 50297** (9 codigos, guarda bloqueante propuesta = 50293 -- por simetria con la guarda 50283 del
  hermano baseline, RE-CONFIRMAR el codigo exacto de la guarda contra `OBJECT_DEFINITION` al construir, no
  asumir por analogia). El maker RE-CONFIRMA estos 9 al construir en Sprint 1 -- son el punto de partida
  real (enmienda s.24), no un rango documentado sin base.
- **GUARD DE PROCEDENCIA (adoptado tras TASK-0253, sello s.15):** la evidencia F-NOVA-01 debe versionarse
  con una clase SQL real (gateada por env vars, NA limpio sin credenciales) -- NINGUN mock/Recording*
  in-memory con resultados hardcodeados puede sustituirla. El checker formal (Analista) Y el adversarial
  informal lo verifican explicitamente (guard cazado 2 veces ya en el proyecto: TASK-0250, TASK-0253).
- **DISENO DE AUTORIZACION (PREP -- converge con hallazgos #5/#7/#8 del backlog de seguridad, DIRECTIVA
  Operador 2026-07-06):** a diferencia de los miembros BASELINE ya cerrados (P4.1/P4.2/P4-005, que
  operan bajo el supuesto temporal DD-01 "usuario autenticado con rol presupuesto", SIN wiring real de
  auth -- gap registrado como hallazgo formal, dueno Analista, NO parcheado retroactivamente en el
  baseline porque alteraria artefactos ya medidos), este miembro GOBERNADO **SI incluye el wiring real de
  autenticacion/autorizacion** como parte de su contrato (ver s.6 restriccion (h) y s.7 criterio 6,
  corregido F-0246-P4006-01: referencia previa a criterio 9 era erronea). Esto
  es DISENO/PREP ahora (esta SPEC se escribe, no se construye); la CONSTRUCCION del wiring ocurre cuando
  esta unidad se promueva en Sprint 1 (post-30-jul), igual que el resto del contrato. El patron de
  autorizacion aqui establecido (rol + [Authorize]/RequireAuthorization real, no solo supuesto documentado)
  es el que hereda el resto del brazo gobernado (converge con #7: transiciones de `BudgetDocumentState` +
  quien-las-ejecuta es la misma preocupacion de autorizacion, aqui aplicada a la transicion Activo->Anulado
  de un Compromiso).
- db_verified_at: proc + tablas de reverso verificados por el DBA en `DbsFinanciero_SANDBOX` (10/10
  pruebas, mismo lote que P4-005, ver `MSG-20260705-Operador-to-Arquitecto-FYI-PAR2-hardening-entregado-confirmado`
  archivado); el maker RE-VERIFICA contra la BD desplegada (F-NOVA-01) para el set exacto de THROW.
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL
  Server 2025 via gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS:
  WebForms/PageMethods, DataTable entre capas, DLLs manuales, capa DATABASE generica, secretos en .config,
  centinelas -99.

## 1. Objetivo definido
El usuario anula un Compromiso/RP (Registro Presupuestal) existente mediante una llamada ATOMICA a
`Budget.Annul_Commitment` (proc de hardening, controlado), que: (a) valida que NO existan obligaciones
activas sobre ese Compromiso (guarda bloqueante, simetrica a la de CDP); (b) si pasa la guarda, libera el
monto del Compromiso de vuelta a la disponibilidad del CDP origen, marca el Compromiso en estado anulado
(via MERGE), y genera el reverso documental/contable correspondiente. Sin reimplementar la guarda ni el
reverso de saldo en C#. A diferencia de su hermano baseline, esta unidad SI requiere autorizacion real por
rol (no solo supuesto documentado) para ejecutar la anulacion.
- Fuente: NOVA-PRES-08 (patron RN-08: 3 efectos coordinados + guarda bloqueante) + NOVA-PRES-05 (saldos de
  Compromiso) + `DRAFT-SPEC-hardening-annul-cdp-compromiso.md` s.3 (version Compromiso).
- Calidad: falsable. Bien: "anular un Compromiso que tiene una Obligacion activa encima devuelve
  ProblemDetails del THROW de guarda bloqueante (dentro del set real 50100/50290-50297, RE-CONFIRMAR cual
  exacto) y NO libera saldo ni cambia el estado del Compromiso; y anular sin el rol requerido devuelve 403
  antes de tocar el proc".

## 2. Usuario objetivo definido
Rol **Gestion de presupuesto (anulaciones de cadena)**: revisa el Compromiso a anular (motivo, usuario
real, correlation-id/task_id para auditoria) y confirma la anulacion. A diferencia del baseline (supuesto
temporal DD-01), aqui el rol se VERIFICA realmente via el mecanismo de autorizacion de la API (s.6h);
policy fina por-operacion (BR-C4, post-Sprint-1) sigue diferida, pero el piso minimo "autenticado con rol
presupuesto" que DD-01 acepto SI se cablea de verdad en esta unidad.

## 3. Alcance definido
Un contrato de mutacion atomico (anulacion) + su preparacion, simetrico a P4-005 pero sobre Compromiso:
- **Guarda bloqueante (RN-08):** el proc rechaza la anulacion si el Compromiso tiene una Obligacion activa
  encima -> uno de los THROW del set real (50100/50290-50297, RE-CONFIRMAR el codigo exacto de esta guarda
  contra `OBJECT_DEFINITION` -- propuesta 50293 por simetria con 50283 del hermano, NO asumir sin
  verificar). La aplicacion NO debe permitir ni siquiera intentar la llamada sin que el usuario vea la
  previsualizacion del estado (Obligaciones activas) primero, pero la guarda AUTORITATIVA vive en el proc.
- **Efecto presupuestal:** libera el monto del Compromiso de vuelta a la disponibilidad del CDP origen
  (el saldo disponible del CDP sube); se lee de la vista de saldo, NO recalculado en C#.
- **Efecto documental:** el Compromiso pasa a estado anulado via MERGE (idempotente: anular dos veces no
  doble-restaura, ver s.6 restriccion (c)).
- **Efecto contable:** comprobante inverso si el Compromiso original tuvo comprobante (misma nota de
  dominio que P4-005: para CDP/RP el tramo contable es NO-OP -- el comprobante inverso real solo aplica de
  Obligacion/Pago hacia abajo; RE-CONFIRMAR con el DBA si Compromiso difiere de CDP en este punto antes de
  fijar el criterio, dado que la firma/reverso puede no ser identica).
- **Autorizacion real (NUEVO vs baseline):** el endpoint de anulacion exige rol "Gestion de presupuesto"
  verificado por el mecanismo de auth de la API (s.6h) -- sin autenticacion/rol valido, 401/403 antes de
  tocar el proc.
- Tenant/auditoria: `SESSION_CONTEXT('tenant_id')` obligatorio (THROW de tenant faltante, RE-VERIFICAR
  numero exacto); usuario real (del contexto de auth, no un campo de formulario) + correlation-id/task_id
  en cada anulacion.

## 4. Fuera de alcance definido
- **Anulacion de CDP** (`Annul_Availability_Certificate`, P4-005, hermano baseline YA CERRADO/`done`):
  territorio del miembro BASELINE -> FUERA (AISLAMIENTO PAR-2). NO leer su implementacion.
- **Crear/aprobar un Compromiso** (`Approve_Commitment_Draft`, P3.3/SPEC-NOVA-P3-003) o ajustarlo
  (`Apply_Commitment_Adjustment`, P4.3/SPEC-NOVA-P4-003, gobernado tambien pero unidad distinta): FUERA.
- **Construir o modificar el proc de hardening:** el proc YA EXISTE (construido por el DBA); esta unidad
  NUNCA toca su definicion SQL, solo consume el contrato via la superficie C#/API.
- **Policy fina de autorizacion por-operacion (BR-C4):** diferida a post-Sprint-1 (DD-01); esta unidad SOLO
  cablea el piso minimo (rol presupuesto autenticado), no la matriz completa por-operacion.
- Contabilidad real si el DBA confirma NO-OP para Compromiso (pendiente re-confirmar, ver s.3).

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada; F-NOVA-01):**
  - Proc: `Budget.Annul_Commitment` (hardening, verificado 10/10 por el DBA). Firma EXACTA (parametros,
    tipos) **NO documentada en el hub -- el maker la extrae de `OBJECT_DEFINITION` al construir**, no debe
    asumirse igual a `Annul_Availability_Certificate` pese al isomorfismo de patron.
  - Tablas de reverso: `Budget.Commitment_Reversal` + `Budget.Commitment_Reversal_Line` (creadas por el DBA
    junto con el proc). Estado del Compromiso anulado: via `MERGE` (no INSERT/UPDATE directo desde C#).
  - Vistas de saldo/validacion existentes de la familia Compromiso (`Budget.vw_Commitment_Availability_Validation`
    u otra que el maker confirme aplica al saldo POST-anulacion contra el proc real, no asumir).
- **THROW (set REAL leido de `OBJECT_DEFINITION` por el DBA -- RE-CONFIRMAR al construir, enmienda s.24):
  50100, 50290, 50291, 50292, 50293, 50294, 50295, 50296, 50297** (9 codigos). El maker mapea cada uno a su
  regla de negocio (tenant faltante, guarda bloqueante Obligacion-activa, no-existe, ya-anulado/
  idempotencia, etc.) confirmando el texto real del proc.
- **API:** `POST /api/budget/commitments/{id}/annul` (body = motivo + usuario/correlation ya derivados del
  contexto de auth); ProblemDetails por THROW; devuelve el estado resultante del Compromiso + el saldo del
  CDP origen post-anulacion (por vista). **Requiere `[Authorize]`/`RequireAuthorization` con rol "Gestion
  de presupuesto" real (s.6h) -- NO opcional, a diferencia del baseline.**
- **UI (apps/nova-web):** flujo de anulacion -- selecciona Compromiso, muestra estado actual (Obligaciones
  activas si las hay), campo de motivo, confirma; muestra el ProblemDetails si el proc rechaza o si el
  usuario no tiene el rol requerido.
- **Capa Application:** `NOVA.Application/Budget/CommitmentAnnulment/` (mapea la solicitud, traduce THROW,
  NO reimplementa la guarda ni el reverso de saldo).
- **Referencias:** NOVA-PRES-08 (patron RN-08), NOVA-PRES-05 (Compromiso), `DRAFT-SPEC-hardening-annul-cdp-compromiso.md`
  (diseno completo del proc), patron congelado de P4.1/P4.2/P4-005 (Apply/Annul atomico, THROW->
  ProblemDetails, guard de procedencia). (NO se lee el hermano P4-005 ni su implementacion --
  aislamiento PAR-2.) Hallazgos de seguridad convergentes: #5/#8 (cero auth en baseline, dueno Analista),
  #7 (transiciones de `BudgetDocumentState` + quien-ejecuta, dueno pattern-setter).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 (React nunca SQL; MCP nunca SQL; C# no reimplementa
  saldos/guardas/numeracion; gateways tipados; cero DataTable) + stack + patron congelado de
  P4.1/P4.2/P4-005.
- Propias:
  - (a) Mutacion SOLO por `Annul_Commitment`; jamas DML directo sobre las tablas de Compromiso o de
    reverso, ni recalculo de saldo/guarda en C#.
  - (b) **GUARDA BLOQUEANTE (RN-08):** el proc, NO la aplicacion, decide si hay Obligaciones activas que
    bloqueen la anulacion; la app puede PREVISUALIZAR (leer si hay Obligaciones activas) para UX, pero la
    decision autoritativa es del proc (uno de los THROW del set real 50100/50290-50297, RE-VERIFICAR cual).
  - (c) **IDEMPOTENCIA:** anular un Compromiso ya anulado no debe doble-restaurar saldo -- verificar contra
    el proc real (puede ser no-op o THROW controlado, RE-VERIFICAR cual).
  - (d) Saldo leido de la vista correspondiente, NUNCA recalculado en C#.
  - (e) DTOs 1:1; THROW->ProblemDetails (cada codigo alcanzable, RE-VERIFICADO); correlation id + task_id +
    usuario real en cada anulacion.
  - (f) **GUARD DE PROCEDENCIA:** el harness de evidencia F-NOVA-01 usa una clase SQL real, gateada por env
    vars, NA limpio sin credenciales -- jamas un mock/Recording* in-memory (precedente TASK-0253).
  - (g) **AISLAMIENTO PAR-2:** NO tocar/leer `Annul_Availability_Certificate` (hermano, P4-005, ya `done`)
    ni su implementacion/repo.
  - (h) **AUTORIZACION REAL (NUEVO vs baseline, PREP #5/#7/#8):** el endpoint exige `[Authorize]`/
    `RequireAuthorization` con verificacion de rol "Gestion de presupuesto" real (no supuesto documentado);
    sin sesion/rol valido, la API responde 401/403 ANTES de invocar el gateway/proc. El mecanismo concreto
    de autenticacion (esquema, emisor de tokens) se define al implementar segun lo que la instancia Nova
    ya tenga disponible (converge con el diseno de #7, mismo mecanismo para el resto del brazo gobernado).
    Test de arquitectura: el endpoint de anulacion DEBE tener el atributo/policy de autorizacion presente
    (mecanico, no solo revision manual).
  - (i) **LECTURA DE RESULT-SET SIN ADIVINANZA (fix-forward de hallazgo #11, quality-data del hermano
    baseline P4-005):** el gateway de produccion NO debe leer columnas del result-set del proc por fallback
    encadenado de nombres (p.ej. intentar `reversal_id` y si falla `..._reversal_id`) ni caer en un DEFAULT
    SILENCIOSO si la columna no aparece (p.ej. asumir estado `'A'` sin verificar). El nombre EXACTO de cada
    columna leida se confirma contra `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_set` del proc
    DESPLEGADO antes de escribir el gateway, y el harness de evidencia F-NOVA-01 DEBE ejercitar el MISMO
    camino de lectura que usa el gateway de produccion (mismos nombres de columna, mismo mecanismo de
    derivacion de estado) -- no un camino de lectura alternativo (p.ej. JOIN a tabla de catalogo) que deje
    sin verificar el codigo real de produccion.
  - (j) **COBERTURA HTTP DE INTEGRACION (fix-forward de hallazgo #12):** cada endpoint mutador nuevo
    (preview + anulacion) tiene al menos un test de integracion HTTP real (`WebApplicationFactory` +
    gateway FALSO inyectado) que ejercita ruta -> endpoint -> mapeo de comando -> gateway; no basta con
    unitarias de la capa Application sin verificar el wiring HTTP completo.
  - (k) **LISTA DE AISLAMIENTO COMPLETA (fix-forward de hallazgo #13):** el test de arquitectura
    `React_app_does_not_contain_sql_or_procedure_calls` (o su equivalente) DEBE incluir el nombre exacto
    del proc de ESTA unidad (`Annul_Commitment`) en su lista de literales prohibidos para el frontend, igual
    que ya cubre a `Apply_Budget_Modification`/`Apply_Availability_Adjustment`. Si el nombre del proc
    mutador se exhibe como texto descriptivo en la UI (p.ej. etiqueta de auditoria), es una EXCEPCION
    EXPLICITA que se documenta y se excluye puntualmente del test, nunca una omision silenciosa de la lista.

## 7. Criterios de aceptacion definidos (Given/When/Then; +un negativo por THROW ALCANZABLE, re-verificado)
> F-NOVA-01: cada negativo cita el THROW conocido o recien confirmado contra `OBJECT_DEFINITION`; el
> maker CONFIRMA los 9 codigos reales (50100, 50290-50297) contra OBJECT_DEFINITION antes de fijar los
> criterios finales. Los tests de mutacion corren en el SANDBOX sellado.
1. **Dado** un Compromiso existente SIN Obligaciones activas, **cuando** un usuario CON el rol requerido
   anula, **entonces** el proc libera el monto a la disponibilidad del CDP origen, el Compromiso queda
   anulado (verificable via MERGE/lectura), y el saldo del CDP sube por el monto liberado (verificable en
   la vista, antes y despues).
2. **Dado** un Compromiso CON una Obligacion activa encima, **entonces** ProblemDetails del THROW de guarda
   bloqueante (dentro del set real 50100/50290-50297, RE-CONFIRMAR cual) y el Compromiso/saldo NO cambian.
3. **Dado** una anulacion sin `SESSION_CONTEXT('tenant_id')`, **entonces** ProblemDetails del THROW de
   tenant faltante (RE-VERIFICAR numero exacto).
4. **Dado** un Compromiso ya anulado, **cuando** se intenta anular de nuevo, **entonces** comportamiento
   idempotente verificado contra el proc real (no-op controlado o THROW, sin doble-restaurar saldo).
5. **Dado** un Compromiso que NO existe, **entonces** ProblemDetails del THROW correspondiente
   (RE-VERIFICAR).
6. **Dado** un usuario SIN el rol "Gestion de presupuesto" (o sin autenticar), **cuando** intenta anular,
   **entonces** la API responde 401/403 y el proc NUNCA se invoca (verificable: cero llamadas al gateway).
7. **Dado** cualquier anulacion exitosa, **entonces** la auditoria queda con usuario real (del contexto de
   auth) + motivo + correlation-id/task_id (verificable en la tabla de reverso o el log de auditoria).
8. **Dado** cualquier caso, **entonces** el saldo se lee de la vista (NO recalculado en C#, verificable en
   el diff); NO toca `Annul_Availability_Certificate` ni tipos de CDP (aislamiento PAR-2, verificable en
   el diff, ni se referencia/lee su implementacion en el repo).
9. **Dado** el harness de evidencia F-NOVA-01, **entonces** usa una clase SQL real (gateada por env vars,
   NA limpio sin credenciales) -- sin ningun mock/Recording* sustituyendo la evidencia.
10. **Dado** el gateway de produccion, **entonces** lee cada columna del result-set por el nombre EXACTO
    confirmado contra `OBJECT_DEFINITION`, sin fallback encadenado de nombres ni default silencioso; el
    harness F-NOVA-01 ejercita el MISMO camino de lectura (fix-forward hallazgo #11).
11. **Dado** los endpoints de preview y anulacion, **entonces** cada uno tiene al menos un test de
    integracion HTTP (`WebApplicationFactory` + gateway falso) que verifica el wiring completo ruta->
    endpoint->comando->gateway (fix-forward hallazgo #12).
12. **Dado** el test de arquitectura de aislamiento del frontend, **entonces** incluye `Annul_Commitment`
    en su lista de literales prohibidos; si el nombre se exhibe como texto descriptivo en la UI, es una
    excepcion explicita documentada, no una omision (fix-forward hallazgo #13).

## 8. Pruebas / gates definidos
- **Unit:** mapeo de la solicitud de anulacion; traduccion THROW->ProblemDetails; enforcement de que la
  guarda/saldo/idempotencia NO se recalculan en C#; verificacion de policy de autorizacion presente.
- **Architecture tests:** Api sin SQL directo; React sin SQL; Mcp sin SQL; cero DataTable; **test de
  aislamiento PAR-2: ningun archivo de esta unidad referencia `Annul_Availability_Certificate` ni tipos de
  CDP** (mismo patron mecanico que TASK-0255/TASK-0254); **test de autorizacion: el endpoint de anulacion
  tiene `[Authorize]`/policy de rol presente (mecanico, falla si se remueve).**
- **Integracion vs DbsFinanciero_SANDBOX (EXECUTE via GRANT, ya concedido):** criterio 1 (happy, delta de
  saldo real, con usuario autorizado), un caso por THROW ALCANZABLE (de los 9 reales: 50100 + 50290-50297
  -- guarda, tenant, no-existe, idempotencia) RE-VERIFICADO contra `OBJECT_DEFINITION`, criterio 6 (403 sin
  rol), criterio 8 (saldo por vista + aislamiento).
- **Gate final:** APROBADO del checker FORMAL del Analista (contexto limpio, SPEC+diff+BD readonly) +
  adversarial informal en sesion separada + arch tests + CI + **F-NOVA-01: cada THROW verificado contra el
  proc desplegado** + guard de procedencia (evidencia SQL real, sin mock) + verificacion de AISLAMIENTO
  PAR-2 + verificacion de autorizacion real (no solo supuesto) + DoD con evidencia real + gates del hub
  verdes + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Asumir el set de THROW sin re-confirmar contra el proc desplegado | Criterio falso, THROW no alcanzable no detectado (F-0246-02) | F-NOVA-01: RE-CONFIRMAR los 9 codigos (50100, 50290-50297) contra OBJECT_DEFINITION antes de fijar los criterios finales |
| Asumir que 50293 es la guarda bloqueante por simetria con 50283 del hermano, sin verificar | Criterio de guarda apunta al THROW incorrecto | RE-VERIFICAR el codigo exacto de la guarda contra OBJECT_DEFINITION antes de fijar el criterio 2 |
| Leer/reusar la implementacion de P4-005 (ya mergeada en el mismo repo producto) "para ir mas rapido" | CONTAMINACION intra-par PAR-2, invalida el contraste Q4 | Restriccion 6g + manifiesto de archivos leidos explicito en el DoD + architecture test de aislamiento mecanico |
| Mock/fixture in-memory disfrazado de evidencia F-NOVA-01 real | Criterio falso-verde no detectado (precedente TASK-0250/0253) | Guard de procedencia (restriccion 6f): clase SQL real, NA limpio, sin credenciales -- checker formal Y adversarial lo verifican |
| Cablear la autorizacion como policy decorativa sin verificacion real de rol (repetir el gap del baseline) | El gap #5/#8 se repite en el brazo que debia corregirlo | Restriccion 6h + criterio 6 + test de arquitectura mecanico que falla si se remueve el atributo/policy |
| Reimplementar la guarda RN-08 o el saldo en C# | Divergencia con la BD (RN-08) | Restricciones 6a/6b/6d; adversarial y checker formal verifican especificamente |
| Fingir un posteo contable que el proc no hace (pendiente re-confirmar NO-OP para Compromiso) | Criterio falso si el DBA confirma que Compromiso SI difiere de CDP en el tramo contable | s.3: RE-CONFIRMAR con el DBA antes de fijar el criterio contable definitivo |
| Checker formal y adversarial en la misma sesion, o compartiendo contexto con el maker | Contaminacion (tokens no separables, independencia comprometida) | DoR: checker formal del Analista en sesion/contexto estructuralmente independiente (SPEC+diff+BD readonly, no la conversacion del maker) |
| Repetir los 3 huecos de calidad no-bloqueantes hallados en el hermano baseline P4-005 (quality-data #11/#12/#13, DECISION-0018 2026-07-06): lectura de columnas por adivinanza+default silencioso, cero test HTTP de integracion para los endpoints nuevos, omision del proc en la lista de aislamiento del frontend | Mismo patron de gaps de calidad no cazados por el GO informal, esta vez en el miembro gobernado con checker formal | Restricciones 6i/6j/6k + criterios 10/11/12 (fix-forward explicito, no parche retroactivo al baseline ya cerrado) |

## 10. Prioridad definida
**GOAL-P4** (anulaciones de cadena, brecha B-04/RN-08 cerrada por hardening), miembro GOBERNADO de
**PAR-2** (par CONFIRMADO s.13/s.23, isomorfo con `Annul_Availability_Certificate`, YA `done`). Pertenencia
Q4: **DENTRO** (miembro de par del contraste; criticidad media; proc de hardening ya verificado 10/10).
Severidad: mutador de anulacion de Compromiso (libera saldo presupuestal hacia el CDP origen).
Dependencias: patron congelado de P4.1/P4.2/P4-005 + proc de hardening (existe, verificado por el DBA) +
preflight ampliado de permisos (YA CONCEDIDO, sello s.24) + diseno de autorizacion real (s.6h, converge
#5/#7/#8). AISLAMIENTO PAR-2: leyo_codigo_hermano=NO pese a que el hermano YA esta mergeado en el mismo
repo producto; el sorteo (sello s.23) ya asigno baseline/gobernado; violacion de aislamiento = par
CONTAMINADO. **LINEA ROJA: esta unidad NO SE CONSTRUYE antes del 30-jul** (pool Q4/gobernado); esta SPEC es
DISENO/PREP unicamente. Desbloquea: el ciclo completo de anulaciones de la cadena presupuestal en Sprint 1
(CDP ya cerrado en la ventana baseline; Compromiso aqui, gobernado, con el patron de autorizacion real que
el resto del brazo hereda).
