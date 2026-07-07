# PREP Contabilidad - Esqueleto de SPEC + patron (estructura, sin construir)

> PREP autonoma 2026-07-07 (cola 5h del operador, item 4). ESTRUCTURA SOLO: el operador + DBA preparan
> la BASE SOLIDA de la BD de Contabilidad (patron Presupuesto: BD reconciliada/endurecida primero). Este
> doc deja listo el PATRON y el ESQUELETO de SPEC para enchufar esa base en cuanto llegue. **NO se
> registra tarea ni se construye** hasta: (1) base del DBA lista, (2) Julian onboardeado (build gobernado),
> (3) post-30-jul si cae en la ventana medida. Fuente del patron: SPEC-NOVA-P4-006 (miembro gobernado de
> PAR-2) + el brazo gobernado de Presupuesto.

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
- **Checker:** Analista adversarial FORMAL (contexto limpio, recibe SPEC + diff + BD readonly, NO la
  conversacion del maker) ADEMAS del adversarial informal (subagente).
- **Medicion/atestacion:** captura de tokens en err.log; sha256 de la SPEC via intent del hub; separar
  tokens_adversarial_informal de tokens_checker_formal.

ESPERA la base del DBA (contenido de dominio -- NO inventar):
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
