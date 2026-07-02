---
decision_id: DECISION-0083
title: "Vision Nova - supersede parcial de DECISION-0077 (fork Zeus-Aegis descartado), ajuste de DECISION-0078 (brazo C condicional), re-alcance del backlog 0230-0234 hacia employee-ready/Nova y arquitectura de repos hub/instancias"
status: accepted
date: 2026-07-02
deciders: [operador humano, Arquitecto]
supersedes: []
supersedes_partial: [DECISION-0077]
superseded_by: []
relates_to: [DECISION-0050, DECISION-0078, DECISION-0081, DECISION-0082, GOAL-VISION-NOVA-001, DIRECTIVA-OPERADOR-F0.1-20260702, ANALISTA-pivote-v2-veredicto]
phase: P2
scope: product
approval_ref: "GO escrito del operador: personal/operador/vision-nova/F0/DIRECTIVA-OPERADOR-F0.1-20260702.md (emitida 2026-07-02) + ORDEN-ARQUITECTO-F0.2-DECISION-hub.md"
---

# DECISION-0083 - Vision Nova: fin del fork, re-alcance del backlog y arquitectura de repos

> Contexto: la ronda 2 del pivote "publicar para ser REPRODUCIDO" cerro CAMBIO-REQUERIDO con 8 bloqueantes
> (Area_comun/artifacts/ANALISTA-pivote-v2-veredicto.md). El operador emitio la directiva F0.1 (dos carriles,
> roadmap fechado, gate duro Sprint 1 = 2026-07-30) y ordeno formalizar esta DECISION-hub como F0.2. Scope de
> producto: no toca el core neutral del protocolo, ni los templates, ni el dataset TFM sellado, ni los pineados.

## Decision

1. **FIN DEL FORK (supersede PARCIAL de DECISION-0077).** La productizacion de Zeus-Aegis como producto
   instalable deja de ser meta activa. Zeus-Aegis se conserva como PANEL F1 read-only del hub (DECISION-0050
   punto 4). No se tira trabajo: TASK-0222 / TASK-0223 / TASK-0226 / TASK-0229 (done) quedan como estan.
   SOBREVIVEN de DECISION-0077: la numeracion TASK-02xx, los prefijos de agrupamiento en el titulo, la
   gobernanza en el hub, las restricciones de neutralidad de dominio y el sandbox. Por eso el supersede es
   parcial (campo `supersedes_partial`), no total: DECISION-0077 sigue vigente en todo lo que no sea la meta
   de producto fork/productizacion.

2. **NUEVA META ACTIVA: GOAL-VISION-NOVA-001.** Metodologia employee-ready + instancia nova-budget distribuida
   + estudio pre-registrado. Convencion de agrupamiento (misma que DECISION-0077: va en titulo + relates_to,
   NUNCA en el id): prefijo de titulo `[VISION-NOVA][Fx.y]` + `relates_to: GOAL-VISION-NOVA-001` en toda tarea
   nueva o re-alcanzada.

3. **AJUSTE DE DECISION-0078 (sigue proposed).** El brazo C (peon -> gate -> critico -> firmante) pasa de brazo
   simultaneo a FASE CONDICIONAL (Fase 3, condicional a la aritmetica pre-registrada del backlog, item F3.2 del
   tablero). La muestra pasa de "tareas sandbox" a tareas reales de Nova Budget bajo gobierno completo,
   manteniendo el sandbox piloto-peones (D:/Agentes/Zeus/piloto-peones) como entorno de ensayo. DECISION-0078
   NO se ratifica hasta el sellado del pre-registro (F3.4).

4. **RE-ALCANCES DEL BACKLOG** (task_upsert, mismo id, titulo nuevo + sufijo
   "[re-alcance: pivote Vision Nova, DECISION-0083]"):
   - TASK-0230 -> [VISION-NOVA][F2.1] new_instance de nova-budget desde tag v1.18.0 + perfil de instancia
     (arm/mode + taxonomia de riesgo). El bootstrapper Electron MUERE del alcance.
   - TASK-0232 -> [VISION-NOVA][F2.3] harness distribuido pull -> escribir -> push inmediato (claims visibles
     entre clones) + hosting privado de la instancia. El instalador firmado de Windows MUERE del alcance.
   - TASK-0233 -> [VISION-NOVA][F2.2] verificacion e2e distribuida: un clon limpio opera 1 tarea completa solo
     via Git (owner Analista; se registra/promueve despues de F2.1).
   - TASK-0234 -> [VISION-NOVA][F2.5] runbook de onboarding remoto de empleados (objetivo <=1 dia, medido;
     alimenta HP6).
   - TASK-0231 se CONSERVA proposed, re-alcanzada a [VISION-NOVA][F6.1] fase peones bajo DECISION-0078 ajustada
     (sandbox D:/Agentes/Zeus/piloto-peones intacto).

5. **ARQUITECTURA DE REPOS.**
   - Hub (multi_agent_project_protocol) = casa VIVA del TOOL (runtime, validador, templates, doctrina) +
     ARCHIVO INMUTABLE (ledger atestado, decisiones, corpus sellado). La doctrina SIEMPRE se desarrolla en el
     hub antes de instanciar.
   - Instancias (nova-budget primero) = repos consumidores creados desde RELEASE TAG del hub via new_instance;
     se actualizan solo via upgrade_instance; JAMAS empujan al hub. Repos de instancia/producto bajo
     D:/Agentes/Zeus/ (DECISION-0050).
   - Modo distribuido = Git puro: empleados con clones del repo de instancia en hosting privado,
     pull -> write -> push; sin acceso al hub.
   - Spec-repo publico (Apache-2.0, sin residuos de instancia) = FUTURO, Carril B, gateado por CB.1 y el
     presupuesto CB (<=1 dia/semana medido con stop).

6. **LOS 8 BLOQUEANTES de la ronda 2** quedan incorporados como obligaciones mapeadas al tablero:
   (1) politica de medicion de empleados -> F3.1; (2) eventos firmados de ayudas/des-atascos/excepciones/
   arbitrajes -> F1.2; (3) trailers bloqueantes Task-Id / Fixes-Task -> F1.3; (4) taxonomia D1-D4 ampliada +
   subconteo declarado -> F1.4; (5) presupuesto Carril B medido con stop -> gate global CB; (6) esta DECISION
   -> F0.2; (7) spike DSSE/in-toto/Rekor -> CB.2; (8) sellado del pre-registro completo con hash + seq de
   inicio + reglas de exclusion + ancla externa -> F3.4. Los bloqueantes 1, 2, 3, 4 y 8 son PRECONDICION del
   Sprint 1 (30-jul); el 5 y el 7 gatean solo el Carril B.

7. **INVARIANTES (no cambian).** Dataset TFM N=500 sellado intocable (tag TFM-dataset-N500); 5 pineados
   byte-identicos; epoch v1.14.0 PINNED; core del protocolo neutral de dominio; sin secretos; F2 write-through
   del panel gateado; repos de producto bajo D:/Agentes/Zeus/ y gobierno SIEMPRE en el hub (DECISION-0050);
   Engram cerrado (DECISION-0081) y PROHIBIDO `gentle-ai install` en maquinas Nova.

## Consecuencias

- El pipeline REQ-ZEUS deja de estar congelado: su continuacion es el backlog Vision Nova. Las tareas
  re-alcanzadas (0230/0231/0232/0233/0234) NO se promueven en esta transaccion; la promocion de F1 llega en
  una orden separada del operador con el backlog F1 descompuesto.
- El bootstrapper Electron (0230 original) y el instalador firmado de Windows (0232 original) quedan fuera de
  alcance: el modo de distribucion es Git puro, no un instalable.
- DECISION-0078 queda pendiente de ratificacion hasta F3.4 (sellado del pre-registro).
