# 02_Asistente - Orden para el arquitecto: medicion #3 + loop por etapas hacia Fase 1/2

> Insumo del operador (asistente Cowork) para el ARQUITECTO (Claude en VS Code).
> El asistente no muta estado ni habla con Codex; esto se ejecuta desde VS Code via submit_intent.
> Fecha: 2026-06-14. Fuente: sintesis_hoja_de_ruta (Fases 0-6) + verificacion read-only del repo a HEAD 237f04d (v1.5.0).

## 0. Objetivo del operador (lo que quiere)

1. Construir la medicion por handoff (#3, cost-attribution) y marcarla hecha.
2. Activar el loop autonomo para que los agentes ejecuten Fase 1 (Skills) y Fase 2 (Connectors).
3. Revisar metricas para observar el comportamiento del loop.

## 1. Hallazgo de verificacion (estado real vs hoja de ruta)

Verificado read-only contra el repo:

- Fase 1 (E1 Skills): NO existe. Sin `skill_registry` en `protocol.config.json`, sin contrato `SKILL` en `Area_comun/protocol/`, sin digestion.
- Fase 0 (prerequisito): incompleta. `Area_comun/protocol/FAILURE_MODES.md` (E5) NO existe; `protocol_research/` (#1) NO existe.
- Fase 2 (E2 Connectors): NO existe. `runtime/adapters/` solo tiene base/llm/replay; sin bloque `connectors`.
- Fase 3 (procedencia): parcialmente decidida. DECISION-0029 (#4 firma por agente + prev_hash + anclaje) y DECISION-0023 (firma-release) aceptadas; #2 PROV y #3 cost-attribution NO construidos.
- Loop: OFF. `runtime.real_invoker.enabled=false` y `runtime.supervised_autonomy.enabled=false` (gated por DECISION-0027). subagents OFF.
- Medicion existente: `runtime/metrics.py`, `runtime/budget.py`, `runtime/eventlog.py` existen (sustrato), pero la imputacion POR handoff/decision/agente no existe.

Conclusion: la hoja de ruta esta desfasada como documento de seguimiento (encabezado v1.1.0/runtime v0.11.0 vs repo v1.5.0; no se siguio su orden; lo entregado v1.2-1.5 fue el carril de mitigacion de contexto + autonomia, que la hoja no lista). Hay que reconciliarla antes de usarla para decidir el siguiente paso.

## 2. Restriccion dura: el sobre del piloto (DECISION-0027)

"Activar el loop para que haga Fase 1 y 2" NO cabe en el primer piloto. DECISION-0027 acota el piloto a:
- UNA tarea de bajo riesgo, fuera de nucleo y `*.template.*` (una nota de prosa).
- caps: `max_turns=2`, `human_checkpoint_every_k=1` (checkpoint obligatorio tras turno 1, sin auto-resume), `wall_clock_ms=180000`; `budget_tokens` + `deadline` por tarea.
- SA.4 sola en su ventana. Capa C OFF. enforce/authoritative intactos. subagents OFF. Falla cerrada. Reversible (despoblar registro restaura `--once`).

E1 (Skills) y E2 (Connectors) son esfuerzo Alto y tocan nucleo (`protocol.config.json`, `tool_policy.py`, `runtime/adapters/`). Dejar que el loop los construya es una ventana MUY posterior y ampliada, con su propia decision y GO. No es el primer paso.

## 3. Plan escalonado (orden recomendada)

### Paso 1 - Reconciliar la hoja de ruta (tracking)
- Actualizar el documento de hoja de ruta al estado real: versiones, marcado hecho/no-hecho por fase, re-secuenciar. Que deje de mentir.
- Entrega: un documento de estado claro (que fase existe, cual no, en que orden seguimos).
- Esfuerzo: bajo. No toca runtime.

### Paso 2 - Construir #3 (cost-attribution por handoff) [medicion]
- Entra por el metodo: DECISION-00xx -> SPEC-00xx con `acceptance_criteria` + `test_plan` -> golden case -> off-by-default -> neutralidad de dominio.
- Alcance: imputar tokens por handoff / decision / agente extendiendo `budget.py` + `metrics.py`, leyendo de `eventlog.py` (esquema de dos planos: plano de protocolo sin texto libre; carga util por hash).
- Acceptance minimo: el golden mide que cada handoff/decision queda imputado; export determinista; off-by-default; sin regresion en intent_flow goldens.
- Marcar #3 HECHO solo cuando el golden pase y se verifique que mide en caliente (no retrofiteado). Reflejarlo en la hoja (Paso 1).

### Paso 3 - Piloto SA.4 medido (observar comportamiento del loop)
- Re-correr el piloto de DECISION-0027 con #3 ACTIVO: tarea de bajo riesgo (nota de prosa en `examples/neutrality_scan_cases/README.md`), caps 2/1/180000, checkpoint obligatorio tras turno 1.
- Esto es exactamente "activar el loop y revisar metricas para ver comportamiento", pero en el paso seguro.
- Entrega: reporte de corrida + reporte humano en `Area_comun/reports/` (Claude redacta, operador ratifica). Metricas a revisar en el Paso 5.
- Activacion = micro-GO explicito del operador en VS Code (poblar `runtime.real_invoker` + `runtime.supervised_autonomy`). Reversible.

### Paso 4 - GATE: ampliar ventana para que el loop ejecute Fase 1/2
Solo si el piloto cierra estable (drift 0 sostenido, replay==hot, cero hard-fails falsos, reportes ratificados):
- Decision NUEVA + GO del operador para ampliar caps/alcance (otra ventana; un solo multiplicador de riesgo por ventana).
- Backlog que el loop ejecutara, cada item entrando por el metodo (DECISION -> SPEC+acceptance+golden -> off-by-default), con maker!=checker, escritor unico (submit_intent), gates y neutralidad:
  - Fase 0: E5 (`FAILURE_MODES.md`) + E6 (test "merece un loop?" en `TASK_PROTOCOL.md`).
  - Fase 1: E1 (skill registry + digestion: contrato SKILL, bloque `skill_registry`, integracion `tool_policy.py`).
  - Fase 2: E2 (capa de conectores MCP sobre tool-policy; deny-by-default; "MCP no concede autoridad").
- Nota de dependencias de la hoja: E1 depende de Fase 0 (E5/E6); E2 depende de E1. Respetar ese orden o waivearlo conscientemente.

### Paso 5 - Revisar metricas (comportamiento)
Sobre el run del Paso 3 (y luego del Paso 4), revisar con #3 + sustrato existente:
- Tokens por handoff / decision / agente (#3).
- Contexto ensamblado por turno (vs `assembled_context_warn_tokens=16000`).
- Run log / metrics.py: turnos, duracion, paradas (human_checkpoint, paused, wallclock, max_turns), hard-fails.
- Drift (debe ser 0) y replay==hot.

## 4. Restricciones de integridad (innegociables, recordatorio)
- Cierres/mutaciones de estado SIEMPRE por submit_intent desde VS Code (escritor unico). Edicion manual = drift.
- Loop y subagents requieren GO explicito del operador; off-by-default; reversible.
- SA.4 sola por ventana; Capa C OFF; enforce/authoritative no se tocan; subagents_enabled false.
- Cambios visibles del protocolo: SemVer + CHANGELOG (incl. #3 y la activacion del loop = MINOR).
- Neutralidad de dominio: nada de terminos de negocio en nucleo ni `*.template.*`.
- Ningun numero no medido como promesa.

## 5. Resumen para pegar al arquitecto (orden corta)
"Arquitecto: (1) reconcilia la hoja de ruta al estado real (hecho/no-hecho + re-secuencia). (2) Construye #3 cost-attribution por handoff entrando por el metodo (decision+spec+acceptance+golden, off-by-default, dos planos), verifica que mide en caliente y marcalo hecho. (3) Prepara el piloto SA.4 de DECISION-0027 (tarea de bajo riesgo, caps 2/1/180000, checkpoint tras turno 1) con #3 activo, listo para mi micro-GO; reporte de corrida + reporte humano. (4) NO amplies caps/alcance para Fase 1/2 sin pilotear estable + decision nueva + mi GO. Todo por submit_intent; SA.4 sola; Capa C/enforce/authoritative intactos; subagents OFF."
