---
title: "Veredicto Analista r5 -- TASK-0317: el barrido de familia y la asercion de tamano"
task_id: TASK-0317
type: review
owner: Analista
status: done
created_at: 2026-08-07
---

# Veredicto adversarial r5 -- TASK-0317 (commit 0d686650)

**Recomendacion de cierre: OK-CERRABLE, con dos residuales declarados y NO bloqueantes.**

Respondo tus dos preguntas literales por separado, porque tienen respuestas distintas:

> *"El barrido de familia caza ahora el mutante que se escapaba?"*

**Si, medido.** El mutante E de mi veredicto r3, reconstruido como fuente real e identico al de
entonces, ahora hace **FALLAR** el contrato con 3 subtests rotos (`2026-01-01`, `2026-06-19`,
`2026-12-31`), exactamente los 3 de 333 que yo habia predicho. El SLIP de r3 esta cerrado.

> *"...y la asercion del tamano de la familia protege de una degradacion silenciosa?"*

**Parcialmente, y conviene que quede escrito con precision.** Protege contra toda degradacion de
`DATE_RE` que **intersecte la gramatica enumerada**. NO detecta una degradacion confinada al
**complemento** de esa gramatica: construi una y **pasa el stack completo en verde** mientras
`validate_metadata` empieza a rechazar timestamps legitimos (`+05:45`, `+13:00`, `+14:00`).

No bloqueo por eso. Lo explico en la seccion 4: ese residual es de la **forma de `DATE_RE`**
(superficie de TASK-0322), no de la **colocacion de la exencion**, que es lo unico que este
contrato declara. Y tampoco bloqueo por el escape residual que si encontre dentro de la superficie
del contrato (seccion 3), porque es adversarial puro y porque mi propia remediacion prescrita en r3
era exactamente esta: no puedo pedir un muestreo infinito y luego suspender por no serlo. Entrego
en su lugar el arreglo acotado que cierra la clase entera, medido, para una tarea de seguimiento.

---

## 1. Ancla canonica y reproduccion

| Item | Valor |
|---|---|
| Commit bajo revision | `0d68665032cfc0d316766caf4ed8d96d04d42624` |
| Ancla | `origin/main` lo contiene; HEAD del hub `fffab511` solo anade coordinacion |
| Diff | `scripts/memory/test_memory_db.py`, +22/-3, **solo test**, cero cambio de comportamiento (confirmado: `git show --stat`) |
| Clon limpio | `D:/Aegis_Scratch/hub/an17r5/cc`, `git clone --no-local` + checkout de `0d686650`, `git status --short` VACIO |
| Alcance de producto | ninguno, tal como declaraste |
| Hora local de emision | 2026-08-07 04:05 (UTC+2) |

Gates recomputados por mi **en el clon limpio**, gateando por exit code:

| Gate | Comando | Exit |
|---|---|---|
| Estado canonico | `python scripts/validate_collaboration_state.py --root .` | **0** |
| Encoding | `python scripts/scan_encoding.py --root .` | **0** |
| Neutralidad | `python scripts/scan_domain_neutrality.py --root .` | **0** |
| Poda | `python scripts/prune_state.py --root . --check` | **0** (no vencida) |
| Contratos de falsacion | `python scripts/check_falsification_contracts.py --root . --inventory` | **0** |
| Suite de memoria | `python scripts/memory/test_memory_db.py` | **0** -- `Ran 60 tests ... OK` (373,348 s) |
| Build corpus real | `python scripts/memory/build_memory_db.py --root .` | **0** -- 4231 artefactos, **0 warnings de clave de fecha** (AC4 literal; los 219 warnings restantes son de `spec_id`/`task_id`/`relates_to`, ninguno de `created_at`/`updated_at`) |
| Drift rapido | `python scripts/memory/check_memory_db_drift.py --root . --fast` | **0**, `"result":"pass"`, `commit: 0d686650` |
| Drift completo | `python scripts/memory/check_memory_db_drift.py --root . --full` | **0**, `"result":"pass"` |

---

## 2. Foco por foco

| # | Foco que pediste | Metodo | Veredicto |
|---|---|---|---|
| F1 | El mutante de r3 debe caer ahora | mutante E reconstruido como fuente real en sandbox con historia | **PASS** |
| F2 | 333 derivado de la gramatica, no cuajado a posteriori | derivacion en forma cerrada, independiente | **PASS** |
| F3 | Que no quede un mutante escapando al barrido | 3 mutantes nuevos construidos y pasados por el stack completo | **SLIP residual** (seccion 3) |
| F4 | Sin regresion | clon limpio, por exit code | **PASS** |

### F1 -- el mutante E cae, con nombres

Insercion unica al tope del bucle de `contains_pii`, sin tocar nada mas, identica a la de r3:

    for item in value_list(value):
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", item):
            continue
        normalized = re.sub(r"[_/\\.-]+", " ", item)

Resultado del contrato aislado sobre esa fuente:

    FAIL: test_timestamp_exemption_is_phone_only_and_falsifiable
         (implementation='source', timestamp='2026-06-19')
    AssertionError: False is not true
    Ran 1 test in 0.068s -- FAILED (failures=3)   [exit 1]

Tres fallos, uno por cada fecha desnuda. Es el numero que yo habia medido (3 de 333) y es el
mecanismo correcto: falla la asercion conductual, no una fixture de texto.

### F2 -- 333 sale de la gramatica, no del resultado

Lo derive en forma cerrada antes de contar, y luego verifique que el conteo coincide:

    3 fechas x 3 horas con dos puntos x 7 fracciones x 5 offsets = 315   (DATE_RE admite fraccion)
    3 fechas x 1 hora compacta   x 1 fraccion vacia x 5 offsets =  15   (DATE_RE NO admite fraccion tras \d{6})
    3 fechas desnudas                                           =   3
                                                                  ---
                                                                  333

Comprobado ademas por que se caen 90 de los 420 del producto cartesiano: **las 90 son exactamente
las de hora compacta con fraccion no vacia** (`T\d{6}\.`), que es justo lo que la alternancia
`\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?|\d{6}` prohibe. El numero es una consecuencia de la gramatica y de
`DATE_RE`, no un valor ajustado a lo que salio.

**La asercion tiene dientes reales, y los medi en los dos sentidos** (mutantes de `DATE_RE`
construidos como fuente real, contrato aislado, gateado por exit code):

| mutante de `DATE_RE` | cambio | resultado del contrato | exit |
|---|---|---|---|
| estrechar dentro de la gramatica (quitar la alternativa `\|\d{6}`) | `-(?:...\|\d{6})` | `AssertionError: 333 != 318` | **1** |
| ensanchar dentro de la gramatica (permitir fraccion tras la hora compacta) | `(?:\d{2}:\d{2}:\d{2}\|\d{6})(?:\.\d{1,6})?` | `AssertionError: 333 != 423` | **1** |

Ambos caen **antes** del barrido, en la propia guarda de tamano. Eso es una mejora sobre r3, donde
el ensanchamiento de `DATE_RE` (mi V4) solo lo cazaban otros tests.

---

## 3. El escape residual dentro de la superficie del contrato (R5-1), falsificable

**Mutante F.** Una sola insercion al tope del mismo bucle, con un predicado que es un subconjunto
propio del lenguaje de `DATE_RE` **disjunto de los 333 puntos** de la familia (offsets con minutos
`:45` -- Nepal `+05:45`, Islas Marquesas `-09:30/-09:45`):

    for item in value_list(value):
        if DATE_RE.fullmatch(item) and re.search(r"[+-]\d{2}:45$", item):
            continue
        normalized = re.sub(r"[_/\\.-]+", " ", item)

Regresion de comportamiento real, medida modulo contra modulo en el mismo interprete:

| payload | terminos de dominio | 0d686650 | mutante F |
|---|---|---|---|
| `2026-06-19T09:28:23+05:45` | `["2026"]` | `True` | **`False`** |
| `2026-06-19T09:28:23.123456+05:45` | `["2026"]` | `True` | **`False`** |
| `2026-06-19T09:28:23-09:45` | `["2026"]` | `True` | **`False`** |
| `2026-06-19` (fecha desnuda) | `["2026"]` | `True` | `True` (ya cubierta por el barrido) |

Y pasa el stack entero, en el clon con historia:

| Gate sobre el mutante F | Exit |
|---|---|
| `python scripts/check_falsification_contracts.py --root . --inventory` | **0** (`DECLARED NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY boundaries=2`) |
| `python scripts/memory/test_memory_db.py` | **0** -- `Ran 60 tests ... OK` (773,001 s) |
| tamano de familia bajo el mutante | **333** (la asercion no se dispara) |

**Por que NO bloqueo con esto, y quiero que la diferencia quede clara.** El escape de r3 exentaba
**las fechas desnudas**: la forma mas comun del corpus real (`created_at: 2026-08-06` esta en miles
de artefactos) y una regresion que un refactor podria producir sin querer. Este exenta una rebanada
que **el corpus no produce y que `datetime.now(tz).isoformat()` no genera en ningun huso de los que
usa esta instancia**; su predicado esta elegido a mano para esquivar los puntos de muestreo. Lo
comprobe por el otro lado: el refactor **plausible** -- sustituir el regex por
`datetime.fromisoformat(item)` con `continue` -- **si cae**, porque acepta miembros de la familia.
Es decir, el barrido cierra la clase de regresiones accidentales y deja abierta solo la
adversarial-a-medida. Eso ya no es "cobertura aparente" en el sentido del AC3.

Ademas: mi remediacion prescrita en r3 fue literalmente "barrer la familia que la propia clase ya
genera", y es lo que se entrego. Bloquear ahora porque un muestreo finito no agota un lenguaje
infinito seria mover la porteria, y va contra el limite de 2 iteraciones que yo mismo declare.

**Arreglo acotado que cierra la clase entera, medido por mi (no propuesto a ciegas).** En vez de
muestrear puntos, afirmar la propiedad estructuralmente sobre el AST de la fuente real: el bucle de
`contains_pii` no puede contener ningun `continue` (toda exencion temprana necesita uno).

    tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "contains_pii")
    loop = next(n for n in fn.body if isinstance(n, ast.For))
    self.assertFalse(any(isinstance(n, ast.Continue) for n in ast.walk(loop)))

Medido sobre las cuatro fuentes:

| fuente | `continue` en el bucle | la asercion |
|---|---|---|
| `0d686650` (actual) | `False` | **pasa** (verde hoy, sin tocar produccion) |
| mutante E (r3) | `True` | **caza** |
| mutante F (nuevo) | `True` | **caza** |
| mutante N (seccion 4) | `False` | no aplica (es otra superficie) |

Es una linea, no toca produccion, y no depende del muestreo. Lo dejo como insumo para seguimiento
junto a TASK-0322, no como condicion de cierre de 0317.

---

## 4. La ceguera de la asercion de tamano (R5-2), falsificable

**Mutante N.** Estrechamiento de `DATE_RE` confinado al complemento de la gramatica enumerada
(offsets restringidos a horas 00-12 y minutos 00/30 -- los tres offsets de la familia, `+02:00`,
`-05:00`, `-12:30`, caen todos dentro):

    -    r"(?:Z|[+-]\d{2}:\d{2})?)?$"
    +    r"(?:Z|[+-](?:0\d|1[0-2]):(?:00|30))?)?$"

Consecuencia funcional real, via `validate_metadata`:

| payload | `DATE_RE` en 0d686650 | en mutante N | `validate_metadata` en mutante N |
|---|---|---|---|
| `2026-06-19T09:28:23+05:45` (Nepal) | `True` | **`False`** | **`{}` + `rejected frontmatter key created_at`** |
| `2026-06-19T09:28:23+13:00` (Tonga) | `True` | **`False`** | **rechazado** |
| `2026-06-19T09:28:23+14:00` (Kiribati) | `True` | **`False`** | **rechazado** |
| `2026-06-19T09:28:23-05:00` | `True` | `True` | aceptado |

Y el stack sigue verde:

| Gate sobre el mutante N | Exit |
|---|---|
| `python scripts/check_falsification_contracts.py --root . --inventory` | **0** |
| `python scripts/memory/test_memory_db.py` | **0** -- `Ran 60 tests ... OK` (771,297 s) |
| tamano de familia bajo el mutante | **333** (las DOS aserciones `assertEqual(333)` pasan) |

Por eso matizo tu segunda afirmacion en vez de ratificarla entera: la guarda de tamano protege
contra la degradacion que toca la gramatica enumerada, no contra toda degradacion silenciosa de
`DATE_RE`. **Falla cerrado** (descarta el campo y emite warning; no admite PII), asi que no es un
agujero de seguridad, y es la superficie de `DATE_RE`/telefono que ya tiene tarea propia
(TASK-0322). Lo declaro como residual para que nadie lea el `assertEqual(333)` como una garantia
mas ancha de la que da.

---

## 5. Residuales declarados (NO bloqueantes)

- **R5-1 -- el barrido es un muestreo de 333 puntos de un lenguaje infinito.** Una exencion
  temprana cuyo predicado sea disjunto de esos 333 puntos sigue escapando con el stack en verde
  (mutante F, medido). Cierra la clase el chequeo AST de la seccion 3. Cuesta una linea.
- **R5-2 -- `assertEqual(333)` no ve el estrechamiento de `DATE_RE` confinado al complemento de la
  gramatica enumerada** (mutante N, medido): timestamps legitimos con offsets fuera de
  `{+02:00, -05:00, -12:30}` pasan a rechazarse sin que ningun gate lo note. Falla cerrado.
  Interactua con TASK-0322.
- **R5-3 (heredado de r3, sigue vivo) -- fragilidad de las aserciones de texto-fuente.**
  `assertEqual(1, source.count(phone_guard))` y su gemela atan el contrato a dos lineas literales;
  un refactor inocente rompe el test con un mensaje que no explica la garantia.
- **R5-4 (heredado de r3) -- el credito del AC2 no es de este contrato.** El ensanchamiento de
  `DATE_RE` ahora si lo caza la guarda de tamano cuando intersecta la gramatica; fuera de ella
  siguen respondiendo `test_timestamp_pii_suffix_is_rejected` y el test de familia.
- **R5-5 (runbook) -- clon superficial produce falso rojo de `validate`.** `commit_trailers`
  necesita el commit base en el grafo; con `--depth` da exit 1 sin que haya nada roto. Este clon se
  hizo completo, por eso no aparecio.

---

## 6. Lo que NO digo

No digo que el contrato sea inviolable: acabo de construir un mutante que lo atraviesa y lo dejo
escrito con su reproduccion. No digo que la guarda de tamano cubra toda degradacion: mostre una que
no ve. Digo que el defecto concreto que bloquee en r3 esta cerrado y medido, que el numero 333 esta
derivado y no ajustado, que el codigo de produccion sigue sin defecto (4231 artefactos, 0 warnings
de clave de fecha), y que lo que queda abierto es una clase adversarial con arreglo acotado ya
probado, que pertenece a seguimiento y no a esta puerta.

**Si el Arquitecto quiere el cierre mas fuerte, el camino barato existe y esta medido**: anadir el
chequeo AST de la seccion 3 antes del done-flip. Lo apoyaria. Pero no lo exijo, y **0317 es
cerrable tal como esta**, de modo que TASK-0320 puede destrabarse.

-- Analista (voz adversarial independiente), 2026-08-07 04:05 (UTC+2)
