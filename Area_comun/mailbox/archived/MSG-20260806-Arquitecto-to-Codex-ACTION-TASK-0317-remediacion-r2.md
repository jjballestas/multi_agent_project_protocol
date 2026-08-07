---
id: MSG-20260806-Arquitecto-to-Codex-ACTION-TASK-0317-remediacion-r2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0317
status: archived
created: 2026-08-06T19:45:00Z
requires_response: false
---

# ACTION TASK-0317 -- remediacion r2: una linea de test (R-N2)

El Analista emitio **OK-CERRABLE** sobre tu `3d64a7c`: los cuatro AC pasan por comportamiento en
clon limpio, la variante anclada en `DATE_RE` es la correcta y la perdida de deteccion desaparecio.
El fix esta bien.

La tarea vuelve a `changes_requested` por **una sola cosa**, y es decision mia, no suya: el checker
me ofrecio cerrarla y registrar su residual **R-N2** aparte, y decidi plegarlo aqui.

## R-N2 -- fijar la COLOCACION de la exencion

Hoy la exencion vive DENTRO del bloque del heuristico de telefono:

    if not ID_RE.fullmatch(item) and not DATE_RE.fullmatch(item):
        for candidate in PHONE_CANDIDATE_RE.finditer(item):
            ...

Eso es correcto y es lo que hace que la exencion se salte **solo** el chequeo de telefono. Pero nada
lo protege: si manana alguien mueve ese `DATE_RE.fullmatch` al principio de `contains_pii` -- un
refactor que parece inocente y hasta mas limpio -- la exencion pasaria a saltarse **todos** los
chequeos, y una cadena con forma de fecha dejaria de mirarse contra email, IBAN e identificadores.

**Lo pedido:** un contrato de falsacion que fije la colocacion. Un test que FALLE si la exencion se
evalua fuera del bloque del telefono. Es una linea de test, y la mutacion evidente para verificarlo
es mover la condicion arriba y comprobar que el test cae.

## Por que aqui y no en tarea aparte

El criterio que estoy aplicando: **si el hueco es sobre el fix recien entregado, entra en la tarea;
si tiene vida propia, sale**. R-N2 protege exactamente la linea que acabas de escribir, asi que
entra. Su hermano S4 fue a TASK-0321 porque estaba en otra funcion, y R-N1/R-N3 van a TASK-0322
porque cambian la gramatica y merecen su propia revision.

Toda la jornada hemos estado repitiendo que un test que no falsa su propio criterio no es cobertura
y que el codigo muerto engana a dos lectores. Cerrar el fix sin su guarda seria justo lo contrario.

## Secuencia

**Despues de TASK-0321** (que estas haciendo) y **antes de TASK-0322 y TASK-0320**: las tres tocan
`scripts/memory/`, y esta fija la colocacion que 0322 no debe violar al estrechar `DATE_RE`.

requested_action: Reclamar TASK-0317, flipearla de changes_requested a in_progress, anadir el
contrato de falsacion que fija la colocacion de la exencion dentro del bloque del heuristico de
telefono, verificar por mutacion que el test cae si la condicion se mueve fuera, recomputar los
gates por exit code en clon limpio y dejar la tarea en in_review con el claim liberado.
