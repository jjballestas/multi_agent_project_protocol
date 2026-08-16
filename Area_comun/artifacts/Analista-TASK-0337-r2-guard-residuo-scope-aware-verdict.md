# Veredicto adversarial -- TASK-0337 r2, el guardia de residuo scope-aware

**Revisor:** Analista (voz independiente / checker)
**Fecha:** 2026-08-16, 05:50 local (UTC+2) -- reloj leido, no estimado
**Instruccion:** `Area_comun/mailbox/open/MSG-20260816-Arquitecto-to-Analista-REVIEW-TASK-0337-r2.md`
**Recomendacion de cierre: CHANGE-REQUIRED**

---

## 1. Ancla canonica

| Elemento | Valor |
|---|---|
| HEAD de protocolo revisado | `623fb8b4` (= `origin/main` en el momento de la revision) |
| Entrega formal del maker | `08acce5d` -- `chore(TASK-0337): deliver nested residue guard for review` |
| Cambio de codigo r2 | `d4c2e8c3` -- `fix(TASK-0337): derive nested instance prefix for residue guard` |
| Control historico (pre-fix) | `67e58387` |
| Clon limpio de revision | `D:/Aegis_Scratch/protocol/rev0337` (`git clone -s`, checkout `623fb8b4`) |
| Clon limpio de control | `D:/Aegis_Scratch/protocol/ctrl0337` (checkout `67e58387`) |

Ningun gate se corrio en el arbol caliente. El arbol vivo tenia modificaciones sin commitear
de terceros en `Area_comun/state/*` y `runtime/state/*`; no se toco ninguna.

## 2. Puertas de protocolo, en el clon limpio a `623fb8b4`

| Gate | Exit |
|---|---|
| `python scripts/validate_collaboration_state.py --root .` | **0** |
| `python scripts/scan_encoding.py --root .` | **0** |
| `python scripts/scan_domain_neutrality.py --root .` | **0** |
| `python scripts/check_falsification_contracts.py --root .` | **0** |
| `protocol_state_drift(.)` | `has_drift = False` |
| `python scripts/test_exec_lease_harness.py` | **1** (`total=31 passed=28 failed=3`) -- ver R-2 |

Ejecucion real del contrato propio de la tarea (que la `verification_cmd` NO invoca):
`run_mailbox_retry_cases.run_residue_scope_pair_case()` -> **exit 0**.

## 3. Como se midio

Se extrajo el guardia y se ejercito el bucle REAL del cron (`peer_mailbox_cron.ps1`) sobre
repositorios git de laboratorio, uno por vector, con agente falso y `-PreExecDeferTimeoutSeconds 1`.
El discriminante es de CONDUCTA: presencia o ausencia de `EXEC_START` en el log del cron, mas el
`reason=` y el `intersections_json=` del `RETRY_DEFER`. Nunca el nombre de un test.

Diferencia deliberada con el fixture entregado: aqui `personal/<Peer>/MEMORY.md` esta **versionada y
modificada** (` M`), no solo sin seguimiento (`??`), para cubrir las dos formas del residuo propio.

## 4. Vector por vector

### AC10 -- derivacion del prefijo de instancia: **PASS**, y la duda queda resuelta

La duda del encargo era: `--show-prefix` devuelve la posicion del CWD, no la de la instancia
gobernada; si el cron arranca desde la raiz del repositorio con `-Root Aegis`, el prefijo saldria
vacio y el defecto seguiria vivo con aspecto de arreglado.

**Es la segunda opcion: el `-C $Root` lo resuelve.** `--show-prefix` se evalua respecto al
directorio de `-C`, no respecto al CWD del proceso que lanza. Medido directamente:

```
git -C Aegis rev-parse --show-prefix          (CWD = raiz del repo)  -> "Aegis/"
git -C <abs>/Aegis rev-parse --show-prefix    (CWD = raiz del repo)  -> "Aegis/"
cd Aegis && git rev-parse --show-prefix                              -> "Aegis/"
git rev-parse --show-prefix                   (CWD = raiz del repo)  -> ""
```

Y el otro lado del par tambien casa: `git status --porcelain` emite rutas relativas a la raiz del
REPOSITORIO en las dos posiciones de CWD (`Aegis/work/target.txt` en ambas), que es exactamente lo
que el prefijo derivado descuenta. Las dos senales concuerdan.

Acreditado ademas por conducta, extremo a extremo, en el layout ANIDADO de verdad:

| Vector | Esperado | Medido |
|---|---|---|
| E1a anidado, CWD = raiz del repo, `-Root <repo>/Aegis`, residuo propio `personal/TestPeer/MEMORY.md` | ARRANCA | `EXEC_START`, sin defer -- **PASS** |
| E1b anidado, CWD = raiz del repo, residuo ajeno que SI intersecta | DIFIERE con el par | `RETRY_DEFER reason=worktree_residue_live paths_json=["Aegis/work/target.txt"] intersections_json=[{"dirty_path":"Aegis/work/target.txt","message_route":"work/target.txt"}]` -- **PASS** |
| E1c anidado, CWD = instancia, residuo propio | ARRANCA | **PASS** |
| E1d anidado, CWD = instancia, residuo ajeno intersectante | DIFIERE con el par | **PASS** |

E1a/E1b contra E1c/E1d es el control que faltaba: **el veredicto no depende del CWD del lanzador.**

El negativo permanente discrimina esta pieza. Mutando la produccion
(`$instancePrefix = ([string](...)).Replace(...)` -> `$instancePrefix = ""`) el contrato
`run_residue_scope_pair_case` sale **exit 1**: el mutante MUERE. Tambien muere el mutante de codigo
muerto (`if ($null -eq $MessageWorkScope) {` -> `if ($true) {`), exit 1.

Residual declarado R-1: la exencion ancla en `$Root`, no en una declaracion de la raiz de gobierno.
Si alguna vez se lanzase con `-Root` apuntando a la raiz del repositorio mientras el gobierno vive en
`Aegis/`, el prefijo saldria vacio y la exencion volveria a morir. No es un escape practico -- con ese
`-Root` el cron tampoco encontraria mailbox ni ledger --, pero conviene que quede escrito que la
precondicion existe.

### AC7 -- el fallo deja de ser mudo, lado negativo: **PASS con reserva**

Lo pedido era comprobar que **no inventa** interseccion cuando no la hay.

| Vector | Esperado | Medido |
|---|---|---|
| E4a plano, residuo ajeno que NO intersecta (`personal/Other/NOTE.md` fuera del scope) | ARRANCA, sin par | `EXEC_START`, sin `RETRY_DEFER` -- **PASS** |
| E4b igual, anidado | ARRANCA, sin par | **PASS** |
| E3a plano, residuo ajeno DENTRO del scope | DIFIERE nombrando el par | `intersections_json=[{"dirty_path":"personal/Other/NOTE.md","message_route":"personal/other"}]` -- **PASS** |

La reserva: existe un camino en el que el guardia difiere emitiendo `intersections_json=[]`, es decir
un diferimiento por residuo que no nombra ningun par. Es el mismo camino del hallazgo H-1, y es
precisamente la senal muda que el AC7 queria eliminar: el operador ve `worktree_residue_live` con
lista de pares vacia y no puede distinguir el interbloqueo de un solape real.

### AC6 -- el deadlock circular: **SLIP. No muere para toda la familia que el AC nombra.**

El AC6 dice, sin condicionar: *el peon termina su exec dejando su propia `personal/<Peer>/MEMORY.md`
sin commitear, y **su siguiente mensaje** ARRANCA en vez de diferirse contra el reloj de 7200 s*.

La exencion del area personal propia solo existe en la rama en la que el scope del mensaje ES
resoluble (`peer_mailbox_cron.ps1:931`). Cuando `Get-MessageWorkDescriptor` devuelve `$null`, el
guardia cae a la regla GLOBAL original (`:928-929`), donde el area personal del PROPIO peon vuelve a
ser relevante (`$Matches[1] -ieq $PeerId`). Y no hay red de seguridad antes: el gate
`message_scope_ambiguous` vive DENTRO de la reserva atomica (`:1206`, tras el `FileStream` de
`:1188`), y el guardia de residuo se evalua antes (`:1451`).

Medido -- es literalmente la firma de NOVA:

| Vector | AC6 exige | Medido |
|---|---|---|
| E2a plano, mensaje SIN `task_id`, residuo propio `personal/TestPeer/MEMORY.md` | ARRANCA | **DIFIERE**: `RETRY_DEFER reason=worktree_residue_live paths_json=["personal/TestPeer/MEMORY.md"] intersections_json=[]` -- **SLIP** |
| E2b plano, `task_id` ausente del indice, residuo propio | ARRANCA | **DIFIERE**, misma firma -- **SLIP** |
| E2c anidado, mensaje sin `task_id`, residuo propio | ARRANCA | **DIFIERE**: `paths_json=["Aegis/personal/TestPeer/MEMORY.md"]` -- **SLIP** |
| E2d control, `task_id` valido y resoluble, residuo propio | ARRANCA | `EXEC_START` -- PASS |

E2d es el control que prueba que E2a-E2c no son un fallo del banco: el mismo residuo, el mismo
layout, cambiando SOLO la resolubilidad del scope, invierte el veredicto.

Peso de campo, derivado del estado canonico en `623fb8b4` (no de un ejemplo):

- **292 de 458 tareas** del indice + archivo (63,8 %) no tienen bloque `scope_routes` parseable, asi
  que todo mensaje ruteado a ellas cae en la rama de scope nulo. Entre ellas hay tareas vivas
  recientes: TASK-0349, 0351, 0352, 0355, 0356, 0357, 0358.
- **10 de 38 mensajes** en `Area_comun/mailbox/open/` no llevan `task_id` numerado (FYI, DIRECTIVA,
  PLAN, RESP del Operador). Ninguno de esos mensajes puede resolver scope.

No es una esquina: es la mayoria del corpus. El interbloqueo circular sigue vivo para ella.

Y no es residuo huerfano de otra tarea. Se comprobo el `out_of_scope` de las dos vecinas: el de
TASK-0337 cubre leases de TASK-0331, umbral de poda y codigo de producto -- nada de esto. TASK-0405
delega el interbloqueo propio a "TASK-0406", pero el propio cuerpo de TASK-0337 registra que
**TASK-0406 se evaluo y se descarto por duplicar AC6/AC7**. El defecto vive, por decision escrita,
dentro del perimetro de TASK-0337.

### AC6, su negativo permanente: **SURVIVOR**

El contrato `retry-residue-scope-pair` se anuncia como *"own personal residue cannot deadlock the next
message while truly intersecting residue still defers with the exact pair"*. Mutando la produccion
para **borrar la exencion del area personal propia** de la rama scope-aware --

```
(-not $candidateIsOwnPersonal) -and $null -ne $candidateComparable -and
      ->  $null -ne $candidateComparable -and
```

-- el contrato sale **exit 0: el mutante SOBREVIVE**. El verde del contrato no lo produce la exencion
que el negativo nombra, sino la prueba de interseccion: en su fixture el area personal del peon nunca
intersecta el scope del mensaje, asi que la exencion no cambia el resultado.

Que no es codigo muerto, tambien medido: con un scope que SI cubre `personal/TestPeer`, la produccion
ARRANCA (E3b) y el mutante DIFIERE con
`intersections_json=[{"dirty_path":"personal/TestPeer/MEMORY.md","message_route":"personal/testpeer"}]`
(E4c). La exencion cambia la conducta; simplemente ningun vector del contrato la pisa.

Los otros dos mutantes declarados si mueren (prefijo: exit 1; codigo muerto: exit 1), asi que el
negativo no es vacuo en bloque -- pero tiene un agujero exactamente sobre la garantia que da nombre
al AC6.

### AC2 del intake -- "el que SI intersecta sigue difiriendo": PASS con un residual latente

| Vector | Esperado | Medido |
|---|---|---|
| E3a residuo ajeno dentro del scope | DIFIERE con el par | **PASS** |
| E1b/E1d lo mismo en anidado | DIFIERE con el par | **PASS** |
| E3d scope con comodin (`work/*.txt`) + residuo ajeno que SI intersecta (`work/target.txt`) | DIFIERE | **ARRANCA** -- ver R-3 |

## 5. Residuales declarados

**R-1 (bajo).** La exencion ancla en `$Root`, no en una declaracion explicita de la raiz de gobierno.
Precondicion, no escape: ver AC10.

**R-2 (medio, NO atribuible a esta entrega).** `python scripts/test_exec_lease_harness.py`, que es
`verification_cmd` declarada de TASK-0337, sale **exit 1** en clon limpio a `623fb8b4`, con
`total=31 passed=28 failed=3`:
`test_silent_process_tree_cpu_is_work_derived_and_mutation_proven`,
`test_live_unreadable_lease_is_preserved_and_deadline_mutant_dies`,
`test_admission_liveness_path_uses_production_functions_and_kills_constant_mutants`.
Control historico en clon limpio a `67e58387` (anterior al fix r2): **exit 1, los MISMOS tres**. La
entrega no lo introduce. Consecuencia practica: esta tarea **no se puede cerrar "por exit code" de su
propia `verification_cmd`**; el discriminante tiene que ser la senal propia (el contrato 0337 y los
vectores de conducta), tal como pedia el encargo.

**R-3 (bajo hoy, latente).** `ConvertTo-ComparableRoute` (`:1051`) anula toda ruta con `*?[]`, y
`ConvertTo-ComparableScope` (`:1068`) las **descarta en silencio** en vez de fallar cerrado. Un scope
parcialmente comodinizado deja al guardia parcialmente ciego sin emitir senal: medido en E3d, un
residuo ajeno real en `work/target.txt` deja de diferir cuando la ruta declarada es `work/*.txt`.
Es la direccion contraria a la del guardia hermano de claims, que para este mismo caso falla CERRADO
y tiene contrato propio (`test_glob_claim_scope_fails_closed_and_kills_guard_mutant`). Prevalencia
medida hoy sobre las 458 tareas: **0 tareas con comodin en `scope_routes`**, luego es latente, no
vivo. Lo declaro para que no se descubra el dia que alguien escriba el primero.

**R-4 (bajo).** El fichero de primera-vista del residuo (`$ResiduePath`) sigue siendo GLOBAL, pero
ahora se escribe desde una vista POR MENSAJE: se borra cuando un mensaje no ve residuo relevante
(`:980`) y se reescribe solo con las filas relevantes de ese mensaje (`:1006`, `:1011`). El reloj de
envejecimiento `live`/`aborted` queda expuesto a churn entre mensajes. La direccion de fallo es la
segura -- al perder la marca cae al `LastWriteTimeUtc` real, y para un borrado cae a `$now`, es decir
`live` = diferir --, por eso no lo cuento como escape; lo dejo declarado.

## 6. Reproduccion

```
git clone -s D:/Agentes/multi_agent_project_protocol D:/Aegis_Scratch/protocol/rev0337
cd D:/Aegis_Scratch/protocol/rev0337 && git checkout 623fb8b4
python scripts/validate_collaboration_state.py --root .        # exit 0
python scripts/scan_encoding.py --root .                       # exit 0
python scripts/scan_domain_neutrality.py --root .              # exit 0
python scripts/check_falsification_contracts.py --root .       # exit 0
python scripts/test_exec_lease_harness.py                      # exit 1 (3/31; ver R-2)
python -c "import importlib.util;s=importlib.util.spec_from_file_location('m','examples/mailbox_retry_cases/run_mailbox_retry_cases.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.run_residue_scope_pair_case()"   # exit 0
```

Los vectores E1-E4 se ejercitaron con un banco propio del revisor que lanza el cron real contra
repositorios de laboratorio, en `D:/Aegis_Scratch/protocol/rev0337/adv0337.py` (fuera del arbol
atestado, no entregable). Los mutantes se aplicaron a la PRODUCCION copiada, no a la cadena de
sustitucion del runner.

## 7. Recomendacion de cierre

**CHANGE-REQUIRED.** Dos cosas, y ninguna es de forma:

- **H-1 (bloqueante).** El AC6 no se cumple para la familia que enuncia. La exencion del residuo
  propio esta condicionada a que el scope del mensaje sea resoluble, y en el 63,8 % de las tareas y
  el 26 % de los mensajes abiertos de hoy NO lo es. En esos casos el guardia reproduce la firma exacta
  de NOVA -- `worktree_residue_live` sobre `personal/<Peer>/MEMORY.md`, con `intersections_json=[]` --
  y el interbloqueo circular sigue sin salida. Criterio de aceptacion de la remediacion, por conducta:
  con residuo propio en `personal/<Peer>/**` y un mensaje **sin `task_id` resoluble**, el exec ARRANCA,
  en los dos layouts; y en el mismo par, un residuo AJENO con scope no resoluble sigue difiriendo
  (la remediacion no puede convertirse en "abrir la puerta a todo residuo").
- **H-2 (bloqueante, es el que hace duradero al H-1).** El negativo permanente no protege la garantia
  que le da nombre: borrar la exencion del area personal propia lo deja verde. Criterio: que
  `run_residue_scope_pair_case` **muera** ante el mutante
  `(-not $candidateIsOwnPersonal) -and` -> (borrado), y que incorpore un vector de scope NO resoluble
  en los dos layouts.

Lo demas esta acreditado: AC10 pasa en las dos topologias y no depende del CWD del lanzador, AC7 tiene
negativo real, y el lado del par que debe seguir difiriendo sigue difiriendo.

**Bucle de arreglo declarado.** Remediacion por Codex sobre `scripts/harness/peer_mailbox_cron.ps1` y
`examples/mailbox_retry_cases/run_mailbox_retry_cases.py`. Puertas afectadas y que vuelvo a correr en
clon limpio: `run_residue_scope_pair_case` (exit 0), los tres mutantes
(prefijo / codigo muerto / exencion-propia: los tres deben MORIR), `validate_collaboration_state.py`,
`scan_encoding.py`, `scan_domain_neutrality.py`, `check_falsification_contracts.py`, y los vectores
E1-E4 de este veredicto. Rejuicio ANTES del commit de cierre. **Maximo 2 iteraciones**; a la tercera
escalo al operador humano.

**Sobre el corte de NOVA a las 09:00:** no lo decido yo, pero dejo el dato para que el Arquitecto
decida con el: la pieza arregla el caso con scope resoluble -- que es real y es el que se vio en vivo
esta noche -- y deja vivo el mismo interbloqueo para la mayoria del corpus. Enviarla tal cual da a
NOVA un arreglo parcial que en su instancia parecera intermitente, que es el modo de fallo mas caro de
diagnosticar a distancia.

-- Analista, 2026-08-16, 05:50 local (UTC+2)
