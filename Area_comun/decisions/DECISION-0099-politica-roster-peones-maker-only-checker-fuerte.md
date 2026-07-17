---
decision_id: DECISION-0099
title: "Politica de roster: peon = ejecutor de codigo subordinado al maker; el maker (modelo fuerte) gobierna y especifica; el checker adversarial permanece en modelo fuerte"
status: active
date: 2026-07-17
author: Arquitecto
approved_by: "Operador (FIRMA MSG-20260717-Operador-to-Arquitecto-FIRMA-decision-0099, commit 585b7ab; aplicada a la version CORREGIDA por DIRECTIVA dca50ec: jerarquia peon-subordinado-al-maker)"
relates_to: [DECISION-0096, DECISION-0097, DECISION-0060]
---

# DECISION-0099 - Politica de roster: peon subordinado al maker; maker gobierna; checker fuerte

## Contexto

El operador dispone de agentes trabajadores adicionales ("peones"), en particular de modelo local
pequeno (clase 3B-8B), para incorporar a rosters de instancias. La metodologia sostiene su
garantia central en el gate adversarial maker!=checker: el checker debe CAZAR defectos reales
(evidencia del propio dia: refutacion del default fail-open y de la colision de PK en el patron
epistemico; 3 BLOCKERs conductuales en la primera unidad de la Fase A). DIRECTIVA del operador
2026-07-17 (MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-politica-roster-peones-solo-codigo-
nunca-checker).

## Decision (3 reglas de roster, capa metodologia, neutral de dominio)

1. **Peon = ejecutor de codigo SUBORDINADO al maker.** El peon (agente trabajador de modelo debil,
   p.ej. local clase 3B-8B) SOLO escribe codigo, bajo la direccion de un maker. NO es un maker
   autonomo y NUNCA ocupa rol de checker, orquestador ni firmante de ratificacion.
2. **El MAKER (modelo fuerte) gobierna a los peones.** El maker asigna a cada peon sub-tareas de
   codigo con especificacion DETALLADA y sin ambiguedad (DoR completo, contrato, acceptance
   verificable, verification_cmd, scope_routes, out_of_scope), y RESPONDE por el resultado ante el
   checker. Una tarea abierta o subespecificada NO se rutea a un peon: el maker la refina primero.
   Cuanto mas debil el modelo, mas carga la especificacion y menos decide el peon.
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

- Operador: FIRMADA (MSG-FIRMA-0099, commit 585b7ab) sobre la version CORREGIDA ordenada por
  DIRECTIVA de correccion pre-sello (commit dca50ec: "los peones solo hacen codigo, GOBERNADOS
  POR EL MAKER, quien les asignara las tareas especificandoles detalladamente lo que deben
  hacer"). Sellada via submit_intent decision (patron DECISION-0091) el 2026-07-17.
