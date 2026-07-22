---
task_id: TASK-0285
title: "[EXPORT] El runner de instanciacion completa nace rojo: el prune_state generado no exporta ledger_head, y la asercion de coordination-default choca con el config runtime-tier vivo"
type: fix
status: review_approved
owner: Codex
phase: P2
priority: medium
created_at: 2026-07-22
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0257, TASK-0281, DECISION-0022, DECISION-0103]
linked_decisions: [DECISION-0022]
file: Area_comun/tasks/TASK-0285-instanciacion-runner-ledger-head.md
intake:
  type: fix
  goal: "Deuda PREEXISTENTE que declaro el maker al entregar TASK-0279 y que el checker CONFIRMO independiente: el runner de instanciacion completa (el que prueba que una instancia recien nacida por el export born-operational arranca sana) esta ROJO por dos causas ajenas a 0279, verificadas en el commit padre 6197e10 sin el codigo de 0279. (1) El prune_state.py generado en la instancia NO exporta ledger_head (falta el modulo/entrypoint que el propio prune usa), asi que el runner falla al invocarlo -- es el mismo ledger_head que TASK-0281 hizo autoritativo para la ventana de evidencia, pero el export no lo arrastra. (2) La asercion de 'coordination-default' del runner choca con el config runtime-tier VIVO de este hub: el runner asume una instancia coordination-tier y este hub corre con event_state distinto, asi que la asercion no aplica y da falso rojo. El efecto es que un gate de humo del export nace en rojo y nadie puede distinguir un fallo real de este ruido preexistente."
  acceptance:
    - "El export born-operational arrastra ledger_head (modulo/entrypoint) a la instancia generada, de modo que el prune_state generado lo encuentre y el runner de instanciacion pueda invocarlo sin fallar por ausencia."
    - "La asercion de coordination-default del runner distingue el tier de la instancia bajo prueba: no da rojo cuando la instancia es runtime-tier legitima; solo falla si el tier declarado no coincide con el config generado."
    - "El runner de instanciacion completa pasa a VERDE sobre una instancia recien exportada, de modo que un rojo futuro sea señal real y no ruido preexistente."
    - "Negativo permanente con su mutacion demostrada: quitar ledger_head del export vuelve a poner el runner en rojo; y una instancia con tier mal declarado tambien."
  verification_cmd:
    - "El runner de instanciacion completa (examples/, patron run_*.py) en VERDE sobre una instancia recien exportada"
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - scripts/
    - examples/
    - runtime/
  out_of_scope:
    - "Cambiar la logica de prune o de ledger_head en si - FUERA, solo se arregla que el EXPORT lo arrastre y que la asercion distinga el tier."
    - "Reabrir 0279, 0281 ni el resto de la maquinaria - FUERA."
    - "protocol.config.json pineado y dataset N=500 - FUERA (fondo intocable)."
  risk: low
  estimate: S
---

# TASK-0285 - El humo del export nace rojo

Origen: el maker lo declaro con honestidad al entregar TASK-0279 ("declared unrelated
fixture debt"), y el checker lo confirmo por su cuenta -- los mismos dos casos fallan en el
commit padre `6197e10`, sin una linea del codigo de 0279. Por eso no cuenta contra 0279 y
sale a unidad propia: un gate de humo que nace en rojo no puede distinguir un fallo real de
su propio ruido, y eso vale exactamente lo mismo que no tener el gate.

Las dos causas son de EXPORT, no de logica: el `ledger_head` que TASK-0281 hizo autoritativo
no se arrastra a la instancia generada, y la asercion de tier asume coordination cuando el
hub corre runtime. Ambas son de arreglo pequeno; lo que importa es que el runner vuelva a ser
señal.
