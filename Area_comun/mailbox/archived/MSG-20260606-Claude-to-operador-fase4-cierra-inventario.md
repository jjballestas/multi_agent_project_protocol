---
message_id: MSG-20260606-Claude-to-operador-fase4-cierra-inventario
type: DECISION_REQUEST
task_id: TASK-0038
from: Claude
to: operador humano
status: archived
requires_response: false
response_owner: none
one_line_summary: Fase 4 N-agente cerrada (DONE). NUCLEO Fases 1-4 completo. Inventario entregado (artifact). DECISION DEL OPERADOR REGISTRADA: consolidar el NUCLEO (Capa A); arrancada TASK-0047 (A.5 suites en CI).
requested_action: none (decision tomada: Capa A)
question: none
answered_by: operador humano
decision: Consolidar el NUCLEO (Capa A) antes de la Fase 5. Inventario formal en Area_comun/artifacts/INVENTARIO-n-agente-cierre-nucleo-20260606.md.
context_refs:
  - Area_comun/specs/SPEC-0038-n-agent-registry.md
  - Area_comun/state/PROJECT_STATE.json
---

# Fase 4 cerrada + INVENTARIO: que falta para terminar la metodologia

Operador: la Fase 4 (TASK-0046, maquina de estados Review/QA) quedo ACEPTADA y DONE tras ratificacion
adversarial (suite 61/61, gates verdes). Con esto el **NUCLEO del programa N-agente (Fases 1-4) esta
completo**: registry de capacidades, event log + idempotencia/fencing, router con fairness, y maquina
Review/QA con corte de bucles. Cubre los criterios 1-12 de SPEC-0038 sec.16.

A continuacion el inventario de lo que FALTA para considerar la metodologia "terminada", en 3 capas.

## Capa A - Completar el programa N-agente (SPEC-0038, criterios 13-17 + test plan global 15.3-15.5)

Estas son brechas de la spec YA congelada; no requieren decision nueva, solo trabajo:

1. **Event log como WRITER VIVO (la brecha arquitectonica mayor).** Hoy `runtime/eventlog.py` existe y
   esta probado, pero el estado (`Area_comun/state/*.json`) se escribe DIRECTO; el event log es aditivo/
   observacional, no la fuente de verdad. Falta: que `apply`/`orchestrator` deriven el estado del log y
   cablear `assert_snapshot_matches` al validador global py/ps1 como hard-gate (FOLLOW-UP rastreado desde
   Fase 2). Sin esto, los invariantes de replay/auditoria no estan realmente activos en el repo vivo.
2. **Golden N=3 y N=5** (15.3): hoy solo N=2 (fallback) esta probado de punta a punta.
3. **Property-based de invariantes I1-I8** (15.4): hoy hay golden puntuales, no property tests.
4. **Concurrency simulation** (15.5): 10 implementadores / 100 tareas / colisiones de claim / vencimiento
   de leases / agentes disabled a mitad de ejecucion / retries / intents duplicados. No existe.
5. **Correr las suites de runtime en CI**: hoy CI corre validador/neutralidad/encoding + algunos golden;
   las ~9 suites de runtime (router, eventlog, review_qa, etc.) corren solo en local/handoff.
6. **Hardening autor-de-record (I1/I2)** [hallazgo de hoy, no bloqueante]: la guarda de exclusion de autor
   confia en `payload.author` (controlable por el actor) en vez del estado. Fix: persistir `original_author`
   en el estado y leer la guarda solo de ahi. Necesario antes de operar agentes no confiables.
7. **SemVer del schema** (criterio 17): justificar/versionar el `turn_schema` para consumidores reales.

## Capa B - Fases 5-7 (CONDICIONADAS, requieren TU decision)

Por diseno (SPEC-0038 sec.14) estas se activan "cuando exista superficie real":

- **Fase 5 - Guardrails y permisos.** tool_policy con allowlist por herramienta, side-effect gates, diff
  obligatorio, bloqueo de acciones sensibles, anti-inyeccion de handoffs. Relevante en cuanto los agentes
  ejecuten acciones externas con efecto real.
- **Fase 6 - Observabilidad y presupuesto.** trace_id por evento, spans por transicion, metricas de routing/
  QA/conflictos/coste, deadline por tarea. (`budget.py` ya existe parcialmente del M2.)
- **Fase 7 - Release engineering.** SBOM, provenance/attestation, changelog desde eventos, rollback como
  saga. Diferido hasta una release real con publicacion de binarios.

## Capa C - La metodologia como PRODUCTO reutilizable (mas alla del dogfooding)

- **TASK-0037**: guia humana operativa neutral + HTML (proposed, sin especificar).
- **Documentacion N-agente** (criterio 16): registry, routing, estados, guardrails, seguridad, handoffs en
  docs publicables.
- **Empaquetar el runtime N-agente para instancias**: hoy `runtime/` vive en este repo (dogfooding); para
  que otras instancias hereden el modelo N-agente habria que llevarlo a las plantillas/scaffolding. [POR
  CONFIRMAR si esta en alcance: las `*.template.*` publican el protocolo de coordinacion, no el runtime.]
- **Release v0.10.0**: acumula DECISION-0016 (areas personales) + Fases 1-4 del N-agente.
- **Wrapper LLM real (claude CLI)** tras el invoker subproceso generico ya existente.

## Decision que pido

1. **Arrancar Fase 5 ahora**, o **consolidar primero el nucleo** (Capa A: writer-vivo + N=3/N=5 + property
   + concurrency + CI)? Mi recomendacion: consolidar el nucleo (Capa A 1-5) antes de Fase 5; el writer-vivo
   (A.1) es el que mas valor de auditoria desbloquea y cierra el FOLLOW-UP de Fase 2.
2. **Release v0.10.0** ahora (con Fases 1-4), o esperar a cerrar la Capa A?
3. **Prioridad de FOLLOW-UPs**: writer-vivo (A.1) vs hardening autor (A.6).

Codex queda SIN cola de Fase 5 (le avise que no la tome hasta tu OK). Mientras tanto puedo encolar trabajo
de Capa A si lo apruebas.
