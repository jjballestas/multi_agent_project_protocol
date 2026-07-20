---
message_id: MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0272-remediacion-iter1-NOGO
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Rutear a Codex la remediacion iteracion 2 (ultima del tope) acotada a F-0272R1-01: sustituir la atribucion por autor git de Get-OwnEvidence (el hub tiene autor UNIFORME 'Analista' en los 300 commits recientes; un commit ajeno durante un exec del cron Analista + token ausente = confirmed falso + seen quemado sin senal, repro E2E determinista E1) por el canal firmado del ledger o degradar capa 3 a nunca-confirmar; anadir negativo de suite con autor uniforme. Recomendado mismo commit: anclar token a ultima linea (F-02) y verificar exit de snapshots + log de rutas del rollback (F-04). Re-juicio Analista con E1/E2/E3 + bateria unit antes del cierre."
question: "Ratificas que la cuarentena de untracked del rollback (F-0272R1-03, escrituras de peer durante la ventana del exec hoy se BORRAN sin log) se difiere como residual explicito de la unidad, o la incluyo como exigencia de la iteracion 2?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0272-remediacion-iter1-veredicto.md
  - Area_comun/handoffs/HANDOFF-TASK-0272-codex-to-arquitecto-remediation-1.md
  - Area_comun/tasks/TASK-0272-harness-seenburn-retry-pregate-rojo.md
one_line_summary: "Re-juicio 0272 iter1: CAMBIO-REQUERIDO acotado -- vectores 1/3/4/5 cerrados (rollback byte-igual, defer correcto, token robusto), pero la evidencia por autor git no discrimina en este hub (autor uniforme) y resucita el burn en el cron Analista (E1); fix = atribucion por ledger firmado + negativo de autor uniforme."
---

# REVIEW - TASK-0272 remediacion iter1: NO-GO acotado (rr=true)

Veredicto completo con tabla vector-por-vector, 21 casos unit + 10 sandboxes E2E,
hallazgos F-0272R1-01..05 y residuales en el artefacto de context_refs. Lo esencial:

- CERRADO y probado: rollback pre-sucio byte-igual (worktree+staged+renames), defer con
  HEAD movido preservando el commit del peer, token exacto robusto (punto/espacio/case lo
  invalidan, ultima-linea gana en enumeraciones), entrega-narrando-obstaculo consumida 1x,
  keyword fallback intacto, tope 3 + RETRY_EXHAUSTED + exclusion.
- BLOQUEANTE (unico): Get-OwnEvidence usa %an y el arbol commitea TODO como 'Analista';
  E1 reproduce el seen-burn silencioso en el cron Analista con un commit concurrente y
  token ausente. La suite del maker pasa porque su sandbox usa autores distintos.
- Residual estructural declarado: la clase {token ausente + exit 0} cae al regex viejo
  (X1 eco NO-GO quema; X2 narracion fuerza retry acotado). Es el diseno decidido de la
  frontera; dimensionado en el artefacto.
- Higiene: el gate documentado runtime/protocol_replay.py --check-drift es VACUO (sin
  entrypoint CLI; exit 0 con --bogus-flag). Drift real verificado por funcion: False
  (clon 5302, vivo 5317). Corregir el comando en handoffs/README o anadir CLI.

Fix-loop declarado: iteracion 2 de 2; un fallo nuevo posterior escala al Operador.
