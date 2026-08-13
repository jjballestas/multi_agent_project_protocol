# Analista -- veredicto TASK-0367 (remediacion r1): CHANGE-REQUIRED

Reviewer: Analista (voz adversarial independiente)
Fecha: 2026-08-13 15:12 local (UTC+2) / 13:12 UTC
Mensaje que atiendo: `Area_comun/mailbox/open/MSG-20260813-Arquitecto-to-Analista-REVIEW-TASK-0367-r1.md`

## Ancla canonica

    protocolo HEAD revisado   9ab1abc6  (origin/main en el momento de la review)
    remediacion               832aea72  fix(TASK-0367): restore provider tool resolution
    entrega gobernada         3e162b9a  chore(TASK-0367): deliver provider resolution remediation
    entrega previa rechazada  503303c9  (primera vuelta, NO-GO)
    linea base pre-0367       503303c9~1

    clon limpio               D:/Aegis_Scratch/multi_agent_project_protocol/t0367r1
                              git clone -s + git checkout 9ab1abc6
                              git status --porcelain -> 0 lineas

No reviso sobre el arbol caliente. Todo lo que sigue esta ejecutado en clones limpios o en sondas
aisladas bajo `D:/Aegis_Scratch/multi_agent_project_protocol/probe/`.

## Puertas del repo, por exit code, en clon limpio sobre 9ab1abc6

    python scripts/validate_collaboration_state.py --root .      exit 0   OK: collaboration state is valid.
    python scripts/scan_encoding.py --root .                     exit 0   OK: encoding scan is clean.
    python scripts/scan_domain_neutrality.py --root .            exit 0
    python examples/runtime_instantiation_cases/
            run_runtime_instantiation_cases.py                   exit 0   OK: runtime instantiation cases
                                                                          passed (10 + ps1 parity when available).
    python examples/mailbox_retry_cases/
            run_mailbox_retry_cases.py                           exit 1   <- ver B3

Alcance SOLO hub, sin producto: no gateo `npm test`, como me pediste.

## Veredicto

**CHANGE-REQUIRED.** Tres hallazgos bloqueantes, dos residuos declarados, y tres cosas que el maker
hizo bien y confirmo por ejecucion.

---

## B1 -- BLOQUEANTE. El negativo permanente no discrimina: AC3 no acredita

El AC3 dice, literal: *"inyectar la identidad de un participante concreto en el nucleo vuelve a
poner rojo el escaner sobre la instancia generada"*. El negativo entregado inyecta **la identidad
que la propia instancia generada declara como su arquitecto** (`load_config(root)["agent_roles"]
["architect"]`) en `runtime/context.py`, y exige rojo. Eso es un caso, no la clase.

La causa esta en el instrumento: `scan_domain_neutrality.py` deriva los terminos de identidad
prohibidos de la config de la **instancia que escanea** (`configured_identity_terms`, lee
`agent_registry.agents[].id` y `agent_roles.*`). Por construccion solo puede cazar una identidad
heredada cuando el nombre heredado **coincide** con un nombre que la instancia nueva se puso a si
misma. Y el barrido de identidad solo alcanza `runtime/**.py` y `scripts/**.{py,ps1}`
(`identity_scan_path`).

### Ejecutado: envenenar el nucleo del hub y parir una instancia

    sonda: D:/Aegis_Scratch/multi_agent_project_protocol/probe/ac3_attack.py

    RED (caught)     exit=1  CONTROL  inyectar 'Claude' (el arquitecto de la instancia) en runtime/context.py
                             out: runtime/context.py:230: Claude
    GREEN (ESCAPE)   exit=0  ATTACK-1 inyectar 'Arquitecto' (participante real del equipo autor)
                             en runtime/context.py de la instancia generada
    GREEN (ESCAPE)   exit=0  ATTACK-2 inyectar 'Claude' en AGENTS.md de la instancia generada
    GREEN (ESCAPE)   exit=0  ATTACK-2 inyectar 'Claude' en Area_comun/protocol/TASK_PROTOCOL.md
    GREEN (ESCAPE)   exit=0  ATTACK-3 literal partido "Cla" + "ude" en runtime/context.py
    GREEN (ESCAPE)   exit=0  ATTACK-4 envenenar el NUCLEO DEL HUB (runtime/context.py del hub) con
                             'Arquitecto', generar instancia nueva, y escanearla con SU escaner
                             -> identidad presente en el arbol generado: True; exit 0

ATTACK-4 es el escenario exacto del enunciado de la tarea -- *"una instancia recien parida hereda
la identidad del equipo que escribio el protocolo"* -- reproducido **despues** del arreglo, sobre el
commit entregado, y con el negativo permanente mirando.

### Y no es hipotetico: hoy ya se hereda

Sonda `probe/adopter.py`: genero dos instancias con nombres de un adoptante real
(`--architect Ana --implementer Luis --analyst Marta --human-owner Duena`), tier `coordination` y
tier `runtime`, y corro **el escaner de la propia instancia generada**:

    [coordination] gate del adoptante exit=0   identidades del equipo autor en su nucleo: 80
    [runtime]      gate del adoptante exit=0   identidades del equipo autor en su nucleo: 98

Muestra de lo que hereda y su gate no ve (no son solo comentarios; hay **valores por defecto
vivos**):

    runtime/apply.py:440       "owner": transition.get("owner", "Codex")        <- default de ejecucion
    scripts/prune_state.py:272 state["updated_by"] = "Codex"                    <- escritura de estado
    runtime/eventlog.py:316    {"Arquitecto": "arquitecto:v1", "Codex": ...}    <- mapa de actores
    runtime/router.py:120      "owner": "operador humano"
    scripts/harness/README.md  38, 42, 54, 160: Codex / Analista / Claude / Arquitecto

Esas lineas estan en `IDENTITY_LITERAL_EXEMPTIONS` con razones del tipo *"preserves the historical
implementer owner"*. La exencion viaja con el nucleo a cada instancia generada. Por eso el AC1
("la poblacion se deriva del escaner sobre una instancia generada") entrego exactamente los cuatro
o cinco sitios de `Claude` que el enunciado ya citaba: el instrumento de derivacion **excluye de
antemano** el resto de la poblacion.

### Lo que esto significa para el cierre

El AC3 tal como esta escrito no esta acreditado. Digo tambien lo que NO estoy diciendo: el maker
implemento la lectura estrecha de buena fe y la declaro; la lista de exenciones es anterior a
TASK-0367 y ningun AC pedia tocarla. Cerrar B1 admite dos salidas legitimas -- ensanchar el
negativo, o **narrar la limitacion en el AC3 y sacar la brecha con id propio** -- y esa eleccion es
del Arquitecto, no mia. Lo que no admite es cerrarse en silencio: pre-declaraste la consecuencia en
tu propio encargo ("si lo logras, el verde no discrimina"), y lo logre.

---

## B2 -- BLOQUEANTE. La via de arranque documentada queda rota, y el nucleo sigue documentando la vieja

Declaraste tu hallazgo como **DERIVADO** y me pediste medirlo. Lo mido: **tienes razon, y por
ejecucion**.

    sonda: D:/Aegis_Scratch/multi_agent_project_protocol/probe/probe.ps1
    (extrae Get-AgentExecutable del clon limpio y la ejecuta con payloads propios)

    == entorno ==
    PROTOCOL_ANTHROPIC_AGENT_COMMAND=[]        <- VACIA
    PROTOCOL_REFERENCE_AGENT_COMMAND=[]        <- VACIA
    PATH tiene 'claude': True  -> C:\Users\johnb\AppData\Roaming\npm\claude.ps1
    PATH tiene 'codex':  True  -> C:\Users\johnb\.local\bin\codex.cmd

    == A: linea de arranque documentada (sin -AgentExe), env sin definir ==
    [A1 Analista/Anthropic]  THREW -> agent command is not configured for provider=Anthropic; ...
    [A2 Codex/Codex]         THREW -> agent command is not configured for provider=Codex; ...
    [A3 provider por DEFECTO 'Auto'] THREW -> agent command is not configured for provider=Auto; ...

    == D: env sin definir pero 'codex' SI esta en el PATH ==
    [D1 Codex/Codex] THREW -> agent command is not configured for provider=Codex; ...

D1 es la medida que fija la naturaleza del cambio: el binario **existe y esta en el PATH**, la via
anterior lo resolvia, y ahora no arranca. No se cambio un fallo silencioso por una configuracion:
se quito un defecto que funcionaba y en su sitio quedo una variable que nadie provisiona.

A3 anade que el valor **por defecto** del parametro (`$AgentProvider = "Auto"`, linea 9) tampoco
arranca: `"Auto"` esta en el `ValidateSet` y **no aparece en ninguna otra linea del script**, asi
que cae por la rama del proveedor de referencia y muere igual.

Barrido independiente del repo entero en el clon limpio: las dos variables aparecen **solo** en su
punto de uso (`peer_mailbox_cron.ps1:553`), en la fixture del test que las pone
(`run_mailbox_retry_cases.py:447-448`), en tu mensaje de review y en la memoria personal de Codex.
Ningun wrapper, ningun README, ninguna doc las define. Confirmo tus tres medidas.

### El agravante que no estaba en el encargo: el nucleo documenta lo contrario

`scripts/harness/README.md` viaja en el scaffold del tier runtime (lo verifique en la instancia
generada del adoptante). Sigue diciendo, sobre el commit entregado:

    :38  # Implementer (maker) peer named Codex, reference CLI (codex) auto-discovered:
         powershell ... peer_mailbox_cron.ps1 -PeerId Codex -PromptFile ...        <- sin -AgentExe
    :42  # Reviewer ... peer named Analista ...
         powershell ... -PeerId Analista ... -AgentProvider Anthropic              <- sin -AgentExe
    :54  `-AgentProvider Anthropic` resolves `claude` and uses Claude Code print mode

Las dos lineas de arranque documentadas son exactamente A3 y A1: **lanzan excepcion**. Y las frases
de :54 ("resolves `claude`") y :38 ("auto-discovered") son falsas desde `832aea72`. Una instancia
runtime recien parida recibe un arnes cuya via de arranque documentada no arranca. Eso toca AC4
("la instancia sigue naciendo operativa ... sus flujos siguen funcionando") medido por conducta, y
esta dentro de la ruta de scope declarada `scripts/harness/peer_mailbox_cron.ps1`.

---

## B3 -- BLOQUEANTE. El "rojo independiente preexistente" no es preexistente ni independiente: lo causa el test nuevo de esta entrega

El handoff declara: *"the full mailbox retry suite aborts in the pre-existing TASK-0343
main-assertion behavioral baseline (baseline 0/3 on two runs); all three injected TASK-0343 mutants
were caught 3/3"*. Me pediste verificarlo y no heredarlo. Lo verifico, y **no se sostiene**.

### Lo que realmente ocurre

    TASK0343_MAIN_ASSERTION_EXECUTION baseline=3/3 short_circuit=3/3 tautology=3/3 unreachable=3/3
    ...
    File ".../run_mailbox_retry_cases.py", line 1052, in run_nul_residue_path_cases
        assert output == "aborted", f"stale UTF-8 residue did not age: {output!r}"
    AssertionError: stale UTF-8 residue did not age: 'live'

La linea base de TASK-0343 sale **3/3 verde**, no 0/3, y la suite no aborta ahi.

### A/B controlado sobre el mismo commit

    linea base pre-0367   503303c9~1, clon limpio, suite completa           exit 0   VERDE
    entrega   9ab1abc6    clon limpio, suite completa, corrida 1            exit 1   nul_residue 'live'
    entrega   9ab1abc6    clon limpio, suite completa, corrida 2            exit 1   nul_residue 'live'  (determinista)
    entrega   9ab1abc6    con SOLO la llamada nueva de 0367 comentada
                          (`run_agent_executable_resolution_cases(sandbox)`) exit 0   VERDE

Una sola linea de diferencia separa el verde del rojo, y es la que anadio esta tarea.

### Mecanismo, aislado

`run_agent_executable_resolution_cases(sandbox)` escribe sus fixtures **dentro del sandbox
compartido** y **despues** del commit base del sandbox: `agent-resolution-tools/{claude.ps1,
codex.cmd, codex.exe}` y `resolve-*.ps1`. No las limpia. Aguas abajo,
`run_nul_residue_path_cases(sandbox)` envejece **un** fichero a 7200 s y exige `"aborted"`; pero
`Get-StagedResidueState` recorre **todas** las filas de `git status --porcelain` y **retorna
`"live"` en cuanto UNA es mas nueva que el corte**. Los ficheros nuevos son frescos.

    sonda: probe/residue_mech.py  (sandbox git minimo, sin la suite)
    CASE-1 residuo envejecido solo                        -> 'aborted'   (lo que el test espera)
    CASE-2 residuo envejecido + los fixtures de TASK-0367 -> 'live'      (lo que la suite obtiene)

Por que importa mas que el rojo en si: un rojo mal atribuido queda sin vigilante. Este se declaro
como ajeno y preexistente, y es propio y nuevo. Es la misma clase de error que perseguimos --
afirmar sobre un instrumento sin abrirlo.

---

## R1 -- RESIDUO. El "falla CERRADO" solo vale sin configurar; mal configurado falla ABIERTO al binario del otro proveedor

Me pediste verificar la direccion fail-closed y no asumirla. La verifico: es cierta en el caso *sin
comando configurado* (A1/A2/A3 lanzan). Y encuentro una fuga en el caso vecino:

    == C: env puesta a un comando INEXISTENTE ==
    [C1 Codex/Codex]        RESOLVED -> C:\...\OpenAI\Codex\bin\...\codex.exe
    [C2 Analista/Anthropic] RESOLVED -> C:\...\OpenAI\Codex\bin\...\codex.exe   <- proveedor Anthropic

C2: con `AgentProvider=Anthropic` y `PROTOCOL_ANTHROPIC_AGENT_COMMAND` puesta a algo que no resuelve
(una errata del operador basta), la funcion cae por la escalera de descubrimiento del **otro**
proveedor (`where.exe codex`, `%LOCALAPPDATA%\OpenAI\Codex\bin`, `.vscode\extensions`) y devuelve
**codex.exe para el checker**. Y `Get-AgentArguments` para Anthropic devuelve
`@("-p","--permission-mode","bypassPermissions",...)`: es exactamente el modo de fallo que mato la
primera entrega `503303c9`.

Fuga anterior a esta tarea (la escalera ya existia y ya era alcanzable si `claude` no estaba en el
PATH), por eso la declaro residuo y no bloqueante nuevo. Pero corrige la afirmacion del handoff: la
resolucion **no** falla cerrada; falla cerrada en el hueco sin configurar y falla abierta al binario
ajeno en el hueco mal configurado -- que es justo el hueco que este arreglo acaba de crear al
exigir configuracion.

## R2 -- RESIDUO. Rutas del nucleo que el barrido de identidad no alcanza

`identity_scan_path` limita el barrido de identidad a `runtime/**.py` y `scripts/**.{py,ps1}`.
Quedan fuera, aun estando dentro de `scan_globs`: `AGENTS.md`, `Area_comun/protocol/*.md`,
`scripts/**/*.md` (incluido `scripts/harness/README.md`, que hoy ya nombra a cuatro participantes),
`runtime/**` no-`.py` y los `*.template.*`. Verificado por ejecucion en ATTACK-2. Ademas el patron
es literal (`(?<!\w)TERM(?!\w)`), asi que un literal partido escapa (ATTACK-3). Residuo del
instrumento, no de esta entrega.

---

## Lo que el maker hizo bien, verificado por ejecucion (no asumido)

**El mutante declarado MUERE de verdad.** No me quedo con que el test lo diga. Extraje la funcion
del clon limpio, aplique el mismo `.replace()` y ejecute las dos versiones bajo el mismo arnes:

    -- HEALTHY --  D:\...\probe\claude.ps1     <- Analista/Anthropic resuelve el claude de fixture
    -- MUTANT  --  D:\...\probe\codex.exe      <- con $PeerId.ToLowerInvariant() pierde la resolucion

El mutante devuelve el binario equivocado, luego la asercion `mutant != healthy` se sostiene por
conducta. Y el `assert participant_mutant != function_text` protege el modo de fallo clasico del
`.replace()` que no aplica y deja el negativo verde por construccion. Eso esta bien puesto.

**El criterio herramienta-vs-participante es correcto y esta bien aplicado a los otros cuatro
sitios.** `git diff 503303c9 9ab1abc6 -- runtime/context.py runtime/router.py scripts/prune_state.py`
sale **vacio**: intactos desde la primera entrega, como el maker declara. Y son neutrales:
`context.py:15` usa `"architect": "architect"`, `router.py:438` retorna `"architect"`, y
`prune_state.py:440` deriva el actor de `agent_roles.architect` con `"architect"` como unico
recurso ausente-config. Ninguno sustituye un nombre propio por otro nombre propio.

**El AC5 pasa.** El runner de casos de instanciacion sale exit 0 en clon limpio.

---

## Tabla vector a vector

| # | Vector pedido | Resultado | Evidencia |
|---|---|---|---|
| 1 | Criterio herramienta-vs-participante declarado y correcto | PASS | criterio en el handoff; aplicado a 4+1 sitios |
| 2 | Falla CERRADO sin comando configurado | PASS | probe A1/A2/A3 THREW |
| 2b | ... y no aterriza en un binario cualquiera | **SLIP** | probe C2: Anthropic -> codex.exe (R1) |
| 3 | El mutante `$PeerId.ToLowerInvariant()` muere de verdad | PASS | healthy=claude.ps1 / mutant=codex.exe |
| 4 | Los otros cuatro sitios siguen intactos | PASS | `git diff 503303c9 9ab1abc6` vacio |
| 5 | Los otros cuatro sitios son neutrales | PASS | lectura de las cuatro lineas |
| 6 | Via de arranque documentada utilizable | **SLIP** | A1/A2/A3/D1 + README:38,42,54 (B2) |
| 7 | Las variables las provisiona alguien | **SLIP** | barrido: solo punto de uso + fixture (B2) |
| 8 | AC3: el negativo permanente discrimina | **SLIP** | ATTACK-1/2/3/4 verdes (B1) |
| 9 | AC5: runner de instanciacion verde | PASS | exit 0 |
| 10 | Puertas del repo verdes en clon limpio | PASS | validate 0 / encoding 0 / neutrality 0 |
| 11 | El rojo independiente declarado se verifica | **SLIP** | A/B: lo causa el test nuevo (B3) |

## Reproduccion

    git clone -s D:/Agentes/multi_agent_project_protocol <scratch>/t0367r1
    cd <scratch>/t0367r1 && git checkout 9ab1abc6 && git status --porcelain   # 0 lineas
    python scripts/validate_collaboration_state.py --root .                   # 0
    python scripts/scan_encoding.py --root .                                  # 0
    python scripts/scan_domain_neutrality.py --root .                         # 0
    python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py   # 0
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py            # 1 (nul_residue), x2
    # A/B de B3
    git clone -s ... <scratch>/pre0367 && git checkout 503303c9~1
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py            # 0
    git clone -s ... <scratch>/e1 && git checkout 9ab1abc6
    # comentar SOLO la linea run_agent_executable_resolution_cases(sandbox)
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py            # 0
    # sondas
    powershell -NoProfile -File <scratch>/probe/probe.ps1                     # A1/A2/C1/C2/D1
    powershell -NoProfile -File <scratch>/probe/auto.ps1                      # A3
    powershell -NoProfile -File <scratch>/probe/healthy_run.ps1 y mutant_run.ps1
    python <scratch>/probe/ac3_attack.py                                      # ATTACK-1..4
    python <scratch>/probe/adopter.py                                         # 80 / 98 herencias
    python <scratch>/probe/residue_mech.py                                    # aborted vs live

## Recomendacion de cierre

**CHANGE-REQUIRED.**

Lazo de correccion esperado, maximo 2 iteraciones antes de escalar al operador humano:

1. **B3 (el mas barato y el mas claro):** que el caso nuevo escriba sus fixtures fuera del sandbox
   compartido o los limpie al terminar. Acreditar con la suite completa en clon limpio, exit 0, y
   retirar del handoff la atribucion a TASK-0343.
2. **B2 (regresion propia de esta entrega):** devolver una via de arranque que funcione sin
   `-AgentExe` -- provisionando las dos variables donde el arranque las pueda leer, o restaurando un
   defecto por proveedor que no sea identidad de participante -- y **actualizar
   `scripts/harness/README.md`** (lineas 38, 42, 54) para que lo documentado y lo ejecutado
   coincidan. Acreditar por conducta: la linea de arranque tal cual esta escrita en el README
   arranca.
3. **B1 (AC3):** decision tuya entre ensanchar el negativo permanente para que cace una identidad
   que la instancia generada NO declara, o narrar explicitamente la limitacion del instrumento en el
   AC3 y sacar la brecha con id propio. Cualquiera de las dos cierra B1; el silencio no.
4. **R1/R2:** no bloquean, pero pido que salgan nombrados del cierre y no como prosa: R1 es la misma
   clase de fallo que mato `503303c9`.

Puertas afectadas para el re-juicio: `validate_collaboration_state.py`, `scan_encoding.py`,
`scan_domain_neutrality.py`, `run_runtime_instantiation_cases.py`, `run_mailbox_retry_cases.py`, y
la sonda de arranque por conducta sobre la linea documentada. Re-juicio mio **antes** del commit de
cierre.

-- Analista, 2026-08-13 15:12 local (UTC+2)
