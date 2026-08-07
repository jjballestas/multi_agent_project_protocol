---
artifact: ANALISTA-TASK-0334-repo-embebido-invisible-veredicto
task_id: TASK-0334
reviewer: Analista
role: checker (adversarial, independent)
created_at: 2026-08-08
anchor_commit: 7692a561df1705c4437da8289ee39806dce736dd
protocol_head_at_review: 59a18e13
verdict: CHANGE-REQUIRED
---

# Veredicto TASK-0334 -- los repos embebidos dejan de ser invisibles

## Resumen en una linea

El mecanismo nuevo funciona y esta bien probado -- ve los seis repos reales del hub, no tiene tope de
profundidad, veta ante fallo y mata el mutante de codigo muerto -- pero al interrogar cada embebido
por separado **tira a la basura el `.gitignore` del padre**, y esas rutas recuperadas entran en un
lector que **BLOQUEA**: sobre un arbol que el padre declara limpio, el guard de residuo pasa de
`none` a `live` y difiere el exec del peer. Eso es AC7 (sin regresion) y el foco D (que no degrade el
ciclo). No es cerrable tal cual.

## Anclaje canonico y reproduccion

Clon limpio en `D:/Aegis_Scratch/mapp0334/cc`, `git checkout --detach 7692a561`, arbol vacio.
Gates recomputados POR EXIT CODE en el clon, no en caliente:

    python scripts/test_exec_lease_harness.py                     -> exit 0   (22/22)
    python scripts/check_falsification_contracts.py --root .
        --workflow .github/workflows/validate.yml                 -> exit 0   (49/49, 8/8 cableados)
    python scripts/validate_collaboration_state.py --root .       -> exit 0
    python scripts/scan_encoding.py --root .                      -> exit 0
    python scripts/scan_domain_neutrality.py --root .             -> exit 0
    protocol_state_drift(Path('.'))  has_drift=False              -> exit 0
    git status --porcelain (clon)                                 -> vacio

Estado canonico del hub verificado sano antes de revisar:
`python scripts/validate_collaboration_state.py` -> exit 0.

## Tabla foco por foco

| Foco / AC | Que exigi | Resultado |
|---|---|---|
| A -- seis repos reales | inventario y veto sobre uno de `personal/` y uno de `.protocol-tmp/` | PASS |
| B -- fail-closed | romper la deteccion y comprobar VETO, no barrido | PASS (con matices, ver S4) |
| C -- limite de profundidad | hasta donde cubre y que pasa mas alla | PASS (sin tope, verificado a nivel 5) |
| D -- coste en camino caliente | coste medido declarado y sin degradar el ciclo | **SLIP S1 + S2** |
| E -- mutante de codigo muerto | el negativo muere ante deteccion presente pero inalcanzable | PASS |
| Nota -- coherencia entre lectores | ambos lectores alineados | PASS |
| AC7 -- sin regresion | suites y gates verdes, sin regresion de comportamiento | **SLIP S1** |

## Lo que SI queda probado (por comportamiento, no por nombre de test)

**A -- los seis reales, no el fixture.** `repository_roots` sobre el hub vivo devuelve 7 raices
(la raiz + los seis embebidos exactos del handoff), walk en 0.0652 s. Con claims sinteticos en
memoria (sin tocar el ledger) y comprobando ademas que el objetivo es invisible al status del padre:

    personal/Codex/task0294_runtime/.githooks/commit-msg
        invisible_to_parent_only=True   dirty_claimed_route=True
    .protocol-tmp/task0267-speed/79507b2b-.../.claude/settings.json
        invisible_to_parent_only=True   dirty_claimed_route=True
    control  .protocol-tmp/zc/__no_such_file__.md  -> dirty_claimed_route=False

El lector PowerShell sobre el mismo hub vivo: `ok=True`, 2705 rutas, y contiene LITERALMENTE los dos
mismos objetivos. Los dos lectores coinciden en recuento y en pertenencia.

**B -- fail-closed, comprobado en los CONSUMIDORES, no solo en el lector.** Falsado con fallos
inyectados y con un `.git` roto de verdad, y con un control que demuestra que el fixture era
genuinamente matable:

    [control sin claim]              action=kill  reason=expired_matching_lease   <- de verdad mataba
    [claim dentro del embebido]      action=skip  reason=dirty_active_claim_route <- VETA
    [fallo de traversal (OSError)]   RAISED -> ninguna decision de kill producida
    [.git file con gitdir obsoleto]  RuntimeError: git status ... failed -> sin kill

    PowerShell, fixture sano:   residue=live     diskproof_null=False
    PowerShell, deteccion rota: residue=unknown  diskproof_null=True
    PowerShell, gitdir obsoleto: residue=unknown diskproof_null=True

`unknown` entra en `Register-PreExecDefer` y `diskproof=$null` entra en `ROLLBACK_DEFER`: los dos
consumidores vetan. **Respuesta a tu pregunta: ante deteccion fallida o ambigua el barredor VETA, no
mata.** Con dos matices honestos: S4 (abajo) y O1 (abajo).

**C -- profundidad.** Sin tope, y no solo un nivel mas que git. Fixture con `a/b/c/inner` (nivel 4) y
un repo DENTRO del embebido en `a/b/c/inner/nested/deeper` (nivel 5):

    REPOS: . | a/b/c/inner | a/b/c/inner/nested/deeper | ig/inner
    a/b/c/inner/live_deep.md                  veto=True
    a/b/c/inner/nested/deeper/live_deeper.md  veto=True

La composicion de rutas es correcta en ambos casos. El limite declarado en el handoff (sin tope de
profundidad, no se siguen symlink/reparse) coincide con lo medido.

**E -- el mutante de codigo muerto muere.** El contrato del commit muta el punto de llamada, asi que
la funcion sigue definida en el fuente: ya es la forma "presente pero inalcanzable". Ademas construi
la forma mas dura por mi cuenta -- la funcion definida **Y llamada** pero neutralizada por dentro
(`return repositories` al principio del cuerpo) -- en los dos lectores:

    M1 python  (repository_roots neutralizada, sigue llamada)       -> contrato FALLA: mutante MUERTO
    M2 ps1     (Get-EmbeddedRepositoryRoots neutralizada, llamada)  -> contrato FALLA: mutante MUERTO

Un `assert "repository_roots" in source` habria sobrevivido a los dos. El contrato prueba el efecto.

**Nota -- coherencia entre lectores.** Sobre el hub vivo: 2705 rutas cada uno. Y sobre un fixture con
rename staged, espacios y no-ASCII dentro del embebido (`emb one/inner/nuevo nombre-n.md` con su par
de origen), los conjuntos son **IDENTICOS**: `PY only: []`, `PS only: []`. La cuarta pasada de la
familia mantiene el hilo.

## SLIPS

### S1 (BLOQUEANTE) -- el `.gitignore` del padre se descarta, y eso cae en un lector que BLOQUEA

Interrogar cada embebido por separado devuelve TODO lo sucio de ese repo, incluido lo que el padre
excluye deliberadamente. En este hub `.gitignore:17` es `.protocol-tmp/`, y ahi viven tres de los
seis embebidos. Medido sobre el hub vivo:

    status del padre -uall                          888 rutas, 0 bajo .protocol-tmp/
    dirty_paths post-fix                           2705 rutas, 1471 bajo .protocol-tmp/

    conjunto de residuo, peer Analista:    2 -> 1473   (+1471)
    conjunto de residuo, peer Codex:     791 -> 2608   (+1817)

Eso no seria grave si solo alimentara `dirty_claimed_route`, donde sobre-detectar es fail-safe (veta
de mas). Pero el mismo `Get-GitStatusPorcelainUtf8` alimenta `Get-StagedResidueState`, que es la
**pre-gate destructiva del ciclo**: `live` entra en `Register-PreExecDefer` y difiere el exec.

Falsacion determinista. Fixture `fx2` con la forma exacta del hub: repo padre con `.gitignore` =
`.protocol-tmp/`, un clon embebido en `.protocol-tmp/zc` con un fichero fresco, y **nada mas sucio**
(`git status --porcelain -uall` del padre: vacio).

    PRE-FIX  (7692a561^)   RESIDUE_STATE=none   -> el exec procede
    POST-FIX (7692a561)    RESIDUE_STATE=live   -> Register-PreExecDefer worktree_residue_live
                           DIAG=.protocol-tmp/zc/note.md

Un arbol que el padre declara limpio ahora bloquea al peer por el contenido de un clon de trabajo que
el propio harness deja bajo `.protocol-tmp/`. Es el footgun ya conocido del residue guard, pero
alcanzado ahora por rutas que la instancia habia declarado irrelevantes.

Hoy en el hub no dispara **por casualidad de fechas**: los seis embebidos tienen mtime de hace 14 a
45 dias, asi que caen en `aborted` (que solo loguea `RETRY_TRANSIENT` y sigue). Basta una escritura
dentro de cualquiera de los tres repos bajo `.protocol-tmp/` en la ventana de 5 minutos
(`AbortedResidueMinutes`) para que pase a `live`. Es un fallo latente, no hipotetico:

    .protocol-tmp/task0267-speed  newest=2026-07-19T23:39:49Z  age_days=18.9
    .protocol-tmp/zc              newest=2026-06-24T01:17:02Z  age_days=44.9
    .protocol-tmp/zc-proto        newest=2026-07-10T22:39:39Z  age_days=28.0

El nucleo del defecto: los dos consumidores tienen direcciones de seguridad **opuestas** -- en el veto
por claim sobre-detectar protege, en el guard de residuo sobre-detectar bloquea -- y el commit
ensancha los dos por igual.

### S2 (BLOQUEANTE) -- el foco D no esta respondido para el lector que de verdad corre

El handoff declara solo el coste de Python (walk 0.0613 s, seis status 0.5510 s). El lector que corre
en cada ciclo de cron es el de PowerShell, y su coste no se declara. Medido sobre el hub vivo:

    PS_WALK_SECONDS=0.7479          (walk de descubrimiento, 7 repos)
    PS_FULL_STATUS_SECONDS=1.4898   (status compuesto completo, 2705 registros)
    baseline previo: un solo git status del padre

    Get-WorktreeDiskProof   PRE-FIX  0.847 s   payload 153030 bytes
    Get-WorktreeDiskProof   POST-FIX 2.990 s   payload 534304 bytes

`Get-WorktreeDiskProof` se calcula **dos veces** por verificacion de rollback y se compara byte a
byte (`$proofAfter -cne $proofBefore`), asi que la superficie de deteccion de drift pasa de ~888
entradas a 2705 ficheros hasheados: mas coste y mas probabilidad de un `ROLLBACK_LEDGER_DRIFT`
espurio por un fichero que cambio dentro de un embebido ajeno al trabajo en curso. Nada de esto esta
declarado.

## Residuales declarados (no bloquean, pero hay que decirlos)

**R1 -- el `.gitignore` DEL EMBEBIDO sigue cegando al barredor, y es la misma familia destructiva.**
Un fichero vivo dentro de un embebido que el propio embebido ignora sigue siendo invisible, y el
barredor lo mata. Fixture `ig/inner` con `.gitignore` = `secret.md`:

    ig/inner/secret.md    veto=False    <- falso negativo destructivo

La frase que define la tarea es "un fichero vivo dentro de un embebido"; este lo es y sigue muriendo.
El AC5 solo obliga a declarar la profundidad, y el handoff solo declara profundidad y symlink: el
limite de ignore no esta declarado en ningun sitio. Es un limite conocido del status a nivel raiz
tambien, asi que no lo cuento como regresion -- pero un mecanismo que se presenta como el cierre de
esta familia tiene que decir por donde sigue abierta.

**R2 -- un `.git` parcial o vacio genera rutas fantasma.** Si `.git` existe pero no es un repo valido,
el descubrimiento de git sube al padre y el status del "embebido" devuelve el estado del PADRE, que
luego se prefija:

    partial_gitdir  ->  ['work/inner/live_work.md', 'work/inner/work/inner/live_work.md']

La direccion es fail-safe (sobre-detecta, no oculta) y el veto sobrevive, pero ensucia el guard de
residuo y el disk proof con rutas que no existen.

## Observacion fuera de alcance (DECISION-0018)

**O1 -- `process_info()` esta roto en esta maquina y el barredor nunca llega a su puerta de veto.**
No lo toca este commit, pero lo encontre al intentar ejercer el camino destructivo de punta a punta.
`Get-CimInstance` ya devuelve `CreationDate` como `DateTime`, asi que
`[System.Management.ManagementDateTimeConverter]::ToDateTime($p.CreationDate)` lanza
("dmtfDate ... fuera del intervalo de valores validos"), el powershell sale con codigo 1 y
`process_info` devuelve `None` para un PID **vivo** (verificado dos veces contra un proceso vivo cuyo
PID si responde a una consulta CIM directa). Consecuencias, con el fuente en la mano:

- toda lease viva se clasifica `cleanup_only / process_dead`, y con `--kill` se le borran lock y lease
  a un proceso que sigue corriendo -- se destruye la exclusion mutua del exec en marcha;
- ese camino retorna ANTES de `dirty_claimed_route`, asi que **todo el arreglo de TASK-0334 queda sin
  efecto en el unico camino que hoy se alcanza**.

Recomiendo tarea propia. No cambia mi veredicto sobre 0334, pero acota cuanto vale hoy su garantia.

## Recomendacion de cierre

**CHANGE-REQUIRED.**

Lo pedido: separar las dos direcciones de seguridad. El conjunto ensanchado es correcto para el veto
por claim (`dirty_claimed_route`), donde sobre-detectar protege; no lo es para los lectores que
bloquean o comparan (`Get-StagedResidueState`, `Get-WorktreeDiskProof`), donde la exclusion declarada
por el `.gitignore` del padre tiene que seguir valiendo. Con S1 y S2 cerrados, y R1/R2 declarados en
el handoff, esto es cerrable.

Bucle de arreglo esperado:

1. Remediacion sobre los dos lectores; el criterio elegido, declarado en el handoff junto al coste
   MEDIDO del lector PowerShell (walk, status compuesto y disk proof) -- foco D.
2. Negativo permanente que fije la eleccion: un repo embebido bajo una ruta ignorada por el padre no
   puede llevar el guard de residuo de `none` a `live`; y el veto por claim dentro de un embebido
   sigue siendo `True`. Con su mutante, como los de este commit.
3. Puertas afectadas: `scripts/test_exec_lease_harness.py`,
   `python scripts/check_falsification_contracts.py`, `validate_collaboration_state.py`,
   `scan_encoding.py`, `scan_domain_neutrality.py`, drift 0 -- todas en clon limpio.
4. Re-juicio mio antes del commit de cierre. **Maximo 2 iteraciones**; a la tercera escala al
   operador humano.

-- Analista (checker independiente; no implemento, no promuevo, no cierro)
