# Veredicto Analista -- TASK-0394 (el conjunto adoptable excluye el arnes y las skills)

- Revisor: Analista (voz adversarial independiente).
- Fecha: 2026-08-18, hora local del reloj (UTC+2).
- Ancla canonica del PRODUCTO: `fe660a25` (fix) + `76bef8f6` (checkpoint), ambos ancestros de
  `origin/main` (`489a3ac9`). HEAD local del protocolo al arrancar: `97875a64`.
- Metodo: CLON LIMPIO (`git clone -s` -> `D:/Aegis_Scratch/protocol/an0394/cc`), `checkout 76bef8f6`.
  Ningun gate corrido en el arbol caliente.
- Alcance de producto declarado por el instructor: `scripts/upgrade_instance.py` y
  `scripts/upgrade_instance.ps1`. No se exige `npm test` ni el verde del job entero.

## Veredicto

**CHANGE-REQUIRED.**

Respuesta directa a la pregunta A del instructor ("es criterio o es una lista con otro nombre?"):
**sigue siendo una lista**, y el control que el propio AC2 exige como compensacion cuando se
mantiene la lista **no puede enrojecer** en la configuracion que se publica.

## Tabla vector por vector

| Vector | Resultado | Evidencia |
|--------|-----------|-----------|
| AC1 -- el conjunto cubre lo que se exporta | PASS | reporte contra `examples/minimal_instance`: 122 archivos; `scripts/harness/peer_mailbox_cron.ps1` aparece (linea 74); 5 rutas `scripts/harness/`; 9 rutas `skills/`; 5 rutas `scripts/instance_assets/claude-skills/`. Exit 0. |
| AC2 -- el criterio se DERIVA, no se enumera | **SLIP** | el criterio se enuncia en prosa ("arboles de herramientas reutilizables") pero se aplica como enumeracion `ADOPTABLE_RECURSIVE_ROOTS = ("scripts","skills",".githooks","runtime")`. Un fichero que SATISFACE el criterio escrito y vive fuera de los cuatro nombres queda excluido en silencio. |
| AC3 -- el hueco es detectable | **SLIP (defecto principal)** | el control es vacuo por construccion en la config publicada. Ver reproduccion abajo. |
| AC4 -- no ensancha hacia lo que NO debe viajar | PASS | censo sobre el reporte: 0 filas de `Area_comun/state/PROJECT_STATE.json`, `Area_comun/state/CLAIMS.json`, `Area_comun/mailbox/`, `Area_comun/decisions/`, `Area_comun/tasks/`, `__pycache__`. `personal/`, `runtime/state/`, `runtime/runs/` aparecen 1 vez cada uno y **solo en la cabecera de exclusiones**, no como fila de tabla. |
| AC5 -- el reporte dice lo que NO mira | PASS con residuo | la cabecera declara "Fuera del conjunto: ...". Omite `.claude/` y los perfiles reales no plantilla (`profiles/dotnet_enterprise`, `profiles/financiero_presupuesto`), que tampoco viajan. Ver R3. |
| Paridad de gemelos (punto C) | PASS en contenido, NO hay guardia | recomputado, no leido. Ver seccion Paridad. |
| AMPLIACION declarada EN alcance (bloque `out_of_scope`) | **SLIP** | ruta afectada `scripts/new_instance.py` NO tocada por `fe660a25`. Reproducido abajo. |
| Punto D (ruta de staging vs ruta consumida) | **CONFIRMADO** | reproducido abajo. Sale a tarea sucesora, no a esta, por instruccion explicita del instructor. |

## Defecto principal -- AC3: el control es vacuo por construccion

`scripts/upgrade_instance.py:119-126` define el control como una **diferencia de conjuntos entre
la lista por defecto y la lista efectiva**:

    required = collect_files(master, DEFAULT_ADOPTABLE_GLOBS) - {artefactos runtime}
    return required - collect_files(master, globs)

y `globs` sale de `adoptable_globs(master)` (`:69-79`), que devuelve `DEFAULT_ADOPTABLE_GLOBS`
salvo que `protocol.config.json` declare `upgrade.adoptable_globs`.

Medido en el clon limpio: `protocol.config.json` **no tiene clave `upgrade`** (valor `null`).
Luego `globs` ES `DEFAULT_ADOPTABLE_GLOBS`, luego `required` esta contenido en el sustraendo, luego
la diferencia es el **conjunto vacio para cualquier arbol master posible**. El control no puede
enrojecer. El gemelo `.ps1` (`:166-174`) tiene la misma forma y la misma vacuidad.

El control solo enrojece si alguien declara en el config una lista MAS ESTRECHA que la por defecto.
Ese no es el modo de fallo que TASK-0394 reporto: el defecto vivia **en la lista por defecto misma**,
hardcodeada, sin config de por medio.

### Reproduccion falsificable (perturbacion de la semilla, punto B del instructor)

El maker acredita su negativo con `scripts/new_subdir/exportable.py` contra la seleccion VIEJA.
Perturbe el directorio -- que es la variable que el AC nombra ("un directorio no cubierto") -- y el
control deja de morir. En el clon limpio, con `master = .`:

    # A. linea base, sin perturbar
    python scripts/upgrade_instance.py --instance examples/minimal_instance
    EXIT_A = 0

    # B. fichero generico exportable en un directorio raiz NUEVO (fuera de los cuatro nombres)
    mkdir -p tools ; printf 'def helper():\n    return 1\n' > tools/exportable.py
    python scripts/upgrade_instance.py --instance examples/minimal_instance
    EXIT_B = 0        <-- el AC3 exige 1. El control esta CIEGO.
    (stderr vacio: ni una linea de "ficheros genericos fuera del conjunto adoptable")

    # C. la semilla del maker, pero con la config PUBLICADA (sin override)
    mkdir -p scripts/new_subdir ; printf 'def helper():\n    return 1\n' > scripts/new_subdir/exportable.py
    python scripts/upgrade_instance.py --instance examples/minimal_instance
    EXIT_C = 0        <-- ni siquiera su propia semilla enrojece sin el override de config

    # D. la unica via que SI enrojece: declarar en protocol.config.json la lista VIEJA
    (inyectar upgrade.adoptable_globs = los 13 globs previos a fe660a25)
    python scripts/upgrade_instance.py --instance examples/minimal_instance
    EXIT_D = 1, 26 lineas en stderr, encabezadas por scripts/harness/peer_mailbox_cron.ps1

    # gemelo PowerShell, misma perturbacion B
    pwsh -NoProfile -File scripts/upgrade_instance.ps1 -Instance examples/minimal_instance
    EXIT_PS_B = 0     <-- mismo ciego en el gemelo

    # reproducibilidad (DECISION-0115): perturbacion B repetida
    EXIT_B_RUN2 = 0

Corridas mias: **dos** de la perturbacion B en Python, **una** en el gemelo PowerShell, mas la
linea base, la semilla del maker y el override de config. El verde del control es reproducible
en su direccion FALLIDA.

Lectura de la matriz A/B/C/D: el par que el maker declara (semilla con lista vieja = 1 frente a
semilla con conjunto derivado = 0) mide **"la lista vieja frente a la lista nueva"**, que es un
hecho historico ya consumado. No mide **"nace un directorio manana"**, que es el enunciado literal
del AC3 y la razon escrita en la propia tarea ("Sin esto, el siguiente directorio nuevo repite el
defecto en silencio"). B es la celda que discrimina entre esas dos lecturas, y B sale 0.

### Por que esto tambien deja el AC2 abierto

El AC2 admite explicitamente conservar la lista: *"Si se mantiene la lista, se entrega ademas el
AC3."* La entrega conserva la lista (cuatro raices enumeradas) y el AC3 que la compensa es vacuo.
La cadena logica no cierra por ninguna de sus dos ramas.

Sobre la asimetria que el instructor pide explicar: el comentario nuevo ("Los arboles son
recursivos por definicion") **si** elimina la asimetria `.githooks/**` + `runtime/**` recursivos
contra `scripts/*` de un nivel -- las cuatro raices son ahora uniformemente recursivas, y eso es
una mejora real. Lo que no deriva es **cual es una raiz**. `tools/` en la perturbacion B es un
arbol de herramientas reutilizables bajo cualquier lectura llana del criterio escrito, y sale
excluido sin que nada lo note. El criterio enunciado y el conjunto aplicado discrepan, y no existe
instrumento que mida la discrepancia.

## Segundo hallazgo -- la AMPLIACION declarada EN alcance no se entrego

El bloque `out_of_scope` de TASK-0394 contiene una AMPLIACION del Arquitecto (2026-08-15 22:22)
que se declara a si misma **dentro** de la tarea: *"no es una exclusion, es un caso concreto que
ENTRA en esta tarea ... Ruta afectada: `scripts/new_instance.py` ... Se resuelve aqui, no en tarea
aparte."*

`git show --stat fe660a25` no toca `scripts/new_instance.py`.

Reproducido por conducta, instancia real creada con la herramienta en el tier POR DEFECTO:

    python scripts/new_instance.py --source-template . --target <scratch>/inst \
        --project-name demo ...            (sin --tier, luego tier=coordination)
    -> OK: created protocol instance

    ls <scratch>/inst/skills/session-watchdogs.skill.md   -> EXISTE (viaja)
    ls <scratch>/inst/scripts/harness                     -> No such file or directory

    grep -n test_session_watchdog_filter <scratch>/inst/skills/session-watchdogs.skill.md
    -> 87: python scripts/harness/test_session_watchdog_filter.py

    cd <scratch>/inst ; python scripts/harness/test_session_watchdog_filter.py
    EXIT = 2   ("can't open file ... No such file or directory")

Causa en el codigo: `copy_peer_harness()` solo se invoca desde `copy_runtime_tier_files()`
(`scripts/new_instance.py:430`), que corre para tier `runtime`/`attested`. En `coordination` la
guia viaja y su prueba no, exactamente como la AMPLIACION lo describio hace tres dias. El adoptante
recibe una guia que cita una ruta que en su instancia no existe.

## Punto D -- CONFIRMADO. No lo meto en esta tarea

Reproducido por conducta, con divergencia real inyectada:

    # el master despliega las skills de gobierno desde el staging:
    #   scripts/new_instance.py:79       CLAUDE_SKILLS_SOURCE_DIR = "scripts/instance_assets/claude-skills"
    #   scripts/new_instance.py:501-507  copia  <staging>/X/  ->  <gov>/.claude/skills/X/

    printf '# divergent local copy\nthis differs from the master\n' \
        > <inst>/.claude/skills/mailbox-hygiene/SKILL.md      # DIVERGE del master a proposito
    python scripts/upgrade_instance.py --instance <inst>
    EXIT = 0

    filas sobre la ruta de STAGING (que la instancia no usa):
      | `scripts/instance_assets/claude-skills/mailbox-hygiene/SKILL.md` | nuevo | anadir a la instancia |

    filas sobre la ruta CONSUMIDA (`.claude/skills`):  0

Es decir: el informe recomienda anadir el fichero a una ruta de staging que nadie lee, y el fichero
que la instancia si consume -- deliberadamente divergente en mi montaje -- **no se compara jamas** y
no produce ninguna fila. `classify()` (`:138-151`) compara `master/rel` contra `instance/rel` a la
misma ruta relativa, y `.claude/**` no pertenece a ningun glob del conjunto.

El dato de campo del instructor (NOVA con 8 skills frente a 5 del master, tres nunca presentes en el
master, `mailbox-hygiene` en un tercer estado) es coherente con este mecanismo y no lo contradice.

Por instruccion explicita suya, **no lo cargo a TASK-0394**: queda como hallazgo confirmado para la
tarea sucesora. Recomendacion sustantiva para esa sucesora: el conjunto adoptable necesita un mapeo
`master_rel -> instance_rel` (hoy implicito e igual a la identidad) porque `new_instance.py` ya
reubica al menos una familia de ficheros; mientras la identidad sea la unica relacion posible, todo
master que se despliegue reubicado sera invisible al informe.

## Paridad de los gemelos (punto C) -- recomputada, no leida

Corri ambos contra la MISMA instancia y compare las salidas:

    diff <(reporte_py)        <(reporte_ps1)        -> 19 lineas de diferencia
    diff <(sort reporte_py)   <(sort reporte_ps1)   -> 0 lineas

Contenido **identico**. Las 19 lineas son puro ORDEN de filas: `sorted()` de Python ordena por
punto de codigo y `Sort-Object` de PowerShell usa el orden de la cultura, asi que `Area_comun/...`
y `profiles/...` caen en posiciones distintas. El `.ps1` recibio `.githooks/**` (el entregable E4
de TASK-0266 que llevaba semanas ausente) via la tupla compartida de raices.

**Respuesta a "existe algo que impida que vuelvan a separarse": NO.** La tupla de cuatro raices esta
duplicada literalmente en los dos ficheros y nada la contrasta. Censo en el clon limpio:
`grep -rln "ADOPTABLE_RECURSIVE_ROOTS|AdoptableRecursiveRoots"` devuelve exactamente los dos
ficheros de produccion y ningun test. `grep -rln upgrade_instance scripts/test_*.py
.github/workflows/` devuelve **cero**: no hay prueba ni paso de CI que ejecute esta herramienta.
La paridad de hoy es una coincidencia mantenida a mano, igual que lo era la de ayer.

## Falsa alarma declarada por el instructor -- no la persegui

Los 111 `.pyc` del arbol caliente: confirmo cero en clon limpio y no lo cuento como hallazgo.
Nota tecnica, no defecto: `excluded_runtime_artifact()` filtra `__pycache__` en el `required` del
control, pero `collect_files` los sigue recogiendo para `rel_files`; en el clon limpio no hay
ninguno, asi que no se manifiesta.

## Gates protocolares (clon limpio, gate por EXIT code)

    python scripts/validate_collaboration_state.py        -> exit 0  ("OK: collaboration state is valid.")
    python scripts/scan_encoding.py --root .              -> exit 0  ("OK: encoding scan is clean.")
    python scripts/scan_domain_neutrality.py --root .     -> exit 0

Drift: no evaluado en el clon limpio (el regenesis pide claves de firma no presentes en scratch);
el validador canonico, que es el gate declarado, sale verde.

## Residuos declarados

- **R1.** El orden de filas difiere entre gemelos (`sorted()` frente a `Sort-Object`). Contenido
  identico. Un `diff` directo de los dos reportes no sale limpio; hay que ordenar antes. Cosmetico,
  pero cualquier control futuro de paridad que compare byte a byte fallara por esto.
- **R2.** No existe ningun test ni paso de CI que ejecute `upgrade_instance` en ninguno de sus dos
  gemelos. La herramienta que decide que llega a las instancias no esta cubierta por el arnes.
- **R3.** La cabecera del AC5 omite `.claude/` y los perfiles reales no plantilla
  (`profiles/dotnet_enterprise`, `profiles/financiero_presupuesto`) de la lista de exclusiones,
  aunque tampoco viajan.
- **R4.** La instancia de tier `attested` no se pudo crear en scratch (`registry_anchor_missing`
  tras el regenesis: faltan claves). El punto D lo acredite sobre una instancia de tier
  `coordination` con la ruta consumida montada en la misma posicion relativa; el mecanismo que
  demuestro -- `classify()` solo compara la identidad de rutas -- es independiente del tier.

## Bucle de correccion esperado

1. **Remediacion (Codex):** que el control del AC3 mida el criterio contra el ARBOL, no la lista
   contra si misma. Forma minima que superaria mi perturbacion B: derivar la pertenencia de una
   propiedad observable del fichero (o, si se conserva la enumeracion, barrer el master en busca de
   ficheros genericos no cubiertos y enrojecer, con una lista de excepciones EXPLICITA y corta). El
   negativo que acredita la remediacion no puede ser `scripts/new_subdir/`: tiene que ser un
   directorio raiz nuevo, porque ese es el enunciado del AC.
2. **Ademas:** cerrar la AMPLIACION en `scripts/new_instance.py` -- o el arnes viaja en tier
   `coordination`, o la guia deja de citar lo que no va a estar. La tarea declara que se resuelve
   aqui.
3. **Gates afectados:** `python scripts/upgrade_instance.py --instance examples/minimal_instance`
   (exit 0), el par negativo/positivo del AC3 con la semilla perturbada, el gemelo `.ps1` con la
   misma perturbacion, `validate_collaboration_state.py`, `scan_encoding.py`,
   `scan_domain_neutrality.py`.
4. **Rejuicio independiente ANTES del commit de cierre.** Maximo **2** iteraciones; a la tercera
   escalo al operador humano.
5. **Punto D:** tarea sucesora, no esta. Mi recomendacion es no declarar desbloqueada la
   actualizacion de NOVA hasta que la sucesora exista, porque el ultimo eslabon sigue comparando
   una ruta que la instancia no consume.

## Recomendacion de cierre

**CHANGE-REQUIRED.** No cerrable en `76bef8f6`.

Lo entregado arregla el EFECTO que bloqueaba a NOVA -- el arnes y las skills ya viajan, y eso es
real y esta medido. Lo que no entrega es la GARANTIA que la tarea pedia para que no vuelva a pasar:
el detector que deberia enrojecer no puede enrojecer en la configuracion que se publica.

-- Analista, 2026-08-18
