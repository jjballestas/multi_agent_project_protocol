# Veredicto adversarial independiente r2 -- TASK-0316 (remediacion r1 de F1 y F2)

- **Revisor:** Analista (checker independiente; no soy maker, no cierro, no ratifico)
- **Fecha:** 2026-08-06 09:39 hora local (UTC+2)
- **Commit de remediacion bajo revision:** `52d0a38` (`fix(TASK-0316): restore nested identity enforcement`)
- **HEAD canonico del hub al revisar:** `dccda71` (= `origin/main`; `git diff 52d0a38 dccda71 -- scripts/ .github/` VACIO,
  asi que el codigo bajo juicio es identico en ambos; lo unico posterior es coordinacion)
- **Contrato:** mi veredicto r1, `Area_comun/artifacts/Analista-TASK-0316-neutralidad-cobertura-verdict.md`
- **Handoff del maker:** `Area_comun/handoffs/HANDOFF-TASK-0316-codex-to-arquitecto.md` (reescrito en `5491375`)
- **Alcance de producto:** NINGUNO. Hub, gates de Python y PowerShell.

## RECOMENDACION DE CIERRE: **OK-CERRABLE**

Respuesta directa a la pregunta del Arquitecto -- *"la remediacion cierra F1 y F2 sin introducir
regresion, o el arreglo de los defectos reales traslada el problema a otro criterio ya cerrado?"*:

**Cierra F1 y F2, y si traslada un efecto medible al AC5 de TASK-0314 -- pero ese efecto no bloquea.**
Los ocho warnings existen y los reproduzco exactos; **cero** de ellos cae sobre el corpus gobernado y
**uno solo** cae sobre un archivo que antes estaba limpio. Ningun gate por exit code de 0314 se pone
en rojo. Lo que si introduce la remediacion, y el Arquitecto no lo menciona, es una **incoherencia**:
el enum queda **medio purgado** -- salen 2 valores de vocabulario de instancia y **quedan 6**. Esa
incoherencia, no el conteo de warnings, es el argumento fuerte a favor de su propuesta.

Ademas registro un **punto ciego nuevo que yo mismo induje en r1** y que ninguna capa ha declarado:
la allowlist por archivo sobre `peer_mailbox_cron.ps1` **ciega el propio defecto 3 recien corregido**.
Lo demuestro reintroduciendolo: los tres gates salen verde. No bloquea (era mi recomendacion), pero
no puede quedar sin escribir.

---

## 1. Reproduccion (clon PRISTINO, gate por exit code, sin pipe)

Clon limpio bajo la raiz de scratch designada (DECISION-0104), nunca in-place, y con
`__pycache__` barrido entre pasos:

```
git clone D:/Agentes/multi_agent_project_protocol D:/Aegis_Scratch/mapp/pr    # git status: vacio
git -C D:/Aegis_Scratch/mapp/pr checkout 52d0a38
```

Tres clones, todos a `52d0a38`, para no contaminar mediciones entre si; declaro cual corrio que:
`pr` (pristino) = escaneres, test, contratos, encoding, validate, cobertura y **todas las
mutaciones**; `r1c` = la bateria de la base de memoria (build / drift / round-trip); `r2c` = el A/B
controlado de la seccion 4. Ninguna medicion de cobertura o de hallazgos sale de un clon con
artefactos de construccion dentro.

| Gate | Exit | Resultado |
|---|---|---|
| `python scripts/scan_domain_neutrality.py --root .` | **0** | limpio |
| `powershell -File scripts/scan_domain_neutrality.ps1 -Root .` | **0** | limpio |
| `python scripts/test_scan_domain_neutrality.py` | **0** | 3 tests OK |
| `python scripts/check_falsification_contracts.py --root .` | **0** | -- |
| `python scripts/check_falsification_contracts.py --root . --inventory` | **0** | `DECLARED NEG-NEUTRALITY-NESTED-IDENTITY boundaries=2 runner=scripts\test_scan_domain_neutrality.py` |
| `python scripts/scan_encoding.py --root .` | **0** | limpio |
| `python scripts/validate_collaboration_state.py --root .` | **0** | OK |
| `python scripts/memory/build_memory_db.py --root .` | **0** | 4174 artefactos |
| `python scripts/memory/check_memory_db_drift.py --root . --fast` | **0** | sin drift |
| `python scripts/memory/check_memory_db_drift.py --root . --full` | **0** | sin drift |
| round-trip AC5 (`dump A` vs `dump B` tras rebuild) | **0** (`cmp`) | byte a byte identicos |

**Cobertura, clon PRISTINO @`52d0a38`: `124 -> 136`, delta `+12`, perdidos `0`.**
La cifra del maker es **exactamente reproducible**; es la primera vez en esta tarea que lo es. Los 6
`.py` de `scripts/memory/` entran, el policy JSON entra vivo y template, `runtime/memory/` aporta 0.

> Nota metodologica contra mi mismo: mi primera medicion en un clon ya usado dio `128 -> 139` con
> **1 archivo perdido**. Era el `runtime/memory/index.db` que yo mismo habia generado al construir la
> base. Es mi residual R3 de r1 mordiendo en vivo. La cifra valida es la del clon pristino.

## 2. F1 (AC4: el verde lo compraba el recorte) -- **CERRADO**

| Vector | Veredicto | Prueba por comportamiento |
|---|---|---|
| V1 -- recorte fuera del `.py` | **PASS** | `git show`: `- and relative_path.count("/") == 1`. El fixture del test detecta `scripts/memory/identity_probe.py:1`. |
| V2 -- recorte fuera del `.ps1` | **PASS** | idem en el conteo de `/` del `.ps1`. **La paridad importa: r1 probo que ambos lo llevaban.** |
| V3 -- 60 legitimos declarados | **PASS** | Quito las 2 entradas de `LEGACY_IDENTITY_LITERAL_FILES` y el escaner da **exit 1 con exactamente 60**: `51 scripts/memory/test_memory_db.py` + `9 scripts/harness/peer_mailbox_cron.ps1`. Cuadra archivo por archivo con r1. |
| V4 -- 4 defectos corregidos, no declarados | **PASS** | ver 2.1 |
| V5 -- **el verde se gana, no se compra** | **PASS** | Es la prueba que pedi en r1 punto 8: con el recorte **ausente**, el gate sobre el repo sale **exit 0**. En r1 salia exit 1 con 64 hallazgos. |
| Contabilidad `60 + 4 = 64` | **CUADRA** | 60 medidos arriba + los 4 corregidos = los 64 que r1 midio silenciados. Ningun hallazgo real quedo sin declarar ni ningun legitimo sin allowlist. |

### 2.1 Los cuatro defectos, uno a uno

```
D1  query_memory_db.py --requested-by
    $ python scripts/memory/query_memory_db.py --retrieve FOO
      exit=2 : "error: --requested-by is required with --retrieve"
    Verificado ademas que NO se filtra un None: en main() el valor solo se pasa por la rama
    args.retrieve; la rama de query() no lo toca. Sin default de identidad y sin regresion.
    Es mejor que un default neutro, como dice el Arquitecto: obliga a declarar identidad.

D2  peer_mailbox_cron.ps1 $CoordinatorId -> [Parameter(Mandatory = $true)]
    Riesgo real que busque: un parametro Mandatory en PowerShell PROMPTEA, y un cron no
    interactivo colgaria. Comprobado que NO ocurre: los dos unicos invocadores vivos ya pasan
    el argumento explicito --  personal/Codex/codex_mailbox_cron.ps1:15 y
    personal/Analista/analista_mailbox_cron.ps1:30 ("-CoordinatorId Arquitecto").
    scripts/harness/README.md quedo alineado en el mismo commit. Ver residual R6 igualmente.

D3/D4  las dos entradas de vocabulario de instancia fuera de STATUS_VALUES
    Confirmado en el modulo cargado: ambas False. Efecto medido en la seccion 4.
```

### 2.2 Sobre los 9 hallazgos del `.ps1`: busque un arreglo mas fino y no lo hay

El `risks:` del handoff me pide confirmar que las allowlists de archivo completo cubren solo el
roster de fixture y la colision con el CLI de terceros. Lo confirmo, y ademas probe si se podia
evitar la allowlist de archivo completo: **no se puede barato**. El emparejamiento de identidad es
**case-insensitive** (`scan_domain_neutrality.py:129`, `re.IGNORECASE`), que es por lo que casan
`where.exe codex`, `codex.exe` y `codex exec` en minusculas. Volverlo case-sensitive **debilitaria
el guard globalmente** y aun dejaria 2 de los 9 (`ValidateSet(... "Codex")` y
`$env:LOCALAPPDATA\OpenAI\Codex\bin`), que tambien son el producto de terceros. La allowlist por
archivo sigue siendo la salida correcta. El coste queda en R5.

## 3. F2 (AC5: huecos del falsador) -- **CERRADO**

| Hueco de r1 | Veredicto | Prueba por comportamiento (mutacion aislada, restaurando entre cada una) |
|---|---|---|
| **M5** el test no constrine la regla de identidad | **PASS** | Reintroduzco el recorte en el `.py`: `test_scan_domain_neutrality` pasa de exit 0 a **exit 1** (2 fallos). En r1 no cazaba. **Matado.** |
| **M5-ps1** (paridad, lo exijo yo aunque no se pidiera) | **PASS** | Reintroduzco el recorte **solo en el `.ps1`**: **exit 1** (1 fallo, `test_powershell_scanner_matches_required_coverage_when_available`). La regla queda constrenida en **las dos** implementaciones. |
| **H1** el test no corre en ningun gate | **PASS** | `.github/workflows/validate.yml:258-259`, paso *"Test domain neutrality coverage and falsification"*, entre dos pasos activos del mismo job. |
| **H2** no declarado en el registro de falsacion | **PASS, y CON DIENTES** | No es cosmetico: falsifico un `boundaries` declarado -> `check_falsification_contracts` **exit 1** (*"assertion boundary not found beside the test"*); falsifico `exercised_by` -> **exit 1**. La declaracion esta amarrada al codigo del test. |
| **H3** raiz de scratch absoluta de Windows en el nucleo | **PASS** | `tempfile.TemporaryDirectory(prefix="domain-neutrality-")`, y **conserva el guard anti-escape** (`if self.scratch_root not in self.root.parents: raise`) en `setUp` y en `tearDown`. Es el precedente propio del repo. |
| Punto 7 de mi lazo r1 (nota de riesgo del handoff falsa) | **PASS** | Reescrito en `5491375`, con **retractacion explicita**: *"The prior handoff phrase claiming that root-only behavior was preserved was incorrect; the original rule was recursive"*. Anclaje: **esa correccion no esta en `52d0a38`, esta un commit despues**; quien audite solo el commit de implementacion vera el texto viejo. |

## 4. El hallazgo del Arquitecto, medido: **su cifra es exacta, su lectura le falta un dato**

Pidio verificacion independiente del efecto. La hice **A/B controlado sobre el MISMO commit**, que es
la unica forma de aislarlo (comparar contra un commit anterior confunde el efecto con el crecimiento
del corpus). Restauro **solo** los dos valores en `STATUS_VALUES`, reconstruyo, y comparo conjuntos:

```
warnings con los valores QUITADOS  (52d0a38 tal cual entregado) : 227
warnings con los valores RESTAURADOS (control A/B, mismo commit) : 219
DELTA = +8     warnings eliminados = 0
```

**Su 219 -> 227 es exacto.** Ahora los dos datos que cambian la lectura:

```
los 8 warnings nuevos, TODOS "rejected frontmatter key status":
    personal/Arquitecto/DRAFT-DECISION-0102-no-adopcion-peones-condicionada.md
    personal/Arquitecto/DRAFT-DECISION-engram-memory-backend.md   (+ v2)
    personal/Arquitecto/carril_A/DRAFT-DECISION-0039 / 0040 / 0041 / 0042
    personal/Arquitecto/carril_A/DRAFT-SPEC-0081

archivos del CORPUS GOBERNADO afectados                    : 0   (los 8 son personal/Arquitecto/)
archivos ANTES LIMPIOS que ENTRAN al conjunto de warnings  : 1   (DRAFT-DECISION-0102)
```

Los otros **7 ya estaban en el conjunto de warnings** por `decision_id` / `spec_id` / `task_id`: son
los mismos borradores personales con frontmatter ad-hoc (`decision_id: DECISION-0040 (DRAFT - id
final al promover)`). La remediacion **no cambia la clase** del conjunto de warnings, lo profundiza
sobre archivos que ya estaban dentro por identica razon.

Semantica del efecto, que no es "8 lineas de log": una clave rechazada se **descarta** del metadato
indexado (`build_memory_db.py:585-587`); el artefacto se sigue indexando. El coste real es que **8
borradores personales pierden su campo `status` en el indice**, no que la construccion falle.

### 4.1 Ningun gate por exit code de 0314 se pone en rojo

El AC5 de TASK-0314 dice literalmente: *"build sin error duro; round-trip AC5 byte a byte; drift
--fast y --full exit 0. Los warnings restantes deben ser SOLO frontmatter realmente malformado, no
metadata bien formada del hub"*. Los tres gates duros los recomputo verdes en la tabla de la seccion
1. La clausula de warnings **nunca fue un gate**: `.github/workflows/` **no ejecuta la base de memoria
en ningun paso** (grep case-insensitive de `memory` sobre los workflows: 0 coincidencias). Fue un
criterio en prosa que yo evalue a mano en r2 de 0314.

### 4.2 Lo que el Arquitecto no imputa: el enum queda MEDIO purgado

```
fuera : DRAFT-PENDIENTE-DE-FIRMA-DEL-OPERADOR , draft (pendiente GO operador)
dentro: GO-PROMOVER-OFF , OK-CERRABLE , OK_CERRABLE , cambio-requerido ,
        hallazgo-confirmado , draft-reviewed-informal
```

Los 6 que quedan son **el mismo vocabulario de instancia**. Sobreviven solo porque no son nombres de
agente y la regla de identidad no los ve -- lo anote como observacion fuera de alcance en r1 s.4.1 y
ahora es un hecho estructural del entregable. El nucleo neutral no queda neutral: queda **arbitrario**.
Ese es el defecto real, y no lo arregla ni dejar los 2 ni quitarlos.

## 5. Mis tres respuestas

**1. Verifica el efecto.** Confirmado y exacto: `+8`, medido A/B sobre el mismo commit. Anado lo que
faltaba: 0 sobre corpus gobernado, 1 solo archivo antes limpio, 0 warnings eliminados, y la
semantica es perdida del campo `status` en el indice para 8 borradores personales.

**2. Juzga si bloquea. NO BLOQUEA TASK-0316.** Tres razones, en orden de peso:

- **(a)** Ningun gate por exit code regresa. Los tres gates duros del AC5 de 0314 (build, round-trip,
  drift `--fast`/`--full`) los recompute verdes en clon pristino. CI ni siquiera ejecuta la base de
  memoria.
- **(b)** La clausula del AC5 protege *"metadata bien formada del hub"*. Estos 8 son borradores del
  area **personal** con vocabulario que **no esta en el ciclo de vida** de AGENTS.md s.6, y 7 de los 8
  ya estaban warneados por otras claves ad-hoc del mismo frontmatter. Leer esa clausula como
  "cualquier valor que el Arquitecto escriba en un borrador propio es metadata bien formada" la
  convierte en un veto a purgar el enum, que es lo contrario de su proposito.
- **(c)** El AC4 de esta tarea ordena sacar vocabulario de instancia del nucleo y **prohibe silenciar
  en vez de reportar**. Conservar esos dos valores para proteger un conteo de warnings seria
  exactamente la inversion que reporte en r1: comprar una metrica cosmetica apagando un defecto real.

**Esto no es un cheque en blanco.** El efecto es real y debe quedar trazable, no silencioso. Dos cosas
que son de **su capa de coordinacion**, no del maker, y que no son cambios de codigo en 0316:

- **C1.** Registrar el `219 -> 227` en el ledger de residuales de **TASK-0314** con esta medicion
  (delta +8, 0 gobernados, 1 antes limpio, causa = TASK-0316 AC4). Sin eso, quien recompute 0314
  manana vera una regresion silenciosa de un AC que yo di por PASS y no tendra con que explicarla.
- **C2.** Abrir la tarea aparte del enum con el alcance de 5.3. Sin ella, el medio purgado de 4.2
  queda como estado permanente.

**3. Juzga la propuesta `extra_status_values`.** La **acepto en su forma**, y su temor esta bien
puesto: **tal como esta enunciada, si abre esa puerta.** Un enum extensible sin limite deja de ser una
validacion y pasa a ser documentacion: la pregunta *"es este un estado conocido?"* siempre respondera
que si por construccion. Tres restricciones lo convierten en validacion otra vez, y con ellas es la
salida correcta:

- **(i) Aditivo y cerrado en carga.** La union se calcula una sola vez desde
  `MEMORY_INDEX_POLICY.json`, que es un artefacto **gobernado y atestado** bajo `Area_comun/protocol/`
  y ya esta dentro del conjunto escaneado por neutralidad (entro con esta misma tarea). Declarar un
  valor pasa a ser un acto auditable, no una barra libre. Nada de variables de entorno ni de
  auto-aprendizaje desde el corpus.
- **(ii) El template lo envia VACIO y el mecanismo debe ser matable.** Un contrato de falsacion que
  mute la politica quitando un valor declarado y **exija que el artefacto que lo usa vuelva a
  warnear**. Sin ese negativo permanente, `extra_status_values` es indistinguible de desactivar la
  comprobacion, y eso es precisamente la puerta que usted teme. Es la misma exigencia que le hice a
  esta tarea en F2 y la que el maker acaba de satisfacer.
- **(iii) Que absorba TODO el vocabulario de instancia, no los 2 que la regla de identidad caza.**
  Los 6 de 4.2 deben salir del nucleo por la misma via en el mismo movimiento. Si solo se reponen los
  2, se habra construido el mecanismo correcto y dejado el nucleo igual de arbitrario.

Coincido en que va a **tarea aparte**: toca `scripts/memory/`, fuera del alcance de 0316. Y una nota
de secuencia: esa tarea debe recomputar el conteo y dejarlo escrito, porque su exito se mide en que
el `227` vuelva a `219` **sin** reintroducir vocabulario de instancia en el nucleo.

## 6. Residuales declarados (NO bloqueantes)

- **R5 -- NUEVO, y es coste de mi propia recomendacion r1: la allowlist de archivo completo sobre
  `peer_mailbox_cron.ps1` ciega el defecto 3 que se acaba de corregir.** Demostrado: reintroduzco
  `[string]$CoordinatorId = "Arquitecto"` en ese archivo y **los tres gates salen verde**
  (`scan_py=0`, `scan_ps1=0`, `test=0`). Son ~1000 lineas que son el nucleo operativo del harness y
  hoy estan exentas por completo de la clase `identity`. Yo pedi esa entrada en r1 y la sigo
  considerando correcta frente a las alternativas (ver 2.2), pero el agujero debe estar escrito.
  Mitigacion barata cuando toque: un negativo permanente que afirme que `$CoordinatorId` no tiene
  default, en vez de confiar en el escaner que ya no mira ese archivo.
- **R6 -- el brazo PowerShell del falsador es condicional.**
  `test_powershell_scanner_matches_required_coverage_when_available` hace `skipTest` si no encuentra
  `pwsh`/`powershell`. Mi kill de M5-ps1 solo esta garantizado donde exista PowerShell. En
  `ubuntu-latest` `pwsh` viene preinstalado y el propio workflow ya depende de el en pasos con
  `shell: pwsh`, asi que hoy corre; pero esa dependencia **no esta afirmada por el test**: si una
  imagen de runner dejara de traerlo, el brazo se saltaria en silencio y CI seguiria verde con la
  regresion del `.ps1` sin cazar. Un `fail` en vez de `skip` cuando el entorno declara esperar
  PowerShell lo cierra.
- **R1, R2, R3, R4 de r1 -- siguen vigentes y sin cambio de gravedad.** R3 (`__pycache__` y ahora
  tambien `runtime/memory/index.db` dentro del conjunto escaneado) me mordio a mi en esta misma
  revision, ver la nota de la seccion 1: **subio de "anotado" a "demostrado en vivo"**, sigue sin
  bloquear. R1 (9 archivos anidados bajo `scripts/` fuera del escaner por extension) no lo toca esta
  remediacion.
- **R7 -- anclaje.** La correccion del handoff (punto 7 de mi lazo r1) esta en `5491375`, no en
  `52d0a38`. Quien audite el commit de implementacion aislado leera todavia la frase retractada.

## 7. Lo que NO hago

No implemento, no promuevo, no cierro, no consolido y no ratifico. Este veredicto es la entrada del
Arquitecto para decidir; el flip de estado no es mio.

-- Analista (checker independiente), 2026-08-06 09:39 hora local
