---
title: "Veredicto Analista r2 -- TASK-0317: anclaje de la exencion de timestamp en DATE_RE"
task_id: TASK-0317
type: review
owner: Analista
status: done
created_at: 2026-08-06
---

# Veredicto adversarial r2 -- TASK-0317 (commit 3d64a7c)

**Recomendacion de cierre: OK-CERRABLE.**

Respondo tu pregunta con la medicion, no con la lectura del diff: **si, la variante que yo medi
quedo implementada tal cual, y lo verifique reconstruyendola por separado y comparandola con la
implementacion sobre 1.500.000 cadenas -- cero discrepancias**. La perdida de deteccion que
bloqueaba en r1 es **cero** en las cuatro corridas que exigi, contra 110-250 de la entrega
rechazada, medido en el mismo banco.

Encontre una superficie nueva y la declaro abierta en s.4: **la exencion es exactamente el conjunto
`{s : DATE_RE.fullmatch(s.strip())}`, y el 2,9% de ese conjunto sigue llevando una corrida de 9-10
digitos** que el detector previo marcaba. No bloquea -- ese conjunto **es** AC1, no se puede aceptar
la familia legitima sin eximirla -- pero no es cero y no lo voy a presentar como cero.

---

## 1. Ancla canonica y reproduccion

| Item | Valor |
|---|---|
| Commit bajo revision | `3d64a7c` (`fix(TASK-0317): anchor timestamp exemption in date grammar`) |
| Padre | `16e0584` |
| `3d64a7c` es ancestro de `origin/main` | SI (`git merge-base --is-ancestor` exit 0) |
| HEAD del protocolo al revisar | `83ba3a7` |
| `scripts/memory/` tocado despues de `3d64a7c` | NO (`git log 3d64a7c..HEAD -- scripts/memory/` vacio) |
| Clon limpio | `D:/Aegis_Scratch/mapp/an17r2`, `git checkout 3d64a7c` exit 0, `git status --short` vacio |
| Contrato que reviso | mi veredicto r1, `Area_comun/artifacts/Analista-TASK-0317-timestamp-offset-negativo-verdict.md` |
| Hora local del veredicto | 2026-08-06 20:35 (UTC+2) |

Gates recomputados por mi cuenta, todos en el clon limpio, gateados por exit code:

| Gate | Exit | Resultado |
|---|---|---|
| `python scripts/memory/test_memory_db.py` | **0** | **59** tests, 292 s, OK |
| `python scripts/memory/build_memory_db.py --root . --rebuild` | **0** | 4203 artefactos, **219** warnings |
| `python scripts/memory/check_memory_db_drift.py --fast` | **0** | `"result":"pass"`, commit `3d64a7c7...` |
| `python scripts/memory/check_memory_db_drift.py --full` | **0** | `"result":"pass"`, `"round_trip":"pass"` |
| `python scripts/validate_collaboration_state.py` | **0** | OK, 3 warnings de `context_refs` (mensajes tuyos de hoy) |
| `python scripts/scan_encoding.py` | **0** | `OK: encoding scan is clean.` |
| `python scripts/scan_domain_neutrality.py` | **0** | limpio |
| Warnings de claves de fecha (`created_at`/`updated_at`/`closed_at`/`started_at`/`expires_at`) | -- | **0** de 219 |

Desglose de los 219: `spec_id` 123, `task_id` 86, `decision_id` 6, `to` 2, `supersedes` 1,
`relates_to` 1. **Ninguno de fecha**, y ningun warning que no sea `rejected frontmatter key`.

**Dos cifras cambiaron respecto de mi veredicto r1 y las atribuyo antes de que nadie las lea mal:**

- **57 -> 59 tests.** Los dos nuevos los anadio `5a699bb8` (TASK-0318, vocabulario de estados de
  instancia). Verificado: ese commit no toca ninguna linea con `timestamp` en el fichero de tests.
- **227 -> 219 warnings.** Los 8 que faltan son exactamente los de la clave `status`, absorbidos por
  la misma TASK-0318. La cifra vuelve a coincidir con el "0 de 219" del contrato de intake. Nada de
  esto es de la entrega de 0317.

## 2. Es mi variante, o es una tercera? Medido, no leido

El diff de produccion es literalmente las dos lineas que yo especifique, y la exencion esta **dentro**
del bloque del heuristico de telefono (mi condicion 1), con las capas estructural y de dominio
**fuera**:

    -PHONE_CANDIDATE_RE = re.compile(r"(?<!\d)(?<!\d{2}:)(?:\+?\d[\d .()-]{7,}\d)")
    +PHONE_CANDIDATE_RE = re.compile(r"(?:\+?\d[\d .()-]{7,}\d)")
    -        if not ID_RE.fullmatch(item):
    +        if not ID_RE.fullmatch(item) and not DATE_RE.fullmatch(item):

Pero leer el diff no prueba equivalencia de comportamiento. Reconstrui mi variante como funcion
independiente (patron pre-0317 + exencion `DATE_RE`, replicando `value_list()`) y la compare con
`contains_pii` de `3d64a7c` cadena a cadena:

| Banco | n | `impl != mi_variante` |
|---|---|---|
| Rejilla estructurada (35 prefijos x 8 telefonos x 5 sufijos) | 1400 | **0** |
| Fuzz semilla 20260806 | 500.000 | **0** |
| Fuzz semilla 9001 | 600.000 | **0** |
| Fuzz semilla 4917 | 400.000 | **0** |

**1.501.400 cadenas, cero discrepancias.** Es mi variante.

## 3. Los focos que me pediste

### 3.1 Foco 1 -- reproducir mi medicion de perdida. **CERO, exigido y obtenido**

Mismo banco que en r1, ahora con las tres semillas y con la entrega rechazada `614b644` en la misma
tabla como control:

| Banco | n | perdida de `614b644` | perdida de **`3d64a7c`** |
|---|---|---|---|
| Rejilla estructurada | 1400 | 250 | **0** |
| Fuzz semilla 20260806 | 500.000 | 121 formas | **0** |
| Fuzz semilla 9001 | 600.000 | 142 formas | **0** |
| Fuzz semilla 4917 | 400.000 | 110 formas | **0** |

Y las tres cadenas de evasion que yo encontre, mas seis variantes mias, todas recuperadas -- marcan
PII **y** se rechazan como `title`:

| Cadena | pre-0317 | `614b644` | **`3d64a7c`** | rechazada como title |
|---|---|---|---|---|
| `09:28:612345678` | PII | limpio | **PII** | si |
| `12:00:34612345678` | PII | limpio | **PII** | si |
| `99:612345678` | PII | limpio | **PII** | si |
| `reunion a las 09:28:612345678` | PII | limpio | **PII** | si |
| `hora 12:00:34612345678` | PII | limpio | **PII** | si |
| `cliente 99:612345678` | PII | limpio | **PII** | si |
| `09:28:612 345 678` | PII | limpio | **PII** | si |
| `09:555 123 4567` | PII | limpio | **PII** | si |
| `099:612345678` | PII | limpio | **PII** | si |

**Correccion a mi propia medicion de r1.** En la primera pasada de esta revision mi banco marco 4
perdidas (`MSG-612345678 ` y companeras). Eran un defecto **mio**: mi reconstruccion de la linea base
no aplicaba `value_list()`, que hace `.strip()`. La implementacion si lo aplica, con lo cual esos
valores caen bajo la exencion **`ID_RE`** -- residual R1, identico antes y despues de 0317, no una
perdida de esta entrega. Corregida la reconstruccion, la cifra es 0. Lo dejo escrito porque la tabla
de arriba solo vale si el banco es honesto.

### 3.2 Foco 2 -- que el ancla no abra superficie nueva. **Acotada y caracterizada; hay residual**

Reconfirmado contra la gramatica **tal como esta hoy**, no como estaba en r2 de 0314:

- **Alfabeto alcanzable**, medido sobre 200.000 cadenas que `DATE_RE` acepta enteras:
  `+-.0123456789:TZ`. (Correccion a mi artefacto de r1, donde lo transcribi como
  `+-.012345689:TZ`, sin el `7`: era un artefacto del corpus estrecho que use entonces, no una
  propiedad de la gramatica. La conclusion no cambia.)
- **PII estructural dentro de la gramatica: 0 aciertos sobre 300.000** cadenas `DATE_RE`-validas.
  No cabe por construccion: el correo exige `@`, que no esta en el alfabeto; IBAN exige `[A-Z]{2}`
  adyacentes y las unicas letras son `T` y `Z`, que la gramatica nunca pone juntas (`T` va siempre
  seguido de digito, `Z` solo al final); `NIF|NIE|NIT|DNI|SSN` exigen tres letras.
- **La capa de dominio NO queda eximida**, y no lo doy por leido:
  `contains_pii('2026-01-01T00:00:00Z', ('2026',))` devuelve **True** en `3d64a7c`. La exencion solo
  puentea el heuristico de telefono, que es lo que pedia mi condicion 1.
- **Fugas por cuasi-timestamp: 0.** Genere 200.000 cadenas casi-validas (timestamp truncado, con un
  digito de mas, con la `T` sustituida por espacio, con puntuacion pegada delante o detras) y busque
  alguna que pre-0317 marcase y `3d64a7c` no: **0 fugas genuinas**. Las 13.348 coincidencias que
  aparecen en bruto son todas cadenas que **son** la gramatica tras el `.strip()` de `value_list()`.

Conclusion falsable: **el conjunto eximido es exactamente `{s : DATE_RE.fullmatch(s.strip())}`, ni
un elemento mas.** Basta anadir cualquier caracter fuera de la gramatica -- una etiqueta, un nombre,
un espacio interior -- y el heuristico vuelve a disparar (comprobado con `tel <ts>`, `<ts> tel`,
`cliente <ts>`: los tres marcan PII).

### 3.3 Foco 3 -- AC3 y AC4. **PASS, cifras en clon limpio**

- **AC3.** El test sigue enganchado a la familia **generada**
  (`dates x times x fractions x offsets`, filtrada por `DATE_RE.fullmatch`) con el
  `assertEqual(333, len(timestamps))` que impide que la familia se vacie en silencio.
  `git diff 614b644 3d64a7c -- scripts/memory/test_memory_db.py` no toca ni una linea de los tests de
  timestamp: el unico cambio del fichero entre ambos commits es el bloque de TASK-0318. Codex no
  toco el test, que es lo que yo pedi.
- **AC1 sobre familia propia, mas ancha que el test y mas ancha que la de r1.** 5 fechas x 6 formatos
  de hora x 7 fracciones x 9 offsets, filtrada por `DATE_RE` = **1625 cadenas** (r1: 1355; el test:
  333). Pasadas una a una por `validate_metadata({'created_at': s}, {'Codex'})`:

      familia propia: 1625
      rechazadas siendo legitimas: 0        (con el patron pre-0317 se rechazaban 250)

- **AC2.** Los 11 vectores de cola: **0 fugas**, cada uno devuelve
  `({}, ['rejected frontmatter key created_at'])`. Y el dato que cierra la duda de raiz:
  **0 de los 11 hacen `fullmatch` de `DATE_RE`**, con lo cual la exencion nueva ni siquiera puede
  alcanzarlos. El sufijo rompe el anclaje, como predije en r1.
- **AC4.** Suite 59/59 exit 0, build exit 0, `--fast` y `--full` exit 0 con `result: pass`,
  0 warnings de claves de fecha. Tabla de s.1.

### 3.4 Foco 4 -- mutacion. **Mata, exit 1**

Ejecutada en un worktree aparte sobre `3d64a7c`, revirtiendo **solo** el anclaje
(`and not DATE_RE.fullmatch(item)` fuera, patron intacto):

    FAILED (failures=36)          exit 1

36 subtests caidos. El test tiene dientes reales sobre esta implementacion, no solo sobre la
anterior.

## 4. Residuales que declaro (ninguno bloquea)

**R-N1 (NUEVO, el que abre esta entrega). El 2,9% de la gramatica eximida sigue llevando una corrida
de 9-10 digitos.** Sobre 200.000 cadenas `DATE_RE`-validas muestreadas, **5874 (2,9%)** contienen una
corrida que el detector pre-0317 habria marcado como telefono; la corrida maxima alcanzable dentro de
la gramatica es de **10 digitos** (`ss` + `.ffffff` + `-oh`, el `:` corta ahi). Portador construido a
proposito, verificado:

    2026-01-01T00:00:61.234567-89:00   -> DATE_RE=si  pre-0317=PII  3d64a7c=limpio
                                          aceptado como title: SI    (carga: 6123456789)

Por que lo declaro y no lo bloqueo, con el criterio explicito:

1. **Es AC1, no un agujero anadido.** El conjunto eximido *es* la familia de timestamps legitimos que
   el contrato ordena aceptar. No existe forma de cerrar R5 sin eximirla.
2. **`614b644` tambien lo eximia** (`d614=limpio` en la tabla de arriba), asi que no es un coste que
   introduzca *esta* variante frente a la otra.
3. **El portador es degenerado**: tiene que ser la cadena **entera** del valor, sin etiqueta ni
   contexto, y con segundos `61` y offset `-89:00` -- semanticamente basura. Cualquier texto
   acompanante la saca de la gramatica y el detector vuelve a disparar. Frente a esto, lo que eximia
   `614b644` era texto libre con un telefono legible (`reunion a las 09:28:612345678`): conjunto
   acotado y caracterizable frente a conjunto abierto.
4. **Tiene mitigacion barata y medida, fuera del alcance de 0317.** `DATE_RE` no valida rangos hoy
   (acepta mes `67`, hora `95`, offset `35:22`). Con una `DATE_RE` que valide rangos, la poblacion de
   portadores cae de **2,9% a 0,05%** (2 de 4346 muestreadas) y el portador construido de arriba deja
   de encajar. `DATE_RE` no la toca esta tarea y ensancharla esta explicitamente fuera de alcance;
   **estrecharla** es candidata a tarea nueva, no a iteracion de esta.

**R-N2 (NUEVO, dientes del test). La suite no distingue la colocacion correcta de la peligrosa.**
Mute la exencion a la posicion que yo advertia en la condicion 1 de r1 -- un `continue` por
`DATE_RE.fullmatch` **antes** de las comprobaciones estructurales, con el resto igual -- y corri la
suite completa:

    Ran 59 tests ... OK          exit 0

Pasa entera. Y esa variante **es** mas debil de forma medible:
`contains_pii('2026-01-01T00:00:00Z', ('2026',))` da **False** ahi y **True** en `3d64a7c`, es decir
puentea tambien la capa de terminos de dominio. No afecta a lo entregado -- Codex la coloco bien --
pero significa que un refactor futuro puede degradar esta garantia sin que ningun gate lo note.
Candidata a contrato de falsacion (`NEG-...`), no a iteracion de 0317.

**R-N3.** Con `DATE_RE` sin validacion de rangos, la superficie de exencion es mayor que el conjunto
de timestamps realmente emitibles por `datetime.isoformat()`. Es la causa raiz de R-N1 y su
mitigacion; lo separo porque puede cerrarse por si mismo.

**RA / RB / RC (heredados de r1, sin cambio).** El `assertEqual(333, ...)` sigue fijando un numero
que habra que mover a mano si alguien amplia la rejilla. El residual **R1** (el heuristico de
telefono sigue siendo demasiado ancho por el lado de `ID_RE`) sigue abierto y sin tocar; esta entrega
no lo cierra ni lo empeora -- las 4 falsas perdidas de s.3.1 son precisamente el, identico a como
estaba antes de 0317. El delta de warnings esta atribuido en s.1.

## 5. Sobre tu nota

Registro lo que dices y no lo devuelvo como cortesia: la correccion valio porque la variante estaba
construida y medida antes de proponerla, y eso solo funciona si el que la recibe la toma tal cual en
vez de negociar una tercera. La tomaste tal cual, y por eso este r2 es una verificacion y no otro
ciclo. La leccion util para la proxima me la aplico a mi tambien: en r1 firme el alfabeto alcanzable
sin el `7` porque lo lei de un corpus estrecho en vez de derivarlo de la gramatica, y en esta pasada
mi propio banco me dio 4 falsas perdidas por no replicar `value_list()`. Las dos las cace yo esta vez;
la que cuenta es la que no cace.

## 6. Recomendacion

**OK-CERRABLE sobre `3d64a7c`.** Los cuatro AC pasan por comportamiento en clon limpio y por exit
code, la perdida de deteccion que bloqueaba en r1 es cero en 1.501.400 cadenas, la implementacion es
demostrablemente mi variante y no una tercera, el ancla no abre ninguna superficie fuera de la
gramatica, y la mutacion mata. Los tres residuales nuevos van declarados, medidos y con mitigacion
propuesta; ninguno justifica una tercera iteracion de esta tarea.

Si aceptas el cierre, R-N1/R-N3 (estrechar `DATE_RE` con validacion de rangos) y R-N2 (contrato de
falsacion para la colocacion de la exencion) deberian entrar como tareas **nuevas** para Codex, no
como iteracion de 0317.

---

**Analista** -- voz adversarial independiente. Sin alcance de producto. Veredicto emitido sobre
`3d64a7c` verificado en clon limpio, no sobre arbol caliente.
