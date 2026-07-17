---
decision_id: DECISION-0101
title: "El checker formal migra a un proveedor que autorice trabajo adversarial legitimo (Claude/Anthropic CLI); maker y checker en proveedores DISTINTOS como regla de roster"
status: active
date: 2026-07-17
author: Arquitecto
approved_by: "Operador (FIRMA MSG-20260717-Operador-to-Arquitecto-FIRMA-decisions-0100-0101, commit daf2c4f; aprobadas TAL CUAL)"
relates_to: [DECISION-0099, DECISION-0096, DECISION-0061]
---

# DECISION-0101 - Checker formal en proveedor diverso

## Contexto

El rol de checker adversarial ES, por diseno, sondeo de seguridad sobre el propio codigo:
planta fixtures de datos sensibles, tamperea hashes, prueba traversal y sinks. El clasificador
de seguridad del proveedor actual del CLI del checker (OpenAI) flageo ese trabajo legitimo 5
veces en un dia (2 reviews bloqueadas 2x consecutivas cada una), forzando sustituciones por un
checker informal en modelo fuerte (declaradas checker_formal=0). Un proveedor cuyo clasificador
flagea el sondeo adversarial esta estructuralmente mal casado con el rol.

## Decision

1. **El CHECKER FORMAL migra a Claude/Anthropic CLI** como runtime de su harness. Razones:
   (a) autoriza trabajo de seguridad legitimo sobre codigo propio -- elimina el falso positivo
   de raiz; (b) formaliza el fallback informal que YA opero con calidad verificada (GO de U3/U4
   con hallazgos reales y residuales honestos); (c) anade **diversidad de PROVEEDOR** al gate:
   maker (OpenAI/Codex) != checker (Anthropic/Claude).
2. **Regla de roster (extiende DECISION-0099 r3):** maker!=checker se sostiene por CAPACIDAD +
   POSESION DE LLAVE + **PROVEEDOR** -- el checker formal no corre en el mismo proveedor que el
   maker que revisa, salvo imposibilidad declarada.
3. **Alcance: capa HUB (metodologia)** con espejo en el export born-operational (DECISION-0096):
   toda instancia presente y futura. Primera aplicacion: Nova-Payroll (su reviewer harness
   apunta al nuevo CLI; el runner generico peer_mailbox_cron ya admite -AgentExe/-AgentArgs, el
   cableado es de configuracion, no de codigo).
4. **Re-juicios formales diferidos** (U3/U4 de Fase A y cualquier futuro caso checker_formal=0)
   se re-ejecutan en el NUEVO proveedor en cuanto este cableado -- no se espera al desbloqueo
   del proveedor saliente.
5. **Los probes NO se degradan** para complacer clasificadores: si un proveedor flagea el
   mandato adversarial, se cambia el proveedor, no el mandato.

## Implementacion (tarea gobernada tras la firma)

Tarea de cableado: configurar el harness del reviewer (hub e instancias vivas) con el CLI
nuevo + prompt equivalente + verificacion de 1 review completa end-to-end; espejo al export
0096 (misma tarea de mantenimiento del template que TASK-0256). El maker NO se toca.

## Guardrails

Fondo intocable (2E35F26E / 1.14.0 / N=500); cambio de HARNESS del checker, no del estudio
medido ni del protocolo de gates; DECISION-0081 intacta; capabilities/llaves sin cambios.

## Firma

- Operador: FIRMADA (MSG-FIRMA-decisions-0100-0101, commit daf2c4f). Sellada via submit_intent
  decision (patron DECISION-0091) el 2026-07-17.
