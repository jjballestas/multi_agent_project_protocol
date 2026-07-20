---
task_id: TASK-0257
title: "[DECISION-0103][C5] Armar el harness: core.hooksPath -> .githooks/ + pre-commit invoca validate_collaboration_state y falla en rojo (hub + export born-operational)"
type: infra
status: in_review
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

## Cierre en curso: blocked con residuales declarados (decision O1 del Operador, 2026-07-20)

El fix-loop agoto su tope (2 iteraciones, 3 veredictos NO-GO del gate E2 con 5+3
hallazgos reales; ver los 3 artefactos ANALISTA-TASK-0257-*). Lo ENTREGADO Y VERIFICADO:
hub armado (hooksPath), juicio staged sin bypass unstaged (F-0257-01 cerrado), borrados
de validador/runtime/estado cubiertos (selector ACMRTD), modo acotado (~0.38s), export a
3 tiers con hash identico, desarme E3, bypass honesto documentado. RESIDUALES DECLARADOS
por decision del Operador (MSG-20260720-Operador-to-Arquitecto-RESP-escalada-0257-O1-
con-correcciones):
- RESIDUAL ESTRUCTURAL (no remediable en el hook): el borrado del PROPIO hook -- un
  hook borrado no se ejecuta; ninguna logica interna lo alcanza. Deteccion SOLO en capa
  CI (paso de existencia+SHA-256, plegado al acceptance de TASK-0267) y en revision de
  diffs. El hook es la primera linea; el CI es el enforcement duro (C5 en su sitio).
- TRANSFERIDO a TASK-0267: los escapes con hook en ejecucion (rename R100 de rutas de
  juicio; arnes de negativos falso-pasa), que la materializacion del indice cubre.
El cierre final de esta tarea (blocked -> in_review -> done) llega tras el aterrizaje
de TASK-0267 y su re-juicio conjunto.

## Desarme operativo (E3)

Si el hook bloquea al equipo, desconectarlo localmente en menos de 30 segundos:

```text
git config --unset core.hooksPath
```

Rearmarlo con `git config core.hooksPath .githooks`. Este desarme es reversible y
no debilita C5: CI, clean-clone y los gates de cron siguen ejecutando el validador.

## Modo acotado

El hook siempre ejecuta el control de poda. El validador completo se selecciona
por rutas staged cuando el commit toca datos colaborativos o cualquiera de los
ejecutables locales que participan en el juicio (`runtime/`, `scripts/` y
`.githooks/` incluidos). El gate de la guia se selecciona solo cuando cambian su
fuente, salida o generador. La seleccion por rutas nunca desactiva el hook.

Cuando aplica el validador completo, el hook exige equivalencia index/worktree
tambien para todo el codigo local del juicio. La regresion permanente
`python scripts/test_precommit_hook.py` verifica que una mutacion unstaged del
validador no pueda convertir en verde un estado gobernado roto staged.
