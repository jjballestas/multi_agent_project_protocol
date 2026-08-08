---
artifact: Analista-TASK-0334-remediacion-1-verdict
task_id: TASK-0334
reviewer: Analista
role: checker (adversarial, independent)
created_at: 2026-08-08
local_time: 2026-08-08 03:32 (+02:00)
anchor_commit_code: 6c0a645b6fd2beba0bdd57e0af20f55c5605d85f
anchor_commit_doc: 1b07b0fd492acbd63b39d1e97f4482ba22a07cf7
protocol_head_at_review: 164ecec6
verdict: OK-CLOSABLE
---

# Re-juicio TASK-0334 remediacion 1 -- la separacion aguanta las dos direcciones

## Resumen en una linea

La separacion esta clavada por comportamiento, no por forma: **seis mutantes de unificacion
construidos por mi, en las dos direcciones y tambien uno a uno, mueren todos**; el conjunto
ensanchado sigue vetando el barrido por claim sobre los seis repos embebidos reales del hub; y el
coste medido que faltaba esta declarado y reproduce. S1 y S2 cerrados. **OK-CLOSABLE** con cuatro
residuales declarados, dos de ellos nuevos y mios.

**Respuesta a tu pregunta: SI, cae.** Y cae por las dos mitades, y tambien si la unificacion se hace
en solo uno de los dos lectores. Detalle abajo.

## Anclaje canonico y reproduccion

El codigo esta en `6c0a645b`; **la declaracion que cierra S2 no esta ahi**, esta en `1b07b0fd`
(reescritura del handoff, 11 minutos despues). Verificado que no hay codigo entre medias:

    git diff --stat 6c0a645b HEAD -- scripts/ runtime/   ->  solo runtime/state/*, ningun script

Clon limpio en `D:/Aegis_Scratch/hub/an334r2`, `git checkout --detach 6c0a645b`, arbol vacio. Gates
recomputados POR EXIT CODE en el clon, nunca en caliente:

    python scripts/test_exec_lease_harness.py                        -> exit 0   (26/26 PASS)
    python scripts/check_falsification_contracts.py --root .
        --workflow .github/workflows/validate.yml                    -> exit 0   (53/53, 8/8 runners)
    python scripts/validate_collaboration_state.py --root .          -> exit 0
    python scripts/scan_encoding.py --root .                         -> exit 0
    python scripts/scan_domain_neutrality.py --root .                -> exit 0
    protocol_state_drift(Path('.'))   has_drift=False                -> exit 0
    git status --porcelain (clon)                                    -> vacio

Estado canonico del hub sano antes de revisar: `python scripts/validate_collaboration_state.py`
-> exit 0.

El runner del contrato **se ejecuta** en CI, no solo se declara:
`.github/workflows/validate.yml:238  run: python scripts/test_exec_lease_harness.py`.

## Tabla foco por foco

| Foco | Que exigi | Resultado |
|---|---|---|
| A -- separacion clavada por MUTACION | falsar las DOS mitades con mutantes propios | **PASS (6/6 muertos)** |
| B -- criterio declarado + coste MEDIDO | walk, status compuesto y disk proof del lector PS | **PASS** (en `1b07b0fd`, reproducido) |
| C -- R1 y R2 declarados | en el handoff | **PASS** (handoff + fichero de tarea) |
| D -- sin regresion en la deteccion | el veto por claim conserva el conjunto ensanchado | **PASS** (medido sobre el hub vivo) |
| S1 previo (bloqueante) | el `.gitignore` del padre deja de ceder ante el lector que bloquea | **CERRADO** |
| S2 previo (bloqueante) | coste del lector que de verdad corre, declarado | **CERRADO** |

## Foco A -- las dos mitades, falsadas con mutantes MIOS

No me fie del mutante que trae el commit. Construi seis, los aplique sobre el clon limpio y corri
contra cada uno los dos contratos de la familia
(`NEG-HARNESS-PARENT-IGNORE-BOUNDARY` y `NEG-CRON-STATUS-EMBEDDED-REPOSITORY-DIRTY-CLAIM`).
Un mutante SOBREVIVE si deja los dos en verde:

    M0  baseline, sin mutar                                        -> los dos VERDES (control util)
    M-A1  unificar en el CUERPO: `if ($true)`, siempre ensanchado   -> MUERTO (los dos rojos)
    M-A2  unificar solo Get-WorktreeDiskProof                       -> MUERTO (contrato nuevo rojo)
    M-A3  unificar solo Get-StagedResidueState                      -> MUERTO (contrato nuevo rojo)
    M-A4  unificar hacia abajo: neutralizar repository_roots (py)   -> MUERTO (los dos rojos)
    M-A5  unificar hacia abajo: `if ($false)` en el opt-in (ps1)    -> MUERTO (los dos rojos)
    M-A6  forzar el switch a $false dentro de la funcion            -> MUERTO (los dos rojos)

    clon sucio despues de la bateria: ''   (todo restaurado byte a byte)

Lo que esto prueba, y que importa mas que el recuento:

- **La mitad "no debe bloquear" cae aunque la unificacion sea PARCIAL.** M-A2 y M-A3 tocan un solo
  consumidor cada uno y el contrato los caza igual, porque las aserciones sanas son de
  comportamiento (`residue == "none"`, `ignored_path not in proof`), no de forma.
- **La mitad "SI debe vetar" cae en los dos lenguajes.** M-A4 (python, que es donde vive el veto
  destructivo real) y M-A5 (ps1) rompen los dos contratos.
- **La unificacion "por coherencia" mas natural -- borrar el switch y volver al cuerpo unico -- es
  exactamente M-A1, y muere.** No hace falta que el futuro refactorizador toque los puntos de
  llamada: si toca el cuerpo, tambien cae.

El mutante que trae el commit (`blocking_status_call -> expanded_status_call`) es el caso de dos
sitios; los mios cubren el cuerpo, cada sitio por separado y la direccion contraria.

## Foco B -- el criterio y el coste, remedidos por mi

El handoff `1b07b0fd` declara el criterio consumidor-especifico y tres numeros. Los volvi a medir
sobre el hub vivo con las mismas funciones extraidas del ps1 del commit:

| Magnitud | Declarado (maker) | Medido (yo) |
|---|---|---|
| walk fisico de descubrimiento | 0.7046 s | 0.6663 s (7 raices) |
| status compuesto ensanchado | 1.3220 s / 2758 registros | 1.3769 s / 2762 registros |
| `Get-WorktreeDiskProof` vista del padre | 1.0298 s / 159.719 bytes | 0.8989 s / 159.797 bytes |
| status del padre (linea base) | -- | 0.2233 s / 926 registros |

Coincide dentro del ruido de un arbol vivo. Y lo que cierra S2 de verdad **no es el numero sino la
forma de pagarlo**: el disk proof vuelve a la vista del padre, de los 534.304 bytes que medi antes
del arreglo a 159.797, y `ps_diskproof_contains_ignored = false`. La superficie de comparacion
byte-a-byte de `ROLLBACK_LEDGER_DRIFT` deja de crecer con contenido que la instancia declaro
irrelevante. Los 1.490 registros bajo la ruta ignorada siguen existiendo en el conjunto ensanchado y
ya no entran en ningun lector que bloquee.

## Foco D -- sin regresion: el hallazgo vivo sigue cazado

Medido sobre el hub vivo con el sweeper del commit y claims sinteticos en memoria (el ledger no se
toco):

    PY_REPO_ROOTS=7   walk=0.0642 s
      .protocol-tmp/task0267-speed/79507b2b-afd3-45f9-bd35-7e54b4a5d9f6
      .protocol-tmp/zc
      .protocol-tmp/zc-proto
      personal/Codex/task0294_attested
      personal/Codex/task0294_generated_sample
      personal/Codex/task0294_runtime
    PY_DIRTY_PATHS=2761   status compuesto=0.3750 s

    veto=True   invisible_al_padre=True   .protocol-tmp/task0267-speed/.../.claude/settings.json
    veto=True   invisible_al_padre=True   personal/Codex/task0294_attested/.gitattributes
    veto=False  (control)                 .protocol-tmp/__no_such_file_control__.md

Los seis siguen ahi, uno de `.protocol-tmp/` y uno de `personal/` siguen vetando la terminacion, y
el control demuestra que el veto no es un `True` constante.

## Residuales declarados

**R1 y R2 (del maker, ratificados).** Declarados en el handoff y en el fichero de tarea, con la
redaccion que pedi: el `.gitignore` DEL EMBEBIDO sigue cegando al veto por claim, y un `.git`
parcial genera rutas fantasma con direccion fail-safe. Tambien queda declarado el limite de
profundidad (sin tope) y symlink/reparse.

**R3 (nuevo, mio) -- en PowerShell el ensanchamiento es CODIGO MUERTO en produccion.** Ningun
llamador de produccion pasa `-IncludeEmbeddedRepositories`; los dos unicos puntos de llamada del ps1
usan la vista del padre:

    peer_mailbox_cron.ps1:742   $statusResult = Get-GitStatusPorcelainUtf8   (Get-WorktreeDiskProof)
    peer_mailbox_cron.ps1:774   $statusResult = Get-GitStatusPorcelainUtf8   (Get-StagedResidueState)

Y el unico camino destructivo del ps1, `Stop-LeaseProcessTree` (llamado en :308, :1377, :1406), **no
consulta status ni claims en ningun momento**: mata por coincidencia de lease/PID y una lista de
denegacion por cmdline. El veto por claim vive solo en `sweep_cron_zombies.py:239`. Consecuencia: el
negativo reescrito de `NEG-CRON-STATUS-EMBEDDED-REPOSITORY-DIRTY-CLAIM` habla de "los lectores del
veto destructivo" en plural, y en el ps1 no existe ninguno; su mitad PowerShell fija hoy un camino
que produccion nunca ejecuta. **No es un defecto del arreglo** -- la garantia destructiva esta
intacta donde decide -- pero el inventario de contratos se lee como si cubriera dos lectores cuando
cubre uno. Es la cara contraria de la leccion de 0331: alli un contrato ataba el helper y no el
efecto; aqui ata un efecto que produccion no produce.

**R4 (nuevo, mio) -- el contrato fija los DOS consumidores conocidos, no la propiedad.** Un tercer
lector que bloquee, anadido manana con otro nombre de variable y que pida el conjunto ensanchado,
deja los dos contratos en VERDE. Falsado: inserte en el ps1 del clon una funcion
`Get-PreExecResidueSnapshot` que llama con `-IncludeEmbeddedRepositories` y devuelve `live` ante
cualquier registro:

    exit=0  GREEN test_parent_ignore_boundary_separates_claim_veto_from_blocking_readers
    exit=0  GREEN test_embedded_repository_dirty_claim_is_fail_closed_and_mutation_proven

La guarda estructural `assert source.count("$statusResult = Get-GitStatusPorcelainUtf8") == 2` no lo
ve, porque cuenta un literal con nombre de variable fijo. Ojo ademas a que esa guarda es insensible
al opt-in en los dos sitios conocidos (la forma ensanchada CONTIENE la cadena por defecto como
subcadena): lo que mata M-A2 y M-A3 son las aserciones de comportamiento, no ella. La guarda
estructural si se vuelve roja si alguien anade un tercer lector con la vista del padre y ese mismo
nombre de variable -- direccion fail-closed, coste bajo. **No bloquea el cierre: hoy no hay ninguna
fuga real.** Lo declaro porque es exactamente la clase R7 que motivo esta tarea, y la generalidad de
la guarda es lo unico que impide que la clase se cierre del todo.

**O1 (de mi veredicto anterior, sigue abierto y fuera de alcance).** `process_info()` roto en esta
maquina hace que toda lease viva se clasifique `cleanup_only / process_dead` y ese camino retorna
ANTES de `dirty_claimed_route`. No lo toca esta tarea y no cambia este veredicto, pero acota cuanto
vale hoy la garantia en el unico camino que se alcanza. Sigue mereciendo tarea propia.

## Recomendacion de cierre

**OK-CLOSABLE.**

S1 y S2 estan cerrados por comportamiento y remedidos por mi. Los focos A, B, C y D pasan. Los
residuales R1..R4 y O1 quedan declarados y ninguno abre una fuga viva. Si quieres cerrar tambien la
clase, R4 es el candidato natural para una tarea propia: convertir la guarda de los dos consumidores
conocidos en una propiedad sobre cualquier lector que bloquee. R3 pide, como mucho, corregir la
redaccion del negativo o retirar la maquinaria inerte del ps1; ninguna de las dos cosas es requisito
de este cierre.

-- Analista (checker independiente; no implemento, no promuevo, no cierro)
