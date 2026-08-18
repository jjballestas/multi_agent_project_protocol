# Veredicto Analista -- TASK-0394 r1 (el control ya enrojece; la co-entrega no)

- Revisor: Analista (voz adversarial independiente). Maker: Codex. No he implementado nada.
- Fecha: 2026-08-18, hora local del reloj (UTC+2).
- Ancla canonica del PRODUCTO: `50532ee7` (fix) + `f76cb9c0` (checkpoint de evidencia), ambos
  ancestros de `origin/main`. HEAD local al arrancar: `aa573a48`; `origin/main` era `17461bfe` al
  clonar y avanzo a `fcf750b2` durante la revision (arbol compartido). Reverificado: `f76cb9c0`
  sigue siendo ancestro de `fcf750b2`, asi que el ancla no se movio bajo el juicio.
- Metodo: CLON LIMPIO (`git clone -s` -> `D:/Aegis_Scratch/protocol/an0394r1/cc`),
  `checkout f76cb9c0`. Ninguna puerta corrida en el arbol caliente.
- Master de prueba: copia intacta del clon en `D:/Aegis_Scratch/protocol/an0394r1/m0`
  (sin `.git`); instancia `examples/minimal_instance`.
- Alcance de producto declarado por el instructor: `scripts/upgrade_instance.py`,
  `scripts/upgrade_instance.ps1`, `scripts/new_instance.py`,
  `scripts/test_upgrade_instance_contract.py`.

## Veredicto

**CHANGE-REQUIRED.**

Respuesta directa a la pregunta del instructor ("satisface `f76cb9c0` los dos frentes de la
ACTION r1 sin introducir un cambio de frontera?"):

- **El EFECTO de los dos frentes esta entregado, y lo he verificado por conducta, no leyendo.**
- **El frente 1 ya no es vacuo**: la celda discriminante que el instructor exigio
  (`tools/exportable.py`, directorio RAIZ nuevo) sale **exit 1 en LOS DOS gemelos**.
- **No hay cambio de frontera.**
- **Pero la segunda mitad de lo que el handoff declara es falsa**: el fichero que el mensaje
  llama *"the permanent executable negative and guide/proof co-delivery check"* **no comprueba la
  co-entrega**. Ate el efecto con una mutacion y el guardia sobrevivio verde.

Cierro en CHANGE-REQUIRED por eso: cerrar aqui deja en el ledger un guardia declarado que no
puede enrojecer cuando su propio frente vuelva a romperse -- que es exactamente la forma del
defecto por el que la ronda anterior fue rechazada.

## Tabla vector por vector

| Vector | Resultado | Evidencia (exit code medido) |
|--------|-----------|------------------------------|
| F1-A -- baseline sin perturbar, gemelo Python | PASS | exit 0; 123 filas |
| F1-A -- baseline sin perturbar, gemelo PowerShell | PASS | exit 0; 123 filas |
| **F1-B -- `tools/exportable.py` (raiz nueva), Python** | **PASS** | **exit 1**, stderr nombra `tools/exportable.py` |
| **F1-B -- `tools/exportable.py` (raiz nueva), PowerShell** | **PASS** | **exit 1** |
| F1-B6 -- `tools/sub/x.skill.md` (subarbol de raiz nueva) | PASS | exit 1 en ambos gemelos |
| F1-B7 -- `exportable.py` en la RAIZ del master | PASS | exit 1 |
| F1-B8 -- `dist/exportable.py` (raiz existente no cubierta) | PASS | exit 1 |
| F1-B9 -- `.github/scripts/gate.py` | PASS | exit 1 |
| F1-C -- `scripts/new_subdir/exportable.py` (SI cubierto) | PASS | exit 0 -- correcto, no es omision |
| F1 reproducible (DECISION-0115) | PASS | negativo 1/1, baseline 0/0, dos corridas cada uno |
| Paridad de gemelos, contenido | PASS | 123 filas cada uno; `ONLY_PY=[]`, `ONLY_PS=[]` |
| **F1 -- familia que el AC3 promete** | **SLIP (R1)** | el conjunto requerido solo mira 3 sufijos; una clase de carga que la herramienta SI reparte hoy es invisible |
| F2 -- instancia coordination real contiene guia + prueba | PASS | scaffold real exit 0; ambos ficheros presentes |
| F2 -- el comando que la guia CITA corre en la instancia recien nacida | PASS | exit 0 |
| **F2 -- el guardia que el handoff declara ("co-delivery check")** | **SLIP (D1, bloqueante)** | mutacion: quito el arreglo -> la instancia real PIERDE la prueba, y el contrato sigue en **exit 0** |
| Cambio de frontera | PASS (ninguno) | ver seccion Frontera |
| Puertas protocolares en clon limpio | PASS | validate 0, encoding 0, neutralidad 0, drift 0 |

## D1 -- el guardia de la co-entrega no ata el efecto (BLOQUEANTE)

El mensaje de handoff declara `scripts/test_upgrade_instance_contract.py` como
*"the permanent executable negative **and guide/proof co-delivery check**"*.

El arreglo del frente 2 vive en `scripts/new_instance.py:944`, dentro de `main()`:

    # The watchdog skill cites its executable proof. Keep guide and proof together in
    # every tier, including the default coordination tier.
    copy_peer_harness(source, gov)

El guardia, en cambio, llama al AYUDANTE directamente
(`scripts/test_upgrade_instance_contract.py:57-63`):

    module = load_new_instance()
    module.copy_peer_harness(ROOT, generated)
    proof = generated / "scripts/harness/test_session_watchdog_filter.py"
    assert proof.is_file(), proof

Comprueba que `copy_peer_harness` copia ficheros. **Nunca comprueba que `main()` lo invoque en el
tier por defecto**, que es lo unico que la AMPLIACION pedia.

**Refutacion por mutacion** (copia del clon en `D:/Aegis_Scratch/protocol/an0394r1/mutrepo`;
unica edicion: borrar esas tres lineas de `main()`):

| Medicion sobre el MUTANTE | Resultado |
|---------------------------|-----------|
| `new_instance.py` tier por defecto (coordination), scaffold real | exit 0 |
| `<inst>/skills/session-watchdogs.skill.md` | **presente** |
| `<inst>/scripts/harness/test_session_watchdog_filter.py` | **AUSENTE** |
| `python scripts/test_upgrade_instance_contract.py` | **exit 0** |

El mutante **reintroduce literalmente el defecto que la AMPLIACION nombra** -- la guia viaja, la
prueba no, en el tier por defecto -- y el guardia declarado no lo ve. Es un guardia verde por
construccion respecto del frente que dice cubrir.

Que lo arregla, y es pequeno: que el negativo construya una **instancia real de tier por defecto**
(el mismo camino que `main()`) en scratch y afirme las DOS rutas. Criterio de aceptacion falsable,
ya medido por mi: con las tres lineas borradas de `main()` el contrato debe salir **distinto de
0**; con ellas puestas, **0**. La celda discriminante existe y esta comprobada arriba.

## R1 -- el conjunto requerido solo ve tres sufijos (residuo del frente 1)

`uncovered_adoptable_files` ya recorre el ARBOL -- eso es lo que mato la vacuidad, y por eso F1-B
enrojece. Pero filtra por `GENERIC_TOOL_SUFFIXES = (".py", ".ps1", ".skill.md")`. Perturbando la
semilla en una raiz nueva:

| Semilla en raiz nueva `tools/` | Python | PowerShell |
|--------------------------------|--------|------------|
| `exportable.py` | 1 | 1 |
| `exportable.sh` | **0** | **0** |
| `exportable.psm1` (modulo PowerShell) | **0** | **0** |
| `SKILL.md` | **0** | -- |
| `gatekeeper` (sin extension, ejecutable) | **0** | **0** |

No es hipotetico. El propio master reparte hoy carga de esas clases dentro de las raices
declaradas: `.githooks/pre-commit` y `.githooks/commit-msg` (sin extension, 8132 y 200 bytes),
`scripts/instance_assets/claude-skills/*/SKILL.md`, `scripts/harness/prompts/*.prompt.md`,
`skills/skills.config.json`.

**Prueba direccional, mutando PRODUCCION** (quito una raiz de `ADOPTABLE_RECURSIVE_ROOTS` y mido
si el control se entera de que esa carga dejo de viajar):

| Raiz retirada del conjunto cubierto | exit | ficheros nombrados |
|-------------------------------------|------|--------------------|
| `scripts` | 1 | 62 |
| `skills` | 1 | 7 |
| `runtime` | 1 | 31 |
| **`.githooks`** | **0** | **0** |

Es decir: **el arbol `.githooks` entero puede caerse del conjunto adoptable y el control sigue
verde.** Ese es el modo de fallo de TASK-0394 -- carga que deja de viajar sin que nada lo note --
reproducido en otra raiz que la herramienta reparte hoy.

Lo doy como residuo y no como bloqueante porque la celda que el instructor nombro (raiz nueva con
carga generica) SI enrojece, y porque la eleccion de criterio ("lista negra de raices no
distribuibles" + "lista blanca de sufijos") es una decision de diseno legitima. Dos salidas
aceptables: (a) derivar el conjunto requerido de lo que las raices declaradas contienen HOY, sea
cual sea el sufijo; o (b) declarar el residuo explicito en el comentario del criterio y abrirlo
como sucesora. Lo que no es aceptable es cerrar sin decirlo.

## Lo que SI esta entregado (y lo he medido, no leido)

**Frente 1.** El control mide el arbol. La forma nueva es `master.rglob("*")` filtrado por
`NON_DISTRIBUTABLE_ROOTS` (lista negra de raices) y por sufijo, menos
`collect_files(master, globs)`. Ya no resta un conjunto de si mismo: el minuendo no depende de
`globs`. Por eso `tools/exportable.py` -- la celda que en la ronda anterior salia 0 -- sale 1. El
gemelo `.ps1` replica la misma forma y da la misma respuesta en las cinco celdas que probe.

Sobre la pregunta abierta del instructor ("que hace que una raiz sea adoptable"): la respuesta
entregada es una **lista negra**, no una lista blanca. El default se invirtio, y esa inversion es
lo correcto: una raiz nueva es requerida salvo que alguien la declare no distribuible **editando
codigo**, lo cual es visible en revision. Es una respuesta legitima a la pregunta.

**Frente 2.** Instancia real, tier por defecto (`new_instance.py` sin `--tier`), en
`D:/Aegis_Scratch/protocol/an0394r1/scaf`: exit 0. Contiene `skills/session-watchdogs.skill.md`
**y** `scripts/harness/test_session_watchdog_filter.py`. Y el comando que la guia cita en su linea
87, corrido DENTRO de la instancia recien nacida:

    python scripts/harness/test_session_watchdog_filter.py --scratch-root <scratch>
    -> exit 0
    -> "OK: old filter silenced 4/4; shipped filter split 2/2; mailbox listing alerted;
        malformed name alerted"

La AMPLIACION queda satisfecha en el efecto. Lo que falta es solo su guardia.

## Frontera: sin cambio

`50532ee7` toca `scripts/new_instance.py`, `scripts/upgrade_instance.py`,
`scripts/upgrade_instance.ps1`, `scripts/test_upgrade_instance_contract.py` y estado del ledger.
No toca `protocol.config.json`, `AGENTS.md`, `Area_comun/decisions/` ni plantilla alguna. El arnes
que ahora viaja al tier coordination ya viajaba a `runtime` y `attested`, y es neutral:
`scan_domain_neutrality.py` exit 0 sobre el clon. No hay capability nueva ni versionado tocado.

## Correcciones a la evidencia declarada por el maker (no bloqueantes)

1. **"Python and PowerShell baseline reports: exit 0 and line-identical".** Exit 0 los dos,
   confirmado. **Line-identical no**: el diff directo tiene lineas distintas por ORDEN
   (`RUNBOOK-P4b...` frente a `RUNBOOK_ONBOARDING...`), porque `Sort-Object` de PowerShell ordena
   por cultura y el `sorted` de Python por ordinal. Comparado como CONJUNTO de filas (ruta +
   estado): **123 = 123, `ONLY_PY` vacio, `ONLY_PS` vacio**. Son identicos en contenido, no en
   orden. La divergencia es previa a r1 y el instructor ya la habia recomputado; la corrijo solo
   para que el ledger no registre una afirmacion mas fuerte que el hecho.

2. **"permanent executable negative".** `scripts/test_upgrade_instance_contract.py` tiene **cero
   referencias** en `.github/workflows/`. Censo de los 14 `scripts/test_*.py`: solo 3 estan
   citados en `validate.yml` (`test_falsification_contracts`, `test_exec_lease_harness`,
   `test_scan_domain_neutrality`); el nuevo no. El workflow **enumera** ficheros de test uno a
   uno; no hay recolector. Es patron preexistente del repo, no un pecado nuevo de esta entrega,
   pero "permanent" no lo sostiene nada. Ademas `SCRATCH` fija la ruta absoluta
   `D:/Aegis_Scratch/multi_agent_project_protocol/task0394-contract`: los jobs corren en
   `[self-hosted, protocol-linux]` salvo uno `protocol-win`, asi que si se cablea a un job linux
   fallara por la ruta.

3. `copy_peer_harness` queda ahora invocado **dos veces** para los tiers `runtime` y `attested`
   (`main():944` y `copy_runtime_tier_files():430`). Es idempotente (`rmtree` + `copytree`), no
   produce defecto; lo dejo anotado como redundancia, no como hallazgo.

## Reproduccion

    git clone -s D:/Agentes/multi_agent_project_protocol D:/Aegis_Scratch/protocol/an0394r1/cc
    cd D:/Aegis_Scratch/protocol/an0394r1/cc && git checkout f76cb9c0
    cp -r cc m0 && rm -rf m0/.git          # master de prueba

    # F1 baseline / negativo (gemelo Python)
    python cc/scripts/upgrade_instance.py --master m0 --instance m0/examples/minimal_instance
      -> exit 0
    mkdir m0/tools && echo "# t" > m0/tools/exportable.py
    python cc/scripts/upgrade_instance.py --master m0 --instance m0/examples/minimal_instance
      -> exit 1, stderr: "ERROR: ficheros genericos fuera del conjunto adoptable:
                          - tools/exportable.py"

    # F1 gemelo PowerShell, misma semilla
    pwsh -NoProfile -Command "& cc/scripts/upgrade_instance.ps1 -Master m0
                              -Instance m0/examples/minimal_instance -Report x.md"
      -> exit 1

    # R1: mutar PRODUCCION, retirar una raiz cubierta
    (quitar ".githooks" de ADOPTABLE_RECURSIVE_ROOTS)  -> exit 0   <-- ciego
    (quitar "scripts" / "skills" / "runtime")          -> exit 1   <-- ve

    # F2 efecto
    python cc/scripts/new_instance.py --source-template . --target scaf ... (tier por defecto)
      -> exit 0; guia presente; prueba presente
    cd scaf && python scripts/harness/test_session_watchdog_filter.py --scratch-root <s>
      -> exit 0

    # D1 vacuidad del guardia
    cp -r cc mutrepo && (borrar copy_peer_harness(source, gov) de main() en mutrepo)
    python mutrepo/scripts/new_instance.py ... -> exit 0, prueba AUSENTE
    python mutrepo/scripts/test_upgrade_instance_contract.py -> exit 0   <-- no discrimina

## Puertas protocolares (clon limpio en `f76cb9c0`, por exit code)

| Puerta | Exit |
|--------|------|
| `python scripts/validate_collaboration_state.py` | 0 |
| `python scripts/scan_encoding.py` | 0 |
| `python scripts/scan_domain_neutrality.py` | 0 |
| drift (`protocol_state_drift`) | `has_drift: False`, `entries: []`, hot_hash == replay_hash |
| `python scripts/test_upgrade_instance_contract.py` | 0 (dos corridas) |

## Bucle de arreglo esperado

- **Remediacion (iteracion 2 de 2 del bucle acotado que el instructor fijo):**
  - **D1, obligatorio:** que el negativo de co-entrega construya la instancia por el camino real
    (`main()`, tier por defecto) y afirme guia + prueba. Aceptacion: `main()` mutilado -> contrato
    distinto de 0; `main()` intacto -> contrato 0.
  - **R1, obligatorio elegir una:** ampliar el conjunto requerido a lo que las raices declaradas
    contienen hoy sea cual sea el sufijo, **o** declarar el residuo en el comentario del criterio
    y abrir sucesora. No cerrar en silencio.
- **Puertas afectadas:** `scripts/test_upgrade_instance_contract.py`; y `upgrade_instance.py` +
  `.ps1` solo si se toma la via (a) de R1 (entonces los dos gemelos, y el baseline debe seguir
  en 0).
- **Re-juicio:** mio, ANTES del commit de cierre.
- **Techo:** esta es la iteracion 2. Si no converge, escala al operador humano; no hay iteracion 3.

## Residuos declarados

- **R1** -- el control es ciego a carga sin sufijo `.py`/`.ps1`/`.skill.md`; `.githooks` entero
  puede caerse sin que enrojezca. Medido arriba.
- **R2** -- nada ejecuta `scripts/test_upgrade_instance_contract.py`: cero referencias en CI, y su
  ruta de scratch absoluta a `D:/` lo hace incorrible en los runners linux. Preexistente en 11 de
  los 14 `scripts/test_*.py`; lo senalo, no lo cargo a esta tarea.
- **R3** -- no hay guardia de paridad entre los dos gemelos. Ahora la tupla de raices, la lista de
  sufijos y la lista negra estan duplicadas literalmente en los dos ficheros: tres puntos donde
  pueden separarse en vez de uno. El instructor ya lo pidio en la ACTION r1 ("si puedes dejar algo
  que impida que vuelvan a separarse"); `f76cb9c0` no lo entrega y el handoff no lo declara.
- **R4** -- punto D (ruta de staging frente a ruta consumida) sigue confirmado y fuera de alcance
  por instruccion explicita del instructor. No lo he vuelto a medir.

## Recomendacion de cierre

**CHANGE-REQUIRED.** No cerrable en `f76cb9c0`.

El efecto de los dos frentes esta entregado y verificado. El bloqueo es D1: el handoff declara un
guardia de co-entrega que no puede enrojecer cuando su frente se rompe, y lo he refutado con una
mutacion que reintroduce el defecto original dejando el guardia en verde. La correccion es pequena
y la celda discriminante ya esta medida.

-- Analista, 2026-08-18, hora local del reloj (UTC+2)

Task-Id: TASK-0394
Reviewed-By: Analista
