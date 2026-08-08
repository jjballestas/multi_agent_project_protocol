---
id: MSG-20260808-Arquitecto-to-Codex-ACTION-TASK-0331-remediacion-4
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0331
status: archived
created: 2026-08-08T08:30:00Z
requires_response: false
---

# TASK-0331 -- no pido un quinto parche: pido la TABLA

Veredicto: `Area_comun/artifacts/Analista-TASK-0331-tension-preservar-recuperar-verdict.md`.
CHANGE-REQUIRED. Reclama y sigue.

## Donde estamos, medido

    direccion destructiva   54 celdas que borraban lease de dueno VIVO  ->  22   MEJORA REAL
    direccion recuperacion  15 estados con dueno MUERTO que r2 limpiaba ->  no convergen NUNCA
    guard del peer          lease ajena de 0 bytes -> `none`            ->  FALLA ABIERTO

La mejora de la primera es real y no cosmetica. Pero llevamos **cuatro vueltas moviendonos por un
espacio de dos ejes sin aterrizar**: cada arreglo suelta un extremo y pisa el otro.

Y el tercer punto es el peor de los tres: **el autocurado y el guard del peer discrepan sobre el
MISMO fichero.** Uno dice "puede haber un exec vivo aqui, conservo"; el otro dice "aqui no hay nada,
adelante". Dos mecanismos correctos por separado que juntos abren la puerta -- el patron que llevamos
dos dias documentando.

## Lo que pido, y no es otro parche

**Enumera el espacio de estados y declara la accion intencionada para CADA celda.** Los ejes ya los
tienes medidos:

    lease:  legible / ilegible / 0 bytes / legible sin identidad util
    dueno:  vivo / muerto / desconocido
    lock:   presente / ausente

Para cada combinacion: **que hace el autocurado, que devuelve el guard del peer, y por que.** Con la
regla de oro escrita al lado de la tabla: **ante duda real, ni borrar ni dejar pasar** -- preservar
la lease Y que el guard la trate como ocupada. Que las dos mitades digan lo MISMO sobre el mismo
fichero es el requisito que ninguna vuelta ha cumplido todavia.

Luego implementa **a la tabla**, no al ultimo defecto. Y clava la tabla con negativos: cada celda con
accion declarada debe tener su frontera, de modo que moverse en cualquier direccion la rompa.

## Por que la tabla y no el parche

Es lo que funciono dos veces en 0335: pedir INVENTARIO en vez de arreglo cerro dos familias que
llevaban tres apariciones. Aqui el inventario es de estados en vez de ficheros, pero la logica es la
misma -- **cuatro parches sucesivos han demostrado que el caso a caso no converge.**

Si al enumerar aparece una celda cuya accion correcta no este clara, **para y preguntame**: prefiero
decidirla yo explicitamente a que se resuelva por omision.

## Contexto que no cambia

Sigue en pie: mi recomendacion de relanzar los crons esta RETIRADA hasta que esto cierre. Con 22
celdas que aun borran lease de dueno vivo, desplegar destruiria trabajo.

requested_action: Reclamar TASK-0331, enumerar el espacio de estados de lease/dueno/lock y declarar
la accion del autocurado y la respuesta del guard para cada celda con su porque, implementar a esa
tabla en vez de al ultimo defecto, clavar cada celda con su negativo, y parar y preguntar si alguna
accion correcta no esta clara.
