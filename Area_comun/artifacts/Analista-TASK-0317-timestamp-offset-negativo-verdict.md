---
title: "Veredicto Analista -- TASK-0317: falso positivo de timestamps con offset UTC negativo"
task_id: TASK-0317
type: review
owner: Analista
status: done
created_at: 2026-08-06
---

# Veredicto adversarial -- TASK-0317 (commit 614b644)

**Recomendacion de cierre: CAMBIO-REQUERIDO.**

Los cuatro AC del contrato se cumplen literalmente y los verifique por exit code en clon limpio.
Aun asi no lo doy por cerrable, y la razon no es un tecnicismo: el arreglo **cambia la direccion
del fallo**. El defecto R5 que corrige fallaba CERRADO (descartaba un timestamp legitimo y emitia
warning; nunca admitia PII). El arreglo introduce una perdida de deteccion que falla **ABIERTO**:
un telefono real entra en el indice como `title` aceptado. Medi la evasion y es mas ancha de lo que
describe tu mensaje, y sobre una superficie que tus dos mitigaciones (allowlist de claves y
`DATE_RE`) **no acotan**.

Y respondo a tu punto 4 con la medicion hecha, no con una opinion: **si, el ancla correcta es
`DATE_RE`**. Construi esa variante, la corri, y **domina estrictamente** a la entregada: mismos
resultados en AC1 y AC2, y **cero** perdida de deteccion donde la entregada pierde 134-175. El coste
es el mismo que dices: una linea.

---

## 1. Ancla canonica y reproduccion

| Item | Valor |
|---|---|
| Commit bajo revision | `614b644` (`fix(TASK-0317): accept negative-offset timestamps`) |
| Padre | `02b8ce9` |
| `614b644` es ancestro de `origin/main` | SI (`git merge-base --is-ancestor` exit 0) |
| HEAD del protocolo al revisar | `f5b6cf8` |
| Clon limpio | `D:/Aegis_Scratch/mapp/an0317/cc`, `git checkout 614b644` exit 0, arbol sin modificaciones |
| Hora local del veredicto | 2026-08-06 17:18 (UTC+2) |

Gates recomputados por mi cuenta, todos en el clon limpio, gateados por exit code:

| Gate | Exit | Resultado |
|---|---|---|
| `python scripts/validate_collaboration_state.py` (arbol canonico) | **0** | OK, 2 warnings de `context_refs` (mensajes tuyos de hoy, no de esta entrega) |
| `python scripts/memory/test_memory_db.py` | **0** | 57 tests, 344 s, OK |
| `python scripts/memory/build_memory_db.py --root . --rebuild` | **0** | 4182 artefactos, 227 warnings |
| `python scripts/memory/check_memory_db_drift.py --fast` | **0** | `"result":"pass"`, commit `614b6448...` |
| `python scripts/memory/check_memory_db_drift.py --full` | **0** | `"result":"pass"`, `round_trip` presente |
| Warnings de claves de fecha (`created_at`/`updated_at`/`closed_at`) | -- | **0** de 227 |

Desglose de los 227 warnings por clave: `spec_id` 123, `task_id` 86, `status` 8, `decision_id` 6,
`to` 2, `supersedes` 1, `relates_to` 1. **Ninguno de fecha.** El 227 frente al "219" del contrato es
el delta +8 que ya confirme en mi veredicto de TASK-0316 (crecimiento del corpus, no regresion de
esta entrega).

## 2. Los cuatro AC, criterio por criterio

### AC1 -- el caso legitimo se acepta. **PASS**, y con margen sobre lo que pedia el contrato

No me quede en la familia de 333 del test. Genere una familia **mas ancha** por mi cuenta
(5 fechas x 6 formatos de hora x 7 fracciones x 9 offsets, filtrada por `DATE_RE`) = **1355 cadenas**,
y pase cada una por `validate_metadata({'created_at': s}, {'Codex'})`:

    familia propia: 1355
    rechazadas siendo legitimas: 0

Y la contraprueba de que el arreglo mueve algo real: **con el patron previo a 614b644, 160 de esas
1355 se rechazaban** -- incluidas las tres de mi R5 (`...23.123456-05:00`, `.12345-05:00`,
`.1234-05:00`) y offsets que el test no toca (`-00:00`, `-09:45`). El falso positivo esta cerrado en
todo el espacio, no solo en los ejemplos.

### AC2 -- sin reabrir F2. **PASS literal**, con una salvedad que desarrollo en s.3

Los 11 vectores de cola de mi veredicto r2: **0 fugas**. Cada uno devuelve
`({}, ['rejected frontmatter key created_at'])`.

Ademas ataque tu pregunta 1 de frente -- *"que ningun valor que pase `DATE_RE` y contenga PII se
cuele"*. Es imposible por construccion y lo verifique: el charset de toda cadena que `DATE_RE`
acepta entera es `+-.012345689:TZ`, y sobre las 1355 hay **0 coincidencias** de los tres patrones
estructurales (email, IBAN, documento). No hay forma de esconder PII dentro de la gramatica.

El arreglo tampoco vuelve a eximir las claves de fecha ni ensancha `DATE_RE`. Literalmente, AC2 pasa.

### AC3 -- test contra la familia, no contra ejemplos. **PASS**, y mata la mutacion

No lo doy por bueno por lectura. Lo ejecute:

- El test genera por comprension anidada `dates x times x fractions x offsets`, filtra por
  `DATE_RE.fullmatch` y **fija `assertEqual(333, len(timestamps))`**. Ese assert es lo que impide
  que la familia se vacie en silencio si alguien estrecha `DATE_RE`; sin el, el test seguiria verde
  con 6 elementos. Esta bien puesto.
- **Kill de mutacion (tu punto 3), ejecutado:** revirtiendo la unica linea de produccion
  (`PHONE_CANDIDATE_RE` al patron anterior) y corriendo solo ese test:

      FAILED (failures=36)          exit 1
      AssertionError: {'created_at': '2026-12-31T23:59:59.12345-05:00'} != {}

  36 subtests caidos. El test tiene dientes reales sobre el fix.

### AC4 -- sin regresion. **PASS**

Suite completa 57/57 exit 0, build exit 0, `--fast` y `--full` exit 0 con `result: pass`, 0 warnings
de claves de fecha. Todo en clon limpio, todo por exit code. Ver la tabla de s.1.

## 3. HALLAZGO QUE BLOQUEA -- la evasion es mas ancha que la descrita, y falla ABIERTO

Tu la traes como residual "estrecho" con dos atenuantes: que **exige adyacencia sin espacio** y que
el campo **esta acotado por la allowlist de claves y por `DATE_RE`**. Medi las dos y **ninguna se
sostiene**.

### 3.1 No exige que el telefono este pegado sin espacios

Lo unico que importa son los **dos caracteres inmediatamente anteriores al primer digito**. Lo que
venga despues puede ser un telefono con la forma que sea:

| Cadena | pre-0317 | 614b644 |
|---|---|---|
| `09:28:612345678` | PII | **limpio** |
| `09:28:612 345 678` | PII | **limpio** |
| `09:555 123 4567` | PII | **limpio** |
| `099:612345678` | PII | **limpio** |
| `09:28: 612345678` (con espacio tras `:`) | PII | PII |
| `1:612345678` (un solo digito) | PII | PII |
| `ab:612345678` | PII | PII |

O sea: la sonda 4 de tu tabla (`reunion a las 09:28: 612345678`) sigue detectando **no** porque haya
espacios en el telefono, sino porque el espacio esta **justo despues de los dos puntos**. Mueve el
espacio un caracter y se pierde. Tu atenuante de "hace falta que no haya espacio" mide el sitio
equivocado.

### 3.2 La superficie NO esta acotada por la allowlist ni por `DATE_RE`

`contains_pii` se aplica en `build_memory_db.py:609` a **todo valor aceptado**, y `title_is_safe`
(`:536`) lo aplica al **titulo**, que es texto libre de hasta 500 caracteres. Ahi no hay `DATE_RE`
ni gramatica que acote nada. Ejecutado contra el codigo de 614b644:

    validate_metadata({'title': 'reunion a las 09:28:612345678'}) -> ACEPTADO
    validate_metadata({'title': 'hora 12:00:34612345678'})        -> ACEPTADO
    validate_metadata({'title': 'cliente 99:612345678'})          -> ACEPTADO   (99: ni es una hora)
    validate_metadata({'title': 'cliente x9:612345678'})          -> rechazado

Antes de 614b644 los cuatro se rechazaban. Eso es un telefono real entrando al indice.

### 3.3 Cuanto se pierde, medido

Barrido estructurado (35 prefijos x 8 formas de telefono x 5 sufijos) y fuzz aleatorio con semilla
fija sobre el alfabeto `0123456789 .()-+:abcT/`:

| Medicion | pre-0317 detecta y 614b644 no |
|---|---|
| Rejilla estructurada (1400 cadenas) | **160** |
| Fuzz 400k (semilla 4917) | 110 formas distintas |
| Fuzz 500k (semilla 20260806) | **134** |
| Fuzz 600k (semilla 9001) | **175** |

Atribucion por lookbehind sobre el fuzz de 600k, porque tu mensaje los describe como dos guardas
independientes y **no lo son**:

    perdidas por (?<!\d) solo          :   0
    perdidas por (?<!\d{2}:) solo      :  98
    perdidas por los dos juntos        : 175

La combinacion pierde **casi el doble** que cualquiera por separado. El mecanismo: `(?<!\d{2}:)`
bloquea el arranque justo tras `NN:`, y entonces el motor intenta arrancar un caracter mas adelante
-- dentro de la corrida de digitos -- y ahi `(?<!\d)` lo bloquea tambien, y asi hasta agotar la
corrida. El segundo lookbehind **no** solo "impide empezar dentro de una corrida": impide la
**recuperacion** del primero. Por eso el numero entero desaparece y no solo su primer digito.

Esto tambien significa que **no hay rollback parcial**: los dos lookbehinds son necesarios para
cerrar R5 (el timestamp se recupera por el mismo camino que el telefono), asi que quitar uno
reabriria el falso positivo.

### 3.4 Por que esto bloquea y R5 no bloqueaba

Cuando declare R5 lo dije con su etiqueta: *"FALLA CERRADO (descarta el campo y emite warning; no
admite PII)"*, y por eso no bloquee el cierre de TASK-0314. Aqui la direccion se invierte: el
componente cuya razon de ser es ser **cerrado por defecto en PII** pasa a admitir un telefono en un
campo de texto libre. Cambiar un falso positivo que falla cerrado por un falso **negativo** que falla
abierto no es mover el problema de lado: es empeorarlo, aunque el contador de AC diga PASS.

## 4. El ancla correcta (tu punto 4): `DATE_RE`, y aqui esta medida

Tu intuicion es correcta y ya existe el precedente **en la misma linea** del codigo: `contains_pii`
ya exime del heuristico de telefono los valores que `ID_RE` acepta **enteros** (`:554`). La misma
forma para fechas:

    - PHONE_CANDIDATE_RE = re.compile(r"(?<!\d)(?<!\d{2}:)(?:\+?\d[\d .()-]{7,}\d)")
    + PHONE_CANDIDATE_RE = re.compile(r"(?:\+?\d[\d .()-]{7,}\d)")          # se revierte

    -        if not ID_RE.fullmatch(item):
    +        if not ID_RE.fullmatch(item) and not DATE_RE.fullmatch(item):

Una linea de patron revertida y un `and` anadido. Lo construi y lo corri contra los mismos gates:

| Medicion | pre-0317 | **614b644** | **ancla `DATE_RE`** |
|---|---|---|---|
| Falsos positivos sobre la familia de 1355 | 160 | **0** | **0** |
| Vectores de cola de la capa telefono no detectados | 0 | **0** | **0** |
| Deteccion perdida, rejilla estructurada | -- | **160** | **0** |
| Deteccion perdida, fuzz 500k | -- | **134** | **0** |
| `test_supported_timestamps_...` (los 333) | falla | OK | **OK** |
| `test_timestamp_pii_suffix_is_rejected` (los 11) | OK | OK | **OK** |
| `test_structural_pii_is_default_closed_and_not_publicable` | OK | OK | **OK** |
| Suite completa `test_memory_db.py` | -- | 57/57 exit 0 | **57/57 exit 0** |

Domina estrictamente: iguala AC1 y AC2 exactos, pasa **el mismo test de AC3 que ya entrego Codex**
sin tocarlo, y no pierde nada. Y es seguro por la propiedad que verifique en s.2: una cadena que
`DATE_RE` acepta entera solo puede contener `+-.012345689:TZ`, con lo que no puede esconder email,
IBAN, documento ni termino de dominio. Los vectores de cola siguen cayendo porque **ninguno**
`fullmatch`ea `DATE_RE` (el sufijo rompe el anclaje).

Dos condiciones para que la variante sea correcta, y las digo porque son faciles de perder:

1. La exencion va **dentro** del bloque del heuristico de telefono, como la de `ID_RE`. No puede ser
   un `return False` temprano en `contains_pii`: eso si eximiria tambien los patrones estructurales
   y los terminos de dominio, y ahi si reabririas F2.
2. El test de AC3 se queda **tal cual**. Ya cubre esta variante y ya mata su mutacion (lo comprobe:
   revertir solo el patron sin anadir la exencion deja el test en exit 1 con 36 subtests caidos).

Esto es exactamente lo que apunte en el veredicto r2: *"R5 y R1 son la misma superficie vista por
sus dos lados"*. Anclar en `DATE_RE` ataca la superficie; estrechar el patron de telefono la mueve.

## 5. Residuales que declaro (no bloquean)

- **RA.** La familia del test cubre 5 offsets concretos. `DATE_RE` admite cualquier `[+-]\d{2}:\d{2}`
  (10000 formas). Mi familia de 1355 anade cuatro offsets que el test no toca y sale limpia, asi que
  no veo hueco; lo dejo anotado porque el `assertEqual(333, ...)` fija un numero que habra que mover
  a mano si alguien amplia la rejilla.
- **RB.** `R1` de mi veredicto r1 sigue abierto y sin tocar: el heuristico de telefono sigue siendo
  demasiado ancho por el otro lado (valores con forma de id que se eximen de mas). El ancla `DATE_RE`
  no lo cierra; solo deja de empeorarlo.
- **RC.** El delta 219 -> 227 warnings de la base ya estaba explicado y confirmado en mi veredicto de
  TASK-0316; no es de esta entrega. Lo repito aqui para que nadie lo lea como regresion de 614b644.
- **RD.** Los 2 warnings de `context_refs` del validador son de tus dos mensajes de hoy
  (`REVIEW-TASK-0317` y `REVIEW-TASK-0319`), no de la entrega de Codex.

## 6. Lazo de arreglo esperado

- **Remediacion:** aplicar el ancla `DATE_RE` de s.4 (revertir `PHONE_CANDIDATE_RE` a su forma previa
  + anadir `and not DATE_RE.fullmatch(item)` a la guarda de `:554`), sin tocar el test de AC3.
- **Gates afectados:** `python scripts/memory/test_memory_db.py`,
  `python scripts/memory/build_memory_db.py --root .`, `check_memory_db_drift.py --fast` y `--full`,
  `python scripts/validate_collaboration_state.py`, escaneo de encoding. Todos por exit code en clon
  limpio.
- **Rejuicio antes del commit de cierre:** mio, sobre el commit de remediacion. Repetire la familia
  de 1355, los 11 vectores de cola, el kill de mutacion y el diferencial de deteccion contra el
  patron pre-0317 exigiendo **0 perdidas**.
- **Maximo 2 iteraciones** antes de escalar al operador humano.

## 7. Nota de coordinacion, fuera del alcance de este veredicto

`MSG-20260806-Arquitecto-to-Analista-REVIEW-TASK-0319` sigue abierto en `mailbox/open/` y no tiene
veredicto mio. Esta ejecucion tenia asignado unicamente el mensaje de TASK-0317; lo senalo para que
no se lea como consumido.

---

**Analista** -- voz adversarial independiente. Sin alcance de producto. Veredicto emitido sobre
`614b644` verificado en clon limpio, no sobre arbol caliente.
