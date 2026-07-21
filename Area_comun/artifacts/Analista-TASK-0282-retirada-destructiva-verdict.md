---
artifact_id: Analista-TASK-0282-retirada-destructiva-verdict
task_id: TASK-0282
reviewer: Analista
verdict: OK-CLOSABLE
anchor_commit: 2d35cf0
canonical_head: 174b34c
created_at: 2026-07-22
---

# Veredicto de cierre - TASK-0282, retirada de la rama destructiva del rollback

Hora local: 2026-07-22 01:30 (reloj del sistema, sin convertir).

## Ancla y reproduccion

Codigo juzgado: `2d35cf0` (fix TASK-0282). El fichero bajo revision,
`scripts/harness/peer_mailbox_cron.ps1`, y la suite `run_mailbox_retry_cases.py` son
**byte-identicos** entre `2d35cf0` y el HEAD canonico `174b34c` (`git diff 2d35cf0 174b34c`
sobre ambas rutas: vacio). Local HEAD == origin/main == `174b34c`. Sin producto en alcance.

Clon limpio en `/d/ccv` (rutas cortas por MAX_PATH), checkout `174b34c`, arbol limpio.
Cuatro gates VERDES alli por exit code, mas drift:

| Gate | Exit |
|---|---|
| `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` | 0 |
| `python scripts/validate_collaboration_state.py` | 0 |
| `python scripts/scan_encoding.py` | 0 |
| `python scripts/scan_domain_neutrality.py` | 0 |
| `protocol_state_drift(.)` -> `has_drift` | False |

Contraste diferencial contra el padre `fafd7fb` (`git diff fafd7fb 2d35cf0 -- ...ps1`): el
diff retira `git reset --hard $HeadBefore`, retira el parametro `$WorktreePatch` y las dos
llamadas `Invoke-PreExecPatch ... $WorktreePatch -Index $false`, retira el snapshot
`git diff --binary --output=$worktreePatch`, y cambia `apply --index` por `apply --cached`.
No queda ninguna copia del harness con los tokens destructivos: `git grep -e "reset --hard"
-e "WorktreePatch" -- '*peer_mailbox_cron*'` no encuentra nada, y solo existe una copia del
harness (no hay export divergente).

## Que hace ahora el rollback (lectura del codigo, funcion Restore-TransientExecResidue)

Orden real, gateado paso a paso:

1. `git read-tree $HeadBefore` (solo indice) con gate por exit -> `index_unstage_failed`.
2. `Invoke-PreExecPatch -PatchPath $IndexPatch -Index $true` (`git apply --cached`) con gate
   por exit -> `index_restore_failed`. **La restauracion del indice ocurre ANTES de cualquier
   movimiento de fichero.**
3. `git ls-files --others --exclude-standard -z` con gate por exit -> `untracked_enumeration_failed`.
4. Por cada untracked NUEVO (no presente en `$UntrackedBefore`): si `Test-LedgerManagedPath`
   -> `continue` (no se toca); si no, `Move-Item` a `.protocol-tmp/rollback-quarantine/<ts>/`
   dentro de su propio `try/catch` -> `quarantine_move_failed`. **Move, nunca Remove.**

La rama de ledger avanzado (evento firmado, `seq`/hash distintos) sigue intacta: preserva el
arbol post-exec completo verificado contra disco y no des-stagea ni mueve nada.

## Tabla vector por vector

| # | Condicion del intake / negativo | Resultado | Evidencia |
|---|---|---|---|
| 1 | NO `reset --hard` y NO re-apply de parche de worktree; codigo eliminado, no condicionado | PASS | diff vs padre; `git grep` sin tokens; una sola copia del harness |
| 2 | Indice restaurado con `git apply --cached` y exit code GATEADO | PASS | lineas 650-653; gate `index_restore_failed` |
| 3 | Indice restaurado ANTES de todo movimiento; cada `Move-Item` aislado; un move que falle no aborta la restauracion ni los demas moves | PASS | orden en codigo (652 antes de 658); `try/catch` por item; el `trap` de funcion no lo captura |
| 4 | Cuarentena (no borrado) con allowlist de mailbox por `Test-LedgerManagedPath` | PASS | suite: `MSG-window.md` sigue en `open/`; mi banco de la allowlist (abajo) |
| 5 | Enumeracion de untracked gateada por exit; si falla, nada se mueve; el snapshot pre-exec tambien gateado | PASS | lineas 656 y 808; mutante `untracked_exit_gate_removed` muere en el contrato |
| 6 | Cuarentena fuera de `Area_comun/` y `runtime/`, bajo `.protocol-tmp/`, y escrito | PASS (con residual R5) | `.gitignore:16` ignora `.protocol-tmp/`; README documenta la ubicacion y el contrato |
| N1 | Exec abortado con trabajo ajeno en el arbol -> el trabajo ajeno SOBREVIVE intacto | PASS (con residuales R1/R2) | `TASK-fixture.md` = `peer-task-edit` intacto; mi Test A prueba que `read-tree` deja el worktree byte-identico |
| N2 | Mensaje entrante en la ventana NO se pone en cuarentena | PASS | suite: `MSG-window.md` == `incoming`; banco allowlist |
| N3 | Fallo del apply del indice: declarado, no silencioso | PASS | gate `index_restore_failed` |
| N4 | Fallo de la enumeracion de untracked: nada se mueve | PASS | gate `untracked_enumeration_failed`, `return` antes del loop |

## Pruebas propias por comportamiento (no confie en nombres de test)

**Test A -- el invariante que sostiene todo.** La garantia "trabajo ajeno byte a byte" depende
por entero de que `git read-tree <tree>` NO toque el worktree. Lo ejecute en sandbox:
un fichero rastreado modificado sin commitear por otro actor -> tras `read-tree $HEAD`, el
worktree queda byte-identico (mismo SHA-256), solo cambia el indice (` M`). Un fichero staged
por el peer queda en el worktree (bytes intactos), solo pasa a untracked. **Confirmado:
read-tree jamas reescribe ni borra contenido del worktree.**

**Test C -- caza de evasion de la allowlist (lo que pediste).** Extraje `Test-LedgerManagedPath`
y le dispare 16 payloads. Toda ruta real de mailbox esta PROTEGIDA: `open/`, `answered/`,
`archived/`, con backslash, minusculas, mayusculas mezcladas. Los unicos `False` con forma de
mailbox son sinteticos: `./Area_comun/mailbox/open/MSG-x.md` (prefijo `./`) y `Area_comun/mailbox`
a secas. Verifique en git real que `git ls-files --others --exclude-standard -z` -- la UNICA
fuente de `$path` -- emite rutas root-relativas limpias, SIN prefijo `./` y sin `..`, incluso
para directorios anidados. Por tanto **la evasion `./` es inalcanzable desde el llamador real**:
un mensaje depositado legitimamente en `Area_comun/mailbox/open/` llega como la forma protegida.
No encontre ningun nombre que evada la allowlist para un mensaje realmente colocado en la cola.

## La pregunta que me hiciste

"Con reset --hard retirado, queda algun camino por el que el rollback siga reescribiendo o
borrando contenido que el exec no creo, o por el que el residuo conservado deje al peer
siguiente sin salida acotada?"

**No, y por eso es GO.** No queda ningun camino que REESCRIBA o BORRE contenido. Las dos unicas
operaciones sobre el arbol son `read-tree` y `apply --cached`, ambas solo-indice (Test A), y un
`Move-Item` a cuarentena que es recuperable y solo alcanza untracked creados EN la ventana y no
gobernados. El contenido rastreado del worktree no se toca nunca; mailbox/state/tasks/runtime-state
no se ponen en cuarentena nunca.

Sobre el residuo que estrangule al peer siguiente: la cuarentena vive bajo `.protocol-tmp/`,
que esta gitignoreado, asi que es INVISIBLE a `git status`/`ls-files` y NO dispara el pre-gate de
residuo de TASK-0281. El otro residuo -- la modificacion del propio exec a un fichero rastreado,
que ya NO se revierte -- deja el arbol sucio y el pre-gate lo ve; pero eso difiere con salida
ACOTADA: `Register-PreExecDefer` topa en `MaxTransientRetries` y emite `RETRY_EXHAUSTED
signal=watchdog`. No hay parada muda ni bucle infinito NUEVO introducido por 0282; ese pre-gate
es la entrega de 0281 (dependencia dura ya cerrada) y su refinamiento es justo el alcance de 0284.

## Residuales declarados (no bloqueantes; algunos firmados por el Operador)

- **R1 (por diseno).** Un fichero creado o staged por OTRO actor de forma concurrente DENTRO de
  la ventana del exec (untracked, no gobernado) se pone en cuarentena (Move a `.protocol-tmp/`,
  recuperable). Es indistinguible de un fichero del exec por definicion; la eleccion firmada fue
  cuarentena-no-borrado justo para este caso. No destructivo.
- **R2 (firmado por el Operador).** Si el exec SOBREESCRIBE un fichero rastreado que otro actor
  tenia sin commitear, el rollback deja el contenido del exec (no revierte el worktree); los
  bytes sin commitear del peer no se restauran. Es la consecuencia directa de retirar el revert
  (el fixture `predirty.txt` asevera `exec-content`). La historia commiteada esta a salvo; solo
  esta en riesgo un cambio sin commitear a un fichero que el exec TAMBIEN escribio, colision de
  escritura concurrente que ningun rollback resuelve.
- **R3 (endurecimiento, inalcanzable hoy).** `Test-LedgerManagedPath` asume entrada normalizada
  por git; una ruta con prefijo `./` o sin normalizar la evadiria, pero el unico llamador la
  alimenta con salida de `git ls-files --others -z`, que nunca produce esas formas (verificado).
  Defensa en profundidad, no una fuga real.
- **R4 (aceptable).** `Area_comun/decisions/` y `Area_comun/reports/` no estan en la allowlist;
  WIP sin firmar bajo esas rutas se pondria en cuarentena (recuperable). Una decision REALMENTE
  firmada queda protegida por la rama de ledger-avanzado (preservacion del arbol completo), no
  por la allowlist. El fixture cubre ese caso (`DECISION-test.md` sobrevive con evento firmado).
- **R5 (documentacion, menor).** El README documenta la ubicacion de la cuarentena y el contrato
  no destructivo, pero la razon explicita del acceptance #6 ("que nadie la mejore hacia dentro
  del arbol gobernado y rompa los escaneos") queda implicita mas que enunciada. La ubicacion es
  correcta y esta gitignoreada; lo doy como pulido, no como bloqueo.

## Sobre la falsabilidad de la suite

`run_nondestructive_rollback_contract()` declara y mata 5 mutantes (reset destructivo, re-apply
de worktree, allowlist quitada, gate de apply quitado, gate de enumeracion quitado); verifique
que el conjunto de supervivientes es vacio. Es un control estatico sobre el texto de la funcion,
complementado por el bucle real que prueba comportamiento: residuo del exec a cuarentena
recuperable, `MSG-window.md` intacto en la cola, fichero rastreado ajeno intacto, y eventos
firmados preservados. Los dos niveles concuerdan con mi lectura y con mis pruebas propias.

## Recomendacion de cierre

**GO -- OK-CLOSABLE.** Las seis condiciones del intake y los cuatro negativos permanentes se
cumplen por comportamiento; los cuatro gates y el drift estan verdes en clon limpio por exit
code. La rama destructiva esta genuinamente retirada: el arbol ajeno deja de poder reescribirse
o borrarse por un exec que aborta. Los residuales R1-R5 son no destructivos y por diseno (R1/R2
respaldados por la enmienda firmada), y ninguno reabre la maquinaria. El harness vivo permanece
sin redesplegar hasta 0284, como corresponde.

-- Analista
