---
artifact_id: Analista-TASK-0368-r4-pointer-discarded-on-missing-status-verdict
task_id: TASK-0368
type: adversarial_review
author: Analista
status: final
created: 2026-08-14
verdict: CHANGE-REQUIRED
---

# Veredicto adversarial -- TASK-0368 remediacion 4 (normalizacion de un solo punto)

**CHANGE-REQUIRED, y con esto agoto mi lazo: ESCALO AL OPERADOR HUMANO.**

Empiezo por tu pregunta, porque la respuesta es un si y decide el veredicto.

> *"El rojo que yo medi, lo produce la deteccion de vigencia o solo el drift de arbol-contra-blob --
> es decir, existe todavia una entrada que cambie la clasificacion SIN enrojecer ninguna puerta?"*

**Tu rojo era trivial: lo produjo el drift de arbol-contra-blob, no la vigencia.** Repeti tu prueba
con el cambio COMMITEADO y con su trailer, y las seis puertas salen en **verde** con el conteo
**quieto en 110**. Eso es exactamente lo que debe pasar y acredita tu mitad buena: `Proposed` ya no
sube el censo, ni con rojo ni sin el. No hay clasificacion erronea que cazar en esa familia, asi que
no hace falta ninguna puerta que la cace.

**Y si: queda una entrada que cambia la clasificacion sin enrojecer NADA.** No es una grafia. Es una
**omision**. Una decision que declara `superseded_by` y **no declara `status`** se clasifica como
**vigente**: el puntero de supersesion -- la senal primaria de AC1 -- se descarta en silencio.

    e2e sobre el corpus real, clon limpio de 95584c3a, cambio COMMITEADO con trailer:
    borro UNA linea (`status: accepted`) de DECISION-0071, que conserva
    `superseded_by: [DECISION-0081]` y un `status_note` que dice literalmente
    "SUPERSEDED por DECISION-0081 ... No es gobierno vivo".

    active_decision_count   110 -> 111
    las SEIS puertas        exit 0, 0, 0, 0, 0, 0
    unico rastro            "decision currentness status is missing" (1 aviso entre 232)

Y no lo hereda de antes de la tarea: **lo introdujo la propia cadena de remediacion de TASK-0368**,
en `31867185` (r2). Con la entrega original (`94aa4ca3`) la misma prueba **no mueve el censo**.

---

## 1. Ancla canonica y reproduccion

| Elemento | Valor |
|---|---|
| Commit bajo revision | `95584c3a1b9dafce82df7c9c9675ace19a0745b5` |
| HEAD del protocolo al revisar | `a47c7973` (origin/main) |
| Linea base A (entrega original de la tarea) | `94aa4ca3` |
| Linea base B (pre-r3) | `7980bfcd` |
| Commit que introduce el defecto | `31867185` (remediacion 2) |
| Alcance | SOLO hub. Sin producto: no gateo `npm test`. |
| Clon limpio | `git clone -s -n <repo> <dst> && git checkout 95584c3a` |
| Raiz de scratch | `D:/Aegis_Scratch/mapp/` (DECISION-0104) |
| Hora | 2026-08-14 13:38 local (UTC+2) |

### Las SEIS puertas, por exit code, en clon limpio de `95584c3a`

| # | Comando | Exit |
|---|---|---|
| 1 | `python scripts/memory/check_memory_db_drift.py --root . --fast` | **0** |
| 2 | `python scripts/memory/test_memory_db.py` | **0** |
| 3 | `python scripts/validate_collaboration_state.py --root .` | **0** |
| 4 | `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` | **0** |
| 5 | `python scripts/scan_encoding.py --root .` | **0** |
| 6 | `python scripts/scan_domain_neutrality.py --root .` | **0** |

Seis de seis en verde sobre la entrega. Puerta 4: `NEG-MEMORY-CURRENT-DECISION-PROPERTY
boundaries=12` (eran 10).

Censo re-derivado por mi con las funciones de produccion sobre `95584c3a`: **112 ficheros de
decision, `active=110`, `superseded=2`, `is_current=1` en 110**. Un unico aviso de vigencia
(DECISION-0059, la que no declara `status`) entre **232** avisos. Coherente con lo declarado.

---

## 2. Lo que r4 SI cierra, y lo cierro yo por conducta

Mis dos criterios de aceptacion de r3 estan **los dos cumplidos**. Lo digo antes que el bloqueante
porque es verdad y porque el arreglo esta bien hecho.

### 2.1 La normalizacion es de UN SOLO punto, y por construccion

No coinciden hoy por casualidad: **leen el mismo objeto**. `load_artifacts:978-980` casefoldea y
**escribe de vuelta** `metadata["status"]`; la puerta compara la variable local (que ES ese valor) y
`decision_policy_state:1195` lee `metadata.get("status")` del mismo diccionario. Verificado:

- `grep casefold scripts/memory/*.py` -> **un solo** `casefold()` sobre status, en la linea 979. El
  de `decision_policy_state` desaparecio; el de la linea 601 es de validacion de la politica, no de
  un artefacto.
- **Todos** los llamantes de `decision_policy_state` pasan metadata salido de `load_artifacts`:
  `policy_row:1216` (`artifact.metadata`) y `check_memory_db_drift.py:34` (`artifact.metadata`). No
  hay un tercero.
- Cero variantes de caja anadidas al allowlist: lo confirmo. `configured_status_values` sigue siendo
  `CORE | extra | current_statuses | non_current_statuses` (37 valores), y `classified` es
  subconjunto suyo -- comprobado por evaluacion, `classified <= status_values` es `True`. Lo que r4
  guarda en la columna `status` es siempre un miembro del allowlist en su forma canonica, asi que la
  escritura de vuelta **no abre una via de admision** por saltarse el allowlist.

### 2.2 La familia de la caja muere entera, y por criterio y no por lista

Ejercite la familia COMPLETA que promete el criterio, no el ejemplo. Los 9 estados clasificados por
4 formas de caja cada uno, mas exoticos:

    forma                          puerta   estado resultante
    los 9 x {minus, MAYUS, Capital, mIxTa}  silent   identico a la forma canonica  (36/36)
    sUpErSeDeD, prOposed                    silent   superseded                    (correcto)
    'superseded' con s larga U+017F         silent   superseded                    (casefold canonico)
    ' superseded', 'superseded ', \t, \n    RAISE    ruta + valor
    homoglifo cirilico, ancho completo      RAISE    ruta + valor
    combinante, ancho cero, '', '   '       RAISE    ruta + valor
    'retired','obsolete','withdrawn'        RAISE    ruta + valor
    U+1E9E inicial (casefold -> 'ssuper')   RAISE    ruta + valor

**Ninguna forma de caja aterriza como `active` debiendo ser `superseded`.** No es una lista mas
larga: es `casefold()`, una funcion canonica. La grieta de r3 esta cerrada por construccion.

E2E sobre el corpus real (tu prueba, commiteada con trailer): `DECISION-0078` `proposed` ->
`Proposed` deja `active_decision_count = 110` y las seis puertas en verde. **Ni sube el censo ni
enrojece nada, porque no hay nada que cazar.** Antes de r4 la misma mutacion daba 110 -> 111.

### 2.3 Los mutantes, re-ejecutados porque r4 los toca

r4 reescribio `decision_policy_state` entera y cambio los asertos de M2, asi que los corri todos
otra vez contra el runner declarado:

| Mutante sobre produccion | Exit | Resultado | Aserto que lo mata |
|---|---|---|---|
| M0 control | 0 | verde | -- |
| M1 clase de estado ignorada | **1** | MUERE | `assertEqual("superseded", rows["DECISION-PROPOSED"][1])` |
| M2 puntero de supersesion ignorado | **1** | MUERE | `assertEqual("superseded", rows["DECISION-OLD"][1])` |
| M7 ausente pasa a NO vigente | **1** | MUERE | `assertEqual("active", rows["DECISION-MISSING-STATUS"][1])` |
| M8 `raise` de `load_artifacts` neutralizado | **1** | MUERE | `with self.assertRaisesRegex(...)` |
| **M9 (nuevo, mio) la normalizacion de r4 anulada** | **1** | **MUERE** | `rows["DECISION-PROPOSED-CASE"]` |

M9 importa: el arreglo de r4 **tiene su propio guardian discriminante**. Si alguien borra el
`casefold()`, el runner declarado se pone rojo. No es un arreglo desnudo.

### 2.4 El inventario: puesto al dia, y la declaracion esta ATADA a la realidad

`assertNotEqual(hot, mutant_hot)` -- la tautologia que documente en r2 y r3 -- **ya no se declara**.
En su lugar entra `assertNotIn("DECISION-OLD", production_hot)`, que es el aserto discriminante de
verdad: si produccion ignora el puntero, `DECISION-OLD` entra en `production_hot` y el aserto cae
(M2 lo confirma). Tambien entra la variante `DECISION-PROPOSED-CASE`. De 10 a 12 fronteras.

Y comprobe que la declaracion no es decorativa: mute UNA cadena declarada a un texto inexistente y
la puerta 4 responde

    INVENTORY_EXIT = 1
    ERROR: NEG-MEMORY-CURRENT-DECISION-PROPERTY: assertion boundary not found beside the test

La puerta verifica **presencia**. Ojo con lo que eso NO verifica: ver residual 5.1.

---

## 3. El bloqueante: el puntero se descarta cuando falta el `status`

### 3.1 Mecanismo

`decision_policy_state` (`build_memory_db.py:1192-1207`) corta antes de mirar el puntero:

    status = metadata.get("status")
    if status is None:
        missing_status = mapping["missing_status"]
        if missing_status == "current_with_warning":
            return mapping["current"]        # <-- sale AQUI, sin leer superseded_by
        raise ...
    ...
    return non_current if value_list(metadata.get("superseded_by")) or declared_non_current else current

La politica atestada declara **dos campos independientes**:

    "non_current_when": "superseded_by_present_or_status_declared_non_current"
    "missing_status":   "current_with_warning"

`non_current_when` es una **disyuncion**: el puntero por si solo basta. `missing_status` dice que
hacer con el ESTADO cuando falta, es decir que el termino `declared_non_current` vale falso -- **no**
que vete el otro termino de la disyuncion. Produccion lo implementa como un cortocircuito que anula
la disyuncion entera. **Produccion contradice su propia politica atestada.**

### 3.2 Prueba falsable, sobre PRODUCCION SIN MUTAR

Anadi al runner declarado UNA fixture y UN aserto, sin tocar produccion:

    write("Area_comun/decisions/DECISION-POINTER-NO-STATUS.md",
          "---\ndecision_id: DECISION-POINTER-NO-STATUS\nsuperseded_by: DECISION-ACCEPTED\n---\n")
    self.assertEqual("superseded", rows["DECISION-POINTER-NO-STATUS"][1])

    python -m unittest ...test_current_decision_is_attested_property_not_status_literal
    - superseded
    + active
    FAILED (failures=1)          exit 1

No es un mutante que sobreviva: es produccion clasificando mal una entrada que la politica atestada
clasifica bien. La fixture `DECISION-MISSING-STATUS` del runner **no tiene puntero**, y
`DECISION-OLD` **si tiene status**; nadie cruza los dos ejes, asi que el hueco es invisible para la
suite. Yo tampoco lo cruce en r2 ni en r3 cuando di el fix 3 por bueno: la falta es tambien mia.

### 3.3 Las dos direcciones, medidas contra la linea base y en el mismo commit

Misma prueba, mismo fichero, control y mutante dentro de cada commit:

    commit                          control   probe (borro `status:`, puntero intacto)   delta
    94aa4ca3 (entrega original)       109              109                                0   puntero respetado
    95584c3a (r4, bajo revision)      110              111                               +1   puntero descartado

`89af4fdb` (r1) tampoco tenia el cortocircuito. `git log -S 'if status is None:'` lo fija en
**`31867185` (r2)**. Es una **regresion de la propia cadena de TASK-0368**, no un residuo heredado.

### 3.4 Por que es bloqueante y no residual

Por la letra de la tarea, no por una regla mia:

- **AC6**: *"ninguna decision pasa a vigente sin que el criterio de AC1 lo explique"*. Esta pasa a
  vigente y el criterio de AC1 dice lo contrario.
- **AC4**: *"si el criterio la clasifica mal, tiene que decirlo RUIDOSAMENTE, no en silencio"*. Seis
  puertas verdes.
- **El negativo declarado de la propia tarea**: *"Ignoring **either** supersession or a declared
  non-current status lets unsafe policy back live rules."* Produccion ignora la supersesion.
- **AC1 cita el dato que lo informa**: *"exactamente UNA tiene `superseded_by` no vacio
  (DECISION-0071 -> DECISION-0081)"*. Esa unica decision no vigente por puntero del corpus tiene su
  vigencia colgando de una linea `status:` que **no es obligatoria**: DECISION-0059 demuestra que
  una decision sin `status` solo produce un aviso, nunca un error.

Y la via de entrada no es una grafia rara: es **omitir una clave opcional**. El camino de autoria
natural -- "marco esta decision como superada apuntando a su sucesora" -- sin escribir `status:`
produce una decision **viva**. Es mas barato de cometer que la mayuscula de r3.

---

## 4. Tabla vector por vector

| Vector | Lo que pediste comprobar | Veredicto | Evidencia |
|---|---|---|---|
| Tu rojo: vigencia o drift trivial? | separarlos | **RESUELTO: drift trivial** | con el cambio commiteado, seis puertas exit 0 y censo 110 quieto |
| Normalizacion de UN SOLO punto | por construccion, no por coincidencia | **PASS** | un unico `casefold()` (l.979) + escritura de vuelta a `metadata`; los 2 unicos llamantes reciben metadata de `load_artifacts` |
| No es una lista disfrazada | cero variantes en el allowlist | **PASS** | allowlist intacto (37); familia de 9x4 + exoticos medida por conducta |
| Familia de caja clasifica igual | toda la familia | **PASS** | 36/36 identicas a la forma canonica; el resto RAISE con ruta y valor |
| El censo no sube en silencio | `Proposed` sobre fichero real | **PASS** | 110 -> 110 commiteado; antes de r4 daba 111 |
| Inventario declarado al dia | quitar la tautologia, declarar lo que mata a M2 | **PASS** | `assertNotEqual(hot, mutant_hot)` fuera; `assertNotIn(...)` dentro; boundaries 10 -> 12; presencia atada (exit 1 al mutarla) |
| M1/M2/M7/M8 siguen muriendo | solo si r4 los toca (los toca) | **PASS** | los 4 en exit 1; control en 0 |
| El arreglo de r4 tiene guardian | -- | **PASS** | M9: anular el `casefold()` pone el runner en exit 1 |
| **Puntero de supersesion + `status` ausente** | tu pregunta | **SLIP -- BLOQUEANTE** | e2e real 110 -> 111 con seis puertas verdes; prueba falsable en produccion sin mutar: `- superseded / + active` |

---

## 5. Residuales declarados (no bloqueantes)

1. **La puerta 4 verifica PRESENCIA, no discriminacion.** Entre las 12 fronteras declaradas hay una
   que **no puede fallar nunca**: `self.assertIn("DECISION-OLD", same_population_pointer_mutant)`,
   siendo `same_population_pointer_mutant = production_hot | {"DECISION-OLD"}`. Es la identidad
   `X in (S | {X})`, cierta para todo `S` y para toda conducta de produccion. Salio una tautologia y
   entro otra distinta; la diferencia importante -- y por eso no bloqueo -- es que **esta vez el
   aserto que de verdad mata a M2 tambien esta declarado**, cosa que en r2 y r3 no pasaba. Sugerido:
   quitar esa linea del inventario (no del test, donde documenta la intencion).
2. **`active_decision_count` se REPORTA pero no se GATEA.** El drift lo imprime y devuelve `pass`
   con cualquier valor. Toda la deteccion de un censo que se mueve depende hoy de que alguien lea el
   JSON. Es la razon estructural por la que 3.2 es silencioso.
3. **`status` no-cadena** (`status: 2026`, `[superseded]`, `{}`, booleano): cae al camino filtrado,
   `metadata["status"]` queda `None` y clasifica `active` con aviso. Es la **misma puerta** que 3.2:
   si ademas lleva puntero, el puntero tambien se descarta (medido: `status=2026 + ptr -> active`).
   Se cierra con el mismo arreglo.
4. **232 avisos en el corpus real.** Cualquier senal nueva por ese canal nace enterrada. El unico
   rastro de 3.2 es un aviso de esa pila.
5. **`build_memory_db.py:1404`**: `int(metadata.get("status") not in {"superseded","archived"})`
   deriva vigencia de dos literales cableados. Confirmado que es **solo** para filas de
   `agent_memory` (`if artifact.artifact_type == "memory"`), fuera del `scope_routes` declarado.
   Tarea aparte, como dije en r3.
6. **M3 sigue siendo un guardian muerto** (el `raise` interno de `decision_policy_state` es
   inalcanzable porque el de `load_artifacts` dispara antes en los dos llamantes). Sin cambio.
7. No corri `check_memory_db_drift --full`: no esta en el `verification_cmd` de la tarea.

---

## 6. Veredicto, lazo y escalada

**CHANGE-REQUIRED.** Un bloqueante (3.x).

Lo que aceptaria como cerrado, por conducta:

1. **La ausencia de `status` anula el termino del estado, no la disyuncion.** Cuando `status` es
   `None`, `decision_policy_state` debe seguir evaluando `value_list(metadata.get("superseded_by"))`
   antes de devolver `current`. El aviso de `missing_status` se mantiene: informa del estado, no
   decide la vigencia. El mecanismo es del maker; esta es la propiedad.
   **Prueba de aceptacion:** la fixture de 3.2 -- una decision con `superseded_by` y sin `status` --
   debe clasificar `superseded`, y borrar la linea `status:` de `DECISION-0071` sobre el corpus real
   **no debe mover `active_decision_count`** (110 -> 110), commiteado con trailer.
2. **El negativo permanente cruza los DOS ejes.** Hoy la suite tiene puntero-con-status
   (`DECISION-OLD`) y status-ausente-sin-puntero (`DECISION-MISSING-STATUS`) y ninguna con los dos.
   Que la fixture nueva quede declarada en `boundaries`.

**Puertas afectadas:** las seis. La 2 es la que debe cambiar de signo con la fixture nueva; la 1 es
la que debe dejar el censo quieto bajo el probe de `DECISION-0071`.

**Lazo:** declare maximo 2 iteraciones. **Las he gastado las dos (r3 y r4).** Por tanto, y como
acordamos, **ESCALO AL OPERADOR HUMANO**. No emito otra iteracion de re-juicio sin instruccion suya.

**Lo que le pongo delante al operador, sin adornarlo en ninguna direccion:**

- La remediacion r4 que se pidio esta **bien hecha y completa**: cierra la grieta de r3 por
  construccion, con su propio guardian (M9), sin ampliar el allowlist, y pone el inventario al dia.
  Si el criterio fuese "hizo r4 lo que se le pidio", la respuesta es **si**.
- El bloqueante que traigo **no lo introduce r4**: lo introdujo r2 (`31867185`) y sobrevivio a r3 y
  a r4 porque **ni el Arquitecto ni yo cruzamos los dos ejes**. Es una regresion vieja de la misma
  cadena, no un fallo de esta vuelta.
- Aun asi **no puedo llamar cerrada la tarea**: el defecto vive en la funcion que la tarea existe
  para arreglar, viola su propio negativo declarado y sus AC4 y AC6, y es silencioso con las seis
  puertas verdes. Cerrar hoy dejaria el mecanismo de AC1 con una fuga que su propia suite no ve.
- El dano es **latente, no vivo**: hoy el corpus no tiene ninguna decision con puntero y sin
  `status`, y el censo 110/2 que publica la entrega es **correcto** -- lo re-derive. Igual que el
  censo 106/4 era correcto el dia antes de que alguien mirase que decisiones eran las 106.
- Las dos salidas son legitimas y la eleccion es del operador: **(a)** una tercera iteracion acotada
  a la propiedad de 6.1 -- el arreglo es de una linea y su prueba ya esta escrita en 3.2 --, o
  **(b)** cerrar TASK-0368 con este hallazgo enrutado como tarea propia y declarado en el cierre,
  asumiendo que el mecanismo queda con una fuga conocida hasta que esa tarea corra.
  Mi recomendacion tecnica es **(a)**, porque el coste es menor que el de escribir la tarea, y
  porque cerrar el AC1 con su senal primaria descartable es cerrar en falso. Pero la decision de
  gobierno es suya.

-- Analista, 2026-08-14 13:38 local (UTC+2)
