---
task_id: TASK-0257
title: "[DECISION-0103][C5] Armar el harness: core.hooksPath -> .githooks/ + pre-commit invoca validate_collaboration_state y falla en rojo (hub + export born-operational)"
type: infra
status: in_progress
owner: Codex
phase: P2
priority: high
created_at: 2026-07-19
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, DECISION-0096, DECISION-0101]
linked_decisions: [DECISION-0103, DECISION-0096]
file: Area_comun/tasks/TASK-0257-d0103-c5-harness-hookspath-precommit-validate.md
intake:
  type: infra
  goal: Armar el harness de commit (DECISION-0103 C5) cableando core.hooksPath a .githooks/ y extendiendo .githooks/pre-commit para invocar validate_collaboration_state y abortar el commit si el estado colaborativo esta en rojo, con espejo en el export born-operational (DECISION-0096) para que toda instancia nueva nazca con el hook armado. Hoy hooksPath esta VACIO y el pre-commit solo corre prune_state --check + drift de la guia HTML; el validador se ejecuta solo porque alguien se acuerda. Esta unidad va PRIMERA para que las unidades 2-9 nazcan ya exigidas por el hook.
  acceptance:
    - git config core.hooksPath devuelve .githooks en el hub, con mecanismo de cableado REPETIBLE documentado para cada clone nuevo (instruccion en README_INSTANCIACION o script de arranque; git no versiona la config local).
    - .githooks/pre-commit invoca python scripts/validate_collaboration_state.py y aborta el commit con exit distinto de 0 si esta rojo; conserva los checks existentes (prune_state --check y drift de la guia HTML).
    - El hook valida el SNAPSHOT que se va a commitear, no el working tree sucio (stash de lo no-staged o indice temporal); si se decide no hacerlo, el limite queda documentado con racional en el propio hook.
    - Coste medido y declarado en el handoff (segundos por commit en este repo); si excede un umbral razonable (~10s) se implementa modo acotado a rutas tocadas -- NUNCA se desactiva (C5.3).
    - Limite honesto documentado; el bypass local de hooks existe en git, por eso el enforcement duro sigue siendo CI + clean-clone + gates de cron; el hook es la primera linea, no la unica.
    - Export born-operational, la instancia generada por new_instance nace con .githooks/pre-commit equivalente + instruccion de cableado en su arranque; demostrado generando una instancia de prueba en directorio temporal.
    - Procedimiento de DESARME documentado en esta tarea y en el handoff (enmienda E3 de la 0103), el comando exacto para desconectar el hook en 30 segundos si bloquea al equipo, con la aclaracion de que no debilita C5 porque el enforcement duro sigue en CI (validate en cada push/PR desde clon limpio).
  verification_cmd:
    - git config core.hooksPath
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
    - Prueba negativa en sandbox (clon temporal): commit con estado colaborativo en rojo es RECHAZADO por el hook; prueba positiva: commit en verde pasa. Evidencia en el handoff.
  scope_routes:
    - .githooks/pre-commit
    - scripts/new_instance.py
    - README_INSTANCIACION.md
    - Area_comun/protocol/
  out_of_scope:
    - Cambiar la logica interna del validador - FUERA (el hook solo lo invoca).
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA (construirlas contamina el preregistro).
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker en el hub - FUERA; esta tanda va por flujo gobernado normal, no por runtime orchestrator.
  risk: medium
  estimate: M
---

# TASK-0257 - [DECISION-0103][C5] Armar el harness de commit

Origen: DECISION-0103 clausula 5, unidad 1 de la tabla de implementacion. Va PRIMERA por
orden explicito del Operador (2026-07-19): armar el harness antes de escribir reglas
nuevas garantiza que las reglas nuevas nazcan ya exigidas y que la propia implementacion
de las unidades 2-9 quede validada por el hook desde el primer commit.

Riesgo principal: falsos rojos del validador bloqueando commits legitimos (p.ej. commits
solo-personal/ con estado compartido en rojo de un peer a medio entregar). Mitigacion:
medir el coste, modo acotado a rutas tocadas si hace falta, y documentar el
comportamiento esperado en ese caso en el propio hook.

OK de arranque del Operador RECIBIDO el 2026-07-19 (gate manual de turno 0 cumplido),
con dos enmiendas que aplican a esta unidad y estan selladas en la 0103: E2 (esta unidad
se revisa EN CUANTO ATERRIZA, con gate propio del checker de proveedor diverso, ANTES de
arrancar TASK-0258) y E3 (el acceptance incluye el procedimiento de desarme del hook).
El cambio de acceptance viene de la propia orden de aprobacion del Operador, no es una
ampliacion silenciosa.

## Desarme operativo (E3)

Si el hook bloquea al equipo, desconectarlo localmente en menos de 30 segundos:

```text
git config --unset core.hooksPath
```

Rearmarlo con `git config core.hooksPath .githooks`. Este desarme es reversible y
no debilita C5: CI, clean-clone y los gates de cron siguen ejecutando el validador.
