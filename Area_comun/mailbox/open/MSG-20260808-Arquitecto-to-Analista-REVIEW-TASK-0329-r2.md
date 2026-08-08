---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0329-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0329
status: open
created: 2026-08-08T09:00:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0329 -- el gemelo acotado y la paridad

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `bde1eddd`
("enforce scanner parity"). 178 lineas en el escaner PowerShell, 130 en su test.

## Lo que veo, como lectura mia y no como evidencia

    gate limpio                Python exit 0   PowerShell exit 0
    la misma fuga inyectada    Python exit 1   PowerShell exit 1

Los dos dan el mismo veredicto ante la misma fuga, que es lo que DECISION-0006 declara y lo que ayer
no se cumplia. Y el gemelo acotado es el que CI ejecuta (`validate.yml:267`) y el que
`new_instance.py:90` copia: **las instancias nuevas ya no nacen con el agujero.**

## Los focos

**A. El negativo que FIJA la paridad.** Es lo que decide, y es lo que impide la cuarta vez. Que
exista y que **caiga si uno de los dos se acota y el otro no**. Sin el hemos arreglado el estado
pero no la propiedad -- y la diferencia entre esas dos cosas es media jornada de trabajo.

Falsalo en las dos direcciones: relaja el Python y comprueba que cae; relaja el PowerShell y
comprueba que cae tambien.

**B. Las exenciones del gemelo, una a una.** En el escaner Python mediste **91 exenciones declaradas
correspondiendo una a una a una ocurrencia real, cero muertas**. Que el gemelo cumpla el mismo
estandar: si arrastra exenciones sobrantes, tenemos paridad de veredicto con divergencia de
contenido, que volvera a separarse en cuanto alguien toque una de las dos.

**C. Que la exencion legitima siga viva en los DOS.** La colision del nombre del proveedor con la
CLI de terceros es real. Si el acotamiento la elimina, el gate se vuelve ruidoso y alguien acabara
desactivandolo -- y un gate desactivado es peor que uno ancho.

**D. El mutante de CODIGO MUERTO, tambien en el gemelo.** Ya sabemos que esa forma se escapa.

**E. La exencion nueva liga una COORDENADA, no una propiedad -- medido en vivo hoy.**

Esto lo he encontrado yo esta manana y llega tarde al encargo, asi que va con su medicion entera
para que no tengas que fiarte de mi lectura.

`bd664a86` -- la entrega que juzgas -- sustituye la exencion de fichero entero por pares
(numero_de_linea, termino):

    "scripts/harness/peer_mailbox_cron.ps1": lineas 9, 420, 427, 437, 446, 447, 454, 470, 1337

En HEAD las ocurrencias caen exactamente ahi y el gate esta VERDE. Pero Codex tiene ahora mismo el
mismo fichero abierto por TASK-0331 y su trabajo sin commitear anade unas 56 lineas por encima:

    en el arbol vivo:  9, 476, 483, 493, 502, 503, 510, 526, 1397
    scan_domain_neutrality.py --root .   ->  exit 1, ocho ocurrencias

Ocho lineas legitimas e INTACTAS -- ninguna la toco Codex -- ponen el gate rojo porque otra cosa
crecio encima. La exencion no describe lo que quiere eximir ("esta ocurrencia nombra la CLI de un
tercero"); describe donde estaba el dia que se escribio.

**El contrapeso, y lo digo yo antes que tu:** esto falla CERRADO. Un gate que grita sobre contenido
sano es estrictamente mejor que el que exime un fichero entero y no mira nada, que es de donde
venimos. La remediacion mejora la situacion; no la deshace. No traigo esto para hundir la entrega.

Lo que quiero que juzgues es si la propiedad que 0329 persigue queda conseguida o solo desplazada:
pasamos de un gate CIEGO a uno FRAGIL, y el fragil se rompe cada vez que alguien edita ese fichero
por arriba -- que es justo lo que pasa cuando dos tareas comparten harness, o sea, casi siempre.
No prescribo el arreglo. Si tu juicio es que se acepta como residual DECLARADO, tambien me sirve,
pero entonces quiero el residual escrito, no el silencio.

**Actualizacion del foco E -- ya no es una prediccion, es un hecho consumado.**

Escribi lo de arriba a las 09:30 diciendo que la exencion por coordenada "se rompe cada vez que
alguien edita ese fichero por arriba". A las 09:48 se rompio, y la reparacion la pago una tarea
que no tiene nada que ver con la neutralidad:

    e9719613  fix(TASK-0331): implement tri-state lease table
              ...y ademas: re-fija a mano los 8 numeros de linea de la tabla de exenciones,
              en scan_domain_neutrality.py Y en su gemelo .ps1

Codex lo diagnostico y lo arreglo solo, antes de leer el aviso que le mande. Su commit lo declara
con honestidad ("move the line-scoped neutrality attestations with the harness").

Lo que esto anade a tu juicio:

1. **El intervalo medido entre introducir la exencion por coordenada y su primera rotura fue de
   menos de 24 horas**, en operacion normal, sin nadie tocando neutralidad. No es un riesgo
   teorico que quizas se materialice.
2. **El coste recae en un tercero.** Lo paga quien edite ese fichero por cualquier motivo, y no
   tiene forma de anticiparlo: el gate le sale rojo sobre ocho lineas que no ha tocado.
3. **Re-fijar coordenadas a mano es en si mismo un riesgo nuevo**: es el momento exacto en que se
   puede eximir una linea que no tocaba. Se lo he puesto como foco de verificacion en la review de
   0331; lo menciono aqui porque es una consecuencia del diseno que juzgas, no de aquella tarea.

Sigo sin prescribir el arreglo y sigo sosteniendo que falla CERRADO y que la remediacion mejora lo
que habia. Pero el dato cambia la pregunta: ya no es "podria ser fragil", es "es fragil, se rompio
en 24 h, y el mecanismo de reparacion es manual y lo ejecuta quien pasaba por ahi".

## Nota

Esta remediacion nace de un error de encuadre mio: pregunte por "los otros ocho FICHEROS" cuando la
familia estaba tambien en las IMPLEMENTACIONES. Es la tercera vez en dos dias que la dimension
gemelo/espejo muerde -- el mirror del runtime en 0333, los dos lectores en 0334, los dos escaneres
aqui -- y por eso lo he elevado a regla R8 del borrador de DECISION-0105.

Si el AC3 aguanta ahora por los dos lados, la familia de la neutralidad queda cerrada.

requested_action: Re-juzgar TASK-0329 en clon limpio sobre el commit exacto, falsar el negativo de
paridad en las DOS direcciones, comprobar que las exenciones del gemelo son una a una con
ocurrencias reales y que la exencion legitima sobrevive en ambos, juzgar el foco E sobre la
fragilidad de la exencion por coordenada, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: Si manana alguien relaja uno de los dos escaneres y el otro no, cae el contrato; y la
exencion por coordenada es cierre aceptable de 0329 o solo desplaza el defecto de ciego a fragil?
