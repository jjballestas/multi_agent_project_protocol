---
decision_id: DECISION-0084
title: "Identidad anti-vibecoding de la metodologia (interrogacion de requisitos + quality panel + excepciones auditadas) + anexo Definition of Ready (10 puntos) + clausula pin-anclado-al-tag"
status: accepted
date: 2026-07-03
deciders: [operador humano, Arquitecto]
supersedes: []
supersedes_partial: []
superseded_by: []
relates_to: [GOAL-VISION-NOVA-001, DECISION-0083, TASK-0239, TASK-0241, MSG-20260703-Operador-to-Arquitecto-ACTION-dor-v2-en-0243]
phase: P2
scope: product
approval_ref: "Directiva del Operador MSG-20260703-Operador-to-Arquitecto-ACTION-dor-v2-en-0243 (commit dae40ac) + alcance de TASK-0243 bajo DECISION-0083/F1"
---

# DECISION-0084 - Identidad anti-vibecoding + Definition of Ready + pin anclado al tag

> Contexto: F1-F (TASK-0243) bajo DECISION-0083. Doctrina corta: registra la identidad de la
> metodologia frente al vibecoding, ancla la reproducibilidad del estudio TFM y anexa la
> Definition of Ready del Operador (checklist de 10 puntos, directiva dae40ac). Scope de
> producto: NO cambia el validador del hub, el core neutral, los templates del core, el
> dataset TFM sellado ni los pineados.

## Decision

1. **Identidad anti-vibecoding (doctrina).** La metodologia rechaza el patron "pedido crudo ->
   implementacion directa". Su identidad operativa es la triada:
   - **Interrogacion de requisitos:** un pedido ambiguo NO se implementa; se somete a intake
     (flujo: pedido crudo -> intake guiado -> brief -> REQ/PRD -> tareas ejecutables). La
     interrogacion existe precisamente con el fin de llenar los 10 puntos del anexo A antes
     de que una tarea sea ready.
   - **Quality panel / gate adversarial:** maker != checker; toda entrega pasa un gate
     independiente (Analista) con severidad por hallazgo (DEFECT_TAXONOMY.md, TASK-0241).
   - **Excepciones auditadas:** toda desviacion (ayuda manual, arbitraje, scope_change,
     intake_exempt) se registra como evento firmado `exception.recorded` (TASK-0239); no
     existen excepciones informales.

2. **Clausula pin-anclado-al-tag (hallazgo F-3).** El pin de los 5 archivos byte-identicos
   (`PINNED_RELATIVE_PATHS` en scripts/agent_metrics.py: eventlog.py,
   validate_collaboration_state.py, protocol.config.json, event-state.runtime.json,
   snapshot.json) esta ANCLADO al tag `TFM-dataset-N500` (-> e3646ae): fija la
   reproducibilidad del estudio sellado, NO congela el software. El validador/runtime VIVO
   evoluciona legitimamente hacia v1.18.0 y siguientes; es medicion, no gate. Lo unico
   intocable en vivo es `protocol.config.json` (epoch v1.14.0 PINNED, byte-identico) hasta
   una re-genesis coordinada (DECISION-0047).

3. **Anexo A vinculante como doctrina; enforcement por capas.** Los 10 puntos son la
   Definition of Ready de tareas de PRODUCTO. En el hub (F1) rigen como doctrina: el intake
   v1 (TASK-0238) cubre 6/10 y NO se reabre ni se toca su validador (anti scope-creep
   pre-30jul). El enforcement estructural de los 4 campos faltantes es de la INSTANCIA
   (F2.1: el TASK_TEMPLATE de nova-budget extiende el bloque intake con los campos v2
   `priority`, `target_user`, `functional_scope`, `assets_inputs`, `tech_constraints`,
   `risks_list`, obligatorios para type feature/product, con regla anti-vacio: "ninguno"
   explicito vale, campo ausente no, placeholder TBD invalido) o de v1.19 (decision futura).

## Anexo A - Definition of Ready del Operador (10 puntos, verbatim)

objetivo definido; usuario objetivo definido; alcance definido; fuera de alcance definido;
contenido/assets definidos; restricciones tecnicas definidas; criterios de aceptacion
definidos; pruebas/gates definidos; riesgos definidos; prioridad definida.

Mapa de cobertura v1 (intake TASK-0238): objetivo/acceptance/verification_cmd/out_of_scope
CUBIERTOS; alcance (scope_routes) y riesgos (risk enum) PARCIALES; usuario objetivo,
contenido/assets, restricciones tecnicas y prioridad NO cubiertos -> campos v2 de instancia.
Detalle: personal/operador/vision-nova/CHECKLIST-DEFINITION-OF-READY-V2.md.

## Consecuencias

- TASK-0230 (F2.1) anota en su cuerpo la extension del template de instancia (campos v2).
- Los prompts/harnesses de agentes de producto adoptan la interrogacion de requisitos como
  paso previo obligatorio a implementar pedidos ambiguos (aterriza en la instancia, F2).
- El estudio TFM permanece reproducible por tag; ningun trabajo F1+ toca los pineados vivos
  salvo el config (intocable).
