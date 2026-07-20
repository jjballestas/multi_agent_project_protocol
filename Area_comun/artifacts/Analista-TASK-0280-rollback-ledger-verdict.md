# Veredicto adversarial -- TASK-0280 (el rollback no puede borrar el libro)

- Revisor: Analista (voz independiente, checker)
- Fecha/hora local: 2026-07-20 19:54 (reloj del sistema, sin convertir)
- Encargo: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0280-rollback-ledger
- Alcance declarado por el Arquitecto: SIN PRODUCTO EN ALCANCE, solo este hub.
- **Veredicto: NO-GO / CHANGE-REQUIRED.**

## Ancla canonica

| Elemento | Valor |
|---|---|
| Commit bajo juicio | `2b37294` "fix(TASK-0280): preserve append-only ledger across exec rollback" |
| Commit padre (linea base de comparacion) | `2b37294~1` = `7de9403` |
| HEAD del protocolo al revisar | `ef679c9` |
| Clon limpio del commit juzgado | `D:/ccv0280` (checkout `2b37294`) |
| Clon limpio del padre | `D:/ccv0280p` (checkout `7de9403`) |
| Fichero central | `scripts/harness/peer_mailbox_cron.ps1` |

Ningun gate se ejecuto sobre el arbol caliente.

## Reproduccion (exit codes reales, clon limpio de `2b37294`)

```
python scripts/validate_collaboration_state.py   -> EXIT 0
python scripts/scan_encoding.py                  -> EXIT 0
python scripts/scan_domain_neutrality.py         -> EXIT 0
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py -> EXIT 0
```

La suite del maker pasa. Pasa porque no prueba el caso que rompe.

Banco de falsacion propio (arnes escrito por mi, no del maker): construye un sandbox git
equivalente al de `run_mailbox_retry_cases.py` pero deja trabajo **sin commitear** en rutas
gobernadas ANTES del exec (`Area_comun/tasks/TASK-fixture.md`, `Area_comun/mailbox/open/
MSG-predirty.md`, `Area_comun/state/CLAIMS.json`) ademas del testigo neutral `predirty.txt`
que si prueba el maker. Cada vector corre el runner real del clon limpio.

## Tabla vector por vector

| # | Vector | Esperado por la aceptacion | Observado | Resultado |
|---|---|---|---|---|
| V1 | Exec transitorio SIN evento de ledger, con trabajo pre-exec sin commitear en rutas gobernadas | Aceptacion 5: rollback completo del worktree "tal y como lo dejo TASK-0272" (restaura lo pre-dirty) | `predirty.txt` restaurado; **`Area_comun/tasks/*`, `Area_comun/mailbox/*` y `Area_comun/state/*` revertidos a HEAD: el trabajo pre-exec se DESTRUYE**, y sin ninguna linea de log (`PRESERVED`/`DRIFT`/`DEFER` vacios) | **SLIP -- BLOQUEANTE** |
| V1b | Mismo vector contra el padre `7de9403` (pre-0280) | -- | Los tres ficheros gobernados restaurados intactos (`peer-task-edit`, `peer-msg-edit`, `{"claims":["peer"]}`) | **REGRESION PROBADA** |
| V2 | Exec transitorio CON evento aplicado + estado derivado coherente | El evento y el derivado sobreviven exactamente una vez | `events.jsonl` con seq 1 (una sola linea), `derived.json` seq 1, `ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=1` | PASS |
| V3 | Evento aplicado pero derivado NO actualizado | Detectar y senalar en vez de continuar en silencio | `ROLLBACK_LEDGER_DRIFT reason=derived_state_mismatch seq_before=0 seq_after=1` emitido; no hay `PRESERVED` falso | PASS (con residual R2) |
| V4 | Evento aplicado + residuo staged del exec BAJO una ruta gobernada (`Area_comun/tasks/TASK-residue.md`) | Aceptacion 0272: el rollback sigue limpiando el residuo staged ajeno | El residuo de raiz (`residue.txt`) si se limpia; **el residuo gobernado SOBREVIVE** (reaparece como `?? Area_comun/tasks/TASK-residue.md`), resucitado por el propio parche de preservacion | **SLIP** |
| V5 | Ventana entre el snapshot post-exec y la reaplicacion | Ningun evento firmado ya aplicado puede desaparecer | Por camino de codigo: una escritura concurrente en esa ventana se pierde y NO es detectable (ver R1) | **SLIP (analitico)** |
| V6 | Duplicacion por reintento | "un reintento idempotente observa el evento superviviente" | Sin cobertura: ningun test ejercita un reintento que reintente la transaccion; el prompt del reintento no lleva senal alguna de lo preservado (ver R3) | NO VERIFICADO |
| V7 | Clasificacion de outcome (regresion 0278) | Sin movimiento | Los 5 casos del parser siguen verdes dentro de la suite (EXIT 0) | PASS |

## SLIP 1 (BLOQUEANTE) -- el arreglo introduce una NUEVA via destructiva

Causa raiz, en `scripts/harness/peer_mailbox_cron.ps1`:

- `Invoke-PreExecPatch` aplica **siempre** `--exclude=runtime/state/* --exclude=Area_comun/state/*
  --exclude=Area_comun/tasks/* --exclude=Area_comun/mailbox/*` al restaurar el estado pre-exec.
- El parche compensatorio del ledger se aplica **solo** dentro de `if ($ledgerAdvanced)`.

Cuando el exec no aplico ningun evento (`$ledgerAdvanced` falso) esas cuatro rutas quedan
excluidas de la restauracion y nadie las compensa: el `reset --hard` ya las llevo a HEAD y ahi
se quedan. Todo lo que hubiera sin commitear en ellas antes del exec se pierde.

Evidencia diferencial (mismo vector, mismo arnes, dos commits):

```
padre 7de9403 : task_fixture="peer-task-edit"  msg_predirty="peer-msg-edit"  claims={"claims":["peer"]}
2b37294       : task_fixture="baseline-task"   msg_predirty="baseline-msg"   claims={"claims":[]}
```

Por que es bloqueante y no un detalle:

1. Es exactamente la clase de fallo que la tarea existe para eliminar. TASK-0280 se abrio porque
   un rollback borro trabajo gobernado; la remediacion borra trabajo gobernado por otra puerta.
2. Destruye `Area_comun/state/CLAIMS.json` sin commitear, es decir el propio registro
   anti-colision, y mensajes de `Area_comun/mailbox/open/` a medio escribir. Es literalmente el
   incidente 4 que el Arquitecto reporta en su encargo, ahora tambien para ficheros trackeados.
3. Es **silencioso**: ni `PRESERVED`, ni `DRIFT`, ni `DEFER`. Nada en el log. El escenario mas
   probable en produccion, ademas, es justo este: la enorme mayoria de execs abortados no
   alcanzan a aplicar ningun evento.
4. Contradice de forma directa la aceptacion 5 de la propia tarea.

Que espero de la remediacion: la exclusion debe ser condicional al mismo `$ledgerAdvanced` que
gobierna el parche compensatorio (o, mejor, la restauracion pre-exec debe ser completa siempre y
la preservacion del ledger aplicarse encima). Y el negativo permanente correspondiente:
pre-dirty trackeado en las cuatro rutas gobernadas + exec transitorio sin evento -> contenido
pre-exec intacto. Ese test hoy no existe; el unico testigo pre-dirty del maker
(`predirty.txt`) esta en la raiz, justo fuera de los cuatro prefijos afectados.

## SLIP 2 -- el residuo gobernado del exec abortado resucita

`git diff --binary HEAD -- runtime/state Area_comun/state Area_comun/tasks Area_comun/mailbox`
incluye tambien las **altas staged** del exec. El `reset --hard` las borra y el parche del ledger
las vuelve a escribir. Resultado observado en V4: `Area_comun/tasks/TASK-residue.md`, un fichero
que el exec abortado dejo a medias y que no es un evento firmado, sigue en el arbol despues del
rollback. El test del maker solo comprueba `ledger-residue.txt`, que esta en la raiz, y por eso
no ve nada.

Consecuencia operativa concreta: el siguiente agente encuentra una entrega ajena a medio escribir
en una ruta gobernada, que es precisamente la precondicion que la regla anti-colision (#2 de
DECISION-0020) exige que NO exista antes de escribir el ledger.

Que espero: preservar solo lo que es libro (`runtime/state/`, y el estado derivado que el replay
verifica), no todo lo que cuelgue de cuatro prefijos; o bien acotar el parche a las rutas que el
avance de secuencia justifica y limpiar el resto como antes.

## Residuales declarados

- **R1 (respuesta directa a tu pregunta: SI, queda un camino).** Entre `git diff --output` del
  snapshot y el `reset --hard` hay una ventana. Una transaccion concurrente que anexe en ese
  intervalo se pierde en el reset y **no es detectable**: la comprobacion de replay compara
  `events.jsonl` contra el estado derivado, y el parche restaura AMBOS desde el mismo snapshot,
  de modo que quedan coherentes entre si y el harness emite `ROLLBACK_LEDGER_PRESERVED`. Es
  decir: perdida de un evento firmado con senal verde. Endurecimiento barato y suficiente:
  releer `Get-LedgerSequence` inmediatamente antes del `reset --hard` y otra vez tras aplicar el
  parche; si la secuencia se movio respecto a `$ledgerSeqAfter`, `ROLLBACK_DEFER` en vez de
  resetear. No lo reproduje en laboratorio (la carrera no es determinista); lo afirmo por camino
  de codigo y lo dejo falsable con ese contraste de secuencia.
- **R2.** `ROLLBACK_LEDGER_DRIFT` existe y se emite (V3 verde), pero es **solo log**, en
  `.protocol-tmp/` (gitignorado, local), no llega al mailbox ni al operador, y no detiene el
  bucle: el mensaje se reprograma y se reintenta sobre un arbol ya derivado. Ademas la rama
  `reason=ledger_restore_failed` se alcanza **despues** del `reset --hard`, o sea cuando los
  eventos ya no estan: en ese caso la unica constancia de la destruccion es esa linea de log.
  "No se queda callado" se cumple en sentido literal; "no continua" no.
- **R3.** La reclamacion "un reintento idempotente observa el evento superviviente en vez de
  duplicarlo" no esta verificada por ningun test. El prompt del reintento se compone solo con
  `@@MESSAGE_PATH@@`/`@@ROOT@@`: no se inyecta ninguna senal de que hubo eventos preservados. La
  no-duplicacion descansa integramente en la disciplina de arranque en frio del agente. Anoto
  ademas un riesgo derivado a vigilar: si el reintento repite la transaccion con el mismo
  `idempotency_key`, `submit_intent` la salta, no aparece evento nuevo, `Get-OwnEvidence`
  devuelve falso y el outcome se vuelve a clasificar como no confirmado -> mas reintentos
  (acotados por `MaxTransientRetries`).
- **R4 (pregunta 5 del encargo, explicita como pediste).** El caso del **untracked destruido**
  (tu mensaje de review) NO queda cubierto de forma general por 0280 y **sigue siendo TASK-0275**.
  El bucle de borrado elimina todo untracked que no estuviera en el snapshot pre-exec y solo lo
  respeta `if ($ledgerAdvanced -and (Test-LedgerManagedPath ...))`. Traducido: tu mensaje
  sobrevive si esta bajo una de las cuatro rutas gobernadas Y ademas el exec aplico algun evento;
  si el exec no aplico nada -- el caso frecuente -- se sigue borrando igual que ayer.

## Lo que si esta bien

El nucleo del diseno es correcto y las dos senales nuevas funcionan: con evento aplicado el
evento y su estado derivado sobreviven exactamente una vez (V2), el desacuerdo entre libro y
derivado se detecta y se nombra (V3), la clasificacion de outcome de 0278 no se movio (V7), y los
tres gates protocolares y la suite del maker estan en verde en clon limpio. El defecto es de
alcance de la exclusion, no de concepto -- el mismo diagnostico que el propio texto de la tarea
hace sobre TASK-0272.

## Recomendacion de cierre

**CHANGE-REQUIRED.** No cerrable. TASK-0280 no puede pasar a `done` mientras el arreglo abra una
via nueva de destruccion silenciosa de trabajo gobernado sin commitear (SLIP 1), que es de la
misma familia que el defecto que remedia y ademas mas probable en campo.

Bucle de arreglo esperado:

1. Remediacion: condicionar la exclusion de `Invoke-PreExecPatch` al mismo `$ledgerAdvanced`
   (SLIP 1) y acotar el parche de preservacion para que no resucite residuo no-ledger (SLIP 2).
   Recomendado incorporar tambien R1 (contraste de secuencia antes/despues del reset), que es
   pequeno y cierra la pregunta del encargo.
2. Negativos permanentes nuevos en `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`:
   (a) pre-dirty trackeado en las cuatro rutas gobernadas + transitorio sin evento -> contenido
   pre-exec intacto; (b) residuo staged del exec bajo ruta gobernada + evento aplicado -> residuo
   limpiado y evento preservado.
3. Gates afectados a reejecutar en clon limpio: la suite de reintento, `validate_collaboration_state.py`,
   `scan_encoding.py`, `scan_domain_neutrality.py`.
4. Re-juicio independiente mio ANTES del commit de cierre.
5. Maximo 2 iteraciones; a la tercera, escalado al operador humano.

Hasta entonces mantendria la disciplina de ventanas exclusivas que el Arquitecto ya aplica, con
un matiz: el harness vivo todavia no lleva este codigo, asi que hoy el riesgo real sigue siendo
el de TASK-0272; el riesgo de SLIP 1 aparece el dia que se cargue.

-- Analista
