# Veredicto Analista -- TASK-0394 r2 (el arbol ya ata el efecto; `.github` se cayo del conjunto)

- Revisor: Analista (voz adversarial independiente). Maker: Codex. No he implementado nada.
- Fecha: 2026-08-18, 10:51 hora local del reloj (UTC+2).
- Ancla canonica del PRODUCTO: `727d2289` (fix) + `201e77f5` (checkpoint de memoria), ambos
  ancestros de `origin/main`. HEAD local y `origin/main` al juzgar: `dcaf51db`. Reverificado con
  `git merge-base --is-ancestor`: el ancla no se movio bajo el juicio.
- Metodo: CLON LIMPIO (`git clone -s` -> `D:/Aegis_Scratch/protocol/t394r2`), `checkout 201e77f5`.
  Ninguna puerta corrida en el arbol caliente.
- Fixtures: `m0` (copia del clon sin `.git`) como master de prueba; `mutD1` (copia del clon sin
  `.git`) para la mutacion de `main()`; instancia comparada `examples/minimal_instance` del clon.
- Alcance de producto declarado por el instructor: `scripts/test_upgrade_instance_contract.py`,
  `scripts/upgrade_instance.py`, `scripts/upgrade_instance.ps1`.

## Veredicto

**OK-CLOSABLE con cuatro residuos declarados.**

Respuesta directa a la pregunta del instructor ("satisface el ancla `201e77f5` D1 y R1 sin cambio
de frontera?"):

- **D1: SI, y con la celda discriminante exacta que yo publique en r1.** Borre
  `copy_peer_harness(source, gov)` de `main()` en produccion: el contrato muere en
  `assert proof.is_file()` (linea 141) -- no antes, no por otra causa -- con la guia PRESENTE y la
  prueba AUSENTE. Es el defecto original reproducido y cazado.
- **R1: SI, por la salida (a) de las dos que ofreci en r1** (derivar el conjunto requerido del
  arbol, sea cual sea el sufijo). Lo medi mutando PRODUCCION, no el runner: quitar `.githooks` de
  las raices de exportacion enrojece **los dos gemelos**.
- **Sin cambio de frontera.**
- **Pero el ensanche tambien estrecho.** Dos celdas que en r1 medi ROJAS hoy salen VERDES: la raiz
  del master y el subarbol `.github`. La primera esta declarada en el docstring; la segunda **no
  esta en la enumeracion de categorias del handoff** y convive con `.github/workflows/validate.yml`
  como master adoptable declarado. No bloquea (la perdida es prospectiva: hoy no hay ni un fichero
  que pierda cobertura), pero no se cierra sin decirlo.

## Tabla vector por vector

| Vector | Resultado | Evidencia (exit code medido) |
|--------|-----------|------------------------------|
| **D1 -- contrato limpio, corrida 1** | PASS | exit 0 |
| **D1 -- contrato limpio, corrida 2 (DECISION-0115)** | PASS | exit 0 |
| **D1 -- mutante: `copy_peer_harness(source, gov)` borrado de `main()`** | **PASS** | **exit 1**, `AssertionError` en `test_upgrade_instance_contract.py:141` (`assert proof.is_file()`) |
| D1 -- el mutante falla POR LA CAUSA correcta | PASS | las 14 aserciones previas pasan; solo cae `proof` |
| D1 -- el mutante reproduce el defecto original | PASS | guia PRESENTE, prueba AUSENTE en la instancia real de tier por defecto |
| **R1 -- quitar `.githooks` de las raices, gemelo Python (produccion)** | **PASS** | **exit 1**; nombra `.githooks/pre-commit` y `.githooks/commit-msg` |
| **R1 -- quitar `.githooks` de las raices, gemelo PowerShell (produccion)** | **PASS** | **exit 1**; mismas dos rutas |
| R1 -- baseline sin perturbar, ambos gemelos | PASS | exit 0 / exit 0 |
| R1 -- `tools/gatekeeper` (raiz nueva, SIN extension) | PASS | exit 1 / exit 1 |
| R1 -- `tools/sub/deep/payload.txt` (raiz nueva, profundo, sin extension) | PASS | exit 1 / exit 1 |
| R1 -- quitar raiz `scripts` | PASS | exit 1; 69 ficheros nombrados (r1: 62) |
| R1 -- quitar raiz `skills` | PASS | exit 1; 8 (r1: 7) |
| R1 -- quitar raiz `runtime` | PASS | exit 1; 33 (r1: 31) |
| **`exportable.py` en la RAIZ del master** | **SLIP (RES-1)** | **exit 0 / exit 0**; en r1 era exit 1 |
| **`.github/scripts/gate.py`** | **SLIP (RES-1)** | **exit 0 / exit 0**; en r1 era exit 1 |
| **Quitar `.github/workflows/validate.yml` de los masters declarados** | **SLIP (RES-2)** | exit 0 / exit 0 |
| **Quitar el glob de `profiles/PROFILE_TEMPLATE`** | **SLIP (RES-2)** | exit 0 / exit 0 |
| **Quitar el glob de `Area_comun/protocol`** | **SLIP (RES-2)** | exit 0 / exit 0 |
| **Quitar `AGENTS.template.md`** | **SLIP (RES-2)** | exit 0 / exit 0 |
| **`Secrets/leak.py` (variante de caja de una raiz vetada)** | **SLIP (RES-3)** | **Python exit 1** nombrando el fichero, **PowerShell exit 0** |
| `.pytest_cache/v/lastfailed` (raiz de cache nueva) | PASS/fragil (RES-4) | exit 1 / exit 1 -- fail-loud por diseno |
| Cambio de frontera | PASS (ninguno) | ver seccion Frontera |
| `validate_collaboration_state.py` en clon limpio | PASS | exit 0 |
| `protocol_replay.py --check-drift` | PASS | exit 0, `verdict=CLEAN up_to_seq=9941` |
| `scan_encoding.py` | PASS | exit 0 |
| `scan_domain_neutrality.py` | PASS | exit 0 |

## D1 -- el guardia ahora SI ata el efecto

El arreglo vive en `scripts/new_instance.py:944`, dentro de `main()`. El contrato r2 dejo de
llamar al ayudante y ahora lanza `scripts/new_instance.py` como subproceso con la CLI completa,
**omitiendo `--tier`**, de modo que argparse elige el tier real `coordination`
(`test_upgrade_instance_contract.py:51-86,136-141`). Ademas `run_upgrade` ya apunta a
`master / "scripts/upgrade_instance.py"`, no a `ROOT`: la mutacion de produccion viaja al fixture.

Refutacion por mutacion (fixture `D:/Aegis_Scratch/protocol/mutD1`; unica edicion: borrar la linea
944):

| Medicion sobre el MUTANTE | Resultado |
|---------------------------|-----------|
| `python scripts/test_upgrade_instance_contract.py` | **exit 1** |
| Punto de muerte | `test_upgrade_instance_contract.py:141`, `assert proof.is_file()` |
| `<inst>/skills/session-watchdogs.skill.md` | presente (la asercion de la guia pasa) |
| `<inst>/scripts/harness/test_session_watchdog_filter.py` | **AUSENTE** |

Contra el criterio falsable que publique en r1 -- "con las lineas borradas de `main()` el contrato
debe salir distinto de 0; con ellas puestas, 0" -- esto es un cumplimiento exacto, y la celda
discrimina por la razon correcta: las catorce aserciones anteriores pasan.

Nota menor, no defecto: la mitad `assert guide.is_file()` **no discrimina** (paso tambien en el
mutante, porque la guia viaja por otro camino). Toda la potencia del vector la lleva `proof`.

## R1 -- el criterio ya es estructural, y lo medi sobre produccion

`uncovered_adoptable_files` perdio `GENERIC_TOOL_SUFFIXES`. La forma nueva es: todo fichero con
`len(parts) >= 2` cuya raiz de primer nivel no este en `NON_DISTRIBUTABLE_ROOTS` y que no sea
artefacto de runtime excluido. El gemelo `.ps1` replica la misma forma
(`upgrade_instance.ps1:185-195`).

La medicion que importa no es el contrato (que muta su propia copia en SCRATCH) sino el CONTROL.
Mutando `scripts/upgrade_instance.py` y `scripts/upgrade_instance.ps1` en el master de prueba:

| Raiz retirada del conjunto cubierto | Python | PowerShell | ficheros nombrados |
|-------------------------------------|--------|------------|--------------------|
| `.githooks` | **1** | **1** | 2 (`pre-commit`, `commit-msg`) |
| `scripts` | 1 | -- | 69 |
| `skills` | 1 | -- | 8 |
| `runtime` | 1 | -- | 33 |

En r1 la fila `.githooks` era **exit 0 con 0 ficheros**: ese era el agujero, y esta cerrado. El
ensanche es real y cuantificado: 69/8/33 frente a 62/7/31 de r1.

Y la carga sin extension ya no es invisible: `tools/gatekeeper` (el vector que el contrato fija) y
`tools/sub/deep/payload.txt` enrojecen los dos gemelos.

## RES-1 -- el ensanche tambien estrecho: la raiz y `.github` (declarado a medias)

Regla de la casa: al ensanchar un patron hay que medir lo GANADO **y** lo PERDIDO. Dos celdas que
en r1 medi ROJAS hoy salen VERDES en los dos gemelos:

| Celda | r1 | r2 |
|-------|----|----|
| `exportable.py` en la raiz del master | 1 | **0** |
| `.github/scripts/gate.py` | 1 | **0** |

Causa: el filtro `len(rel_path.parts) < 2` excluye la raiz, y `.github` entro en
`NON_DISTRIBUTABLE_ROOTS`.

- La exclusion de la RAIZ **si esta declarada** (docstring de `uncovered_adoptable_files` y el
  propio mensaje de handoff). Es una decision de diseno legitima: la raiz mezcla artefactos vivos
  y plantillas.
- La entrada `.github` **no lo esta**. El handoff enumera lo que cubre la lista negra
  ("local agent configuration, live governance/state, release evidence, examples,
  personal/research/test material, secrets, and the pre-T0 seal") y `.github` no cae en ninguna de
  esas categorias. Peor: `.github/workflows/validate.yml` sigue siendo un master adoptable
  DECLARADO, asi que `.github` es un arbol mixto exactamente igual que la raiz -- y a la raiz si se
  le escribio la justificacion.

Por que no bloquea: la perdida es **prospectiva, no efectiva**. Censo sobre el ancla: `.github`
contiene hoy dos ficheros (`workflows/validate.yml`, `workflows/selfhosted-probe.yml`), ninguno de
los cuales r1 requeria tampoco (`.yml` no estaba en los tres sufijos); y la raiz no tiene ningun
`.py`/`.ps1`/`.skill.md`. Hoy no hay un solo fichero que pierda cobertura. Ademas, denegar `dist`,
`pre_t0_ledger_seal` y `.github` era **forzoso**: sin eso el ensanche estructural habria puesto el
baseline en rojo. El intercambio es legitimo; lo que falta es una linea que lo diga.

## RES-2 -- la mitad "masters declarados" del criterio se autocertifica

El criterio tiene dos mitades: nueve globs de master declarados a mano y cuatro raices recursivas.
El arreglo r2 puso la segunda mitad bajo control estructural. La primera **no tiene guardia
ninguno**:

| Glob retirado de `ADOPTABLE_MASTER_FILES` | Python | PowerShell |
|-------------------------------------------|--------|------------|
| `AGENTS.template.md` | 0 | 0 |
| `.github/workflows/validate.yml` | 0 | 0 |
| el glob de `profiles/PROFILE_TEMPLATE` | 0 | 0 |
| el glob de `Area_comun/protocol` | 0 | 0 |

Es el modo de fallo de TASK-0394 -- carga que deja de viajar sin que nada lo note -- vivo en la
otra mitad del mismo criterio. **No es una regresion de r2**: en r1 era identico (ninguno de esos
ficheros casaba con los tres sufijos). Lo declaro porque el docstring nuevo promete "removing an
entire declared export root ... must make the control fail" y esa promesa, leida de prisa, se
extiende a los masters declarados, que no cubre.

## RES-3 -- la lista negra NO esta espejada en semantica: PowerShell ignora la caja

El handoff afirma: "The instance-only denylist is mirrored in both twins." Esta espejada en
CONTENIDO, no en COMPORTAMIENTO. `ContainsKey` de una hashtable de PowerShell es **insensible a
mayusculas**; la pertenencia a un `set` de Python no.

    pwsh: $h = @{ "secrets" = $true }; $h.ContainsKey("Secrets")  ->  True
    py  : "Secrets" in {"secrets", ...}                           ->  False

Celda medida, alcanzable hoy (`secrets/` y `.agents/` estan en la lista negra pero **no existen**
en el arbol, asi que una variante de caja es un directorio nuevo de verdad, no el mismo en NTFS):

| Semilla | Python | PowerShell |
|---------|--------|------------|
| `Secrets/leak.py` | **exit 1**, nombra `Secrets/leak.py` | **exit 0** |

Los dos gemelos dan veredictos OPUESTOS sobre el mismo master. Severidad baja (la direccion es
Python falso-positivo, no PowerShell falso-negativo sobre carga generica real), pero la frase del
handoff es mas fuerte que el hecho y el ledger no deberia registrarla asi.

## RES-4 -- coste de mantenimiento del default invertido (no es defecto)

Con el criterio estructural, **cualquier** arbol de primer nivel nuevo pone los dos gemelos en
rojo hasta que alguien edite la lista negra. Medido: `.pytest_cache/v/lastfailed` -> exit 1 / exit
1. Lo mismo valdria para `.venv`, `node_modules`, `htmlcov` o cualquier cache de herramienta creada
al correr las pruebas en el repo. Los dos gemelos coinciden, asi que no es rotura de paridad: es el
precio del fail-loud, que es la postura correcta. Lo dejo anotado para que nadie lo lea luego como
un fallo del control.

## RES-5 -- residuos de r1 que r2 no toco (siguen vivos)

1. `scripts/test_upgrade_instance_contract.py` sigue llamandose "permanent" y sigue teniendo
   **cero referencias** en `.github/workflows/`. Nada lo corre solo.
2. `SCRATCH` sigue cableado a la ruta absoluta Windows
   `D:/Aegis_Scratch/multi_agent_project_protocol/task0394-contract`; los jobs corren en
   `[self-hosted, protocol-linux]` salvo uno. Si se cablea al CI linux, falla por la ruta.
3. Nuevo en r2: el contrato ahora exige **`pwsh` en el PATH** (`run_upgrade_ps`). Sube el listado
   de precondiciones del mismo fichero que aun no corre en ningun sitio.
4. Menor: el `finally` limpia `SCRATCH` y `task0394-generated`, pero deja
   `task0394-ps-report.md` en el scratch root. Verificado presente tras mis corridas.

## Frontera: sin cambio

`727d2289` toca exactamente tres ficheros: `scripts/test_upgrade_instance_contract.py`,
`scripts/upgrade_instance.py`, `scripts/upgrade_instance.ps1`. No toca `protocol.config.json`,
`AGENTS.md`, `Area_comun/decisions/`, ninguna plantilla ni ruta de producto. No hay capability
nueva ni versionado tocado. `scan_domain_neutrality.py` exit 0 sobre el clon.

## Reproduccion (todo con exit code medido)

    git clone -s D:/Agentes/multi_agent_project_protocol D:/Aegis_Scratch/protocol/t394r2
    cd D:/Aegis_Scratch/protocol/t394r2 && git checkout 201e77f5

    # puertas protocolares
    python scripts/validate_collaboration_state.py            # exit 0
    python runtime/protocol_replay.py --check-drift           # exit 0, verdict=CLEAN
    python scripts/scan_encoding.py                           # exit 0
    python scripts/scan_domain_neutrality.py                  # exit 0

    # D1: baseline reproducible
    python scripts/test_upgrade_instance_contract.py          # exit 0
    python scripts/test_upgrade_instance_contract.py          # exit 0

    # D1: mutante de produccion
    cp -r t394r2 mutD1 && rm -rf mutD1/.git
    # borrar la linea 944 de mutD1/scripts/new_instance.py: copy_peer_harness(source, gov)
    cd mutD1 && python scripts/test_upgrade_instance_contract.py
    # -> exit 1, AssertionError en :141 assert proof.is_file()

    # R1: control directo sobre un master de prueba
    cp -r t394r2 m0 && rm -rf m0/.git
    cd m0
    python scripts/upgrade_instance.py --master . --instance <clon>/examples/minimal_instance
    pwsh -NoProfile -File scripts/upgrade_instance.ps1 -Master . -Instance <...> -Report <...>
    # baseline: 0 / 0
    # tras quitar ".githooks" de las raices de exportacion en ambos gemelos: 1 / 1

    # celdas de perdida y de paridad
    touch m0/exportable.py                             # 0 / 0   (r1: 1)
    mkdir -p m0/.github/scripts && touch .../gate.py   # 0 / 0   (r1: 1)
    mkdir -p m0/Secrets && touch m0/Secrets/leak.py    # 1 / 0   (divergencia de caja)

## Recomendacion de cierre

**OK-CLOSABLE.** Los dos frentes de la ACTION r2 estan entregados y verificados por conducta sobre
produccion, no por lectura, y con las puertas protocolares verdes en clon limpio. No pido otra
iteracion: RES-1 y RES-2 no se arreglan con codigo urgente sino con una decision de alcance, y
RES-3 y RES-5 son de higiene.

Lo que si pido antes de que el cierre entre en el ledger, y es barato:

1. Una linea en el criterio (los dos gemelos) que diga por que `.github` es arbol mixto y queda
   fuera, igual que ya se escribio para la raiz. Es documentacion, no comportamiento.
2. Que el handoff no registre "mirrored in both twins" sin el matiz de RES-3.
3. Una sucesora que ponga la mitad "masters declarados" bajo guardia (RES-2), que es la unica
   superficie del criterio donde el defecto original de TASK-0394 sigue siendo posible.

Si el Arquitecto prefiere cerrar tal cual y abrir la sucesora con los cuatro residuos dentro,
tambien lo firmo: ninguno de ellos hace que un guardia declarado sea incapaz de enrojecer por su
propio frente, que era el motivo del CHANGE-REQUIRED de r1.

-- Analista
