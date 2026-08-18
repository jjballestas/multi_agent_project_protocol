---
message_id: MSG-20260818-Arquitecto-to-Operador-VEREDICTO-camino-de-subida
from: Arquitecto
to: Operador
type: RESP
task_id: none
status: open
requires_response: true
response_owner: Operador
one_line_summary: "VEREDICTO BLOQUEA, por unanimidad de los tres revisores y con dos bloqueantes que verifique YO contra el genesis real (seq 672). R6 y la rama de config de R4 rompen la cadena por su via documentada. Y R0, la clausula rectora, dice lo contrario de lo que el sistema hace: el Operador NO es actor registrado y no puede sellar una decision. El fondo es solido y R5 es su mejor clausula; lo que no se puede firmar es el documento de hoy."
requested_action: "Decide sobre las enmiendas E1-E8 de la seccion final: ninguna exige rehacer el draft, son cirugia sobre R0, R4 y R6 mas una renumeracion. Y decide el punto que NO puedo decidir yo: si se da de alta un actor human_owner en el agent_registry, porque eso toca el config PINEADO y es tu llave."
question: "Autorizas la reescritura de R0/R4/R6 segun E1-E3, y que hacemos con R0 sabiendo que dotarlo de mecanismo exige tocar el config pineado: lo dejamos como limite declarado o entra en la cola de una re-genesis futura?"
context_refs:
  - personal/asesor/DRAFT-DECISION-0104-camino-de-subida-instancia-a-master.md
  - Area_comun/decisions/DECISION-0047-versionado-epoca-bajo-4.md
  - Area_comun/tasks/TASK-0410-la-paridad-de-inventario-de-identidad-diverge-entre-gemelos-y-su-censo-no-cuadra.md
deadline_or_blocking_level: normal
---

# VEREDICTO -- BLOQUEA. Tres revisores, unanimidad, dos bloqueantes verificados por mi

Hora del reloj: **2026-08-18 07:55 local (UTC+2)**. Tres revisores independientes, seis lentes
repartidas, el autor excluido. **Los tres votan BLOQUEA**, por caminos distintos y sin contradecirse.

**El fondo del draft es solido.** R0/R1/R2/R3/R5 apuntan a lo correcto y **R5 es la mejor clausula
del texto**. Lo que no se puede firmar es **el documento de hoy**.

## Los dos bloqueantes, verificados POR MI contra el evento genesis real

    genesis REAL de la cadena:  seq 672   prev_hash 649d99e6eb37c29c764f48cd
    canonical_hash(config)               = 649d99e6eb37c29c764f48cd    COINCIDEN

    R6 sube protocol_version    -> ccd1d191...    genesis mismatch
    R6 sube runtime_version     -> 28628d72...    genesis mismatch
    R4 via upgrade.adoptable_globs en el config -> 13a7a27c...  genesis mismatch

**B1 -- R6 es la politica CONTRARIA a la vigente.** Dice que la promocion incrementa
`protocol_version` y `runtime_version`. Ambas viven en el config pineado, asi que R6 convierte
**cada promocion en una re-genesis**, que esta prohibida y que negaste por escrito el 17-ago
("esa llave es del operador humano en persona"). Agravante medido: **su justificacion es falsa**.
R6 se justifica "para que `upgrade_instance.py` tenga contra que comparar", pero `classify()`
compara **contenido de fichero**, no versiones: hub y NOVA declaran **la misma version** y difieren
en 41 ficheros.

**B2 -- R4 nombra como verificacion un instrumento medido hoy como FALSO en los dos sentidos.**
Experimento controlado: skill desplegada y **corrompida** produce "igual, sin accion"; skills
desplegadas y **correctas** producen "nuevo, anadir a la instancia". Aplicando R4 literalmente a su
propia primera aplicacion, el veredicto seria "la pieza no ha subido" sobre una pieza desplegada y
en uso.

## El hallazgo que mas me importa, tambien verificado por mi

**R0, la clausula rectora, dice lo contrario de lo que el sistema hace.**

    agent_registry: Arquitecto(orchestrator) | Codex(implementer) | Analista(reviewer)
    human_owner en el config: None

R0 dice que "la promocion ocurre unicamente cuando el Operador la firma". Medido: **el Operador no
es un actor registrado**, `human_owner` es un string suelto y no una fila del registry, y el unico
que puede sellar un intent `decision` es el **Arquitecto**. Tu firma en el markdown **no la lee
ningun gate**. La clausula que gobierna a las otras seis es la que menos mecanismo tiene.

**Y aqui esta el limite que no puedo resolver yo:** dotar a R0 de mecanismo exige dar de alta un
actor `human_owner` en el `agent_registry`, que vive **dentro del config pineado**. Es tu llave.

## Lo que deja al draft sin efecto aunque se firme

**Su unica aplicacion nombrada ya se consumo sin pasar por el.** La memoria hibrida esta promovida:
**TASK-0314 `done` el 2026-08-06**, con `scripts/memory/` ya en el hub. Y sus AC **no contienen
ninguna medicion de coste**, que es justo lo que R5 exige. Firmado tal cual, el draft nace con
**cero aplicaciones vinculantes**.

## Sobre la enmienda del generador: no es construible como esta, y la propuse yo

Lo digo porque es mia. El revisor cuantifico que **el 86,2 % del hueco entre vivo y master no
contiene ningun token** de los que la enmienda enumera: son parrafos enteros de juicio editorial,
sobre los que el fallo-cerrado **no puede dispararse**. El mejor oraculo derivable que se pudo
construir cubre el **4,6 %**.

Y el modelo que yo queria copiar esta peor de lo que crei: **TASK-0410 esta rojo, sin arrancar desde
hace dos dias**, y su paso **no se ejecuta en CI en 19 de 19 corridas** porque el job muere antes,
en el paso 23. Disenaron ademas cuatro bypasses del gate propuesto, y **el mas barato cuesta cero**
porque el gate heredaria un job que ya muere antes de llegar.

## Enmiendas exactas -- ninguna exige rehacer el draft

**E1. R6, sustituir entero.** La promocion se registra en el CHANGELOG y en registries **fuera** del
config pineado; `protocol_version` y `runtime_version` **no se tocan**. Anadir `DECISION-0047` a
`relates_to`.

**E2. R4, borrar la rama del config y reescribir la verificacion.** Los globs entran **solo** en
codigo. La verificacion pasa a exigir el mapeo `master_rel -> instance_rel` y la comparacion sobre
la ruta **CONSUMIDA**, con **puerta de secuencia**: R4 no es exigible hasta que TASK-0394 y
TASK-0417 esten en `done`.

**E3. R0, o mecanismo o limite declarado.** Con alta de actor `human_owner` (tu llave), o el texto
**dice** que la firma es un acto fuera del ledger que ningun gate comprueba. Lo que no puede es
afirmar un mecanismo que no existe.

**E4. R5, hacerla falsable.** Hoy ninguna medicion puede suspenderla ("el signo del delta NO es
criterio de rechazo") y nada detecta su ausencia. Detector: el intake de la tarea de promocion
contiene los tres numeros y el comando que los reproduce; el gate enrojece si falta cualquiera.

**E5. R2, nombrar la unidad contable:** N eventos de tipo T en el log atestado, declarados por la
pieza en su intake. Si no se puede nombrar T, que el texto admita que es juicio humano.

**E6. R3, cerrar la ceguera antes de invocar el gate.** `scan_domain_neutrality` escanea **0 de 198**
ficheros bajo `claude-skills`, y los masters ya filtran `TASK-0235/0236/0240`. Anadir
`scripts/**/*.md` a `scan_globs`.

**E7. Renumerar a DECISION-0121**, no a 0120: **0120 la ocupe yo hace una hora** con el borrador de
la clausula de poda que me encargaste en A2. Y reconstruir `relates_to`, que hoy omite **todas** las
decisiones que colisionan con el: 0047, 0104, 0110, 0117, 0118 y las TASK-0394/0417.

**E8. Anadir R7:** ninguna promocion toca `protocol.config.json`. Si una promocion necesita una
clave nueva ahi, la pieza **no es elegible**: se rehace para vivir en codigo o en un registry
externo, o se escala como re-genesis, que es una decision aparte.

## Lo que NO recomiendo

**No derogarlo ni rehacerlo.** El diagnostico que lo motiva sigue siendo correcto --*una regla que no
viaja no es del protocolo, es de este repo*-- y R5 es una clausula que este repo necesita. Es
cirugia sobre tres clausulas, no una reescritura.

-- Arquitecto, 2026-08-18 07:55 local (UTC+2)
