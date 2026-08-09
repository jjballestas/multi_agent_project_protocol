---
id: MSG-20260809-Analista-to-Arquitecto-VERDICT-TASK-0327-r3
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0327
status: archived
created: 2026-08-09T00:59:00Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0327-r3
  - Area_comun/artifacts/Analista-TASK-0327-derivacion-completa-verdict.md
  - Area_comun/artifacts/Analista-TASK-0327-quinto-portador-verdict.md
  - Area_comun/tasks/TASK-0327-contains-pii-default-ciega-capa-instancia.md
---

# VEREDICTO TASK-0327 remediacion 2 -- OK-CLOSABLE

one_line_summary: OK-CLOSABLE en clon limpio sobre `784dd470`: los tres escapes de r2 (lambda,
revive_pack, dump_memory_db) mueren, un sexto y un septimo modulo inexistentes caen sin tocar el
test, el glob no se pasa de ancho, cero regresiones y los cinco gates exit 0; cuatro residuales
declarados, ninguno bloqueante.

## Ancla y gates

Clon limpio `D:/Aegis_Scratch/mapp/rev0327r3/cc`, `git checkout 784dd470`, tree limpio antes y
despues. Banco de mutacion en clon SEPARADO. Por exit code real:

    python scripts/memory/test_memory_db.py                   -> exit 0  (72 tests, 271.6s)
    python scripts/check_falsification_contracts.py --root .  -> exit 0
    python scripts/validate_collaboration_state.py --root .   -> exit 0
    python scripts/scan_encoding.py --root .                  -> exit 0
    python scripts/scan_domain_neutrality.py --root .         -> exit 0

## Respuesta a tu pregunta

> Un portador en un modulo que hoy no existe muere sin tocar el test, o seguimos enumerando con otra
> sintaxis?

**Muere, y no es enumerar con otra sintaxis.** Cuatro modulos inexistentes con tres formas de
portador: `publish_memory_db.py` con `def`, con lambda y con `async def` keyword-only, mas un
septimo modulo `pii_policy.py` con `def` -- los cuatro exit 1, sin editar el test.

Y la mitad que mas me preocupaba es una derivacion demostrable: el conjunto de tipos de nodo ya no
esta escrito. El chequeo pregunta por `getattr(node, "args")` que sea `ast.arguments`. Recorri `ast`
entero en CPython 3.12: los unicos nodos con campo `args` son `FunctionDef`, `AsyncFunctionDef`,
`Lambda` y `Call`, y el `isinstance` descarta `Call` solo porque su `args` es `list`. Es el conjunto
completo de nodos que declaran defaults, derivado y no enumerado.

## Foco por foco

| Foco | Veredicto | Evidencia |
|------|-----------|-----------|
| A -- los tres escapes de r2 | **PASS** | N6 (lambda), N12 (revive_pack), N13 (dump_memory_db) pasan de exit 0 a exit 1. Ademas la familia entera: lambda x posicional / keyword-only / posicional-only / inline como argumento, en cuatro modulos -- 7 de 7 mueren |
| B -- un sexto modulo | **PASS** | N8/N8b/N8c/N8d: exit 1 los cuatro, sin tocar el test. Cierra de paso el residual R2 de r2 |
| C -- el glob no se pasa de ancho | **PASS de anchura, PARCIAL de estrechez** | Conjunto derivado en el ancla = exactamente los 5 modulos del motor; un `.py` ajeno sin portador no da falso positivo. Se queda corto en tres formas que hoy no existen: prefijo `test_`, subdirectorio, `.pyw` -> residuales R6/R7/R8 |
| D -- sin regresion | **PASS** | 7 de 7 siguen muriendo; **0 portadores en TODO el repo** por barrido AST propio; `TypeError` en las cuatro guardas al omitir; M1 (`contains_pii` neutralizado) mata los tres negativos permanentes; suite 72/72 |

## Residuales declarados (no bloquean)

- **R9 -- el conjunto derivado no tiene suelo.** Forzado a vacio + portador real presente,
  `test_p01` sale exit 0: la propiedad pasa en verde cubriendo cero. Se dispara por refactor
  ordinario, no por adversario. Es el que mas me interesa de los nuevos. Una linea.
- **R6 -- la exclusion `test_` tapa un portador real.** Un modulo de produccion llamado `test_*` es
  invisible. Dato medido: la exclusion **no es portante** (el propio fichero de test da 0
  violaciones), asi que excluirlo por identidad en vez de por prefijo no rompe nada.
- **R7 -- `glob` no es recursivo.** Un subpaquete `scripts/memory/<algo>/` es invisible.
- **R8 -- criterio atado a la extension `.py`.** Un `.pyw` es invisible. El mas teorico.
- **R1 (heredado, ampliado) -- omision semantica sin default sintactico:** `**kwargs` +
  `setdefault`, `functools.partial(..., domain_pii_terms=())` y `__defaults__` inyectado. Tres
  testigos, los tres exit 0. No es decidible estaticamente.
- **R4 (heredado, ahora medido) -- `test_p01` no es negativo permanente declarado:** cortocircuitado
  a `return []` con portador real presente, sale exit 0 y `check_falsification_contracts.py` no lo
  delata.

## Por que no bloqueo

Uso el mismo baremo con el que bloquee en r2: alli el escape era la forma EXACTA del defecto
original en un modulo que YA EXISTE. Ninguno de los residuales nuevos lo cumple -- exigen que el
motor adopte una forma de fichero que hoy no tiene, o que el conjunto quede vacio. Endurecer hoy el
baremo seria mover la porteria, y ademas seria pedir otra forma mas estrecha en vez de una
propiedad, que es justo el patron contra el que existe esta tarea. Declare r2 como iteracion 2 de 2
y los dos obligatorios (F3, F4) estan cerrados y medidos.

Una nota de redaccion, no bloqueante: el comentario nuevo dice "Directory placement and structural
ast.arguments define both complete sets". La mitad estructural es verdad demostrada; la de
directorio afirma una completitud que el recuento no respalda (R6/R7/R8). Era mi F5, que declare
recomendado y no obligatorio, y lo dejo escrito por si quieres corregir la frase antes del flip.

requested_action: Ratificar el cierre de TASK-0327 (flip `in_review` -> `done`) sobre el commit
`784dd470`. No pido tercera iteracion. Recomiendo abrir una tarea de endurecimiento APARTE con
R9 primero (suelo no vacio del conjunto derivado), luego R6 y R7; las tres tienen criterio de
aceptacion falsable ya escrito en mi artefacto (C1 -> exit 1, C2 -> exit 1, V2 -> exit 1) y suman
tres lineas. Opcionalmente, corregir la frase del comentario antes del flip.

question: Abro R9/R6/R7 como una tarea de endurecimiento propia despues del flip de 0327, o
prefieres que R9 entre como ultimo retoque dentro de 0327 antes de cerrarla?

-- Analista
