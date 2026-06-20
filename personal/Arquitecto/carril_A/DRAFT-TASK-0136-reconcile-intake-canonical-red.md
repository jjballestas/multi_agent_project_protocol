# DRAFT - TASK-0136: Remediacion - el intake dejo el canonico ROJO (validate exit 1); reconciliar + regresion-proof

> DRAFT en personal/Arquitecto; NO promovido. Espera ratificacion. maker=Codex / checker=Arquitecto.
> Anomalia DECISION-0018: el intake ya mergeado (TASK-0133/0134) produjo estado que ROMPE el validador del
> protocolo. PRIORIDAD sobre los 4 SPECs (no se puede promover sobre canonico rojo).

## Sintoma (canonico 5c918d2)
`validate_collaboration_state` exit 1, **12 errores** por los 4 requisitos montados via intake:
- **B1 (4 err):** cada `task_upsert` requirement fija `file: Area_comun/tasks/req-<hex>-requirement-seed.md`
  pero el builder NUNCA crea ese archivo -> "references missing task file".
- **B2 (8 err):** el relay del intake construyo claim scopes `TASK_INDEX.json#REQ-<hex>` y
  `PROJECT_STATE.json#active_tasks/REQ-<hex>`, pero el validador (regex `PROJECT_STATE_SELECTOR_PATTERN`,
  scripts/validate_collaboration_state.py L76: `^(active_tasks/TASK-\d{4}|...)$`) SOLO reconoce ids
  `TASK-NNNN`, no el esquema `REQ-<hash>` que el intake crea (DECISION-0051/0052) -> "invalid row selector".

## Causa raiz
Mismatch entre el esquema de id de requisitos del intake (`REQ-<hash>`, ratificado) y (a) la creacion del
seed file (no se escribe) y (b) la regex de selectores del validador (solo `TASK-NNNN`).

## Alcance (remediacion; opcion 1 ratificada por el operador)
1. **Validador (core neutral):** extender los patrones de selector para aceptar ids de requisito
   `REQ-[0-9A-Fa-f]+` ademas de `TASK-\d{4}` (en `active_tasks/...` y en el selector de TASK_INDEX).
   Reconoce el esquema ratificado; cambio minimo, neutral (sin dominio). [Arquitecto provee la spec exacta del
   regex; Codex implementa; Arquitecto checker. Si el operador prefiere que yo autore el core directamente y
   Codex/Analista revisen, lo ajusto.]
2. **Intake builder (Zeus-protocol):** que cada intake EXECUTE deje el canonico VERDE:
   - escribir el seed file en el `file:` referenciado (frontmatter consistente + narrativa + intencion), o no
     fijar `file:` para seeds (decision de implementacion; recomiendo ESCRIBIR el seed = trazabilidad);
   - construir los claim scopes del relay con selectores VALIDOS para el validador.
   - **PRUEBA NEGATIVA/COMPORTAMIENTO PERMANENTE:** un test que tras un intake EXECUTE corre el validador y
     asevera exit 0 (regresion-proof: un intake nunca mas rompe el canonico).
3. **Reconciliar los 4 requisitos existentes:** crear los 4 seed files (REQ-DCC3BC1A/FB27AF72/B65E7802/
   444E0DE5) con su contenido (recuperado del ledger); con el validador ya tolerante a `REQ-` ids, los claims
   released dejan de marcar error. Resultado: validate exit 0.

## DoD / cierre
- `validate_collaboration_state` exit 0 CON y SIN secretos (clon limpio, DECISION-0046); drift 0; #4 epoca
  1.14.0 byte-identica; encoding/neutrality exit 0.
- Test permanente "intake deja canonico verde" verde (regresion-proof); node --test/CI verde.
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker. Commit como Arquitecto +
  Co-Authored-By: Codex.

## Nota
Tras cerrar TASK-0136 (canonico verde), retomo los 4 SPECs de a una empezando por el #1 (REQ-DCC3BC1A,
DRAFT-SPEC-0086-ext3 ya listo).
