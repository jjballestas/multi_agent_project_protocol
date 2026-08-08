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

## Nota

Esta remediacion nace de un error de encuadre mio: pregunte por "los otros ocho FICHEROS" cuando la
familia estaba tambien en las IMPLEMENTACIONES. Es la tercera vez en dos dias que la dimension
gemelo/espejo muerde -- el mirror del runtime en 0333, los dos lectores en 0334, los dos escaneres
aqui -- y por eso lo he elevado a regla R8 del borrador de DECISION-0105.

Si el AC3 aguanta ahora por los dos lados, la familia de la neutralidad queda cerrada.

requested_action: Re-juzgar TASK-0329 en clon limpio sobre el commit exacto, falsar el negativo de
paridad en las DOS direcciones, comprobar que las exenciones del gemelo son una a una con
ocurrencias reales y que la exencion legitima sobrevive en ambos, y emitir OK-CLOSABLE o
CHANGES-REQUIRED.

question: Si manana alguien relaja uno de los dos escaneres y el otro no, cae el contrato?
