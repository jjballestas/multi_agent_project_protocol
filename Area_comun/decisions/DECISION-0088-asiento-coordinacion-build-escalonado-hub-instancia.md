---
decision_id: DECISION-0088
title: "Asiento de coordinacion escalonado: la governance del ESTUDIO/meta y la metodologia canonica viven en el hub (Aegis-core); la governance OPERATIVA de un equipo de producto vive en su instancia Aegis/ tras ADOPTARLA; migracion post-sello con regla dual de cross-atestacion. Enmienda de aclaracion a DECISION-0050 #5"
status: accepted
date: 2026-07-04
deciders: [operador humano, Arquitecto]
supersedes: []
supersedes_partial: [DECISION-0050]
superseded_by: []
relates_to: [DECISION-0050, DECISION-0085, DECISION-0087, DECISION-0083, DECISION-0022, GOAL-VISION-NOVA-001]
phase: P2
scope: governance
approval_ref: "Aprobada por el Operador (John Ballestas) 2026-07-04: REQUEST MSG-20260704-Operador-to-Arquitecto-REQUEST-asiento-coordinacion-build-nova + respuesta FYI-asiento (commit 96ebae2) + aprobacion interactiva 'apruebo redaccion de enmienda corta a 0050/0085'. Frontera de governance -> aprobacion humana registrada."
---

# DECISION-0088 - Asiento de coordinacion escalonado (hub-ahora / instancia Aegis-despues)

> Contexto: al fijar el workflow del Operador para el build de Nova surgio una tension entre
> DECISION-0050 #5 ("la governance de TODOS los proyectos vive en el UNICO hub constante; los repos de
> producto rotan") y DECISION-0085/0087 (cada proyecto tiene su instancia `Aegis/`; ya existe NOVA/Aegis,
> construida en F2 con governance/coordinacion/atestacion propia via Git). No es contradiccion si se
> escalona por TIEMPO y por CAPA. Esta enmienda aclara el #5 y fija la regla de migracion + cross-atestacion.

## Decision

1. **Dos capas de governance, dos asientos distintos:**
   - **Meta / estudio / metodologia canonica -> Aegis-core (el hub).** El dataset del ESTUDIO (medicion,
     sello, corpus, cadena #4 del hub) y la fuente canonica de la metodologia viven SIEMPRE en el hub. Esto
     es lo que DECISION-0050 #1 llama "the dataset". Nunca migra.
   - **Governance OPERATIVA de un equipo de producto -> su instancia `Aegis/`.** Los claims/tasks/mailbox/
     GOs del build de un producto adoptante viven en su instancia (p.ej. NOVA/Aegis), una vez ADOPTADA.

2. **Aclaracion de DECISION-0050 #5:** "un hub unico gobierna todo" aplica a la governance del ESTUDIO/meta
   y a la metodologia canonica (Aegis-core). NO impide que un equipo de producto adoptante opere su build en
   su propia instancia `Aegis/` (DECISION-0085/0087). Los repos de PRODUCTO (codigo) siguen rotando y nunca
   albergan governance (0050 #1 intacto); la instancia `Aegis/` NO es un repo de producto, es la capa de
   metodologia aplicada al equipo.

3. **Escalonamiento por tiempo (regla operativa para Nova AHORA):**
   - **Durante la ventana del estudio (GOAL-P1 3-8 jul + SPECs Sprint 1 hasta el sello Etapa 1 / ~30-jul):**
     el asiento de coordinacion del brazo GOBERNADO es el **HUB**. Razon dura: el brazo gobernado es el
     TRATAMIENTO que el estudio mide; su atestacion debe estar en el mismo #4 que la medicion y el sello, en
     UN solo asiento. Abrir un segundo asiento (NOVA/Aegis) a mitad del estudio crea una costura de
     cross-atestacion justo antes del sello (regla de oro del sello: nada nuevo cerca del sello). Hoy funciona
     desde el hub.
   - **Codigo de producto -> NOVA/Nova-Budget** (repo propio, lazy; sin multi-root, 0050).

4. **Trigger de migracion:** tras SELLAR y MEDIR la Etapa 1 del estudio, el build de Nova migra a NOVA/Aegis
   como la primera instancia employee-run real (que es, ademas, la evidencia de transferibilidad del propio
   estudio: la replica employee-run pre-registrada). La migracion es un paso de ADOPCION, no una accion a
   mitad del estudio.

5. **Regla dual de cross-atestacion (aplica al migrar):**
   - **Hub (Aegis-core):** #4 del ESTUDIO/meta + sello + metodologia canonica.
   - **NOVA/Aegis:** #4 OPERATIVO del equipo Nova (claims/tasks/mailbox/GOs del build).
   - **Cruce:** el journal de medicion del hub registra, en cada gate, el **sha256 de la atestacion de la
     instancia** NOVA/Aegis. La instancia atesta su operacion; el hub atesta el estudio que la observa;
     verificable por terceros; los dos #4 NO se mezclan.

## Alcance y limites
- Es aclaracion de interpretacion + regla de migracion; NO toca el epoch pineado, el N=500 sellado, ni la
  cadena #4 existente. No fuerza ninguna migracion ahora (Nova se coordina en el hub durante el estudio).
- DECISION-0050 #1 (codigo en repo de producto, governance nunca ahi) queda intacto. DECISION-0085/0087
  (instancia `Aegis/` por proyecto) quedan intactos y ahora con su rol temporal explicito.

## Consecuencias
- (+) Workflow del Operador fijado: build coordinado en el hub por ahora; codigo en Nova-Budget; NOVA/Aegis
  en reserva-probada para post-sello.
- (+) Integridad del estudio protegida (asiento unico durante la ventana; sin costura antes del sello).
- (+) La vision employee-ready (equipos operan su instancia) queda con camino claro y trigger definido.
- (-) Introduce un paso de migracion post-sello (planificado, no improvisado) con su regla de cross-atestacion.
