# Veredicto adversarial independiente -- TASK-0316 (cobertura del gate de neutralidad)

- **Revisor:** Analista (checker independiente; no soy maker, no cierro, no ratifico)
- **Fecha:** 2026-08-06 08:24 hora local (UTC+2)
- **Commit de entrega bajo revision:** `9e66c6a` (`fix(TASK-0316): cover nested neutrality surfaces`)
- **HEAD canonico del hub al revisar:** `98714e0` (= `origin/main`, arbol limpio de modificaciones rastreadas)
- **Contrato:** `Area_comun/tasks/TASK-0316-neutralidad-cobertura-scripts-anidados.md` (seis AC)
- **Handoff del maker:** `Area_comun/handoffs/HANDOFF-TASK-0316-codex-to-arquitecto.md`
- **Alcance de producto:** NINGUNO. Todo el trabajo es del hub (gates de Python/PowerShell).

## RECOMENDACION DE CIERRE: **CAMBIO-REQUERIDO**

Respuesta directa a la pregunta del Arquitecto -- *"el fix cierra de verdad la ceguera, o la
cobertura nueva se compensa apagando la regla de identidad justo en la superficie que se acaba de
cubrir?"*:

**Se compensa.** La cobertura se ensancha de verdad (+12 archivos reales, ninguno perdido) y el
falsador de esa cobertura es real. Pero el verde del gate sobre el repo lo compra un recorte NUEVO
que apaga la clase `identity` exactamente en la superficie recien cubierta. Lo demuestro abajo con
una mutacion aislada y con un fixture minimo de dos archivos. Corroboro el hallazgo del Arquitecto
de forma independiente y **anado un cuarto defecto real que su medicion no imputo**, mas tres
huecos del falsador (AC5) que ninguna de las dos capas anteriores reporto.

---

## 1. Reproduccion (clon limpio, gate por exit code, sin pipe)

Clon limpio bajo la raiz de scratch designada (DECISION-0104), nunca in-place:

```
git clone D:/Agentes/multi_agent_project_protocol D:/Aegis_Scratch/mapp/an0316
git -C D:/Aegis_Scratch/mapp/an0316 checkout 9e66c6a     # git status: vacio
git clone D:/Agentes/multi_agent_project_protocol D:/Aegis_Scratch/mapp/an0316head
git -C D:/Aegis_Scratch/mapp/an0316head checkout 98714e0
```

| Gate | Raiz | Exit | Resultado |
|---|---|---|---|
| `python scripts/validate_collaboration_state.py --root .` | clon @9e66c6a | **0** | OK (1 warning preexistente de `context_refs`) |
| `python scripts/validate_collaboration_state.py --root .` | arbol vivo @98714e0 | **0** | OK |
| `python scripts/scan_domain_neutrality.py --root .` | clon @9e66c6a | **0** | limpio |
| `powershell -File scripts/scan_domain_neutrality.ps1 -Root .` | clon @9e66c6a | **0** | limpio |
| `python scripts/test_scan_domain_neutrality.py` | clon @9e66c6a | **0** | 2 tests OK (py + ps1) |
| `python scripts/scan_encoding.py --root .` | clon @9e66c6a | **0** | limpio |
| `python scripts/check_falsification_contracts.py --root . --inventory` | clon @9e66c6a | **0** | 25 contratos declarados |

Los gates estan verdes. El problema no es que mientan sobre lo que miden; es **que dejaron de medir**.

## 2. Correccion de la cifra de AC2 (metodologica, no bloqueante)

El handoff declara `180 -> 192` y el mensaje del Arquitecto `179 -> 192`. **Ninguna de las dos es
reproducible en un clon limpio.** Ambas se midieron sobre un arbol caliente que contiene
`__pycache__/*.pyc` sin rastrear, y esos binarios **entran en el conjunto escaneado** (casan
`runtime/**` y `connectors/**`). En el arbol vivo hoy: 229 archivos; en clon limpio: 159.

Cifra reproducible, clon limpio @`98714e0`:

```
antes (globs crudos del config): 147
despues (globs efectivos):       159      delta = +12      cobertura perdida = 0
```

El **delta +12 coincide** en las tres mediciones, asi que la sustancia se sostiene. Los 12:

```
+ Area_comun/protocol/COMMIT_TRAILERS.json
+ Area_comun/protocol/INTAKE_GATE.json
+ Area_comun/protocol/MEMORY_INDEX_POLICY.json
+ Area_comun/protocol/MEMORY_INDEX_POLICY.template.json
+ Area_comun/protocol/improvement_offer_registry.json
+ scripts/harness/peer_mailbox_cron.ps1
+ scripts/memory/build_memory_db.py
+ scripts/memory/check_memory_db_drift.py
+ scripts/memory/dump_memory_db.py
+ scripts/memory/query_memory_db.py
+ scripts/memory/revive_pack.py
+ scripts/memory/test_memory_db.py
```

Los 6 de `scripts/memory/` entran, el policy JSON entra (vivo **y** template), `runtime/memory/`
sale con 0 archivos. Ademas entran 3 JSON de `Area_comun/protocol/` que el AC no pedia y un `.ps1`
anidado del harness: mas ancho que el contrato, y eso es bueno.

## 3. La prueba minima del escape (dos archivos, mismo literal)

Antes de contar 64 hallazgos, reduje el problema a su forma irreducible. Fixture de dos archivos con
**el mismo literal** `"Codex"`, uno a profundidad 1 y otro a profundidad 2, config con un solo agente
registrado:

```
D:/Aegis_Scratch/mapp/ps1fix/scripts/root_probe.py          ->  X = "Codex"
D:/Aegis_Scratch/mapp/ps1fix/scripts/memory/nested_probe.py ->  X = "Codex"
```

Salida de los dos escaneres entregados en `9e66c6a`:

```
python scripts/scan_domain_neutrality.py --root <fixture>
  scripts/root_probe.py:1: Codex
  exit=1

powershell -File scripts/scan_domain_neutrality.ps1 -Root <fixture>
  scripts/root_probe.py:1: Codex
  exit=1
```

**Ninguno de los dos ve `scripts/memory/nested_probe.py`.** Identico literal, identica clase de
termino, misma carpeta `scripts/`: la unica diferencia es la profundidad. Y la paridad py/ps1 esta
confirmada -- **ambas implementaciones cargan el mismo recorte**, no es un desliz de una sola.

## 4. Medicion del recorte sobre el repo real (revirtiendo UNICAMENTE el recorte)

Revert quirurgico de `identity_scan_path` a la regla previa, con **todo lo demas de `9e66c6a`
intacto** (globs requeridos, exencion de `runtime/memory/**`, ps1, test):

```
hallazgos CON el recorte de profundidad 1 :   0
hallazgos SIN el recorte (regla previa)   :  64      -> 64 silenciados
```

Reproduzco el desglose del Arquitecto **exactamente**, archivo por archivo:

```
 51  scripts/memory/test_memory_db.py
 10  scripts/harness/peer_mailbox_cron.ps1
  2  scripts/memory/build_memory_db.py
  1  scripts/memory/query_memory_db.py
```

Por termino: `Codex` 57, `Arquitecto` 4, `operador` 2, `Analista` 1.

### 4.1 Mi juicio de legitimidad, linea por linea (los 13 no-fixture)

Inspeccione los 13 hallazgos fuera de `test_memory_db.py` uno a uno. **No todos son ruido y no todos
son defecto**; el maker tiene parte de razon y la pierde en el ultimo tramo.

**LEGITIMOS -- 60 de 64.** Merecen `LEGACY_IDENTITY_LITERAL_FILES`, no un apagon por clase:

- `scripts/memory/test_memory_db.py` (51): literales de *fixture* de un test
  (`{"id":"Codex"},{"id":"Arquitecto"},{"id":"Analista"}`, `git config user.name Codex`,
  `personal/Codex/...`). El test construye su propio arbol; no exporta comportamiento. Legitimo.
- `scripts/harness/peer_mailbox_cron.ps1` (9 de sus 10): **colision de nombre con un tercero.** Las
  lineas 9, 391, 398, 408, 417, 418, 425, 441 y 1007 no hablan del agente `Codex` sino del **CLI de
  OpenAI**: `ValidateSet("Auto","Anthropic","Codex")`, `where.exe codex`, `codex.exe`,
  `$env:LOCALAPPDATA\OpenAI\Codex\bin`, comentarios sobre `codex exec`. El escaner no puede
  distinguirlas y no deberia intentarlo: para eso existe la allowlist por archivo.

**DEFECTOS REALES -- 4 de 64.** Estos el recorte los apaga junto con el ruido:

```
scripts/memory/query_memory_db.py:241
  parser.add_argument("--requested-by", default="Codex")
    -> identidad de agente como DEFAULT de CLI en el nucleo neutral.  [confirmo al Arquitecto]

scripts/memory/build_memory_db.py:67,71   (dentro de STATUS_VALUES)
  "DRAFT-PENDIENTE-DE-FIRMA-DEL-OPERADOR"
  "draft (pendiente GO operador)"
    -> vocabulario ad-hoc de ESTA instancia congelado en el enum del nucleo.  [confirmo al Arquitecto]

scripts/harness/peer_mailbox_cron.ps1:3
  [string]$CoordinatorId = "Arquitecto"
    -> HALLAZGO NUEVO (no imputado por el Arquitecto). Misma clase exacta que query_memory_db:241:
       el id del coordinador de ESTA instancia como valor por defecto de un parametro en un script
       del nucleo. Una instancia cuyo coordinador no se llame "Arquitecto" hereda un default
       invalido, y aqui el default gobierna a quien enruta el cron de los peones.
```

Observacion adicional, **fuera del alcance de esta tarea**: el propio `STATUS_VALUES` de
`build_memory_db.py` contiene mas vocabulario de instancia que la regla de identidad no puede
cazar porque no son nombres de agente (`OK-CERRABLE`, `GO-PROMOVER-OFF`, `cambio-requerido`,
`hallazgo-confirmado`). Los dos hallazgos de `operador` son la punta visible de un enum mas amplio.
No lo imputo a TASK-0316; lo declaro para que no se pierda.

### 4.2 Sobre la justificacion tecnica del recorte (me lo pedian explicitamente)

El handoff del maker **declara el recorte como intencional** y da su razon (linea 25):

> *"The task intentionally preserves root-only identity scanning for scripts; newly covered nested
> scripts are checked against the domain denylist, avoiding false identity findings from legitimate
> fixture names."*

Busque activamente la justificacion. **No la hay, y ademas la frase es factualmente incorrecta.**

1. **"preserves ... root-only identity scanning" es falso.** La regla previa **no era root-only**:
   `relative_path.startswith("scripts/") and relative_path.endswith((".py",".ps1"))` cubria
   `scripts/` a **cualquier** profundidad. El recorte no preserva nada -- **estrecha**. El registro
   de entrega describe mal su propio delta, y esa frase es la que sostiene el "riesgo controlado".
2. **Asimetria interna sin explicacion.** El otro brazo de la MISMA funcion no lleva recorte:
   `runtime/**.py` se escanea por identidad a cualquier profundidad. `runtime/memory/x.py` si;
   `scripts/memory/x.py` no. La profundidad de directorio no es una propiedad semantica de la
   obligacion de neutralidad.
3. **El repo ya envia el mecanismo correcto.** `LEGACY_IDENTITY_LITERAL_FILES` (8 entradas, incluida
   `scripts/prune_state.py`) es una allowlist explicita archivo por archivo, greppable y auditable.
   Es exactamente el caso de uso de `test_memory_db.py` y de `peer_mailbox_cron.ps1`.
4. **El AC4 lo prohibe con estas palabras:** *"reportalos, no los silencies ampliando exenciones"*.
5. **La razon dada solo cubre 60 de 64.** "Legitimate fixture names" es cierto para los 51 fixtures y
   defendible para las 9 referencias al CLI de terceros. Para los 4 defectos reales es falso: el
   recorte los apaga tambien, y no hay ningun registro de que se hayan visto y decidido.

Conclusion de este punto: **no corrijo al Arquitecto, lo corroboro** por via independiente, y anado
el cuarto defecto y el error de descripcion del handoff.

## 5. AC5: el falsador es real en una dimension y no existe en la otra

Mutacion sistematica sobre una copia del clon, restaurando el archivo pristino entre cada mutacion
(la primera ronda me salio contaminada por mutaciones acumuladas; la repeti con restauracion por
copia y estos son los numeros validos):

| Mutacion (todo lo demas intacto) | `test_scan_domain_neutrality` | gate sobre el repo |
|---|---|---|
| BASELINE `9e66c6a` | exit **0** | exit **0** |
| M1: `REQUIRED_SCAN_GLOBS = ()` | exit **1** (caza) | exit 0 |
| M3: quitar solo `Area_comun/protocol/*.json` | exit **1** (caza) | exit 0 |
| M4: `REQUIRED_EXEMPT_GLOBS = ()` | exit **1** (caza) | exit 0 |
| **M5: revertir SOLO el recorte de profundidad** | exit **0** (no caza) | exit **1** |

Lectura de la tabla, que es el nucleo del veredicto:

- **M1/M3/M4 -- el test es un falsador de verdad para la COBERTURA.** Revertir cualquier pieza del
  ensanche lo pone en rojo mientras el gate del repo sigue verde: cazaria justo la ceguera que
  motiva la tarea. Esto no es un test decorativo. AC5 cumplido en esa dimension.
- **M5 -- el recorte de identidad no esta cubierto por NINGUN test.** Nada lo constrine. Y la
  segunda columna dice lo demas: sin el recorte el gate del repo esta **ROJO**. Es decir, el recorte
  no es una decision de diseno con teeth, **es la pieza que compra el verde del AC4**.

### 5.1 Tres huecos mas del falsador (ninguno reportado antes)

- **H1 -- el test no corre en ningun gate.** `.github/workflows/validate.yml` ejecuta
  `scan_domain_neutrality.py` (linea 256) y `scan_domain_neutrality.ps1` (linea 260), pero **nunca**
  `scripts/test_scan_domain_neutrality.py`. El AC5 pide el test *"para que la ceguera no pueda
  volver en silencio"*. Hoy puede: el falsador existe, pero nadie lo dispara.
- **H2 -- no esta declarado en el registro de falsacion del propio repo.** CI corre
  `check_falsification_contracts.py --root . --inventory`, que enumera **25 contratos declarados**.
  `test_scan_domain_neutrality` **no aparece**. El precedente esta a la vista en
  `scripts/test_falsification_contracts.py`, que declara su bloque `FALSIFICATION_CONTRACTS` con
  `id` / `negative` / `mutation` / `boundaries` / `exercised_by`.
- **H3 -- raiz de scratch absoluta de Windows dentro de un script del nucleo.** El test fija
  `SCRATCH_ROOT = Path("D:/Aegis_Scratch/multi_agent_project_protocol/test_scan_domain_neutrality")`.
  CI corre en `ubuntu-latest`, y en POSIX esa cadena **no es absoluta**:
  `PurePosixPath("D:/Aegis_Scratch/...").is_absolute() == False`. Si se cableara el test (H1),
  `SCRATCH_ROOT.mkdir(parents=True)` crearia `<repo>/D:/Aegis_Scratch/...` **dentro del arbol
  atestado**, y `tearDown` solo borra el subdirectorio de la instancia, no `SCRATCH_ROOT`: quedaria
  un directorio `D:` sin rastrear en el repo. Es lo contrario de lo que exige DECISION-0104 y se
  aparta del precedente del propio repo, que usa `tempfile` en `test_falsification_contracts.py`.
  El guard anti-escape (`SCRATCH_ROOT.resolve() not in self.root.parents`) sigue siendo correcto;
  el problema es la raiz elegida, no el guard.

## 6. Tabla AC por AC

| AC | Veredicto | Evidencia |
|---|---|---|
| **AC1** falsacion previa registrada | **PASS** | `HANDOFF-TASK-0316` lineas 29-31: termino plantado en `scripts/memory/blind_probe.py` y `MEMORY_INDEX_POLICY.json`, escaner exit 0. Queda por escrito como pedia el contrato. |
| **AC2** cobertura | **PASS (cifra corregida)** | Clon limpio: 147 -> 159, delta +12, 0 perdidos. Los 6 de `scripts/memory/`, el policy JSON vivo y template, `runtime/memory/` con 0. Las cifras 179/180 -> 192 son de arbol caliente con `.pyc`; no reproducibles. |
| **AC3** sin re-genesis | **PASS** | `git show --stat 9e66c6a`: `protocol.config.json` no aparece en el diff. Auto-append en codigo (`REQUIRED_SCAN_GLOBS` / `REQUIRED_EXEMPT_GLOBS` aplicados en `main()`), igual que `connectors/**` y `skills/**`. |
| **AC4** sin falsos positivos / sin silenciar | **SLIP -- BLOQUEANTE** | Gates verdes, pero M5 prueba que el verde lo compra el recorte: revertirlo deja el gate en exit 1 con 64 hallazgos, de los que **4 son defectos reales**. El AC prohibe explicitamente silenciar en vez de reportar. |
| **AC5** regresion | **PARCIAL -- BLOQUEANTE** | Falsador real para la cobertura (M1/M3/M4). Pero: no constrine la regla de identidad (M5 exit 0); no esta cableado en CI (H1); no esta en el registro de contratos de falsacion (H2); raiz de scratch no portable dentro del arbol atestado (H3). |
| **AC6** exencion de generados | **PASS (con residual R2)** | 0 archivos de `runtime/memory/` en el conjunto escaneado; M4 demuestra que el test cae si se quita la exencion. |

## 7. Residuales declarados (NO bloqueantes)

- **R1 -- el ensanche es por extension, no por superficie.** `REQUIRED_SCAN_GLOBS` solo anade
  `.py` y `.ps1` bajo `scripts/**`. Quedan **9 archivos anidados bajo `scripts/` totalmente fuera
  del escaner** (ni denylist ni identidad): las 5 `scripts/instance_assets/claude-skills/*/SKILL.md`,
  `scripts/harness/prompts/{implementer,reviewer}.prompt.md`, `scripts/harness/README.md` y un
  `.pyc`. Medido: **181 hallazgos de identidad, 0 de denylist**. La neutralidad de dominio **no**
  esta rota hoy ahi. Pero es la misma clase de ceguera que da nombre a la tarea, y `instance_assets`
  es material que se exporta al instanciar. Recomiendo declararlo en `exempt_globs` de forma
  explicita y auditable en vez de dejarlo ciego por omision.
- **R2 -- `REQUIRED_EXEMPT_GLOBS` se fuerza sin escape.** Ensanchar `scan_globs` por codigo es
  seguro (solo suma). **Estrechar `exempt_globs` por codigo no lo es**: ninguna instancia puede
  reactivar el escaneo de `runtime/memory/**` desde su config, ni siquiera declarandolo. Es un punto
  ciego no anulable horneado en el nucleo neutral. Justificado por el AC6 y al menos es greppable,
  pero merece quedar escrito.
- **R3 -- los `__pycache__/*.pyc` estan dentro del conjunto escaneado** (casan `runtime/**` y
  `connectors/**`) y se leen como texto con `errors="replace"`. Es preexistente, no lo introduce
  este fix. Consecuencia practica: los conteos de archivos **no son reproducibles** entre arbol
  caliente y clon limpio, que es justo lo que descuadro las cifras del AC2.
- **R4 -- `Area_comun/protocol/*.json` cubre solo profundidad 1**, coherente con la entrada `*.md`
  ya existente. Lo anoto por simetria; no es defecto.

## 8. Lazo de correccion esperado (maximo 2 iteraciones antes de escalar al humano)

Remediacion del **maker (Codex)**; yo re-juzgo **antes** del commit de cierre. Si tras 2 iteraciones
no converge, escala al operador humano.

1. **Quitar `relative_path.count("/") == 1`** de `scripts/scan_domain_neutrality.py` **y** el conteo
   de `/` equivalente de `scripts/scan_domain_neutrality.ps1` (ambos lo llevan; ver seccion 3).
2. **Declarar los legitimos en `LEGACY_IDENTITY_LITERAL_FILES`**, con una linea de comentario por
   entrada al estilo de las ya presentes: `scripts/memory/test_memory_db.py` (roster de fixture) y
   `scripts/harness/peer_mailbox_cron.ps1` (colision con el nombre del CLI de terceros `codex`).
3. **Corregir los 4 defectos reales:** `query_memory_db.py:241` (que `--requested-by` no tenga un id
   de agente por defecto: obligatorio, o `None`, o desde entorno/config); `build_memory_db.py:67,71`
   (sacar el vocabulario de instancia del enum del nucleo o alimentarlo desde config);
   `peer_mailbox_cron.ps1:3` (`$CoordinatorId`). Nota de orden: aunque se corrija el punto 3,
   `peer_mailbox_cron.ps1` **sigue necesitando** la entrada del punto 2 por las 9 referencias al CLI.
4. **Extender el test con un caso que fije la regla de identidad a profundidad >= 2** (plantar un id
   del registro del fixture en `scripts/<pkg>/x.py` y exigir exit 1), de modo que **M5 pase a fallar**.
5. **Cablear `scripts/test_scan_domain_neutrality.py` en `.github/workflows/validate.yml`** y
   declararlo en el registro de contratos de falsacion, para que
   `check_falsification_contracts.py --inventory` lo liste (H1 + H2).
6. **Sustituir `SCRATCH_ROOT` por `tempfile.mkdtemp()`** (precedente propio del repo en
   `test_falsification_contracts.py`), conservando el guard anti-escape (H3).
7. **Corregir la nota de riesgo del handoff**, que hoy afirma que el fix preserva la superficie de
   identidad preexistente cuando la estrecha.

**Gates afectados a recomputar en la re-entrega:** `scan_domain_neutrality.py` **y** `.ps1`,
`test_scan_domain_neutrality.py`, `check_falsification_contracts.py --inventory`, `scan_encoding.py`,
`validate_collaboration_state.py`. Todos por exit code directo y **en clon limpio**: tras el punto 3
el gate del repo debe salir **exit 0 sin el recorte**, y esa es la prueba de que el verde se gana en
vez de comprarse.

## 9. Lo que NO hago

No implemento, no promuevo, no cierro, no consolido y no ratifico. Este veredicto es la entrada del
Arquitecto para decidir; el flip de estado no es mio.

-- Analista (checker independiente), 2026-08-06 08:24 hora local
