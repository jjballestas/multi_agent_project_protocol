# Session report - Eficiencia de tokens + Runtime M0 + claims por fila

- Date: 2026-06-05
- Phase: P2 (Adopcion y expansion)
- Process status: closed (checkpoint commiteado; quedan tareas `ready` para la proxima sesion)
- Ratification: draft (redactado por Claude; pendiente ratificacion de Codex)

## 1. In One Sentence
Se cerro el track de eficiencia de tokens (cold-start **-75%**), se entrego el **runtime M0** del
orquestador, y una colision real en vivo origino **DECISION-0011 (claims por fila)** que ya quedo
implementada — todo verde y commiteado en `8c09037`.

## 2. What Was Done
- **Medidor de costo de contexto** (TASK-0023): `measure_context_cost.py/.ps1` + bloque `token_cost`,
  `--json`/`--budget`, read-only. Gate before/after.
- **Poda de estado a historico** (TASK-0024): `CLAIMS_ARCHIVE`/`TASK_INDEX_ARCHIVE`; el validador lee
  `caliente ∪ archivo`. Cold-start **37 391 -> ~9.5k tokens (-75%)** sin perder nada (archivar != borrar).
- **Runtime M0** (TASK-0026 diseno, TASK-0027 impl): contrato de turno (`turn_schema.json`), router
  determinista, validador de turno (esquema + write-allowlist + anti-carrera) y `orchestrator --plan`
  dry-run; `enabled:false` por defecto; `runtime/**` en el scan de neutralidad.
- **Claims por fila** (DECISION-0011, TASK-0028): el chequeo de solape trataba `TASK_INDEX`/`PROJECT_STATE`
  como archivo completo y serializaba el trabajo paralelo; ahora soporta scope `ruta#fila`.
- **Diseno runtime M1 y M2** (TASK-0029): apply+gate+commit/revert + interfaz adapter + replay loop
  (SPEC-0029/0030); M2 (adapters reales + loop autonomo + observabilidad) esbozado.

## 3. SDD Summary
- Specs creadas: SPEC-0028 (claims por fila), SPEC-0029 (apply+gate+vcs), SPEC-0030 (adapter+replay+loop).
- Tasks implementadas contra spec: TASK-0023 (SPEC-0023), TASK-0024 (SPEC-0024), TASK-0027 (SPEC-0026/0027),
  TASK-0028 (SPEC-0028). Diseno: TASK-0026, TASK-0029.
- Acceptance satisfechas: medidor 3 escenarios + read-only; poda sin perdida + validador union + -75%;
  runtime M0 12/12 golden; claims por fila 5/5 golden con paridad PowerShell.
- Test plans ejecutados: golden + validador + scan + regresion en los 4 ejemplos; todos verdes.
- Desviaciones: runtime M1 acota la invocacion de agente real a **M2** (M1 usa replay adapter para ser
  determinista). Documentado en DISENO-runtime-m1 §0.

## 4. Decisions
- **DECISION-0011 (claims por fila):** nacida de una colision real en vivo (Claude y Codex necesitaban
  los mismos JSON de estado). Aditiva/MINOR; `CLAIMS.json`/`mailbox` siguen exentos; atomicidad fisica
  via escritor unico del orquestador. Consecuencia: Claude y Codex pueden tocar filas distintas del
  estado sin serializarse.
- Bajo **DECISION-0008** (tokens) y **DECISION-0009** (runtime), sin cambios de frontera nuevos.

## 5. Current Project State
- Commit `8c09037` en `main`; arbol limpio; validador + scan + golden verdes; cold-start ~9.5k tok.
- Done: TASK-0023, 0024, 0026, 0027, 0028, 0029. Ready: TASK-0025, 0030, 0031.
- Sin claims activos. Sin mensajes que requieran respuesta.

## 6. Next Steps
1. **Codex:** TASK-0025 (frontmatter minimo) -> TASK-0030 (runtime M1 apply+gate) -> TASK-0031 (loop).
2. **Claude:** revisar esas entregas; derivar specs/tasks de **runtime M2** tras aceptar M1.
3. Eventual corte de version: tokens (v0.7.0) cuando cierre 0025; runtime (v0.8.0) cuando cierre M1.
4. Proxima poda: archivar la ventana reciente de done (0024/0027/0028/0029).

## 7. What We Need From The Human Owner
- **Push** del commit `8c09037` (local; pendiente de tu visto bueno para subir al remoto privado).
- Confirmar prioridad de la proxima sesion: cerrar tokens (0025) vs avanzar runtime M1 (0030/0031).
- Aprobacion humana sera necesaria para **activar** el runtime (`enabled:true`) cuando llegue M2.

## 8. Risks Or Ambiguities
- Acumulacion de tareas `done` en estado caliente (ventana reciente): mitiga la proxima poda.
- Disenos M1/M2 por delante de la implementacion: bajo riesgo de churn (la interfaz de adapter esta fija).
- Activar el runtime sobre el repo real es cambio de modo de operacion: gate humano obligatorio.

## 9. Communication Status
- Open messages (requiring response): ninguno.
- Active blocks: ninguno.
- Decisions required / human-required: push del commit + prioridad de la proxima sesion (no bloqueante).

## 10. Details
- Decisiones: DECISION-0008, DECISION-0009, DECISION-0011.
- Specs: SPEC-0023/0024/0026/0027/0028/0029/0030.
- Tasks: TASK-0023/0024/0026/0027/0028/0029 (done), TASK-0025/0030/0031 (ready).
- Artefactos: DISENO-eficiencia-de-tokens, DISENO-runtime-orquestacion-automatizada, DISENO-runtime-m1,
  DISENO-runtime-m2.
- Commit: `8c09037` (checkpoint verde de la sesion).
