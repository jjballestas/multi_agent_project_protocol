# Veredicto Analista -- TASK-0350 (detector de marcadores del instanciador)

**Veredicto: OK-CLOSABLE**, con un residuo declarado y una observacion nueva que no es de esta tarea.

La pregunta central de la review -- "puedes construir un marcador que el instanciador SI deberia
sustituir y que el patron nuevo deje pasar?" -- tiene respuesta: **si, pero solo anadiendo una clave
que hoy no existe y que nada prohibe anadir**. No hay fuga viva. Hay una invariante sin guardia.

---

## 1. Anclaje canonico

| Cosa | Valor |
|------|-------|
| Commit bajo review | `192c5deabfef481b0f4db558da24afa679bfd2e9` (Codex, 2026-08-12 20:02:27 +0200) |
| Control (padre) | `694bd7e4` |
| `origin/main` al abrir la review | `6a469cc0` |
| Clon limpio | `D:/Aegis_Scratch/protocol/analista-0350/clone` (`git clone -s -n` + `checkout 192c5dea`) |
| Clon de control | `D:/Aegis_Scratch/protocol/analista-0350/pre` (`checkout 192c5dea^`) |
| Alcance | SOLO hub. Sin producto en alcance: **no** gateo `npm test`, por instruccion explicita. |

Nada se midio en el arbol caliente. Los dos clones se crearon con `-s` (objetos compartidos) y `-n`,
no con `--depth 1`, para no romper el recorrido de trailers.

## 2. Puertas del repo, por exit code, en clon limpio a `192c5dea`

| Comando | Exit |
|---------|------|
| `python scripts/validate_collaboration_state.py --root .` | **0** |
| `python scripts/scan_encoding.py --root .` | **0** |
| `python scripts/scan_domain_neutrality.py --root .` | **0** |
| `python runtime/protocol_replay.py --check-drift --root .` | **0** -- `verdict=CLEAN up_to_seq=8977` |
| `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py` | **1** -- por el residuo de TASK-0367, ver AC5 |

Estado canonico del repo vivo antes de empezar: `validate_collaboration_state.py` exit **0**. No
revise sobre un arbol a medio entregar.

## 3. Que cambia el diff, y cuanto de ancho es

El cambio de produccion es **una linea** en `scripts/new_instance.py:29`:

    -PLACEHOLDER_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
    +PLACEHOLDER_RE = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")

`git show --name-only 192c5dea` toca, en codigo: `scripts/new_instance.py` y
`examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py`. El resto es
materializacion de estado gobernado (`Area_comun/state/*`, `runtime/state/*`) y el fichero de la
tarea. **No es mas ancho de lo declarado.**

Grep de `PLACEHOLDER_RE` en todo el arbol: tres usos, todos en `new_instance.py` (757 `render_text`
missing, 764 `sub`, 801 `find_unresolved_placeholders`). **Cero listas de excepciones** de ruta,
linea o literal. La correccion es de criterio, no de enumeracion.

## 4. Tabla vector a vector

| AC | Que promete | Veredicto | Como lo rompi / medi |
|----|-------------|-----------|----------------------|
| AC1 | El criterio de pertenencia, no la lista | **PASS** | Ver 4.1 |
| AC2 | El positivo real sigue muriendo | **PASS** | Ver 4.2 |
| AC3 | Sobrevive al cambio de coordenada | **PASS** | Ver 4.3 |
| AC4 | Las DOS direcciones | **PASS en espacio-de-ficheros; SLIP declarado en espacio-de-claves** | Ver 4.4 |
| AC5 | La firma se mueve, el residuo es preexistente y transferido por id | **PASS** | Ver 4.5 |
| AC6 | Declarado el destino del motor | **PASS**, con una correccion de precision | Ver 4.6 |

### 4.1 AC1 -- el criterio

El criterio entregado es: *los nombres de marcador son identificadores que posee el instanciador, y
un identificador empieza por letra; un doble-brace que empieza por digito es texto del producto (un
cuantificador de regex doblado dentro de una cadena `rf`)*. Eso es un criterio de pertenencia, no una
lista.

No me lo creo por declarado: lo **corroboro derivandolo**. Barrido del arbol fuente completo
buscando nombres que el patron VIEJO casaba y el NUEVO no:

    Area_comun/artifacts/Analista-TASK-0320-...-verdict.md   ['40', '64']
    Area_comun/mailbox/archived/MSG-20260807-...-TASK-0320.md ['40']
    examples/runtime_instantiation_cases/run_...cases.py      ['128']
    personal/Analista/MEMORY.md                               ['40']
    scripts/memory/test_memory_db.py                          ['40', '64']
    scripts/test_exec_lease_harness.py                        ['0']

Seis ficheros, y **cada uno de los nombres perdidos es puramente numerico**. Ni uno es un
identificador. La clase que el criterio nombra es exactamente la clase que el cambio pierde.

El descarte de las otras dos salidas se sostiene: resolver `test_memory_db.py` como plantilla haria
que el instanciador se adjudicase sintaxis de regex del producto (y `render_text` reventaria pidiendo
un reemplazo para `40`); excluir el fichero o sacar el motor del copiado quitaria comportamiento
ejecutable para callar un instrumento que dice la verdad en los demas casos -- y dejaria pasar,
mudo, al siguiente fichero del producto que caiga en la misma coincidencia.

### 4.2 AC2 -- el negativo discrimina

El par del maker se reproduce en clon limpio: `clean_exit=0`, `dirty_exit=1`, y la generacion sucia
imprime `ERROR: Unresolved placeholders remain in generated instance: genuine-marker.txt`.

No me quedo con su instrumento. Inyecte **mis** marcadores genuinos en **mis** coordenadas, incluidos
los bordes de la gramatica:

| Coordenada mia | Contenido | Marcado? |
|----------------|-----------|----------|
| `z/y/x/buried.md` | `{{PROJECT_GOAL}}` | SI |
| `Area_comun/README.md` | `{{HUMAN_OWNER}}` | SI |
| `one.txt` | `{{A}}` (una sola letra) | SI |
| `two.txt` | `{{P0}}` (letra + digito) | SI |
| `three.txt` | `{{X_1}}` | SI |

5 de 5. El detector caza la familia entera, no el ejemplo dado.

### 4.3 AC3 -- supervivencia al cambio de coordenada

El maker eligio `product_regex.py` con `rf"[0-9a-f]{{128}}"`. **Mude yo el texto ofensor a cinco
coordenadas que el no eligio y a formas de la misma clase que el no uso:**

| Coordenada mia | Formas | Marcado? |
|----------------|--------|----------|
| `a/b/c/d/deep_note.md` (profundidad 4) | `{{64}}`, `{{3,17}}` | no |
| `Area_comun/protocol/quant.txt` | `{{0}}`, `{{9}}`, `{{128}}`, `{{2,}}` | no |
| `scripts/memory/other_engine.py` (otro fichero del MISMO motor) | `{{1,12}}`, `{{40}}` | no |
| `top_level_quant.cfg` (raiz del arbol) | `{{1_000}}`, `{{0_A}}`, `{{7}}` | no |
| `no_ext_file` (sin extension) | `{{42}}` | no |

`find_unresolved_placeholders` devuelve `[]`. **El resultado no cambia al mudar de coordenada, de
profundidad, de extension ni de forma.** No hay allowlist que matar porque no hay allowlist.

### 4.4 AC4 -- las DOS direcciones

**Direccion "ganado": vacia por construccion, no por muestreo.** El lenguaje nuevo
`[A-Z][A-Z0-9_]*` es un subconjunto estricto del viejo `[A-Z0-9_]+`. Nada que el viejo no casara
puede casar el nuevo. Lo confirmo ademas empiricamente abajo.

**Direccion "perdido", medida por mi sobre una instancia REALMENTE generada** (no sobre el caso que
el maker escribio). Genere una instancia `runtime` desde el clon limpio -- `GEN_EXIT=0`, que ya es
resultado: antes del fix la generacion abortaba -- y recorri el arbol resultante con mis propias dos
expresiones:

    BEFORE (patron viejo): [('scripts/memory/test_memory_db.py', ['40', '64'])]
    AFTER  (patron nuevo): []
    LOST  (viejo y no nuevo): scripts/memory/test_memory_db.py -> nombres {40, 64}
    GAINED(nuevo y no viejo): []

Coincide exactamente con lo que el maker declara, y ahora esta derivado. Un fichero perdido, sus dos
nombres puramente numericos, cero ganados. **La diferencia es exactamente la que AC1 explica.**

Las 28 claves de `build_replacements` las extraje del fuente y las pase por ambos patrones: **0 claves
fuera del patron nuevo, 0 fuera del viejo**. Hoy no se pierde ningun positivo real.

**SLIP declarado (latente, no vivo).** `PLACEHOLDER_RE` gobierna las DOS cosas: la deteccion (801) y
la **sustitucion** (757 y 764). Estrechar el patron estrecha tambien el dominio de lo que se
sustituye. Construido y ejecutado:

    replacements = {"_INTERNAL": "v1", "2FA_MODE": "v2", "PROJECT_NAME": "ok"}
    texto        = "a={{_INTERNAL}} b={{2FA_MODE}} c={{PROJECT_NAME}}"
    render_text  -> "a={{_INTERNAL}} b={{2FA_MODE}} c=ok"
    find_unresolved_placeholders(sobre esa salida) -> []
    el patron VIEJO habria casado: ['_INTERNAL', '2FA_MODE', 'PROJECT_NAME']

Es decir: una clave que el instanciador **posee** y que no case la gramatica **no se sustituye y
ademas no se detecta**. Sale literal a la instancia generada, en silencio. Bajo el patron viejo esas
dos claves se sustituian bien. Para esa clase de entrada, el fix convierte un fallo ruidoso en uno
mudo.

Por que **no** lo cuento como fallo de esta entrega: las 28 claves de hoy cumplen la gramatica, asi
que la fuga **no es alcanzable sin cambiar codigo**, y AC4 se mide sobre el conjunto de ficheros de
una corrida real, que sale limpio. Por que **si** lo declaro: la invariante "toda clave de
`build_replacements` casa `PLACEHOLDER_RE`" vive **solo en un comentario**. Grepee el arbol entero:
no hay ni una asercion, ni un caso del runner, ni un gate que la compruebe. El criterio es correcto y
esta sin guardia -- que es, en pequeno, la misma distancia entre forma y propiedad que esta tarea
existe para cerrar.

### 4.5 AC5 (enmendado) -- la firma se mueve

Con **control historico**, que es lo que hace discriminante la afirmacion:

| | Cases que fallan | Firma |
|-|------------------|-------|
| `192c5dea^` (control) | **8** | TODAS: `Unresolved placeholders remain in generated instance: scripts\memory\test_memory_db.py` |
| `192c5dea` | **2** | NINGUNA de marcadores. Las dos por identidad cableada: `runtime/context.py:15`, `runtime/router.py:438`, `scripts/prune_state.py:252`, `scripts/prune_state.py:442`, y `scripts/harness/peer_mailbox_cron.ps1:553` (solo tier runtime) |

(a) La firma **se mueve**: desaparece por completo y la generacion llega hasta chequeos posteriores.
Ocho cases dejan de morir. (b) El residuo es **preexistente derivado del diff**: ninguna de esas
cinco rutas aparece en `git show --name-only 192c5dea`, luego este commit no lo pudo introducir; y en
el control estaba **enmascarado** porque la generacion abortaba antes de llegar al escaner. (c) Esta
transferido a **TASK-0367** por id, en `out_of_scope` de la tarea y en el HANDOFF. No lo trato como
fallo de 0350.

### 4.6 AC6 -- destino del motor, y una correccion de precision

El motor **viaja**: la instancia generada trae `scripts/memory/` con los seis scripts
(`build_memory_db.py`, `check_memory_db_drift.py`, `dump_memory_db.py`, `query_memory_db.py`,
`revive_pack.py`, `test_memory_db.py`). Ni el fichero ni su contenido se excluyen. Eso es lo que AC6
pide declarar, y es cierto.

El HANDOFF anade "and remains executable there". Lo comprobe por comportamiento en vez de heredarlo, y
**la frase se pasa de fuerte**:

| Entorno | `python scripts/memory/test_memory_db.py` |
|---------|-------------------------------------------|
| Clon fuente (hub) | **exit 0** -- `OK`, 72/72 |
| Instancia generada, recien parida (sin commit) | exit 1 -- 3 errores |
| Instancia generada, tras darle un commit inicial | exit 1 -- **70/72**, 1 error + 1 fallo |

Perseguidas las tres causas hasta su traza, ninguna es del motor ni de esta tarea:

1. `test_current_tree_build_does_not_change_tracked_status` -- `git rev-parse --verify HEAD^{commit}`
   sale 128 porque la instancia recien creada no tiene commit. **Desaparece al hacer el commit
   inicial**, lo que cierra el diagnostico.
2. `test_new_instance_exports_complete_memory_toolchain` -- `FileNotFoundError` sobre
   `scripts/new_instance.py`: una instancia no embarca el instanciador, por diseno. Es un test **del
   hub** que viaja dentro del motor.
3. `test_account_identifier_presentations_are_structural_and_falsifiable` --
   `assertGreater(len(object_ids), 100)` con `1`: el corpus es el arbol git, y una instancia recien
   nacida tiene un commit.

Ninguna es de marcadores, ninguna toca las rutas del diff. AC6 se cumple en lo que pide (declarar el
destino, y el motor efectivamente viaja y **ejecuta**: 70 de 72). Lo que no es exacto es leer
"executable" como "suite verde en una instancia recien parida". Lo anoto como precision, no como
fallo -- pero ver la observacion nueva de la seccion 6.

## 5. Residuos declarados

1. **La invariante clave-a-gramatica no tiene guardia** (seccion 4.4). Latente, no viva. Coste del
   cierre: una asercion de que toda clave de `build_replacements` casa `PLACEHOLDER_RE`, mas un caso
   en el runner que la ejerza. **No pido bloquear 0350 por esto**; recomiendo que el Arquitecto le
   ponga id propio.
2. **Fuga preexistente por fichero no decodificable**, identica antes y despues. Un
   `{{PROJECT_NAME}}` genuino dentro de un fichero UTF-16 o binario escapa a la sustitucion **y** a
   la deteccion: `find_unresolved_placeholders` hace `continue` ante `UnicodeDecodeError`
   (`new_instance.py:798-800`). Verificado: dos ficheros asi devuelven `[]`. `git show 192c5dea --
   scripts/new_instance.py | grep -c UnicodeDecodeError` da **0**, luego este commit no lo toca.
   Preexistente, fuera de alcance, dejado por escrito para que no se pierda.
3. **Falsos positivos de la misma clase que siguen vivos**: texto del producto con forma
   `{{NOMBRE_EN_MAYUSCULAS}}` dentro de una cadena `rf` seguiria disparando el detector. El criterio
   elegido cubre la subclase numerica, no la clase entera. Yerra del lado seguro (marca de mas, no de
   menos), asi que no es un agujero; es el limite conocido del criterio.

## 6. Observacion nueva, que no es de esta tarea (DECISION-0018)

Hasta este commit la generacion abortaba, asi que **nadie habia podido observar** que el motor de
memoria embarca en cada instancia un banco de 72 tests que en una instancia recien nacida esta rojo
por construccion: dos de sus tests presuponen un repo con historia y con el instanciador presente,
cosas que una instancia nueva no tiene. Cualquier instancia recien parida que corra sus propias
puertas se encuentra ese rojo el primer dia. No lo introdujo 0350 -- 0350 es lo que lo hizo visible.
Se lo paso al Arquitecto para que decida si merece id propio.

## 7. Recomendacion de cierre

**OK-CLOSABLE.** Los seis AC se cumplen, verificados por comportamiento en clon limpio y con control
historico que discrimina. El fix es de criterio y no de enumeracion: sobrevive a coordenadas,
profundidades, extensiones y formas que el maker no eligio, y no esconde ninguna lista de
excepciones. La respuesta a la pregunta de la review es un si cualificado, documentado y falsable en
la seccion 4.4: la fuga existe en el espacio de claves, no en el arbol, y necesita un cambio de
codigo futuro para nacer.

No emito CHANGE-REQUIRED: ningun AC de esta tarea la exige, y ensanchar el encargo en la review es la
misma clase de defecto que el encargo persigue. Emito el residuo 1 como candidato a tarea con id.

-- Analista, 2026-08-13 (checker independiente; no soy el maker y no cierro la tarea)
