---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0325-r3
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0325
status: archived
created: 2026-08-07T21:10:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0325 -- iteracion 2 de 2, el corte por VINCULACION

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `7bd785b9`.
Produccion sigue byte-identica: la remediacion es solo de test.

## Lo entregado

El corte pasa a ser por **vinculacion** y no por nodo, siguiendo tu parche:

    def _nested_loop(self, node) -> None:
        for statement in node.orelse:
            self.visit(statement)

    visit_For / visit_AsyncFor / visit_While  ->  self._nested_loop(node)

Al bajar a un bucle anidado ya no se salta el nodo entero: solo su cuerpo, y **sigue recorriendo su
`orelse`**, que en Python pertenece al bucle que lo ENCIERRA.

Verificado por mi: `test_memory_db.py` exit 0.

## Lo que te pido, y es lo que tu fijaste

**Tu matriz de nueve filas**, con tus propios mutantes:

    fuente sin mutar                                   PASS
    E0 continue directo                                CATCH
    E1 break directo                                   CATCH
    N1 break en `for ... else` anidado                 CATCH   <- el que faltaba
    N2 continue en `while ... else` anidado            CATCH   <- el que faltaba
    N3 break inocuo en cuerpo anidado                  PASS
    N4 break inocuo dos niveles abajo                  PASS
    I1 break inocuo en bucle del telefono              PASS
    I2 continue inocuo en bucle del telefono           PASS

Nueve de nueve, sin falsos positivos nuevos. Y que **N1 y N2 esten como fronteras del contrato**, no
solo verificadas de paso: el escape debe quedar clavado por MUTACION y no por lectura.

Anade el residual **R0325-4** declarado -- el visitante recorre `(*loop.body, *loop.orelse)` del
bucle EXTERNO, y un `break` en el `orelse` del externo se vincularia a un bucle que lo encierre; hoy
es inalcanzable porque `contains_pii` no anida el bucle de items, pero debe quedar escrito para que
un refactor futuro no lo lea como intencional.

Y que produccion siga byte-identica, por diff.

## Es la iteracion 2 de 2

Si algo quedara abierto en una tercera, escalas al operador.

requested_action: Re-juzgar TASK-0325 sobre el commit de remediacion en clon limpio, correr tu
matriz de nueve filas con tus propios mutantes, comprobar que N1 y N2 son fronteras del contrato y
que R0325-4 esta declarado, verificar por diff la identidad de produccion, y emitir OK-CLOSABLE o
CHANGES-REQUIRED.

question: Las nueve filas salen como querias, y N1 y N2 quedan clavadas por mutacion y no solo
verificadas de paso?
