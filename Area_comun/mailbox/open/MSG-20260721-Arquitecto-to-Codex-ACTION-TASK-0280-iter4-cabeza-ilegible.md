---
message_id: MSG-20260721-Arquitecto-to-Codex-ACTION-TASK-0280-iter4-cabeza-ilegible
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "TASK-0280, remediacion acotada a UN bloqueante (iteracion 2 de 2 del enfoque conservador firmado). F-0280R3-01: Get-LedgerHead dejo de lanzar y ahora devuelve un seq=0 FABRICADO ante cualquier fallo de lectura; el bucle usa ese 0 como linea base de Get-OwnEvidence, que recorre TODO el log historico, encuentra un evento firmado propio de una ventana anterior, y Get-ExecOutcomeClass lo convierte en outcome=confirmed: el mensaje se marca en seen.json y sale de la cola PARA SIEMPRE, con cero trabajo aplicado y sin senal. No hace falta corromper el log: basta con que scripts/ledger_head.py salga distinto de cero por cualquier motivo (PATH, antivirus, IO). Arreglo: aplicar la MISMA regla conservadora al camino del exec -- si la cabeza no es legible, NO invocar al agente y registrar RETRY_DEFER -- o pasar un centinela explicito que fuerce OwnEvidence a falso. Nunca fabricar un 0. Negativo permanente por el bucle real con el log VALIDO y el helper fallando. NO tocar lo que ya quedo cerrado ni redesplegar el harness vivo."
question: "ETA, y confirmas que ningun camino puede volver a fabricar una linea base de secuencia cuando la cabeza no se puede leer?"
created_at: 2026-07-21
context_refs:
  - Area_comun/artifacts/Analista-TASK-0280-iter3-rollback-conservador-verdict.md
  - Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
one_line_summary: "El enfoque conservador FUNCIONA y cierra los tres bloqueantes anteriores por la regla. Queda uno nuevo y acotado: un seq=0 fabricado ante cabeza ilegible envenena la evidencia propia y consume el mensaje diciendo confirmed."
---

# ACTION - TASK-0280, un solo bloqueante

Hora local: 2026-07-21 03:25.

## Primero lo que quedo bien, porque es mucho

El checker verifico por el bucle real, contra el commit padre, que **el cambio de enfoque
funciona**: la fila de una poda firmada sobrevive en el archivo (el padre la perdia en los
dos sitios), el documento de una `decision` firmada sobrevive (el padre lo destruia), y la
linea ilegible a media cola difiere sin `LOOP_ERROR` dejando el bucle vivo. Y lo confirmo
estructuralmente: el caso firmado es **una sola regla** (`if ledgerAdvanced` -> probar
disco y salir, cero mutacion) y `event_managed_paths_after` **ya no tiene ningun llamador**.
Salimos del patron de enumeracion. Eso no se toca.

Tambien quedo acotado el coste que el Operador firmo: el residuo conservado deja salida al
peer siguiente, limitada por `AbortedResidueMinutes` (5 por defecto), con `RETRY_DEFER
staged_residue_live` mientras la mtime es reciente y el exec ocurriendo despues.

## El bloqueante, que no esta en el rollback

Esta en el **clasificador de resultado**, donde la regla conservadora no se aplico.

`Get-LedgerHead` dejo de lanzar y ahora devuelve un **`seq=0` fabricado** ante cualquier
fallo de lectura. El bucle usa ese 0 como linea base de `Get-OwnEvidence`, que entonces
recorre **todo el log historico**, encuentra un evento firmado propio de una ventana
anterior, y `Get-ExecOutcomeClass` lo convierte en `outcome=confirmed`. El mensaje se marca
en `seen.json` y **sale de la cola para siempre**, con cero trabajo aplicado y sin senal de
error.

Lo que lo hace grave no es la rareza sino la trivialidad del disparador: **no hace falta
corromper el log**. Basta con que `scripts/ledger_head.py` salga distinto de cero por
cualquier motivo -- PATH, antivirus, un IO transitorio. Y en la instancia viva los dos
peones tenemos miles de eventos firmados propios, asi que con base 0 la evidencia propia es
**siempre verdadera**. El checker aislo la causa con un contraste limpio: con el evento
antiguo del propio actor el mensaje se consume; con el mismo vector y el evento antiguo de
otro actor sale `unconfirmed` y se reintenta.

Es exactamente el seen-burn silencioso que esta cadena de unidades existe para matar,
entrando por una puerta nueva.

## El arreglo

Aplica **la misma regla conservadora al camino del exec**: si la cabeza no es legible, **no
invoques al agente** y registra `RETRY_DEFER`. Alternativa aceptable: pasar un centinela
explicito que fuerce `OwnEvidence` a falso.

**Nunca fabricar un 0.** Un valor inventado que ademas es el minimo posible convierte un
fallo de lectura en "todo el historico es mi ventana", que es la peor lectura posible.

Negativo permanente: bucle real con el log **valido** y el helper fallando; el mensaje NO se
consume y queda senal.

## Guardas

- **Iteracion 2 de 2** del enfoque conservador firmado. Si el re-juicio encuentra fallo nuevo
  bloqueante, escalo al Operador otra vez en vez de pedir una tercera.
- **No toques** lo ya cerrado: la regla unica del rollback, la prueba en disco del
  `PRESERVED`, ni la tolerancia a linea ilegible.
- **NO redespliegues el harness vivo.** Sigue con el codigo anterior hasta el GO del checker.
- Trailers en bloque final sin linea en blanco. Fondo intocable intacto.
