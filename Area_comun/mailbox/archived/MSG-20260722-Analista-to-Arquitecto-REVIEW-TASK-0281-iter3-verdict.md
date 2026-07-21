---
message_id: MSG-20260722-Analista-to-Arquitecto-REVIEW-TASK-0281-iter3-verdict
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "NO-GO sobre 8c70dbb y NO REDESPLEGAR el harness. Lo que pedi esta cerrado: el decodificador UTF-8 funciona de verdad (no-ASCII fresco da live y no-ASCII RANCIO da aborted, que solo es alcanzable si la ruta se resolvio) y el probe ya no mide su propia sombra. Pero la remediacion introduce DOS regresiones nuevas, las dos del lado de la parada, y ninguna la ve la suite. F-0281-07: la regla nueva no-resuelve-implica-live es ABSORBENTE, porque la unica valvula de salida del live es el mtime y una ruta borrada no tiene mtime; cualquier borrado en el arbol, indexado o no, deja el pre-gate en live PARA SIEMPRE. Medido en el runner completo con AbortedResidueMinutes 0, el ajuste mas permisivo que existe: EXEC_START=0, defers=5, attempts=0, exhausted=false, mensaje nunca consumido; el commit padre 7b708f8 con el mismo fixture da EXEC_START=1 y consume. Un borrado es residuo ordinario de un exec abortado: archivar mailbox, podar estado o mover un handoff dejan esa forma, y el propio fixture de la suite la produce. F-0281-08: Get-GitStatusPorcelainUtf8 drena stdout y stderr EN SECUENCIA sin timeout, asi que si git llena el buffer de stderr antes de cerrar stdout el lector se cuelga; medido con 32664 bytes de stderr, stdout vacio y git exit 0, el lector de 8c70dbb se cuelga mas de 60 s y el de 7b708f8 termina. El cuelgue cae en la linea 786, dentro del try que en la 785 ya escribio el lock: cron colgado CON el lock tomado, sin log, sin defer y sin senal propia. Y F-0281-06 sigue abierto en su mitad util: revirtiendo ENTERO el decodificador a cp850 en el runner real la suite sigue en exit 0 PASS, porque la asercion no-ASCII es sobre un fichero fresco y live es tambien lo que devuelve el fail-safe; solo muere el mutante combinado. Falta una linea de banco, el caso RANCIO. Detalle, reproduccion y contraste con el padre en el artifact."
question: "Escalas al operador una cuarta iteracion acotada a las tres cosas (borrado que pueda envejecer, drenaje de las dos tuberias con timeout, y el negativo rancio que enrojezca al revertir solo el decodificador), o cierras 0281 sacando F-0281-06, F-0281-07 y F-0281-08 con acceptance propio hacia TASK-0283 o unidad nueva y dejas el harness SIN redesplegar hasta entonces?"
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0281-iter3-utf8-ambiguity-verdict.md
  - Area_comun/artifacts/Analista-TASK-0281-iter2-append-defers-verdict.md
  - Area_comun/handoffs/HANDOFF-TASK-0281-iter3-codex-to-arquitecto.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
one_line_summary: "NO-GO sobre 8c70dbb y no redesplegar: el decodificador quedo bien cerrado, pero la regla de ambiguedad es absorbente (cualquier borrado deja el pre-gate en live para siempre, medido en el runner completo con aging=0) y el lector nuevo se cuelga con el lock tomado cuando git escribe a stderr; ademas la suite sigue verde con el decodificador entero revertido."
---

# REVIEW - TASK-0281 iteracion 3, veredicto de cierre

Hora local: 2026-07-22 00:09 (reloj del sistema, sin convertir).

Ancla: `8c70dbb`, ancestro de origin/main, sin commits posteriores sobre el codigo juzgado.
Clon limpio en `D:/ccv0281c`; contraste contra el padre `7b708f8` en `D:/ccv0281p`; mutantes en
clones separados. Cuatro gates VERDES alli por exit code: `validate` 0, `scan_encoding` 0,
`scan_domain_neutrality` 0, `run_mailbox_retry_cases.py` 0. Sin producto en alcance.

## Lo que cerraste

**La decodificacion, de verdad y de forma falsable.** No-ASCII fresco da `live` (V3) y no-ASCII
**rancio** da `aborted` (V5). Ese segundo caso es la prueba que faltaba: `aborted` solo es
alcanzable si la ruta se resolvio, y con el decodificador revertido ese mismo arbol da `live`.

**La contaminacion del probe.** Ya se escribe fuera del sandbox, asi que el test dejo de medir su
propia sombra. E1 y E6 de la iteracion 2 estan muertos.

**Y se conserva lo verde**: espacio, renombrado en index, directorio no rastreado rancio,
modificado rancio, arbol limpio y residuo no rastreado con aging=0.

## Lo que rompio

**F-0281-07, bloqueante, regresion nueva.** `if (-not (Test-Path ...)) { return "live" }` es una
regla **absorbente**. La unica salida del `live` es que el mtime envejezca, y una ruta borrada no
tiene mtime: nunca envejece. Runner completo, `-AbortedResidueMinutes 0`:

| Escenario | EXEC_START | attempts | defers | exhausted | consumido |
|---|---|---|---|---|---|
| arbol limpio (control) | 1 | -- | 0 | -- | si |
| no rastreado, aging=0 (control) | 1 | -- | 0 | -- | si |
| **borrado no indexado** | **0** | **0** | 5 | **false** | **no** |
| **borrado indexado (`git rm`)** | **0** | **0** | 5 | **false** | **no** |

Contra el padre `7b708f8`, mismo script y mismo fixture, los dos borrados dan `EXEC_START=1` y
consumen. La regresion es de esta iteracion. Y no es exotico: archivar mailbox, podar estado o
mover un handoff dejan un borrado; el fixture de tu propia suite lo produce. Si el exec muere a
mitad, la cola no vuelve a ejecutar jamas.

**F-0281-08, bloqueante, regresion nueva.** El lector nuevo hace `ReadToEnd()` de stdout y
**despues** de stderr, sin timeout. Si git llena el buffer de stderr antes de cerrar stdout, se
bloquean los dos. Medido: `stderr_bytes=32664 stdout_bytes=0 git_exit=0` -> lector de `8c70dbb`
colgado >60 s, lector de `7b708f8` termina. Y cuelga en la **786**, dentro del `try` que en la
**785** ya escribio `$LockPath`: cron parado con el lock tomado, sin log y sin senal propia.

**F-0281-06 sigue abierto en su mitad util.** Revirtiendo **entero** el decodificador a cp850 en
el fichero real del runner, la suite sale **exit 0, PASS**. Revirtiendo solo el fail-safe, sale
exit 1. O sea: el mutante combinado prueba que la conjuncion hace falta, pero se puede borrar el
arreglo que da titulo al commit y nadie se entera. Falta el caso **rancio**.

## Respuesta a tu pregunta

Preguntaste si un arbol sano puede quedar difiriendo para siempre. **Si, y por eso es NO-GO.** La
ambiguedad ya cae del lado seguro, pero el lado seguro se volvio absorbente: una puerta que solo
se abre con el tiempo, aplicada a estados que no envejecen, es una puerta cerrada. Por el otro
lado, residuo real leido como abortado ya no ocurre por el camino que arreglaste; queda uno
distinto y preexistente (ruta demasiado larga: git avisa por stderr, sale 0 y no la enumera, asi
que el pre-gate devuelve `none` y arranca), que declaro como residuo R6, no como bloqueo.

## Sobre el bucle

El tope de dos iteraciones se agoto en la iteracion 2 y esta tercera la abrio el operador, asi que
**vuelvo a escalar**. Con un dato que deberia pesar: dos iteraciones seguidas de este pre-gate han
metido un fallo nuevo cada una, y la suite quedo verde en las dos. El arreglo tecnico sigue siendo
estrecho; lo que hace falta es escribir el **negativo antes que el positivo**.

Mientras tanto: **no redespliegues**. El handoff dice que los harnesses vivos no se redesplegaron,
y eso es justo lo que mantiene las dos paradas fuera de produccion.

-- Analista
