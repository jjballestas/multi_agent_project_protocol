---
decision_id: DECISION-0099
title: "Politica de roster: agentes-peon = maker-only con intake explicito; el checker adversarial permanece en modelo fuerte"
status: draft-pendiente-firma
date: 2026-07-17
author: Arquitecto
approved_by: PENDIENTE (firma del operador)
relates_to: [DECISION-0096, DECISION-0097, DECISION-0060]
---

# DECISION-0099 - Politica de roster: peon maker-only, checker fuerte

## Contexto

El operador dispone de agentes trabajadores adicionales ("peones"), en particular de modelo local
pequeno (clase 3B-8B), para incorporar a rosters de instancias. La metodologia sostiene su
garantia central en el gate adversarial maker!=checker: el checker debe CAZAR defectos reales
(evidencia del propio dia: refutacion del default fail-open y de la colision de PK en el patron
epistemico; 3 BLOCKERs conductuales en la primera unidad de la Fase A). DIRECTIVA del operador
2026-07-17 (MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-politica-roster-peones-solo-codigo-
nunca-checker).

## Decision (3 reglas de roster, capa metodologia, neutral de dominio)

1. **Peon = maker-only.** Un agente-peon se asigna EXCLUSIVAMENTE a tareas de desarrollo/build
   como maker. Nunca ocupa rol de checker, orquestador, ni firmante de ratificacion.
2. **Intake explicito obligatorio.** Toda tarea asignada a un peon lleva intake DoR COMPLETO y
   contrato sin ambiguedad (acceptance verificable, verification_cmd, scope_routes, out_of_scope).
   Cuanto mas debil el modelo, mas carga la spec y menos decide el peon. Una tarea abierta o
   subespecificada NO se rutea a un peon: se refina primero o se asigna a un maker frontier.
3. **El checker permanece en modelo fuerte.** El rol de revision adversarial no se degrada a un
   modelo debil bajo ninguna circunstancia. maker!=checker debe sostenerse por CAPACIDAD ademas de
   por posesion de llave: un checker incapaz de refutar convierte el gate en rubber-stamp
   (cumplimiento formal, garantia vacia) y contamina la evidencia del estudio.

## Aplicacion

- Capa: HUB (metodologia). Aplica a toda instancia presente y futura.
- Espejo en el export born-operational (DECISION-0096): las instancias nuevas nacen con esta
  politica anotada en su contrato de roster (AGENTS/roster de instancia). Cableado del espejo =
  tarea de mantenimiento del template, no bloquea nada.
- Instancias vivas: el trio actual de Nova-Payroll (maker frontier + checker fuerte) YA cumple.
  La politica gatea la INCORPORACION futura de peones locales.
- No altera DECISION-0060 (roles owner-closeable) ni el flujo de capabilities.

## Firma

- Operador: PENDIENTE. Al firmar: submit_intent decision (patron DECISION-0091) + esta cabecera
  pasa a status: active con la referencia de la firma.
