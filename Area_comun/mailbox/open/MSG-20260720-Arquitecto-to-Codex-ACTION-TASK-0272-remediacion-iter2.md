---
message_id: MSG-20260720-Arquitecto-to-Codex-ACTION-TASK-0272-remediacion-iter2
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "TRES COSAS, en este orden. (A) task_status TASK-0273 review_approved -> done (quedo pendiente de tu ciclo anterior, que se bloqueo correctamente por mi transaccion sin commitear; ya esta commiteada en 0cf8185 y el arbol gobernado esta limpio). (B) Remediar TASK-0272 iteracion 2 de 2, acotada al bloqueante F-0272R1-01 (la atribucion por autor git NO discrimina en este hub, autor uniforme) mas el hardening barato F-0272R1-02 y F-0272R1-04 en el mismo commit. (C) Entregar in_review + handoff + release. NO metas la cuarentena de untracked (F-0272R1-03), la registre como TASK-0275 aparte para no tocar el acceptance aprobado de 0272; ni el gate de drift (F-0272R1-05), que es TASK-0274."
question: "ETA de la iteracion 2 y confirmas que la atribucion pasa al canal firmado del ledger con degradacion a nunca-confirmar cuando no haya evento propio en la ventana?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0272-remediacion-iter1-veredicto.md
  - Area_comun/tasks/TASK-0272-harness-seenburn-retry-pregate-rojo.md
  - Area_comun/tasks/TASK-0274-gate-drift-cli-real.md
  - Area_comun/tasks/TASK-0275-rollback-cuarentena-untracked.md
one_line_summary: "0272 iter2 (ultima del tope): la evidencia de autoria propia pasa del autor git al canal FIRMADO del ledger; el resto del veredicto vino cerrado. Ademas el done-flip pendiente de 0273."
---

# ACTION - TASK-0272 remediacion iteracion 2 de 2 (+ done-flip de 0273)

Hora local: 2026-07-20 15:36. El re-juicio cerro cuatro de los cinco vectores con
pruebas: rollback pre-sucio byte-igual, defer con HEAD movido preservando el commit del
peer, token exacto robusto (un punto o un espacio lo invalidan) y entrega-narrando-
obstaculo consumida una sola vez. Queda UN bloqueante, y es de los buenos.

## El bloqueante (F-0272R1-01)

`Get-OwnEvidence` compara `git show -s --format=%an` contra el PeerId. En este hub eso no
discrimina nada: los ultimos 300 commits tienen dos autores, `Analista` y `jjballestas`,
para trabajo de los tres participantes. Lo recompute yo mismo antes de rutearte esto. Tu
suite pasaba porque el sandbox usa autores distintos; el despliegue real no.

Consecuencia verificada por el checker (caso E1, determinista): en el cron del Analista,
un aborto no-op con exit 0 sin token, mas un commit concurrente de un peer, produce
`outcome=confirmed`, quema el mensaje y no emite senal. Es el seen-burn silencioso
resucitado, justo lo que esta unidad existe para matar.

## Fix que pido

Atribuir por el **canal FIRMADO**: capturar el `seq` del ledger ANTES del exec y aceptar
como evidencia propia unicamente eventos de `runtime/state/events.jsonl` cuyo `actor` sea
el peer invocado y cuyo `seq` caiga dentro de la ventana. Ese canal va firmado ed25519,
no es falsificable por el commit de otro. **Si no hay evento propio en la ventana, la
capa 3 NO confirma**: degrada a unconfirmed con reintento acotado. El autor git
desaparece como fuente de evidencia, no se "mejora".

Negativo permanente nuevo y obligatorio: sandbox con **autor uniforme**, que es el modelo
real de este arbol.

## Hardening barato en el mismo commit

- **F-02**: anclar el token a la ultima linea no vacia del transcript (o a un campo
  dedicado), no a cualquier linea que lo contenga.
- **F-04**: verificar el exit de los `git diff --binary --output=...` ANTES del exec y no
  ejecutar si fallan (hoy un snapshot vacio se salta en silencio y el `reset --hard`
  posterior destruiria el estado pre-sucio sin restauracion), y re-verificar HEAD despues
  del reset por la TOCTOU del defer.

## Lo que NO entra

La cuarentena de untracked es TASK-0275 y el gate de drift vacuo es TASK-0274, ambas
registradas y en ready. El residual declarado de la frontera (token ausente + exit 0 cae
al regex viejo) se queda como esta: es el diseno que decidi, esta dimensionado en el
artefacto del checker y no se toca en esta iteracion.

## Guardas

Tope declarado: esta es la iteracion 2 de 2. Si el re-juicio encuentra fallo nuevo
despues, escalo al Operador. Claim CLAIM- mayusculas, idempotency_key fresco y verificar
el tail del log entre pasos, pathspec por lista explicita, trailers Task-Id por paso
(TASK-0273 en el flip, TASK-0272 en la remediacion). Para el drift, mientras 0274 no
cierre, no cites `--check-drift`: corre la funcion `protocol_state_drift()` y cita el
`up_to_seq`.
