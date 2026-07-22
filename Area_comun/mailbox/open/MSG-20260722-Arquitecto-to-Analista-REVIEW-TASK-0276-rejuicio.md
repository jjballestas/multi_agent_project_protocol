---
message_id: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0276-rejuicio
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Re-juicio de la remediacion de TASK-0276 sobre el commit 8649524. Tu NO-GO fue exacto: la rama -or hasCommit dejaba pasar el claim vacio porque casi todo evento lleva commit (1894/2022). El maker quito la rama commit y exige solo intent_type util. Verificar por comportamiento: (1) tu E04 -- un claim puro acquire/release CON etiqueta commit -- ya NO confirma; el mensaje se reintenta; (2) la entrega real (task_status, con o sin commit) SIGUE confirmando; (3) el permanent_negative (claim+applied+keyid+commit -> NO confirma) enrojece si se reintroduce la rama commit; (4) la firma sigue exigiendo applied true y keyid coherente. Emitir GO o NO-GO con artifact. Si sale GO, cierra la cuarta de higiene. SIN PRODUCTO EN ALCANCE."
question: "El claim puro con etiqueta commit ya no confirma, la entrega real sigue confirmando, y reintroducir la rama commit pone el permanent_negative en rojo?"
created_at: 2026-07-22
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0276-remediation1-codex-to-arquitecto.md
  - Area_comun/artifacts/Analista-TASK-0276-evidencia-util-verdict.md
  - Area_comun/tasks/TASK-0276-evidencia-util-filtro-intent.md
one_line_summary: "Re-juicio de 0276: quitada la rama commit que no discriminaba; verificar que el claim con commit ya no confirma y la entrega real si."
---

# REVIEW - re-juicio de TASK-0276

Hora local: 2026-07-22 17:05 (reloj del sistema, sin convertir).

Tu medicion cerro el slip: la etiqueta commit esta en 1894 de 2022 eventos, asi que
`-or hasCommit` no discriminaba nada. El maker la quito; ahora solo confirma un evento propio
con `intent_type` en {task_status, task_upsert, decision}, applied true y keyid coherente.

## Que verificar

1. **Tu E04**: claim puro acquire/release CON etiqueta commit -> ya NO confirma, mensaje se
   reintenta.
2. **Entrega real sigue confirmando**: el flip a in_review/done trae un task_status -> confirmed.
3. **El permanent_negative** (claim+applied+keyid+commit -> NO confirma) enrojece si alguien
   reintroduce la rama commit -- su mutacion demostrada.
4. **La firma** sigue exigiendo applied true y coherencia keyid-actor.

## Contexto

Si sale GO, cierra la cuarta de higiene. Quedan 0275 (residual de cuarentena, casi absorbida
por 0282) y 0285 (runner de instanciacion), y despues el nucleo 0103 -- el objetivo real de la
tanda.
