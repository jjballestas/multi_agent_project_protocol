# BORRADOR DE DECISION -- "La causa cruza la frontera, o no hay frontera"

> **NO INSCRITA.** Borrador del Arquitecto del hub para firma del operador. Redactado 2026-08-22
> 00:0x local a partir de la seccion 5 del informe de la instancia NOVA (2026-08-21T21:30Z) y de
> seis instancias verificadas en el arbol de este hub.

## Contexto

La instancia NOVA reporto seis defectos y anadio una lectura: los seis son la misma familia. La
verifique instancia por instancia leyendo nuestro codigo, y la lectura se sostiene. En los seis, el
sistema **TIENE el dato correcto en el punto exacto de la decision y lo pierde**: lo descarta, lo
sustituye por un literal, o lo presenta como otra cosa.

    1. submit_intent.py:1089/1095   el registro de claves dice v2; el enlace fija el literal v1
    2. peer_mailbox_cron.ps1:1441   la salida de error del proveedor se captura, se pasa como
                                    $InvokerDiagnostics y no se lee: exit!=0 -> "transient"
    3. peer_mailbox_cron.ps1:1643   Stop-LeaseProcessTree devuelve si el kill funciono;
                     y :1678        dos llamantes lo envuelven en [void] -- y un tercero, :339,
                                    SI lo honra
    4. eventlog.py:32               key_unavailable declarado en el vocabulario; ningun productor
    5. eventlog.py:745/1061         declared_unavailable_key_ids se calcula, se transporta y el
                                    cuerpo no lo lee
    6. peer_mailbox_cron.ps1:1529   la sonda produce drain_timeout / malformed_status; el defer
                                    registra la constante "residue_probe_failed"

Seis sitios distintos, tres ficheros, dos lenguajes, y un mismo gesto. No es casualidad estadistica:
es lo que pasa cuando nadie ha escrito la regla.

## Decision propuesta

**En este protocolo, una frontera que clasifica esta obligada a propagar el dato que la
discrimina.** En concreto:

1. **No se colapsa una causa calculada en una constante.** Si el codigo computa un motivo, ese
   motivo llega hasta donde se decide o se diagnostica. Sustituirlo por una etiqueta generica en la
   ultima linea es perder la causa, no resumirla.
2. **Un vocabulario declarado es producible.** Si un conjunto enumera motivos o estados, cada
   termino tiene un productor real, o sale del conjunto. Un vocabulario que promete distinciones
   que el codigo no sabe hacer es documentacion falsa dentro del propio codigo.
3. **Un parametro que se calcula y se transporta, se consume.** Si no se consume, se elimina junto
   con su computo y su transporte. Un parametro muerto hace creer a quien lee la firma que el
   veredicto tiene en cuenta algo que no tiene en cuenta.
4. **El veredicto que una funcion devuelve se consume en TODAS sus llamadas.** Si una llamada lo
   ignora deliberadamente, lo dice en el codigo y explica por que. Cuando el mismo fichero honra el
   veredicto en un sitio y lo descarta en otro, la version debil es una omision, no una eleccion.
5. **"El instrumento no pudo decidir" NUNCA comparte etiqueta con "el estado es X".** Fallo de
   instrumento y estado adverso son diagnosticos opuestos y exigen etiquetas distintas: el primero
   se repara, el segundo se espera.
6. **Lo irresoluble no se resuelve inventando.** Un proceso que no ha terminado no tiene codigo de
   salida; un exec sin veredicto no autoriza a soltar su lease. Ante la ausencia de dato, se
   preserva la reserva y se declara la ausencia.

## Como se hace exigible

- **En review:** ante codigo de frontera, una pregunta obligatoria -- *que dato calcula esta
  frontera, y quien lo lee*. Un dato calculado sin lector es un hallazgo, aunque nada falle hoy.
- **En la acreditacion:** cada arreglo de esta familia se prueba perturbando la **produccion**, no
  el runner, y con el par completo: la rama degradada debe morder Y la rama sana debe seguir
  pasando. Un negativo que solo ejercita el camino feliz no acredita nada.
- **Alcance:** aplica al nucleo neutral (runtime/, scripts/) y a la capa operacional del arnes. No
  introduce ningun termino de dominio ni cambia ninguna frontera de gobierno.

## Tareas que la instancian (ya registradas, todas `ready`)

    TASK-0423   el enlace de firma contra el registro de claves        (regla 1, 4)
    TASK-0424   los fallos de proveedor no son fallos de la tarea      (regla 1, 5)
    TASK-0425   el lease de un exec vivo no se suelta                  (regla 4, 6)
    TASK-0426   vocabulario declarado y parametro muerto               (regla 2, 3)
    TASK-0427   el motivo de la sonda sobrevive al defer               (regla 1, 5)

## Lo que NO propone esta decision

No propone reescribir el arnes, ni un refactor transversal, ni bloquear trabajo en curso. Las cinco
tareas se hacen por su via normal, con maker y checker distintos. Lo unico que anade es **una regla
que permita cazar la sexta instancia antes de que cueste una noche**, y un criterio de review que
hoy no existe escrito en ninguna parte.

## Pendiente de decidir por el operador

1. Si se inscribe como DECISION del protocolo (con numero) o queda como criterio de review sin
   rango normativo.
2. Si la regla 4 (veredicto consumido en todas las llamadas) se convierte ademas en un chequeo
   mecanico -- hay pocas funciones que devuelvan veredicto y seria barato -- o se queda en review
   humana.
