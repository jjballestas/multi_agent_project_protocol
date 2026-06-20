---
message_id: MSG-20260620-Arquitecto-to-Operador-BLOCKER-canonico-rojo-draft-remediacion
task_id: none
type: DECISION
from: Arquitecto
to: Operador
status: archived
requires_response: false
response_owner: Operador
one_line_summary: "BLOQUEO: canonico 5c918d2 validate exit 1 (12 errores) por defectos del intake ya mergeado (B1 seed files nunca escritos; B2 validador no reconoce ids REQ-<hash> en selectores de claim). Preempta el triage (no se promueve sobre rojo). Ratificaste opcion 1 = remediar primero. DRAFT-TASK-0136 listo (validador acepta REQ-, builder escribe seed + scopes validos + test regresion-proof, reconcilia los 4 seeds). Espera tu ratificacion del draft -> GO a Codex. Draft #1 (reset/confirm) en cola detras."
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-TASK-0136-reconcile-intake-canonical-red.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0086-ext3-intake-reset-confirm.md
  - scripts/validate_collaboration_state.py
deadline_or_blocking_level: blocking
---

# BLOQUEO - canonico ROJO por el intake; DRAFT de remediacion (opcion 1 ratificada)

## Hallazgo (verificado en canonico 5c918d2)
`validate_collaboration_state` exit **1**, 12 errores, por los 4 requisitos montados via intake. NO por mis
cambios (working tree limpio). Dos defectos del intake ya mergeado (TASK-0133/0134), anomalia DECISION-0018:
- **B1 (4):** el builder fija `file: req-<hex>-requirement-seed.md` pero NUNCA lo escribe.
- **B2 (8):** el validador (regex L76, solo `active_tasks/TASK-NNNN`) NO reconoce los ids `REQ-<hash>` del
  intake -> los claim scopes del relay (`#REQ-...`, ya released) salen "invalid row selector".

No puedo promover ningun SPEC mientras el canonico este rojo (no cumpliria validate exit 0).

## Remediacion (DRAFT-TASK-0136; opcion 1 que ratificaste)
1. **Validador (core neutral):** aceptar `REQ-[0-9A-Fa-f]+` ademas de `TASK-\d{4}` en los selectores.
2. **Intake builder (Codex):** escribir el seed file + claim scopes validos + **test permanente** "un intake
   deja el canonico VERDE" (regresion-proof: nunca mas rompe el canonico).
3. **Reconciliar los 4 seeds existentes** (contenido recuperado del ledger) -> validate exit 0.
maker=Codex / checker=Arquitecto; #4 byte-identica; gates con/sin secretos; clon limpio.

## Pregunta de implementacion (tu eleccion, menor)
El validador es core/neutral (mi dominio). Lo autoro YO y Codex/Analista revisa, o lo implementa Codex dentro
de TASK-0136 con mi check? Recomiendo: Codex implementa todo (builder+regex+tests) y yo checker (mantiene
maker!=checker); yo proveo la spec exacta del regex. Dime si prefieres otra division.

Ratifica DRAFT-TASK-0136 -> GO a Codex. Tras cerrarlo (canonico verde) retomo los 4 SPECs de a una desde el
#1 (DRAFT-SPEC-0086-ext3 ya listo). NOTA: este hilo se mueve sobre canonico rojo a proposito (es la
remediacion); lo dejo explicito.
