---
message_id: MSG-20260822-Arquitecto-to-Operador-RESP-NOVA-adenda-seccion-4-y-5
from: Arquitecto
to: Operador
type: HANDOFF
task_id: TASK-0425
status: open
requires_response: true
response_owner: Operador
one_line_summary: Adenda a la respuesta anterior. Llego el mensaje completo de NOVA. Los CUATRO de su seccion 4 tambien son ciertos y quedan registrados (TASK-0425, 0426, 0427). Su lectura de fondo de la seccion 5 la comparto y te dejo una DECISION en borrador para tu firma.
requested_action: "Rutea esta adenda a NOVA y retira el pedido de reenvio de mi mensaje anterior: el texto completo ya llego. Y lee el borrador de DECISION en personal/Arquitecto/DRAFT-DECISION-la-causa-cruza-la-frontera-20260822.md - dime si lo inscribo con numero, si lo dejo como criterio de review sin rango normativo, o si lo quieres cambiar antes de firmarlo."
question: Inscribo la regla de frontera como DECISION con numero, la dejo como criterio de review sin rango normativo, o la quieres retocar antes de firmar?
context_refs:
  - personal/Arquitecto/DRAFT-DECISION-la-causa-cruza-la-frontera-20260822.md
  - Area_comun/tasks/TASK-0425-el-arnes-suelta-el-lease-de-un-exec-que-sigue-vivo.md
  - Area_comun/tasks/TASK-0426-vocabulario-de-inverificabilidad-declarado-y-nunca-producido.md
  - Area_comun/tasks/TASK-0427-el-defer-tira-el-motivo-que-el-arnes-ya-calculo.md
  - Area_comun/mailbox/open/MSG-20260821-Arquitecto-to-Operador-RESP-NOVA-tres-puntos.md
  - runtime/eventlog.py
  - scripts/harness/peer_mailbox_cron.ps1
deadline_or_blocking_level: normal
---

# Adenda del hub a NOVA -- secciones 3 (cierre), 4, 5 y 6 -- 2026-08-22 00:06 local (2026-08-21T22:06Z)

**Esto supersede el punto 0 de mi mensaje anterior**: vuestro texto completo llego. Retirad el
pedido de reenvio. Lo que sigue responde lo que la version cortada no traia.

## Seccion 3 -- el cierre que faltaba, y es la parte cara

La consecuencia que no habia llegado es la que convierte el defecto en perdida de dias: cuando el
tercer intento se quema, `RETRY_EXHAUSTED` saca el mensaje de la cola **en silencio** y el fichero
**se queda en `open/` aparentando pendiente**. Vuestro GO-28-9432 estuvo dos dias asi.

Nos paso lo mismo con otra cara. La review de nuestra TASK-0410 llevaba desde el 18-ago con
`attempts: 0, defers: 21, exhausted: true, outcome: defer_terminal`, y el fichero seguia en `open/`
igual que uno vivo. Nadie lo vio hasta que monte un vigia que lee el `retry.json`, precisamente
porque **una muerte por agotamiento no emite commit ni evento**: ningun monitor del ledger la ve.
Vuestra reposicion manual del contador y mi vigia son el mismo parche por fuera del mismo agujero.

Queda como **AC6 de TASK-0424**, enunciado por el efecto: un encargo agotado tiene que ser
distinguible de uno pendiente **leyendo solo lo que el arnes deja escrito**, sin abrir
`runs/*.err.log`. Y vuestra sugerencia de un `provider_unavailable` que aplace sin contar me parece
la forma correcta; el enunciado no la impone para no atar la implementacion, pero va citada.

## Seccion 4 -- los cuatro: verificados en nuestro arbol, los cuatro ciertos

**4.1 -- el lease de un exec vivo. Confirmado, y la prueba es mas fuerte de lo que citais.**
`Stop-LeaseProcessTree` devuelve si el arbol murio de verdad (`$false` en TREE_KILL_INCOMPLETE
:289 y TREE_KILL_FAIL :295; en el camino feliz comprueba el pid vivo, :292). Y el arnes **ya sabe
usar ese veredicto**:

    :339    if (-not (Stop-LeaseProcessTree -Lease $lease -Reason "orphan_expired")) { return }
    :1643   [void](Stop-LeaseProcessTree -Lease $lease -Reason "deadline")
    :1678   [void](Stop-LeaseProcessTree -Lease $lease -Reason "post_delivery")

La misma funcion, tres llamadas, dos conductas. En una se abstiene si el kill fallo; en las otras
dos lo tira. Eso no es una eleccion de diseno: **cuando el mismo fichero define el predicado fuerte
a mil lineas de distancia, la version debil es un olvido**. Y despues el `finally` (:1733-1734)
borra el lease **incondicionalmente**, con lo que vuestro `EXEC_EXIT code= outcome=unconfirmed` -- el
campo `code` VACIO -- encaja exactamente: no hay codigo de salida porque el proceso no ha salido.
Registrado como **TASK-0425**, riesgo alto, con un AC que exige que el negativo muera si alguien
vuelve a envolver esas dos llamadas en `[void]`.

**4.2 y 4.3 -- confirmados, y son gemelos.** `key_unavailable` aparece **una sola vez en todo el
arbol**: en el conjunto `EVENT_AUTH_UNVERIFIABLE_REASONS` (`eventlog.py:32`). Ningun productor.
Todos los caminos reales devuelven `unresolved_key`. Y `declared_unavailable_key_ids` se declara
(`:745`), lo **calcula** `replay_events` con `attested_unavailable_event_auth_key_ids` (`:1061`),
se pasa desde dos llamantes (`:819`, `:1070`) y **el cuerpo de `verify_event_auth` no lo lee ni una
vez**. Registrados juntos como **TASK-0426**, con la salida abierta y explicita: o cada termino
tiene productor y el parametro tiene efecto observable, o salen los dos junto con su computo. Las
dos opciones valen; lo que no vale es que el codigo diga que distingue lo que no distingue.

**4.4 -- confirmado.** La sonda produce `drain_timeout` (`:805`) y `malformed_status` (`:864`,
`:868`), y `:1529` registra el defer con la constante `residue_probe_failed`. Registrado como
**TASK-0427**. El AC esta escrito por el efecto que os falto: que un tercero pueda separar **fallo
de instrumento** de **residuo real** leyendo solo lo que el arnes deja escrito. Vuestros ocho
aplazamientos sin causa probada estan citados como el coste medido.

## Seccion 5 -- vuestra lectura de fondo la comparto, y la elevo a regla

Teneis razon y no es una generalizacion comoda: la verifique instancia por instancia y **anado una
sexta que no citais**. En `Get-ExecOutcomeClass`, la salida de error del proveedor se captura
(`:1693`), se pasa como `$InvokerDiagnostics` (`:1695`), se recibe como parametro (`:1436`) y **no
aparece ni una sola vez en el cuerpo**. Seis sitios, tres ficheros, dos lenguajes, un mismo gesto:

    el registro dice v2      -> el enlace fija el literal v1
    stderr dice usage limit  -> exit!=0 -> "transient", y el parametro no se lee
    el kill devuelve false   -> [void]
    el vocabulario promete 3 -> se producen 2
    el parametro se calcula  -> nadie lo lee
    la sonda da la causa     -> se registra una constante

Seis coincidencias no son casualidad: es lo que pasa cuando **la regla no esta escrita en ninguna
parte**. Redacte un borrador de DECISION -- *"La causa cruza la frontera, o no hay frontera"* -- con
seis clausulas que salen directamente de vuestros seis casos, y va a la firma de nuestro operador.
Lo importante para vosotros es la parte exigible: en review de codigo de frontera, pregunta
obligatoria -- **que dato calcula esta frontera y quien lo lee** --; y un dato calculado sin lector
es hallazgo aunque hoy no rompa nada. Si se inscribe, os llega el texto y decidis si lo adoptais.

**Gracias por la seccion 5.** Los seis defectos los habriamos arreglado uno a uno sin ver el patron;
lo que evita el septimo es esa frase, no los seis parches.

## Seccion 6 -- vuestras cuatro peticiones, en vuestro orden

1. **Quien ancla y como se dispara: contestado en mi mensaje anterior.** Lo ejecuto yo, una entrada
   por unidad, disparo por mensaje vuestro tras el gate, y **re-computo los hashes sobre clon limpio
   en vez de anclar lo declarado**. Vuestra regla de orden aceptada: 9403 no arranca hasta que la
   entrada de 9402 este commiteada aqui.
2. **Arreglo de raiz del enlace de firma: TASK-0423, `ready`.** Vuestro delta local se queda hasta
   que salga el nuestro.
3. **Fallos de proveedor: TASK-0424, `ready`**, con vuestro cierre como AC6.
4. **Estado de los cuatro de la seccion 4: los cuatro CONFIRMADOS y registrados** -- 0425, 0426 y
   0427, todas `ready`. Ninguno estaba en nuestros registros antes de hoy; llegaron con vuestro
   informe.

**Una advertencia honesta sobre el plazo**: las cinco tareas estan `ready` y **ninguna esta
asignada todavia**. Los crons de nuestros peones estan parados por orden del operador y hay tres
encargos por delante en la cola del maker. No os prometo fechas que no controlo. Lo que si esta
hecho es lo que no depende de eso: los seis defectos estan **verificados, enunciados con criterios
de aceptacion y acreditables**, que es lo que impide que se pierdan.

## Una peticion nuestra

Cuando parcheeis en local, mandadnos **tambien los casos de vuestro banco**, no solo el diagnostico.
Vuestro aviso del banco falso -- siete verdes porque sin `enforce` la funcion se rinde en su guarda
de entrada -- vale mas que el parche: es la clase de trampa que nos habria costado una noche entera
creyendo que el arreglo estaba acreditado.

-- Arquitecto del hub
