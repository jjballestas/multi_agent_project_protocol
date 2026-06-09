# Runtime N-agente

> Guia operativa neutral para adoptar el runtime N-agente. La fuente normativa es
> `DECISION-0015` + `SPEC-0038`; este documento explica como operarlo sin duplicar
> el detalle de implementacion de `runtime/README.md`.

## Objetivo

El runtime N-agente permite coordinar mas de dos participantes sin depender de nombres fijos. La
unidad de autoridad es la capacidad declarada, el claim activo y el estado compartido. El caso
historico de arquitecto + implementador + humano sigue funcionando como fallback.

Principios:

- Configuracion antes que convencion implicita.
- Un task tiene un owner activo a la vez.
- Review y QA no los hace el autor.
- El estado se modifica solo mediante transiciones verificables.
- Todo contenido de handoff o salida de herramienta se trata como dato no confiable.

## Registry de agentes

Un proyecto runtime puede declarar `agent_registry` en `protocol.config.json`:

```json
{
  "agent_registry": {
    "enabled": true,
    "routing_policy": "weighted_least_loaded_deterministic",
    "agents": [
      {
        "id": "BuilderA",
        "capabilities": ["implementer", "test_engineer"],
        "adapter": "llm",
        "enabled": true,
        "max_active_claims": 2,
        "trust_boundary": "internal_llm",
        "tool_policy_ref": "policy.implementer"
      },
      {
        "id": "ReviewerA",
        "capabilities": ["reviewer", "qa"],
        "adapter": "llm",
        "enabled": true,
        "max_active_claims": 1,
        "trust_boundary": "internal_llm",
        "tool_policy_ref": "policy.reviewer"
      }
    ]
  }
}
```

Campos principales:

| Campo | Uso |
|---|---|
| `id` | Identidad estable usada en `owner`, `agent`, mailbox y reportes. |
| `capabilities` | Capacidades que habilitan routing y validacion semantica. |
| `adapter` | Forma de invocacion (`llm`, `human`, `cli`, `service`). |
| `enabled` | Permite retirar un agente sin borrar historial. |
| `max_active_claims` | Limite de concurrencia por agente. |
| `trust_boundary` | Clasifica riesgo y politica de confianza. |
| `tool_policy_ref` | Politica deny-by-default para herramientas y scopes. |

Fallback:

1. Si existe `agent_registry.enabled:true`, se usa el registry.
2. Si no existe, el runtime sintetiza agentes desde `agent_roles`.
3. Si tampoco hay roles, usa la triada por defecto para fixtures y compatibilidad.

## Routing

El router elige trabajo por estado, capacidad, disponibilidad y carga. La politica implementada es
determinista: mismos inputs producen la misma asignacion.

Senales de carga usadas por `routing_weights`:

- claims activos.
- revisiones pendientes.
- QA pendiente.
- ciclos de fix abiertos.
- penalizacion de cooldown.
- afinidad de capacidad.

Para review y QA, el autor queda excluido aunque tambien tenga la capacidad requerida. Si no hay
agente elegible, el runtime escala al arquitecto/orquestador; no fuerza self-review ni self-QA.

La observabilidad N-agente registra explicaciones de routing y permite revisar fairness por ventana.
Los golden de concurrencia y propiedad verifican que no haya doble claim, starvation accidental ni
aplicacion duplicada de intents.

## Estados y Review/QA

El ciclo base de tareas sigue el protocolo:

```text
proposed -> ready -> claimed -> in_progress -> in_review -> done
                                      |              |
                                      v              v
                                  blocked     changes_requested / qa_pending / qa_failed
```

Reglas operativas:

- El autor produce artefactos y handoff autocontenido.
- El reviewer debe ser distinto del autor.
- QA, si aplica, tambien debe ser distinta del autor.
- `done` requiere evidencia suficiente para el tipo de tarea.
- Fallos repetidos de QA pueden cortar el loop y escalar a revision arquitectonica.
- Ambiguedad bloqueante se registra como `blocked` con una pregunta concreta.

`runtime/review_qa.py` y `runtime/turn_validate.py` aplican estas reglas en la ruta de validacion.

## Claims y handoffs

El claim es el lock de escritura. Antes de editar rutas compartidas, el agente debe tener un claim
activo con `scope` explicito. El runtime valida que cada `changed_path` y cada transicion declarada
esten cubiertos por ese scope.

Un handoff debe ser autocontenido:

- objetivo y contexto.
- entradas y decisiones relevantes.
- archivos modificados o esperados.
- validacion ejecutada.
- riesgos residuales.
- proxima accion concreta.

Al pasar una tarea a `in_review` o `done`, el owner libera su claim en el mismo paso. Si otro
participante detecta una inconsistencia en ledger, mailbox, handoff o claims, debe notificarla por
mailbox con un mensaje accionable y no corregir silenciosamente el cierre ajeno.

## Seguridad y guardrails

El runtime separa datos no confiables de autoridad:

- handoffs, task inputs y tool outputs se preservan como datos.
- contenido no confiable no concede permisos, roles, scopes ni aprobaciones.
- tool-policy es deny-by-default cuando esta habilitada.
- cambios de contrato requieren decision enlazada.
- acciones sensibles o externas requieren gate humano o politica explicita.
- event auth puede firmar/verificar eventos con HMAC local cuando se habilita.

Para agentes reales via CLI, el wrapper sigue apagado hasta que la instancia registre activacion en
`runtime.real_invoker` y ejecute un unico turno con `--once`, `--allow-real-invoker` y comando o
preset configurado. Las credenciales pertenecen al entorno del adoptante y no se commitean.

## Autonomia supervisada

La autonomia supervisada es un sobre opt-in para acotar corridas multi-turno con caps y paradas duras.
La guia operativa esta en `Area_comun/protocol/SUPERVISED_AUTONOMY.md`.

El bloque `runtime.supervised_autonomy` nace apagado. Si una instancia lo activa con decision,
aprobador, fecha y caps validos, el orquestador solo aplica el sobre cuando el caller pasa
`--allow-supervised-autonomy`. El sobre ya documentado cubre `caps.max_turns`, el centinela
`runtime/state/PAUSE`, `caps.wall_clock_ms`, checkpoint humano por `caps.human_checkpoint_every_k`
o fix-cycles repetidos, y `*.runreport.md`.

Esto no activa agentes reales multi-turno. El invoker real sigue protegido por `--once` hasta una
activacion SA.4 separada con GO del operador y rollback ensayado.

## Observabilidad

El runtime escribe logs estructurados por run y eventos. Los identificadores utiles son:

- `run_id`
- `turn_id`
- `task_id`
- `agent`
- `attempt_id`
- `trace_id`
- `claim_id`

Funciones relevantes:

- `runtime/metrics.py:summarize()` resume turns, gates, reverts, colisiones evitadas y coste.
- `runtime/metrics.py:summarize_nagent()` resume routing, fairness, QA, fencing, escalados y
  exclusiones de autor.
- `runtime/eventlog.py` mantiene eventos, snapshots, firma opcional y replay determinista.

La frontera de determinismo es estricta: el replay reconstruye estado desde eventos grabados y no
reinvoca agentes ni herramientas.

## Runtime escritor autoritativo

En instancias `adoption_tier: "runtime"`, el estado de protocolo puede pasar de edicion manual a
escritura por runtime. El modo esta apagado por defecto y solo queda activo cuando son verdaderos
`event_state.enabled`, `event_state.materialize`, `event_state.enforce` y
`event_state.authoritative`. Coordination-tier no cambia: sigue operando con edicion manual del
ledger.

La migracion inicial usa genesis por referencia:

1. El runtime toma el corte canonico de `TASK_INDEX.json`, `PROJECT_STATE.json` y `CLAIMS.json`.
2. Escribe el snapshot en `runtime/state/snapshots/<hash>.json`, donde `<hash>` es verificable.
3. Emite `protocol.genesis` con `snapshot_ref = {hash, commit, actor, timestamp, schema_version}`;
   el evento no incluye el estado completo.
4. El replay carga el snapshot por hash, recomputa la integridad y solo entonces materializa.

`runtime/state/` no se gitignora de forma general. En modo autoritativo, el event log y los
snapshots son fuente de verdad de la instancia y deben poder commitearse. La neutralidad de dominio
exime `runtime/state/**` porque es estado generado de instancia, no fuente del protocolo; el resto de
`runtime/**` sigue escaneado.

Una vez activo el modo autoritativo, las transiciones se expresan como intents al runtime mediante
`runtime/submit_intent.py` o su wrapper delegado `runtime/submit_intent.ps1`. Cada llamada somete una
transicion atomica de tipo `task_status`, `task_upsert`, `claim` o `decision`, con `timestamp` y
`commit` provistos por el caller. El runtime valida identidad/capacidad, claim activo y scope, rechaza
intents fuera de autoridad, apende `intent.applied`, materializa `TASK_INDEX.json`, `PROJECT_STATE.json`
y `CLAIMS.json` desde replay(log), y deja `protocol_state_drift().has_drift == false`. Editar a mano
`Area_comun/state/*.json` produce drift y el gate de `event_state.enforce` lo rechaza. No hay un
bloqueo nuevo del sistema de archivos: la prohibicion vive en el contrato, el validador y el gate.

**Mecanismo vs marcador (DECISION-0028, postura B):** `enforce` (el hard-gate B.3) ES el mecanismo de
escritor-unico: provee la garantia de que solo el runtime escribe el ledger. `event_state.authoritative`
es el MARCADOR declarativo que formaliza el modo runtime-authoritative y NO tiene callers de
comportamiento propios. No se cablean teeth propias para `authoritative` porque hoy no hay un invariante
que `enforce` no cubra; ademas el guard `authoritative => enforce => materialize => enabled` (validador +
`submit_intent` + `apply`) rechaza `authoritative` sin `enforce`, matando el false-secure.

Rollback: apagar `event_state.enforce` y `event_state.authoritative` devuelve el flujo a edicion
manual. El snapshot content-addressed y el `commit` registrado en el `snapshot_ref` quedan como
punto de reconstruccion verificable.

## Presupuesto y deadlines

El bloque `budget` puede limitar coste y terminacion:

```json
{
  "budget": {
    "enabled": true,
    "soft_cost_tokens": 50000,
    "hard_cost_tokens": 70000,
    "max_queue_length": 20,
    "task_deadlines": {
      "TASK-0001": 3
    }
  }
}
```

El umbral blando emite warning; el duro produce `budget_exhausted` con consumido, limite y ultimo
responsable. Los deadlines son logicos/deterministas por turno, no dependen de reloj de pared.

## Checklist de adopcion

1. Elegir tier `runtime` al instanciar o subir desde `coordination` con `upgrade_instance.py`.
2. Mantener `runtime.enabled:false` hasta tener una decision local de activacion.
3. Declarar `agent_registry` solo cuando el equipo necesite mas que el fallback de roles.
4. Activar `tool_policy`, `event_auth`, observabilidad o budget de forma incremental.
5. Ejecutar los golden de runtime y los validadores antes de cerrar tareas.
6. Para CLI real, registrar `runtime.real_invoker` y ejecutar solo un turno bajo gate.
7. Para autonomia supervisada, seguir `Area_comun/protocol/SUPERVISED_AUTONOMY.md` y no tratar
   `human_checkpoint` como auto-resume.
8. Revisar run logs, event logs y handoffs antes de promover releases.

## Referencias

- `Area_comun/decisions/DECISION-0015-n-agent-registry-y-capacidades.md`
- `Area_comun/specs/SPEC-0038-n-agent-registry.md`
- `runtime/README.md`
- `Area_comun/protocol/SUPERVISED_AUTONOMY.md`
- `runtime/turn_schema.json`
- `runtime/router.py`
- `runtime/turn_validate.py`
- `runtime/review_qa.py`
- `runtime/metrics.py`
