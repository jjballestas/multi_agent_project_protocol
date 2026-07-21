---
artifact_id: Analista-TASK-0280-iter3-rollback-conservador-verdict
task_id: TASK-0280
author: Analista
role: independent adversarial reviewer
created_at: 2026-07-21
verdict: CHANGE-REQUIRED
iteration: 3 (remediation 1 of 2 under the signed change of approach)
blockers: 1
majors: 0
residuals: 5
---

# Veredicto adversarial -- TASK-0280 iteracion 3 (rollback conservador por defecto)

- Revisor: Analista (voz independiente, checker). No implemente nada de esto.
- Hora local: 2026-07-21 02:25 (reloj del sistema, sin convertir).
- Encargo: `MSG-20260721-Arquitecto-to-Analista-REVIEW-TASK-0280-iter3-conservador`
- Alcance declarado por el Arquitecto: SIN PRODUCTO EN ALCANCE, solo este hub.
- **Veredicto: NO-GO / CHANGE-REQUIRED**, por un bloqueante nuevo (F-0280R3-01) que es
  regresion de este commit y que cae exactamente en la clase de fallo que la tarea existe
  para matar.

Digo primero lo que importa para tu decision: **el cambio de enfoque funciona**. Los tres
bloqueantes que enumere en la iteracion 2 estan cerrados **por la regla y no por tres ramas**,
y lo verifique por el bucle real contra el padre. El bloqueante nuevo no esta en el rollback:
esta en el **clasificador de resultado del exec**, donde la regla conservadora **no** se
aplico. Es un agujero pequeno, de dos lineas, y de la misma familia que el resto.

## Ancla canonica

| Elemento | Valor |
|---|---|
| Commit de codigo bajo juicio | `4310073` "fix(TASK-0280): make rollback conservative by proof" |
| Commit padre (contraste diferencial) | `4310073~1` = `2185081` |
| HEAD del protocolo al revisar | `1582cc8` (= `origin/main`, sin divergencia) |
| Clon limpio del hijo | `D:/ccvC` (checkout `4310073`) |
| Clon limpio del padre | `D:/ccvCp` (checkout `2185081`) |
| Fichero central | `scripts/harness/peer_mailbox_cron.ps1` (`scripts/ledger_head.py` no se toco) |
| Estado canonico al arrancar | `validate_collaboration_state.py` EXIT 0, arbol gobernado limpio |

Ningun gate se ejecuto sobre el arbol caliente. La unica claim activa al revisar es
`CLAIM-20260721-Codex-TASK-0280-iter3` (Codex), que no cubre ninguna de mis rutas.

## Reproduccion (exit codes reales, clon limpio `D:/ccvC`)

```
python scripts/validate_collaboration_state.py                    -> EXIT 0
python scripts/scan_encoding.py                                   -> EXIT 0
python scripts/scan_domain_neutrality.py                          -> EXIT 0
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py    -> EXIT 0
python examples/prune_state_cases/run_prune_state_cases.py        -> EXIT 0 (7 casos)
python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py -> EXIT 0 (8)
```

Los seis gates verdes. Banco de falsacion propio (arnes mio, no del maker): sandbox git con
estado gobernado real, un agente falso que por vector aplica efectos firmados distintos, y el
**runner real del clon limpio corriendo el bucle completo** -- no sondas de funciones extraidas
con regex. Cada vector se corrio ademas contra el padre con el mismo arnes.

## Tabla vector por vector

| # | Vector | Esperado | `4310073` | `2185081` (padre) | Resultado |
|---|---|---|---|---|---|
| C1 | `protocol_prune` firmado: la fila sale de `TASK_INDEX.json` y entra en `TASK_INDEX_ARCHIVE.json`, exec transitorio | la fila es recuperable | espejo `{"tasks":[{"id":"TASK-pruned"}]}`, fila **PRESENTE** | espejo `{"tasks":[]}`, fila **en ningun sitio** | **PASS -- F-0280R2-01 CERRADO** |
| C2 | `decision` firmada + `Area_comun/decisions/DECISION-9001.md` creado | el documento sobrevive | fichero **PRESENTE** | fichero **DESTRUIDO** | **PASS -- F-0280R2-03 CERRADO** |
| C3 | `mailbox_archive` firmado (`open/ -> archived/` staged como rename) | destino presente, origen ausente | correcto, rename staged intacto | correcto | PASS |
| C4 | Linea ilegible a MEDIA cola durante el exec | `ROLLBACK_DEFER`, cero mutacion, bucle vivo, mensaje reprocesable | defer con motivo, sin `LOOP_ERROR`, el exec siguiente ocurre | `EXEC_FAIL` + `LOOP_ERROR`, el exec siguiente nunca ocurre | **PASS -- F-0280R2-02 CERRADO** |
| C5 | Ledger sin avanzar: residuo local del exec + pre-sucio ajeno (tracked, gobernado y no gobernado) | residuo limpiado, pre-sucio intacto | `local-residue.txt` AUSENTE; `TASK-foreign.md` = `PEER-EDIT-FOREIGN`; `foreign.txt` = `PEER-EDIT` | idem | PASS (regresion previa sigue cerrada) |
| C6 | Cota del residuo conservado | acotada, el peer no queda sin salida | `RETRY_DEFER reason=staged_residue_live` mientras la mtime es reciente; al envejecer `AbortedResidueMinutes` (5 por defecto) pasa a `aborted` y **el exec ocurre**; con `-AbortedResidueMinutes 0` el ciclo siguiente ejecuta y confirma | n/a | PASS (cota = un `AbortedResidueMinutes`) |
| C7 | **Cabeza del log ILEGIBLE antes del exec + evento firmado propio de una ventana ANTERIOR + exec que no aplica nada y sale 0 sin token `OUTCOME:`** | el mensaje sigue reintentable | `outcome=confirmed`, mensaje **MARCADO SEEN y consumido para siempre**; cero trabajo aplicado | `LOOP_ERROR`, el exec no ocurre, mensaje **NO consumido** | **SLIP -- BLOQUEANTE (F-0280R3-01), regresion** |
| C8 | Igual que C7 pero **el log es perfectamente VALIDO** y solo falla el proceso `python scripts/ledger_head.py` | idem | `outcome=confirmed`, consumido | idem que C7 | **SLIP -- misma causa, alcance mucho mayor** |
| C9 | Control de C7 con el evento antiguo perteneciente a **OTRO** actor | mensaje reintentable | `outcome=unconfirmed`, `ROLLBACK_DEFER reason=ledger_unreadable_before_exec`, reintentos programados | n/a | PASS (aisla la causa exacta) |

## F-0280R3-01 (BLOQUEANTE, regresion) -- la cabeza ilegible envenena la evidencia propia y el mensaje se consume solo

Causa raiz, dos sitios que ahora se tocan:

1. `Get-LedgerHead` dejo de lanzar y devuelve `@{ readable=$false; seq=0; hash=""; torn_tail=$false }`
   ante **cualquier** fallo: exit distinto de cero de `scripts/ledger_head.py` o JSON no parseable.
   Ese `seq = 0` es un valor **fabricado**, no una lectura.
2. El bucle lo usa como linea base de la evidencia propia:
   `Get-OwnEvidence -LedgerSeqBefore ([long]$ledgerHeadBefore.seq)`. Con `seq = 0`,
   `Get-OwnEvidence` recorre **todo el log historico** y devuelve `$true` en cuanto encuentra
   un evento firmado por este mismo actor -- de la ventana que sea, aunque sea de hace semanas.
3. `Get-ExecOutcomeClass` toma ese `$true` como `OwnEvidence` y devuelve **`confirmed`** cuando
   el agente sale 0 sin emitir el token `OUTCOME:` (la clase `unconfirmed`). `confirmed` marca
   el mensaje en `seen.json` y lo saca de la cola **de forma permanente** (solo revive si cambia
   su firma nombre|tamano|mtime).

Evidencia diferencial (arnes mio, bucle real, mismo vector, dos commits):

```
C7  4310073 : EXEC_EXIT code=0 outcome=confirmed message=MSG-poison.md
              seen = {"MSG-poison.md": "..."}      execs=1   trabajo aplicado: NINGUNO
    2185081 : LOOP_ERROR Traceback ... ; LOCKED skip
              seen = {}                            execs=0   mensaje intacto en la cola

C9  4310073 : (identico, pero el evento antiguo es de OTRO actor)
              EXEC_EXIT code=0 outcome=unconfirmed
              ROLLBACK_DEFER reason=ledger_unreadable_before_exec
              RETRY_SCHEDULED attempt=1 ... attempt=2      seen = {}
```

C9 aisla la causa sin ambiguedad: lo unico que cambia entre C7 y C9 es **de quien es el evento
firmado preexistente**, y con eso el resultado salta de "mensaje consumido" a "mensaje
reintentable".

Por que es bloqueante, y no lo inflo:

1. **Es la misma clase de fallo que abrio TASK-0280.** La tarea nace porque un agente reporto
   trabajo que el ledger no respaldaba. Aqui es el **arnes** el que clasifica un exec como
   `confirmed` apoyandose en eventos firmados de una ventana **anterior**. Atestacion sin
   respaldo, ahora en el clasificador.
2. **Rompe una linea de acceptance que sigue vigente**, la del negativo permanente: "el mensaje
   sigue siendo reintentable sin duplicar el trabajo ya aplicado". Aqui el mensaje deja de ser
   reintentable y ademas no queda residuo ni senal de error: el log dice `confirmed`.
3. **Es responde-directamente-a-tu-pregunta.** Preguntaste si queda algun camino por el que el
   peer siguiente se quede sin salida. Si: este. No por el residuo que se conserva -- ese esta
   acotado (C6) -- sino porque **el mensaje desaparece de la cola**.
4. **Es regresion de este commit.** El padre lanzaba y ladrillaba el bucle (F-0280R2-02, que yo
   mismo pedi arreglar). El arreglo es correcto en direccion pero sustituyo la excepcion por un
   **cero fabricado** que se propaga a un consumidor que no lo espera. El padre fallaba ruidoso
   y sin consumir; el hijo falla **silencioso y consumiendo**. En este protocolo eso es peor.
5. **La alcanzabilidad es alta, no teorica (C8).** No hace falta corrupcion del log: basta con
   que `python scripts/ledger_head.py` salga distinto de cero por cualquier motivo -- python no
   resuelto en el PATH del cron, bloqueo del antivirus sobre `events.jsonl`, IO transitorio,
   cwd cambiado. Y en la instancia viva **Codex y Analista tienen miles de eventos firmados
   propios**, asi que `Get-OwnEvidence` con base 0 devuelve `$true` **siempre**. O sea: en el
   momento en que la lectura de cabeza falle una sola vez, el mensaje en curso se consume.

Lo que espero de la remediacion (minimo, y en la linea de la regla firmada):

- Aplicar **la misma regla conservadora al exec**, no solo al rollback: si
  `$ledgerHeadBefore.readable` es `$false`, **no invocar al agente**; registrar
  `RETRY_DEFER reason=ledger_unreadable_before_exec` y soltar el lock. Ante ambiguedad no se
  actua; y de paso no se genera residuo que luego haya que conservar.
- Si prefieres seguir ejecutando: que la linea base de `Get-OwnEvidence` sea un **centinela
  explicito** (no `0`) que fuerce `$false` cuando la cabeza no es legible. Un `seq` fabricado
  nunca puede pasar por una lectura.
- Negativo permanente nuevo, **por el bucle real**: cabeza ilegible antes del exec + evento
  firmado propio anterior + exec que sale 0 sin token -> el mensaje **no** queda en `seen.json`.
  El vector C8 (log valido, helper que falla) es el que hay que escribir, porque es el barato de
  reproducir y el que cubre las dos causas.

## Lo que si esta bien, y quiero que se lea con el mismo peso

Esto no es "otra ronda igual". El enfoque cambio de verdad y se nota en la forma del codigo:

- **Es una regla, no tres ramas.** El cuerpo entero del caso firmado es
  `if ($ledgerAdvanced) { probar disco; return }`: cero mutacion, sin lista de rutas, sin
  `kind`s, sin nombres de evento. Lo verifique leyendo la funcion completa y midiendo tres
  efectos firmados distintos (poda, decision, movimiento de mailbox) en un solo vector: los tres
  sobreviven **por la misma linea de codigo**. `event_managed_paths_after` ya **no tiene ningun
  llamador**, que es la confirmacion estructural de que la enumeracion se abandono.
- **Los tres bloqueantes de la iteracion 2 estan cerrados de verdad** (C1, C2, C4), y en C1 y C2
  el hijo es **estrictamente mejor** que el codigo hoy desplegado.
- **El `PRESERVED` es de disco.** `Get-WorktreeDiskProof` lee `git status --porcelain -z
  --untracked-files=all` y hace `Get-FileHash` SHA-256 fichero a fichero sobre el disco real,
  dos veces, y compara; ademas exige `Test-LedgerDerivedState` (drift replay) en verde. No es
  una comprobacion en memoria disfrazada. Lo que **prueba** es "el arbol no cambio bajo mis pies
  y no hay drift", no "los efectos que el evento nombra existen" -- lo declaro abajo como
  residual, con la semantica exacta, pero es una lectura fiel de la linea firmada.
- **El `trap { ...; return }` de `Restore-TransientExecResidue` corta la funcion de verdad.** Lo
  probe explicitamente en PowerShell 5.1 (error aritmetico y `throw` desde funcion anidada): en
  los dos casos la ejecucion **no** continua a las lineas siguientes. No hay camino por el que se
  registre `ROLLBACK_DEFER reason=rollback_probe_failed` y despues se ejecute el `reset --hard`.
- **La cota del residuo esta medida (C6).** El residuo staged que ahora se conserva bloquea al
  peer por `RETRY_DEFER reason=staged_residue_live` mientras la mtime sea reciente, y se libera
  al cumplirse `AbortedResidueMinutes` (5 por defecto): la precondicion de DECISION-0020 se rompe
  de forma **acotada por un temporizador**, no indefinida, y `RETRY_DEFER` no consume reintentos.
- **La clasificacion de outcome de 0278 no se movio**: `Get-ExecOutcomeClass` es byte a byte
  identica al padre (lo verifique con `diff` sobre la funcion extraida de ambos commits), y los
  cinco casos de parser del maker siguen en verde.
- **Pre-sucios ajenos intactos** (C5), gobernados y no gobernados, index y worktree.

## Residuales declarados

- **R-A (semantica de `PRESERVED`).** `ROLLBACK_LEDGER_PRESERVED ... proof=disk` significa "el
  arnes no muto nada, el arbol fue estable entre dos lecturas y no hay drift". **No** significa
  "los ficheros que los eventos firmados nombran existen": si el propio exec borro el documento
  de una `decision` que firmo, se emite `PRESERVED` igual. Bajo la regla conservadora es
  correcto (el destructor seria el agente, no el arnes), pero la linea del log promete mas de lo
  que verifica.
- **R-B (la declaracion del residuo no enumera).** La linea `PRESERVED` no nombra **que** quedo
  sucio, y vive solo en `.protocol-tmp/` (gitignorado, local). "Declarado y visible" se cumple
  de forma minima: para saber que se conservo hay que correr `git status` a mano. Es el residual
  R2 de la iteracion 1, que ahora pesa mas porque el residuo es el modo normal de operacion.
- **R-C (acumulacion sin techo).** Cada exec transitorio con avance de ledger deja su residuo y
  el siguiente lo hereda como pre-sucio. Cada ciclo esta acotado por `AbortedResidueMinutes`,
  pero la **suma** no tiene techo si la causa persiste. Es el coste que el Operador firmo; lo
  dejo declarado para que se sepa que la cota es por-ciclo, no total.
- **R-D (`event_managed_paths_after` es codigo muerto con un defecto conocido).** Ya no la llama
  nadie, pero sigue publicandose como maquinaria neutra y **sigue sin nombrar**
  `TASK_INDEX_ARCHIVE.json` ni `CLAIMS_ARCHIVE.json` (el bloqueante F-0280R2-01). Cualquier
  llamador futuro hereda el agujero cerrado hoy por otra via. Borrarla o arreglarla, pero no
  dejarla ahi con el defecto dentro.
- **R-E (parseo de renames en `Get-WorktreeDiskProof`).** Con `--porcelain=v1 -z` un rename emite
  la ruta original como **campo NUL separado**, no como `ruta -> ruta`; la rama `' -> '` es
  codigo muerto y el campo original se procesa como si fuera una entrada, quedando troceado por
  `Substring(3)`. Es inocuo hoy (el troceo es determinista, identico en las dos lecturas, asi que
  no produce DRIFT falso: lo medi en C3 con un rename staged real y salio `PRESERVED`), pero es
  una huella que no corresponde a ningun fichero.

Observacion de coordinacion, no hallazgo: `CLAIM-20260721-Codex-TASK-0280-iter3` sigue **activa**
con la tarea en `in_review`. AGENTS.md s7 pide que el owner libere su claim en el mismo paso de
coordinacion en que mueve la tarea a `in_review`. Lo senalo por DECISION-0018 y no lo toco.

## Recomendacion de cierre

**CHANGE-REQUIRED.** TASK-0280 no puede pasar a `done` con F-0280R3-01 abierto.

Sobre el redespliegue de los dos crons, que es tu decision y no la mia, te doy el cuadro
completo: el hijo es **estrictamente mejor que el padre desplegado** en todo lo que medi salvo
C7/C8, y ahi el padre no es "bueno", es ruidoso -- ladrilla el bucle y deja el mensaje sin
procesar. El hijo, en cambio, **consume el mensaje en silencio diciendo `confirmed`**. Si
redespliegas antes del arreglo, quiero que quede escrito que un unico fallo de lectura de la
cabeza del log basta para que el mensaje en vuelo desaparezca de la cola sin senal de error, y
que eso afecta a los dos peones vivos por igual, sin depender de ninguna capability. El arreglo
es de dos lineas y no toca la regla firmada, asi que mi consejo concreto es: arreglalo primero y
redespliega despues; el coste es una iteracion corta, no otra ronda de diseno.

Bucle de arreglo esperado:

1. F-0280R3-01: aplicar la regla conservadora tambien al exec (no invocar al agente con la
   cabeza ilegible) o centinela explicito para `Get-OwnEvidence`. Sin tocar nada mas.
2. Negativo permanente nuevo por el **bucle real** (vector C8: log valido, helper que falla ->
   `outcome` no `confirmed`, mensaje no marcado `seen`).
3. Gates a reejecutar en clon limpio: los seis de arriba.
4. Re-juicio independiente mio **antes** del commit de cierre.
5. Tope: esta es la remediacion **1 de 2** bajo el enfoque firmado. Si una segunda iteracion no
   lo cierra, escala al Operador con este veredicto como evidencia.

-- Analista
