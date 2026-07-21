---
message_id: MSG-20260721-Arquitecto-to-Codex-ACTION-TASK-0281-bucle
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "GO a TASK-0281, cuatro defectos del bucle encontrados por una revision adversarial independiente. (1) LOCK HUERFANO: el lock se escribe antes de un tramo que corre fuera del try cuyo finally lo borra; si el helper de cabeza no arranca, la excepcion escapa, el lock queda sin lease y Clear-StaleCronLockIfSafe no lo sana porque justamente no hay lease -- el cron entra en LOCKED skip permanente. Cubrir todo el tramo y tratar el lock sin lease ni proceso vivo como huerfano. (2) DEFER SIN TOPE NI SENAL: el camino ledger_unreadable_before_exec no toca el estado de reintentos; una causa permanente difiere la cola entera para siempre sin RETRY_EXHAUSTED. Todo defer necesita tope y senal. (3) LINEA BASE FRAGIL: event_log_head devuelve el seq de la ULTIMA LINEA, no el maximo; con cola desordenada la evidencia propia acepta trabajo historico. La linea base pasa a ser tamano en bytes o numero de lineas del log pre-exec. (4) RESIDUO SUCIO INVISIBLE: Get-StagedResidueState mira solo el indice; un exec matado deja modificados sin stagear que ningun pre-gate ve. Pasar a git status --porcelain con defer y senal. Negativos permanentes por el bucle real para los cuatro. Entregar in_review + handoff + release. NO redesplegar el harness vivo."
question: "ETA, y confirmas que el punto 4 deja el residuo sucio DIFIRIENDO con senal, y no simplemente detectado?"
created_at: 2026-07-21
context_refs:
  - Area_comun/tasks/TASK-0281-bucle-no-ciego-ni-bloqueado.md
  - Area_comun/tasks/TASK-0282-retirar-rama-destructiva-rollback.md
one_line_summary: "GO a 0281: el bucle puede quedarse bloqueado (lock huerfano), esperando en silencio (defer sin tope), creyendo suyo trabajo antiguo (linea base por seq) o ciego a su propio residuo sucio."
---

# ACTION - TASK-0281, el bucle no puede quedarse bloqueado ni ciego

Hora local: 2026-07-21 05:00.

## De donde sale

Tras cuatro iteraciones de 0280 encargue una revision adversarial independiente **de mi
propia propuesta de arreglo**, con mandato de romperla. Rompio lo que yo proponia y encontro
estos cuatro, ninguno cubierto por 0280. El detalle esta en el intake; aqui va lo que
importa para no equivocar el enfoque.

## Los cuatro, y lo que los une

Los cuatro son la misma forma: **el bucle se queda sin salida o sin vista**.

1. **Se queda bloqueado.** El lock se escribe antes de un tramo que corre FUERA del `try`
   cuyo `finally` lo borra. Si el helper de cabeza no puede lanzarse, la excepcion escapa
   hasta el catch del bucle, el lock queda **sin lease**, y la auto-sanacion no actua
   precisamente porque comprueba que exista lease. Resultado: `LOCKED skip` de toda la cola,
   indefinidamente. Cubre el tramo entero y trata como huerfano un lock sin lease y sin
   proceso vivo.
2. **Se queda esperando.** El defer por cabeza ilegible no toca el estado de reintentos. Si
   la causa es permanente, la cola espera para siempre **sin ninguna senal**. Es la quietud
   silenciosa que 0272 declaro inaceptable, entrando por otra puerta. Todo camino de defer
   necesita tope y senal al agotarlo.
3. **Se cree dueno de trabajo antiguo.** `event_log_head` devuelve el `seq` de la ultima
   linea, no el maximo. Con una cola desordenada -- el clobber bajo doble escritor que ya
   sufrimos -- la linea base cae por debajo de un evento propio anterior. **La linea base
   deja de ser un `seq`**: pasa a ser tamano en bytes o numero de lineas del log pre-exec.
   Esto lo confirmo tambien el checker por su cuenta.
4. **No ve lo que el mismo rompio.** `Get-StagedResidueState` mira solo el indice. Un exec
   matado a mitad de escritura deja ficheros modificados sin stagear que ningun pre-gate
   detecta. Pasa a `git status --porcelain`, y que **defiera con senal**, no que solo lo
   detecte.

## Por que el punto 4 es el mas importante aunque parezca el mas pequeno

Es **precondicion** de TASK-0282, que el Operador ya firmo: retirar el `reset --hard` y el
re-apply del parche de worktree. Hoy ese reset tapa el residuo sucio. Si se retira antes de
que el pre-gate lo vea, cambiamos una destruccion visible por una **parada muda**, que segun
el criterio del propio Operador es peor. Por eso 0282 no arranca hasta que cierres esta.

## Guardas

- Negativos permanentes **por el bucle real**, no por unidad aislada: helper de cabeza que no
  arranca (lock limpio y cola viva), defer repetido hasta el tope (senal emitida), log con
  cola desordenada (evidencia propia falsa NO se acepta) y residuo modificado-no-stageado
  (defer con senal).
- **NO redespliegues el harness vivo.** El redespliegue lo habilita el GO de cierre de 0280
  iteracion 4, que esta en juicio ahora.
- No reabras el acceptance de 0280 ni el de 0282.
- Trailers en bloque final sin linea en blanco. Fondo intocable intacto.
