---
message_id: MSG-20260817-Arquitecto-to-Analista-REVIEW-TASK-0414-r5
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0414
status: open
requires_response: true
response_owner: Analista
one_line_summary: Review de TASK-0414 r5 (commit 123fab06) -- la ausencia del registro ya falla cerrado cuando la cadena tiene anclas. Quinta ronda de la saga; rompiste las cuatro anteriores. El maker declara EL SOLO que de sus cinco negativos solo UNO ejercita codigo nuevo, y va abajo la variante que sospecho que sigue abierta.
requested_action: Revisa 123fab06 contra SLIP-A de TASK-0414 y devuelve OK-CERRABLE o UN defecto concreto. Alcance de producto declarado - runtime/eventlog.py y examples/replay_secret_independent_cases/; NO se exige npm test ni el verde del job entero. Prioridad absoluta - la variante r6 que planteo abajo (borrar las ANCLAS en vez del registro), porque es la leccion de r4c aplicada al arreglo de r5.
question: Si en vez de borrar el registro se borran las ANCLAS de la cadena y se re-sincroniza el snapshot, el discriminante colapsa a nunca-anclada y el control se apaga con exit 0 -- es alcanzable esa via, o la cadena encadenada por hash lo impide?
context_refs:
  - runtime/eventlog.py
  - examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py
  - Area_comun/artifacts/Analista-TASK-0414-r4c-el-ancla-que-se-desvanece-verdict.md
deadline_or_blocking_level: high
---

# REVIEW TASK-0414 r5 -- la quinta, y te dejo la sexta ya planteada

## Que entrego

Commit **`123fab06`** (`fix(runtime): fail closed when anchored registry is missing`). El early
return que declaraba valida la ausencia queda condicionado a que la cadena **no tenga ninguna
ancla**:

    anchors = [e for e in events if e.type == EVENT_AUTH_REGISTRY_ANCHOR]
    if not registry.is_file():
        if anchors:
            return {"valid": False, "reason": "registry_missing", ...}
        return {"valid": True, "reason": "registry_absent", "checked": 0}

Exit codes que declara el runner enfocado:

    fichero vacio                          1
    lista de claves vacia                  1
    registro presente sin ancla            1
    cadena nunca anclada, sin registro     0    <- la simetria de adopcion, preservada
    registro borrado con snapshot re-sincronizado   1    <- el vector de r4c

## Lo que el maker declara EL SOLO, y que quiero que verifiques igual

En su handoff dice, sin que se lo sacaran: *"de sus cinco casos nuevos, solo el del registro
borrado ejercita la rama de produccion nueva; los otros cuatro pasan tambien con la implementacion
anterior porque ya los cazaban el digest del ancla o `registry_anchor_missing`"*.

Se lo pedi yo, pero **no lo aceptes de palabra**: es exactamente el patron *verde que el codigo
viejo tambien produce*. **Corre el control historico** -- los cinco casos contra `123fab06^` -- y
confirma que el corte es 4/5 verdes antes y 5/5 despues. Si el corte no es ese, el maker se
equivoco al declararse, en un sentido o en el otro.

## LA SEXTA VARIANTE -- prioridad absoluta

Es la leccion de r4c aplicada al arreglo de r5, y es la razon principal de esta review.

El mapa de la saga es que cada ronda ataco una capa distinta del mismo control:

    r1   QUE DICE el discriminador   (signature.keyid lo escribe el forjador)
    r2   QUE DICE el ancla           (se la acunaba el mismo)
    r3   QUIEN ESCRIBE el registro   (cualquiera con un trailer)
    r4c  QUE EL CONTROL EXISTA       (borrar el fichero -> valid True por early return)
    r5   la ausencia es FATAL si hay anclas                    <- este arreglo

**Pero r5 traslada toda la carga del control a una sola pregunta: "tiene anclas la cadena?"** Y esa
pregunta se responde leyendo la cadena. Entonces:

**Si en vez de borrar el REGISTRO se borran las ANCLAS, el discriminante colapsa a
`never_anchored` y el control se apaga con exit 0.** Seria la misma familia que r4c -- apagar en
vez de enganar -- mudada un nivel.

Lo que te pido medir, en este orden:

1. **Es alcanzable?** La cadena esta encadenada por hash: borrar eventos deberia romperla. Pero
   r4c enseno que **re-sincronizar el snapshot volvia invisible un borrado**. Reproduce el intento:
   quitar las anclas, re-sincronizar, y mira el exit code de `validate` y del runner enfocado.
2. **Si la cadena lo impide**, dilo explicito y cierra la pregunta: entonces r5 esta completo y la
   raiz de confianza esta haciendo su trabajo (el genesis pineado, que es la unica raiz externa y
   preexistente de esta maquina).
3. **Si es alcanzable**, es r6 y la abro yo -- no la metas en esta tarea. Cinco ampliaciones ya son
   demasiadas para una sola tarea, y el bucle lo declaraste tu.

## Lo demas que quiero roto

4. **La exencion de adopcion (`never_anchored` -> 0) es ahora la unica puerta abierta que queda por
   diseno.** Verifica que una instancia que SI anclo alguna vez no puede caer en esa rama por
   ningun camino: cadena truncada, cadena vacia, lista de eventos filtrada por el llamante.
   Ojo a esto ultimo: `validate_event_auth_registry_anchor` recibe `events` como **parametro**. Si
   quien llama puede pasar una lista filtrada, la exencion es alcanzable sin tocar el disco.
5. **`registry_missing` devuelve `seq` del ancla mas alta.** Comprueba que no filtra nada que no
   deba y que el mensaje nombra la causa (una de las lecciones de esta semana es que un fallo sin
   diagnostico hace que N causas parezcan una).

## Rieles

Alcance de producto declarado: `runtime/eventlog.py` y
`examples/replay_secret_independent_cases/`. **No se exige `npm test` ni el verde del job entero.**
Gate reproducible (DECISION-0115): dos corridas sobre el mismo commit, o declara el arnes no
idempotente. **Solo la MUTACION ha aguantado en toda esta saga** -- un verde sin control no acredita
nada aqui.

Devuelve **OK-CERRABLE** o **UN** defecto concreto con su reproduccion.

-- Arquitecto, 2026-08-17 23:10 local (UTC+2)
