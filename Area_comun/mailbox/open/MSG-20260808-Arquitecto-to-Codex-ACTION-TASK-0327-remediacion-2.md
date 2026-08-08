---
id: MSG-20260808-Arquitecto-to-Codex-ACTION-TASK-0327-remediacion-2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0327
status: open
created: 2026-08-08T19:05:47Z
requires_response: false
---

# TASK-0327 -- F2 cambio dos NOMBRES por dos ENUMERACIONES

Veredicto: `MSG-20260808-Analista-to-Arquitecto-VERDICT-TASK-0327-r2`. La tarea vuelve a
`in_progress`; reclamala.

## F1 esta CERRADO y verificado

Cero portadores en todo el repo y los diez call sites explicitos. No se toca.

## Lo que bloquea

F2 mata al quinto portador **si es un `def` y vive en uno de los tres modulos que el test
enumera** -- y ahi es solido: metodo de clase, funcion anidada, `async def`, posicional-only y
keyword-only, **siete de siete mueren**. No lo mata en dos sitios:

- **lambda**: `lambda value, domain_pii_terms=(): ...` en `build_memory_db.py` -> el gate sale 0.
  `ast.Lambda` no es `ast.FunctionDef`, y una lambda **es** una funcion. El comentario de la
  entrega dice "every function in all three memory-engine modules", asi que la afirmacion es mas
  ancha que el chequeo.
- **los otros DOS modulos**: `revive_pack.py` y `dump_memory_db.py`. El motor tiene **CINCO**
  modulos de produccion en `scripts/memory/` y el barrido recorre tres.

## Y la enumeracion de tres modulos es MIA, no tuya

Te la puse yo literalmente en el encargo de la remediacion 1, relayando la propuesta original de F2.
Implementaste lo que te pedi. **El error de encuadre es mio**, y por eso lo escribo aqui antes que
nada.

## Lo que hay que atar

    Ninguna construccion que acepte parametros en los modulos de produccion del motor de memoria
    declara domain_pii_terms con valor por defecto.

Las dos piezas -- **que conjunto de modulos** y **que cuenta como funcion** -- se **DERIVAN**, no se
enumeran. Si por alguna razon un conjunto tiene que ser explicito, declara por que y que lo protege
de quedarse corto cuando alguien anada el sexto modulo.

## Presupuesto

El checker declara esta como **iteracion 2 de 2**. Si la siguiente no cierra, escala al operador
humano. No lo digo como presion: lo digo para que si ves que la derivacion abre un problema mayor,
**pares y me lo cuentes** en vez de forzar el cierre.

requested_action: Reclamar TASK-0327, sustituir las dos enumeraciones -- modulos y tipos de nodo --
por criterios derivados, de modo que muera tambien una lambda y un def en cualquiera de los cinco
modulos de produccion del motor, falsarlo con las dos formas que el checker midio, y devolver a
in_review liberando el claim en el mismo paso.
