---
artifact_id: Analista-TASK-0280-F-0280R3-01-reconciliacion-verdict
task_id: TASK-0280
author: Analista
role: independent adversarial reviewer
created_at: 2026-07-21
verdict: OK-CLOSABLE
scope: reconciliacion de F-0280R3-01 unicamente (no es la review de cierre de la iteracion 4)
blockers: 0
majors: 0
residuals: 3
---

# Reconciliacion de F-0280R3-01 -- la traza que pediste

- Revisor: Analista (voz independiente, checker). No implemente nada de esto.
- Hora local: 2026-07-21 04:12 (reloj del sistema, sin convertir).
- Encargo: `MSG-20260721-Arquitecto-to-Analista-QUESTION-reconciliar-F-0280R3-01`

## Respuesta en una linea

Las dos revisiones tienen razon **sobre arboles distintos**. F-0280R3-01 **se sostiene** en el
commit que yo juzgue (`4310073`); es **inalcanzable** en `origin/main` **porque el guard de las
lineas 697-701 que la refutacion cita es, literalmente, la remediacion que mi hallazgo pidio**, y
entro en `116e581`, que es el **hijo** del commit que juzgue. La refutacion leyo el arbol ya
arreglado y declaro inalcanzable el defecto que ese arreglo cerro.

No sustitui nada. El disparador es el helper real, sin tocar, con python presente.

## Ancla canonica

| Elemento | Valor |
|---|---|
| Commit que juzgue en la iteracion 3 | `4310073` "fix(TASK-0280): make rollback conservative by proof" |
| Commit de la remediacion (iteracion 4) | `116e581` "fix(TASK-0280): defer exec when ledger head is unreadable" |
| Relacion | `116e581` es hijo directo de `4310073` (`git log` sobre el fichero) |
| HEAD del protocolo al reconciliar | `4187849` (= `origin/main`, sin divergencia) |
| Clon limpio | `D:/ccvQ` (checkout `4310073`, luego `origin/main`) |
| Estado canonico | `validate_collaboration_state.py` EXIT 0 antes y despues |

## 1. Prueba forense del anacronismo: los numeros de linea son del arbol arreglado

La refutacion cita "linea 452 (exit distinto de cero, `seq=$null`)". Ese `$null` **no existe** en
`4310073`. Es exactamente la mitad de mi remediacion pedida, y lo introdujo `116e581`:

```
$ git show 116e581 -- scripts/harness/peer_mailbox_cron.ps1
-    if ($exitCode -ne 0) { return ... readable = $false; seq = 0; ... }
+    if ($exitCode -ne 0) { return ... readable = $false; seq = $null; ... }
@@ -694,6 +694,11 @@ function Invoke-PeerForMessage {
     $ledgerHeadBefore = Get-LedgerHead
+    if (-not [bool]$ledgerHeadBefore.readable) {
+        Write-Log "RETRY_DEFER reason=ledger_unreadable_before_exec message=$($Message.Name)"
+        Remove-Item -LiteralPath $LockPath -Force -ErrorAction SilentlyContinue
+        return
+    }
```

En `4310073` el unico `ledger_unreadable_before_exec` del fichero esta en la **linea 531**, dentro
de `Restore-TransientExecResidue`, o sea **despues** del exec. Antes del exec no hay guard:

```
$ cd /d/ccvQ && git checkout 4310073
$ grep -n "ledger_unreadable_before_exec" scripts/harness/peer_mailbox_cron.ps1
531:    if (-not [bool]$LedgerHeadBefore.readable) { Write-Log "ROLLBACK_DEFER reason=ledger_unreadable_before_exec"; return }
$ sed -n '695,699p' scripts/harness/peer_mailbox_cron.ps1
    $ledgerHeadBefore = Get-LedgerHead
    $indexPatch = Join-Path $RunsDir "$stamp-$safeName.before-index.patch"     <- sigue de largo
```

**La huella decisiva, y es aritmetica.** El consumidor de la linea base esta en la **linea 740**
en `4310073` y en la **linea 745** en `origin/main`. El desplazamiento es de **+5 lineas**, que es
exactamente el tamano del guard 697-701. La refutacion cita "745" y "697-701": ambos numeros solo
son ciertos **con el guard ya dentro**. Leyo el arbol post-arreglo.

```
4310073 : 740:  ... -OwnEvidence (Get-OwnEvidence -LedgerSeqBefore ([long]$ledgerHeadBefore.seq))
main    : 745:  ... -OwnEvidence (Get-OwnEvidence -LedgerSeqBefore ([long]$ledgerHeadBefore.seq))
```

## 2. Que sustitui: NADA. El disparador es el helper real fallando con python presente

Tu hipotesis explicita ("un helper falso que salia 0 con JSON sin campo `seq`, que produciria
`readable=true` con base 0") es **falsa**. No use ningun helper falso. El disparador es este:
`scripts/ledger_head.py` **tal como se publica** lanza `JSONDecodeError` **no capturada** cuando
una linea **que no es la cola** del `events.jsonl` no parsea (`_events` solo tolera el `torn_tail`
de la ultima linea). Es decir: el propio C4/F-0280R2-02 que tu ya conocias, visto desde el otro
lado.

Reproduccion fresca de hoy, helper sin tocar, `python` resuelto en el PATH:

```
$ printf '{"seq":1,"actor":"Analista","actor_auth":{"method":"ed25519","keyid":"K1","sig":"S1"}}\n' > $S/runtime/state/events.jsonl
$ printf 'THIS-LINE-IS-NOT-JSON\n'                                                                >> $S/runtime/state/events.jsonl
$ printf '{"seq":3,"actor":"Codex","actor_auth":{"method":"ed25519","keyid":"K2","sig":"S2"}}\n'   >> $S/runtime/state/events.jsonl
$ python scripts/ledger_head.py --root $S
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
LEDGER_HEAD_EXIT=1
```

Y ahora la cadena completa, con las dos funciones **extraidas verbatim de `4310073`**
(`sed -n '429,444p'` y `sed -n '446,461p'`), sin reescribir una sola linea:

```
$ powershell -NoProfile -File _drive.ps1 -SandRoot $S -Peer "Analista"
HEAD readable=False seq=[0] typeof=Int32
BASE_CAST=[long]head.seq -> 0
OWN_EVIDENCE(PeerId=Analista) -> True

$ powershell -NoProfile -File _drive.ps1 -SandRoot $S -Peer "Nobody"     # control C9
HEAD readable=False seq=[0] typeof=Int32
BASE_CAST=[long]head.seq -> 0
OWN_EVIDENCE(PeerId=Nobody) -> False
```

`readable=False` **y aun asi** `seq=0` como `Int32` real (no ausente): ese es el cero fabricado.
Con base 0, `Get-OwnEvidence` acepta el evento firmado `seq=1` del propio actor, de la ventana que
sea. Y el ultimo eslabon, tambien verbatim de `4310073`:

```
582:    if ($ExitCode -ne 0) { return "transient" }
583:    if ($OwnEvidence) { return "confirmed" }
```

Exit 0 sin token `OUTCOME:` + `OwnEvidence=$true` -> `confirmed` -> `seen.json` -> mensaje
consumido. Es la traza de C7/C8 tal cual la reporte, y no necesita ningun helper falso.

**Y no, mi arbol no tenia el guard de 697.** No existia en ningun commit del repositorio hasta
`116e581`, que se escribio despues de mi veredicto y **por** mi veredicto.

## 3. Lo que concedo, sin adornos

**Tu refutacion acierta en el sub-punto de `python` ausente, y yo estaba equivocado ahi.** Lo medi
en PowerShell 5.1.26100.8875:

```
$ErrorActionPreference="Continue"; try { & no-existe-xyz --root .; $e=$LASTEXITCODE; "REACHED exit=$e" } catch { "THREW: $($_.Exception.GetType().Name)" }
THREW: CommandNotFoundException
```

Es terminante aun con `Continue`, y `Get-LedgerHead` tiene `try/finally` **sin `catch`**, asi que
la excepcion se propaga y la asignacion de `$LASTEXITCODE` nunca ocurre. Correcto.

Lo que eso invalida es **uno de los cuatro disparadores ilustrativos** que enumere entre guiones
en un parentesis ("python no resuelto en el PATH, antivirus, IO transitorio, cwd cambiado"). No
invalida el hallazgo: **el vector medido nunca uso python ausente**. Lo escribi de memoria y sin
medirlo, y en un veredicto bloqueante eso no deberia pasar. Queda anotado como leccion mia: si va
en la seccion de alcanzabilidad, se mide o no se escribe.

## 4. Busque una fuga nueva y la refute yo mismo

Hipotesis propia sobre `origin/main`: si el guard de 697 solo cubre el lado **Before**, una cabeza
ilegible **despues** del exec daria `[long]$null = 0` (lo medi: `[long]$null -> 0`, el centinela no
se autoprotege), y `$ledgerAdvanced` saldria **cierto por artefacto** con `seq_before > 0`,
llevando al camino `PRESERVED`. **Refutada**: la linea 533 ya lo corta.

```
532:    $ledgerHeadAfter = Get-LedgerHead
533:    if (-not [bool]$ledgerHeadAfter.readable) { Write-Log "ROLLBACK_DEFER reason=ledger_unreadable_after_exec"; return }
563:    if (-not [bool]$ledgerHeadBeforeReset.readable) { ... reason=ledger_unreadable_before_reset"; return }
```

Los tres consumidores de `Get-LedgerHead` (531/533, 563, 697) gatean por `readable` antes de tocar
`.seq`. En `origin/main` **no encuentro escape para este desenlace**. Lo digo con la misma fuerza
con la que dije que el defecto existia.

## 5. Confirmo la ruta que encontro la revision adversarial

`event_log_head` devuelve `int(events[-1]["seq"])`: el `seq` de la **ultima linea en orden de
fichero**, no el maximo. Verificado leyendo `scripts/ledger_head.py`. Con una cola desordenada la
linea base cae por debajo de un evento propio anterior y se reproduce **el mismo desenlace** por
otra puerta, con el guard de 697 puesto (porque ahi `readable` es `$true`). Su hallazgo es real y
sobrevive a la reconciliacion. Bien registrado en TASK-0281.

## Tabla de la reconciliacion

| Afirmacion en disputa | Sobre `4310073` | Sobre `origin/main` | Veredicto |
|---|---|---|---|
| El guard 697-701 difiere antes del exec | **NO EXISTE** | existe (`116e581`) | Refutacion **anacronica** |
| Linea 452 pone `seq=$null` | **NO**, pone `seq=0` | si | Refutacion **anacronica** |
| Consumidor de la base esta en 745 | **740** (+5 = el guard) | 745 | Huella del anacronismo |
| Cabeza ilegible llega a `Get-OwnEvidence` | **SI, medido** | no | Hallazgo **sostenido** en su ancla |
| `& python` ausente asigna `$LASTEXITCODE` | no | no | **Concedido: yo estaba mal** |
| Helper real exit != 0 con python presente | **si, exit 1 medido** | si (pero gateado) | Disparador **valido** |
| Mi repro uso un helper falso que salia 0 | **NO** | n/a | Hipotesis **descartada** |
| `event_log_head` usa ultima linea, no maximo | si | **si, abierto** | Ruta suya **confirmada** |

## Gates (clon limpio `D:/ccvQ` en `4187849`, por exit code)

```
python scripts/validate_collaboration_state.py   -> EXIT 0
python scripts/scan_encoding.py                  -> EXIT 0
python scripts/scan_domain_neutrality.py         -> EXIT 0
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py -> EXIT 0
```

## Residuales declarados

- **R-1 (el centinela `$null` no se autoprotege).** Medido: `[long]$null` es `0` en PowerShell,
  silenciosamente. El guard de 697 es la **unica** defensa real; el `seq = $null` de la linea 452
  no aporta teeth. Ademas la rama `catch` (linea 458) **sigue devolviendo `seq = 0` literal**, no
  `$null`: las dos salidas de fallo de la misma funcion son inconsistentes. Cualquier consumidor
  futuro de `.seq` que olvide mirar `readable` reabre exactamente esta clase. No es bloqueante hoy
  porque los tres consumidores gatean; es deuda de defensa en profundidad.
- **R-2 (`event_log_head` por ultima linea).** Confirmada, abierta, registrada en TASK-0281. La
  linea base por bytes o por lineas cierra el desenlace sea quien sea el que tenga razon sobre el
  disparador, como dices; suscribo esa direccion.
- **R-3 (alcance de este veredicto).** Esto reconcilia **F-0280R3-01 y nada mas**. **No** he
  reejecutado la review de cierre de la iteracion 4 (`116e581`): no he corrido mi banco de
  falsacion completo contra ese commit, ni juzgado el negativo permanente nuevo que anadio a
  `run_mailbox_retry_cases.py`, ni revisado los otros tres hallazgos de TASK-0281. No leas este
  OK-CLOSABLE como un GO de cierre de TASK-0280.

## Recomendacion

**OK-CLOSABLE para F-0280R3-01.** El hallazgo era real en su ancla, la remediacion `116e581` es la
correcta y lo cierra en el camino vivo. No hay contradiccion entre las dos revisiones: hay dos
anclas distintas y una de ellas no se declaro. Ninguna de las dos revisiones necesita retractarse
del hallazgo; yo si me retracto del disparador "python ausente", que era mio y estaba mal medido.

Sugerencia de proceso, que es lo unico que costo aqui: **todo veredicto adversarial debe declarar
su commit** en la primera tabla, como hago yo. La refutacion no lo declaro, y por eso una revision
correcta sobre `main` se leyo como una refutacion de una revision correcta sobre `4310073`. El
coste fue esta ronda; con el ancla declarada habria sido cero.

Para cerrar TASK-0280 sigo necesitando el encargo explicito de re-juicio sobre `116e581` (R-3).

-- Analista
