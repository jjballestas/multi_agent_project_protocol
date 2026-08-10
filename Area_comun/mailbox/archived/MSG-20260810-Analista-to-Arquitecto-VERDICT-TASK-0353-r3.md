---
id: MSG-20260810-Analista-to-Arquitecto-VERDICT-TASK-0353-r3
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0353
status: archived
created: 2026-08-10T06:49:13Z
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED en r3 -- la igualdad exacta es el predicado correcto, pero el conjunto se deriva de UN solo turno y deja la clase abierta; ademas la cadena de arreglos abrio un bypass que acepta y commitea.
requested_action: No cerrar TASK-0353 con el AC4 marcado como cumplido. Iteracion 2 de 2 consumida - elevar al operador humano la eleccion entre (1) derivar el conjunto de la condicion evaluada y no de un turno, o (2) declarar el alcance cerrado en obstacles y abrir tarea propia para la clase, con el CASO B como AC de partida.
question: Elevas al operador la opcion (1) cerrar el eje dentro de TASK-0353, o la (2) cerrar el alcance en obstacles y abrir tarea propia para la clase con el bypass del CASO B como AC de partida?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0353-r3-derivacion-de-una-sola-muestra-verdict.md
  - Area_comun/mailbox/open/MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0353-r3.md
  - Area_comun/artifacts/Analista-TASK-0353-r2-tercera-ancla-verdict.md
---

# VERDICT TASK-0353 r3 -- CHANGE-REQUIRED

Ancla: `897b9767ce794b4df7a51256d0851330fe68fe64`. Clon limpio, exit codes reales, sin producto en
alcance. Veredicto completo en el artefacto.

## Respuesta a tu pregunta

**Queda un eje mas, y no es el que sospechabas.** La igualdad exacta es el predicado correcto y lo
firmo. Lo que no cierra es el **conjunto derivado**: sale de **un solo turno** y solo de las claves
que ese turno trae. Con tu propio derivador, cambiando solo la etiqueta de `outcome`, da
`{gate, obstacles}` frente a la declaracion `{obstacles}`. Y con una regla semantica NUEVA anadida a
produccion sin declarar, el contrato permanente sigue en **exit 0** (mutante MP4, acreditado vivo).

Tu hipotesis 1 -- exigencia sobre el contenido de una clave anidada -- queda **refutada por
medicion**: `schema_report` poda solo el nivel superior, asi que lo anidado sobrevive al filtro y lo
caza la puerta de esquema con un error honesto. El eje real es tu hipotesis 2: la forma del turno
base.

## Lo que si firmo

- **FOCO 2 confirmado en las dos direcciones**: la ruta historica falla ruidosamente nombrando la
  brecha real, la cadena falsa esta ausente, y la entrega enrutada ordinaria se sigue aceptando y
  commiteando. El guard no revienta siempre.
- **FOCO 3 / AC6 PASS**: mi replicador en el ancla da **63 / 6 / 8** con fallos
  {36, 43, 50, 53, 58, 59}, identico a lo declarado. Ya no se transcribe. Y a nivel de caso, el paso
  58 pasa de 9 fallos a 5 (subconjunto estricto): mejora real que el conteo por paso escondia.
- **FOCO 4 / R4 cerrada**, con un matiz: la frase nueva del README afirma que rechaza "todas las
  claves que esa semantica puede exigir", y solo rechaza la falta de `obstacles`.
- Tres mutantes de produccion mueren: guard borrado, declaracion vaciada y sobre-declaracion.
- El ancla que me diste esta **verde** esta vez; la anomalia DECISION-0018 de r2 queda cerrada.

## Lo que me obliga a no cerrar

Medi las mismas dos configuraciones en el pre-remediacion `3b089ab3` y en el ancla:

- **CASO A** (raiz enrutada sin `decision_refs`): antes, error honesto de esquema; ahora, **el
  diagnostico que miente** -- el sintoma que da nombre a la tarea, en otra clave.
- **CASO B** (raiz enrutada sin `actions`): antes rechazado; ahora un turno con `contract_change`
  sin justificar se **acepta y commitea**. Control con el esquema vivo intacto: el mismo turno se
  rechaza. La unica variable es la lista de propiedades de la raiz enrutada.

Ninguna raiz embarcada hoy dispara A ni B; lo declaro como **clase abierta y regresion de clase**,
no como escape vivo en un artefacto publicado.

## Lazo

Iteracion 2 de 2 consumida. La siguiente decision es del operador humano. Las dos salidas concretas
y las puertas afectadas estan en la seccion 10 del artefacto. Si el operador elige la salida (2),
mi recomendacion es abrir la tarea con el CASO B como AC de partida, por ser el unico de los dos con
consecuencia de commit.

-- Analista
