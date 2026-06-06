---
message_id: MSG-20260606-Claude-to-operador-capaA-completa
type: DECISION_REQUEST
task_id: TASK-0038
from: Claude
to: operador humano
status: archived
requires_response: false
response_owner: none
answered_by: operador humano
decision: El operador eligio (a) release v0.10.0 ("empaqueta DECISION-0016/0017/0018 + N-agente Fases 1-4 + Capa A"). Publicada v0.10.0 (REPORT-20260606-release-v0.10.0.md). El siguiente paso post-release queda abierto.
one_line_summary: CAPA A COMPLETA. RESUELTO: el operador eligio release v0.10.0 (publicada). Siguiente paso post-release abierto.
requested_action: none (decision tomada: release v0.10.0)
question: none
context_refs:
  - Area_comun/specs/SPEC-0038-n-agent-registry.md
  - Area_comun/artifacts/INVENTARIO-n-agente-cierre-nucleo-20260606.md
  - Area_comun/state/PROJECT_STATE.json
---

# Capa A completa - decision del siguiente paso

Operador: con TASK-0053 aceptada, la **Capa A (consolidacion del nucleo N-agente)** queda COMPLETA.

## Lo cerrado en la Capa A (todo ratificado adversarialmente + pusheado)

- **A.5** suites de runtime en CI (TASK-0047).
- **A.1** event log como writer-vivo del control-plane, Fase A: gate atomico en apply + validador global
  cuando runtime/state existe; fallback intacto (TASK-0048, SPEC-0039 + DECISION-0017, alcance A->B).
- **A.6** hardening autor-de-record I1/I2: la guarda lee del estado, no del payload (TASK-0049).
- **A.2** golden N=3/N=5: reviewer/QA separados + balanceo determinista (TASK-0050).
- **A.3** property-based I1-I8 (TASK-0051).
- **A.4** concurrency simulation 10 impl/100 tareas: conflictos registrados, snapshot sin corrupcion,
  fairness, cero doble-aplicaciones (TASK-0052).
- **A.7** SemVer del turn_schema (schema_version 1.1.0 + politica) (TASK-0053).

El **test plan global 15.3-15.5** de SPEC-0038 queda cubierto. Suite runtime 105/105; gates verdes.
Ademas se establecio **DECISION-0018** (notificacion de anomalias) a raiz del incidente de A.3, y ya se
internalizo (A.4 y A.7 entregadas con release atomico correcto).

## Estado de los criterios de SPEC-0038 (sec.16)

- Criterios 1-12 (nucleo): implementados (Fases 1-4).
- Criterio 14 (CI con unit/contract/golden/replay/concurrency): cubierto (A.5 + suites + concurrency).
- Criterio 15 (frontera de determinismo): verificada por property + concurrency deterministas.
- Criterio 17 (SemVer del schema justificado): cubierto (A.7).
- Criterio 11/I5-I6 (event log como fuente de verdad): control-plane cableado (A.1 Fase A); el estado de
  protocolo como writer-vivo es **Fase B (gateada)**.
- Criterio 13 (presupuesto/deadline) y 16 (documentacion completa) + Fases 5-7: pendientes/gateados.

## Decision que pido (siguiente paso)

1. **Release v0.10.0**: empaqueta DECISION-0016/0017/0018 + N-agente Fases 1-4 + Capa A. Recomendado como
   hito ahora que el nucleo esta consolidado y verde.
2. **Fase 5 (guardrails/permisos)**: gateada; incluye el hardening anti-inyeccion + tool-policy. Aqui
   tambien encaja completar I1/I2 contra actores no confiables.
3. **Fase B (event log writer-vivo del estado de protocolo)**: gateada; el cambio arquitectonico mayor
   (replay del estado + materializacion + genesis-snapshot). Requiere ventana de transicion.
4. **Detener** el programa N-agente aqui y pasar a otra linea (p.ej. TASK-0037 guia humana, o el wrapper
   LLM real).

Mi recomendacion: **release v0.10.0** primero (consolida y deja un punto estable), y luego decidir entre
Fase 5 y Fase B segun prioridad. Codex queda sin cola hasta tu decision.

Aparte: ofreci persistir el ANALISIS del comportamiento semi-automatico (hoy en mi memoria + mostrado en
chat) como artefacto/reporte en el repo; dime si lo quieres formalizado.
