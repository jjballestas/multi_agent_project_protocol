# SPEC-NOVA-P6-003 - OpenTelemetry / Observabilidad (traces, metrics, logs, health)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Brazo GOBERNADO, pool Q4.
> SPEC de infraestructura transversal (no ata a un proc de BD). Generada desde NOVA_Architecture s.13 + NOVA-GOAL-001.

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P6-003 - task_id (hub): TASK-0246
- owner_maker: agente desarrollador de la instancia gobernada (Sprint 1); repo producto Nova-Budget
- checker: Analista (adversarial, contexto limpio, SPEC + diff + repo)
- arm: gobernado - unit: P6.3 (OpenTelemetry)
- q4_membership: **DENTRO** (criticidad baja; enumerada nominalmente en el pool Q4)
- isolation: item de POOL Q4 gobernado, transversal (infra); SIN hermano baseline y SIN solape con ninguna unidad baseline (no toca read models P2.1/P2.2 ni ajustes P4.x). Manifiesto de archivos leidos: NOVA_Architecture_ExperienciasGH.md (s.13) + NOVA-GOAL-001. leyo_codigo_hermano = NO.
- db_verified_at: N/A (SPEC de infra; no consume objetos BD). El maker verifica la instrumentacion contra el codigo desplegado del vertical slice P1.
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio
- stack (obligatorio): OpenTelemetry SDK .NET (traces/metrics/logs) sobre ASP.NET Core .NET 10; exportadores OTLP; correlation id propagado React+TS+Vite -> NOVA.Api -> NOVA.Application -> NOVA.Infrastructure -> NOVA.Mcp. Anti-patrones PROHIBIDOS: logs sin correlation id, secretos del endpoint OTLP en .config, instrumentacion que acopla dominio a infraestructura.

## 1. Objetivo definido
El operador y el equipo observan NOVA de punta a punta: cada request de negocio genera una traza correlacionada
(React -> API -> caso de uso -> operacion SQL), con metricas por endpoint/duracion-de-SP/errores/validaciones y
logs estructurados con contexto (modulo, usuario, operacion, correlation id), mas health checks de las
dependencias -- todo via OpenTelemetry, sin acoplar el dominio a la infraestructura.
- Fuente: NOVA_Architecture s.13 (Observabilidad) + NOVA-GOAL-001 regla 8 (auditoria+correlation id) y DoD (logs con correlation id) + GOAL-P1 (correlation-id+task_id ya sembrado en la fundacion).
- Calidad: falsable. Bien: "un POST /api/budget/commitment-drafts/{id}/approve emite una traza con spans anidados API->UseCase->SP y un correlation id que aparece en el log estructurado de las 4 capas".

## 2. Usuario objetivo definido
Roles **operador de la metodologia / DevOps / soporte**: consumen trazas, metricas y health para operar y
diagnosticar. No es una superficie de negocio; es capacidad transversal. Sin matriz de permisos de negocio; el
acceso al backend de observabilidad se protege por infraestructura (fuera de esta SPEC).

## 3. Alcance definido
1. Instrumentacion de TRAZAS: un span raiz por request HTTP; spans hijos por caso de uso (NOVA.Application) y por operacion de infraestructura/SQL (NOVA.Infrastructure, incl. duracion del SP/gateway). Propagacion del contexto de traza a NOVA.Mcp cuando actua como cliente interno.
2. CORRELATION ID: generado/propagado desde React (header), aceptado por NOVA.Api, propagado a Application/Infrastructure/Mcp y EMBEBIDO en logs y en la auditoria de toda mutacion (regla 8 del GOAL); enlazado con task_id donde aplique (continuidad con GOAL-P1).
3. METRICAS: por endpoint (conteo, latencia, codigos), duracion de SPs/gateways, tasa de errores de negocio (ProblemDetails) y de validaciones fallidas.
4. LOGS estructurados: nivel + timestamp + modulo + usuario + operacion + correlation id (+ tenant si aplica); errores de negocio con codigo THROW y ProblemDetails asociado.
5. HEALTH CHECKS: SQL Server (DbsFinanciero), servicios internos, y el estado de migraciones; endpoint de health expuesto.
6. Exportacion OTLP configurable por ambiente (endpoint/credenciales fuera del repo).

## 4. Fuera de alcance definido
- El backend/coleccion de observabilidad (Collector, almacenamiento, dashboards): despliegue/infra, no esta SPEC.
- Seguridad/OIDC/JWT (P6.1) y auditoria de negocio como tabla (P6.2): SPECs separadas; esta SPEC SOLO embebe el correlation id en la auditoria existente, no define su esquema.
- Metricas de negocio/BI (ejecucion presupuestal): es reporte (P2.2 baseline / Doc 11), NO observabilidad tecnica.
- Cualquier cambio a la logica de dominio o a los procs de BD por instrumentar (la observabilidad es no intrusiva).

## 5. Contenido / assets definidos
- **Codigo:** wiring de OpenTelemetry en `NOVA.Api/Program.cs` (AddOpenTelemetry: Tracing + Metrics + Logging); `NOVA.Infrastructure/Observability/` (ActivitySource por capa, instrumentacion de gateways/SPs con duracion); middleware de correlation id en `NOVA.Api/Middleware/`.
- **Instrumentacion:** AspNetCore + HttpClient (para Mcp) + SqlClient (duracion de comandos); ActivitySource propios para casos de uso; Meter propios para las metricas de negocio-tecnico (errores/validaciones).
- **Contratos:** header de correlation id estandar (p.ej. `X-Correlation-Id` / W3C traceparent); DTO de health.
- **Config:** endpoint OTLP + service.name/version por ambiente (Secret Manager/variables, NUNCA .config con secretos).
- **Referencias:** NOVA_Architecture s.13 (Observabilidad) + s.11 (MCP como cliente interno, propaga correlation id), NOVA-GOAL-001 (regla 8, DoD, P1 correlation-id+task_id), NOVA_Apendice_Estructura_DotNet10.

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 (esp. 4 casos de uso -> gateways tipados; 8 auditoria+correlation id; DoD logs con correlation id) + maestro-P1..P6 + stack del preambulo.
- Propias:
  - (a) La instrumentacion es NO INTRUSIVA: NOVA.Domain NO referencia OpenTelemetry ni Infrastructure (architecture test); la observabilidad vive en Api/Infrastructure/Application-abstractions.
  - (b) TODO log lleva correlation id (regla dura del GOAL); un log sin correlation id = defecto.
  - (c) El correlation id se propaga a las 4 capas y a Mcp; se acepta el entrante de React si viene (W3C traceparent) o se genera en el borde.
  - (d) Secretos del exportador OTLP fuera del repo (Secret Manager/variables); jamas en appsettings versionado.
  - (e) La duracion de SPs/gateways se mide en Infrastructure sin cambiar el contrato de los gateways tipados (no DataTable).
  - (f) Health checks no exponen datos sensibles ni cadenas de conexion.

## 7. Criterios de aceptacion definidos (Given/When/Then)
1. **Dado** un request de negocio (p.ej. aprobar un CDP), **cuando** se ejecuta, **entonces** se emite una traza con span raiz HTTP + span de caso de uso + span de la operacion SQL (con duracion del SP), todos con el mismo trace id.
2. **Dado** un correlation id entrante desde React (header), **cuando** atraviesa API->Application->Infrastructure->Mcp, **entonces** el MISMO correlation id aparece en los logs estructurados de las 4 capas y en la auditoria de la mutacion.
3. **Dado** una mutacion sin correlation id, **cuando** se registra, **entonces** el gate lo detecta como defecto (ningun log de mutacion sin correlation id).
4. **Dado** un error de negocio (THROW->ProblemDetails), **cuando** ocurre, **entonces** se incrementa la metrica de errores de negocio con la etiqueta del endpoint y el log lleva el codigo THROW.
5. **Dado** el endpoint de health, **cuando** se consulta, **entonces** reporta el estado de SQL Server, servicios internos y migraciones, sin exponer secretos.
6. **Dado** NOVA.Domain, **cuando** corre el architecture test, **entonces** NO referencia OpenTelemetry ni Infrastructure (instrumentacion no intrusiva).
7. **Dado** la config, **cuando** se inspecciona el repo, **entonces** NO hay endpoint/credencial OTLP versionado (secretos fuera del repo).

## 8. Pruebas / gates definidos
- **Unit:** middleware de correlation id (genera/propaga/acepta entrante); mapeo error de negocio -> metrica + log con THROW.
- **Architecture tests:** Domain sin OpenTelemetry/Infrastructure; Application sin ASP.NET; el correlation id fluye por abstracciones, no por acople directo.
- **Integracion:** un request end-to-end del vertical slice P1 produce la traza esperada (spans anidados) y el correlation id en los logs de las 4 capas (assert sobre el exportador en memoria/test); health check responde con las dependencias; ausencia de secretos en config (scan).
- **Gate final:** APROBADO del Analista (12 puntos, enfasis en 2=no reimplementacion/no acople de dominio, 10=regresion documental de runbook de observabilidad, 11=mensajes de error) + DoD de NOVA-GOAL-001 con evidencia real (traza capturada, logs con correlation id, health) + verde de gates del hub + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Acoplar el dominio a OpenTelemetry | Rompe la pureza de NOVA.Domain (regla de capas) | Restriccion 6a; architecture test (criterio 6) |
| Logs sin correlation id | Trazabilidad rota (viola regla 8/DoD del GOAL) | Restriccion 6b; criterio 3 lo detecta |
| Secretos del exportador OTLP en el repo | Exposicion de credenciales | Restriccion 6d; criterio 7 (scan) |
| Instrumentacion que altera el contrato de los gateways (DataTable) | Viola regla 5 del GOAL | Restriccion 6e: medir duracion sin cambiar el contrato tipado |
| Confundir metricas tecnicas con reporte de negocio (P2.2) | Solape con territorio de reporte/baseline | Campo 4 lo excluye: observabilidad tecnica != reporte de ejecucion |
| Health check que filtra cadenas de conexion | Fuga de datos sensibles | Restriccion 6f; criterio 5 |

## 10. Prioridad definida
**GOAL-P6** (release operable: observabilidad), brazo GOBERNADO, unidad P6.3. **Pertenencia Q4: DENTRO**
(criticidad baja; enumerada nominalmente en el pool Q4; su bajo riesgo calibra la fabrica de tareas del estudio).
Severidad s.08: capacidad transversal, no bloqueante de negocio. Dependencias: GOAL-P1 (fundacion tecnica ya
siembra correlation-id+task_id, health/OpenAPI/ProblemDetails/logging estructurado; P6.3 extiende ese piso a OTel
completo). NO depende de brecha de BD (es infra; no consume procs). AISLAMIENTO: transversal, sin hermano baseline
ni solape con read models/ajustes baseline. Desbloquea: operacion observable del Sprint 1 (diagnostico de jams,
latencias de SP, tasa de errores por endpoint) -- util para la propia instrumentacion del estudio.
