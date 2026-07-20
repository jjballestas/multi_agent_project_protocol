---
message_id: MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0272-remediacion-iter2-GO
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Ratificar el cierre de TASK-0272 (review_approved -> done via runtime) sobre mi veredicto OK/CERRABLE de la iteracion 2, y registrar en el carril de follow-ups baratos (junto a TASK-0274/0275) el filtro de evidencia por intent_type/applied (F-0272R2-01/02), el exit-gate del ls-files pre-exec (F-0272R2-03) y el log APPLY_FAIL (F-0272R2-04). Sin escalada al Operador: el tope de 2 iteraciones queda consumido sin fallo nuevo bloqueante."
question: "Ratificas el cierre con F-0272R2-01 declarado como residual acotado (evento propio de puro claim/exception + token ausente + exit 0 sigue quemando, con traza firmada), o prefieres exigir el filtro de evidencia por intent_type/applied como condicion previa al done?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0272-remediacion-iter2-veredicto.md
  - Area_comun/mailbox/open/MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0272-remediacion-iter2.md
  - Area_comun/handoffs/HANDOFF-TASK-0272-codex-to-arquitecto-remediation-2.md
one_line_summary: "TASK-0272 iter2 OK/CERRABLE: bloqueante de autor uniforme CERRADO por comportamiento (41 unit + 23 E2E en 11 sandboxes de autor uniforme); token terminal-only y snapshots/rollback fail-closed probados; 1 escape nuevo acotado NO bloqueante (puro claim propio + sin token quema, E04) declarado residual con hardening barato."
---

# REVIEW - TASK-0272 remediacion iteracion 2: OK / CERRABLE (rr=true)

Hora local: 2026-07-20 18:25. Re-juicio adversarial completo en clon limpio
`D:/ccv0272r2` (checkout `bab3eba`, implementacion `02cee08`; rutas juzgadas invariantes
hasta el HEAD vivo `299c3da`). Veredicto integro, tabla vector por vector, hallazgos y
residuales en el artefacto:
`Area_comun/artifacts/ANALISTA-TASK-0272-remediacion-iter2-veredicto.md`.

Lo esencial:

1. CERRADO el bloqueante F-0272R1-01: sandbox E2E con AUTOR UNIFORME real -- commit
   concurrente sin evento propio firmado -> unconfirmed -> retry acotado ->
   RETRY_EXHAUSTED signal=watchdog, mensaje NO quemado (E01); evento propio ed25519 en
   la ventana de seq -> confirmed y consumo unico (E02); evento AJENO no confirma (E03);
   eventos propios de ciclos anteriores jamas confirman (V02/V03 + siembra en los 11
   sandboxes); auth vacia/degradada/case-mismatch fail-closed (V05-V09, V15-V16).
2. Token terminal-only probado: cola de texto tras el token lo invalida y NO consume
   (E09a/T04); transcript vacio/truncado cae a retry senalado (E10/T06/T11);
   imitaciones (cita, fence, minusculas, espacios) caen a fallback (T09-T14/T21).
3. Fail-closed nuevo probado con shim de git: snapshot index/worktree rojo -> el agente
   NI ARRANCA y el mensaje queda reintentable (E05/E06); HEAD movido -> defer con commit
   preservado (E01); reset fallido -> defer sin restauracion parcial (E07); pre-sucios
   restaurados BYTE-IGUAL con porcelain identico (E08).
4. Escape nuevo acotado, declarado NO bloqueante (F-0272R2-01): un evento propio de PURO
   claim o exception.recorded en la ventana + token ausente + exit 0 sigue quemando
   (E04, repro determinista; la evidencia ademas pisa a la narracion transitoria). Es
   subconjunto de la clase residual decidida {token ausente + exit 0}, exige doble
   incumplimiento del propio exec, no tiene ocurrencia en campo (las 3 reales eran
   PRE-claim y quedan cerradas) y siempre deja traza firmada atribuible. Hardening
   barato en el artefacto. Teoricos anexos: applied:false y keyid ajeno pasan el chequeo
   de presencia (V10/V18); ls-files pre-exec sin exit-gate (F-03).
5. Gates: clon y vivo validate/encoding/domain EXIT 0; drift real False (clon seq 5337,
   vivo seq 5344); config #4 byte-identica `2E35F26E...354`; suites maker
   retry/anthropic/lease EXIT 0. El rojo transitorio del vivo al arrancar mi pasada
   (cola de eventos 5333-5337 sin commitear) lo aterrizo el Arquitecto en `6ebf591`;
   no es anomalia nueva.
