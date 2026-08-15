---
artifact_id: Analista-TASK-0373-f2-enfriado-en-seco-verdict
task_id: TASK-0373
type: adversarial_review
author: Analista
status: final
created: 2026-08-15
verdict: CHANGE-REQUIRED
---

# Veredicto adversarial -- TASK-0373, F2 del enfriado en seco

**CHANGE-REQUIRED.** Un bloqueante, y es exactamente el que AC2 existe para impedir.

El stub, renderizado por la produccion entregada sobre la ruta indexada exacta de una tarea `done`
real de esta instancia, deja el **validador canonico en exit 1**. No cuelga el puntero: lo que rompe
es el bloque `intake`. El test del maker no lo ve porque su unica muestra es
`examples/minimal_instance/TASK-0001`, que esta **exenta** del hard-gate de intake por ser
`id <= TASK-0238`. Es una muestra tomada de la mitad exenta de la poblacion.

Respondo tambien tu pregunta de cabecera, medida y no opinada: **el manifiesto reconstruye la fila de
`cold_packs` 1:1 -- las siete columnas NOT NULL --, pero los campos POR ARTEFACTO los LLEVA, no los
reconstruye.** Ningun lector los exige y ninguna tabla se puebla con ellos.

## 0. Ancla canonica

    commit revisado           17f36268   (implementacion e74109b4)
    clon limpio               D:/Aegis_Scratch/protocol/rev0373/c1  (git clone -s, checkout 17f36268)
    clones auxiliares         c2 (familia completa de 273 stubs), c3 (repro minimo y sondas)
    alcance                   SOLO hub. No gatee `npm test`, tal como declaraste.
    estado canonico al medir  validate exit 0 antes de empezar

Nada de lo que sigue se midio en el arbol caliente. Todo gateado por exit code real, sin tuberia.

## 1. Puertas sobre el ancla, en clon limpio

    exit=0  python scripts/memory/test_memory_db.py               Ran 78 tests, OK
    exit=0  python scripts/memory/check_memory_db_drift.py --root . --fast   result: pass
    exit=0  python scripts/validate_collaboration_state.py --root .
    exit=0  python scripts/scan_encoding.py --root .

Las cuatro verdes. Coinciden con tu segunda corrida. El resto de este veredicto no discute puertas:
discute lo que las puertas no miran.

## 2. AC2 -- el BLOQUEANTE, reproducido en un solo fichero

Repro minimo, en `c3`, arbol por lo demas identico al ancla:

    P=Area_comun/tasks/TASK-0350-el-port-del-motor-de-memoria-deja-marcadores-sin-resolver.md
    # render_stub(candidato real de la propuesta viva) -> $P
    python scripts/validate_collaboration_state.py --root .
    exit=1
    ERRORS:
    - Task TASK-0350 missing intake block

    # restaurado el fichero original, mismo arbol:
    exit=0

Y a la escala que la regla enviada realmente propone: en `c2` renderice el stub sobre **los 273
candidatos** de la propuesta viva (los 273 estan referenciados por el indice fusionado, lo comprobe).

    python scripts/validate_collaboration_state.py --root .
    exit=1
    11 errores, los 11 de la misma clase: "Task TASK-XXXX missing intake block"
    python scripts/scan_encoding.py --root .   exit=0

El stub conserva `artifact_id`, `status`, `storage`, `cold_path`, `sha256`,
`git_commit_at_freeze` y `rehydration_command`. Pierde `intake`, y con el, `id`, `title`, `owner`,
`type`, `file` y `reviewer`. El hard-gate de intake es obligatorio para `id > TASK-0238`; las
anteriores estan exentas de por vida. Por eso la familia se parte en dos mitades y el maker probo la
mitad exenta.

AC2 se acredita, con sus palabras, "comprobando que `validate_collaboration_state` sigue VERDE".
Sobre la poblacion que la regla enviada selecciona, no sigue verde.

### 2.1 Y el verde del maker no discrimina

En `examples/minimal_instance`, un fichero de **cero bytes** en la ruta de TASK-0001 deja el
validador igual de verde:

    : > Area_comun/tasks/TASK-0001-implementer-minimal-instance.md
    python scripts/validate_collaboration_state.py --root <copia de minimal_instance>
    exit=0   (solo WARNING: "Task TASK-0001 file has no status metadata")

El verde de `test_f2_stub_at_original_task_path_keeps_canonical_validator_green` no viene del
contenido del stub. Viene de que el fichero exista. Un stub vacio produce el mismo verde, asi que ese
test no distingue entre el formato entregado y ninguno.

### 2.2 La regla de oro funciona, pero no esta probada

Lo constructivo primero: la clausula forzadora **funciona**. Con `requires_stub: false` en la regla,
los 273 candidatos referenciados siguen saliendo con `requires_stub=1`. Medido.

Pero ningun test lo sujeta. Dos mutantes sobre PRODUCCION, suite `-k f2` completa:

    SURVIVE (verde)  requires_stub = int(bool(rule["requires_stub"]))        # muere la clausula
    SURVIVE (verde)  referenced_index_paths(root) -> return set()            # ciega el indice

La propiedad anti-B1 se puede borrar entera de produccion sin poner rojo nada. Ademas, la guarda
`if artifact.relative_path in referenced and not requires_stub: raise` es **inalcanzable por
construccion**: `requires_stub` ya se calcula como `... or path in referenced`.

### 2.3 El `rehydration_command` que se escribe en el stub no corre

    python scripts/memory/query_memory_db.py --retrieve task:Area_comun/tasks/TASK-0350-...md
    exit=2   error: --requested-by is required with --retrieve

Con `--requested-by Analista` anadido, el id resuelve y devuelve el artefacto (exit 0). El puntero es
bueno; la **linea de comando literal que el stub promete como "verificable"** no lo es.

## 3. AC1 -- tu pregunta, respondida por conducta

**Reconstruye la fila de pack 1:1.** `render_pack_manifest` exige en escritura las cinco claves de
cabecera y los ocho campos por artefacto; `load_cold_packs` produce la fila y el test compara las
siete columnas NOT NULL de `cold_packs`. Eso se sostiene.

**Los campos por artefacto no se reconstruyen: se transportan.** Escribi a mano un manifiesto en
`Area_comun/archive/cold-packs/CP-9/pack.manifest.json` con
`"artifacts": [ {}, {"artifact_id": "X"} ]`, lo commitee y lo pase por el lector:

    load_cold_packs ACCEPTED rows:
    ('CP-9','task_history','Area_comun/archive/cold-packs/CP-9','refs/heads/main','2026-08-15',
     'aca7cff...',2)

Aceptado, exit 0, `artifact_count=2`. Ninguno de los ocho campos que AC1 enumera es exigido en
lectura, y ninguna tabla se puebla con ellos: `stubs` sigue en 0 y ademas se **borra en cada build**
(esta en la lista de tablas derivadas que se vacian). El round-trip esta cerrado a granularidad de
pack; a granularidad de artefacto el manifiesto es hoy solo de escritura.

No lo cuento como bloqueante: AC1, en su letra, pide que el manifiesto LLEVE los campos y que la
tabla se reconstruya, y ambas cosas se cumplen. Lo dejo como residual declarado y como respuesta
exacta a tu pregunta.

## 4. AC5 -- el golden del stub es golden; los del manifiesto no

Mutantes sobre PRODUCCION, suite `-k f2` completa (linea base 5/5, exit 0):

    KILLED    stub: "storage: cold_stub" -> "storage: frozen___"        (control, exit 1)
    SURVIVE   pack manifest: indent=2 -> indent=4
    SURVIVE   pack manifest: sort_keys=True -> False
    SURVIVE   pack manifest: required_artifact pierde "closed_at"
    SURVIVE   pack manifest: required_pack pierde "git_ref"
    SURVIVE   manifest-index: indent=2 -> indent=4
    SURVIVE   manifest-index: clave raiz "packs" -> "cold_packs"
    KILLED    pack manifest: clave raiz "artifacts" -> "items"          (lo mata el LECTOR, no un golden)
    KILLED    manifest-index: required pierde "sha256_manifest"         (control, exit 1)
    KILLED    propose_cold deja de excluir claims activos               (control, exit 1)

La causa es visible en el test: para el manifiesto y para el indice de manifiestos, la asercion es

    self.assertEqual(rendered, memory_db.render_pack_manifest(header, [artifact]))

es decir, **produccion contra produccion**. Eso prueba determinismo, no formato. AC5 pide el PAR:
"mutar un campo del formato pone rojo, y el formato correcto pasa". Para el stub existe ese par
(bytes esperados literales). Para el manifiesto y el manifest-index no existe: el formato puede
cambiar de sangria, de orden de claves o de nombre de la clave raiz y la suite sigue verde. El
manifest-index, ademas, **no tiene ningun lector** en el arbol, asi que nada lo ata por ninguna via.

El `assertNotEqual(expected.replace(b"status: done", b"status: blocked"), rendered)` del test del
stub es vacuo por construccion (muta la constante esperada, no produccion); el golden real es el
`assertEqual` de arriba, y ese si discrimina.

## 5. AC4 -- se mueve con la regla, pero no se deriva SOLO de la regla

Barrido de ejes sobre el corpus real, misma ancla, un eje por corrida:

    BASE (regla enviada)                     count= 273
    enabled true->false                      count=   0   rules_evaluated=[]
    target_retention_class cold->warm        count=   0   rules_evaluated=[]
    selector status=done -> status=in_review count=   0
    selector status=done -> status=blocked   count=   0
    artifact_type task->decision             count=   0
    window_count 100->0                      count= 373
    window_count 100->300                    count=  73
    window_count 100->10000                  count=   0
    segunda regla (handoff, done)            count= 275
    requires_stub true->false                count= 273  (los 273 siguen con requires_stub=1)

En esos ejes la propuesta se mueve con la regla, monotona y coherente. Tu duda ("una sola muestra")
queda cubierta: no se mueve una vez, se mueve con cada eje que el motor sabe leer.

**El defecto esta en los ejes que NO sabe leer, y es silencioso.** Misma regla, mismo commit, mismo
arbol, selector legal de dos clausulas:

    selector: "status=done&owner=Codex"
    con runtime/memory/index.db presente   -> exit 0, count=  0
    con runtime/memory/index.db ausente    -> exit 0, count=188

Cero warnings en ambos casos. La causa: `_proposal_artifacts`, cuando el DB derivado existe, arma
`SourceArtifact.metadata` con **cuatro** claves (`status`, `created_at`, `closed_at`, `_sha256`);
`_selector_matches` resuelve cualquier otra clave a `""` y devuelve `False`. Un selector con clave no
soportada (`foo=bar`) tambien da 0 en silencio, sin error de validacion.

Consecuencia practica para F3: el conjunto propuesto depende de si existe un fichero **gitignorado y
no versionado** (`runtime/memory/index.db`), no solo de la regla y del indice. Cero candidatos es
exactamente lo que parece una respuesta correcta cuando no hay nada que enfriar. La direccion
peligrosa es la inversa a la intuitiva: quien anade una clausula para ESTRECHAR y corre en la maquina
sin DB se lleva 188 rutas en vez de las que creia.

Con el selector enviado (`status=done`) no hay divergencia: DB presente y ausente dan 273 identicos,
mismos paths, mismos campos. El riesgo esta latente, no activo.

## 6. AC3 -- dry-run de verdad, y mas fuerte de lo que declara

Ensucie el arbol a proposito (un tracked modificado + un untracked nuevo) y corri la propuesta:

    exit=0  python scripts/memory/build_memory_db.py --propose-cold --root .
    censo SHA-256 de los 5780 ficheros del arbol, .git excluido, GITIGNORADOS INCLUIDOS:
    ADDED 0   REMOVED 0   CHANGED 0

Byte a byte identico, incluido el `index.db` de 14 MB. PASA, y pasa por encima de lo que AC3 pide.

Lo digo porque el instrumento declarado se queda corto: `git status --porcelain` es **ciego** a todo
lo gitignorado, y `runtime/memory/` lo esta. Una escritura ahi no la habria visto la acreditacion
declarada. Aqui no la hubo -- el DB se abre en `mode=ro` --, pero el instrumento no es el que
acredita la propiedad. Dato colateral: la suite de tests si construye ese DB de 14 MB en la raiz del
repo, y porcelain tampoco lo ve.

## 7. AC6 -- frontera dura, respetada

    Area_comun/archive          ABSENT en el clon limpio
    git ls-tree -r HEAD | grep "^Area_comun/archive/"    -> 0 rutas
    DB construido sobre el ancla:  cold_packs 0   stubs 0   hot_cold_rules 1   artifacts 4913

`hot_cold_rules` pasa de 0 a 1: es precisamente lo que F2 introduce. Cero movimiento confirmado.

## 8. Tabla vector por vector

| AC | Criterio | Resultado | Evidencia |
|----|----------|-----------|-----------|
| AC1 | Manifiesto reconstruye la tabla 1:1 | PASA con residual | 7 columnas NOT NULL verificadas; lector acepta `artifacts:[{}]`, exit 0 |
| AC2 | Regla de oro anti-B1, por conducta | **SLIP -- BLOQUEANTE** | 1 stub -> validate exit 1; 273 stubs -> 11 errores de intake; verde del maker no discrimina; clausula forzadora sin test |
| AC3 | `--propose-cold` es dry-run | PASA | exit 0 con arbol sucio; 5780 ficheros sin un byte de cambio |
| AC4 | La seleccion se DERIVA | PARCIAL | 11 ejes se mueven; divergencia silenciosa 0 vs 188 segun exista el DB |
| AC5 | Goldens estables y discriminantes | SLIP | golden del stub real; manifiesto y manifest-index se comparan contra si mismos, 6 mutantes de formato sobreviven |
| AC6 | Cero movimiento | PASA | sin `Area_comun/archive`, `cold_packs`=0 |

## 9. Residuales declarados

1. El `artifact_id` de las tareas del corpus sale como `task:<ruta>`, no como `TASK-0350`. El stub y
   el `rehydration_command` heredan ese id de ruta. Resuelve (con `--requested-by`), pero es un id
   sintetico, y es preexistente a esta entrega.
2. `check_memory_db_drift --fast` sigue reportando `"stubs":"noop-until-f2"` despues de F2. Marcador
   preexistente; lo dejo senalado, no lo cuento contra la entrega.
3. La tabla `stubs` no la puebla nadie y se vacia en cada build. Coherente con "cero movimiento",
   pero significa que la mitad por artefacto del formato no tiene consumidor todavia.
4. Solo 5 de las 273 rutas propuestas estan en el TASK_INDEX caliente; el resto vive en el archivo.
   Los 11 errores de intake salen del conjunto que el validador si mira.
5. Anomalia operativa, no de la entrega (DECISION-0018): durante mi ventana de escritura un exec del
   peer borro del arbol compartido este artefacto cuando aun estaba untracked, entre el `git add` y
   el commit. Lo reescribi desde area propia y lo aterrice de forma atomica. Lo senalo al Arquitecto
   como incidente del guard de residuos, sin tocar rutas ajenas.

## 10. Recomendacion de cierre

**CHANGE-REQUIRED.** El bloqueante es AC2 y es de forma, no de arquitectura: el stub tiene que
conservar lo que el hard-gate de intake exige (o el gate tiene que reconocer `storage: cold_stub`
como forma legitima, y eso seria DECISION, no parche). Mientras el stub deje el validador canonico en
rojo sobre la poblacion que la regla propone, **F3 no se puede encender**: su primer movimiento real
pondria el estado canonico en rojo, que es justo el modo de fallo que la regla de oro existe para
impedir.

Lo demas no bloquea y no lo inflo: AC3 y AC6 pasan limpios, AC1 pasa en su letra con la respuesta a
tu pregunta declarada, AC4 se deriva en once ejes con una divergencia latente que no toca el selector
enviado, y AC5 necesita goldens de bytes de verdad para el manifiesto.

### Bucle de correccion esperado

- **Remediacion (1 iteracion):** (a) el stub conserva el `intake` -- o el par (`id`, `intake`) que el
  validador exige -- para tareas `id > TASK-0238`; (b) un test que ejercite la ruta NO exenta, es
  decir una tarea moderna del corpus, no `minimal_instance/TASK-0001`; (c) goldens de bytes literales
  para `render_pack_manifest` y `render_manifest_index`; (d) un negativo que mate el mutante de la
  clausula forzadora de `requires_stub`; (e) `rehydration_command` ejecutable tal cual se escribe.
  AC4 (divergencia DB / arbol) lo recomiendo como **tarea propia**, no como remediacion de esta: es
  precondicion de F3, no de F2, y no toca el selector enviado.
- **Puertas afectadas:** `test_memory_db.py`, `validate_collaboration_state.py` sobre el arbol con el
  stub puesto, `scan_encoding.py`, `check_memory_db_drift --fast`.
- **Re-juicio:** mio, sobre el commit de remediacion, en clon limpio y antes del commit de cierre.
- **Maximo 2 iteraciones** antes de escalar al operador humano.

-- Analista, 2026-08-15 02:10 local (UTC+2)
