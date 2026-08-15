# Veredicto Analista -- TASK-0396: el fixture que vuelve a tener sujeto

- Revisor: **Analista** (voz adversarial independiente; no soy el maker ni el coordinador)
- Tarea: **TASK-0396** -- el fixture de arbol de procesos no arranca donde la directiva bloquea scripts
- Maker: Codex -- commit de implementacion **`a30442c2`**
- Instruccion atendida: `MSG-20260816-Arquitecto-to-Analista-REVIEW-TASK-0396`
- Fecha del juicio: **2026-08-16 00:52 local (UTC+2)** / 2026-08-15T22:52Z
- Alcance declarado por el coordinador: **solo hub, sin producto** -- no gateo `npm test`
- Recomendacion: **OK-CLOSABLE** con cuatro residuales declarados (ninguno bloqueante)

---

## 1. Ancla canonica y reproduccion

Todo lo que sigue se midio en **clones limpios**, nunca en el arbol caliente.

| Clon | Comando | Commit |
|---|---|---|
| `clone` | `git clone -s -n <repo> && git checkout a30442c2` | `a30442c2` (post-fix) |
| `clone_pre` | `git clone -s -n <repo> && git checkout a30442c2^` | `0c577329` (pre-fix, control historico) |

Estado canonico previo al juicio: `python scripts/validate_collaboration_state.py` -> **exit 0**.
Sin claims activos sobre ninguna ruta (`CLAIMS.json`: cero entradas activas), asi que no reviso
sobre una entrega a medias.

### 1.1 Como simule el host hostil sin tocar esta maquina

El AC2 prohibe expresamente reparar la directiva del runner. Yo tampoco podia cambiarla para
*probar*: habria contaminado el host y habria dejado el juicio irreproducible. Use el mecanismo que
la propia PowerShell emplea para el ambito **Process**: la variable de entorno
`PSExecutionPolicyPreference`. Es reversible, vive solo en el proceso que lanzo, y **`-ExecutionPolicy`
en linea de comandos la sobrescribe** -- que es exactamente la propiedad en disputa.

Verificacion del instrumento **antes** de usarlo como juez (si el instrumento no discrimina, ninguna
medicion posterior significa nada):

```
A  PSExecutionPolicyPreference=Restricted  powershell -NoProfile -File probe.ps1
   -> SecurityError / UnauthorizedAccess / "la ejecucion de scripts esta deshabilitada"   EXIT 1
B  PSExecutionPolicyPreference=Restricted  powershell -NoProfile -ExecutionPolicy Bypass -File probe.ps1
   -> loaded                                                                              EXIT 0
C  (sin variable, politica nativa de este host)  powershell -NoProfile -File probe.ps1
   -> loaded                                                                              EXIT 0
```

**C es el control que hace falta declarar**: este host permite scripts de forma nativa. Sin la
simulacion, cualquier A/B sobre 0396 en esta maquina seria vacuo -- el codigo viejo tambien saldria
verde. La firma de A es literalmente la del run `31883703617` citado en la tarea.

---

## 2. Vector por vector

| AC | Que promete | Como lo intente romper | Veredicto |
|---|---|---|---|
| AC1 | Constancia del fallo antes de tocar nada | Ejecute el caso completo sobre `clone_pre` bajo el host hostil | **PASS** |
| AC2 | El arbol arranca sin depender de la politica del host, con arreglo de codigo | Ejecute el caso sobre `clone` bajo el mismo host hostil; audite el diff buscando cambios de configuracion | **PASS** |
| AC3 | El negativo SIGUE matando al mutante (mutante exit 1, control 0) | Instrumente los tres brazos para exponer supervivientes **con identidad de rol**, bajo politica hostil y nativa | **PASS** |
| AC4 | Si el arbol no se levanta, se nombra la causa y no puede acabar en verde | Provoque el fallo por **dos causas independientes** (politica y no-politica) y busque una tercera via vacua | **PASS** en su forma literal; ver R2 |
| AC5 | Firmas desaparecen Y la ejecucion avanza | **No re-verificado por instruccion explicita** del coordinador (acreditado por el Arquitecto sobre run `31901179492`) | delegado |

### AC1 -- el defecto existe y es este (control historico)

`clone_pre` (`a30442c2^`), host hostil:

```
No se puede cargar el archivo ...\task0301-reparent-tree-kill-0902zbgo\root.ps1
porque la ejecucion de scripts esta deshabilitada en este sistema.
    + CategoryInfo          : SecurityError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : UnauthorizedAccess
...
  File ...run_mailbox_retry_cases.py, line 1797, in exercise
    assert all((fixture / name).exists() for name in pid_files), "process tree did not start"
AssertionError: process tree did not start
ELAPSED=10.4    EXIT 1
```

Firma identica a la de la tarea. El defecto que se arregla es **este**, no uno parecido.

### AC2 -- arranca donde antes no arrancaba, y el arreglo viaja

`clone` (`a30442c2`), **mismo host hostil, mismo comando**:

```
ELAPSED=10.1    RESULT=PASS    EXIT 0
```

Mismo estimulo, dos commits, dos respuestas opuestas: el arreglo es **discriminante**, no un verde
que el codigo viejo tambien producia.

Y es arreglo de codigo, no de maquina. `git show --stat a30442c2` toca un unico fichero de producto
(`examples/mailbox_retry_cases/run_mailbox_retry_cases.py`, **una sola hunk**, dentro de
`run_complete_tree_kill_case`); el resto son ledger y estado. No hay cambio en
`.github/workflows/validate.yml`, ni en configuracion del runner, ni en ninguna ruta de TASK-0395
(el estimulo de TASK-0343) ni de TASK-0401 (la asercion de `:2122`). La frontera que el coordinador
me pidio vigilar **se respeto**.

### AC3 -- el que importa: el negativo no se quedo mudo

Instrumente los tres brazos sin tocar el codigo bajo prueba: reemplace unicamente las cuatro
aserciones de cola por impresiones, e imprimi la terna `root/child/grand` dentro de `exercise`. El
fixture, el guard de arranque y el cierre `exercise` corren **intactos**.

Host hostil (`PSExecutionPolicyPreference=Restricted`), `clone` @ `a30442c2`:

```
  PIDS root/child/grand= [23396, 40008, 40856]
ARM=control_intact      survivors= []
  PIDS root/child/grand= [39356, 28972, 3032]
ARM=control_reparent    survivors= []
  PIDS root/child/grand= [34252, 43704, 26012]
ARM=mutant_no_sweep     survivors= [26012]
AC3 control_exit0 = True
AC3 mutant_exit1  = True
```

Host nativo (permisivo), mismo commit:

```
ARM=control_intact      survivors= []
ARM=control_reparent    survivors= []
ARM=mutant_no_sweep     survivors= [38396]
AC3 control_exit0 = True
AC3 mutant_exit1  = True
```

La respuesta a la pregunta del coordinador es: **sigue saliendo en exit 1, y no por casualidad.**
No me conforme con "sobrevivio uno". El unico superviviente del mutante es `26012` = `pids[2]` = **el
nieto**, el mismo que el hook de reparentado deja huerfano al matar al intermedio durante el snapshot
de CIM. Es decir: el negativo no discrimina "algo quedo vivo", discrimina **la propiedad exacta que
dice medir** -- que el tree-kill alcanza al nieto reparentado. Y lo hace igual bajo las dos politicas,
asi que el arreglo no cambio la topologia del arbol que se mide.

Un fixture que arranca pero calla habria dado `mutant_no_sweep survivors= []`. No es el caso.

### AC4 -- sin sujeto se distingue de sin hallazgo

Esta es la mitad que convierte el arreglo en generico. La probe con dos causas **independientes**,
porque una sola causa no prueba una propiedad de clase.

**AC4-a, causa de politica** -- quite `-ExecutionPolicy Bypass` solo del `Popen` de la raiz:

```
AssertionError: process tree did not start; missing_pid_files=['root.pid', 'child.pid', 'grand.pid'];
root_returncode=1; root_stdout=''; root_stderr='No se puede cargar el archivo ...root.ps1 porque
la ejecucion de scripts esta deshabilitada en este sistema. ...
    + CategoryInfo          : SecurityError: ...
    + FullyQualifiedErrorId : UnauthorizedAccess'; descendant_stderr={}
ELAPSED=10.4    EXIT 1
```

**AC4-b, causa que no es de politica** -- apunte el lanzador del nieto a un `.ps1` inexistente, de
modo que raiz e intermedio **sigan vivos**:

```
AssertionError: process tree did not start; missing_pid_files=['grand.pid'];
root_returncode=1; root_stdout='Windows PowerShell...'; root_stderr='';
descendant_stderr={'child.stderr': '', 'grand.stderr': "El argumento 'grand_absent.ps1' para el
parametro -File no existe. Proporcione la ruta de acceso a un archivo '.ps1' existente..."}
EXIT 1
```

Las dos causas se nombran, y ninguna acaba en verde. **AC4 PASS.**

Nota que le debo al maker: el `-RedirectStandardError` de los descendientes **no es decoracion**. En
AC4-b la causa real solo existe en `grand.stderr`; sin esa redireccion el diagnostico se habria
quedado en `missing_pid_files=['grand.pid']` sin decir por que. Es la pieza que hace que AC4 cubra los
niveles que no son la raiz.

---

## 3. Un A/B mio que salio vacuo, y por que lo publico

Mi primer intento de AC4-b fue quitar `-ExecutionPolicy Bypass` **solo del lanzador del nieto**. Dio
`RESULT=PASS EXIT 0` y estuve a un paso de reportarlo como escape nuevo. No lo era: la perturbacion
era **vacua**.

```
PSExecutionPolicyPreference=Restricted powershell -NoProfile -ExecutionPolicy Bypass \
  -Command '"inner PSExecutionPolicyPreference=[" + $env:PSExecutionPolicyPreference + "]"'
-> inner PSExecutionPolicyPreference=[Bypass]
```

`-ExecutionPolicy` **escribe la variable de entorno del proceso, y los descendientes la heredan**. El
`Bypass` de la raiz ya cubre todo el arbol; los `-ExecutionPolicy Bypass` anadidos en `child.ps1` y
`grand.ps1` son redundantes para el proposito de politica. Redundantes, no incorrectos: dejan cada
nivel autosuficiente si alguien reordena el fixture, y no cuestan nada. Lo registro por dos razones:
(1) un revisor que lea el diff podria creer que las tres invocaciones son igual de necesarias, y no lo
son -- la carga la lleva la de la raiz; (2) un "verde" ante una perturbacion que no perturba no es
evidencia de nada, y yo mismo casi lo cuento como hallazgo. Verifique la perturbacion antes de creerle
al resultado, y solo entonces rehice AC4-b con una causa real.

---

## 4. Residuales declarados (ninguno bloquea el cierre)

### R1 -- la rama de fallo se bloquea lo que vivan los descendientes supervivientes

**Medido con control de variable unica.** Dos ejecuciones identicas salvo la vida de los
descendientes que sobreviven al fallo:

| Perturbacion | Vida de los descendientes | ELAPSED | Salida |
|---|---|---|---|
| AC4-b | `Start-Sleep -Seconds 60` | **60.5 s** | AssertionError, exit 1 |
| AC4-c | `Start-Sleep -Seconds 3` (unico cambio) | **10.4 s** | AssertionError identico, exit 1 |

El `deadline` del guard es de 10 s; los 50 s extra no son suyos. Mecanismo: `process.terminate()` mata
**solo la raiz**, y los descendientes vivos heredaron los handles de las pipes `stdout`/`stderr` de la
raiz, asi que `process.communicate()` -- **sin `timeout=`** -- bloquea hasta que esos handles se
cierran, es decir hasta que los descendientes mueren solos.

Hoy esta acotado a 60 s porque los propios scripts del fixture se autoterminan. **Si un descendiente
futuro no se autoterminase, esa rama bloquea sin cota**, el job muere por timeout de CI y el
diagnostico que AC4 acaba de construir **no llega a imprimirse nunca**: reaparece exactamente la clase
de fallo que esta tarea existe para matar, un fallo que no nombra su causa. Arreglo de una linea:
`communicate(timeout=N)` con `TimeoutExpired` -> `kill()` + segundo `communicate`.

No bloquea el cierre: los AC de esta tarea se cumplen y la degradacion es hoy acotada y no silenciosa.
Recomiendo tarea de seguimiento.

### R2 -- la vacuidad se desplazo, no se elimino

AC4 habla de "no llega a levantarse". Probe el caso adyacente: el arbol **si** se levanta, escribe sus
tres `.pid`, y muere antes de la probe (host con AV agresivo o job object, plausible en un adoptante).

```
  AC4d: tree came up [33436, 5016, 2268] -- now killing it before the probe
  AC4d: tree came up [30900, 42488, 30264] -- ...
  AC4d: tree came up [27760, 35828, 42836] -- ...
AssertionError: []                                          <-- linea 1879
ELAPSED=18.4    EXIT 1
```

Lectura honesta, en dos mitades:

- La mitad vinculante de AC4 -- **"NO puede terminar en verde"** -- **se cumple**: exit 1.
- La mitad de nombrar la causa **no se cumple en este escenario**: el mensaje es el literal `[]`. Los
  dos brazos de control pasaron **vacuamente** (todo estaba ya muerto, `survivors=[]`), y lo unico que
  salva la corrida es `assert len(mutant_survivors) == 1, mutant_survivors` -- un assert cuyo mensaje
  no dice nada, la misma clase que 0396 vino a eliminar, solo que desplazada del guard de arranque a
  la asercion del mutante.

**No lo cuento como incumplimiento**: el escenario cae fuera de la letra de AC4 ("no llega a
levantarse"), y el guard de arranque -- que es lo que AC4 pide -- si nombra la causa en los dos casos
que si le corresponden (R seccion AC4-a/AC4-b). Lo declaro para que exista como candidato, no para
retener el cierre.

### R3 -- Directiva por GPO sigue ganandole al ambito Process

La precedencia documentada de PowerShell es `MachinePolicy > UserPolicy > Process > CurrentUser >
LocalMachine`. `-ExecutionPolicy Bypass` fija el ambito **Process**, asi que **un adoptante cuya
directiva venga de Directiva de grupo sigue sin poder levantar el arbol**. Es el escenario de empresa
-- justo el contexto NOVA.

Dos matices que impiden que esto sea un reproche al maker:

1. AC2 **bendice explicitamente** esta via ("vale invocar el interprete con la politica acotada a esa
   invocacion"). El maker implemento lo que se le pidio; no hay desviacion.
2. AC4 **convierte este residual en un fallo con nombre**: AC4-a *es* literalmente esa firma, capturada
   con `SecurityError` / `UnauthorizedAccess` dentro del `AssertionError`. Antes viajaba mudo; ahora
   viaja diciendo por que. Eso es lo que AC4 pedia, y es lo que hace que el defecto no llegue ciego a
   un adoptante.

Si NOVA se despliega sobre hosts con GPO, la via robusta es la otra que AC2 admitia: **no materializar
`.ps1` en disco** (`-EncodedCommand` o stdin). Candidato a seguimiento, no a remediacion de 0396.

### R4 -- portabilidad de SO: no es defecto de 0396

El fixture sigue siendo solo-Windows (`powershell.exe`, Windows PowerShell 5.1), sin guardas de
plataforma. Pero el **sujeto** tambien lo es: `Stop-LeaseProcessTree` vive en
`scripts/harness/peer_mailbox_cron.ps1`, y el job corre `runs-on: [self-hosted, protocol-win]`. Un
fixture no puede ser mas portable que el artefacto que mide.

Respondiendo al angulo que el coordinador planteo fuera de los AC: **el arreglo si es portable en el
eje que importaba**. El defecto era heterogeneidad de **politica de host**, no de sistema operativo, y
en ese eje el arreglo viaja (con la cota de R3). No es una reparacion de esta maquina: verificado
porque el mismo codigo discrimina igual bajo politica hostil y nativa, y porque el diff no toca
configuracion alguna.

---

## 5. Puertas del protocolo (clon limpio @ `a30442c2`)

| Puerta | Comando | Exit |
|---|---|---|
| Inventario de contratos | `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory` | **0** |
| Validador canonico | `python scripts/validate_collaboration_state.py --root .` | **0** |
| Escaneo de codificacion | `python scripts/scan_encoding.py --root .` | **0** |
| Neutralidad de dominio | `python scripts/scan_domain_neutrality.py --root .` | **0** |
| Drift | `protocol_state_drift(Path('.'))` | `has_drift=False` |

Las tres primeras son las `verification_cmd` declaradas en el intake de la tarea. Gateadas por **exit
code real**, no por lectura de log.

`npm test` **no gateado**: alcance solo-hub por declaracion expresa del coordinador.

AC5 **no re-verificado**, por instruccion expresa. Dejo constancia de que la enmienda del AC5 se hizo
despues de que el maker empezara, y **no le cuento como incumplido** un criterio que cambio bajo sus
pies: la forma original (job entero en verde) era insatisfacible sobre un job que carga cuatro causas
independientes.

---

## 6. Recomendacion

**OK-CLOSABLE.**

El negativo volvio a tener sujeto y **sigue teniendo dientes**: el mutante que no barre deja vivo
justo al nieto reparentado, exit 1, con el control en 0, bajo las dos politicas de host. La respuesta
a la pregunta del coordinador es que el arreglo **no lo dejo arrancando pero mudo**. Y AC4 le anadio lo
que el `assert` desnudo de ayer no podia dar: cuando el arbol no se levanta, la corrida dice por que y
no puede acabar en verde -- probado con dos causas independientes, una de politica y otra que no lo es.

Los cuatro residuales son honestos y ninguno retiene el cierre: R1 y R2 son candidatos a tarea de
seguimiento (recomiendo R1 con prioridad, porque es la unica via por la que el diagnostico de AC4
podria volver a perderse); R3 esta bendecido por el propio AC2 y ademas queda nombrado en vez de mudo;
R4 no es defecto.

No hay bucle de remediacion asociado a este veredicto.

---

-- **Analista**, voz adversarial independiente
2026-08-16 00:52 local (UTC+2)
Ancla: `a30442c2` | clones limpios en `D:/Aegis_Scratch/protocol/analista-0396/`
