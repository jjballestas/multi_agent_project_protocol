# INVENTARIO - Que falta para terminar la metodologia (cierre del nucleo N-agente)

- Fecha: 2026-06-06
- Autor: Claude (arquitecto)
- Estado del repo: HEAD 30143d9 en main; v0.9.0 publicada; gates verdes.
- Referencia normativa: Area_comun/specs/SPEC-0038-n-agent-registry.md (congelada, criterios 1-17, invariantes I1-I8, test plan global 15.1-15.5, plan de fases sec.13-14).
- Decision del operador (2026-06-06): consolidar el NUCLEO (Capa A) antes de las fases condicionadas.

## 0. Resumen ejecutivo

El **nucleo del programa N-agente (Fases 1-4) esta COMPLETO y ratificado** (criterios 1-12 de SPEC-0038).
Lo implementado y aceptado con ratificacion adversarial:

| Fase | Tarea | Entregable | Estado |
|------|-------|-----------|--------|
| 1 Registry + validacion semantica | TASK-0043 | load_agent_registry (fallback 3 niveles), schema agent enum->string, turn_validate semantico | DONE |
| 2 Event log + idempotencia/fencing | TASK-0044 | eventlog.py append-only (seq writer-only), idempotencia por tupla, fencing por-aggregate, snapshot/compactacion, negative replay | DONE |
| 3 Router balanceado + fairness | TASK-0045 | router weighted-least-loaded determinista, exclusion de autor, fairness gate (A4), explanation | DONE |
| 4 Maquina de estados Review/QA | TASK-0046 | review_qa.py: failure_signature canonica (A8), corte de bucles bidireccional no-evadible, defect logs, evidencia obligatoria, assign_fix | DONE |

Suite de runtime: 61/61 golden + gates py (validador/encoding/neutralidad) verdes.
Fallback N=2 byte-equivalente intacto en todas las fases.

## 1. Capa A - Completar la spec ya congelada (ELEGIDA por el operador)

Brechas de SPEC-0038 que NO requieren decision nueva, solo trabajo. Secuenciacion recomendada:

| # | Item | Criterio/seccion SPEC | Riesgo | Valor | Estado |
|---|------|-----------------------|--------|-------|--------|
| A.5 | Correr las suites de runtime en CI | 14 (CI: unit/contract/golden/replay/concurrency) | Bajo | Alto (protege regresiones de todo lo demas) | ENCOLADO (TASK-0047) |
| A.1 | Event log como WRITER VIVO + assert_snapshot_matches en validador global | 11, 12, I5/I6, FOLLOW-UP Fase 2 | Alto (cambia el mecanismo de escritura del estado) | Muy alto (activa auditoria/replay reales) | Por especificar (spec propia; posible DECISION) |
| A.2 | Golden N=3 y N=5 | 15.3 | Bajo | Alto (demuestra multi-agente real) | Pendiente |
| A.3 | Property-based de invariantes I1-I8 | 15.4 | Medio | Alto (garantia formal vs casos puntuales) | Pendiente |
| A.4 | Concurrency simulation (10 impl/100 tareas/leases/disabled mid-exec/intents duplicados) | 15.5 | Medio | Alto (estresa fencing/idempotencia/fairness) | Pendiente |
| A.6 | Hardening autor-de-record (I1/I2 desde estado, no payload) | I1/I2, sec.20 A9 | Bajo | Medio-alto (cierra evasion adversarial) | Pendiente (hallazgo de la review de Fase 4) |
| A.7 | SemVer del schema de turno | 17 | Bajo | Medio | Pendiente |

Notas:
- **A.1 (writer-vivo)** es la brecha arquitectonica mayor. Hoy `runtime/eventlog.py` esta implementado y
  probado, pero el estado (`Area_comun/state/*.json`) se escribe DIRECTO desde `apply.py`; el event log es
  aditivo/observacional (solo `turn_validate` lo consulta para fencing/idempotencia). Hasta cablearlo como
  writer vivo y poner `assert_snapshot_matches` como hard-gate del validador global, los invariantes de
  replay/auditoria (I5/I6) no estan realmente activos en el repo vivo. Por su riesgo (cambia como se persiste
  el estado) merece spec propia y posible DECISION antes de implementar.
- **A.6 (hallazgo de la review de Fase 4):** la guarda de exclusion de autor usa `task_author(task, payload)`
  que prioriza `payload.author`/`original_author` sobre el estado; un actor adversarial podria declarar un
  autor falso y evadir el rechazo self-review/self-QA. Riesgo nulo hoy (actores de buena fe, replay/recorded).
  Fix: persistir `original_author` en el estado en la 1ra asignacion (apply) y que la guarda lea solo del estado.

## 2. Capa B - Fases 5-7 (CONDICIONADAS, requieren decision del operador)

Por diseno (SPEC-0038 sec.14) se activan cuando exista superficie real (acciones externas con efecto,
publicacion de binarios). NO arrancadas; Codex sin cola de Fase 5.

- **Fase 5 - Guardrails y permisos:** tool_policy con allowlist por herramienta, side-effect gates, diff
  obligatorio, bloqueo de acciones sensibles, anti-inyeccion en handoffs. (Aqui encaja tambien A.6.)
- **Fase 6 - Observabilidad y presupuesto:** trace_id por evento, spans por transicion, metricas de
  routing/QA/conflictos/coste, deadline por tarea. (`runtime/budget.py` ya existe del M2, parcial.)
- **Fase 7 - Release engineering:** SBOM, provenance/attestation, changelog desde eventos, release checklist,
  rollback como saga. Diferido hasta una release real con publicacion.

## 3. Capa C - La metodologia como PRODUCTO reutilizable

Mas alla del dogfooding de este repo:

- **TASK-0037** (proposed): guia humana operativa neutral + formato HTML reusable.
- **Documentacion N-agente** (criterio 16): registry, routing, estados, guardrails, seguridad, handoffs en
  docs publicables.
- **Empaquetar el runtime para instancias:** hoy `runtime/` vive en este repo; las `*.template.*` publican el
  protocolo de coordinacion, no el runtime. Por confirmar si el runtime N-agente debe distribuirse a instancias.
- **Release v0.10.0:** acumula DECISION-0016 (areas personales) + Fases 1-4 del N-agente.
- **Wrapper LLM real (claude CLI)** tras el invoker subproceso generico ya existente.

## 4. Criterios de aceptacion de SPEC-0038 (sec.16): estado

Implementados (nucleo): 1 (registry N), 2 (fallback N=2), 3 (schema sin enum rigido), 4 (validacion agente/
firma-atribucion/capacidad/version), 5 (router + fairness), 6 (review/QA != autor), 7 (QA failure sin bucles),
8 (claims con lease/version/fencing), 9 (retry + idempotencia), 10 (humano sin escalados de 1er nivel),
11 (event log append-only seq + snapshot) - **implementado pero no como writer vivo (ver A.1)**, 12 (trazabilidad
por run/task/agent/attempt).

Pendientes: 13 (presupuesto/deadline con escalado - parcial via budget.py, Fase 6), 14 (CI con unit/contract/
golden/replay/concurrency - ver A.5/A.4), 15 (frontera de determinismo documentada - parcial), 16 (documentacion
completa - Capa C), 17 (SemVer del schema justificado - ver A.7).

## 5. Plan inmediato (decision Capa A)

1. **TASK-0047 (encolada a Codex, A.5):** llevar las suites de runtime al workflow de CI (.github/workflows),
   aditivo, sin tocar contrato. Da cobertura de regresion a todo el nucleo.
2. **A.1 writer-vivo:** Claude especifica una spec (y evalua si requiere DECISION por tocar el mecanismo de
   escritura del estado) antes de encolar implementacion.
3. Luego A.2/A.3/A.4 (golden N=3/N=5, property-based, concurrency sim) y A.6/A.7.

Release v0.10.0: a criterio del operador; recomendacion = publicar tras cerrar al menos A.5 + A.1.
