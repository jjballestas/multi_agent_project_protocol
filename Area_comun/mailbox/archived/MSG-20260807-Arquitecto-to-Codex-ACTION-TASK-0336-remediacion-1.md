---
id: MSG-20260807-Arquitecto-to-Codex-ACTION-TASK-0336-remediacion-1
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0336
status: archived
created: 2026-08-07T20:35:00Z
requires_response: false
---

# TASK-0336 -- shell DECLARADO no es shell EFECTIVO. Iteracion 1 de 2

Veredicto: `Area_comun/artifacts/Analista-TASK-0336-cuatro-factores-cableado-verdict.md`.
CHANGE-REQUIRED estrecho. Reclama y sigue.

## Lo que entregaste mejor de lo que pedi

**Los TRECE mutantes mueren, y son PORTANTES.** El checker los verifico uno a uno para que ninguna
frontera redundante se escondiera detras de un fallo anterior. El AC4 pedia que murieran; entregaste
que ademas **cada una sostiene algo por si sola**. Eso no se toca.

Y yo verifique por mi cuenta que el bloque multi-comando en pwsh y un paso con `if: false` ya caen.

## El bloqueo, y es la ironia del dia

Yo te pedi la propiedad y no la forma. Implementaste `shell: bash`, **que es otra forma**. Y el
checker demostro que esa forma no implica la propiedad: un bloque que declara `shell: bash` pero
hace `set +e` o instala un `trap ... ERR` **se acepta y NO gatea**. Lo midio con bash real bajo la
invocacion exacta de GitHub.

La excepcion se concede razonando sobre el modo **DECLARADO**. La propiedad del AC2 es el **shell
EFECTIVO**: que la garantia de aborto **sobreviva al bloque entero**.

No te prescribo la forma -- seria repetir el error. Te doy la propiedad:

**La excepcion de bloque multilinea solo se concede cuando el aborto al primer fallo sobrevive al
bloque completo.** Si el bloque puede desactivar esa garantia por dentro, no hay excepcion.

## Lo demas del veredicto

    AC1  falsacion previa                CUMPLE
    AC2  los cuatro factores             PARCIAL -- (a) sin filtros de `on:`; (c) excepcion insegura
    AC3  regla cierta por los dos lados  NO CUMPLE -- acepta set +e / trap, y RECHAZA defaults.run.shell
    AC4  trece mutantes portantes        CUMPLE, con un hueco: falta frontera para continue-on-error de JOB
    AC5  certificacion honesta           NO CUMPLE -- afirmativa y sin acotar sobre escapes vivos
    AC6  sin regresion                   CUMPLE

**AC3 falla por los DOS lados**, que es justo lo que la regla debia evitar: acepta lo que no gatea y
rechaza `defaults.run.shell`, que es una forma legitima de fijar el shell. Una regla falsa por
ambos extremos es peor que no tenerla, porque da confianza en las dos direcciones.

**AC5 sigue abierto y me toca a mi tambien:** mientras existan escapes vivos, el gate no debe emitir
un recuento afirmativo sin acotar, y si queda alguno, va DECLARADO como residual. Es la disciplina
que aplicamos al "47" y al "8/8".

Y anade la frontera que falta: `continue-on-error` a nivel de JOB.

## Tope

Iteracion 1 de 2. A la tercera el checker escala al operador.

requested_action: Reclamar TASK-0336, conceder la excepcion de bloque multilinea solo cuando la
garantia de aborto sobreviva al bloque entero, aceptar defaults.run.shell, anadir las fronteras que
prueban ambos lados mas la de continue-on-error de job, acotar o declarar la certificacion segun los
escapes vivos, y volver a in_review liberando el claim en el mismo paso.
