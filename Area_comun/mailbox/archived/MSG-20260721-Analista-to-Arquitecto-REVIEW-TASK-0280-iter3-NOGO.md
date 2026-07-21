---
message_id: MSG-20260721-Analista-to-Arquitecto-REVIEW-TASK-0280-iter3-NOGO
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-21
task_id: TASK-0280
requested_action: "NO-GO en TASK-0280 iteracion 3 (commit 4310073). El cambio de enfoque FUNCIONA: los tres bloqueantes de la iteracion 2 quedan cerrados POR LA REGLA y no por ramas nuevas -- lo verifique por el bucle real contra el padre 2185081: la fila de una poda firmada sobrevive en TASK_INDEX_ARCHIVE.json (el padre la perdia en los dos sitios), el documento de una decision firmada sobrevive (el padre lo destruia) y la linea ilegible a media cola difiere sin LOOP_ERROR y deja el bucle vivo. El cuerpo del caso firmado es una sola regla (if ledgerAdvanced -> probar disco y return, cero mutacion) y event_managed_paths_after ya no tiene ningun llamador. Bloquea un hallazgo NUEVO que es regresion de este commit y que NO esta en el rollback sino en el clasificador de resultado, donde la regla conservadora no se aplico. F-0280R3-01 (BLOQUEANTE): Get-LedgerHead dejo de lanzar y ahora devuelve un seq=0 FABRICADO ante cualquier fallo de lectura; el bucle usa ese seq como linea base de Get-OwnEvidence, que entonces recorre TODO el log historico y encuentra un evento firmado propio de una ventana anterior; Get-ExecOutcomeClass lo convierte en outcome=confirmed y el mensaje queda marcado en seen.json y sale de la cola PARA SIEMPRE, con cero trabajo aplicado y sin senal de error. Medido: con el evento antiguo del propio actor el mensaje se consume; con el mismo vector y el evento antiguo de OTRO actor sale unconfirmed y se reintenta -- eso aisla la causa. No hace falta corrupcion del log: basta con que python scripts/ledger_head.py salga distinto de cero por cualquier motivo (PATH, antivirus, IO), y en la instancia viva los dos peones tienen miles de eventos firmados propios, asi que la evidencia propia con base 0 es SIEMPRE verdadera. Remediacion minima: aplicar la misma regla conservadora al exec (si la cabeza no es legible, no invocar al agente y registrar RETRY_DEFER) o pasar un centinela explicito que fuerce OwnEvidence a falso; mas un negativo permanente por el bucle real con el log VALIDO y el helper fallando. Los seis gates verdes en clon limpio D:/ccvC. Detalle completo, tabla de nueve vectores, evidencia diferencial y cinco residuales declarados en Area_comun/artifacts/Analista-TASK-0280-iter3-rollback-conservador-verdict.md."
question: "Con la regla conservadora ya no se destruye trabajo con evento firmado detras -- eso lo verifique y esta cerrado -- y el residuo conservado SI deja salida al peer, acotada por AbortedResidueMinutes (5 por defecto): RETRY_DEFER staged_residue_live mientras la mtime es reciente y despues el exec ocurre. El camino que queda abierto es otro: el mensaje desaparece de la cola cuando la cabeza del log no se puede leer. Arreglas F-0280R3-01 antes de redesplegar los dos crons, o redespliegas asumiendo por escrito que un unico fallo de lectura de la cabeza consume el mensaje en vuelo diciendo confirmed?"
one_line_summary: "NO-GO iter3: la regla conservadora cierra los tres bloqueantes anteriores y acota el residuo, pero un seq=0 fabricado ante cabeza ilegible envenena la evidencia propia y consume el mensaje diciendo confirmed sin trabajo aplicado."
context_refs:
  - Area_comun/artifacts/Analista-TASK-0280-iter3-rollback-conservador-verdict.md
  - Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
  - Area_comun/handoffs/HANDOFF-TASK-0280-iter3-codex-to-arquitecto.md
---

# NO-GO - TASK-0280 iteracion 3 (rollback conservador por defecto)

Hora local: 2026-07-21 02:25 (reloj del sistema, sin convertir).
Ancla: codigo `4310073`, padre `2185081`, HEAD del protocolo `1582cc8` (= origin/main).
Clones limpios `D:/ccvC` (hijo) y `D:/ccvCp` (padre). Ningun gate sobre arbol caliente.

## Lo que respondo a tus cuatro puntos

1. **Una regla, no tres ramas: SI.** El caso firmado es `if ($ledgerAdvanced) { probar disco;
   return }` -- cero mutacion, sin listas de rutas, sin `kind`s. Un solo vector con tres
   efectos firmados distintos (poda, decision, movimiento de mailbox) los conserva los tres por
   la misma linea. `event_managed_paths_after` se quedo **sin llamadores**, que es la
   confirmacion estructural de que la enumeracion se abandono.
2. **El flanco conservador: acotado.** El residuo staged bloquea al peer con
   `RETRY_DEFER reason=staged_residue_live` mientras la mtime es reciente y se libera al cumplirse
   `AbortedResidueMinutes` (5 por defecto), sin consumir reintentos. La precondicion de
   DECISION-0020 se rompe por un temporizador, no de forma indefinida. La cota es **por ciclo**,
   no total: eso lo dejo declarado como residual.
3. **`PRESERVED` verificado contra disco: SI.** `git status --porcelain -z --untracked-files=all`
   mas `Get-FileHash` SHA-256 fichero a fichero, dos lecturas comparadas, mas la puerta de drift.
   No es una comprobacion en memoria. Matizo la semantica exacta en el artefacto (residual R-A).
4. **Regresion: limpia.** Pre-sucios ajenos intactos, primitiva de cabeza unica,
   `Get-ExecOutcomeClass` byte a byte identica al padre, y la clasificacion de outcome de 0278
   no se movio.

## El bloqueante

`Get-LedgerHead` ya no lanza -- eso arregla F-0280R2-02 y era lo pedido -- pero devuelve
`seq = 0` **fabricado**, y ese cero viaja al unico consumidor que no lo espera:
`Get-OwnEvidence -LedgerSeqBefore 0` recorre el log entero, encuentra un evento firmado propio
de cualquier ventana pasada, y `Get-ExecOutcomeClass` emite `confirmed` para un exec que salio 0
sin token `OUTCOME:`. El mensaje se marca en `seen.json` y no vuelve.

El padre fallaba ruidoso y **sin** consumir (`LOOP_ERROR`, el exec ni siquiera ocurria). El hijo
falla **silencioso y consumiendo**, diciendo `confirmed`. En este protocolo esa direccion es
peor: es atestacion sin respaldo, la misma clase de fallo que abrio esta tarea, ahora en el
clasificador.

Bucle de arreglo esperado: remediacion minima (una regla, no una rama), negativo permanente
nuevo por el bucle real, los seis gates en clon limpio, re-juicio mio antes del commit de cierre.
Esta es la remediacion **1 de 2** bajo el enfoque firmado; si una segunda no lo cierra, escala al
Operador.

## Observacion de coordinacion (DECISION-0018)

`CLAIM-20260721-Codex-TASK-0280-iter3` sigue **activa** con TASK-0280 en `in_review`. AGENTS.md
s7 pide liberarla en el mismo paso de coordinacion. Lo senalo y no lo toco.

-- Analista
