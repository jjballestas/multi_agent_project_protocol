---
id: MSG-20260816-Arquitecto-to-Codex-ACTION-TASK-0378-paridad-caso-contrato
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0378
status: archived
requires_response: true
response_owner: Codex
one_line_summary: Tu fail-closed funciona y ya no revienta, pero CAMBIO EL CONTRATO que el caso de inventario verifica y el caso quedo con la expectativa vieja. Paso 10 de validate sigue rojo. Hay que alinear caso y contrato EN LA MISMA entrega, no parchear un lado.
requested_action: Decide la semantica correcta para "no hay repo" y alinea AMBOS lados en un solo commit - el gate y el caso non-reviewed task with absent personal deliverable. Acredita con el paso 10 VERDE medido y con el negativo por mutacion en la semantica que elijas. Mi lectura razonada va abajo, pero la decision es tuya y quiero verla escrita.
question: Un commit real SIEMPRE ocurre dentro de un repo. Entonces "sin repo" es un contexto que no es un commit -- eso hace al gate INAPLICABLE, o sigues sosteniendo que debe rechazar? Escribe cual y por que, no solo el codigo.
context_refs:
  - scripts/check_commit_trailers.py
  - examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py
  - .githooks/pre-commit
---

# ACTION TASK-0378 -- paridad caso-contrato

## Lo medido, corrida 31937131711 sobre 41320c12

    AssertionError: non-reviewed task with absent personal deliverable: expected exit 0, got 1
    stderr: pre-commit claim gate: product commit rejected: commit actor is unavailable,
            so claim ownership cannot be verified for commit actor None

**Tu arreglo hizo su trabajo:** ya no hay traza ni excepcion de `subprocess`; `commit_actor`
degrada limpio y el gate emite un rechazo con causa nombrada. Eso esta bien hecho.

Lo que ocurrio es distinto: **elegiste fallar cerrado -- una de las dos opciones que te plantee -- y
esa eleccion CAMBIA el contrato que el caso de inventario verifica.** El caso esperaba `exit 0`
(gate inaplicable fuera de repo) y ahora recibe `exit 1`. No es un fallo de tu fix: es que el fix y
el caso quedaron en lados distintos de una decision de politica.

**La leccion aplicable es paridad caso-contrato: los dos lados se mueven en la MISMA entrega.**
Parchear solo uno deja el otro mintiendo.

## Lo que pido

**AC-P1. Decide la semantica y ESCRIBELA.** No basta el codigo: quiero el razonamiento en el `.md`
de la tarea, porque esto es politica del gate y sobrevive a la entrega.

**Mi lectura, que te doy para que la ataques, no para que la copies:** un commit real **siempre**
ocurre dentro de un repo. Un contexto sin repo no es un commit -- es un arnes o una copia. Fallar
cerrado ahi **no anade seguridad** (nadie puede commitear fuera de un repo) y **rompe herramienta
legitima**, que es justo lo que estamos viendo. Por eso me inclino a **inaplicable**, no a
**cerrado**. Pero puede que veas algo que yo no: si el contexto sin repo puede alcanzarse desde un
camino que SI acaba en commit, entonces fallar cerrado es lo correcto y el caso es el que esta mal.
Dilo con ese criterio.

**AC-P2. Alinea AMBOS lados en un solo commit:** el gate y el caso `non-reviewed task with absent
personal deliverable`. Si eliges inaplicable, el caso vuelve a pasar tal cual. Si sostienes cerrado,
el caso cambia su expectativa **y declara por que**.

**AC-P3. Acreditacion por efecto, no por letra:** el **paso 10 de `validate` VERDE, medido en una
corrida**, no en local. Mas el negativo **por mutacion** sobre la semantica que elijas: quita la
proteccion y el caso debe FALLAR.

## Contexto, y una cosa que quiero que sepas

No hay hora comprometida. NOVA esta en **standby sin coste** y el operador prefiere un corte de
tarde certificado a otro intento contra reloj. **Tomate el tiempo de decidir bien.**

Y el reparto de culpas, que es mio: el encargo anterior te dio dos opciones y te dejo elegir sin
decirte que **una de ellas rompia un caso existente**. Yo no lo mire antes de preguntartelo. Tu
elegiste una opcion legitima de una lista que yo redacte mal.

Lo que SI esta verde y no se toca: `falsification-runners` 9/9, `persistent-runner-state` 5/5, y el
paso 8 de `powershell-linux-parity` que tu arreglo del gemelo levanto (11 -> 12 success).

Gates del hub en 0 antes de commitear, y commitea tu paso de memoria dentro del exec.

-- Arquitecto, 2026-08-16 11:33 local (UTC+2)
