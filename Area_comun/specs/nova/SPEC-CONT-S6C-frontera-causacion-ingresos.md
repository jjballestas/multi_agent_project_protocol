# SPEC-CONT-S6C - Frontera de causacion de ingresos / CxC (Slice 6C, CONTRATO de frontera, NO build)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Miembro del kit SPEC-CONT (ver
> SPEC-CONT-000-index). **SPEC-FRONTERA (contrato/gobernanza), NO superficie-sobre-proc:** especifica el borde por el
> que el MODULO FUENTE de ingresos/CxC (propietario, NO Contabilidad) genera comprobantes definitivos de causacion
> llamando `Accounting.Post_Voucher` en su propia transaccion, enlazados por una tabla puente del modulo propietario,
> sin pasar por borradores contables y sin que Contabilidad escriba en el modulo fuente. El SDD marca R8 como
> **CONTEMPLADO** (prioridad ALTA) -- el modulo fuente NO esta modelado; esta SPEC fija el CONTRATO, no construye el
> modulo. Fuente: SDD accounting_module_requirements.html R8 (Slice 6C) + warning-box de cabecera (Contabilidad =
> modulo derivado) + SPEC-CONT-000 (cross-check S6C) + patron gobernado NOVA-SPEC-T-001.

## Preambulo de gobierno (DoR)
- spec_id: SPEC-CONT-S6C - task_id (instancia): asignado SOLO cuando el modelo del documento fuente y la tabla puente
  esten autorizados en SQL definitivo (gate previo); NO antes (el modulo fuente no existe).
- owner_maker: agente desarrollador del MODULO FUENTE de ingresos/CxC (NO Contabilidad); Contabilidad solo EXPONE el
  contrato ya existente (`Post_Voucher`).
- checker: **Analista (adversarial FORMAL, contexto limpio: SPEC + diff + BD readonly, NO la conversacion del
  maker)** + adversarial informal en sesion separada.
- arm / q4_membership / isolation: N/A (frontera; no se mide; no esta en la muestra N=6 del pre-registro
  DECISION-0094). Criticidad de INTEGRIDAD **ALTA** (si la frontera se relaja, un modulo fuente podria escribir
  estado contable mal-atribuido o duplicado, o Contabilidad podria acoplarse a tablas ajenas).
- **base congelada de referencia:** sello `ACCOUNTING_BASE_SOLID_20260711`, source_bundle_sha256
  `608b4370d5a6adde8111f85c9de828ade4eee7999a12187509bcb80dd8b1bef5` (ver SPEC-CONT-000). El contrato de Contabilidad
  (`Post_Voucher` + validacion de partida doble + numeracion + inmutabilidad + R1) YA existe y es MIGRADO.
- **precondicion / preflight:** el contrato consumido por la frontera EXISTE en Contabilidad (MIGRADO):
  `Accounting.Post_Voucher`, `Accounting.Voucher`, `Accounting.Voucher_Line`, `Accounting.Voucher_Relation`. Los
  TIPOS de comprobante `income_accrual` y `accounts_receivable_accrual` existen en el catalogo (activos en las 3 BD),
  PERO **NO son procs de `Accounting` ni estan en el verifier** -- son source_types que el modulo fuente usa al
  llamar `Post_Voucher`. El proc legacy `ModuloGeneral.Contabilizar_Causacion_ingreso` (schema `ModuloGeneral`, NO
  `Accounting`) es CONTEMPLADO. La tabla puente fuente<->comprobante es CONTEMPLADA (nombre/columnas NO definidos
  hasta cerrar el modelo fuente -- NO inventar identificador).
- **F-NOVA-01:** **N/A por diseno.** S6C no introduce procs de `Accounting` nuevos ni GRANT EXECUTE -> no hay
  THROW-set propio del verifier (cross-check SPEC-CONT-000: los procs `income_accrual`/`accounts_receivable_accrual`
  no son de `Accounting`, correcto que esten fuera del verifier). La verificacion posible es sobre `Post_Voucher`
  (ya cubierto por S2) y sobre el CONTRATO de frontera (tests de contrato/gobernanza, s.8), no un harness SQL propio.
- **guard de procedencia:** cuando el modulo fuente abra, sus tests de causacion corren contra BD real (no mocks) y
  demuestran el borde (all-or-nothing con la tx del documento fuente); mientras tanto, esta SPEC es contrato.
- **diseno de autorizacion (real, no supuesto DD-01):** la autorizacion de causar/aprobar vive en el MODULO FUENTE
  (operador de ingresos/cartera, contador que parametriza, supervisor que aprueba), NO en Contabilidad; el rol se
  declara del lado fuente sin acoplar a Contabilidad (RE-CONFIRMAR al abrir el modulo fuente).
- **measurement:** N/A (no se mide).
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): mismo stack gobernado; la frontera se consume por un gateway tipado a `Post_Voucher`, dentro
  de la transaccion del documento fuente. Anti-patrones PROHIBIDOS: DML contable directo desde el modulo fuente,
  escritura de Contabilidad en tablas del modulo fuente, FK directa en cabeceras, Presupuesto como generador contable.

## 1. Objetivo definido
Definir el CONTRATO de frontera para que el modulo fuente de ingresos/CxC genere comprobantes definitivos de
causacion llamando `Accounting.Post_Voucher` en su propia transaccion, enlazados por una tabla puente del modulo
propietario, sin pasar por borradores contables y sin que Contabilidad escriba en el modulo fuente. Contabilidad es
un MODULO DERIVADO: postea el asiento cuando el fuente lo causa, pero NO posee el documento fuente ni su aprobacion.
El BUILD del modulo fuente es FUERA DE ALCANCE (CONTEMPLADO hasta cerrar el modelo fuente); esta SPEC fija el borde.
- Fuente: SDD R8 + warning-box de cabecera; SPEC-CONT-000 (cross-check S6C).
- Calidad: falsable. Bien: "una causacion aprobada en el modulo fuente publica via `Post_Voucher` un comprobante
  `income_accrual`/`accounts_receivable_accrual` `posted` (NO borrador), enlazado por la tabla puente del lado
  fuente; si `Post_Voucher` falla, revierte TODO el documento fuente; y Contabilidad NUNCA escribe en las tablas del
  modulo fuente ni modifica el comprobante original en un ajuste (nace un comprobante relacionado via
  `Voucher_Relation`)".

## 2. Usuario objetivo definido
El **modulo fuente de ingresos/CxC** (sistema propietario: causa/aprueba el documento fuente y llama `Post_Voucher`)
y sus roles (operador de ingresos/cartera, contador que parametriza cuentas, supervisor que aprueba), TODOS del lado
fuente. Contabilidad NO tiene usuario propio en este flujo: expone el contrato `Post_Voucher` y refleja el asiento en
R1. El consumidor humano ve el resultado en los reportes RO de Contabilidad (S1), no captura la causacion a mano.

## 3. Alcance definido (el CONTRATO de frontera)
- **Publicacion cruzada:** el modulo fuente aprueba/causa el documento y llama `Accounting.Post_Voucher` EN LA MISMA
  TRANSACCION, con `source_type` `income_accrual` o `accounts_receivable_accrual` (segun regla aprobada; NO
  `manual_accounting`). Resultado: documento fuente definitivo + comprobante `posted` + registro en la tabla puente
  fuente<->comprobante (con rol del comprobante y trazabilidad).
- **Direccion UNICA de datos:** SOLO fuente -> Accounting (escritura via `Post_Voucher` dentro de la tx del
  documento fuente). Contabilidad NO lee ni escribe tablas del modulo fuente. La atribucion fuente<->comprobante se
  guarda del lado FUENTE (tabla puente), NO en Contabilidad (sin FK directa en cabeceras de `Voucher`).
- **Sin borradores automaticos:** el flujo automatico NO deja comprobantes en `Accounting.Voucher_Draft` (el borde no
  pasa por borradores contables).
- **Inmutabilidad + ajustes:** el comprobante definitivo es inmutable; un ajuste/anulacion NACE en el modulo de
  ingresos/CxC y genera un NUEVO comprobante relacionado (`Accounting.Voucher_Relation`); Contabilidad NO modifica el
  original.
- **Idempotencia del borde (requisito del contrato; el SDD es silencioso -- decision del kit):** el contrato EXIGE
  una clave natural documento-fuente -> un unico `Voucher`, para que un reintento no duplique el asiento. El
  mecanismo fisico (columna/constraint) lo fija el modulo fuente al construir; el contrato lo REQUIERE.
- **Parametrizacion de cuentas:** `Accounting.Budget_Accounting_Use` (MIGRADO desde `Pres016t`) puede ORIENTAR las
  cuentas (IVA / por cobrar / gasto) que el modulo fuente usa al armar las lineas, SIN convertir Presupuesto en
  generador contable. La frontera de esta parametrizacion (que expone Contabilidad vs que consume el fuente) se
  RE-CONFIRMA al abrir el modulo fuente.
- **Controles de periodo en el cruce:** las lineas deben tener tercero, cuenta auxiliar activa, fecha permitida por
  P03/P04/P05/P06 y debitos = creditos (validacion central de `Post_Voucher`). Un periodo cerrado/enviado -> error
  funcional y NO persiste documento fuente parcial (rollback del documento completo).

## 4. Fuera de alcance definido
- **CONSTRUIR/MODELAR el modulo fuente de ingresos/CxC** (CONTEMPLADO hasta cerrar el modelo fuente): el documento
  fuente, su aprobacion/causacion, la tabla puente fisica, los ajustes/anulaciones, la parametrizacion de negocio
  (base/IVA). Esta SPEC es el CONTRATO, no el modulo.
- **Los procs/tipos `income_accrual`/`accounts_receivable_accrual` como superficie de Contabilidad:** NO son procs de
  `Accounting`; correcto que esten fuera de la superficie contable. Contabilidad solo expone `Post_Voucher`.
- **Capturar causaciones como comprobantes manuales desde Contabilidad** (S2): la causacion cruza por `Post_Voucher`
  desde el fuente, no por captura manual.
- **Usar Presupuesto como origen del comprobante** ("Presupuesto no contabiliza"): `source_module_code = 'budget'`
  es rechazado por `Accounting.Voucher`.
- **Reversos de egresos, radicaciones, obligaciones** (siguen los ADR de cadena de gasto: `decision_log.html#
  adr-reversar-pago`, `#adr-reversar-obligacion`) y **corregir la debilidad legacy de base/IVA en radicaciones** (se
  resuelve en el modulo fuente, no desde Contabilidad ni Presupuesto): FUERA.
- **Completar facturacion/cartera** si el modulo fuente aun no esta modelado.

## 5. Contenido / assets definidos
- **Consumido de Contabilidad (MIGRADO, YA existe):** `Accounting.Post_Voucher`, `Accounting.Voucher`,
  `Accounting.Voucher_Line`, `Accounting.Voucher_Relation`; parametrizacion `Accounting.Budget_Accounting_Use`.
  Tipos `income_accrual` / `accounts_receivable_accrual` (catalogo, activos en 3 BD).
- **CONTEMPLADO (lo aporta el modulo fuente al abrir, NO se inventa aqui):** `ModuloGeneral.Contabilizar_Causacion_
  ingreso` (proceso legacy), la TABLA PUENTE fuente<->comprobante (nombre/columnas por definir), la clave de
  idempotencia fisica, y el rol de auth del lado fuente.
- **Contrato abstracto de la tabla puente:** identidad del documento fuente + `voucher_id` del comprobante generado +
  rol del comprobante + trazabilidad (quien/cuando/tx); NO una FK directa en la cabecera de `Voucher`; vive del lado
  fuente. (Nombre fisico y columnas: al build del modulo fuente.)
- **Referencias:** SDD R8 + warning-box; SPEC-CONT-S2 (`Post_Voucher`, captura/ajuste manual = el otro consumidor);
  patron congelado NOVA-SPEC-T-001; ADR de cadena de gasto (linkeados, no copiados).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 + stack + preambulo compartido del kit (SPEC-CONT-000).
- Propias (invariantes de frontera):
  - (a) **UNA VIA fuente->Accounting:** el modulo fuente escribe el asiento SOLO via `Post_Voucher`, dentro de su
    propia tx; Contabilidad NUNCA lee ni escribe tablas del modulo fuente.
  - (b) **ALL-OR-NOTHING EN EL BORDE:** si `Post_Voucher` falla, revierte TODO el documento fuente (no quedan
    documentos fuente aprobados sin contabilizacion, ni asientos sin documento).
  - (c) **SIN BORRADORES AUTOMATICOS:** el flujo automatico NO deja comprobantes en `Accounting.Voucher_Draft`.
  - (d) **ENLACE EN TABLA PUENTE DEL FUENTE, NO FK EN CONTABILIDAD:** el enlace operativo fuente<->comprobante va en
    la tabla puente del modulo fuente con rol del comprobante; NO se agrega FK directa en cabeceras de `Voucher` ni se
    escribe desde Contabilidad.
  - (e) **INMUTABILIDAD:** los comprobantes definitivos son inmutables; ajustes/anulaciones nacen en el modulo fuente
    y generan un NUEVO comprobante relacionado (`Voucher_Relation`); Contabilidad no modifica el original.
  - (f) **PRESUPUESTO NO CONTABILIZA:** `source_module_code = 'budget'` rechazado por `Accounting.Voucher`;
    `Budget_Accounting_Use` solo orienta cuentas, no genera el comprobante.
  - (g) **IDEMPOTENCIA DEL BORDE:** clave natural documento-fuente -> un unico `Voucher`; un reintento no duplica el
    asiento (el contrato lo exige; el mecanismo fisico lo fija el modulo fuente).
  - (h) **VALIDACION CENTRAL EN `Post_Voucher`:** tercero + cuenta auxiliar activa + fecha permitida (P03-P06) +
    debitos=creditos + minimo 2 lineas -- las enforza `Post_Voucher`, no el modulo fuente por su cuenta.
  - (i) **MCP:** el MCP del modulo fuente solo invoca APIs autorizadas del modulo fuente; NUNCA propone SQL contable
    directo.

## 7. Criterios de aceptacion definidos (Given/When/Then; contrato de frontera)
> S6C no tiene THROW-set propio del verifier (N/A por diseno); los negativos citan la validacion central de
> `Post_Voucher` (S2) y las invariantes de frontera. Se verifican al abrir el modulo fuente.
1. **Dado** una causacion aprobada en el modulo fuente, **cuando** el modulo llama `Post_Voucher` en su transaccion,
   **entonces** quedan (i) documento fuente definitivo, (ii) comprobante `posted` con `source_type`
   `income_accrual`/`accounts_receivable_accrual` (no `manual_accounting`), (iii) un registro en la tabla puente
   fuente<->comprobante con rol y trazabilidad.
2. **Dado** el flujo automatico, **cuando** termina, **entonces** NO quedan comprobantes automaticos en
   `Accounting.Voucher_Draft` (el borde no pasa por borradores).
3. **Dado** un fallo de `Post_Voucher` (descuadre, tercero ausente, cuenta mayor, fecha bloqueada, fuente sin
   numeracion), **cuando** ocurre, **entonces** REVIERTE el documento fuente completo y NO persiste documento fuente
   parcial ni asiento.
4. **Dado** un periodo cerrado/enviado (P03/P04/P05/P06), **cuando** el modulo fuente intenta causar con fecha
   bloqueada, **entonces** la API devuelve error funcional y NO persiste documento fuente parcial.
5. **Dado** un comprobante de causacion `posted`, **cuando** se consulta R1 (reportes RO de Contabilidad),
   **entonces** el asiento se refleja inmediatamente (Contabilidad es la fuente de verdad del asiento).
6. **Dado** un ajuste/anulacion de la causacion, **cuando** se procesa, **entonces** NACE en el modulo de
   ingresos/CxC y genera un NUEVO comprobante relacionado (`Voucher_Relation`); Contabilidad NO modifica el original
   (inmutable).
7. **Dado** el enlace fuente<->comprobante, **cuando** se persiste, **entonces** vive en la tabla puente del modulo
   fuente con rol del comprobante; NO hay FK directa en cabeceras de `Voucher` ni escritura desde Contabilidad.
8. **Dado** un reintento de la misma causacion (mismo documento fuente), **cuando** se reprocesa, **entonces** NO se
   duplica el `Voucher` (idempotencia por clave natural del documento fuente).
9. **Dado** `source_module_code = 'budget'` (o Presupuesto como origen), **cuando** intenta postear, **entonces**
   `Accounting.Voucher` lo rechaza (Presupuesto no contabiliza).
10. **Dado** el MCP del modulo fuente, **cuando** opera, **entonces** solo invoca APIs autorizadas del modulo fuente;
    NUNCA propone ni ejecuta SQL contable directo.

## 8. Pruebas / gates definidos
- **Tests de CONTRATO (no harness SQL propio; se ejercitan al abrir el modulo fuente):** el borde all-or-nothing
  (criterio 3), sin borradores (criterio 2), idempotencia por documento fuente (criterio 8), rechazo de
  `budget` (criterio 9), inmutabilidad + ajuste como comprobante relacionado (criterio 6), enlace en tabla puente sin
  FK en Contabilidad (criterio 7).
- **Architecture tests:** el modulo fuente NO ejecuta DML contable directo (solo `Post_Voucher` via gateway tipado);
  Contabilidad NO referencia tablas del modulo fuente; MCP sin SQL contable (criterio 10).
- **Reutiliza la validacion de `Post_Voucher` (S2):** tercero/cuenta/fecha/cuadre -- no se re-implementa aqui; los
  negativos de linea citan la validacion central (S2), no un THROW-set nuevo de S6C.
- **Gate final:** APROBADO del checker FORMAL del Analista (contexto limpio, evalua el CONTRATO + la conformidad del
  modulo fuente cuando abra) + adversarial informal en sesion separada + arch tests + atestacion sha256. **Mientras el
  modulo fuente NO exista, el gate de S6C es la aprobacion del CONTRATO** (esta SPEC), no una corrida de codigo.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Contabilidad se acopla a tablas del modulo fuente (o FK directa) | Rompe el modulo derivado; acoplamiento bidireccional fragil | Restricciones 6a/6d + criterio 7 |
| El fuente deja documento aprobado sin contabilizacion (o asiento sin documento) | Descuadre entre modulos; asiento huerfano | Restriccion 6b (all-or-nothing) + criterio 3 |
| Doble posteo por reintento (sin idempotencia) | Asiento duplicado (el SDD no define la clave) | Restriccion 6g + criterio 8 (clave natural exigida por el contrato) |
| Causacion capturada como comprobante manual desde Contabilidad | Se pierde la atribucion fuente + se salta el borde | s.4 (fuera) + criterio 1 (source_type correcto, no manual) |
| Presupuesto usado como generador contable | Contabilidad derivada de un modulo que no contabiliza | Restriccion 6f + criterio 9 (rechazo `budget`) |
| Contabilidad modifica el comprobante original en un ajuste | Se rompe la inmutabilidad del definitivo | Restriccion 6e + criterio 6 (comprobante relacionado) |
| Inventar el nombre/columnas de la tabla puente antes de cerrar el modelo fuente | Contrato falso que el build no cumple | s.5 (contrato abstracto; nombre fisico al build del fuente) |
| Comprobante automatico residual en `Voucher_Draft` | El borde deja basura no confirmada | Restriccion 6c + criterio 2 |

## 10. Prioridad definida
**GOAL frontera de causacion de ingresos/CxC** (prioridad ALTA en el SDD; Contabilidad como modulo derivado depende
de que los modulos fuente causen bien). Pertenencia Q4: N/A (frontera, no se mide; no esta en la muestra N=6). Es un
CONTRATO de gobernanza, no una superficie con harness propio. Dependencias: el contrato de `Post_Voucher` (existe,
MIGRADO) + el modelo del documento fuente y la tabla puente (CONTEMPLADO, gate previo). **FRONTERA: esta SPEC es el
CONTRATO; el modulo fuente se construye por separado cuando su modelo abra (post-cierre del modelo fuente), no en el
Sprint 1 de Contabilidad.** Desbloquea: que los ingresos/CxC generen asientos gobernados sin acoplar Contabilidad.
**Nota de gaps (RE-CONFIRMAR al abrir el modulo fuente, no supuestos):** (1) la tabla puente NO tiene nombre/columnas
en el SDD -- contrato abstracto, no inventar; (2) el SDD es silencioso sobre la clave de idempotencia -- el contrato
la EXIGE, el fuente la materializa; (3) `income_accrual`/`accounts_receivable_accrual` son TIPOS, no procs -- la
superficie contable ya existe (`Post_Voucher`), falta el CALLER del fuente; (4) el rol de auth vive del lado fuente;
(5) el alcance de `Budget_Accounting_Use` (que orienta vs que consume) se re-confirma al abrir el fuente.
