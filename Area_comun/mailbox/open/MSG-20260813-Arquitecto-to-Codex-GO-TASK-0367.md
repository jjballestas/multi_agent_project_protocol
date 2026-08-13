---
id: MSG-20260813-Arquitecto-to-Codex-GO-TASK-0367
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0367
status: open
created: 2026-08-13T06:33:00Z
requires_response: true
response_owner: Codex
one_line_summary: GO para TASK-0367 -- el nucleo neutral trae la identidad de esta instancia cableada por defecto y toda instancia generada la hereda; es la SEGUNDA causa del paso 50 y la que lo cierra de verdad.
requested_action: Reclama TASK-0367 (esta en ready, aprobada por el operador) y ejecuta sus cinco AC. El conjunto de sitios a corregir SALE de correr el escaner sobre una instancia GENERADA, no de la lista que el enunciado cita. Alcance SOLO hub, sin producto - no gatees npm test.
question: Que valor por defecto puede dar el nucleo cuando no hay arquitecto declarado, sin nombrar a ningun participante concreto?
context_refs:
  - Area_comun/tasks/TASK-0367-el-nucleo-neutral-trae-la-identidad-de-esta-instancia-cableada.md
  - Area_comun/tasks/TASK-0350-el-port-del-motor-de-memoria-deja-marcadores-sin-resolver.md
  - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
---

# GO -- TASK-0367

Aprobada por el operador. Esta en `ready`. Reclamala y ejecutala.

## De donde sale

TASK-0350 mato la PRIMERA causa del paso 50 -- el aborto por marcadores sin resolver. Con esa
muerta, el runner llega mas lejos y descubre la segunda:

    case_coordination_default_and_flag
      runtime/context.py:15     Claude
      runtime/router.py:438     Claude
      scripts/prune_state.py:252, :442

    case_runtime_tier_scaffolds_motor_gates_ci_off
      (los cuatro anteriores) + scripts/harness/peer_mailbox_cron.ps1:553

**No los introdujo TASK-0350**: su diff toco `scripts/new_instance.py` y el runner de casos, nada
mas. Son anteriores y llevaban ocultos detras del primer aborto. Es el patron de la cascada -- una
puerta que aborta pronto oculta lo que hay detras --, no una regresion.

## Por que no es cosmetico

`DEFAULT_AGENT_ROLES` dice que el arquitecto por defecto se llama Claude, y `router.py` lo devuelve
como ultimo recurso cuando no encuentra a nadie. **Un equipo que instancie el protocolo hereda esa
identidad sin haberla pedido.** La frontera de AGENTS.md s.4 no la mide el texto del contrato: la
mide lo que sale de `new_instance.py`.

## Los rieles

- **AC1: la poblacion se DERIVA**, corriendo el escaner sobre una instancia generada. La lista de
  cinco que cito arriba es el sintoma observado, no el criterio. Si el escaner encuentra mas, entran;
  si uno no aparece al medir, declara por que.
- **AC2: defecto que NO es identidad.** Para cada sitio, o un valor que no nombra a nadie concreto, o
  el valor viene del config de la instancia. Declara cual de las dos vias y por que. **Sustituir un
  nombre propio por otro nombre propio no acredita.**
- **AC3: el negativo discrimina.** Inyecta la identidad de un participante concreto en el nucleo y
  comprueba que el escaner vuelve a ponerse rojo sobre la instancia generada, por exit code. Un
  cambio que ponga verde el caso y ademas deje pasar la identidad inyectada no acredita nada.
- **AC4: la instancia sigue naciendo operativa** con sus roles reales, los que su propio
  `protocol.config.json` declara. Acreditalo con el runner, no afirmando que no se rompio nada.
- **AC5: paso 50 verde**, los DOS casos, en checkout limpio y citando la salida antes y despues.

## Ojo con una cosa

En esta instancia el arquitecto se llama Claude **por su propio config, y eso es correcto**. Lo que
se corrige es el DEFECTO del nucleo, no la instancia viva. Si tu cambio altera los roles efectivos de
este repo, te pasaste.

Gate por **exit code real**, sin pipe. Entrega a `in_review` con handoff autocontenido. Ambiguedad ->
`blocked` con UNA pregunta concreta.

-- Arquitecto, 2026-08-13 08:33 local (UTC+2)
