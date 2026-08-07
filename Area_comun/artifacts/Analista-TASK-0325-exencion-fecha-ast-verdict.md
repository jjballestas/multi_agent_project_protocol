---
artifact_id: ANALISTA-TASK-0325-exencion-fecha-ast-verdict
task_id: TASK-0325
type: artifact
owner: Analista
reviewer: Analista
status: done
created_at: 2026-08-07
project: multi_agent_project_protocol
relates_to:
  - TASK-0317
  - TASK-0322
  - SPEC-MEMORIA-HIBRIDA
---

# Veredicto Analista -- TASK-0325: endurecimiento de la exencion de fecha (AST + R5-1 + R5-2)

**Recomendacion de cierre: CHANGE-REQUIRED** (una sola iteracion, SIN tocar codigo de produccion).

La pregunta que abria el mensaje de revision -- "esto es el resultado correcto o es la forma de
cerrar una tarea sin hacer nada" -- tiene respuesta clara: **no es una tarea vacia**. El chequeo AST
**falla cerrado** en los cuatro vectores de desaparicion que se me pidio probar, los dos mutantes
**mueren de verdad** al ejecutarlos contra produccion, y la propiedad que los contratos afirman **ya
se cumplia**, asi que dejar `build_memory_db.py` byte-identico era lo correcto.

Lo que bloquea el cierre es otra cosa, y la encontre buscando la fuga que el foco A no cubria:
**el detector AST mira el conjunto de nodos equivocado**. Prohibe `ast.Continue` en todo el subarbol
del bucle. Eso deja simultaneamente (a) una **fuga real y demostrada** -- el mismo bypass estrecho
con `break` en lugar de `continue`, un identificador de distancia, que **pasa la suite entera 64/64
en verde** y hace que `contains_pii` devuelva `False` sobre un email -- y (b) un **falso positivo**:
un `continue` inocuo en el bucle interno del telefono hace fallar el contrato. Las dos cosas son la
misma causa raiz y se arreglan con un solo cambio localizado dentro del propio test entregado.

## Anclaje canonico

| Elemento | Valor |
|---|---|
| Repo | `multi_agent_project_protocol` (hub). **SIN PRODUCTO EN ALCANCE** -- ningun `npm test` de Nova/Zeus |
| Commit revisado | `70a22d88ed17591faf606da515729a6a3f8bbbd6` (el citado en la instruccion) |
| `origin/main` al abrir | `4260dae7` (el commit citado es ancestro: `git merge-base --is-ancestor` exit **0**) |
| Clon limpio | `D:/Aegis_Scratch/map/r0325`, detached en `70a22d88`, `git status --short` **vacio** |
| Estado canonico previo | `validate_collaboration_state.py` exit **0** en el arbol vivo antes de empezar |
| Hora local | 2026-08-07 09:47 (UTC+2) |

Todos los numeros de este veredicto salen del clon, no del arbol caliente. Los mutantes se
aplicaron **sobre produccion en el clon** y se restauraron; al terminar, `git status --short` del
clon sale vacio y la fuente vuelve byte-identica al commit citado (verificado por el propio driver).

## Reproduccion (todo por exit code, en clon limpio)

| Comando | Exit | Evidencia |
|---|---|---|
| `python scripts/memory/test_memory_db.py` | **0** | `Ran 64 tests in 203.348s ... OK` |
| `python scripts/check_falsification_contracts.py --root . --inventory` | **0** | 36 DECLARED; incluye `NEG-MEMORY-DATE-EXEMPTION-NO-CONTINUE` y `NEG-MEMORY-DATE-OFFSET-COVERAGE` |
| `python scripts/validate_collaboration_state.py` | **0** | `OK: collaboration state is valid` |
| `python scripts/scan_encoding.py` | **0** | `OK: encoding scan is clean` |
| `python scripts/scan_domain_neutrality.py` | **0** | limpio |
| `git diff --exit-code 70a22d88^ 70a22d88 -- scripts/memory/build_memory_db.py` | **0** | produccion **byte-identica**, confirmado |

Los dos runners nuevos estan **realmente ejecutados** por CI, no solo declarados:
`.github/workflows/validate.yml:49` invoca `python scripts/memory/test_memory_db.py`. Lo comprobe
expresamente por la leccion de TASK-0330 (contratos declarados que CI nunca corre).

## Foco A -- verdad vacia en el selector AST: **REFUTADO**

Esta era la preocupacion principal y **no se sostiene**. Mute produccion en el clon de cuatro formas
distintas de "el objetivo del selector deja de existir" y corri **solo** el contrato AST:

| Mutante sobre produccion | Exit del contrato | Resultado |
|---|---|---|
| A1 -- el bucle se **elimina** (cuerpo recto sobre `value_list(value)`) | **1** | FALLA (cierra) |
| A2 -- `contains_pii` se **renombra** a `contains_pii_impl` + alias con el nombre publico | **1** | FALLA (cierra) |
| A3 -- el bucle se **parte en dos** bucles directos | **1** | FALLA (cierra) |
| A4 -- el bucle se **envuelve** en un `if` (deja de ser hijo directo del cuerpo) | **1** | FALLA (cierra) |

La razon es que el selector no devuelve "no encontre nada, luego no hay `continue`": afirma
`assertEqual(1, len(functions))` y `assertEqual(1, len(loops))` **antes** de mirar el subarbol, y
ademas ancla `assertEqual(1, source.count(normalized_line))`. **Respuesta directa a tu pregunta: si
el bucle dejara de existir, el contrato FALLA, no pasa en verde.** El contrato no se apaga solo.

## Foco B -- los mutantes, ejecutados por mi: **PASS**

Aplique cada mutacion **a produccion** en el clon y corri su contrato:

| Mutante aplicado a produccion | Contrato | Exit | Resultado |
|---|---|---|---|
| `continue` temprano para fecha valida `+05:45` | `test_contains_pii_item_loop_has_no_early_continue` | **1** | `FAILED (failures=1)` -- muere |
| offsets restringidos a `(0\d\|1[0-2]):(00\|30)` | `test_valid_offset_complement_is_falsifiable` | **1** | `FAILED (failures=5)` -- muere |

Los dos mueren de verdad. No estoy citando el handoff.

## Foco C -- "produccion sin cambios" cierto y correcto: **PASS**

- **Cierto:** `git diff --exit-code` sobre `build_memory_db.py` entre `70a22d88^` y `70a22d88` sale
  **0** (byte-identica). El commit solo toca `test_memory_db.py` (+92) y estado del ledger.
- **Correcto:** la propiedad ya se cumplia. Medido por AST directamente sobre la fuente citada:
  nodos `Continue` en el bucle de `contains_pii` = **0**; nodos `Break` = **0**. Y los cuatro offsets
  ya los aceptaba `DATE_RE`. No hay contrato que pase afirmando una propiedad que la fuente incumple.

## Foco D -- coherencia con TASK-0322: **PASS**

`70a22d88` **desciende** de la entrega de 0322 (`c9a7ff05` es su padre), asi que el estrechamiento ya
esta dentro. Barrido independiente contra la gramatica post-0322 `(?:0\d|1[0-3]):[0-5]\d|14:00`:

- Los cuatro que 0325 afirma: `+05:45` -> True, `-09:45` -> True, `+13:00` -> True, `+14:00` -> True.
- **80 offsets reales** del rango IANA en uso (UTC-12:00 a UTC+14:00, minutos 00/30/45):
  **rechazados = 0**. El estrechamiento de 0322 no tira ningun offset legitimo.

Riesgo de acoplamiento comprobado y **descartado**: el contrato de 0325 ancla la gramatica por texto
literal (`assertEqual(1, source.count(offset_grammar))`), asi que una edicion futura de `DATE_RE` lo
rompe. Fui a ver si mi propio CHANGE-REQUIRED sobre 0322 lo detonaria: **no**, esa remediacion es de
**solo declaracion, cero codigo**. Las dos tareas aterrizan coherentes. Que el acoplamiento falle
cerrado ante un cambio de gramatica es correcto, no un defecto.

## Foco E -- TASK-0317 intacta: **PASS**

`test_timestamp_pii_suffix_is_rejected` + `test_timestamp_exemption_is_phone_only_and_falsifiable`
juntos: exit **0**. Los **11** vectores de sufijo siguen rechazados y la familia sigue afirmando
`assertEqual(333, len(timestamps))` con las 333 marcadas como PII. AC4 sin regresion.

## El bloqueo: el detector mira el conjunto de nodos equivocado

### La fuga, demostrada (SLIP-0325-1)

Tome el **mismo mutante estrecho** que el contrato nuevo usa y cambie **una palabra**:

```python
        if DATE_RE.fullmatch(item) and item.endswith("+05:45"):
            break                       # <-- `break`, no `continue`
        normalized = re.sub(r"[_/\\.-]+", " ", item)
```

Es una fuga **real**, no teorica, y es **estrictamente mas fuerte** que la que el contrato cubre,
porque `break` aborta el bucle entero y por tanto tambien ciega los items **posteriores**:

| Entrada | fuente | mutante `break` |
|---|---|---|
| `"2026-06-19T09:28:23+05:45"` con termino de dominio `2026` | `True` | **`False`** |
| `["2026-06-19T09:28:23+05:45", "contact me at a@b.com"]` | `True` | **`False`** |

El segundo caso es el que importa: **un email se cuela por el gate de PII** porque el `break` impide
llegar a mirarlo.

Y la evidencia decisiva: con ese mutante aplicado a produccion, la **suite completa** da
`Ran 64 tests in 207.490s ... OK`, **exit 0**. Ni el contrato AST nuevo, ni el contrato de colocacion
de 0317, ni el de offsets, ni ningun otro de los 36 lo ven. La familia de 333 de 0317 no incluye
`+05:45`, que es justo el hueco que 0325 venia a tapar -- y lo tapa solo para `continue`.

### El falso positivo (SLIP-0325-2)

El mismo `ast.walk` sobre todo el subarbol marca control de flujo que **no pertenece** al bucle de
items. Un `continue` inocuo dentro del bucle interno `for candidate in PHONE_CANDIDATE_RE.finditer`
-- donde `continue` significa "siguiente candidato de telefono", nada que ver con saltarse chequeos
-- hace **fallar** el contrato (exit 1). Eso bloquea un refactor legitimo.

### Tabla de decision del detector (medida, no argumentada)

`shipped` = lo entregado; `naive fix` = anadir `ast.Break` al mismo `ast.walk`; `scoped fix` =
solo el control de flujo **propiedad** del bucle externo (los bucles anidados re-vinculan
`break`/`continue`; los `FunctionDef`/`Lambda` anidados se excluyen).

| Variante de produccion | shipped | naive fix | scoped fix |
|---|---|---|---|
| fuente (commit citado) | PASS | PASS | PASS |
| **E1: bypass estrecho con `break` (fuga real)** | **PASS (hueco)** | CATCH | **CATCH** |
| `break` inocuo en el bucle interno del telefono | PASS | **CATCH (falso positivo)** | PASS |
| `continue` inocuo en el bucle interno del telefono | **CATCH (falso positivo)** | CATCH | PASS |

Solo la columna `scoped fix` acierta en las cuatro filas. El arreglo de una palabra **no** basta:
cierra el hueco pero empeora el falso positivo. Es la misma leccion que ya nos costo una vuelta en
este hilo -- el contrato tiene que atar el **efecto**, no una forma sintactica concreta.

## Tabla vector-por-vector

| # | Vector / criterio | Resultado |
|---|---|---|
| A1-A4 | Verdad vacia del selector AST (borrar / renombrar / partir / envolver) | **PASS** (falla cerrado en los 4) |
| B1 | Mutante `continue` temprano `+05:45` muere | **PASS** (exit 1) |
| B2 | Mutante de offsets restringidos muere | **PASS** (exit 1) |
| C1 | `build_memory_db.py` byte-identico | **PASS** (`git diff --exit-code` = 0) |
| C2 | La propiedad ya se cumplia (0 `Continue`, 0 `Break` en el bucle) | **PASS** |
| D1 | Los cuatro offsets aceptados tras el estrechamiento de 0322 | **PASS** |
| D2 | 80 offsets IANA reales, ninguno rechazado | **PASS** |
| D3 | Acoplamiento textual con la gramatica de 0322 | **PASS** (falla cerrado; la remediacion de 0322 no lo detona) |
| E1 | 11 vectores de sufijo rechazados | **PASS** |
| E2 | Familia de 333 miembros conservada | **PASS** |
| G | Gates protocolarios (validate / encoding / neutralidad / inventario) | **PASS** (exit 0) |
| G2 | Runner de los contratos nuevos realmente ejecutado por CI | **PASS** (`validate.yml:49`) |
| **S1** | **`break` estrecho: fuga real, suite 64/64 verde** | **SLIP** |
| **S2** | **`continue` inocuo en bucle anidado: falso positivo** | **SLIP** |

## Remediacion pedida (una iteracion, cero codigo de produccion)

Un solo cambio, dentro de `scripts/memory/test_memory_db.py`, en el helper del contrato
`NEG-MEMORY-DATE-EXEMPTION-NO-CONTINUE`:

1. Sustituir el `ast.walk(loop) if isinstance(node, ast.Continue)` por un recorrido que recoja
   `ast.Continue` **y** `ast.Break` **solo cuando pertenecen al bucle externo**: al descender a un
   `For`/`AsyncFor`/`While` anidado se deja de recoger, y los `FunctionDef`/`AsyncFunctionDef`/
   `Lambda` anidados no se visitan.
2. Anadir el mutante `break` a las fronteras del contrato, con el mismo patron que ya usa el
   mutante `continue`, para que la fuga quede clavada por mutacion y no por lectura.
3. Actualizar el texto del negativo declarado en `FALSIFICATION_CONTRACTS` para que diga lo que la
   guarda protege de verdad (salida temprana del bucle de items, no unicamente `continue`), y
   renombrar el id si el Arquitecto lo considera necesario.

**Gates afectados:** `python scripts/memory/test_memory_db.py` (exit 0) y
`python scripts/check_falsification_contracts.py --root . --inventory` (exit 0). No se toca
`build_memory_db.py`: sigue byte-identico.

**Falsacion que exijo en la re-entrega** (la corro yo, no la doy por buena leida):

- La tabla de cuatro filas de arriba con la columna `scoped fix`: **CATCH** en E1 y **PASS** en los
  dos casos inocuos del bucle anidado.
- La suite completa con el mutante E1 aplicado a produccion debe salir **RED** (hoy sale verde).
- AC4 sin regresion: 11 vectores + familia de 333 + los cuatro offsets, todos exit 0.

**Bucle de fix:** remediacion -> re-juicio del checker **antes** del commit de cierre. **Maximo 2
iteraciones**; si a la segunda sigue sin cerrar, escalo al operador humano.

## Residuales declarados (no bloquean)

- **R0325-1 (heredado, informativo).** La cobertura del contrato AST sigue siendo **sintactica**. Con
  el `scoped fix` quedan cubiertos `continue` y `break`; un bypass equivalente por reestructuracion
  (`if not DATE_RE...: <todos los chequeos>`) o por filtrado del iterable en un helper externo sigue
  invisible para el AST. Lo medi: las tres formas pasan el contrato entregado. **La diferencia es
  que esas tres, en su version amplia, SI las mata el contrato de colocacion de 0317** (rompen la
  afirmacion positiva sobre los 333). Solo la version **estrecha** sobre un offset fuera de la
  familia muestreada se escapa de todo -- y es justo la que la remediacion clava para `break`. Cerrar
  la familia entera pide un contrato **por comportamiento** (muestreo de offsets fuera de los 333
  contra `contains_pii`), no mas AST. Candidato a tarea propia.
- **R0325-2 (informativo).** La familia de 333 de 0317 y el conjunto de offsets de 0325 son
  **disjuntos**: 0317 muestrea `("", "Z", "+02:00", "-05:00", "-12:30")` y 0325 anade
  `+05:45/-09:45/+13:00/+14:00` pero **solo contra `DATE_RE`**, nunca contra `contains_pii`. Ese
  hueco es exactamente por donde entra SLIP-0325-1. Unificar ambos muestreos cerraria R0325-1 de
  raiz.
- **R0325-3 (heredado de 0322, ya declarado en su veredicto).** `DATE_RE` usa `\d` sin `re.ASCII`.
  No lo reabro aqui.

## Conclusion

La tarea **no** es un cierre vacio: produccion no cambiaba porque no debia cambiar, el selector AST
falla cerrado, los dos mutantes mueren y AC2/AC4 se cumplen. Pero la guarda entregada, tal como esta,
deja verde una fuga de PII demostrada que es mas fuerte que la que cierra, y ademas bloquea un
refactor inocuo. Las dos cosas salen del mismo `ast.walk` mal acotado y se corrigen juntas dentro
del artefacto ya entregado, sin tocar produccion.

**CHANGE-REQUIRED.** Si el Arquitecto juzga que la letra de AC1 (`continue`, literal) gobierna sobre
el negativo declarado ("bypasses later checks"), la alternativa disciplinada es cerrar en
OK-CLOSABLE **registrando SLIP-0325-1 como residual de severidad bloqueante con owner y tarea
propia**, nunca como observacion. Mi recomendacion es arreglarlo ahora: cuesta una iteracion y esta
dentro del fichero que la tarea ya toco.

-- Analista
