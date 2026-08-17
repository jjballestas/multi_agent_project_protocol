# Veredicto Analista -- TASK-0414 r5: la ausencia ya muerde, y la que no muerde es la del ancla

Revisor: Analista (checker independiente). Maker: Codex. Encargo:
`MSG-20260817-Arquitecto-to-Analista-REVIEW-TASK-0414-r5`.

## Ancla canonica

    commit del producto bajo juicio   123fab06  fix(runtime): fail closed when anchored registry is missing
    control historico                 123fab06^ = dbb9294f
    HEAD del protocolo al revisar     3bb82158  docs(TASK-0378): record r5 review memory
    tarea                             TASK-0414  owner Codex  reviewer Analista  status in_review
    claims activos                    ninguno (CLAIMS.json sin entradas activas)
    clon limpio                       git clone -s -n <repo>; git checkout <commit>  (cuatro arboles)
    scratch root                      D:/Aegis_Scratch/protocol/an0414r5/  (DECISION-0104)
    cadena medida                     9162 eventos, cabeza seq 9833
                                      un unico event_auth.registry_anchor, seq 9764
                                      cero eventos chain.anchor
    hora                              2026-08-18 00:56 local (UTC+2)

Nada se midio en el arbol caliente: tiene modificaciones de terceros que no son mias.

## Veredicto

**OK-CERRABLE.**

SLIP-A esta cerrado, y lo esta **en la puerta**, no solo en la funcion: el vector exacto de r4c
--borrar el registro y re-sincronizar el snapshot-- pasaba en `123fab06^` y falla en `123fab06`,
medido sobre la cadena real de 9162 eventos con el mismo arbol y la misma mutacion.

Y la pregunta de la sexta tiene respuesta, es afirmativa, y va primero.

---

## 1. La pregunta -- r6 es ALCANZABLE, la cadena no lo impide

> Si en vez de borrar el registro se borran las ANCLAS de la cadena y se re-sincroniza el snapshot,
> el discriminante colapsa a nunca-anclada y el control se apaga con exit 0 -- es alcanzable esa via,
> o la cadena encadenada por hash lo impide?

**Es alcanzable. La cadena no lo impide.** Tres mediciones, en orden de dureza.

### 1a. Con el ancla a MEDIA cadena (el log de hoy): la CLI de drift sale en 0 con el hueco puesto

Arbol `r6a`: clon limpio de `123fab06`, quito la linea del ancla de `runtime/state/events.jsonl`,
borro el registro, y re-sincronizo con `rebuild_snapshot` (herramienta publica, la misma de r4c).

    validate_event_auth_registry_anchor(all_events(root), root=root)
        -> {'valid': True, 'reason': 'registry_absent', 'checked': 0}     <- el control, APAGADO

    python runtime/protocol_replay.py --check-drift --root .
        PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=9833
        EXIT 0                                                            <- la puerta de drift, VERDE

    validate_chain(all_events(root), cfg, root=root)
        -> {'valid': False, 'reason': 'gap at seq 9765: expected 9764', 'seq': 9765}

    python scripts/validate_collaboration_state.py --root .
        ERROR: Runtime event log snapshot mismatch: snapshot mismatch: state hash differs
        ERROR: Runtime event log chain invalid: gap at seq 9765: expected 9764
        EXIT 1

Lo que hay que leer aqui no es el 1 final: es que **la CLI de drift sale en 0 teniendo delante un
hueco de seq**. `protocol_state_drift` no llama a `validate_chain` en ningun punto
(`runtime/protocol_replay.py:1186-1218`): mira estado materializado, ancla del registro, prune y slim
views. Un evento que no aporta estado --y el ancla del registro no aporta ninguno-- se puede quitar
del log sin que esa puerta lo vea. Quien cierre r6 mirando `--check-drift` va a ver verde.

Lo que hoy muerde es el detector de huecos dentro de `validate_collaboration_state.py`
(`validate_eventlog_chain`). Y eso lleva a la medicion siguiente.

### 1b. Con el ancla en la COLA: no hay hueco que detectar

El detector de huecos solo tiene algo que ver porque **hoy** hay 69 eventos despues del ancla. En el
instante en que un ancla se appendea, el ancla **es** la cola -- y lo fue durante todo r4c (aquel
veredicto lo dice: "el ancla es la cola del log, seq 9764 = ultimo evento").

Mido ese estado sin inventarmelo: tomo el prefijo genuino de la cadena real hasta seq 9764, cuyos
`prev_hash` son los de produccion, y cuya cola es exactamente el ancla.

    prefijo seq<=9764: 9093 eventos, cola seq 9764 type=event_auth.registry_anchor

    validate_chain(prefijo)                     -> valid True   'chain valid'
    validate_chain(prefijo menos la cola)       -> valid True   'chain valid', checked_events=9091
    validate_event_auth_registry_anchor(prefijo menos la cola, registro BORRADO)
                                                -> {'valid': True, 'reason': 'registry_absent', 'checked': 0}

**Sin hueco, sin corrupcion, y con el control apagado.** Quitar la cola de una cadena encadenada por
hash no rompe ningun `prev_hash`: cada evento encadena hacia atras, y nadie encadena hacia el que ya
no esta. El genesis pineado ata el **principio** de la cadena; no hay nada que ate el **final**.

### 1c. Y no hay pin externo de la cabeza que lo compense

    eventos chain.anchor en el log: 0

`verify_anchor_monotonicity` recorre eventos `chain.anchor` y con cero de ellos devuelve
`checked=0, valid=True`: `validate_eventlog_anchors` es hoy una puerta **vacua**. La configuracion
declara `anchor_enabled: true` con backend `git-remote`, pero ninguna puerta embarcada compara la
cabeza contra ese remoto. No hay tercero que note que la cadena perdio su ultimo evento.

### Respuesta cerrada

r6 existe y es de la misma familia que r4c --apagar en vez de enganar-- mudada un nivel. **No la
meto en esta tarea**, como usted pidio. Lo que r6 tiene que medir y yo no medi, para que no se cierre
con menos: **la variante de cola, extremo a extremo**. Mis 1b son mediciones de los dos
discriminantes (`validate_chain` y el guardia del registro) sobre la cadena real; no reconstrui un
arbol completo con el estado caliente re-materializado a seq 9763, porque eso exige revertir 69
eventos de trabajo real y es una mutacion distinta de la que se ataca. Esa es la unica pieza que
falta, y es la que decide si r6 es un agujero de puerta o solo de discriminante.

---

## 2. El control historico -- el maker se declaro bien: 4/5 antes, 5/5 despues

No lo acepte de palabra. Tres medidas, de la mas fina a la mas gruesa.

### 2a. Por comportamiento, funcion contra funcion, con mis propias cargas

Cargo `runtime/eventlog.py` de las dos versiones como dos modulos distintos y ejercito las cinco
formas contra un registro sintetico propio (no el runner del maker):

    caso                                 123fab06^      123fab06     razon vieja / razon nueva
    ----------------------------------   ------------   ----------   -------------------------------------
    registry_deleted                     FAIL           PASS         registry_absent / registry_missing
    registry_empty                       PASS           PASS         registry_anchor_mismatch / idem
    registry_empty_key_list              PASS           PASS         registry_anchor_mismatch / idem
    never_anchored_without_registry      PASS           PASS         registry_absent / registry_absent
    registry_without_any_anchor          PASS           PASS         registry_anchor_missing / idem

    CORTE:  OLD 4/5   NEW 5/5

(Mas un control de sanidad: anclado con el registro intacto -> `registry_anchor_valid` en ambas.)

### 2b. A nivel de runner, en 2x2, con la unica variable siendo las tres lineas nuevas

    tests viejos x codigo viejo    EXIT 0
    tests nuevos x codigo viejo    EXIT 1   AssertionError en la linea 237:
                                            assert missing_registry["valid"] is False
    tests nuevos x codigo nuevo    EXIT 0   (dos corridas, stdout byte-identico)

Muere en el primer caso nuevo y solo en ese: el negativo **discrimina**, y discrimina exactamente
donde el maker dijo. El unico delta de produccion entre las dos versiones son las tres lineas de
`runtime/eventlog.py` (el cambio de `scan_domain_neutrality.{py,ps1}` es el numero de linea de una
exencion, que se corre porque el fichero crecio 3 lineas).

### 2c. En la PUERTA, sobre la cadena real, con el vector de r4c

Misma mutacion en los dos arboles: `rm Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json` +
`rebuild_snapshot(root)`.

    puerta                                       123fab06^                   123fab06
    ------------------------------------------   -------------------------   ----------------------------
    runtime/protocol_replay.py --check-drift      EXIT 0  verdict=CLEAN       EXIT 1  DRIFT path=
                                                  (el escape de r4c, vivo)     Area_comun/protocol/
                                                                               EVENT_AUTH_KEY_REGISTRY.json
    scripts/validate_collaboration_state.py       EXIT 1                      EXIT 1

**Esto es lo que acredita el arreglo**: la CLI de drift pasa de 0 a 1 con la misma mutacion sobre el
mismo arbol. Es un verde que el codigo viejo daba y ya no da.

Y lo corrijo antes de que se cite mal: **el validador canonico no discrimina aqui.** Sale en 1 en las
dos versiones, y en `123fab06^` sale en 1 por un motivo que no tiene nada que ver con este arreglo
(`Runtime event log snapshot mismatch: state hash differs`). Sobre la cadena de hoy, `rebuild_snapshot`
ya no re-sincroniza del todo, asi que el escape de r4c --que en su dia daba 0 en las **dos** puertas--
hoy solo se reproduce en la CLI de drift. La discriminacion medida es real y esta en esa CLI y en el
motivo nombrado (`EVENT_AUTH_KEY_REGISTRY.json` aparece en el 1 nuevo y no en el viejo); no en el exit
code del validador.

---

## 3. Vector por vector

    vector                                                        veredicto
    -----------------------------------------------------------   ---------------------------------------
    SLIP-A: la ausencia del registro anclado ya es fatal           PASS   (2c, con control historico)
    Autodeclaracion del maker 4/5 -> 5/5                           PASS   (2a y 2b, confirmada)
    Gate reproducible (DECISION-0115): dos corridas                PASS   (runner 0/0, stdout identico)
    r6: borrar las ANCLAS en vez del registro                      SLIP   ALCANZABLE (seccion 1) -- es r6,
                                                                          no de esta tarea, por su instruccion
    La exencion never_anchored no es alcanzable por el llamante    PASS estrecho (ver abajo)
    ... ni por cadena truncada / vacia / filtrada                  SLIP   es el mismo r6 (seccion 1)
    registry_missing: no filtra de mas, nombra la causa            PASS   (con dos residuos cosmeticos)

**Sobre el llamante (su punto 4).** `validate_event_auth_registry_anchor` recibe `events` como
parametro y **confia en el**: si le pasan una lista sin anclas y el registro no esta, devuelve
`registry_absent` con `valid: True`. Lo verifique con carga propia:

    V([], root=<registro presente>)   -> registry_anchor_missing   (valid False)
    V([], root=<registro ausente>)    -> registry_absent           (valid True)   <- la exencion
    V([evento no-ancla], root=<registro ausente>) -> registry_absent (valid True)

El unico llamante de produccion es `protocol_state_drift`
(`runtime/protocol_replay.py:1196`), y pasa `all_events(root)` **sin filtrar**. Por eso el PASS es
estrecho y honesto: hoy no hay ruta en proceso que filtre la lista. La exencion no se alcanza
*enganando al llamante*; se alcanza *quitando el ancla del disco*, que es la seccion 1.

**Sobre `registry_missing` (su punto 5).** La rama devuelve exactamente:

    {'valid': False, 'reason': 'registry_missing', 'seq': <seq del ancla mas alta>, 'checked': <n anclas>}

No hay digests, ni rutas, ni contenido del registro (no podria: el fichero ya no esta). No filtra
nada que no deba. Y el motivo **nombra la causa** y es distinguible de sus tres vecinos
(`registry_anchor_missing`, `registry_anchor_mismatch`, `registry_anchor_invalid`), que es lo que pide
la leccion de esta semana sobre fallos sin diagnostico. PASS.

Ademas, probe formas de ausencia que el maker no cubrio, y todas fallan cerradas:

    registro es un DIRECTORIO en la ruta canonica, con ancla   -> registry_missing   (valid False)
    ancla sin campo seq, registro ausente                      -> registry_missing   (valid False, seq None)

---

## 4. Residuos declarados

**R1 -- el caso se llama como el vector de r4c, pero no ejecuta el vector de r4c.** El caso nuevo
`registry_deleted_resynced_snapshot` **no re-sincroniza ningun snapshot**: hace `registry_path.unlink()`
y llama a la funcion pura. Lo que prueba es el veredicto de la funcion, no que la puerta se ponga roja.
Todo el escape de r4c era un verde **extremo a extremo con las dos puertas en 0**, y ninguno de los
cinco casos nuevos toca puerta alguna. El fin a fin lo medi yo (seccion 2c) y sale bien; la evidencia
del repositorio no lo demuestra. No bloquea el cierre: el nombre promete de mas, el codigo no miente.

**R2 -- una rama muerta donde antes habia otra.** En `runtime/eventlog.py`, doce lineas por debajo del
arreglo, sobrevive `if not actual: return {"valid": False, "reason": "registry_missing", ...}`. Ahora es
**inalcanzable**: `actual` solo puede venir vacio si el fichero no existe, y ese caso ya retorna arriba.
Es la imagen especular del defecto de r4c (alli el negativo bueno quedaba a la sombra del early return;
aqui el negativo bueno se subio y dejo al viejo sin alcanzar). Inofensivo hoy, y trampa para el proximo
que lea el fichero y crea que ese `if` cubre algo.

**R3 -- `seq` se devuelve en crudo.** `latest.get("seq")` sin normalizar: puede salir `None`, y con un
`seq` no numerico `int()` lanza `ValueError` sin capturar. Preexistente (el mismo `int()` estaba en la
rama de anclas del codigo viejo) y **falla cerrado** --la excepcion sube al `try/except` de
`validate_protocol_state_drift`, que la convierte en `validation.fail`--, asi que no es una via de
escape. Cosmetico.

**R4 -- `--check-drift` no ejercita la cadena.** Medido en 1a: exit 0 con un hueco de seq delante. No es
un defecto de esta entrega; es el terreno sobre el que se juega r6, y conviene que este escrito antes
de abrirla.

---

## 5. Puertas, por exit code, en clon limpio de 123fab06

    python scripts/validate_collaboration_state.py --root .            EXIT 0   OK: collaboration state is valid.
    python runtime/protocol_replay.py --check-drift --root .           EXIT 0   verdict=CLEAN up_to_seq=9833
    python scripts/scan_encoding.py                                    EXIT 0   OK: encoding scan is clean.
    python scripts/scan_domain_neutrality.py                           EXIT 0
    examples/replay_secret_independent_cases/                          EXIT 0   corrida 1
      run_replay_secret_independent_cases.py                           EXIT 0   corrida 2, stdout byte-identico

Alcance de producto declarado respetado: `runtime/eventlog.py` y
`examples/replay_secret_independent_cases/`. No corri `npm test` ni el job entero; el encargo no lo
exige.

## 6. Reproduccion

    cd D:/Aegis_Scratch/protocol/an0414r5
    git clone -s -n D:/Agentes/multi_agent_project_protocol cc   && (cd cc  && git checkout 123fab06)
    git clone -s -n D:/Agentes/multi_agent_project_protocol old  && (cd old && git checkout 123fab06^)

    # 2b -- 2x2 de runner
    cp cc/examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py \
       old/examples/replay_secret_independent_cases/
    (cd old && python examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py)  # 1
    (cd old && git checkout examples/ && python examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py)  # 0
    (cd cc  && python examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py)  # 0

    # 2c -- vector de r4c en la puerta, en los dos arboles
    #      rm Area_comun/protocol/EVENT_AUTH_KEY_REGISTRY.json ; rebuild_snapshot(root)
    #      python runtime/protocol_replay.py --check-drift --root .     old -> 0    cc -> 1

    # 1a -- r6 a media cadena
    #      quitar la linea event_auth.registry_anchor de runtime/state/events.jsonl
    #      rm el registro ; rebuild_snapshot(root)
    #      --check-drift -> 0 CLEAN ;  validate_collaboration_state -> 1 (gap at seq 9765)

    # 1b -- r6 en la cola, sobre la cadena real
    #      prefijo = [e for e in all_events(root) if e.seq <= 9764]     (cola = el ancla)
    #      validate_chain(prefijo[:-1]) -> valid True
    #      validate_event_auth_registry_anchor(prefijo[:-1], root=<sin registro>) -> registry_absent

## 7. Recomendacion de cierre

**OK-CERRABLE.** Cierre TASK-0414 (in_review -> done) sobre `123fab06`.

Dos cosas que son suyas y no de Codex:

1. **Abra r6 con la variante de COLA, no con la de media cadena.** La de media cadena la caza el
   detector de huecos; la de cola no la caza nadie, y es la posicion natural de un ancla recien
   escrita. Si r6 se abre y se cierra midiendo solo el borrado a media cadena, va a salir verde por
   una propiedad temporal --que hoy hay 69 eventos detras-- y no por una garantia.
2. **R1 conviene que viaje con r6**, no con una sexta vuelta de esta: el hueco de evidencia es que
   ningun caso del runner ejercita las puertas extremo a extremo, y r6 es precisamente la tarea que
   necesita ese arnes.

-- Analista, 2026-08-18 00:56 local (UTC+2)
