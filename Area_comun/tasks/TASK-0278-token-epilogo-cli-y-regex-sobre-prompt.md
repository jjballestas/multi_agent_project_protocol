---
task_id: TASK-0278
title: "[HARNESS][CAMPO] El token de outcome es invisible en produccion: el epilogo del CLI va DESPUES de la ultima linea, y el regex de respaldo lee el prompt del propio encargo"
type: fix
status: in_progress
owner: Codex
phase: P2
priority: high
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0272, TASK-0276, DECISION-0103, DECISION-0020]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0278-token-epilogo-cli-y-regex-sobre-prompt.md
intake:
  type: fix
  goal: "Defecto de CAMPO observado dos veces en los primeros quince minutos tras desplegar TASK-0272 (execs de las 16:44 y las 16:56 del 2026-07-20). La regla terminal-only introducida en la iteracion 2 exige que el token OUTCOME sea la ULTIMA linea no vacia del transcript, pero el CLI del implementador imprime su propio epilogo (tokens used y el conteo) DESPUES de la respuesta del modelo, asi que el token NUNCA es la ultima linea en produccion. El agente lo emitio correctamente ('OUTCOME: transient' en ambos casos) y el harness lo ignoro. Peor todavia, al caer al respaldo por texto libre, el regex escanea el transcript COMPLETO, que incluye el prompt del encargo con el intake pegado dentro, y ahi vive literalmente 'out_of_scope' y 'FUERA de alcance', asi que la cadena marca DEFINITIVE lo que el agente declaro TRANSIENT. Resultado neto, un aborto reintentable queda consumido sin reintento y sin senal, que es exactamente el seen-burn silencioso que TASK-0272 existe para eliminar."
  acceptance:
    - "El token se reconoce aunque el CLI anada su epilogo: la busqueda ignora las lineas de epilogo conocidas del invocador o busca el token como ULTIMA APARICION en linea propia con igualdad exacta, sin volver a admitir tokens en medio de la prosa."
    - "El respaldo por texto libre deja de leer el ECO DEL PROMPT: solo se escanea la respuesta propia del agente, no el encargo ni el intake que van dentro del transcript."
    - "Con el mismo transcript real de los dos execs del 2026-07-20 (adjuntos en runs/), el outcome resultante es transient, no definitive; se anaden como fixtures permanentes de regresion."
    - "Negativo permanente: transcript con epilogo del CLI tras el token para CADA invocador soportado (implementador y checker), porque sus epilogos son distintos."
    - "Un outcome DEFINITIVE nunca puede derivarse solo del respaldo por texto libre; exige token exacto o exit code, para que ningun aborto reintentable pueda consumirse por coincidencia lexica."
    - "Espejo en el harness generico del export born-operational."
  verification_cmd:
    - "Runner de la suite del reintento (examples/, patron run_*.py) en verde, con los fixtures nuevos"
    - "Reproduccion sobre los transcripts reales de .protocol-tmp/codex_mailbox_cron/runs/ del 2026-07-20"
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - scripts/
    - examples/
    - personal/Codex/
    - personal/Analista/
  out_of_scope:
    - "Reabrir el acceptance de TASK-0272, que ya esta cerrada - FUERA, esto es un defecto de campo posterior."
    - "Cambiar la frontera de autoridad decidida (token exacto, luego exit, luego evidencia propia, y el texto libre solo como respaldo) - FUERA, el defecto es que la implementacion no la respeta en produccion."
    - "Tocar el CLI del invocador o su salida - FUERA, el harness debe tolerar el epilogo, no exigir que desaparezca."
    - "protocol.config.json pineado y dataset N=500 - FUERA (fondo intocable)."
  risk: high
  estimate: S
---

# TASK-0278 - El token existia y el harness no lo veia

Evidencia de campo, dos ejecuciones reales del 2026-07-20 bajo el harness recien
desplegado:

| hora | mensaje | lo que dijo el agente | lo que registro el harness |
|------|---------|-----------------------|----------------------------|
| 16:44 | ACTION done-flip 0272 | `OUTCOME: transient` | `outcome=definitive` |
| 16:56 | GO TASK-0277 | `OUTCOME: transient` | `outcome=definitive` |

En ambos el transcript termina asi:

```
OUTCOME: transient
tokens used
42.041
```

La ultima linea no vacia es el conteo de tokens del CLI, no el token del contrato. La
regla terminal-only, que se anadio para que nadie pudiera colar un token en mitad de la
prosa, choca de frente con un invocador que escribe despues del modelo.

El segundo defecto es mas silencioso y mas grave: cuando el token no se reconoce, el
respaldo por texto libre escanea el transcript ENTERO, y ahi esta pegado el prompt del
encargo, que incluye el intake con sus `out_of_scope` y sus `FUERA de alcance`. Es decir,
el respaldo no lee lo que el agente respondio, lee lo que yo le pedi. Cualquier encargo
con un bloque de alcance bien escrito arrastra su propio exec a `definitive`.

Por que es prioridad alta pese a ser una unidad pequena: el efecto es exactamente el
fallo que la tanda declaro como el peor observado. Un aborto legitimo por ventana ocupada
se marca como definitivo, el mensaje se consume, nadie reintenta y no queda senal. Lo
detectamos porque el despliegue lo hizo visible a los quince minutos, no porque un gate lo
cazara.
