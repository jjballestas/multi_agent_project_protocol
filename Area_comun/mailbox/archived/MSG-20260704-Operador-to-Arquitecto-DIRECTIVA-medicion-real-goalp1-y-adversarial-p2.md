---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-medicion-real-goalp1-y-adversarial-p2
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - personal/operador/vision-nova/RUNBOOK-MEDICION-PILOTO-GOAL-P1.md (runbook de medicion)
  - personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_journal.csv (tiene la fila SMOKE en la clave GOAL-P1)
  - Area_comun/handoffs/HANDOFF-TASK-0247-codex-to-arquitecto-1.md (evidencia del build real)
one_line_summary: "Dos acciones. A) MEDICION REAL de GOAL-P1: el journal tiene la fila SMOKE ocupando la clave GOAL-P1 con valores falsos (tokens=12000, fecha_fin=08-jul) -> resetea el journal (archiva a .smoke.csv + fresco) y entrega los tokens_dev/tiempo REALES de la sesion de Codex (pid 148868) para que el Operador cierre la fila real y tu atestes el sha256; reporta que campos NO fueron capturables (hallazgo del piloto para el freeze del schema). B) BLINDAR ADVERSARIAL-SEPARADO para las unidades MEDIDAS P2+ (confirmado por el Operador): el adversarial informal debe ser AGENTE SEPARADO en contexto limpio (dev!=adversarial), nunca self-review del maker; hornear como requisito en las SPECs/GOs de P2.1/P2.2/P4.1/pares y taggear tokens_adversarial_informal a ese agente separado."
requested_action: "[DIRECTIVA] Dos acciones del Operador (2026-07-04). ACCION A -- HABILITAR LA MEDICION REAL DE GOAL-P1 (el Operador corre medir-goalp1.ps1, pero necesita 2 insumos que solo tu tienes): (1) RESETEA EL JOURNAL del corpus: hoy personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_journal.csv tiene la fila SMOKE en la clave GOAL-P1 (event_seq 1-4, tokens_dev=12000 de ejemplo, fecha_fin=2026-07-08 futuro, brazo=baseline). El build REAL no puede escribirse sobre esa clave (append-only + ya cerrada) sin contaminar el corpus sellado. Archiva el journal smoke (p.ej. medicion_journal.smoke.csv + regenera medicion.csv) y deja un journal LIMPIO, para que el Operador abra la fila real de GOAL-P1 sin colision. (2) ENTREGA los datos REALES de la sesion de Codex que construyo GOAL-P1 (pid 148868): tokens_dev reales (fuente_tokens = runtime/comando de la tabla sellada), tiempo de pared, sesiones_n, y si hubo tokens_adversarial_informal del adversarial (checker_formal=0 y coordinacion_gobierno=0 por baseline). Con eso el Operador corre: abrir -> actualizar (orchestration_mode=mono, reworks_n=0, secuencia_veredictos=APROBADO) -> cerrar (estado_final=done, fecha_fin=2026-07-04, tokens reales) -> verificar; tu tomas el sha256 y lo atestas via submit_intent al #4 del hub (corpus del sello). REPORTA como HALLAZGO DEL PILOTO: que campos del schema fueron REALMENTE capturables y cuales cayeron a NA/degradacion (es el proposito del piloto; alimenta el freeze del schema v1.0 en el sello). Alternativa (si el Operador te delega): cierra tu la fila real (tienes corpus+datos+atestacion) y el Operador ratifica. ACCION B -- BLINDAR EL ADVERSARIAL-SEPARADO PARA LAS UNIDADES MEDIDAS P2+ (confirmado por el Operador): para P2.1, P2.2, P4.1 y los miembros de par, el adversarial informal de 12 puntos DEBE ser un AGENTE SEPARADO EN CONTEXTO LIMPIO (NOVA_PROMPT: dev != adversarial, nunca comparten conversacion), NUNCA el self-review del maker. GOAL-P1 quedo ok (excluido del contraste + tu re-verificaste independiente), pero de P2 en adelante es la '1 adversarial' de la definicion del brazo baseline: si el maker escribe su propio adversarial, contamina el brazo. Hornea el requisito en las SPECs/GOs de esas unidades (campo explicito 'adversarial = sesion separada, contexto limpio') y en la medicion taggea tokens_adversarial_informal a ese agente separado. RESPONDE con: (a) journal reseteado (confirmacion + ruta del smoke archivado); (b) datos reales de Codex entregados (o fila real cerrada si el Operador delega) + sha256 atestado; (c) hallazgos de capturabilidad del piloto; (d) confirmacion de que el requisito adversarial-separado queda horneado para P2+."
question: ""
---

# DIRECTIVA - Medicion real de GOAL-P1 (habilitar) + blindar adversarial-separado P2+

Dos acciones del Operador.

## A - Habilitar la medicion real de GOAL-P1
El Operador corre `medir-goalp1.ps1`, pero necesita 2 insumos que solo tu tienes:
1. **Resetea el journal:** hoy tiene la fila SMOKE en la clave GOAL-P1 (tokens=12000 de ejemplo,
   fecha_fin=08-jul futuro). El build real no puede escribirse encima (append-only + cerrada) sin
   contaminar el corpus sellado. Archiva el smoke (medicion_journal.smoke.csv) y deja journal LIMPIO.
2. **Entrega los datos REALES de la sesion de Codex** (pid 148868): tokens_dev reales, tiempo de pared,
   sesiones_n, tokens_adversarial_informal si hubo. Con eso el Operador abre/actualiza/cierra/verifica y
   tu atestas el sha256 -> #4 del hub (corpus del sello).
REPORTA como hallazgo del piloto que campos fueron capturables y cuales cayeron a NA (proposito del
piloto; alimenta el freeze del schema v1.0). Alternativa: cierras tu la fila real y el Operador ratifica.

## B - Blindar adversarial-separado para P2+ (confirmado por el Operador)
Para las unidades MEDIDAS (P2.1/P2.2/P4.1/pares), el adversarial informal de 12 puntos DEBE ser un
AGENTE SEPARADO en contexto limpio (dev != adversarial), nunca self-review del maker. GOAL-P1 ok
(excluido + re-verificaste), pero de P2 en adelante es la '1 adversarial' del brazo baseline. Hornea
el requisito en las SPECs/GOs y taggea tokens_adversarial_informal a ese agente separado.

Responde: journal reseteado + datos reales/sha256 atestado + hallazgos de capturabilidad + confirmacion adversarial-separado P2+.
