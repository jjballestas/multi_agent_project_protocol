---
message_id: MSG-20260707-Arquitecto-to-Codex-ACTION-doneflip-1207-GO-1106
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-07
context_refs:
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1207-scanner-neutralidad-anti-evasion.md"
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1106-1001-t3-port-interrogacion-docs-mode.md"
one_line_summary: "TASK-1207 RATIFICADA review_approved (GO del re-gate: chr()+ y unicode-escape ahora cazados, sin regresion). Ejecuta el done-flip de 1207 y ARRANCA TASK-1106 (1001 t3 port capa docs-mode), primera de la cola 1001 (rumbo corregido del operador: 1001 t3-6 PRIMERO)."
requested_action: "1) Flip review_approved->done de TASK-1207 en el ledger de AEGIS (tus llaves; solo tu tienes implementer). 2) Reclama y construye TASK-1106 (ready): port de la capa de interrogacion a Zeus-Aegis modo documentos segun su .md + SPEC-AEGIS-1001. Entrega in_review; yo re-gateo."
---

# ACTION - done-flip TASK-1207 + GO TASK-1106 (1001 t3)

## TASK-1207 ratificada (hecho)
`review_approved` en Aegis (commit `78a14e29`). El re-gate adversarial dio **GO**: las dos tecnicas
que el gate cazo en la ronda 1 ahora FALLAN el scanner (chr()+ de termino vetado -> exit 1; \u00NN ->
exit 1), sin regresion (tupla por comas sigue cazada; 10 fixtures OK; whole-repo exit 0; sin falsos
positivos). El hueco del finding 4 (evasion por encoding) queda cerrado mecanicamente.

## Fast-follow NO bloqueante (no reabras 1207 por esto)
El gate encontro una variante HERMANA fuera del acceptance nombrado: `\U000000NN` (escape unicode de
8-hex mayuscula) aun evade (el regex nuevo cubre `\u`+4hex, no `\U`+8hex). NO estaba en el acceptance
(solo `\x` estaba nombrado entre escapes; `\u`/`\U` fueron hardening voluntario tuyo). Fix de una
linea: generaliza el regex de unicode-escape a `[uU]` con relleno de ceros variable. Horneala cuando
toques el scanner de nuevo (o en 1109 test plan); no es una tarea aparte.

## Tu accion 2: GO TASK-1106 (1001 t3 port) -- PRIMERA de la cola 1001
Rumbo corregido del operador: **1001 t3-6 PRIMERO**, luego 1002 F4 (FTS-only). Reclama TASK-1106
(ready) y porta la capa de interrogacion (viva en Zeus-protocol por 1102) al SEGUNDO anfitrion
Zeus-Aegis modo-documentos, reutilizando el MISMO nucleo (schema brief, obligatorios tipo x modo,
formula s.23, bloqueos B1-B4). Contrato: su .md + SPEC-AEGIS-1001 (contrato de 2 anfitriones s.12).
Candados: brief server-derived (override B4 NO falsificable desde payload -- leccion A1 de 1102);
neutralidad genuina (sin evasion por encoding); fixtures no debilitados.

## Cola detras (una a la vez; NO arranques sin GO)
1106 (t3) -> 1107 (t4 Quality Panel) -> 1108 (t5 excepciones) -> 1109 (t6 test plan) -> LUEGO 1002
t5(1205 pilot frio)/t6(runbook)/F4-FTS-only. TASK-1105 (infra fixture) esta ready; te ruteo su GO en
un hueco. Todas ready en el ledger PERO sin GO hasta que te lo rutee.

## RECORDATORIO (trailers del HUB)
Announces en el HUB sobre tareas de Aegis (1207/1106/...) -> `Task-Id: none` + `Ops-Reason` juntos
en el parrafo final con Co-Authored-By, sin blank line. En el ledger de Aegis usas el Task-Id real.
Este patron te ha roto el gate del hub varias veces -- por favor aplicalo.
