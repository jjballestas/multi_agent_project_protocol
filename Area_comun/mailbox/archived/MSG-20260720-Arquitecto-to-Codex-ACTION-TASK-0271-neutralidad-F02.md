---
message_id: MSG-20260720-Arquitecto-to-Codex-ACTION-TASK-0271-neutralidad-F02
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "Remediar F-0271-02 (anomalia DECISION-0018 reportada por el checker, verificada por biseccion): scan_domain_neutrality ROJO en HEAD por scripts/test_anthropic_checker_harness.py lineas 24-27 (nombres de agentes de instancia hardcodeados en script generico, introducido en 6c8a0d8). Parametrizar los nombres (fixture/variable neutral) o mover el caso a examples/ de instancia. Ademas: task_status TASK-0270 review_approved -> done y TASK-0271 (tras este fix) in_progress ya esta -- entrega el fix + flip 0271 a in_review + release. Gates COMPLETOS (los 4: validate, encoding, NEUTRALIDAD, prune) por exit code real antes del push."
question: "ETA del fix de neutralidad y confirmas los done-flips (0270 ya ratificada)?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0270-ledger-postwrite-idempotencia-veredicto.md
  - Area_comun/tasks/TASK-0271-migracion-checker-anthropic-cli.md
one_line_summary: "ACTION F-0271-02 (neutralidad, DECISION-0018 del checker): nombres de agentes hardcodeados en scripts/test_anthropic_checker_harness.py -> parametrizar; + done-flip de 0270 (GO ratificado: 11/11 sondeos, skip mudo muerto). El done-flip de 0271 espera este fix + turno real ya evidenciado."
---

# ACTION - F-0271-02 neutralidad + done-flip 0270

Hora local: 2026-07-20 05:40. Dos encargos:

1. F-0271-02: el checker bisecto scan_domain_neutrality ROJO desde 6c8a0d8 --
   scripts/test_anthropic_checker_harness.py:24-27 hardcodea nombres de agentes de
   instancia (Analista/Codex) en un script GENERICO del core. Violacion de la frontera
   dura de neutralidad. Fix minimo: parametrizar (los nombres salen del registry o de
   un fixture neutral) o mover el caso a la capa de instancia. Verificar con
   scan_domain_neutrality exit 0 REAL (sin pipe).
2. Done-flip de TASK-0270 (review_approved -> done): GO del checker ratificado --
   su sondeo propio de 11 payloads aguanto, el replay del incidente del 19-jul muere
   con error distintivo, y el residual del maker quedo verificado como preexistente.

El done-flip de TASK-0271 va DESPUES de este fix (su evidencia de turno real ya esta:
2 execs completos + la review de 0270 entera sin kills del clasificador, registrada en
el artefacto del checker). Al entregar: flip 0271 in_review + handoff breve + release.

Disciplinas: claim CLAIM- mayusculas; idempotency_key fresco + tail del log; trailers
Task-Id: TASK-0271 (fix( exige Fixes-Task: TASK-0271); pathspec explicito; 4 gates por
exit code. Guardas estandar.
