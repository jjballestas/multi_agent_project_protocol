---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0331-r5
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0331
status: archived
created: 2026-08-08T10:15:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0331 -- la tabla de 24 celdas

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `e9719613`.

## Lo que veo, como lectura mia y no como evidencia

La tabla que pediste esta declarada entera -- `lease` (legible / ilegible / 0 bytes / legible sin
identidad util) x `owner` (vivo / muerto / desconocido) x `lock` (presente / ausente) -- con una
regla uniforme: **solo PID mas hora de arranque del proceso prueba `dead`; la evidencia ausente o
ilegible es `unknown`.** Las muertas se borran, las desconocidas se preservan tras un marcador
atomico de recuperacion.

## El foco que decide: la frontera declarada

La entrega declara una frontera y quiero que la juzgues como el punto central, no como una nota:

> una lease ilegible o sin identidad y sin evidencia util de lock no puede distinguirse
> automaticamente de una huerfana muerta; se preserva a proposito y queda tras el marcador
> explicito

**Mi duda es si eso no es el defecto original con otro nombre.** El modo de fallo que abrio 0331 era
"encallado a prueba de rearranques": el sistema se quedaba atascado y hacia falta que yo entrara a
mano. La regla nueva dice, para un subconjunto de estados, exactamente eso: preservar y exigir
intervencion del operador.

Hay una diferencia real y a favor de la entrega: antes el atasco era **mudo** y ahora es **ruidoso**
(`SELF_HEAL_MANUAL_RECOVERY_REQUIRED`). Un atasco visible es mucho mejor que uno silencioso. Pero
esa mejora solo compensa si el estado `unknown` es **raro**.

Asi que la pregunta concreta: **con que facilidad se alcanza `unknown` en operacion NORMAL?** Si una
muerte dura corriente -- de las que ya nos han pasado varias veces esta semana -- deja una lease
ilegible sin lock, entonces hemos cambiado recuperacion automatica por una llamada al operador en el
caso comun, y eso seria una regresion de autonomia disfrazada de mejora de seguridad. Si en cambio
solo se alcanza bajo corrupcion que no se da sola, la frontera esta bien puesta.

Mide la reachability, no la aceptes declarada.

## Los demas focos

**A. La asimetria de la regla, y el reuso de PID.** "Solo PID mas hora de arranque prueba muerto" es
correcto justamente porque el PID solo no basta: el sistema operativo los reutiliza y un PID muerto
reasignado a un proceso ajeno se leeria como vivo y preservaria la lease para siempre. Comprueba que
la comparacion de hora de arranque **discrimina de verdad** y no es vacua -- que exista un caso donde
el PID coincide y la hora no, y que ahi decida `dead`.

**B. Celdas DECLARADAS frente a celdas EJERCIDAS.** Son 24 declaradas. Cuantas observa realmente el
contrato? Es la distincion que nos ha mordido toda la semana -- 0330 con los 23 runners que CI no
corria, 0336 con las formas que el gate listaba sin exigir. Una tabla de 24 celdas de las que el test
toca 9 es una tabla de 9. Quiero el numero medido, y si alguna celda es inalcanzable por
construccion, que vaya declarada como tal y no contada.

**C. Los cuatro mutantes.** `unknown->dead`, evidencia de lock ignorada, admision de peer en unknown,
marcador suprimido. Que cada uno muera, y que al menos donde aplique sea mutante de **codigo muerto**
-- guarda presente pero inalcanzable -- no solo de borrado de linea.

**D. Sin regresion en lo ya probado, que aqui es mucho.** Cuatro vueltas acumuladas: la carrera del
codigo viejo, la admision atomica, `DeleteOnClose` bajo muerte dura, los 17 vectores malformados, los
228 mensajes que recupero F2, y la convergencia a tres rearranques de la r3. Nada de eso debe haberse
movido.

**E. El re-fijado de neutralidad que hizo de paso, y por que lo miro.** La entrega movio las
atestaciones de neutralidad por linea junto con el harness (yo se lo autorice: la tabla de exenciones
fija numeros de linea y sus ~56 lineas nuevas los desplazaban). Verifica que el conjunto exento es
**EL MISMO** -- las mismas ocho ocurrencias, solo reubicadas -- y que no se ha colado ninguna linea
distinta. Re-fijar coordenadas a mano es justo el momento en que se exime algo que no tocaba.

**F. REGRESION QUE YA HE MEDIDO YO -- no la busques, verificala y juzgala.**

Esta la encontre despues de mandarte el encargo, revisando por que CI lleva rojo. La entrega **rompe
un contrato de falsacion que CI ejecuta**, y es reproducible en local:

    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py   ->  exit 1
    AssertionError: TASK-0284 pre-gate contract is incomplete   (linea 342)

Condicion que falla, medida una a una: el contrato exige que
`Write-Utf8NoBom -Path $LockPath` aparezca DESPUES de `$residueState = Get-StagedResidueState`.
**La cadena del lock ya no existe en el fichero** -- `find` devuelve -1 -- porque la remediacion 4
la renombro o la reestructuro. Las otras ocho condiciones del contrato pasan.

En el CI del 6-ago este job estaba VERDE y solo fallaba `validate`; hoy falla tambien
`falsification-runners`. O sea: **es regresion de esta entrega**, no deuda heredada.

Lo que quiero de ti aqui, y no es que confirmes un exit code que ya tengo:

1. **Si el reemplazo es correcto en el fondo.** Puede que la escritura del lock ahora sea mejor
   (atomica, con otro helper) y lo unico roto sea la cadena que el contrato mira. Si es asi, lo que
   hay que arreglar es el CONTRATO, no la implementacion, y quiero que lo digas con esas palabras.
2. **Si el contrato deberia seguir existiendo en esa forma.** Ata NUEVE SUBCADENAS LITERALES del
   harness. Es la cuarta vez que un refactor legitimo lo rompe -- 0316, 0319, 0321 y ahora 0331 --
   y es exactamente el patron del borrador DECISION-0105 que tambien te he mandado a revisar.
3. **Si hay algo mas de la entrega que ningun gate de su verification_cmd mira.** El
   `verification_cmd` de 0331 NO incluye este runner, y `check_falsification_contracts.py` sale
   verde porque comprueba DECLARACION, no ejecucion. Por eso la entrega pudo declararse verde con
   esto roto. Busca si hay mas huecos de ese tipo.

## Nota


Cuarta vuelta, y como en las anteriores cada una cerro algo real y encontro algo real. Si al cerrar
esta aparece un estado vecino, dimelo y particiono: ya tengo TASK-0337 contratada para el guard de
residuo, que es este mismo defecto de scope en la funcion de al lado, y no la ruteo hasta que 0331
cierre.

requested_action: Re-juzgar TASK-0331 en clon limpio sobre el commit exacto, medir la reachability
real del estado unknown en operacion normal, contar cuantas de las 24 celdas ejerce de verdad el
contrato, falsar los cuatro mutantes, comprobar que el conjunto de exenciones de neutralidad no
cambio al re-fijarse, verificar que no se movio lo ya probado, y emitir OK-CLOSABLE o
CHANGES-REQUIRED.

question: El estado unknown -- que exige intervencion del operador -- se alcanza en operacion normal
o solo bajo corrupcion que no se da sola? Es decir, hemos hecho visible un atasco raro o hemos
cambiado la recuperacion automatica por una llamada al operador en el caso comun?
