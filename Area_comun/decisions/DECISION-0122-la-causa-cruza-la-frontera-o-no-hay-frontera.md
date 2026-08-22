---
id: DECISION-0122
title: La causa cruza la frontera, o no hay frontera
status: accepted
date: 2026-08-22
proposer: Arquitecto
approver: operador humano
supersedes: none
related: [DECISION-0018, DECISION-0033, DECISION-0115]
scope: nucleo neutral (runtime/, scripts/) y capa operacional del arnes
---

# DECISION-0122 -- La causa cruza la frontera, o no hay frontera

## Contexto

El 2026-08-21 la instancia NOVA reporto seis defectos del codigo de este hub y anadio una lectura:
que no son seis defectos sueltos sino **uno**. Verifique cada instancia leyendo el arbol -- no
aceptandola del informe -- y la lectura se sostiene. Anadi una septima que encontre yo y ellos una
octava mirandose a si mismos.

En todas, el sistema **tiene el dato correcto en el punto exacto de la decision y lo pierde**: lo
descarta, lo sustituye por un literal, lo aplana, o lo deja bajo un nombre que ya significa otra
cosa.

    1  submit_intent.py:1089/1095  el registro de claves dice v2 -> el enlace fija el literal v1
    2  peer_mailbox_cron.ps1:1441  stderr dice "usage limit" -> exit!=0 -> "transient";
                                   $InvokerDiagnostics se captura, se pasa, se recibe y NO se lee
    3  peer_mailbox_cron.ps1:1643  Stop-LeaseProcessTree devuelve si el kill funciono -> [void]
                        y :1678    ...mientras :339, en el mismo fichero, SI lo honra
    4  eventlog.py:32              key_unavailable declarado en el vocabulario; ningun productor
    5  eventlog.py:745/1061        declared_unavailable_key_ids se calcula, viaja, nadie lo lee
    6  peer_mailbox_cron.ps1:1529  la sonda produce drain_timeout / malformed_status; el defer
                                   registra la constante "residue_probe_failed"
    7  (instancia NOVA)            el sello nombra 3 eventos de instrumentacion: dos no tienen
                                   emisor en ninguna parte, y el tercero -- cost.attributed --
                                   tiene el nombre ocupado por DECISION-0033: otro esquema, otras
                                   dimensiones, y ademas apagado

Siete sitios, cuatro ficheros, dos lenguajes, dos instancias. Eso ya no es casualidad estadistica:
es lo que ocurre cuando la regla no esta escrita en ninguna parte.

## Decision

**Una frontera que clasifica esta obligada a propagar el dato que la discrimina.** En concreto:

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
7. **Un nombre significa UNA cosa dentro de una instancia.** Si una capacidad nueva necesita un
   nombre que ya esta ocupado por otro esquema, toma otro nombre o la colision se resuelve de forma
   explicita y registrada. **Un nombre con dos significados es peor que un nombre ausente**: la
   ausencia se ve, la homonimia hace creer que la capacidad existe. Corolario operativo: **encender
   un emisor homonimo para "cumplir" es peor que no emitir**, porque deja el ledger con aspecto de
   instrumentado sin estarlo.

## Como se hace exigible

- **En review:** ante codigo de frontera, una pregunta obligatoria -- *que dato calcula esta
  frontera, y quien lo lee*. Un dato calculado sin lector es un hallazgo, aunque nada falle hoy.
  Y ante un nombre de evento, motivo o estado: *este nombre significa ya otra cosa en algun sitio*.
- **En la acreditacion:** cada arreglo de esta familia se prueba perturbando la **produccion**, no
  el runner, y con el par completo -- la rama degradada debe morder Y la rama sana debe seguir
  pasando (DECISION-0115). Un negativo que solo ejercita el camino feliz no acredita nada.
- **Discriminador barato, medido en campo:** si el MISMO fichero honra un veredicto en una llamada
  y lo envuelve en `[void]` en otra, es omision y no diseno. Es la forma mas rapida de separar un
  olvido de una decision.
- **Alcance:** aplica al nucleo neutral (`runtime/`, `scripts/`) y a la capa operacional del arnes.
  No introduce ningun termino de dominio y no cambia ninguna frontera de gobierno.

## Tareas que la instancian

    TASK-0423   el enlace de firma contra el registro de claves           (clausulas 1, 4)
    TASK-0424   los fallos de proveedor no son fallos de la tarea         (clausulas 1, 5)
    TASK-0425   el lease de un exec vivo no se suelta                     (clausulas 4, 6)
    TASK-0426   vocabulario declarado y parametro muerto                  (clausulas 2, 3)
    TASK-0427   el motivo de la sonda sobrevive al defer                  (clausulas 1, 5)

La septima instancia vive en la instancia NOVA y su tratamiento es de su trio, no de este. Se cita
aqui porque es la que motiva la clausula 7.

## Lo que esta decision NO hace

No ordena reescribir el arnes, no exige un refactor transversal y no bloquea trabajo en curso. Las
cinco tareas van por su via normal, con maker y checker distintos. Lo unico que anade es una regla
que permite **cazar la octava instancia antes de que cueste una noche**, y un criterio de review que
hasta hoy no estaba escrito en ninguna parte.

## Procedencia

El patron lo enuncio el Arquitecto de la instancia NOVA en la seccion 5 de su informe del
2026-08-21T21:30Z, y la clausula 7 sale de su hallazgo del 2026-08-22 sobre su propio runtime. Este
hub verifico las seis primeras instancias en su arbol y aporto la segunda mitad de la instancia 2
(`$InvokerDiagnostics`). Se registra la procedencia porque la regla vale mas que los parches y
porque la encontro quien la sufrio.
