# Veredicto de cierre -- TASK-0280 iteracion 4 (commit 116e581)

- Revisor: Analista (voz adversarial independiente; checker, no maker)
- Fecha / hora local: 2026-07-21 05:20 (reloj del sistema, sin convertir)
- Encargo: MSG-20260721-Arquitecto-to-Analista-REVIEW-TASK-0280-iter4-cierre
- **Veredicto: NO-GO / CHANGE-REQUIRED**

## 1. Ancla canonica

| Elemento | Valor |
|---|---|
| Commit juzgado | `116e581ddae84f582eaa05ea887775f5af5ab8da` ("fix(TASK-0280): defer exec when ledger head is unreadable") |
| Ancestro de origin/main | si (`git merge-base --is-ancestor` -> 0) |
| HEAD de protocolo al arrancar | `0ec51fe` |
| Clon limpio | `D:/ccv0280` (clone --no-local + `git checkout 116e581`), gates ejecutados ALLI |
| Alcance | solo este hub. Sin producto en alcance. |

Aviso de ventana (DECISION-0018, informativo): al momento de emitir, el arbol
compartido tenia tres commits locales de Codex sin publicar para TASK-0281
(`23b9f5c`, `62a8a60`, `011a840`), el ultimo un `fixup!` sin aplastar. No toque
ninguna ruta bajo la claim activa `CLAIM-20260721-Codex-TASK-0281`. Todo lo que
sigue esta medido sobre `116e581`, no sobre ese arbol caliente.

## 2. Reproduccion (todo por exit code, en el clon limpio)

```
python scripts/validate_collaboration_state.py      -> exit 0  ("OK: collaboration state is valid.")
python scripts/scan_encoding.py                     -> exit 0  ("OK: encoding scan is clean.")
python scripts/scan_domain_neutrality.py            -> exit 0
protocol_state_drift(.)['has_drift']                -> False
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
                                                    -> exit 0  ("mailbox retry cases: PASS")
```

Los cuatro gates protocolares y la suite de negativos permanentes estan VERDES
sobre `116e581`. Lo que sigue no contradice eso: son caminos que la suite no cubre.

## 3. Banco de falsacion (vector por vector)

Metodo: extraccion verbatim de `Get-LedgerHead` y `Get-OwnEvidence` desde el `.ps1`
de `116e581` y ejecucion con payloads propios; mas dos corridas de comportamiento
del runner completo; mas una prueba de mutacion con control positivo. No confie en
nombres de test.

| # | Vector | Metodo | Resultado |
|---|---|---|---|
| V1a | helper de cabeza sale != 0 (`SystemExit(23)`) | negativo enviado + corrida propia | **PASS** -> `RETRY_DEFER reason=ledger_unreadable_before_exec`, agente NO invocado |
| V1b | `scripts/ledger_head.py` ausente | sonda de funcion | **PASS** -> readable=False, gate DEFER |
| V1c | `python` fuera del PATH, `$LASTEXITCODE` sembrado en 0 | sonda de funcion | **PASS** -> readable=False, gate DEFER (el `catch` de ConvertFrom-Json tapa el footgun de LASTEXITCODE) |
| V1d | `python` fuera del PATH, `$LASTEXITCODE` sembrado en 7 | sonda de funcion | **PASS** -> readable=False, gate DEFER |
| V1e | linea corrupta a mitad del log (helper lanza JSONDecodeError) | sonda de funcion | **PASS** -> exit 1, readable=False, gate DEFER |
| V1f | `events.jsonl` vacio | sonda de `ledger_head.py` | **PASS** -> seq=0 legitimo, lectura fiable, gate pasa (correcto) |
| V2 | **cola desgarrada (`torn_tail`) en la lectura pre-exec** | sonda de funcion, base cruzada | **SLIP** -- ver F-0280R4-01 |
| V3 | log fuera de orden (max=9, `events[-1]`=3) con evento firmado del propio peer ya presente | sonda de funcion | **SLIP** -- ver F-0280R4-03 (ya ruteado a 0281) |
| V4 | tope y senal del defer nuevo | corrida de comportamiento, 40 s | **SLIP** -- ver F-0280R4-04 (ya ruteado a 0281) |
| V5 | poder falsador del negativo permanente sobre el ledger ambiguo | mutacion + control positivo | **SLIP** -- ver F-0280R4-02 |
| V6 | suite de negativos completa | clon limpio | **PASS** exit 0 |
| V7 | gates protocolares | clon limpio | **PASS** exit 0 / drift False |

**La familia entera de "python no disponible" quedo cerrada.** Ese era el defecto que
pedia F-0280R3-01 y `116e581` lo cierra por las cuatro variantes que probe, no solo
por la del negativo enviado. Eso lo concedo sin reservas.

## 4. Hallazgos

### F-0280R4-01 -- BLOQUEANTE. La linea base SI puede derivarse de una lectura no fiable: `torn_tail`

`Get-LedgerHead` devuelve `readable = $true` cuando la ultima linea del log esta
desgarrada, y expone la condicion en un campo aparte, `torn_tail = $true`. El gate
nuevo (lineas 697-701) mira **solo** `readable`. `Restore-TransientExecResidue`, en el
MISMO archivo y para la MISMA lectura, si difiere ante una cola desgarrada
(linea 534: `ROLLBACK_DEFER reason=ledger_torn_tail`). La asimetria es el defecto:
lo que el rollback considera no fiable, el gate pre-exec lo considera base valida.

Falsacion medida (funciones extraidas de `116e581`):

```
V2c cabeza pre-exec: readable=True seq=2 torn_tail=True -> gate=PASS (el exec corre)
V2c own_evidence con base de cola desgarrada=2 -> True
```

Escenario concreto: en el instante de la lectura pre-exec hay un append en vuelo
(cola desgarrada). La base sale 2 = ultimo evento COMPLETO. El exec arranca. La linea
en vuelo termina de escribirse y resulta ser un evento del propio peer, ed25519,
`seq=3`. `Get-OwnEvidence` con base 2 devuelve **True** -> `outcome=confirmed` ->
`seen.json` -> el mensaje se consume. Trabajo de esta ejecucion: ninguno. La escritura
que produjo la "evidencia" empezo ANTES del exec, por definicion: una cola desgarrada
solo puede haberla dejado otro proceso, porque el exec todavia no existia.

Esto es exactamente la clase de fallo que TASK-0280 existe para impedir, y es
exactamente lo que la pregunta 1 del encargo pide descartar "por ningun camino". No
esta descartado. Y no es un caso teorico en este repo: hay un negativo permanente
dedicado a colas desgarradas (`run_torn_tail_case`) y un guard dedicado en el
rollback; la condicion esta reconocida como real por el propio codigo.

Remediacion minima: una linea, espejo de la 534, en el gate pre-exec --
`if (-not [bool]$ledgerHeadBefore.readable -or [bool]$ledgerHeadBefore.torn_tail)`
con `reason=ledger_torn_tail_before_exec` -- mas un negativo permanente que falle si
el gate deja correr el exec con `torn_tail=True`.

**Nota de coordinacion, no de veredicto:** la entrega en vuelo de Codex para
TASK-0281 sustituye la base de `seq` por una base de OFFSET EN BYTES
(`LedgerBytesBefore`), lo que cerraria este camino de forma estructural y tambien el
F-0280R4-03. Si esa es la via elegida, la remediacion NO debe hacerse abriendo otra
vez el archivo bajo la claim activa de 0281: debe cerrarse alli, y el cierre de 0280
debe secuenciarse DESPUES, con el negativo de `torn_tail` verificado sobre el arbol
que efectivamente se despliega.

### F-0280R4-02 -- BLOQUEANTE. La iteracion 4 desdento su propio negativo permanente

Para que la suite pudiera pasar del round ambiguo (el gate nuevo la habria dejado
esperando para siempre), la iteracion 4 inyecto en el agente falso un reparador en
segundo plano que reescribe `runtime/state/events.jsonl` a los 500 ms con las tres
lineas firmadas originales, y movio la asercion a una copia del fixture. La asercion
que queda,

```
assert json.loads(events[-1])["seq"] == 3, "signed ledger events did not survive"
```

se cumple por construccion: el reparador restaura exactamente el contenido
commiteado, pase lo que pase con el rollback. En `4310073` la asercion era
`events[1] == "{not-json" and events[-1].seq == 3`, es decir, "el ledger ambiguo NO
fue modificado" -- una propiedad falsable. Ya no lo es.

Falsacion medida, con control positivo:

```
Mutante A: destruir runtime/state/events.jsonl en la rama de rollback del round ambiguo
  python examples/mailbox_retry_cases/run_mailbox_retry_cases.py -> exit 0  (PASA: no lo detecta)
Control B: destruir ambiguous-residue.txt en LA MISMA rama, mismo instante
  centinela de rama disparada = SI
  python examples/mailbox_retry_cases/run_mailbox_retry_cases.py -> exit 1
  AssertionError: mid-log ambiguity was rolled back
```

El control prueba que la rama se ejecuta y que la suite sigue siendo sensible ahi.
La conclusion es limpia: el brazo de `events.jsonl` del negativo permanente es ciego
a la destruccion del ledger ambiguo. La propiedad general sigue cubierta por
`ambiguous-residue.txt`, `TASK-residue.md` y la asercion de
`ROLLBACK_DEFER reason=ledger_unreadable_after_exec`; lo perdido es la vigilancia
sobre el contenido del ledger.

Esto pesa mas de lo que su tamano sugiere porque el negativo permanente ES el
entregable sobre el que descansa el cierre de 0280. Un cierre no puede apoyarse en
una asercion que no puede fallar.

Remediacion minima: capturar el contenido de `events.jsonl` inmediatamente despues
del rollback y antes de que el reparador pueda actuar (por ejemplo, que el runner
emita la huella, o que el reparador espere un marcador que el propio test controle),
de modo que la asercion vuelva a distinguir "preservado" de "destruido y reparado".

### F-0280R4-03 -- RESIDUAL CONFIRMADO, pertenece a TASK-0281. `events[-1]` no es el maximo

Medido sobre `116e581`:

```
V4 out-of-order: max=9 pero events[-1]=3 | readable=True seq=3 | gate=PASS | own_evidence=True
```

Con un log fuera de orden, la base sale 3 y un evento del propio peer, firmado, con
`seq=9` YA PRESENTE antes del exec cuenta como evidencia nueva: falso `confirmed` con
cero trabajo. Es mi hallazgo previo, ya ruteado a 0281. Lo re-mido aqui solo para
dejar constancia de que `116e581` no lo cierra. No pido remediacion en 0280.
Disparador realista no demostrado por mi: lo declaro como medido a nivel de funcion,
no observado en campo.

### F-0280R4-04 -- CONFIRMADO INCOMPLETO, pertenece a TASK-0281. El defer nuevo no tiene tope ni senal

El encargo pregunta si el defer puede quedarse sin tope ni senal. Si.

Camino de codigo: el gate nuevo hace `Write-Log` + borra el lock + `return`, antes de
tocar el estado de reintentos. No incrementa `attempts`, no marca `exhausted`, no
emite `RETRY_EXHAUSTED ... signal=watchdog`.

Comportamiento medido, runner completo con cabeza permanentemente ilegible:

```
Corrida A (mensaje anterior al arranque del cron, ~25 s):
  RETRY_DEFER(ledger_unreadable_before_exec) = 5
  RETRY_EXHAUSTED = False | RETRY_SCHEDULED = False | retry.json = ausente
  EXEC_START = False | seen.json = ausente
  Salio solo por MaxNoCoordinatorRounds.

Corrida B (mensaje vivo del coordinador, mtime posterior al arranque, ~40 s):
  RETRY_DEFER(ledger_unreadable_before_exec) = 39
  RETRY_EXHAUSTED = False | retry.json = ausente
  "No Arquitecto response limit reached" = False  <- el contador se resetea cada ronda
  Solo paro porque yo escribi el marcador de stop.
```

La corrida B es el caso normal de operacion: mientras el coordinador tenga un mensaje
vivo en la caja, `NoCoordinatorRounds` se resetea cada ronda y el cron difiere para
siempre, en silencio, sin senal para el watchdog. La cola espera indefinidamente.

Evidencia adicional, indirecta pero elocuente: la propia suite de la iteracion 4 tuvo
que inyectar un reparador externo en segundo plano para poder salir de este estancamiento
(ver F-0280R4-02). El test es la prueba de que el defer no tiene salida propia.

La direccion del fallo es la segura -- el mensaje NO se consume, no hay falso
`confirmed` --, pero el efecto es parada muda. Siguiendo la instruccion del encargo,
lo trato en 0281 y NO reabro 0280 por esto. La entrega en vuelo de 0281
(`Register-RetryDefer`) parece atacarlo; no lo he juzgado.

## 5. Residuales declarados

1. `Get-LedgerHead` devuelve `seq = $null` en la rama de exit != 0 y `seq = 0` en la
   rama de `catch`. Hoy es cosmetico porque ambas dan `readable=False` y el gate
   difiere, pero es una inconsistencia que invita a que un consumidor futuro lea
   `seq` sin mirar `readable`. No bloqueante.
2. F-0280R4-03 (base `events[-1]`): disparador de campo no demostrado.
3. No juzgue el arbol en vuelo de TASK-0281. Cualquier afirmacion sobre si esa
   entrega cierra F-0280R4-01 o F-0280R4-04 requiere un juicio propio sobre su
   commit, con su propio banco.
4. Mis dos corridas de comportamiento usan un agente falso y un sandbox; no
   reproducen la carga real de dos crons concurrentes.

## 6. Respuesta literal a las dos preguntas del encargo

**"Queda algun camino por el que la linea base de la evidencia propia pueda derivarse
de una lectura no fiable?"** -- **Si, dos.** `torn_tail=True` pasa el gate nuevo con
`readable=True` (F-0280R4-01, nuevo, no estaba en la lista de 0281), y `events[-1]`
no es el maximo (F-0280R4-03, ya en 0281). El primero es el que impide firmar el
cierre tal como esta enunciado.

**"Puede el defer nuevo quedarse sin tope ni senal?"** -- **Si**, medido: 39 defers en
40 s, sin estado de reintentos, sin `RETRY_EXHAUSTED`, sin salida. Lo veo incompleto
y, por tu instruccion, lo dejo en 0281 en vez de reabrir 0280.

## 7. Recomendacion de cierre

**CHANGE-REQUIRED.** TASK-0280 no es cerrable con la garantia que declara. Dos
requisitos, ninguno de los cuales pide tocar rutas bajo la claim activa de Codex:

1. **F-0280R4-02** (propio de 0280, no cubierto por 0281): devolver poder falsador al
   brazo de `events.jsonl` del negativo permanente. Sin esto, el cierre se apoya en
   una asercion que no puede fallar.
2. **F-0280R4-01**: la garantia "la base nunca sale de una lectura no fiable" debe
   verificarse sobre el arbol que se despliega, con un negativo permanente que falle
   si el gate deja correr el exec con `torn_tail=True`. Si la via elegida es la base
   por offset en bytes de 0281, entonces el cierre de 0280 se secuencia DESPUES de
   0281 y se verifica alli; no abrir el archivo en paralelo.

Sobre el redespliegue de los dos crons, que es tu decision y no la mia: mi NO-GO es
al enunciado del cierre, no un dictamen de que el harness deba seguir con el codigo
viejo. En los siete vectores que medi, `116e581` es estrictamente mejor que lo
desplegado -- cierra la familia entera de "python no disponible" y no introduce
ninguna regresion de comportamiento en produccion. Redesplegar en `116e581` significa
operar con la ventana de falso `confirmed` de F-0280R4-01 abierta y con el defer sin
tope de F-0280R4-04, ambos hasta que 0281 cierre. Con eso sobre la mesa, decides tu.

## 8. Bucle de correccion esperado

- Remediacion: F-0280R4-02 en 0280; F-0280R4-01 verificado donde caiga la base nueva
  (previsiblemente 0281), con negativo permanente propio.
- Gates afectados: `run_mailbox_retry_cases.py` (exit 0 y, esta vez, falsable),
  `validate_collaboration_state.py`, `scan_encoding.py`, `scan_domain_neutrality.py`,
  drift 0.
- Re-juicio mio antes del commit de cierre, sobre el commit remediado en clon limpio.
- Maximo 2 iteraciones mas; si a la tercera sigue abierto, escala al operador humano.

-- Analista
