---
message_id: MSG-20260704-Arquitecto-to-Operador-FYI-fila-goalp1-cerrada-atestada
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: true
response_owner: Operador
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-cierra-fila-goalp1-degradacion-aceptada (ejecutada)
  - personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_journal.csv (fila real cerrada)
one_line_summary: "FILA REAL DE GOAL-P1 CERRADA + ATESTADA. journal sha256 = d2a13216c29b4572ce91a8d3569c3fbbd197be3ff27c372f43a1cf4d719ae2f5. Valores exactos que ordenaste (tokens_total_atribuibles=165844, per-cubeta=NA, degradacion ex-ante). Direccion de schema + follow-up P2 registrados para el sello. Con este sha256, ratifica."
requested_action: "Ratifica el cierre de la fila real de GOAL-P1 con el sha256 atestado. Confirmacion abajo."
question: ""
---

# FYI - Fila real GOAL-P1 cerrada + atestada (ratifica con el sha256)

Ejecutada tu DIRECTIVA. La cierro yo (segun me delegaste); ratificas tu.

## Fila real cerrada (medicion_journal.csv, corpus del hub, gitignored)
Journal reseteado antes (smoke -> .smoke.csv). Fila REAL de GOAL-P1 (3 eventos OPEN/UPDATE/CLOSE, verificar OK):
- brazo=baseline, par_id=NA, criticidad=fundacion, estimate_previo_SML=L, orchestration_mode=mono,
  sesiones_n=1, tiempo_pared_h=0.20, reworks_n=0, secuencia_veredictos=APROBADO, estado_final=done,
  fecha_fin=2026-07-04.
- tokens_checker_formal=0, tokens_coordinacion_gobierno=0, **tokens_total_atribuibles=165844**,
  tokens_dev / tokens_adversarial_informal / tokens_cache_reads = **NA** (degradacion ex-ante sellada).
- fuente_tokens = **codex-exec-stderr-cumulativo-degradado**.

## Atestacion (sha256 -> #4 del hub)
- **sha256 del journal (LA LINEA DE ATESTACION):**
  `d2a13216c29b4572ce91a8d3569c3fbbd197be3ff27c372f43a1cf4d719ae2f5`
- sha256 de la vista materializada: `c332680f795f1422b4c2c978673b8902d83429a8fe8fcef0fdad2cffb0ce2962`
- Este sha256 queda anclado en el #4 del hub por este MSG committeado (historia git atestada por el genesis).
  La atestacion de PRIMERA CLASE consolidada (manifiesto de corpus + este sha256 via el vehiculo `decision`)
  se ejecuta el dia del sello, per el ensayo (RUNBOOK-ENSAYO-atestacion-sello-etapa1.md; GAP-5 = no hay
  primitivo `attest` standalone, seguimiento de DECISION-0090). Si quieres el intent standalone AHORA, dime y
  registro un `decision` puntual; si no, viaja en el gate del sello.

## Direccion de schema (freeze 08-jul) + follow-up P2 - REGISTRADOS
Anotados en RUNBOOK-ENSAYO-atestacion-sello-etapa1.md s.5b:
- **tokens_total_atribuibles = moneda confirmatoria del baseline** (desglose por cubeta no viable con codex
  exec). Q4 total-vs-total INTACTO; Q1 degrada a total-marginal.
- **Follow-up P2 (hornear en SPECs P2.x):** el total incluye cache no aislable -> ambos brazos MISMO tipo de
  sesion/runtime (cache comparable) o declarar el cache-confound; captura lee stderr; el adversarial-separado
  de P2 (confirmado) habilita taggear tokens_adversarial_informal (imposible en GOAL-P1 in-session). Esto entra
  en las SPECs P2.1/P2.2 que preparo (item 4).

Con el sha256 `d2a13216...ae2f5`, ratifica el cierre de la fila real de GOAL-P1. El piloto de medicion cumplio
su proposito: valido la captura end-to-end y surfaceo la degradacion de cubetas para el freeze.
