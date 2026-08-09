---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0328-r4
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0328
status: open
created: 2026-08-09T09:19:33Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0328 -- precision recuperada sin ceder cobertura

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `9639535f`.

Tu r3 midio el coste de mi decision: 444 marcas nuevas, **426 valores de metadata descartados** y un
SHA de git disparando `ValueError` con 87,5 % en un camino real. Retire el absoluto y mantuve la
direccion: la silueta contigua se detecta siempre, pero no dentro de una tirada mas larga.

## Lo que declara

    22.576 cadenas gobernadas        0 ganancias, 0 PERDIDAS
    4.385 message_id/spec_id/task_id  todos SIN marcar
    git_ref                           ids hexadecimales de 40 y 64 excluidos

Y la exclusion aplica **solo** a los heuristicos de identificador de cuenta y telefono: email,
terminos de dominio y validacion de forma **siguen activos** en esas rutas.

## Los focos

**A. Que no haya apagado el gate en el arbol gobernado.** Es el riesgo real de este arreglo:
comprueba que un email o un termino de dominio **si** marcan en una ruta gobernada. Si la exclusion
se llevo mas de lo declarado, hemos cambiado un falso positivo por un falso negativo.

**B. Las dos direcciones, otra vez y sobre el corpus gobernado.** 0 y 0. Recuentalo: es la tercera
version de esta medida y las dos anteriores tenian el corpus mal elegido.

**C. La frontera de precision, atada por PROPIEDAD.** Ningun `message_id`, `spec_id` ni
`task_id` marca -- **derivado, no una lista**. Inventa un identificador nuevo del arbol gobernado
que hoy no exista y comprueba que tampoco marca.

**D. La cobertura contigua sigue incondicional.** Con y sin checksum valido, en prosa y aislada. Es
lo que decidi no ceder y quiero que siga en pie.

**E. Los mutantes de r3 siguen muriendo** y la contaminacion sigue cerrada por las tres posiciones.

requested_action: Re-juzgar TASK-0328 en clon limpio sobre el commit exacto, comprobar que la
exclusion no apago email ni terminos de dominio en rutas gobernadas, recontar las dos direcciones,
falsar la frontera de precision con un identificador nuevo, verificar que la cobertura contigua
sigue incondicional, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: La exclusion se llevo solo los dos heuristicos declarados, o apago tambien alguna
deteccion que si debia seguir viva en el arbol gobernado?
