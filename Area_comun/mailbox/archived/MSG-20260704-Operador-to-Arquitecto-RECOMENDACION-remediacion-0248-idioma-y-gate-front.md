---
message_id: MSG-20260704-Operador-to-Arquitecto-RECOMENDACION-remediacion-0248-idioma-y-gate-front
from: Operador
to: Arquitecto
type: FYI
status: archived
requires_response: false
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0248-skill-codegen-triage (F-0248-01/02/03)
  - personal/asesor/DRAFT-skill-codegen-triage.md (diseno de referencia; lo alineo a ingles)
one_line_summary: "Dos aclaraciones para la remediacion de TASK-0248 (antes de rutear a Codex). F-0248-02: resuelvela a INGLES {path, reason, verifying_gate, red_flags}, NO revertir a espanol: la capa NEUTRAL es EXPORTABLE/publicable (Carril B) y su SKILL.md ya es ingles; mi draft uso nombres en espanol = inconsistencia MIA, actualiza el spec a ingles (yo alineo mi draft). F-0248-01 (loader) y F-0248-03 (gate producto) = implementacion pura, Codex remedia. NOTA F-0248-03: apps/nova-web sin script 'test' es un hueco LATENTE de GOAL-P1 (el front tenia typecheck, no test) que el clon-limpio del Analista destapo; cerrar antes de las unidades P2 (front medido); GOAL-P1 excluido del contraste, no critico alli."
requested_action: "[RECOMENDACION] Antes de rutear la remediacion de TASK-0248 a Codex, dos aclaraciones del diseno (para no gastar un ciclo en la direccion equivocada): (1) F-0248-02 (forma de salida): RESUELVELA A INGLES -- {path, reason, verifying_gate, red_flags}. NO revertir la entrega a espanol {camino, razon, gate, banderas}. Razon: la capa NEUTRAL de la skill es EXPORTABLE/publicable (Carril B) y su SKILL.md ya esta en ingles; los nombres en espanol venian de MI draft (inconsistencia mia, no de Codex). Actualiza el spec de TASK-0248 a la forma en ingles; yo alineo mi DRAFT-skill-codegen-triage.md a ingles para que quede coherente. (2) F-0248-01 (loader DECISION-0061) y F-0248-03 (gate producto npm test) son IMPLEMENTACION pura -> Codex remedia (registrar en skills.config.json + loader especifico; corregir el EXIT del gate). De acuerdo con el fix-loop del Analista (max 2 iteraciones). NOTA sobre F-0248-03: que apps/nova-web falle 'npm test' por script ausente es un HUECO LATENTE DE GOAL-P1 (la fundacion dejo typecheck del front pero NO un harness de test del front), que el chequeo en clon limpio del Analista destapo. Para la skill, basta corregir el gate. Pero registralo: antes de las unidades MEDIDAS P2 que toquen el front, el harness de test del front debe existir y correr verde en clon limpio (si no, el gate de esas unidades sera falso-verde como en TASK-0209). GOAL-P1 esta excluido del contraste, asi que no es critico reabrirlo; es deuda a cerrar antes del front de P2. No requiere respuesta; es insumo para que la remediacion vaya derecha."
question: ""
---

# RECOMENDACION - Remediacion de TASK-0248: idioma de salida + hueco de gate del front

Antes de rutear la remediacion a Codex, dos aclaraciones (para no gastar un ciclo mal):

## F-0248-02 (forma de salida) -> resolver a INGLES
Deja `{path, reason, verifying_gate, red_flags}`. **NO** revertir a espanol `{camino, razon, gate, banderas}`.
La capa NEUTRAL es EXPORTABLE/publicable (Carril B) y su SKILL.md ya es ingles; los nombres en espanol
venian de MI draft (inconsistencia mia). Actualiza el spec de TASK-0248 a ingles; yo alineo mi DRAFT.

## F-0248-01 + F-0248-03 = implementacion (Codex remedia)
Loader (registrar en skills.config.json + loader especifico) y gate producto (corregir el EXIT de npm test).
De acuerdo con el fix-loop del Analista (max 2 iteraciones).

## Nota sobre F-0248-03 (hueco latente de GOAL-P1)
Que `apps/nova-web` falle `npm test` por script ausente = la fundacion GOAL-P1 dejo typecheck del front pero
NO un harness de test del front; el clon-limpio del Analista lo destapo. Para la skill basta corregir el gate.
Pero REGISTRALO: antes de las unidades MEDIDAS P2 que toquen el front, el harness de test del front debe
existir y correr VERDE en clon limpio (si no, el gate de P2 seria falso-verde). GOAL-P1 excluido del contraste
-> no critico reabrirlo; es deuda a cerrar antes del front de P2.
