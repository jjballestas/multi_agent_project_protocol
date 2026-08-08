# MEMORY - Analista (voz analista; firma "Analista", antes "Claude-analista") - multi_agent_project_protocol

> FIRMA (2026-06-15, orden del operador): firmo como **Analista** (sin prefijo "Claude-", que confunde con
> el arquitecto Claude). Mensajes from: Analista / to: Analista. Carpeta personal/Analista/ por ahora.
> Runbook privado de la voz analista. Conciso: rol + estado de la ultima sesion + lecciones.
> El detalle tecnico profundo (escritor unico, flags, capabilities) vive en `personal/Arquitecto/MEMORY.md`
> (arquitecto). Yo no muto estado; solo lo entiendo.
> Ultima actualizacion: 2026-07-22 (8) (TASK-0283 CIERRE iter3 NO-GO/CHANGE-REQUIRED sobre commit 8b61b05, veredicto commit 3ed3af2: acceptance REFINADO por el Arquitecto -completitud absoluta retirada por indecidible-; el maker cambio el glob a `rglob("*.py")` sobre examples/ Y scripts/ -> CASO C cerrado en el eje de FICHERO: coloque negativos marcados sin contrato en subdir profundo + nombre no estandar bajo AMBOS arboles -> visibles y rojos, missing=2 exit1; A3 marcador load-bearing -quitarlo pone stale-loud- y A4 regresion de contrato declarado siguen con dientes. BLOQUEANTE = escape NUEVO por PLACEMENT: `permanent_negatives()` y `function_source()` iteran solo `tree.body`, asi que un negativo REAL con su marcador `PERMANENT_NEGATIVE:` correcto pero escrito como METODO DE CLASE (A2a) o FUNCION ANIDADA (A2b) es INVISIBLE -> 15/15/0 exit0. NO es el caso retirado -alli la senal esta AUSENTE; aqui el marker esta PRESENTE y el walk somero lo descarta-; rompe la clausula #2 -marker necesario pero NO suficiente, la colocacion top-level tampoco esta escrita- y la mitigacion documentada -revision/CI- NO lo atrapa porque el revisor VE el marcador y asume cobertura; el export new_instance.py lo propaga a suites basadas en clase -unittest/pytest-. Remediacion iter 1 de 2: F1 ast.walk / F2 fail-closed sobre marcador extraviado + doc de colocacion; anadir 2 casos al self-test -metodo Y anidado->rojo-. Clon limpio /d/c283i3, exit codes. PRUNE DUE 95.35>=90 senalado no corrido -es del Arquitecto-. SIN PRODUCTO EN ALCANCE); antes (7) (TASK-0283 RE-JUICIO del denominador independiente NO-GO/CHANGE-REQUIRED sobre commit 2a52e0c, veredicto commit fae8e02: el maker cerro mi bloqueante de iter1 -denominador REAL independiente de la lista de contratos, `missing` computado, un negativo MARCADO sin contrato -> ROJO missing=1 exit1, y Q1a/Q4 siguen con dientes- PERO el universo es auto-declarado DOS veces: una funcion solo entra si lleva el marker `PERMANENT_NEGATIVE:` Y vive en `examples/**/run_*.py`; inyecte un negativo REAL sin marker (B) -> invisible 14/14 missing=0, y un negativo REAL con marker en fichero fuera del glob (C) -> invisible; corrobora `attestation_negative_cases` -negativos reales sin marker, no contados- que choca con acceptance #3 clausula 2 "sin dejar el resto pendiente indefinido"; iteracion 2 de 2 -> escale al operador la DECISION DE ALCANCE -marcado-solo vs estructural- con dos direcciones R1 fail-closed / R2 enrolar-el-resto; prune vencido 94.59>=90 senalado no corrido; SIN PRODUCTO EN ALCANCE); antes (6) TASK-0283 el guardian del guardian NO-GO/CHANGE-REQUIRED, veredicto commit 4925de5: el checker de falsabilidad es un validador de DECLARACION por subcadena -- tiene dientes contra la DEGRADACION de un contrato declarado -Q1a borrar frontera real / Q4 relajar una de dos ambos rojos- pero NO contra la ENTRADA de un negativo no declarado -inyecte un test-sombra sin contrato y el inventario siguio 14/14 verde-; `missing=0` es literal sin denominador independiente; choca con acceptance #3 y la pregunta del REVIEW; remediacion = denominador independiente + self-test negativo-no-declarado->ROJO; re-juicio mio, max 2 iter; prune vencido senalado no corrido). Antes (5) TASK-0274 RE-JUICIO del negativo del flag GO/OK-CLOSABLE sobre entrega 0831701 / fix de test 77afe05, veredicto commit 0c9f089: la remediacion TEST-ONLY anadio en case_cli_is_a_real_aborting_gate la corrida AISLADA que pedi -- `--check-drift --root <root> --bogus-flag` con assert !=0 -- y en clon limpio MutC (parse_known_args) AHORA deja la suite ROJA en ese caso (error = salida CLEAN de la combinacion aislada), la canonica pasa 9/9, produccion byte-identica d7bd4d3 (los 6/6 vectores siguen vigentes), MutA/MutB siguen rojos; los TRES negativos del gate tienen dientes; pregunta de gating del Arquitecto = SI; ruteado GO, cierre (done-flip + release) es del orquestador. Antes (4) TASK-0274 CHANGE-REQUIRED sobre 6f2084f, veredicto commit 4ce8b2e: el gate es REAL en produccion -- 6/6 vectores PASS y MutA/MutB con dientes -- PERO el negativo PERMANENTE del flag desconocido esta confundido y NO enrojece bajo parse_known_args (MutC queda verde), el mismo anti-patron que la unidad erradica una capa abajo; fix de una linea de test, re-juicio con MutC como criterio de dientes; antes (3) TASK-0279 gate de trailers en commit-msg GO/OK-CLOSABLE sobre 15fe9c8, veredicto commit 7908874: el gate ABORTA las cuatro clases con commits reales, respeta la tarea podada real, cada negativo enrojece al mutar su guarda, y es espejo fiel -- mas estricto -- del validador post-hoc; deuda del runner de instanciacion PREEXISTENTE confirmada; antes TASK-0284 banco RE-JUICIO GO sobre 947c6f5).

## Ultima actualizacion 2026-08-08 (48) - TASK-0334 repos embebidos: CHANGE-REQUIRED (iter 1 de 2)

- Encargo `MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0334`. **SIN PRODUCTO EN ALCANCE.**
- Entrega `7692a561`; veredicto **CHANGE-REQUIRED** en `f795d04a`
  (artifact `Area_comun/artifacts/ANALISTA-TASK-0334-repo-embebido-invisible-veredicto.md`).
- Gates en clon limpio sobre el commit exacto, por exit code: harness 22/22, contratos 49/49 y 8/8
  cableados, validate, encoding, neutralidad, drift 0, arbol vacio.

### Leccion 1: arreglar la CEGUERA de un lector puede romper OTRO consumidor del mismo lector

El fix hace que `Get-GitStatusPorcelainUtf8` / `dirty_paths` interroguen cada repo embebido por
separado. Correcto para `dirty_claimed_route` (sobre-detectar VETA = protege). Pero el MISMO lector
alimenta `Get-StagedResidueState`, donde sobre-detectar **BLOQUEA** el exec del peer. **Direcciones
de seguridad opuestas sobre un lector compartido.** Al interrogar el embebido se descarta el
`.gitignore` del padre: en este hub `.protocol-tmp/` esta ignorado y ahi viven 3 de los 6 embebidos
-> +1471 rutas. Falsacion: fixture con la forma del hub -> pre-fix `RESIDUE_STATE=none`, post-fix
`RESIDUE_STATE=live`. **Al revisar un lector compartido: enumerar TODOS sus consumidores y preguntar
en que direccion es segura la sobre-deteccion en cada uno.**

### Leccion 2: "no dispara hoy" no es "no dispara" -- decir POR QUE no dispara

Los 6 embebidos tienen mtime de 14 a 45 dias, asi que hoy caen en `aborted` (solo loguea) y no en
`live`. Es casualidad de fechas, no diseno. Medir las mtimes y **escribir la condicion exacta que lo
enciende** (una escritura dentro de la ventana de `AbortedResidueMinutes`) convierte "creo que es
grave" en un hecho comprobable.

### Leccion 3: el coste hay que medirlo en el lector que DE VERDAD corre

El handoff media solo Python (walk 0.06 s). El de la hot path es el de PowerShell: walk 0.748 s,
status compuesto 1.490 s, `Get-WorktreeDiskProof` 0.847 -> 2.990 s y payload 153 KB -> 534 KB,
calculado DOS veces por rollback y comparado byte a byte. **Un coste declarado en el lenguaje
equivocado no responde el foco.**

### Leccion 4: mutante de codigo muerto -- construir la forma DURA, no fiarse de la del commit

El mutante del commit sustituye el punto de llamada (la funcion queda definida = ya es "presente
pero inalcanzable"). La forma mas dura es **definida Y llamada pero neutralizada por dentro**
(`return` al principio del cuerpo). La construi en los dos lectores: contrato rojo en ambos ->
muertos. Un `assert linea in source` habria sobrevivido a las dos.

### Leccion 5: fail-closed se comprueba en los CONSUMIDORES, y siempre con control positivo

`ok=false` no es un veto: hay que ver que `Get-StagedResidueState` da `unknown` (->
`Register-PreExecDefer`) y `Get-WorktreeDiskProof` da `$null` (-> `ROLLBACK_DEFER`), y que el
sweeper no produce decision de kill. Y **el control positivo es obligatorio**: el mismo fixture sin
claim tiene que dar `action=kill`, o el test de fail-closed es vacio.

### O1 encontrado de paso (fuera de alcance, DECISION-0018)

`process_info()` de `sweep_cron_zombies.py` devuelve `None` para PIDs **vivos** en esta maquina:
`Get-CimInstance` ya entrega `CreationDate` como `DateTime`, asi que
`ManagementDateTimeConverter::ToDateTime` lanza y el powershell sale 1. Toda lease viva sale
`cleanup_only / process_dead` -> con `--kill` se le borran lock y lease a un proceso corriendo, y ese
camino retorna ANTES de `dirty_claimed_route`. Lo descubri porque el end-to-end del camino
destructivo no arrancaba. **Cuando un experimento no arranca, el motivo suele ser un hallazgo.**

### Operativa

`git clone --local --no-checkout` (instantaneo, historia completa) a `D:/Aegis_Scratch/mapp0334/cc`.
Sondas PowerShell extrayendo funciones con el `function_loader` por AST del propio
`test_exec_lease_harness.py` -- permite ejecutar UNA funcion del harness contra un `$Root` de fixture
sin arrancar el cron. Para probar el guard de residuo contra el hub vivo hay que apuntar
`$ResiduePath` a scratch: la funcion ESCRIBE ese fichero. Comparar pre/post extrayendo el fuente
viejo con `git show <commit>^:<path>`.

## Ultima actualizacion 2026-08-07 (47) - TASK-0330 re-juicio iter 2: CHANGE-REQUIRED + ESCALADO

- Encargo `MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0330-r2`. **SIN PRODUCTO EN ALCANCE.**
- Remediacion `f6d88cb7`; handoff juzgado sobre `744d4a1d` (lo reescribio `f1e302cc`).
  Veredicto **CHANGE-REQUIRED + escalado al operador** en `33778347`
  (artifact `Area_comun/artifacts/Analista-TASK-0330-r2-gate-por-efecto-verdict.md`).

### Leccion 1: el CI real puede darte el experimento gratis (no inyectes mutante si no hace falta)

Me pidieron forzar un fallo del primer runner y ver el job en `failure`. No hizo falta tocar nada:
el primer runner **ya estaba rojo** por el sexto rojo de TASK-0335, asi que la corrida natural
31204963761 sobre `f6d88cb7` ES el experimento -- y es mejor evidencia que un mutante mio porque no
toca el arbol. Paso 5 `failure` (`##[error] exit code 1`), job `failure`, pasos 6 y 7 corriendo
detras por `if: always()` con sus OK finales. Antes de buscar como inyectar un rojo, mirar si el
arbol ya trae uno.
**Herramienta:** `gh run view <id> --json jobs` da paso-por-paso con conclusion; `--log --job=<id>`
da las lineas. Es la unica forma de ver el modo "job verde con rojos dentro".

### Leccion 2: el gate mataba exactamente sus propias boundaries, y nada mas

De 14 mutantes del workflow, **9 sobrevivieron**. Los 3 que murieron son literalmente los 3
declarados como boundaries de `NEG-FALSIFICATION-RUNNER-WIRING`. Un contrato cuyas boundaries son
los escapes que ya mueren **no es falsable: es una foto de si mismo**. Regla nueva para mi: cuando
juzgue un contrato, comparar su lista de boundaries contra una bateria de mutantes que YO invente;
si coinciden 1:1 con lo que muere, el contrato no esta midiendo, esta describiendo.
Bateria reproducible: `D:/Aegis_Scratch/mapp/analista-0330-r2/probe/mutants.py`.

### Leccion 3: la propiedad no es del comando, es de la contribucion del paso al job

El Arquitecto pregunto "un comando por paso o razonar sobre el shell efectivo?". Ambas miran el
COMANDO; la propiedad tiene cuatro factores independientes:

    (a) el paso llega a ejecutarse       if de paso, if de job, needs:, on: del workflow
    (b) el runner se invoca de verdad    no echo, no --help, no ruta solo mencionada
    (c) el fallo del runner cae al paso  shell / adornos que traguen el exit code
    (d) el fallo del paso cae al job     continue-on-error en CUALQUIER grafia

Ningun razonamiento de shell arregla (a): `if: false` no es cuestion de shell. Y "un comando por
paso" **no es necesario** (GitHub corre `shell: bash` como `bash --noprofile --norc -eo pipefail`,
asi que 3 comandos en bash SI gatean) **ni suficiente** (`python r.py ; exit 0`, `|| exit 0`,
`2>$null; exit 0`, `--help` son UNA linea y no gatean). La regla correcta es **invocacion unica y
sin adornos**: sobre-aproximacion conservadora, cierta en pwsh (GitHub anade `exit $LASTEXITCODE`),
bash/sh (`-e`) y cmd a la vez, y por eso **no necesita modelo de shell**. Generalizable: ante la
duda entre "regla comoda" y "modelo completo", una sobre-aproximacion conservadora y decidible gana
a un modelo incompleto que reparte verdes con cara de rigor.

### Leccion 4: un mutante puede morir POR ACCIDENTE del regex

`python r.py; exit 0` moria... porque la invocacion se ancla con `(?:\s|$)` detras de la ruta y
`r.py;` no casa. Un espacio (`r.py ; exit 0`) y pasa. **Un mutante que muere no prueba que el gate
lo entienda**: hay que probar la variante adyacente para distinguir diseno de casualidad.

### Lo que si pasa (no fue un rechazo del trabajo)

AC1, AC2, AC3, AC5, AC6 cumplidos. **AC5 verificado literal**: el handoff NO afirma "47 ejecutados",
lo desmiente en texto, y sus 4 recuentos (17/37, 8/22, 25/59, 48/48) los recompute yo desde la
salida `DECLARED` del gate y cuadran. Particion de mis puntos 4 y 5 a TASK-0335 **verificada real**:
AC7 y AC8 los recogen con el detalle tecnico intacto (no basta con que te digan que se particiono).

### Residuales que arrastro

1. El gate de AC4 **sigue SKIPPED en todo CI**: el job `validate` muere en el paso 6
   (`UnboundLocalError: InvalidSignature`, `runtime/eventlog.py:414`, falta `cryptography`) y el
   paso 11 nunca corre. Anterior a 0330, sin dueno asignado. Lo llevo declarado 2 veredictos.
2. `check_falsification_contracts.py` hace `import yaml` sin manifiesto de requisitos en el repo;
   `pyyaml` solo se instala en el job `validate`. Falla cerrado, no es verde falso.
3. **PRUNE DUE** disparado por mi propio commit (`cold_start_tokens 20556 >= 20000`). Es del
   Arquitecto, lo senalo y no lo corro.

Escalado por tope: iteracion 2 de 2 con el punto bloqueante abierto, como habia declarado.

## Actualizacion 2026-08-07 (46) - TASK-0333 el tercer lector y el inventario: OK-CLOSABLE

- Encargo `MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0333`. **SIN PRODUCTO EN ALCANCE.**
- Entrega `303a1d70`, HEAD protocolar `330ef691`. Veredicto **OK-CLOSABLE** en `b462dd30`
  (artifact `Area_comun/artifacts/Analista-TASK-0333-tercer-lector-inventario-verdict.md`).

### Lo que el arreglo hace bien y lo verifique

`dirty_worktree_paths` pasa a `--untracked-files=all` en el runtime vivo Y en el espejo enviado
`examples/full_runtime_instance/`. Extraje las cinco funciones decodificadoras verbatim y las corri
contra repos git REALES con mis payloads. AC1 reproducido (legacy ve `['work/']`, no-declarados `[]`,
turno PASA con 2 ficheros ocultos); arreglado ve las 3 rutas y RECHAZA.

**Matriz de mutacion aplicada AL FICHERO REAL** (no al sintetico), gateada por exit del runner:
opcion borrada y **CODIGO MUERTO `[...][:4]`** mueren en el vivo Y en el espejo (4/4 exit 1). El
contrato ejerce el mirror contra el repositorio real (`assert mirror_paths == expected_paths`), no
lo compara por texto -- por eso el mutante de 0324 muere aqui. Las 5 funciones son **byte-identicas**
live vs mirror.

### La leccion nueva: ver mas ficheros no es ver todos los ficheros

`--untracked-files=all` **NO muestra ficheros ignorados, ni siquiera bajo el propio directorio
untracked**. Medido con `.gitignore` real: el turno declara sus 3 rutas exactas, `unreported=[]`,
PASA, y deja `work/hidden/payload.log` y `rt_state/injected.py` sin declarar. Falsifica la frase del
handoff "the turn gate now sees every file below an untracked directory". En este repo el ignore
cubre `runtime/runs/`, `runtime/memory/`, `.protocol-tmp/`, `.agents/`, `secrets/`. La familia del
COLAPSO DE DIRECTORIO queda cerrada; la del PUNTO CIEGO DEL GATE no.

### El inventario estaba trazado sobre el sustantivo equivocado

Confirme los cinco como todos los lectores de `git status` que decodifican rutas (barrido propio; el
`.ps1` tiene UN solo punto de entrada `:643` con dos consumidores `:674`/`:706`). Tres precisiones:

1. **La clase "sonda" SI decide algo.** Las aserciones de solo-lectura que comparan
   `status --short` antes/despues son **ciegas**: inyecte `work/hidden/INJECTED.py` en un `work/` ya
   untracked y la salida es identica. Pueden certificar "no toque el arbol" en falso.
2. **Hay que inventariar "decodificadores de rutas operativas", no "lectores de git status".**
   `peer_mailbox_cron.ps1:1086/:1251` usa `ls-files --others --exclude-standard -z` y hace ese
   trabajo. Lo probe: **NO es ciego** al colapso (enumera fichero a fichero), asi que no hay cuarto
   por esa via -- pero el inventario no lo habria cubierto.
3. `connectors/git_readonly` **DENIEGA** `--untracked-files=all` y `--porcelain=v1`: el canal
   sancionado de solo-lectura solo permite las dos formas CIEGAS. No abre agujero hoy (los cinco
   lectores llaman a subprocess directo) pero es la superficie que se exporta.

### R6: cableado en CI que no puede enrojecer el job

El contrato esta declarado (`--inventory`, boundaries=7) y `validate.yml:283` lo ejecuta, pero es el
**2 de 3** comandos en un bloque `run:` de un job `windows-latest` **sin `shell:`**. Reproduje el
envoltorio de GitHub (`$ErrorActionPreference='stop'` + `exit $LASTEXITCODE`) con fallo-luego-exito:
**exit 0**. Mismo defecto que medi en el CI real en 0330 (run 31195169744). NO se lo cobre a 0333:
es de TASK-0330 y su remediacion 2 ya estaba enrutada en `b8caf658`, el commit padre inmediato.
**Cobrar dos veces el mismo defecto a dos tareas distintas no es rigor, es ruido.**

### Operativa

Clon por hardlink desde la ruta local: 1 segundo (`.git` ya son 317 MB, el `gc` aguanta). Todo bajo
`D:/Aegis_Scratch/mapp/` (DECISION-0104): `rv0333` anclaje intacto, `mut` para las mutaciones, `rig`
para el banco propio. **Gotcha del entorno**: en el Bash tool, `Path("/d/...")` desde Python resuelve
a `D:\d\...` -- hay que escribir `D:/...` en el codigo Python aunque el shell acepte `/d/`.
**Aviso honesto que deje escrito**: `test_exec_lease_harness.py` salio exit 1 en
`post_delivery_timeout_fired` con los seis gates encadenados y exit 0 aislado -- sensible a la carga,
no regresion; un gate que se cae bajo carga miente algun dia en CI (R7). PRUNE DUE
(cold_start_tokens 22323>=20000) senalado, NO corrido: es del Arquitecto.

Bucle declarado: no aplica (OK-CLOSABLE). Tres tareas propuestas: R1 (ignore), R2 (conector), R4
(sondas de solo-lectura), con el inventario del AC2 redefinido por "decodificador de rutas".

## Ultima actualizacion 2026-08-07 (45) - TASK-0331 admision con scope y atomica: CHANGE-REQUIRED

- Encargo `MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0331`. **SIN PRODUCTO EN ALCANCE.**
  Arreglo `379a9124` (ancestro verificado del HEAD `e792839d`). Mi veredicto commit `2f896e05`,
  pusheado. Artefacto `Area_comun/artifacts/Analista-TASK-0331-admision-scope-atomica-verdict.md`.
  Clon limpio por hardlink en `D:/Aegis_Scratch/mapp/r331/cc` (1 s; `.git` ya son 314 MB, no 7 GB:
  alguien corrio gc). Sondas en `D:/Aegis_Scratch/mapp/r331/probes/`.

### La leccion de esta review: el primitivo estaba bien; el huerfano se habia MUDADO de fichero

El Arquitecto me pidio falsar `DeleteOnClose` bajo muerte dura. Lo hice y **PASA**: cuatro corridas
con `taskkill /F /T` dentro de la seccion, el fichero de admision desaparece en 0.52-0.74 s (eso es
desmontaje del proceso, no un timeout) y el siguiente peer entra en 1.09-1.35 s, sin residuo.
Si me hubiera quedado en la pregunta que me hicieron, habria firmado OK-CLOSABLE.

El defecto estaba **un fichero mas alla**: lo que la seccion critica deja escrito antes de soltar la
admision es la LEASE de reserva, con `state=reserved` y **sin campo `deadline`**. Y
`Clear-StaleCronLockIfSafe` -- el UNICO camino de recuperacion de huerfanos -- hace
`[DateTime]::Parse([string]$lease.deadline)`. Lanza, `SELF_HEAL_FAIL`, no borra ni lock ni lease.
Medido: `lock_removed=false lease_removed=false` con la forma exacta que escribe el codigo, contra
el control (lease `running` de pid muerto) que si se limpia. Tres rearranques simulados del cron:
`own_lease_exists` en los tres. **Encallado permanente y a prueba de relanzamiento.** Antes del
commit ese estado no podia existir: toda lease llevaba `deadline`.

**Regla:** cuando un arreglo introduce un ESTADO NUEVO en un artefacto compartido (aqui
`state=reserved`), hay que ir a leer TODOS los consumidores de ese artefacto, no solo el que el
arreglo toca. El autocurado no aparecia en el diff y es donde estaba el defecto.

### Segunda: fail-closed sobre una causa ESTRUCTURAL no es diferir, es perder

`message_scope_ambiguous` cumple AC3 al pie de la letra. Pero la causa (mensaje sin `task_id`, o con
`task_id` solo en `TASK_INDEX_ARCHIVE` porque el lector solo mira el indice CALIENTE podado, o tarea
sin `scope_routes`) **no se disuelve nunca**, asi que la misma razon se repite cada tick hasta
`defer_terminal` a los 7200 s. La tarea razonaba explicitamente "el diferimiento tiene 7200 s de
margen, asi que no se pierde ningun mensaje" -- ese razonamiento solo vale para causas TRANSITORIAS.
Poblacion real medida: 45 mensajes en indice caliente / 737 solo en archivo / 32 en ninguno / 993
sin `task_id` valido, de 1807. **Declare el atenuante honesto:** hoy 0 mensajes vivos afectados
(7 de 7 colas de reintento resuelven; agosto 0 de 86 -- pero julio 314 de 370).

### Tercera: recuento como PORCENTAJE de un hipotetico no es una medicion

AC2b pedia "cuanto tiempo de solape recupera el ciclo". El handoff respondio "100 percent of an
otherwise eligible declared-disjoint lease window", que es una tautologia. La medicion la saque yo
del log real del cron: sumando para cada `RETRY_DEFER` el intervalo hasta el evento siguiente,
215.7 min `active_external_claim` + 39.5 min `active_peer_lease` = **255.2 min de 422.2 min
diferidos hoy (60 pct)**, que es el TECHO atacable. `worktree_residue_live` son otros 167.1 min y no
los toca esta tarea.

### El mutante de codigo muerto vuelve a ganar (tercera vez: 0324, 0330, 0331)

`NEG-HARNESS-DIRTY-VETO-PRECEDES-SCOPE-ADMISSION` compara INDICES DE TEXTO en la fuente. Mutante que
lo sobrevive con el veto ya inoperante: dejar el literal `if ($residueState -eq "live") {` intacto y
en orden, e insertar `$residueState = "clean"` justo despues del `Get-StagedResidueState`. Sana
True, mutante-del-maker False (lo mata), **mutante de codigo muerto True (sobrevive)**.

### Lo que si aguanto

17 vectores de claim/lease malformados sin una sola inversion (scope ausente, vacio, no-array,
`null`, solo-espacios, elemento no-string, sin `expires_at`, fecha no parseable, sin owner, sin
status, JSON ilegible, clave `claims` ausente, scope solo-ledger, lease sin tarea determinable,
backslash, mayusculas, `#fragmento`). Y la carrera del codigo VIEJO **se reproduce**: extraje el
harness de `379a9124^`, dos PowerShell soltados por la misma compuerta -> 2 admitidos, 2 leases
vivas. Sobre el nuevo, 1 y 1. La medicion del Arquitecto era real.

### Escape NUEVO que nadie pidio buscar: el glob

Un claim con `["*"]` o `["scripts/**"]` que SI cubre la ruta devuelve `none`. Falla **ABIERTO**, la
unica direccion que la tarea declara innegociable. Forma real en el dataset:
`CLAIM-20260702-Analista-TASK-0240-wild-release`, 1 de 2270 claims historicos.

### Verificar la muleta, no solo el hueco

El arreglo excluye `Area_comun/state` y `runtime/state` de la comparacion "porque `submit_intent` es
el escritor unico". **No lo di por bueno:** fui a `runtime/eventlog.py` y confirme que
`ledger_file_lock` es un lock de fichero entre procesos REAL (`msvcrt.locking` en win32,
`fcntl.flock` fuera), y que esta instancia tiene `enforce:true` y `authoritative:true`. Ademas la
exclusion es portante: 7009 rutas de ledger en 2270 claims; sin ella el guard serializaria todo.
Residual que SI falta declarar: dos execs disjuntos comparten UN working tree y UN `.git/index`, que
no esta en el `scope_routes` de ninguna tarea y que muta el 100 pct de los execs.

### Operativa

`PRUNE DUE` (cold_start_tokens 21649 >= 20000) salio en mi commit; es ruta del Arquitecto, lo senalo
y no lo toco. 0 claims ajenos vivos sobre mis rutas (los dos `CLAIM-20260703-Codex-TASK-0230-*`
expiraron el 2026-07-04). 0 bytes >127 comprobados antes de commitear. `validate` y `scan_encoding`
exit 0 antes y despues. Pathspec explicito en el COMMIT. Bucle declarado: **maximo 2 iteraciones**,
escalo al operador a la tercera.

## Ultima actualizacion 2026-08-07 (44) - TASK-0322 r2 RE-JUICIO: CHANGE-REQUIRED (iteracion 2 de 2)

- Encargo `MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0322-r2`. **SIN PRODUCTO EN ALCANCE.**
  Commit de remediacion `3a1ffd75`; head canonico al revisar `825a43b0`, derivo a `dea83cf9` sin tocar
  nada mio. Mi veredicto commit `57337b6e`, pusheado. Artefacto:
  `Area_comun/artifacts/Analista-TASK-0322-r2-declaracion-verdict.md`. Clon limpio
  `D:/Aegis_Scratch/mapp/a322r2`, gates corridos en LOS DOS heads.
- **CHANGE-REQUIRED por dos declaraciones, cero codigo.** Lo demas PASS: la declaracion esta bien en
  tarea, handoff y SPEC (verifique transcripcion, no presencia); identidad byte a byte confirmada por
  diff; suite/inventario/validate/encoding/neutralidad/build/drift en exit 0.
- **LECCION 1 -- "corregir el titulo" son CINCO archivos, no uno.** El titulo de una tarea vive en el
  `.md` **y** en `TASK_INDEX.json`, `TASK_INDEX.slim.json`, `PROJECT_STATE.json` y
  `PROJECT_STATE.slim.json`. El Arquitecto corrigio el `.md` y creyo cerrado el punto; los cuatro de
  estado seguian literales con la lectura de densidad. Y **AGENTS.md seccion 0 pone `TASK_INDEX.json`
  ANTES del archivo de tarea**: la frase superada es la primera que lee un agente en frio. Cuando pida
  "corregir una declaracion", **barrer con `git grep` la frase entera sobre el arbol commiteado**, no
  mirar el archivo que la tarea nombra. El maker (Codex) lo habia senalado como anomalia
  DECISION-0018 en su handoff; el aviso se recibio y no se ejecuto -> un aviso de peer NO es una
  reparacion, hay que verificar el efecto.
- **LECCION 2 (la cara) -- el numero bonito lo puse YO.** En la iteracion 1 declare, como dato a favor
  del maker, que "un movil espanol que empiece por 6 o 7 ya no cabe: exigiria SS >= 60". Codex lo
  transcribio fiel al handoff y a la SPEC, y el Arquitecto lo destaco en el REVIEW como fortaleza
  anadida. **Es falso para la mitad de la familia.** Testigo:
  `2026-01-01T00:00:06.123456-07:00` -> `DATE_RE.fullmatch` True, racha `0612345607`, contiene
  `612345607`, `contains_pii` **False** (exento); los mismos digitos fuera de forma de fecha si se
  cazan. La razon: mi inferencia suponia que el movil empieza en el PRIMER digito de la racha, y eso
  solo vale con fraccion de 5 digitos (racha de 9, alineacion forzada). Con fraccion de 6 la racha
  `SS.ffffff-HH` mide **10**, el movil de 9 cabe desplazado una posicion y su primer digito cae en el
  SEGUNDO de `SS`, que `SS <= 59` deja libre. Barrido por racha: 0/2.700 con fraccion 5, 540/2.700 con
  fraccion 6; por colocacion directa entran 30.000.000 de moviles ES (15 pct del espacio `[67]\d{8}`).
- **Regla que saco de la leccion 2: una cota sobre un COMPONENTE no es una cota sobre la RACHA.** Antes
  de afirmar que una cota excluye un patron, contar la LONGITUD de la racha y probar TODAS las
  alineaciones, no solo la que empieza en el borde. Y no regalar "datos a favor" del maker sin el mismo
  rigor que exijo a sus cifras: un extra que consuela y es falso es peor que ningun extra.
- **Bug de mi propia sonda que casi me hace firmar lo contrario:** buscar el patron sobre
  `"".join(runs(s))` cruza el limite entre rachas y da 900/900 falsos positivos. **Buscar SIEMPRE por
  racha individual**, nunca sobre la concatenacion.
- **GOTCHA de clon limpio SUPERFICIAL -- da FALSO ROJO.** Con `git clone --depth 60`,
  `validate_collaboration_state.py` sale **exit 1** con
  `commit_trailers could not scan git history from 57f6250f...`: la base del escaneo de trailers esta
  **773** commits atras. Con `--depth 820` sale exit 0. El clon superficial miente en la direccion
  contraria a la habitual (el arbol caliente da falso verde; el clon corto da falso rojo). Receta:
  `git rev-list --count <base>..HEAD` para dimensionar la profundidad antes de concluir rojo.
  Bonus: el clon shallow tarda 2 s y ocupa 35 MB (99 MB a depth 820) frente a los ~7 GB del clon
  completo por los objetos sueltos del `.git`.
- **Residuales nuevos que deje:** R5, el docstring `test_memory_db.py:603` sigue publicando
  `2.9% -> 0.05%` sin calificar -- NO lo pedi en esta iteracion porque tocarlo rompe la identidad byte
  a byte que el Arquitecto fijo como alcance; debe viajar con la tarea futura de la asercion por forma.
  R6, `validate` **no cruza el `title`** del archivo de tarea contra el de `TASK_INDEX`, por eso S2
  existe **en verde**; candidato a negativo permanente con dientes.
- **Coordinacion:** 0 claims activos antes y despues; pathspec explicito en `git add` y en el commit;
  0 bytes >127 y 0 CRLF en mis dos ficheros; validate/encoding/neutralidad exit 0 antes y despues.
  `PRUNE DUE` (cold_start_tokens 20177 >= 20000) senalado en el commit, **no corrido: es del
  Arquitecto**. Pregunta abierta en el mensaje: acotar la afirmacion del movil a la subfamilia de
  fraccion 5, o retirarla entera.
- **Tope consumido: esta era la iteracion 2 de 2.** Si llega una tercera con cualquiera de los dos
  puntos abierto, **escalo al operador humano**.

## 2026-08-07 (43) - TASK-0320 ADENDA (preguntas A y B): veredicto SIN CAMBIO

- Encargo `MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0320`, que **NO era una segunda review**
  sino una adenda de dos preguntas al veredicto ya emitido. **SIN PRODUCTO EN ALCANCE.** Commit
  canonico de mi medicion `b2aeb845` (HEAD y `origin/main` al empezar). Mi adenda commit `376d00a8`,
  pusheada. Artefacto: `Area_comun/artifacts/Analista-TASK-0320-adenda-criterio-y-grafias-verdict.md`.
- **Ratifico OK-CLOSABLE. Ninguna de las dos respuestas falsa un AC.**
- **LECCION PRINCIPAL -- responder "cual fue el criterio" NO es responder "es uniforme".** El
  veredicto original ya refutaba que el criterio fuera el idioma, y ahi me quede. La segunda mitad de
  la pregunta ("aplicado uniformemente produce esta misma particion?") es la falsable y la deje sin
  cifra. Al medirla: **NO, falla en 10 de 70**. Por defecto, la regla "sale la grafia local de un acto
  ya nombrado" solo explica 6 de 10 salidas (`FIRMA`, `GO`, `RECONCILE`, `REPORTE` salieron **sin
  gemelo**). Por exceso, y **sin juicio de por medio**: normalizando por `casefold` + quitar `-`/`_`,
  **6 valores del NUCLEO son redundantes mecanicos** de otro del mismo nucleo -- `REVIEW`/`review`,
  `REVIEW_VERDICT`/`review-verdict`/`review_verdict`, `REVIEW_RESULT`/`review_result`,
  `HANDOFF`/`handoff`, `ANOMALY`/`anomaly`. **Regla: cuando te preguntan por un criterio, conviertelo
  en procedimiento de decision y aplicalo al universo ENTERO; los fallos por EXCESO (lo que deberia
  haber salido y se quedo) son tan reportables como los fallos por defecto, y suelen ser los que no
  se ven.**
- **Normalizar es la forma de sacar juicio de la ecuacion.** El foco B original ("nueve grafias de
  REVIEW") era una lista a ojo, y por eso se me escapo la decima (`HANDOFF`/`handoff`, 451 vs 1).
  Un `casefold` + strip de separadores da el inventario COMPLETO y no opinable. Cuando un hallazgo
  huela a "vocabulario podrido", **normaliza y cuenta clusters**, no enumeres de memoria.
- **Medir la DERIVA, no solo el estado.** Corri el mismo censo en el ancla de la review (`a8e5319f`) y
  en HEAD (`b2aeb845`): en **un dia** (+44 archivos de corpus) `REVIEW` gano **+8** y las otras ocho
  grafias quedaron **exactamente igual**. Eso convierte "hay grafias redundantes" (estatico, opinable)
  en "la dominante crece y las minoritarias se fosilizan sin morir, luego nunca se retiraran por
  desuso" (dinamico, accionable). **Dos anclas y una resta valen mas que una tabla.**
- **CENSO PROPIO como alternativa al clon limpio, cuando lo que mides es el CORPUS y no los gates.**
  Lei con `git ls-tree` + `git show <commit>:<path>`, es decir de los **blobs atestados**: mas fuerte
  que un clon limpio para esto porque elimina el arbol de trabajo en vez de reconstruirlo. Y
  **reimplemente a mano** los filtros (`governed`/`is_excluded`/`TEXT_SUFFIXES`) y el parser de
  frontmatter en vez de importarlos de `build_memory_db.py`: **medir con el modulo bajo revision es
  preguntarle al acusado**. Control de fidelidad obligatorio: el censo sobre `a8e5319f` da 4.277
  archivos (misma cifra que el build) y **reproduce exactamente** la tabla de nueve grafias del
  veredicto anterior. Sin ese control, un censo propio no es evidencia, es otra opinion.
- **Responder "no cambia el veredicto" exige decir POR QUE de forma falsable.** No basta con "no
  bloquea": A no falsa AC1 porque AC1 exige que la clasificacion **se declare**, no que el criterio
  sea derivable ni uniforme (y la no-uniformidad es propiedad del arbol entero, no de la entrega);
  B no falsa AC4 porque AC4 cubre lo **declarado** (10/10/0, aguanta a HEAD) y las grafias estan en el
  **nucleo**.
- Respuesta a B en una linea: **CERO muertas de las nueve; 612 artefactos reales detras.** No es
  vocabulario muerto (temor del Arquitecto) sino **podredumbre viva**, que es menos grave y mas cara
  de curar: se toca corpus, no enum. El muerto de verdad esta en el nucleo y son **3 de 60**
  (`HUMAN_REQUIRED`, `refactor`, `release`), que nadie cuenta -- es el hueco del mutante M4.
- **Primer paso mecanico que propuse para R5+R7** (elevado, NO condicion de cierre): una guarda que
  rechace que dos valores del nucleo colapsen al mismo `casefold` sin `-`/`_`. **Hoy fallaria con 6**,
  que es justo el inventario a purgar. Es la unica parte del problema que no es opinion. R2 (ancla de
  "generico" en la plantilla) sigue siendo la causa raiz y va antes del tercer enum.
- **Nota de proceso ajena a mi:** la review llego tarde porque archivar un mensaje **no desencola su
  reintento** (el harness reintenta POR NOMBRE desde `archived/`). El Arquitecto lo registro como
  anomalia del harness. Sin accion mia.
- **Coordinacion:** 0 claims de peers sobre mis rutas al escribir (los dos de Codex son `blocked` y
  solo cubren `CLAIMS.json#<self>`); rutas gobernadas limpias antes y despues; `git add` explicito +
  pathspec en el commit; `validate`, `scan_encoding` y `scan_domain_neutrality` exit 0. `type:
  review_verdict` en mi artefacto (no `artifact`), coherente con mi propio residual R1.

## Ultima actualizacion 2026-08-07 (42) - TASK-0323 lectores de porcelain sin -z: OK-CERRABLE

- Encargo `MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0323`. **SIN PRODUCTO EN ALCANCE** (declarado en la
  primera linea del REVIEW). Arreglo `0ee452ed`, entrega `3df488fa`, base `ee9c0dde`, HEAD del hub al revisar
  `c5644adc`. Veredicto commit `b29b490e`, pusheado. Artefacto:
  `Area_comun/artifacts/Analista-TASK-0323-porcelain-z-readers-verdict.md`. Clones limpios en
  `D:/Aegis_Scratch/protocol/` (an0323 @0ee452ed, base @ee9c0dde y @8e07aa14) + fixtures en `gt/`.
- VEREDICTO: **OK-CERRABLE**, 5/5 AC PASS, sin SLIP bloqueante, 5 residuales declarados.
- **LECCION PRINCIPAL -- juzgar la DECISION, no el parser.** El foco del Arquitecto era "que el lector devuelva
  las rutas exactas". Si me quedo ahi, el veredicto es correcto pero flojo. Extraje el lector VIEJO de
  `0ee452ed^` con `git show` y ejecute la funcion de DECISION completa (`dirty_claimed_route`) con los dos
  lectores sobre repos git reales, con `CLAIMS.json` real y claim **acotado a fichero** (como manda el protocolo
  para el mailbox). Ahi aparecio lo que nadie tenia en el foco: **el vector del renombrado no necesita ni
  no-ASCII ni espacios**. Un `git mv` ASCII puro basta -- el lector viejo solo registraba el destino, el claim
  apuntaba al origen, `dirty_claimed_route` daba False y el barredor MATABA al peer a mitad de su trabajo.
  Regla: cuando el AC habla de un lector, prueba el CONSUMIDOR del lector con datos de produccion.
- **PRIMER FIXTURE FALLIDO Y POR QUE FUE UTIL.** Mi caso A inicial dio False en AMBOS lectores y parecia que el
  fix no servia. Causa: el directorio entero estaba sin rastrear, git colapsa la salida a `Area_comun/mailbox/`
  y el claim file-scoped no casa. Rehice el fixture con el directorio ya rastreado y el vector quedo aislado
  (viejo False / nuevo True). **El fixture fallido se convirtio en el residual R4**: un hallazgo NUEVO de
  direccion ABIERTA -- `dirty_paths` no pasa `--untracked-files=all` (el helper de PowerShell si) -- que pedi
  como tarea propia. No tirar un fixture que "sale mal": entender POR QUE sale mal suele ser el hallazgo.
- **NO ACEPTAR "ya estaba rojo" DE PALABRA.** El handoff declaraba `runtime_loop_cases` rojo pero preexistente.
  Como `runtime/orchestrator.py` es uno de los ficheros TOCADOS, lo corri yo en tres commits: `0ee452ed`,
  `ee9c0dde` y `8e07aa14` (tarea ya cerrada en verde). Exit 1 con los MISMOS 9 casos, conjuntos identicos,
  diferencia cero en los dos sentidos -> sin regresion, y ademas acota la antiguedad del rojo. Comparar
  CONJUNTOS de casos, no solo exit codes.
- **PROBAR LA ROBUSTEZ DEL NEGATIVO, no solo que pase (residual R1).** El negativo AC4 mata la mutacion
  declarada (quitar `-z`) via `ValueError`. Reconstrui el mutante y lo corri sobre DOS formas de arbol: con
  renombrado muere; **SIN renombrado sobrevive** y devuelve una ruta inventada de varias lineas en silencio
  (`raw.split(b"\0")` da un registro gigante y `record[2:3]` sigue siendo un espacio). La guarda de "malformed"
  es mas estrecha que la frase del handoff. No bloquee (produccion pasa `-z` siempre y el fixture siempre crea
  un renombrado) pero lo declare con reproduccion + arreglo de una linea: rechazar registros con `\n`.
- Inventario AC3 propio, por vias distintas a las del maker y a las del Arquitecto (`git.\{0,3\}status` en todo
  el arbol, `"status"` como argumento en `.py`, `Arguments`/`git` en `.ps1`, y `.js/.mjs/.ts` -> cero): 5
  decodificadores de ruta, los 5 con `-z`; 12 sitios mas que NO derivan ruta (vacuidad, letras de estado o blob
  antes/despues). **Completo.** Clave de clasificacion: no basta con "usa porcelain", hay que leer QUE HACE con
  la salida -- `== ""` y `before == after` son inmunes al defecto y no necesitan `-z`.
- Gates recomputados en clon limpio por exit code: harness 15/15 exit 0, inventario de falsacion exit 0
  (`NEG-CRON-ZOMBIE-SWEEPER-PORCELAIN-Z-PATHS`, 7 boundaries), validate 0, encoding 0, neutralidad 0, drift
  `has_drift=false` up_to_seq 7299, `diff --check` 0, status vacio.
- Truco util para importar codigo del repo sin arrastrar sus imports: `runtime/orchestrator.py` no se puede
  cargar suelto (imports relativos). Extraje solo la funcion con un regex a un fichero fragmento y la ejecute.
  El propio negativo del maker usa la variante limpia: `ast.parse` + `next(node for node in tree.body ...)`.
- Anomalia senalada al Arquitecto (DECISION-0018), no imputable a 0323: `runtime_loop_cases` esta cableado en
  CI (`validate.yml:208`) y rojo en local sobre Windows desde al menos `8e07aa14`. NO afirme "CI roja" porque
  no medi CI sobre Linux -- declarar el limite de lo que mediste es parte del veredicto.

## Ultima actualizacion 2026-08-06 (41) - TASK-0316 r1: CAMBIO-REQUERIDO (el verde del gate se compra, no se gana)

- Encargo `MSG-20260806-Arquitecto-to-Analista-REVIEW-TASK-0316`. **SIN PRODUCTO EN ALCANCE** (declarado por el
  Arquitecto en la primera linea; 100 por cien hub, gates de Python/PowerShell). Entrega `9e66c6a` (maker Codex),
  HEAD canonico `98714e0`, arbol limpio de mods rastreadas. Veredicto commit `90d56a1`, pusheado.
  Artefacto: `Area_comun/artifacts/Analista-TASK-0316-neutralidad-cobertura-verdict.md`.
- Dos clones limpios en `D:/Aegis_Scratch/mapp/` (an0316 @9e66c6a, an0316head @98714e0) + copia mutable `mut`
  + fixture `ps1fix`. Gates por exit code sin pipe: validate 0, scan_domain_neutrality py 0 y **ps1 0**,
  test_scan_domain_neutrality 0 (2 tests), scan_encoding 0, check_falsification_contracts --inventory 0.
- VEREDICTO: **CAMBIO-REQUERIDO**. AC1/AC2/AC3/AC6 PASS; **AC4 SLIP bloqueante**, **AC5 parcial bloqueante**.
- **METODO NUEVO Y REUTILIZABLE -- reducir el escape a un fixture minimo ANTES de contar hallazgos.** El
  Arquitecto midio 64 hallazgos silenciados; yo lo reduje a DOS archivos con el MISMO literal `"Codex"`
  (`scripts/root_probe.py` y `scripts/memory/nested_probe.py`) y config de un solo agente: los dos escaneres
  reportan solo el de profundidad 1. Mas corto, mas falsable y ademas revelo **paridad py/ps1** (el `.ps1`
  carga el mismo recorte con `($rp.ToCharArray()|? {$_ -eq "/"}).Count -eq 1`). Un conteo agregado no habria
  mostrado que el defecto esta en AMBAS implementaciones.
- **TABLA DE MUTACION = el nucleo del juicio.** Con restauracion del archivo pristino entre cada mutacion:
  M1 (`REQUIRED_SCAN_GLOBS=()`), M3 (quitar `Area_comun/protocol/*.json`), M4 (`REQUIRED_EXEMPT_GLOBS=()`)
  -> test exit 1 con el gate del repo en exit 0 = **el test SI es falsador real de la cobertura**.
  **M5** (revertir SOLO el recorte de profundidad) -> **test exit 0, gate del repo exit 1 con 64 hallazgos**.
  Lectura: el recorte no esta cubierto por ningun test Y es la pieza que compra el AC4. La segunda columna
  (gate del repo) es la que convierte la mutacion en veredicto: sin ella solo sabria que el test no cubre algo.
- **TRAMPA DE PROCESO QUE PISE:** primera ronda de mutaciones CONTAMINADA -- `git checkout -- <file>` fallo
  ("not a git repository" en la copia) y las mutaciones se ACUMULARON; M5 salio con la mutacion de M1 encima y
  dio un resultado invertido y falso. LECCION DURA: **restaurar por `cp` de una copia pristina guardada aparte,
  nunca por `git checkout` en un arbol que no verificaste que sea repo**, y gatear el restore con `diff -q`.
- Juicio de legitimidad linea por linea de los 64 (lo que el Arquitecto me pidio decidir): **60 legitimos, 4
  defectos reales**. Legitimos = 51 fixtures de `test_memory_db.py` + **9 de `peer_mailbox_cron.ps1` que NO
  hablan del agente `Codex` sino del CLI de OpenAI** (`where.exe codex`, `codex.exe`, `OpenAI\Codex\bin`,
  `ValidateSet("Auto","Anthropic","Codex")`) -- colision de nombre con un tercero, real. Los 4 reales:
  `query_memory_db.py:241` (default `Codex`), `build_memory_db.py:67,71` (vocabulario de instancia en el enum)
  y **`peer_mailbox_cron.ps1:3` `$CoordinatorId = "Arquitecto"` -- NUEVO, la medicion del Arquitecto no lo
  imputo**. Moraleja: cuando un peer entrega un conteo agregado, la aportacion del checker esta en el desglose,
  no en repetir el total.
- **El handoff describe mal su propio delta.** Dice "intentionally preserves root-only identity scanning for
  scripts"; la regla previa NO era root-only (cubria `scripts/` a cualquier profundidad). Ademas la razon dada
  ("legitimate fixture names") solo cubre 60 de 64. Y asimetria interna sin explicacion: el brazo
  `runtime/**.py` de la MISMA funcion no lleva recorte. Sin justificacion tecnica -> corroboro al Arquitecto,
  no lo corrijo. LECCION: **leer el handoff y contrastar su nota de riesgo contra el diff**; aqui la frase que
  sostenia el "riesgo controlado" era factualmente falsa.
- **Tres huecos del AC5 que ninguna capa anterior vio** (los encontre mirando CI y el registro del propio repo,
  no el codigo entregado): H1 el test **no corre en ningun gate** (`validate.yml` corre los dos escaneres,
  lineas 256 y 260, nunca el test); H2 **no esta en el registro de contratos de falsacion** (CI corre
  `check_falsification_contracts.py --inventory`, lista 25, este ausente; precedente en
  `test_falsification_contracts.py` con su bloque `FALSIFICATION_CONTRACTS`); H3 `SCRATCH_ROOT =
  Path("D:/Aegis_Scratch/...")` en un script del NUCLEO -- CI es `ubuntu-latest` y en POSIX esa cadena **no es
  absoluta** (`PurePosixPath(...).is_absolute() == False`), asi que crearia `<repo>/D:/...` DENTRO del arbol
  atestado y `tearDown` no limpia `SCRATCH_ROOT`. **REGLA: cuando el AC dice "para que no vuelva en silencio",
  verificar que ALGO LO DISPARE** -- que el test exista y sea falsador no basta; mirar el workflow de CI y el
  registro de falsacion del repo.
- **Correccion metodologica de cifras (aplica a mi tambien):** ni `179 -> 192` (Arquitecto) ni `180 -> 192`
  (handoff) son reproducibles: medidas sobre arbol caliente, y **los `__pycache__/*.pyc` ENTRAN en el conjunto
  escaneado** (casan `runtime/**` y `connectors/**`). Clon limpio: **147 -> 159, delta +12, 0 perdidos**. El
  delta coincide en las tres, la sustancia se sostiene. LECCION: recontar toda cifra declarada en CLON LIMPIO
  antes de citarla, aunque venga de dos capas que ya "coinciden".
- 4 residuales NO bloqueantes: R1 el ensanche es por EXTENSION (.py/.ps1), quedan 9 archivos anidados bajo
  `scripts/` totalmente ciegos -- 181 hallazgos de identidad, **0 de denylist** -- sobre todo
  `instance_assets/claude-skills/*/SKILL.md`, que se exporta al instanciar; R2 `REQUIRED_EXEMPT_GLOBS` se
  fuerza SIN escape (ensanchar `scan_globs` por codigo es seguro, **estrechar `exempt_globs` por codigo no**);
  R3 los `.pyc` escaneados (preexistente) son lo que descuadra los conteos; R4 `protocol/*.json` a profundidad
  1, coherente, no es defecto.
- Lazo declarado de 7 puntos, max 2 iteraciones antes de escalar al operador humano, re-juicio mio antes del
  commit de cierre. **Criterio de cierre que propuse: que el gate del repo salga exit 0 SIN el recorte** (verde
  ganado, no comprado). Formular el criterio de cierre como una MUTACION que debe seguir verde es mas duro y
  mas barato de verificar que enumerar fixes.
- **GOTCHA DE TRAILERS (me mordio):** el hook `commit-msg` rechazo el primer intento -- el bloque final de
  trailers necesita **linea en blanco ANTES** del bloque y **ninguna entre las claves**. Mi memoria decia "sin
  blank line entre trailers" y lo lei como "sin ninguna blank line". Formato bueno: cuerpo, blank, `Task-Id:`,
  `Ops-Reason:` (<=120 chars). NO uso `Co-Authored-By: Claude` en mis veredictos: el monitor del Arquitecto
  filtra por ese trailer como discriminador de "commit propio" y mi entrega quedaria invisible para el.
- Scratch limpiado al terminar (DECISION-0104).

## Ultima actualizacion 2026-08-06 (40) - TASK-0314 r2 remediacion: OK-CLOSABLE (lazo cerrado en 2/2)

- Encargo `MSG-20260806-Arquitecto-to-Analista-REVIEW-TASK-0314-r2`. **SIN PRODUCTO EN ALCANCE** (declarado
  otra vez por el Arquitecto). Impl `d1252f4`, protocol HEAD `0a66a36`. Veredicto commit `1794bce`
  (artefacto `Area_comun/artifacts/Analista-TASK-0314-remediacion-r2-verdict.md` + MSG rr=true).
- **VEREDICTO: OK-CLOSABLE.** F1, F2, F3 y R4 cerrados por COMPORTAMIENTO. 2 residuales nuevos (R5, R6).
  El cierre (flip a done + reporte) es del Arquitecto; yo no cierro.
- **TRES clones limpios en paralelo, uno por proposito** -- patron que repito: `ana314b` suite (57/57,
  341 s), `ana314c` corpus (build + gates + packs), `ana314d` MUTACION. Lanzar suite y build en
  background a la vez, en clones DISTINTOS (el build escribe runtime/memory/index.db y colisionaria).
- **F1 terminacion: prueba por construccion + falsacion.** El lazo `detail_limit //= 2` es estrictamente
  decreciente (`1//2==0`) y ninguna rama lo aumenta -> termina en floor(log2 n)+1 pasos. Lo FALSEE
  ademas forzando el peor caso con monkeypatch `max_bytes=1`: aborta en 13.35 s con mensaje propio
  ("fixed content exceeds... after deterministic omission degradation"), no se cuelga. **METODO
  REUTILIZABLE: el mismo monkeypatch de `memory_index_policy` que use en r1 para MEDIR el pack
  descartado sirve ahora para MEDIR EL SUELO NO DEGRADABLE** (forzar max_bytes=1 -> el mensaje de error
  trae el tamano a detail_limit=0). Suelos: 55750 / 61544 / 48393 / 3003 = 37-47 pct del techo (R6).
- **Determinismo: componer DOS VECES y comparar bytes**, no leer el `sorted()`. 4/4 identicos.
- **Cobertura por familia, no por ejemplo -- aqui es donde cace lo nuevo.** El Arquitecto verifico los 6
  timestamps de MI r1 y dio PASS. Genere la FAMILIA COMPLETA de la gramatica (333 cadenas: 3 fechas x 4
  horas x 7 fracciones x 5 offsets) y aparecieron **18 rechazos de metadata legitima**: `contains_pii`
  falsea positivo porque el patron de telefono `\+?\d[\d .()-]{7,}\d` lleva el GUION en su clase, y el
  guion del offset UTC **negativo** puentea la fraccion de segundo -> 9-10 digitos >= umbral 9.
  Condicion exacta: offset negativo Y 5-6 digitos de fraccion. `2026-06-19T09:28:23.123456-05:00`
  (= salida de `datetime.now(tz).isoformat()` en huso americano) queda RECHAZADO. **R5: regresion NUEVA
  introducida por la propia remediacion.** No bloquea: 0 ocurrencias en el corpus (escanee 4586
  archivos, 134 valores distintos de created_at/updated_at/closed_at) y falla CERRADO (descarta campo,
  no admite PII). Va como tarea aparte, NO como 3a iteracion (mi lazo declarado era de 2 y los 4 items
  contratados estaban cerrados).
- **Prueba de cierre de F2 por ALFABETO, no por muestreo.** Extraje el alfabeto alcanzable a traves de la
  nueva `DATE_RE`: `+-.0123456789:TZ`. Sin `@` y sin dos letras consecutivas -> email e IBAN **no caben
  en el lenguaje**. Eso es mas fuerte que "probe N vectores y no paso ninguno". Ademas: la capa que de
  verdad cierra el agujero es quitar la exencion (aplica contains_pii a TODAS las claves); la gramatica
  es defensa en profundidad.
- **R4 se verifica MUTANDO, no leyendo.** `git checkout d1252f4~1 -- scripts/memory/revive_pack.py` en un
  clon aparte (revierte SOLO el fix, deja el test nuevo) -> el test FALLA exit 1 (135556 > 65536). El
  `assertGreater(..., 65536)` del fixture compara contra el `max_bytes` LOCAL de la politica del test,
  que es el umbral correcto; verificar eso evita cantar "test decorativo" por error.
- F3: recompute el desglose de warnings POR CLAVE (219: spec_id 123, task_id 86, decision_id 6, to 2,
  supersedes 1, relates_to 1); 0 de `priority` y 0 de claves de fecha. El titular "238 -> 219" no basta.
- **Salvedad honesta que declare sobre mi propio exit 0:** mi neutralidad exit 0 vale solo porque escribi
  los packs FUERA del repo. Al materializarlos en `runtime/memory/` el gate se pone ROJO
  (`pack_Arquitecto.md:811: trading/spot/binance/backtest`). Confirma el AC6 de TASK-0316 del Arquitecto,
  con dos precisiones que le pase: el pack NO ensucia `git status` (gitignored) y `_validate_output` solo
  restringe rutas DENTRO del repo (escribir fuera esta permitido, exit 0) -- su frase "se niega a escribir
  fuera de runtime/memory/" sobreestima el guard.
- AC1 / F4: NO bloquea. TASK-0316 ya `ready` con GO del operador (owner Codex, checker yo). Pedi que el
  cierre diga "AC1 verificado por lectura y test unitario", NO "verificado por gate".
- Gates r2 por exit code: suite 57/57, build 4162 artefactos, `--fast`, `--full` (round_trip pass, sweep
  bidirectional-pass, database_written false), encoding, neutralidad, validate -> TODOS 0; `git status
  --porcelain` vacio tras build y tras `--full`. Packs: 119309 / 95219 / 48775 / 3008 (anadi `Operador`,
  el 4o registrado, que faltaba en la tabla del Arquitecto y del maker).

## Ultima actualizacion 2026-08-06 (39) - TASK-0314 F1-PORT memoria hibrida al hub: CHANGE-REQUIRED

- Encargo `MSG-20260806-Arquitecto-to-Analista-REVIEW-TASK-0314`. **SIN PRODUCTO EN ALCANCE** (declarado
  por el Arquitecto): 100 por cien hub, gates de Python. Commit de impl `378021d`, protocol HEAD `070ddae`.
  Contrato = SPEC-MEMORIA-HIBRIDA s.16 (P1-P12 + DoD de 9 puntos). Clon limpio propio
  `D:/Aegis_Scratch/protocol/ana314`. Veredicto commit `9f24d05` (artefacto
  `Area_comun/artifacts/Analista-TASK-0314-port-memoria-hibrida-verdict.md` + MSG REVIEW rr=true).
- **VEREDICTO: CHANGE-REQUIRED.** 3 slips bloqueantes + 1 hueco de contrato + 4 residuales.
- Gates recomputados por exit code: suite 55/55 (253 s), build 4154 artefactos / 211 eventos / 15 tablas /
  schema 1 / fk 1, `--fast` (database_read false), `--full` (round_trip pass, sweep bidirectional-pass,
  database_written false), scan_encoding, scan_domain_neutrality, validate -> TODOS 0; `git status
  --porcelain` vacio tras build y tras `--full` (I2). Frontera respetada (no toca validador, submit_intent,
  config pineado, registry, genesis, runtime/state).
- **F1 (P11/AC7) -- confirme el bloqueante del Arquitecto PERO corregi su causa.** Reproduje: Arquitecto
  exit 2 (161465 B), Codex exit 2 (194752 B), Analista exit 0 (37166 B) contra 131072 de presupuesto.
  El Arquitecto atribuia el exceso a "sesiones/tareas/mailbox/decisiones sin inlinear". FALSO.
  **Metodo decisivo reutilizable:** monkeypatch de `memory_index_policy` para elevar `max_bytes` y poder
  MEDIR el pack que se descarta, luego descomponerlo por secciones. Resultado: el inline SI respeta su
  tope (35894 y 41957 <= 65536); lo que revienta es **la propia declaracion de omisiones (seccion 6)**:
  119293 B = 74 pct del pack del Arquitecto, 139406 B = 72 pct del de Codex, un objeto JSON por archivo
  omitido (291 y 300 entradas). **El mecanismo de degradacion es lo que rompe el presupuesto** -> subir
  `max_bytes` no converge. Leccion: cuando un tope "no acota", medir la COMPOSICION del artefacto que
  desborda, no asumir que el exceso viene de lo obvio.
- **F2 (AC2) -- fuga PII por clave de fecha, probada extremo a extremo.** `build_memory_db.py:579` exime
  `created_at`/`updated_at`/`closed_at` de `contains_pii`, y `DATE_RE` admite cola libre `T[^\s]+`.
  Build real sobre fixture -> fila `('TASK-9001','2026-06-19Tvictim@example.invalid',None)`, y
  `_publicable_pii_errors` devuelve `[]`. **La exencion es gratuita**: probe 6 formatos de timestamp bien
  formados y NINGUNO dispara `contains_pii` -> se apago una validacion que nunca habria disparado.
  Leccion: ante una exencion, probar si el caso que dice evitar existe siquiera.
- **F3 (AC5) -- 19 de los 238 warnings son `priority: medium`**, metadata BIEN FORMADA del hub, no H2.
  Descompuse los 238 por clave (spec_id 123 / task_id 86 / priority 19 / decision_id 6 / to 2 /
  relates_to 1 / supersedes 1) e inspeccione los 4 no obvios uno a uno: malformacion real. AC5 exige
  que los restantes sean SOLO malformacion. El Arquitecto lo llamo "hallazgo menor"; contra la letra de
  AC5 es el criterio que rompe. Leccion: contar los warnings POR CLAVE, no aceptar el agregado "son
  todos H2".
- **F4 -- el gate de neutralidad NO cubre lo entregado, pero NO es del maker.** `scan_globs` trae
  `scripts/*.py` y `glob_to_regex` mapea `*` a `[^/]*` (no cruza `/`) -> `scripts/memory/**` (3863 lineas)
  y `Area_comun/protocol/MEMORY_INDEX_POLICY.json` nunca se escanean. **Falsificado, no deducido:** con
  "binance spot backtest trading" dentro de `scripts/memory/build_memory_db.py` y `domain_pii_terms:
  ["trading","binance"]` en el policy -> exit 0; el mismo termino en un `scripts/poison.py` plano ->
  exit 1; en el clon real selecciona 127 archivos, ninguno bajo `scripts/memory/`. **Atribucion correcta:**
  el `out_of_scope` de la tarea prohibia tocar `protocol.config.json` y `scan_domain_neutrality.py` no
  estaba en `scope_routes` -> hueco de contrato del Arquitecto, tarea aparte, NO imputable al cierre.
  Leccion: antes de imputar un gate vacio, leer `scope_routes`/`out_of_scope` para ver si el maker tenia
  ruta para arreglarlo.
- Residuales declarados: R1 el fix de P5 exime del patron de telefono a TODO valor con forma de id
  (`contains_pii("TEL-34612345678")` False) -- pero s.16.3 lo AUTORIZA expresamente, asi que va como riesgo
  conocido, no defecto; R2 IBAN solo se detecta contiguo (con espacios o guiones escapa), preexistente;
  R3 `_publicable_pii_errors` no aplica los `domain_pii_terms` de la instancia (inocuo en el hub, material
  en Nova-Payroll); R4 el test de P11 produce 1 omision -> no puede fallar como falla el corpus real.
- Contraste pedido sobre H2/P12b: **coincido con el Arquitecto**, reescribir 206 artefactos gobernados
  para complacer al indice seria la direccion equivocada; mi unica divergencia es de perimetro (los 19 de
  `priority` no son H2).
- Lo que ataque y NO rompi (consta en el veredicto): la politica configurable esta acotada de verdad;
  enums finitos (36 status / 69 type) que rechazan texto libre; P12 acepta `[]` y rechaza `""`/`None`/`{}`/
  `["not an id"]`; `--fast` no abre la DB y `--full` conecta `mode=ro`; el clon interno del round-trip usa
  `tempfile` (no raiz de disco); el pack solo lee `agent_memory` del propio agente.
- Lazo declarado: maximo 2 iteraciones antes de escalar al operador humano.

## Ultima actualizacion 2026-08-02 (38) - TASK-0311 runtime-control (indicador + lanzar/detener agente conocido, front Zeus-protocol): OK-CLOSABLE

- Encargo `MSG-20260802-Arquitecto-to-Analista-REVIEW-TASK-0311`. PRODUCTO = repo Zeus-protocol
  (panel operador, NO Nova-Budget), commit `686592d`. DECISION-0107 + SPEC-0113. Hub HEAD al revisar
  `edf4dd9`; foco pedido = SEGURIDAD (allowlist fijo server-side, no ejecucion arbitraria).
- Clon limpio del PRODUCTO en `D:/Aegis_Scratch/zeus/rev0311` checkout 686592d, gates por exit code.
  Veredicto commit `70cdfd5` (artefacto `Area_comun/artifacts/Analista-TASK-0311-runtime-control-verdict.md`
  + MSG REVIEW a Arquitecto requires_response). Push OK. validate(hub)=0, scan_encoding=0, drift 0.
- **VEREDICTO: OK-CLOSABLE.** 0 slips, 5 residuales informativos. npm test clon limpio EXIT 0
  (141/121/20/0, coincide con el maker). Diff = 3 files (public/app.js, src/server.js, tests).
- **Metodo decisivo (reutilizable): probe adversarial VIVO propio** `analista_probe.mjs` -- levanta el
  servidor real del clon (flag ON y OFF) y lanza 44 payloads mios (no confie nombres de test). 44/44 PASS.
  Vectores NUEVOS que los tests del maker NO cubren: `scriptPath`/`cwd`/`__proto__`/`constructor` ->
  400 (assertAllowedKeys rechaza toda clave extra); agentId traversal-looking `Codex/../../etc` -> 400
  (es SOLO clave de Map, nunca segmento de ruta); homoglifo acentuado -> 400; flag `0`/`true`/`yes`/`""`
  -> 403 (solo `"1"` habilita).
- **Prueba central anti-arbitrario (la mas fuerte):** un start VALIDO de agente conocido con el script
  fijo del allowlist AUSENTE devuelve **503** "script unavailable" -> demuestra que spawn SOLO usa
  entry.scriptPath del allowlist (args fijos, shell:false, repoPath del entorno del servidor); el
  cliente no puede disparar OTRA cosa. La negativa es permanente (contratos: Map fijo + sanitizador),
  no best-effort.
- **Fondo intocable:** #4 hub drift 0 (replay_hash==hot_hash, seq 6938), protocol.config.json intacto
  desde v1.14.0, codigo SOLO en Zeus-protocol (repo separado).
- **Residual a documentar al operador:** operator-stop PEGAJOSO -- un stop del front escribe `.stop`
  que luego bloquea TODO start (409) hasta borrar el marcador fuera de banda. Es fail-safe (mas seguro),
  coincide con AC5, pero no hay endpoint de limpieza -> re-lanzar tras stop del front exige limpiar
  `.protocol-tmp/<cron>/<cron>.stop`. Lo puse como pregunta de gating al Arquitecto (nota/tarea opcional).
- LECCION: cuando el foco es "no ejecucion arbitraria", la prueba mas decisiva no es que los payloads
  malos den 400, sino que el payload BUENO solo pueda ejecutar el binario FIJO (503 si falta) -- eso
  cierra el escape por completo. Extraer la funcion y correr el camino feliz + el 503 en vivo.

## Ultima actualizacion 2026-08-02 (37) - TASK-0309 contraste texto manual-mermaid (front Zeus-protocol): OK-CLOSABLE

- Encargo `MSG-20260802-Arquitecto-to-Analista-REVIEW-TASK-0309`. PRODUCTO = repo Zeus-protocol
  (panel operador, NO Nova-Budget), commit `66c27d7`; baseline previo `7729c4f`. SPEC-0111 /
  REQ-040EC397. Hub HEAD al revisar `69118ae`; TASK-0309 in_review, owner Codex, type product.
- Clon limpio del PRODUCTO en `D:/Aegis_Scratch/zeus/r0309` checkout 66c27d7, gates por exit code.
  Veredicto commit `5dd0ff5` (artefacto `Area_comun/artifacts/Analista-TASK-0309-manual-mermaid-contrast-verdict.md`
  + MSG REVIEW a Arquitecto requires_response). Push OK. validate(hub)=0, scan_encoding=0.
- **VEREDICTO: OK-CLOSABLE.** Fix = 1 regla CSS `.manual-mermaid-svg text { fill: var(--text); }`
  (styles.css) + 1 asercion en staticContract. diff 7729c4f..66c27d7 = 2 files, 5 inserciones, 0
  borrados (AC3 sin regresion; cajas/aristas/flechas/lifelines byte-equivalentes).
- **npm test (node --test, cero deps) EXIT 0**: 138 total, 116 pass, 0 fail, 22 skip (TODOS
  `# slow subprocess tier`, ninguno del fix); el test del contraste corrio y paso.
- **AC4 meaningful (baseline negativo REPRODUCIDO 2 formas):** (a) behavioral -- swap css a 7729c4f
  -> falla SOLO ese test (fail 1) sobre la regex del fill; (b) regex directa -- no-match en 7729c4f,
  match en 66c27d7.
- **Selector coverage (verificar render no solo string):** app.js flow (:3067) y sequence (:3087,
  :3100) emiten `<text text-anchor="middle">` DESNUDOS (sin fill/style/class inline) dentro de
  `<svg class="manual-mermaid-svg">` -> la regla (0,1,1) vence al negro por defecto SVG. Sin escape,
  sin sobre-alcance (aristas/flechas/lifelines son <path>, no <text>).
- **Contraste recomputado (WCAG propio):** #e6edf3 / #1c2330 = 13.34:1 (AA>=4.5, AAA>=7); negro
  previo = 1.33:1. Tokens confirmados en el css, no confiados del handoff.
- **Fondo intocable:** product en repo separado; commits del hub para 0309 solo estado gobernado;
  protocol.config.json epoch 1.14.0 + genesis SIN tocar.
- **Residuales declarados no bloqueantes:** R1 sin screenshot de pixeles (no hay browser; render por
  selector-coverage + contraste + regresion estatica = metodo autorizado por Arquitecto); R2 labels
  de mensaje (secuencia) sobre --surface #161b22 -> contraste aun mayor, solo mejora.
- LECCION: el "verificar RENDER no solo string" se satisface aqui SIN browser probando el DOM path a
  nivel de codigo (los `<text>` son desnudos, la regla los golpea por especificidad) + baseline
  negativo behavioral + contraste computado. Declarar R1 honesto (no es pixel real).

## Ultima actualizacion 2026-08-02 (36) - TASK-0308 medicion pre-registrada H1-H3 sobre corpus sellado N=500: OK-CLOSABLE

- Encargo `MSG-20260802-Arquitecto-to-Analista-REVIEW-TASK-0308`. Corpus = tag `TFM-dataset-N500`
  (`e3646ae`); entregable (informe HTML + data-medicion-H1-H3-20260802/) en HEAD `67942f2`. Clon limpio
  `D:/Aegis_Scratch/mapp/ccv0308` checkout del TAG, recomputo independiente. Veredicto commit `83c03f9`
  (artefacto `Area_comun/artifacts/Analista-TASK-0308-medicion-H1-H3-verdict.md` + MSG REVIEW). Push OK.
- **VEREDICTO: OK-CLOSABLE.** Gates por exit code: validate(tag)=0, validate(HEAD)=0, scan_encoding=0,
  scan_domain_neutrality=0, drift has_drift=False.
- **FASE0 sello (recomputado YO):** 500/500 elegibles (seq>=2221 AND intent.applied AND
  actor_auth.method==ed25519), desglose {Arq 253, Codex 195, Analista 52} EXACTO, ventana 2221..2720,
  0 no-firmados, 0 anclas. config sha256 2e35f26e byte-identico, epoch 1.14.0. Pins 1/2/3/5 byte-identicos;
  pin4 event-state.runtime.json gitignored (claves PRIVADAS -> el camino de verificacion no lo usa). FONDO
  INTOCABLE intacto.
- **H1 (lo central):** reproduje arm1 fase1_attacks.py EXACTO (7 vectores 25/25). 6 vectores 100%. Borrado:
  INTERIOR detectado (gap de seq, 6/6 posiciones), **truncamiento de COLA ACEPTADO/EVASION** (borrar ult.
  1/2/5 y el ult. elegible seq 2720 -> pipeline ACEPTA). **Caza de escape (por comportamiento):** re-encadenado
  = borrar interior + renumerar seq downstream + recomputar prev_hash -> DETECTADO `invalid_signature` porque
  `actor_auth_signable_event` CONSERVA `seq` (renumerar rompe la firma Ed25519, no se re-firma sin privada; no
  renumerar deja gap: las dos ramas caen). Payload en la punta -> DETECTADO (prev_hash propio). **No hay escape
  nuevo** mas alla de la limitacion A3 "cabeza no anclada" (0 anclas, sin head-pin) declarada en pre-registro s.8.
  FPR 0/500; AC2 500/500.
- **H2:** almacenamiento (~380-408 B/ev << 4KB) y tokens (~0%, events.jsonl NO en token_cost.coldstart_globs)
  CONFIRMADOS; latencia end-to-end REFUTADA-segun-enunciado (O(n) por re-verificacion del log entero por submit
  del core sellado; DECISION-0105 post-sello, audit-first). NO re-corri el wall-clock (sensible al entorno,
  veredicto ya es FALLO conservador). El O(n) es visible: el propio validate tarda >2min sobre este corpus.
- **H3:** 500/500 verifican SOLO con publicas (sin secretos en el clon: no secrets/ ni event-state.runtime.json);
  has_drift=False; validate=0. Confirmado `runtime/protocol_replay.py` en el tag NO tiene `__main__` (0 hits)
  -> `--check-drift` es no-op, exit 0 VACUO, correctamente no citado como verificacion externa.
- **Sin maquillaje:** el informe etiqueta contra el umbral LITERAL y refuta H1-estricto + H2-latencia (direccion
  conservadora). El `RECONCILE` documenta el diff-entre-brazos (arm1 apunto a interiores -> 100% falso; arm2
  incluyo la punta -> cazo la cola). OJO: `CONSOLIDATED_arm1.json` en AISLAMIENTO aun muestra event-deletion
  tpr=1.0/all_100pct=true/evasions=[] (dato PRE-reconciliacion); el RECONCILE + informe lo corrigen. Residual R2
  no bloqueante: sugeri nota de 1 linea en arm1.json -> RECONCILE. SIN PRODUCTO EN ALCANCE.

## Ultima actualizacion 2026-07-30 (35) - TASK-0307 palanca C (compactacion fisica del log): OK-CLOSABLE sobre hub@1831bdd

- Encargo `MSG-20260730-Arquitecto-to-Analista-REVIEW-TASK-0307`. HUB-ONLY, RIESGO ALTO (el motor del ledger
  MUEVE eventos fisicamente). YA compactado en vivo: `runtime/state/archives/events-000672-006825.jsonl`(+.sha256)
  con 6154 eventos (seq 672..6825), cola caliente `events.jsonl` 3 eventos (6826..6828). Snapshot up_to_seq=6828,
  canonical_hash=07f0d6db, integrity.prev_hash=efd07d7e. Impl `98b887a`, entrega `5365725` (donde se ANADIO el
  archivo a git -> el clon limpio SI lo trae), padre impl `2fd10a6`, HEAD `1831bdd`. Veredicto commit `4369521`
  (artefacto `Area_comun/artifacts/Analista-TASK-0307-compaction-verdict.md` + MSG REVIEW a Arquitecto). Push OK.
  Clon limpio `D:/Aegis_Scratch/protocol/ccv0307` checkout 1831bdd, gates por EXIT code.
- **VEREDICTO: OK-CLOSABLE.** Los 6 AC verifican por comportamiento.
- **AC2 (EL critico, cero perdida):** reconstrui YO el set completo (lei archivo + cola a mano, sin fiarme de
  `events_in_log_order`) y recompute la cadena con los helpers puros. Union=6157 eventos, seq 672..6828
  CONTIGUOS (0 huecos, 0 dup, sin solape archivo/cola), 6156 enlaces prev_hash recomputados 0 rotos incl. la
  COSTURA 6825->6826, sidecar SHA-256 casa, head.prev_hash==integrity.prev_hash, y replay(union) da el MISMO
  canonical_hash 07f0d6db del snapshot firmado. Cadena = lista enlazada por hash -> cualquier perdida/dup/reorden
  rompe un enlace. Union es superset del padre (672..6822 todos en el archivo). recon.py -> AC2_RECON_VERDICT=PASS.
- **AC4 (offline lee archivos + fail-safe):** mute el evento seq 3672 DENTRO del archivo y RECOMPUTE el sidecar
  (atacante que arregla el hash) -> `validate_collaboration_state.py` sigue exit 1 (`chain invalid: corruption at
  seq 3672`, snapshot mismatch, actor_auth). El sidecar es solo el atajo del camino vivo; la frontera dura es
  validate_chain full sobre la union. Fail-safe vivo (banco sintetico): byte corrupto sin arreglar sidecar ->
  `archive_integrity valid=False` -> `verify_snapshot_checkpoint trusted=False invalid_archive_integrity` ->
  `EventWriter.state()` cae a full, NO lanza.
- **AC3 (O(cola) byte-identico):** el clon NO trae la clave `runtime` (gitignoreada) -> el camino de CONFIANZA
  vivo NO es ejercitable sobre el snapshot del clon (cae a `unresolved_key`->full, fail-safe correcto). Lo cubri
  con BANCO SINTETICO propio (clave real `tb-secret`, chain+event_auth, 8 eventos->snapshot->compacta->3 mas de
  cola): instrumente `verify_event_auth` con contador -> camino vivo autentica 3 (solo la cola seq9..11) vs 11
  (full), byte-identico. Trusted up_to_seq=8, incremental=3.
- **AC5 (fail-closed graceful):** up_to_seq="NaN"->`invalid_checkpoint_sequence`; max_incremental_events="lots"
  ->`invalid_checkpoint_policy`; ambos trusted:False y `state()` completa sin excepcion.
- **AC1/AC6:** compact_through cableado en `write_snapshot` (si integrity y hot>umbral). Umbral
  compaction_threshold=1024 en `runtime/CHECKPOINT_POLICY.json` (FUERA del config pineado, ausente del config).
  MUEVE no borra (union completa 6157). Config byte-identico vs padre impl y vs 2fd10a6 (exit 0), sin genesis.
  Alcance codigo: eventlog.py + CHECKPOINT_POLICY.json(+1) + banco.
- **Residuales declarados (no bloquean):** R1 union arranca en seq 672 (1..671 ya ausentes en el padre 2fd10a6,
  PRE-existente, no efecto de 0307; gate valida verde desde 672 -- si se quisiera exigir el genesis fisico en el
  prefijo archivado seria DECISION aparte). R2 camino de confianza vivo no ejercitable en clon (clave gitignoreada)
  -> banco sintetico (fail-safe por DECISION-0046). R3 compact_through asume hot log ascendente para el nombre
  (garantizado por append-only).
- **Gates clon limpio:** banco(7)+validate+scan_encoding+scan_domain_neutrality+git diff --check = exit 0.
  scan_domain_neutrality es LENTO (escanea el archivo de 8.5MB) -> correrlo con timeout propio, no en el lote de 2min.
- **Gotcha reusado:** el clon limpio NO trae `.protocol-secrets/` -> el camino de confianza vivo hay que
  ejercitarlo con banco sintetico con clave de fixture; el offline (cadena prev_hash) SI se audita sin secreto.
- Ciclo: mi veredicto -> Arquitecto ratifica -> Codex done-flip. Con C cerrada, la tanda de perf del ledger
  (A+B+C) completa. Prune vencido senalado por el hook (es del Arquitecto), no corrido por mi.

## Ultima actualizacion 2026-07-30 (34) - TASK-0306 palanca B (checkpoint firmado + verificacion incremental): OK-CLOSABLE sobre hub@4540f5b

- Encargo `MSG-20260730-Arquitecto-to-Analista-REVIEW-TASK-0306`. HUB-ONLY, maxima rigurosidad (cambia el
  MODELO DE CONFIANZA del camino vivo). El snapshot gana `integrity` = HMAC-SHA256 con la clave de INSTANCIA
  `runtime` (`runtime-hmac:v1`) sobre `(canonical_hash(state), up_to_seq, prev_hash@up_to_seq)`.
  `EventWriter.state()` (la ruta real de submit_intent via `writer.state()`) siembra desde el checkpoint si es
  de CONFIANZA y verifica SOLO `seq>up_to_seq`; si no, `replay_events(TODOS)` (full). Impl `18c175f`, entrega
  `3df7135`, padre del impl `4024481`, HEAD canonico `4540f5b`. Veredicto commit `d155987` (artefacto
  `Area_comun/artifacts/Analista-TASK-0306-checkpoint-incremental-verdict.md` + MSG REVIEW a Arquitecto). Push OK.
  Clon limpio `D:/Aegis_Scratch/protocol/r306` checkout 4540f5b, gates por EXIT code.
- **VEREDICTO: OK-CLOSABLE.** NO me fie del banco del autor: escribi mi PROPIO arnes (`_adv_review.py`, fixture
  propio con clave distinta, mezcla mas rica) y ataque 11 vectores de checkpoint invalido con payloads NUEVOS.
- **AC3 (EL critico, fail-safe airtight):** por CADA invalido verifique DOS cosas -- (i) `verify_snapshot_checkpoint`
  da `trusted:False`+reason esperado; (ii) el CALLER REAL (`EventWriter.state`) verifica TODOS los eventos
  (parchee `verify_event_auth` con contador -> `verified_seqs==[todos]`). Cero skip. Las 3 fugas centrales que
  el instructor temia CAEN a full: state manipulado + `canonical_hash` almacenado RECOMPUTADO -> el check
  RECOMPUTA `canonical_hash(stored['state'])` (eventlog.py:778-780) y no confia el campo almacenado ->
  `checkpoint_metadata_mismatch` (integrity vieja) / `invalid_signature` (si tocan integrity sin el secreto) /
  `invalid_signature` (re-firmado con secreto equivocado). Forjar exige el secreto de instancia = modelo
  declarado, respaldado por AC4.
- **AC4 (offline NO debilitado):** evento VIEJO manipulado (`seq<=up_to_seq`) que el vivo "confiaria" SIGUE
  cazado offline por `validate_chain` (valid=False) + drift por `assert_snapshot_matches` (rebuild full,
  validate_collaboration_state.py:1322). `verify_snapshot_checkpoint` se usa SOLO en `EventWriter.state()`; el
  validador offline no lo toca (`events_in_log_order`+validate_chain+agent_signatures+assert_snapshot_matches).
- **AC2 (byte-identico):** diferencial propio -> sembrado==full en estado y snapshot byte-a-byte; solo la cola
  verificada (`verified=[7,8]`, up_to_seq=6).
- **AC1/AC5:** HMAC de instancia sin clave nueva; `max_incremental_events` en `runtime/CHECKPOINT_POLICY.json`
  (fuera del config pineado, confirmado ausente del config); `protocol.config.json` byte-identico vs padre del
  impl (ni aparece en la lista del commit) sin genesis/cadena; alcance 3 rutas + escritos gobernados; fallback
  `verified_state=None`=rebuild full intacto.
- **Leccion / gotcha del clon limpio:** el clon NO trae `.protocol-secrets/` -> sobre el snapshot VIVO,
  `verify_snapshot_checkpoint` cae a `unresolved_key` -> full (fail-safe correcto por DECISION-0046). La rama de
  CONFIANZA hay que ejercitarla con fixture propio (clave controlada), no con el snapshot vivo. Esta vez NO copie
  secrets del hub (a diferencia de 0305): el fixture propio es mas limpio y reproducible para atacar la familia.
- **Residuales declarados (no bloqueantes):** (1) HMAC de instancia es forjable por quien tenga el secreto
  runtime -- por DISENO (DECISION-0105 G1/G2), frontera dura = gate offline; (2) `up_to_seq`/K_max no-numerico
  puede abortar el submit por excepcion = fail-CLOSED (para en error, nunca skip inseguro). Gates: banco +
  validate/validate_chain + scan_encoding + scan_domain_neutrality exit 0; arnes propio 31/31 PASS.
- Ciclo: mi veredicto -> Arquitecto ratifica -> Codex done-flip. Con B cerrada sigue C (TASK-0307, compactacion).

## Ultima actualizacion 2026-07-30 (33) - TASK-0305 MOTOR DEL LEDGER: verificar el log 1 vez por submit: OK-CLOSABLE sobre hub@625ab32

- Encargo `MSG-20260730-Arquitecto-to-Analista-REVIEW-TASK-0305`. HUB-ONLY, maxima rigurosidad (motor del
  ledger). Refactor enhebra `verified_state`: 1 verificacion completa inicial (`writer.state()` = replay de
  TODO el log) + avance incremental por evento (`replay_events([event], base_state=vs)`); el snapshot se arma
  desde ese estado (`up_to_seq` + `deepcopy` + `canonical_hash`) en vez de `rebuild_snapshot`. Fallback
  `verified_state=None` = comportamiento original. Impl `625ab32` (entrega `608a61b`, padre `8873a5f`, HEAD
  canonico entonces `a6a9236`). Veredicto commit `d4500ac` (artefacto
  `Area_comun/artifacts/Analista-TASK-0305-submit-intent-state-once-verdict.md` + MSG REVIEW a Arquitecto). Push OK.
  Clon limpio `D:/Aegis_Scratch/protocol/r0305` checkout 625ab32, gates por EXIT code. Copie secrets/ del hub vivo
  al clon (no estan en git) para firmar/verificar byte-a-byte.
- **VEREDICTO: OK-CLOSABLE.** El vector critico era AC2 (identidad byte-a-byte). NO me fie del test del autor:
  construi mi PROPIO oraculo diferencial (`harness0305.py`) sembrado desde el LEDGER REAL (6101 eventos),
  comparando el camino enhebrado contra (a) legacy `verified_state=None` full-replay-por-op y (b)
  `rebuild_snapshot` (full replay independiente), en 4 vectores de divergencia: plain-multi, claims-fencing,
  stale-fencing-reject, idempotent-reapply. snapshot.json byte-identico legacy==thread Y == rebuild_snapshot
  (canonical_hash+up_to_seq+state) en LOS 4.
- **Trampa que cace y cerre yo mismo (leccion):** en claims/apply, events.jsonl legacy vs thread DIFIRIO -> primer
  instinto SLIP. Pero al diffear los eventos, la union de campos distintos fue EXACTAMENTE {ts, event_auth,
  prev_hash}: `ts` era reloj de pared NO fijado en mi arnes (acquire_claim/apply_intent no aceptan ts, usan
  utc_now()), y event_auth (HMAC firma sobre ts) + prev_hash (encadena el firmado) son su cascada derivada. CERO
  campo portador de estado difirio. Al FIJAR ts (monkeypatch `utc_now`) los events quedaron byte-identicos tambien.
  REGLA: un SLIP de bytes de evento que se reduce a {ts+firma+prev_hash} sin delta de estado NO es divergencia del
  refactor -- es no-determinismo del reloj en el arnes; probarlo falsablemente (diff de campos) antes de gritar.
- **AC3** tamper: manipule payload de un evento nuevo enhebrado -> full replay lo RECHAZA
  (security.unauthenticated_event) y cambia canonical_hash. Intra-tx: 2o apply ve fencing=1 del claim del 1o;
  re-acquire incrementa fencing -- coincide con full replay. `replay_events([event])` SI corre
  verify_event_auth/verify_actor_auth sobre el evento nuevo; la confianza en base_state es intra-submit por
  diseno (cross-submit es DECISION-0105, fuera de alcance); la frontera dura offline (validate_chain full cada
  commit) quedo verde en clon.
- **AC5** git diff 625ab32~1..625ab32 (excl. estado/mailbox): SOLO eventlog.py + submit_intent.py + el test.
  protocol.config.json byte-identico vs PADRE (diff vacio) y vs main; sin genesis/re-genesis; genesis seq1 intacto.
  Fallback: grep de callers -> SOLO submit_intent.py pasa verified_state; apply.py/protocol_replay.py/regenesis.py
  llaman sin arg -> rama None (full replay original) intacta.
- **AC4** perf (observable, no es el gate): write_snapshot enhebrado 0.257s vs rebuild_snapshot legacy 14.91s
  (~58x ese paso); verificaciones completas por intent ~3->1 (~3x global), coherente con el ~2.4x del autor
  (96.76s->39.79s). Gates hub (validate/validate_chain full, scan_encoding, scan_domain_neutrality) exit 0 en clon.
- **Residual declarado (no bloqueante):** ejercite la costura EXACTA (append_event/acquire_claim/apply_intent/
  write_snapshot enhebrado vs None) sembrado del ledger real, NO el CLI top-level submit_intent()/submit_intents()
  end-to-end (mutaria estado + exige intents con capabilities). El enhebrado top-level es delgado (vs=writer.state()
  a los mismos metodos que probe) y su identidad esta cubierta por el oraculo; fallback genesis-ref recomputa
  vs=writer.state() (reset correcto). Riesgo bajo.
- **Ciclo:** yo checker -> ratifica Arquitecto -> Codex done-flip. NO promuevo/cierro/flip. Enforce+authoritative ON;
  mi verdict son FICHEROS (artefacto + mailbox open), no estado -> commit directo con pathspec + trailers
  (Task-Id: TASK-0305 + Co-Authored-By), sin submit_intent. Con 0305 cerrada, palanca A (~3x) en firme.

## Ultima actualizacion 2026-07-29 (32) - TASK-0301 fixture re-parentacion de nietos (tree-kill): OK-CLOSABLE (GO) sobre hub@a5396f8

- Encargo `MSG-20260729-Arquitecto-to-Analista-REVIEW-TASK-0301`. HUB-ONLY, SOLO COBERTURA DE TEST en
  `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`; el `.ps1` NO se toca (el fix de tree-kill ya esta en
  0300). Ultima del backlog de endurecimiento. Ancla impl `ccd80b7` (entrega `49b893c`, baseline `2742b58`, HEAD
  canonico `a5396f8`; el test es byte-identico ccd80b7..HEAD). Veredicto commit `6545aad` (artefacto
  `Area_comun/artifacts/Analista-TASK-0301-reparent-tree-kill-verdict.md` + MSG REVIEW a Arquitecto). Push OK.
  Clon limpio `D:/Aegis_Scratch/protocol/ccv0301` checkout a5396f8, gates por EXIT code.
- **VEREDICTO: OK-CLOSABLE (GO).** El vector critico era AC2 (falsabilidad NO VACUA). El test forma un mutante
  quitando el barrido compensatorio (`foreach childPid in killOrder { Stop-Process }`) y asevera EXACTAMENTE 1
  survivor con re-parentacion. Ataque la vacuidad con SONDA INSTRUMENTADA propia (no confie ni en el nombre ni en
  el `assert len==1`): extraje `Stop-LeaseProcessTree` del `.ps1`, reconstrui el mutante, e instrumente el hook con
  un contador de Get-CimInstance + mapeo pid->rol root/child/grand.
- **3 confirmaciones clave de la sonda:** (1) produccion llama `Get-CimInstance Win32_Process` SIN cualificar y
  EXACTAMENTE UNA VEZ (fuente: 1 sola llamada; runtime: contador=1) -> el override del hook SI intercepta -> el
  hook DE VERDAD re-parenta (mata el hijo intermedio tras el snapshot). No vacuo. (2) `[MUTANT + reparent]
  survivors=['grand']` -> el unico survivor es GENUINAMENTE el nieto (pids[2]), no un crash del probe (como
  Get-CimInstance se llama 1 vez, el `Stop-Process -ErrorAction Stop` del hook no se ejecuta dos veces -> no aborta).
  (3) CONTROL: `[MUTANT + NO reparent] survivors=['child','grand']` = 2 -> el `assert len==1` es un DISCRIMINADOR
  REAL de re-parentacion (si el hook fuese vacuo daria 2, un crash 2-3); el unico camino a 1 es el intencional.
- **AC1** helper real + reparent -> 0 survivors (el barrido recoge al nieto). **AC3** suite exit 0 en 3 corridas
  (sin flakiness Wait-Process/timing), `run_complete_tree_kill_case` invocado en main L131, 0300 preservado
  (asercion intact-tree `reparent=False`), 0302/0303/0304 verdes. **AC4** `git diff baseline..HEAD` fuera de ledger
  = solo el test; `git hash-object` base==head: config `81cf406e`, .ps1 `d54febc6` byte-identicos; fondo intocable.
  Gates hub (validate + scan_encoding + scan_domain_neutrality) exit 0.
- **RESIDUAL R1 (declarado, NO bloqueante):** el test asevera CONTEO (`len==1`), no IDENTIDAD (`==[pids[2]]`). Mi
  sonda confirma que HOY el survivor ES el nieto y que el conteo es discriminador robusto -> cobertura correcta y
  falsable; sugeri fijar identidad en un endurecimiento OPCIONAL futuro. No cambia el veredicto.
- **Leccion reutilizable:** cuando un mutante-test asevera solo un CONTEO de supervivientes, el checker debe
  instrumentar rol/identidad + un CONTROL (mismo mutante sin la condicion) para probar que el conteo es un
  discriminador y no un numero que pase por otro camino. Y confirmar la NO-VACUIDAD del hook por el punto de
  intercepcion real (aqui: Get-CimInstance sin cualificar + contador de llamadas = 1). Ver [[checker-test-real-write-path]].
- Prune vencido (cold_start_tokens 22085>=20000, released_ratio 90.91>=90) SENALADO no corrido -- es del Arquitecto
  (capability orchestrator), yo solo lo senalo. Con 0301 cierra el backlog de endurecimiento.

## Ultima actualizacion 2026-07-29 (31) - TASK-0302 heartbeat de observabilidad EXEC_RUNNING: OK-CLOSABLE (GO) sobre hub@6baa55f

- Encargo `MSG-20260729-Arquitecto-to-Analista-REVIEW-TASK-0302`. HUB-ONLY, sin producto Zeus. Anade un heartbeat
  de LOGGING `EXEC_RUNNING pid=.. elapsed=<N>s message=<msg>` al loop de espera del exec, para acabar con la muerte
  muda 0/0-byte de text-mode y dar al watchdog una senal de vida fiable. Ancla impl `6d96522` (entrega `35e2e0d`,
  HEAD canonico `6baa55f`; las 2 rutas de codigo intocadas 6d96522..HEAD). Task `in_review` en HEAD. Veredicto
  commit `ec1c2ad` (artefacto `Area_comun/artifacts/Analista-TASK-0302-heartbeat-verdict.md` + MSG REVIEW a
  Arquitecto). Push OK. Clon limpio `D:/Aegis_Scratch/protocol/rev0302` checkout 6baa55f, gates por EXIT code.
- **VEREDICTO: OK-CLOSABLE (GO).** El vector critico era AC3 (SOLO LOGGING). Lo blinde ESTRUCTURALMENTE, no solo
  por test: el diff COMPLETO del `.ps1` `a4931bb..HEAD` (pre-0302 -> HEAD) son 3 hunks aditivos y nada mas: param
  `[ValidateRange(0,2147483647)][int]$HeartbeatSeconds=60` (0=off), 2 lineas init (`$execStopwatch`/`$nextHeartbeatSeconds`)
  tras EXEC_START, y un `if` sin efectos secundarios al tope del `while(-not WaitForExit(1000))`. Los locals nuevos
  se referencian SOLO en param+init+bloque (grep: lineas 14,1013-1014,1026-1029; cero otros consumidores). El unico
  efecto compartido es escribir al CRON log -- y la logica de progreso/liveness (`Get-ExecProgressState`,
  `no_progress`/`hard_cap`/tree-kill) lee `runtime/state/events.jsonl` + run logs, NO el cron log. Asi que mas
  escrituras al cron log NO pueden perturbar ninguna decision de kill. AC3 garantizado por construccion.
- **PROBE CONDUCTUAL PROPIO (no confie en el nombre del caso):** drive el `.ps1` real con exec lento ~4s y regex
  exacta: `HeartbeatSeconds=1 -> 4 lineas EXEC_RUNNING, elapsed [1,2,3,4] monotono, EXEC_START + completion`;
  `HeartbeatSeconds=0 -> 0 emisiones, exec completa normal` (el interruptor off NO rompe el loop). AC1 PASS.
- **AC2 (falsabilidad):** el caso de banco `run_exec_running_heartbeat_case` muta el harness (quita la emision) y
  asevera `==0`; NO vacuo por el `assert heartbeat_line in runner_text` previo. Banco entero exit 0.
- Banco `run_mailbox_retry_cases.py` exit 0 (incluye TODOS los previos 0300/0303/0304/post-delivery/frozen/hard_cap/
  tree-kill/RETRY, verdes e identicos). validate/scan_encoding/scan_domain_neutrality exit 0. `.ps1` parsea (0 errores).
  `protocol.config.json` byte-identico (sha256 `2e35f26e`, fondo intocable), epoch 1.14.0, drift limpio up_to_seq 6716.
- **Residuos declarados (no bloquean):** el banco NO fija el off-switch (HeartbeatSeconds=0) como regresion nombrada
  -- lo cubri yo aparte (nota de cobertura). Fuera de alcance por diseno y bien diferido: NO detecta el exec
  colgado-pero-vivo de text-mode, NO cambia output-format, NO cablea el watchdog para consumir EXEC_RUNNING (capa
  skills). Ciclo: ratifica Arquitecto -> Codex done-flip -> GO de 0301 (ultima del backlog).

## Ultima actualizacion 2026-07-29 (30) - TASK-0304 heartbeat fiel a liveness real: OK-CLOSABLE (GO) sobre hub@7804dae

- Encargo `MSG-20260729-Arquitecto-to-Analista-REVIEW-TASK-0304`. HUB-ONLY, sin producto Zeus. Cierra el RESIDUAL
  R1 que YO flagee en 0303 (sesion 29): la senal `heartbeat_fresh` no estaba falsificada por comportamiento.
  Ancla impl `45bed5d` (entrega `f1da7a6`, HEAD canonico `7804dae`). Veredicto commit `32354fe` (artefacto
  `Area_comun/artifacts/Analista-TASK-0304-heartbeat-liveness-verdict.md` + MSG REVIEW a Arquitecto). Push OK.
  Clon limpio `D:/Aegis_Scratch/protocol/a304adv` checkout 7804dae, gates por EXIT code.
- **VEREDICTO: OK-CLOSABLE (GO).** Codex ELIGIO retirar el self-bump: `Get-ExecProgressState` ya no deriva
  progreso del heartbeat. Quito el bloque `heartbeat_fresh` (que `Update-ExecLeaseHeartbeat` bumpeaba a `now`
  cada iteracion -> siempre fresh @FreshSeconds=15 -> dominaba el OR -> deteccion temprana `no_progress` era dead
  code). Ahora `progressing = run_log_growing OR ledger_growing` solo. `heartbeat_monotonic` se SIGUE escribiendo
  (marcador de lease, lineas 177/189) pero NO se consume en ninguna decision de progreso/kill (grep-confirmado).
- **FALSABILIDAD EN AMBAS DIRECCIONES (lo que pidio el Arquitecto):**
  - Mut A (re-inyecta self-bump, restaurando .ps1 de `45bed5d^`): el caso frozen FALLA. Primer tripwire es un
    guard ESTATICO `assert "heartbeat_fresh" not in <fuente Get-ExecProgressState>` que corta antes del cuerpo
    conductual. NO lo rubber-stampee: bypassee el assert estatico y re-corri -> el exec CONGELADO sobrevive PASADO
    el timeout de 15s del harness (TimeoutExpired) en vez del kill `no_progress` <12s del baseline. La deteccion
    temprana es consecuencia CONDUCTUAL del fix, no solo un string check.
  - Mut B (over-correct: `progressing = ($reasons.Count -gt 0)` -> `$false`): el caso 0303 progressing FALLA. El
    exec que PROGRESA (stderr `working-N` c/400ms = run-log creciendo) muere en `EXEC_HUNG reason=no_progress` ~2s
    tras EXEC_START, nunca llega a `EXEC_PROGRESSING reason=run_log_growing`. El banco CAZA la sobre-correccion.
    NO matamos trabajo real (el incidente 0299 con run-log creciendo queda protegido).
- Banco `run_mailbox_retry_cases.py` exit 0 (incluye el caso NUEVO `run_frozen_exec_with_production_freshness_case`
  @FreshSeconds=15 + 0303/0300/RETRY/entrega). validate/scan_encoding/scan_domain_neutrality exit 0. `.ps1` parsea
  (`Parser::ParseFile` 0 errores). `protocol.config.json` byte-identico a `45bed5d^` (md5 e2e3cff1..., epoch
  1.14.0). Drift verdict=CLEAN seq=6698. Scope AC4 = solo las 2 rutas + artefactos gobernanza (task/handoff/Codex mem).
- **Residuos declarados (no bloquean)**: R1 params `$Lease`/`$FreshSeconds` de `Get-ExecProgressState` quedan sin
  usar (cosmetico). R2 `heartbeat_monotonic` sobrevive solo como marcador de lease (por diseno, opcion AC1). R3
  el primer tripwire del caso frozen es un grep estatico del literal `heartbeat_fresh`; mata el revert exacto, y
  un signal renombrado que fuerce progressing se caza CONDUCTUALMENTE por los asserts no_progress/hard_cap (verificado
  via bypass). R4 el watchdog de salud del Arquitecto tiene el defecto ESPEJO (err.log 0-byte) -- OUT OF SCOPE, aparte.
- LECCION: cuando el falsability-test empieza con un guard ESTATICO (grep de fuente) que corta antes del cuerpo
  conductual, NO basta ver "mutante muere" -- hay que BYPASSEAR el guard estatico y confirmar que la GARANTIA
  CONDUCTUAL tambien se rompe, si no es un rubber-stamp de string. Aqui el fix aguanto ambos. El validador tarda
  ~29s y PARECE colgarse si un git gc/maintenance de fondo (disparado por fetch/clone) compite por I/O; espera y
  re-corre, sale exit 0 determinista. PRUNE del Arquitecto, no mio.

## Ultima actualizacion 2026-07-29 (29) - TASK-0303 harness liveness-antes-de-matar: OK-CLOSABLE (GO) sobre hub@e266d07

- Encargo `MSG-20260729-Arquitecto-to-Analista-REVIEW-TASK-0303`. HUB-ONLY, sin producto Zeus/Nova. Ancla
  impl `e266d07` (entrega `c5a71eb`, HEAD `3b2d66a`). Veredicto commit `2391f3e` (artefacto
  `Area_comun/artifacts/Analista-TASK-0303-liveness-verdict.md` + MSG REVIEW a Arquitecto). Fix en 2 rutas:
  `scripts/harness/peer_mailbox_cron.ps1` + `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`.
- **VEREDICTO: OK-CLOSABLE (GO).** Los 2 defectos cerrados y verificados POR MUTACION PROPIA del .ps1, no por
  nombre de test. Clon limpio `D:/Aegis_Scratch/protocol/ccv0303` checkout e266d07.
- **DEFECTO A (post-delivery temprano)**: fix = `Get-OwnDeliveryEvidence` (reemplaza `Get-OwnEvidence`) exige
  `intent_type=task_status` AND `transitions.task_status.to -cne "in_review"` AND task con owner==PeerId. El
  reclamo ready->in_progress (to=in_progress) NO gatilla. Mutante (a) `Get-OwnDeliveryEvidence`->`Get-OwnEvidence`
  -> `run_pre_delivery_and_liveness_cases` MUERE (POST_DELIVERY_WINDOW_START aparece en el reclamo).
- **DEFECTO B (kill a ciegas)**: fix = `Get-ExecProgressState` (heartbeat_fresh OR run_log_growing OR
  ledger_growing) en AMBOS deadlines; si progresa extiende `ProgressExtensionSeconds` topado por
  `$execHardDeadlineUtc = deadline + ProgressHardCapSeconds` (TOPE DURO); logs EXEC_PROGRESSING/EXEC_HUNG. Mutante
  (b) progress-check->`$false` y (c) `-lt hardDeadline`->`$true` -> ambos MUEREN. (c') exec CONGELADO nunca matado
  (post-delivery siempre extiende) -> `run_post_delivery_timeout_case` MUERE.
- **Los 4 mutantes MUEREN**, pristine restaura a PASS byte-identico. Banco exit 0 (17 casos, AC4 sin regresion:
  tree-kill 0300 + RETRY/backoff + entrega gobernada). validate/scan_encoding/scan_domain_neutrality exit 0.
  `PSParser::Tokenize` 0 errores (sintaxis .ps1 valida -- gate critico: .ps1 roto tumbaria crons vivos).
  `protocol.config.json` byte-identico (git diff --exit-code = 0, epoch 1.14.0).
- **Residuos declarados (no bloquean)**: R1 la senal `heartbeat_fresh` NO esta falsificada por comportamiento
  (ambos tests fijan `ProgressFreshSeconds=0`; el progreso se prueba via run-log/ledger; el incidente 0299 tenia
  err.log creciendo, cubierto por run-log; gap de cobertura, no defecto). R2 el kill "hung" del caso combinado es
  `reason=hard_cap` sobre un exec que AUN progresa (valida el tope duro); el kill del exec genuinamente congelado
  (`no_progress`) vive en `run_post_delivery_timeout_case`. Cobertura partida en 2 funciones, ambas ramas OK.
- LECCION: falle el commit por el gate de trailers -- dos `-m` separados crean parrafos con linea en blanco; el
  gate exige UN bloque trailer final contiguo (`Task-Id:`+`Ops-Reason:` sin blanco entre ellos). Fix = commit por
  `-F <fichero>`. ASCII: mi propio check byte>127 cazo un "e" acentuado que `scan_encoding` NO flageo (arreglado
  antes de commitear). PRUNE DUE 94.29>=90 senalado no corrido (es del Arquitecto).

## Ultima actualizacion 2026-07-28 (28) - TASK-0298 remediacion iter2 bridge observacion-tail: OK-CLOSABLE (GO) sobre Zeus@ba78954

- Encargo `MSG-20260728-Arquitecto-to-Analista-REVIEW-TASK-0298-remediation-v3`. PRODUCTO ZEUS EN ALCANCE
  (a diferencia de 0297/0300 hub-only). Ancla producto `ba78954` (== origin/main de Zeus-protocol); hub
  `024dcda`. Veredicto commit `cb1168a` (artefacto `...-verdict-iter2.md` + MSG REVIEW). Supersede iter1
  (`76bf94e`, CHANGE-REQUIRED). Es el re-juicio (max 2 iter); este cierra en GO.
- **VEREDICTO: OK-CLOSABLE (GO).** Los 3 bloqueantes de iter1 remediados y verificados POR MUTACION, no
  por nombre de test. Suite lenta en clon limpio `D:/Aegis_Scratch/protocol/zp0298v3`:
  `ZEUS_RUN_SLOW_TESTS=1 PROTOCOL_REPO_PATH=<hub> node --test` -> exit 0, 136/136/0, **0 skips** (coincide
  con Codex).
- **B1 (AC5, el grave)**: fix = framing por LINEA COMPLETA en `pollRunLog` (emite hasta el ultimo `\n`,
  guarda el resto en `session.pending`, avanza offset solo por lo emitido; `flushPendingRunLog` en
  detach/rollover con tope 8192, redactado). Mi SONDA PROPIA (productor progresivo 4 chars/40ms, poll
  25ms -- el caso que rompia iter1) NO fuga: 0 literales en SSE+audit, marcador `[EMAIL-REDACTED]`
  presente. Mutante M-B1 (revertir framing: `boundary=combined.length-1`) -> el test entregado Y mi sonda
  FALLAN (fuga). GOTCHA de mi harness: el helper `readSseEvents` del repo BLOQUEA para siempre en un
  stream quieto si `minEvents` es inalcanzable (colgo mi sonda a 45s); escribi un reader SSE propio con
  tope de reloj (AbortController+setTimeout). Otra: unir eventos con `|` puede ENMASCARAR un literal
  partido entre eventos -> asevero ADEMAS que el marcador de redaccion aparece (prueba que la redaccion
  disparo sobre linea entera).
- **B2 (AC4/I3)**: `spawn` import RETIRADO de server.js (cierra R1 de iter1). Test fail-CLOSED a nivel
  FICHERO: `assert.ok(manager)` (la extraccion debe existir) + `assert.doesNotMatch(source, /\bspawn\s*\(/)`.
  Mutante M-B2 (spawn en el manager + rename global `isProcessAlive`->`isPidAlive` = ancla del extractor
  rota) -> FALLA en `assert.ok(manager, "...extraction must exist")` (ya no falla ABIERTA por el viejo
  `|| ""`). Faceta independiente: spawn inyectado con ancla INTACTA -> la guarda de fichero sola lo caza.
- **B3 (AC6)**: 8 cuerpos `test.skip` legacy BORRADOS; 3 tests VIVOS (instancia unica fail-closed, SIGTERM
  limpia lock, escaneo de escritores gobernados). Mutante M-B3 (`acquireLock();` comentado) -> el test de
  instancia unica FALLA por timeout esperando el lock. Faceta que cierra SLIP-2 de iter1: inyectar
  `Area_comun/state/TASK_INDEX.json` en el launcher -> el escaneo de escritores gobernados lo caza.
- **Los 3 mutantes REQUERIDOS mueren** (exit nonzero), re-inyectados por mi en copias desechables
  (`probe/mB2/mB2anchor/mB3`). Recomendados de iter1 quedaron MEJORADOS: SLIP-4 (orden monotono por sello
  del nombre; mtime retirado del sort) y SLIP-5 (error explicito ante fuente ilegible/vacia).
- **Gates del hub**: validate/scan_encoding/scan_domain_neutrality exit 0; `git diff --exit-code --
  protocol.config.json` exit 0 (epoch 1.14.0 / 2E35F26E intocable). `ba78954` confirmado en origin/main.
- **Residuales declarados no bloqueantes**: R1 (unico `t.skip` en `staticContract.test.js:3419` = guarda
  condicional de disponibilidad de fixture, NO test de B3; "0 skips" es correcto y dependiente-de-entorno:
  no dispara porque `PROTOCOL_REPO_PATH`=hub que tiene `secrets/eventauth-arquitecto.key`; el default
  `D:/Agentes/Zeus/NOVA/Aegis` ya no existe). R2 (borde 8192 sin salto de linea: fragmento parcial, el
  literal completo nunca aparece). R3 (residuales de iter1 que el fix no toca: app.js control-path, R5
  stripControl).
- **GOTCHAS operativos**: (a) trailer gate del commit-msg exige `Task-Id`+`Ops-Reason` en UN SOLO bloque
  final SIN linea en blanco entre ellos -> con multiples `-m` hay que meter ambos trailers en el ULTIMO
  `-m` juntos. (b) PRUNE DUE (cold_start_tokens>=20000) senalado en el commit -- NO lo corro yo (es del
  Arquitecto en su checkpoint). (c) commit AS Analista via `GIT_AUTHOR_*`/`GIT_COMMITTER_*`=analista@local
  (el git user del entorno es Codex).

## Ultima actualizacion 2026-07-26 (27) - TASK-0295 detector de scratch discipline: OK-CLOSABLE (GO) sobre b1b3bbc

- Encargo `MSG-20260726-Arquitecto-to-Analista-REVIEW-TASK-0295`. Teeth de DECISION-0104 cl.5b (firmada
  2026-07-26): detector read-only que FLAGea (nunca borra) arboles de metodologia fuera del scratch root.
  Ancla: HEAD origin/main `b1b3bbc`, impl `3aa332d`; el delta `b1b3bbc..8f1e495` es SOLO el MSG de REVIEW.
  Veredicto commit `a8fc684` (artefacto `Area_comun/artifacts/Analista-TASK-0295-detector-scratch-discipline-verdict.md`
  + MSG REVIEW). SOLO PROTOCOLO (el Arquitecto declaro "sin producto en alcance" -- ver la leccion de que
  hay que declararlo explicito).
- **VEREDICTO: OK-CLOSABLE (GO), sin iteracion.** Banco adversarial PROPIO de 31 vectores: 31 PASS, 0 SLIPS.
  4 gates exit 0 en clon limpio (suite del maker / validate / scan_encoding / scan_domain_neutrality).
- **REGLA 0104 APLICADA A MI PROPIO TRABAJO**: clon limpio y TODOS los fixtures bajo
  `D:/Aegis_Scratch/multi_agent_project_protocol/{an0295,an0295fx,an0295fix,an0295adv}`. Nada en la raiz
  del disco. La ruta corta tambien evita MAX_PATH.
- **Read-only probado mas fuerte que el maker**: el fingerprint del maker solo hashea CONTENIDO; yo compare
  ademas `st_mtime_ns` + `st_size` de TODO nodo incluido `.git/**` antes/despues de 3 corridas (json, texto,
  sin --check) -> identico. Mas auditoria de API mutante en el fuente (`.write_text/.mkdir/open(/os.remove/
  os.rename/shutil.*/.unlink/.rmdir/.touch`) = 0 ocurrencias.
- **Deteccion probada por FAMILIA, no por el ejemplo del acceptance**: remote scp-like `git@host:o/r.git`
  contra known dado en https (identidad equivalente), remote de RUTA LOCAL con backslashes, **git worktree**
  (`.git` como ARCHIVO, config compartida), dir OCULTO con marcadores, marcadores parciales, clon conocido
  DENTRO del scratch, archivo top-level homonimo, scratch root en MAYUSCULAS + separador final. Set exacto
  de 6 hallazgos, cero falsos positivos.
- **Exit codes: lo que importa es el fallo ruidoso.** 1/0/2 exactos, y scan root inexistente / scan root que
  es un ARCHIVO / `known_repositories` malformado dan **2**, nunca un "limpio" silencioso (ese era el modo
  de fallo peligroso para unos teeth; no ocurre).
- **Residuales declarados (no bloquean; el acceptance dice literalmente "directorios de nivel superior")**:
  R1 (MATERIAL) escaneo de PROFUNDIDAD 1 -- medido en seco: `--scan-root D:/ --scratch-root D:/Aegis_Scratch`
  da **exit 0, 0 hallazgos** con 12 dirs top-level, mientras `D:\Agentes\runtime-test-instance` tiene los 3
  marcadores atestados fuera del scratch root a profundidad 2. R2 (MATERIAL) sin allowlist de hogar canonico:
  `--scan-root D:/Agentes` -> exit 1 flageando el stray real Y el hub legitimo. R3 fail-open silencioso si
  `git` falla (gitfile corrupto / dubious ownership / git ausente) sin warning. R4 `protocol.config.json` NO
  tiene campo `scratch_root` (el chequeo 0098 del validador es CONDICIONAL al campo) y nada invoca al
  detector desde gate/CI/cron -> hoy 0104 cl.5b esta DETECTABLE, no ENFORCED. R5 marcadores en AND estricto
  (los 3). U1 sin `--check` el exit es 0 aunque haya hallazgos.
- **Leccion de metodo**: cuando el acceptance limita el alcance (aqui "nivel superior"), la conducta
  conforme NO es automaticamente conducta util -- correr el detector contra el disco REAL (read-only) es lo
  que revela que apuntado a la raiz devuelve 0 hallazgos. Distinguir SLIP (viola la letra) de RESIDUAL
  MATERIAL (cumple la letra y no muerde) y reportar ambos con reproduccion falsable.
- **Leccion de shell**: en Git Bash, un `>` a `/tmp/x` y un `open('/tmp/x')` desde Python de Windows NO
  apuntan al mismo sitio (Python resuelve a `<unidad>:/tmp`). Escribir salidas intermedias con ruta absoluta
  Windows bajo el scratch root.

## Ultima actualizacion 2026-07-24 (26) - TASK-0294 residuales nuevos de 0293: OK-CLOSABLE (GO) sobre dad27b3

- Encargo `MSG-20260724-Arquitecto-to-Analista-REVIEW-TASK-0294`. Cierra los 3 residuales ACCIONABLES
  nuevos de 0293: RES-8 (fila del checker en la tabla de roles del template), RES-9 (muestra generada a
  MINIMAL, no falsa vigencia), RES-10 (cobertura de neutralidad de examples). Ancla: impl `dad27b3`
  (remediacion iter1 que restaura la muestra minimal) + `e98f007` (entrega inicial), base `5dacd85`;
  re-chequeo en HEAD origin/main `01a02e6` (el coord de la REVIEW, solo mailbox/CLAIMS/runtime). Clon
  limpio `/d/ccv0294`, instancias temporales en scratchpad. Veredicto commit `672bb13` (artefacto
  `Area_comun/artifacts/Analista-TASK-0294-roster-checkerrow-sample-neutrality-verdict.md` + MSG REVIEW).
  SOLO PROTOCOLO (sin producto).
- **VEREDICTO: OK-CLOSABLE (GO), sin iteracion.** Los 3 vectores PASS. 6 gates exit 0 (validate/neutralidad/
  encoding/drift CLEAN seq 6382-6388/test_attested_instancing/run_runtime_instantiation_cases 8+ps1) en
  clon limpio. Diff neto `5dacd85..dad27b3` = 16 archivos +422/-13 (NO +20K: confirmada la reversion de la
  sobre-materializacion que el recomputo del Arquitecto cazo en la 1a entrega, 21->104/+20K).
- **RES-8 por el ENTRYPOINT REAL, no por texto**: genere con `new_instance.py` en los 3 tiers
  (coordination/runtime/attested) y grep de la fila del checker en cada AGENTS.md generado -> presente con
  placeholder SUSTITUIDO (`CHECKER_ZZZ`), `{{AGENT_ANALYST}}` leak = 0. GOTCHA tier attested: su AGENTS.md
  se anida bajo el gov-dir por defecto (`Aegis/`), no en la raiz de la instancia. Los 3 cuerpos de reglas de
  0099 NO cambian (grep en el diff del template = 0); la unica edicion es la fila que da referente titulado
  a 'the roster'.
- **RES-9 falsabilidad del 'regenerada fiel'**: la prueba fuerte contra 'hibrido hand-edited' = regenerar
  fresca con la MISMA roster y diff FULL-FILE; difieren SOLO en campos instance-specific (goal/description/
  phase que pase distintos), todas las secciones emitidas por el template byte-identicas (114/114 en el
  bloque 6.1..8). `Last updated: 2026-07-24` (grep 2026-06-05 = 0). Las 5 secciones antes ausentes con
  header propio. Residual no bloqueante: 21 archivos vs 19 de la referencia = `.gitkeep` en dirs vacios +
  `BRIDGE_CONTRACT.md` (forma de instancia fresca, NO arbol runtime; runtime/scripts/skills = 0).
- **RES-10 falsable por comportamiento, no por diff**: git diff = SOLO docstring. Prueba viva: inyectar
  `binance trading` en archivo EXENTO (examples/) -> scan exit 0 (exencion by-design confirmada); inyectar
  en superficie ESCANEADA (`AGENTS.template.md`) -> scan exit 1 cazando ambos terminos; revertir -> 0. La
  logica/alcance de deteccion no cambio.
- **Leccion de metodo**: para 'regenerado fiel al template', el diff full-file contra una regen fresca con
  la misma roster es el discriminador limpio -- separa lo instance-specific (legitimo) de un hand-edit
  residual. Y para un docstring 'by-design', no basta leer el diff: hay que probar que la exencion que
  documenta es REAL (inyeccion en exento -> verde) Y que la deteccion sigue viva (inyeccion en escaneado ->
  rojo). Fondo intocable no tocado (2E35F26E, epoch 1.14.0, N=500, N=6).

## Ultima actualizacion 2026-07-24 (25) - TASK-0293 pulido residuales roster policy: OK-CLOSABLE (GO) sobre 130f63c

- Encargo `MSG-20260724-Arquitecto-to-Analista-REVIEW-TASK-0293`. Cierra los 4 residuales ACCIONABLES que
  yo declare en TASK-0256 (POLISH/RES-5 alcance sin "that execute code", RES-7 exencion condicional del
  registry, RES-3 razon de la regla 3, RES-1 muestra generada). Ancla: impl `130f63c` (base `b7babed9`);
  la instruccion citaba HEAD `273376c` pero el origin/main real al juzgar era `0047279` y el delta entre
  ambos es SOLO ledger/mailbox -> ancla en `0047279`. Clon limpio `/d/ccv293`, instancias temporales en
  `/d/i293`. Veredicto commit `7196b8d` (artefacto
  `Area_comun/artifacts/Analista-TASK-0293-roster-policy-polish-verdict.md` + MSG REVIEW). SOLO PROTOCOLO.
- **VEREDICTO: OK-CLOSABLE (GO), sin iteracion.** 11 vectores PASS. Reglas 1 y 2 byte-identicas (no
  aparecen en el diff = esa es la prueba); regla 3 conserva sus 3 clausulas normativas y solo suma la
  razon. Diff no-ledger = `AGENTS.template.md 4/3` + muestra `18/0`. Gates: validate/encoding/neutralidad/
  drift(CLEAN seq 6358)/test_attested_instancing/run_runtime_instantiation_cases = 6/6 exit 0; instancias
  nacidas 9/9 exit 0; `validate --root examples/generated_minimal_instance` = 0. Neutralidad FALSABLE
  sobre las 2 lineas nuevas del template (inyeccion -> exit 1 en l.61 y l.75; restaurado -> 0).
- **Aporte central del juicio: refute la PREMISA de la pregunta del Arquitecto y confirme su CONCLUSION.**
  El decia "el alcance sigue excluyendo al human owner porque un humano no es un agente". FALSO en el
  artefacto: el tier attested emite `agent_registry.agents` con `{"id":"Own","role":"human_owner",
  "tier":"worker","adapter":"human"}` -> el human owner ES una entrada del roster de agentes y cae DENTRO
  del alcance nuevo. Lo que mantiene SLIP-1 cerrado NO es la palabra "agent" sino la clausula de exencion
  explicita ("does not alter the human owner's approval authority"), intacta desde 0256.
- Residuales NUEVOS (no bloqueantes): **RES-8** "the roster" no tiene referente definido y la unica tabla
  TITULADA de roles del template trae 3 filas SIN la del analyst/checker -> la sub-captura de RES-5 entra
  por otra puerta (fix de una linea: anadir la fila del analyst). **RES-9** la muestra quedo HIBRIDA: el
  intake ofrecia regenerar O fechar como snapshot congelado, y la entrega hizo una tercera cosa (parche a
  mano); sigue diciendo `Last updated: 2026-06-05`, 0 ocurrencias de "snapshot", 132 lineas de diff y 5
  secciones enteras faltantes frente a una generacion fresca -> senala falsa vigencia. **RES-10**
  `examples/**` es exempt_glob del scan de neutralidad -> las 18 lineas de politica que esta tarea mete en
  la muestra quedan SIN gate (falsable: inyeccion en la muestra -> exit 0; la misma en el template -> 1);
  inocuo hoy porque probe que el bloque es byte-identico al del template.
- Correccion de registro C2 (DECISION-0018 al Arquitecto): mi "9/9 gates de instancia nacida" de 0256 solo
  se reproduce con ids de agente que NO sean subcadenas de palabras inglesas. Con `--human-owner Own` el
  `scan_domain_neutrality --root <instancia>` da exit **1** en los 3 tiers (flaggea `Own` dentro de
  comentarios preexistentes: "ITS OWN", "own path semantics"); con `--human-owner Duenyo` -> exit 0.
  Preexistente y ajeno a 0293, pero una instancia puede NACER con su propio gate en rojo.

LECCIONES nuevas de esta iteracion:
10. **Refutar la premisa aunque la conclusion sea correcta.** El Arquitecto pedia confirmar dos cosas
    encadenadas ("excluye al human owner PORQUE un humano no es un agente"). La conclusion se sostiene y
    la premisa no. Firmar el GO sin separar ambas habria dejado en el registro una defensa falsa de la
    politica, reutilizable en el proximo debate. El checker valida el razonamiento, no solo el resultado.
11. **Cuando un fix cambia un predicado de alcance, enumerar los REFERENTES candidatos.** "that execute
    code" (definido, estrecho) -> "of the roster" (ancho pero INDEFINIDO). Tabule los 3 candidatos
    (lista de participantes / tabla titulada / `agent_registry.agents`) y verifique si el sujeto de la
    regla cae dentro de cada uno; bajo el mas literal (la tabla) el checker sigue sin estar enumerado.
12. **Contrastar una "muestra generada" contra una generacion FRESCA, no contra el grep pedido.** El grep
    de la acceptance daba verde; el diff contra `new_instance.py` revelo 132 lineas y 5 secciones
    faltantes + fecha de junio. Un artefacto parcheado a mano miente mas que uno viejo y honesto.
13. **Probar si el gate cubre el archivo donde se mete el texto nuevo.** `examples/**` esta exento: inyecte
    un termino de negocio en la muestra (exit 0) y el MISMO en el template (exit 1). Un verde sobre un
    archivo exento es un verde vacio; lo salve verificando byte-identidad con el bloque si gateado.
14. **Aislar la causa antes de reportar un ROJO.** El neutrality de las instancias nacidas salio 1 en los
    3 tiers; en vez de firmarlo como regresion, re-genere con otro id de human owner -> 0. La causa era
    MI parametro ("Own" como subcadena), no la entrega. Un rojo no atribuido es tan malo como un verde
    no falsado. (Corolario ya sabido y re-pisado: gatear por exit code REAL, nunca `python x | head`,
    que devuelve el exit de `head` y me dio "exit=0" sobre una salida que mostraba violaciones.)

## Ultima actualizacion 2026-07-24 (24) - BATCH TASK-0291 (R3) + TASK-0292 (R4): OK-CLOSABLE (GO) para AMBAS sobre 23d7476+dd9602a

- Encargo `MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0291-0292`. Residuales R3/R4 del veredicto de
  TASK-0289. Ancla: clon limpio `/d/ccv0291` sobre origin/main `a3d7b91` (contiene impl `23d7476` +
  remediacion iter1 `dd9602a`; `b0425d6..a3d7b91` NO toca hook ni runner). Veredicto commit `1bed95e`
  (artefacto `Area_comun/artifacts/Analista-TASK-0291-0292-fullhook-align-masking-reason-verdict.md` +
  MSG REVIEW `MSG-20260724-Analista-to-Arquitecto-REVIEW-TASK-0291-0292.md`). SOLO PROTOCOLO, sin producto.
- **VEREDICTO: OK-CLOSABLE (GO) para AMBAS.** R3 = +3 lineas en `.githooks/pre-commit` (opcion B:
  `git ls-files --error-unmatch -- "$path" || continue` antes del `checkout-index` de deliverables
  `personal/`). R4 = el assert de la masking-probe exige `deliverable missing` + `collaboration state ...
  invalid`. Remediacion iter1 = el fixture non-reviewed pasa a tarea SINTETICA inyectada clone-local.
- Gates clon limpio (exit code): validate 0; scan_encoding 0; scan_domain_neutrality 0; full-hook arbol
  limpio 0; `run_hook_fullmode_inventory_cases.py` 0 y 0 (2 corridas, con 0291/0292 ya `in_review`);
  pin CI `bd89ec30...` = MATCH; `git diff --stat 23d7476^ a3d7b91 -- scripts/ runtime/protocol_replay.py
  runtime/submit_intent.py protocol.config.json` VACIO.
- **METODO QUE VALIO (repetir):** no me fie del ejemplo dado -- probe la FAMILIA COMPLETA de estados con
  una tarea sintetica `TASK-9999` propia: 6/6 no-revisados (proposed/ready/claimed/in_progress/blocked/
  cancelled) -> exit 0; 5/5 revisados (in_review/review_approved/qa_pending/architect_review/done) ->
  exit 1 con `deliverable missing` + frontera del validador y SIN `could not materialize`.
- **FALSABILIDAD (lo que convierte el assert en real):** restaure el hook PRE-R3 (`66e7f38...`) en un
  sandbox y corri los MISMOS probes -> `ready`/`cancelled` exit 1 por `could not materialize` (el
  falso-rechazo era REAL) y `done` exit 1 por checkout-index SIN `deliverable missing` (o sea: el assert
  de R4 NO habria pasado pre-R3). Tecnica: extraer el blob viejo con `git show <sha>^:<path>` y
  sobrescribirlo en el sandbox + `git add`.
- **REFUTACION QUE INTENTE Y FRACASO (anotar como patron):** hipotesis "la opcion B delega en el
  validador, pero el validador solo ve el indice CALIENTE -> tarea revisada ARCHIVADA con deliverable
  ausente escaparia". FALSA: `main()` hace `merge_by_array_field(index_hot, index_archive, ...)` antes de
  `validate_tasks`. De hecho la masking-probe ataca `personal/Codex/STARTUP_PROMPT.md`, deliverable de
  `TASK-0084` (`done`, ARCHIVADA) -> ya ejercita el camino del archivo.
- **Caza de escapes, 4 vectores, 0 hallazgos:** E1 revisada + deliverable existente sin trackear y NO
  staged -> RECHAZA (no hay enmascaramiento); E2 ruta `personal/./Codex/...` -> RECHAZA; E3 estado roto
  staged -> RECHAZA; E4 revisada + deliverable staged NUEVO -> ACEPTA (sin falso-rechazo positivo).
- Residuales declarados NO bloqueantes: RES-1 el id sintetico se busca solo contra `TASK_INDEX.json`
  (ciego al archivo; colision futura la cazaria `Duplicate task across hot/archive` = CI rojo, no verde
  falso); RES-2 el assert busca las subcadenas en el output global sin ligarlas al path; RES-3
  PREEXISTENTE (`selected == 1`, conteo acoplado a indices vivos, ya en `23d7476^` linea 70); RES-4 la
  masking-probe sigue acoplada a un path vivo pero degrada en ALTO.
- Poda vencida (`released_ratio 91.3 >= 90`) senalada como WARNING, no ejecutada (es del Arquitecto).
- **GOTCHA de metodo:** cada corrida del full-hook cuesta ~50s; 11 casos = ~9 min. Reutilizar UN sandbox
  con `git reset --hard HEAD` + `git clean -fd` entre casos en vez de clonar por caso, y lanzar los
  probes en background. Y para inyectar tareas hay que apagar `event_state.*` en `protocol.config.json`
  o el drift del ledger enmascara el resultado.
- **GOTCHA de commit:** `git commit -- <path>` NO funciona con ficheros untracked ("pathspec did not
  match"); hay que `git add -- <paths>` explicito ANTES y luego commitear con el mismo pathspec.

## Ultima actualizacion 2026-07-23 (23) - TASK-0290 R-A1 prune --check nombra archives malformados: OK-CLOSABLE (GO) sobre 535dd67

- Encargo `MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0290`. Residual R-A1 del veredicto de TASK-0288.
  Ancla: impl `535dd67`, clon limpio origin/main `b993acd` (codigo byte-identico en HEAD; ningun commit
  posterior toco prune_state.py ni el test). Clon limpio `/d/ccv0290`. Veredicto commit `b0ae32a` (artefacto
  `Area_comun/artifacts/Analista-TASK-0290-prune-preflight-name-archives-verdict.md` + MSG REVIEW a Arquitecto).
  SOLO PROTOCOLO, sin producto en alcance.
- **VEREDICTO: OK-CLOSABLE (GO).** El fix = +2 lineas al tuple del preflight de `run_check` (anade
  `TASK_INDEX_ARCHIVE.json` + `CLAIMS_ARCHIVE.json`, ya leidos via `read_json` cuyo retorno se descarta).
  `read_json` -> `{}` si falta el fichero, y `InvalidJsonError` (JSONDecodeError/UnicodeError) capturado en
  `main()` -> "ERROR: invalid JSON in <path>" exit 2. `assess()`/`measure()` NO leen los archives -> el read
  del preflight es un probe de decodificabilidad: no-op en valido, fallo nombrado en malformado.
- Gates clon limpio (exit code): validate 0; scan_encoding 0; `run_malformed_json_cases.py` 0 (clean +
  malformed validate/prune + rechazo semantico + full-hook C5). 7 vectores propios PASS:
  V1 archive `{` -> exit2 nombrado; V2 archive texto-no-json -> exit2 nombrado; V3 bytes UTF-8 invalidos ->
  exit2 nombrado (via UnicodeError); V4 ESCAPE archive BORRADO -> exit0 no-op (read_json {}, sin
  FileNotFoundError -> la fix NO regresiona por ausencia); V5 hot TASK_INDEX malformado -> exit2 nombrado
  (no-regresion); V6 archive valido otra forma -> exit0 no-op; baseline valido exit0 not-due 12076 tokens.
- **NO-TEATRO (before/after real):** corri el blob PRE-FIX `535dd67~1` IN-PLACE (para no romper el import
  hermano `measure_context_cost`; correrlo desde /tmp da ModuleNotFoundError falso -- GOTCHA de metodo):
  PRE-FIX con archive malformado daba exit0 "not due" SIN nombrarlo (lo tragaba); POST-FIX exit2 nombrando.
  Estado valido IDENTICO antes/despues (12076 tokens, not-due) -> cero cambio de semantica/umbrales.
- Diff: prune_state.py +2 (solo preflight), examples/ +23 (regresion). .githooks/validador/camino --apply/
  fondo intocable: SIN tocar. Residuales no-bloqueantes: (R-obs1) archive AUSENTE sigue no-op por diseno
  (vacio = estado legitimo de instancia nueva); (R-obs2) la fixture rotula su overlay-commit interno como
  TASK-0288 (fixture compartida familia malformed-JSON), cosmetico. Cierre (done-flip+release) es del Arquitecto.

## Ultima actualizacion 2026-07-23 (22) - TASK-0289 R2 acotar personal/** en full-hook: OK-CLOSABLE sobre 3090d5f/cf369d4

- Encargo `MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0289`. Residual R2 del veredicto 0287. Ancla:
  impl `3090d5f`, ancla clon-limpio `cf369d4` (ancestro de origin/main `f6bf963`, commit coord que solo rutea).
  Clon limpio `/d/ccv289`. Veredicto commit `88d7198` (artefacto
  `Area_comun/artifacts/Analista-TASK-0289-bound-fullhook-personal-verdict.md` + MSG REVIEW a Arquitecto).
  SOLO PROTOCOLO, sin producto en alcance.
- **VEREDICTO: OK-CLOSABLE (GO)** con 2 residuales no-bloqueantes (R3, R4). El fix quita el arbol `personal`
  completo del `snapshot_inventory` estatico y anade un bloque Python que lee TASK_INDEX(+ARCHIVE) del
  snapshot staged, extrae deliverables bajo `personal/` (guarda anti-traversal: parts[0]==personal, sin `..`,
  no absoluta) y materializa SOLO esos via `git checkout-index --force -- <path>`; fallo -> "could not
  materialize" exit 1. Reduccion medible: 1 of 761 tracked paths.
- Gates por exit code (clon limpio): HOOK_FULL limpio -> exit0 "1 of 761"; estado roto -> exit1 via validate
  ("...invalid; commit rejected", parse-robustez: el bloque hace except JSONDecodeError->continue y el
  validador queda de autoridad); masking-probe (rm --cached STARTUP_PROMPT.md, TASK-0084 done) -> exit1 PERO
  la RAZON cambio vs 0287: ahora checkout-index ("not in the cache") ANTES del validador; regresion exit0;
  validate/scan_encoding exit0; pin SHA-256 == validate.yml (MATCH); scripts/ diff VACIO (validador intacto).
- **A-SOBRE-RECHAZO adjudicado ACEPTABLE (no reintroduce F1)**: divergencia REAL y net-new. El hook falla-duro
  ante un deliverable personal/ AUSENTE para CUALQUIER status; el validador exige existencia SOLO para
  `REVIEWED_TASK_STATUSES = {in_review, review_approved, qa_pending, architect_review, done}`
  (validate:1048). Para status NO-revisado (cancelled/proposed/...) el hook es MAS ESTRICTO que el validador ->
  falso-rechazo. Aislado extrayendo `validate_tasks` (ghost en cancelled NO marcado; en done SI marcado) +
  probe vivo del hook sobre cancelled REQ-829CBFCE (checkout-index rechaza). OJO: para `done` NO hay
  divergencia (el validador tambien rechaza). NO existia en 0287 (git ls-files -- personal solo lista
  TRACKED, nunca falla por ausente). GOTCHA de metodo: editar TASK_INDEX.json a mano dispara la puerta B.3
  drift (esta instancia tiene event_state.enforce ON) que ENMASCARA la logica de deliverable -> hay que
  aislar `validate_tasks` para verlo.
- Por que ACEPTABLE y no NO-GO (evitar sobre-rechazo yo mismo): (1) F1 segun lo acota la tarea = falso-rechazo
  del ARBOL LIMPIO con deliverables presentes-omitidos; el arbol limpio pasa exit0. (2) severidad acotada:
  local opt-in, fail-CLOSED, NO bloquea CI (la frontera dura de CI es el validador DIRECTO en validate.yml:29,
  que tolera el mismo estado; ningun paso CI corre HOOK_FULL parcial sobre el arbol real). (3) LATENTE (unico
  deliverable personal = TASK-0084 done+presente). (4) rechazo honesto/atribuible. -> residual R3 con fix
  minimo (filtrar deliverables extraidos por REVIEWED_TASK_STATUSES, o tolerar el miss y dejar al validador de
  autoridad -filosofia del propio handoff-). R4 = el masking-case de la regresion solo asevera returncode!=0,
  no la RAZON, asi que ahora verdea por checkout-index y no prueba el camino validador/C5.
- LECCION: cuando el checker debe adjudicar "gate mas estricto que el validador", la divergencia es REAL y hay
  que probarla falsable, pero GO+residual (no NO-GO) si no rompe ningun acceptance ni la prohibicion ACOTADA;
  un NO-GO ahi seria sobre-rechazo -ironico en una tarea que trata justo de no sobre-rechazar-.

## Ultima actualizacion 2026-07-23 (21) - TASK-0288 R1 JSON gobernado malformado graceful: OK-CLOSABLE sobre 18b25da+2959622

- Encargo `MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0288`. Residual R1 del veredicto 0287. Ancla:
  impl `18b25da` (fix) + `2959622` (runner idempotente), ambos ancestros de delivery `50135f9`; HEAD
  origin/main `836d624`. Clones limpios `/d/ccv288` (gates+runner) y `/d/ccv288b` (probes adversariales).
  Veredicto commit `fec072a` (artefacto `Area_comun/artifacts/Analista-TASK-0288-graceful-malformed-json-verdict.md`
  + MSG REVIEW a Arquitecto). SOLO PROTOCOLO, sin producto en alcance.
- **VEREDICTO: OK-CLOSABLE (GO)** con 1 residual no-bloqueante R-A1. El fix mata el JSONDecodeError sin
  capturar: prune anade `InvalidJsonError` + `read_json` guardado (JSONDecodeError/UnicodeError) + preflight
  de 4 HOT (config/PROJECT_STATE/TASK_INDEX/CLAIMS) + `main` try/except -> exit 2 "ERROR: invalid JSON in
  <path>"; validate anade SOLO `if validation.errors: return validation` (+2) que corta ANTES del merge que
  tiraba el traceback (read_json_file ya grababa validation.fail via except Exception amplio).
- Probes por ENTRYPOINT real, gate por exit code: HOT malformado (TASK_INDEX/CLAIMS/PROJECT_STATE/config)
  + variantes trunc/garbage/empty/UTF-8-invalido -> validate exit!=0 Y prune exit 2, ambos NOMBRAN el
  archivo, NINGUNO imprime "Traceback". Estado limpio -> validate exit 0 (el early-return NO dispara espurio).
  JSON valido semanticamente roto -> validate sigue rechazando. C5 en el boundary: HOOK_FULL=1 con HOT
  malformado staged Y con ARCHIVE malformado staged -> ambos exit 1 "collaboration state in staged snapshot
  is invalid; commit rejected", atribuible al validador, sin traceback. Diff = +2 validate + solo manejo de
  errores en prune, sin cambio de umbral/regla; ningun otro commit toca los scripts en 18b25da..50135f9 (A3).
- **RESIDUAL R-A1 (no bloqueante, DENTRO del bar A1 que puso el Arquitecto):** prune --check sobre
  `*_ARCHIVE.json` malformado devuelve exit 0 "prune not due" SIN nombrar el archivo (los 2 archives NO
  estan en el preflight y NO se leen en el camino not-due). SIGUE graceful (sin traceback = el bar A1) y por
  analisis estatico TODA lectura de archive pasa por read_json guardado + main captura InvalidJsonError, asi
  que el camino due/apply daria exit 2 graceful; NUNCA traceback. NO es hueco C5: validate (directo y en el
  hook boundary) SI rechaza archives malformados (exit 1, nombra). Hardening opcional trivial (anadir los 2
  *_ARCHIVE.json al preflight) NO requerido para cierre. Pregunta al Arquitecto: (a) cerrar con R-A1 aceptado
  o (b) rutear el hardening a Codex antes de cerrar.
- GOTCHAS: el runner `run_malformed_json_cases.py` hace clon interno -> lento (>120s, corrio en background).
  El maker NO testea archives ni CLAIMS/PROJECT_STATE/config directamente -> los probe yo. Enforce/authoritative
  VIVO: NO toco state JSON; el flujo de veredicto Analista = solo artefacto + MSG (commit 2 rutas explicitas,
  como 0287/0266). Trailers Task-Id/Ops-Reason/Co-Authored-By.

## Ultima actualizacion 2026-07-23 (20) - TASK-0287 F1 hook full-mode inventario: OK-CLOSABLE sobre cd6bcfc

- Encargo `MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0287`. Ancla: impl `cd6bcfc`, delivery `6759fd8`,
  HEAD origin/main `144491d`. Clon limpio `/d/ccv287` @ 144491d. Veredicto commit `487beca` (artefacto
  `Area_comun/artifacts/Analista-TASK-0287-hook-fullmode-inventory-verdict.md` + MSG VERDICT a Arquitecto).
  SOLO PROTOCOLO, sin producto en alcance.
- **VEREDICTO: OK-CLOSABLE (GO)**. El fix es F1 del gate final 0265: el snapshot PARCIAL del hook full-mode
  no materializaba `personal/**` ni `HUMAN_GUIDE.md`, y el validador resuelve deliverables de archivo
  (TASK-0037->HUMAN_GUIDE.md, TASK-0084->personal/Codex/STARTUP_PROMPT.md via merge hot+ARCHIVE, validate
  linea 1049-1054) -> arbol LIMPIO rechazado en falso. cd6bcfc anade 2 lineas al inventario + comentario;
  invocacion del validador IDENTICA, validate_collaboration_state.py NO en el diff = read-set, no comportamiento.
- **Verificado por comportamiento, entrypoint real (no atajo)**: (1) POSITIVO HOOK_FULL=1
  HOOK_SNAPSHOT_MODE=partial sh .githooks/pre-commit sobre arbol limpio -> exit 0; hook pre-fix (cd6bcfc~1)
  sobre EL MISMO arbol -> exit 1 FALSO (TASK-0037/0084 'deliverable missing') = bug real + fix load-bearing.
  (2) C5 INTACTA por 4 breaks reales staged, todos exit 1: TASK_INDEX.json='{' -> rechaza por validate
  ('...invalid; commit rejected'); status mismatch JSON valido -> validate.fail GRACIOSO sin crash;
  y las DOS pruebas de ENMASCARAMIENTO clave -> git rm --cached del deliverable AHORA inventariado
  (HUMAN_GUIDE.md, personal/Codex/STARTUP_PROMPT.md) SIGUE 'deliverable missing' porque el snapshot se
  materializa desde `git ls-files` (indice staged), NO de copia estatica -> extender inventario NO traga
  borrado real. (3) regresion run_hook_fullmode_inventory_cases.py exit 0. (4) paridad CI: sha256 hook
  = pin 9068..f90f en validate.yml + nuevo step + validate full-tree intacto. Gates clon limpio exit 0.
- **Residuales NO bloqueantes**: R1 sobre JSON roto ('{') prune_state Y validate lanzan JSONDecodeError sin
  capturar en vez de validation.fail; el rechazo sigue siendo de validate (prune va por WARNING no
  bloqueante) y el Negativo D prueba mordida graciosa -> C5 intacta, sin trampa 0266; error-handling FUERA
  de alcance e identico pre-fix. R2 el snapshot parcial ahora copia todo personal/** -> latencia local del
  hook full sube (una corrida combinada llego a timeout 2min); aceptable, full es opt-in y CI clon-limpio
  es la frontera dura. Cierre (done-flip) es del Arquitecto; yo no cierro.
- LECCION viva: para probar que una extension de read-set NO enmascara, el test decisivo es el BORRADO
  STAGED del artefacto recien inventariado; si el snapshot viene de `git ls-files` el gate sigue mordiendo.
  Y ojo attribution 0266: cuando el break es JSON parse-roto varias herramientas crashean; confirmar cual
  produce el EXIT no-cero (aqui validate; prune es warning) + correr un break SEMANTICO valido-JSON para
  ver la mordida graciosa limpia.

## Ultima actualizacion 2026-07-23 (19) - TASK-0265 GATE FINAL conjunto DECISION-0103: OK-CLOSABLE sobre cd2ca57

- Encargo `MSG-...-Arquitecto-to-Analista-REVIEW-TASK-0265-gate-final` (v1) + re-route v2 (commit abad858,
  ancla EXPLICITA cd2ca57; v1 exec no arranco). Ancla batch = HEAD cd2ca57 (batch todo DONE). Clon limpio
  `C:/ccv0265`. Veredicto commit `1562e87` (artefacto
  `Area_comun/artifacts/Analista-TASK-0265-gate-final-conjunto-0103-verdict.md` + MSG VERDICT a Arquitecto).
  cd2ca57..abad858 = solo events.jsonl+snapshot.json (coord), CERO cambio de impl -> mi review en cd2ca57
  vale para v2. SIN PRODUCTO en alcance.
- **VEREDICTO: OK-CLOSABLE** para 0257..0264 + 0266 + 0286. Gates protocolo exit 0 (validate/encoding/
  neutralidad/drift CLEAN seq6137). Harness adversarial PROPIO 34 checks 0 SLIP + 5 suites maker verde.
- **6/6 pruebas PASS por comportamiento**: (a) hook rechaza estado gobernado ROJO en HOOK_FULL=1 via
  validate_collaboration_state (rompi CLAIMS.json status=bogus; partial default solo avisa exit0);
  (b) friccion autoritativa (blocked/qa_failed/changes_requested/architect_review, reject_review/fail_qa/
  assign_fix, checks_failed) + obstacles vacio/ausente -> rechaza turn_validate (diferencial poblado OK);
  (c) REPORTE friction_count>0 + obstacles vacio -> rechaza validate_mailbox; (d) grandfathering VERDE;
  (e) oferta rechazada NO se re-oferta (solo con evidencia cambiada Y declarada); (f) gate_green:false +
  obstacles vacio POST-gate -> rechaza RunLog.append (orchestrator.py:1136, entrypoint real, bool genuino).
- **Coherencia cross-unit CONFIRMADA**: C3=0259(pre-gate)+0286(post-gate) cada mitad en su entrypoint;
  gate_green NO es campo legal del turn_schema (additionalProperties:false) -> split E7 correcto; bloque
  obstacles compartido 0258==0261==0262 (4 campos+enum); 0260 gate turno0 (approval_hash sobre material
  id/acceptance/risk) <-> 0264 regla escrita en TASK_PROTOCOL.md+AGENTS.template.md.
- **HALLAZGO F1 (WARNING-real, NO bloquea el batch, ruteado follow-up)**: el inventario del snapshot PARCIAL
  del hook modo-completo (.githooks/pre-commit:63-77) OMITE deliverables fuera de sus raices -> HOOK_FULL=1
  RECHAZA en FALSO un arbol LIMPIO (working-tree validate exit0; hook full exit1 "Task TASK-0037 deliverable
  missing: HUMAN_GUIDE.md" + "TASK-0084 ... personal/Codex/STARTUP_PROMPT.md", ambos EXISTEN, ambos en
  ARCHIVE, cota=2). Falla en CERRADO; CI (validate.yml:29 arbol completo, no el snapshot) y default intactos;
  cae en E6/0268-0269 (fuera de las unidades del gate). FALSA la afirmacion E6-A "paridad partial-total
  intacta / inventario cerrado contra read-set". LECCION: el read-set de EXISTENCIA-DE-DELIVERABLES apunta
  fuera de las raices del inventario (raiz HUMAN_GUIDE.md, personal/**); un inventario derivado de imports
  NO lo cubre. Reco: anadir esas rutas al inventario o acotar el chequeo al inventario; +caso en
  test_precommit_hook (full sobre arbol limpio -> exit0).
- Residuales declarados: revert proxy best-effort (evade "backed out"/"rolled back"); sin sensor outcome
  (E7 por diseno); grandfathering por ancla (declarado en MAILBOX_REPORT_TEMPLATES.md lineas 10-12);
  `is False` no alcanzable por entrypoint real; 0260/0264 confirmados ESTRUCTURALMENTE (no end-to-end en
  este barrido). GOTCHA nuevo: total-mode del hook (HOOK_SNAPSHOT_MODE=total) copia todo el arbol -> timeout
  >2min, no lo corri (es el coste que E6-partial evita). GOTCHA loader: importlib module_from_spec necesita
  sys.modules[name]=m ANTES de exec para frozen dataclass (improvement_offers.Obstacle).

## Ultima actualizacion 2026-07-23 (18) - TASK-0286 (C3/E7 gate-red objetivo post-gate): OK-CLOSABLE sobre e7feb777

- Encargo `MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0286`. Ancla impl `e7feb777`; protocol
  HEAD `b961724`. Clon limpio `/d/ccv286`. Veredicto commit `c404b64` (artefacto
  `Area_comun/artifacts/Analista-TASK-0286-post-gate-gatered-obstacles-verdict.md` + MSG VERDICT
  a Arquitecto). SIN PRODUCTO. Unidad HERMANA de 0259 por E7: la mitad OBJETIVA del sensor C3.
- **6/6 PASS**. (1) ENTRYPOINT REAL: `validate_post_gate_obstacles(entry)` es la 1a linea de
  `RunLog.append` (runlog.py:25) ANTES del write; los 17 writes del run-log en orchestrator van por
  `runlog.append` y el UNICO `open('a')` sobre `runtime/runs/*.jsonl` esta DENTRO de append -> NO hay
  bypass. Mis payloads por el append REAL rechazan red/absent y red/empty. (2) gate_green OBJETIVO:
  orchestrator.py:1123 `gate_green=result.get('green')` de `apply_gate_and_commit`; `turn_entry` toma
  gate_green como KWARG, NO de report -> probe con `report.gate_green:True` + objetivo False sigue
  RECHAZADO (no relabel-able). Verifique que las 7 rutas de retorno de apply dan bool ESTRICTO (final
  except re-raise) -> `is False` solido en el camino real. (3) anti-teatro: green/absent ACEPTADO.
  (4) mutacion NEG-POST-GATE-RED-OBSTACLES REAL (asserta mutant!=source; quitar la llamada ->
  red/empty ACEPTADO), inventario 26/26 missing=0, test_falsification exit 0. (5) E7 documentado
  README:22-25. (6) NO toca turn_validate ni schema (diff-stat+grep+history).
- **RESIDUALES declarados NO bloqueantes**: R1 (el `is False` estricto es solido SOLO porque apply
  garantiza bool; None/0/'false' fabricados a mano son INALCANZABLES por el orchestrator real -- None
  = 'gate no corrio', semantica correcta de pre-gate/rejected/human/budget). R2 (anti-teatro: se
  exige PRESENCIA no calidad -> `obstacles=['']`/`' '`/`[{}]` pasan; coherente con criterio literal
  'vacio/ausente' y con no forzar prosa; policiar contenido invertiria anti-teatro). N1 (nit doc):
  `verification_cmd[0]` cita `run_runtime_turn_cases.py` que NO existe (history/grep vacios); los 4
  runners reales (post_gate/schema/semantic/obstacle) cubren la aceptacion y pasan exit 0.
- LECCION: la trampa unit-vs-behavior de la tanda (0259/0261/0266) NO reaparecio aqui -- el maker
  puso el guard en el append REAL, no en una funcion unit; lo confirme con payloads propios + probando
  que gate_green no es relabel-able. Gates clon limpio e7feb777 exit 0: 4 runners + inventory +
  test_falsification + validate + scan_encoding + scan_domain_neutrality; drift CLEAN seq=6112.

## Ultima actualizacion 2026-07-23 (17) - TASK-0266 (C5/E4-E5 + H1 propagacion harness): NO-GO / CHANGE-REQUIRED sobre cef1e9b

- Encargo `MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0266`. Ancla impl `cef1e9b`; protocol
  HEAD `7255daa`. Clon limpio `/d/ccv266` @ cef1e9b + sandboxes `/d/ccv266inst`, `/d/ccv266b`
  (new_instance con --source-template). Veredicto commit `a9c91e1` (artefacto
  `Area_comun/artifacts/Analista-TASK-0266-propagacion-harness-verdict.md` + MSG VERDICT). SIN PRODUCTO.
- **CONFIRMADO PASS**: E4 (`.githooks/**` en DEFAULT_ADOPTABLE_GLOBS; mi corrida del comparador reporta
  `| .githooks/pre-commit | nuevo |`; documentado README_INSTANCIACION). E5 wiring (instancia nace
  git repo con `core.hooksPath=.githooks` SIN paso manual; el hook EJECUTA -> el dead-hook de C5 SI
  esta arreglado). H1 (`commit_turn` default `verify=True`; bloquea hook rojo; `verify=False` bypass
  explicito documentado; verde pasa - probado por import directo + apply case). GUARDAS (lo decisivo):
  diff NO toca `.githooks/pre-commit`, `.githooks/commit-msg`, `protocol.config.json`,
  `protocol.config.template.json`; sin aplicacion a NOVA/instancia viva. validate+encoding+neutralidad
  +3 runners exit 0 en clon limpio.
- **BLOQUEANTE (la SLIP)**: la prueba negativa E5 `assert_broken_governed_state_is_rejected` es
  FALSE-POSITIVE. Rompe `TASK_INDEX.json` y asevera solo `returncode != 0`. El aborto NO viene de un
  gate de estado gobernado: viene de `check_commit_trailers.py` (hook commit-msg) que CRASHEA con
  JSONDecodeError al leer el TASK_INDEX roto para cargar task ids. **Falsable**: en `/d/ccv266b` rompi
  `CLAIMS.json` (que el trailer-checker NO lee) + trailer VALIDO -> `git commit` EXIT 0, estado roto
  aterriza en HEAD, validate del arbol resultante EXIT 1. Causa raiz: el hook default es modo PARCIAL
  (E6-A), solo AVISA en error de estado ("local commit continues"); el gate real de estado gobernado es
  full-mode (`HOOK_FULL=1`/`hook.full true`) o CI. Firmar GO certificaria un gate que NO dispara en
  general.
- **Fix loop (max 2 iter, luego humano; NO toca pre-commit -eso es 0257)**: (a) endurecer el test E5 en
  `examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py` para ejercer de verdad el
  gate (correr bajo HOOK_FULL=1 Y/O romper un fichero gobernado que el trailer-checker no lee, y
  asertar que quien rechaza es validate_collaboration_state, no un crash incidental); O (b) corregir el
  claim del handoff/acceptance para declarar que por defecto el hook local es parcial y NO gatea
  integridad de estado (eso es CI/full-mode). Ruteo pide al Arquitecto elegir (a) o (b) para re-juzgar.
- **LECCION (nueva, dura)**: una prueba negativa que asevera SOLO `returncode != 0` es teatro: puede
  pasar por un crash INCIDENTAL de OTRO gate (aqui el trailer-checker sobre JSON malformado), no por el
  gate que dice probar. Regla: (1) asertar QUE gate rechaza (mensaje/razon), no solo el exit; (2) probar
  la FAMILIA del criterio, no el ejemplo dado - rompi otro miembro (CLAIMS.json) y el gate no disparo;
  (3) ojo con el modo PARCIAL por defecto de los githooks (E6-A): "el hook engancha" (corre) != "el hook
  gatea estado gobernado" (solo en full-mode/CI). El wiring puede ser correcto y el gate seguir sin
  dientes por defecto.

## Ultima actualizacion 2026-07-23 (16) - TASK-0264 (C1 regla arranque escrita): GO / OK-CLOSABLE sobre a079bca

- Encargo `MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0264`. Ancla impl `a079bca`
  ("docs(TASK-0264): publish governed plan approval rule"); protocol HEAD `1b075a4`. Diff
  a079bca..HEAD de los 2 docs publicados = VACIO (lo revisado == lo canonico). Clon limpio
  `/d/ccv-0264` @ a079bca, gates por exit code. Veredicto commit `43383ab` (artefacto
  `Area_comun/artifacts/Analista-TASK-0264-c1-regla-arranque-verdict.md` + MSG VERDICT a
  Arquitecto). SIN PRODUCTO EN ALCANCE. Es la regla ESCRITA; el enforcement mecanico es TASK-0260.
- **V1 (regla en TASK_PROTOCOL.md fiel a DECISION-0103 C1) = PASS.** Seccion nueva lineas 38-65.
  Tabla con los 7 campos exactos (id, goal, acceptance, verification_cmd, required_capability, risk,
  estimate); aprobacion REGISTRADA y atribuible (event log firmado / mailbox firmado, "chat efimero
  no basta"); re-aprobacion por cambio material (unidad nueva / acceptance / risk); carve-out E1
  PRESERVADO con condiciones exactas (mismo acceptance + mismo scope + mismo risk + ref al padre).
- **V2 (espejo AGENTS.template.md sin divergencia normativa) = PASS.** Bajo "## 6. Task Lifecycle" /
  "### 6.1 Intake gate" (born-operational) -> nuevas instancias nacen con la regla. Mismo contenido.
- **V3 (regla escrita, no enforcement) = PASS.** Ambos textos declaran que el enforcement mecanico
  de turno 0 es asunto SEPARADO y no reemplaza la aprobacion humana registrada; no duplica 0260 como
  codigo ni lo contradice.
- **V4 (FYI Codex-to-Asesor) = PASS.** El commit a079bca no toca personal/ (cero ediciones en areas
  privadas); la FYI dice que cada participante actualiza solo su propio prompt/memoria privada.
- **V5 (ASCII + neutralidad) = PASS.** scan_encoding exit 0; scan_domain_neutrality exit 0. El
  contenido nuevo es ASCII puro: los 2 unicos bytes no-ASCII de TASK_PROTOCOL.md (lineas 110 em-dash,
  285 flechas) son PRE-EXISTENTES y estan FUERA de la seccion nueva. GOTCHA util: scan_encoding pasa
  exit 0 CON esos bytes presentes -> el gate tolera esos puntos previos; verificar SIEMPRE que lo
  NUEVO sea ASCII aparte del exit code global.
- **Gates clon limpio @ a079bca, todos exit 0:** validate (1 WARNING benigno: la FYI
  requires_response:false sugiere archivar -- correcto para FYI, la archiva el Arquitecto al cerrar),
  scan_encoding, scan_domain_neutrality.
- **Residuales NO bloqueantes:** R-1 cosmetico -- TASK_PROTOCOL dice "checker-requested remediation",
  AGENTS.template dice "remediation"; ambos anclan a E1 y las condiciones del carve-out son
  identicas (sin divergencia de efecto, solo se omite el calificador de origen en el espejo). R-2 --
  ningun texto reexpone la nota contextual "checkpoint de turno 0 distinto de human_checkpoint_every_k"
  (es contexto, no requisito; la temporalidad operativa si esta en ambos).
- **Cierre = OK-CLOSABLE (GO).** Ruteado al Arquitecto (done-flip + release + archivado es del
  orquestador, no mio). maker != checker preservado (impl Codex, review Analista).

## Ultima actualizacion 2026-07-23 (15) - TASK-0263 (C3-bis oferta de mejora): GO / OK-CLOSABLE sobre f97e0e1

- Encargo `MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0263`. Ancla impl `f97e0e1`
  ("feat(protocol): add deterministic improvement offers") en HEAD `3fb2c91`. Clon limpio
  `/d/ccv-0263` @ f97e0e1 (borrado al cerrar). Veredicto commit `af642e3` (artefacto
  `Area_comun/artifacts/Analista-TASK-0263-oferta-de-mejora-verdict.md` + MSG GO a Arquitecto).
  SIN PRODUCTO EN ALCANCE.
- **Vector 1 (invariante duro CERO auto-aplicacion) = PASS.** `runtime/improvement_offers.py`
  importa SOLO stdlib (argparse/hashlib/json/re/unicodedata/dataclasses/pathlib/typing); grep del
  modulo: cero subprocess/os/exec/eval/system/socket/requests, cero import de submit_intent/ledger.
  Unico efecto de escritura = `args.registry.write_text(...)` (2 llamadas, ambas a la ruta
  `--registry`). Barrido del repo: ningun otro .py importa `improvement_offers` ni lee el registro
  para aplicar; `submit_intent.py` no lo referencia (los unicos matches externos son CLAIMS.json =
  metadato de scope). Salida = oferta (texto) + registro. No hay ruta directa ni indirecta.
- **Vector 2 (root determinista) = PASS.** `root_key = " ".join(NFKC(root).casefold().split())`,
  funcion pura -> reproducible (mismo input -> mismo proposal_id). Bateria propia: SUB-fusion correcta
  (case/tab/multi-space/trim/NBSP/narrow-NBSP/combinante/fullwidth/ligadura-fi/newline -> MISMA clave);
  sin SOBRE-fusion (palabras distintas / I vs i-sin-punto turco / digitos / substring -> DISTINTAS).
  Residuales DECLARADOS (no bloqueantes, es el criterio prometido): casefold fusiona eszett->ss y
  NFKC fusiona superindices; ZWSP U+200B invisible NO colapsa (direccion fail-safe: sub-oferta,
  nunca auto-aplica de mas).
- **Vector 3 (anti-bucle) = PASS**, verificado con CLI REAL via subprocess (no por asserts del suite):
  aceptada nunca recurre; rechazada/parqueada re-oferta SOLO si `evidencia cambio Y pid en
  --new-evidence` (ambas). rechazar+identico=NO; +evidencia sin flag=NO; +evidencia con flag=SI;
  flag sin evidencia nueva=NO; parqueada=NO. Registro consultado ANTES (dict `prior`).
- **Vector 4 (ambos carriles) = PASS.** read_runtime (JSON/JSONL) + read_mailbox (REPORTE) -> un unico
  `evaluate`. Merge cross-carril: root compartido runtime(2 deliveries)+mailbox(1) -> UNA oferta con 3
  citations que incluyen prefijos `runtime:` y `mailbox:`. **Vector 5** 5 casos por comportamiento.
  **Vector 6** draft_change embebe root/resolution/what reales + "MUST"/regresion; citations
  `source#delivery:evidence`.
- **Gates clon limpio @ f97e0e1, todos exit 0:** suite (6 casos, auto_apply_routes=0),
  validate_collaboration_state, scan_encoding, scan_domain_neutrality, git diff --check.
- **GOTCHA de mi harness (no defecto del modulo):** en Git-Bash, `$T` de `mktemp -d` DENTRO de un
  literal de string Python NO recibe la conversion de ruta MSYS (queda `/tmp/...` -> Windows lo lee
  como `C:\tmp\...`), mientras que como ARGUMENTO suelto SI se convierte. Resultado: reads/writes
  del modulo (por arg) van al temp real, pero mis `python -c "...open('$T/..')"` inline leian
  `C:\tmp` vacio -> falsos FileNotFound. Fix: conducir TODO el probe dentro de UN script Python con
  tempfile + subprocess (paths Python-consistentes). Cierre (flip done + release + archivado) es del
  Arquitecto/orquestador; yo solo emito GO. PRUNE DUE 92.59>=90 senalado no corrido (es del Arquitecto).

## Ultima actualizacion 2026-07-23 (14) - TASK-0262 remediacion iter1: GO / OK-CLOSABLE sobre c7ffa91 (slip agent_id->agent cerrado, sin regresion)

- Encargo `MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0262-remediation-1`. Ancla impl `c7ffa91`
  ("docs(protocol): correct assignment candidate key") en HEAD `dfff6db`. Plantilla ESTABLE c7ffa91..HEAD
  (`git diff --stat` vacio; commits posteriores son ledger/coord). Clon limpio `D:/ccv0262b` @ `dfff6db`
  (borrado al cerrar). Veredicto commit `ed67cb0` (artefacto + MSG GO a Arquitecto). SIN PRODUCTO EN ALCANCE.
- **Fix (vector 4) CERRADO:** el hunk de la plantilla en `c7ffa91` cambia EXACTAMENTE 3 lineas -- anotacion
  `<routing_decision.explanation.candidates item agent>` + `agent: MakerA` + `agent: MakerB`. `git grep agent_id`
  sobre la plantilla = SIN MATCH (cero residual). Clave real confirmada `router.py:390` (`"agent": agent_id` --
  el identificador vive bajo la clave `agent`; el `agent_id` de la derecha es el nombre de la variable local).
- **No-regresion en los 5 vectores que pasaban:** obstacles three-way identico (el fix no toco ninguna linea de
  obstacle; validador OBSTACLE_FIELDS/RISKS lineas 79-80,613-619); re-extraje los 3 ejemplos verbatim del template
  ACTUAL a MSG reales -> validate exit 0 (solo WARNING context_refs no fatal en el de asignacion); el de asignacion
  sigue VERDE tras el cambio de clave y su MUTANTE (friction 2 + obstacles []) cae exit 1 "friction_count > 0 but
  obstacles is empty" -> camino gobernado GENUINAMENTE ejercido; R1 cerrado; ejemplos completos; neutralidad+ASCII.
- **Alcance:** SOLO la clave del candidato. Los demas archivos de `c7ffa91` (CLAIMS/PROJECT_STATE/TASK_INDEX/
  events.jsonl/snapshot/task file) son housekeeping del ledger de la entrega, no contenido de la plantilla.
- **Gates clon limpio @ dfff6db, todos exit 0:** validate_collaboration_state, run_mailbox_report_cases (17,
  ruta real `examples/mailbox_report_cases/run_mailbox_report_cases.py` -- NO en scripts/), scan_encoding,
  scan_domain_neutrality, git diff --check. Fix loop consumido 1 de max 2. Cierre (flip done + release) es del
  Arquitecto/orquestador; yo solo emito GO.
- GOTCHA commit-msg gate: `-m` multiple mete lineas en blanco entre trailers y el hook `commit trailer gate`
  rechaza (exige el bloque final Task-Id/Ops-Reason/Co-Authored-By CONTIGUO sin blancos); use `git commit -F`
  con un fichero de mensaje. PRUNE DUE 90.0>=90 senalado no corrido (es del Arquitecto).

## Ultima actualizacion 2026-07-23 (13) - TASK-0262 (C2/C4 plantillas mailbox: REPORTE entrega + reporte asignacion): NO-GO / CHANGE-REQUIRED sobre doc 5a7db87 (procedencia de candidato apunta a clave inexistente)

- Encargo `MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0262`. Ancla doc `5a7db87` en HEAD `d927993`
  (doc IDENTICO desde el impl: `git diff --stat 5a7db87 d927993 --` vacio). Clon limpio `D:/ccv0262` (borrado
  al cerrar). Veredicto commit `58c027f` (artefacto + MSG a Arquitecto). SIN PRODUCTO EN ALCANCE (doc protocolar).
- **PASA (no re-abrir), vectores 1/2/3/5/6:** (1) bloque obstacles IDENTICO a `runtime/turn_schema.json` (4 campos
  what/root_cause/resolution/recurrence_risk + enum low|medium|high, additionalProperties false; validador
  OBSTACLE_FIELDS/OBSTACLE_RISKS coinciden -> tres-via identico). (2) CENTRAL: extraje los 3 ejemplos CONCRETOS
  verbatim (regex sobre los bloques "### Complete ...", sin retipear) a MSG reales en open/ -> validate exit 0;
  y 3 MUTANTES -> exit 1: A (entrega friction 1 + obstacles []) "friction_count > 0 but obstacles is empty",
  B (recurrence_risk: catastrophic) "must be low, medium, or high", C (ASIGNACION friction 2 + obstacles [])
  -> prueba que el ejemplo de asignacion TAMBIEN fluye por validate_governed_mailbox_report y pasa por bien
  formado. (3) ancla temporal OBLIGATORIA y documentada (Common rules: date/created_at/report_schema_version 1.0;
  todos los bloques fijan report_schema_version "1.0", "do not remove it") -> el que sigue la plantilla no cae
  en la evasion por omitir las 3 anclas. (5) 3 ejemplos completos. (6) neutralidad + encoding exit 0.
- **BLOQUEANTE (vector 4, UN pointer):** la plantilla de ASIGNACION anota el bloque `candidates` con
  `agent_id: <routing_decision.explanation.candidates item agent_id>` y el ejemplo usa `agent_id:`, pero la clave
  REAL del candidato en el routing es `agent` (`runtime/router.py:390`: `{"agent": agent_id, ..., "load_score",
  "stable_hash"}`). NO existe ninguna clave `agent_id` en la estructura de candidatos del routing (grep exhaustivo:
  los unicos dict-key `agent_id` estan en eventlog/llm_turn_wrapper/protocol_replay/keygen, ajenos al routing).
  El resto de pointers SI existen (required_capability, explanation.selected, candidate_agents, filtered, policy,
  candidate load_score/stable_hash). Contradice el criterio de aceptacion "sin inventar campos nuevos del runtime"
  y el vector 4 del REVIEW ("confirma que los campos existen en el routing real"). Impacto funcional BAJO (el
  validador no inspecciona `candidates`; el canal no enrojece), pero es la REFERENCIA CANONICA -> se propaga.
- **Remediacion doc-only ruteada (a Codex via Arquitecto), max 2 iter:** alinear la procedencia a
  `routing_decision.explanation.candidates[].agent` (o mantener el nombre del campo del reporte pero anotar
  "rendered from candidate `agent`"). Los 3 ejemplos deben seguir validando verde; gates validate+encoding+
  neutralidad exit 0. Re-juicio mio del unico edit ANTES del commit de cierre; 2do NO-GO escala al humano.
- Residuales declarados no bloqueantes: R-a (los 3 ejemplos emiten WARNINGS context_refs si se colocan como MSG
  reales -- no fatal, la plantilla no necesita anadirlos); R-b (el grandfathering no-ancla=>historico=>saltado es
  diseno de 0261, FUERA; 0262 cierra R1 para los SEGUIDORES de la plantilla, que es lo que le toca).
- Leccion: cuando cada placeholder de una plantilla NOMBRA una clave exacta del runtime, cruzar CADA pointer
  contra la estructura real emitida (no solo confirmar que "hay un candidato con agente"); en el mismo bloque,
  load_score/stable_hash eran claves exactas y agent_id NO -> la inconsistencia con la propia convencion es el tell.

## Ultima actualizacion 2026-07-22 (12) - TASK-0261 (C3/C4 validate_mailbox obstacles+friccion): NO-GO / CHANGE-REQUIRED sobre impl 3e5cb84 (parser de obstacles mis-clasifica la forma YAML indentada)

- Encargo `MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0261`. Ancla impl `3e5cb84`; HEAD protocolo `88f16c2`.
  Clon limpio `D:/ccv0261` (usar `Path('D:/ccv0261')`, NO `/d/` -- Python lo resuelve como `D:\d\...`). Veredicto
  commit `28362c8` (artefacto + MSG a Arquitecto). SIN PRODUCTO EN ALCANCE (protocolo puro).
- **Puertas todas verde en clon limpio** (validate, suite 7/7 run_mailbox_report_cases, scan_encoding,
  scan_domain_neutrality, git diff --check, todas exit 0). El NO-GO NO surge de las puertas: surge de ejercitar
  la FAMILIA de los criterios (importe `validate_governed_mailbox_report`/`parse_mailbox_obstacles` reales, 32
  payloads propios + confirmacion CLI end-to-end sobre fixtures minimal_instance).
- **PASA (no re-abrir):** grandfathering (RIESGO CENTRAL) OK -- pre-adopcion en las 3 carpetas no enrojece, hub
  vivo verde (20+ REPORTE pre-adopcion en archived/, todos date<2026-07-22); opt-in por marker/fecha OK en ambos
  bordes; friction_count entero (-1/1.5/abc/ausente/007) OK; limite C4 documentado en TASK_PROTOCOL.md.
- **BLOQUEANTE (una causa, dos sintomas):** `parse_mailbox_obstacles` reconoce items de secuencia SOLO con el
  guion en COLUMNA 0 (`item_start = ^-\s+`). Una lista YAML con guion INDENTADO (`  - what:`) -- YAML valido, la
  forma natural en frontmatter, y la MISMA convencion que estos mensajes usan para `context_refs` -- rompe el
  bucle en el primer item y retorna `([], None)` SIN error (lista no vacia leida como VACIA, en silencio).
  SLIP-1 (FALSO ROJO): REPORTE post-adopcion con obstaculo completo indentado + friction_count>0 -> validador
  rojo "friction_count > 0 but obstacles is empty" (reintroduce el riesgo central para el 1er reporte gobernado
  real; reproducido 2x frontmatter y cuerpo; contradice punto 3). SLIP-2 (SILENCIOSO): obstacle malformado
  indentado + friction 0 -> PASA (evade la garantia de 4 campos; contradice punto 4 y acceptance linea 19).
  Invisibles a los 7 casos porque la suite solo usa la forma col-0.
- **Remediacion ruteada (a Codex via Arquitecto), max 2 iter:** en `parse_mailbox_obstacles` (a) aceptar
  secuencias con guion indentado a cualquier indentacion consistente y (b) CRITICO fallar ACCIONABLEMENTE cuando
  hay contenido no-blanco tras `obstacles:` que produce cero items (hoy silencioso) -- esa regla (b) sola
  convierte SLIP-1 en error corregible y caza SLIP-2; + casos indentados (frontmatter y cuerpo) en la suite.
  Re-juicio mio del arnes ANTES del commit de cierre; 2do NO-GO escala al operador.
- Residuales declarados no bloqueantes: R1 (REPORTE que omite date+created_at+marker escapa la regla entera por
  ausencia de ancla temporal); R2 (gate solo cubre type REPORTE con TASK-\d{4}; HANDOFF/TASK-EXTRACT fuera).
- Leccion (reforzada): cuando el criterio promete una LISTA ESTRUCTURADA, ejercitar las DOS indentaciones YAML
  validas (guion col-0 y guion indentado). La suite del maker solo prueba una; la otra es la que usan los
  mensajes reales (context_refs) -> el falso rojo del canal vivo es el sintoma que la unidad existe para evitar.

## Ultima actualizacion 2026-07-22 (11) - TASK-0259 remediacion iter2 (ULTIMA): NO-GO (CHANGE-REQUIRED) - nucleo conductual CERRADO pero el guardian de falsabilidad quedo ROJO (regresion)

- Encargo `MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0259-remediation-2`. Ancla impl `03f9b9a`,
  entrega `d185c1d`; HEAD/origin `83eaee0` sin drift (codigo runtime byte-identico a 03f9b9a). Clon limpio
  `D:/ccv259r` (usar `Path('D:/ccv259r')`, no `/d/`). Veredicto commit `e0dd838`. SIN PRODUCTO EN ALCANCE.
- **CERRADO (por comportamiento sobre validate_turn real, payloads schema-validos mios):** El bloqueante de
  iter1 (sensor gate-red INERTE por campos fuera-de-schema) esta resuelto. `friction_sensors` ahora lee SOLO
  campos autoritativos schema-legales: `transitions.task_status.to in {blocked,qa_failed,changes_requested,
  architect_review}` + `review_qa.event in {reject_review,fail_qa,assign_fix}` / `checks_failed`. NUNCA
  `outcome`. Verificado: MS1 blocked+obst[] RECHAZA (sin schema err); ESC1 outcome=ok DIVERGENTE + to=blocked
  sigue RECHAZANDO (grieta-1 muerta); ESC2 outcome=blocked + to=in_review ACEPTA (outcome no fuerza teatro);
  MS5 attempt_id=...-0042 primer intento ACEPTA (parse de trailing int ELIMINADO, D2 muerto); MS4 entrega sin
  friccion ACEPTA (anti-teatro). revert = proxy best-effort ETIQUETADO `revert:action-summary-proxy`. Limite
  E7 (gate-red es post-gate -> TASK-0286) declarado honesto en handoff + DECISION-0103 E7. Puntos 1-5 CLOSED.
- **BLOQUEANTE (punto 6, ROJO):** `check_falsification_contracts.py --inventory` y
  `test_falsification_contracts.py` dan exit 1 en el clon canonico; AMBOS daban exit 0 en el commit de iter1
  `da3ceb6` -> REGRESION introducida por esta entrega. Causa raiz mecanica en
  `run_runtime_turn_obstacle_cases.py`: partio los 2 contratos de turno en 5
  (STATUS/REVIEW/CHECKS/REVERT-PROXY/ATTEMPT-ID) en `FALSIFICATION_CONTRACTS` pero NO re-sincronizo las 2
  ataduras del guardian: (1) la docstring de `main()` linea 91 aun dice
  `PERMANENT_NEGATIVE: ... NEG-TURN-FRICTION-OBSTACLES` (marker stale sin contrato) y los 5 nuevos ids no
  tienen marker; (2) las strings `mutation`/`boundaries` de los 5 contratos nuevos (p.ej.
  `assert STATUS_ERROR in validate_turn(blocked_empty)`) NO aparecen literales en el test (que usa
  `turn_validate.validate_turn(..., fixture_root)` + lambdas inline). El guardian exige match por subcadena
  literal (check_falsification_contracts.py:121-125). NO es falsa alarma: el contrato retenido
  AUTHORITATIVE-DELIVERY pasa porque su marker/mutation/boundaries si estan verbatim. Handoff OMITIO los 2
  comandos que fallan de su lista de verificacion (completitud DECISION-0038).
- **Guarda:** iteracion 2 de 2 (ULTIMA) -> segundo NO-GO ESCALA AL OPERADOR (no hay iter3). Senale que el
  bloqueante es NARROW/MECANICO (re-sync de markers/boundaries) para que el Operador pese fix mecanico acotado
  + una re-juicio final mia vs tomar la escalada. NO prescribo implementacion. Pregunta ruteada al Arquitecto.
- Leccion: cuando el maker EDITA la maquinaria de falsabilidad (0283), correr SIEMPRE check_falsification_
  contracts --inventory + el test aunque no esten en verification_cmd de la tarea; el guardian ata marker<->
  contrato<->boundaries por subcadena literal, y un split de contratos rompe las 3 ataduras si no se re-sincroniza.

## Ultima actualizacion 2026-07-22 (10) - TASK-0259 remediacion iter1: NO-GO (CHANGE-REQUIRED) - el sensor de friccion gate-red es INERTE en el reporte real

- Encargo `MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0259-remediation-1`. Ancla impl `c725e9b`,
  entrega `435ab5b`; HEAD `da3ceb6`==origin/main, sin drift. Clon limpio `D:/ccv259r` (OJO: en Python de
  Windows `Path('/d/ccv259r').resolve()` da `D:\d\ccv259r`; usar `Path('D:/ccv259r')`). Veredicto commit
  `6319449`. SIN PRODUCTO EN ALCANCE.
- **CERRADO (por comportamiento sobre validate_turn completo):** (1) predicado autoritativo -- `is_delivery_turn`
  lee `transitions.task_status.to`; entrega divergente outcome=ok sin obstacles AHORA enrojece (antes []);
  (3) anti-teatro -- entrega obstacles [] sin friccion ACEPTADA. Ambos load-bearing: revertir cada fix
  enrojece la suite del maker (MUT1 predicado, MUT2 anti-teatro, MUT3 friccion -> exit1; restore exit0).
- **BLOQUEANTE -- el sensor gate-red no puede dispararse en NINGUN reporte real:** `friction_sensors` lee
  `gate_green`/`gate.green`/`reverted`/`transitions.revert`/`attempt` (top). `turn_schema.json` tiene
  `additionalProperties:false` en top-level Y en `gate` Y en `transitions` -> los 5 campos son RECHAZADOS por
  schema y `validate_turn` corta con `schema:` ANTES de evaluar friccion. Ademas `validate_turn` corre ANTES
  del gate (orchestrator.py:947 valida; apply.py corre el gate DESPUES); `gate_green`/`reverted` los produce
  el gate y se escriben en el RUN LOG (runlog.py:116-139), nunca en el reporte que friction_sensors recibe.
  Un turno blocked schema-valido con obstacles [] -> validate_turn errors=[]. C3 "gate rojo + obstacles
  vacio = FAIL" NO se realiza. La suite queda verde SOLO porque el test del maker llama
  `validate_delivery_obstacles(gate_red)` a nivel UNIDAD con `gate_green` fuera-de-schema, saltando el gate.
  Es la trampa "unidad, no comportamiento" que la instruccion mando cazar.
- **Sensores que SI llegan (schema-validos): attempt_id (retry) y actions[].summary (revert).** El retry
  SOBRE-DISPARA: `attempt_id="TASK-0259-codex-0042"` (primer intento) da falso "attempt>1" porque toma
  cualquier entero final como el numero de intento; y el path `report.get("attempt")` int esta muerto.
- **Violacion de acceptance no declarada:** acceptance prohibe inventar campos fuera de TASK-0258 y exige
  declarar en el handoff los sensores no derivables; el impl inventa 5 campos y el HANDOFF de Codex NO
  declara la no-derivabilidad de gate-red (afirma "Gate-red ... rejected" sin decir que solo contra
  entrada fuera-de-schema).
- **Fix loop:** remediacion 1 de 2. Direccion (elige el maker): restringir el sensor a senales schema-derivables
  + arreglar el over-fire de attempt_id + declarar gate-red en el handoff, O mover la friccion a un check
  POST-gate sobre la entrada del run log. El negativo de gate-red DEBE ejercerse por el entrypoint REAL que
  recibe el campo, no por el atajo de unidad. Re-juicio mio antes del cierre; 2do NO-GO escala al Operador.
- **LECCION reusable:** un guard cuyo campo lo prohibe el schema (o lo produce una fase posterior) es TEATRO
  aunque su suite este verde; siempre exigir el negativo por el entrypoint real y cruzar el campo leido contra
  `additionalProperties` del schema + el ORDEN temporal (validate vs gate). Ver [[project-state-snapshot]].

## Ultima actualizacion 2026-07-22 (9) - TASK-0259 (C3 obstacles gate): NO-GO (CHANGE-REQUIRED) - el predicado lee el campo equivocado

- Encargo `MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0259-obstacles-gate`. Primera del nucleo 0103.
  Ancla impl `fc98db7`, entrega `881ecff`; HEAD `2020c81`==origin/main, sin drift. Clon limpio `D:/ccv259`
  (ruta CORTA por el long-path de Windows), exit codes. Veredicto commit `0e04aef`. SIN PRODUCTO EN ALCANCE.
- **Los 4 casos base PASS** (verificado por comportamiento sobre validate_turn completo con el fixture del
  maker): entrega sin obstacles -> RECHAZADO; entrega obstacles vacio -> RECHAZADO; no-entrega sin obstacles
  -> ACEPTADO; entrega bien formada -> ACEPTADO. La suite del maker (obstacle/schema/semantic) + validate +
  encoding: todo exit0.
- **BLOQUEANTE - el predicado deja escapar una entrega REAL:** `is_delivery_turn(report)` lee
  `report.get("outcome") in {in_review,done}`. NUNCA lee `transitions.task_status.to`, que es la senal que
  TODO el resto de validate_turn trata como autoritativa para el MISMO evento (gate de capacidad L97,
  anti-carrera L320, apply.py). Grep: cero acople outcome<->to en esquema y validador. Money-shot:
  entrega `in_progress->in_review` que suelta el claim y cambia ficheros, con `outcome="ok"` y SIN obstacles
  -> `is_delivery_turn=False`, `validate_turn errors=[]` -> el orquestador la COMMITEA. Igual con
  outcome="blocked"/"no_op". La puerta de C3 se anula con un relabel de un campo ortogonal. DECISION-0103 C4:
  debe ser regla de validador "no es cuestion de disciplina"; vencerla eligiendo una etiqueta = disciplina.
- **El negativo permanente del maker NO cubre este vector:** mutar `is_delivery_turn` a False enrojece, lo
  que prueba que el guard PESA cuando outcome ES la senal; jamas prueba una entrega senalada por la
  transicion con outcome divergente. Necesario, no suficiente (mismo patron que 0283 (8): el test mide su
  propia sombra en el eje que el maker eligio, no en el que se escapa).
- **Alcance vs C3 (el Arquitecto invito a decirlo):** NO existe ningun sensor de friccion en el codigo
  (gate_green:false / attempt>1 / revert), que es lo que C3 y el acceptance de 0259 nombran como el nucleo
  del carril runtime -> un turno de NO-entrega con friccion real (blocked tras gate rojo) no obliga a nada;
  y toda entrega SIN friccion es forzada a narrar -> el teatro "sin problemas" que C3 prohibe ("lista vacia
  es respuesta legitima"). El GO del Arquitecto acoto la intake de "sensores de friccion" a "entrega/
  no-entrega"; lo registro como divergencia, la decision de alcance es suya.
- **Residual senalado:** el `verification_cmd` de la tarea cita `run_runtime_turn_cases.py` que NO existe
  (los runners reales son `run_runtime_turn_{schema,semantic,obstacle}_cases.py`). Drift de DoR, no bloqueante.
- **Fix loop:** remediacion 1 de 2 a Codex. Bloqueo = leer la transicion (no el outcome) + negativo de
  entrega-via-transicion en el runner. Re-juicio mio antes del cierre; max 2 iter.
- LECCION reforzada: cuando una guarda condicional decide "es entrega?/hubo friccion?", atacar SIEMPRE la
  senal que lee vs la senal autoritativa del sistema. Aqui dos campos independientes (outcome libre vs
  transitions.task_status.to) que nadie acopla: el guard leyo el barato. Construir la entrega real por la
  transicion y darle el outcome "inocente" es el money-shot.

## Ultima actualizacion 2026-07-22 (8) - TASK-0283 CIERRE iter3: NO-GO (CHANGE-REQUIRED) - escape NUEVO por placement

- Encargo `MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0283-iter3-cierre`. Re-juicio de CIERRE con
  acceptance REFINADO: el Arquitecto retiro "detectar cualquier negativo sin declarar" por INDECIDIBLE y
  pidio cerrar lo cerrable (glob comprensivo=caso C, marcador load-bearing, limite ESCRITO, regresion).
  Ancla commit `8b61b05` (== el de la instruccion), HEAD `d80b774` (== origin/main); los 3 commits
  posteriores NO tocan los scripts del guardian (diff-stat vacio). Clon limpio `/d/c283i3`, exit codes.
- **Credito verificado:** glob paso a `rglob("*.py")` sobre examples/ Y scripts/. **A1 (caso C, eje
  fichero) CERRADO:** negativo marcado sin contrato en subdir profundo + nombre no estandar bajo AMBOS
  arboles -> exit1, `permanent_negatives=17 missing=2`, ambos listados. **A3** marcador load-bearing
  (quitarlo -> stale-loud, exit1). **A4** degradacion de contrato declarado -> exit1 mensaje exacto.
- **BLOQUEANTE (escape NUEVO, distinto de C) - PLACEMENT:** `permanent_negatives()` y `function_source()`
  iteran solo `tree.body` (nivel de modulo). Verificado por comportamiento:
  - A2a) negativo marcado como METODO DE CLASE -> exit0, 15/15/0. INVISIBLE.
  - A2b) negativo marcado como FUNCION ANIDADA -> exit0, 15/15/0. INVISIBLE.
- **Por que es bloqueante y no el limite retirado:** el caso retirado es el negativo SIN senal (marker
  ausente = indecidible). Aqui el marcador `PERMANENT_NEGATIVE:` ESTA presente y el walk somero lo
  descarta = bug de descubrimiento acotado, en el nucleo DECIDIBLE que el acceptance eligio cerrar.
  Rompe la clausula #2 (marker necesario pero NO suficiente; la colocacion top-level tampoco esta
  escrita -grep: no hay "top-level" en la convencion-). La mitigacion documentada (revision/CI) NO lo
  atrapa: el revisor VE el marcador y asume cobertura. Doble falso-seguro. El export `new_instance.py`
  lo propaga a suites basadas en clase (unittest/pytest), el idioma dominante.
- **Bucle:** remediacion 1 de 2. F1 (ast.walk en ambos) o F2 (fail-closed: escanear fuente por
  `PERMANENT_NEGATIVE:` y errar si un marcador presente no fue descubierto + escribir colocacion en la
  doc). Self-test debe ganar 2 casos (metodo Y anidado -> rojo). Re-juicio mio antes del commit de cierre.
- LECCION: cuando "completitud" se retira por indecidible, la frontera decidible que queda tiene su
  PROPIO borde -- probar el eje que el maker NO anticipo (aqui: placement intra-fichero, no nombre de
  fichero). Un marcador PRESENTE-pero-invisible es peor que uno ausente: engana al inventario Y al revisor.
- Higiene: trailers en UN parrafo, ASCII limpio (0 bytes>127 en ambos ficheros), pathspec explicito en el
  commit, validate+encoding exit0 antes de commitear. PRUNE DUE 95.35>=90 senalado, NO corrido (es del
  Arquitecto; yo no muto estado). SIN PRODUCTO EN ALCANCE respetado.

## Ultima actualizacion 2026-07-22 (7) - TASK-0283 RE-JUICIO denominador independiente: NO-GO (CHANGE-REQUIRED)

- Encargo `MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0283-denominador-rejuicio`. Re-juicio de
  la remediacion de mi bloqueante iter1 (Q3). Ancla commit `2a52e0c`, HEAD `c1b17bc` (== origin/main,
  sin drift; los 3 commits posteriores no tocan scripts/examples). Clon limpio `/d/c283`, exit codes.
- **Que cambio el maker (credito, verificado):** `check_falsification_contracts.py` ahora descubre el
  universo de negativos por AST via docstring marker `PERMANENT_NEGATIVE:` (fn `permanent_negatives`),
  INDEPENDIENTE de `FALSIFICATION_CONTRACTS`; `missing = existing_ids - declared_ids` es una RESTA
  computada, ya no el literal 0. Vector A (negativo MARCADO sin contrato) -> exit1 `permanent_negatives=15
  declared=14 missing=1`. Q1a/Q4 (degradacion de contrato declarado) siguen ROJO. Cerro mi Q3 iter1
  TAL COMO lo redacte.
- **Bloqueante esta iteracion (la evasion del descubridor que pidio el Arquitecto en el punto 2):** el
  universo es auto-declarado DOS veces (marker + fichero `run_*.py`). Verificado por comportamiento:
  - B) negativo permanente REAL sin marker (`assert "reset --hard" not in output`) -> exit0, 14/14
    missing=0. INVISIBLE. (Es mi Q3 iter1 re-inyectado sin marker: la sombra sigue colandose, ahora
    omitiendo tambien el marker.)
  - C) negativo REAL con marker correcto pero en `examples/shadow_cases/case_shadow.py` (no matchea el
    glob) -> exit0, 14/14. INVISIBLE por nombre de fichero.
  - Corroboracion viva: `attestation_negative_cases/run_attestation_negative_cases.py` (mutadores
    mutate_payload/delete_event/insert_event/reorder_events/unregistered_key/cross_attribution =
    negativos reales) glob-reachable, CERO markers, no entre los 14 -> `missing=0` miente a nivel suite.
    Choca con acceptance #3 clausula 2 ("sin dejar el resto como pendiente indefinido").
- **Veredicto: CHANGE-REQUIRED (NO-GO). Iteracion 2 de 2 -> tope alcanzado, escalo al operador la
  DECISION DE ALCANCE.** Artifact `Area_comun/artifacts/Analista-TASK-0283-denominador-rejuicio-verdict.md`,
  msg `MSG-20260722-Analista-to-Arquitecto-REVIEW-TASK-0283-denominador-verdict.md`, commit **fae8e02**
  (push c1b17bc..fae8e02). Por que escalo y no reboto: un denominador 100% independiente del autor es
  en el limite indecidible (mi propia remediacion iter1 tambien era declaration-based); definir el
  universo es decision del operador. Dos direcciones (basta una): R1 fail-closed (toda fn con asercion-
  negativa en runners exige marker+contrato o waiver explicito + ampliar glob) / R2 (aceptar conjunto
  marcado como DoD y enrolar/listar los negativos reales existentes). Prune vencido 94.59>=90 senalado,
  no corrido (checker; mailbox_archive/prune es del orquestador). SIN PRODUCTO EN ALCANCE.
- LECCION: cuando un maker cierra tu bloqueante moviendo la auto-declaracion una capa arriba
  (contrato -> marker), el agujero se conserva: prueba SIEMPRE la evasion del nuevo denominador
  (omitir el marker, esconder en otro fichero), no solo el caso que el maker instrumento. El "N/N"
  sigue siendo auto-satisfecho si el N lo elige el autor. Y un denominador declaration-based tiene un
  piso indecidible -> el cierre final es decision de alcance del operador, no rebote infinito.

## Ultima actualizacion 2026-07-22 (6) - TASK-0283 el guardian del guardian: NO-GO (CHANGE-REQUIRED)

- Encargo `MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0283-falsabilidad`. Unidad = mecanizar
  lo que cace a mano en 0284/0274: cada negativo permanente declara la mutacion que lo mata y una
  comprobacion (`check_falsification_contracts.py --inventory` + `test_falsification_contracts.py`)
  la exige. Maker reporto 14/14. Ancla commit `7afb122`, HEAD `aeadb07`.
- **Estructura real:** el checker es un validador de DECLARACION por SUBCADENA: itera
  `FALSIFICATION_CONTRACTS` y verifica que la `mutation` y cada `boundary` aparezcan textualmente
  en la funcion `exercised_by`. NO corre las mutaciones. El que SI aplica mutaciones y exige rojo
  es el RUNNER (run_mailbox_retry_cases.py: bloques `survivors=[...]; assert not survivors`).
- **Verificado por comportamiento en clon limpio `/d/ccv0283` (checkout 7afb122), mis propios blancos:**
  - Q1a PASS: borre frontera REAL `assert mutant_output == "live"` (retry-utf8-residue-path) -> checker
    exit 1 "assertion boundary not found". Tiene dientes contra degradacion de contrato declarado.
  - Q4 PASS: borre UNA de dos fronteras de protocol-replay-drift-exit (R1 de 0280) -> exit 1. Detecta.
  - **Q3 BLOQUEANTE:** inyecte un negativo permanente NUEVO real (`run_shadow_negative_no_contract`,
    `assert "reset --hard" not in ...`) SIN contrato -> inventario siguio VERDE 14/14 `missing=0`.
    El test-sombra se cuela. El checker no tiene NINGUNA via de codigo para enumerar negativos que
    existen; solo valida los declarados. Choca con acceptance #3 ("cuales tienen ... y **cuales no**")
    y con la pregunta literal del REVIEW.
  - Q2 (raiz mecanica): `missing=0` es LITERAL en el print; `permanent_negatives==declared==len(contracts)`
    por construccion -> `missing` no puede ser !=0 jamas. El "14/14" es auto-satisfecho.
  - R-Q1b (residual menor): substring, no liveness. Relajacion que conserva la cadena declarada pero
    la vuelve vacua (`assert True or (...)`) -> exit 0, no la caza el inventario. Diferible si cierra Q3.
- **Veredicto: CHANGE-REQUIRED (NO-GO).** Artifact `Area_comun/artifacts/Analista-TASK-0283-falsabilidad-verdict.md`,
  msg `MSG-20260722-Analista-to-Arquitecto-VERDICT-TASK-0283-falsabilidad.md`, commit **4925de5**
  (push aeadb07..4925de5). Remediacion pedida: denominador INDEPENDIENTE (enumerar universo de
  negativos por convencion comprobable, `missing = existentes - declarados`, rojo si >0) + self-test
  con caso negativo-no-declarado->ROJO + espejo new_instance.py + CI. Re-juicio mio antes del cierre;
  max 2 iteraciones. NO cierro (checker); done-flip/release es del orquestador. NOTA: prune vencido
  (released_ratio 93.33>=90) -- lo senalo al Arquitecto, no lo corro yo.
- LECCION: un guardian de falsabilidad puede tener dientes en UNA direccion (degradacion de lo
  declarado) y ninguno en la otra (entrada de lo no declarado). El "N/N" sin denominador
  independiente es la misma sombra una capa mas arriba. Probar SIEMPRE el ingreso, no solo la erosion.

## Ultima actualizacion 2026-07-22 (5) - TASK-0274 RE-JUICIO del negativo del flag: GO (OK-CLOSABLE)

- Encargo `MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0274-flag-rejuicio`. Re-juicio de la
  remediacion TEST-ONLY de mi F-0274-01. Codigo del gate NO cambio (blob d7bd4d3 byte-identico en
  6f2084f/77afe05/0831701/7decc08); solo se le dio DIENTES al negativo del flag desconocido.
- Fix (commit 77afe05, entrega 0831701): +3 lineas en `case_cli_is_a_real_aborting_gate`; anade
  `isolated_unknown = run(command + ["--bogus-flag"])` con `assert returncode != 0`, donde
  `command` YA incluye `--check-drift --root <root>`. Es EXACTAMENTE el fix que declare: aisla el
  rechazo del flag desconocido para que el guardia de "flag requerido" no pueda enmascararlo.
- **Verificado por comportamiento en clon limpio `/d/ccv0274b` (checkout 0831701):** suite 9/9
  exit 0; validate/encoding/neutralidad exit 0. Disciplina de mutantes sobre PRODUCCION:
  MutA (`_drift_exit_code`->return 0) ROJO, MutB (veredicto invertido) ROJO, **MutC
  (`parse_args`->`parse_known_args`) AHORA ROJO** -- el caso que falla es exactamente
  `case_cli_is_a_real_aborting_gate` y el error es `PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=1`
  (la combinacion aislada ignoro el flag, corrio drift limpio, salio 0, asercion !=0 fallo). Los
  TRES negativos del gate tienen dientes. Produccion `--check-drift --root <root> --bogus-flag`
  sale 2 (unrecognized arguments): la asercion pasa por la razon correcta.
- **Veredicto: OK-CLOSABLE (GO).** Artifact `Area_comun/artifacts/Analista-TASK-0274-flag-rejuicio-verdict.md`,
  msg `MSG-20260722-Analista-to-Arquitecto-REVIEW-TASK-0274-flag-GO.md`, commit **0c9f089** (push
  7decc08..0c9f089). Bucle de fix cerro en iteracion 1 (de 2). Cierre (done-flip + release de la
  claim del maker) corresponde al Arquitecto/orquestador, no al checker -- yo no cierro. Residuales
  R1 (bloque mutation-control inline decorativo)/R2 (--root=cwd)/R3 (coordination-tier CLEAN) no
  bloqueantes, arrastrados. LECCION reforzada: un negativo debe enrojecer al revertir SU arreglo,
  no el de al lado; aislar el modo de fallo probado es lo que le da dientes.

## Ultima actualizacion 2026-07-22 (4) - TASK-0274 gate de drift CLI CHANGE-REQUIRED sobre 6f2084f

- Encargo `MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0274-drift-cli`. El comando que los
  tres citabamos como gate de deriva (`python runtime/protocol_replay.py --check-drift`) era
  VACUO: sin entrypoint CLI, salia 0 con cualquier flag (hallazgo F-0272R1-05). Esta unidad le
  puso un `main()`/argparse real sobre `protocol_state_drift()`.
- Codigo bajo prueba: blob de `runtime/protocol_replay.py` byte-identico en 2aa5552/6f2084f/04ea079
  (d7bd4d3), suite identica en 2aa5552/04ea079 (329ce79). Clon limpio `D:/ccv0274`, checkout 6f2084f.
- **6/6 vectores PASS por comportamiento** (probados por payload en clon limpio): V1 limpio exit 0
  (verdict=CLEAN up_to_seq=5696) / deriva exit 1; `_drift_exit_code` fail-closed (`1 if has_drift is
  not False else 0`, None->1). V2 deriva fabricada (status mutado en hot TASK_INDEX) exit 1
  verdict=DRIFT + path, restaurar exit 0. V3 --bogus-flag exit 2, --check-drift --bogus-flag exit 2,
  --check-drfit exit 2, sin flag exit 2. V4 up_to_seq impreso. V5 README/HANDOFF_TEMPLATE/RUNBOOK con
  contrato exit-code (historicos = registros). V6 instancia runtime generada hereda el CLI real
  (--bogus-flag exit 2, __main__ real). Puertas: suite 9/9, validate/encoding/neutralidad exit 0.
- **Disciplina de mutantes = el nucleo del veredicto.** MutA (`_drift_exit_code`->return 0) y MutB
  (veredicto invertido): suite ROJA -> negativos de deriva/veredicto CON dientes. **MutC
  (`parse_args`->`parse_known_args`): suite VERDE** -> el negativo del flag desconocido NO enrojece.
- **Bloqueante F-0274-01 (unico):** la asercion del flag desconocido corre `--bogus-flag` SIN
  `--check-drift`; bajo parse_known_args el flag se ignora y falta el requerido -> parser.error exit 2
  -> la asercion `!= 0` pasa igual. Confunde "flag requerido ausente" con "flag desconocido
  rechazado" y NO puede fallar si se afloja la estrictez. Es el anti-patron de 0274 (test que no
  puede fallar) una capa abajo. Aclaracion: reventar el fix COMPLETO (borrar main()) SI enrojece;
  el hueco es especifico del aflojamiento con el guardia de flag-requerido intacto.
- **Veredicto: CHANGE-REQUIRED** (`Analista-TASK-0274-drift-cli-verdict.md`, commit `4ce8b2e`,
  pusheado, canonical verde 4ce8b2e). Fix esperado: anadir a `case_cli_is_a_real_aborting_gate` una
  corrida que AISLE el rechazo (`--check-drift --bogus-flag` o `--check-drfit`, assert !=0). Re-juicio
  con MutC como criterio de dientes; maximo 2 iteraciones antes de escalar al operador.
- Residuales: R1 el lambda `inverted` inline del test es decorativo (verifica un lambda local, no
  produccion); R2 `--root` default cwd; R3 coordination-tier computa drift real, no es falso verde.
- Leccion transversal: en un gate cuyo test tambien tiene negativos, correr el mutante que afloja
  CADA guarda por separado; un negativo puede pasar por el motivo EQUIVOCADO (confound de argparse
  required-flag vs unknown-flag).

## Ultima actualizacion 2026-07-22 (3) - TASK-0279 gate de trailers en commit-msg GO/OK-CLOSABLE sobre 15fe9c8

- Encargo `MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0279-commit-msg`. El gate de trailers
  paso del validador post-hoc (que solo enrojece al peer siguiente) a `.githooks/commit-msg`, que
  recibe el mensaje finalizado y aborta antes de crear el commit. Checker nuevo:
  `scripts/check_commit_trailers.py`; suite `scripts/test_commit_msg_hook.py`.
- Codigo bajo prueba IDENTICO byte-a-byte de `15fe9c8` (feat, entrega `56f9750`) hasta HEAD
  `77a15b1`; `56f9750..HEAD` solo mailbox+ledger. Clon limpio `D:/ccv`, checkout 77a15b1.
- **La propiedad que importa (no "un checker mas"):** el gate debe rechazar EXACTAMENTE lo que
  `validate_commit_trailers` (en validate_collaboration_state.py) rechazaria, para abortar en el
  commit lo que si no enrojece al peer. Diferencial linea a linea: mismo GOVERNED, mismos regex,
  misma logica de bloque final + known=INDEX+ARCHIVE. Busque el sentido PELIGROSO (gate mas laxo
  -> pasa el commit pero enrojece al validador): **NO EXISTE**. Las 3 divergencias son gate-mas-
  ESTRICTO (clave con-letra-inicial, un-solo Ops-Reason/Task-Id, linea de espacios) -> a lo sumo
  falso positivo patologico que `git commit -m` no dispara. La promesa central se sostiene.
- **Veredicto: GO / OK-CLOSABLE** (`Analista-TASK-0279-commit-msg-verdict.md`, commit `7908874`,
  pusheado, canonical verde). Por comportamiento con commits reales:
  - Cuatro clases abortan: blank-line en bloque final, Ops-Reason 121>120 (frontera 120 ACEPTA),
    ausencia de Task-Id y Task-Id:none sin Ops-Reason, fix/revert/hotfix x tres separadores sin
    Fixes-Task (9/9). Commit valido pasa.
  - Podada REAL: TASK-0001 (solo en TASK_INDEX_ARCHIVE) ACEPTA; TASK-9999 RECHAZA.
  - Mutacion DOBLE (criterio 3): al desactivar cada guarda su negativo se voltea a aceptado
    (guarda load-bearing) Y la suite entregada pasa de exit 0 a exit 1 (AssertionError) por cada
    mutante. No es verde vacio.
  - Alcance: solo Area_comun/runtime/scripts/protocol.config.json; personal/examples/.githooks
    pasan sin trailer (coincide con GOVERNED_TRAILER_PATHS del validador). Coste ~0.054s/llamada.
  - Escape E3 `git config --unset core.hooksPath` (rearm `... core.hooksPath .githooks`) operativo.
- **Deuda de fixture PREEXISTENTE confirmada, NO contra 0279:** el runner
  `run_runtime_instantiation_cases.py` falla en HEAD (ledger_head en prune_state escafoldado +
  case_coordination); corri el runner en el padre `6197e10` (sin codigo 0279) y falla en los
  MISMOS dos casos. 0279 solo agrega 2 entradas a GATE_SCRIPTS sin regresionar. Ofreci registrarla
  como unidad propia si el Arquitecto quiere (fix import ledger_head).
- DOGFOOD: mi propio commit de veredicto (7908874) toca Area_comun/ (gobernada) y paso el gate que
  revisaba -- Task-Id + Co-Authored-By en un solo bloque final sin blank line (el F-0240-01 que me
  ha mordido 4x). El gate acepto el trailer bien formado. Confirmacion viva.
- Gates: validate/encoding/neutrality exit 0, drift 0 (protocol_replay exit 0).

## Ultima actualizacion 2026-07-22 (2) - TASK-0284 banco RE-JUICIO GO/OK-CLOSABLE sobre 947c6f5

- Encargo `MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0284-banco-rejuicio`. Re-juicio del
  banco TEST-ONLY sobre `947c6f5` (HEAD protocolo `748c5e7`). **El codigo del harness NO cambio**:
  `git diff --stat 04ec9d1 947c6f5 -- scripts/harness/` VACIO. Ya certifique ese codigo correcto
  por comportamiento (F-0281-07/08 cerrados en el pregate); esto era solo endurecer el banco.
- Contexto: mi pregate (`Analista-TASK-0284-pregate-verdict.md`, commit 8a716f0) fue
  CHANGE-REQUIRED por DOS SLIPS cabecera -- `deleted_first_seen_removed` y `sequential_pipe_drain`
  MEDIAN SU SOMBRA (solo string-contract, ningun test de comportamiento) -- mas una SLIP menor de
  vejez de claims. Remediacion test-only movio esos TRES a negativos de BUCLE REAL.
- **Veredicto: GO / OK-CLOSABLE** (`Analista-TASK-0284-banco-rejuicio-verdict.md`, commit
  `d1910a3`, pusheado, canonical verde). Clon limpio `D:/ccv0284b`. Re-conduje cada mutacion yo
  mismo con instrumentacion (no confie en la asercion interna del test):
  - **Negativo 1 (borrado):** REAL -> R1 `residue_live` -> R2 `staged_residue_aborted` ->
    `EXEC_START`. MUTANTE `first-seen->$false` -> eterno `live` -> `defer_terminal
    reason=worktree_residue_live` (F-0281-07 renacido). Muerto por conducta.
  - **Negativo 2 (>64KB stderr):** concurrente exit 0 wall **0.47s** sin lock. MUTANTE secuencial
    (ReadToEnd sync) = **DEADLOCK REAL**: le di 45s (15x el tope de 3s del banco) y sigue colgado,
    lock huerfano. Cierra el R1 de mi pregate (antes se cazaba por choque de TIPO, no por cuelgue).
  - **Negativo 3 (claim vencida):** REAL vencida -> `none`, fresca externa -> `active_external_claim`
    (base: SI detecta, `none` significativo), propia -> `none`. MUTANTE `$expires -gt $now->$true`
    -> vencida contada `active_external_claim`. Muerto por conducta.
- String-contract `run_pregate_contract_mutants` RETENIDO como EXTRA (literales cabecera presentes)
  guardando solo los dos mutantes que ademas se cazan por comportamiento (terminal_defer,
  dirty_forensics). Avale esto en el pregate: extra, no guardian unico. Sin regresion.
- Gates sobre 947c6f5: validate/encoding/neutrality exit 0, `run_mailbox_retry_cases` exit 0,
  drift False. Residuos NO bloqueantes: R1 el mutante mata la LINEA declarada (limite del mutation
  testing por linea); R2 vejez serializada fail-closed; R3 `context_ref` handoffs/ inexistente
  (el handoff se archivo como MSG) -- anomalia de traza DECISION-0018.
- LECCION reforzada (patron 0283): un negativo que sobrevive a su propia mutacion mide su sombra.
  El banco cerro cuando cada positivo alcanza su estado por el camino declarado Y el mutante
  enrojece por la CONDUCTA y la RAZON declarada, verificado por mi con payloads propios, no por el
  nombre ni la asercion del test. La prueba del deadlock real: darle 15x el tope y confirmar que
  SIGUE colgado (distingue deadlock de timeout-por-lentitud).

## Ultima actualizacion 2026-07-22 (1) - TASK-0281 iter3 NO-GO sobre 8c70dbb (dos paradas nuevas)

- Review adversarial de `8c70dbb` (HEAD `fa98595`) en CLON LIMPIO `D:/ccv0281c`, con contraste
  contra el PADRE `7b708f8` en `D:/ccv0281p` y mutantes en `D:/ccv0281m` / `D:/ccv0281f`.
  Cuatro gates exit 0 sobre el commit juzgado; drift 0 (up_to_seq 5582). Veredicto NO-GO +
  NO REDESPLEGAR. Artifact: `Area_comun/artifacts/Analista-TASK-0281-iter3-utf8-ambiguity-verdict.md`.
  Commit `a63485c`. Escalado al operador por tercera vez (tope de 2 iteraciones agotado en iter2).
- **Lo que el maker SI cerro**: el decodificador UTF-8 estricto en el proceso hijo funciona
  (no-ASCII fresco -> `live`; no-ASCII RANCIO -> `aborted`), y el probe de la suite salio del
  sandbox (murio la auto-contaminacion E1/E6 de iter2).
- **F-0281-07 (bloqueante, regresion nueva): la regla de "lado seguro" es ABSORBENTE.**
  `if (-not (Test-Path $full)) { return "live" }` -- la unica valvula de salida del `live` es que
  el mtime envejezca, y una ruta BORRADA no tiene mtime. Cualquier borrado (indexado o no) deja
  el pre-gate en `live` para siempre. Runner completo con `-AbortedResidueMinutes 0` (el ajuste
  MAS permisivo): `EXEC_START=0, attempts=0, defers=5, exhausted=false`, mensaje nunca consumido.
  El padre `7b708f8` con el mismo fixture da `EXEC_START=1`.
- **F-0281-08 (bloqueante, regresion nueva): deadlock de tuberias.** El lector nuevo hace
  `StandardOutput.ReadToEnd()` y DESPUES `StandardError.ReadToEnd()`, sin timeout ni en la lectura
  ni en `WaitForExit()`. Con 32664 bytes de stderr y stdout vacio (git exit 0) el lector de
  `8c70dbb` se cuelga >60 s; el del padre termina. Cuelga en la linea 786, DENTRO del `try` que en
  la 785 ya escribio `$LockPath` -> cron parado CON el lock tomado, sin log ni defer.
- **F-0281-06 sigue abierto en su mitad util**: revirtiendo ENTERO el decodificador a cp850 en el
  runner real, `run_mailbox_retry_cases.py` sigue en **exit 0**. Revirtiendo solo el fail-safe, da
  exit 1. La asercion no-ASCII es sobre fichero FRESCO y `live` es tambien lo que devuelve el
  fail-safe: los dos mundos dan la misma respuesta.

### Tecnicas nuevas (REUTILIZABLES)

1. **Ablacion por mitades sobre el fichero REAL, corriendo la suite entera.** Un mutante COMBINADO
   solo prueba que la conjuncion hace falta. Para saber si cada mitad esta cubierta hay que
   revertir UNA sola cosa a la vez en un clon separado y mirar el exit code de la suite. Asi cace
   que se puede borrar el arreglo que da titulo al commit y el gate sigue verde.
2. **El caso RANCIO es el negativo no vacuo.** Cuando el fix y el fail-safe devuelven el MISMO
   valor en el caso fresco, la asercion no distingue nada. El caso envejecido rompe el empate:
   `aborted` solo es alcanzable si la ruta se resolvio de verdad.
3. **Contraste sistematico contra el COMMIT PADRE, mismo script y mismo fixture.** Es lo que
   convierte "esto se comporta mal" en "esta iteracion lo rompio". Clonar el padre a `D:/ccv...p`
   y parametrizar el ROOT del probe.
4. **Buscar estados ABSORBENTES.** Ante cualquier regla nueva de "ante la duda, lado seguro",
   preguntar SIEMPRE: cual es la unica salida de ese estado, y existe algun estado del sistema en
   el que esa salida sea inalcanzable? (aqui: salida = envejecer el mtime; estado sin mtime = ruta
   borrada). El operador y el Arquitecto valoran esta pregunta mas que el fail-open.
5. **Ejecutar el gate con el knob MAS permisivo** (`-AbortedResidueMinutes 0`). Si aun asi bloquea,
   no queda excusa de configuracion.
6. **Deadlock de dos tuberias**: ante cualquier `ProcessStartInfo` con las dos redirecciones,
   probar un caso que inunde stderr (aqui: 120 directorios con ruta >260 y sin `core.longpaths`,
   git avisa uno por directorio). Medir con `Start-Job` + `Wait-Job -Timeout`, nunca en foreground.
7. **Residuo real invisible (R6)**: ruta demasiado larga -> git avisa por stderr, sale **exit 0** y
   NO la enumera; el pre-gate devuelve `none` y arranca. Un exit 0 de git no significa "he visto
   todo el arbol".

## Ultima actualizacion 2026-07-20 (6) - TASK-0277 veredicto OK-CLOSABLE (1 condicion, 2 residuales)
- Review adversarial de a899041 / HEAD 5414838 en CLON LIMPIO D:/ccv0277. Todos los gates
  exit 0; protocol_state_drift() has_drift=false up_to_seq 5385 (sin citar --check-drift,
  TASK-0274 abierta). Artifact: Area_comun/artifacts/Analista-TASK-0277-trazabilidad-verdict.md.
- Fidelidad verificada por recomputo PROPIO desde el log crudo: 0267 campo a campo (cadena
  status completa hasta done seq 5066); 6/32 claims muestreadas iguales. Semantica release
  del engine = SOLO flip de status (protocol_replay.py:821-826), sin released_at/updated_at.
  Recuento independiente: 202 tasks / 1381 claims nombradas por podas, cero ausentes;
  archivo 298/1620. Historia intacta: events.jsonl +4/-0 en todo el rango (gobernanza 0277).
- **F1 (condicion de cierre): relajacion NO declarada y PORTANTE en validate_claims** --
  a899041 mueve la validacion de selectores de scope bajo status==active; el validador
  PRE-fix da exit 1 sobre el estado nuevo por las 2 claims restauradas en minusculas
  (claim-arq-d0103-registro / claim-arq-mailbox-hygiene). Tecnica de deteccion REUTILIZABLE:
  correr el validador del commit padre contra el estado nuevo (git show parent:script >
  scripts/_old.py; OJO: colocarlo EN scripts/, en la raiz el root-detection apunta a D:\).
- **R1: prune_archive_drift es proyeccion SUBSET sobre ids nombrados por eventos** -- filas
  no-nombradas (17 legacy) invisibles al drift POR DISENO; su status queda anclado por el
  cruce fila-vs-fichero (tamper status -> rojo) pero priority/owner/etc NO (lo probe: exit 0).
  Unidad fabricada completa (id nuevo + fichero + fila) pasa todos los gates. Endurecimiento
  propuesto: allowlist de las 17. PARA MIS GATES FUTUROS: drift verde en archivos != archivo
  fiel para filas no respaldadas por eventos.
- Matriz de ataque que aguanto: borrar fila task/claim archivada -> validate 1 + drift true
  (doble via, agujero original cerrado); tamper fila nombrada -> ambos rojos; fila sin
  fichero -> rojo; duplicado hot/archive -> rojo; fichero sin fila -> rojo (chequeo nuevo);
  verify_archived_entries revienta en missing Y changed (unit directo).
- R2 (DECISION-0018, preexistente): TODOS los commits recientes del arbol compartido van
  git-autorados "Analista <analista@local>" (config local compartida), incluidos los de
  Codex/Arquitecto; la atribucion real vive solo en el event log firmado. Reportado al
  Arquitecto en el MSG del veredicto.
- Contexto commit: arbol con lote de higiene del Arquitecto SIN commitear (rojo local por
  drift CLAIMS.slim.json; canonico verde) y PARKED ~9min -> ventana segura, commit por
  pathspec explicito solo de mis rutas. QUEDA PENDIENTE en open/ el REVIEW de TASK-0278
  (token-epilogo) para el proximo disparo; NO procesado en esta ejecucion.

## Ultima actualizacion 2026-07-20 (5) - DECISION cierre 0272 consumida (no-op, sin respuesta requerida)
- MSG-20260720-Arquitecto-to-Analista-DECISION-cierre-0272-residuales (rr=false, sin
  pregunta) CONSUMIDO informativamente; si sigue en open/ en el proximo disparo, NO
  reprocesar. El Arquitecto RATIFICA el cierre de 0272 con F-0272R2-01 como residual
  declarado (razones: doble incumplimiento del propio exec + traza firmada atribuible +
  burn de campo era PRE-claim y E01 lo cierra). Done-flip ruteado a Codex
  (MSG-...-Arquitecto-to-Codex-ACTION-doneflip-0272).
- Los 4 residuales F-0272R2-01..04 van a **TASK-0276** (ready, owner Codex, reviewer YO):
  filtro de evidencia por applied:true + intent_type en {task_status,task_upsert,decision}
  o payload.commit; keyid coherente con actor (cierra V10/V18); exit-gate del ls-files
  pre-exec (F-03, alimenta cuarentena 0275); log APPLY_FAIL (F-04); espejo born-operational.
  Verifique el archivo: acceptance cubre los 4 + negativo/positivo permanentes; out_of_scope
  prohibe reabrir 0272 y tocar la frontera token>exit>evidencia>regex. Mi futuro re-juicio
  de 0276 debe re-correr la clase E04 (puro claim sin token NO consume) en sandbox autor
  uniforme.
- **TASK-0277** (proposed, espera Operador, toca Area_comun/state/): agujero de
  trazabilidad hallado por el Arquitecto -- TASK-0267 podada del indice caliente (seq 5093)
  sin aterrizar su fila en el archivo. PARA MIS GATES: el chequeo de drift NO cubre los
  archivos de poda y el validador NO cruza ficheros de tareas contra filas del indice; un
  "validate EXIT 0 + drift 0" NO garantiza indice-archivo completo. Considerar cruce manual
  tasks/ vs TASK_INDEX(+ARCHIVE) en juicios futuros que dependan de historia podada.
- Estado al consumir: tree con entrega in-flight del Arquitecto (0276/0277 + DECISION
  untracked, state M), validate vivo EXIT 0; no-op sin commit (heartbeat), sin escritura
  gobernada mia. Mi observacion del rojo transitorio de la pasada iter2 quedo confirmada
  por el Arquitecto (su cola de eventos, aterrizada en 6ebf591).

## Ultima actualizacion 2026-07-20 (4) - TASK-0272 remediacion iter2 OK/CERRABLE (fix-loop consumido)
- Re-juicio de la iteracion 2 (implementacion 02cee08, ultima del tope): veredicto
  **OK/CERRABLE con residuales declarados** en `a5e1acd` (artefacto
  ANALISTA-TASK-0272-remediacion-iter2-veredicto.md + MSG GO rr). Ancla: clon limpio
  D:/ccv0272r2 checkout bab3eba; rutas juzgadas invariantes 02cee08..299c3da (el HEAD
  avanzo 2 veces durante la pasada: 6ebf591 aterrizo instruccion + cola eventos
  5333-5342, 299c3da reporte al Operador; diff vacio en harness/suite).
- CERRADO F-0272R1-01 por comportamiento: bateria propia 41 unit (Get-OwnEvidence +
  Get-ExecOutcomeClass extraidas VERBATIM por regex) + 23 asserts E2E en 11 sandboxes
  AUTOR UNIFORME (D:/sb0272r2, runner real, fake agent por contador, shims de git en
  PATH para forzar exit 7/9 selectivo). Commit concurrente sin evento propio ->
  unconfirmed -> RETRY_EXHAUSTED signal=watchdog (E01); evento propio ed25519 en ventana
  -> confirmed 1x (E02); ajeno no confirma (E03); auth vacia/case/old-seq fail-closed
  (V02-V09/V15-V16); not_enforced_phase2 -> capa nunca-confirma (V06). Token
  terminal-only: cola de texto lo invalida sin consumir (E09a/T04); vacio/truncado ->
  retry senalado. Snapshots rojos -> agente NI ARRANCA (E05/E06 con shim); reset fallido
  / HEAD movido -> defer sin restauracion parcial (E07/E01); pre-sucios BYTE-IGUAL +
  porcelain identico + rename revertido (E08).
- ESCAPE nuevo declarado NO bloqueante F-0272R2-01 (WARNING-real acotado): evento propio
  de PURO claim o exception.recorded en ventana + token ausente + exit 0 -> confirmed ->
  burn (E04 repro determinista; la evidencia PISA la narracion transitoria). No bloquea:
  subconjunto de la clase residual decidida {token ausente + exit 0}; exige doble
  incumplimiento del propio exec; 0 ocurrencias en campo (las 3 reales eran PRE-claim,
  cerradas); deja traza firmada atribuible. Hardening barato recomendado: evidencia solo
  applied:true con intent_type en {task_status,task_upsert,decision} o payload.commit.
  Teoricos: V10 applied:false (stale fencing, solo via runtime/apply.py, no en flujo
  mailbox) y V18 keyid AJENO pasan el chequeo de PRESENCIA (no criptografico; la propia
  suite del maker usa sig fixture); F-03 ls-files pre-exec sin exit-gate (borraria
  untracked pre-existentes si fallara, alimenta 0275); F-04 git apply sin exit (log
  APPLY_FAIL). Residuales: R-B token gana a exit!=0 (T15); R-C stderr ruidoso pierde el
  token sistematicamente (degrada, no quema); TOCTOU ms reset; R-F peer-writes en
  ventana = TASK-0275; drift CLI = TASK-0274.
- Gates: clon bab3eba validate/encoding/domain EXIT 0 + drift False/5337; vivo EXIT 0 +
  drift False/5344; config #4 byte-identica 2E35F26E...354; suites maker
  retry/anthropic/lease EXIT 0. El vivo arranco ROJO (cola de eventos de Codex 5333-5337
  sin commitear, snapshot atras) y verdeo cuando el Arquitecto la aterrizo en 6ebf591:
  rojo transitorio de entrega in-flight, documentado en el veredicto, sin FYI extra.
- Fix-loop 2/2 CONSUMIDO sin fallo nuevo bloqueante -> sin escalada al Operador;
  next_recommended = Arquitecto ratifica done + registra follow-ups baratos junto a
  0274/0275. Hook aviso PRUNE DUE 93.75 (poda = checkpoint del Arquitecto, no mia).
- Patron reutilizable consolidado: shim git.cmd en PATH con findstr selectivo por
  subcomando (exit 7/9) para probar caminos de fallo del harness por comportamiento;
  probes en scratchpad probe_0272_iter2_unit.py / probe_0272_iter2_e2e.py.

## Ultima actualizacion 2026-07-20 (3) - TASK-0272 remediacion iter1 NO-GO acotado
- Re-juicio de la remediacion 2c3b17b (frontera token>exit>evidencia>regex). Veredicto
  CAMBIO-REQUERIDO con BLOQUEANTE UNICO en `417bd01`; artefacto
  ANALISTA-TASK-0272-remediacion-iter1-veredicto.md + MSG rr NOGO. Ancla: clon limpio
  D:/ccv0272r1 en 2c3b17b; invariancia de rutas juzgadas verificada hasta mi commit
  (0cf8185 del Arquitecto aterrizo durante la pasada; diff vacio en harness/suite).
- CERRADO probado (bateria propia 21 unit + 10 E2E, sandboxes D:/sb0272r1): rollback
  BYTE-IGUAL de pre-sucios worktree+staged+renames (E3, status identico); ROLLBACK_DEFER
  con HEAD movido preserva commit del peer (E4); token exacto robusto (punto/espacio/
  case/indent/prefijo lo invalidan; tokens[-1] gana en enumeracion+veredicto final);
  entrega narrando obstaculo + token confirmed consumida 1x (E6); keyword fallback (E7);
  tope 3 + RETRY_EXHAUSTED signal=watchdog + exclusion (E8); defer residuo vivo (E10).
- BLOQUEANTE F-0272R1-01 (WARNING-real): Get-OwnEvidence atribuye por %an y el hub
  commitea TODO con autor uniforme 'Analista|analista@local' (300 commits verificados;
  el propio coord 0cf8185 del Arquitecto lo confirma). Cron Analista: commit ajeno
  durante exec + token ausente + exit 0 -> confirmed -> seen QUEMADO sin senal (E1
  repro determinista). Cron Codex: capa 3 inerte. La suite del maker usa autores
  DISTINTOS -> verde enganoso. Fix pedido: atribucion por eventos firmados del ledger o
  capa 3 nunca-confirma + negativo de suite con autor uniforme. Iteracion 2 de 2 (fallo
  nuevo posterior escala a Operador). Leccion 0268 reconfirmada: JAMAS atribuir por
  autor git en este arbol.
- Hallazgos no bloqueantes: F-02 token line-scoped imitable en fence/enumeracion (A1
  confirmed, A2 definitive burn; 0 carriers tracked hoy; hardening = ultima linea);
  F-03 escrituras de peer DURANTE la ventana del exec destruidas (E5: untracked borrado
  sin log + tracked barrido por reset --hard; PRE-EXISTENTE iter0, cuarentena
  recomendada; pregunte al Arquitecto si se difiere como residual); F-04 snapshots sin
  verificar exit + TOCTOU rev-parse->reset; F-05 gate documentado
  `runtime/protocol_replay.py --check-drift` es VACUO (sin __main__; --bogus-flag exit
  0) -- drift real via protocol_state_drift(): clon False/5302, vivo False/5317;
  RETRACTO parcial: mi iter0 cito el comando vacuo como gate.
- Residual estructural dimensionado: clase {token ausente + exit 0} cae al regex viejo
  (X1 eco NO-GO quema via fallback; X2 narracion fuerza retry acotado; E9 negativa
  libre 3x + senal). Es diseno DECIDIDO de la frontera (regex fallback conservado).
- Gates: clon 2c3b17b validate/encoding/domain EXIT 0 + suites retry/anthropic/lease
  EXIT 0; vivo validate/encoding/domain EXIT 0; config #4 byte-identica 2E35F26E...354.
  Commit propio con pathspec 2 files + trailers en bloque unico; push fast-forward
  limpio sobre 0cf8185. Hook aviso PRUNE DUE 91.67 (poda = checkpoint del Arquitecto,
  no mia).
- Bateria reutilizable: probe_0272_iter1.py (scratchpad de sesion) extrae el
  clasificador VERBATIM por regex del runner del clon (no copia a mano) + 10 sandboxes
  E2E con agente falso por contador; patron replicable para el re-juicio iter2.

## Ultima actualizacion 2026-07-20 (2) - TASK-0273 deadlock poda-vs-claim GO/CERRABLE
- Veredicto GO en `b43c6c6` (artefacto ANALISTA-TASK-0273-deadlock-poda-veredicto.md + MSG
  GO rr=true). Ancla: clon limpio D:/ccv0273 en 18e7cfd; implementacion 3062214 (=51deaf1).
  Durante la pasada el Arquitecto commiteo d96ea57 (coord 0272 NO-GO + ACTION iter1 +
  higiene de 8) EN EL ARBOL LOCAL COMPARTIDO: sus mods de arranque (state + archived)
  aterrizaron ahi; mi commit quedo encima fast-forward; invariancia de rutas juzgadas
  18e7cfd..d96ea57 = diff VACIO. Leccion repetida: fetch + merge-base ANTES de push.
- Bateria propia 9/9 PASA (sandbox espejo del fixture de test_precommit_hook.py con hook
  real): S3 ataque central poda-vencida + estado invalido staged en FULL -> aborta identico
  con WARNING presente; S5 vencida + guia-drift (bounded) aborta; S7 vencida + borrado
  staged de prune_state.py aborta (judgment file); S8 vencida + borrado workflow CI aborta.
  El aviso NO enmascara ningun juicio. Camino GENUINO extra con fixture real de examples:
  check EXIT 1 -> CI sim EXIT 1 accionable -> apply real archiva respetando claim activo +
  in_progress -> check EXIT 0 -> noop 0.077s.
- Medicion clave (la que pedia el REVIEW): --apply no-op 0.293s/0.281s vs --check 0.377s
  (viva, enabled, no vencida; antes 87-89s, ~300x), no_op:true transaction:null, CERO bytes
  de ledger (sha256 antes/despues 5 archivos + porcelain vacio). El early-return de
  apply_prune evalua assess() ANTES del gate de enforcement -> tampoco abre claim/intent en
  runtime-authoritative.
- Espejo born-operational: hook byte-identico sha256 739d9ead...704e en runtime Y attested;
  pin CI actualizado y coincide con el archivo (un pin viejo = CI rojo); attested encapsula
  con defaults.run.working-directory hacia governance-dir (rutas resuelven); skill
  mailbox-hygiene con "Poda coordinada en el checkpoint" solo viaja en tier ATTESTED via
  scaffold_governance_claude (runtime sin governance-dir NO lleva claude-skills).
- Residuales: R1 crash de prune en local ya no aborta (CI fail-closed lo caza); R2
  disparador NUEVO next_actions>8 (clave ya en config pineado) endurece CI - vigilar
  cadencia de condensacion; R3 due-path sin clave mode (cosmetico); R4 assert de coste noop
  del maker solo cubre DISABLED (yo cubri enabled en vivo); R5 runtime_instantiation_cases
  2 casos rojos (coordination_default_and_flag + runtime_tier_scaffolds_motor_gates_ci_off)
  PRE-EXISTENTES verificados identicos en 3062214~1 - pide unidad de mantenimiento.
- Gates: clon validate/encoding/domain/drift EXIT 0; vivo validate EXIT 0; config #4
  byte-identica 2E35F26E...354; suites maker prune/runtime-prune/hook/attested EXIT 0.

## Ultima actualizacion 2026-07-20 - TASK-0272 seenburn NO-GO + TASK-0258 re-juicio GO
- DOS veredictos en una pasada (orden de cola del Arquitecto: 0258 primero). Ancla comun:
  clon limpio D:/ccv0272 en e7ad9e6; HEAD avanzo DOS veces durante la pasada (0273 aterrizo
  3062214/67ac1e8/22a0a2a + memoria maker f46437f); invariancia de rutas juzgadas verificada
  por diff (solo new_instance.py cambio, pin CI hook de 0273, fuera de alcance juzgado).
- TASK-0258 re-juicio F-0258-01 GO/CERRABLE en `305efd1`: SCHEMA_VERSIONING.md linea 9
  `Current version: 1.3.0` + seccion DECISION-0103 C3 con MINOR veraz; diff VACIO
  feb43c0..HEAD en schema/validate/suites; suites 8/8 + 5/5 EXIT 0 en clon. Runners reales:
  run_runtime_turn_schema_cases.py / run_runtime_turn_semantic_cases.py (no run_turn_cases).
- TASK-0272 (fin seen-burn silencioso) CAMBIO-REQUERIDO/NO-GO en `8cb4b45`. Bateria propia:
  sandboxes git efimeros + runner REAL scripts/harness/peer_mailbox_cron.ps1 + fake agent
  scripteado (probe_0272.py en scratchpad de sesion; escenarios S2-S10 documentados en el
  artefacto). 3 PASA (S2 keyword-definitivo consume 1x; S8 tope 3 + RETRY_EXHAUSTED
  signal=watchdog + exclusion; S10 defer residuo vivo sin quemar) / 6 SLIPS deterministas:
  S5 commit de PEER durante exec -> abort no-op = confirmed = SEEN QUEMADO SIN SENAL (el bug
  resucitado; evidencia = HEAD+status global no atribuible); S4 eco "NO-GO" en transcript ->
  definitive quema retirada DECISION-0020; S9 entrega CONFIRMADA narrando "claim ajeno
  activo" (vocabulario obstacles[] de 0258!) -> transient 3x -> RETRY_EXHAUSTED falso, seen
  jamas; S6 ruta PRE-modificada staged por el exec -> rollback la salta: queda "M " staged
  con contenido del exec y el contenido del peer DESTRUIDO (clase dominante 11:03, state
  files casi siempre pre-sucios); S3 negativa principiada fraseada libre ("no asumo: soy
  checker") -> unconfirmed -> 3 reintentos (AC dice JAMAS); S7 rename staged sobrevive
  (porcelain "old -> new" una-ruta). Causa raiz: regex texto libre > exit+evidencia.
- Fix-loop declarado (iter 1/2): (1) contrato outcome por TOKEN exacto tipo STOP_JOB, regex
  solo fallback; (2) atribucion de evidencia; (3) rollback por delta de INDICE + renames;
  (4) negativos permanentes S2/S4/S5/S6/S9. Re-juicio = re-correr bateria completa.
- Espejo born-operational verificado: export runtime-tier shippea runner byte-identico
  sha256 21afee4c...; tier coordination NO shippea harness (diseno pre-0272, residual R1).
  Wrappers codex/analista_mailbox_cron.ps1 = thin con paridad de params retry.
- Gates: clon validate/encoding/domain/drift EXIT 0; vivo validate EXIT 0; config #4
  byte-identica 2E35F26E...354; suites maker retry/anthropic/lease EXIT 0.
- LECCION operativa: el arbol paso de sucio (ledger peer in-flight) a limpio y de vuelta a
  sucio DURANTE la ventana de entrega; commit con pathspec explicito de MIS 4 rutas salio
  limpio ("2 files changed" cuadro ambas veces) sin esperar quietud total -- esperar quietud
  absoluta en este arbol es inalcanzable en horas activas; gatear por claims=0 en MIS rutas
  + pathspec + verificacion post-commit del stat.
- PENDIENTE al cierre de sesion: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0273-
  deadlock-poda.md sigue en open/ sin procesar (llego durante esta pasada; siguiente disparo).

## Ultima actualizacion 2026-07-20 - TASK-0269 materializacion parcial GO + cifra E6
- Revision adversarial de TASK-0269 (E6-C, materializacion parcial de rutas del validador
  en .githooks/pre-commit). Ancla: 07fad8a/3ec6a70/0ce5397, HEAD 1757c8f, clon limpio
  D:/ccv0269; invariancia verificada a c0096f3 (Arquitecto commiteo la instruccion +
  higiene DURANTE mi pasada; diff vacio en rutas juzgadas). GO/CERRABLE en `5c2642a`.
- PARIDAD TODO PASA: suite maker EXIT 0 + 5 probes propios en el repo REAL partial-vs-total
  (accept valido, TASK_INDEX roto, delete centinela validate.yml con validador REAL, R100
  validator-out, delete CLAUDE.md no-leida): verdicts identicos, misma razon; cero escapes.
- INVENTARIO cierra: read-set derivado por mi del codigo (validador + prune + eventlog/
  protocol_replay + RUNTIME_TIER_REQUIRED_PATHS); git del validador es solo-historia;
  event-state.runtime.json/secretos untracked = ausentes de ambos snapshots; barrido de
  deliverables reviewed hot(25)+archive(278) -> cero fuera del inventario.
- LA CIFRA (gobierna criterio ex-ante E6): caliente quieta 70.7/71.6 s, frio 99.7 s, piso
  observado 43.0 s (2.9x umbral). Desglose: materializar 1.9 s (3571 files; total 2.3 s/
  4382), prune 0.6 s, validador directo 35.4 s -> domina validador+entorno (Defender sobre
  archivos recien materializados; firmas ledger; rev-list de trailers), NO la materializacion.
  Rama unica: > 15 s -> E6-A PERMANENTE, hibrido no autorizado. Maker 108.2 s bajo carga
  confirmado en rama, corregido en magnitud.
- Residuales: R1 deliverable fuera de inventario = falso rechazo futuro (fail-closed, hoy 0
  casos); R2 /tmp/protocol-index.0BANIM residuo del maker ante kill duro (trap no sobrevive
  SIGKILL; 12 corridas propias sin residuo nuevo); R3 varianza ambiental 43-108 s sin efecto
  en la rama; R4 instruccion llego untracked, aterrizo en c0096f3 (rojos transitorios del
  vivo a mitad de ventana = entrega in-flight del peer, no anomalia).
- Gates: clon 1757c8f validate sin secretos/encoding/domain EXIT 0; drift false
  up_to_seq=5201 hot==replay; config #4 byte-identica 2E35F26E...354; vivo post-c0096f3
  validate/encoding/domain EXIT 0; suite hook EXIT 0.
- Artefacto `Area_comun/artifacts/ANALISTA-TASK-0269-materializacion-parcial-veredicto.md`;
  MSG rr `MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0269-materializacion-parcial-GO.md`.
  LECCION metodologica: medir la cifra ANTES de correr la bateria de probes (la bateria
  contamina el caliente; mis corridas quietas 70.7/71.6 quedaron como la cifra oficial y las
  de la bateria 43-56 s como piso/banda de varianza).

## Ultima actualizacion 2026-07-20 - TASK-0258 obstacles[] CAMBIO-REQUERIDO (docs-only)
- Revision adversarial de TASK-0258 (bloque obstacles[] en runtime/turn_schema.json,
  DECISION-0103 C3 carril runtime). Ancla funcional origin/main `9ce238b`, implementacion
  `9be450d`, entrega `34d5dff`, clon limpio /d/ccv0258 + clon contraste pre-0258 /d/ccv0258p.
  HEAD avanzo a `feb43c0` durante la pasada; invariancia verificada con diff VACIO sobre
  turn_schema/fixtures/SCHEMA_VERSIONING/task.md y gates re-corridos en feb43c0.
- FUNCIONAL TODO PASA: suites 8/8 + semantic 5/5 EXIT 0; 36 payloads propios via
  Draft7Validator (mismo consumidor que turn_validate.py:277) sin un solo escape (missing
  required x4, additionalProperties item y raiz, familia enum completa con case/espacios/
  null/int, tipos, no-array, item mixto); e2e validate_turn 3/3 (poblado valido, malformado
  rechazado, vacio valido); 22 suites consumidoras EXIT 0; bump 1.2.0->1.3.0 = MINOR
  correcto; forma canonica == DECISION-0103 c.3, TASK-0261 se ancla textual a la de 0258.
- BLOQUEA solo F-0258-01 (WARNING-real, docs-only): SCHEMA_VERSIONING.md linea 9 sigue
  `Current version: 1.2.0` con schema 1.3.0 y sin seccion de justificacion del MINOR
  (patron del doc: 1.1.0 Capa A, 1.2.0 Fase 5.2). Precedente 0268-H1 aplicado.
- A-0258-02 (DECISION-0018, ajena a la unidad, RESUELTA en pasada): canonico ROJO en clon
  limpio de 9ce238b por drift B.3 de los 3 slims -- divergencia de push (local aa98267 con
  rematerializacion vs 9ce238b publicado sin ella, mismo mensaje/timestamp). El Arquitecto
  reconcilio en a6e540f; feb43c0 verde. LECCION: ante commits gemelos local/remoto con mismo
  mensaje, diff de TREES (los slims delataron el clobber); el vivo verde miente sobre el
  canonico (leccion clean-clone confirmada otra vez).
- Residuales: R1 minLength 1 mas estricto que el AC (0261/0262 deben replicarlo o los
  carriles divergen); R2 examples/full_runtime_instance/runtime/turn_schema.json pineado en
  1.2.0 SIN obstacles (rechaza reportes con obstacles; new_instance copia runtime/ canonico
  asi que el camino normal no muerde); R3 4 suites rojas preexistentes (instantiation, loop,
  protocol_materialize, supervised_autonomy) invariantes pre/post; R4 instruccion REVIEW
  llego sin commitear (luego en 6950a48); R5 mismatch 0257 transitorio ya inexistente.
- Gates: validate vivo con secretos EXIT 0; clon feb43c0 sin secretos EXIT 0 (9ce238b fue
  EXIT 1 por A-0258-02); domain/encoding EXIT 0; config #4 byte-identica 2E35F26E...354 en
  vivo y ambos clones.
- Veredicto commiteado y pusheado por mi en `0676697` (pathspec explicito, 2 files, hook de
  Codex in-flight paso limpio); artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0258-obstacles-schema-veredicto.md`; MSG rr a
  Arquitecto
  `Area_comun/mailbox/open/MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0258-obstacles-CAMBIO-REQUERIDO.md`.
- Fix-loop declarado: Codex actualiza SCHEMA_VERSIONING.md (Current version 1.3.0 +
  justificacion DECISION-0103 C3) -> re-juicio barato (lectura doc + validate clon limpio
  EXIT 0 + encoding EXIT 0; SIN re-probes funcionales). Iteracion 1/2, maximo 2 antes de
  Operador. Codex tenia claim activo TASK-0269 (hook precommit) durante mi entrega; mis
  rutas sin claim ajeno.

## Ultima actualizacion 2026-07-20 - TASK-0268 re-juicio H1: GO (CERRABLE), ratificada
- Re-juicio de lectura anclado en ab5a017, clon limpio /d/ccv0268h1. W1-W6 PASAN:
  README_INSTANCIACION corregido en c06fbad dice la verdad del reparto E6-A (default
  acotado juzga el arbol sin materializar; garantia staged solo bajo flag o CI).
  Re-probado por comportamiento a HEAD: staged roto aceptado por default en 0.455 s;
  HOOK_FULL=1 materializo (checkout-index a tmp) y rechazo exit 1.
- Invariancia probada con diff VACIO b37e638..ab5a017 sobre hook/suite/validate.yml/
  new_instance.py; SHA 4dae776c identico en hook y ambos pines. Gates clon: validate 0
  (drift 0), encoding 0, neutralidad 0, config 2E35F26E byte-identica.
- Atribucion del fix confirmada en ledger firmado (seq 5133-5140 Codex); el author de
  git es uniforme "Analista <analista@local>" en el arbol compartido: NUNCA usar el
  author de git para atribuir, solo los eventos firmados.
- ENTREGA ACCIDENTADA (leccion doble): (1) mi commit fue bloqueado por el hook acotado
  "PRUNE DUE released_ratio 90" -- condicion TREE-LOCAL creada por staging sin
  commitear de Codex (memoria final de c2abc9c); diagnostico falsable = correr el hook
  a HEAD en clon limpio ("prune not due"). NO pode alrededor de entrega ajena a medias
  ni bypasee el gate; prepare entrega desde clon. (2) Antes de poder entregar, el
  Arquitecto commiteo 1fe0256 barriendo el index COMPLETO: mi artefacto (snapshot
  pre-edicion, integro), mi MSG GO rr=true movido DIRECTO a archived/ (nunca paso por
  open/ en canonico) y la memoria de Codex; ratifico 0268 (review_approved) en el
  mismo commit. Segunda recurrencia del arrastre (tras 51dd52e), ahora sobre archivo
  en edicion activa: un Edit mio fallo "File does not exist" porque el peer MOVIO el
  archivo entre mis dos edits. FYI DECISION-0018 emitido
  (MSG-...-FYI-sweep-mid-edit-1fe0256); addendum de cronologia en el artefacto.
- LECCION operativa: en este arbol compartido la ventana escribir->stagear->commitear
  debe ser MINIMA y verificarse despues (diff tree vs HEAD) que la version aterrizada
  es integra; un "File does not exist" subito en ruta compartida = peer activo AHORA,
  parar y re-leer git status antes de seguir.
- Artefacto: ANALISTA-TASK-0268-rejuicio-H1-veredicto.md (con addendum, commit propio
  post-1fe0256); GO consumido en archived/. Cadena de cierre disparada por el
  Arquitecto (0257, 0258, 0269, gate 0265) -- yo sigo checker-only.

## Ultima actualizacion 2026-07-20 - TASK-0268 reparto E6-A CAMBIO-REQUERIDO (docs-only)
- Revision adversarial anclada en hub `f2d07a3` (clon limpio /d/ccv0268 + sondeos en
  /d/ccv0268b), implementacion `b37e638`: CAMBIO-REQUERIDO acotado a docs.
- FUNCIONAL TODO PASA: default acotado en commit gobernado real 0.455/0.482/0.483 s
  (<~2 s del AC; handoff 0.449 s reproducido); poda rota bloquea; drift de guia staged
  bloquea; staged gobernado ROTO aceptado por default en 0.494 s (no invoca validador) y
  RECHAZADO bajo flag con mecanica v2 intacta (HOOK_FULL=1 exit 1 29.3 s; git config
  hook.full true exit 1 32.4 s; env gana sobre config false). CI: diff solo linea pin,
  pin 4dae776c == sha256 real. Suite exit 0. Espejo born-operational: hook byte-identico
  en tiers coordination y runtime; runtime emite CI con pin nuevo.
- H1 (bloqueante, falsable): README_INSTANCIACION dice "para todo commit materializa el
  snapshot staged" y el default NO materializa (inspecciona el arbol; el hook mismo lo
  declara). Refutado en ambas direcciones (staged roto aceptado 0.5 s; prune roto solo-
  en-arbol rechazado). Remediacion docs-only 1-2 frases; hook y pin no cambian.
- Residuales R1-R5: arranque frio 22.5 s ambiental; via git-config sin caso de suite;
  dependencia de arbol en acotado (declarada); HOOK_FULL solo "1"; auto-borrado del
  validador solo lo caza CI. Neutralidad roja en ancla = fixture preexistente 0271
  (0 hits en rutas 0268; verde a 45eb10f).
- Gates: validate con/sin secretos exit 0 (drift 0 en ancla); encoding 0; config #4
  2E35F26E byte-identica; events.jsonl del ancla integro (delta posterior = chain
  creciendo por 0271, no drift).
- LECCION propia: bug en mi sonda (dict de env en el parametro posicional equivocado ->
  HOOK_FULL nunca llego al hook y "full" parecio no ejecutar); verificar SIEMPRE que el
  flag llego (timing 0.4 s vs 30 s delato el error). Sin esa segunda mirada habria
  reportado un falso CRITICAL.
- ANOMALIA DECISION-0018 senalada por FYI: commit 51dd52e del Arquitecto (coord 0271,
  sin pathspec) arrastro mi MSG de veredicto staged en el arbol compartido; contenido
  correcto en canonico, solo atribucion cruzada. Esperar ventana segura NO protege del
  peer que commitea pelado: minimizar la ventana add->commit y re-verificar que "1 file
  changed" cuadre con lo stageado.
- Veredicto: artefacto en fa43bfc; MSG rr (dentro de 51dd52e) =
  `MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0268-veredicto.md`; artefacto =
  `Area_comun/artifacts/ANALISTA-TASK-0268-reparto-acotado-veredicto.md`.
- Fix-loop declarado: Codex corrige README -> re-juicio (lectura + encoding + validate
  clon limpio); iteracion 1/2, maximo 2 antes de Operador.

## Ultima actualizacion 2026-07-20 - TASK-0267 hook v2 NO-GO
- Revision adversarial anclada en hub
  `7c98fd47044b394c8d879ed19c2578431c23e4a7`, implementacion `b583090`:
  CAMBIO-REQUERIDO / NO CERRABLE.
- F-0267-01 CRITICAL: el selector `git diff --cached --name-only` pierde el
  origen gobernado de un rename R100 hacia fuera. Probes por commit real de
  validator `scripts/ -> docs/` y estado `Area_comun/state/ -> docs/` terminaron
  EXIT 0. El negativo permanente solo renombra dentro de `scripts/`.
- F-0267-02 WARNING-real: `prune_state.py --check` sigue ejecutandose desde el
  worktree antes del snapshot; mutarlo solo en unstaged a EXIT 23 cambia el
  veredicto de un commit limpio.
- Pasan suite permanente, deletes validator/runtime/state, staged invalido,
  aislamiento del validator, peer unstaged en Area_comun, cleanup, arming,
  export default/coordination/runtime y pin CI. Suite agregada de instanciacion
  sigue EXIT 1 en dos asserts ya declarados por el maker.
- Medicion propia: frio 45.756 s, caliente 46.555 s, ambos EXIT 0; se reporta
  como riesgo y no como veto por reserva del Operador.
- Gates: validate con/sin secretos, domain y encoding EXIT 0; drift 0 seq
  5000/5012; chain valida; config #4 byte-identica SHA-256 `2E35F26E...354`.
- Veredicto commiteado y pusheado en `42eab07`; artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0267-hook-v2-veredicto.md`; MSG rr a
  Arquitecto
  `MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0267-hook-v2-NOGO.md`.
- Fix-loop: remediar familia R100-out y prune live, negativos permanentes,
  re-gates y re-juicio Analista; iteracion 1/2, maximo 2 antes de Operador.

## Ultima actualizacion 2026-07-19 - TASK-0257 re-juicio final iteracion 2 NO-GO
- Revision adversarial anclada en hub `f64dcbdf9080ce87d4722c50662bb375d9d3c57a`,
  remediacion `e2cadd8`: CAMBIO-REQUERIDO / NO CERRABLE / ESCALAR AL OPERADOR.
- ACMRTD cierra delete de validator/runtime/state y T; F-0257-01/02 pasan. Dos
  bloqueantes: borrar `.githooks/pre-commit` seguido de commit real termina exit 0,
  y R100 del validator desde `scripts/` a `docs/` termina commit exit 0 porque
  `--name-only` pierde el origen gobernado.
- La regresion permanente da falso verde para delete del hook: ejecuta con `sh`
  el path ya borrado y trata ese fallo de invocacion como rechazo del commit.
- Gates: suite 0; delete validator/runtime/state 1 esperado; delete hook 0
  inesperado; rename-out 0 inesperado; T 1 esperado; exports 3 tiers 0; validate
  con/sin secretos, domain y encoding 0; drift 0 seq 4967/4972; config #4 intacta.
- Veredicto commiteado por Analista en `0b52864`; artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0257-gate-propio-E2-rejuicio-final-iter2-veredicto.md`;
  MSG rr a Arquitecto
  `MSG-20260719-Analista-to-Arquitecto-REVIEW-TASK-0257-rejuicio-final-iter2-NOGO.md`.
- Tope 2/2 agotado: no abrir otra remediacion o re-juicio sin directiva explicita;
  Arquitecto debe escalar el historial completo al Operador.

## Ultima actualizacion 2026-07-19 - TASK-0257 re-juicio iteracion 1 NO-GO
- Revision adversarial anclada en hub `7fbb88acb94613502de115f4ceb7d6c72bfec9fb`,
  remediaciones `33af66b` y `5e5b2d5`: CAMBIO-REQUERIDO / NO CERRABLE.
- F-0257-01 pasa para modificaciones: estado gobernado roto staged + validator con
  `raise SystemExit(0)` unstaged termina hook exit 1. F-0257-02 pasa: gobernado
  exit 0 en 29.532 s; modo acotado no gobernado exit 0 en 0.401 s.
- F-0257-03 WARNING-real nuevo: `git diff --cached --name-only --diff-filter=ACMR`
  excluye eliminaciones. Probe propio en clon limpio: `git rm
  scripts/validate_collaboration_state.py` + hook termina exit 0 con diff staged
  `D`; el validator eliminado no se ejecuta.
- Suite permanente exit 0. Export coordination/runtime/attested: new_instance y
  validate exit 0; hook SHA-256 comun
  `E803C867977977E5AC04445AE1CE5B440DE7B0B2669FC44358E3F6439717062C`.
- Gates canonicos: validate sin secretos/domain/encoding exit 0; vivo con secretos
  validate exit 0; drift 0 seq 4934; chain valid 4262 eventos; config #4
  byte-identica SHA-256 `2E35F26E...354`. Producto NOT_RUN por alcance canonico.
- Veredicto commiteado por Analista en `774f858`; artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0257-gate-propio-E2-rejuicio-iter1-veredicto.md`;
  MSG rr a Arquitecto
  `MSG-20260719-Analista-to-Arquitecto-REVIEW-TASK-0257-rejuicio-iter1-NOGO.md`.
- Fix-loop: remediar eliminaciones staged en toda la familia de rutas, agregar
  negativos permanentes y pedir re-juicio Analista antes de cierre. Al agotarse
  el tope de 2 iteraciones, un fallo adicional se escala al Operador.

## Ultima actualizacion 2026-07-19 - TASK-0257 gate propio E2 NO-GO
- Revision adversarial anclada en hub `59607c022b0c1e3dceaf963eba26db9fcbcdc2bc`
  e implementacion `acfe91d943f8`: CAMBIO-REQUERIDO / NO CERRABLE.
- F-0257-01 WARNING-real: `.githooks/pre-commit` solo protege equivalencia
  index/worktree en rutas de datos gobernadas, no en el validator ni sus dependencias.
  Probe propio: mismatch staged de TASK-0257 + `raise SystemExit(0)` UNSTAGED en
  `scripts/validate_collaboration_state.py` aterrizo con commit exit 0; el mismo
  mismatch con validator canonico salio exit 1.
- F-0257-02 WARNING-real: acceptance exige modo acotado si hook completo excede
  ~10 s; probe positivo midio 11.531 s y negativo 12.944 s, sin modo acotado.
- Pasan hub armado, positivo/negativo base, suciedad personal permitida, suciedad
  gobernada rechazada, export de coordination/runtime/attested, desarme E3 y bypass
  honesto. Producto NOT_RUN porque REVIEW canonico declara SIN PRODUCTO EN ALCANCE.
- Gates canonicos: validate/domain/encoding/prune exit 0; drift 0 seq 4913; chain
  valid 4241 eventos; config #4 byte-identica SHA-256 `2E35F26E...354`.
- Artefacto `Area_comun/artifacts/ANALISTA-TASK-0257-gate-propio-E2-veredicto.md`;
  MSG rr a Arquitecto `MSG-20260719-Analista-to-Arquitecto-REVIEW-TASK-0257-gate-propio-E2-NOGO.md`.
  Arquitecto materializo ambos concurrentemente en `2bd5f61`; Analista dejo autoria
  final canonica en `5f56d64` sin cambiar el NO-GO.
- Fix-loop: remediar F-0257-01/F-0257-02, re-gatear y re-juicio Analista previo a
  cierre; maximo 2 iteraciones antes de operador. TASK-0258 permanece sin abrir.

## Ultima actualizacion 2026-07-17 - patron EXTRACTED-vs-INFERRED: DIFERIR-LIMPIO
- Revision adversarial docs-only registrada y pusheada por Analista en commit `476ceac`
  (`review(ops): Analista final refuta reserva epistemica`). Ancla canonica: instruccion y SPEC en
  `cae10ad95d194d263ad5eff88f5d16fc714ae28c`. Artefacto:
  `Area_comun/artifacts/ANALISTA-OPS-patron-extracted-inferred-aristas-veredicto.md`; MSG rr a Arquitecto:
  `Area_comun/mailbox/open/MSG-20260717-Analista-to-Arquitecto-REVIEW-patron-extracted-inferred-aristas.md`.
- Veredicto: REFUTA la recomendacion del Arquitecto de diferir a F4 con dos columnas reservadas en DDL v1.
  Posicion final DIFERIR-LIMPIO: la DB es cache reconstruible; el default `extracted` falsea procedencia ante
  omisiones; la PK actual colisiona aristas extracted/inferred del mismo triple; F1 no define el mapeo completo
  key->edge_type; F4 debe disenar procedencia, evidencia, algoritmo/version/config y score de una vez.
- `mentions` no demuestra inferencia en F1: la SPEC enumera el edge_type pero no define su fuente. El claim
  "todo extracted F1-F3" es compatible con la intencion de la SPEC, no una garantia hasta precisar el mapeo.
  El descarte definitivo de confianza continua tambien se refuta: F4 puede elegir score determinista, confianza
  calibrada o tiers; el round-trip requiere semantica y serializacion canonica.
- Alcance sin producto y sin `npm test` por orden expresa. Gates: validate vivo con secretos EXIT 0; clon limpio
  `cae10ad` sin secretos EXIT 0; encoding/domain EXIT 0; drift false `up_to_seq=4693`; `protocol.config.json`
  byte-identico SHA-256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Colision observada: Arquitecto commiteo el borrador en `ceda165` mientras Analista aun completaba tabla/gates.
  El follow-up `476ceac` deja la revision final con autor Analista y pide al Arquitecto archivar el hilo resuelto.

## Ultima actualizacion 2026-07-13 - DECISION-0094 sello N=6 OK-ATESTADO
- Verificacion independiente s.11.5 del sello pre-registro N=6 registrada por Analista en commit `a560079`
  (`review(sello-n6): Analista attests sha256`). Artefacto:
  `Area_comun/artifacts/ANALISTA-OPS-sello-preregistro-N6-veredicto.md`; MSG rr a Arquitecto:
  `Area_comun/mailbox/open/MSG-20260713-Analista-to-Arquitecto-REVIEW-sello-preregistro-N6-OK.md`.
- Ancla canonica hub: instruccion
  `Area_comun/mailbox/open/MSG-20260713-Arquitecto-to-Analista-REQUEST-verif-independiente-sha256-sello-N6.md`;
  HEAD `269590d900a19d98fbc38874fda6eb0f4cdcb844`; decision
  `Area_comun/decisions/DECISION-0094-sello-preregistro-contabilidad-N6.md`; artefacto sellado
  `Area_comun/artifacts/SELLO-PREREGISTRO-contabilidad-employee-run-N6.md`.
- Resultado: OK-ATESTADO / CERRABLE. En clon limpio de HEAD, el one-liner sha256 recomputo
  `28fd963b2472b1b6277b45e38e3bdf92686f022b0c41de4ab6a1338597d45828`, exacto al valor anclado en DECISION-0094.
  Evento #4 de decision en seq 4658 y release de la transaccion en seq 4659; drift 0 hasta seq 4662.
- Gates: validate vivo con secretos EXIT 0; validate clon limpio sin secretos EXIT 0; domain vivo/limpio EXIT 0;
  encoding vivo/limpio EXIT 0; drift vivo/limpio false `up_to_seq=4662`; `protocol.config.json` worktree
  byte-identico vivo/limpio sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
  Producto Nova-Budget NOT_RUN por instruccion canonica `SIN PRODUCTO EN ALCANCE`.
- Residual declarado: la pre-datacion se atesta contra documentos/eventos canonicos del hub; no fue auditoria
  externa de repositorios de producto.

## Ultima actualizacion 2026-07-12 - TASK-9304 F-9304-01 re-juicio OK/CERRABLE
- TASK-9304 F-9304-01 re-juicio registrado por Analista en commit `155897b`
  (`review(TASK-9304): Analista OK F9304 rejuicio`). Artefacto:
  `Area_comun/artifacts/ANALISTA-TASK-9304-F9304-01-rejuicio-veredicto.md`; MSG rr a Arquitecto:
  `Area_comun/mailbox/open/MSG-20260712-Analista-to-Arquitecto-REVIEW-TASK-9304-F9304-01-rejuicio-OK.md`.
- Ancla canonica hub: instruccion
  `Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Analista-REVIEW-TASK-9304-F9304-01-rejuicio.md`;
  Aegis clean clone en commit `8159716cfaa0b3720de889841b14b82844730799`; fix citado `7f80e481`.
- Resultado: OK/CERRABLE. `python examples/chain_cases/run_tests.py` EXIT 0, 40/40; Aegis
  validate/domain/encoding EXIT 0; drift false `up_to_seq=3856`; `validate_chain` baseline `valid=true`.
  Repro propia de F-9304-01: append `tamper` al export pre-T0 -> `validate_collaboration_state.py` EXIT 1
  y `validate_chain` `valid=false`, razon `pre_t0 sealed export hash mismatch`.
- No regresion F-9303-01: probe propio sobre `config_epoch_history[1].boundary_id` y boundary payload
  `sealed_segment.event_count` sigue fallando cerrado. `protocol.config.json` Aegis byte-identico entre
  `00ccb55b`, `7f80e481` y `8159716c`, sha256
  `77242D63090144C8818426927CC8AF149F4FE36C7637AE1B84387674D4BDD283`.
- Hub gates: validate con secretos EXIT 0; hub clean clone sin secretos validate EXIT 0; domain/encoding EXIT 0;
  drift false `up_to_seq=4627`; chain valid `checked_events=3955`; hub config sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Residuales: `jball-live` sigue diferido a la maquina de John; ataque coordinado export pre-T0 +
  `protocol.config.json` actualizado valida verde en probe aislada, por lo que el cierre depende de #4
  byte-identica/anclada; Nova-Budget root `npm test` limpio EXIT `-4058` por ausencia de `package.json`, fuera
  del alcance canonico de este REVIEW.

## Ultima actualizacion 2026-07-12 - TASK-9304 jball reanchor NO-GO
- TASK-9304 review formal registrado por Analista en commit `d0f7974`
  (`review(TASK-9304): Analista blocks jball reanchor`). Artefacto:
  `Area_comun/artifacts/ANALISTA-TASK-9304-jball-reanchor-veredicto.md`; MSG rr a Arquitecto:
  `Area_comun/mailbox/open/MSG-20260712-Analista-to-Arquitecto-REVIEW-TASK-9304-jball-reanchor-NOGO.md`.
- Ancla canonica hub: instruccion
  `Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Analista-REVIEW-TASK-9304-jball-reanchor.md`;
  Aegis clean clone en commit `00ccb55b9d02e676c9cf31218f4ae1edc25c3ee1`.
- Resultado: CAMBIO-REQUERIDO / NO CERRABLE. Aegis pasa `python examples/chain_cases/run_tests.py`
  39/39, validate/encoding/domain EXIT 0, drift false `up_to_seq=3841`, chain valid `checked_events=3169`.
  Epoca 1 `[672,3807]` y epoca 2 `[3809,3836]` sellos recomputados match; F-9303-01 de epoca 2 falla cerrado
  para tamper payload/config-history; `jball:v1` registrado con pubkey
  `pSGHuZPbQQF4aJn4dBhyRSiCUn1DKrMwhAUjjLVyWd0=` e implementer.
- Bloqueo F-9304-01: TASK-9304 AC5 promete que tamper en cualquier epoca, incluido `pre_t0`, hace fallar
  `validate_chain`. Probe propia en copia limpia agrego `tamper` a
  `pre_t0_ledger_seal/events-pre-t0-000001-000671.jsonl`; `python scripts/validate_collaboration_state.py`
  siguio EXIT 0 y `validate_chain` devolvio `valid=true`. Fix-loop: hard-gatear
  `pre_t0_provenance.sealed_export` o corregir canonicamente el AC para excluir pre-T0 del contrato
  `validate_chain`; re-juicio Analista antes de cierre, maximo 2 iteraciones.
- Hub gates: validate con secretos EXIT 0; hub clean clone sin secretos validate EXIT 0; encoding/domain EXIT 0;
  drift false `up_to_seq=4625`; chain valid `checked_events=3953`; hub config sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`, `protocol_version=1.14.0`.
- Nota: el commit del veredicto uso `Task-Id: none` + `Ops-Reason` porque TASK-9304 vive en Aegis y el gate de
  trailers del hub rechaza Task-Id no existente en el TASK_INDEX local.

## Ultima actualizacion 2026-07-12 - TASK-9303 F9303-01 re-juicio OK/CERRABLE
- TASK-9303 F-9303-01 re-juicio registrado por Analista en commit `a1c3644`
  (`review(TASK-9303): Analista OK boundary seal regate`). Artefacto:
  `Area_comun/artifacts/ANALISTA-TASK-9303-F9303-01-rejuicio-veredicto.md`; MSG rr a Arquitecto:
  `Area_comun/mailbox/open/MSG-20260712-Analista-to-Arquitecto-REVIEW-TASK-9303-F9303-01-rejuicio-OK.md`.
- Ancla canonica hub: instruccion
  `Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Analista-REVIEW-TASK-9303-F9303-01-rejuicio.md`;
  Aegis clean clone en commit `65b83c5202554610d52e68e627d241fe1a6695ed`.
- Resultado: OK/CERRABLE para F-9303-01. `python examples/chain_cases/run_tests.py` en clean clone Aegis
  EXIT 0, 26/26. Probe propia de 16 mutaciones evento/config (`boundary_id`, hashes, `event_type`,
  `boundary_seq`, `sealed_segment.sha256/event_count/seq_range`) confirmo 16/16 fallan cerrado. Sello 672..3807
  recomputado desde event-log: 3136 lineas, sha256
  `32a769f371794a01598d4932e95f18af6f65c8db24487241b658f3d51cf570d7`, match con config.
- Gates: Aegis validate/encoding/domain EXIT 0, drift false `up_to_seq=3818`, chain valid `checked_events=3146`;
  hub validate con secretos EXIT 0, hub clean clone sin secretos validate EXIT 0, domain/encoding EXIT 0,
  drift false `up_to_seq=4578`, chain valid `checked_events=3906`. Aegis `protocol.config.json`
  byte-identico entre `9fb0f12d`, `65b83c52` y working tree, sha256
  `3E93CABD81B890FA98431EDB2F17A05946DB69CC36246F94905C497F22D634D6`; hub config sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Residuales declarados: `event_auth.signature` HMAC mutation fuera de alcance; 7b `jheredia-live` diferido al
  A2-nominal por instruccion canonica; no ejecutar Nova-Budget `npm test` cuando el REVIEW canonico diga
  "SIN producto Nova-Budget en alcance".

## Ultima actualizacion 2026-07-12 - TASK-9303 Aegis chain reanchor NO-GO
- TASK-9303 review formal registrado por Analista en commit `b9c6d23`
  (`review(TASK-9303): Analista blocks chain reanchor`). Artefacto:
  `Area_comun/artifacts/ANALISTA-TASK-9303-chain-reanchor-veredicto.md`; MSG rr a Arquitecto:
  `Area_comun/mailbox/open/MSG-20260712-Analista-to-Arquitecto-REVIEW-TASK-9303-chain-reanchor-NOGO.md`.
- Ancla canonica hub: instruccion
  `Area_comun/mailbox/open/MSG-20260712-Arquitecto-to-Analista-REVIEW-TASK-9303-chain-reanchor.md`;
  Aegis clean clone en commit `95717820b9390f4a73cb8072ac4fb570fcd7a68d`.
- Resultado: CAMBIO-REQUERIDO / NO CERRABLE. Aegis chain_cases 14/14, validate/encoding/domain EXIT 0 y drift
  false up_to_seq 3814. Sello viejo 672..3807 recomputado match
  `32a769f371794a01598d4932e95f18af6f65c8db24487241b658f3d51cf570d7`. Bloqueo F-9303-01: `validate_chain`
  acepta tamper de `chain.regenesis_boundary.payload` y del sello `config_epoch_history` (`boundary_id`,
  `old_config_hash`, `sealed_segment.sha256`, `event_count`, `seq_range`) con `valid true`.
- Hub gates: validate con secretos EXIT 0; validate secretless clean clone EXIT 0; scan_encoding EXIT 0;
  scan_domain_neutrality EXIT 0; drift false up_to_seq 4576; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Fix-loop esperado: Codex debe endurecer `validate_chain` para verificar equivalencia completa frontera<->config
  y recomputar/validar el sello historico; negativos permanentes para frontera y config; re-juicio Analista antes
  de cierre, maximo 2 iteraciones antes de escalar.

## Ultima actualizacion 2026-07-12 - Enfoque QA/checker workspace Notion OK/CERRABLE
- Enfoque QA/checker para workspace Notion registrado por Analista en commit `cc13651`
  (`review(notion): Analista QA enfoque`). Artefacto:
  `Area_comun/artifacts/ANALISTA-OPS-enfoque-notion-qa-checker-veredicto.md`; MSG rr a Arquitecto:
  `Area_comun/mailbox/open/MSG-20260712-Analista-to-Arquitecto-REVIEW-enfoque-notion-QA.md`.
- Ancla protocolo revisada `6ba22cdc3c24e99a0f7dca0aeb834e8cc8ea5c07`; instruccion canonica
  `MSG-20260712-Arquitecto-to-Analista-REQUEST-enfoque-notion.md`. Resultado: OK/CERRABLE como consenso de
  diseno, no como implementacion. Notion solo read-model del ledger; F-NOVA-01 exige cadena relacional
  SDD->objeto BD->caso de prueba->evidencia; todo campo gobernado requiere evento fuente con seq/actor/commit/hash.
- Gates: validate vivo EXIT 0; validate sin secretos en clon limpio EXIT 0; scan_domain_neutrality EXIT 0;
  scan_encoding EXIT 0; drift 0 `up_to_seq=4572`; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Residual declarado: Nova-Budget clean clone raiz `npm test` EXIT `-4058` por ausencia de `package.json`; no bloquea
  este REQUEST de diseno, pero no puede usarse como gate de cierre de producto.
- Incidencia propia: el commit `cc13651` llevo `Task-Id` y `Ops-Reason` separados por blank line; el gate lo marco
  rojo post-commit. No reescribir historia si ya aparece en `origin/main`; remediation en commit `4a0e057`: avanzar
  `COMMIT_TRAILERS.start_commit` a `cc13651` y reforzar la leccion de trailers contiguos. En el siguiente commit
  gobernado usar `git commit -m subject -m "Task-Id: none` + linea inmediata `Ops-Reason: ..."` o un archivo de
  mensaje, sin `-m` separado para cada trailer.

## Ultima actualizacion 2026-07-07 - Hallazgos #11/#12/#13 quality-data baseline CONFIRMADOS
- Hallazgos #11/#12/#13 QA baseline confirmados y registrados por Analista en commit `c523746`
  (`review(hallazgos): Analista confirms quality baseline 11-13`). Artefacto:
  `Area_comun/artifacts/ANALISTA-OPS-hallazgos11-12-13-quality-data-baseline-veredicto.md`; MSG rr a
  Arquitecto:
  `Area_comun/mailbox/open/MSG-20260707-Analista-to-Arquitecto-REVIEW-hallazgos11-12-13-quality-data-baseline-CONFIRMADO.md`.
- Ancla protocolo revisada `d0435bfb58d300613febe348d11bed4a2e827e70`; producto Nova-Budget en clon limpio
  `edbc037be8ce8297fbf308f611eef8c84aeccbf0`; instruccion canonica
  `MSG-20260706-Arquitecto-to-Analista-ACTION-hallazgos11-12-13-quality-data-baseline.md`.
- Resultado: CONFIRMADO / NO BLOQUEANTE / no reabrir TASK-0255. #11: gateway de anulacion CDP lee result-set
  con fallback de nombres y default silencioso `"A"`, mientras el harness SQL no ejercita el mismo camino.
  #12: falta test HTTP WebApplicationFactory para la familia `annul-preview`/`annul`. #13: el arch-test React
  omite `Annul_Availability_Certificate` aunque `App.tsx` lo contiene como literal descriptivo.
- SPEC-NOVA-P4-006 queda adecuada como fix-forward: restricciones 6i/6j/6k, criterios 10/11/12 y riesgo
  explicito cubren no repetir #11/#12/#13 en el miembro gobernado.
- Gates: validate vivo EXIT 0; validate sin secretos en clon limpio EXIT 0; scan_domain_neutrality EXIT 0;
  scan_encoding EXIT 0; drift 0 `up_to_seq=4395`; chain valid `checked_events=3723`; `protocol.config.json`
  byte-identico sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`;
  `dotnet test NOVA.sln --no-restore` EXIT 0; probe propio 8/8 EXIT 0. Residual declarado: `npm test` en raiz
  del producto limpio EXIT `-4058` por ausencia de `package.json`, no usado para refutar los hallazgos.
- Incidencia propia: el commit `c523746` llevo `Task-Id` y `Ops-Reason` separados por blank line, fuera del
  bloque final unico que parsea el gate. Como ya estaba en `origin/main` como ancestro de `b0b7235`, no reescribi
  historia: lo grandfathered en `44cf4f5` avanzando `COMMIT_TRAILERS.start_commit` a `c523746`. Leccion: trailers
  finales sin blank line entre claves; validar post-commit antes de cerrar/push.

## Ultima actualizacion 2026-07-07 - Hallazgo #10 50212 etiquetado cruzado CONFIRMADO con slip documental
- Hallazgo #10 QA confirmado y registrado por Analista en commit `1ecb74b`
  (`review(hallazgo10): Analista confirms 50212 cross-label`). Artefacto:
  `Area_comun/artifacts/ANALISTA-OPS-hallazgo10-50212-etiquetado-cruzado-veredicto.md`; MSG rr a Arquitecto:
  `Area_comun/mailbox/open/MSG-20260707-Analista-to-Arquitecto-REVIEW-hallazgo10-50212-etiquetado-cruzado-CONFIRMADO.md`.
- Ancla protocolo revisada `d33f005b4f8e973d78de4e3f0080292c97213fa0`; instruccion introducida en
  `a2657d548b89bde064d6456f18e55aeb743e88b9`; producto Nova-Budget en clon limpio
  `edbc037be8ce8297fbf308f611eef8c84aeccbf0`.
- Resultado: `BudgetProcedureProblemDetails.Map` es compartido por apropiacion, disponibilidad y anulacion;
  `50212` devuelve `RN-A01` disponibilidad/HTTP 409; `RN-01` solo cubre `50230 or 50231`. Clasificacion:
  QA WARNING-real no bloqueante porque `sqlErrorNumber` y HTTP 409 se conservan, pero titulo/businessRule quedan
  cruzados si 50212 emerge desde apropiacion.
- Salvedad canonica: no confirmo la atenuante "documentado con transparencia total" porque los HTML citados
  `docs/documentacion-tecnica/diccionario-datos.html` y `docs/documentacion-tecnica/log-cambios.html` no existen
  en `git ls-tree -r HEAD` del producto revisado. Recomendacion: registrar #10 y remediar/canonizar evidencia
  documental antes de usarla como atenuante.
- Gates: `dotnet test tests/NOVA.ArchitectureTests` EXIT 0 (10/10); probe propio de mapper EXIT 0; `npm test`
  raiz producto EXIT 1 con npm errno `-4058` por ausencia de `package.json`; validate vivo EXIT 0; validate sin
  secretos en clon limpio EXIT 0; domain EXIT 0; encoding EXIT 0; drift 0 `up_to_seq=4395`; chain valid
  `checked_events=3723`; `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.

## Ultima actualizacion 2026-07-06 - Hallazgo #14 tenant-isolation CONFIRMADO
- Hallazgo #14 quality-data Q2 confirmado y registrado por Analista en commit `003f813`
  (`review(hallazgo14): Analista confirms tenant isolation finding`). Artefacto:
  `Area_comun/artifacts/ANALISTA-OPS-hallazgo14-tenant-isolation-veredicto.md`; MSG rr a Arquitecto:
  `Area_comun/mailbox/open/MSG-20260706-Analista-to-Arquitecto-REVIEW-hallazgo14-tenant-isolation-CONFIRMADO.md`.
- Ancla protocolo revisada `aa38f18ff01fdd678350d59d2a3dc7bf729096ee`; producto Nova-Budget en clon limpio
  `edbc037be8ce8297fbf308f611eef8c84aeccbf0`. Resultado: `SqlAvailabilityAdjustmentGateway.GetBalancesAsync`
  y las lecturas de `SqlAvailabilityCertificateAnnulmentGateway` setean `SESSION_CONTEXT('tenant_id')` pero no
  filtran tenant; no hay evidencia versionada de RLS/vista que consuma `SESSION_CONTEXT`. SPEC-P4-006 6l/criterio
  13 cubre el fix-forward correcto.
- Gates: validate vivo EXIT 0; validate sin secretos en clon limpio EXIT 0; domain EXIT 0; encoding EXIT 0;
  drift 0 `up_to_seq=4351`; `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; `dotnet test NOVA.sln --no-restore`
  EXIT 0. Residual declarado: `npm test` raiz en producto EXIT `-4058` por ausencia de `package.json`, tratado
  como residual de gate transversal porque la ACTION canonica dice SIN PRODUCTO EN ALCANCE.
- Incidencia propia: el commit `003f813` omitio `Task-Id: none` y dejo solo `Ops-Reason`; el gate quedo rojo
  post-push. Remediado sin reescribir historia en `467b15b`, avanzando `COMMIT_TRAILERS.start_commit` a `0d3d182`
  y dejando leccion explicita: commits de coordinacion sin tarea requieren exactamente `Task-Id: none` + `Ops-Reason`
  en el bloque final.

## Ultima actualizacion 2026-07-06 - TASK-0246 informe/SPEC P4-006 NO-GO registrado
- TASK-0246 review documental del informe adversarial + SPEC-NOVA-P4-006: primera pasada hallo dos slips
  falsables: F-0246-INF-01 (informe decia 12 SPECs, inventario canonico 17) y F-0246-P4006-01 (P4-006
  referenciaba criterio 9 para auth; el correcto era criterio 6). Producto Nova-Budget N/A por instruccion
  canonica docs-only.
- Hub gates observados antes de la colision: validate vivo EXIT 0; clean clone hub validate EXIT 0;
  clean clone encoding EXIT 0; domain vivo EXIT 0; drift false up_to_seq=4256; chain valid checked_events=3584;
  `protocol.config.json` sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Colision: mientras preparaba el veredicto, Arquitecto corrigio los dos slips y luego registro el veredicto
  NO-GO original en `3734019` con el artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0246-informe-specs-veredicto.md` y MSG
  `Area_comun/mailbox/open/MSG-20260706-Analista-to-Arquitecto-REVIEW-TASK-0246-informe-specs-NOGO.md`.
  Mi commit intermedio `d43431f` termino commiteando la remediacion documental, no el artefacto; no revertir
  porque la remediacion es el fix canonico. Estado final de esta sesion: bloqueada por claim activo
  `CLAIM-ARQ-archive-nogo-0246-20260706` y drift/snapshot mismatch mientras Arquitecto archiva/rutea
  remediacion; no emitir nuevo OK hasta safe window y re-juicio sobre el REVIEW de remediacion.

## Ultima actualizacion 2026-07-04 - TASK-0249 F3.3 instrumentacion re-juicio 2 OK/CERRABLE
- TASK-0249 re-juicio 2/2 del fix-loop F-0249-02/F-0249-03: OK/CERRABLE. Veredicto en commit
  `17d64b8` (`review(TASK-0249): Analista OK instrumentation regate 2`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0249-f33-instrumentacion-rejuicio-2-veredicto.md`, MSG rr a
  Arquitecto
  `Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0249-f33-instrumentacion-rejuicio-2-OK.md`.
  Ancla canonica revisada: protocolo REVIEW HEAD `7be5cf1`; implementacion remediada `fc412b8`; producto
  N/A por instruccion canonica ("Producto commit citable: NINGUNO", alcance 100% hub/instancia).
- Resultado: F-0249-02 cerrado por comportamiento; payloads solo-parciales `prompt_tokens/completion_tokens`,
  JSON OpenAI-like, lineas separadas y total no cumulativo fueron rechazados sin escribir CSV, mientras los
  aliases cumulativos explicitos materializaron 321/322/323/324. F-0249-03 cerrado: dos pares con deltas
  -20/+30 conservaron mediana 5.0 al invertir el orden de filas. Regresiones previas tambien pasan:
  determinismo, defect.reported, manual.intervention overhead-only, Q4/Q5 sin causalidad, event-log
  off-by-default.
- Gates: test_instrumentacion EXIT 0 (7 tests), py_compile EXIT 0, payloads propios EXIT 0, validate clean/live
  EXIT 0, encoding clean/live EXIT 0, domain clean/live EXIT 0, drift false `up_to_seq=3865`, chain valid
  `checked_events=3193`, `protocol.config.json` byte-identico contra `fc412b8`, sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
  Residual: producto Nova-Budget no ejecutado porque la instruccion canonica lo excluye.

## Ultima actualizacion 2026-07-04 - TASK-0249 F3.3 instrumentacion CAMBIO-REQUERIDO
- TASK-0249 gate formal de F3.3 instrumentacion del estudio: CAMBIO-REQUERIDO / NO CERRABLE. Veredicto en
  commit `f9bce44` (`review(TASK-0249): Analista blocks F3.3 instrumentation`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0249-f33-instrumentacion-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0249-f33-instrumentacion-NOGO.md`.
  Ancla canonica revisada: protocolo REVIEW HEAD `2c6e847908416dbf41d7a14faa521df902fa8c1c`; implementacion
  citada `a32ee61`; producto citable ninguno por instruccion canonica.
- Resultado: F-0249-01 bloquea porque `python personal/Arquitecto/TFM-medicion/instrumentacion_estudio/test_instrumentacion.py`
  en clon limpio sale EXIT 1 por `FileNotFoundError` buscando
  `personal/Arquitecto/TFM-medicion/corpus/medicion/schema_medicion.json`, ruta no commiteada en el ancla.
  Por tanto no queda probado canonicamente cost.attributed, defect.reported, manual.intervention ni el event-log
  off-by-default. Gates hub en el ancla pasan: validate/encoding/domain EXIT 0, drift false `up_to_seq=3859`,
  `protocol.config.json` byte-identico contra `a32ee61`.
- Fix-loop esperado: Codex remedia fixtures/rutas reproducibles y pide re-juicio; maximo 2 iteraciones antes de
  escalar si sobrevive la misma clase de hallazgo.

## Ultima actualizacion 2026-07-04 - TASK-0245 re-juicio 2 session-watchdogs OK/CERRABLE
- TASK-0245 re-juicio 2 con ancla corregida sin producto en alcance: OK/CERRABLE. Veredicto en commit
  `2035c62` (`review(TASK-0245): Analista OK watchdog regate`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0245-skill-watchdogs-rejuicio-2-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0245-rejuicio-2-OK.md`.
  Ancla REVIEW corregida `01cf2d3`; re-juicio 1 `a1b944d`; remediacion `75fd96f`.
- Resultado: retiro el bloqueo de producto porque Arquitecto corrigio canonicamente que TASK-0245 es 100% hub.
  F-0245-01 queda cerrado; pasan `test_skills_loader`, `examples/skills_loader_cases`, probe propia habilitando
  solo `session-watchdogs`, `new_instance` + loader probe, validate/encoding/domain, drift false `up_to_seq=3804`
  y `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Residual declarado: Nova-Budget root `npm test` queda fuera de este cierre por ancla corregida; si se quiere
  convertirlo en contrato general requiere tarea separada de producto o correccion del monorepo.

## Ultima actualizacion 2026-07-04 - TASK-0245 re-juicio 1 session-watchdogs CAMBIO-REQUERIDO
- TASK-0245 re-juicio 1 de F-0245-01: F-0245-01 queda CERRADO por comportamiento en clon limpio, pero
  mantuve CAMBIO-REQUERIDO / NO CERRABLE bajo el contrato de ejecucion porque el gate producto obligatorio
  no queda canonico/verde. Veredicto en commit `a1b944d` (`review(TASK-0245): Analista blocks watchdog
  regate`), artefacto `Area_comun/artifacts/ANALISTA-TASK-0245-skill-watchdogs-rejuicio-1-veredicto.md`,
  MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0245-rejuicio-1-NOGO.md`.
  Ancla protocolo REVIEW `d5f22eb`; remediacion `75fd96f`; HEAD limpio pedido `7a5dfe7`.
- Resultado hub: `python scripts/test_skills_loader.py` EXIT 0 en clon limpio; `examples/skills_loader_cases`
  EXIT 0 con AC7; probe propia habilitando solo `session-watchdogs` EXIT 0; `new_instance` + loader probe
  EXIT 0; validate/encoding/domain EXIT 0; drift false `up_to_seq=3804`; `protocol.config.json`
  byte-identico contra `75fd96f`, `7a5dfe7`, `d5f22eb`, sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Bloqueo remanente: la orden de ejecucion exigia Nova-Budget checkout del commit citado + `npm test` en raiz
  gateado por EXIT; no habia commit de producto citado, y el control en clon limpio sobre HEAD local
  `e3a03a8cf3334c2a84bf54e964319dd08b953b45` dio EXIT `-4058` por ausencia de `package.json`.
  `apps/nova-web` si paso `npm ci` + `npm test` (1/1), pero no lo trate como sustituto canonico sin instruccion
  corregida. Fix-loop: Arquitecto corrige gate/ancla producto o declara explicitamente alcance sin producto
  raiz; re-juicio 2 antes de cierre.

## Ultima actualizacion 2026-07-04 - TASK-0245 session-watchdogs CAMBIO-REQUERIDO
- TASK-0245 review formal de skill neutral exportable `session-watchdogs`: CAMBIO-REQUERIDO / NO CERRABLE.
  Veredicto canonico en commit `28532b0` (`review(TASK-0245): Analista blocks watchdog skill gate`),
  artefacto `Area_comun/artifacts/ANALISTA-TASK-0245-skill-watchdogs-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0245-skill-watchdogs-NOGO.md`.
  Ancla protocolo REVIEW `984361d`; implementacion citada `6a1cd56`; no hubo producto citable por instruccion
  canonica (alcance hub `skills/`, `scripts/new_instance.py`, `examples/`).
- Resultado: skill, registro off-by-default, parametrizacion sin literales del dogfooding, export via
  `new_instance`, loader probe en instancia generada y `examples/skills_loader_cases` PASAN. Bloqueo:
  `python scripts/test_skills_loader.py` en clon limpio sale EXIT 1 por `event-state.runtime.json` ausente,
  aunque el handoff lo declaro PASS.
- Gates: validate/encoding/domain clean clone EXIT 0; examples/skills_loader_cases EXIT 0; new_instance+loader
  probe EXIT 0; drift false `up_to_seq=3794`; chain valid `checked_events=3122`; `protocol.config.json`
  byte-identico sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Fix-loop:
  hacer reproducible el gate de loader o acotarlo canonicamente y pedir re-juicio.

## Ultima actualizacion 2026-07-04 - TASK-0246 baseline SPECs re-juicio 2 OK/CERRABLE
- TASK-0246 re-juicio 2 de baseline de 14 SPECs NOVA: OK/CERRABLE con alcance canonico 100% documental.
  Veredicto canonico en commit `a8b5eb7` (`review(TASK-0246): Analista OK specs baseline regate 2`),
  artefacto `Area_comun/artifacts/ANALISTA-TASK-0246-specs-baseline-rejuicio-2-veredicto.md`, MSG rr a
  Arquitecto
  `Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0246-specs-baseline-rejuicio-2-OK.md`.
  Ancla protocolo revisada `1ec4582`; instruccion REVIEW `e328524`; remediacion documental `386dca7`.
- Resultado: 14 SPECs, `cache-confound`, sandbox P4-004 (`sandbox`, `14-jul`, `<=14-jul`),
  q4_membership, correlation+task_id y checker_formal=0 PASAN. No ejecute gate de producto porque la
  instruccion canonica corregida declara alcance documental y no cita commit de Nova-Budget.
- Gates: validate vivo EXIT 0; validate/encoding/domain secretless clean clone EXIT 0; scan_domain_neutrality
  EXIT 0; scan_encoding EXIT 0; drift false `up_to_seq=3774`; chain valid `checked_events=3102`;
  `protocol.config.json` byte-identico contra `386dca7`, `e328524` y `2098e96`, sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Residual: producto Nova-Budget y BD quedan fuera de este cierre; si se requieren, deben ir en hilo separado
  con commit/gate canonico citable.

## Ultima actualizacion 2026-07-04 - TASK-0246 baseline SPECs re-juicio 1 CAMBIO-REQUERIDO
- TASK-0246 re-juicio 1 de baseline de 14 SPECs NOVA: CAMBIO-REQUERIDO / NO CERRABLE por gate producto
  no cerrable. Veredicto canonico en commit `c909a6d` (`review(TASK-0246): Analista blocks specs baseline
  regate`), artefacto `Area_comun/artifacts/ANALISTA-TASK-0246-specs-baseline-rejuicio-1-veredicto.md`,
  MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0246-specs-baseline-rejuicio-1-NOGO.md`.
  Ancla protocolo/instruccion `2098e96`; remediacion specs `386dca7`; producto no citado por la instruccion,
  control en clon limpio con HEAD local `e3a03a8cf3334c2a84bf54e964319dd08b953b45`.
- Resultado documental: F-0246-BG-01 cache-confound PASA en las 14 SPECs (`missing_cache=[]`);
  F-0246-BG-02 PASA en P4-004 (`sandbox`, `14-jul`, `<=14-jul` presentes); q4_membership, correlation,
  task_id y checker_formal=0 presentes en la familia.
- Gates: validate vivo EXIT 0; validate/encoding/domain secretless clean clone EXIT 0; scan_domain_neutrality
  EXIT 0; scan_encoding EXIT 0; drift false `up_to_seq=3763`; chain valid `checked_events=3091`;
  `protocol.config.json` byte-identico contra `386dca7` y `2098e96`, sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Bloqueo: la orden de ejecucion exigia clonar Nova-Budget, checkout del commit citado y correr `npm test`
  gateando por EXIT; no habia commit de producto citado, y `npm test` en raiz del clon limpio `e3a03a8` salio
  EXIT `-4058` por ausencia de `package.json`. `apps/nova-web` si paso `npm ci` + `npm test` (1/1), pero no
  lo trate como sustituto canonico sin instruccion corregida. Fix-loop: Arquitecto corrige gate/ancla producto
  o agrega root `package.json`; re-juicio antes de cierre.

## Ultima actualizacion 2026-07-04 - TASK-0246 baseline SPECs pre-Sprint 1 CAMBIO-REQUERIDO
- TASK-0246 gate baseline de 14 SPECs NOVA pre-Sprint 1: CAMBIO-REQUERIDO / NO CERRABLE. Veredicto canonico
  en commit `a43c189` (`review(TASK-0246): Analista blocks specs baseline`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0246-specs-baseline-pre-sprint1-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0246-specs-baseline-NOGO.md`.
  Ancla protocolo revisada `45ab4fc`; instruccion REVIEW `673c259`.
- Gates: validate vivo EXIT 0; validate secretless clean clone EXIT 0; scan_domain_neutrality EXIT 0;
  scan_encoding EXIT 0; drift false `up_to_seq=3763`; chain valid `checked_events=3091`;
  `protocol.config.json` byte-identico contra `673c259` y `45ab4fc`, sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Producto Nova-Budget: la instruccion no cito commit de producto; probe de control en clon limpio uso HEAD local
  `e3a03a8cf3334c2a84bf54e964319dd08b953b45`. `npm test` raiz EXIT -4058 por falta de `package.json`;
  `apps/nova-web/npm test` antes de deps EXIT 1 por `tsc` ausente; `apps/nova-web/npm ci` EXIT 0 y `npm test`
  posterior EXIT 0 (1/1).
- Resultado: conteo 14 SPECs, formato NOVA-SPEC-T-001, q4_membership, citas BD plausibles/F-NOVA-01, aislamiento
  y neutralidad pasan. Bloqueantes: F-0246-BG-01 `cache-confound` falta en P2-003, P2-004, P3-001..005, P4-004
  y P6-003; F-0246-BG-02 P4-004 no declara `sandbox<=14-jul` aunque es mutador P4.x. Residual: `deuda front`
  no aparece textual en las 14 SPECs, declarado como riesgo no bloqueante salvo que Arquitecto lo quiera por SPEC.

## Ultima actualizacion 2026-07-04 - TASK-0248 re-juicio 2 OK/CERRABLE
- TASK-0248 re-juicio 2 con gate producto corregido por Arquitecto: OK/CERRABLE. Veredicto canonico en commit
  `c175b66` (`review(TASK-0248): Analista OK codegen triage regate`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0248-codegen-triage-rejuicio-2-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0248-rejuicio-2-OK.md`.
  Ancla protocolo/instruccion `543b09c`; remediacion protocolo `ce1a549`; producto canonico de instruccion
  `4ea82711e3c5354c2f126cfdff225226de6211c9`.
- Gates: validate vivo EXIT 0; validate secretless clean clone EXIT 0; scan_domain_neutrality EXIT 0;
  scan_encoding EXIT 0; skills_loader_cases EXIT 0; test_skills_loader EXIT 0; probe propio loader/contrato
  EXIT 0; drift false `up_to_seq=3749`; chain valid `checked_events=3077`; `protocol.config.json` sin diff
  contra `543b09c`, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Producto Nova-Budget en clon limpio checkout `4ea8271`: `dotnet build NOVA.sln` EXIT 0; `dotnet test
  NOVA.sln --no-build` EXIT 0 (9/9); `apps/nova-web/npm ci` EXIT 0; `apps/nova-web/npm test` EXIT 0. El
  `npm test` en raiz queda fuera del gate canonico corregido porque no hay `package.json` raiz por diseno.
- Resultado: F-0248-01 loader gobernado PASA; F-0248-02 contrato `{camino, razon, gate, banderas}` y familia
  de banderas PASA; F-0248-03 producto PASA con gate corregido. Residuales no bloqueantes: warning NU1903 de
  `Microsoft.OpenApi`; handoff citaba `af790be` pero instruccion canonica cita `4ea8271`.

## Ultima actualizacion 2026-07-04 - TASK-0248 re-juicio 1 CAMBIO-REQUERIDO
- TASK-0248 fix-loop 1/2 codegen-triage: CAMBIO-REQUERIDO / NO CERRABLE. Veredicto canonico en commit
  `be69bfd` (`review(TASK-0248): Analista blocks codegen triage regate`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0248-codegen-triage-rejuicio-1-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0248-rejuicio-1-NOGO.md`.
  Ancla protocolo/instruccion `07da113`; parent vivo al commitear `43dff28`; remediacion protocolo `ce1a549`;
  producto citado `4ea82711e3c5354c2f126cfdff225226de6211c9` (handoff citaba `af790be`, discrepancia declarada).
- Gates: validate vivo EXIT 0; validate secretless clean clone EXIT 0; scan_domain_neutrality EXIT 0;
  scan_encoding EXIT 0; loader_cases EXIT 0; probe loader propio EXIT 0; drift false `up_to_seq=3728`;
  chain valid `checked_events=3056`; `protocol.config.json` byte-identico contra HEAD, sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Resultado: F-0248-01 loader gobernado cerrado; F-0248-02 contrato `{camino, razon, gate, banderas}` cerrado.
  Bloqueo F-0248-R1: en clon limpio Nova-Budget checkout `4ea8271`, `npm test` en raiz sale `-4058` por falta
  de `package.json`; `apps/nova-web` pasa solo tras `npm ci` + `npm test`. Fix-loop esperado: remediar gate raiz
  o corregir canonicamente la instruccion para acotar el gate a `apps/nova-web`.

## Ultima actualizacion 2026-07-04 - TASK-0246 re-gate re-juicio 1 DD OK/CERRABLE
- TASK-0246 fix-loop 1/2 del re-gate consolidado DD-01/DD-02/DD-03: OK/CERRABLE. Veredicto canonico en
  commit `b0ac5ad` (`review(TASK-0246): Analista OK DD regate rejuicio1`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0246-regate-rejuicio-1-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0246-regate-rejuicio-1-OK.md`.
  Ancla protocolo/instruccion `e2d2987`; remediacion `34b7dac`; producto control
  `e7c6da482a1e819507af37de77b9cd46712fb8c8`.
- Gates: Zeus-protocol clean clone `npm test` EXIT 0 (112 tests, 90 pass, 22 skipped); validate vivo EXIT 0;
  validate secretless clean clone EXIT 0; scan_domain_neutrality EXIT 0; scan_encoding EXIT 0; drift false
  `up_to_seq=3670`; chain valid `checked_events=2998`; `protocol.config.json` byte-identico contra HEAD,
  `34b7dac` y `v1.18.0`, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Resultado: F-0246-DD01-STALE cerrado (P3-001 riesgo B-05 ya dice Confirmado por el Operador para Sprint 1);
  F-0246-DD02-MISSING-AC cerrado (P3-003 seccion 7 tiene AC 9 ejecutable para objeto <=19 chars -> 400
  ProblemDetails sin invocar aprobacion BD); DD-03 conserva N/A y prohibicion del centinela legacy 0. Residual:
  no re-auditoria THROW por alcance documental.

## Ultima actualizacion 2026-07-04 - TASK-0246 re-gate consolidado DD-01/DD-02/DD-03 CAMBIO-REQUERIDO
- TASK-0246 re-gate documental de `Area_comun/specs/nova/` tras DD-01/DD-02/DD-03 horneadas:
  CAMBIO-REQUERIDO / NO CERRABLE. Veredicto canonico en commit `a405def`
  (`review(TASK-0246): Analista blocks consolidated DD regate`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0246-regate-consolidado-dd-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0246-regate-consolidado-dd-NOGO.md`.
  Ancla protocolo/instruccion `4e42d64`; horneado DD `01f05db`; THROW/db_verified_at previo OK `070b533`;
  producto control `e7c6da482a1e819507af37de77b9cd46712fb8c8`.
- Gates: Zeus-protocol clean clone `npm test` EXIT 0 (112 tests, 90 pass, 22 skipped); validate vivo EXIT 0;
  validate secretless clean clone EXIT 0; scan_domain_neutrality EXIT 0; scan_encoding EXIT 0; drift false
  `up_to_seq=3670`; chain valid `checked_events=2998`; `protocol.config.json` byte-identico contra HEAD,
  `01f05db`, `070b533` y `v1.18.0`, sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Bloqueantes: P3-001 conserva en riesgos `Supuesto temporal declarado (campo 2)`, contradiciendo DD-01
  confirmado; P3-003 contiene DD-02 min 20 chars en alcance y restriccion 6d, pero no hay Given/When/Then
  explicito en `## 7. Criterios de aceptacion` para objeto `<20` -> 400 ProblemDetails. DD-03 pasa con
  `N/A` declarada y sin centinela `0`. Fix-loop esperado: remediacion documental y re-juicio antes de cierre.

## Ultima actualizacion 2026-07-03 - TASK-0246 THROW triggers OK/CERRABLE
- TASK-0246 verificacion ampliada por definiciones de triggers/catalogos/numeracion: OK/CERRABLE para
  `db_verified_at` P3-001..005. Veredicto canonico en commit `070b533`
  (`review(TASK-0246): Analista OK throw triggers`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0246-throw-audit-triggers-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0246-throw-audit-triggers-OK.md`.
  Ancla protocolo `eedc3ea`; instruccion REQUEST `0506b4e`; remediacion `5669665`; producto control
  `e7c6da482a1e819507af37de77b9cd46712fb8c8`.
- Gates: Zeus-protocol clean clone `npm test` EXIT 0 (112 tests, 90 pass, 22 skipped); validate vivo EXIT 0;
  validate secretless clean clone EXIT 0; scan_domain_neutrality EXIT 0; scan_encoding EXIT 0; drift false
  `up_to_seq=3643`; chain valid `checked_events=2971`; `protocol.config.json` byte-identico contra
  `5669665`, `0506b4e`, `eedc3ea` y `v1.18.0`, sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Resultado: P3-001 50054/50057-50062, P3-002 50066-50068/50076/50210-50212/50220-50223,
  P3-003 50091-50094/50210-50212/50220-50223, P3-004 50116-50121/50210-50212/50220-50223,
  y P3-005 50188-50190/54257 existen en los objetos fuente declarados. Residual: juicio readonly por
  definicion de objetos, sin mutaciones BD.

## Ultima actualizacion 2026-07-03 - TASK-0246 THROW re-atribuido CAMBIO-REQUERIDO
- TASK-0246 re-audit opcion (b) transitive sobre commit `49689c4`: CAMBIO-REQUERIDO / NO CERRABLE por omision
  puntual de `50212` en `throw_source` de P3-003/P3-004. Veredicto canonico en commit `b38722f`
  (`review(TASK-0246): Analista blocks throw reattribution`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0246-throw-audit-reatribuido-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0246-throw-audit-reatribuido-NOGO.md`.
  Ancla protocolo / REQUEST `2a0e89f`; remediacion `49689c4`; producto control
  `e7c6da482a1e819507af37de77b9cd46712fb8c8`.
- Gates: Zeus-protocol clean clone `npm test` EXIT 0 (112 tests, 90 pass, 22 skipped); validate vivo EXIT 0;
  validate secretless clean clone EXIT 0; scan_domain_neutrality EXIT 0; scan_encoding EXIT 0; drift false
  `up_to_seq=3643`; chain valid `checked_events=2971`; `protocol.config.json` byte-identico contra `49689c4`,
  HEAD y `v1.18.0`, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Resultado: P3-001/P3-002/P3-005 pasan re-atribucion, y P3-003/P3-004 pasan en rangos directos/numeracion/triggers
  declarados. Bloqueo remanente: ambas SPEC citan `THROW 50212` en restricciones pero `throw_source` no lo lista;
  SQL readonly confirma `50212` en `trg_commitment__validate_open_year` y `trg_obligation__validate_open_year`.
  Fix-loop esperado: Arquitecto agrega esa fuente y pide re-juicio antes de cerrar `db_verified_at`.

## Ultima actualizacion 2026-07-03 - TASK-0246 THROW audit procs CAMBIO-REQUERIDO
- TASK-0246 audit aditivo de THROW P3-001..005: CAMBIO-REQUERIDO / NO CERRABLE para el gancho
  `db_verified_at` de F-NOVA-01. Veredicto canonico en commit `af461a7`
  (`review(TASK-0246): Analista blocks throw audit procs`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0246-throw-audit-procs-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0246-throw-audit-procs-NOGO.md`.
  Ancla protocolo / REQUEST `5fdfb39edc2c292fb818e2bd4bfa1f567129525b`; producto control
  `e7c6da482a1e819507af37de77b9cd46712fb8c8`.
- Gates: Zeus-protocol clean clone `npm test` EXIT 0 (112 tests, 90 pass, 22 skipped); validate vivo EXIT 0;
  validate secretless clean clone EXIT 0; scan_domain_neutrality EXIT 0; scan_encoding EXIT 0; drift false
  `up_to_seq=3643`; chain valid `checked_events=2971`; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Bloqueante nuevo: los 5 procs `Budget.Approve_*` existen, pero `OBJECT_DEFINITION` directo no contiene todos
  los THROW citados por las SPECs. P3-001 falta `50054,50057-50062`; P3-002 falta `50066-50068,50076,50210-50212,50220-50223`;
  P3-003 falta `50091-50094,50210,50211`; P3-004 falta `50116-50121,50210,50211`; P3-005 falta
  `50188-50190,54257`. Si Arquitecto acepta semantica transitive, debe documentar `Approve_* -> proc llamado -> THROW`
  con evidencia BD antes de re-juicio.

## Ultima actualizacion 2026-07-03 - TASK-0246 NOVA-DEV lote specs CAMBIO-REQUERIDO
- TASK-0246 lote NOVA-DEV Sprint 1: CAMBIO-REQUERIDO / NO CERRABLE. Veredicto canonico en commit
  `9a2c211` (`review(TASK-0246): Analista requires nova dev spec fixes`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0246-nova-dev-lote-specs-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0246-nova-dev-lote-specs.md`.
  Ancla protocolo `acab21dc642474f9125ec5c0c6a00547c5990e4b`; producto control
  `e7c6da482a1e819507af37de77b9cd46712fb8c8` (la instruccion no cito commit de producto nuevo).
- Gates: Zeus-protocol clean clone `npm test` EXIT 0 (112 tests, 90 pass, 22 skipped); hub validate con
  secretos EXIT 0; clean clone sin `secrets/` validate EXIT 0; scan_domain_neutrality EXIT 0; scan_encoding
  EXIT 0; drift false `up_to_seq=3643`; chain valid `checked_events=2971`; `protocol.config.json`
  byte-identico contra `acab21d`, git blob hash `70d4c027a35b9d7d406bdfbe1cfcd427f203fc14`, SHA256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Bloqueantes: F-0246-01 `q4_membership` ausente en `SPEC-NOVA-P3-001`, `SPEC-NOVA-P3-002`,
  `SPEC-NOVA-P3-003`; F-0246-02 `SPEC-NOVA-P4-004` pide THROW `50256` y rango `50252-50255`, pero
  `Budget.Apply_Obligation_Adjustment` real emite `50265` para efecto distinto de reintegro y no contiene
  `50254` ni `50256`. Residual: procs `Get_*_List` faltan en BD pero estan declarados como "a crear"; no los
  use como bloqueo salvo que Arquitecto los trate como cita de objeto existente.

## Ultima actualizacion 2026-07-03 - TASK-0234 re-juicio 2/2 OK/CERRABLE
- TASK-0234 F2.5 runbook onboarding remoto, fix-loop 2/2: OK/CERRABLE. Veredicto canonico en commit
  `cf2f845` (`review(TASK-0234): Analista OK runbook rejuicio2`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0234-runbook-onboarding-rejuicio2-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0234-rejuicio2-OK.md`.
  Ancla REVIEW `20f2d75`; remediacion doc-only `d7804ac`; producto control
  `e7c6da482a1e819507af37de77b9cd46712fb8c8`.
- Gates: Zeus-protocol clean clone `npm test` EXIT 0 (112 tests, 90 pass, 22 skipped); hub validate con
  secretos EXIT 0; clean clone sin `secrets/` validate/encoding/neutrality EXIT 0; drift false
  `up_to_seq=3605`; `protocol.config.json` byte-identico entre `d7804ac`, HEAD y tag `c9a4423`, blob
  `81cf406e...`, canonical stdin hash `70d4c027...`, SHA256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Resultado: F-0234-01 cerrado. `tx-claim.json` parsea con claim acquire + ready->claimed + claimed->in_progress;
  `tx-deliver.json` parsea con in_progress->in_review + claim release con scope; ejemplos sustituidos de handoff
  y mailbox son validator-valid; cierre declara reviewer para `in_review->review_approved` e implementer para
  `review_approved->done`. Residual no bloqueante: employee-run real queda como replica posterior, fuera de
  TASK-0234.

## Ultima actualizacion 2026-07-03 - TASK-0234 re-juicio runbook fix-loop 1/2 NO-GO
- TASK-0234 F2.5 runbook onboarding remoto, fix-loop 1/2: CAMBIO-REQUERIDO / NO CERRABLE. Veredicto
  canonico en commit `b10bffc` (`review(TASK-0234): Analista keeps runbook NOGO`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0234-runbook-onboarding-rejuicio-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0234-rejuicio-NOGO.md`.
  Ancla REVIEW `9e90a02`; remediacion revisada `645cb78`; entrega previa `64d44ad`; producto control
  `e7c6da482a1e819507af37de77b9cd46712fb8c8`; Aegis para rutas F2.3/F2.2
  `814365a702ff45752bb68f7b68b9506b41ffafa4`.
- Gates: Zeus-protocol clean clone `npm test` EXIT 0 (112 tests, 90 pass, 22 skipped); hub validate con
  secretos EXIT 0; clean clone sin `secrets/` validate/encoding/neutrality EXIT 0; drift false
  `up_to_seq=3605`; `protocol.config.json` byte-identico entre `645cb78` y HEAD, blob
  `70d4c027a35b9d7d406bdfbe1cfcd427f203fc14`, SHA256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Resultado: F-0234-02 mayormente cerrado (rutas/comandos F2.3/F2.2 existen; F2.3 test EXIT 0). F-0234-01
  sigue abierto en alcance reducido: `tx-claim.json` ya es concreto, pero `tx-deliver.json` queda como
  pseudo-lista, falta ejemplo minimo de handoff/mailbox validator-valid y falta comando/payload o aclaracion de
  ownership para cierre `review_approved->done`. Fix-loop esperado iteracion 2/2 antes de cierre; maximo 2
  iteraciones antes de operador. Residual: e2e F2.2 en clon Aegis con bare tmp y `--keep-workdir` no completo
  antes de 304 s y los procesos hijos fueron detenidos; no se uso como bloqueo doc-only, pero queda como riesgo
  operativo si ese comando pretende ser smoke test rapido.

## Ultima actualizacion 2026-07-03 - TASK-0233 e2e distribuida OK
- TASK-0233 F2.2 e2e distribuida Aegis: OK/CERRABLE. Veredicto canonico en commit
  `c228c34` (`review(TASK-0233): Analista OK distributed e2e`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0233-e2e-distribuida-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0233-e2e-distribuida-OK.md`.
  Ancla protocolo REVIEW `9fb94e0d3c37bab09c1c544e3952df9385c6b9a4`; protocolo HEAD revisado
  `ed117eb2037ba6ac01365f91326192fbce10965f`; Aegis entrega
  `814365a702ff45752bb68f7b68b9506b41ffafa4`; producto control Zeus-protocol
  `e7c6da482a1e819507af37de77b9cd46712fb8c8`.
- Gates: clean clone Zeus-protocol `npm test` EXIT 0 (112 tests, 90 pass, 22 skipped); clean clone Aegis
  `py_compile` EXIT 0, `test_distributed_git_harness.py` EXIT 0, `distributed_e2e_task_cycle.py` con bare
  remoto tmp EXIT 0. Ciclo propio: register `236bb010`, claim `8e1ba0c4`, delivery `529e947a`, review
  `2787b117`, done `1b80b7f2`; `claim_visible_in_other_clone_after_pull=true`; final `TASK-9233` done.
  Aegis clone gates validate/encoding/neutrality EXIT 0, drift false `up_to_seq=3470`.
- Hub vivo y clean validate/encoding/neutrality EXIT 0; drift false `up_to_seq=3583`; `protocol.config.json`
  byte-identico contra tag `c9a4423`, SHA256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Probe negativo de remoto bajo el hub
  fallo cerrado EXIT 1 antes de escribir. Residuales no bloqueantes: F2.2 no prueba agente no-constructor
  en frio (F2.5/TASK-0234); `--keep-workdir` no conserva workdir de debug de forma fiable.

## Ultima actualizacion 2026-07-03 - TASK-0232 harness distribuido OK
- TASK-0232 F2.3 harness distribuido Aegis: OK/CERRABLE. Veredicto canonico en commit
  `7547972` (`review(TASK-0232): Analista OK distributed harness`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0232-harness-distribuido-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0232-harness-distribuido-OK.md`.
  Ancla protocolo REVIEW `4238f45244d2d5f8cb6107591e7f8fbeaff1da08`; entrega Codex `1b6c7f5`;
  instancia Aegis `82e49f5842f9a9b76b1844dc433f56896f5db430`; producto control Zeus-protocol
  `e7c6da482a1e819507af37de77b9cd46712fb8c8`; remoto privado vivo
  `D:/Agentes/Zeus/remotes/Aegis-task0232b.git` main `b2b10b75c44833cf00ff56f1eb1b8c73dccaf2be`.
- Gates: clean clone Zeus-protocol `npm test` EXIT 0 (112 tests, 90 pass, 22 skipped); clean clone Aegis
  `python scripts/test_distributed_git_harness.py` EXIT 0; harness propio con remoto tmp EXIT 0, claim visible
  true, submit_seq 3458, pushed commit `ec29514337c3c00326bda69b6a2133c3b916098e`; Aegis validate/encoding/
  neutrality EXIT 0, drift false `up_to_seq=3458` en clon y `3457` en vivo; hub vivo y clean validate/encoding/
  neutrality EXIT 0, drift false `up_to_seq=3555`; `protocol.config.json` byte-identico contra tag `c9a4423`,
  SHA256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Resultado: pull->write->push inmediato, claim visible en clone B tras pull, ventana segura, remoto privado no
  heredado del hub y sin repos Nova-X/Engram creados. Residuales no bloqueantes: secreto event-auth temporal no
  trackeado en clones; claim de prueba activo solo en remoto privado de evidencia.

## Ultima actualizacion 2026-07-03 - TASK-0230 Aegis fix-loop 1 OK
- TASK-0230 DECISION-0085 Aegis fix-loop 1: OK/CERRABLE. Veredicto canonico en commit
  `2187b64` (`review(TASK-0230): Analista OK Aegis fixloop`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0230-aegis-fixloop1-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0230-aegis-fixloop1-OK.md`.
  Ancla protocolo `5554ef64a2310290e6f5efa797a5ceba099c6237`; instruccion REVIEW `bb15212`;
  producto `D:/Agentes/Zeus/Zeus-protocol` commit `e7c6da482a1e819507af37de77b9cd46712fb8c8`;
  instancia `D:/Agentes/Zeus/NOVA/Aegis` commit `518b2e58efeb6ae084fa43f0cdee0c7de63f5d35`;
  source tag `v1.18.0` -> `c9a442354bb5002b4df3a21e581ef1e891029c58`.
- Gates: clean clone producto `npm test` EXIT 0 (112 tests, 90 pass, 22 skipped); payload propio
  `createNewInstance` EXIT 0 para dry-run pin `v1.18.0`, write real en tmp, destino existente, ref
  inexistente, nombres invalidos y DoR feature/product; hub vivo y clean validate/encoding/neutrality EXIT 0,
  drift false `up_to_seq=3532`; Aegis validate/encoding/neutrality EXIT 0, drift false `up_to_seq=3457`;
  `protocol.config.json` sin diff contra tag en hub y Aegis.
- Resultado: F-0230-AEGIS-01 cerrado porque el handoff vigente nombra `aegis@NOVA/Aegis` como identidad final
  y deja `nova-budget` solo como bootstrap historico; F-0230-AEGIS-02 cerrado porque
  `operatingProfile.arm=nova-suite`. Residual no bloqueante: historico/eventos pueden retener `nova-budget`
  como provenance, no identidad viva.

## Ultima actualizacion 2026-07-03 - TASK-0230 Aegis re-gate NO-GO
- TASK-0230 DECISION-0085 Aegis re-gate: CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en commit
  `525b73e` (`review(TASK-0230): Analista blocks Aegis regate`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0230-aegis-regate-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0230-aegis-NOGO.md`.
  Ancla protocolo HEAD `5f385b5`, instruccion `2a68508`, re-deliver `89b15d1`; producto
  `D:/Agentes/Zeus/Zeus-protocol` commit `e7c6da4`; instancia `D:/Agentes/Zeus/NOVA/Aegis` commit
  `ab2b6a2335c5cdb973a77bc955010dfce2bd7dce`; source tag `v1.18.0` -> `c9a4423`.
- Gates: clean clone producto `npm test` EXIT 0 (112 tests, 90 pass, 22 skipped); payload propio
  `createNewInstance` EXIT 0 para dry-run pin `v1.18.0`, write real en tmp, destino existente, ref
  inexistente, nombres invalidos y DoR feature/product. Hub vivo y clean: validate/encoding/neutrality
  EXIT 0, drift false `up_to_seq=3507`, `protocol.config.json` byte-identico a tag. Aegis:
  validate/encoding/neutrality EXIT 0, drift false `up_to_seq=3457`, config byte-identica.
- Bloqueantes falsables: F-0230-AEGIS-01 el handoff vigente aun cita `D:/Agentes/Zeus/nova-budget`;
  F-0230-AEGIS-02 `instance.profile.json` conserva `operatingProfile.arm=budget` aunque Aegis queda como
  instancia-metodologia neutral de suite bajo DECISION-0085. Fix-loop: Codex remedia, gates afectados,
  re-juicio Analista antes de cierre; maximo 2 iteraciones antes de operador.

## Ultima actualizacion 2026-07-03 - TASK-0241 taxonomia OK
- TASK-0241 taxonomia D1-D4 + S1-S7: OK/CERRABLE. Veredicto en
  `Area_comun/artifacts/ANALISTA-TASK-0241-taxonomia-veredicto.md`; MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0241-taxonomia-OK.md`.
  Ancla protocolo `d5b426e4191729c3f8a8763984e20998f5566aed`; implementacion `ded4972`;
  flip review `40ae114`; producto control `D:/Agentes/Zeus/Zeus-protocol` commit
  `b2b2395da39090109db6de2dc50726dbaab1a11e`.
- Clean clone producto `C:/Users/johnb/AppData/Local/Temp/analista-0241-product-54facf6978364a05b8b070c11d543dae`;
  `npm test` EXIT 0 (109 tests, 87 pass, 22 skipped). Clean clone protocolo
  `C:/Users/johnb/AppData/Local/Temp/analista-0241-protocol-61049c06007743dfb4fc10ecb8dc584b`;
  validate/encoding/neutrality EXIT 0; vivo validate/encoding/neutrality EXIT 0; drift false
  `up_to_seq=3401`; `protocol.config.json` diff contra HEAD EXIT 0 y sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Vectores: S2-S7 cubren los 6 huecos pivote-v2; anti-cajon-de-sastre prohibe S1 por defecto;
  subconteo esperado declara 6 fuentes y cota inferior; severidad en doc y STARTUP_PROMPT; mesa 10/10
  parseada con D1-D4/S1-S7 exactos; neutralidad verde. Residual no bloqueante: prompt embebido del cron
  queda como seguimiento operativo de TASK-0242, no bloqueo de la taxonomia documental.

## Ultima actualizacion 2026-07-03 - TASK-0244 release v1.18.0 OK
- TASK-0244 release v1.18.0: OK/CERRABLE. Veredicto canonico en commit `461342b`
  (`review(TASK-0244): Analista OK release 1180`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0244-release-1180-veredicto.md`, MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0244-release-OK.md`.
  Ancla protocolo REVIEW `d0529a4d512d67405a02aefaf7be296966ada675`; tag `v1.18.0` apunta al commit
  `c9a442354bb5002b4df3a21e581ef1e891029c58`; trailer gate activo en
  `Area_comun/protocol/COMMIT_TRAILERS.json` con `start_commit cd3642d`.
- Clean clone producto `C:/Users/johnb/AppData/Local/Temp/analista-0244-6345365ad5c341689bfbc1beed189e2b/zeus-product`
  sobre `b2b2395da39090109db6de2dc50726dbaab1a11e`; `npm test` EXIT 0 (109 tests, 87 pass, 22 skipped).
  Clean clone protocolo tag `c9a4423` y HEAD `d0529a4`: validate/encoding/neutrality EXIT 0; vivo
  validate/encoding/neutrality EXIT 0; `test_trailers` EXIT 0 (9 casos); drift false `up_to_seq=3463`;
  chain valid `checked_events=2791`; `protocol.config.json` byte-identico a `TFM-dataset-N500`, sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Vectores: CHANGELOG cubre TASK-0238/0239/0240/0241/0242/0243; tag y mensaje pin-epoch correctos;
  templates sync en AGENTS.template s.6.1-6.4, HANDOFF_TEMPLATE, TASK_TEMPLATE y TASK_PROTOCOL; commit
  trailers post-activacion finales en `c87103c` y `d0529a4`. Residual no bloqueante: la instruccion REVIEW
  no cito commit de producto nuevo; use Zeus-protocol `b2b2395` como control, no como ancla de aceptacion.

## Ultima actualizacion 2026-07-03 - TASK-0242 envelope fix-loop OK
- TASK-0242 envelope/fix-loop gate: OK/CERRABLE. Veredicto preparado en
  `Area_comun/artifacts/ANALISTA-TASK-0242-envelope-fixloop-veredicto.md`; MSG rr a Arquitecto
  `Area_comun/mailbox/open/MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0242-envelope-fixloop-OK.md`.
  Ancla protocolo REVIEW `b78c6ce88005641c811191173572f6ef7060d141`; implementacion `fd0d059`;
  entrega `550c9ad`; producto control `D:/Agentes/Zeus/Zeus-protocol` commit
  `b2b2395da39090109db6de2dc50726dbaab1a11e`.
- Clean clone producto `C:/Users/johnb/AppData/Local/Temp/analista-0242-product-1fbddfdc7c094e51b1413d56bc7e6847`;
  `npm test` EXIT 0 (109 tests, 87 pass, 22 skipped). Clean clone protocolo
  `C:/Users/johnb/AppData/Local/Temp/analista-0242-protocol-2d5c90629fb441049f180f355a23f934`;
  validate/encoding/neutrality EXIT 0; vivo validate Python/PowerShell, encoding y neutrality EXIT 0;
  drift false `up_to_seq=3396`; `protocol.config.json` byte-identico hash-object
  `70d4c027a35b9d7d406bdfbe1cfcd427f203fc14`.
- Vectores: schema 7 campos en `TASK_PROTOCOL.md`; regla final text/nunca tool call; root
  `TASK_TEMPLATE.md`; fix-loop maximo 2 iteraciones + escalada al operador; prompts Codex/Analista con
  trailers y fix-loop; handoff real conforme; activacion TASK-0240 no implicita porque `trailer_start_seq`
  sigue fuera de scope y config intacta. Residual no bloqueante: examples contienen nota compacta, no bloque
  completo.

## Rol (clave)
- VOZ analista independiente en revisiones adversariales. NO arquitecto, NO consolidador.
  maker != checker: no leo las otras voces mientras produzco la mia; no consolido, no decido,
  no muto estado autoritativo (eso = submit_intent del arquitecto/runtime, escritor unico).
- Lentes ejercidas: fuentes/SOTA (existencia de papers + coincidencia de claims;
  CONFIRMADO/MAL-ATRIBUIDO/NO-VERIFICABLE) y honestidad/metodologia (no-overreach, fidelidad de
  taxonomias, completitud de gobernadores, consistencia entre decisiones).
- Principio rector: umbrales/metas de la MEDICION PROPIA (measure_context_cost, DECISION-0008),
  no de citas.

## Entrega (formato)
- Artefacto `Area_comun/artifacts/ANALISTA-<tema>.md`: veredicto de cabecera + por punto
  PASA / CAMBIO REQUERIDO (concreto, falsable) / RIESGO DECLARADO. Proporcional; sin meta-proyecto.
- Aviso compact en `Area_comun/mailbox/open/`, requested_action -> artefacto.

## Pasadas entregadas (historial)
- TASK-0240 trailer gate (2026-07-02): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en `aac12e6`
  (`review(TASK-0240): Analista blocks trailer parser`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0240-trailers-veredicto.md`, MSG rr
  `Area_comun/mailbox/open/MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0240-trailers-NOGO.md`.
  Ancla protocolo REVIEW `ae016274d547c2c3ae9d77c1c5e32da08a425451`; implementacion
  `6360569`; entrega `08b00ec`; producto control `D:/Agentes/Zeus/Zeus-protocol`
  commit `b2b2395da39090109db6de2dc50726dbaab1a11e`. Clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0240-product-4f9b6aec7b0a445abc36389f5318671e`;
  `npm test` EXIT 0 (109 tests, 87 pass, 22 skipped). Clean clone protocolo
  `C:/Users/johnb/AppData/Local/Temp/analista-0240-protocol-707ca64ec143438f8a0d0498577ab34a`;
  `test_trailers`, Python validator, PowerShell validator, neutrality y encoding EXIT 0. F-2 pasa:
  `commit_trailers` no esta activo, `protocol.config.json` byte-identico SHA256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`, drift false `up_to_seq=3348`
  tras claim/release. Bloqueante F-0240-01: una linea exacta `Task-Id: TASK-0240` en un parrafo no final,
  seguida por otro parrafo, pasa `validate_commit_trailers` sin errores; SPEC B.1 exige trailers git en la
  ultima seccion. Pedir parser de trailers finales y test negativo permanente.
- TASK-0239 re-gate actor remediation (2026-07-02): OK/CERRABLE. Veredicto canonico en `8643955`
  (`review(TASK-0239): Analista OK actor remediation`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0239-exception-recorded-veredicto.md`, MSG rr
  `Area_comun/mailbox/open/MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0239-actor-OK.md`.
  Ancla protocolo REVIEW `f2c972db70232b9e2e188aa503ad30fd4c1cf0c8`; implementacion remediacion
  `bc9cc8d84927f32837cdfc9ee5cdc301f6115aaa`; producto control `D:/Agentes/Zeus/Zeus-protocol`
  commit `b2b2395da39090109db6de2dc50726dbaab1a11e`; clean clone
  `C:/Users/johnb/AppData/Local/Temp/analista-0239-regate-4e5782fe3e0744f39477b13da4b70d2b`.
  `npm test` producto EXIT 0 (109 tests, 87 pass, 22 skipped); `python scripts/test_exception_recorded.py`
  EXIT 0 (6/6); `python scripts/test_intake_gate.py` EXIT 0 (12/12); py_compile EXIT 0; PowerShell
  validator EXIT 0. F-0239-01 cerrado: actor ajeno rechaza en single submit y transaccion good+bad sin append
  parcial; actor list/dict/int/bool/NUL rechaza; actor exacto emite `exception.recorded` con actor payload/evento
  igual al caller. Rechazos base y R5 TASK-0238 sin regresion; validate/neutrality/encoding live y clean EXIT 0;
  drift false `up_to_seq=3315`; `protocol.config.json` SHA256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residual no bloqueante: `require_text`
  normaliza por `str(...).strip()`, pero el guard de actor cierra las formas probadas.
- TASK-0238 R5 re-gate (2026-07-02): OK/CERRABLE. Veredicto canonico en `992b5ef`
  (`review(TASK-0238): Analista OK R5 regate`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0238-r5-regate-veredicto.md`, MSG rr
  `Area_comun/mailbox/open/MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0238-r5-OK.md`.
  Ancla protocolo revisada en clon limpio `8df7e62f7ee38867cc5b4354753e0a5f0941fb84`; implementacion
  `076193dc2209cb915d3b453bb734cadf459c9160`; coord `a87ae6b`; producto de control
  `D:/Agentes/Zeus/Zeus-protocol` commit `b2b2395da39090109db6de2dc50726dbaab1a11e`; clean clone
  `C:/Users/johnb/AppData/Local/Temp/analista-0238-r5-1dca9fff677942d4b97e28342968c286`.
  `npm test` producto EXIT 0 (109 tests, 87 pass, 22 skipped); `python scripts/test_intake_gate.py`
  EXIT 0 (12/12). F-0238-01 cerrado: `intake_exempt:true` con `exception_ref:999` sin evento rechaza
  en Python validator, PowerShell validator y `submit_intent`, dejando `TASK_INDEX` en `proposed`; wrong kind,
  wrong task y wrong type tambien rechazan. R0/R1 status family sin regresion; protocol.config SHA256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; validate/neutrality/encoding EXIT 0;
  drift false `up_to_seq=3275`. Residual: positivo futuro con evento real queda para TASK-0239/F1-B; probes
  sinteticos sin firma activan actor-auth/snapshot, por eso aisle el matcher con `exception_recorded_exists`.
- Post-commit memoria higiene (2026-07-02): commit `16e62ab` (`chore(personal): record Analista hygiene closure`)
  dejo canonico el FYI de cierre al Operador y esta memoria. Gates previos: `validate_collaboration_state.py`
  EXIT 0 con warning archivable de FYI; `scan_encoding.py` EXIT 0.
- Higiene area personal (2026-07-02): commit `d77ee98` (`chore(personal): archive Analista claim drafts`)
  archiva 15 JSON de claims consumidos en `personal/Analista/archive/claims/`. Conservados como vigentes:
  `MEMORY.md`, `STARTUP_PROMPT.md`, `README.md` y `analista_mailbox_cron.ps1`. FYI de cierre:
  `Area_comun/mailbox/open/MSG-20260702-Analista-to-Operador-FYI-higiene-area-personal.md`.
- TASK-0229 allowlist DECISION-0082 gate final (2026-07-02): OK/CERRABLE. Veredicto canonico en `4a1ead0`
  (`review(TASK-0229): Analista OK allowlist gate`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0229-allowlist-veredicto.md`, MSG
  `MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0229-allowlist-OK`. Ancla instruccion protocolo
  `3f1cedf0`; HEAD protocolo revisado `77b62e9d28df568213e6f71a4e95b74f88a1a238`; producto canonico
  `D:/Agentes/Zeus/Zeus-Aegis` commit `72984b09f0ec2f29ec8ba75e3660b94a8db80bb3`; clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0229-allowlist-aegis-5318c8e0fdc44c04983eb04df122b02f`.
  `npm test` EXIT 0; `corepack pnpm --dir vendor/hermes-2.3.0 build` EXIT 0; `electron:bundle-server`
  EXIT 0. `git grep -n -I -i hermes -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/electron/server-bundle.cjs`
  dio 892 hits y la allowlist `docs/DECISION-0082-HERMES-ALLOWLIST.md` cubre 892/892 (missing 0, extra 0,
  duplicados 0). Los 3 hits previos estan a Zeus (`provider-wizard.tsx:657`, `hermes-world-embed.tsx:12`,
  `claude-update.ts:34`); patrones historicos user-facing solo dejaron `expected hermes-workspace` en test
  fixture. Gates protocolo vivo y clean: validate/neutrality/encoding EXIT 0; drift false `up_to_seq=3208`
  tras claim/release; #4 sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0229 remediacion branding #5 bajo DECISION-0082 (2026-07-02): CAMBIO-REQUERIDO / NO-GO.
  Veredicto canonico en `51de440` (`review(TASK-0229): Analista blocks branding remediation 5`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-5-veredicto.md`, MSG
  `MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0229-remediacion-branding-5-NOGO`. Ancla instruccion
  protocolo `ccfbc00d25aead1604f2b54a37135d2a0c20d2ed`; HEAD protocolo al iniciar review
  `79651c74d40a89d444c0a75de40f78e2a7f2b7d1`; producto canonico `D:/Agentes/Zeus/Zeus-Aegis` commit
  `3c8c08420182073fdfde01ed953abd3ec20ba02f`; clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0229-rem5-aegis-971135bb8dd2487bb70960b80188002e/zeus-aegis`.
  `npm test` EXIT 0 (83 files / 562 tests); build EXIT 0; `electron:bundle-server` tras build EXIT 0; direct
  bundle sin build previo EXIT 1 por `dist/server/server.js` ausente (residual no bloqueante). Los tres hits
  exactos de ronda 4 pasan: `provider-wizard.tsx` ya no contiene `hermes`, `source=hermes-workspace` no aparece
  en embed/bundle, y `claude-update.ts` expone `zeus-aegis-workspace` como expected repo. Bloqueo falsable:
  DECISION-0082 exige allowlist etiquetada por cada hit Hermes restante y no encontre tal artefacto/lista en repo
  ni handoff; sin esa carga de prueba no puedo validar que no haya etiquetas falsas ni que todos los restantes sean
  identificador/import/comentario/dev-log/test-fixture/licencia-provenance/env-shim. Gates protocolo live y clean:
  validate/neutrality/encoding EXIT 0; drift false `up_to_seq=3155` tras claim/release; #4 sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Pivote "publicar para ser citado" (2026-07-02): CAMBIO-REQUERIDO, no NO-GO. Veredicto en commit
  `79651c7` (`review: Analista verdict on publishing pivot`), artefacto
  `Area_comun/artifacts/ANALISTA-pivote-publicar-citado-veredicto.md`, MSG
  `Area_comun/mailbox/open/MSG-20260702-Analista-to-Operador-REVIEW-pivote-publicar-citado.md`.
  Ancla protocolo `756477e683a94f6eca803bb0b02f662893554f8b`; sin producto canonico porque la instruccion
  de pivote no cita repo/commit de producto. Gates: validate live EXIT 0, validate secretless clone EXIT 0,
  scan_domain_neutrality EXIT 0, scan_encoding EXIT 0, drift false `up_to_seq=3153`, `protocol.config.json`
  sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Fuentes verificadas: Hinds/NoLabs
  2026-01-21 y NIST CAISI 2026-02-17 confirman anclas; Gartner confirma demanda macro; IETF AAT, nono/Sigstore
  y Agent Receipts/Pipelock/Microsoft AGT debilitan el claim amplio de unicidad. HP1/HP3/HP4 pasan con
  estrechamiento; HP2 parcial; HP5 no concedida por calendario/TFM/spec extraction. Cambio pedido:
  Semana 0 TFM/PII/licencia, claim estrecho, reproduccion externa antes de MCP/Action, kill criteria falsables.
- TASK-0229 remediacion branding #4 scope DECISION-0082 (2026-07-02): CAMBIO-REQUERIDO / NO-GO.
  Veredicto canonico en `406bb57` (`review(TASK-0229): Analista blocks scoped branding remediation 4`),
  artefacto `Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-4-scope-veredicto.md`, MSG
  `MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0229-remediacion-branding-4-NOGO`. Ancla protocolo
  `fd7c10ff595dda475444e39a885e3963471d4f2a`; producto canonico `D:/Agentes/Zeus/Zeus-Aegis` commit
  `1c81b109c533eaaf266c337bdb3bae5f0bf8f6ef`; nota: `1c81b10` no existe en `Zeus-protocol` (rev-parse
  exit 1) y si en `Zeus-Aegis` (exit 0), use el repo citado por TASK-0229/handoff 4. Clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0229-rem4-aegis-a6b482ee17a74db38f8bac3aca1436fe`. `npm test`
  EXIT 0 (83 files / 562 tests); `zeus-env-aliases.test.ts` EXIT 0 (3/3); build EXIT 0; `electron:bundle-server`
  EXIT 0; bundle diff EXIT 0; no package/appId/NOTICE/LICENSE diff relevante. Gates protocolo live y clean:
  validate/neutrality/encoding EXIT 0; drift false `up_to_seq=3149`; #4 sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Bloqueo falsable bajo DECISION-0082
  (no cero-grep): quedan hits user-facing Hermes en `src/screens/settings/components/provider-wizard.tsx:657`
  (`hermes` como comando renderizado en setup UI), `src/screens/playground/hermes-world-embed.tsx:12`
  (`source=hermes-workspace` en URL de iframe navegada), y `src/routes/api/claude-update.ts:34/:87`
  (`expected hermes-workspace repo` como error publico posible del update center). No bloquee identificadores,
  imports, comentarios, fixtures, storage/env-shim o provenance no renderizados.
- TASK-0229 remediacion branding #3 (2026-07-02): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `28b20f2` (`review(TASK-0229): Analista blocks branding remediation 3`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-3-veredicto.md`, MSG
  `MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0229-remediacion-branding-3-NOGO`. Ancla protocolo
  `2e3900c80a2ce831b0c7c7dbdb19d9b59a447154`; producto `D:/Agentes/Zeus/Zeus-Aegis` commit
  `1b047d3b4d601351090b95fe53641aa8946769dc`; clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0229-rem3-aegis-f661c42c78eb46b58cc655e1c0232f95`.
  `npm test` EXIT 0 (83 files / 562 tests); `zeus-env-aliases.test.ts` EXIT 0 (3/3); build EXIT 0;
  `electron:bundle-server` EXIT 0; no package/appId/binario rename diff detectado; MIT license intacta.
  Bloqueo falsable: grep residual `hermes` sigue devolviendo user-facing no allowlist en links renderizados y
  mensajes publicos de error/help: `src/routes/early-access.tsx`, `src/screens/playground/hermes-world-landing.tsx`,
  `src/server/claude-agent.ts`, `src/server/gateway-capabilities.ts`, `src/routes/api/mcp/$name.logs.ts`,
  `src/routes/api/mcp/discover.ts`, `src/routes/api/swarm-dispatch.ts`, con copias en
  `electron/server-bundle.cjs` (ej. `137158-137161`, `260996`, `274304`, `281149`, `282140`). Gates protocolo
  live y clean: validate/neutrality/encoding EXIT 0; drift false `up_to_seq=3140`; #4 sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0229 remediacion branding #2 (2026-07-02): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  commit de review `review(TASK-0229): Analista blocks branding remediation 2`, artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-2-veredicto.md`, MSG
  `MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0229-remediacion-branding-2-NOGO`. Ancla protocolo
  `735e9a45aa8ad02bf5fd56514823239211ae85af`; producto `D:/Agentes/Zeus/Zeus-Aegis` commit
  `c9eb971480fa5eecc9c50cf0329e6676921007bb`; clon limpio producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0229-rem2-aegis-171993b6308741fd873bc6b10215f1f2/zeus-aegis`.
  `npm test` EXIT 0 (83 files / 562 tests); `zeus-env-aliases.test.ts` EXIT 0 (3/3); `corepack pnpm --dir
  vendor/hermes-2.3.0 build` EXIT 0; diff package/appId/binarios relevante vacio. Bloqueo falsable:
  `git grep -n -I -i "hermes" -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/electron/server-bundle.cjs`
  sigue devolviendo cadenas user-facing no allowlist, por ejemplo `Spawning a Hermes swarm worker`,
  `Detected Hermes profiles`, `Hermes config`, `Build a scheduled Hermes task`, `Hermes Realm`,
  `Hermes Sigil`, `Could not load Hermes configuration` y copias en `electron/server-bundle.cjs`.
  Gates protocolo vivo y clean: validate/neutrality/encoding EXIT 0; drift false `up_to_seq=3124` antes
  de claim y `3126` tras claim/release; #4 sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0229 remediacion branding (2026-07-02): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `9699cf0` (`review(TASK-0229): Analista blocks branding remediation`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-veredicto.md`, MSG
  `MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0229-remediacion-branding-NOGO`. Ancla protocolo
  `a99a2b5aeccf697810b7fec5f280ea5f79520569`; producto Zeus-Aegis
  `bcb2715b39df895de0ce6bb209cdb0eb3a363a5a`; clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0229-rem-branding-75b26ccc78bb49d687ce99891074b581/zeus-aegis`.
  `npm test` EXIT 0 (83 files / 562 tests); `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run
  src/server/zeus-env-aliases.test.ts` EXIT 0 (3/3); `corepack pnpm --dir vendor/hermes-2.3.0 build` EXIT 0;
  no-rename diff de `package.json` y `electron-builder.config.cjs` EXIT 0. Bloqueo falsable: `src/**` y
  `electron/server-bundle.cjs` siguen exponiendo cadenas Hermes visibles fuera de allowlist, entre ellas
  `Hermes updated`, `Hermes Dashboard`, `Hermes Kanban`, `HermesWorld`, `hermes gateway restart`, `hermes --gateway`,
  `~/.hermes` y `NousResearch/hermes-agent`; conteo probe: `HermesWorld: 359`, `Hermes Dashboard: 27`,
  `Hermes Kanban: 22`, `~/.hermes: 64`. Gates protocolo live/clean validate/neutrality/encoding EXIT 0, drift false
  (`up_to_seq=3118` live tras claim/release, `3116` clean), #4 sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0229 WS3 branding white-label (2026-07-02): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `7d15fa6` (`review(TASK-0229): Analista blocks WS3 branding`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0229-ws3-branding-veredicto.md`, MSG
  `MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0229-ws3-branding-NOGO`. Ancla protocolo
  `ab120827f36cc5fd6d5fbc9975318b19e0f6fd3a`; producto canonico `D:/Agentes/Zeus/Zeus-Aegis` commit
  `ea3f52ce30abefe266b81661189d6d7864d69cb3` (incluye branding `980445cd7a3d0662040da72181fb285a4c003cb6`).
  Clean clone producto `C:/Users/johnb/AppData/Local/Temp/analista-0229-ws3-6feea6e1392a4806840fdf1817f905e0/zeus-aegis`.
  `npm test` EXIT 0 (wrapper 376.1 s, 83 files / 562 tests en tramo vendor); `corepack pnpm --dir
  vendor/hermes-2.3.0 build` EXIT 0; probe propio Vitest alias HERMES fallback URL/dashboard/password sin ZEUS EXIT 0
  (2/2). Bloqueo falsable: `git grep -n -I "Hermes Agent|Hermes Workspace|HERMES_API_URL|hermes setup|hermes gateway run"
  -- vendor/hermes-2.3.0/src` devuelve multiples cadenas visibles, entre ellas
  `src/components/connection-startup-screen.tsx:28/361/366`, `src/components/onboarding/setup-step-content.tsx:135`,
  `src/components/mobile-hamburger-menu.tsx:226`, `src/screens/mcp/mcp-screen.tsx:62` y
  `src/screens/skills/skills-screen.tsx:465`; `electron/server-bundle.cjs` versionado tambien contiene textos visibles
  Hermes. Gates protocolo live y clean-protocol: validate/neutrality/encoding EXIT 0, drift false `up_to_seq=3104`,
  #4 sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- Reviews huerfanas 0194/0199/0201/0203/0211/0215 (2026-07-02): OK/CERRABLE para cierre formal
  administrativo a `done`. Veredicto canonico en `25c0a09` (`review: Analista confirms orphan review
  closures`), artefacto `Area_comun/artifacts/ANALISTA-reviews-huerfanas-cierre-formal-veredicto.md`,
  MSG `MSG-20260702-Analista-to-Arquitecto-REVIEW-reviews-huerfanas-cierre-formal.md`. Alcance exacto:
  confirmo que los seis outputs de review son finales y completos; no reinterpreto sus recomendaciones
  historicas (`CAMBIO-REQUERIDO` sigue siendo NO-GO de su ronda; `TASK-0203` sigue OK/CERRABLE) y no ejecuto
  flips de estado como Analista. Ancla protocolo `7c70e81d73f2b1911976bb97bcea78b0e32bf40c`; control clean
  clone `Zeus-protocol` commit `b2b2395da39090109db6de2dc50726dbaab1a11e`, `npm test` EXIT 0 (109 tests,
  87 pass, 22 skipped). Gates protocolo live/secretless validate/neutrality/encoding EXIT 0; drift false
  `up_to_seq=3102` antes del claim y claim/release propio materializado en seq 3103/3104; #4 sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0237 remediacion re-gate vendor watchdog (2026-07-02): OK/CERRABLE. Veredicto canonico en
  `a9eebcc` (`review(TASK-0237): Analista OK vendor watchdog remediation`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0237-remediacion-veredicto.md`, MSG
  `MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0237-remediacion-OK`. Ancla protocolo bajo review
  `37cbd5dbc28c96a031f45037fc3609a047a7f82e`; producto canonico `D:/Agentes/Zeus/Zeus-Aegis` commit
  `ea3f52ce30abefe266b81661189d6d7864d69cb3`; `ea3f52c` no existe en `Zeus-protocol` y si en `Zeus-Aegis`.
  Clean clone producto `C:/Users/johnb/AppData/Local/Temp/analista-0237-rem-9b40d4523603470c8fba9b5a7ec68a57/zeus-aegis`.
  Root `npm test` en clon limpio: exit 0 en tres corridas consecutivas (83 files / 562 tests; wrapper total
  793.2 s). Vendor watchdog `ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS=1 npm --prefix vendor/hermes-2.3.0 test` exit 124
  en 2.2 s y `RUNNER_SURVIVORS=0` para node/npm/pnpm/cmd/esbuild bajo el clon. Probe de fallo real:
  Vitest intencional `expect(1).toBe(2)` exit 1 en 7.1 s. Gates protocolo live y secretless:
  validate/neutrality/encoding EXIT 0, drift false `up_to_seq=3071`, `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residuales declarados: timeout de 1 ms
  puede dispararse durante preparacion del runner, pero el comando canonico sale 124 acotado y no deja arbol vivo;
  exclusiones upstream preexistentes quedan fuera de TASK-0237.
- TASK-0236 harness remediation (2026-07-02): OK/CERRABLE. Veredicto canonico en `27f4950`
  (`review(TASK-0236): Analista OK harness remediation`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0236-harness-veredicto.md`, MSG
  `MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0236-OK`. Ancla protocolo bajo review
  `3523ecb`; producto de control `D:/Agentes/Zeus/Zeus-protocol` clean clone commit
  `b2b2395da39090109db6de2dc50726dbaab1a11e` (la instruccion no cito commit de producto distinto).
  Producto `npm test` EXIT 0 (109 tests, 87 pass, 22 skipped). Clean clone protocolo: validate EXIT 0,
  neutrality EXIT 0, encoding EXIT 0, drift false `up_to_seq=3041`, #4 sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Vivo: validate/neutrality/encoding/drift
  EXIT 0, drift false `up_to_seq=3043`. `python scripts/test_exec_lease_harness.py` EXIT 0 (9/9);
  py_compile y parser PowerShell de Codex/Analista/Arquitecto EXIT 0. Vectores: prompt por exec, tree-kill
  `/T /F`, instancia unica, lease huerfana vencida, stop exacto y regresiones de 0235 pasan. Residual declarado:
  tests de harness mayoritariamente estructurales, no end-to-end con `codex exec` real colgado, pero cubren los
  contratos del jam.
- TASK-0237 hang-proof npm test Zeus-Aegis (2026-07-02): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `1d7e569` (`review(TASK-0237): Analista blocks hang proof`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0237-hang-proof-veredicto.md`, MSG
  `MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0237-NOGO`. Ancla protocolo
  `cf84aa06f98dcf371e47c035b0c7ebe4e60a9ba2`; producto canonico `D:/Agentes/Zeus/Zeus-Aegis`
  commit `b3d863a9889c67274590232959eeb07ac324a548`; `b3d863a` no existe en `Zeus-protocol` (cat-file exit
  128) y si en `Zeus-Aegis` (exit 0). Clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0237-aegis-c38fe58fa1f14ee6b89c1cfe45d3dd3a/zeus-aegis`.
  `npm test` en clon limpio paso 3/3: exit 0 en 258.6s, 129.4s y 216.8s (83 files / 562 tests). Root watchdog
  `ZEUS_AEGIS_ROOT_TEST_HARD_TIMEOUT_MS=1 npm test` exit 124 en 1.2s. Bloqueo falsable: vendor watchdog
  `ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS=1 npm --prefix vendor/hermes-2.3.0 test` no termino dentro de 120s; el log
  muestra `zeus-aegis-f0-test: hard timeout after 1ms` pero Vitest siguio ejecutando tests. Bug real no enmascarado:
  test inyectado con `expect(1).toBe(2)` via `vitest run` exit 1 en 7.0s. Gates protocolo live y secretless:
  validate/neutrality/encoding EXIT 0, drift false (`up_to_seq=3041` live, `3032` secretless), `protocol.config.json`
  sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
- TASK-0235 cron policy A/B (2026-07-02): CAMBIO-REQUERIDO / NO-GO de cierre canonico. Veredicto canonico en
  `30e694c` (`review(TASK-0235): Analista blocks cron policy AB canon`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0235-cron-policy-AB-veredicto.md`, MSG
  `MSG-20260702-Analista-to-Arquitecto-REVIEW-cron-policy-AB`. Ancla REVIEW/protocolo
  `cc1dac4a411217d5e0291e73d27fefe37c7b9f3e`; documento
  `personal/Arquitecto/DISCUSSION-cron-zombie-policy.md`; TASK-0235 ya cerrada como implementacion de exec-lease.
  Producto no citado por la instruccion; control clean clone `Zeus-protocol`
  `b2b2395da39090109db6de2dc50726dbaab1a11e`, `npm test` EXIT 0 (109 tests, 87 pass, 22 skipped). Sustantivo A/B
  PASA con condiciones: no matar por Restart Manager, solo lease vencido PID+start-time, dry-run, re-check bajo
  lock, owner target unico, checker-owner explicito, deny-list, dirty-claimed-route guard y post-kill
  validate/drift/encoding. Probes propios: lease viva futura -> `lease_not_expired`; lease Analista mientras se barre
  Codex -> `owner_not_target`; owner/checker Analista -> `checker_owner_excluded`. Bloqueo canonico: clean clone
  protocolo `cc1dac4` validate sin secretos EXIT 1 por mismatches `TASK-0229` index blocked vs file ready y
  `TASK-0237` index in_progress vs file ready; vivo validate EXIT 0 por cambios locales ajenos. Drift clean false
  `up_to_seq=3028`; drift vivo false `up_to_seq=3032`; neutrality/encoding EXIT 0; `protocol.config.json` sha256
  `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
- TASK-0235 remediacion exec-lease (2026-07-01): OK/CERRABLE. Veredicto canonico en `8529cfe`
  (`review(TASK-0235): Analista OK remediation`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0235-remediacion-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0235-remediacion`. Ancla protocolo que materializa la
  instruccion `3ba2f11dc689f41b4f428c9d2ea8acd68a280868`; implementacion bajo review
  `bcd14081f0ef7723a1a7396dde742b403060550d`; producto control `Zeus-protocol`
  `b2b2395da39090109db6de2dc50726dbaab1a11e`. Clean clone producto `npm test` EXIT 0 (109 tests, 87 pass,
  22 skipped). Clean clone protocolo: py_compile, parser PowerShell, `test_exec_lease_harness.py` EXIT 0 (6/6),
  validate/neutrality/encoding EXIT 0 y drift false `up_to_seq=2918`. Probes propios: PID muerto pre-deadline
  en `Clear-StaleCronLockIfSafe` Codex y Analista deja `lock_exists=false`, `lease_exists=false` y log
  `SELF_HEAL_STALE_LOCK ... state=pre_deadline`; `sweep_cron_zombies.py --kill` con lease vencido/proceso muerto
  devuelve EXIT 0, `action=cleanup_only`, y borra lock+lease. No-regresion probada: dry-run no borra, owner/checker
  exclusion, lease no vencido, PID-reuse guard, deny-list `npm test`, y token unico `STOP_JOB` en summary/
  requested_action (broad `stop/para` no activa). Gates vivos validate/neutrality/encoding EXIT 0, drift false
  `up_to_seq=2920`; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0235 exec-lease hardening (2026-07-01): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `ca479f8` (`review(TASK-0235): Analista blocks exec lease`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0235-exec-lease-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0235-exec-lease`. Ancla instruccion/protocolo vivo
  `710cf60993b5961052b2e79afa476b54e03b810b`; implementacion bajo review
  `c4c15be075aaaea81c53bd06695caed9f6efa663`; producto control `Zeus-protocol`
  `b2b2395da39090109db6de2dc50726dbaab1a11e`. Clean clone protocolo
  `C:/Users/johnb/AppData/Local/Temp/analista-0235-s_chkkte/protocol`: py_compile, parser PowerShell,
  `test_exec_lease_harness.py`, validate, neutrality, encoding y drift EXIT 0 (`up_to_seq=2884`). Clean clone
  producto `npm test` EXIT 0 (109 tests, 87 pass, 22 skipped). Gates vivo validate/neutrality/encoding EXIT 0,
  drift false `up_to_seq=2912` antes del claim y `2914` tras claim/release; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Bloqueos falsables: la funcion real
  `Clear-StaleCronLockIfSafe` deja `lock_exists=true` y `lease_exists=true` cuando el PID esta muerto antes del
  deadline (EXIT 1), justo el incidente motivador con `ExecTimeoutSeconds=3600`; y `sweep_cron_zombies.py --kill`
  con lease vencido/proceso muerto devuelve `cleanup_only` EXIT 0 sin borrar lock ni lease. Recomendacion: limpiar
  lock+lease si PID ya no matchea por PID+start-time aunque el deadline no haya vencido; y materializar
  `cleanup_only` o fallar duro.
- TASK-0227 remediacion-6 (2026-07-01): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `733f217` (`review(TASK-0227): Analista blocks remediation 6`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0227-remediacion-6-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0227-remediacion-6`. Ancla protocolo vivo
  `96493b8c2a7e2e075930a386485f0f7d7aab5e50`; instruccion REVIEW materializada por `d5aeb1c`;
  producto citado por handoff `D:/Agentes/Zeus/Zeus-Aegis` commit
  `b58e6abeaa86e8bddad06f2f4906f6de3ea1851c`. Nota de ancla: la orden generica nombra
  `Zeus-protocol`, pero `b58e6ab` no existe alli; existe en `Zeus-Aegis`. Clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0227-rem6-cfe668d6bbda4030b8c16835c764284c/zeus-aegis`:
  `corepack pnpm --dir vendor/hermes-2.3.0 test` EXIT 0 (82 files / 559 tests) y targeted
  `governance-readonly.test.ts` EXIT 0 (16/16). Los 5 casos rem-5 ahora dan `matched=true`, y tambien
  las claves literal/simple/quoted/computed en `fetch`, `const opts` para fetch, `new Request`, `axios(...)`
  inline y `axios.request(...,{...})` inline. Probe propio EXIT 1 por slips nuevos dentro del AC literal/local:
  `const cfg = { "method": "POST" }; axios.request('/api/governance/state', cfg)` matched=false y
  `const cfg = { "url": "/api/governance/state", "method": "POST" }; axios(cfg)` matched=false. Gates protocolo
  vivo y clean validate/neutrality/encoding EXIT 0; drift false `up_to_seq=2904` antes de claim y `2906`
  tras claim/release; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0227 remediacion-5 (2026-07-01): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `71787c4` (`review(TASK-0227): Analista blocks remediation 5`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0227-remediacion-5-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0227-remediacion-5`. Ancla protocolo/instruccion
  `7953df12150c69d7f48c417252303c45ba4cc405`; producto citado `bbf84e714e2bff4b29fba325fa0e7a20192a1df6`.
  Nota de ancla: `D:/Agentes/Zeus/Zeus-protocol` no contiene `bbf84e7`; el commit existe en
  `D:/Agentes/Zeus/Zeus-Aegis`. Clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0227-rem5-c0552dd117574b13865b1e18159c7c5b/zeus-aegis`:
  `corepack pnpm --dir vendor/hermes-2.3.0 test` EXIT 0 (suite full verde; `governance-readonly.test.ts`
  16 tests). Probe propio del guard F1 EXIT 1: el caso rem-4 tipado `const opts: RequestInit = { method:
  'POST' }; fetch('/api/governance/state', opts)` y previos pasan, pero las claves string-literal dentro de
  objeto literal enumerable salen `matched=false`: `fetch(..., { "method": "POST" })`, `const opts:
  RequestInit = { "method": "POST" }; fetch(..., opts)`, `fetch(new Request(..., { "method": "POST" }))`,
  `axios.request(..., { "method": "POST" })`, y `axios({ "url": "/api/governance/state", method: "POST" })`.
  Gates protocolo vivo y clean validate/neutrality/encoding EXIT 0; drift false `up_to_seq=2900`;
  `protocol.config.json` sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0222 remediacion-2 (2026-07-01): GO/CERRABLE. Veredicto canonico en `7741923`
  (`review(TASK-0222): Analista OK remediation 2`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0222-remediacion-2-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0222-remediacion-2`. Ancla protocolo REVIEW/HEAD
  `e44e08f5f0c9b1e6294ce5002c9a4dfbb4b35bca`; producto citado en handoff
  `D:/Agentes/Zeus/Zeus-Aegis` commit `3b25b8b9f6b7a1a0520f02d10e8f9394c80a7627`; clon limpio
  `C:/Users/johnb/AppData/Local/Temp/analista-0222-rem2-cd68c18135414a2f80b86767ee2ae228/zeus-aegis`.
  Nota de ancla: la orden generica nombraba `Zeus-protocol`, pero ese repo no contiene `3b25b8b`; el commit existe
  en `Zeus-Aegis`, que es el `product_repo` canonico de la tarea. `npm test` en clon limpio EXIT 0 dos veces
  consecutivas (82 files / 559 tests; run 2 duration 138.34 s); targeted stats/F1 EXIT 0 (4 passed, stats 1103 ms).
  Probes propios del parser de tokens y guard F1 EXIT 0: cola 128 KiB, token viejo fuera de cola excluido,
  multilinea dentro de 4 lineas suma, multilinea despues de 4 se ignora, y familia F1 cubierta bloqueada.
  Gates protocolo vivo y clean validate/neutrality/encoding EXIT 0; drift false `up_to_seq=2888` tras claim/release;
  `protocol.config.json` sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0227 remediacion-4 (2026-07-01): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `6014596` (`review(TASK-0227): Analista blocks remediation 4`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0227-remediacion-4-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0227-remediacion-4`. Ancla protocolo vivo al claim
  `c4c15be075aaaea81c53bd06695caed9f6efa663`; instruccion REVIEW materializada en
  `2a881e6db3e1e9910ee747525494053676fc08db`; producto citado
  `534b95eaaf952be81c635aedab528e6663041e1e`. Nota de ancla: `D:/Agentes/Zeus/Zeus-protocol` no contiene
  `534b95e`; el commit existe en `D:/Agentes/Zeus/Zeus-Aegis`. Clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0227-rem4-0977876a2d4e48c89be806b704728d22/zeus-aegis`:
  `npm test` EXIT 0 (82 files / 559 tests; `governance-readonly.test.ts` 16 tests). Probe propio del guard F1
  acotado EXIT 1: los tres negativos de rem-3 pasan (`fetch` con opts local sin tipo, `new Request`, y
  `axios.request` posicional), pero `const opts: RequestInit = { method: 'POST' }; fetch('/api/governance/state',
  opts)` sale `matched=false`. Veredicto: con DECISION-0079 actual, objeto local tipado con method literal sigue
  dentro de la familia enumerable prometida; pedir fix o acotar explicitamente la decision. Gates protocolo:
  validate/neutrality/encoding EXIT 0, drift false `up_to_seq=2886`, `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0222 remediacion stats (2026-07-01): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `3eea590` (`review(TASK-0222): Analista blocks stats remediation`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0222-remediacion-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0222-remediacion`. Ancla protocolo/instruccion
  `b942389b0243ab7a4085689af6b157bdeb1bbaa8`; producto Zeus-Aegis
  `a68eb34297d81a77a92c0d8fb378933f3f2796f6`; clon limpio producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0222-remed-zeus-aegis-52ac4b8230a944329a51e0eb6c1dd714`.
  `npm test` en clon limpio EXIT 1: el test de stats ya no hace timeout (`exposes token stats...` visible en
  943 ms), pero la suite full termina con `Unhandled Rejection: Error: Channel closed` /
  `ERR_IPC_CHANNEL_CLOSED`; gate de cierre sigue rojo por exit-code. Targeted stats EXIT 0 (1142 ms) y targeted
  F1/stats/read-only EXIT 0. Payload propio del scanner: cola 128 KiB respeta bound (token viejo fuera de cola no
  suma), multilinea dentro de 4 lineas suma, multilinea a 5 lineas se ignora, dataset sigue `500/500`.
  Gates protocolo vivo y clean validate/neutrality/encoding EXIT 0; drift false `up_to_seq=2871` post-claim;
  `protocol.config.json` sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0227 remediacion-3 (2026-07-01): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `bda1278` (`review(TASK-0227): Analista blocks remediation 3`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0227-remediacion-3-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0227-remediacion-3`. Ancla REVIEW/protocolo
  `77a90ad331c69d90517f1670bd9c8431f6522864`; commit producto citado
  `19ebd48d0f5b57ea96ba181410a04066695870bd`. Nota de ancla: `D:/Agentes/Zeus/Zeus-protocol`
  no contiene `19ebd48` tras fetch; el commit existe en `D:/Agentes/Zeus/Zeus-Aegis`, y ahi se ejecuto
  el clon limpio `C:/Users/johnb/AppData/Local/Temp/analista-0227-rem3-aegis-b2da77cc7d1c48f88208ce86f051aa9f`.
  `npm test` producto EXIT 0; `governance-readonly.test.ts` 16 tests pasa. Los cuatro escapes de rem-2
  pasan: `fetch` method variable/template/lowercase/shorthand/computed literal y `axios.post`,
  `axios.request({url,method})`, `axios({url,method})`. Bloqueo nuevo falsable por probe propio del guard:
  `const opts={method:'POST'}; fetch('/api/governance/state', opts)` matched=false,
  `fetch(new Request('/api/governance/state', {method:'POST'}))` matched=false, y
  `axios.request('/api/governance/state', {method:'POST'})` matched=false. Gates protocolo vivo y clean:
  validate/neutrality/encoding EXIT 0; drift false `up_to_seq=2862`; `protocol.config.json` sha256
  `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`. Recomendacion: remediacion-4
  con esos tres negativos permanentes o AC F1 acotado formalmente.
- TASK-0227 remediacion-2 (2026-07-01): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `b2e2e39` (`review(TASK-0227): Analista blocks remediation 2`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0227-remediacion-2-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0227-remediacion-2`. Ancla REVIEW
  `f7c92ba`, redelivery protocolo `464b479b4b3c5a46ca064a8f31871fafb97f1208`, protocolo HEAD
  `b73aa9004da544c911ff7fdf76dc78dd70ce5ce2`, producto Zeus-Aegis `88091b1ee299734fa860ad9229556575f312eb38`.
  Clean clone producto `C:/Users/johnb/AppData/Local/Temp/analista-0227-product-b3b7af714ad64b2a9e421a5b295e164b`:
  `npm test` EXIT 124 a 604s; targeted vitest governance-readonly EXIT 124 a 304s. Los 4 escapes previos pasan
  (method variable, template method, lowercase method, axios.post), pero probe propio sobre
  `GOVERNANCE_FORBIDDEN_WRITE_PATTERNS` salio EXIT 1 por slips nuevos: `fetch(..., { method })`,
  `fetch(..., { ['method']: 'POST' })`, `axios.request({ url, method: 'POST' })`, y
  `axios({ url, method })`. Clean clone protocolo validate/neutrality/encoding EXIT 0; drift false `up_to_seq=2848`;
  `protocol.config.json` sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. El workspace
  vivo no fue ancla; validate vivo salia rojo por cambio local ajeno en `CLAIM-20260701-Codex-DECISION-0078`
  con selector invalido.
- TASK-0228 WS5 HEAD limpio (2026-07-01): GO/CERRABLE. Veredicto canonico en `12ea5d3`
  (`review(TASK-0228): Analista OK clean head`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0228-ws5-head-limpio-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0228-ws5-head-limpio`. Ancla protocolo/instruccion
  `a0de55a3fd8eba26d7c8cdc96967a538944e09fa`; implementacion bajo review `7353070`; producto control
  `Zeus-protocol` clean clone `b2b2395da39090109db6de2dc50726dbaab1a11e`; clean clone protocolo en
  `C:/Users/johnb/AppData/Local/Temp/analista-0228-protocol-headlimpio-40433666df5b4a77bcc9ee3553d0210e`.
  Clean clone protocolo validate/neutrality/encoding exit 0; drift `has_drift=false up_to_seq=2842`;
  `protocol.config.json` sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
  Producto `npm test` exit 0 (109 tests, 87 pass, 22 skipped). Sustantivo TASK-0228 PASA: coordination
  instancia valida con 4 participantes/personales; TASK sintetica `owner: Analista` valida exit 0; probe
  `owner: Intruso` tambien valida exit 0 y queda declarado como no-gateado; decisiones 0072/0073/0077 existen;
  maker!=checker queda disciplinario; attested valida con 3 public keys (`arquitecto:v1`, `codex:v1`,
  `analista:v1`) mas `human_owner` sin signer. Recomendacion: Arquitecto puede cerrar si no hay cambio posterior
  fuera de la ancla.
- TASK-0228 WS5 AC corregido (2026-07-01): CAMBIO-REQUERIDO / NO-GO de cierre canonico. Veredicto en
  `6fdc06a` (`review(TASK-0228): Analista blocks corrected AC on clean gate`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0228-ws5-ac-corregido-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0228-ws5-ac-corregido`. Ancla protocolo/instruccion
  `8d9b87185f6397801f8a3160d4536dded4213a78`; implementacion bajo review `7353070`; producto control
  `Zeus-protocol` clean clone `b2b2395da39090109db6de2dc50726dbaab1a11e`; clean clone protocolo/producto en
  `C:/Users/johnb/AppData/Local/Temp/analista-0228-ac-review-4993debf951f490687d48d6d8094b3bd`. Sustantivo
  TASK-0228 PASA contra AC honesto: coordination instancia valida con 4 participantes/personales; TASK sintetica
  `owner: Analista` valida exit 0; decisiones 0072/0073/0077 existen; maker!=checker queda disciplinario no
  gateado; attested valida con 3 signers (`Arquitecto`, `Codex`, `Analista`) + `human_owner` worker. Bloqueo:
  clean clone canonico `8d9b871` falla `python scripts/validate_collaboration_state.py` exit 1 por mismatch ajeno
  `TASK-0223` (`TASK_INDEX=done`, task file=`review_approved`). Vivo validate/neutrality/encoding exit 0 solo por
  cambio local no commiteado en TASK-0223; no usable como ancla. `npm test` producto exit 0 (109 tests, 87 pass,
  22 skipped); drift clean/live false `up_to_seq=2842`; `protocol.config.json` sha256
  `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
- TASK-0228 WS5 alta Analista NOVA (2026-07-01): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `619f419` (`review(TASK-0228): Analista blocks WS5`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0228-ws5-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0228-ws5`. Ancla instruccion/protocolo
  `f7c92ba394f0284f9b80ed9e3ac5e3035a353830`; implementacion bajo review `7353070`
  (`feat(instancing): add analyst participant to new instances`); producto Zeus-protocol sin commit citado,
  control clean clone `b2b2395da39090109db6de2dc50726dbaab1a11e`; clean clone review
  `C:/Users/johnb/AppData/Local/Temp/analista-0228-review-303773e8c6de4cf684bcd81b3576fc50`.
  `npm test` producto exit 0; `new_instance.py --tier coordination` exit 0 y generated NOVA valida exit 0 con
  4 agentes/personales; TASK sintetica `owner: Analista` valida exit 0. Bloqueo falsable: probe `owner: Intruso`
  tambien valida exit 0, y probe `owner: Codex` + `reviewer: Codex` valida exit 0 aunque
  `allow_self_review:false`; por tanto maker!=checker queda declarativo/no gateado. Ademas no encontre decision
  canonica que cite `NOVA-ARQ-001` fuera de tarea/GO/REVIEW. Riesgo declarado: `--tier attested` crea 4 agentes
  pero solo 3 signers (`human_owner` worker), asi que "4 firmantes" necesita aclaracion. Gates protocolo vivo y
  clean `7353070`: validate, neutrality, encoding exit 0; drift vivo `has_drift=false up_to_seq=2842`, clean
  `has_drift=false up_to_seq=2825`; `protocol.config.json` sha256
  `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
- TASK-0223 vista Instanciar-proyecto (2026-07-01): GO/CERRABLE. Veredicto canonico en
  `cd67775` (`review(TASK-0223): Analista OK instancing view`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0223-vista-instanciar-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0223-vista-instanciar`. Ancla protocolo/instruccion
  `7c65448967f9e4253eec234945d48660ae371a92`; producto Zeus-Aegis
  `4ff95d929e41c13c04750c2ebed1947978724896`; clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0223-zeus-aegis-9b29a374d46a4b03be4800b25584cf01`;
  clean clone protocolo `C:/Users/johnb/AppData/Local/Temp/analista-0223-protocol-3bd9adae194940e6aba48a9c669f57f0`.
  `npm test` producto exit 0; payloads propios contra `buildInstancePlan`/guard exit 0 (5 familias);
  render `/governance` exit 0 con screenshot `task0223-analista-instancing-render.png`, guard visible
  "El panel NO escribe el ledger", `no ejecuta new_instance.py`, 0 writes a `/api/governance`. Gates protocolo
  vivo y clean `7c65448`: validate, scan_domain_neutrality, scan_encoding exit 0; drift vivo
  `has_drift=false up_to_seq=2811`, clean `has_drift=false up_to_seq=2804`; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residual no bloqueante:
  Playwright uso Chrome del sistema porque el browser empaquetado no estaba instalado; F1 sigue copy-only.
- OPS-CRON-ZOMBIE-POLICY (2026-07-01): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `78a4b36` (`review(OPS-CRON-ZOMBIE-POLICY): Analista blocks zombie sweep`), artefacto
  `Area_comun/artifacts/ANALISTA-OPS-CRON-ZOMBIE-POLICY-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-cron-zombie-policy`. Ancla instruccion/propuesta
  `ba617c6` (`personal/Arquitecto/DISCUSSION-cron-zombie-policy.md`); protocolo vivo durante review
  `7c65448967f9e4253eec234945d48660ae371a92`; producto Zeus-protocol sin commit citado en instruccion,
  control clean clone `b2b2395da39090109db6de2dc50726dbaab1a11e`, `npm test` exit 0 (109 tests, 87 pass,
  22 skipped). Bloqueo falsable: Restart Manager prueba holder de handle, no liveness; la propuesta dice
  excluir "exec legitimamente en curso" pero no define lease/heartbeat/start-time/owner verificable, por lo que
  puede matar trabajo lento pero vivo y el exec del checker. Gates protocolo vivo y clean `ba617c6`: validate,
  neutrality, encoding exit 0; drift vivo `has_drift=false up_to_seq=2806`, clean `has_drift=false up_to_seq=2804`;
  `protocol.config.json` sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
  Recomendacion: volver a borrador; permitir solo intervencion manual de emergencia con dry-run, PID+start-time,
  exclusion de checker y confirmacion humana hasta que exista contrato de lease verificable.
- TASK-0222 vista Estadisticas (2026-07-01): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `8fd4d2e` (`review(TASK-0222): Analista blocks stats view`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0222-vista-stats-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0222-vista-stats`. Ancla protocolo/instruccion
  `3c39541655fe5540b3042e1ff50cd5443506a630`; producto Zeus-Aegis
  `ff82538f31abb45cc4314fd396051a81e62dfe24`; clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0222-zeus-aegis-c86962bd130948cd9612e9afa8ab5be5`; clean clone
  protocolo `C:/Users/johnb/AppData/Local/Temp/analista-0222-protocol-cee01171f623430591f78ee615aa1dc6`.
  Bloqueo falsable: `npm test` en clean clone producto sale EXIT 1; falla
  `src/server/governance-readonly.test.ts` en `exposes token stats and frozen dataset progress through the
  read-only stats endpoint` por timeout a 30000 ms. Targeted vitest con `--testTimeout=60000` tambien EXIT 1
  porque el test declara timeout interno 30000 ms. Endpoint/render pasan funcionalmente: HTTP 200,
  dataset `500/500`, tag `TFM-dataset-N500`, minSeq `2221`, breakdown Analista 52 / Arquitecto 253 /
  Codex 195, screenshot local `task0222-analista-stats-render.png`. F1 read-only de superficie cambiada sin
  write-path nuevo en diff. Gates protocolo vivo y clean: validate, neutrality, encoding exit 0; drift 0
  `up_to_seq=2795`; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Recomendacion: devolver a Codex
  para hacer verde el full clean-clone gate antes de cierre.
- TASK-0227 F1 boundary (2026-07-01): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `88d0568` (`review(TASK-0227): Analista blocks F1 boundary`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0227-f1-boundary-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0227-f1-boundary`. Ancla protocolo citada
  `9e0206e48b66227a9165a2970d9f717d51b0953f`; protocolo vivo durante review
  `245e521f1420f87614a59bc640ca219a87899a44`; producto Zeus-Aegis
  `15c52fb134ee21cc9d716af8f9d8a9c7aba0e741`; clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/analista-0227-zeus-aegis-31a2123de8544283adf546a486497d3e`.
  `npm test` exit 0 (82 files, 556 tests) y test F1 canonico exit 0. Bloqueo falsable:
  el guard F1 falla para write-paths reales con `method: POST` with backtick quotes, `const m='POST';
  fetch(...,{method:m})`, `method:'post'` lowercase, y `axios.post(...)`: todos salieron exit 0 en
  test dirigido mutado. Controles positivos si sostienen: `fetch(...,{method:'POST'})` literal y
  `submit_intent` sin guard local salen exit 1. Gates protocolo vivo y clean `9e0206e`: validate,
  scan_domain_neutrality, scan_encoding exit 0; drift vivo `has_drift=false up_to_seq=2791`, clean
  `has_drift=false up_to_seq=2758`; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Recomendacion: devolver a Codex
  para ampliar el guard F1 por familia y anadir negativos permanentes.
- TASK-0225 Arquitecto-cron remediacion-2 (2026-07-01): GO/CERRABLE. Veredicto canonico en
  `e2fd73d` (`review(TASK-0225): Analista OK remediation 2`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0225-remediacion-2-veredicto.md`, MSG
  `MSG-20260701-Analista-to-Arquitecto-REVIEW-TASK-0225-remediacion-2`. Ancla protocolo/instruccion
  `349a8cac40d3fdfaa7ccf463769db1526b3d6766`; implementacion bajo review `8385868`
  (`fix(TASK-0225): repair ws snapshot classifier`); producto Zeus-protocol sin commit citado en la
  instruccion, control clean clone `b2b2395da39090109db6de2dc50726dbaab1a11e`, `npm test` exit 0
  (109 tests, 87 pass, 22 skipped). Clean clone protocolo
  `C:/Users/johnb/AppData/Local/Temp/analista-0225-review-1089e690106144bcbb9ff5d19a2a088f/protocol`:
  `-RunClassifierSelfTest` exit 0 (3/3), `-DryRunOnce` exit 0 con `ledger_write=false`,
  `ws_snapshot.in_review=[TASK-0222,TASK-0225,TASK-0227]` y `decision=review_or_ratify`. Payloads propios
  extraidos por AST sobre `Test-WsTask` + `New-WsSnapshot` exit 0 (6/6): TASK-02xx sin project, REQ-ZEUS sin
  project, titulo WS sin project, project conocido, ready no relevante no promueve, ready relevante promueve
  solo sin reviews. Gates protocolo vivo y clean: validate, scan_domain_neutrality, scan_encoding exit 0;
  drift vivo/clean `has_drift=false up_to_seq=2775`; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residual no bloqueante: clasificador
  heuristico amplio puede contar falsos positivos, pero falla conservador (review/espera, no promocion falsa).
- TASK-0225 Arquitecto-cron review (2026-06-30): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en
  `9d0bcc0` (`review(TASK-0225): Analista blocks Arquitecto cron`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0225-arquitecto-cron-veredicto.md`, MSG
  `MSG-20260630-Analista-to-Arquitecto-REVIEW-TASK-0225-arquitecto-cron`. Ancla protocolo HEAD
  `4e9fd4dcefc6eb67da8b35323e81866dca59e14c`; implementacion `a1cecb275d853f64cdaa4701d65cc50dc8e685af`;
  delivery `15c02b2787850b81e8835c7a3d02481e0fda39d7`; producto Zeus-protocol no tenia commit citado,
  control clean clone `b2b2395da39090109db6de2dc50726dbaab1a11e`, `npm test` exit 0 (109 tests, 87 pass,
  22 skipped). Bloqueo falsable: dry-run canonico en clean clone `15c02b2` exit 0 y `ledger_write=false`,
  pero con `TASK-0225` y `TASK-0226` `in_review` en TASK_INDEX devolvio `ws_snapshot.in_review=[]` y
  `decision=promote_one_ready_task`. Payload propio confirmo causa: `Get-WsSnapshot` filtra por
  `project` obligatorio; una tarea `TASK-0299`/`REQ-ZEUS WS` `in_review` sin `project` da `in_review=0`,
  mientras la misma con `project=multi_agent_project_protocol` o `Zeus-protocol` da `review_or_ratify`.
  Gates protocolo vivo y clean clone: validate, scan_domain_neutrality, scan_encoding exit 0; drift vivo
  `has_drift=false up_to_seq=2752`, clean `has_drift=false up_to_seq=2746`; `protocol.config.json`
  sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
- OPS-MEDICION-H1-H3 (2026-06-30): GO/CERRABLE. Veredicto canonico en `1ddf249`
  (`review(OPS-MEDICION): Analista OK H1-H3 measurement`), artefacto
  `Area_comun/artifacts/ANALISTA-medicion-H1-H3-veredicto.md`, MSG
  `MSG-20260630-Analista-to-Arquitecto-REVIEW-medicion-H1-H3`. Ancla protocolo/instruccion
  `333e1693879fce9dc592c53f2cf55736f672abd3`; corpus sellado `TFM-dataset-N500`
  `e3646ae01fff1f59a5d7882bfd7c8d744ff1c5f9`; `protocol.config.json` sha256
  `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`. Reproduccion limpia en
  `C:/Users/johnb/AppData/Local/Temp/analista-medicion-h1h3-cceb1aabf84d441b9f3494ff504bb71c`:
  H1 detection exit 0 (450/450; A1 200, A2 200, A3 50; 0 evasions), H1 FPR/AC2 exit 0
  (FPR 0/500, AC2 500/500), H2 exit 0 (delta mediana 1.5186 ms, p95 3.2708 ms, store
  0.42254 KB/ev, tokens 0.0%), H3 exit 0 (acuerdo 1.0, hash interno/externo
  `dd2fd60eef525589f0ed8f1d581f45bfed584ab3ba2b3dc6c5624fbbbcc10ff0`, Ed25519 public-only
  500/500). Producto Zeus-protocol no tenia commit citado; gate general ejecutado en clean clone
  `C:/Users/johnb/AppData/Local/Temp/zeus-protocol-review-medicion-8785d154c92a46fdb61ea1286ad7c9b9`,
  HEAD `b2b2395da39090109db6de2dc50726dbaab1a11e`, `npm test` exit 0 (109 tests, 87 pass,
  22 skipped). Gates protocolo: validate con/sin secretos, scan_domain_neutrality, scan_encoding
  exit 0; drift final `has_drift=false up_to_seq=2731`. Residuales no bloqueantes: A3 se sostiene
  como genesis/chain-hash efectivo porque el corpus tiene 0 `chain.anchor`; tokens 0% es estructural/
  by-design, no telemetria empirica. Claim Analista acquire/release seq 2730/2731; push a origin/main OK.
- TASK-0226 WS1 remediation re-review (2026-06-30): GO/CERRABLE bajo gate DOC-ONLY. Veredicto canonico en
  `266e4af` (`review(TASK-0226): Analista OK WS1 remediation`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0226-remediacion-veredicto.md`, MSG
  `MSG-20260630-Analista-to-Arquitecto-REVIEW-TASK-0226-remediacion`. Ancla protocolo/instruccion
  `fc1955e650abdbeb8af9641e5142f107b2da6549`; producto Zeus-Aegis
  `055c95653921c1d5c95cdb5d1bf2a510331837b3`; clean clone producto
  `C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-0226-remed-2d7d9b501bd04276a258658789d07980`;
  clean clone protocolo `C:/Users/johnb/AppData/Local/Temp/protocol-review-0226-remed-2e1acf48843b4ee9925ac7e4c01541fb`.
  Confirmado: commit producto doc-only (`M docs/BRANDING-PLAN-WS1.md`), `git diff --check` exit 0, residual D4
  concreto en `vendor/hermes-2.3.0/THIRD-PARTY-NOTICES.md` con entrada `hermes-agent (NousResearch)` si WS3
  redistribuye binario/imagen/instalador/offline artifact. Gates protocolo vivo y clean: validate,
  scan_domain_neutrality, scan_encoding exit 0; drift final vivo `has_drift=false up_to_seq=2729`; clean
  `has_drift=false up_to_seq=2727`; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. `npm test` producto clean timeout exit
  124 a 363s; declarado residual no bloqueante por instruccion DOC-ONLY/NOVA DECISION-0006 y transferido a
  TASK-0227. Claim Analista acquire seq 2728, release seq 2729.
- TASK-0226 WS1 branding inventory (2026-06-30): CAMBIO-REQUERIDO / NO-GO. Veredicto en
  `Area_comun/artifacts/ANALISTA-TASK-0226-ws1-branding-veredicto.md`, MSG
  `MSG-20260630-Analista-to-Arquitecto-REVIEW-TASK-0226-ws1`. Ancla protocolo durante review
  `15c02b2787850b81e8835c7a3d02481e0fda39d7`; instruccion REVIEW materializada desde
  `Area_comun/mailbox/open/MSG-20260630-Arquitecto-to-Analista-REVIEW-TASK-0226-ws1.md`; producto
  Zeus-Aegis `4644455e9a0527b8d7eebe7b92efd77d5f9a3dba`; clean clone
  `C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-0226-12828a40f00241b4a89d23ec50bcb0a9`.
  El commit producto es document-only (`A docs/BRANDING-PLAN-WS1.md`) y `git diff --check` sale 0; el
  documento cubre inventario hermes, shim superficial `ZEUS_* -> HERMES_* -> CLAUDE_*`, no renombrar
  binarios/appId/updater, purga Hermesworld/NousResearch y preservacion MIT. Bloqueo falsable: `npm test`
  en clean clone sale exit 1; fallan `src/server/governance-readonly.test.ts` por timeout en lectura de
  artifacts/decisions/handoffs/ledger y por `submit_intent` en UI. Bajo la instruccion, gatea por EXIT y no
  es cerrable aunque parezca preexistente. Gates protocolo vivos y clean clone sin secretos: validate,
  scan_encoding y scan_domain_neutrality exit 0; drift #4 false `up_to_seq=2716`; `protocol.config.json`
  sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`. Claim Analista
  `CLAIM-20260630-Analista-TASK-0226-ws1-review` seq 2714 acquire, seq 2716 release; TASK-0226 movido
  `in_review -> changes_requested`.
- TASK-0224 re-review remediacion (2026-06-30): OK/CERRABLE. Veredicto canonico en `6fb6116`
  (`review(TASK-0224): Analista OK remediation`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0224-remediacion-veredicto.md`, MSG
  `MSG-20260630-Analista-to-Arquitecto-REVIEW-TASK-0224-remediacion`. Ancla protocolo/instruccion
  `004cb0ab2b7b1533dd6cac2862248dddab526b46`; commit bajo review `7bfc15f3bb4704648dc556a455cfff11d24423a4`;
  producto control Zeus-protocol `b2b2395` (la instruccion no cito commit de producto especifico). Claim Analista
  `CLAIM-20260630-Analista-TASK-0224-remediation-review`: acquire seq 2698; review_approved seq 2699; release
  seq 2700. Confirmado por comportamiento: `inject_report_metadata` limpia familia plana EN/ES (`Date`, `Updated`,
  `Fecha`, `Actualizado`, `Dataset status`, `Dataset actualizado`), familia con negrita, variantes con espacios y
  caso sin cabecera; reporte real `REPORT-20260605-release-v0.2.0.md` con `- Date: 2026-06-05` genera solo
  `- **Updated:** 2026-06-29T12:34:56Z` + dataset `477/500`. Gates: py_compile exit 0; golden human guide exit 0;
  clean clone protocolo `7bfc15f` validate/neutrality/encoding/golden exit 0; vivo validate/encoding/neutrality
  exit 0; drift 0 `up_to_seq=2700`; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; clean clone producto `b2b2395` `npm test`
  exit 0 (109 tests, 87 pass, 22 skipped). Residual no bloqueante: normalizador solo cubre las seis familias de
  metadata conocidas, no cualquier clave arbitraria.
- TASK-0224 review report redactor (2026-06-29): CAMBIO-REQUERIDO / NO-GO. Veredicto canonico en `6a7a4b6`
  (`review(TASK-0224): Analista blocks report redactor`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0224-report-redactor-veredicto.md`, MSG
  `MSG-20260629-Analista-to-Arquitecto-REVIEW-TASK-0224`. Ancla protocolo bajo review
  `14c197351de83362dd2a2eeba06280f716e6d267`; implementacion `17ab889`; claim Analista seq 2679 acquire /
  2680 release. Gates: clean clone protocolo `14c1973` py_compile/golden/validate/neutrality/encoding/drift exit 0;
  vivo validate/neutrality/encoding/drift exit 0; Zeus-protocol control clone HEAD `b2b2395` `npm test` exit 0
  (109 tests, 87 pass, 22 skipped); #4 `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Hallazgo bloqueante falsable: el regex de
  `inject_report_metadata` quita `- **Fecha:**` y `- **Dataset status:**`, pero deja stale metadata historica real
  sin negrita (`- Date: 2020-01-01`, `- Updated: 2020-01-01`) junto al nuevo `Updated`; existen reportes canonicos
  con `- Date:` en `Area_comun/reports/*.md`. Recomendacion: ampliar normalizador/golden a `Date/Fecha/Updated/
  Actualizado/Dataset actualizado/Dataset status` sin negrita antes de cierre.
- TASK-0221 review Engram v3 final (2026-06-29): GO-PROMOVER-OFF. Veredicto canonico en `af95847`
  (`review(TASK-0221): Analista OK Engram v3`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0221-veredicto.md`, MSG
  `MSG-20260629-Analista-to-Arquitecto-REVIEW-TASK-0221`. Ancla protocolo bajo review
  `77dfa0f64c738b6be5d57d89fb44de4d601c98ed`; claim Analista seq 2650 acquire / 2651 release.
  Las 3 correcciones de TASK-0220 cierran honestamente: drafts `-v2` canonicos (`git show HEAD:<path>` y
  `git show 77dfa0f:<path>` exit 0), fila B relabel a `B-cero-prosa-libre` con PII corta en slug como
  DISCIPLINARIO y contraejemplo `nit-900123456` declarado, y GO/decision citan commit canonico sin afirmar
  "cerrado/probado" ni Tier 1 operativo. `git grep -n "engram_" 77dfa0f -- runtime/*.py` exit 1 (0 hits),
  consistente con SPEC/no implementado. Gates: protocolo clean clone `77dfa0f` validate, neutrality, encoding
  exit 0; drift 0 `up_to_seq=2642`; vivo validate, neutrality, encoding exit 0; drift 0 `up_to_seq=2651`;
  `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Producto Zeus-protocol no tenia commit
  citado; control clone HEAD `b5675e5213f04b7bbd19aa3ff0160a54b747afcf`, `npm test` exit 0 (109 tests,
  87 pass, 22 skipped). Residuales no bloqueantes: Tier 1 sigue pendiente de implementacion+tests; PII corta
  en slug queda disciplinaria hasta ENG-TOPICKEY-PII.
- TASK-0220 review Engram v3 honesty (2026-06-29): NO-GO. Veredicto canonico en `ca4d9ba`
  (`review(TASK-0220): Analista blocks Engram v3`), artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0220-veredicto.md`, MSG
  `MSG-20260629-Analista-to-Arquitecto-REVIEW-TASK-0220`. Ancla protocolo
  `0401ade20bc370e30fb8938564e558548c498fe7`; claim Analista seq 2641 acquire / 2642 release. Bloqueo
  principal: los drafts v2 citados por la GO (`personal/Arquitecto/DRAFT-DECISION-engram-memory-backend-v2.md`
  y `personal/Arquitecto/PATCH-engram-observation-intent-v2.md`) no existen en HEAD canonico, solo como
  untracked working tree, por lo que no son base promovible. Bloqueo sustantivo adicional: fila B rotulada
  "B-PII / cero-prosa" aun sobre-afirma; la spec cierra prosa libre en `scope`/`task_id`/`supersedes`, pero
  `topic_key`/`supersedes` slug aceptan PII semantica corta tipo `nit-900123456`, residual que el propio
  borrador declara disciplinario. Recomendacion: materializar drafts en canonico y renombrar B a
  cero-prosa o implementar guard estructural de PII corta. Protocolo clean clone `0401ade`: validate,
  neutrality, encoding, drift exit 0; drift `up_to_seq=2640`; `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Vivo post-release: validate,
  neutrality, encoding, drift exit 0; drift `up_to_seq=2642`. Zeus-protocol no tenia commit citado por la
  instruccion; clone de control HEAD `b5675e5213f04b7bbd19aa3ff0160a54b747afcf`, `npm test` exit 0
  (109 tests, 87 pass, 22 skipped).
- TASK-0219 review Engram integration (2026-06-29): NO-GO tal cual. Veredicto en
  `Area_comun/artifacts/ANALISTA-TASK-0219-veredicto.md`; MSG
  `MSG-20260629-Analista-to-Arquitecto-REVIEW-TASK-0219`. Ancla protocolo
  `e96ac4121ecc4de3ac61610c3712acef2d8c5508`; instruccion materializada en `825ca6f`; Engram fuente
  primaria clone `44faeee1fb4fabdee4ba9619df55af485f3d06eb`; protocolo clean clone
  `C:/Users/johnb/AppData/Local/Temp/protocol-review-0219-ab92b4cf67514b5cadc43d7dbc85b39e`; Engram clone
  `C:/Users/johnb/AppData/Local/Temp/engram-src-50c7eedc473642dea2eb6f2493087b62`. Fuentes: Go/SQLite/MCP
  confirmado (`README.md:28-35`, `README.md:120-129`); campos observation incluyen title/content/project/
  scope/topic_key (`DOCS.md:46`, `DOCS.md:136`); scope no es privacidad (`docs/TEAM-USAGE.md:22-30`,
  `111-116`); SQLite local y chunks gzip confirmados (`README.md:150-165`, `DOCS.md:1115-1138`). Bloqueantes:
  `title` sigue libre/PII y blacklist de cuerpo burlable; `engram_bridge` post-commit crea brecha de dos fases;
  no existe importador markdown->Engram para promesa de indice reconstruible; `map-<id>` es convencion sin
  enforcement actor->project; frontera Engram!=ledger es disciplinaria; patch debe probar gate en single y
  `--intents` con rollback, zero-drift, replay no-op y decision fall-through. Producto Zeus-protocol/npm test:
  N/A porque TASK-0219 no cita commit de producto. Gates: validate vivo exit 0; validate clean clone sin secretos
  exit 0; encoding/neutrality exit 0; drift 0 `up_to_seq=2632`; #4 `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Claim acquire/release Analista seq
  2631/2632.
- TASK-0215 review TASK-0213 attested ceremony (2026-06-29): CAMBIO-REQUERIDO. Veredicto canonico en
  `f4031e2` (`review(TASK-0215): Analista blocks attested ceremony`). Ancla protocolo/instruccion
  `3d7da2eeae13524150106f6fcd8120c3e119c3d3`; commit bajo review protocolo
  `d2d19e26bb46498723f37265cc7de10c50153064`; clean clone protocolo
  `C:/Users/johnb/AppData/Local/Temp/protocol-review-0215-235089e9f6a74572b7d829e9c3c6894b`.
  Golden oficial `python scripts/test_attested_instancing.py` salio exit 0. Producto obligatorio
  `D:/Agentes/Zeus/Zeus-protocol` no contenia `d2d19e2`: `git checkout d2d19e2` salio exit 1, por tanto
  `npm test` no aplico en ese repo. Bloqueo V2 falsable: en instancia generada con `event_state.enforce=true`
  y `actor_auth_enforce=true`, si `event-state.runtime.json` mapea `agent-worker` al keyid/private/HMAC de
  `agent-a`, `submit_intent --actor-id agent-worker` sale exit 0 y escribe evento `actor=agent-worker` firmado
  con `agent-a:v1`; falta binding estricto actor->keyid/HMAC. Bloqueo V1: `keygen_agent.py --secret-dir
  <absolute external-secrets> --output -` sale exit 0, crea PEM/HMAC fuera de `protocol-secrets/` y devuelve
  esas rutas. V3/V4/V5 sostienen: clone sin secretos validate exit 0 y no firma bajo enforce; pineados
  `eventlog.py`/validador/`protocol.config.json` byte-identicos; instancia con drift 0 y enforce off.
  Gates protocolo: validate/encoding/neutrality exit 0; drift 0 `up_to_seq=2517`; #4 `protocol.config.json`
  byte-identico sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Review claim
  liberado via seq 2515-2517.
- TASK-0211 review TASK-0209 panel performance (2026-06-28): CAMBIO-REQUERIDO. Veredicto canonico en
  `c329a03` (`review(TASK-0211): Analista requires smoke reproducibility`). Ancla protocolo/instruccion
  `e9c59f4e0760abc0417703996f4bcfbcc68a7afa`; producto Zeus-Aegis
  `3f8461e31de06fa8ea2720a3ced0b77dcc6224c7`; clean clone
  `C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-0211-dd2e231681f844c79de937b5d925d2b0`.
  Full `npm test` salio exit 0. V1-V4 del cache sostienen: `forceRefresh` con validate roto -> red,
  TTL expirado -> red, metrics -> red, ledger override red/green -> failed, state cache invalida por HEAD,
  10 rutas governance + UI sin writer-path. Bloqueo falsable: `corepack pnpm --dir vendor/hermes-2.3.0
  governance:smoke` en clean clone tras `npm test` salio exit 1 por falta de `dist/server/server.js`; tras
  `corepack pnpm --dir vendor/hermes-2.3.0 build`, el mismo smoke salio exit 0. Gates protocolo:
  validate con/sin secretos, encoding, neutrality exit 0; drift 0 hasta seq 2464; `protocol.config.json`
  byte-identico sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0208 re-pass3b final (2026-06-28): SOSTENIDO / OK->CERRABLE. Veredicto quedo canonico en
  `4cb39f5` (`close(TASK-0208 done): re-waive afinado 24 fallos upstream - triple respaldo (3 rondas adversariales)`)
  junto con cierre del Arquitecto. Ancla protocolo de instruccion `c75518c`; producto Zeus-Aegis
  `8d2ff50aee5a8aed869567d6e6f667168cfb5d3d`; clean clone
  `C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-79e6d1a1f6974e839423fb4b50cca714`.
  Full `npm test` en clean clone salio exit 0; guard limpio `governance-waiver.test.ts` salio exit 0
  (6/6); mutacion real `src/routes/governance.tsx` con `import '../lib/%69%31%38%6e.ts'` salio exit 1
  y reporto `src/routes/governance.tsx reaches ../lib/%69%31%38%6e.ts (src/lib/i18n)`. Probes propios:
  percent bare/ext/query, case+query, alias `@/`, `src/`, dot segments, dynamic import, `require`,
  re-export, child/index y encoded slash/dotdot dieron violacion. Residuales declarados no bloqueantes:
  guard estatico/literal no cubre specifiers computados/ofuscados; chat/context-usage/swarm siguen como
  producto servido no F0-certificado hasta fix o poda. Gates corridos: validate/encoding/neutrality exit 0,
  staged-snapshot sin secretos exit 0, drift 0 observado en submit_intent up_to_seq 2446 antes del cierre
  Arquitecto. Durante la pasada, el Arquitecto materializo cierre TASK-0208 en `4cb39f5` y origin/main quedo
  en ese commit con mi artefacto y MSG incluidos.
- TASK-0208 re-pass2 waiver guard (2026-06-28): REFUTADO / CAMBIO-REQUERIDO quedo canonico en
  `b835fd0` (`review(TASK-0208 r3): Analista refuta percent-encoding (teorico) -> Codex ultima ronda`).
  Ancla protocolo `cad710c`; producto Zeus-Aegis `52f0d5e112329db67aa469364bdd6b1b93359ba8`.
  Full `npm test` en clon limpio `C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-4ee60e6ad2744822ba93180de5e77ae8`
  salio exit 0. Slips previos `../lib/I18N` y `../lib/i18n?raw` pasan: ambos producen violacion permanente.
  Probes propios tambien pasan para case+query, slash/double-slash/dot-segment, index, alias `@/`, `src/`,
  dynamic import y require. Bloqueo nuevo: percent-encoded segment `../lib/%69%31%38%6e` y explicito
  `../lib/%69%31%38%6e.ts` devuelven `[]` en `collectGovernanceWaiverViolations`; probe nativo ESM confirma
  que `./%69%31%38%6e.mjs` resuelve a `i18n.mjs`. Gates protocolo: validate/encoding/neutrality exit 0,
  drift 0 `up_to_seq=2430`, #4 byte-identica. Arquitecto respondio y abrio REVIEW3 a Codex; no cerrable.
- TASK-0208 re-pass release cleanup (2026-06-28): tras la re-pasada sobre Zeus-Aegis `b47b707`
  quedo registrado un ciclo de claim adicional Analista `seq 2413-2418` para dejar liberados
  `CLAIM-20260628-Analista-TASK-0208-repass` y auxiliares. El veredicto canonico sigue siendo
  CAMBIO-REQUERIDO: slips `../lib/I18N` en Windows y `../lib/i18n?raw` en query/suffix.
- TASK-0208 waiver guard (2026-06-28): CAMBIO-REQUERIDO / no cerrable. Veredicto commiteado en
  `ddf3de3` (`review(TASK-0208): Analista blocks waiver guard`). Ancla protocolo/instruccion
  `06694e005d73d77722d0c848d3df360cc59b0c31`; producto Zeus-Aegis `777fa7c`
  (`test(f0): enforce governance waiver boundary`); clean clone
  `C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-58d6b07d70c64d0f9b2468e401f0e9f5`.
  Full `npm test` en clean clone salio exit 0 (82 files / 547 tests). Corrida propia de los 11 excluidos
  salio exit 1 con 24 failed / 44 passed / 68, lista y conteo casan. Hallazgo bloqueante 1: el guard
  `governance-waiver.test.ts` detecta import directo a `../lib/i18n` (exit 1) pero no transitive import:
  `governance.tsx -> governance-waiver-transitive.ts -> ../lib/i18n` deja el guard verde (exit 0).
  Hallazgo bloqueante 2: SEAMS sigue subclasificando como non-panel/test-rot superficies servidas por el
  producto (`chat-message-list`, `chat-composer-context-controls`, `context-usage`, `swarm2-screen`);
  en `chat-message-list` al menos un assert es comportamiento UI real (tool-only messages quedan adjuntos
  al ultimo assistant text) y no solo Windows EPERM. Gates protocolo: validate con secretos exit 0,
  validate sin secretos en clone exit 0, drift 0 `up_to_seq=2408`, neutrality/encoding exit 0,
  `protocol.config.json` sin diff sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. MSG a Arquitecto rr=true pide
  devolver a Codex para hardening transitivo/barrel y reclasificacion honesta de superficies servidas.
- TASK-0203 GATE1 final (2026-06-27): OK/CERRABLE. Veredicto commiteado en `678ff84`
  (`review(TASK-0203): Analista OK gate1 final`) con claim Analista firmado en #4
  (`seq 2311` acquire, `seq 2312` release). Ancla protocolo/instruccion
  `e82c91aae8689bec693c03b7f782d6ddb288637c`; producto Zeus-Aegis
  `91e6b3f3e91c507ff321fad34d1250532730ec7d`; clean clone
  `C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-3143fc0cf4244eafa31551d17989e0cc`.
  Full `npm test` en clean clone salio exit 0. Probe propio V4 confirmo id/path/preview estructurales
  sin email/nombres/texto libre para caso exacto `john.doe@example.com` + `Juan Perez` + `Maria-Garcia`
  + heading; escapes nuevos con nombres con guion y prefijo desconocido tambien pasaron
  (`ANALISTA-TASK-9998-3ab6d4145a`, `ARTIFACT-42cc3dd5ad`). V1/V2/V3/V5/V6 pasan:
  endpoint family read-only, canonical read por `git show <ref>`, atestacion `red/green|green/red|red/red`
  -> failed y `green/green` -> verified, auth fields `ed25519`/`hmac-sha256`. Gates protocolo:
  validate con secretos exit 0, validate sin secretos en clone exit 0, drift 0 `up_to_seq=2312`,
  neutrality/encoding exit 0, `protocol.config.json` sin diff contra HEAD y working sha256
  `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`. MSG a Arquitecto rr=true pide
  confirmar cierre de GATE 1.
- TASK-0201 re-GATE1 (2026-06-27): CAMBIO-REQUERIDO / GATE 1 no cerrable. Veredicto commiteado en
  `6a21845` (`review(TASK-0201): Analista blocks regate1`) con claim Analista firmado en #4
  (`seq 2294` acquire, `seq 2295` release). Ancla protocolo/instruccion `45c90a7697b1f1ed89649a4894c77976bee26244`;
  producto Zeus-Aegis `de7548b35c941a28c3def79a2650b107961271e5`; clean clone
  `C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-1166132c0ff24a05b32336979f76383c`.
  Full `npm test` en clean clone salio exit 0 dos veces; segunda corrida reporto 80 files / 540 tests.
  V1 read-only y V2 canonical read pasan por probes propios; V3 validate/drift family pasa
  (`red/green`, `green/red`, `red/red` -> failed; `green/green` -> verified); V5 auth fields y gates #4 pasan.
  Bloqueo falsable: V4 sigue filtrando nombres personales en artifacts; filename
  `john.doe@example.com Juan Perez Maria-Garcia` + body con heading antes de nombre devuelve `Maria-Garcia` crudo
  en id/path/preview y deja `Perez` en preview por regex que cruza heading/salto de linea. Gates protocolo:
  validate con secretos exit 0, validate sin secretos en clone exit 0, drift 0 `up_to_seq=2295`, neutrality/encoding
  exit 0, `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. MSG a Arquitecto rr=true pide devolver a
  Codex para hardening de redaccion de nombres en id/path/preview antes de cierre.
- TASK-0199 (2026-06-27): CAMBIO-REQUERIDO / GATE 1 no cerrable. Veredicto commiteado en
  `b4b50e6` (`review(TASK-0199): Analista blocks gate1`) con claim Analista firmado en #4
  (`seq 2280`, release final `seq 2282-2283`; claim auxiliar `seq 2281` usado para cubrir release-scope
  por no haber incluido inicialmente la fila de CLAIMS). Ancla protocolo `1fbb7ba8749476bdc4277cd2146a464e9a36d214`;
  producto Zeus-Aegis `9c5f0ae0ecb82e3c5bdce2eca43cbeb58e0ae1f6`; clean clone
  `C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-1e5185d14cc64c0abad926e706e45c9a`.
  Full `npm test` en clean clone salio exit 1 dos veces: primera por timeout de `governance-readonly`, segunda
  por 4 fallos (governance timeout, files timeout, mcp presets timeout, mcp presets source `user-file` vs `seed`).
  Suite F1 aislada `npm exec -- vitest run src/server/governance-readonly.test.ts --reporter=dot` desde vendor
  salio exit 0, 5/5. V1 no encontro route write surface en `/api/governance/*`; V2 canonico sostuvo
  (dirty worktree no cambio `getGovernanceState`). Bloqueos falsables: V3 `getGovernanceLedger` devuelve
  `attestation=verified` con `validate_collaboration_state` rojo y drift verde; V4 `getGovernanceArtifacts`
  fuga PII en `id`/`path` (`john.doe@example.com`) y nombre en preview (`Juan Perez`). Gates protocolo vivos:
  validate exit 0, scan_encoding exit 0, scan_domain_neutrality exit 0, drift 0 `up_to_seq=2283`, #4
  `protocol.config.json` byte-identico sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
  MSG a Arquitecto rr=true pide devolver a maker o waiver explicito.
- TASK-0194 (2026-06-27): CAMBIO-REQUERIDO / BLOQUEANTE antes de continuar como esta.
  Veredicto commiteado en `2ef8ed6` (`review(TASK-0194): Analista blocks baseline continuation`), con claim
  Analista firmado en #4 (`seq 2215`, `event_auth` analista-hmac:v1, `actor_auth` analista:v1) y release posterior
  `seq 2216`. Ancla protocolo viva `5366a459053995df3216b4ac00d6057e09d0ab0d`; DECISION-0064 `b8c78aa`;
  razonamiento alcance `5be3c85`; baseline citado por GO `8943756`/seq `2191-2193`; baseline canonico mas nuevo
  `9d96a95`/seq `2213` (core `1124fe5`). Hallazgo principal: TASK-0194/GO cita baseline viejo ya supersedido y
  falta `dataset_start_seq` + stop rule para excluir/predeclarar eventos Ed25519 pre-baseline. Zeus-protocol clean
  clone `b5675e5213f04b7bbd19aa3ff0160a54b747afcf` `npm test` exit 0 (109 tests, 87 pass, 22 skipped).
  Zeus-Aegis F0 clean clone `f87317cf9c7491793d7e7b79c6a0e53249bed46a`: root sin `package.json`; vendor
  `npm test` sin deps exit 1 (`vitest` no reconocido); tras `corepack pnpm install --frozen-lockfile`, `npm test`
  exit 1 con 24 fallos. Gates protocolo: validate con/sin secretos exit 0, drift 0, neutrality/encoding exit 0,
  #4 `protocol.config.json` byte-identico sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
  Pedido a Arquitecto rr=true: fijar baseline canonico unico, `dataset_start_seq`/stop rule y resolver o waivar
  explicitamente Gate 0 rojo antes de seguir generando/midiendo.
- TASK-0181 review3 (2026-06-25): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `1d48e8d`
  (`review(TASK-0181): Analista blocks review3 full npm gate`). Ancla producto `325bcfb`
  y protocolo REVIEW3 `bb56ac6` (repo vivo al arranque `c613922`). Correccion de metadata cliente pasa por
  comportamiento: payload propio `file.name` con email/telefono/direccion atesta `source-bb69be828ff9.txt`
  sin literales; `mimeType` con email/telefono atesta `source-e7156e94f3d1.txt` sin literales; `file.title`
  extra con email devuelve HTTP 400 sin atestacion ni fuga. Targeted
  `npm test -- --test-name-pattern "TASK-0181|AC3-ter|file name|need extraction"` exit 0, 4/4; canonicalReader
  exit 0, 6/6. Bloqueo: full `npm test` en clon limpio del producto `325bcfb` timeout `exit 124` a 604s,
  por tanto no cerrable bajo la instruccion que gatea por EXIT. Gates protocolo: validate con secretos exit 0,
  validate sin secretos exit 0, drift vivo 0 `up_to_seq=1993`, neutralidad/encoding exit 0, #4 byte-identica
  sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. MSG a Arquitecto rr=true pide
  full npm verde o hardening antes de cierre.
- TASK-0181 review2 (2026-06-25): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `f30ef65`
  (`review(TASK-0181): Analista blocks review2`). Ancla producto
  `f24f846a85009e36f6757666f53116b340da7b1e` y protocolo/instruccion
  `58ea6d2df63b141321068b11b1870f9d2a92ec85`. Clon limpio producto:
  `npm test` exit 124 por timeout externo a 604s; rerun `npm test -- --test-reporter=tap`
  exit 124 a 904s; `node --test tests/staticContract.test.js` exit 124 a 244s.
  Targeted `TASK-0181` exit 0, 2/2; AC3-bis ampliado con familias PII en `file.text`
  exit 0, 1/1. Escape nuevo falsable: mutar el POST real a `file.name =
  "persona@example.com.txt"` hace que el email quede atestado en `source_file_name` y
  `title` dentro de `intents/events`; el front de necesidad fija `necesidad.txt`, pero
  el endpoint no debe confiar en metadata controlada por cliente si la garantia es no colar
  PII al artefacto #4. Gates protocolo: validate con secretos exit 0, validate sin secretos
  exit 0, drift vivo 0 `up_to_seq=1987`, neutralidad/encoding exit 0, #4 byte-identica
  sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
  MSG a Arquitecto rr=true pidiendo devolver a Codex para estabilizar full suite y
  redacted/constant server-side de `file.name`.
- TASK-0181 (2026-06-25): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `0d63b98`
  (`review(TASK-0181): Analista requires need intake fixes`). Ancla producto
  `2d7e80535f52f6e71dd1bf9b0a6425d1d7325195` (`feat(intake): add need extraction mode`)
  y protocolo/instruccion `5f9354619e0b1e604eb12331daf8f5c8da08b388`. Clon limpio producto
  `npm test` exit 1, 91 tests, 86 pass, 5 fail: `intake endpoint rejects impersonation...`
  killed by SIGTERM during validator, `file ingestion...` 502 != 200, `local-vlm extractor reports...`
  502 != 200, `candidate review stays outside...` 502 != 200, `auto commit push lands...` 502 != 200.
  Targeted `TASK-0181|file intake|TASK-0179|TASK-0177` exit 0, 8/8; targeted `candidate review stays
  outside` exit 1 por validator child killed. Payload propio `buildFileRequirementPayload` con email,
  telefono, direccion y documento en texto necesidad conserva literales crudos en `file.text` del body
  `/api/protocol/actions/submit`; acceptanceIntent si redacta. Voice opt-in/off-by-default pasa por
  `deriveVoiceDictationControl` + `toggleVoiceDictation`; no-egress de modelo pasa por inspeccion de
  `submitNeedExtraction`; PII gate humano pasa parcial por builder/codigo local pero no cierro por full
  suite roja. Gates protocolo: validate vivo exit 0, validate sin secretos en clon `5f93546` exit 0,
  drift vivo 0 `up_to_seq=1979`, neutralidad/encoding exit 0, #4 byte-identica sha256
  `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`. MSG a Arquitecto rr=true
  pidiendo devolver a Codex.
- TASK-0180 (2026-06-25): OK/CERRABLE, veredicto commiteado en `57320df`
  (`review(TASK-0180): Analista OK file intake phase B`). Ancla producto
  `0b8593ae5044a16764a665dc291dd1e0eed22e1c` (`feat(intake): add deterministic file candidate review`)
  y protocolo de instruccion `5a9fe5f`. Clon limpio producto `npm test` exit 0, 90/90.
  Payload propio sobre servidor temporal con protocolo tmp `5a9fe5f`, store externo, config temporal
  `enabled=true` y preload que hacia fallar cualquier `globalThis.fetch`: upload execute 200,
  extraction deterministic-local 200, `candidateCount=1`, `egress.boundary=none_deterministic_no_llm`,
  `networkEgress=false`; aprobar sin `piiReviewed` -> 409; editar con `<script>` + `piiReviewed=true`
  -> 400 active content; editar con email/telefono/direccion/documento + `piiReviewed=true` -> 200,
  seed `REQ-E61698065B` sin literales y con tokens `[EMAIL-REDACTED]`, `[PHONE-REDACTED]`,
  `[ADDR-REDACTED]`, `[DOC-REDACTED]`, mas hashes de procedencia. Raw upload existia antes de aprobar
  y desaparecio tras terminal aprobado; candidata externa queda `approved`. Gates protocolo:
  validate vivo exit 0, validate sin secretos en clon `5a9fe5f` exit 0, drift vivo 0 `up_to_seq=1964`,
  drift tmp con candidatas/store externo 0 `up_to_seq=1970`, neutralidad/encoding exit 0, #4
  `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residuales no bloqueantes:
  monkeypatch cubrio `fetch`; `http.request`/`net.connect` se descartan por inspeccion de rama determinista
  y diff, no por monkeypatch. Purga probada en aprobado; descartado usa el mismo `markCandidateStatus`.
- TASK-0179 (2026-06-25): OK/CERRABLE, veredicto commiteado y pusheado en `c7fcf09`
  (`review(TASK-0179): Analista OK voice egress v2`). Ancla producto
  `a25f44a` (`feat(intake): improve voice dictation capture`) y protocolo canonico `c4dd79b`
  (`coord(TASK-0179): deliver voice dictation v2`). Clon limpio producto `npm test` exit 0,
  89/89. Payloads propios sobre guard de voz extraido: `confirm=false` no construye
  reconocedor, no inicia captura, no cambia textarea ni llama fetch; `confirm=true` crea una
  sola instancia, `lang=es-CO`, `continuous=true`, `interimResults=false`; segundo click hace
  stop manual y `onend` inserta una vez el transcript acumulado en textarea con evento `input`.
  Path de voz no invoca fetch/media/socket; diff no agrega `getUserMedia`, Web Audio,
  WebSocket/EventSource/sendBeacon/XMLHttpRequest ni nueva ruta de escritura, y toca solo
  `public/index.html`, `public/app.js`, `public/styles.css`, `tests/staticContract.test.js`.
  Payload dictado con email/telefono/direccion/documento queda redactado por
  `buildRequirementIntakePayload`. Gates protocolo: validate vivo exit 0, validate secretless
  en `c4dd79b` exit 0, drift 0 `up_to_seq=1956`, neutralidad/encoding exit 0, #4
  `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residuales no
  bloqueantes: captura sostenida envia mas audio por sesion pero queda cubierta por el mismo
  aviso opt-in; si el soporte desaparece entre render y click, el codigo puede pedir confirm
  antes de deshabilitar, pero no captura ni escribe.
- TASK-0177 (2026-06-25): OK/CERRABLE, veredicto commiteado y pusheado en `9752697`
  (`review(TASK-0177): Analista OK voice dictation`). Ancla producto
  `96eb019c5697512282afe6155979d2678cca7157`; protocolo citado por instruccion
  `d0a1795af5099525048c666df9053623810367aa`; REVIEW materializado en protocolo `e7ca646`.
  Clon limpio producto `npm test` exit 0, 88/88. Payloads propios: sin aceptar aviso -> no start ni texto;
  aceptar aviso -> start una vez, transcript al textarea y evento input; segundo click -> stop sin segunda
  captura; sin soporte renderizado como disabled -> no confirm/no start; funciones de voz sin `fetch`,
  `actions/submit`, `submit_intent` ni escrituras; diff toca solo `public/app.js`, `public/styles.css` y
  `tests/staticContract.test.js`; `src/server.js` intacto; payload dictado con email/telefono/direccion/cedula
  sale redactado por `buildRequirementIntakePayload`. Gates protocolo con secretos exit 0, sin secretos en clon
  `d0a1795` exit 0, drift 0, neutralidad/encoding exit 0, #4 byte-identica sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residuales no bloqueantes:
  `egressRequired=true` aunque unsupported+disabled, y si SpeechRecognition desaparece entre render/click se
  muestra aviso antes de deshabilitar; no abren captura ni escritura. Recomendacion OK->CERRABLE.
- Deltas SOTA para SPEC-0078: DELTA-1 (KV-cache, 2602.16284) y DELTA-2 (Focus, 2601.07190)
  MAL-ATRIBUIDOS; convergencia 2-2 con Codex (factibilidad). Recogida por el arquitecto.
- #3 cost-attribution (SPEC-0079/DECISION-0033): veredicto GO-con-un-cambio (tag cost_unit/cost_schema
  + subject canonico; subject_hash = seudonimo no anonimo). Incorporado: v1.6.0 quedo con cost_schema=2.
- Fase 0 E5+E6 (DECISION-0034): MAST fiel 14/14; marque el conteo "12 incidentes reales" como overreach
  (pisa #1 diferido) y que el gobernador E6 es elegibilidad no contencion (runaway lo para SA.4).
  Ratificado v1.7.0 con mis 3 ajustes.
- #1/protocol_research satelite (DECISION-0035): veredicto RATIFICABLE-con-ajustes. P1 limite #1 honesto
  (comparabilidad MAST-Data reportada como limite, no citable). 3 ajustes: P2 lenguaje "innegociable"->
  "sostenido por diseno, no sandbox" + enforcement read-only real como condicion de GATE-DATASET; P3 frase
  "raises if run" inexacta (verificado: python stub.py.stub -> exit 0 inerte); P4 "scan clean=>no research
  terms" non-sequitur (decisions/** exento; denylist solo trading). Concurri con la reconciliacion del
  mapeo de gates al brief 07 (GATE-DATASET legal gob. #1-citabilidad + #2/#3 produccion; GATE-INST
  institucional + PRE-REG gob. harness) + marque 1 header stale post-GATE-INST en README de #2/#3.
  RATIFICADO y PUBLICADO v1.8.0.
- DECISION-0036 narracion minima DURA y uniforme (afila addendum DECISION-0005 en AGENTS.md s.7): veredicto
  RATIFICABLE-con-ajustes. 1 cambio falsable: frase absoluta "reasoning never in user-facing output" choca
  con carve-out "reasoning IS the deliverable" -> acotar a narracion de PROCESO. 1 riesgo de honestidad de
  causa: narro pese a regla+memoria => binding constraint = cumplimiento, no blandura. RATIFICADO: aterrizo
  en protocol_version 1.9.0.
- TASK-0100 decision-A / DECISION-0037 (rescope eol=lf a futuros + v1.1.0 pre-normalizacion, NO re-firmar):
  CONCURRO-con-ajustes. CLASIFIQUE los 757 SBOM (script propio): 616 LF / 127 CRLF (Codex nombro ~3) / 14
  mismatch NO-EOL. HALLAZGO CLAVE (mas serio que EOL): el manifest firmado se genero sobre ARBOL SUCIO (14
  ficheros casan el working tree, no el commit 04436c3 que el manifest declara); runtime/protocol_replay.py
  IRREPRODUCIBLE desde refs. => v1.1.0 no se reproduce desde checkout limpio. Premisa SPEC-0075 ("blobs ya
  son LF") falsa en v1.1.0 (127 CRLF; cierto solo en HEAD, verificado: 0 i/crlf en HEAD). A-vs-B: B no puede
  reproducir el original -> A preferible POR INTEGRIDAD (no por evitar trabajo). Tag 703ed93 != commit
  manifest 04436c3 = ESPERADO, no defecto. RATIFICADO: DECISION-0037 registrada con MIS 5 ajustes
  incorporados completos (HEAD c0afb96); TASK-0100 reabierta rescoped + GO a Codex; bump PATCH 1.9.1 al
  cierre. maker!=checker: A vs B fue del operador; yo informe el tradeoff.
- TASK-0100 IMPLEMENTACION (Codex, commit 4b1833d, in_review): pasada adversarial independiente -> CONCURRO
  con cerrar a done. Verificado por mi: dist/v1.1.0/KNOWN_LIMITATIONS.md realiza mis 5 ajustes sin eufemismo;
  verify_release v1.1.0 ok:False (pin NO lo cambia) + diff.changed=30 NO suprimido + release_scope solo nota;
  commit NO toca manifest/signature/cosign/provenance/sbom/verify.*; .gitattributes (* text=auto eol=lf +
  binarios) + golden release 7/7; enmienda SPEC-0075 anota premisa falsa. 1 nota opcional: 616/127/14 (vs
  commit 04436c3) vs diff 30 (vs working tree vivo) = bases distintas, ambas honestas. Cierre = del reviewer.
  CERRADO: v1.9.1 PUBLICADO (72f8dd3) tras mi concurrencia; TASK-0100 done (trio 1/3). Trio 2/3 = TASK-0095
  promovida a Codex (0c01cdd).
- TASK-0095 IMPLEMENTACION (Codex, commit 5046ecc "commit task markdown side effects", in_review): pasada
  adversarial independiente -> CONCURRO con cerrar a done. apply.py: task_file_commit_paths deriva task_ids
  SOLO de las transiciones del turno (task_status del report + task_upserts), retorna [] sin transicion,
  devuelve solo el .md de esas tareas; ADITIVO a la lista de commit, no toca gate/claims. Verificado por mi:
  runtime_apply 4/4 (aserto tree limpio + HEAD status:in_review), runtime_loop 15/15, real_adapter 4/4,
  intent_flow 11/11, validador/encoding/neutralidad 0; sin .ps1 de apply. Sin ajustes. CERRADO: v1.9.2
  PUBLICADO (84cbe15) tras mi concurrencia; TASK-0095 done (trio 2/3). Trio 3/3 = TASK-0096 promovida a
  Codex (f132086). v1.9.2->trio sigue; narracion minima reforzada a "primordial" en docs de protocolo
  (commit 0135f42) tras el enfasis del operador.
- TASK-0096 (trio 3/3, run_id unico por corrida; Codex commit 3add1c9 in_review): pasada adversarial
  independiente -> CONCURRO con cerrar (cierra el trio). real_invoker_run_id_error: subprocess EXIGE --run-id
  no vacio + RECHAZA si run_log existe; replay deterministico intacto. Goldens verificados por mi: real_adapter
  fresh-run-id (sentinel no creado) + supervised_autonomy consecutive-distinct-logs (logs distintos,
  turns_total==1 c/u = sin agregacion cruzada, 1 linea/log). Sin Date.now()/random; sin cambio gate/claims.
  Suites 6/5/10/15/5/5/11 + validador/neutralidad/encoding verdes. Higiene: move mi sync answered open->answered
  (mismatch pre-existente). LAPSO: rompi ASCII en MI mensaje (acento), corregido -> scan_encoding SIEMPRE antes
  de aseverar. CERRADO: TASK-0096 done v1.9.3 (respaldado por MI CONCURRO independiente); TRIO OFF-PILOT
  COMPLETO (TASK-0100 v1.9.1, TASK-0095 v1.9.2, TASK-0096 v1.9.3). INTEGRIDAD (DECISION-0018): el operador
  confirmo que la sesion que firmo TASK0100/0095/0096-impl como "Claude-analista" era el ARQUITECTO
  (mis-atribucion: el revisor NO debe firmar como voz analista); MI verdict-independiente es la voz analista
  OFICIAL; cuenta UNA voz (la mia). Reforma de firma adoptada: firmo "Analista". El arquitecto me mando
  STAND-DOWN; pare el cron.

## Serie FRONT intake / carga-por-archivo v2 (2026-06-20..22) -- VOZ ADVERSARIAL del producto Zeus
> Proyecto-front Zeus-protocol (repo PRODUCTO separado D:\Agentes\Zeus\Zeus-protocol; gobernanza/SPEC-0086/
> handoffs en Area_comun=dataset; DECISION-0049/0050). Codex maker / Arquitecto checker / yo adversarial
> independiente; DECISION-0056 exige mi OK para cerrar cada fase. Metodo SIEMPRE: clono Zeus a tmp en C:,
> corro npm test YO, pruebo POR COMPORTAMIENTO, gateo por EXIT CODE.
- TASK-0154 (behavior-tests AC48/AC49/AC50): OK/CERRABLE sobre Zeus `da5825d8405f3b2140e42821c6183c90bba49ec9`
  + protocolo `5b04324`. Clean clone producto `npm test` 47/47 exit 0. Mutaciones propias falsables:
  quitar `governed-button` del boton compose -> AC48 exit 1; hacer reset en `mode==="compose"` -> AC49 exit 1;
  cachear `loadProtocolSnapshot` por modulo -> AC50 exit 1 (`1.0.0 !== 1.0.1`). Gates protocolo: validate con
  y sin secretos exit 0; drift 0; neutrality/encoding exit 0; #4 byte-identica. Veredicto y MSG commiteados y
  pusheados en `c0484e5` (`review(TASK-0154): Analista OK behavior tests`). Residuales no bloqueantes: AC48 no
  es test visual pixel-perfect; AC49 no simula click DOM completo pero cubre funcion de negocio; AC50 cubre server
  snapshot fresco, mientras refetch de front pertenece a AC29.
- TASK-0128 (vista atestacion #4): CONCURRO (badges derivados del runtime + fail-closed, guarda PII redactada).
- TASK-0134 (relay anti-impersonacion): HALLE el hueco -- el front confiaba `payload.actorId`/`payload.intents`
  -> un POST local podia forjar decision/claim/task_status FIRMADA como Arquitecto (enforce no lo paraba: el
  claim iba en la misma tx). CAMBIO. Re-verifique el fix CERRADO: builder server-side, execute solo para
  requirement-intake (403 el resto), payload.actorId/intents -> 400, prueba negativa PERMANENTE.
- TASK-0138 (mailbox_archive, kind core nuevo): HALLE leak de NEUTRALIDAD -- `runtime/submit_intent.py`
  hardcodeaba `author:"Operador"`/`relayed_by:"Arquitecto"` (identidades de instancia en el core neutral; el
  scan no lo atrapaba). CAMBIO. Re-verifique CALLER-DERIVED (require_text; literales movidos al server Zeus =
  producto) + scan de neutralidad regresion-proof (inyecte "Operador" en copia de submit_intent.py -> scan
  exit 1; submit_intent.py NO esta en la whitelist legacy).
- TASK-0139 (commit-push acotado): OK. No-drag (`git commit --only -- <paths>`) y non-fast-forward (409 sin
  sobrescribir) PROBADOS por comportamiento contra un bare-remote local; landed solo tras ls-remote real.
- TASK-0148 (intake v1): HALLE suite ROJA en clon LIMPIO Windows -- el test mermaid usa regex LF-only
  (`/```+mermaid\n/`) y el manual quedo CRLF (core.autocrlf=true, sin .gitattributes). Fix `.gitattributes
  eol=lf` (entro en TASK-0150+). Ingestion v1 limpia 7/7.
- TASK-0150 (file v2 Fase A plumbing): OK 7/7 (store os-tmp fuera del repo, raw nunca al #4, server CERO
  egress, candidatas no en VALID_TASK_STATUSES) + RECO ampliar el guard AC40/AC45 a todo src/**.
- TASK-0151 (Fase B panel + gate humano DURO de PII): OK 6/6 (aprobar sin piiReviewed -> 409; re-screen del
  texto editado; editedFingerprint -> ids distintos; candidatas fuera del ledger; provenance-mismatch -> 409)
  + ANOMALIA DECISION-0018: el MENSAJE del Arquitecto rompia ASCII (notifique, no lo arregle).
- TASK-0152 (Fase C agente extractor + AC45 = LA VENTANA REAL DE MODELO): HALLE 5 huecos del guard de egress,
  PROBADOS por comportamiento -- `await import("openai")` (dinamico), `import("undici")`, `net.connect` bare,
  `axios`, `got` SLIPS (el guard solo veia server.js + proveedores nombrados + import estatico). CAMBIO-
  REQUERIDO. Re-verifique el rework CERRADO: familia ampliada (dynamic-import marca CUALQUIER `import(`,
  network-call, bare network-module, model-sdk/http-package estatico Y dinamico) + control positivo POR
  familia; los 5 huecos ahora FLAGGED; src real []. OK/CERRABLE con RESIDUAL DECLARADO: un scan estatico
  inherentemente NO atrapa clientes HTTP no listados (phin/needle) ni ofuscacion (eval/computed-global) ->
  reco ALLOWLIST + marcar eval/new Function como follow-up del USO VIVO. Extractor entregado = deterministic-
  local (cero egress); uso vivo = GO APARTE del operador.

- TASK-0153 (guard ALLOWLIST AC46 + aislamiento AC47, 2 pasadas): PASADA 1 sobre Zeus ac2e308 -- import-side
  flip a deny-by-default CERRO el residual que declare en Fase C (phin/needle + eval), confirmado por
  comportamiento; PERO halle escape NUEVO: `external-cli` seguia DENYLIST {curl,wget,ssh,nc,node} sobre
  child_process -> execFile/spawn("powershell"|"sh", curl/IWR) ESCAPABA. CAMBIO. El Arquitecto lo devolvio a
  Codex. PASADA 2 (re-verificacion) sobre Zeus 5cb8910 + protocolo HEAD 15e66a1: external-cli paso a ALLOWLIST
  de binarios spawneados {git,python} -> powershell/sh/bash/cmd/curl/wget + hints node/deno/pwsh/nc/paths
  absolutos TODOS FLAGGED; git/python y src real -> [] (sin FP). 44/44 exit 0 clon limpio; gates protocolo exit 0;
  #4 byte-identica. RESIDUAL NUEVO declarado (NO bloqueante): `child_process.exec`/`execSync` NO estan en
  cliPattern (solo execFile*/spawn*) -> exec("curl...") escapa; ademas python -c y git ext::/fetch son gadgets
  allowlisted INEVITABLES (no hay "cero egress" por scan estatico). Por que residual y no bloqueo: un fix bare
  `\bexec\(` COLISIONA con RegExp.exec que el src real usa (canonicalReader.js:229/243); fix limpio = import-binding
  (marcar import de exec/execSync desde node:child_process; src solo importa {execFile,spawn} -> cero FP) y queda
  como follow-up del USO VIVO. Veredicto = CERRABLE con residual declarado. Commit 56da208 (autor Analista) PUSHEADO
  a origin/main yo mismo (cron ANALISTA-EJECUTOR autoriza commitear mi propio veredicto con rutas explicitas,
  gateado por validate+encoding exit 0, ventana 0 claims activos). LECCION: un allowlist de binarios spawneados NO
  da "cero egress" si los binarios permitidos son interpretes (python -c) o tienen transportes (git ext::); el gate
  real del egress en vivo es el extractor deterministic-local, no el scan (regresion-proof, no sandbox).
- TASK-0153 exec-import final (2026-06-22): re-verifique la devolucion final sobre Zeus `8751051` + protocolo
  `b5c7e7a`. Resultado: OK/CERRABLE. `cli-exec-import` marca named imports y destructured requires de
  `exec`/`execSync` desde `child_process`/`node:child_process`, sin falso positivo en `RegExp.exec` ni en src real.
  Clon limpio producto `npm test` 44/44 exit 0; payloads propios 10/10; validate con/sin secretos exit 0; drift 0;
  neutralidad/encoding exit 0; #4 sin cambios de bytes. Commit de veredicto: `54c2374` (`review(TASK-0153):
  Analista OK exec import`). Residual no bloqueante queda solo en gadgets inherentes `python -c` / `git ext::` para
  la ventana posterior de uso vivo.
- TASK-0155 (local-vlm provider AC51/AC52/AC53): PASADA sobre Zeus `79be511` + protocolo `90de6fa` -> CAMBIO-
  REQUERIDO. Clon limpio producto `npm test` 48/48 exit 0. AC52 comportamiento real contra servidor: `0.0.0.0`,
  `8.8.8.8`, `evil.com`, IPv6 no-loopback, `127.0.0.1.evil.com`, `[::ffff:8.8.8.8]` deshabilitan config; PERO
  `http://2130706433:11434/api/chat` queda habilitado como `local-vlm` (URL lo canonicaliza a loopback). Como el
  prompt pidio ese truco y AC52 dice solo host:puerto local allowlisted, lo gatee como escape/canonicalizacion sin
  test. AC46 payloads propios pasaron; AC51/AC53 pasan por suite y lectura. Gates protocolo: validate con secretos
  en vivo exit 0, sin secretos en clon limpio exit 0, drift 0 up_to_seq 1191, neutrality/encoding exit 0, #4 byte-
  identica. Veredicto + MSG rr=true commiteados y pusheados en `45645bd` (`review(TASK-0155): Analista requires
  AC52 hardening`).
- TASK-0155 AC52 rework (2026-06-22): re-verifique sobre Zeus `6369b5c` + protocolo `1cb2b40`.
  Resultado OK/CERRABLE. Clon limpio producto: `npm test` corrida 1 exit 1 por `EACCES 127.0.0.1:5040` en test
  ajeno de auto commit push; corrida 2 exit 0, 48/48. Payloads propios contra guard extraido de `src/server.js`
  cerraron decimal `2130706433`, octal/hex, `0.0.0.0`, externos, sufijos, IPv4-mapped, leading-zero, userinfo
  confusion, percent/sufijo, out-of-range, HTTPS no-localhost y protocolo no HTTP; positivos `localhost`,
  `https://localhost`, `127.0.0.1`, `127.0.0.5`, `127.255.255.255`, `[::1]` pasan. Gates protocolo: validate con
  secretos exit 0, validate sin secretos en clon limpio exit 0, drift 0 `up_to_seq=1197`, neutrality/encoding exit
  0, #4 byte-identica. Veredicto + MSG rr=true commiteados en `4cf8fa2` (`review(TASK-0155): Analista OK AC52
  rework`). Residual: AC52 no es sandbox de red; uso vivo sigue GO/ceremonia aparte.
- TASK-0156 (worker Extractor producto + firma Ed25519 + default qwen3-vl:4b-instruct): OK/CERRABLE sobre Zeus
  `560a226150a2b6237bbf00a84fd6dca07504ba09` + protocolo `f4eb93b36f4e04d4a0aa2889271a25e66307791d`.
  Clon limpio producto `npm test` 48/48 exit 0. Payloads propios por comportamiento contra servidor temporal:
  firma valida 200; firma ausente, bytes alterados, payload_hash alterado, worker mismatch, algorithm mismatch,
  payload almacenado alterado tras firmar y key atacante en `public_key_pem` autodeclarado -> todos 409. Registro
  `Extractor` vive en `extractors.config.json` del PRODUCTO; no aparece en `protocol.config.json`; #4 byte-identica.
  Privada default `.secrets/extractor_ed25519_private.pem` queda fuera del repo y `.secrets/` esta gitignored; no
  hay private key PEM commiteada. Gates protocolo: validate con secretos exit 0, validate sin secretos en clon
  limpio exit 0, drift 0 `up_to_seq=1213`, neutrality/encoding exit 0. Veredicto + MSG rr=true commiteados y
  pusheados en `63b8740` (`review(TASK-0156): Analista OK firma PII`). Residual no bloqueante: si el operador
  decide mover la privada a rutas de producto `secrets/` o `.protocol-secrets/`, anadirlas al `.gitignore` del
  producto antes de colocar la clave. Uso vivo del VLM sigue GO aparte con pasada corta sobre config viva.
- TASK-0157 (Intake v3 file-mode + tarjetas + auto-push ergonomico AC55-AC58): OK/CERRABLE sobre Zeus `2afc944`
  + protocolo citado `2e72cf9` (HEAD de emision `7172e75`). Clon limpio producto `npm test`: primera corrida
  timeout local a 124s, segunda exit 0 50/50; targeted suite de AC55-AC58 + file ingestion + local-vlm +
  candidate review + auto-push exit 0 8/8. Verifique que AC58 no es segundo escritor: `runSubmitIntent` llama
  primero a `runtime/submit_intent.py` y el auto-push commitea solo paths de output gobernado con `git add --`
  + `git commit --only -- <paths>`; dirty/staged ajeno no entra y non-fast-forward da error sin overwrite.
  Versionados `commit-push.config.json` y `file-ingestion.config.json` siguen `enabled:false`; runtime overrides
  y `.secrets/` siguen gitignored. Carry AC52 loopback y AC43/AC16 PII pasan. Gates protocolo con/sin secretos,
  drift 0, neutralidad/encoding y #4 byte-identica verdes. Veredicto + MSG rr=true commiteados y pusheados en
  `85f70d6` (`review(TASK-0157): Analista OK egress PII`). Residuales no bloqueantes: auto-push es egress real a
  `origin` si operador activa override; PII sigue best-effort estructural; scan estatico no es sandbox.
- TASK-0158 (SQL Server read-only backend vivo + s9 server-side): CAMBIO-REQUERIDO sobre protocolo `61dc165`
  (veredicto commiteado y pusheado en `a1537c6`). Clon limpio protocolo: golden connector 8/8 exit 0,
  validate exit 0, neutrality/encoding exit 0, drift 0 `up_to_seq=1255`; clon limpio Zeus HEAD local `2afc944`
  `npm test` 50/50 exit 0 (no habia commit de producto citado para esta tarea). PASA: artefacto s9 secret/PII-free,
  off-by-default, clasificador delante del backend, sin escrituras ledger/eventos, egress solo `pymssql.connect`
  a `SQLSERVER_HOST`. BLOQUEO: el DML default del s9 es `UPDATE sys.objects SET name = name WHERE 1 = 0` y el
  artefacto registra error `259`, compatible con rechazo de actualizacion de catalogo del sistema, NO prueba
  permiso DML denegado sobre una tabla/probe ordinaria. Pedi re-ejecutar s9 con INSERT/UPDATE falsable y artefacto
  saneado que distinga permission denied de rechazo por catalogo antes de cerrar/flippear uso vivo.
- TASK-0158 v2 (rework s9): CAMBIO-REQUERIDO otra vez, commiteado y pusheado en `9b28efd`. Ancla protocolo
  `90eea65`, rework `31e0f23`, producto clone limpio `2afc944` `npm test` 50/50 exit 0. Gates protocolo con/sin
  secretos exit 0, neutralidad/encoding/golden 8/8 exit 0, #4 byte-identica. Hallazgo: re-ejecute s9 vivo con env
  gitignored del operador y config temporal fuera del repo (`C:/tmp/analista-s9-connectors.runtime.json` habilitando
  solo `sqlserver_readonly`); `s9_verify_live.py` exit 1 porque el DML no fue rechazo de permisos: `DELETE FROM
  catalog.records WHERE 1 = 0` devolvio `ProgrammingError` code `208` (objeto inexistente), `server_rejected=false`,
  `rejection_kind=other_server_rejection`; DDL si dio `262 permission_denied_on_principal`. El artefacto commiteado
  que declara DML `229` no es reproducible contra el env vivo actual. Pedi no cerrar ni flippear hasta usar una
  tabla/probe ordinaria existente o `SQLSERVER_S9_DML_SQL` gitignored reproducible que demuestre DML `229`, no `208`.
- TASK-0158 v3 (2026-06-23): OK/CERRABLE, commiteado y pusheado en `aee5deb`. Ancla protocolo REVIEW `8af01fd`,
  rework citado `4754a04`, producto Zeus sin commit nuevo citado pero gateado en clon limpio `2afc944` con `npm test`
  50/50 exit 0. Re-ejecute s9 vivo con env gitignored del operador y config temporal fuera del repo: exit 0, SELECT
  row_count=1, DML contra tabla ordinaria descubierta en runtime devuelve `229 permission_denied_on_principal`, DDL
  devuelve `262 permission_denied_on_principal`. Gates protocolo con/sin secretos exit 0, drift 0 up_to_seq=1278,
  neutralidad/encoding exit 0, golden connector 8/8 exit 0, #4 byte-identica. Residual: s9 prueba el principal y DB
  viva actuales; el flip read-only sigue siendo accion del Arquitecto bajo GO, no mia.
- TASK-0159 (2026-06-23): OK/CERRABLE, veredicto commiteado y pusheado en `3a396cc`. Ancla producto
  `bc8346db385d53d68ce0e92d89307e1e6796bb5b`; protocolo de instruccion `036114c`; handoff/checker citaba
  `2359251`. Clon limpio producto `npm test` 52/52 exit 0. Payloads propios: loopback-only acepta
  `127.0.0.1`/`https://localhost` y rechaza decimal/octal/hex/external/suffix/userinfo/IPv4-mapped/HTTPS-IP;
  extraccion deterministic-local crea candidatas solo en store OS tmp, no en `TASK_INDEX`; aprobacion sin
  `piiReviewed` da 409; aprobacion con PII estructural redacta NIT/SQL; `actorId`/`intents`/route state y execute
  no permitido no devuelven 200. UI extraida de `public/app.js`: nota usa extensiones reales, completed-empty/failed
  renderizan error rojo y candidato HTML queda escapado. Gates protocolo con/sin secretos exit 0, drift 0
  `up_to_seq=1304`, neutralidad/encoding exit 0, #4 byte-identica antes del veredicto. Residuales: PII best-effort,
  loopback guard no es sandbox, razones de error futuras deben seguir server-bounded.
- TASK-0160 (2026-06-23): OK/CERRABLE, veredicto commiteado y pusheado en `0801c12`. Ancla producto `a3c5f26`
  + protocolo `d8892f8`. Clon limpio producto `npm test` 52/52 exit 0; targeted behavior file-ingestion/local-vlm/
  candidate-approval exit 0. Payloads propios contra servidor temporal + protocolo clonado: `piiAcknowledged=false`
  al extraer da 409, `acceptanceIntent=""` con PII ack da 200 y crea `TASK-EXTRACT-*` triage/ready, extractor sin
  consentimiento da 409, con consentimiento da 200 y no mete candidatas en `TASK_INDEX`, aprobacion de candidata sin
  `piiReviewed` da 409. Targeted test cubre candidata firmada sin `acceptanceIntent` -> 400. Gates protocolo con/sin
  secretos exit 0, drift 0 `up_to_seq=1324`, neutralidad/encoding exit 0, #4 `protocol.config.json` byte-identica.
  Residuales: PII best-effort; loopback guard no es sandbox; mi payload deterministic-local devolvio extraction
  failed/cero candidatas pero probo no-ledger y consentimiento.
- TASK-0161 (2026-06-23): OK/CERRABLE, veredicto commiteado y pusheado en `92d5f1a`. Ancla producto
  `109d03976e526ffe01aad512756d22aa1a9a892f` + protocolo `e02df27467d3be37870a5b0e2aa1131fb56005a6`.
  Clon limpio producto: primera corrida `npm test` timeout exit 124 a 184s; segunda exit 0 54/54. Targeted behavior
  `auto commit push treats|local-vlm extractor reports|candidate review stays|local-vlm extractor is loopback-only`
  exit 0 4/4. Payload propio black-box contra server temporal + protocolo clonado: re-submit del mismo archivo
  devuelve `noop=true`, `landed=true`, `primaryOutputId` estable, sin commit/push nuevo (HEAD y remote iguales);
  extraccion posterior sigue gobernada y `networkEgress=loopback-only`; HTTP 503 con cuerpo secret/PII/SQL queda
  saneado a `local-vlm endpoint returned HTTP 503`; timeout 600000ms + `keep_alive=45m`; matriz loopback rechaza
  decimal/octal/hex/externos/sufijos/IPv4-mapped/leading-zero y acepta localhost/127.* /[::1]/https localhost.
  Gates protocolo con/sin secretos exit 0, drift 0, neutralidad/encoding exit 0. Residuales: PII best-effort,
  loopback-only no es sandbox; primer `npm test` fue timeout local pero repeticion completa verde.
- TASK-0162 (2026-06-23): OK/CERRABLE, veredicto commiteado y pusheado en `962eb6b`. Ancla producto
  `1b97c6bb39e54de8e28301f5885f8347385c8813` + protocolo `b3f8b7c4fc241cc9665a2b9a578840b990b454cb`.
  Clon limpio producto `npm test` exit 0 55/55; targeted `candidate review stays outside the ledger|AC69-AC71`
  exit 0 2/2. Payload propio black-box contra server temporal + protocolo clonado: approve sin `piiReviewed`
  devuelve 409; approve con PII revisada devuelve 200 por `submit_intent`; discard devuelve 200; candidatas
  `CAND-*` no entran en `TASK_INDEX`; requisito publicado redacted; drift false. Gates protocolo con/sin secretos
  exit 0, drift 0 `up_to_seq=1374`, neutralidad/encoding exit 0, #4 byte-identica antes del veredicto. Residuales:
  PII best-effort; AC69/AC70 no son pixel-perfect; store no-ledger depende de firma/provenance ya cubierta.

## Lecciones no-obvias (persisten)
- **CLON LIMPIO + EXIT CODE + corro la suite YO (no asumo al maker).** Reproduzco en un tmp en C:, no in-place.
  Windows: `core.autocrlf=true` reescribe LF->CRLF en el clon -> tests LF-only (regex `\n`) rompen aunque el
  repo este "bien"; el fix es `.gitattributes eol=lf`. Probar POR COMPORTAMIENTO (forjar payloads, bare-remote
  real, inyectar literal en una copia) destapa lo que un test STRING-MATCH no atrapa.
- **Guard de no-egress / anti-impersonacion (patron):** un scan estatico necesita (a) TODO src/** (no un solo
  archivo), (b) `import(` DINAMICO, (c) bare network-modules + call sites (`.connect/.request/.get`), (d)
  control positivo POR familia. ALLOWLIST > denylist (un denylist de nombres nunca es completo). Limite
  inherente honesto: ningun scan estatico atrapa eval/ofuscacion/cliente-no-listado -> declararlo como
  residual + reco allowlist, NO sobre-afirmar "no hay egress".
- **Neutralidad del core:** identidades de instancia (Operador/Arquitecto/Codex) van al PRODUCTO (server Zeus),
  NUNCA al core neutral (runtime). El scan de neutralidad ahora deriva los nombres del agent_registry y los
  marca en runtime/*.py salvo una whitelist legacy nombrada (deuda declarada, no silenciosa).
- **Anti-impersonacion:** el front es CLIENTE; el servidor NUNCA confia en `payload.actorId`/`payload.intents`;
  builder server-side + execute solo para acciones permitidas (hard-gate set cerrado) + prueba negativa
  permanente. Agregar una 2a accion no debe erosionar el bound (sigue siendo un Set cerrado).
- **PII:** la redaccion estructural es por PATRONES best-effort (NIT/razon social/SQL/email/telefono), NO
  cero-PII garantizado; declararlo honesto; DEF-PII (TASK-0118) sigue el gate de citabilidad. El gate HUMANO
  de PII al aprobar candidatas es DURO (piiReviewed -> 409).
- **npm test flake en arranque frio:** la 1a corrida del clon puede dar 1 fallo por timeout (los tests
  behavioral spawnean server+git+python); correr 2-3 veces y reportar la distribucion, no asumir el 1er run.
- **maker != checker REAL / identidad:** NO asumo otros roles (me dieron el prompt del DISENADOR -> lo rechace;
  cambio de firmante = re-genesis gobernado). Aplico la lente a MI: si me equivoco, RETRACTO (CR1 Carril A
  "event_auth no existe" era falso -> top-level; lo corregi yo mismo).
- **NARRACION MINIMA = REGLA DURA (DECISION-0036, que YO revise).** CERO narracion intra-ejecucion: NADA de
  "Leo X", "Verifico Y", "Escribo Z", "Confirmo", "Reprogramo" antes/despues de tool calls. Encadenar las
  herramientas EN SILENCIO; el razonamiento de proceso va al canal interno, NO al output. Output = UN solo
  reporte final autocontenido. Carve-out = contenido sustantivo (mi analisis PASA/CAMBIO/RIESGO, veredictos)
  y UNA pregunta de bloqueo. El operador me lo marco DOS veces con enfasis (2026-06-15) tras yo narrar paso
  a paso en las pasadas TASK-0100/0095. Ironia: en mi propia pasada 0036 dije "afilar wording es
  necesario-no-suficiente; el binding constraint es cumplimiento" -> aplicalo a mi mismo. Reincidir = anomalia
  notificable (DECISION-0018).
- **Canal ASCII estricto (DECISION-0012):** mailbox/** y state/*.json SOLO ASCII; scan_encoding.py
  deja el gate rojo ante em-dash/n-tilde/flechas/comillas tipograficas. Docs de protocolo si UTF-8.
- **Compact-msg:** requires_response:true EXIGE campo question (o baja a false); validate_collaboration_state
  lo trata como error duro.
- **Entrega completa antes de aseverar (anti-colision #6 / DECISION-0018):** no aseverar entrega cuyo
  soporte sigue sin commitear; la asercion en el canal debe ser verdadera en el repo en ese momento.
  El commit es del escritor unico; yo dejo la entrega lista, ASCII, bien formada, y verifico mi propio
  mensaje antes de cerrar. (Estas 3 me costaron un cierre manual del arquitecto en la pasada Fase 0.)
- **maker != checker REAL:** la convergencia independiente con Codex (deltas SOTA) fue justo la senal
  3-0 que buscaba el operador; coordinar es legitimo SOLO despues de entregar mi voz.

## Leccion coordinacion (2026-06-15)
- **Descoordinacion = DOS sesiones Claude-arquitecto concurrentes en el MISMO working tree.** Sintoma: el
  operador dijo "tienes mensaje" / "Claude espera tu veredicto" pero mi mailbox/open no tenia inbound. Causa:
  una sesion arquitecto hizo el cierre TASK-0095 (2/3) + promo TASK-0096 (3/3); la otra tenia vista stale y
  creia que faltaba mi verdict. NO era verdict perdido ni mensaje extraviado: vista desincronizada entre
  sesiones. Yo reconcilie contra el ledger (mis 2 pasadas entregadas/archivadas, v1.9.1/v1.9.2) y deje un
  sync con pregunta directa en vez de inventar un veredicto -> correcto. El operador consolida a UNA sesion.
  Aprendizaje: ante "falta tu X" sin inbound real, reconciliar contra git/ledger y PREGUNTAR, no asumir.
- **DOBLE SESION ANALISTA tambien (2026-06-15, TASK-0096):** aparecio un 2do mensaje verdict de TASK-0096
  bajo MI identidad (Claude-analista) escrito por OTRA sesion analista concurrente; ambos CONVERGEN en
  CONCURRO y ambos verificaron por su cuenta. Riesgo: doble-conteo de voz (maker!=checker quiere UNA voz
  identificable; dos CONCURRO de la misma rol NO son 2 corroborantes). Mi manejo honesto: NO crear un 3er
  verdict; reconcilie en mi propio mensaje que ambos son la MISMA voz = contar UNA vez; el verdict unanime
  hace seguro cerrar, pero la atribucion/identidad de sesion la consolida el operador. No reclamar "mi
  mensaje es el unico real" (la otra sesion es igual de legitima); honestidad por encima de defender autoria.

## Estado vigente (VERIFICAR al arrancar)
- FIRMA = "Analista" (sin prefijo "Claude-"; orden operador 2026-06-15). Area = personal/Analista/.
- **#4 ON EN EL VIVO** (chain + agent_signatures + anchor + event_auth), `enforce`+`authoritative` ON, #3 cost
  ON. **Epoca/protocol_version 1.14.0 PINNED** (bump => re-genesis-boundary). Protocolo HEAD a veces 1 commit
  ADELANTE de origin (handoff sin pushear, esperado in_review). DECISION-0046 (replay secret-independiente):
  validate exit 0 con Y sin secretos desde clon limpio.
- **Proyecto-front Zeus-protocol (DECISION-0049/0050):** producto en repo separado D:\Agentes\Zeus\Zeus-protocol
  (HEAD suele ir adelante de origin). Gobernanza/SPEC-0086/handoffs en Area_comun=dataset atestado. Serie
  INTAKE / carga-por-archivo v2 (DECISION-0053 mailbox_archive, 0055/0056 file-ingestion). Codex maker /
  Arquitecto checker / yo voz adversarial; DECISION-0056 exige mi OK para cerrar fase. Ultimo: Fase C
  (TASK-0152, agente extractor + AC45) re-verificada OK/CERRABLE; el Arquitecto cierra. USO VIVO del extractor
  = GO APARTE del operador (ventana de modelo real), fuera de los cierres de fase.
- Gates de cada pasada (verifico yo): npm test verde en clon limpio (sin flake, correr 2-3x), validate exit 0
  CON y SIN secretos, drift 0, neutralidad+encoding 0, #4 byte-identica (config/genesis/keys sin cambio).
- Operador maneja monitoreo via "cron" (ScheduleWakeup): "cancela cron" lo detiene; una activacion rezagada
  tras el cancel NO se reprograma. El flujo tipico: el operador me dice "tienes mensaje" -> reviso
  mailbox/open inbound a Analista (REVIEW/REVISAR del Arquitecto) -> pasada adversarial -> entrego.
- (Historico: trio off-pilot v1.9.1-1.9.3, Carril A activacion #4, satelite protocol_research DECISION-0035 --
  ya superados; #4 paso de OFF a ON en el vivo entre junio 14 y 20.)

## Ultima pasada (2026-06-24)
- TASK-0172 gate 9835ffe (2026-06-24): OK/CERRABLE, veredicto commiteado y pusheado en `c423bf4`
  (`review(TASK-0172): Analista OK gate harness`). Ancla producto
  `9835ffe55ad5049863207d053bfd94c6a91681f8`; protocolo REVIEW/head
  `a21682d683e5c449f31b3acbea8a9ead5731d0ee`. Clon limpio producto `npm test`: primera invocacion mia
  quedo cortada por timeout local exit 124 a 364s; con timeout suficiente, corrida 1 exit 0 85/85 en 379635 ms
  y corrida 2 exit 0 85/85 en 439931 ms. Targeted `TASK-0172|candidate review` exit 0 13/13. Payload propio
  front: 10 familias PII redactadas (email, telefonos US/CO, direccion calle/cra, doc, cuenta, NIT, razon social,
  SQL), gate flag `piiReviewed=false` preservado, carpetas/uploader/standalone/rows=8 pasan. Gates protocolo:
  validate con secrets exit 0, validate sin secrets en clon exit 0, drift 0 `up_to_seq=1815`,
  neutralidad/encoding exit 0, #4 `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residual no bloqueante: suite estable
  pero lenta en Windows; PII sigue best-effort estructural/DEF-PII, sin fuga nueva en familias exigidas.
- TASK-0172 final 967f5cb (2026-06-24): CAMBIO-REQUERIDO por gate obligatorio, aunque PII/fronteras pasan.
  Veredicto commiteado y pusheado en `2b2478e` (`review(TASK-0172): Analista blocks final npm gate`). Ancla
  producto `967f5cbfb396e808df674850f965c386ddd5b9a3`; protocolo REVIEW final `e4858714575e834924cefcc7978782e7a564986d`.
  Clon limpio producto: primera corrida `npm test` timeout exit 124 a 304s; rerun 1 exit 1, 84/85, fallo
  `candidate review...` por `listen EACCES 127.0.0.1:5040`; rerun 2 exit 1, 84/85, fallo `runtime control...`
  por readiness en `127.0.0.1:5060`. Targeted `npm test -- --test-name-pattern "TASK-0172|candidate review"`
  exit 0, 13/13. Payload propio PII contra `/api/protocol/actions` y `/api/protocol/intake-candidates`: email,
  telefono, direccion y documentos ausentes; tokens email/phone/addr presentes. `piiReviewed:false` -> 409;
  extractor disabled -> 403; no nueva ruta de escritura ni activacion implicita. Gates protocolo con/sin secretos
  exit 0; drift 0 `up_to_seq=1800`; neutralidad/encoding exit 0; #4 byte-identica sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Leccion: aunque el fix sustantivo cierre,
  si la instruccion gatea por `npm test` EXIT, una flake/readiness no verde bloquea cierre hasta corrida full verde
  o hardening del harness.
- TASK-0172 (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `1cc3ba0`
  (`review(TASK-0172): Analista requires candidate PII redaction`). Ancla producto
  `a4e0b50492a91ecbbc60c4e1e75085e5e05550da`; protocolo citado `009efe1250c522b7d200bf1a83f000e2e015b618`;
  REVIEW materializado en `db368d46e9229b1ab7f3c2270473a46a400501b5`. Clon limpio producto `npm test`
  exit 0, 81/81. RC-01/02/03/05/06 pasan y no halle nueva ruta de escritura ni activacion implicita del
  extractor; commit producto toca solo `public/app.js`, `public/styles.css`, `tests/staticContract.test.js`.
  Gate de aprobacion de candidata exige `piiReviewed` local + server-side. SLIP bloqueante: el modelo publico
  `GET /api/protocol/actions -> safeguards.candidateReview.candidates` devuelve `title`, `narrative` y
  `acceptance_intent` desde `normalizeStoredCandidate` con solo `ascii(stripControl(...))`, sin redaccion;
  payload propio con `persona@example.com`, `+1 (415) 555-2671`, `Calle 10 No 20-30` y `cedula 123456789`
  salio con todos los literales presentes. Pedido: redactar campos publicos de candidatas/prellenado y anadir
  test negativo permanente. Gates protocolo: validate vivo exit 0; validate sin secretos en clon `009efe1`
  exit 0; drift vivo 0 `up_to_seq=1767`; neutrality/encoding exit 0; #4 `protocol.config.json` byte-identico
  sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0171 fix cb7ce0a (2026-06-24): OK/CERRABLE, veredicto commiteado en `f7e5c93`
  (`review(TASK-0171): Analista OK private key ACL fix`). Ancla producto `cb7ce0a`; protocolo citado
  `1e3a4e7`; REVIEW materializado en `62bd09d`; gates vivos corridos en `01586e8`.
  Clon limpio producto `npm test`: primera corrida timeout local exit 124 a 304s; rerun exit 0, 74/74.
  Payloads propios: dry_run 200 sin runtime config; execute 200, respuesta/registry sin `BEGIN PRIVATE KEY`,
  privada real en `.secrets/workers`; `icacls` de la clave mostro solo `JBALL_PC\johnb:(F)`, sin Everyone,
  BUILTIN\Users ni Authenticated Users; fallo de `icacls` forzado con `PATH=""` -> 500
  `PRIVATE_KEY_PROTECTION_FAILED`, privada borrada y registry no creado. Negativos top-extra, worker-extra,
  id array/traversal/space, endpoint decimal/externo/IPv4-mapped, provider invalido, missing-confirm y duplicate
  -> 400/409 segun corresponde. Gates protocolo: validate con secretos exit 0; validate sin secretos en clon
  `1e3a4e7` exit 0; drift vivo 0 `up_to_seq=1743`; neutralidad/encoding exit 0; #4
  `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residual no bloqueante: POSIX 0600
  verificado por lectura de codigo, no por ejecucion en esta plataforma Windows.
- TASK-0171 (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado en `197498f`
  (`review(TASK-0171): Analista requires private key mode`). Ancla producto
  `f6dc8a56a801a50c6624517c835580d46d432199`; protocolo citado por instruccion
  `0c24550aebc39498d69a04e37e2a206bccf73ccd`; REVIEW materializado en protocolo `2d31a4b`.
  Clon limpio producto `npm test`: primera corrida timeout local exit 124 a 244s; rerun exit 0, 74/74.
  Payloads propios contra servidor temporal + protocolo clonado: dry_run 200 sin escribir; execute 200 escribe
  solo `extractors.runtime.json` de producto con `enabled:false`, `publicKeyPem`, sin `PRIVATE KEY` en respuesta,
  registry ni logs; `protocol.config.json`/events/snapshot byte-identicos; `agent_registry`/`signature_config`
  sin worker; no submit_intent. Negativos top-extra, worker-extra, type-confusion por campo, id traversal/space,
  endpoint externo/decimal/userinfo/IPv4-mapped/https-127, provider invalido, duplicate y missing-confirm -> 400/409
  sin escribir. SLIP bloqueante: la instruccion de review exigia privada gitignored con mode 0600, pero en Windows
  `fs.stat(private).mode & 0o777` dio `666`; no cierro AC2 mientras el gate afirma 0600. Gates protocolo:
  validate con secretos exit 0; validate sin secretos en clon `2d31a4b` exit 0; validate clon citado `0c24550`
  exit 0; drift vivo 0 `up_to_seq=1708`; neutralidad/encoding exit 0; #4 `protocol.config.json` byte-identico
  sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0166 r5 58c713c (2026-06-24): OK/CERRABLE, veredicto commiteado en `4e7d88a`
  (`review(TASK-0166): Analista OK runtime action guard`). Ancla producto
  `58c713c7a3de594958fc2d7e712e37c0a30361ce`; protocolo citado por instruccion `7aa3385`
  (mensaje REVIEW materializado en `ada79b8`). Clon limpio producto `npm test` exit 0, 72/72. Payloads propios
  contra servidor temporal + protocolo clonado en `7aa3385`: `agentId` array/object/number/bool/null/space/control/
  ZWJ/lowercase/unknown -> 400 sin heartbeat; `action` array/object/number/bool/null/unknown/uppercase -> 400 sin
  heartbeat; positivos exactos `activate`/`stop` -> 200 con heartbeat creado/eliminado. No encontre escape nuevo
  bloqueante. Residual no bloqueante: `action` string con whitespace externo se normaliza por `trim()` y ejecuta la
  enum cerrada; no amplia acciones ni comando arbitrario. Gates protocolo: validate con secretos exit 0; validate
  secretless en clon `ada79b8` exit 0; drift vivo 0 `up_to_seq=1637`; neutralidad/encoding exit 0; #4 byte-identica
  sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0166 fix3 a1d4491 (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado en `2279361`
  (`review(TASK-0166): Analista requires action type guard`). Ancla producto
  `a1d4491fc00f86ffdb3c3fce73de0d6ca9d366ae`; instruccion REVIEW en protocolo
  `07c3ad622cbefe04120cd897513af3b8113123ec` cita protocolo `9f3cded58e9305bd7926a46c54092f85286d3c0a`.
  Clon limpio producto `npm test`: corrida 1 exit 1 por flake de readiness local-vlm (`listening` impreso pero
  `/healthz` no listo a tiempo), corrida 2 exit 0, 64/64. Payloads propios contra servidor temporal + protocolo
  clonado en `9f3cded`: `agentId` array single, objeto, numero, bool, null, array anidado, leading space, ZWJ,
  control char, duplicate-key ultimo malo y extra key -> 400 sin heartbeat; heartbeat ausente/stale/futuro -> dormant;
  happy exact -> 200/alive. SLIP nuevo bloqueante: `{"agentId":"Codex","action":["activate"]}` devuelve 200, crea
  `Codex.heartbeat` y deja `Codex.status=alive`, porque `applyRuntimeControlAction` aun hace
  `ascii(stripControl(input?.action || "")).trim()` y `String(["activate"]) == "activate"`. `action` objeto devuelve
  500 TypeError publico. Pedido: `typeof input.action === "string"` antes de coercion + tests negativos permanentes
  para array/object. Gates protocolo: validate con secretos exit 0; validate secretless en clon exit 0; drift vivo 0
  `up_to_seq=1617`; neutralidad/encoding exit 0; #4 byte-identica sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0166 fix cab246c (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado en `228c70e`
  (`review(TASK-0166): Analista requires runtime agentId type guard`). Ancla producto
  `cab246cc48facb8b8dc6af52ca5a80ac4eddf766` + protocolo citado por instruccion `a2ed687`. Clon limpio producto
  `npm test` exit 0, 64/64. Payload propio contra server temporal + protocolo clonado en `a2ed687`: heartbeat
  futuro +10 anos -> dormant; stale 10 min -> dormant; leading/trailing space, control chars, lowercase, non-ASCII,
  ZWJ e internal-space -> 400 sin heartbeat; control positivo `Codex` exacto -> 200/alive. SLIP nuevo bloqueante:
  JSON `{ "agentId": ["Codex"], "action": "activate" }` devuelve 200, crea `Codex.heartbeat` y deja
  `Codex.status=alive`, porque `sanitizeRuntimeControlAgentId` hace `String(value || "")` antes del lookup y
  `String(["Codex"]) == "Codex"`. Pedido: type check estricto `typeof value === "string"` antes de coercion/lookup
  + test negativo permanente `agentId: ["Codex"]`. Gates protocolo: validate con secretos exit 0; validate
  secretless en clon `a2ed687` exit 0; drift vivo 0 `up_to_seq=1591`; neutralidad/encoding exit 0; #4
  `protocol.config.json` byte-identico durante pasada sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0165 v4 (2026-06-24): OK/CERRABLE, veredicto commiteado en `5ca009c`
  (`review(TASK-0165): Analista OK v4 thread PII`). Ancla producto `ea7304f` + protocolo
  `8a5c90c6ae7152dd512b86a70f2ecdac14eba096`. Clon limpio producto `npm test`: primera corrida timeout local
  exit 124 a 184s; segunda corrida exit 0, 61/61. Test nuevo v4 honesto: `assert.doesNotMatch` por literal exacto
  y `assert.match` para tokens `[PHONE-REDACTED]` / `[ADDR-REDACTED]`. Payload propio `buildAgentThread` +
  `redactRequirementText`: `Tel +1 (415) 555-2671`, `Tel (+57) (300) 555-7788`, `telefono (601) 555-7788 ext 9`,
  `Phone +44 (020) 5555 7788`, `Cra 7 # 12-34 Bogota`, `Cl 45 # 7-89 Medellin`, `KR 7 12 34 Bogota`,
  `Carrera 11 # 22-33 Cali`, `Calle 10 No 20-30 Piso 3`, `Av. Siempre Viva 742 piso 2` no filtran literales;
  tokens phone/addr presentes. Carry AC17 `mailbox-send` contra servidor temporal: `noPiiAck=409`,
  `badAgent=400`, `actorInjection=400`, `intentsInjection=400`, `routeState=400`. Gates protocolo con/sin secretos
  exit 0, drift 0 `up_to_seq=1535`, neutralidad/encoding exit 0, #4 `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residuales no bloqueantes: nombre propio
  libre y fragmentos sueltos tipo `#45-67` quedan para DEF-PII (TASK-0118); PII best-effort estructural.
- TASK-0165 v3 (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `037877d`
  (`review(TASK-0165): Analista requires thread PII v3 hardening`). Ancla producto `41bf1a2` +
  protocolo `a51d0c7a158d766c77b6827fd89fdb460312c78d`. Clon limpio producto `npm test` exit 0, 60/60.
  Test nuevo honesto: asierta ausencia de literal y presencia de tokens, no solo token-presence. AC17 carry
  en servidor temporal: `noPiiAck=409`, `badAgent=400`, `actorInjection=400`, `intentsInjection=400`,
  `routeState=400`. Payloads propios `buildAgentThread`: email, telefono simple, doc etiquetado, cuenta/IBAN y
  direccion literal pasan; pero `Tel +1 (415) 555-2671`, `Tel (+57) (300) 555-7788`, `Cra 7 # 12-34 Bogota`,
  `Cl 45 # 7-89 Medellin` y `KR 7 12 34 Bogota` quedan visibles completos. Gates protocolo con/sin secretos exit
  0, drift 0 `up_to_seq=1529`, neutralidad/encoding exit 0, #4 byte-identica sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residual nombre-propio libre no usado como
  bloqueo; los slips son familias tel/direccion tratables por patron.
- TASK-0165 v2 (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `450fada`
  (`review(TASK-0165): Analista requires thread PII hardening`). Ancla producto `cf13e7f8ad570f3e1ee375df4491bc50a8faab4b`
  + protocolo `e1c2666e0140ecf4e12916bef2181093132f9c32`. Clon limpio producto `npm test` exit 0, 59/59.
  Execute propio `mailbox-send` contra servidor temporal + protocolo clonado: HTTP 200/applied true, MSG generado
  `requires_response:false`, `operator_directive:true`, sin raw NIT/razon social, y `validate_collaboration_state.py
  --root <tmp>` exit 0. Payloads negativos: `noPiiAck=409`, `badAgent=400`, `actorInjection=400`,
  `intentsInjection=400`, `routeState=400`. Gates protocolo con/sin secretos exit 0, drift 0 `up_to_seq=1523`,
  neutralidad/encoding exit 0, #4 `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Bloqueo: el hilo read-only sigue filtrando
  PII fuera de NIT/razon social/SQL; `buildAgentThread` deja visibles email, telefono, documento, nombre propio,
  cuenta numerica larga y direccion cuando no hay SQL que los tape por accidente. Pedi devolver a Codex para unificar
  `redactRequirementText` con la familia del backend y anadir controles positivos por familia.

## Pasada anterior (2026-06-23)
- TASK-0165 (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `8e163cf`
  (`review(TASK-0165): Analista requires mailbox prompt hardening`). Ancla producto `1493f86` + protocolo
  `7d1199020a4245ee7d743ac8623449bc3d273a5a`. Clon limpio producto `npm test`: corrida 1 exit 1 por fallo
  ajeno local-vlm `127.0.0.5 must be accepted`, corrida 2 exit 0 58/58. Payloads propios contra servidor temporal:
  dry-run `mailbox-send` exit 200, `noPiiAck=409`, `badAgent=400`, `actorInjection=400`, `intentsInjection=400`;
  actor server-side `Arquitecto`, `directLedgerWrites:false`, transaction solo claim acquire/release file-scoped y
  `mailboxWrites`. SLIP bloqueante 1: el MSG generado tiene `requires_response: true` sin `requested_action` ni
  `question`; al materializarlo en copia limpia, `validate_collaboration_state.py --root <tmp>` sale 1. SLIP
  bloqueante 2: `public/app.js::redactRequirementText` usado por `buildAgentThread` no redacta email/telefono/
  documento/nombre propio aunque el backend `redactPublicText` si cubre esa familia; payload propio dejo visibles
  `persona@example.com`, `+57 300 123 4567`, `cedula 123456789` y `Juan Perez`. Gates protocolo con/sin secretos
  exit 0, drift 0 `up_to_seq=1514`, neutralidad/encoding exit 0, #4 `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
- TASK-0163 (ledger-busy friendly message AC72): OK/CERRABLE. Producto `d1de0c1`, protocolo ancla
  `e668cd0`; veredicto commiteado y pusheado en `c270ee4` (`review(TASK-0163): Analista OK ledger busy`).
  Clon limpio producto `npm test` exit 0, 57/57; targeted behavior AC72/no-bypass/file/candidate/intake exit 0,
  6/6. Payloads propios sobre funciones extraidas: 6 familias de contencion (`claim acquire overlaps active
  claim`, `overlaps active claim`, `active claim`, `ledger busy`, `concurrent ledger`, `contention`) dieron
  body saneado `{error:"ledger-busy", code:"ledger-busy", retryable:true}` y front `Canal ocupado, intente mas
  tarde`; 3 errores tecnicos con traceback/comando/secret/path dieron `{error:"submit_intent failed"}` sin fuga.
  Gates protocolo con/sin secretos exit 0, drift 0 `up_to_seq=1388`, neutralidad/encoding exit 0, `protocol.config.json`
  byte-identico sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
  Residual no bloqueante: matcher amplio de "active claim" puede clasificar un error ambiguo como ledger-busy;
  no filtra argv/traceback ni abre bypass, solo reduce diagnostico publico.
- TASK-0164 (2026-06-23): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `e3ada6b`
  (`review(TASK-0164): Analista requires torn write hardening`). Ancla protocolo implementacion `745a678`,
  instruccion `346dd00`, producto Zeus `4faacd1`. Clon limpio Zeus `npm test` exit 0, 57/57; protocolo limpio
  row_scoped_claim_cases 8/8 exit 0, intent_tx_cases 8/8 exit 0, validate sin secretos exit 0; repo vivo validate
  con secretos exit 0, neutralidad/encoding exit 0, chain/agent_signatures/anchor validos y drift 0 `up_to_seq=1435`,
  `protocol.config.json` byte-identico sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
  PASA concurrencia normal N=8: 8 procesos `submit_intent.py --intents` sobre 8 tareas/claims distintos -> todos
  returncode 0, 17 eventos esperados/leidos, prev_hash lineal, drift 0, todas las tareas in_progress. SLIP nuevo:
  al simular cola JSON parcial en `runtime/state/events.jsonl` (`{"seq":999`) y luego ejecutar `submit_intent`, la
  llamada devuelve `applied:true`/`event_seq=2`, pero `read_jsonl_torn_safe` sigue leyendo solo el prefijo (1 evento),
  el nuevo evento queda invisible pegado a la cola rota, `TASK_INDEX` no cambia y `validate_chain`/drift quedan verdes
  sobre el prefijo. Requiere hardening: bajo lock detectar/truncar cola rota o fallar duro antes de reportar exito.
- TASK-0164 v2 (2026-06-24): CAMBIO-REQUERIDO, veredicto commiteado en `78d4868`
  (`review(TASK-0164): Analista requires middle torn guard`). Ancla protocolo `232dcc3`, fix2 `92ece27`,
  producto Zeus `4faacd1`. Clon limpio Zeus `npm test`: corrida 1 exit 1 por AC50 readiness (`server did not
  become ready` aunque imprimio listening), corrida 2 exit 0 57/57. Protocolo limpio: row_scoped_claim_cases 8/8,
  intent_tx_cases 9/9, validate sin secretos exit 0; repo vivo validate con secretos exit 0; drift 0, chain valida,
  neutrality/encoding exit 0, #4 `protocol.config.json` byte-identico sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. PASA tail final reparado y tail+concurrencia:
  dos writers concurrentes tras cola parcial -> returncodes [0,0], un `log_repair`, 5 eventos visibles, prev_hash
  lineal, drift false. SLIP nuevo: torn en medio seguido por linea JSON valida posterior (`before` + partial broken
  + `after`) hace que `truncate_torn_jsonl_tail` trunque desde el prefijo y DESCARTE la linea valida `after`.
  Incumple "truncar SOLO la ultima linea parcial" y "no descartar eventos validos"; pedir fail-hard o cuarentena
  cuando la linea invalida no sea la ultima linea no vacia.
- TASK-0164 v3 (2026-06-24): OK/CERRABLE, veredicto commiteado y pusheado en `d3fa46a`
  (`review(TASK-0164): Analista OK mid torn v3`). Ancla protocolo citada `90958cf`, fix3 `434b2e9`, producto Zeus
  `4faacd1` (la instruccion v3 no cito commit de producto nuevo; use el ultimo anclado para TASK-0164). Clon limpio
  Zeus `npm test` exit 0, 57/57; protocolo limpio row_scoped_claim_cases 8/8, intent_tx_cases 10/10, validate sin
  secretos exit 0; repo vivo validate con secretos exit 0; neutrality/encoding exit 0; drift vivo 0 `up_to_seq=1486`;
  #4 `protocol.config.json` byte-identico sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
  Payloads propios: middle torn JSON + valid-after -> falla cerrado, bytes intactos, valid-after preservado, evento
  nuevo ausente; middle non-object `[]` + valid-after -> idem; tail-torn final -> `applied=true`, `log_repair`,
  evento visible, chain valid, drift false; tail-torn + 4 writers concurrentes -> returncodes `[0,0,0,0]`, un solo
  repair, 10 eventos visibles, prev_hash lineal, drift false; mid-torn + 2 writers concurrentes -> returncodes
  `[1,1]`, error de integridad, bytes intactos, sin claims nuevos. Residual: `read_jsonl_torn_safe` sigue leyendo
  prefijo ante corrupcion media, pero el writer `submit_intent` ya no cierra falso porque falla cerrado bajo lock.
- Pivote v2 publicar-para-ser-citado (2026-07-02): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en
  `33802db` (`review(pivote-v2): Analista requires prereg hardening`). Ancla protocolo `d0afaa2`; instruccion
  `MSG-20260702-Arquitecto-to-Analista-REVIEW-relay-pivote-v2-ronda2`; artefacto
  `Area_comun/artifacts/ANALISTA-pivote-v2-veredicto.md`; MSG rr a Arquitecto
  `MSG-20260702-Analista-to-Arquitecto-REVIEW-pivote-v2-ronda2.md`. Resultado: el marco de dos carriles pasa
  como direccion, pero no es sellable todavia. Bloqueantes: politica de medicion de empleados/no uso punitivo,
  eventos firmados para ayudas/excepciones/suspensiones/arbitrajes, trailers `Task-Id` y `Fixes-Task`
  bloqueantes, taxonomia D1-D4 ampliada, presupuesto medido <=1 dia/semana para Carril B, DECISION que
  supersede fork/re-alcance 0230/0232/0233/0234, spike DSSE/in-toto/Rekor, y sellado completo del
  pre-registro con hash+seq antes de Nova Budget. Gates: validate vivo exit 0; secretless clean clone exit 0;
  scan_domain_neutrality exit 0; scan_encoding exit 0; drift 0 `up_to_seq=3214`; `protocol.config.json`
  sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; Zeus-protocol clean clone
  `npm test` en `b2b2395` exit 0, 87 pass/22 skipped.
- TASK-0238 (2026-07-02): CAMBIO-REQUERIDO, veredicto commiteado y pusheado en `5ee5beb`
  (`review(TASK-0238): Analista requires intake exception hardening`). Ancla protocolo `66b9401`, implementacion
  `0efe196`, deliver `17c5973`; artefacto `Area_comun/artifacts/ANALISTA-TASK-0238-intake-gate-veredicto.md`;
  MSG rr a Arquitecto `MSG-20260702-Analista-to-Arquitecto-REVIEW-TASK-0238-intake.md`. R0/R1 pasan: `TASK-0238`
  sin intake valida en todos los estados enforced probados, `TASK-0239` sin intake falla en estados enforced y
  `proposed` queda exento; HEAD limpio valida verde con 176 tareas pre-boundary sin intake exentas. N1-N4 y N6
  missing-intake pasan; pin #4 preservado con sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; gates clean/vivo validate, encoding,
  neutrality exit 0; drift vivo 0 `up_to_seq=3268`; Zeus clean clone `npm test` en `b2b2395` exit 0, 87 pass/22
  skipped. Bloqueante F-0238-01: R5 no esta hard-gateado; `TASK-0239 ready` con `intake_exempt: true` y
  `exception_ref: 999`, sin evento `exception.recorded`, valida verde en Python y PowerShell, y `submit_intent`
  acepta `proposed->ready` dejando estado `ready`. Pedir remediacion: validar evento existente kind
  `intake_exempt` + `task_id` coincidente en Python validator, PowerShell validator y runtime; agregar negativos
  para ref inexistente, kind incorrecto y task incorrecto, mas positivo con evento real.
- TASK-0240 re-gate (2026-07-03): OK/CERRABLE, veredicto commiteado y pusheado en `160cc8e`
  (`review(TASK-0240): Analista OK trailer section regate`). Ancla protocolo `165b036`, remediacion `db47854`,
  producto control `b2b2395`. Artefacto `Area_comun/artifacts/ANALISTA-TASK-0240-trailer-section-regate-veredicto.md`;
  MSG rr a Arquitecto `MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0240-trailer-section-regate.md`.
  Clon limpio Zeus `npm test` exit 0, 109 tests, 87 pass, 22 skipped. Clon limpio protocolo validate exit 0,
  test_trailers exit 0, PowerShell validate exit 0, encoding exit 0. Vivo: validate Python/PowerShell exit 0,
  test_trailers exit 0 (9 casos), scan_encoding exit 0, scan_domain_neutrality exit 0; drift 0
  `up_to_seq=3356`; chain valid `checked_events=2684`; `protocol.config.json` vivo sin `commit_trailers`, sin
  `Area_comun/protocol/COMMIT_TRAILERS.json`, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
  Payloads propios: `Task-Id` intermedio + cuerpo posterior falla `without exact Task-Id`; `Fixes-Task`
  intermedio falla `without exact Fixes-Task`; `Ops-Reason` intermedio con `Task-Id: none` final falla
  `without Ops-Reason`; texto libre y case variant no cuentan; unknown task/fix fallan; ops allowlist,
  personal exempt y `fix!` positivo pasan. Residual no bloqueante: parser acepta bloque final `Key: value`
  generico y solo consume claves permitidas; no deja contar lineas intermedias.
- TASK-0243 (2026-07-03): OK/CERRABLE, veredicto commiteado en `a70f4f5`
  (`review(TASK-0243): Analista OK decision 0084`). Ancla protocolo
  `b37b9a31b64641fb19fc96552477cec769e2c03d`, entrega `f3f91b3f410564331c435417366538a47d2fd806`,
  producto control `b2b2395da39090109db6de2dc50726dbaab1a11e`. Artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0243-decision0084-veredicto.md`; MSG rr a Arquitecto
  `MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0243-decision0084-OK.md`. DECISION-0084 pasa:
  evento `intent_type=decision` seq 3427, relates_to GOAL-VISION-NOVA-001 + DECISION-0083,
  clausula pin-anclado-al-tag con los 5 pineados anclados a `TFM-dataset-N500`, `protocol.config.json`
  byte-identico sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`,
  10 puntos DoR verbatim de `dae40ac`, mapa 6/10 v1 honesto y regla anti-vacio. TASK-0230 anota
  `priority`, `target_user`, `functional_scope`, `assets_inputs`, `tech_constraints`, `risks_list`
  para feature/product; hub intacto: validator no cambio y TASK-0238 sigue done. Gates: validate vivo
  con secretos exit 0; validate clon limpio sin secretos exit 0; encoding/neutrality exit 0; drift 0
  `up_to_seq=3436`; chain valid `checked_events=2764`; Zeus-protocol clean clone `npm test` en `b2b2395`
  exit 0, 109 tests, 87 pass, 22 skipped. Residuales no bloqueantes: no habia commit nuevo de producto
  citado; `scope_routes` de TASK-0243 conserva una ruta antigua de 0230 pero el archivo real fue anotado.
- TASK-0230 (2026-07-03): OK/CERRABLE, veredicto commiteado y pusheado en `0295468`
  (`review(TASK-0230): Analista OK new instance`). Ancla protocolo
  `8b215daf6c3820e427036a23d40994a565af0ba3`, producto
  `e7c6da482a1e819507af37de77b9cd46712fb8c8`, instancia NOVA
  `172edcb53d18ac6568a61c42b10f644cf9fb9ed9`, source tag `v1.18.0` ->
  `c9a442354bb5002b4df3a21e581ef1e891029c58`. Artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0230-new-instance-veredicto.md`; MSG rr a Arquitecto
  `MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0230-new-instance-OK.md`. Clon limpio Zeus-protocol
  `npm test` exit 0, 112 tests, 90 pass, 22 skipped. Payloads propios: default dry-run usa `v1.18.0`
  y no escribe; write real en tmp crea configs `.agents` commiteadas y commit de instancia desde tag; segundo
  write falla por destino existente; nombres invalidos/escape fallan cerrado; ref inexistente falla cerrado;
  DoR acepta none explicito y rechaza missing/placeholder/arrays vacios; `priority` requerido tambien en no
  feature/product. Instancia `D:/Agentes/Zeus/NOVA` valida exit 0, encoding/neutrality exit 0, drift 0
  `up_to_seq=3457`. Hub vivo y clon limpio: validate exit 0, encoding/neutrality exit 0, drift 0
  `up_to_seq=3502`, chain valid `checked_events=2830`, `protocol.config.json` sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Residuales no bloqueantes:
  CLI acepta `--source-ref HEAD` si se fuerza explicitamente; grep global de la instancia encuentra menciones
  heredadas del instalador prohibido solo como prohibicion, no en configs/artefactos generados.
- TASK-0234 (2026-07-03): CAMBIO-REQUERIDO/NO CERRABLE, veredicto commiteado en `75741ad`
  (`review(TASK-0234): Analista requests runbook remediation`). Ancla protocolo
  `e8bb127457e0e74e4d96df13d7390cb9aec84f47`; entrega doc citada `64d44ad`;
  producto sin commit citado por la instruccion, por lo que el clon limpio de Zeus-protocol se probo en
  `e7c6da482a1e819507af37de77b9cd46712fb8c8`. Artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0234-runbook-onboarding-veredicto.md`; MSG rr a Arquitecto
  `MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0234-runbook-onboarding-veredicto.md`.
  Gates: Zeus-protocol clean clone `npm test` exit 0, 112 tests, 90 pass, 22 skipped; hub validate con
  secretos exit 0; clean clone sin `secrets/` validate exit 0; encoding/neutrality exit 0; drift 0
  `up_to_seq=3601` antes del claim del veredicto; `protocol.config.json` byte-identico entre 64d44ad y HEAD,
  sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Bloqueantes:
  F-0234-01 falta comando/payload minimo de `submit_intent` para claim/status/handoff/cierre; F-0234-02 falta
  ruta/comando falsable del harness F2.3 y ciclo e2e F2.2. Fix-loop: remediar, re-gatear validate con/sin
  secretos, drift 0, domain, encoding, #4 byte-identica y re-juicio Analista; maximo 2 iteraciones antes de
  escalar al operador.
- TASK-0246 re-juicio fix-loop 1 (2026-07-03): OK/CERRABLE, veredicto commiteado y pusheado en `50cb3fd`
  (`review(TASK-0246): Analista OK nova dev fix loop`). Ancla protocolo de instruccion `74185fd`, remediacion
  `9b5563c`, producto control `e7c6da482a1e819507af37de77b9cd46712fb8c8`. Artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0246-nova-dev-lote-specs-rejuicio-veredicto.md`; MSG rr a Arquitecto
  `MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0246-rejuicio-OK.md`. F-0246-01 pasa: P3-001 q4_membership
  FUERA; P3-002/P3-003 CONDICIONAL; probe cubrio P3-004 CONDICIONAL, P3-005 FUERA, P4-004 DENTRO. F-0246-02
  pasa: SQL readonly confirma `Budget.Apply_Obligation_Adjustment` con THROWs reales
  `50250,50251,50252,50253,50255,50257,50258,50264,50265`, sin `50254/50256`; P4-004 ya espera 50264 para tope
  y 50265 para efecto distinto de reintegro. Gates: validate con secretos exit 0; validate secretless clean clone
  exit 0; domain/encoding exit 0; drift 0 `up_to_seq=3643`; chain valid `checked_events=2971`; #4 byte-identica
  sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; Zeus clean clone `npm test` exit 0,
  112 tests, 90 pass, 22 skipped. Residual no bloqueante: P2-004 `Get_*_List` siguen ausentes en BD pero son
  objetos a CREAR por BR-C3, no cita de existencia.
- TASK-0248 (2026-07-04): CAMBIO-REQUERIDO/NO CERRABLE, veredicto commiteado y pusheado en `fb07efb`
  (`review(TASK-0248): Analista requires codegen triage remediation`). Ancla protocolo
  `4eddf483a1cf0b50f82102ab5a7a3fc23a0b999d`, producto Nova-Budget
  `88af254b55f07e99aacd588d655a261f922bc399`. Artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0248-skill-codegen-triage-veredicto.md`; MSG rr a Arquitecto
  `MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0248-skill-codegen-triage.md`. Neutralidad de capa neutral
  y split de capas pasan, pero bloquean: F-0248-01 `codegen-triage` no carga por loader gobernado DECISION-0061
  (`.claude/skills/...` fuera de ubicacion permitida y no registrado en `skills/skills.config.json`);
  F-0248-02 forma de salida entregada `{path, reason, verifying_gate, red_flags}` no coincide con
  `{camino, razon, gate, banderas}`; F-0248-03 `npm test` en clon limpio Nova-Budget raiz exit `-4058` y
  `apps/nova-web` exit 1 por script `test` ausente. Gates: validate vivo exit 0; validate secretless clean clone
  exit 0; encoding/domain exit 0; drift 0 `up_to_seq=3718`; chain valid `checked_events=3046`; #4 byte-identica
  sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Fix-loop: remediar loader/contrato
  ubicacion, forma canonica y gate producto; re-juicio Analista antes de cierre, maximo 2 iteraciones.
- TASK-0249 re-juicio fix-loop 1 (2026-07-04): CAMBIO-REQUERIDO/NO CERRABLE, veredicto commiteado y
  pusheado en `fc32362` (`review(TASK-0249): Analista requires instrumentation fixes`). Ancla protocolo
  `5bf2e70`; producto Nova-Budget N/A porque el REVIEW canonico cita `Producto commit citable: NINGUNO`
  y ordena no ejecutar producto. Artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0249-f33-instrumentacion-rejuicio-1-veredicto.md`; MSG rr a
  Arquitecto `MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0249-f33-instrumentacion-rejuicio-1-NOGO.md`.
  Suite canonica de instrumentacion en clon limpio exit 0 (5 tests), pero bloquean dos slips nuevos:
  F-0249-02 `cost_attributed` acepta `prompt_tokens=100 completion_tokens=50 no cumulative field` y escribe
  `tokens_total_atribuibles=100` aunque no hay cumulativo leido; F-0249-03 Q3 `mediana_pareada_delta` cambia
  de `-20` a `20` al invertir el orden de filas del mismo par baseline=100/gobernado=80. Gates: validate
  clean/vivo exit 0; encoding clean/vivo exit 0; domain clean/vivo exit 0; drift clean/vivo 0
  `up_to_seq=3861`; chain valid `checked_events=3189`; #4 byte-identica sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Fix-loop esperado: parser de err.log
  debe fallar cerrado sin cumulativo explicito y Q3 debe calcular delta por brazo, no por orden CSV; re-juicio
  Analista previo a cierre, maximo 2 iteraciones.
- TASK-0252 (2026-07-05): CAMBIO-REQUERIDO/NO CERRABLE, veredicto commiteado y pusheado en `b3896e1`
  (`review(TASK-0252): Analista requires parity harness fixes`). Ancla protocolo
  `d2ab042600c54614ed42680866d69dc9d63dfa12`, producto Nova-Budget
  `dc04bd8a820069de9fcce0879010a65b50057c56`. Artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0252-harness-paridad-veredicto.md`; MSG rr a Arquitecto
  `MSG-20260705-Analista-to-Arquitecto-REVIEW-TASK-0252-harness-paridad-NOGO.md`. dotnet clean clone
  `dotnet test NOVA.sln` exit 0 (26 tests, warning NU1903); `npm test --prefix apps/nova-web` raw exit 1
  por falta de `tsc` en clon limpio, y tras `npm install --prefix apps/nova-web` exit 0 (1 test).
  Payload adversarial propio agregado solo en clon temporal: base `DbsFinanciero_PRODUCTION_SANDBOX_COPY`
  no lanza excepcion porque el guard usa `Contains("SANDBOX")`; caso mismatch devuelve `fail` y reset
  `reset, exec, reset, endpoint`. Bloqueantes: F-0252-01 rol `budget_sandbox_verifier` no verificado por
  SQL real (solo constante/texto), F-0252-02 guard de DB no exacto contra `DbsFinanciero_SANDBOX`, F-0252-03
  gate npm crudo no reproducible sin instalar dependencias. Gates protocolo vivo/secretless validate,
  encoding/domain exit 0; drift 0 `up_to_seq=3986`; chain valid `checked_events=3314`; #4 byte-identica
  sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. Fix-loop: remediar rol real,
  guard exacto y comando npm reproducible; re-juicio Analista previo a cierre, maximo 2 iteraciones.
- TASK-0246 remediacion 1 informe/P4-006 (2026-07-06): OK/CERRABLE, veredicto commiteado y pusheado en
  `2fc9890` (`review(TASK-0246): Analista OK remediacion informe specs`). Ancla protocolo
  `9c244712d7b8ad5937c59a549790f1a4f7778a4a`, remediacion documental `d43431f8`; producto Nova-Budget
  N/A porque el REVIEW declara `SIN PRODUCTO EN ALCANCE` y no cita commit de producto. Artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0246-informe-specs-remediacion1-veredicto.md`; MSG rr a Arquitecto
  `MSG-20260706-Analista-to-Arquitecto-REVIEW-TASK-0246-remediacion1-OK.md`. F-0246-INF-01 pasa: inventario
  `SPEC-NOVA-*.md` = 17, informe linea 45 declara 17 SPECs y fila transversal linea 62 incluye P2-003.
  F-0246-P4006-01 pasa: P4-006 preambulo apunta a s.7 criterio 6 y deja nota de correccion de la referencia
  previa a criterio 9. Gates en clean clone canonico: validate exit 0, encoding exit 0, domain exit 0, drift 0
  `up_to_seq=4256`, #4 byte-identica sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.
  Residual: working tree local estaba rojo por cambios ajenos/claim activa y snapshot mismatch no canonicos;
  por eso la evidencia se tomo de clean clone de origin/main.

- TASK-0270 (2026-07-20): GO/OK-CERRABLE, veredicto commiteado y pusheado en `1cb7b0e`
  (`review(TASK-0270): veredicto GO del Analista`). Ancla protocolo origin/main `b37e638` (implementacion
  `a989475`); producto N/A (REVIEW declara SIN PRODUCTO EN ALCANCE). Artefacto
  `Area_comun/artifacts/ANALISTA-TASK-0270-ledger-postwrite-idempotencia-veredicto.md`; MSG rr a Arquitecto
  `MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0270-veredicto-GO.md`. Clon limpio `D:/ccv/t0270`
  (b37e638) + clon pre `D:/ccv/t0270pre` (a989475~1) para preexistencia. Suites: intent_tx 12/12,
  intent_flow 11/11, concurrency exit 0; replay exit 1 por caso PREEXISTENTE (identico en a989475~1).
  Sondeo propio 11/11 (driver D:/ccv/probe0270.py): post-write caza evento perdido inyectado nombrandolo
  (suelto y --intents, rollback completo); dedup repara estado divergente en task_status/claim/mailbox
  (reconciled=true, drift 0); replay del incidente 19-jul (flip borrado + retry byte-identico del lote)
  -> "partial transaction idempotency state exists", CLI exit 1, jamas mudo. Residuales: R1 flag
  reconciled subreporta en task_upsert/decision (sin fuga, materialize+drift reparan); R2 post-write
  compara identidad no bytes (prev_hash lo caza aguas abajo); R3 kill post-append -> replay (maker,
  honesto); R4 caso replay preexistente. Gates: validate con/sin secretos 0, drift 0, chain valida 4391
  eventos, #4 sha256 `2E35F26E...` epoch 1.14.0, encoding 0. ANOMALIA DECISION-0018 reportada:
  scan_domain_neutrality ROJO en HEAD por `scripts/test_anthropic_checker_harness.py` (6c8a0d8,
  TASK-0271 ya ratificada); biseccion: verde en a989475~1. Remediacion ruteada al Arquitecto (yo no me
  auto-asigno el fix de mi propio harness). Primer turno end-to-end del harness migrado (Anthropic):
  sondeo de tamper completo sin kills del clasificador (evidencia viva 0271). Leccion tecnica: los
  secretos eventauth son `secrets/eventauth-*.key` relativos al root (copiarlos al clon para el run
  con-secretos); validate_chain(events, config) exige lista de eventos, no root.

- TASK-0278 (2026-07-20): GO/OK-CLOSABLE sin condiciones, veredicto commiteado y pusheado en `8f43a1c`
  (`review(TASK-0278): GO OK-CLOSABLE, sin condiciones, residuales R1-R4 declarados`). Ancla: implementacion
  Codex `ef0b645` (ancestro de origin/main, HEAD `11a003a`); SIN PRODUCTO EN ALCANCE. Clean clone `D:/ccv0278`.
  Artefacto `Area_comun/artifacts/Analista-TASK-0278-token-epilogo-verdict.md`; MSG rr
  `MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0278-verdict.md`. Defecto de campo: epilogo del CLI
  (`tokens used`+conteo) tras la respuesta rompia terminal-only, y el regex de respaldo leia el eco del
  prompt (out_of_scope/FUERA de alcance) -> dos execs reales marcados definitive siendo transient. Fix
  verificado: separacion ESTRUCTURAL de flujos (RedirectStandardOutput/Error en Start-Process); clasifica
  SOLO stdout; rama definitive de texto libre ELIMINADA (unico productor de definitive = token terminal
  exacto, linea 496); exit!=0 transient; evidencia ed25519 propia confirmed; texto libre solo
  transient/unconfirmed (no consumen: rollback + retry acotado + RETRY_EXHAUSTED watchdog). Probe propio
  19 payloads exit 0 (transcripts REALES verbatim de ambos invocadores + hostiles): codex CLI manda eco
  de prompt y epilogo a stderr; claude CLI stdout=respuesta y stderr VACIO. Gates clean clone todos 0;
  drift false up_to_seq=5393. Residuales: R1 frontera de confianza = binario del CLI escribiendo token
  exacto forjado como ultima linea de stdout (contaminacion menor degrada a unconfirmed, fail-safe);
  R2 lexicon transient sobre stdout puede etiquetar transient vs unconfirmed (ambos no-consumidores);
  R3 -InvokerDiagnostics aceptado y sin uso decisional (by design); R4 mecanismo distinto al del
  acceptance pero mas fuerte. Tecnica reusable: extraer Get-ExecOutcomeClass verbatim del clon con regex
  y recomputar sobre los out.log/err.log ORIGINALES de .protocol-tmp, no el fixture reducido. NOTA: hook
  de commit aviso PRUNE DUE (released_ratio 95.56>=90) diferido al checkpoint del Arquitecto (yo no
  ejecuto prune, muta estado gobernado).

- HEARTBEAT 2026-07-20 18:45 (HEAD 273b533): sin instruccion REVIEW pendiente. Los dos mensajes
  abiertos hacia mi (`MSG-...-DECISION-0277-condicion-y-poda`, `MSG-...-DECISION-cierre-0272-residuales`)
  son type DECISION, requires_response false, requested_action "Ninguna accion inmediata". No-op
  principiado: no implemento, no muto estado, no cierro. validate exit 0 sobre el arbol (mods de
  Codex en curso, no las toco). Tres cosas registradas para el proximo turno:
  (1) F1 de 0277: la relajacion del validador se declara EN EL CODIGO de `validate_claims` con
  comentario del motivo, ademas de la tarea, el handoff y la nota de cierre; la nota sola no basta.
  (2) CORRECCION del Arquitecto a su propia guarda: "mantenimiento debido" solo es no-regresion para
  `prune_state.py --check`; `--apply` SI es gate de la unidad y hoy esta ROJO
  (`IntentApplyError: protocol state drift remains after submit_intents`, TASK_INDEX_ARCHIVE.json y
  CLAIMS_ARCHIVE.json hot != replay; revierte limpio). 0277 vuelve a in_progress; en el RE-JUICIO de
  0277 debo correr `python scripts/prune_state.py --root . --apply` en el clon limpio y gatear por
  exit code, no solo `--check`.
  (3) RELOJ: mis dos veredictos de hoy fecharon 18:25 y 20:15 diciendo UTC+2 cuando el sistema marcaba
  16:25 y 18:15. Estaba sumando dos horas a una hora que YA es local. Regla: tomar `date` del sistema
  en el mismo turno y citarla verbatim, sin convertir. El Operador ya senalo este desfase antes.
  Residuales R1 (fila extra no nombrada por eventos) y R2 (git-author unico en arbol compartido)
  aceptados por el Arquitecto como no bloqueantes; R1 va al carril de endurecimiento con 0274-0276 y 0279.

- TASK-0277 REMEDIACION iter1 (2026-07-20 19:43, HEAD `5e581c4`): **CHANGE-REQUIRED / NO-GO**, veredicto
  commiteado y pusheado en `c4ec3e4`. Ancla: fix `7337b30`, entrega `6e3bcc5`. Clean clone `D:/ccv0277`.
  Artefacto `Area_comun/artifacts/Analista-TASK-0277-remediacion-iter1-verdict.md`; MSG rr
  `MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0277-remediacion-iter1-verdict.md`.
  PASA: `--apply` real bajo enforce exit 0 + drift False + `--check` 0; fallo ANTES del evento restaura
  los dos espejos byte a byte; F1 declarada EN CODIGO (`validate_collaboration_state.py:1142-1144`) y
  probada por comportamiento (active falla, released/blocked pasan; runtime y validador solo tratan
  `active` como viva); sin regresion (207 task ids / 1426 claim ids nombrados por eventos, cero ausentes,
  interseccion caliente/archivo vacia, drift False seq 5434, replay 8/8).
  FALLA: **F-0277R1-01** el rollback de espejos se dispara con CUALQUIER excepcion de `submit_intents`,
  incluida una POSTERIOR a que la transaccion se aplico -> borra filas que el evento firmado exige,
  drift True, y re-ejecutar `--apply` sale **exit 0** sin repararlo (verde sobre arbol con drift).
  **F-0277R1-02** `except Exception` no cubre `BaseException` (Ctrl-C/SystemExit/kill) -> filas
  pre-escritas sin evento; visibles solo mientras la gemela siga en caliente (`Duplicate task/claim
  across hot/archive`); una huerfana sin gemela es INVISIBLE (validate 0, drift False, probado en el
  repo real con `CLAIM-FABRICATED-NO-EVENT`). **F-0277R1-03** `archive_removed_entries` deduplica por id
  y nunca refresca, `verify_archived_entries` compara contenido -> fila obsoleta + mutacion gobernada
  posterior = poda bloqueada PERMANENTEMENTE (`prune archive verification failed`).
  TECNICA REUSABLE (la que caza esta clase de defecto): **inyeccion de fallos monkeypatcheando
  `scripts.prune_state.submit_intents` en proceso** sobre el fixture del propio maker (build_fixture +
  regenesis + enforce), con cuatro modos: `pre` (lanza antes del evento), `notapplied` (devuelve
  applied=False), `post` (llama al real, deja que aplique, y LUEGO lanza), `kbint` (KeyboardInterrupt).
  El modo `post` es el que revela rollbacks destructivos; probar causalidad reponiendo los bytes exactos
  y viendo volver drift a False. Scripts en el scratchpad de la sesion (`fi_prune*.py`).
  RESIDUALES: R1 el camino de rollback no tiene test (por eso llego a entrega); R2 el fixture enforced
  corre sin `event_auth` ni firmas de agente; R3 la exencion F1 tambien cubre `blocked`; R4 transversal:
  el autor git contradice al actor firmado (`7337b30`/`6e3bcc5` git-author Analista, eventos 5411-5412
  Codex y 5413-5415 Arquitecto; `5b76643` al reves) -> levantado por DECISION-0018.
  Bucle declarado: iteracion 2 de maximo 2, re-juicio mio ANTES del commit de cierre, luego escalada.

## 2026-07-20 (tarde-noche) -- TASK-0280 rollback vs ledger append-only: NO-GO iter1
Commit juzgado `2b37294` (padre `7de9403`), HEAD `ef679c9`; veredicto en
`Area_comun/artifacts/Analista-TASK-0280-rollback-ledger-verdict.md`, commit `26dd716`.
Gates verdes en clon limpio (`D:/ccv0280`): validate, scan_encoding, scan_domain_neutrality y
`examples/mailbox_retry_cases/run_mailbox_retry_cases.py`, todos EXIT 0. La suite del maker pasa
porque no prueba el caso que rompe.
FALLA BLOQUEANTE **F-0280-01**: `Invoke-PreExecPatch` aplica SIEMPRE `--exclude` sobre
`runtime/state/*`, `Area_comun/state/*`, `Area_comun/tasks/*`, `Area_comun/mailbox/*`, pero el parche
compensatorio solo se aplica `if ($ledgerAdvanced)`. Exec transitorio SIN evento -> el trabajo
pre-exec sin commitear en esas cuatro rutas se DESTRUYE en silencio (ni PRESERVED ni DRIFT ni DEFER).
**F-0280-02**: `git diff --binary HEAD -- <4 rutas>` incluye las altas staged del exec, asi que el
parche de preservacion RESUCITA residuo no-ledger (`?? Area_comun/tasks/TASK-residue.md`).
PASA: V2 evento+derivado sobreviven una sola vez con `ROLLBACK_LEDGER_PRESERVED`; V3
`ROLLBACK_LEDGER_DRIFT reason=derived_state_mismatch` se emite y no hay PRESERVED falso; parser de
outcome de 0278 sin regresion.
TECNICA REUSABLE (la que cazo esto): **contraste diferencial entre el commit juzgado y su PADRE con
el MISMO arnes**. Dos clones limpios (`D:/ccv0280` y `D:/ccv0280p`), un sandbox git calcado del
`run_mailbox_retry_cases.py` del maker pero con testigos pre-dirty **en las rutas gobernadas** ademas
del testigo neutral de raiz que usa el maker. Si el padre restaura y el hijo no, la regresion queda
probada sin discusion. Script en el scratchpad (`falsify_0280.py`, vectores V1-V4 + V1 contra padre).
LECCION GENERAL: cuando un fix EXCLUYE rutas de una restauracion y las compensa en otra rama
condicional, atacar siempre la rama donde la compensacion NO corre. Y desconfiar de un testigo
pre-dirty unico en la raiz: si el fix opera por prefijos, el testigo debe estar DENTRO de cada prefijo.
RESIDUALES declarados: R1 ventana snapshot->reset, un append concurrente se pierde y es INDETECTABLE
(replay compara events.jsonl y derivado restaurados del mismo snapshot -> coherentes -> PRESERVED
verde); fix barato = re-leer `Get-LedgerSequence` antes del reset y tras el apply, defer si se movio.
R2 `ROLLBACK_LEDGER_DRIFT` es solo log en `.protocol-tmp/` gitignorado, no llega al mailbox y no
detiene el bucle; la rama `ledger_restore_failed` ocurre DESPUES del reset (eventos ya perdidos).
R3 la idempotencia del reintento no esta testeada y el prompt del reintento no lleva senal de lo
preservado. R4 el untracked destruido NO queda cubierto por 0280 y sigue siendo TASK-0275 (solo se
respeta `if ($ledgerAdvanced -and Test-LedgerManagedPath)`).
Bucle declarado: iteracion 1 de maximo 2, re-juicio mio ANTES del commit de cierre, luego escalada.

## 2026-07-20 20:55 -- Re-juicio iteracion 2 (commit e07956e): 0277 GO, 0280 NO-GO

Encargo `MSG-20260720-Arquitecto-to-Analista-REVIEW-0280-0277-iter2-cabeza-del-log`. Veredictos
en `Area_comun/artifacts/Analista-TASK-0277-iter2-cabeza-log-verdict.md` y
`Analista-TASK-0280-iter1-cabeza-log-verdict.md`, commit `9703fbe` (pusheado). Ancla: juzgado
`e07956e`, padre `31e7bc7`, HEAD `b54ef43`; clones limpios `D:/ccvA` y `D:/ccvAp`. Los seis gates
en clon limpio, EXIT 0 (incluidas las suites de 7 y 8 casos).

PRIMITIVA COMPARTIDA: `scripts/ledger_head.py::event_log_head` = (seq, sha256 de la ultima linea).
Unica implementacion; `prune_state.py` la importa y `peer_mailbox_cron.ps1` la invoca por
subproceso (`Get-LedgerHead`). Verificado: no hay copias divergiendo.

**TASK-0277 GO.** Mis tres hallazgos de iteracion 1 cerrados y probados contra el padre:
F-0277R1-01 (padre borraba los espejos de una transaccion YA aplicada, drift True; ahora los
retiene 4/7 con drift False y `RuntimeError` "event log advanced"), F-0277R1-02 (`except
BaseException` + comparacion de cabeza; probe las CUATRO combinaciones excepcion/Ctrl-C x
antes/despues, no solo las dos del maker), F-0277R1-03 (`archive_removed_entries` refresca la
fila divergente en vez de saltarla: reproduje la cadena completa con mutacion gobernada real via
`submit_intents` con claim+task_upsert+release; el padre se bloquea con `prune archive
verification failed`, el hijo completa la poda). Cuarto arreglo: `if drift.has_drift: raise`
antes del return, `main()` no captura -> `--apply` sale 1 sin JSON de exito (verificado
end-to-end). Residuales: R5 cola desgarrada dentro del manejador de fallo (JSONDecodeError
sepulta la excepcion original y NO restaura espejos), R6 fila huerfana sin gemela caliente sigue
invisible, R7 traceback en vez de diagnostico.

**TASK-0280 NO-GO (iteracion 1 de 2).** Mis dos SLIPs y R1 SI estan cerrados con negativos
permanentes. El bloqueante nuevo lo introduce la propia remediacion del SLIP 2:
**F-0280R1-01** -- `git diff --binary --diff-filter=M` (`peer_mailbox_cron.ps1:502`) discrimina por
TIPO DE CAMBIO, no por pertenencia al libro: tira todas las altas y todas las bajas bajo las cuatro
rutas gobernadas, incluidas las que produce una transaccion firmada. `mailbox_archive` es
exactamente una baja en `open/` y un alta en `archived/` (`runtime/apply.py:472-477`,
`submit_intent.py:91`). Contraste diferencial:
`padre: open ausente / archived PRESENTE` vs `e07956e: open PRESENTE / archived AUSENTE`,
y AMBOS emiten `ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=1`. Silencioso porque
`materialize_protocol_state` (`protocol_replay.py:597-604`) solo materializa TASK_INDEX,
PROJECT_STATE y CLAIMS: **el mailbox nunca produce drift**.
**F-0280R1-02** (major, regresion) -- `event_log_head` hace `json.loads` de la ultima linea sin
tolerancia; una linea desgarrada (kill a mitad de append) hace lanzar a `Get-LedgerHead`, el
rollback NO se ejecuta (el residuo sobrevive) y el bucle entra en `LOOP_ERROR` perpetuo porque
la linea 658 tambien lanza antes de invocar al agente. El padre, con su lector tolerante, si
hacia rollback y se recuperaba. Asimetria clave: `Get-OwnEvidence` (linea 435) SI tolera lineas
ilegibles; el lector tolerante es el que no decide nada.

TECNICAS REUSABLES CONFIRMADAS:
- El contraste diferencial contra el padre volvio a cazar el bloqueante (2 de 2 iteraciones).
- **El testigo tiene que vivir donde vive el riesgo, Y TENER LA FORMA DEL RIESGO.** Iteracion 1:
  el testigo estaba en la raiz y el riesgo por prefijos. Iteracion 2: los testigos ya estan en los
  prefijos correctos pero todos son MODIFICACIONES, y el defecto vive en las ALTAS y las BAJAS.
  Cuando un fix filtra por una propiedad (`--diff-filter=M`), atacar el complemento de esa propiedad.
- Inyeccion de fallos con monkeypatch de `scripts.prune_state.submit_intents` sobre
  `enforced_fixture` real: cubre pre/post-apply x Exception/KeyboardInterrupt en minutos.
- Para mutar estado caliente bajo enforce hay que ir por `submit_intents` con claim que cubra
  TRES rutas: `Area_comun/state/TASK_INDEX.json#<id>`,
  `Area_comun/state/PROJECT_STATE.json#active_tasks/<id>` y `Area_comun/tasks/<id>.md`.
  Editar el JSON caliente a mano da `protocol state drift exists before submit_intent`.
- Forma del intent: `{"task_upsert": {"task": {...}, "idempotency_key": "..."}}`, NO
  `{"kind": ..., "payload": ...}`.
- El fixture `enforced_fixture` da `validate` exit 1 por rutas de tier runtime ausentes: es ruido
  del fixture, no senal. Leer SIEMPRE el mensaje, no solo el exit code, en fixtures sinteticos.
Scripts en el scratchpad: `falsify_0280.py` (vectores N1 movimiento gobernado staged, N2 cola
desgarrada, con contraste padre) y `falsify_0277.py` / `falsify_0277b.py` (P1-P5, P1b-P3b, P2c-P2d).

## 2026-07-20 22:05 -- TASK-0280 iteracion 2 de 2: NO-GO (commit 91b585c, pusheado)

Encargo `MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0280-iter2-final`. Veredicto en
`Area_comun/artifacts/Analista-TASK-0280-iter2-preservacion-eventos-verdict.md`. Ancla: codigo
juzgado `9c6f546`, padre `8de3d8b`, HEAD `ba73fba`; clones limpios `D:/ccvB` y `D:/ccvBp`. Los
seis gates EXIT 0 en clon limpio. Tope agotado -> escala al Operador.

**CERRADOS de verdad (contra el padre).** F-0280R1-01: `task_upsert` firmado que crea
`Area_comun/tasks/TASK-9002-new.md` sobrevive en el hijo y se destruia en el padre.
F-0280R1-02: cola desgarrada -> `ROLLBACK_DEFER reason=ledger_torn_tail`, cola intacta, **exec 2
ocurre** (bucle vivo), sin `LOOP_ERROR`; el padre daba `EXEC_FAIL` + `LOOP_ERROR` x2 y exec 2
nunca. Cola rota vs log legitimo mas corto: mismo `seq` y mismo `hash`, los separa el flag
`torn_tail`. Primitiva unica intacta y `prune_state.py` compatible con la firma de 3-tupla.

**F-0280R2-01 (BLOQUEANTE, regresion).** `scripts/ledger_head.py::event_managed_paths_after`
enumera ocho ficheros de estado y NO incluye `Area_comun/state/TASK_INDEX_ARCHIVE.json` ni
`CLAIMS_ARCHIVE.json`, y no tiene rama para `protocol_prune` (su payload no lleva `task_id` ni
`message_id`, solo `transitions.protocol_prune.task_ids`/`claim_ids`). Pero
`prune_state.py::apply_prune_via_submit_intent` escribe esos espejos A PROPOSITO antes de llamar
a `submit_intents`, porque la puerta de drift post-apply los exige (comentario en
`prune_state.py:555-560`). Diferencial: padre = fila EN el espejo; hijo = `{"tasks":[]}` en
caliente Y en el espejo -> la fila no existe en ningun sitio, con `ROLLBACK_LEDGER_PRESERVED`.
Invisible porque `materialize_protocol_state` no materializa los espejos -> nunca hay drift.
Atenuante declarado: `protocol_prune` exige capability `orchestrator`, que hoy solo tiene el
Arquitecto (Codex y Analista no) -- pero `mailbox_archive` exige la misma y fue el vector con el
que bloquee la iteracion 1.

**F-0280R2-02 (MAJOR, regresion).** `_events` parsea TODAS las lineas y relanza; el padre solo
parseaba la ultima, asi que le era invisible una linea ilegible a media cola. Medido por el
bucle: hijo = `EXEC_FAIL` + `LOOP_ERROR` x2 sin rollback, residuo sobrevive; padre = rollback OK
+ `ROLLBACK_LEDGER_DRIFT`. En aislado: `ledger_head.py --root <log corrupto a media cola>` da
EXIT 1 en el hijo y EXIT 0 en el padre. `submit_intent` trunca la cola desgarrada antes de anexar
(`runtime/eventlog.py::truncate_torn_jsonl_tail`) pero RECHAZA la corrupcion a media cola con
`EventLogIntegrityError` -> estado terminal para escritor y ahora tambien para lector.

**F-0280R2-03 (major, NO regresion).** `decision` firmada sobrevive; su
`Area_comun/decisions/DECISION-*.md` se destruye, con `PRESERVED`. `Area_comun/decisions/` no
esta en los cuatro prefijos del rollback. Cae en R4.
**F-0280R2-04 (menor).** `run_torn_tail_case` extrae `Get-LedgerHead` y
`Restore-TransientExecResidue` del `.ps1` con regex y las corre en aislado: no prueba que el
bucle sobreviva ni que el mensaje siga procesable, y no habria cazado la corrupcion a media cola.
Residuales nuevos: R5 (el residuo sobrevive por diseno a cada defer y se acumula si la causa es
persistente) y R6 (tarea que solo vive en el espejo no resuelve a ninguna ruta).

TECNICAS REUSABLES CONFIRMADAS (3 de 3 iteraciones):
- **El contraste diferencial contra el padre volvio a cazar el bloqueante.** Tres de tres.
- **Cuando un fix pasa de un filtro ancho a una LISTA EXACTA, auditar la lista contra la fuente
  de verdad del runtime, no contra el ejemplo del hallazgo.** Metodo que funciono: enumerar
  `Area_comun/state/` y `runtime/state/` en disco y cruzarlos contra `materialize_to_disk`
  (6 ficheros) y `submit_intent::files_for_backup` (tarea + ambos lados del mailbox). Lo que
  sobra en el `ls` y falta en la lista ES el agujero. Aparecieron los dos `*_ARCHIVE.json`.
- **Enumerar las OCHO `kind`s de `INTENT_TYPES` y preguntar por cada una "que fichero escribe".**
  `protocol_prune` -> espejos; `decision` -> DECISION-*.md; ninguna de las dos tiene rama en la
  derivacion. Las kinds que el maker probo (`mailbox_archive`, `task_upsert`) son las dos que si
  funcionan.
- **Probar por el BUCLE REAL, no por sondas de funciones extraidas.** El maker probo la cola
  desgarrada con una sonda; yo por el runner completo, y ahi se ve lo que la sonda no ve
  (exec 2 ocurre / no ocurre, residuo, `LOOP_ERROR`).
- Cambio de aridad de una funcion compartida (`event_log_head` de 2-tupla a 3-tupla): grepear
  TODOS los callers antes de nada. Aqui estaban bien (comparacion de tuplas).
- El sandbox del maker no tiene `Area_comun/state/TASK_INDEX.json`, asi que su suite NUNCA
  ejercita la rama de derivacion por fichero de tarea. Mi arnes si lo pone.
Script en el scratchpad: `bench_0280_iter2.py` (vectores VA_prune, VB_decision, VC_taskupsert,
VD_torntail, VE_midcorrupt; parametrizado por clon, corre el runner real, imprime observacion
JSON y NO afirma -- el juicio es mio).

NOTA DE HIGIENE: el hook de commit avisa `PRUNE DUE: released_ratio 90.0 >= 90`. No es mio
(exige `orchestrator`), pero lo hace mas urgente: la proxima poda es justo la transaccion que
F-0280R2-01 puede dejar sin traza si la interrumpen.

---

## 2026-07-21 -- TASK-0280 iteracion 3 (rollback conservador por defecto): NO-GO

Ancla: hijo `4310073`, padre `2185081`, HEAD `1582cc8`. Clones limpios `D:/ccvC` / `D:/ccvCp`.
Mi veredicto: `Area_comun/artifacts/Analista-TASK-0280-iter3-rollback-conservador-verdict.md`
(commit `b2ba2aa`, pusheado). Mensaje: `MSG-20260721-Analista-to-Arquitecto-REVIEW-TASK-0280-iter3-NOGO`.

El Operador firmo el 2026-07-21 00:25 el CAMBIO DE ENFOQUE (no otra ronda del mismo): rollback
CONSERVADOR POR DEFECTO, y `ROLLBACK_LEDGER_PRESERVED` solo tras prueba contra disco. La regla
funciona: el cuerpo del caso firmado es `if ($ledgerAdvanced) { probar disco; return }`, cero
mutacion, sin listas de rutas ni `kind`s. `event_managed_paths_after` quedo SIN LLAMADORES (esa
es la confirmacion estructural de que la enumeracion se abandono; `scripts/ledger_head.py` ni se
toco en el commit).

Cerrados y verificados por MI arnes (bucle real, contraste diferencial):
- F-0280R2-01 (poda firmada perdia la fila en los dos sitios): la fila sobrevive en
  `TASK_INDEX_ARCHIVE.json`; el padre la perdia.
- F-0280R2-03 (documento de `decision` firmada destruido): sobrevive; el padre lo destruia.
- F-0280R2-02 (linea ilegible a media cola ladrillaba el bucle): difiere con motivo, sin
  `LOOP_ERROR`, el exec siguiente ocurre.
- Pre-sucios ajenos intactos; `Get-ExecOutcomeClass` byte a byte identica al padre.

BLOQUEANTE NUEVO F-0280R3-01 (regresion de este commit, y NO esta en el rollback):
`Get-LedgerHead` dejo de lanzar -- correcto -- pero devuelve `seq=0` FABRICADO ante cualquier
fallo. Ese cero es la linea base de `Get-OwnEvidence`, que entonces recorre TODO el log y
encuentra un evento firmado propio de una ventana anterior; `Get-ExecOutcomeClass` emite
`confirmed` para un exec que salio 0 sin token `OUTCOME:`; el mensaje se marca en `seen.json` y
sale de la cola para siempre, sin trabajo aplicado y sin senal de error. El padre fallaba
ruidoso y SIN consumir. No requiere corrupcion: basta un exit != 0 de `python
scripts/ledger_head.py` (PATH, antivirus, IO), y los dos peones vivos tienen miles de eventos
firmados propios, asi que la evidencia propia con base 0 es SIEMPRE verdadera.

LECCION METODOLOGICA (la que quiero recordar): cuando un arreglo sustituye una EXCEPCION por un
VALOR POR DEFECTO, hay que grepear a quien viaja ese valor. Aqui el `0` era seguro para el
rollback (todas las ramas lo tratan como "no legible") y venenoso para el clasificador de
resultado, que solo veia el `seq`. La regla conservadora se aplico al rollback pero NO al exec:
el arnes sigue invocando al agente con la cabeza del log ilegible.

TECNICAS QUE FUNCIONARON (repetir):
- El CONTROL que aisla la causa: mismo vector, cambiando UNA sola cosa (el actor del evento
  antiguo) -> `confirmed`/consumido vs `unconfirmed`/reintentado. Sin ese control, el hallazgo
  seria una hipotesis.
- La VARIANTE que amplia la alcanzabilidad: repetir el vector con el log VALIDO y solo el helper
  fallando (stub que sale 1). Convierte "corrupcion rara" en "cualquier fallo de entorno".
- Verificar semantica de PowerShell por experimento y no por memoria: `trap { ...; return }` SI
  corta la funcion (lo probe con error aritmetico y con `throw` anidado). Sin eso habria
  reportado un falso positivo.
- `AbortedResidueMinutes` (5 por defecto) es lo que ACOTA el residuo conservado: con 0 el ciclo
  siguiente ejecuta; con 5 sale `RETRY_DEFER reason=staged_residue_live` hasta que envejece la
  mtime. La suite del maker corre con 0, asi que su verde NO demuestra la cota real.

Scripts en el scratchpad: `bench_v1.py` (cabeza ilegible), `bench_v1b.py` (helper que falla),
`bench_v1_control.py` (otro actor), `bench_v2.py` (tres efectos firmados + regresion + cota).

Observacion DECISION-0018 senalada: `CLAIM-20260721-Codex-TASK-0280-iter3` sigue activa con la
tarea en `in_review`.

## 2026-07-21 04:12 -- RECONCILIACION F-0280R3-01 (commit 3b47b3a)

Encargo: `MSG-20260721-Arquitecto-to-Analista-QUESTION-reconciliar-F-0280R3-01`. El Arquitecto
encargo una revision adversarial independiente que declaro mi bloqueante F-0280R3-01 **no
alcanzable**, citando el guard de las lineas 697-701 y `seq=$null` en la 452.

VEREDICTO: **OK-CLOSABLE**, sin contradiccion real. Las dos revisiones tienen razon sobre
**arboles distintos**. F-0280R3-01 se sostiene sobre `4310073` (el commit que juzgue) y esta
cerrado en `origin/main` por `116e581`, que ES la remediacion que mi hallazgo pidio y que es
**hijo directo** de `4310073`. La refutacion leyo el arbol ya arreglado.

LECCION #1, LA GRANDE -- **EL ANACRONISMO DE ANCLA**. Una revision que no declara su commit
puede refutar a otra correcta simplemente por leer el arbol posterior al arreglo. Como se caza,
y es barato: **los numeros de linea son una huella datable**. El consumidor de la linea base
(`Get-OwnEvidence -LedgerSeqBefore ([long]$ledgerHeadBefore.seq)`) esta en la **740** en
`4310073` y en la **745** en `main`: +5, exactamente el tamano del guard 697-701 que la
refutacion citaba. Cuando alguien cite lineas de un fichero, VERIFICAR contra que commit
resuelven ANTES de discutir el fondo. Y en mis propios veredictos, la tabla de ancla canonica
en primera posicion no es ceremonia: es lo que hace la refutacion falsable.

LECCION #2 -- **NO ESCRIBIR DISPARADORES SIN MEDIRLOS**. Concedi un sub-punto: enumere "python
no resuelto en el PATH" como disparador ilustrativo y es FALSO. Medido en PS 5.1.26100.8875:
`& binario-ausente` lanza `CommandNotFoundException`, terminante aun con `ErrorActionPreference`
en `Continue`, y `Get-LedgerHead` tiene `try/finally` **sin `catch`**, asi que se propaga y
`$LASTEXITCODE` nunca se asigna. El vector MEDIDO nunca lo uso, asi que el hallazgo no dependia
de el, pero en un veredicto bloqueante la seccion de alcanzabilidad se mide o no se escribe.

EL DISPARADOR REAL, para no volver a dudarlo: `scripts/ledger_head.py` **sin tocar**, con python
presente, sale **1** por `JSONDecodeError` NO capturada cuando una linea que **no es la cola** del
`events.jsonl` no parsea (`_events` solo tolera el `torn_tail` de la ultima linea). No hace falta
ningun helper falso. Cadena medida con las funciones extraidas verbatim de `4310073`:
`readable=False` pero `seq=0` (Int32 real, cero fabricado) -> `[long]0` -> `Get-OwnEvidence` acepta
un evento firmado propio historico -> linea 583 `if ($OwnEvidence) { return "confirmed" }` ->
`seen.json`. Control C9 (mismo vector, actor ajeno) -> `False`. 

LECCION #3 -- **BUSCAR LA FUGA NUEVA Y REFUTARLA YO MISMO**. Hipotetice que el guard solo cubria
el lado *Before* y que una cabeza ilegible DESPUES del exec daria `[long]$null = 0` (medido: el
centinela `$null` NO se autoprotege) inflando `$ledgerAdvanced`. **Refutada por la linea 533**
(`ledger_unreadable_after_exec`). Reportar la refutacion propia con la misma fuerza que el
hallazgo es lo que hace que el hallazgo pese.

RESIDUAL R-1 vivo: la rama `catch` (linea 458) sigue devolviendo `seq = 0` literal mientras la 452
devuelve `$null`. Inconsistente, y como `[long]$null` es `0` igualmente, **el guard es la unica
defensa real**. Cualquier consumidor futuro de `.seq` que olvide `readable` reabre la clase.

CONFIRMADA la ruta que encontro la revision adversarial: `event_log_head` devuelve
`int(events[-1]["seq"])`, ultima linea en orden de fichero, **no el maximo**. Con cola desordenada
reproduce el mismo desenlace por otra puerta y CON el guard puesto (ahi `readable` es `$true`).
Registrada en TASK-0281.

ALCANCE DECLARADO, importante: esto NO es la review de cierre de la iteracion 4. No corri el banco
de falsacion contra `116e581`, ni juzgue su negativo permanente nuevo, ni los otros tres hallazgos
de TASK-0281. Pedi encargo explicito de re-juicio en la pregunta del mensaje.

Gates por exit code (clon limpio `D:/ccvQ` en `4187849` + arbol): validate 0, scan_encoding 0,
neutralidad 0, mailbox_retry_cases 0. Aviso no bloqueante al commitear: PRUNE DUE
(released_ratio 93.75 >= 90) -- es del Arquitecto, no lo toco, queda senalado.

---

## 2026-07-21 05:25 -- TASK-0280 iteracion 4, re-juicio DE CIERRE sobre 116e581: NO-GO

Commit del veredicto: `ec5d9cc`. Artifact:
`Area_comun/artifacts/Analista-TASK-0280-iter4-cierre-verdict.md`. Ancla: `116e581` (ancestro
verificado de origin/main), gates corridos en clon limpio `D:/ccv0280`: validate 0, encoding 0,
neutralidad 0, drift False, `run_mailbox_retry_cases.py` 0. El encargo era la puerta del
redespliegue de los dos crons.

CONCEDIDO Y MEDIDO: la familia entera de "python no disponible" quedo cerrada, no solo la
variante del negativo enviado. Cuatro variantes propias mas la del helper: helper exit != 0,
helper ausente, `python` fuera del PATH con `$LASTEXITCODE` sembrado en 0 y en 7, y linea
corrupta a mitad del log. Las cinco difieren sin invocar al agente. El footgun de PowerShell
(`$LASTEXITCODE` conserva el valor previo cuando el comando no existe) queda tapado por el
`catch` de `ConvertFrom-Json`, no por el chequeo de exit code: defensa en profundidad accidental
pero real.

**LECCION #1 -- LA ASIMETRIA DENTRO DEL MISMO ARCHIVO ES DONDE VIVE LA FUGA.** F-0280R4-01:
`Get-LedgerHead` devuelve `readable=True` con `torn_tail=True`; el gate pre-exec (697-701) mira
solo `readable`, mientras `Restore-TransientExecResidue` SI difiere ante `torn_tail`
(linea 534). Cuando el mismo codigo trata la misma lectura como fiable en un punto y no fiable
en otro, el punto laxo es el defecto. Medido: base=2 con cola desgarrada, gate PASS, y
`Get-OwnEvidence` con esa base devuelve `True` al completarse la linea en vuelo como evento
propio `seq=3` -> falso `confirmed` con cero trabajo. Una cola desgarrada solo pudo dejarla otro
proceso: el exec aun no existia. Buscar asimetrias entre guards hermanos ANTES de buscar
vectores exoticos.

**LECCION #2 -- PRUEBA DE MUTACION CON CONTROL POSITIVO PARA JUZGAR UN NEGATIVO PERMANENTE.**
F-0280R4-02: la iteracion 4 desdento su propio negativo. Para salir del round ambiguo (que con
el gate nuevo se colgaba) inyectaron un reparador en segundo plano que reescribe
`runtime/state/events.jsonl` a los 500 ms con el contenido commiteado; la asercion
`events[-1].seq == 3` pasa por construccion. No lo argumente: lo medi. Mutante que destruye
`events.jsonl` en la rama de rollback ambigua -> suite exit 0 (ciega). Control positivo que
destruye `ambiguous-residue.txt` en LA MISMA rama, con centinela para probar que la rama se
ejecuta -> suite exit 1. **Un mutante que no dispara no prueba nada: el centinela + el control
son obligatorios.** Receta reutilizable para cualquier "negativo permanente" que me presenten.

**LECCION #3 -- MEDIR EL "SIN TOPE" CON DOS CORRIDAS, NO CON UNA.** F-0280R4-04: la primera
corrida (mensaje anterior al arranque del cron) salio sola por `MaxNoCoordinatorRounds` y habria
dado un falso "si tiene tope". La segunda, con el mensaje del coordinador VIVO (mtime posterior
al arranque, que es el caso normal), reseteo el contador cada ronda: 39 defers en 40 s, sin
`retry.json`, sin `RETRY_EXHAUSTED`, sin salida. **La variante que refuta es la que reproduce la
condicion de operacion real, no la mas facil de montar.**

RUTEO respetado: F-0280R4-03 (`events[-1]` no es el maximo, re-medido: max=9 con base 3 y
`own_evidence=True`) y F-0280R4-04 van a TASK-0281 por instruccion explicita del Arquitecto; no
reabri 0280 por ellos. Bloqueantes de 0280: solo F-0280R4-01 y F-0280R4-02.

**LECCION #4 -- SEPARAR EL VEREDICTO DE LA DECISION OPERATIVA.** El encargo ataba mi GO al
redespliegue de los crons. Di NO-GO al ENUNCIADO DEL CIERRE y dije aparte, con los datos, que en
los siete vectores medidos `116e581` es estrictamente mejor que lo desplegado y que redesplegar
es decision del Arquitecto/Operador, no mia. Un checker no debe secuestrar una decision
operativa con su gate tecnico, ni ablandar el gate para no estorbarla.

VENTANA COMPARTIDA: al escribir, Codex tenia entrega en vuelo de TASK-0281 (llego a hacer
`reset`: `23b9f5c`/`011a840` desaparecieron y reaparecieron como `33e3af7`). Sondee cada 20 s
hasta ver arbol gobernado limpio + commit de memoria (cierre DECISION-0026) y solo entonces
comitee, con pathspec explicito de mis dos archivos. Un `scan_encoding` dio `PermissionError`
transitorio mientras el peer escribia: **un gate rojo durante la ventana del peer se reintenta
antes de reportarlo como fallo**. PRUNE DUE (released_ratio 94.29) queda senalado al Arquitecto,
no lo toco.

DATO UTIL PARA EL PROXIMO ENCARGO: la entrega de 0281 sustituye la base de `seq` por offset en
BYTES (`LedgerBytesBefore`) y anade `Register-RetryDefer` + `SELF_HEAL_ORPHAN_LOCK`. Eso cerraria
estructuralmente F-0280R4-01 y F-0280R4-03, pero NO lo he juzgado: requiere banco propio sobre su
commit. Ojo especifico: con base por bytes, un truncado del log (longitud menor) o una reescritura
del mismo tamano dejan de ser detectables por longitud.

## 2026-07-21 (2) - TASK-0281 sobre 8ea4874: NO-GO. Cuatro deslices, dos bloqueantes.

Encargo: MSG-20260721-Arquitecto-to-Analista-REVIEW-TASK-0281-y-orden-de-cierre. Clon limpio
`D:/ccv0281` sobre `8ea4874`. Gates: validate / encoding / neutralidad / drift 0 / suite
`run_mailbox_retry_cases.py` -> los cinco exit 0. Commit del veredicto: `57f6250` (empujado).
Artifact: `Area_comun/artifacts/Analista-TASK-0281-bucle-liveness-verdict.md`.

Veredicto: puntos 1 (lock huerfano) y 2 (defer con tope y senal) CERRADOS. Puntos 3 (ventana
por bytes) y 4 (residuo) NO.

- **F-0281-01 (bloqueante).** La ventana por bytes asume append-only ESTRICTO. Con el log
  reescrito y mas largo que la base, la ventana `[base, fin)` cubre historia: probe con el
  runner completo, agente que no hace nada y no emite token -> `outcome=confirmed` + `seen`.
  Incumple el acceptance verbatim (dice "o reescrita"). No hipotetico:
  `runtime/eventlog.py:1131` (`compact_through`) reescribe `events.jsonl` en sitio.
- **F-0281-02.** Compactacion que encoge -> `currentLength -le base` -> oculta trabajo propio
  REAL. Falla de los DOS lados segun la reescritura acabe mas larga o mas corta.
- **F-0281-03 (bloqueante).** `Get-StagedResidueState` LANZA con rutas que git entrecomilla
  (espacio o byte no-ASCII): `Test-Path` con comillas -> "Caracteres no validos". La llamada
  esta en la linea 696, FUERA del `try` que abre en la 735, asi que la excepcion cae en el
  `catch` del bucle -> `LOOP_ERROR` indefinido, sin `retry.json`, sin `RETRY_EXHAUSTED`, sin
  invocar al agente. Es el defecto (2) reintroducido por la puerta del arreglo del (4).
- **F-0281-04 (bloqueante).** El defer agota y senaliza pero NO recupera: veto ambiental
  (peer ocupado 3 rondas) consume el mismo presupuesto que un intento real sin que el agente
  corra ni una vez; despues el mensaje queda excluido de la cola PARA SIEMPRE aunque el arbol
  se limpie, con `Heartbeat processable_messages=0`.

**LECCION #1 -- UNA BASE POSICIONAL HEREDA EL PROBLEMA QUE VIENE A RESOLVER.** Cambiar de
`seq` a bytes mata el camino concreto (`torn_tail` no puede acortar el fichero) pero no la
FAMILIA: cualquier ancla que dependa de la POSICION en un fichero cae en cuanto el fichero se
reescribe. La pregunta correcta ante una base nueva no es "cierra el caso que me dieron" sino
**"que supuesto sostiene la base, y quien en el repo lo rompe"**. Buscar el rompedor con grep
en el propio codigo (`write_text` sobre el log) convirtio una objecion teorica en una cita.

**LECCION #2 -- MEDIR EL ARREGLO DE UN DEFECTO CONTRA EL ACCEPTANCE DE LOS OTROS.** F-0281-03
no aparece atacando el punto 4: aparece preguntando "que le hace el punto 4 al punto 2". En
una tarea que cierra N defectos de la misma familia, el vector mas productivo es el
CRUZADO: el arreglo de (4) reabrio (2). La suite del maker nunca lo veria porque cada
negativo prueba su propio punto.

**LECCION #3 -- BUSCAR LA EXPOSICION REAL EN EL PROPIO REPO, NO ARGUMENTAR PROBABILIDAD.**
"Rutas con espacio" suena a caso de laboratorio hasta que `git ls-files | grep ' '` devuelve
`examples/full_runtime_instance/personal/operador humano/.gitkeep` -- una area de participante
SHIPPEADA, justo donde DECISION-0016 manda escribir. Un unico grep convierte "podria pasar"
en "pasa aqui". Hacerlo SIEMPRE antes de graduar la severidad.

**LECCION #4 -- "AGOTA Y SENALIZA" NO ES "SE RECUPERA".** El maker cumplio la letra del
acceptance y aun asi creo perdida de mensajes. Al medir un presupuesto de reintentos hay que
correr la SEGUNDA fase: quitar la causa y ver si el sistema vuelve. Y ojo con el reporte que
se auto-declara sano: `processable_messages=0` con un mensaje vivo sin responder en `open/`
es un reporte FALSO, del mismo genero que un tablero desactualizado.

**LECCION #5 -- CONTAMINACION DE LA PROPIA SONDA.** Mi primer probe D escribia `p.ps1` DENTRO
del sandbox bajo prueba, asi que `git status` lo veia fresco y TODOS los casos daban "live":
un falso PASS y un falso SLIP a la vez. La sonda que se mide a si misma no mide nada. Los
probes van FUERA del arbol observado, siempre. Lo cazo un resultado incoherente (un caso que
"pasaba" y otro que devolvia cadena vacia), no una revision del codigo del probe.

Ventana: Codex tenia entrega en vuelo de F-0280R4-02 (claim activa sobre `CLAIMS.json#...` y
`personal/Codex/Memory.md`); espere a su commit de memoria (`98f3d53`, cierre DECISION-0026) y
comitee con `git add` + `git commit -- <pathspec>` de mis dos archivos. **PRUNE DUE
released_ratio 95.0 >= 90** senalado al Arquitecto; no lo toco.

Bucle declarado: remediacion de Codex acotada a los tres puntos del apartado 6 del artifact,
re-juicio mio ANTES del commit de cierre, **maximo 2 iteraciones** y a la tercera escalo al
operador.

---

## 2026-07-21 16:37 -- TASK-0280 F-0280R4-02: GO al cierre (commit c7d8b8e)

Encargo: MSG DECISION del Arquitecto desacoplando 0280 de 0281. Pregunta literal: el
control positivo del maker prueba que el brazo puede fallar, o solo que falla ante SU
mutacion? Anclaje: HEAD canonico `39aa3dc`, commit juzgado `32cea00` (byte-identicos en
los dos ficheros bajo revision). Clon limpio `D:/ccv0280`. Veredicto **GO / OK-CERRABLE**;
artifact `Area_comun/artifacts/Analista-TASK-0280-F02-cierre-verdict.md`.

**LECCION #1 -- NO REPRODUCIR EL CONTROL DEL MAKER: ESCRIBIR EL PROPIO BANCO.** Para
refutar "control positivo a medida" no sirve re-correr su mutante. Escribi NUEVE mias
sobre la rama exacta (`peer_mailbox_cron.ps1:565`) variando DOS ejes a la vez:
*ordenamiento* (antes del defer / despues / en la ventana ciega tras la captura del
checker) y *forma del dano* (vaciado / append / borrado del fichero / eliminacion de la
rama entera). 8 muertos de 9. Un banco de un solo eje habria confirmado al maker sin
probar nada. Driver reutilizable: python que aplica el mutante, corre la suite, mide exit
code y revierte con `git checkout --` entre mutantes.

**LECCION #2 -- PREGUNTAR SIEMPRE *QUIEN* MATA AL MUTANTE, NO SOLO SI MUERE.** El hallazgo
util del dia (R1) no salio del marcador 8/9 sino de leer el MENSAJE de cada fallo: M6 y M8
pasaron la asercion NUEVA y murieron en la VIEJA (`events[-1].seq==3`). O sea el poder
falsador lo sostiene un PAR de aserciones con fronteras distintas (nueva = `fixture ->
defer`; vieja = lo posterior al defer), y el maker no lo declara. Quien relaje la vieja
creyendo que la nueva la subsume desdienta el brazo otra vez. Un mutante que muere "por
otro sitio" es informacion, no ruido.

**LECCION #3 -- UN SUPERVIVIENTE PUEDE SER CORRECTO.** M9 (destruir y reescribir
byte-identico) sobrevive y NO es un escape: el criterio exige preservar CONTENIDO, y lo
preserva. Registrar como residual (la barrera es un muestreo de dos puntos de contenido,
no una invariante de "no se escribe"), nunca como SLIP. Inflar un superviviente correcto a
defecto quema credibilidad para el hallazgo que si importa.

**LECCION #4 -- REVISAR LOS SIETE CRITERIOS, NO SOLO EL REPARADO.** Estaba firmando un
CIERRE, no una remediacion. Repase las 7 lineas de acceptance incluida la que nadie mira
(espejo born-operational): `new_instance.py --tier runtime` a sandbox -> exit 0, validate
de la instancia nueva exit 0, `peer_mailbox_cron.ps1` byte-identico sha256 `3215b0b2...`.
De paso salio R5: `examples/` NO se exporta, asi que la instancia hija hereda la garantia
SIN heredar el negativo que la protege (preexistente, declarado, no bloqueante).

**LECCION #5 -- EL DOD MANDA SOBRE MI PROPIO VEREDICTO ANTERIOR.** Mi iter4 declaro
F-0280R4-01 (`torn_tail`) BLOQUEANTE y condiciono el cierre a secuenciarlo tras 0281. El
Arquitecto desacoplo. Antes de aceptar o rechazar fui a las SIETE lineas de acceptance de
TASK-0280: `torn_tail` no esta en ninguna -- entro como defecto del gate adyacente que el
maker introdujo remediando. Acepto el desacople por esa razon concreta, NO por deferencia,
y dejo escrito en el artifact que el GO no firma esa garantia. Regla: cuando el arquitecto
mueve una frontera, se verifica contra el DoD escrito, no contra lo que yo dije antes.

**LECCION #6 -- MI PROPIO COMMIT DEJO EL ESTADO CANONICO ROJO (reincidencia F-0240-01).**
`57f6250` (veredicto 0281) llevaba `Ops-Reason` separado de `Co-Authored-By` por LINEA EN
BLANCO -> el parser solo lee el ULTIMO parrafo, asi que el Task-Id quedo invisible ->
`validate` ROJO en `c4ce07a` y otro avance de linea base a costa del Arquitecto. Es mi 4a-5a
recurrencia segun su bitacora. **REGLA DURA: trailers en UN SOLO parrafo final, sin lineas
en blanco entre ellos, Co-Authored-By INCLUIDO en ese mismo bloque.** Verificar SIEMPRE con
`git log -1 --format=%B | cat -A` tras commitear. Lo reporte sobre mi mismo (DECISION-0018)
y pedi que TASK-0279 (chequeo de trailers en pre-commit que ABORTA) deje de estar en ready.

**LECCION #7 -- EL VALIDATE PUEDE MENTIR EN LOS DOS SENTIDOS BAJO ARBOL COMPARTIDO.** Al
arrancar, el arbol caliente daba drift en `CLAIMS.json` (el Arquitecto escribia) y minutos
despues drift False; `scan_encoding` dio exit 1 una vez y exit 0 dos veces seguidas (Codex
escribiendo). Un gate rojo transitorio en arbol compartido NO es un veredicto: repetirlo y
confirmarlo en CLON LIMPIO antes de reportarlo. El unico rojo real era el mio (trailers).

Ventana: Codex con claim activa `CLAIM-20260721-Codex-TASK-0281-iter2` sobre los DOS
ficheros que juzgue -- por eso todo el juicio salio del clon limpio, cero lecturas del
arbol caliente. Commit con `git add` + `git commit -- <pathspec explicito>` de mis dos
archivos; su entrega de iter2 quedo fuera. Push llevo tambien su commit `b59726b` (arbol
compartido); `c7d8b8e` es ancestro de `origin/main` y origin/main valida verde en clon
limpio. **PRUNE DUE released_ratio 95.35 >= 90** re-senalado al Arquitecto; no lo toco.

Sin bucle de correccion: GO, no CHANGE-REQUIRED. Seis residuales declarados (R1 el que
importa); si el Arquitecto quiere R1/R3 como unidad, es trabajo nuevo.

---

## 2026-07-21 17:34 -- TASK-0281 iteracion 2 (commit 7b708f8): NO-GO ACOTADO + escalado del tope

Veredicto en `Area_comun/artifacts/Analista-TASK-0281-iter2-append-defers-verdict.md`,
mensaje `MSG-20260721-Analista-to-Arquitecto-REVIEW-TASK-0281-iter2-verdict.md`,
commit `4d4fd81` (pusheado; validate 0 y scan_encoding 0 tras el push).
Clon limpio `D:/ccv0281b` sobre `7b708f8`; los 4 gates verdes ALLI.

**LECCION #8 -- UN TEST PUEDE PROBAR SU PROPIA CONTAMINACION.** El negativo permanente que
declaraba cerrado el vector no-ASCII (`run_nul_residue_path_cases`) escribe su propio
`nul-residue-probe.ps1` DENTRO del sandbox que evalua: ese fichero ya es residuo fresco no
rastreado, asi que `Get-StagedResidueState` devuelve `live` **aunque el fichero objetivo no
exista**. Lo demostre con el experimento de vacuidad (probe fresco, SIN objetivo -> `live`) y
con la descontaminacion (probe envejecido con `os.utime` -> el espacio sale `live`, el
no-ASCII sale `aborted`). **TECNICA REUTILIZABLE: ante un negativo que pasa, ejecutarlo SIN
la condicion que dice detectar; si sigue verde, no prueba nada.** Segundo contaminante en el
mismo sandbox: el caso anterior deja `runtime/state/events.jsonl` recien escrito.

**LECCION #9 -- POWERSHELL MAL-DECODIFICA LAS RUTAS QUE GIT EMITE EN UTF-8.**
`[Console]::OutputEncoding` es cp850 (ibm850) en esta maquina: `git status --porcelain -z`
emite el nombre en UTF-8 y PowerShell lo reconstruye mal, `Test-Path` da False y el residuo
se vuelve invisible. `-z` mata el entrecomillado (el espacio SI quedo arreglado) pero no la
decodificacion. Instrumentar siempre imprimiendo `[Console]::OutputEncoding`, el nombre en
disco, el nombre que decodifica git y los CODIGOS de caracter -- ahi se ve el mojibake.
Afecta tambien a `Get-WorktreeDiskProof` y a la limpieza de no-rastreados del rollback.

**LECCION #10 -- LA DIRECCION DEL DANO ES PARTE DEL VEREDICTO.** El mismo vector paso de
fallar CERRADO y ruidoso (LOOP_ERROR, 12 rondas de atasco en iter1) a fallar ABIERTO y
callado (el runner pisa la entrega viva del peer y lo registra como `staged_residue_aborted`,
que se lee como seguro). Un arreglo que cambia de direccion el fallo NO cierra el vector, y
el silencio lo empeora. Medirlo SIEMPRE sobre el runner completo, no solo con la funcion
extraida: la funcion daba `aborted` (ambiguo), el runner dio `EXEC_START=1` + mensaje
consumido (inequivoco).

**LECCION #11 -- PROBAR EL REVES (falso rechazo), no solo el escape.** El Arquitecto lo pidio
explicitamente y valio: contraste del hash por bloques de PowerShell contra `hashlib` sobre el
`events.jsonl` VIVO (6.857.842 bytes) en 8 longitudes incluidas las fronteras 65535/65536/65537
-> MATCH byte a byte en 4 ms. Sin eso, "no encontre falso rechazo" seria una opinion.

**GOTCHA DE HERRAMIENTA:** una funcion PowerShell llamada `Git` se auto-invoca (PowerShell es
case-insensitive y las funciones ganan a los ejecutables) -> recursion infinita y el probe
cuelga sin salida. Nombrarla `RunGit` e invocar `git.exe`. Y `Push-Location` no basta para
los comandos nativos: usar `git.exe -C <dir>` explicito.

**VECTOR VACIO:** salto de linea en nombre de fichero NO es alcanzable en Windows (Win32
rechaza chars < 32, tambien por `\?\`). Documentarlo como muerto por plataforma, no por el
arreglo; re-abrirlo si el runner se porta a POSIX (alli `-join ""` perderia el salto).

Cerrados y bien probados en esta iteracion: punto 1 (append puro por hash: 13 vectores) y
punto 3 (defers con `EXEC_START=0`, `attempts=0`, recuperacion al limpiarse el arbol, y
agotamiento post-exec que SIGUE excluyendo -> no hay reproceso infinito). Del punto 2 quedaron
cerrados el espacio y la excepcion contenida en el `try` (`.git` roto -> 3 `EXEC_FAIL`, cero
`LOOP_ERROR`, ni lock ni lease huerfanos).

Trailers en UN SOLO parrafo (leccion #6 aplicada, sin reincidencia). **PRUNE DUE
released_ratio 95.83 >= 90** sigue pendiente del Arquitecto; no lo toco.

**Tope de 2 iteraciones AGOTADO -> escale la decision al operador humano.** Si el Arquitecto
cierra 0281 igualmente, exigi que F-0281-05 y F-0281-06 salgan con ACCEPTANCE PROPIO (TASK-0283
o unidad nueva), nunca como residuo suelto.

---

## 2026-07-22 - TASK-0276 (evidencia util) VEREDICTO: NO-GO / CHANGE-REQUIRED (commit 2b54caa)

Juzgue el fix `18ce287` que cerraba mi residual F-0272R2-01 (E04: un exec de puro claim
acquire/release quema el mensaje sin trabajo util). El fix filtra la evidencia propia por
`applied:true` + coherencia keyid-actor + `intent_type in {task_status,task_upsert,decision}`
**O** `payload.commit`. **BLOQUEE por la rama `-or $hasCommit`.**

**HALLAZGO CLAVE (falsable, ganado por leer el ledger, no por confiar en los nombres de test):**
`payload.commit` NO es senal de trabajo util. `runtime/submit_intent.py::event_payload_for`
(lineas 645-646) estampa el `--commit` del llamante en el payload de TODO intent, ANTES de
ramificar por tipo -> tambien claim y exception. En el ledger vivo del clon: **1894 de 2022
eventos ed25519 de claim llevan payload.commit**, incluidos 25+ acquire/release standalone
(p.ej. `analista-task-0194-review-claim` / `-release`). Asi que un claim puro con etiqueta
--commit (el patron REAL dominante) confirma via la rama commit -> E04 NO cerrado.

**Probe propio** (extraje Get-OwnEvidence del runner del clon, imite la forma del evento REAL):
pure_claim_no_commit->False (modelo del maker), pero pure_claim_acquire_label->True,
pure_claim_release_label->True, exception_with_commit->True (FUGAS). V2/V3/V4 pasan
(real_delivery_status->True, applied_false->False, foreign_key->False).

**Disciplina 0283 con dientes:** M1-M5 (revertir cada correccion en el runner del clon)
enrojecen la suite (exit 1). El problema NO era falta de dientes -> era que la ESPEC del
positivo "commit" en run_useful_own_evidence_cases es la incorrecta (afirma que claim+commit
DEBE confirmar), asi que el filo E04 se cuela dentro de la propia suite.

**LECCION METODOLOGICA:** cuando un fix usa un campo del payload como proxy de una propiedad
semantica ("commit => entrega"), VERIFICAR el proxy contra el ledger real antes de aprobar.
El maker modelo "pure claim" = claim sin commit; el ledger dice que los claims reales SI
llevan commit. El ejemplo del test mintio por omision; el conteo del ledger lo caza.

**Remediacion pedida a Codex (via Arquitecto, response_owner Arquitecto):** eliminar la rama
`-or $hasCommit` (la entrega real ya confirma via task_status sin commit, probado) o gatearla
para excluir claim/exception; anadir PERMANENT_NEGATIVE (claim+commit -> NO confirma); corregir
el caso "commit". Re-juicio mio en clon limpio antes del GO, **max 2 iteraciones antes de
escalar al humano**. Trailers Task-Id en un solo parrafo (sin reincidencia).

## TASK-0276 RE-JUICIO (iter2) -- GO / OK-CLOSABLE (2026-07-22 17:28, commit 6340b43)

CERRADO. El maker (Codex, fix 6eb57c9, entregado en 8649524) elimino la rama independiente
`-or $hasCommit` de Get-OwnEvidence. Ahora solo confirma intent_type en
{task_status,task_upsert,decision} con applied true, ed25519, keyid coherente y sig no vacia.
**payload.commit quedo IRRELEVANTE.**

Re-juzgado en clon limpio a 8649524 (D:\ccv0276b). Probe propio por comportamiento (17 casos,
mismo extractor Get-OwnEvidence del ps1, NO los nombres de tests):
- pure_claim_acquire_commit / release_commit -> False (E04 CERRADO)
- familia completa con commit (mailbox_archive/protocol_prune/exception/project_narrative) -> False
- entrega real (task_status +-commit, task_upsert, decision) -> True (sin regresion de positivo)
- applied_false / foreign_key / not_ed25519 / empty_sig / foreign_actor -> False (firma OK)
- uppercase_keyid -> False (residual conservador: retry, no burn; peers reales usan minuscula)

Dato clave que cierra el slip: en el ledger, intent_types con commit son claim=2634,
mailbox_archive=1078, prune=21, exception=2; solo confirman task_status+upsert+decision
(1069 eventos). La etiqueta commit ya no discrimina.

**MUTACION DEMOSTRADA (V3):** en un 2o clon limpio (D:\ccv0276m, checkout 8649524) reintroduje
la rama commit en el fuente peer_mailbox_cron.ps1 -> la suite run_useful_own_evidence_cases
enrojece (AssertionError "contract is incomplete", exit 1). El contrato exige
`if (-not $hasUsefulIntent) { continue }` presente y `$hasCommit` ausente. Permanent_negative
con dientes reales.

Gates: validate/scan_encoding/neutralidad exit 0, drift 0 (has_drift=False), suite del reintento PASS.

Veredicto en Area_comun/artifacts/ANALISTA-TASK-0276-rejuicio-GO-verdict.md (supersede el
CHANGE-REQUIRED de iter1). Mensaje MSG-20260722-Analista-to-Arquitecto-REVIEW-TASK-0276-GO.md
(requires_response true, response_owner Arquitecto). Commiteado con pathspec explicito +
trailers Task-Id/Ops-Reason/Co-Authored-By, push OK a origin/main. Fix loop cerrado en iter2
(1 remediacion), sin escalar al humano.

**LECCION confirmada:** mi leccion metodologica de iter1 (verificar el proxy commit contra el
ledger real) fue la que forzo el fix correcto -- el maker paso de "commit => entrega" a
"solo intent_type util => entrega". El re-juicio por comportamiento + la mutacion de fuente
en clon limpio es lo que da el GO defendible.

---

## TASK-0275 (residual de cuarentena) - GO / OK-CLOSABLE (2026-07-22 17:39)

REVIEW del Arquitecto: residual REDUCIDO de la cuarentena (el mecanismo mover-en-vez-de-borrar
ya se entrego en TASK-0282). Commit citado 81fe270; HEAD canonico c6b1af5. Verifique que runner
+ harness + README son BYTE-IDENTICOS entre ambos (sha256 del runner igual, diff vacio), asi que
corri comportamiento contra codigo == citado y protocolo contra HEAD. Clon limpio D:/ccv-0275.

Tres puntos, todos PASS por comportamiento:
1. Log EN EXITO: peer_mailbox_cron.ps1:745 emite `ROLLBACK_QUARANTINED path=$path
   quarantine_path=$quarantineRelative` DENTRO del foreach tras Move-Item exitoso (por fichero,
   no solo el primero). E2E run_mailbox_retry_cases.py:938-971 reproduce residue.txt (untracked
   de peer nacido en la ventana, count==2), aborta, exige el log + el fichero en
   .protocol-tmp/rollback-quarantine/<id>/. Familia completa: mailbox de la ventana NO se pone
   en cuarentena (allowlist Test-LedgerManagedPath).
2. Retencion: README:149-155 = 30d, limpieza manual operador/Arquitecto, loop nunca auto-borra.
   grep confirma NINGUN camino borra la cuarentena. AbortedResidueMinutes es cutoff del residuo
   staged, NO GC de cuarentena. Coincide con acceptance reducida (task 62-64).
3. Negativo permanente: DOS mutaciones mias en clon limpio. A) borrar el log -> ROJO en contrato
   estatico (run_nondestructive_rollback_contract linea 258). B) dejar el string EXACTO pero
   guardarlo con `if($false){...}` -> contrato estatico PASA pero E2E ROJO en linea 969
   ("successful quarantine did not log both recovery paths"). Prueba que el E2E es el diente real,
   no una prueba por-nombre/por-presencia-de-string.

**LECCION reutilizable:** cuando un contrato de mutacion es SOLO string-presence, la mutacion B
(mantener el string y neutralizar el comportamiento con if($false)/guard) distingue si el E2E
mide comportamiento o solo mide su propia sombra. Aqui las DOS capas cazan la regresion -> GO
defendible. (Contrasta con 0284, donde 2 de 5 negativos SOLO median su sombra -> CHANGE-REQUIRED.)

Residual declarado R1 (no bloqueante): la retencion es documental/gobernanza, NO maquinal; la
cuarentena crece sin cota hasta limpieza humana -- exactamente lo ratificado (el loop no debe
auto-borrar para no re-introducir destruccion silenciosa).

Gates: validate/encoding/neutrality exit 0, arbol tracked del clon limpio == HEAD (drift limpio),
suite del reintento PASS. Artifact Analista-TASK-0275-cuarentena-residual-verdict.md + msg
MSG-20260722-Analista-to-Arquitecto-REVIEW-TASK-0275-verdict.md (requires_response, owner
Arquitecto). Commit 059c1d4 pathspec explicito + trailers, push OK. El flip a done es del
Arquitecto (yo checker-only). Sigue 0285 (runner instanciacion) y luego el nucleo 0103.

---

## TASK-0259 iter3 (guardian re-sync, MECANICA) -- GO / OK-CLOSABLE -- 2026-07-22 21:32

Commit veredicto 784e587 (pathspec explicito + trailers Task-Id/Ops-Reason, push OK). Impl bajo
revision 7c7bc1c / deliver 03f5bf9; clon limpio en canonical 779fb46 (rutas de codigo
byte-identicas a 7c7bc1c). iter3 = fix mecanico autorizado por el Operador tras mi NO-GO iter2.

Que confirme (los 4 puntos de la instruccion, todos PASS):
1. INTOCABILIDAD: `git diff 03f9b9a 7c7bc1c -- runtime/turn_validate.py runtime/turn_schema.json`
   = VACIO. Unico cambio de codigo: run_runtime_turn_obstacle_cases.py (32 lineas). El corazon
   conductual que confirme en iter2 no se toco.
2. GUARDIAN VERDE: check_falsification_contracts.py --inventory exit 0 Y
   test_falsification_contracts.py exit 0 (AMBOS rojos en iter2). Los 8 gates verdes en clon limpio.
3. LOS 5 NEGATIVOS ENGANCHAN DE VERDAD: main() ahora marca los 6 permanent-negatives (linea 91;
   se quito el stale NEG-TURN-FRICTION-OBSTACLES). Los mutation/boundaries declarados mapean
   VERBATIM a lineas de test REALMENTE EJECUTADAS. NO confie en los asserts del maker: reimplemente
   friction_sensors desde cero y quite UNA rama por vez -> STATUS_ERR/assign_fix/CHECKS_ERR/
   REVERT_ERR desaparecen al revertir por validate_turn (entrypoint REAL), ATTEMPT_ERR aparece al
   reintroducir el counter-parse. Permanencia real, no text-theater.
4. NO-REGRESION: MS1-MS5/ESC1-ESC4 identicos a iter2 (codigo no cambio).

CLAVE reutilizable: el guardian (check_falsification_contracts.py) es TEXT-PRESENCE puro (verifica
que mutation/boundaries aparezcan verbatim en el exercised_by y que markers<->contratos sean
biyectivos); NO ejecuta la mutacion. La EJECUCION la garantiza OTRO gate (el runner corre main()
con asserts vivos, exit 0). Un re-sync legitimo alinea las DECLARACIONES al codigo de test REAL;
el fraude seria alinear el test a declaraciones decorativas. Aqui guardian+runner+mi-revert-
independiente coinciden -> GO defendible. (Espejo de la leccion 0275/0284: la mutacion que
distingue diente-real de sombra.)

Residuales declarados (ninguno bloqueante): (R1) revert proxy evadable POR DISENO -- mi probe
"Rolled back" (dos palabras) NO dispara el regex single-token `rollback`; senal estructurada
diferida a TASK-0258. (R2) el positive boundary declarado del negativo REVIEW es una ASIGNACION
(`review_errors = ...`), no un assert explicito; el positive real (runner linea 132) SI ejecuta
pero no es boundary enforced por el guardian -> cobertura del guardian mas delgada en esa direccion.

ANOMALIA a vigilar (DECISION-0018, senalada al Arquitecto): el pre-commit hook reporto PRUNE DUE
(released_ratio 90.91 >= 90). La poda es operacion COORDINADA del Arquitecto (prune_state.py
--apply), no mia (checker-only). El commit local continua; CI es la frontera dura. Que el
Arquitecto corra la poda en su proximo checkpoint.

Flip a done = del Arquitecto (yo checker-only). Con esto TASK-0259 (nucleo tanda 0103) queda GO;
la cadena de remediacion 0259 cierra tras 3 iteraciones (iter1 NO-GO friccion inerte, iter2 NO-GO
guardian rojo, iter3 GO).

---

## TASK-0260 (C1 vista de plan + gate turno 0) -- GO / OK-CLOSABLE (2026-07-22 22:15)

Commit veredicto 7366925 (push OK). Impl b7d29c1 (deliver 5cfeb47); runtime/*.py + example
IDENTICOS a HEAD 1ab1be1 -> puertas en b7d29c1 = HEAD vivo. Clon limpio D:/ccv0260 @ b7d29c1;
TODAS las puertas exit 0 (plan_approval_cases + 3 turn runners + validate + scan_encoding +
neutrality + git diff --check). Extraje render_plan/plan_approval_error/run_loop del CLON y corri
28 payloads PROPIOS (no los del maker) sobre toda la familia de cada punto -> 28/28 PASS.

Diseno del gate (correcto en ambas direcciones): render_hash = TODO el render; approval_hash =
SOLO {id, acceptance, risk} sorted-by-id. Display (goal/verification_cmd/required_capability/
estimate) mueve render_hash pero NO approval_hash -> no invalida en falso. Material (acceptance/
risk/unidad nueva) mueve approval_hash -> invalida. Reorden del index NO invalida (sort por id).
Auth: actor in human_actors(caps=human_owner) + payload.approval_hash==expected + type==plan.approved
+ verify_event_auth (si event_auth) + verify_actor_auth (si agent_signatures). run_loop rehusa
turno-0 con ok:false "turn-zero plan approval required" ANTES de cualquier mutacion (cero efecto
colateral); probe: con firmas ON y sin actor_auth -> rechazado (sin falso-seguro). Gate NO toca
supervised_autonomy/human_checkpoint. Hub intacto: los 5 eventos del commit son intent.applied
(submit_intent lifecycle 0260), no orchestrator; sin RUN-*.jsonl; config/dataset/6-reservadas
fuera del filelist.

CLAVE reutilizable: probar el "arranca" de forma INTEGRAL en run_loop, no solo el guarda aislado
(el test del maker solo asertaba plan_approval_error(...) is None para esa direccion). Y probar la
direccion de NO-invalidacion-falsa (cambiar campos no-materiales) ademas de la de invalidacion.

Residuales declarados (ninguno bloquea C1): R1 alcance por decision_id (unidad ligada a otra
decision queda excluida del plan decision-scoped y no invalida; con decision_id=None todas cuentan).
R2 fuerza de auth = postura event-log (con event_auth+agent_signatures off, actor confia en texto
plano; not_enforced_phase2 pasa aun con firmas ON -> escotilla GLOBAL de fase 2, no nueva). R3 slip
cosmetico: intake verification_cmd nombra run_runtime_turn_cases.py inexistente; reales = 3 split +
plan_approval, todos verdes.

ANOMALIA (DECISION-0018, senalada al Arquitecto en el MSG): prune_state --check = DUE
(released_ratio 92.59>=90); poda --apply es op de orchestrator bajo enforce, no mia; que la corra
en su checkpoint. Flip a done = del Arquitecto (yo checker-only).

---

## 2026-07-22 23:43 -- TASK-0261 remediacion iter1 (parser obstacles indentado): GO (OK-CLOSABLE)

Commit veredicto: bf39da7 (pusheado). Impl bajo revision: f1d9c30; padre b6fa2b1;
HEAD canonico b07035c. SIN PRODUCTO.

Mi NO-GO previo (verdict obstacles-friction) probo un defecto de robustez: parse_mailbox_obstacles
solo veia el guion en columna 0; una lista YAML INDENTADA (convencion context_refs) se leia VACIA
en silencio -> SLIP-1 (falso rojo a lista valida indentada con friction>0) y SLIP-2 (malformado
indentado con friction 0 pasaba). iter1 reescribe el parser: item_start `^([ \t]*)-\s+...` (guion
a cualquier indent), ancla item_indent al primer guion, campos exigen indent ESTRICTAMENTE mayor,
continuacion idem.

Verificado por COMPORTAMIENTO en clon limpio contra el entrypoint real (subprocess, exit-code) Y
contra el padre para probar el before-state:
- SLIP-1 lista indentada valida + friction 2: frontmatter exit 1->0, cuerpo 1->0. Cerrado.
- SLIP-2 malformado indentado + friction 0: frontmatter exit 0->1, cuerpo 0->1 (needle
  "must contain exactly"). Cerrado.
- No-regresion 9/9: grandfathering, opt-in ambos bordes, 4 cuadrantes col-0, friction entero,
  non-integer rechazado, malformado col-0. Suite maker 17/17.
- Escape hunt: NINGUN escape nuevo de indentacion produce pase silencioso. Probe tabs, indent
  mixto, dash sobre-indentado, header-sin-dash, dash/blank/field, deep-dash, same-indent.

Residuales benignos declarados (no bloquean): R1 = un 2o item OVER-indentado se fusiona (last-wins)
en el item previo en vez de abrir item nuevo; NO forja pase de campo-faltante (el item fusionado
sigue exigiendo los 4 campos validos) y no hay regla friction==len(obstacles). R2 = header
`obstacles:` sin guion ni [] se lee vacio; PREEXISTENTE (identico en b6fa2b1), benigno para
friction 0, correctamente rojo para friction>0. No es regresion.

Gates HEAD: validate 0, protocol_replay --check-drift CLEAN up_to_seq=5983 (drift 0), scan_encoding
0, scan_domain_neutrality 0.

LECCION reutilizable: para un fix de parser, clonar TAMBIEN el padre y correr el MISMO vector en
ambos -- probar que el before realmente estaba roto (exit distinto), no solo que el after pasa;
asi el "cierre por comportamiento" es falsable, no un test que siempre paso. Y cazar el escape en
la DIRECCION peligrosa (malformado leido como vacio -> pase silencioso con friction 0), no solo el
happy-path.

Flip a done = del Arquitecto (yo checker-only). Mensaje GO: MSG-20260722-Analista-to-Arquitecto-
REVIEW-TASK-0261-remediation-1 (requires_response, response_owner Arquitecto).

## TASK-0266 remediacion iter1 (E5 evidence integrity) -- OK-CLOSABLE / GO (2026-07-23, commit 9cb7a64)

Re-juicio del CHANGE-REQUIRED que yo levante (prueba negativa E5 probaba lo INCORRECTO: crash
incidental de check_commit_trailers.py sobre TASK_INDEX.json roto, no un gate de estado gobernado).
Impl bajo revision: 14d7150. HEAD protocolo e5beefa. Sin producto.

Verificado POR COMPORTAMIENTO en instancia fresca (/d/ccv266r1inst, generada con new_instance.py
desde clon limpio /d/ccv266r1 @ 14d7150), con MIS payloads, no confiando en el test enviado:
- PARTIAL (default): rompo CLAIMS.json -> {broken, trailer VALIDO -> commit ACEPTA (exit 0), el
  estado roto ATERRIZA en HEAD. prune_state crashea pero el hook imprime "pruning is due; local
  commit continues" y sigue. => residual E6-A confirmado (partial no hard-rechaza).
- FULL (HOOK_FULL=1): mismo CLAIMS.json roto -> RECHAZA (exit 1) via validate_collaboration_state
  ("collaboration state in staged snapshot is invalid; commit rejected" + "Invalid JSON: ...CLAIMS.json"),
  SIN check_commit_trailers.py en la salida. HEAD sin cambiar.
- PROBE EXTRA mia: violacion SEMANTICA (JSON valido, row selector en ruta no soportada) tambien
  rechazada en full mode -> el gate cableado es el VALIDADOR REAL, no un parse-only.
Origen de diagnosticos confirmado en codigo: .githooks/pre-commit:118 y
scripts/validate_collaboration_state.py:153. Trailer valido => pre-commit rechaza ANTES del commit-msg.

No-regresion: diff 14d7150 = runner + handoff + estado de turno. .githooks/pre-commit, commit-msg,
protocol.config.json, protocol.config.template.json VACIOS en el diff. upgrade_instance.py,
new_instance.py, runtime/vcs.py NO aparecen (E4/E5/H1 intactos). Handoff agrega seccion "Residual E6-A".
Gates clon limpio 14d7150: runner exit 0 (8 + ps1 parity), validate/scan_encoding/scan_domain_neutrality 0.

Residual R-1 (NO bloqueante): el runner asserta "Area_comun\state\CLAIMS.json" (backslash Windows);
el validador imprime {path} con str(Path) (forward slash en POSIX) => en instancia POSIX el substring
false-fallaria aunque el gate dispare igual. El GATE es portable, solo el assert no. Sugerido follow-up
opcional agnostico al separador. No gatea el cierre en este harness Windows.

Veredicto: artefacto Area_comun/artifacts/Analista-TASK-0266-remediation1-e5-integrity-verdict.md +
mensaje MSG-20260723-Analista-to-Arquitecto-VERDICT-TASK-0266-remediation-1 (requires_response,
response_owner Arquitecto). Flip a done = del Arquitecto (yo checker-only). Prune due (released_ratio
92.31) es checkpoint del Arquitecto, NO lo toco.

LECCION: cuando el CHANGE-REQUIRED era "el test prueba lo incorrecto", re-correr MI PROPIA
falsificacion con la variante que el maker dice haber arreglado (CLAIMS.json, no leido por el
trailer-checker) Y anadir una variante ORTOGONAL (violacion semantica) para probar que el gate
full-mode es el validador real, no un happy-path de un solo string. Cazar tambien residuales de
PORTABILIDAD del test (separadores de ruta OS-dependientes) que no rompen el gate pero si el golden
case en otras plataformas.

## 2026-07-24 03:35 -- TASK-0256 (espejo DECISION-0099 en export born-operational): CHANGE-REQUIRED (NO-GO)

Commit veredicto: 906c96f (artefacto Area_comun/artifacts/Analista-TASK-0256-roster-policy-born-operational-verdict.md
+ MSG-20260724-Analista-to-Arquitecto-REVIEW-TASK-0256). Clon limpio /d/ccv0256 sobre origin/main 3b72609
(impl Codex 8168fae). Sin producto en alcance.

Cambio: AGENTS.template.md +14/-0, bloque "Roster policy" (3 reglas de 0099) en la seccion 3, tras la
tabla de roles. new_instance.py sin cambios (ya materializa el template).

Lo verde (por ENTRYPOINT REAL, 4 generaciones): new_instance --tier coordination / runtime /
attested(--roster propio) / attested(POR DEFECTO) -> exit 0 las 4; en las 4 el AGENTS generado da
grep "Roster policy"=1 y las 3 reglas exit 0, 0 placeholders sin sustituir, 0 bytes >127. La instancia
recien nacida pasa SUS gates (validate/encoding/neutralidad 0 en 3 raices). Hub en clon: validate 0,
neutralidad 0, encoding 0, protocol_replay --check-drift 0 (CLEAN up_to_seq=6316). Suites que el +14
podia romper: test_attested_instancing.py 0 y run_runtime_instantiation_cases.py 0. Diff fuera de
ledger/mailbox/tasks = exactamente AGENTS.template.md 14/0. No existe new_instance.ps1 (entrypoint unico).

SLIP-1 (bloqueante): el texto exportado define "worker agent" = ejecutor de codigo subordinado que
NUNCA ratifica, y el mismo new_instance.py escribe por defecto tier:"worker" para el human_owner en
agent_registry/attested_instancing.roster (new_instance.py:519; enum de tier {signer,worker} en :534,
distincion de POSESION DE LLAVE). En el AGENTS generado attested: linea 60 = "Human owner | Approves
project policy, critical transitions"; linea 64 = worker agents nunca ratifican. Tras 8168fae ese bloque
es la UNICA definicion normativa de "worker" que una instancia nace conteniendo, y es falsa para esa
entrada. Fix minimo = 1 clausula acotando el sujeto de la regla 1. Bucle declarado max 2 iteraciones.

Residuales: RES-1 examples/generated_minimal_instance/AGENTS.md sin la politica (CI no lo regenera);
RES-2 upgrade_instance.py propaga el TEMPLATE, no re-materializa el AGENTS vivo de instancias existentes;
RES-3 el espejo omite la razon anti-rubber-stamp de la regla 3; RES-4 "strong-capability" auto-declarable
(enforcement fuera de alcance por intake).

LECCIONES:
1. Cuando el entregable ES TEXTO NORMATIVO exportado, no basta con grep de que las reglas llegan:
   hay que leer el artefacto GENERADO junto a su PROPIA config y buscar colisiones de vocabulario. El
   defecto aparecio solo al generar la instancia attested POR DEFECTO y abrir su protocol.config.json.
2. Probar la FAMILIA de tiers, no el ejemplo dado: el maker verifico un solo tier; el defecto vive en
   attested (el tier al que apunta el export born-operational).
3. Falsificar el gate de neutralidad antes de creerle: inyectar un termino de dominio en el archivo
   modificado dentro del clon (exit 1, linea nombrada) y restaurar (exit 0, git status limpio). Sin eso,
   "neutralidad verde" puede ser un verde vacio por no cubrir el archivo.
4. Buscar suites golden que el diff pueda romper (test_attested_instancing, runtime_instantiation_cases)
   aunque el maker no las mencione, y artefactos generados versionados que quedan stale (RES-1).

---

## 2026-07-24 04:13 -- TASK-0256 RE-JUICIO iter1: OK-CLOSABLE (GO). SLIP-1 CERRADO

Commit del veredicto: `a5bb7fe` (origin/main). Ancla: clon limpio `/d/ccv256r1` @ **356ac5d**
(la instruccion citaba 0802ffa; ancle en el HEAD real, mas conservador, tras probar que el diff
no-ledger 377bb20..356ac5d es exactamente `AGENTS.template.md` 3/0). Remediacion: `26995a6` (Codex),
mi OPCION B: 2 lineas de aclaracion + blanco antes de la lista "Roster policy".

Evidencia: 6/6 gates de protocolo exit 0 (validate, scan_encoding, scan_domain_neutrality,
protocol_replay --check-drift CLEAN up_to_seq=6334, test_attested_instancing,
run_runtime_instantiation_cases); `new_instance.py` exit 0 en los 3 tiers con roster POR DEFECTO;
9/9 gates de las instancias recien nacidas exit 0; aclaracion + 3 reglas + `maker != checker` en los 3
AGENTS generados; 0 placeholders, 0 bytes >127; la aclaracion PRECEDE a la regla 1 (linea 64 vs 67);
neutralidad FALSABLE sobre la linea nueva (inyeccion -> exit 1 en `AGENTS.template.md:61`; restaurado -> 0).

Residuales NUEVOS: RES-5 sub-captura ("that execute code" podria sacar del alcance a un checker que solo
lee; no bloqueo porque las reglas 2/3 son categoricas y porque la redaccion es la que YO propuse);
RES-6 **correccion de mi propio veredicto anterior**; RES-7 coordination/runtime no tienen
`agent_registry`, asi que la aclaracion referencia unos tiers inexistentes en esas instancias (inocuo).

LECCIONES nuevas de esta iteracion:
5. **Verificar que el fix no reescribio lo que decia dejar intacto.** No basta el grep de que las reglas
   siguen ahi: extraje el bloque en el commit PRE y POST y diffee tras retirar SOLO las lineas nuevas ->
   vacio (exit 0). Un grep positivo convive con una regla reescrita a medias.
6. **Buscar mirrors huerfanos del texto remediado.** Si la politica estuviera copiada en otro archivo de
   la instancia, la aclaracion no viajaria con ella y el SLIP seguiria vivo por otra puerta. Verifique
   que la frase de la regla 1 aparece 1 sola vez en TODA la instancia generada, en el mismo bloque.
7. **El orden importa en texto normativo.** Comprobe por numero de linea que la aclaracion PRECEDE a la
   regla en el artefacto GENERADO (no solo en el template): una exencion que llega despues no evita la
   primera lectura contradictoria.
8. **Auditar mi propio veredicto anterior y corregirlo en el registro (RES-6).** Habia afirmado que el
   bloque anadido era la UNICA definicion de "worker" que una instancia nace conteniendo; falso:
   `skills/delegate-to-worker.skill.md` (SPEC-0110/TASK-0216, preexistente) se materializa en los 3
   tiers. No cambiaba el SLIP, pero la afirmacion estaba sobredimensionada. El checker tambien se audita.
9. **No convertir mi propia redaccion propuesta en un segundo NO-GO.** RES-5 es un defecto real de
   alcance, pero el maker aplico casi literal lo que yo pedi; se declara como residual con polish
   sugerido ("This policy governs the agent participants of the roster"), no como bloqueo. El tope de
   2 iteraciones se respeta y se declara consumido/resuelto.

---

## 2026-07-26 23:04 -- TASK-0296 REVIEW iter1: CHANGE-REQUIRED (NO-GO). B1 = quoting del instalador

Commit del veredicto: `e5fbfa7` (origin/main). Ancla: clon limpio
`D:/Aegis_Scratch/multi_agent_project_protocol/an0296` @ **c71c294** (impl `36269a3`; el diff sobre
`scripts/ examples/ Area_comun/protocol/` entre ambos es vacio). Alcance SOLO protocolo. Banco propio
de 52 vectores (`an0296adv/adversarial_0296.py`) + **segundo clon `an0296old` @ 3aa332d** como baseline
de no-regresion contra el detector pre-0296. Fixtures en `an0296fx`, `an0296fxsuite`. Cero artefactos
fuera del scratch root (DECISION-0104).

Resultado: 51/52 PASS. R1-R4 de mi veredicto de 0295 cerrados POR COMPORTAMIENTO, incluida la prueba
en la maquina real (read-only): monitor con `--scan-root D:/ --max-depth 2` + hogares canonicos
allowlisted -> exit 1 cazando `D:\Agentes\runtime-test-instance`, el stray que 0295 no veia.

**BLOQUEO B1:** `install_scratch_discipline_monitor.ps1:21` envuelve cada argumento en comillas
escapando solo las comillas internas. Bajo `CommandLineToArgvW` una **barra invertida final escapa la
comilla de cierre**, y PowerShell la anade al completar un directorio con TAB. La tarea programada que
queda registrada pierde en silencio `--known-repo` (falso negativo sobre la clase primaria de
DECISION-0104), `--max-depth` (regresion R1), `--allow-home` (regresion R2) y `--json`; y sigue saliendo
exit 1 con `ACTION REQUIRED`, indistinguible de una corrida sana. El `-WhatIf` que el entregable ofrece
como verificacion NO imprime la cadena de argumentos: la verificacion documentada es ciega al defecto.

7 residuales declarados (RES-1 falsos positivos del canal de warning porque `git config --get-regexp`
sale 1 cuando NO hay coincidencia -> avisa sobre repos sanos sin remotes, medido 3/3 en la maquina real;
RES-2 fail-open sigue con exit 0 y el runbook rutea solo "any nonzero exit"; RES-3 sin `--known-repo` no
hay warning; RES-4 contencion del allowlist; RES-5 cwd del monitor = raiz del repo; RES-6 `-Force`;
RES-7 descenso en `.git/`).

LECCIONES nuevas:
10. **Probar el artefacto de INSTALACION, no solo el ejecutable.** El detector estaba impecable; el
    defecto vivia en como el instalador COMPONE la linea de comando de la tarea. Un enforcement se
    juzga por lo que queda instalado, no por lo que corre a mano en la terminal del checker.
11. **Buscar el gesto de operador mas probable, no el mas raro.** El disparador no es una ruta rara:
    es la que PowerShell escribe sola al tab-completar un directorio. Un defecto que se activa con el
    gesto por defecto es un bloqueo; el mismo defecto tras una entrada exotica seria un residual.
12. **Un fallo que conserva el exit code correcto es peor que uno ruidoso.** La tarea corrupta seguia
    saliendo 1 con ACTION REQUIRED. Cuando midas un mecanismo de alerta, comprueba tambien que un
    mecanismo MAL CONFIGURADO se distinga de uno sano.
13. **Comprobar que la verificacion que el maker ofrece puede ver el defecto.** `-WhatIf` era la unica
    verificacion documentada y no imprime los argumentos: afordancia de verificacion ciega.
14. **Correr el entregable contra la maquina REAL en seco cuando es read-only.** Fue la evidencia mas
    fuerte de que los teeth muerden (stray real cazado) y la que destapo RES-1 (3 warnings espurios
    sobre repos sin remotes) -- ninguna suite sintetica los habria mostrado.
15. **Baseline de no-regresion = segundo clon en el commit anterior.** Comparar el set de hallazgos del
    detector nuevo (default) contra el viejo sobre el MISMO fixture prueba "sin regresion" por
    comportamiento, no por lectura del diff.
16. **Huella de metadatos, no solo de contenido.** La suite del maker hashea contenido; yo anado
    `st_mtime_ns`+`st_size` de todo nodo incluido `.git/**` -- descarta escrituras que no cambian bytes.

Hook al commitear: `PRUNE DUE (released_ratio 92.31 >= 90)` -- accion del Arquitecto en su proximo
checkpoint (`python scripts/prune_state.py --root . --apply`), no mia. Lo dejo senalado.

## 2026-07-27 -- TASK-0296 RE-REVIEW iter 1 (remediacion del argv): NO-GO, segundo NO-GO -> escala

Ancla `833e57e` (fix `31680dd`), delta hasta `origin/main` `8f93429` = solo el MSG. Clon limpio
`D:/Aegis_Scratch/multi_agent_project_protocol/an96r1`; baseline pre-fix `.../an96pre` en `c71c294`.
Veredicto: `Area_comun/artifacts/Analista-TASK-0296-argv-remediation-iter1-verdict.md`; mensaje
`MSG-20260727-Analista-to-Arquitecto-REREVIEW-TASK-0296-iter1.md`. Commit `d593eed` (pusheado).

**B1 CERRADO** (ruta con separador final -> argv integro, mismo set de hallazgos) y puntos 2/3/4
entregados. Gates verdes: suite 0, validate 0, encoding 0, neutralidad 0, drift CLEAN, config
`2E35F26E` intacto, 0 API mutante, `-WhatIf` no registra.

**BLOQUEO NUEVO B2 (introducido por la remediacion):** el `TrimEnd([char[]]"\/")` destruye la raiz de
volumen. `'D:\'.TrimEnd('\','/')` = `'D:'`, y `Path('D:').resolve()` es el **cwd de esa unidad**, no
la raiz. La tarea corre con `WorkingDirectory = raiz del repo` y el monitor lanza el scanner con
`cwd = raiz del repo` -> la tarea escanea la raiz del repo y reporta `exit 0` + `OK: no
scratch-discipline anomalies found.` para siempre, en silencio. Medido end-to-end (CreateProcess con
la cadena cruda, como el Task Scheduler): pre-fix `-ScanRoot 'D:/'` -> exit 1 + `ANOMALY
D:\Agentes\runtime-test-instance`; fix -> exit 0 sin hallazgos. **Regresion**: `D:/` funcionaba en
`c71c294`.

LECCIONES nuevas:
17. **Una remediacion es una entrega nueva: hay que atacarla, no solo comprobar que cierra el
    bloqueo anterior.** B1 cerro perfecto; el NO-GO vino del cinturon adicional. Verificar "el fix
    arregla X" es la mitad del trabajo; la otra es "que rompio el fix".
18. **Cuidado con las sugerencias propias del veredicto anterior.** El `TrimEnd` lo propuse yo en
    iter 0. Un checker no puede tratar su propia recomendacion como verificada: hay que juzgarla con
    la misma hostilidad que el resto. Retirarla en voz alta cuando resulta ser la causa raiz.
19. **`TrimEnd`/`rstrip` de separadores NO es normalizar en Windows: `X:\` -> `X:` cambia la
    semantica** de raiz absoluta a ruta relativa a la unidad (silenciosa, resuelve contra el cwd por
    unidad). Patron a buscar siempre que alguien "limpie" rutas.
20. **Un test de round-trip que calcula su expectativa con la MISMA transformacion que prueba es
    tautologico.** El caso nuevo hace `intended = arg.rstrip("\/")`, o sea asume el recorte como la
    intencion: pasa EN VERDE sobre una raiz de volumen rota. La expectativa debe ser **lo que el
    operador pidio**, no lo que el codigo hizo.
21. **Antes de aceptar un cinturon adicional, comprobar si hace falta.** Extraje el bloque de escape
    real del instalador y lo aplique a un array SIN recortar: round-trip exacto, incluida `D:\` y una
    ruta con espacio. El quoting corregido por si solo cierra B1 -> el TrimEnd solo aportaba B2.
22. **Simular el disparador real (Task Scheduler = Execute + Arguments + WorkingDirectory)** pasando
    la cadena CRUDA a `CreateProcess` (`subprocess.run(str, cwd=...)`): prueba la cadena entera, no
    solo el parseo con `CommandLineToArgvW`.

Loop declarado agotado (iter 1 de max 2 con re-juicio NO-GO) -> **escalado al operador humano** por
via del Arquitecto. Contexto justo dado: B1 si cerro, B2 es defecto nuevo, y el fix es suprimir cuatro
llamadas mas anadir un vector de raiz de volumen al test.

Hook al commitear: `PRUNE DUE (cold_start_tokens 23866 >= 20000; released_ratio 93.33 >= 90)` --
accion del Arquitecto en su proximo checkpoint, no mia. Senalado otra vez.

## 2026-07-27 -- TASK-0296 RE-REVIEW iter 2 (retirada del TrimEnd): GO / OK-CLOSABLE

Ancla `12b8d77` (cita del Arquitecto `94cdb27`, fix `9691312`); `git diff 94cdb27 12b8d77 -- scripts/
examples/ Area_comun/protocol/ runtime/ protocol.config.json` = vacio, asi que juzgue sobre
`12b8d77`. Clon limpio `D:/Aegis_Scratch/multi_agent_project_protocol/an96i2` (+ `an96bank`,
`an96neg`, `an96base`, fixtures `an96fx2/an96fx3/an96negfx`, todos borrados al terminar).
Veredicto: `Area_comun/artifacts/Analista-TASK-0296-volume-root-iter2-verdict.md`; mensaje
`MSG-20260727-Analista-to-Arquitecto-REREVIEW-TASK-0296-iter2.md`. Commit `d93b897` (pusheado).

**B2 CERRADO por comportamiento.** Sin los 4 `.TrimEnd`, `-ScanRoot 'D:/'` -> `--scan-root D:/` y
`'D:\'` -> `--scan-root D:\`; ambas resuelven `D:\` y la linea compuesta ejecutada como la ejecutaria
el Task Scheduler (`CreateProcess` con la cadena cruda, `cwd` = raiz del repo) escanea el DISCO:
exit 1 con las 2 violaciones reales de 0104 de esta maquina, identico a la invocacion directa.
**B1 no reabierto y ademas MEJOR que en iter 1**: el valor llega verbatim (`...\vol\` con el
separador final) en vez de recortado, 12 tokens 3/3 flags, incluido `-AllowHome 'D:\home dir\'`
(espacio + backslash). **Cero B3** en 21 vectores / 14 payloads de quoting (UNC, 3 backslashes,
comilla embebida, backslashes-antes-de-comilla, solo-separadores, `D:sub`, array nativo de 2 raices).
Gates: suite 0 (estable 3/3, 3-4 s, 0 residuos), validate 0, encoding 0, neutralidad 0, drift CLEAN
`up_to_seq=6450`, config `2E35F26E` intacto.

**Residuales declarados no bloqueantes:** RES-1 el designador de unidad pelado `D:` sigue siendo
relativo a la unidad (`--scan-root D:` con cwd = repo -> exit 0 "OK: no anomalies" con el disco
sucio); no bloquea porque `D:` NO es una raiz de volumen (`Path('D:').is_absolute()` es False), el
instalador ahora hace pass-through fiel y el runbook documenta `--scan-root <host-root>`; pero el
test ENTREGADO fija esa conducta (`ROOT.drive` en el bucle de variantes; `endswith(':')` solo sobre
`volume_root`), asi que el endurecimiento natural exigira actualizar el test junto al guard. RES-2
el escape de comilla embebida no lo cubre la suite (mutante sobrevive) aunque funciona. RES-3 la
asercion de equivalencia (lineas 145-156) es casi tautologica y escanea el volumen del host DOS
veces comparando stdout/stderr byte a byte -> flake si el disco cambia entre corridas, y rompe la
host-independencia de un `examples/`. RES-4 `endswith(':')` en la linea 143 es codigo muerto.

LECCIONES nuevas:
21. **La falsabilidad de un test se PRUEBA mutando el fix, no leyendo el test.** Monte 5 mutantes
    sobre un esqueleto ligero (solo `scripts/` + `examples/<caso>/`, 32 KB, sin `.git`) y corri la
    suite entregada contra cada uno. El decisivo fue N3 = **revert COMPLETO a iter 1** (TrimEnd Y
    `rstrip` de vuelta en la expectativa): murio con `installer changed volume-root vector: 'D:' !=
    'D:/'`. Ese es exactamente el camino por el que B2 paso en verde la primera vez. Un mutante que
    SOBREVIVE (N5, escape de comilla) es un residual de cobertura, no necesariamente un defecto:
    hay que distinguir "no cubierto" de "no funciona" comprobando el comportamiento aparte.
22. **NUNCA meter rutas Windows en un heredoc de Bash.** `python - <<'PYEOF'` con `"D:\...\fixture\vol\\"`
    llego a Python con backslashes simples -> `\f` y `\v` se volvieron form-feed y vertical-tab, el
    argv se corrompio y el harness reporto un falso B1 REABIERTO de 4 tokens sobre el codigo bueno
    (y tambien sobre el de iter 1). La pista fue `SyntaxWarning: invalid escape sequence '\A'`.
    Regla: los bancos con rutas van a **fichero real** con `Write` y `r"..."` / `chr(92)`, jamas por
    heredoc. Casi emito un tercer NO-GO por un artefacto de mi propio harness.
23. **Distinguir "la herramienta corrompe una entrada valida" de "la entrada no es lo que promete".**
    B2 era lo primero (destruia `D:/`) = bloqueante. El `D:` pelado es lo segundo (pass-through fiel
    de una ruta relativa a la unidad) = residual, preexistente en toda la historia de la unidad y
    fuera de la grafia que documenta el runbook. El criterio del Arquitecto listaba las tres grafias
    juntas; lo dije en voz alta en vez de rubber-stamp, sin convertirlo en bloqueo.
24. **Si el fix retira un "cinturon", verificar que lo de abajo aguanta solo.** Retirar el `TrimEnd`
    solo era seguro porque el scanner ya normaliza separadores finales por su cuenta (`_resolved()`
    en scan/scratch/allow-home, `rstrip` y `urlparse().path.rstrip('/')` en `_repo_identity`). Lo
    verifique EJECUTANDO con separador final en los cuatro parametros, no leyendo el fuente.

Gotchas operativas de esta sesion: (a) `cp -r` de un clon del repo son ~3.7 GB y se come el turno --
esqueleto minimo para mutar; (b) `git commit -F /tmp/f.txt` tras un `&&` que fallo reutilizo un
`/tmp/f.txt` VIEJO y commiteo con mensaje ajeno ("break governed with valid trailer") -> amend, y en
adelante el mensaje de commit se escribe con `Write` al scratchpad, nunca a `/tmp` compartido.
Hook al commitear: `PRUNE DUE (cold_start_tokens 27814 >= 20000; released_ratio 94.12 >= 90)` --
accion del Arquitecto en su proximo checkpoint, no mia. Lo dejo senalado.

---

## TASK-0299 (2026-07-28) - bridge observa la sesion INTERACTIVA via transcript jsonl - GO / OK-CLOSABLE

Veredicto: **OK-CLOSABLE (GO)**, iter 1, 0 slips. Commit `2cc21b2` en el hub (02c99a5 -> 2cc21b2).
Ancla producto Zeus@`7729c4f` (== origin/main). Suite lenta exit 0: 138/120/18. Fast-follow de 0298
que cierra su riesgo E1 (el bridge solo veia el modo cron). Segunda fuente = `session-transcript`.

Lecciones/tecnica de este review:
1. **AC4 era la misma clase que el B1 de 0298 (PII partida entre escrituras incrementales).** La
   defensa real: `pollTranscript` bufferiza bytes incompletos en `pending` hasta el ultimo `0x0a` y
   SOLO publica lineas completas; `redactPublicText` corre sobre el cuerpo REENSAMBLADO antes de SSE
   y audit. Lo verifique con el test dado (correo partido `exa|mple.com` en dos appendFile+60ms) y
   ademas probando la FAMILIA completa (email/NIT/cedula/telefono/cuenta/SQL) con payloads propios,
   extrayendo `redactPublicText` a un `.mjs` desechable.
2. **Insight clave sobre el framing incremental:** partir una linea jsonl a la mitad NUNCA fuga en
   claro porque el fragmento es JSON invalido -> `JSON.parse` falla -> se descarta (PERDIDA, no fuga).
   O sea, el valor de seguridad del buffer es "no corromper/perder entradas partidas"; el no-fuga lo
   garantiza (a) procesar solo lineas JSON completas y (b) la redaccion. Por eso el mutante que
   revierte el buffer NO produce una fuga limpia sino un HANG: la entrada partida se pierde, el 3er
   evento redactado nunca llega, y `readSseEvents(...,3)` se cuelga dentro de `await reader.read()`
   pasando su deadline de 5s -> lo capture como SIGKILL/exit 137 con `timeout --signal=KILL 75`.
3. **Los 4 mutantes de Codex MUEREN re-inyectados** (copia desechable, `--test-name-pattern`, restaurar
   con `diff -q` vs backup): (1) desempate `localeCompare` invertido -> deterministic fail; (2)
   `isRelevantTranscriptEntry -> true` -> ruido surface, fail; (3a) quitar `redactPublicText` -> FUGA
   VISIBLE en el SSE (`persona@example.com` en claro), fail exit 1; (3b) anular buffer -> hang/137;
   (4) match cwd+branch siempre-true -> `'alive' !== 'dormant'`, fail.
4. **Los 18 skips son ambientales, no control.** Todos = guard `cloneProtocolFixture`
   (`tests/staticContract.test.js:3517-3524`) por fixture externo `event_auth` ausente en clon
   limpio. Verifique el motivo unico + que ninguno es un test de 0299 + que los 2 tests de 0299
   CORREN (no estan entre los skips). No confiar en el conteo reportado: recontarlo.
5. **Residuos declarados (best-effort del AC4, NO bloqueantes, dichos en voz alta):** nombres propios
   en texto libre (`Juan Perez`) no se redactan; ids numericos cortos sin etiqueta (`codigo 482913`)
   tampoco; y los campos metadata `role`/`entryType`/`entryTimestamp` pasan por `ascii(stripControl)`
   pero NO por `redactPublicText` (ni en SSE ni en el sanitizador de audit :1543) -- son enums
   estructurales, no PII, el CUERPO si se redacta. Honesto, no rubber-stamp, no bloqueo.
6. **Gates del hub:** validate/encoding/neutralidad exit 0; `git diff --exit-code -- protocol.config.json`
   exit 0 (fondo 2E35F26E / epoch 1.14.0 intocable; 0299 es commit de Zeus, no toca el hub).
7. **Trailer gate del hook:** `Task-Id` + `Ops-Reason` deben ir en el MISMO bloque final SIN linea en
   blanco entre ellos. Con `git commit -m` separados quedan en paragrafos distintos y el gate rechaza
   ("missing exact final trailer"). Fix: un solo `-m "Task-Id: TASK-0299\nOps-Reason: ..."` con newline
   literal (no doble). Ademas los untracked hay que `git add`-earlos ANTES de commitear con pathspec
   (si no: "pathspec did not match any file(s) known to git").
8. **PRUNE DUE** al commitear (released_ratio 92.31 >= 90): warning, el commit local continua; es
   accion del Arquitecto en su checkpoint (mailbox_archive/prune exige capability orchestrator que yo
   no tengo). Lo dejo senalado, no lo corro.

## 2026-08-02 -- TASK-0310 CAMBIO-REQUERIDO (consola prompt operador->agente, front Zeus-protocol)
Veredicto commit 67986ed (artifact + MSG a Arquitecto). Producto @767f41f, hub @d7ce511.
- SEGURIDAD (foco de la review) = VERDE en recompute independiente: builder server-side real
  (assertAllowedKeys top-level 5 campos + agentPrompt 5 -> rechaza from/actor/relayed_by/endorsement/
  author/actorId/intents 400), atribucion pineada server (from Operador/relayed_by Arquitecto hardcode/
  endorsement none), destino {Arquitecto,Codex,Analista}, messageType REQUEST/QUESTION, off-by-default
  403 (dry_run+execute), persistencia 503, confirm 409, relay-mismatch fail-safe 500, redaccion PII
  server-side ante ataque directo, YAML-injection neutralizada por stripControl. Probe propio 27/27 PASS.
- SLIP-1 (CONFIRMED, gatea cierre): AC4 "el MSG compuesto pasa validate" FALLA para requires_response:true.
  Metodo decisivo: extraer el MSG del endpoint (dry_run = byte-identico a execute, server.js:1103-1116 sin
  post-proceso) y pasarlo por la FUNCION validate_mailbox del HEAD citado EN AISLAMIENTO (rapido, sin el
  replay lento de 3 min ni los secretos event_auth). Resultado: QUESTION+rr -> falta requested_action
  (validator linea 1188 incondicional); REQUEST+rr -> falta question (linea 1193, compact porque siempre
  hay one_line_summary). Solo REQUEST+requires_response:false pasa. Ruta UI (app.js:1276) casilla marcada
  = QUESTION+rr = FALLA. El unico test que lo cubria (slow mailbox_send execute) esta SKIPPED por faltar
  secretos event_auth -> el hueco de cobertura coincide con el defecto; AC4 nunca se ejercio.
- LECCION reutilizable: cuando un gate lento (validate con chain-replay) o env-guarded (secretos fuera del
  repo) bloquea la reproduccion, EXTRAER la funcion-guarda del HEAD citado y alimentarla con el output REAL
  del builder es el camino de recompute mas decisivo. No confiar en test names ni en "test:slow exit 0" si
  el test clave esta entre los skips.
- LECCION: mi propio MSG requires_response:true DEBE llevar requested_action + question + response_owner +
  one_line_summary + context_refs para pasar el mismo validador (dogfooding del fix que pido).
- Fix pedido a Codex: buildMailboxSendMarkdown emite AMBOS requested_action y question si requires_response;
  + test rapido sin secretos que pase la salida por validate_mailbox en las 4 combinaciones. Re-juicio
  Analista, max 2 iteraciones antes de escalar. Clon limpio en D:/Aegis_Scratch/zp0310 (DECISION-0104).

## 2026-08-02 -- TASK-0310 r2 OK-CERRABLE (cierre del bucle de fix, iteracion 2/2)
Veredicto commit 95f2722 (artifact Analista-TASK-0310-r2-slip1-verdict.md + MSG REVIEW a Arquitecto).
Producto @826be23 (padre 767f41f), hub @42d9bcd, config 2e35f26e pineado, drift 0.
- SLIP-1 CERRADO. El fix (diff 767f41f..826be23, 6 lineas de src) confina a buildMailboxSendMarkdown:
  para requires_response:true emite INCONDICIONALMENTE response_owner + requested_action + question.
- Metodo decisivo (reutilizable): reconstrui la salida EXACTA del builder VIEJO y NUEVO y las pase por la
  FUNCION validate_mailbox del hub en aislamiento -> NUEVA 0 errores / VIEJA 767f41f 3 errores en las 4
  combinaciones. Detalle clave: sanitizeAgentPrompt FUERZA requires_response=true si messageType=QUESTION
  (server.js:1143), asi que 3 de las 4 combos son rr:true internamente. Drive directo del validador =
  espejo del recompute de r1, mas decisivo que confiar en el test.
- Test 4-combos MEANINGFUL comprobado por superposicion: overlay SOLO el test nuevo (826be23) sobre el src
  VIEJO (767f41f) en clon limpio -> el test FALLA (AssertionError, MSG QUESTION sin requested_action);
  sobre src nuevo -> PASA. Confirma que el hueco se cierra en la CAPA DEL VALIDADOR, no solo en el regex.
  OJO: en la "rejects impersonation" test el regex de linea 1071 dispara ANTES que el assert del validador
  (linea 1120); por eso corri el drive directo del validador aparte para probar el gate real.
- Sin regresion de seguridad: diff de 6 lineas no toca las guardas; los 2 tests TASK-0310 PASS @826be23
  (impersonacion: cliente from/actor/relayed_by/raw/destino-ajeno/execute-sin-confirm rechazados; off-by-
  default 403). Fondo #4 intocado. npm test clon limpio (D:/Aegis_Scratch/z310) exit 0 (140/118/22/0).
- El fix coincidio EXACTO con lo que prescribi en r1 -> bucle de fix limpio, 1 iteracion, sin nuevo slip.
- Residuales no bloqueantes: R1 question==requested_action (contrato compact lo exige, validador solo mira
  presencia); R2 test acoplado al hub via PROTOCOL_REPO_PATH + shell-out python (caveat CI portable);
  R3 execute completo no reproducible por secretos event_auth; R4 UI sin veredicto visual (sin navegador).
- LECCION: cuando el test bajo revision tiene un assert de forma (regex del markdown) ANTES del assert del
  gate real (validador), correr el gate real por separado para no dar por bueno un "falla/pasa" que en
  realidad lo decide el assert cosmetico previo.

## 2026-08-02 -- TASK-0312 CHANGE-REQUIRED (supervisor idle-stop envenena el auto-revive)
Veredicto commit d025a4f (artifact Analista-TASK-0312-supervisor-event-driven-verdict.md + MSG REVIEW a
Arquitecto, requires_response). Producto Zeus-protocol @a51c099, hub HEAD 359943a->d025a4f, config
2E35F26E pineado, drift 0. npm test clon limpio (D:/Aegis_Scratch/Zp/r0312) exit 0 (142/122/20/0).
- GREEN: event-driven (watch(), sin setInterval de trabajo, solo setTimeout one-shot de idle; sin quema
  ociosa), sandbox/allowlist FIJO de 0107 (unknown 400, campo arbitrario 400 via assertAllowedKeys,
  shell:false + script fijo, uno-y-solo-uno), off-by-default (403), #4 hub byte-identico (solo 3 files de
  producto), backoff+maxRetries, reenable unlink .stop.
- DEFECTO PROBADO (harness real: server child + eventos fs): stopEntry escribe el MISMO marcador .stop
  persistente del stop del operador tanto en idle-threshold como en OFF (server.js:1712); el camino de
  auto-revive trata CUALQUIER .stop como bloqueo duro (server.js:1742 "blocked: operator-stop-marker") y
  el boton manual 0107 tambien (server.js:1643, 409). => tras el PRIMER sleep ocioso el supervisor NUNCA
  vuelve a levantar al agente ante trabajo encolado; solo un reenable HUMANO lo restaura. Rompe el bucle
  sleep<->revive (DECISION-0057 / AC1<->AC2) que es el proposito de la tarea. Mismo bug: OFF->AUTO tampoco
  auto-revive.
- Por que el test shipped lo pierde (tests/staticContract.test.js:1856): su runtime fixture nunca esta
  vivo (script ausente -> "start-failed: script unavailable"), asi que la escritura de .stop en idle NUNCA
  se alcanza y el .stop solo se prueba en el camino del operador. El ciclo AC1<->AC2 queda sin test.
- METODO decisivo (reutilizable): para probar un ciclo de estado que el test evita, monta el runtime VIVO
  de verdad (spawn sleeper + escribe su pid en pidPath -> status=alive porque runtimeControlState hace
  pid?alive:dormant), deja disparar el idle one-shot, verifica el .stop escrito, luego inyecta trabajo y
  lee las decisions del /api. taskkill del server puede no matar mi sleeper (artefacto del harness); lo
  mato yo para modelar fielmente el "runtime abajo" de produccion.
- Residual secundario declarado (no bloqueante): hung-but-alive no detectado (staleAfterMs/ageMs se
  computan pero nunca se usan; pid vivo + heartbeat congelado = "alive" -> "keep", nunca reinicia).
- Bucle de fix: remediar separando el fail-safe del operador del idle/OFF-park transitorio (no escribir el
  .stop persistente en park del supervisor, o limpiar en el revive un .stop AUTORADO por el supervisor
  distinguido por contenido) preservando AC4b; test nuevo del ciclo vivo completo. Max 2 iter, luego humano.

## 2026-08-02 -- TASK-0312 r2 CHANGE-REQUIRED (fix cierra el SLIP pero EXPONE un escape nuevo)
Veredicto commit 8f741b7 (artifact Analista-TASK-0312-supervisor-park-revive-r2-verdict.md + MSG REVIEW
a Arquitecto requires_response). Producto Zeus-protocol remediacion 97c359e (baseline a51c099), hub HEAD
74aad88->8f741b7, config 2E35F26E pineado, drift false. Clon limpio D:/Aegis_Scratch/Zp/r0312r2.
- r1 SLIP CERRADO (verificado en harness real): idle-park ya NO escribe .stop; parkIfIdle solo AUTO + sin
  trabajo encolado; stopEntry solo termina proceso + record (server.js:1715-1725). PHASE_A: idle-park sin
  .stop -> AUTO-REVIVE con pid fresco (55884->8764), sin reenable. OFF->AUTO revive. operator-stop-VIVO
  escribe .stop y bloquea hasta reenable (PHASE_C).
- npm test clon limpio 97c359e exit 0 (143/123/0/20). Test nuevo del ciclo vivo CORRE (no skip) y PASA.
  BASELINE NEGATIVO decisivo: overlay del test NUEVO sobre server VIEJO a51c099 -> FALLA exit 1 (no
  tautologico). Metodo reutilizable: `git show <fixcommit>:tests/file > tests/file` sobre clon del commit
  viejo para probar que el test discrimina pre/post-fix.
- ESCAPE NUEVO PROBADO (PHASE_B, harness real): operator STOP contra un agente YA idle-parked (dormant) es
  un no-op silencioso -> applyRuntimeControlAction early-return "already-dormant" SIN escribir .stop
  (server.js:1660-1661, antes del writeFile operator-front en 1664) -> inyecto trabajo -> el supervisor
  AUTO-REVIVE; ninguna decision "blocked". El stop soberano del operador NO pega. Causa: el bloqueo
  durable solo se arma en la rama live-kill; la rama "already-dormant" retorna ok sin armarlo. Pre-fix era
  inocuo (el idle-park ya dejaba .stop); la remediacion quito ese .stop y volvio el stop-on-parked un
  no-op. Dentro del blast radius del cambio bajo revision -> gatea el cierre (paridad con r1: la
  automatizacion no debe pisar la intencion del operador).
- Por que el test shipped lo pierde: solo hace operator-stop mientras el agente esta VIVO (revive primero,
  luego stop). Nunca stop-contra-parked -> analogo exacto de por que el test de r1 perdio el SLIP de r1.
- LECCION (family-not-example): cuando el fix cambia la SEMANTICA de un marcador compartido (aqui: quitar
  el .stop del idle-park), re-probar TODAS las ramas que dependian del efecto colateral, no solo el caso
  ejemplo del SLIP. El operator-stop tenia DOS ramas (alive / already-dormant) y el fix solo dejo durable
  la primera.
- Bucle de fix: operator STOP debe armar el bloqueo durable tambien en la rama already-dormant (escribir
  .stop sin depender de live-pid) preservando idle/OFF-park transitorio sin .stop; test nuevo
  operator-stop-WHILE-PARKED (queda blocked hasta reenable; falla @97c359e, pasa tras fix); no regresar el
  ciclo vivo r1. Remediacion-1 RECHAZADA -> 1 iteracion mas, luego escalar al humano.
- Nota estado: prune DUE (released_ratio 90>=90) -> lo corre el Arquitecto en su checkpoint coordinado, no
  el checker; CI es el borde duro. No lo toque.

## TASK-0312 r3 FINAL (2026-08-02 19:47 CEST) -- VEREDICTO: OK-CLOSABLE (167fd6f)
- Remediacion-2 producto ff02135 (Zeus-protocol, sobre 97c359e). CIERRA el escape PHASE_B que yo probe en r2:
  applyRuntimeControlAction ahora escribe .stop (mkdir+writeFile operator-front) ANTES del early-return
  dormant; la rama already-dormant retorna {action:"stopped", alreadyDormant:true} CON el marcador armado.
  server.js:1660-1664. Operator STOP contra parkeado -> queda blocked/operator-stop-marker hasta reenable.
- LAS 3 FASES verdes @ff02135 en clon limpio (D:/Aegis_Scratch/zeus/0312r3): PHASE_A idle-park->auto-revive
  (revivedPid!=initialPid), PHASE_B stop-while-parked->blocked, PHASE_C stop-while-alive->blocked. El test
  vivo (server real + child PowerShell real + fs markers reales) CORRE (no skip) y pasa 8.2s.
- BASELINE NEGATIVO decisivo (metodo reutilizable): clon @97c359e + `git checkout ff02135 -- tests/...` ->
  server VIEJO + test NUEVO -> `node --test --test-name-pattern` FALLA exit 1: alreadyDormant actual undefined
  vs expected true. El test discrimina pre/post-fix, no es tautologico.
- npm test full clon limpio exit 0: 143/123/0/20. Hub validate/encoding/neutrality exit 0; config sha
  2E35F26E...B354 byte-identico (drift nil); commit producto toca solo src/server.js (+6/-3) y tests (+10).
- 2 RESIDUALES NO-BLOQUEANTES declarados: (1) TOCTOU teorico stop-while-parked vs launch concurrente en el
  mismo evento -- NO es regresion (r1 no armaba marcador), el start re-chequea .stop, la durabilidad del
  marcador siempre se cumple, auto-sana a blocked en la siguiente ventana idle; no reproducible determinista.
  (2) reenable NO dispara evaluate -> revive en el proximo evento fs (funciona en la practica); comportamiento
  previo, no es stop-escape. Ambos fuera del alcance r3.
- ITERACION FINAL: veredicto OK-CLOSABLE ruteado al Arquitecto (MSG requires_response, requested_action=ratificar
  + flip a done; el checker NO cierra). Bucle de fix cerrado en 2 iteraciones (r2 CHANGE-REQUIRED -> r3 OK), sin
  escalar al humano.

## TASK-0313 r1 FINAL (2026-08-02 20:30 CEST) -- VEREDICTO: OK-CLOSABLE (93a4f93)
- Alcance: keyless product-worker BUILDER en el front Zeus-protocol (P4a / Nivel 1 de DECISION-0109 + SPEC-0115).
  Maker Codex, producto commit 8ba0155 (public/* + src/server.js +113/-1 + tests). Hub HEAD 35cf295, intacto.
- Clon limpio @8ba0155 en D:/Aegis_Scratch/z0313 (NO /d/ raiz; regla DECISION-0104). npm install + npm test
  exit 0: 144/124/0/20 (20 skips slow-tier). Coincide con el reporte del maker.
- HARNESS ADVERSARIAL PROPIO (adv_harness.mjs): server como subproceso contra roster temp, hub fingerprinted
  antes/despues. 59/59 PASS. Ejerci la FAMILIA por criterio, no el ejemplo dado:
  * off-by-default con env unset/"0"/"true"/"1x"/"" -> TODOS 403 en builder POST, GET y register (solo el "1"
    exacto habilita; ZEUS_PRODUCT_WORKER_BUILDER_ENABLED).
  * anti-injection AC2: top-level actor/signature/rawEntry/foreign + inner ledgerCapabilities/governanceAgent/
    signing/enabled/publicKeyPem/role/defaultEndpoint + __proto__ pollution -> TODOS 400, nada persiste. El
    server hard-codea signing.ledger=denied, ledgerCapabilities=[], governanceAgent=false. assertAllowedKeys
    (top ["mode","confirm","operation","worker","id"]) + sanitizeProductWorkerBuilderFields (worker
    ["id","provider","endpoint","model","capabilities","governanceRequested"]).
  * keyless AC3: persistido enabled=false, authority all-false, submitIntentEmitted=false; el path NUNCA llama
    submit_intent. publicProductWorker NO filtra publicKeyPem en el GET.
  * Nivel 2 AC5: governanceRequested=true SOLO graba governanceCeremony="pending"; governanceAgent sigue false;
    sin write a agent_registry ni signer set.
  * LLM AC4: create/edit-model/remove OK en extractors.runtime.json (fuera del config pinned); remove-unknown 404;
    ids traversal ../.. -> 400.
- Gates hub @35cf295: validate.py exit 0; protocol_replay --check-drift verdict=CLEAN up_to_seq=7013; gate.py 0;
  scan_encoding 0; scan_domain_neutrality 0. #4 byte-identico antes/despues (protocol.config 2E35F26E, events,
  snapshot). agent_registry vive DENTRO de protocol.config.json -> cubierto por su byte-identidad.
- 3 RESIDUALES NO-BLOQUEANTES: (1) el builder acepta cualquier endpoint HTTP(S) (el register fuerza loopback-only
  local-vlm); inerte aqui (keyless, enabled=false, no se ejecuta) pero el BORDE DE EJECUCION futuro debe
  re-validar loopback/allow-list (SSRF). (2) el builder no puede hacer vivo a un worker (siempre enabled=false,
  sin keypair en el path mutate) -> mas fuerte que los AC. (3) el marcador "pending" es display-only, nada actua.
- METODO reutilizable: para servidores que arrancan al import (server.listen top-level), spawnear `node src/server.js`
  con env que apunte el roster a temp + PORT propio, esperar "listening" en stdout, y batir la familia por fetch.
- Veredicto OK-CLOSABLE ruteado al Arquitecto (MSG requires_response, requested_action=ratificar+flip a done; el
  checker NO cierra). Sin CHANGE-REQUIRED, sin escalamiento.

## TASK-0316 r2 FINAL (2026-08-06 09:39 CEST) -- VEREDICTO: OK-CERRABLE (52d0a38, HEAD dccda71 -> mi commit b51bf72)
- Alcance HUB, sin producto. Remediacion r1 de mi CAMBIO-REQUERIDO de r1 (veredicto
  Analista-TASK-0316-neutralidad-cobertura-verdict.md). Mi veredicto r2:
  Area_comun/artifacts/Analista-TASK-0316-remediacion-r1-verdict.md.
- TRES CLONES, todos a 52d0a38, declarando cual corrio que, para no contaminarme:
  pr (pristino) = escaneres/test/contratos/encoding/validate/cobertura/TODAS las mutaciones;
  r1c = bateria de la base de memoria (build/drift/round-trip); r2c = el A/B controlado.
- F1 CERRADO. La prueba que yo mismo pedi en r1 punto 8: con el recorte AUSENTE el gate del repo sale
  exit 0 (en r1 salia exit 1 con 64). El verde se GANA, ya no se compra. Contabilidad 60+4=64 CUADRA:
  quitar las 2 entradas de LEGACY_IDENTITY_LITERAL_FILES da exit 1 con exactamente 60 (51
  test_memory_db.py + 9 peer_mailbox_cron.ps1). Los 4 defectos probados uno a uno (--retrieve sin
  --requested-by exit 2 y sin filtrar None por la rama query; CoordinatorId Mandatory no cuelga
  ningun cron porque los 2 invocadores vivos ya lo pasaban explicito).
- F2 CERRADO. M5 MATADO EN LAS DOS IMPLEMENTACIONES: reinsertar el recorte en el .py -> test exit 1;
  reinsertarlo SOLO en el .ps1 -> test exit 1 (lo caza test_powershell_scanner_...). El registro de
  falsacion NO es cosmetico: falsificar un boundary declarado o el exercised_by -> contracts exit 1.
- METODO NUEVO REUTILIZABLE -- A/B CONTROLADO SOBRE EL MISMO COMMIT. Para medir el efecto de un cambio
  sobre un conteo (warnings), NO comparar contra el commit anterior (confunde el efecto con el
  crecimiento del corpus): parchear el MISMO clon restaurando solo lo quitado, reconstruir y comparar
  CONJUNTOS, no totales. Resultado: 219 -> 227, delta +8, 0 eliminados. Y el dato que decide:
  0 archivos del corpus gobernado, 1 SOLO archivo antes limpio (los otros 7 ya warneaban por
  decision_id/spec_id/task_id). El diff de conjuntos dice lo que el diff de totales esconde.
- REGLA: antes de declarar que una clausula de un AC "se rompe", comprobar si esa clausula es un GATE
  POR EXIT CODE o solo prosa. Aqui CI no ejecuta la base de memoria en ningun paso (grep -i memory
  sobre .github/workflows = 0). Los 3 gates duros del AC5 de 0314 (build, drift --fast, drift --full,
  round-trip byte a byte) los recompute VERDES. Por eso no bloquea.
- LO QUE NINGUNA CAPA IMPUTO Y ES EL ARGUMENTO FUERTE: el enum queda MEDIO PURGADO. Salen 2 valores de
  vocabulario de instancia y quedan 6 (GO-PROMOVER-OFF, OK-CERRABLE, OK_CERRABLE, cambio-requerido,
  hallazgo-confirmado, draft-reviewed-informal); sobreviven solo porque no son nombres de agente.
- SOBRE PROPUESTAS DE MECANISMO (extra_status_values): aceptar la FORMA y ponerle las restricciones que
  la devuelven a ser validacion en vez de documentacion -- (i) aditivo y cerrado en carga desde un
  artefacto GOBERNADO, (ii) template vacio + un NEGATIVO PERMANENTE QUE LO MATE (sin contrato de
  falsacion, extensible == apagado), (iii) que absorba TODO el vocabulario, no lo que un gate cazo.
- R5 NUEVO Y ES COSTE DE MI PROPIA RECOMENDACION R1, LO DIGO: la allowlist de ARCHIVO COMPLETO sobre
  peer_mailbox_cron.ps1 CIEGA el defecto 3 recien corregido -- reintroducir $CoordinatorId="Arquitecto"
  deja los TRES gates en verde. Busque un arreglo mas fino: el match es case-insensitive
  (scan_domain_neutrality.py:129 re.IGNORECASE), volverlo sensible debilita el guard global y aun deja
  2 de los 9. LECCION: cuando recomiendo una allowlist por archivo, medir y declarar QUE deja de
  vigilarse; mitigacion barata = un negativo permanente sobre el defecto concreto.
- R6: el brazo PowerShell del falsador hace skipTest si no hay pwsh -> el kill de M5-ps1 solo esta
  garantizado donde exista PowerShell; la dependencia no esta afirmada por el test.
- R7 (anclaje): la correccion del handoff (mi punto 7 de r1, con retractacion explicita, bien hecha)
  esta en 5491375, NO en 52d0a38. CASI LO REPORTO COMO DEFECTO por leer el handoff en el clon del
  commit de implementacion. REGLA: cuando el commit citado es solo el de implementacion, verificar los
  artefactos de coordinacion en HEAD antes de imputar que faltan.
- R3 DE R1 SUBIO DE ANOTADO A DEMOSTRADO EN VIVO, contra mi: mi primera medicion de cobertura salio
  128->139 con 1 perdido porque el clon ya tenia el runtime/memory/index.db que YO habia generado.
  La valida es la del clon pristino: 124 -> 136, +12, 0 perdidos (y coincide EXACTO con el maker, por
  primera vez en esta tarea). REGLA DURA: medir cobertura solo en clon sin construir nada, y barrer
  __pycache__ entre pasos.
- Bucle de fix cerrado en 1 iteracion (r1 CAMBIO-REQUERIDO -> r2 OK-CERRABLE), sin escalar al humano.
  Ruteado al Arquitecto con requested_action = ratificar + C1 (registrar el 219->227 en el ledger de
  residuales de 0314) + C2 (abrir la tarea del enum). El checker NO cierra.

## TASK-0317 (2026-08-06, 17:20 local UTC+2) -- CAMBIO-REQUERIDO sobre 614b644, commit del veredicto 42194e0

- ENTREGA: una linea. `PHONE_CANDIDATE_RE` pasa de `(?:\+?\d[\d .()-]{7,}\d)` a
  `(?<!\d)(?<!\d{2}:)(?:\+?\d[\d .()-]{7,}\d)`, mas el test regenerado a familia de 333.
  Cierra mi R5 de TASK-0314 (timestamps ISO con offset negativo y fraccion de 5-6 digitos).
- LOS CUATRO AC PASAN Y LOS RECOMPUTE EN CLON LIMPIO `D:/Aegis_Scratch/mapp/an0317/cc` @ 614b644:
  familia PROPIA de 1355 (mas ancha que las 333 del test: 5 fechas x 6 horas x 7 fracciones x 9
  offsets filtradas por DATE_RE) con 0 falsos positivos y 160 rechazos bajo el patron previo; 11
  vectores de cola con 0 fugas; suite 57/57 exit 0 (344 s); build exit 0; drift --fast y --full
  exit 0 `result: pass`; 227 warnings, 0 de claves de fecha. El 227 vs "219" del contrato es el
  delta +8 que ya confirme en 0316, NO regresion de esta entrega.
- KILL DE MUTACION EJECUTADO (no por lectura): revertir la linea de produccion deja
  `test_supported_timestamps_...` en exit 1 con 36 subtests caidos. El `assertEqual(333, ...)` es
  lo que impide que la familia se vacie en silencio si alguien estrecha DATE_RE. Test con dientes.
- POR QUE BLOQUEO AUNQUE 4/4 AC PASEN -- **DIRECCION DEL FALLO**. R5 fallaba CERRADO (descartaba el
  campo, warning, nunca admitia PII). Esto falla ABIERTO: un telefono real entra al indice como
  `title` ACEPTADO. Cambiar un falso positivo fail-closed por un falso negativo fail-open en el
  componente cuya razon de ser es ser cerrado por defecto en PII es EMPEORAR, aunque el contador de
  AC diga 4/4. **REGLA NUEVA: contar AC no es el veredicto; la direccion del fallo manda.**
- LAS DOS ATENUANTES DEL ARQUITECTO, REFUTADAS CON MEDICION (el las trajo de buena fe como
  residual "estrecho"):
  (a) "exige adyacencia sin espacio" -> FALSO. Solo cuentan los DOS caracteres previos al primer
      digito; el telefono puede llevar espacios: `09:555 123 4567` y `09:28:612 345 678` se pierden.
      Su sonda 4 (`09:28: 612345678`) sobrevive porque el espacio esta TRAS los dos puntos.
  (b) "acotado por la allowlist de claves y por DATE_RE" -> FALSO para la superficie ancha:
      `contains_pii` (build_memory_db.py:609) corre sobre TODO valor aceptado y `title_is_safe`
      (:536) sobre `title`, TEXTO LIBRE de 500 caracteres sin gramatica. `reunion a las
      09:28:612345678` -> ACEPTADO. **LECCION: cuando evaluo un cambio a un predicado compartido,
      enumerar TODOS sus llamadores antes de aceptar el argumento de acotamiento del proponente.**
- LOS DOS LOOKBEHINDS NO SON INDEPENDIENTES (el mensaje los describia como dos guardas separadas).
  Atribucion por fuzz de 600k: `(?<!\d)` solo = 0 perdidas; `(?<!\d{2}:)` solo = 98; los dos juntos
  = 175. El segundo bloquea la RECUPERACION del primero: tras `NN:` el motor arranca un caracter mas
  adelante y `(?<!\d)` lo mata, y asi hasta agotar la corrida -> desaparece el numero entero.
  Corolario: NO hay rollback parcial, los dos son necesarios para cerrar R5.
  **TECNICA: atribuir la perdida a CADA guarda por separado y a la combinacion; las interacciones
  entre lookbehinds no se ven razonandolas, se ven midiendolas.**
- PERDIDA MEDIDA: 160 en rejilla estructurada (35 prefijos x 8 telefonos x 5 sufijos), 134 en fuzz
  500k (semilla 20260806), 175 en fuzz 600k (semilla 9001), 110 formas distintas en fuzz 400k.
  Semillas fijas SIEMPRE, para que el Arquitecto pueda reproducir el numero exacto.
- NO ME QUEDE EN "CAMBIO-REQUERIDO": CONSTRUI Y CORRI LA ALTERNATIVA que el propio Arquitecto
  sospechaba (su punto 4). Ancla en DATE_RE, precedente en la MISMA linea (ya exime lo que
  `ID_RE.fullmatch` acepta entero): revertir el patron + `if not ID_RE.fullmatch(item) and not
  DATE_RE.fullmatch(item):`. Resultado: iguala AC1 (0 falsos positivos sobre 1355) y AC2 (0 vectores
  perdidos), pasa SIN TOCARLO el mismo test de AC3 y la SUITE COMPLETA 57/57 exit 0, y pierde **0**
  en rejilla y en fuzz 500k. DOMINA ESTRICTAMENTE al mismo coste de una linea.
  Seguridad verificada, no asumida: el charset de toda cadena que DATE_RE acepta ENTERA es
  `+-.012345689:TZ`, con 0 coincidencias de email/IBAN/documento sobre las 1355 -> no cabe PII en la
  gramatica; los 11 vectores caen igual porque ninguno hace fullmatch (el sufijo rompe el anclaje).
  Dos condiciones que puse en el handoff porque son faciles de perder: la exencion va DENTRO del
  bloque del heuristico de telefono (nunca `return False` temprano en `contains_pii`, eso eximiria
  los patrones estructurales y reabriria F2), y el `assertEqual(333, ...)` se queda.
  **REGLA: cuando el proponente pregunta "es esta el ancla correcta?", responder con la variante
  CONSTRUIDA Y MEDIDA contra los mismos gates, no con una opinion. Convierte un debate en un dato.**
- CONFIRMA MI PROPIO r2 DE 0314: "R5 y R1 son la misma superficie vista por sus dos lados". Anclar en
  DATE_RE ataca la superficie; estrechar el patron de telefono la mueve de lado. R1 sigue abierto.
- LAZO DECLARADO: remediacion con el ancla DATE_RE; gates por exit code en clon limpio; rejuicio mio
  sobre el commit de remediacion exigiendo **0 perdidas** en el diferencial contra el patron
  pre-0317; maximo 2 iteraciones antes de escalar al operador. Pedi ademas al Arquitecto mantener la
  regla de s.16.7 (no declarar el motor listo para exportar) hasta que cierre la REMEDIACION.
- GOTCHA DE HERRAMIENTA (me costo dos intentos): el Python es de Windows, asi que rutas `/tmp/...`
  pasadas a `python -c` fallan con FileNotFoundError aunque bash las resuelva; usar el scratchpad con
  ruta Windows. Y `check_memory_db_drift.py --full` escribe ruido de git (detached HEAD) antes del
  JSON: parsear la ULTIMA linea que empieza por `{`, no el fichero entero.
- GOTCHA: `importlib` para cargar build_memory_db.py fuera de su paquete exige
  `sys.modules["mdb"] = mdb` ANTES de `exec_module`, o los `@dataclass` revientan.
- COORDINACION: `MSG-20260806-Arquitecto-to-Analista-REVIEW-TASK-0319` sigue ABIERTO sin veredicto
  mio; esta ejecucion solo tenia asignado el de 0317. Lo senale en el mensaje para que no se lea
  como consumido. Sin claims activos al escribir; commit por pathspec explicito; validate, encoding
  y neutralidad exit 0 antes y despues del commit.

## 2026-08-06 -- TASK-0319 (harness: inanicion por defers pre-exec) -- CAMBIO-REQUERIDO sobre a7c6e96

- VEREDICTO: 7/8 AC en verde, bloqueo por **AC6**. Artefacto
  `Area_comun/artifacts/Analista-TASK-0319-harness-defer-starvation-verdict.md`, commit `9959a0a`.
- **LECCION CENTRAL -- EL MOCK OCULTA EL FORMATO QUE ESTA EN DISCUSION.** El test del maker
  (`test_residue_excludes_foreign_personal_and_caps_diagnostics`) mockea `Get-GitStatusPorcelainUtf8`
  con una cadena sintetica de solo registros `?? <ruta>`. El defecto vivia justo en la codificacion
  REAL que el mock no produce. Cuando el AC habla de un FORMATO (salida de git, de un parser, de un
  protocolo), la sonda tiene que alimentar el productor REAL, no una cadena a mano. Yo cargue por AST
  las funciones reales del .ps1 y las corri contra repos git de verdad en scratch: ahi salio a la
  primera.
- **EL DEFECTO CONCRETO, para reconocer el patron:** `git status --porcelain=v1 -z` NO usa ` -> `
  para renombrados; emite DOS registros NUL-separados, `R  <nueva>` y luego `<vieja>` **sin prefijo
  de estado**. Un filtro que asume `XY <ruta>` y hace `Substring(3)` a todos amputa 3 caracteres a la
  ruta vieja. Y si la fila `R` se filtra, el huerfano pierde el emparejamiento `$index++` de mas
  abajo. Resultado medido: `residue_state=live` donde AC6 exige `none`, y un `paths_json` con una
  ruta FANTASMA (`sonal/Analista/...`).
- **CODIGO MUERTO QUE PARECE COBERTURA.** La rama ` -> ` no puede dispararse jamas (git no la emite
  bajo `-z`; en Windows `>` ni es caracter legal de nombre). Convencio a DOS lectores independientes
  (handoff del maker y recomputo del Arquitecto, que escribio literalmente "maneja renombres (` -> `)").
  **REGLA: cuando un revisor justifica un PASS citando una rama concreta, comprobar que esa rama es
  ALCANZABLE antes de aceptarla.**
- **MATIZ SOBRE MI PROPIA LECCION DE 0317 ("la direccion del fallo manda").** No es un comodin. Aqui
  la direccion "conservadora" (un defer de mas) ES el dano que el AC persigue: AC6 existe para que un
  area privada ajena deje de generar defers. Preguntar siempre: conservador *respecto de que*
  garantia. En AC7 equivocarse de mas es gratis; en AC6 no.
- ACOTE EL IMPACTO CON HONESTIDAD y aun asi bloquee: no es regresion y se auto-degrada a `aborted` a
  los 5 min (`AbortedResidueMinutes`). Bloqueo por **AC falsado sobre vector ordinario** (`git mv` en
  la carpeta de borradores del propio peer), no por magnitud. Decirlo explicito evita que el bloqueo
  se lea como alarmismo.
- RESPONDI SUS DOS PREGUNTAS CON DATO, NO CON OPINION:
  (1) La alternancia de causas reinicia el reloj para siempre -- CONFIRMADO (12 sondeos alternando
  con presupuesto de 1s -> cero `RETRY_EXHAUSTED`), pero ACEPTABLE: es literalmente lo que pide AC3, y
  un tope absoluto re-crea el defecto que la tarea elimina, solo que con constante mayor. Lo que falta
  es OBSERVABILIDAD: no hay ningun campo monotono (`defers` vuelve a 1 y `defer_started_at` se
  resella en cada cambio de causa). Pedi `first_defer_at` -> `total_age_seconds` en `RETRY_DEFER`.
  (2) Las entradas terminales previas no se auto-curan (seleccion linea 942 descarta `exhausted=true`;
  `Reset-PreExecDefer` no corre hasta 1008) -- CONFIRMADO, pero recomende NO curarlas por olfateo de
  esquema: "sin `defer_reason` = obsoleta" es heuristica de un solo uso que al dia siguiente es codigo
  muerto permanente, **la misma clase de rama que acababa de falsar**. Re-armado correcto = la FIRMA
  del mensaje, que ya es content-addressed.
- HALLAZGO LATERAL: el handoff declara `validate_collaboration_state.py` PASS, pero en clon limpio
  sobre `a7c6e96` sale **exit 1** (drift de los tres `*.slim.json` bajo `enforce`, hard-fail B.3).
  Verde en `092b9b0` y `b9698d6`. **REGLA: verificar los gates sobre el commit que el handoff CITA,
  no solo sobre HEAD; un drift transitorio de mitad de entrega se ve ahi y en ningun otro sitio.**
- TECNICA REUTILIZABLE: sonda PowerShell que extrae funciones por AST
  (`[Parser]::ParseFile` + `FindAll(FunctionDefinitionAst)` + `Invoke-Expression $node.Extent.Text`)
  y las corre con `$Root`/`$PeerId` inyectados. Permite ejercer una funcion del harness contra un
  repo git real sin lanzar el cron. Sondas en `D:/Aegis_Scratch/mapp/p0319/`.
- GOTCHA: `git clone` completo del hub tarda >2 min y revienta el timeout por defecto de Bash;
  reutilizar un clon existente con `git checkout <sha>` y subir el timeout.
- GOTCHA: `>` no es caracter legal de nombre de archivo en Windows, asi que el vector ` -> ` inyectado
  en un nombre NO es reproducible en esta plataforma; declararlo como no alcanzable, no como no probado.
- COORDINACION: sin claims de peer sobre mis rutas; commit por pathspec explicito de mis DOS archivos
  (habia entrega del Arquitecto a medio escribir en `Area_comun/state/*` y `runtime/state/*` -- no la
  toque). Clean-clone-validate sobre MI commit `9959a0a` antes de push: validate y encoding exit 0.
  Push OK; el Arquitecto commiteo encima (`2b7b7fc`) en el arbol compartido y subio en el mismo push.
  Aviso de poda vencida (`cold_start_tokens`) -- es del checkpoint coordinado del Arquitecto, no mio.

## 2026-08-06 (20:20 CEST) -- TASK-0319 r2: OK-CERRABLE sobre d28277d (mi commit c564bb3)

- VEREDICTO: **OK-CERRABLE**. S1 (mi bloqueante de r1) cerrado en sus tres puntos.
  Artefacto `Area_comun/artifacts/Analista-TASK-0319-r2-record-pairing-verdict.md`;
  mensaje `MSG-20260806-Analista-to-Arquitecto-REVIEW-TASK-0319-r2.md`. 5 gates exit 0 en clon
  limpio `D:/Aegis_Scratch/mapp/cc0319r2` sobre `d28277d`, INCLUIDO validate sobre el propio commit
  de remediacion (el S3 de r1 no se repitio).
- **TECNICA QUE HAY QUE REPETIR SIEMPRE: mutar la FUENTE REAL para comprobar que un boundary nuevo
  tiene dientes.** No basta con leer que el test crea un repo git de verdad. Reverti el bucle de
  emparejamiento al filtro ciego de r1 dentro del clon limpio, corri la suite -> **exit 1** fallando
  exactamente en `assert rename["state"] == "none"`, y restaure con `git checkout --`. Eso convierte
  "el maker anadio un test" en "el test mata el defecto que yo encontre". Sin ese paso el veredicto
  es un rubber stamp con tabla.
- 20 vectores gatados con git REAL + funciones reales por AST, 0 SLIPS (sondas
  `D:/Aegis_Scratch/mapp/p0319r2/probe.py` y `probe2.py`, reutilizables): 4 cruces de la regla de
  unidad, copia, `RM`, `RD`, espacios, tope de 10 con 12 renombrados, origen de 2 chars, pares
  consecutivos, fuga tras el par, stream truncado.
- **LECCION DE METODO: un vector que falsa al REVISOR tambien es evidencia -- no lo borres.** Mi
  vector V (origen en `RCpersonal/`) salio `live` donde yo esperaba `none`; al revisar, mi
  expectativa estaba mal (no esta bajo `personal/`, es ruta gobernada). Lo deje en la tabla marcado.
- `git status --porcelain=v1 -z` de esta maquina **no emite `C`** ni con `status.renames=copies`
  (emite `A `). Para ejercer el registro `C` hay que inyectar stream sintetico y DECLARARLO como tal
  en la tabla, nunca venderlo como git real.
- HALLAZGO NUEVO S4 (NO bloqueante, tarea aparte): `Get-WorktreeDiskProof` (linea 655) conserva la
  rama muerta ` -> ` (linea **663**) y el `Substring(3)` a ciegas -> produce la ruta amputada
  `sonal/Analista/n-old.md` dentro de `proof=disk`, y `$null` si el origen tiene <4 chars. No bloquea
  (los dos snapshots comparados aplican la misma transformacion; no hay `ROLLBACK_LEDGER_PRESERVED`
  falso) y mi S1.2 estaba redactado sobre el filtro de residuo. **REGLA: no ensanchar el alcance del
  bucle a posteriori; abrir tarea nueva.** Frase para reutilizar: "se arreglo la instancia, no la clase".
- **DOS CORRECCIONES FACTUALES AL COORDINADOR, segunda vez seguida (r1 S3, r2 aqui):** el REVIEW r2
  decia "suite 8/8" (son 13/13) y "ya no queda ningun `-match ' -> '`" (falso, linea 663). Verificar
  SIEMPRE con grep las afirmaciones categoricas de cobertura del mensaje que me rutean: en r1 fue
  justo una afirmacion asi la que dejo pasar el defecto.
- `unknown` NO es via de escape: `peer_mailbox_cron.ps1:1006-1008` difiere con `residue_probe_failed`
  y retorna ANTES de `Get-AdditionalWorkSignal`, `Reset-PreExecDefer` y toda toma de lock. Verificado
  en el llamador, no asumido.
- GOTCHA CORREGIDO respecto a r1: `git clone` LOCAL con hardlinks tarda **23 s**, no >2 min. El
  `--no-hardlinks` de r1 era lo que copiaba los ~7,4 GB de objetos sueltos del `.git`. Para gatear en
  clon limpio: `git clone <ruta> <dst>` sin `--no-hardlinks`.
- COORDINACION: Codex tenia claim ACTIVO `CLAIM-20260806-Codex-TASK-0319-remediation-1` sobre harness,
  suite, estado y task file -- **ninguna de mis dos rutas** (`Area_comun/artifacts/`,
  `Area_comun/mailbox/open/`). Commit por pathspec explicito, arbol gobernado limpio, push OK
  (`acd82a8..c564bb3`). Post-commit validate exit 0.

## 2026-08-06 (20:50 CEST) -- TASK-0317 r2: OK-CERRABLE sobre 3d64a7c (mi commit f98df23)

- VEREDICTO: **OK-CERRABLE**. El bloqueante de r1 (el arreglo fallaba ABIERTO: perdia 134-175 casos
  de deteccion de telefono) esta cerrado. Artefacto
  `Area_comun/artifacts/Analista-TASK-0317-r2-anclaje-date-re-verdict.md`; mensaje
  `MSG-20260806-Analista-to-Arquitecto-REVIEW-TASK-0317-r2.md`. **7 gates exit 0** en clon limpio
  `D:/Aegis_Scratch/mapp/an17r2` sobre `3d64a7c`: suite 59/59, build, drift `--fast` y `--full`,
  validate, scan_encoding, scan_domain_neutrality. Lazo cerrado en **1 de las 2 iteraciones**.
- **TECNICA NUEVA QUE HAY QUE REPETIR: cuando el maker dice "implemente TU variante", no leas el
  diff -- RECONSTRUYE tu variante como funcion independiente y compara SALIDA CONTRA SALIDA sobre
  cientos de miles de cadenas.** Reconstrui el anclaje y lo compare con `contains_pii` real:
  **1.501.400 entradas, 0 discrepancias**. Eso convierte "el diff parece el mio" en "es el mio".
  Sonda reutilizable: `D:/Aegis_Scratch/mapp/probe_0317_r2.py`, `probe2_*.py`, `probe3_*.py`.
- **TRAMPA QUE ME PILLE A MI MISMA: al reconstruir una linea base hay que replicar TODA la
  normalizacion del original.** Mi primer banco marco 4 perdidas falsas (`MSG-612345678 `) porque no
  aplicaba `value_list()`, que hace `.strip()`. Con el strip, esos valores caen bajo la exencion
  `ID_RE` (residual R1, identico antes y despues). **Regla: antes de reportar una perdida, verifica
  que tu baseline pasa por las mismas funciones que el codigo real.** Un baseline sucio inventa
  defectos y quema credibilidad igual que un rubber stamp.
- **MUTACION EN DOS SABORES, no uno.** M1 (revertir el arreglo) -> exit 1, 36 subtests: el test tiene
  dientes. **M2 (colocar el arreglo MAL -- `continue` por `DATE_RE` ANTES de las comprobaciones
  estructurales, que es justo la anti-pauta que yo advertia en r1) -> los 59 tests pasan exit 0**,
  siendo esa variante medible mas debil (`contains_pii('2026-01-01T00:00:00Z', ('2026',))` da False
  ahi y True en lo entregado: puentea la capa de dominio). **Mutar hacia el fallo CORRECTO no basta;
  hay que mutar tambien hacia la version PLAUSIBLE-PERO-DEBIL.** Eso es lo que revela huecos de
  dientes. Residual R-N2.
- **CARACTERIZAR la superficie del arreglo, no solo medir que no perdi nada.** El conjunto eximido es
  exactamente `{s : DATE_RE.fullmatch(s.strip())}` (0 fugas genuinas sobre 200.000 cuasi-timestamps).
  Y aun asi **el 2,9% de ese conjunto lleva una corrida de 9-10 digitos**: portador construido
  `2026-01-01T00:00:61.234567-89:00` (carga `6123456789`) se acepta como `title`. **No bloquea porque
  ese conjunto ES el AC1** -- no se puede cerrar el falso positivo sin eximirlo -- y porque cualquier
  etiqueta lo saca de la gramatica. Residual R-N1. Mitigacion medida: con `DATE_RE` validando rangos
  cae a 0,05% (R-N3). Declararlo aunque no bloquee; presentarlo como "cero" habria sido falso.
- **ATRIBUIR TODA CIFRA QUE CAMBIA ENTRE RONDAS.** 57->59 tests y 227->219 warnings NO eran de esta
  entrega: los dos los causa `5a699bb8` (TASK-0318, vocabulario de estados). Verificado con
  `git show 5a699bb8 -- <test> | grep -c timestamp` = 0. Sin esa atribucion, una de las dos se lee
  como regresion y la otra como mejora inexistente.
- **CORRIJO PUBLICAMENTE DOS ERRORES MIOS DE r1** (en el artefacto y en el mensaje): el alfabeto
  alcanzable de `DATE_RE` es `+-.0123456789:TZ` -- en r1 lo transcribi sin el `7` porque lo LEI de un
  corpus estrecho en vez de DERIVARLO de la gramatica; y las 4 falsas perdidas de arriba. Un veredicto
  que no corrige sus propias cifras no vale como contrato para la ronda siguiente.
- COORDINACION: **0 claims activos** al escribir; arbol gobernado sin entrega a medias. Ojo, el arbol
  compartido avanzo solo durante mi revision (83ba3a7 -> 831771d, el Arquitecto ratifico 0319 y
  ruteo 0320/0321): **re-`git fetch` + comprobar ancestro JUSTO antes de commitear**, no al empezar.
  Commit por pathspec explicito, push OK (`831771d..f98df23`). Aviso de poda vencida
  (`cold_start_tokens`) sigue siendo del checkpoint del Arquitecto, no mio.
- GOTCHA util: `git worktree add --detach <dst> <commit>` desde el clon limpio es la forma barata de
  tener un arbol MUTABLE para mutaciones sin ensuciar el clon donde corren los gates (y sin pagar un
  segundo clone). `git worktree remove --force` al terminar.

## 2026-08-06 (22:25 CEST) -- TASK-0321 diskproof: OK-CERRABLE sobre 0a008f06 (mi commit e2286c4)

- Encargo `MSG-20260806-Arquitecto-to-Analista-REVIEW-TASK-0321`. **SIN PRODUCTO EN ALCANCE**
  (declarado en la primera linea). Continuacion directa de MI hallazgo S4 del veredicto r2 de 0319:
  el mismo defecto de emparejamiento vivo en `Get-WorktreeDiskProof`. Artefacto
  `Area_comun/artifacts/Analista-TASK-0321-diskproof-pairing-verdict.md`, pusheado
  (`53e380f6..e2286c4b`). Seis AC PASAN, 0 SLIPS en 25 vectores.
- Anclaje: arreglo `0a008f06`, entrega `2fb770cc`, pre-arreglo `38b46096`, gates en `53e380f6`.
  Dos clones: `--depth 1` para el codigo y `--shared` para los gates.
- **LECCION DE CLONADO -- `--depth 1` HACE ROJO EL VALIDADOR.** El clon superficial dio
  `VALIDATE_EXIT=1` con `commit_trailers could not scan git history from 57f6250f...: rev-list
  ... exit 128`: no es un defecto de la entrega, es que el clon no tiene la historia desde el
  genesis. Casi lo reporto como bloqueante. **Para gatear `validate` hace falta historia
  completa**; la forma barata en este repo (7 GB de objetos sueltos) es `git clone --shared`,
  que no copia objetos y da todas las refs. `--depth 1` sirve para leer/ejecutar codigo, no para
  gatear el protocolo.
- **METODO QUE FUNCIONO: NUEVO vs VIEJO en el MISMO repo y el MISMO instante.** Cargo las dos
  versiones de la funcion por AST (`Parser::ParseFile` + `FunctionDefinitionAst` +
  `Invoke-Expression`) desde el `.ps1` entregado y desde `git show 0a008f06^:<ruta>` volcado a
  fichero, y las corro contra el mismo repo git recien creado. La falsacion del AC1 sale sola y
  es incontestable: `s/disk-old.md`, `older/old name.md`, `e-old.md`, `/c/deep-old.md`, y dos
  rutas destruidas a `.md` con dos renombrados.
- **BUSCAR EL DESALINEO, NO SOLO LA RUTA AMPUTADA.** El modo de fallo caro de un parser por pares
  no es la ruta del par, es el CORRIMIENTO que contamina todo lo posterior. Lo ataque con cinco
  vectores dedicados (renombrado entremezclado con modificado/borrado/untracked, dos renombrados
  seguidos, par + normal, normal + par + normal, dos pares seguidos). Ninguno desalineo.
- **PowerShell 5.1, gotchas verificados y no supuestos:** `Where-Object { $_ }` **conserva** la
  cadena `"0"` (solo cae la vacia) -- lo probe antes de escribir nada, era una hipotesis de
  escape razonable y era falsa. Y `$null.Replace(...)` es error NO terminante: el script sigue,
  exit code 0, la variable queda `$null`.
- **DOS DE MIS SEIS MUTACIONES ERAN EQUIVALENTES Y LO VERIFIQUE ANTES DE REPORTARLAS.** Sobrevivir
  la suite no prueba hueco de cobertura. (a) Quitar la guarda de limites sobrevive porque
  `IsNullOrWhiteSpace($null)` ya cierra el caso: solo quitando LAS DOS guardas se fabrica
  `[null, moved.md]`. (b) Invertir el orden del par sobrevive porque la funcion hace
  `Sort-Object { $_.path }` antes de serializar, asi que el orden interno no es observable.
  Reportarlas como huecos habria sido vender dos falsos hallazgos. Huecos REALES: rama `C`,
  reintroduccion de la rama muerta, y rechazo de origen en blanco.
- **HALLAZGO NUEVO R3, fuera de alcance: el defecto HERMANO en los lectores SIN `-z`.** El
  Arquitecto pidio ampliar el barrido a otros scripts y ahi aparecio:
  `sweep_cron_zombies.dirty_paths()` convierte `?? "personal/caf\303\251.md"` en
  `'"personal/caf/303/251.md"'` -- sin `-z` manda `core.quotepath`, git entrecomilla y escapa en
  octal, y el `.replace("\\","/")` convierte las barras de escape en separadores. Su consumidor
  `dirty_claimed_route()` falla **ABIERTA**: el barredor de zombis puede matar a un peer que
  escribe una ruta reclamada. Mismo patron en `runtime/orchestrator.py:667` y `:688` y en el
  espejo de `examples/full_runtime_instance/`. **No es S4** (ahi ` -> ` si lo emite git). Ruteado
  como pregunta al Arquitecto, no tocado.
- Descarte ademas la hipotesis del **duplicado obsoleto del harness**: `find` da una sola copia y
  `test_new_instance_exports_identical_harness` pasa. Merecia la pena mirarlo: un exportador que
  publica el parser viejo seria un AC5 fallado invisible al grep del archivo entregado.
- **ATRIBUIR ANTES DE REPORTAR, otra vez.** `prune_state --check` daba exit 1 en el ancla y la CI
  falla con eso. Antes de escribirlo como bloqueante lo medi en cuatro commits: ya estaba vencida
  en `38b46096`, **antes** de TASK-0321. El Arquitecto la corrio en `53e380f6` mientras yo
  revisaba y el gate quedo verde. De bloqueante a nota de trazabilidad.
- Discrepancia de cifras menor, anotada sin dramatizar: el recomputo del Arquitecto cita 8/8 en la
  suite del harness y son **14** casos. El exit code es lo que gatea.
- COORDINACION: 0 claims activos sobre mis rutas al escribir, arbol gobernado sin mods rastreadas.
  El arbol avanzo durante la revision (`6dfdd4c7` -> `d192d32d` -> `53e380f6`): **re-`git fetch`
  justo antes de commitear**, no al empezar (segunda vez seguida que salva el commit). Pathspec
  explicito en el `git commit`, nunca `git add` pelado. Trailers `Task-Id` + `Ops-Reason` +
  `Co-Authored-By`. Ojo: `check_commit_trailers.py --root .` da exit 2, es error de USO (espera un
  fichero de mensaje de commit); el gate real de trailers va dentro de `validate`, que dio 0.
- Limpieza: `git worktree remove --force` de los cuatro arboles temporales de la atribucion de la
  poda + `git worktree prune`. Scratch bajo `D:/Aegis_Scratch/mapp/` (DECISION-0104).

## 2026-08-07 (01:10 CEST) -- TASK-0317 r3 contrato de colocacion: CAMBIO-REQUERIDO sobre f2c6c315 (mi commit c49cc3a9)

- **Pregunta del Arquitecto:** el contrato `NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY` tiene dientes de
  verdad, o se puede mover la exencion sin que ningun gate lo note? Respuesta medida: **caza 4 de
  las 5 formas que construi; la quinta pasa el stack completo en verde.**
- **METODO QUE FUNCIONO Y REPITO: el mutante como FUENTE REAL, no como cadena en un test.** Para
  cada vector escribi el mutante en `scripts/memory/build_memory_db.py` de un sandbox y pregunte lo
  unico que importa: *si un maker commiteara esta regresion, falla el gate?* Cazados: A (exencion
  extraida a funcion aparte + `continue` al tope), B (movida debajo del telefono, encima del
  dominio), D (exencion calculada en sitio y reusada para saltar el dominio). No cazado por el
  contrato pero cazado por otro test: C (ensanchar `DATE_RE` -> 11 subtests de
  `test_timestamp_pii_suffix_is_rejected`, AC2 con dientes mecanicos).
- **EL SLIP (E) y su leccion generalizable:** un contrato de falsacion cuyo unico diente conductual
  sobre la fuente real es `assertTrue(f(UN_EJEMPLO))` solo fija **un punto del espacio**. Movi al
  tope del bucle una exencion mas ESTRECHA que el payload del contrato
  (`re.fullmatch(r"\d{4}-\d{2}-\d{2}", item)` + `continue`): deja intacto el timestamp del contrato,
  respeta las dos cadenas-fixture (`count == 1`), y **pasa `check_falsification_contracts
  --inventory` exit 0 y `test_memory_db.py` 60/60 OK en clon limpio CON historia**, mientras
  `contains_pii("2026-06-19", ["2026"])` pasa de `True` a `False`. Cuando revises un contrato,
  pregunta siempre: *que subconjunto del espacio cubre el payload, y que queda fuera?*
- **El argumento que convierte el hallazgo en bloqueo, no en residual:** el escape cae DENTRO del
  enunciado del propio contrato ("Moving the date exemption above the phone heuristic..."), asi que
  es el contrato fallando su propia promesa. Y reproduce el patron que el AC3 de esa misma tarea
  llama textualmente *"parte del defecto"* (fijar ejemplos que esquivan la mitad negativa).
- **CONTROL OBLIGADO ANTES DE CANTAR "CAZADO" O "SE CUELA":** mi primer sandbox era `git archive`
  sin `.git`, y ahi `test_current_tree_build_does_not_change_tracked_status` da ERROR **siempre**,
  tambien en el arbol SIN mutar. Corri el control sin mutar, vi el mismo error, y repeti E en el
  clon con historia -> alli el gate entero es verde. Sin ese control habria vendido un falso cazado.
- **REMEDIACION PROBADA, NO PROPUESTA A CIEGAS.** El generador de familia ya existe 30 lineas mas
  arriba en la misma clase (`test_memory_db.py:365-381`, 333 cadenas). Barrido sobre esa familia:
  **0 de 333** en f2c6c315 (verde hoy, no obliga a tocar produccion) y **3 de 333** en el mutante E
  (`2026-01-01`, `2026-06-19`, `2026-12-31`). Dar la remediacion medida cambia el tono del veredicto
  de "no me fio" a "cuesta una iteracion".
- **GOTCHA DE CLON LIMPIO, para el runbook:** gatear en clon **superficial** (`--depth`) da un
  FALSO ROJO de `validate`: `commit_trailers could not scan git history from 57f6250f...` porque el
  commit base no esta en el grafo. `git fetch --unshallow` y el mismo comando da exit 0. Casi lo
  reporto como bloqueante.
- Gates recomputados en el clon limpio (f2c6c315, tree limpio), todo por exit code: `validate` 0,
  `scan_encoding` 0, `scan_domain_neutrality` 0, `prune --check` 0,
  `check_falsification_contracts --inventory` 0, `test_memory_db.py` 0 (60/60, 323 s),
  build 0 (4225 artefactos, 219 warnings, **0 de clave de fecha** = AC4 literal),
  drift `--fast` 0 y `--full` 0 (`"result":"pass"`).
- Cableado verificado, no inferido: `--inventory` lista el contrato con runner
  `scripts\memory\test_memory_db.py`; el checker exige `mutation` y cada `boundaries` **literales**
  dentro del cuerpo del `exercised_by`; CI lo corre en `validate.yml:47-50` y el fichero cierra con
  `unittest.main`. No repetimos 0316.
- **ALCANCE DEL BLOQUEO, declarado explicito para que no se re-litigue:** el fix funcional que
  aprobe en r2 sobre `3d64a7c` esta intacto y sigue correcto (lo re-medi). El cambio pedido se
  limita a la asercion conductual del test nuevo.
- Residuales declarados: R3-1 aserciones de texto-fuente fragiles pero **fail-closed** (fueron las
  que cazaron B; el mensaje `1 != 0` no explica la garantia); R3-2 el credito de AC2 es de
  `test_timestamp_pii_suffix_is_rejected`, no de este contrato (interactua con TASK-0322);
  R3-3 el falso rojo del clon superficial.
- COORDINACION: 0 claims activos sobre mis rutas; arbol gobernado sin mods rastreadas ajenas;
  `git fetch` justo antes de commitear (origin/main habia avanzado a `e6736185`). Pathspec explicito
  en el `git commit`, nunca `git add` pelado. Trailers `Task-Id` + `Ops-Reason` + `Co-Authored-By`.
  Scratch bajo `D:/Aegis_Scratch/hub/an0317/` (DECISION-0104), pendiente de limpiar al stand-down.
- Bucle declarado: r4 acotada a `scripts/memory/test_memory_db.py`; gates
  `test_memory_db.py` + `check_falsification_contracts --inventory` + `validate` + `scan_encoding` +
  drift; **re-juicio antes del commit de cierre re-corriendo el mutante E y exigiendo que FALLE**;
  maximo 2 iteraciones antes de escalar al operador.

## 2026-08-07 04:15 (UTC+2) -- TASK-0317 r5: OK-CERRABLE sobre 0d686650 (commit 626f20bc)

Cierro el hilo que bloquee en r3. Veredicto **OK-CERRABLE con dos residuales declarados**.
Artefacto: `Area_comun/artifacts/Analista-TASK-0317-barrido-familia-r5-verdict.md`.
Mensaje: `MSG-20260807-Analista-to-Arquitecto-VEREDICTO-TASK-0317-r5.md`.

- **RE-JUICIO CUMPLIDO TAL COMO LO DECLARE EN R3:** reconstrui el mutante E como fuente real y
  exigi que FALLARA. Falla: 3 subtests rotos (`2026-01-01`, `2026-06-19`, `2026-12-31`), exit 1,
  exactamente los 3 de 333 que habia predicho. No lo di por bueno leyendo el diff.
- **VERIFICAR UN NUMERO MAGICO = DERIVARLO ANTES DE CONTARLO.** Para 333 hice la forma cerrada
  primero (3 fechas x 3 horas con dos puntos x 7 fracciones x 5 offsets = 315, + 3x1x1x5 = 15 de
  hora compacta sin fraccion, + 3 fechas desnudas) y solo despues confirme el conteo. Ademas
  comprobe **por que** caen 90 de las 420 del cartesiano: son exactamente las de hora compacta con
  fraccion, que la alternancia de `DATE_RE` prohibe. Asi se distingue "derivado" de "cuajado a
  posteriori" sin depender de la palabra del maker.
- **UNA GUARDA SE MIDE EN LOS DOS SENTIDOS.** No basta con que `assertEqual(333)` pase hoy: hay que
  romperla a proposito. Estrechar `DATE_RE` dentro de la gramatica -> `333 != 318` exit 1; ensancharla
  -> `333 != 423` exit 1. Sin esas dos mediciones la frase "protege de la degradacion silenciosa"
  es prosa.
- **ESCAPES NUEVOS QUE ENCONTRE (y por que NO bloquee).** Dos mutantes nuevos, ambos con el stack
  entero VERDE (`inventory` 0, suite 60/60 OK):
  - **mF (R5-1):** exencion temprana con predicado disjunto de los 333 puntos (offsets con minutos
    `:45`). `contains_pii` pasa de True a False para `+05:45`/`-09:45`. Es la misma clase que el
    SLIP de r3, pero adversarial a medida.
  - **mN (R5-2):** estrechamiento de `DATE_RE` confinado al COMPLEMENTO de la gramatica enumerada
    (offsets a horas 00-12 y minutos 00/30). El conteo sigue en 333, las dos `assertEqual(333)`
    pasan, y sin embargo `validate_metadata` empieza a RECHAZAR `+05:45` (Nepal), `+13:00` (Tonga),
    `+14:00` (Kiribati). Falla cerrado. Es superficie de TASK-0322, no de la colocacion.
- **LECCION DE JUICIO, la mas importante de esta ronda: distinguir el escape PLAUSIBLE del
  ADVERSARIAL A MEDIDA.** En r3 bloquee bien porque lo que se colaba eran las **fechas desnudas**,
  la forma mas comun del corpus, producible por un refactor sin querer. Aqui lo que se cuela es un
  predicado elegido a mano para esquivar los puntos de muestreo. Lo verifique por el otro lado: el
  refactor plausible (`datetime.fromisoformat` + `continue`) **si cae**. Bloquear otra vez habria
  sido **mover la porteria**: mi propia remediacion prescrita en r3 fue literalmente este barrido, y
  yo mismo declare maximo 2 iteraciones. Un checker que exige que un muestreo finito agote un
  lenguaje infinito no deja cerrar nada nunca.
- **CUANDO NO BLOQUEO, ENTREGO EL ARREGLO ACOTADO MEDIDO.** En vez de muestrear puntos, afirmar la
  propiedad sobre el AST: el bucle de `contains_pii` no puede contener ningun `continue`. Medido en
  las 4 fuentes: verde en `0d686650`, caza mE y mF, una linea, cero produccion. Va como insumo de
  seguimiento junto a TASK-0322, no como condicion de cierre.
- **GOTCHA DE HERRAMIENTA QUE ME COSTO DOS INTENTOS FALSOS:** los heredocs `<<'PY'` con regex de
  Python me llegaron con los backslashes mutilados y el `str.replace` no aplico -> los "mutantes"
  eran copias SIN MUTAR y el test pasaba en verde. **Casi canto un falso PASS.** Dos defensas que
  adopto: (1) `assert s.count(OLD) == 1` antes de cada replace, que fue lo que lo cazo; (2) escribir
  el script de mutacion a FICHERO con la herramienta Write y ejecutarlo, nunca por heredoc. Y ojo al
  copiar una linea de fuente: la de `DATE_RE` termina en `)"`, no en `)`.
- Gates recomputados en clon limpio con historia (`D:/Aegis_Scratch/hub/an17r5/cc`, checkout de
  `0d686650`, `git status` vacio), todo por exit code: `validate` 0, `scan_encoding` 0,
  `scan_domain_neutrality` 0, `prune --check` 0, `check_falsification_contracts --inventory` 0,
  `test_memory_db.py` 0 (60/60, 373 s), build 0 (**4231** artefactos, **0** warnings de clave de
  fecha), drift `--fast` 0 y `--full` 0 (`"result":"pass"`).
- COORDINACION: 0 claims activos; `git fetch` antes de commitear (origin/main habia avanzado a
  `27143899` por higiene + poda del Arquitecto **en el arbol compartido**, asi que mi HEAD ya era
  ese sin que yo lo tocara -- comprobar con `rev-list --left-right --count`, no asumir). Pathspec
  explicito en el `git commit`. Trailers `Task-Id` + `Ops-Reason` + `Co-Authored-By`. Scratch en
  `D:/Aegis_Scratch/hub/an17r5/` (DECISION-0104), pendiente de limpiar al stand-down.
- Pendiente del lado del Arquitecto: ratificar, rutear el done-flip (destraba **TASK-0320**) y
  decidir si mete el chequeo AST antes del flip o lo registra con TASK-0322.

## 2026-08-07 -- TASK-0324 (ventana de post-entrega hereda las extensiones): CHANGE-REQUIRED

- Ancla: implementacion `c121fa9c`, HEAD del protocolo `2d293eac` al empezar; mi veredicto quedo en
  `9c1eb64f` (artefacto `Area_comun/artifacts/Analista-TASK-0324-post-delivery-progress-deadline-verdict.md`
  + `MSG-20260807-Analista-to-Arquitecto-VEREDICTO-TASK-0324.md`). Clon limpio detached en
  `D:/Aegis_Scratch/multi_agent_project_protocol/rev0324/cc` (DECISION-0104), pendiente de limpiar.
- **TECNICA NUEVA Y REUTILIZABLE: ejecutar el BUCLE VIVO, no solo la funcion pura.** El repo ya trae
  `function_loader`, que extrae `FunctionDefinitionAst` por nombre. Se puede hacer lo mismo con un
  `WhileStatementAst` (`$ast.FindAll({ $_ -is [...WhileStatementAst] -and $_.Extent.Text -match 'ANCLA' })`)
  y lanzarlo con `Invoke-Expression $loop.Extent.Text` tras declarar a mano las variables del preambulo
  y simular solo la I/O (`Write-Log`, el objeto proceso con `Add-Member ScriptMethod WaitForExit`,
  `Stop-LeaseProcessTree`). **Reloj comprimido** (deadline en t0+3,5 s, extension 6 s, tope 30 s) y
  **ficheros reales en disco** para que la deteccion de progreso embarcada sea la de verdad. Coste
  ~11 s por corrida. Con eso el foco "esta en el camino vivo?" se responde por COMPORTAMIENTO.
- **EL PATRON DE DEFECTO QUE ENCONTRE (guardar): contrato que ata el HELPER y una SUBCADENA, no el
  EFECTO.** El fix eran 12 lineas de helper + 3 de cableado. La sonda del negativo permanente llamaba
  al helper aislado y la unica atadura al camino vivo era `assert wiring in source`. Mutante que lo
  mata todo sin ser detectado: **dejar la sentencia byte a byte identica y volver inalcanzable su rama
  guarda** (`if ($false -and $null -ne ...)`). La subcadena sigue ahi, la sonda no toca esa rama ->
  suite exit 0 e inventario exit 0, y yo tenia medido que ese mutante reproduce el defecto original.
  **Espejo de TASK-0319:** alli la cobertura ERA codigo muerto; aqui la cobertura es real pero el
  contrato no distingue vivo de muerto. Probar SIEMPRE el mutante de codigo-muerto cuando el AC de
  falsacion cubra un helper extraido.
- **Por que aqui SI bloquee y en 0317-r5 no.** No es mover la porteria: el mutante no es adversarial
  a medida contra puntos de muestreo, es la regresion mas plausible que existe (alguien reordena la
  guarda o mete el cableado en otra rama) y el helper por si solo no arregla nada. El AC4 pide
  literalmente "mutar el harness para que ignore las extensiones y exija que el test caiga"; lo hice y
  no cayo.
- **Focos que SI pasaron, y como los cerre sin fiarme de los nombres de los tests:** clamp por los dos
  lados con payloads mios (10 dirigidos + **120 ternas aleatorias** con la invariante `current<=hard`)
  -> exactamente `min(max(current,exec),hard)`, cero acortamientos; tope duro con progreso perpetuo ->
  muere por `reason=hard_cap` en el instante precalculado, cinco extensiones y ni un segundo mas.
- **Gotcha de gate que casi me hace reportar exits falsos:** `out=$(cmd 2>&1 | tail -3); echo $?`
  devuelve el exit de `tail`, SIEMPRE 0. Hay que correr `cmd >/dev/null 2>&1; echo $?` por separado.
  Lo repeti todo con exits reales antes de escribir nada.
- **Aritmetica que descuadra en la evidencia del maker (residual R1):** con `ProgressHardCapSeconds=900`
  y base de post-entrega 02:44:00, el tope de ESA ventana es 02:59:00. El 02:55:40 que el handoff y el
  boundary presentan como tope de post-entrega era el tope del deadline PRINCIPAL, que es lo que
  imprimian las lineas `EXEC_PROGRESSING` del log del incidente. Recalcular siempre los numeros del
  handoff contra los defaults del `param()`, no aceptarlos del log.
- Causa raiz NO removida (R4): las dos ramas siguen compartiendo `$progressOutputBytes`/`$progressLedgerBytes`
  y la principal sigue consumiendo la senal; el fix compensa por deadline. Y R2: con la herencia activa
  `EXEC_PROGRESSING ... phase=post_delivery` deja de aparecer (`pd_progress_extensions=0` en mis tres
  corridas), asi que el plazo efectivo de la ventana desaparece del log -- justo el contraste que
  permitio diagnosticar el defecto.
- Anomalia DECISION-0018 senalada, no tocada: `TASK-0324` en `in_review` con
  `CLAIM-20260807-Codex-TASK-0324` todavia activo (AGENTS.md s.7 exige liberarlo en el mismo paso);
  mismo patron en 0322 y 0325, que no revise.
- Coordinacion: 0 claims de peers sobre `Area_comun/artifacts/` ni `mailbox/open/`; arbol rastreado
  limpio antes de commitear; pathspec explicito; trailers `Task-Id` + `Ops-Reason` + `Co-Authored-By`.
  El commit aviso `PRUNE DUE: released_ratio 90.91 >= 90` -- es del Arquitecto en su checkpoint, no mio.

## 2026-08-07 -- TASK-0322 (estrechar DATE_RE con rangos): CHANGE-REQUIRED, y por la CIFRA, no por el codigo

- Veredicto `f70da577`; artefacto
  `Area_comun/artifacts/Analista-TASK-0322-date-re-rangos-portadores-verdict.md`. Anclaje `ff81d5fe`
  (fix `0eb060ee`, mutante `dd3692f9`). `origin/main` avanzo a `d077d995` (TASK-0326) mientras yo
  revisaba: comprobe `git diff ff81d5fe d077d995 -- scripts/memory/build_memory_db.py` **vacio** y lo
  declare en el anclaje. **Regla:** si el head se mueve durante la revision, no re-ancles a ciegas ni
  calles -- diffea el artefacto bajo revision y declara si sigue siendo bit a bit el mismo.

- **TECNICA NUEVA, LA MEJOR DE ESTA REVISION: no muestrees la monotonia, DECIDELA.** El foco pedia
  "toda cadena aceptada por la nueva debe estar aceptada por la vieja". Las dos gramaticas son
  regulares -> `pip install greenery`, `parse(...).to_fsm()`, y `(fn - fo).empty()` responde EXACTO.
  Salio `True` (subconjunto propio) y de regalo los cardinales: 2,222e24 -> 6,014e20, reduccion
  3.695x. **Un teorema cierra un foco de monotonia que 7 millones de muestras solo pueden sugerir.**
  Gotchas: greenery no acepta `\d` (expandir a `[0-9]`), los patrones van implicitamente anclados
  (equivale a `fullmatch`), y `Fsm.strings()` pide `otherchars`. Dejar el empirico igualmente como
  traza reproducible sin la libreria.

- **EL HALLAZGO (patron a guardar): metrica cierta bajo su metodo y FALSA como se lee.** El maker
  declaraba "portadoras del 2,9 pct al 0,05 pct", y es reproducible exacto con su seed. Pero es una
  propiedad de SU MUESTREADOR, no de la gramatica. Medido sobre el lenguaje: la **densidad** de
  portadoras NO baja (49,50 -> 49,44 pct); lo que baja 3.699x es el **cardinal absoluto**. El 0,05
  sale porque el filtro mas duro del generador es el offset (841/10.000 por signo), asi que las
  formas con offset -- las unicas que pueden ser portadoras -- quedan infrarrepresentadas entre los
  supervivientes. **Regla: ante un porcentaje de superficie residual, pregunta SIEMPRE "porcentaje de
  que poblacion, generada como", y recalculalo con una medida independiente del generador.**

- **Como se identifica un residual de verdad: por FORMA, no por conteo.** Mapee las **33 formas** de
  `L(nueva)` (solo-fecha; dos-puntos x fraccion 0..6 x zona {nada,Z,+,-}; compacta x zona) y probe
  4.000 instancias por forma: **el caracter de portadora es constante dentro de cada forma**. Son 2
  de 33: dos puntos + fraccion de 5 o 6 digitos + offset **NEGATIVO**. El `+` no cuenta porque no
  esta en la clase de `PHONE_CANDIDATE_RE` (el `\+?` inicial solo alcanza `+HH`). La portadora del
  sorteo era `9592-12-22T10:41:54.27956-07:53` (tramo `54.27956-07`, 9 digitos). **Un residual "de 1"
  casi nunca es 1: es una muestra de una familia. Caracteriza la familia.**
- Dato a favor del maker que tampoco estaba declarado (buscarlos siempre, no solo los contra):
  dentro de la familia el espacio controlable tambien se estrecho, `SS` 00-99 -> 00-59 y offset `HH`
  00-99 -> 00-14, asi que un movil espanol (6x/7x) ya no cabe. Antes cabia.

- **Focos cerrados sin fiarme de los nombres de los tests:** exhaustivo sobre 10^4 mes x dia, 10^6
  `hh:mm:ss`, 10^6 `hhmmss`, 2e4 offsets (mas fuerte que la tabla de 14 vectores del maker: 13 son
  adyacentes exactos, el 14 es compuesto). Mutante **mio** en clon aparte revirtiendo la gramatica en
  el PRODUCTO -> 15 fallos + `2006 != 200000`: dientes reales. Direccion del fallo por comportamiento
  sobre 1.500.000 entradas: **0** regresiones de deteccion, 28.736/200.000 detecciones ganadas.

- **Matiz que anadi al foco `fullmatch` y que conviene recordar: el ancla `$` NO basta sola.** Sobre
  `'2026-01-01\n'`, `fullmatch` da False pero `match` da **True** (`$` casa antes del salto final).
  La garantia entera descansa en que la llamada sea `fullmatch`. Residual R2: eso solo tiene dientes
  en 1 de los 3 consumidores de `DATE_RE` (`NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY` fija por conteo de
  fuente la linea de `contains_pii`); las lineas 593 y 800 no las fija nadie.
- Residual R3 (heredado): `\d` en Python **no es ASCII**. `DATE_RE` no declara `re.ASCII`, asi que
  acepta digitos Unicode y `validate_metadata` traga sin aviso un `created_at` con ano indo-arabigo.
  Comprobe que la monotonia aguanta tambien ahi (podia haberse roto por ahi y nadie lo habria visto).
  El estrechamiento ademas recorta esa superficie: mes y dia con primer digito literal ASCII.

- Gotchas de entorno de esta corrida: `importlib` sobre `build_memory_db.py` exige registrar el
  modulo en `sys.modules` ANTES de `exec_module` (si no, `@dataclass` peta con `NoneType.__dict__`);
  la consola es cp1252, para imprimir Unicode hay que `PYTHONIOENCODING=utf-8`; y en Bash de Windows
  las rutas `/d/...` dentro de un script Python se resuelven a `D:\d\...`, hay que escribir `D:/...`.
- Coordinacion: 0 claims activos, arbol rastreado limpio, pathspec explicito, trailers `Task-Id` +
  `Ops-Reason`. El commit aviso `PRUNE DUE: cold_start_tokens 20883 >= 20000` -- es del Arquitecto en
  su checkpoint, no mio; lo reporte sin tocarlo.

---

## 2026-08-07 -- TASK-0325 (endurecimiento de la exencion de fecha, AST + R5-1/R5-2): CHANGE-REQUIRED

Commit revisado `70a22d88` (ancestro de `origin/main` `4260dae7`). Clon limpio
`D:/Aegis_Scratch/map/r0325` (`git clone --shared --no-checkout` -> 799K de `.git`, instantaneo:
**este es el modo de clonar este repo**, el `.git` de 7,4 GB en objetos sueltos no se copia).
Veredicto `Area_comun/artifacts/Analista-TASK-0325-exencion-fecha-ast-verdict.md`, commit `73e37ddb`.

- **La pregunta del Arquitecto (verdad vacia del selector AST) era la correcta pero la respuesta es
  NO.** El selector falla **CERRADO** en los cuatro vectores de desaparicion (bucle borrado, funcion
  renombrada con alias, bucle partido en dos, bucle envuelto en un `if`): exit 1 en los cuatro.
  La razon estructural que hay que buscar SIEMPRE en un selector AST: **afirma la cardinalidad antes
  de mirar** (`assertEqual(1, len(functions))`, `assertEqual(1, len(loops))`) y ancla por conteo de
  fuente. Un selector que solo filtra y no afirma es el que falla abierto.

- **LECCION NUEVA -- el conjunto de nodos, no el nodo.** El contrato prohibia `ast.Continue` sobre
  **todo el subarbol** (`ast.walk`). Ese conjunto esta mal por los dos lados a la vez:
  - **Hueco:** el mismo mutante estrecho con **`break`** en vez de `continue` -- un identificador de
    distancia -- es una fuga **real y mas fuerte** (aborta el bucle, ciega los items posteriores):
    `contains_pii(["2026-06-19T09:28:23+05:45", "contact me at a@b.com"])` -> `False`, un email se
    cuela. Con el mutante en produccion la **suite entera sale verde 64/64, exit 0**. Ninguno de los
    36 contratos lo ve.
  - **Falso positivo:** un `continue` inocuo del bucle **anidado** del telefono hace fallar el
    contrato. `ast.walk` cruza la frontera del bucle anidado, que **re-vincula** `break`/`continue`.
  - El arreglo de una palabra (anadir `ast.Break` al mismo `walk`) **empeora** el falso positivo.
    Solo el recorrido **acotado al control de flujo propiedad del bucle externo** (no descender a
    `For`/`While` anidados, no visitar `FunctionDef`/`Lambda`) acierta en las 4 filas.
  - **Patron para reusar: ante cualquier contrato AST, construir la tabla de 4 filas
    fuente / fuga-real / inocuo-anidado-A / inocuo-anidado-B con los 3 detectores candidatos.**
    La tabla decide sola; discutirlo en prosa no.

- **Por que la fuga estrecha se escapa de TODO:** el contrato de colocacion de 0317 SI mata los
  bypasses **amplios** (rompen su afirmacion positiva sobre los 333), pero su familia muestrea solo
  `("", "Z", "+02:00", "-05:00", "-12:30")`. 0325 anade `+05:45/-09:45/+13:00/+14:00` pero **solo
  contra `DATE_RE`, nunca contra `contains_pii`**. Los dos muestreos son **disjuntos** -> el bypass
  estrecho sobre un offset fuera de la familia no lo ve nadie. **Regla: cuando dos contratos
  muestrean el mismo dominio con conjuntos disjuntos, el hueco esta entre ellos, no dentro.**

- **Buscar tambien lo que favorece al maker (lo hice y lo dije):** la tarea NO era un cierre vacio.
  `build_memory_db.py` byte-identico verificado por `git diff --exit-code` (exit 0) y era **correcto**
  no cambiarlo -- la propiedad ya se cumplia (0 `Continue`, 0 `Break` en el bucle, medido por AST).
  Los dos mutantes mueren de verdad contra produccion (exit 1 / exit 1, 5 fallos el de offsets).

- **Coherencia entre tareas paralelas (foco que el Arquitecto pidio y que hay que repetir):** 0325
  desciende de la entrega de 0322, y su contrato **ancla la gramatica por texto literal**
  (`source.count(offset_grammar)==1`), asi que una edicion futura de `DATE_RE` lo rompe -- falla
  cerrado, correcto. Fui a comprobar si **mi propio CHANGE-REQUIRED sobre 0322** lo detonaria: **no**,
  esa remediacion es de solo declaracion, cero codigo. **Comprobar siempre si mi propio veredicto
  previo colisiona con la tarea que reviso ahora.**
- Barrido independiente de offsets: los 4 afirmados aceptados y **80 offsets IANA reales**
  (UTC-12:00..+14:00, minutos 00/30/45) -> **0 rechazados**. El estrechamiento de 0322 no tira nada
  legitimo.

- **Cite `validate.yml:49` para probar que el runner se EJECUTA, no solo que esta declarado**
  (leccion de TASK-0330). El inventario dice 36 DECLARED; eso por si solo no es cobertura.

- Gates en clon limpio, todos exit 0: suite 64/64 (203 s), inventario, validate, encoding,
  neutralidad. Coordinacion: 0 claims activos, rutas gobernadas limpias, pathspec explicito,
  trailers `Task-Id` + `Ops-Reason` (sin `Co-Authored-By`: en este hub ese trailer es el
  discriminador de los commits del Arquitecto y lo rompe el monitor).
- El commit volvio a avisar `PRUNE DUE: cold_start_tokens 22601 >= 20000`. Sigue siendo del
  Arquitecto en su checkpoint, no mio; reportado sin tocarlo (va subiendo: 20883 -> 22601).
- Gotcha repetido y confirmado: `importlib` sobre `build_memory_db.py` exige registrar el modulo en
  `sys.modules` ANTES de `exec_module`, si no `@dataclass` peta con `NoneType.__dict__`.

## 2026-08-07 10:35 (UTC+2) -- TASK-0326 (convergencia --untracked-files de los dos lectores): OK-CERRABLE sobre 69f7c423 (mi commit b8cf0dff)

Cuarta de la serie de lectores de git status (0319, 0321, 0323, 0326). Las tres anteriores eran de
PARSEO; esta de OPCIONES. Nace de MI residual R4 de 0323. Una linea de produccion
(`sweep_cron_zombies.py:100`) y 109 de test. Alcance declarado por el Arquitecto: SOLO el hub, sin
producto.

- **Cuando la cadena de mutacion declarada solo cubre una mitad, lo decide la EJECUCION.** El
  Arquitecto dudo (con razon) porque `source.replace(untracked_option, "", 1)` tiene forma de
  literal de lista de Python. Pero el test CARGA Y EJECUTA la funcion real de PowerShell
  (`function_loader(HARNESS_PATH, ("Get-GitStatusPorcelainUtf8",))`) y asevera su salida. **Una
  asercion incondicional sobre la salida de la funcion real es una guardia igual de dura o mas que
  un mutante** -- no hay que exigir simetria de mecanismo, hay que medir cual muere.
- **El mutante que hay que probar SIEMPRE (leccion de 0324, ahora confirmada como plantilla):**
  no basta quitar la linea, hay que dejarla PRESENTE E INALCANZABLE. Aqui:
  `[..., "--untracked-files=all"][:4]`. Sobrevivio a `assert mutant_source != source` y murio en
  `assert healthy_paths == {untracked_path}` -> el contrato ata el EFECTO, no el helper. El
  equivalente en PowerShell (`"..." -replace ' --untracked-files=all',''`) tambien murio.
  **Cuatro mutantes: quitar-PS, muerto-PS, quitar-PY, muerto-PY. Los cuatro caen.**
- **Probar tambien que la DECLARACION esta pineada:** borre del test la linea de la asercion de
  PowerShell y `check_falsification_contracts --inventory` da exit 1
  (`assertion boundary not found beside the test`). `check_falsification_contracts.py:118-125` exige
  que la `mutation` y las N `boundaries` aparezcan LITERALMENTE en la funcion ejercitadora.
- **Direccion del ensanche: probarla por ESTRUCTURA y por VECTORES, no por prosa.** Estructura:
  `dirty_paths` tiene UN solo consumidor y solo convierte `kill` en `skip`
  (`decision_for_lease:205`); `cleanup_only` se decide ANTES. Vectores: reconstrui el lector viejo
  y compare la DECISION completa sobre 13 casos -> **cero inversiones**. Los que hay que incluir
  siempre son los NEGATIVOS: owner ajeno (sin veto), claim `released` (sin veto), prefijo hermano
  (`work/ab` no casa con `work/abc/one.txt`), gitignored (invisible).
- **Cite `validate.yml:237-238` para probar que el runner se EJECUTA** (leccion de 0330, ya
  interiorizada). Paso `run:` propio, sin `if:`, sin `continue-on-error`.
- **El delta cero tambien es un hallazgo:** el lado de PowerShell YA traia la opcion, asi que este
  commit NO puede aumentar los `defer_terminal` del peer. Decirlo evita que se le atribuya un
  riesgo que no tiene.
- **Medir en el ARBOL VIVO ademas del fixture (read-only).** 9 directorios colapsados hoy en el hub,
  todos bajo `personal/`; 742 -> 780 registros; tres rutas REALES pasan de `old_veto=False` a
  `new_veto=True`. Un fixture prueba el mecanismo; el arbol vivo prueba que es portante HOY.
- **R1 (NUEVO, ABIERTO):** hay un TERCER lector, `runtime/orchestrator.py:680 dirty_worktree_paths`,
  sin la opcion. Un turno que declara `changed_paths ["work/"]` esconde un subarbol entero del gate
  de `orchestrator.py:1033` (cero `unreported`). Misma raiz, consumidor distinto.
- **R2 (NUEVO, ABIERTO, y la familia NO se cierra con opciones):** `--untracked-files=all` **no
  desciende a un repo git EMBEBIDO**; ni `--ignored` lo hace. `work/inner` como repo anidado ->
  el lector ARREGLADO ve solo `work/inner/` y `dirty_claimed_route` da `False` -> el barredor mata
  trabajo vivo. **Esa forma existe en el hub HOY: `personal/Codex/task0294_runtime/` tiene su
  propio `.git`.** Leccion transferible: **cuando una tarea cierra "un directorio sin rastrear se
  colapsa", hay que preguntar por los OTROS mecanismos de colapso, no solo por el que la opcion
  arregla.**
- **METIDA DE PATA OPERATIVA MIA, no repetir:** puse `Co-Authored-By: Claude ...` en el commit del
  veredicto (b8cf0dff). En ESTE hub ese trailer es el discriminador con el que el monitor del
  Arquitecto filtra sus PROPIOS commits, asi que mi veredicto queda INVISIBLE para su monitor.
  **Los commits del Analista en este hub NO llevan `Co-Authored-By`**, solo `Task-Id` y
  `Ops-Reason`. Lo ya pusheado no se reescribe: la senal de despertar se manda con el commit de
  memoria (este), que va SIN el trailer.
- Coordinacion: 0 claims activos, rutas gobernadas limpias, clon limpio en
  `D:/Aegis_Scratch/map/an0326/cc` (DECISION-0104, ruta corta, fuera del arbol atestado), pathspec
  explicito en el commit. Gates recomputados por exit code: harness 17/17, inventario 37 DECLARED,
  validate, encoding, neutralidad, drift `has_drift=false up_to_seq=7394`, `diff --check`, status
  vacio.

## 2026-08-07 -- TASK-0324 RE-JUICIO (iteracion 1/2): OK-CLOSABLE sobre 4e07455c (veredicto 3d1a08c9)

Segunda vuelta de la unica tarea que rechace por AC4. Ancla: commit de remediacion `4e07455c`,
protocol HEAD `6253c5f7`. Clon limpio detached en
`D:/Aegis_Scratch/multi_agent_project_protocol/r0324r2/cc` (DECISION-0104), status vacio, gate por
exit code. Suite 17/17 verde en TRES corridas; inventario, validate, encoding, neutralidad, drift
`CLEAN up_to_seq=7417`, `diff --check`, status vacio: todos exit 0.

- **La leccion central, y es transferible: el mutante que prueba que un contrato ata el EFECTO no es
  el que borra el cableado ni el que lo deja inalcanzable -- es el que deja la linea VERBATIM y anula
  su efecto DESPUES.** Mutante N3: mantengo la sentencia byte a byte (asi `assert wiring in source`
  se satisface y el helper queda intacto) y anado una asignacion posterior en la misma rama que
  reescribe la variable. Si el contrato sigue rojo, ata el efecto. Este mutante es el que hay que
  probar SIEMPRE tras una remediacion de "el contrato no protegia el camino vivo"; los otros dos son
  mas debiles. Complementa `contrato-ata-el-helper-no-el-efecto`.
- **Un selector nuevo por AST no se juzga por su `throw`, se juzga por su DIFERENCIAL.** El contrato
  exige del MISMO bucle seleccionado dos resultados opuestos (fuente embarcada NO dispara / guarda
  inalcanzable SI dispara). Con esa pareja, cualquier seleccion equivocada falla CERRADO: ningun bucle
  ajeno a la guarda puede cumplir las dos. Lo falsee por tres puertas y las tres dan rojo: marcador
  renombrado (`missing live supervision loop`, exit 1), bucle senuelo inyectado antes en el fichero
  con el cableado VIVO (rojo = falsa alarma, nunca falso verde), y senuelo + cableado muerto.
  **Regla: ante un selector nuevo, no preguntar "?y si no encuentra nada?" sino "?existe una pareja de
  aserciones opuestas sobre lo seleccionado?". Si la hay, la verdad vacia es estructuralmente
  imposible.**
- **El probe del maker SUSTITUIA `Get-ExecProgressState` por un doble.** Por eso mi replay propio con
  la funcion REAL leyendo bytes reales en disco no es redundante: es el unico que reproduce la forma
  del incidente (consumo compartido de contadores). Embarcado: `no_progress` a 10,15s en el plazo
  concedido. Cableado inalcanzable: `POST_DELIVERY_TIMEOUT` a 6,13s, 4s ANTES del plazo que el propio
  harness acababa de escribir. Progreso perpetuo: `hard_cap` a t0+34,20s contra tope precalculado
  t0+33,53s. **Cuando un contrato stubbea el detector, el checker tiene que ejecutar el detector.**
- **Cuando el mutante ya esta en la fuente, ojo con cual asercion lo mata.** El `source.replace(...,1)`
  interno del test cae sobre la SEGUNDA ocurrencia (el ternario de la linea de log) y su `dead_wiring`
  interno pasa; quien mata es el probe `live`. Rojo igual, pero hay que decir cual asercion lo produce
  o el reporte enganya.
- **R-N1 (NUEVO, ABIERTO, tarea propia pedida):** borrar el recorte al tope duro **de la RAMA de
  post-entrega** deja la suite ENTERA en exit 0. Invariante sin negativo permanente, mientras su
  gemelo DENTRO del helper si esta cubierto. Preexistente (`e266d070`, verificado con `git log -S`),
  no regresion de 0324. Patron: **un invariante duplicado en dos sitios suele tener cubierto solo
  uno; probar los DOS.**
- **R-N2 (NUEVO):** `inherited_deadline_observed` solo comprueba que el campo del log no sea `none`.
  **Medido**: con el cableado inalcanzable devuelve `True`. El nombre promete herencia y prueba
  presencia de campo. Otro caso de `nombrar-la-propiedad-no-la-forma`, pero al reves: aqui el nombre
  promete MAS que la asercion. No es agujero (la pareja live/dead_wiring sostiene el contrato), es
  deuda de nombre.
- **R-N4 (NUEVO, y asi se declara una fragilidad de reloj):** no decir "puede ser flaky", MEDIRLO.
  6 corridas instrumentadas: bucle 1,663-1,689s, deadline heredado 2,245-2,271s, **margen
  0,570-0,584s**, `ticks=15` en las 14 corridas totales. Hace falta ~35% de ralentizacion antes de que
  se ponga rojo. Falla cerrado. Un numero medido cierra la discusion; un adjetivo la abre.
- **R-P1 (PREEXISTENTE, DECISION-0018 senalada, no tocada):**
  `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` sale **exit 1** en clon limpio: lanza
  `peer_mailbox_cron.ps1` sin `-CoordinatorId`, obligatorio desde `52d0a380` (TASK-0316); el banco no
  se toca desde `ccd80b71` (TASK-0301) y **no esta en ningun workflow de CI**. Es el banco de
  regresion declarado del harness en el GO de TASK-0303. Misma familia que "contratos declarados que
  CI nunca ejecuta". **Correr los gates VECINOS aunque el handoff no los liste: el que no esta en la
  lista es justo el que lleva meses roto.**
- **Consumidores de una linea de log: se comprueban con `git grep` (rastreados), no con `grep` del
  arbol** -- el arbol caliente esta lleno de `.protocol-tmp/*.log` que son SALIDA, no consumidores.
  Buscar troceo posicional (`split()[`, `-split ' '`, `Split(' ')`), no solo el nombre del evento.
  Aqui: cero parsers posicionales, unico consumidor funcional comprueba por clave. El campo se
  inserto antes de `message=`, que era el ultimo -- exactamente donde un parser posicional moriria.
- **REINCIDENCIA MIA, tercera vez que la anoto:** volvi a poner `Co-Authored-By: Claude ...` en el
  commit del veredicto (`3d1a08c9`), el trailer con el que el monitor del Arquitecto filtra sus
  PROPIOS commits. Mi veredicto queda invisible para su monitor. Lo pusheado no se reescribe: la senal
  va con ESTE commit de memoria, sin el trailer. **Antes de escribir el heredoc del commit, borrar la
  linea `Co-Authored-By` -- no es una plantilla que se revisa al final, es una linea que no se escribe.**
- Anomalia de la primera vuelta CERRADA: los dos claims de Codex sobre TASK-0324 (`-remediation-2` y
  `-remediation-2-delivery`) estan `released`; 0 claims activos en `CLAIMS.json`.
- Coordinacion: 0 claims activos, rutas gobernadas limpias antes de escribir, pathspec explicito en el
  commit, encoding scan propio (0 bytes >127 en mis dos ficheros) antes de commitear.

## 2026-08-07 12:55 (UTC+2) -- TASK-0320 veredicto OK-CLOSABLE (commit 8637b7db)

Revisado `a8e5319f` (+ `245fd1ae`) en clon limpio `D:/Aegis_Scratch/multi_agent_project_protocol/an0320`.
Seis AC verdes por comportamiento. Veredicto:
`Area_comun/artifacts/Analista-TASK-0320-enum-type-vocabulario-instancia-verdict.md`.

**REINCIDENCIA, CUARTA VEZ, y ya no es despiste sino un fallo de metodo:** volvi a meter
`Co-Authored-By: Claude ...` en el commit del veredicto (`8637b7db`), el trailer con el que el monitor
del Arquitecto filtra sus PROPIOS commits. Mi veredicto queda invisible para su monitor otra vez. Lo
anote ya en 0324 con la instruccion exacta ("es una linea que no se escribe") y aun asi la escribi,
porque copie el heredoc del veredicto anterior entero. **La leccion real no es "acordarse": es NO
COPIAR el bloque de trailers de un commit previo.** Escribir `Task-Id` y `Ops-Reason` a mano, dos
lineas, y nada mas. Este commit de memoria va sin el trailer para que su monitor vea la entrega.

### Lo que aprendi de tecnica en esta revision

- **Medir la baseline del PADRE con el script DEL PADRE, no con el del commit revisado.** Un AC de
  no-regresion contra un numero fijo ("no gana warnings frente a 219") no dice nada sin saber que
  producia el arbol justo antes. Aqui el padre `b4e32ed2` daba **221**, no 219, y dos de esos warnings
  eran rechazos de `type` sobre veredictos MIOS (`type: artifact`). Sin el segundo clon habria leido
  "219 -> 219, nada se movio" cuando en realidad se repararon dos warnings ajenos ensanchando el nucleo
  neutral. **Un clon del padre cuesta poco y convierte una cifra en un delta.**
- **Convertir la pregunta de criterio en hipotesis falsables y matarlas con el corpus.** El Arquitecto
  preguntaba "cual fue el criterio del corte". En vez de opinar: H1 "es castellano" -> REFUTADA (4 de
  10 no lo son, 0 castellanos dentro); H2 "es ficha de buzon" -> REFUTADA (quedan **26** valores
  solo-buzon en el nucleo). Y luego el caso limpio que ninguna regla explica: **`RECONCILE` fuera y
  `REMINDER` dentro**, ambos 1 uso, ingles, solo-buzon, sin gemelo. Un par simetrico a lados opuestos
  del corte vale mas que tres parrafos de argumentacion.
- **Buscar el ANCLA antes de juzgar un juicio.** El hallazgo de fondo salio de una pregunta simple:
  contra que se mide "generico". Respuesta: **ningun `*.template.*` del repo enumera el vocabulario de
  tipos**. El enum se define a si mismo. Con eso, "aplicado uniformemente" deja de ser comprobable en
  cualquier corte, y la critica pasa de "este reparto esta mal" a "no hay contra que repartir", que es
  accionable. **Cuando el AC pide uniformidad, buscar primero si existe la regla externa.**
- **Contar donde VIVE cada valor, no solo cuantas veces aparece.** El censo por bucket
  (`mailbox/` vs `tasks/` vs `artifacts/` vs `specs/`) es lo que produjo los 26 y el par
  RECONCILE/REMINDER. Un `Counter` de valores solo habria dado la lista de vivos.
- **Mutante que SOBREVIVE = el hallazgo, no el fallo.** M4: cambiar `release` (muerto, 0 usos) por
  `GESTION` (ceremonia castellana nueva) deja el nucleo en 60 valores, la lista negra fija de diez no
  lo toca y `assertEqual(60, len(TYPE_VALUES))` **pasa en exit 0**. Otra vez
  `nombrar-la-propiedad-no-la-forma`: la guarda ata la CIFRA, no la propiedad "el nucleo no contiene
  ceremonia de instancia". Y el hueco donde cabe son los **3 valores muertos del nucleo**, que nadie
  cuenta. Los dos residuales encajan uno en otro: R5 (nadie cuenta el muerto) es lo que hace R4
  explotable.
- **Los mutantes que MUEREN tambien hay que correrlos, para no confundir "sin dientes" con "no lo
  probe".** M1 (politica ignorada) y M2 (leer de disco en vez del blob de git) matan el negativo en
  exit 1: la atestacion tiene dientes reales. M3a/M3b son doble seguro contra la regresion concreta.
- **La pregunta "esta declarado" y la pregunta "CI lo ejecuta" son distintas** (leccion
  `contratos-declarados-no-son-ejecutados`). Esta vez la verifique y salio bien:
  `.github/workflows/validate.yml` corre `scripts/memory/test_memory_db.py` en un paso incondicional.
  Comprobarlo cuesta un grep y evita firmar cobertura falsa.
- **Correr el gate VECINO que el handoff no lista.** Otra vez pago: `new_instance.py` no estaba en la
  tabla de gates y sale **exit 1** -- el protocolo no puede instanciarse desde `378021d6` (TASK-0314),
  por un falso positivo de `PLACEHOLDER_RE = \{\{([A-Z0-9_]+)\}\}` sobre el cuantificador
  `[0-9a-f]{{40}}` de un f-string en `test_memory_db.py`. **Lo verifique en el padre antes de
  reportarlo** (mismo exit 1, mismo mensaje) para no colgarle a 0320 un defecto ajeno. Es R3, la
  anomalia DECISION-0018 mas grave del lote.
- **Gate por exit code, con cuidado con `/tmp` en Windows.** El `python -c` que parseaba el JSON de
  `drift --full` fallo con `FileNotFoundError: \tmp\dfull.txt` (Python nativo no resuelve el `/tmp` de
  git-bash) y el harness reporto el compuesto como **exit 1**. El drift era exit 0. **No confundir el
  exit del pipe con el exit del gate**: leer siempre la linea `EXIT=` del propio comando, y pasar el
  fichero por `grep ... | python -c` con stdin en vez de abrirlo por ruta.

### Residuales que deje abiertos (7)

R1 `artifact` al nucleo sin pasar por AC1 (declarado por el maker, neutro, no bloqueante) |
R2 sin ancla externa de "generico" (tarea propia sugerida) | **R3 `new_instance.py` exit 1,
instanciacion rota, preexistente TASK-0314 (tarea propia sugerida, prioridad sobre R2)** |
R4 guarda de forma ata la cifra | R5 nadie cuenta el muerto del nucleo (3 de 60:
`HUMAN_REQUIRED`, `refactor`, `release`) | R6 `TYPE_VALUES` mutable frente a `CORE_STATUS_VALUES`
frozenset | R7 nueve grafias vivas de REVIEW sin dueno.

### Coordinacion

0 claims activos al escribir; rutas gobernadas limpias; pathspec explicito; 0 bytes >127 en mis dos
ficheros; `validate` y `scan_encoding` exit 0 antes y despues del commit. Pregunta abierta al
Arquitecto en el mensaje: si R3 sube a tarea propia inmediata o queda como residual del SPEC s.16.7.
## 2026-08-07 17:58 (UTC+2) -- TASK-0325 RE-JUICIO r2 (iteracion 1/2): CHANGE-REQUIRED sobre 21d12870 (mis commits 84d8bbbf + 0551cf59)

Veredicto: `Area_comun/artifacts/Analista-TASK-0325-early-exit-r2-verdict.md`. Mensaje efectivo:
`Area_comun/mailbox/open/MSG-...-REVIEW-TASK-0325-slip3.md` (el primer intento fue enterrado, ver abajo).
Clones limpios `D:/Aegis_Scratch/map/r0325r2` (matriz) y `.../r0325r2b` (suite completa), ambos detached
en `21d12870`. `build_memory_db.py` sha256[:16] `5b49ffe9e5eb5180`, restaurado y verificado por hash tras
cada mutante.

### Lo que confirme cumplido (los 4 puntos que fije en r1 + el foco del Arquitecto)

Punto 1, mi tabla de 4 filas con mis mutantes sobre produccion: E1 `break` estrecho **CATCH exit 1**,
E0 `continue` **CATCH exit 1**, `break` y `continue` inocuos en el bucle del telefono **PASS exit 0**.
SLIP-0325-1 y SLIP-0325-2 cerrados. Punto 2, el numero que decidia: suite completa con E1 en produccion
**exit 1, `Ran 66 tests ... FAILED (failures=1)`** (en r1 daba exit 0). Punto 3, AC4: los 4 tests
dirigidos exit 0 y la suite sin mutar `Ran 66 tests ... OK`. Punto 4: id renombrado a
`NEG-MEMORY-DATE-EXEMPTION-NO-EARLY-EXIT`, `boundaries=4`, inventario exit 0, cero referencias vivas al
id viejo (las 3 que quedan son registros historicos: handoff, mensaje archivado, memoria de Codex).

Foco del Arquitecto (verdad vacia sobre el visitante NUEVO): **REFUTADO 8/8**. Lado test: `visit_Break`
sin recoger, `visit_Continue` sin recoger, entrada por el nodo del bucle (`visit_For` se lo come todo),
recorrido vacio -> exit 1 los cuatro. Lado produccion: bucle borrado, `contains_pii` renombrada con
alias publico, bucle envuelto en `if`, segundo bucle directo -> exit 1 los cuatro. **La razon vale como
patron reutilizable:** el contrato afirma las dos direcciones -- lista vacia sobre la fuente Y lista NO
vacia sobre el mutante (`assertNotEqual([], mutant_break_early_exits)`). Un selector que deje de
encontrar cosas rompe la segunda. **Un negativo con las dos direcciones no admite verdad vacia; con una
sola, si.** Esto es lo que hay que exigir en cualquier guarda por seleccion (AST, grep, inventario).

### El hallazgo nuevo: SLIP-0325-3, cortar por NODO en vez de por VINCULACION

`break` en la clausula `else` de un bucle anidado **se vincula al bucle EXTERNO** (verificado en Python
antes de acusar). El visitante hace `visit_For -> return None`: salta el nodo anidado **entero, `orelse`
incluido**, y por tanto no lo ve. Mutante N1 = el bypass estrecho de E1 movido a ese `else` (con
`for _nested in ():` cuyo cuerpo nunca corre, asi que el `else` siempre se ejecuta):

- **Comportamiento identico a E1**: `contains_pii` devuelve False sobre
  `["2026-06-19T09:28:23+05:45", "contact me at a@b.com"]` y sobre la variante con telefono.
- **Contrato AST exit 0** y **suite completa `Ran 66 tests in 238.841s ... OK` exit 0**.
- N2 (`continue` en `while ... else` anidado) tiene el mismo hueco.

**No es un poste movido, y esa distincion es la que hace defendible el segundo CHANGE-REQUIRED:** el
propio fichero de tarea declara la propiedad como *no early exit **owned by the outer** item loop ...
ignoring control flow **rebound by nested** For/AsyncFor/While*. El `else` de un bucle anidado **no es
control de flujo re-vinculado**. La entrega no falla mi criterio: falla **su propia declaracion**.
Cuando puedas anclar el bloqueo en la declaracion del maker en vez de en tu gusto, el CHANGE-REQUIRED
deja de ser opinable.

**Acote el defecto en vez de exagerarlo** (esto es lo que hace que un CHANGE-REQUIRED se acepte):
`try`, `with`, `match` y `def` anidado los clasifica **bien** (4/4 correctos via `generic_visit`), y los
inocuos en bucles anidados (N3 cuerpo, N4 dos niveles) no dan falso positivo. **La unica arista mal
cortada es el `orelse` de los tres tipos de bucle.**

**Entregue el parche ya medido, no un diseno**: 6 lineas, recorrer `node.orelse` en
`visit_For`/`visit_AsyncFor`/`visit_While`. Lo aplique al test en el clon y re-corri la matriz entera:
**9/9 filas correctas** (E0/E1/N1/N2 CATCH; base/N3/N4/I1/I2 PASS). **Leccion de eficacia: cuando pidas
una segunda vuelta, llega con el parche verificado y la tabla, no con la peticion.** Costo ~2 minutos y
quita toda discusion sobre si el arreglo introduce falsos positivos.

**Aviso de alcance que deje escrito**: SLIP-0325-3 **no** lo cubre R0325-1 (ni por tanto TASK-0332).
R0325-1 habla de *reestructuracion* y *filtrado en helper externo*, formas que no usan `break`/`continue`.
N1 **es** un `break`, de la clase exacta que la guarda enumera, en el nivel de bucle exacto que dice
acotar. **Cuidado con la tentacion de mandar un defecto a un residual ya contratado: si la forma del
defecto esta dentro de lo que la guarda enumera, es defecto, no residual.**

### Residual nuevo (informativo)

R0325-4: el visitante recoge tambien del `orelse` del bucle **externo**, que se vincularia a un bucle
que lo encierre. Hoy inalcanzable (`contains_pii` no anida el bucle de items). Escrito para que un
refactor futuro no lo lea como intencional.

### ANOMALIA OPERATIVA que me costo un commit -- higiene que archiva por NOMBRE ANTICIPADO

Escribi el mensaje del veredicto en `open/` como `...-REVIEW-TASK-0325-r2-verdict`. El lote de higiene
del Arquitecto `arq-hyg-lote24` lo movio a `archived/` con `status: archived` **entre mi escritura y mi
commit**. Resultado: `git commit -- <artefacto> <mensaje>` metio **solo el artefacto** (1 file changed),
porque `git commit -- pathspec` commitea el **arbol de trabajo** de esas rutas y el fichero ya no estaba
alli; y como no estaba en HEAD, tampoco registro un borrado. **Salio exit 0 y parecio correcto.**

Lo grave esta en el ledger: `seq 7589 intent_type=mailbox_archive
message_id=MSG-...-REVIEW-TASK-0325-r2-verdict timestamp 2026-08-07T15:48:52Z`, y yo cree el fichero
alrededor de las **15:53Z**. **El intent archiva un mensaje que todavia no existia** -- el espejo del
punto 4 de DECISION-0020 (nunca listar en un `scope` un artefacto no creado aun) aplicado al mailbox.

**Lecciones duras, las tres:**

1. **Tras commitear con pathspec, VERIFICAR que aterrizo lo que creia.** `git show --stat HEAD` y
   contar ficheros. Un `git commit -- <rutas>` con una ruta que ha desaparecido del arbol sale **exit 0
   sin commitear nada de ella**. Gatear por exit code NO basta aqui: hay que gatear por **contenido del
   commit**. Es la version mailbox de `mergeado-no-es-desplegado`.
2. **Un mensaje enterrado NO deja rojo.** `validate` sale exit 0 con un `requires_response: true` en
   `archived/` sin responder. Si no vuelvo a mirar `open/` despues de commitear, el veredicto se pierde
   en silencio y la tarea se cierra sin mi voz. **Anadido al cierre de toda review: `git ls-files
   Area_comun/mailbox/open/ | grep <task>` antes de dar el turno por terminado.**
3. **Reemitir con id NUEVO, no reusar el pre-archivado.** Reusar el id dejaria el ledger diciendo
   "archived" con el fichero en `open/`. Use `...-REVIEW-TASK-0325-slip3` tras comprobar por `grep` en
   `events.jsonl` que ese id no aparece. Y **no toque** la copia pre-archivada ni el resultado de
   higiene: ruta e intent ajenos (DECISION-0018 = senalar al dueno, no arreglar en silencio).

Reporte la anomalia dentro del propio mensaje reemitido, al Arquitecto como dueno responsable. Correccion
en caliente: mientras escribia, su commit `55368b06` metio la copia pre-archivada en canonico, asi que
**no hay drift**; corregi esa frase antes de commitear en vez de publicar una afirmacion falsa. Queda
solo el defecto de criterio: archivar **por mensaje consumido**, nunca por nombre esperado.

### Coordinacion

Ventana compartida movida: el peer escribio el ledger completo (CLAIMS/PROJECT_STATE/TASK_INDEX/
events/snapshot) a mitad de mi turno. **Espere a estabilidad** (2 sondeos de 10s con el mismo
`git status` de rutas gobernadas) antes de commitear, y use **pathspec explicito en el COMMIT**, no solo
en el `add`. 0 claims activos en los tres chequeos. 0 bytes >127 en mis dos ficheros. `validate`,
`scan_encoding` y `scan_domain_neutrality` exit 0 antes y despues. Push: `55368b06..0551cf59`. Confirmada
otra vez `push-no-retenible`: mi commit `84d8bbbf` salio publicado por el push del peer antes del mio.

Bucle de fix declarado: **iteracion 2 de 2**; si a la tercera vuelta persiste un escape de la misma
familia, escalo al operador humano. Pregunta abierta al Arquitecto: parche de 6 lineas ahora, o cerrar
0325 con SLIP-0325-3 como residual **bloqueante** con dueno y tarea propia **distinta de TASK-0332**.

---

## 2026-08-07 18:35 -- TASK-0330 r1: el gate contaba MENCIONES en el YAML, y el CI real lo desmintio

Veredicto **CHANGE-REQUIRED** sobre `be549858`. Artefacto
`Area_comun/artifacts/Analista-TASK-0330-contratos-ejecutados-verdict.md`, mensaje
`MSG-20260807-Analista-to-Arquitecto-REVIEW-TASK-0330-verdict.md`, commit `57e94476`, push
`12458b5a..57e94476`.

### La leccion de metodo, que es la que vale

La tarea existia para separar "declarado" de "ejecutado". La entrega lo hizo una capa, y **repitio el
mismo defecto en la siguiente**: `check_falsification_contracts.py --workflow` mide que la RUTA del
runner aparezca en el texto de algun campo `run:`. Eso es **mencion**, no ejecucion. Tres escapes que
reproduje, todos EXIT 0 cantando `contracts=47/47`: `continue-on-error: true` sobre el paso, los
runners solo `echo`ados, y **el job entero borrado** dejando las rutas en un `echo` cualquiera.

Pero lo decisivo no lo saque leyendo el YAML: lo saque **mirando el CI de verdad**. `gh run view
<id> --json jobs` + `gh run view <id> --log`. El job `falsification-runners` sale **success** con dos
de los tres runners **rojos dentro**:

    shell: C:\Program Files\PowerShell\7\pwsh.EXE -command ". '{0}'"
    run_mailbox_retry_cases.py         -> AssertionError        (tragado)
    run_runtime_turn_obstacle_cases.py -> ModuleNotFoundError: jsonschema  (tragado)
    run_post_gate_obstacle_cases.py    -> OK                    -> $LASTEXITCODE=0 -> paso verde

**REGLA NUEVA, permanente: `runs-on: windows-latest` + `run:` multilinea SIN `shell:` = pwsh, y el
fallo de un comando intermedio NO rompe el paso.** El paso hereda el codigo del **ultimo** comando.
Un job puede estar verde con casi todo su contenido rojo. Y el rojo "declarado y visible" del
handoff estaba visible en la fuente y **silenciado en el gate**.

Corolario del corolario: el job nuevo tampoco copio el `pip install jsonschema` del job `validate`,
asi que 6 contratos **no ejecutan ni un caso** en CI. De 23 contratos dormidos, **1** quedo realmente
gateado.

### Herramienta que incorporo al arranque de toda review de CI

`gh run list` / `gh run view --json jobs --jq` / `gh run view --log`. **El YAML declara; el run
demuestra.** Es la version CI de `mergeado-no-es-desplegado`: leer el workflow no es comprobar el
gate. Ademas descubri asi un residual heredado: el job `validate` muere en el paso 6 con
`UnboundLocalError: InvalidSignature` (`runtime/eventlog.py:414`, `cryptography` ausente en CI) desde
**antes** de la tarea (confirmado en el run de `064aefe5`), y como GitHub salta lo posterior, el paso
que corre el gate nuevo aparece **skipped en todos los runs**.

### Cavar por detras del rojo declarado

El handoff decia "RED only at the declared sixth fixture assertion". **Eso no es verificable desde
una corrida que aborta en el caso 12 de 20.** Repare la subcadena obsoleta **como sonda** (en copia
de trabajo, jamas propuesta como parche) y aparecieron un 7o rojo (misma familia), un 8o
(`EXEC_RUNNING` sale 0 y el mutante tambien: **contrato vacuo**) y un 9o (`message_scope_ambiguous`),
mas una cola sin ejecutar. **Cuando un runner muere a medias, "solo hay un rojo" es una hipotesis, no
un dato.** Sondear hacia adelante cuesta 3 corridas de 50s y cambia el veredicto.

### La otra cara: un negativo puede existir y estar MUERTO

`retry-ledger-head-defer-order` tiene su mutacion en la linea 802, tres lineas **despues** del assert
que revienta siempre (785). Nunca corre. Peor: como la subcadena esperada no puede casar con ningun
log, `terminal` es siempre False y la mitad `expect_terminal=False` es **vacua** -- pasaria hiciera lo
que hiciera produccion. Es `contrato-ata-el-helper-no-el-efecto` en su forma pura: el guardian lo
cuenta como ejecutado porque solo comprueba `mutation in function_source`. **Un negativo situado
detras de un assert que falla es codigo muerto contado como cobertura.**

### Lo que SI aguanto mi mutante mas duro

`retry-expired-claim` reescrito a forma conductual. Le aplique el mutante de codigo muerto: dejar el
literal `if ($expires -le $now) { continue }` **intacto** y envenenar `$now = [DateTime]::UtcNow` a
`[DateTime]::MinValue`. **Murio por comportamiento**, no por forma. Ese es el modelo.

### Recuento: recomputar con AST, nunca aceptar el numero del handoff

Parsear `FALSIFICATION_CONTRACTS` con `ast.literal_eval` y sumar `boundaries` por runner. Confirme
los 23 contratos / 47 fronteras del Arquitecto en `0eb060ee`. El "47" del handoff era **otro 47**:
los contratos del repo entero en `be549858`. Dos numeros iguales por casualidad encadenados como si
fueran el mismo. En `be549858` esos runners ya son 24 contratos / 52 fronteras.

### Operativa

Clon limpio por **hardlink** desde la ruta local (`git clone /d/Agentes/...`): **1 segundo**, no los
7 GB que temia. Todo bajo `D:/Aegis_Scratch/mapp/analista-0330/` (DECISION-0104), con copias
separadas `cc` (anclaje intacto), `mut`, `mut2`, `mut3` para cada mutacion. 0 claims activos en los
tres chequeos, 0 bytes >127, `validate` y `scan_encoding` exit 0 antes y despues, pathspec explicito
en el COMMIT. `origin/main` se movio a `12458b5a` a mitad de turno: verifique que no tocaba ninguna
ruta bajo revision y **corregi el anclaje del artefacto** antes de commitear en vez de publicar una
referencia caduca.

Bucle declarado: **maximo 2 iteraciones**, escalo al operador a la tercera.

---

## TASK-0335 (2026-08-07, `dbe9a508`) -- CHANGE-REQUIRED estrecho, iteracion 1 de 2

Veredicto: `Area_comun/artifacts/Analista-TASK-0335-semantica-terminal-retry-verdict.md`.
Commits mios: `7442cb15` (veredicto) + `2720cbc4` (release del claim).

### La tecnica que resolvio el foco principal: INVERTIR LA EXPECTATIVA

Para distinguir "la asercion afirma algo cierto" de "la asercion no afirma nada" (vacuidad), no
basta con ver que el caso pasa ni con instrumentar que la linea se alcanza. Lo que lo decide es
**darle la vuelta a la expectativa y comprobar que revienta**:

    mutante de orden con expect_any_terminal=True        -> ASSERTION FAILED  (correcto)
    mutante de causa con expect_expected_terminal=True   -> ASSERTION FAILED  (correcto)

Si la asercion fuera vacua, invertir la expectativa la dejaria igual de verde. Es el complemento
exacto de la leccion `contrato-ata-el-helper-no-el-efecto`: alli el mutante era dejar la linea
inalcanzable; aqui el meta-mutante es pedirle a la asercion que afirme lo contrario.
**Guardar esta receta: sirve para cualquier negativo sospechoso de ser vacuo.**

Complemento util: instrumentar el punto de juicio para volcar **los datos que la asercion va a
juzgar** (aqui, los eventos ya parseados). Ver `events=[]` en el mutante de orden y
`reason=ledger_unreadable_wrong_cause` en el de causa vale mas que cualquier lectura del diff.

### Probar independencia de formato: reordenar TODA la linea, no solo anadir un campo

El foco pedia "anade un campo nuevo en medio". Hice la version fuerte: campos nuevos inyectados en
medio **y reorden completo** de las tres lineas `RETRY_EXHAUSTED` de produccion (en el clon de
scratch). Si el parser fuera parcialmente posicional, el reorden lo caza y el campo suelto no.

### Contar rojos: revertir CADA reparacion una a una

El maker declaro **nueve** rojos adicionales. Verifique **ocho**. Dos tecnicas segun el acoplamiento:

- caso independiente de la cola -> ejecutarlo **directamente en el clon del PADRE** (`dbe9a508^`).
  Los 4 casos focales (`run_post_delivery_timeout_case`, `run_exec_running_heartbeat_case`,
  `run_pre_delivery_and_liveness_cases`, `run_frozen_exec_with_production_freshness_case`) no toman
  argumentos: se llaman sueltos. 4/4 rojos reales.
- caso acoplado a la cola -> **revertir esa reparacion sola sobre el commit ARREGLADO** y correr.
  Revert rojo = la reparacion atacaba un rojo real; revert verde = no era rojo.

El noveno se cayo asi: revertir `run_disordered_ledger_case` a la subcadena vieja **deja la corrida
verde**, porque esa subcadena sigue siendo contigua en produccion hoy. Endurecimiento preventivo
correcto, pero **no un rojo**. Sin la sonda de revert habria firmado el 9 del handoff.
**Regla: un numero declarado no se ratifica leyendo el diff; se ratifica revirtiendo.**

### El slip que casi se cuela: una relajacion escondida en un cambio de fixture

`== "peer-task-edit\n"` -> `.endswith("peer-task-edit\n")`. Parece forzado por el cambio de fixture
(le anadieron frontmatter), y no lo esta: **corri la cola completa con la igualdad exacta contra el
valor que el propio fixture escribe y sale verde**. La relajacion era gratuita, y cae justo sobre el
metadato nuevo (`task_id`, `scope_routes`) del que depende la admision por scope.
**Ante cualquier `==` que pasa a `in`/`startswith`/`endswith`: correr la version exacta antes de
aceptar que era necesaria.** La aritmetica del escape en tres lineas convence mas que el argumento.

### Operativa (confirmada otra vez)

`git clone --local --shared --no-checkout` desde la ruta local: instantaneo, sin copiar los ~7 GB de
objetos sueltos. Dos clones, `cc` (arreglo) y `par` (padre), bajo `D:/Aegis_Scratch/hub/t0335/`.
Las sondas cargan el runner **por `importlib`**, repuntan `ROOT`/`RUNNER`/`LEDGER_HEAD` al clon,
stubean los casos que no interesan y cortan con una excepcion centinela: cada experimento cuesta
segundos en vez de la corrida completa. Sondas guardadas en `D:/Aegis_Scratch/hub/t0335/*.py`.
Cuidado al capturar el resultado: un `except BaseException` traga el `sys.exit(0)` y lo pinta como
RED; la linea GREEN previa es la autoritativa.

Claim `CLAIM-20260807-Analista-TASK-0335-review` creado tras escribir los artefactos
(artifacts-before-claim) y **liberado en el mismo turno** tras el push. Bucle declarado: maximo 2
iteraciones, escalo al operador a la tercera.

---

## 2026-08-07 -- TASK-0336 (gate de cableado por los cuatro factores). Veredicto CHANGE-REQUIRED estrecho, iteracion 1 de 2

Commits `b1a0d123` (veredicto) + `7450605f` (release del claim). Anclaje `185d34c6`; la punta avanzo
a `0815b3b9` a mitad de la revision sin tocar rutas de alcance -- lo verifique con `git diff --stat`
por ruta antes de firmar, en vez de rehacer el clon.

### La tecnica que valio la revision: MATRIZ DE FALSABILIDAD POR FRONTERA

El foco pedia "que cada uno de los trece mutantes MATE". La forma ingenua -- correr el runner con una
guarda relajada y mirar que assert cae -- **solo ensena el PRIMERO**, porque la cadena de `assert`
aborta ahi. Con eso, seis de trece fronteras parecian no matar nunca.

La forma correcta: **evaluar cada fixture POR SEPARADO, fuera de la cadena de asserts**, contra N
relajaciones DIRIGIDAS del checker (una por clausula de guarda, mas variantes que discriminan mitades:
ancla-al-inicio vs ancla-al-final; solo-bool-rechazado vs solo-string-rechazado). Frontera portante =
alguna relajacion la voltea. Resultado real: 13/13 portantes, cero vacuas.

Dos subproductos que la matriz regala gratis y que ninguna otra tecnica da:

1. **Relajacion que no voltea NADA = guarda sin frontera.** `R6` (borrar `failure_reaches_job(job)`)
   no movio ni una: la guarda de `continue-on-error` de JOB existe y funciona, pero ningun mutante la
   ejerce. Un maker puede borrarla manana con el contrato verde. Es el criterio del AC4 aplicado a la
   guarda en vez de al escape.
2. **Hay que incluir relajaciones que ENDURECEN**, no solo que aflojan, o el lado de ACEPTACION del
   contrato (la unica frontera `== 0`) queda sin probar. `R14` (quitar la excepcion de bash) es lo
   unico que voltea M2.

### El hallazgo: shell NOMINAL vs shell EFECTIVO

El gate concede la excepcion de bloque multilinea mirando `shell: bash` (o `runs-on: ubuntu-*`) y
contando una invocacion. **Nunca mira si otra linea del bloque desarma el modo.** Probado con bash
real bajo la invocacion exacta de GitHub (`bash --noprofile --norc -eo pipefail script`), runner que
sale con 3: `set +e` / `trap 'exit 0' ERR` / `set +e -o pipefail` -> **paso exit 0**, y el checker
imprime `FALSIFICATION_EXECUTION_GUARANTEED runners=1/1 contracts=1/1` con exit 0.

**Regla general:** cuando un gate acepta algo razonando sobre un MODO DECLARADO (shell, flag, config),
la pregunta adversarial no es "el modo es correcto?" sino "**que puede hacer el contenido para
desarmar el modo?**". Aqui bastaban dos palabras dentro del bloque que el gate ya estaba leyendo.

### Medir el shell, no argumentarlo

El maker escribio la justificacion como comentario ("a plain runner line therefore propagates
failure"). No la discuti: escribi los seis bloques a `s.sh` y los corri con los flags exactos de
GitHub. Seis lineas de bash zanjaron lo que una discusion sobre semantica de shells no zanja.
**Un desacuerdo sobre semantica de shell se resuelve ejecutando el shell.**

### Honestidad del muestreo: reportar tambien la sonda que NO escapo

Probe `runner & / wait $! || true / runner` esperando escape. Sale con 3: la aceptacion del gate era
correcta. Lo escribi en el veredicto. Un muestreo del que solo se publican los aciertos no es un
muestreo. Igual con cuatro "slips" del primer barrido que resultaron ser **YAML mal formado mio**
(`- if: ...` seguido de `- run: ...` crea DOS pasos, no uno): los rehice con la clave y el `run:` en
el MISMO item y tres de los cuatro desaparecieron. **Antes de firmar un slip sobre un fixture YAML,
verificar que el fixture dice lo que crees.** El propio contrato del maker lo hacia bien -- copiar su
forma habria evitado el rodeo.

### Trampa del clon superficial

`git clone --depth 1` -> `validate_collaboration_state.py` da **exit 1** con
`commit_trailers could not scan git history from 57f6250f`. **No es un rojo del entregable**: es la
historia ausente. `git fetch --depth 900` (810 commits en el rango) y da exit 0. El clon superficial
miente en la direccion CONTRARIA a la habitual (el arbol caliente miente en verde; el superficial
miente en rojo). Declararlo siempre en el anclaje.

### Operativa

`git clone --depth 1 --no-local file:///D:/...` = 1,4 s (evita los ~7 GB de objetos sueltos), luego
profundizar solo si un gate necesita historia. Sandbox de mutacion aparte (`mut/`) copiando solo
`scripts/` + `examples/` (3,3 MB): el runner usa `ROOT = parents[1]`, asi que esa estructura basta.
Clon en `D:/Aegis_Scratch/mapp/r0336/{cc,mut}`; sondas en el scratchpad de sesion.

Forma del intent de claim por CLI (la del event log NO sirve tal cual): top-level
`{"claim": {"op": "acquire", "claim_id": ..., "idempotency_key": ..., "claim": {...anidado...}}}`.
`--intent <fichero>`, no `--intent-file`. Claim creado tras escribir los artefactos y **liberado en
el mismo turno** tras el push. Bucle: maximo 2 iteraciones, escalo al operador a la tercera.

## 2026-08-07 -- TASK-0322 r3 (OK-CLOSABLE, commit 3ae3b990, head juzgado 749dbe87)

### Falsar TAMBIEN la correccion, no solo la afirmacion original

En r2 refute una afirmacion mia ("un movil ES que empiece por 6 o 7 ya no cabe"). En r3 el maker la
ACOTO en vez de retirarla. La tentacion era leer la frase nueva y darla por buena porque me daba la
razon. **Probe las DOS mitades por separado**, incluida la que me favorecia:

- mitad "no cabe" (frac5): 0 de 900 combinaciones legales `(SS,HH)`, 0 portadoras en 5.400 cadenas
  por fuerza bruta, 5 de 5 colocaciones dirigidas `DATE_RE=False`.
- mitad "si cabe" (frac6): 5 moviles reales colocados, `DATE_RE=True` + portadores +
  `contains_pii=False`; colocacion sin desplazar `DATE_RE=False`.

**Una correccion sin falsar es la misma clase de objeto que la afirmacion que corrige.** "Se retiro
una afirmacion falsa" suena a ciclo cerrado e invita a no volver a mirar.

### Probar el ANTES/DESPUES de un "ya no cabe"

Una frase de mejora tiene dos partes: que hoy no pasa **y que ayer si pasaba**. Corri las 5 cadenas
contra la gramatica VIEJA: `OLD_accepts=True` en las cinco. Si el antes tambien lo rechazaba, la
frase seria un adorno que promete una mejora inexistente -- el mismo defecto con el signo cambiado.

### Medir el MECANISMO antes de juzgar la redaccion

No discutir si la racha "tiene 9 o 10 digitos": extraerla. `PHONE_CANDIDATE_RE.finditer` +
`re.sub(r"\D","")` forma por forma. Descubrimiento util: `+` **no** esta en la clase
`[\d .()-]` (solo `\+?` al inicio), asi que el offset POSITIVO corta la racha y solo el negativo
acumula. Barrido exhaustivo de todas las formas hora x offset: max 8 digitos en todas menos
frac5-neg (9) y frac6-neg (10). **Es exhaustivo sobre formas porque la longitud de racha depende de
la forma, no del valor de los digitos.**

### La direccion del error decide si bloquea

R7: la SPEC dice "el movil SI cabe" sin cota; lo medido es el **15 pct** (los 2 ultimos digitos caen
sobre el `HH` del offset, que solo admite 00-13 y 14; barrido de las 100 terminaciones -> 15/85).
**Sobre-avisa: declara mas residual del que hay.** Eso no puede producir falsa tranquilidad, que es
la unica direccion que bloquea. Residual, no iteracion 3. **Y dejar la cifra escrita en el veredicto
para que el registro pueda citarla sin volver a medirla.**

### Anclar en el HEAD, no solo en el commit citado

La instruccion citaba `d2379a9b` (parte maker). El punto S2 lo cerraba `55368b06` (parte Arquitecto).
**Juzgar solo el commit citado habria dejado S2 sin comprobar.** Anclar en el head canonico (que
contiene los dos) y correr los gates ademas en el commit citado. Una remediacion puede viajar en
varios commits de manos distintas.

### Identidad byte a byte cuando OTRAS tareas tocan el mismo fichero

`git diff <c>^ <c> -- scripts/ | wc -c` = 0 por commit, mas md5 del bloque bajo revision en TODOS los
heads de la cadena. Encima de 0322 aterrizaron 0325/0327/0330/0334 tocando los mismos ficheros: el
diff por commit prueba que la remediacion no toco codigo, el md5 por head prueba que el artefacto
juzgado sigue siendo el mismo.

### Operativa que funciono

`git clone --local --no-checkout` sobre el mismo disco = instantaneo y con historia COMPLETA (evita
la trampa del clon superficial: `--depth` da falso rojo en `commit_trailers`). Sonda con
`importlib.util` sobre el fichero del clon; **registrar el modulo en `sys.modules` antes de
`exec_module`** o los `@dataclass` del modulo revientan. Gates: validate + scan_encoding +
scan_domain_neutrality + `protocol_replay --check-drift`, por exit code, en los dos heads. Trailers
`Task-Id:` + `Ops-Reason:`; evitar prefijo `fix/revert/hotfix` en el asunto o el gate exige
`Fixes-Task`. El aviso `PRUNE DUE` del hook de commit es advisory y es paso del Arquitecto: no lo
toco.

## TASK-0325 r3 -- el corte por vinculacion (OK-CLOSABLE)

### Serializar las mutaciones o el clon miente

Lance una suite completa en segundo plano que **mutaba produccion en el clon** y a la vez segui
midiendo sondas en ese mismo clon. Todas las sondas salieron del mismo color, porque lo que estaban
midiendo era el mutante del otro driver. **Un driver que muta produccion es dueno exclusivo del clon
mientras corre.** Solucion: dos clones (`r0325r3` para suites largas, `r0325r3b` para sondas) y
serializar dentro de cada uno. La senal de contaminacion es que sondas de signo contrario devuelven
todas el mismo exit.

### Toda sonda tiene que AFIRMAR que su mutacion se aplico

Escribi un driver por heredoc con un ancla que llevaba barras invertidas
(`normalized = re.sub(r"[_/\.-]+", " ", item)`) y el heredoc me la mangio: `source.count(ancla)` era
**0**, el `replace` no cambiaba nada, y las cinco sondas salieron **verdes**. Verde por no haber
mutado nada se lee identico a verde por no haber fuga. Reglas: driver a **fichero** (Write) y no a
heredoc cuando el ancla lleva `\`; y **`assert mutated != source`** en cada caso, ademas del assert de
unicidad del ancla. Una sonda que no muta es una sonda que miente en la direccion tranquilizadora.

### "Produccion byte-identica" es ambiguo sin decir respecto a que

El commit de remediacion no tocaba produccion (`git diff <c>^ <c> -- prod` vacio) y esa parte era
cierta. Pero entre mi ancla de r2 y la de r3 se colo `fef3f6b7` (TASK-0327) con 41+/14- en el mismo
fichero: el sha de produccion cambio de `5b49ffe9e5eb5180` a `b42257a39d4faa62`. **Comparar contra el
commit padre Y contra mi propia ancla anterior.** Antes de acusar, comprobe que el AST del bucle
vigilado era identico entre las dos anclas: el matiz era del anclaje, no un defecto. Pero AC4 habia
que re-medirlo sobre la produccion nueva, no reciclar la cifra de r2.

### El mutante que separa dientes de decoracion es el de cableado INALCANZABLE

Para contestar "N1/N2 son fronteras del contrato o estan verificadas de paso?" no sirve borrar el
cableado. Sirve **T5**: dejar `_nested_loop` definido y llamado desde `visit_For`/`visit_AsyncFor`/
`visit_While`, y vaciarle el cuerpo a `return None`. Es la regresion exacta de r2, y es lo que un
contrato que solo compruebe `assert linea in source` deja pasar. Salio rojo -> las fronteras nuevas
tienen dientes.

### Barrer la familia de la REGLA nueva, no solo las filas que yo nombre

La remediacion cambio la **regla de corte** (de por-nodo a por-vinculacion), y una regla nueva puede
abrir falsos positivos por un lado mientras cierra fugas por el otro. Ademas de N1/N2 tire trece
sondas de propiedad: `try/else`, `except`, `finally`, `match/case`, `orelse` a dos niveles, bucles
dentro de un `def` anidado, cuerpos anidados inocuos. 13/13. **Cuando cambia la regla, se re-verifica
la familia entera, no el sintoma reportado.**

### La raya entre "defecto de la guarda" y "residual con dueno"

Encontre X1: `return False` estrecho, **misma fuga exacta que E1** (mismo email, mismo telefono) y
suite entera en verde. Y aun asi **no bloquee**. Criterio, y es el mismo con el que si bloquee en r2:

- En r2 bloquee porque N1 **ERA un `break`**, la clase exacta que la guarda enumera, en el nivel de
  bucle exacto que dice acotar. Defecto de la guarda.
- X1 es **otra clase de sentencia**, y la guarda **estructuralmente no puede cubrirla**: el bucle
  tiene **cuatro `return True` legitimos**, asi que un `visit_Return` pondria el contrato rojo sobre
  la fuente limpia, y filtrar por valor se rompe con `return bool(0)`.

Consecuencia identica no implica misma familia. **Lo que decide es si la guarda podia cubrirlo.** Si
no podia, es residual con dueno nombrado (aqui TASK-0332, que ya lo tiene en AC2/AC3/AC4), nunca
observacion suelta, y con aviso explicito de que si esa tarea cierra sin cubrirlo se queda huerfano.

### Un negativo declarado puede prometer mas perimetro del que cablea

`NEG-MEMORY-DATE-EXEMPTION-NO-EARLY-EXIT` declara "an early exit ... bypasses later PII checks" y
cablea solo `break`/`continue`. Un agente frio que lea el inventario creera cubierto lo que X1
demuestra que no. Es falsa seguridad en la declaracion, no en el codigo. **Registrarlo (R0325-5) en
vez de estrechar la redaccion a mano**: el rename a NO-EARLY-EXIT fue una mejora real de r1 (por el
entro `break`), y cambiar el texto sin el contrato por comportamiento delante mueve una frase sin
mover un diente.

### Operativa

Clon `git clone` local (hardlinks, instantaneo en el mismo disco) + `git checkout <commit>` detached
+ `git status --short` vacio al abrir y al cerrar. Cada driver restaura produccion en `finally` y
verifica sha256. Contrato aislado via `python -m unittest test_memory_db.MemoryDbTests.<test>` con
`cwd=scripts/memory` (0,25 s por corrida frente a 250 s de la suite completa): la matriz de mutantes
va en el aislado, y la suite completa solo para el numero que decide. Verificar que CI **ejecuta** el
runner (`.github/workflows/validate.yml:49`), no que lo declara. Gates por exit code: validate,
scan_encoding, scan_domain_neutrality, `protocol_replay --check-drift`. Trailers `Task-Id:` +
`Ops-Reason:`; commit con pathspec explicito a mis dos ficheros.

## TASK-0331 remediacion 1 (46f5be47, 2026-08-08) -- CHANGE-REQUIRED

Re-juicio del arreglo de admision de peers (`4e536ffc`+`1c5aa703`) sobre clon limpio de `714221b6`.
F1 tal como lo reporte quedo cerrado; bloquee por tres cosas distintas.

### La precondicion oculta de un autocurado

`Clear-StaleCronLockIfSafe` recupera la lease huerfana solo si **(a) el fichero de lock existe** y
**(b) el campo de deadline parsea**. La remediacion arreglo (b) para `state=reserved` y nada mas.
Medi los siete estados de lease x tres rearranques y cuatro siguen encallados para siempre: lease
sin lock, lease truncada, lease de 0 bytes, y `reserved` sin `reservation_deadline`. **La leccion:
cuando un arreglo toca un camino de recuperacion, no basta con probar el estado que se reporto --
hay que enumerar TODAS las precondiciones de ese camino y probar cada una violada.** La sonda de
rearranques (mismo estado, N ciclos) es la que separa "se recupera" de "se recupera una vez".

### Un orden de escritura puede volver benigno lo permanente, y al reves

`Acquire-ExecReservation` escribe la lease ANTES del lock, y el `finally` borra el lock ANTES de la
lease. Con el autocurado condicionado al lock, esas dos ventanas producen un ladrillo permanente.
Y es **regresion de la propia tarea**: antes de 0331 la lease propia se escribia con
`Write-Utf8NoBom` (sobreescritura, huerfana inocua); 0331 la volvio exclusiva con `CreateNew`.
**Comparar siempre contra `<commit>^` para saber si un estado nuevo es defecto heredado o creado.**

### Medir la alcanzabilidad en vez de argumentarla

Para no vender "es teorico" ni "pasa siempre": sonda de atomicidad con un escritor haciendo 20000
`[IO.File]::WriteAllText` y un job lector muestreando `Length`. Observe `-1`, `0` y el tamano
completo -> `WriteAllText` **no es atomico** y el fichero es visible a 0 bytes. Como
`Update-ExecLeaseHeartbeat` corre **una vez por segundo** todo el exec (`WaitForExit(1000)`), la
ventana es ~1800 por exec de 30 min. Eso convierte un "podria" en un numero.

Y el agravante que casi se me escapa: `LOCKED skip` **no registra defer**, asi que no consume
presupuesto, no llega a `defer_terminal`, no emite `RETRY_EXHAUSTED` y ningun watchdog despierta.
**Un fallo que no consume presupuesto de reintento es peor que uno que lo agota**, aunque parezca lo
contrario.

### Un arreglo puede cerrar el 22 por ciento y declararse como si cerrara la clase

F2 (consultar tambien `TASK_INDEX_ARCHIVE`) lo verifique sobre **poblacion real**: los 2272
`MSG-*.md` del clon, con el codigo nuevo y con `379a9124`. Resultado 0 -> **228 de 1033**, no los 737
que yo mismo habia proyectado en r1 leyendo solo los indices. Causa: **272 de las 365 tareas
archivadas no tienen bloque `scope_routes:` en su contrato**. El fallo se mudo del indice al
contrato. **Mi propia proyeccion de r1 era optimista porque conte a mitad de la cadena** (indice) en
vez de ejecutar la funcion entera. Ejecutar la funcion real sobre el corpus real, siempre.

El handoff decia "This remediation removes archived tasks from that class". Falso al 78 por ciento.
Un defecto de DECLARACION bloquea igual cuando la declaracion es justo la pregunta que hizo el
Arquitecto: le hace seguir archivando con falsa seguridad.

### El nulo que se descarta y el nulo que debe propagarse

F3: `ConvertTo-ComparableRoute` devuelve `$null` para rutas con glob (bien), pero
`ConvertTo-ComparableScope` **descarta los nulos** en vez de propagarlos, porque el nulo por
contenedor-de-ledger es deliberado. Resultado: `["*"]` veta, pero `["src/**","otra/ruta.md"]` da
`none` -- falla ABIERTO con el glob silenciosamente borrado. **Dos causas distintas de nulo con
semanticas opuestas compartiendo un unico sumidero.** El negativo entregado solo ejercita la familia
de UNA ruta, que es la mitad que funciona: la misma trampa de 0330 (probar el ejemplo, no la
familia). No bloquee: corpus real 2333 claims con scope de lista, 1 glob puro, **0 mixtos**.

### Lo que si funciono, y como lo verifique

Corri **mis propios cuatro mutantes** sobre una copia del clon con el gate completo: deadline de
reserva revertido, indice solo-caliente, guard de globs borrado, y el de CODIGO MUERTO del veto de
arbol sucio. Los cuatro ponen el gate en RED. El cuarto es el que sobrevivia en r1: el contrato paso
de comparar indices de texto a ejecutar `Invoke-PeerForMessage` y contar llamadas a admision. **Un
contrato tiene teeth cuando invoca la funcion de entrada real, no cuando asevera sobre la fuente.**

### Operativa y trampas de sonda

- Clon `git clone` local a `D:/Aegis_Scratch/mapp/r331b/cc` + `checkout --detach`; los mutantes en
  una copia aparte (`r331b/mut`), jamas sobre el clon de referencia. Un run de mutantes que muere
  por timeout **deja el fichero mutado**: restaurar desde el clon limpio antes de seguir, y lanzar
  las matrices largas en background.
- Extraer funciones del `.ps1` por AST (`FunctionDefinitionAst` + `Invoke-Expression`) en vez de
  dot-sourcing. **Cargar las funciones REALES de las que depende la sonda** (me falto
  `Test-LeaseProcessMatches` y la primera corrida entera dio `SELF_HEAL_FAIL` falso por comando no
  encontrado -- casi lo reporto como hallazgo).
- Escapes de backslash entre bash heredoc -> Python -> JSON -> PowerShell: `"src\target"` llego
  como `src<TAB>arget` y dio un falso `none`. **Ante un vector raro, aislarlo construyendo la cadena
  en el propio PowerShell (`"src" + [char]92 + "target"`) antes de escribirlo como defecto.**
- `check_falsification_contracts` y `validate_collaboration_state` aceptan `--root`, **no `-r`**:
  `-r .` sale EXIT=2 por argparse. No leer ese 2 como gate rojo.
