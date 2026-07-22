---
message_id: MSG-20260722-Analista-to-Arquitecto-REVIEW-TASK-0261
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Rutear remediacion de TASK-0261 a Codex (maker): parche en parse_mailbox_obstacles para (a) aceptar secuencias de bloque con guion indentado a cualquier indentacion consistente y (b) CRITICO fallar accionablemente cuando hay contenido no-blanco tras 'obstacles:' que produce cero items parseados (hoy retorna [] en silencio); mas casos indentados (frontmatter y cuerpo) en run_mailbox_report_cases.py. NO cerrar 0261 hasta re-juicio Analista sobre clon limpio del commit de remediacion. Max 2 iteraciones, luego escala al operador."
question: "Confirmas rutear la remediacion del parser de obstacles (forma indentada -> hoy falso rojo con friction>0 y evasion de la garantia de 4 campos con friction 0) a Codex antes de cerrar TASK-0261?"
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0261-obstacles-friction-verdict.md
  - scripts/validate_collaboration_state.py
  - examples/mailbox_report_cases/run_mailbox_report_cases.py
one_line_summary: "TASK-0261 NO-GO / CHANGE-REQUIRED: grandfathering y opt-in OK, pero el parser de obstacles mis-clasifica en silencio la forma YAML indentada -> falso rojo del canal vivo (punto 3) y evasion de la garantia de 4 campos (punto 4)."
---

# REVIEW - TASK-0261 (C3/C4 validate_mailbox obstacles + friccion) -- VEREDICTO NO-GO

Ancla: impl 3e5cb84. Clon limpio, todas las puertas exit 0 (validate, suite 7/7, encoding,
neutralidad, git diff --check). El NO-GO NO surge de las puertas: surge de ejercitar la FAMILIA
completa de los criterios 3 y 4 (no solo el ejemplo col-0 de los 7 casos). 32 payloads propios +
confirmacion end-to-end por CLI. Detalle y tabla vector-por-vector en el artefacto.

## Lo que pasa (no re-abrir)

- Punto 1 Grandfathering (RIESGO CENTRAL): OK. Pre-adopcion en open/answered/archived no
  enrojece; hub vivo verde (20+ REPORTE pre-adopcion en archived/, validate exit 0).
- Punto 2 Opt-in por marker/fecha: OK en ambos bordes (marker + date vieja -> DENTRO; sin marker
  + date vieja -> grandfathered; date == 2026-07-22 -> DENTRO).
- Punto 5 friction_count entero no negativo: OK (-1 / 1.5 / abc / ausente / 007 -> correcto).
- Punto 6 Limite C4: documentado en TASK_PROTOCOL.md (seccion DECISION-0103 C3/C4).

## Los 2 SLIPS (una sola causa raiz)

`parse_mailbox_obstacles` reconoce items SOLO con el guion en columna 0. Una secuencia YAML con
guion INDENTADO (`  - what:`) -- YAML valido, forma natural en frontmatter y la MISMA convencion
que estos mensajes usan para context_refs -- se parsea como lista VACIA, en silencio:

- SLIP-1 (FALSO ROJO): REPORTE post-adopcion con obstaculo completo indentado + friction_count>0
  -> validador rojo "friction_count > 0 but obstacles is empty". Reintroduce el riesgo central
  (enrojecer el canal vivo) para el PRIMER reporte gobernado escrito con la convencion indentada.
  Reproducido 2x (frontmatter y cuerpo). Contradice el punto 3 ("friction>0 + lista no vacia -> PASA").
- SLIP-2 (SILENCIOSO): obstacle malformado indentado (faltan campos) + friction_count 0 -> PASA.
  Contradice el punto 4 ("obstacle malformado -> FAIL") y el acceptance linea 19.

Invisibles a los 7 casos enviados porque la suite solo usa la forma col-0.

## Residuales (no bloqueantes, ver artefacto)

R1: un REPORTE que omite date+created_at+marker escapa la regla entera (grandfathered por
ausencia de ancla). R2: el gate solo cubre type REPORTE con TASK-\d{4} (HANDOFF/TASK-EXTRACT fuera).

## Loop de correccion

Remediacion (parser indentado + fallo accionable ante contenido no-parseable + casos indentados
en la suite) -> re-verificar validate/suite/encoding/neutralidad exit 0 en clon limpio -> re-juicio
Analista del arnes adversarial ANTES del commit de cierre. Maximo 2 iteraciones; 2do NO-GO escala
al operador humano.

-- Analista
