# PREP Contabilidad - Esqueleto de SPEC + patron (estructura, sin construir)

> PREP autonoma 2026-07-07 (cola 5h del operador, item 4). ESTRUCTURA SOLO: el operador + DBA preparan
> la BASE SOLIDA de la BD de Contabilidad (patron Presupuesto: BD reconciliada/endurecida primero). Este
> doc deja listo el PATRON y el ESQUELETO de SPEC para enchufar esa base en cuanto llegue. **NO se
> registra tarea ni se construye** hasta: (1) base del DBA lista, (2) Julian onboardeado (build gobernado),
> (3) post-30-jul si cae en la ventana medida. Fuente del patron: SPEC-NOVA-P4-006 (miembro gobernado de
> PAR-2) + el brazo gobernado de Presupuesto.

## HITO 2026-07-11 (UTC) -- BASE SOLIDA + WS1 + THROW reales CAPTURADOS (design-source, fuera del hub)

> DISPOSICION GOBERNADA (Arquitecto, sesion 2026-07-11 ~00:25 local UTC+2): el operador cerro con el DBA la
> BASE SOLIDA de la BD de Contabilidad (patron Presupuesto) y verifico un fix de integridad, todo en el
> paquete DESIGN-SOURCE `D:/Agentes/Ingenas` (FUERA del hub). Esto es design-source PREP; NO abre el build
> gobernado (sigue gated por Julian onboardeado + base en el hub + calendario post-30-jul) y NO toca el
> baseline congelado ni el core pineado (epoch 1.14.0, config 2E35F26E). Registro = este artefacto atestado
> (#4, via commit gobernado) + FYI al operador. NO es DECISION (no cambia protocolo/frontera/dominio) ni
> task de build (las tareas de build de Contabilidad viven en el ledger de la instancia -- DECISION-0050 --
> y crearlas aqui rozaria abrir el build gated).

ENTREGADO (con evidencia; rutas relativas a `D:/Agentes/Ingenas`):
- **WS1 (57 formularios legacy -> casos de uso, por slice, con THROW por proc):**
  `dictionary/accounting_ws1_base_solida.html` (verificado presente).
- **Brechas cerradas para "base solida", desplegadas en DbsFinanciero + DbsFinanciero_SANDBOX + SNJDC**
  (smokes con ROLLBACK, residuo 0):
  - CGN/CHIP trimestral: `sql/accounting/definitive/schema/027` (catalogo CHIP versionado, lote, export al
    centavo, P05; no reproduce el ajuste de un peso). THROW 54400-54457.
  - Cierre anual: `sql/accounting/definitive/schema/028` (comprobante annual_close via Post_Voucher, saldos
    iniciales de la siguiente vigencia por cuenta-tercero, P07). THROW 54460-54487.
- **F-NOVA-01:** THROW reales re-verificados contra OBJECT_DEFINITION en las 3 BD (WS1 seccion D).
- **FIX DE INTEGRIDAD (verificado estaticamente por el asistente del operador):** el bypass de periodo
  cerrado del cierre anual se acoto a una escotilla `SESSION_CONTEXT(N'accounting_annual_close')` que SOLO
  activa `Accounting.Close_Annual_Accounting_Period` (set antes de Post_Voucher, reset despues y en CATCH).
  Las 3 guardas (52204 trg_voucher__validate_insert, 52233 Post_Voucher, 52512 trg_voucher__date_controls)
  usan `AND NOT (item='annual_close' AND COALESCE(TRY_CONVERT(int, SESSION_CONTEXT(...)),0)=1)`. Captura
  manual restringida a los 3 tipos manuales (THROW 52252), sin regresion de otros modulos (solo aplica a
  `source_module='accounting'` y not system_generated). Objetos: `schema/015`, `schema/023`, `schema/028`.

EFECTO EN EL ESQUELETO: los placeholders del ESQUELETO SPEC-CONT (s.1) YA SON INSTANCIABLES por unidad --
el contenido de dominio que esperaba la base del DBA (mapa formularios->unidad, THROW reales por proc,
tablas base/reverso, modelo de estados + auth) esta disponible en el paquete design-source. La
instanciacion por-unidad y el registro de tareas de build siguen GATED (Julian onboardeado + base en el
hub + Sprint 1 post-30-jul). Ver s.4 (backlog) para el follow-up de endurecimiento no bloqueante.

## 0. Lo que YA se puede fijar (pattern-ready) vs lo que ESPERA la base del DBA

READY (invariantes de patron, heredados de Presupuesto -- no dependen de la base):
- **Superficie sobre procs, no reimplementacion en C#:** cada unidad de Contabilidad es una superficie
  tipada sobre un proc de hardening (validacion + efectos coordinados + guarda bloqueante en SQL); la capa
  de aplicacion NO reimplementa la logica de negocio ni el reverso de saldo.
- **F-NOVA-01 (re-verificacion de THROW):** los codigos de error (THROW) de cada proc se RE-CONFIRMAN
  contra el `OBJECT_DEFINITION` del proc desplegado al construir, nunca por analogia ni por rango
  documentado sin base. Preflight ampliado (VIEW DEFINITION + SELECT) lo hace el DBA por unidad.
- **Guard de procedencia:** la evidencia F-NOVA-01 se versiona con una clase SQL real (gateada por env
  vars, NA limpio sin credenciales); NINGUN mock/Recording* in-memory con resultados hardcodeados la
  sustituye. Lo verifican el checker formal (Analista) Y el adversarial informal.
- **Aislamiento intra-par/intra-familia:** manifiesto explicito de archivos leidos en el DoD; el maker de
  una unidad NO lee la implementacion de una unidad hermana isomorfa (contaminacion = fuera del
  confirmatorio). Aplica si Contabilidad se mide como pares.
- **Auth real desde el arranque gobernado:** a diferencia del baseline de Presupuesto (supuesto DD-01 sin
  wiring), el brazo gobernado incluye wiring real de autenticacion/autorizacion (rol + [Authorize]/
  RequireAuthorization real) como parte del contrato. Contabilidad hereda esto.
- **Stack obligatorio:** React+TS+Vite (front sin SQL) / ASP.NET Core .NET (capas) + MCP / SQL Server via
  gateways tipados / OpenTelemetry / ProblemDetails. **Anti-patrones PROHIBIDOS:** WebForms/PageMethods,
  DataTable entre capas, DLLs manuales, capa DATABASE generica, secretos en .config, centinelas -99.
- **Gates de patron (verdes por exit-code, heredados del baseline Presupuesto/GOAL-P1):** (a) `dotnet build`
  limpio; (b) `dotnet test` = unit + **architecture tests** (los 5 arch tests del baseline: capas, sin
  DataTable entre capas, front sin SQL, gateway tipado, sin anti-patrones) + integracion HTTP verde en
  CLON LIMPIO; (c) **F-NOVA-01 real** (guard de procedencia con clase SQL gateada por env, NA limpio) +
  al menos un NEGATIVO por THROW ALCANZABLE re-verificado contra `OBJECT_DEFINITION`; (d) neutralidad de
  dominio + `scan_encoding` sobre la SPEC/artefactos del hub. Ningun mock/Recording* sustituye (c). El
  CONTENIDO por-unidad de (b)/(c) (que arch test aplica, que THROW) ESPERA la base del DBA; el PATRON de
  gates es fijo ahora.
- **Checker:** Analista adversarial FORMAL (contexto limpio, recibe SPEC + diff + BD readonly, NO la
  conversacion del maker) ADEMAS del adversarial informal (subagente).
- **Medicion/atestacion:** captura de tokens en err.log; sha256 de la SPEC via intent del hub; separar
  tokens_adversarial_informal de tokens_checker_formal.

ENTREGADO POR LA BASE DEL DBA (design-source, 2026-07-11 -- ver HITO arriba; ya NO se espera, se instancia):
- El mapa **~57 formularios -> casos de uso** (que superficie es cada unidad).
- El mapeo **Access -> esquema SQL Accounting** (~37 tablas maco/Cont): tablas base, tablas de reverso,
  procs de hardening por unidad.
- Los **THROW / guardas bloqueantes** reales por proc (F-NOVA-01, del OBJECT_DEFINITION).
- La **descomposicion S/M/L** de las unidades y su membresia de par/medicion.
- El **modelo de estados** contable (analogo a BudgetDocumentState) y quien ejecuta cada transicion (auth).

## 1. Esqueleto de SPEC por unidad de Contabilidad (rellenar por unidad, patron P4-006)

```
# SPEC-CONT-<Px-NNN> - <Unidad> (<brecha/RN>, <arm/par si mide>)

## Preambulo de gobierno (DoR)
- spec_id / task_id (hub): asignado al registrar la tarea de superficie (post-base + Julian; post-30-jul si mide).
- owner_maker: agente desarrollador de la instancia gobernada (Contabilidad); repo producto <Nova-Contabilidad>.
- checker: Analista adversarial FORMAL (contexto limpio) + adversarial informal.
- arm / q4_membership / isolation: <segun sorteo del sello si mide; CRITICA si es par isomorfo>.
- precondicion / preflight (F-NOVA-01): proc de hardening EXISTE + verificado por el DBA (N/N pruebas);
  GRANT EXECUTE + VIEW DEFINITION + SELECT concedidos; set REAL de THROW del OBJECT_DEFINITION.
- guard de procedencia: evidencia SQL real gateada por env vars; sin mocks.
- diseno de autorizacion: rol + auth real (no supuesto).
- db_verified_at / attestation (sha256) / stack (obligatorio, anti-patrones prohibidos).

## 1. Objetivo definido (FALSABLE)
## 2. Usuario objetivo definido (rol)
## 3. Alcance definido
## 4. Fuera de alcance definido
## 5. Contenido / assets definidos
## 6. Restricciones tecnicas definidas (superficie-sobre-proc; F-NOVA-01; auth; aislamiento; sin reimplementar)
## 7. Criterios de aceptacion definidos (Given/When/Then; +un NEGATIVO por THROW ALCANZABLE, re-verificado)
## 8. Pruebas / gates definidos (unit + integracion HTTP + F-NOVA-01 real; gates verdes por exit-code)
## 9. Riesgos definidos (contaminacion intra-par; reusar gateway/UI hermano; THROW asumido por analogia)
## 10. Prioridad definida
```

## 2. Flujo de trabajo cuando llegue la base (WS1 -> SPECs -> build)
1. **WS1 (analisis, mio, sobre la base):** mapear los ~57 formularios a casos de uso; Access -> esquema SQL
   Accounting; identificar procs de hardening, THROW, tablas base/reverso por unidad; descomposicion S/M/L;
   modelo de estados + auth. Insumo del corpus Etapa 2.
2. **SPECs por unidad:** instanciar el esqueleto s.1 con el contenido de dominio del WS1 (F-NOVA-01 real).
3. **Build gobernado (Julian + Sprint 1):** registrar tareas de superficie, gate Analista formal +
   adversarial, aislamiento, atestacion. Respeta la linea roja Q4/30-jul.

## 3. Frontera (recordatorio)
Nada de esto toca el estudio medido, el genesis del hub, ni la Q4. El BUILD gobernado espera a Julian +
la base del DBA. Solo la ESTRUCTURA/PATRON avanza ahora. Cuando la base este lista, este esqueleto se
enchufa: el analisis WS1 llena los placeholders y las SPECs se instancian.

Estado al 2026-07-11: la BASE DEL DBA esta ENTREGADA en design-source (ver HITO arriba) -> los
placeholders son instanciables. Lo que sigue gated es el BUILD gobernado (Julian onboardeado + base
promovida al hub/instancia + Sprint 1 post-30-jul). El pubkey ed25519 de Julian (`jheredia:v1`) LLEGO;
la re-genesis A2 del config de Aegis + alta en agent_registry + gate e2e de 2 clones esperan GO explicito
del operador (reactiva agentes) -- NO se ejecuta unilateralmente.

## 4. Backlog / follow-up (no bloqueante)
- **Endurecer captura manual (source_module_code):** hacer que la captura manual FIJE
  `source_module_code='accounting'` para que el THROW 52252 no sea esquivable a nivel BD (hoy
  `Post_Voucher_Draft` lo lee del draft). El bypass de periodo cerrado NO depende de esto -- lo cubre la
  escotilla `SESSION_CONTEXT(N'accounting_annual_close')` de forma independiente. Se instancia como
  unidad/hardening cuando abra el build gobernado de Contabilidad; no reabre el sello ni el baseline.
