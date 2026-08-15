---
id: TASK-0399
title: El probe de turno corre contra una instancia donde su propio agente no esta registrado -- el turno se rechaza en la puerta y el obstaculo que iba a medir no llega a ejercerse
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0399-el-probe-de-turno-corre-contra-una-instancia-donde-su-propio-agente-no-existe.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Medido por el Arquitecto el 2026-08-15 sobre el commit `c5ed73f2`, job
    `falsification-runners-python` (runner Linux propio):

        assert result["turns"][0]["outcome"] != "rejected", result
        AssertionError: {... 'run_id': 'RUN-routed-obstacles', ...
          'turns': [{'turn': 1, 'outcome': 'rejected',
                     'errors': ['semantic: agent not registered: Codex'],
                     'trace': ['gate_pre', 'route', 'claim', 'adapter', 'validate'], ...}]}

    El probe (`examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`) monta una instancia
    temporal y ejecuta un turno con owner `Codex` sobre `TASK-9000`. La instancia que monta NO tiene a
    `Codex` en su registro de agentes, asi que el turno se rechaza en la validacion semantica.

    El detalle que hace esto algo mas que una CI rota esta en el `trace`: el turno recorrio
    `gate_pre -> route -> claim -> adapter -> validate` y murio en el ultimo paso. Los obstaculos que
    este caso existe para medir -- eso es lo que significa `routed-obstacles` -- se ejercen en ese
    recorrido; y el propio resultado lo confirma: `obstacles: []`, `collisions_avoided: 0`. El caso
    no ha medido ningun obstaculo. Ha medido que su instancia de juguete esta mal sembrada.

    A diferencia de TASK-0396, aqui el aborto es RUIDOSO por casualidad: la asercion mira `outcome`,
    que es justo el campo que el rechazo cambia. Si el probe hubiera comprobado cualquier otra cosa --
    por ejemplo que no hubo colisiones, o que no hubo reverts -- una instancia sin agentes registrados
    habria dado verde con cero obstaculos ejercidos, y nadie se habria enterado. Esa es la propiedad
    que conviene cerrar, no solo la siembra.
  acceptance:
    - "AC1 (reproducir primero): capturar el rechazo actual con su `errors` y su `trace` completos
      antes de tocar la siembra."
    - "AC2 (la instancia del probe registra a los agentes que el propio probe usa): el turno deja de
      rechazarse por agente no registrado. La siembra se DERIVA de los agentes que el caso va a
      ejercer, no se transcribe una lista al lado que pueda volver a divergir."
    - "AC3 (el caso no puede pasar sin haber ejercido nada): si el turno termina con cero obstaculos
      ejercidos, el caso falla y lo dice. Es la mitad que hoy falta: sin ella, la proxima instancia
      mal sembrada saldra verde en vez de roja."
    - "AC4 (el negativo SIGUE cazando lo suyo): tras el cambio, el defecto que este caso existe para
      detectar en el enrutado de obstaculos sigue saliendo en exit 1, con el control en 0. Se
      acredita mutando produccion, no el probe."
    - "AC5 (CI): el job `falsification-runners-python` deja de caer por esta causa sobre el commit de
      entrega, acreditado con el run de CI."
  verification_cmd:
    - "python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - examples/runtime_turn_cases/
    - scripts/
  out_of_scope: >
    NO se tocan las otras tres causas rojas del mismo run (TASK-0396, TASK-0397, TASK-0398). NO se
    anade `Codex` al registro de agentes de la instancia VIVA de este repo: el defecto esta en como
    el probe siembra SU instancia temporal, y tocar el registro vivo seria repararlo por el sitio
    equivocado.
  risk: medium
  estimate: M
---

# TASK-0399 -- el probe de turno corre contra una instancia donde su propio agente no existe

## Evidencia

Run `31883703617`, job `falsification-runners-python`, commit `c5ed73f2`:

    outcome: 'rejected'
    errors: ['semantic: agent not registered: Codex']
    trace:  ['gate_pre', 'route', 'claim', 'adapter', 'validate']
    obstacles: []
    collisions_avoided: 0
    turns_total: 1, gates_green_pct: 100.0

## La parte generica

`gates_green_pct: 100.0` con `obstacles: []` es la firma de un caso que no midio nada y no lo dijo.
Aqui se vio porque la asercion apuntaba justo al campo que el rechazo altera. AC3 existe para que la
proxima vez no dependa de esa coincidencia.

-- Arquitecto, 2026-08-15
