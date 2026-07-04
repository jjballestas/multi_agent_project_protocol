# SPEC-NOVA-P2-003 - UI de exploracion (shell frontend: grilla, filtros, detalle, export)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Brazo GOBERNADO, pool Q4.
> SPEC de FRONTEND (React) transversal. Generada desde NOVA-GOAL-001 (GOAL-P2 "UI de exploracion") + arquitectura.

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P2-003 - task_id (hub): TASK-0246
- owner_maker: agente desarrollador de la instancia gobernada (Sprint 1); repo producto Nova-Budget (apps/nova-web)
- checker: Analista (adversarial, contexto limpio, SPEC + diff + app)
- arm: gobernado - unit: P2.3 (UI de exploracion)
- q4_membership: **DENTRO** (criticidad BAJA; calibra la taxonomia de defectos D1-D4 del estudio -- tarea de bajo riesgo, alto valor de calibracion)
- isolation: FRONTEND puro (React+TS). SIN backend read-model propio; SIN SQL; consume endpoints existentes de forma GENERICA. No reimplementa ni referencia los read models BASELINE P2.1 (parametros) ni P2.2 (reporte de ejecucion): es la CAPA DE PRESENTACION reutilizable, no su logica. Manifiesto de archivos leidos: NOVA-GOAL-001 + arquitectura (s.10 desacoplamiento frontend). leyo_codigo_hermano = NO.
- **measurement (DIRECTIVA operador medicion-real 2026-07-04):** cache-confound -> ambos brazos MISMO runtime/tipo de sesion (cache comparable) o declarar el confound; captura de tokens = err.log (stderr); desglose por cubeta no capturable -> tokens_total_atribuibles. checker_formal=0 en el brazo baseline.
- db_verified_at: N/A (frontend; no consume BD). El maker verifica contra los contratos OpenAPI del vertical slice P1.
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio
- stack (obligatorio): React + TypeScript + Vite; cliente generado desde OpenAPI; el frontend JAMAS accede a SQL ni duplica logica transaccional (regla 1/pre-validacion solo de formato). ProblemDetails renderizado como error de negocio. Anti-patrones PROHIBIDOS: logica de negocio critica en React, llamadas SQL desde el front, acoplar la UI a un endpoint concreto (debe ser generica/reutilizable).

## 1. Objetivo definido
El usuario explora cualquier conjunto de datos de Budget (parametros, listados por documento, reportes) desde una
UI reutilizable -- grilla densa con filtros, detalle y export -- que consume los endpoints REST existentes de forma
generica, renderiza errores de negocio (ProblemDetails) y no reimplementa ninguna logica de backend.
- Fuente: NOVA-GOAL-001 GOAL-P2 ("Implementar UI de exploracion: grilla, filtros, detalle, export basico") + arquitectura s.10 (desacoplamiento frontend) + DoD (sin SQL desde React).
- Calidad: falsable. Bien: "la grilla se instancia sobre `GET /api/budget/commitments` con su panel de filtros derivado del contrato OpenAPI, pagina en servidor, muestra el detalle de una fila y exporta lo consultado, sin ninguna llamada SQL".

## 2. Usuario objetivo definido
Rol **Consulta / Gestion de presupuesto** (operador diario): explora, filtra, inspecciona y exporta. Es capacidad
de presentacion transversal; el control de acceso real es del backend (los endpoints), no de la UI. La UI solo
valida FORMATO de entrada (fechas, rangos), nunca reglas transaccionales (viven en backend, arquitectura s.10).

## 3. Alcance definido
1. **DataGrid** reutilizable: columnas tipadas desde el DTO, orden, paginacion en SERVIDOR (delega al endpoint), densidad configurable, formato de moneda (miles de pesos, presentacion).
2. **FilterPanel** generico: deriva los controles de filtro de los parametros del endpoint (fecha/rango/enum/texto); aplica y limpia; vigencia EXPLICITA (F-NOVA-05), sin default cuando `is_current` no es confiable.
3. **DetailDrawer/View**: inspeccion de una fila (todos los campos del DTO) sin consulta adicional si el resultset ya los trae.
4. **Export**: exporta EXACTAMENTE lo consultado (mismos filtros, mismas cifras) a CSV/XLSX en cliente sobre el resultset recibido.
5. **Manejo de errores**: renderiza `ProblemDetails` (codigo/titulo/detalle) como mensaje de negocio; distingue 400 (parametros) de 200-vacio (sin datos) con leyenda de grilla.
6. **Cliente OpenAPI**: consumo tipado generado del contrato; correlation id propagado en cada request (observabilidad, P6.3).

## 4. Fuera de alcance definido
- Los READ MODELS de backend (parametros P2.1 baseline, reporte de ejecucion P2.2 baseline, listados P2-004): esta SPEC NO los implementa ni los referencia por logica; solo los CONSUME como endpoints genericos.
- Reglas de negocio/validacion transaccional (viven en backend; la UI solo valida formato).
- Autenticacion/OIDC (P6.1) y observabilidad backend (P6.3): SPECs separadas; la UI solo propaga correlation id y renderiza el estado de auth existente.
- Graficas/BI: la exploracion es grilla+filtros+detalle+export, no dashboards analiticos.

## 5. Contenido / assets definidos
- **Codigo (apps/nova-web):** componentes `ExplorationGrid`, `FilterPanel`, `DetailDrawer`, `ExportButton`, `ProblemDetailsAlert`; hook `useExplorationQuery` (paginacion/orden/filtros server-side); cliente OpenAPI tipado.
- **Contratos consumidos (genericos):** cualquier `GET` de listado/lectura de Budget que exponga resultset + parametros (p.ej. los de P2-004, el reporte, parametros); la UI se configura por endpoint, no se acopla a uno.
- **Presentacion:** formato de moneda (miles de pesos), densidad, i18n es-CO.
- **Referencias:** NOVA-GOAL-001 (GOAL-P2 + catalogo de APIs + DoD), arquitectura s.10 (desacoplamiento) y s.13 (correlation id). (NO se referencia la logica de los read models baseline -- aislamiento.)

## 6. Restricciones tecnicas definidas
- Heredadas: reglas de NOVA-GOAL-001 (1 React nunca SQL; 7 ProblemDetails; DoD sin SQL desde React, frontend typecheck) + arquitectura s.10 + stack del preambulo.
- Propias:
  - (a) React JAMAS accede a SQL ni consume DLLs/logica local; solo APIs HTTP tipadas (OpenAPI).
  - (b) La UI valida FORMATO (fecha/rango), NUNCA reglas transaccionales (backend es la palabra final).
  - (c) Paginacion/orden en SERVIDOR (delega al endpoint); el export es sobre el resultset recibido, no re-consulta.
  - (d) Componentes GENERICOS/reutilizables: no acoplar la grilla/filtros a un endpoint concreto (se configura por contrato); asi la misma UI sirve listados, reporte y parametros.
  - (e) Vigencia explicita (F-NOVA-05); ProblemDetails renderizado como negocio (no stack traces ni "Error 50115" a secas).
  - (f) Correlation id propagado en cada request (P6.3); typecheck de frontend en verde (DoD).

## 7. Criterios de aceptacion definidos (Given/When/Then)
1. **Dado** un endpoint de listado (p.ej. `GET /api/budget/obligations`), **cuando** monto la ExplorationGrid sobre el, **entonces** renderiza columnas tipadas del DTO, pagina en servidor y ordena delegando al endpoint (sin traer todo el dataset).
2. **Dado** el FilterPanel, **cuando** aplico filtros (vigencia, fecha, fuente), **entonces** la grilla re-consulta el endpoint con esos parametros; vigencia es explicita (sin default enganoso).
3. **Dado** una fila, **cuando** abro el detalle, **entonces** muestra todos los campos del DTO sin consulta adicional (si el resultset los trae).
4. **Dado** un resultado, **cuando** exporto, **entonces** el archivo reproduce exactamente la grilla consultada (mismos filtros/cifras) desde el resultset.
5. **Dado** un 400 con ProblemDetails, **cuando** la API responde, **entonces** la UI muestra el mensaje de negocio (codigo/titulo/detalle); un 200 vacio muestra leyenda "sin datos".
6. **Dado** el codigo del front, **cuando** corre el gate, **entonces** NO hay ninguna llamada SQL ni logica transaccional en React (grep/lint) y el typecheck pasa.
7. **Dado** la misma UI, **cuando** se configura sobre dos endpoints distintos (listado y reporte), **entonces** funciona sin cambios de codigo especificos por endpoint (reutilizacion; criterio de la exploracion generica).

## 8. Pruebas / gates definidos
- **Unit (frontend):** `useExplorationQuery` (paginacion/orden/filtros server-side); render de ProblemDetails; export sobre resultset; validacion de formato.
- **Typecheck + lint:** frontend typecheck en verde (DoD); lint que prohibe fetch a rutas no-API / patrones SQL.
- **Integracion (component/e2e ligero):** montar la grilla sobre un endpoint del vertical slice P1, aplicar filtros, ver detalle y exportar; verificar paginacion server-side (no trae todo); render de error de negocio.
- **Gate final:** APROBADO del Analista (12 puntos, enfasis en 3=no SQL directo desde React, 6=UX de fallo con mensajes de negocio, 10=regresion de documentacion de componentes) + DoD de NOVA-GOAL-001 (compila front, typecheck, sin SQL desde React) con evidencia real (capturas del flujo) + verde de gates del hub + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Logica de negocio/validacion transaccional en React | Divergencia con el backend; viola regla 1/arquitectura | Restriccion 6a/6b; el adversarial busca logica de negocio en el front |
| Llamada SQL o acceso a datos desde React | Rompe el desacoplamiento | Restriccion 6a; lint/grep (criterio 6) |
| Traer todo el dataset y paginar en cliente | Latencia con resultsets grandes (652+ filas) | Restriccion 6c: paginacion en servidor (criterio 1) |
| Acoplar la UI a un endpoint concreto | Pierde el valor de exploracion generica | Restriccion 6d; criterio 7 (dos endpoints, un codigo) |
| Reimplementar/duplicar un read model baseline (P2.1/P2.2) | Solape de territorio | Campo 4: la UI solo CONSUME endpoints, no implementa read models |
| Errores como stack trace o "Error 5011x" | UX de fallo pobre | Restriccion 6e: ProblemDetails como negocio (criterio 5) |

## 10. Prioridad definida
**GOAL-P2** (read model / UI de exploracion), brazo GOBERNADO, unidad P2.3. **Pertenencia Q4: DENTRO** (criticidad
BAJA; su bajo riesgo la hace ideal para CALIBRAR la taxonomia de defectos D1-D4 del estudio). Severidad s.08:
capacidad de presentacion transversal, no bloqueante. Dependencias: GOAL-P1 (fundacion: React+TS+Vite scaffold,
cliente OpenAPI, ProblemDetails) + al menos un endpoint de lectura para montar la exploracion (p.ej. P2-004 o los
read models existentes). NO depende de brecha de BD (es frontend puro). AISLAMIENTO: FRONTEND, sin backend
read-model propio; consume endpoints genericos; no reimplementa ni lee la logica baseline P2.1/P2.2. Desbloquea: la
experiencia de exploracion reutilizable para todas las pantallas de Budget.
