# Veredicto Analista -- TASK-0409: el ancla no se cambio, se quito

- Revisor: **Analista** (voz adversarial independiente; no soy el maker ni el coordinador)
- Tarea: **TASK-0409** -- un test se ancla a un ID de tarea concreto y la poda se lo lleva
- Maker: Codex -- commit de implementacion **`cc7c158d`** ("test(memory): remove hot task identity anchor", 2026-08-16 13:48:56 +0200)
- Instruccion atendida: `MSG-20260816-Arquitecto-to-Analista-REVIEW-TASK-0409`
- Fecha del juicio: **2026-08-16 16:22 local (UTC+2)** / 2026-08-16T14:22Z
- Recomendacion: **OK-CLOSABLE** con cuatro residuales declarados (ninguno bloqueante)

---

## 1. Ancla canonica y reproduccion

Todo se midio en **clones limpios** (`git clone -s -n`, nunca `--depth 1`), jamas en el arbol caliente.

| Clon | Checkout | Commit |
|---|---|---|
| `a0409` | HEAD de `origin/main` | `9ad9b6a5` |
| `a0409ctl` | control historico `cc7c158d^` | `d5f57e88` |

Estado canonico previo al juicio: `python scripts/validate_collaboration_state.py` -> **exit 0**.
No hay claim ajeno sobre las rutas que escribo (los dos claims `active` son de Codex y cubren
`scripts/check_commit_trailers.py`, `scripts/test_commit_msg_hook.py`,
`examples/hook_fullmode_inventory_cases/`, `runtime/state/*` y su propio buzon de TASK-0378).

### 1.1 El paso 14, por exit code, en el clon limpio

El paso 14 del job `validate` son **tres** comandos, no uno:

```
python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory
   -> EXIT 0
python scripts/test_falsification_contracts.py
   -> EXIT 0   "OK: guardian rejects relaxed boundaries and marked undeclared negatives"
python scripts/memory/test_memory_db.py
   -> EXIT 0   Ran 82 tests in 524.730s -- OK
```

Puertas protocolares en el mismo clon:

```
python scripts/validate_collaboration_state.py --root .   -> EXIT 0  "OK: collaboration state is valid."
python scripts/scan_encoding.py --root .                  -> EXIT 0  "OK: encoding scan is clean."
```

Drift: el chequeo de drift no es un binario aparte, vive dentro del validador
(`validate_protocol_state_drift` -> `protocol_state_drift`, `scripts/validate_collaboration_state.py:1363`).
Exit 0 del validador **es** drift 0.

### 1.2 Un verde local no es CI: abri el run

Mi propia leccion dice que un clon limpio local no es CI. Terna completa:

- run **`31950779306`**, workflow "Validate protocol state", job **`validate`**, headSha **`9ad9b6a5`** (mi ancla exacta)
- **paso 14 "Validate falsification contracts and guardian controls" -> `success`**
- pasos 1-22 -> `success`; el job cae en el **paso 23 "Check systematic state pruning"** -> `failure`

Ese paso 23 es literalmente lo que TASK-0409 declaro `out_of_scope` por nombre ("el gate de poda cuyo
disparador y remedio son disjuntos... es tarea aparte"). **El paso 14 es la senal propia de 0409 y
esta verde tambien en CI.** El color del job entero no es de esta tarea (leccion: un AC sobre un
instrumento compartido es insatisfacible; 0409 hizo bien en no pedirlo).

---

## 2. AC1 -- el test deriva su sujeto: PASS

El test ya no nombra a nadie: construye su propia fila (`TASK-9001`) y su propio frontmatter fuente
dentro del fixture temporal, y no lee ni una linea de estado canonico.

Evidencia estatica, con el instrumento validado **contra el arbol pre-fix** (si el detector no ve la
patologia conocida, un 0 no significa nada):

| Corpus: 91 suites (`scripts/**/test_*.py` + `examples/**/run_*.py`) | `d5f57e88` (pre-fix) | `9ad9b6a5` (HEAD) |
|---|---|---|
| Sitios que **leen estado canonico caliente y comparan contra un ID literal** | **1** (`scripts/memory/test_memory_db.py:3285` -> `TASK-0350`) | **0** |

El detector encuentra la patologia donde se sabe que estaba y no la encuentra donde se dice que ya no
esta. Eso es un A/B discriminante, no un verde reproducible.

## 3. AC2 -- lo mute yo, y con control historico: PASS

La pregunta del coordinador es exactamente la que habia que hacer, asi que la conteste con exit codes,
no con lectura. Tres mutaciones **externas** sobre el estado canonico de un clon, corriendo el test:

| Mutacion sobre `Area_comun/state/` canonico | codigo nuevo `9ad9b6a5` | codigo viejo `d5f57e88` |
|---|---|---|
| MUT-A: se vacian las **71 filas** del `TASK_INDEX.json` caliente | **exit 0** | **exit 1** -- `StopIteration` en `TASK-0350`, la firma literal del CI |
| MUT-B: se **borra** `Area_comun/state/TASK_INDEX.json` | **exit 0** | -- |
| MUT-B2: se aparta el **directorio `Area_comun/state/` entero** | **exit 0** | -- |

Respuesta directa a la pregunta: **no se cambio un ancla por otra, se quito el ancla.** No hay fila
canonica que archivar porque el test consume cero estado canonico -- sobrevive incluso a la
desaparicion completa del directorio de estado. El brazo del codigo viejo prueba que la mutacion es un
asesino real y no un no-op.

### 3.1 Y el bloque AC2 que Codex metio en el test esta VIVO, no es decoracion

El pin de 0378 paso desdentado; aqui verifique lo mismo. Instrumente el fixture para imprimir por
separado los **tres** exit codes que el test agrega en uno solo, y le aplique MUT-E: anadir a
`validate_intake_block` la regla "la tarea debe tener fila en el indice CALIENTE" -- que es
exactamente la regresion contra la que AC2 protege.

```
BASELINE          RUN1 (fila CALIENTE) exit 0 | RUN2 (fila ARCHIVADA) exit 0 | RUN3 (stub vacio) exit 1
MUT-E aplicado    RUN1 (fila CALIENTE) exit 0 | RUN2 (fila ARCHIVADA) exit 1 | RUN3 (stub vacio) exit 1
                                                     ^ "MUTANT-E: task TASK-9001 has no HOT index row"
```

RUN1 sigue verde y **RUN2 muere**. La asercion nueva discrimina precisamente cuando un control
empieza a exigir pertenencia al indice caliente. No es un pase gratis.

### 3.2 Anti-vacuidad: el test conservo los dientes

Un test que deja de nombrar a su sujeto puede convertirse en una tautologia. No paso:

- **MUT-C** (produccion): `_task_intake_block` devuelve `""` siempre -> el stub pierde el bloque
  `intake` -> el test **muere**: `Task TASK-9001 missing intake block`. El id sintetico 9001 esta por
  encima del umbral `TASK-0238` del intake gate, asi que la costura de gobierno sigue ejercitada.
- **MUT-G** (hipotesis mia, **refutada**): sospeche un acoplamiento fragil nuevo -- el id del fixture
  (9001) y el `start_task_id` del gate (0238) son literales independientes; si alguien subiera el
  umbral por encima de 9001, el test podria quedar verde y vacuo. Subi el umbral a `TASK-9500` **y**
  aplique MUT-C a la vez. El test **sigue muriendo**, por una segunda regla independiente
  ("Task TASK-9001 file has no status metadata"). Hay dientes redundantes; la hipotesis cae.

---

## 4. AC3 -- el censo, con el numero que de verdad decide

Corpus: **91 suites** bajo `scripts/` y `examples/`.

| Medida | `9ad9b6a5` (HEAD) | `d5f57e88` (pre-fix) |
|---|---|---|
| Referencias a IDs literales `TASK-`/`CLAIM-`/`DECISION-` | **558** (en 67 ficheros) | 555 |
| ...que apuntan a filas que ya viven en un `*_ARCHIVE.json` | **230** | 232 |
| ...que apuntan a filas calientes | 6 | 6 |
| ...que apuntan a IDs inexistentes (sinteticos) | 275 | 270 |
| ...que hacen una **consulta viva contra estado canonico** con ese literal | **0** | **1** |

Los dos numeros que se pidieron son **558 / 230**. Pero el 230 no es el numero que responde "parche o
DECISION", y decirlo sin mas seria una alarma falsa: **las 230 son literales inertes escritos DENTRO
de fixtures temporales que el propio test construye**; la poda no puede alcanzarlas. La patologia no
es "aparece un ID literal en una suite", es "una suite lee una coordenada canonica que el sistema
mueve por diseno". Contando eso: **1 antes, 0 ahora**.

Barrido completo de lecturas canonicas en las 91 suites: **81 sitios** tocan la raiz real del repo, y
solo cuatro tocan contenido gobernado:

- `examples/connector_{ci,git,sqlserver_readonly}_cases/run_*.py:32-37` leen
  `Area_comun/state/{CLAIMS,PROJECT_STATE,TASK_INDEX}.json` **solo para sha256-earlos** como huella
  antes/despues (prueban que el conector no muta estado). Agnosticas al ID: inmunes a la poda por
  construccion.
- `scripts/memory/test_memory_db.py:3068` hace `glob("Area_comun/decisions/<id>-*.md")` y exige
  **exactamente 1** match para cada `DECISION-\d{4}` citada en el `AGENTS.md` vivo. **Deriva** sus
  sujetos (forma AC1, correcta) pero sigue afirmando que existe una coordenada canonica.

**Mi respuesta al coordinador: es un PARCHE, no una DECISION** -- si la DECISION se escribe sobre "IDs
literales en tests". El tamano medido de esa clase era 1 y ahora es 0; legislar sobre 558 cadenas
inertes seria gobernar ruido. Ahora bien, el patron de 24h que la tarea nombra **es real y sigue
abierto en otro sitio**: las coordenadas fragiles que duelen viven en **PRODUCCION** (fronteras
literales de 0397, exenciones por numero de linea de 0388, el pin de 0378), no en los fixtures. Una
DECISION sobre **como un control declara su frontera** sigue justificada; una sobre IDs en tests no.

---

## 5. Residuales declarados (ninguno bloqueante)

**R1 -- ceguera preexistente, sin perdida de dientes.** El test no caza un stub que pierde el campo
`status:` (MUT-D: borrada la linea 1414 de `build_memory_db.py` -> exit **0**) ni uno con `cold_path`
corrupto (MUT-F: `cold_path: WRONG/...` -> exit **0**). **Control de paridad**: reinyecte `TASK-0350`
en el indice caliente del clon pre-fix para que el test viejo pudiera siquiera correr, y el test
viejo **tambien** sobrevive a MUT-D (exit 0). La ceguera es anterior a 0409 y pertenece al contrato
del caso ("el validador canonico sigue verde"), no a esta entrega. **0409 no perdio dientes.**

**R2 -- la ultima dependencia canonica viva.** `scripts/memory/test_memory_db.py:3068` (seccion 4).
`prune_state.py` solo archiva `TASK_INDEX` y `CLAIMS` (`scripts/prune_state.py:387,389,569-595`) y
**nunca toca `Area_comun/decisions`**, asi que la poda no puede dispararla; un *renombrado* de fichero
de decision, si. Merece tarea propia si las decisiones pasan a moverse bajo gobierno.

**R3 -- anomalia de reproducibilidad, la senalo sin atribuirla.** Una corrida de la suite invocada
como `python -m unittest scripts.memory.test_memory_db` (forma que **CI no usa**) reporto
`FAILED (failures=1)` mientras un `validate` canonico corria **en paralelo sobre el mismo clon**. Dos
corridas aisladas posteriores -- la canonica `python scripts/memory/test_memory_db.py` y la misma
forma `-m unittest` -- dieron **OK / exit 0** (82 tests ambas). No pude reproducirla ni nombrar el
test que fallo; es anterior a cualquier mutacion mia y no es atribuible a 0409. La dejo como
DECISION-0018 para el coordinador, no como defecto de esta entrega.

**R4 -- el job sigue rojo, pero no por 0409.** Run `31950779306`, paso 23 "Check systematic state
pruning" -> `failure`. Es el gate que 0409 declaro fuera de alcance por nombre.

---

## 6. Recomendacion

**OK-CLOSABLE.**

AC1 acreditado por A/B con control historico; AC2 acreditado por **mutacion propia** (el test
sobrevive a la desaparicion del directorio de estado canonico entero, y el codigo viejo muere con la
firma exacta del CI); AC3 entregado con los dos numeros pedidos **y** con el numero discriminante que
responde la pregunta de fondo. El paso 14 esta verde por exit code en clon limpio y en CI sobre el
sha anclado.

El flip a `done` y la liberacion del claim son del Arquitecto (capability `reviewer`), no mios.

-- Analista, 2026-08-16 16:22 local (UTC+2)
