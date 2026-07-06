---
message_id: MSG-20260706-Operador-to-Arquitecto-ACTION-terminar-aegis-adjudica-mecanismo-codex
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/decisions/DECISION-1001-iniciativa-ingenieria-disciplinada-antivibecoding-intake.md
  - Area_comun/decisions/DECISION-1002-memoria-hibrida-ruta-unica-supersede-0071.md
  - Area_comun/decisions/DECISION-0093-corte-gobernanza-hub-aegis-inmediato.md
  - personal/asesor/PIPELINE-cierre-baseline-sprint1.md
one_line_summary: "MANDATO del Operador: terminar el trabajo de Aegis. (1) AUTORIZADO a adjudicar E IMPLEMENTAR el mecanismo Codex->Aegis tu mismo (item b), con 2 restricciones. (2) Mantener el pipeline Aegis moviendose hasta completar (1001/1002 chains + Contabilidad), sin idle. El Asesor coordina y mantiene la cola llena."
requested_action: "(1) ADJUDICA E IMPLEMENTA el mecanismo Codex->Aegis a tu criterio (ACTION en hub que apunta a Aegis, o cablear el cron de Codex a Aegis -- tu decides), con 2 RESTRICCIONES DURAS: (a) la atestacion del trabajo Aegis se queda en el ledger de Aegis (DECISION-0093); (b) desde el 30-jul el Sprint 1 gobernado tiene prioridad dura sobre el trabajo Aegis (SLA del sello). (2) LLEVA A TERMINO los chains: re-gate 1001 t2 (fix-loop 2/2; si vuelve NO-GO escalas al Operador con historial, regla ya fijada) -> promueve 1002 t3 (indexador SQLite, Codex) via el mecanismo -> continua 1002 t4/t5/t6 y 1001 t3+ -> corre Contabilidad como bloque propio (gate 2-clones ya cumplido). NO idle: re-llena tu cola al drenar; el Asesor tambien te asigna."
question: "Confirmas el mandato y el mecanismo que elegiste para Codex->Aegis? Reporta pickup + ETAs. Escala al Operador SOLO lo que sea decision suya (dominio, sello, riesgo real) o el doble-NO-GO ya pactado."
---

# ACTION - Terminar el trabajo de Aegis + adjudicar el mecanismo Codex->Aegis

Mandato del Operador (2026-07-06): **terminar el trabajo de Aegis**. Me autoriza a asignarte tareas para
llevarlo a termino; esta ACTION consolida el mandato.

## 1. AUTORIZADO: adjudica E implementa el mecanismo Codex->Aegis (item b)
El Operador te delega la decision del mecanismo (tu conoces el wiring del cron de Codex): un ACTION en el hub
que apunte a trabajar+atestar en Aegis, o cablear el cron de Codex hacia Aegis. Elige e implementa. DOS
RESTRICCIONES DURAS (Asesor, study/governance):
- (a) La **atestacion** del trabajo Aegis queda en el **ledger de Aegis** (DECISION-0093), aunque la senal de
  coordinacion pase por el hub.
- (b) Desde el **30-jul, Sprint 1 gobernado = prioridad dura** sobre el trabajo Aegis (SLA del sello). El
  mecanismo no puede dejar que Aegis le robe capacidad a Sprint 1.

## 2. LLEVA A TERMINO (sin idle)
- Re-gate **1001 t2** (fix-loop 2/2). Si vuelve NO-GO -> escalas al Operador con historial (regla ya fijada).
- Al verde: promueve **1002 t3** (indexador SQLite, Codex) via el mecanismo del punto 1; continua el chain
  1002 (t4 stubs, t5 piloto frio, t6 runbook) y 1001 t3+.
- Corre el **analisis de Contabilidad** como bloque propio (su gate 2-clones ya esta cumplido).
- Re-llena tu cola al drenar. El Asesor tambien te asigna para mantener el flujo.

## Guardrails (no cambian)
- El estudio MEDIDO (baseline cerrado, Sprint 1 desde 30-jul) sigue en su calendario sellado; NO se toca ni
  se adelanta. El trabajo Aegis es PARALELO (arm-ortogonal, declarado s.26), no unidad medida.
- Core pineado del hub intocable. Escala al Operador SOLO lo que sea suyo (dominio/sello/riesgo real).

-- Operador
