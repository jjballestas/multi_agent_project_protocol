---
decision_id: DECISION-0011
title: Claims por fila para los ledgers de estado (TASK_INDEX / PROJECT_STATE)
status: accepted
date: 2026-06-05
ratified_at: 2026-06-05
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0007, DECISION-0009, DECISION-0001, TASK-0027, TASK-0028]
phase: P2
---

# DECISION-0011 — Claims por fila para los ledgers de estado

## Contexto
El claim funciona como **lock** (DECISION-0007) y su granularidad es **archivo completo**. El
chequeo de solape del validador (`validate_collaboration_state`) **exime** `Area_comun/state/CLAIMS.json`
y `Area_comun/mailbox/**` —porque son *ledgers* donde cada agente edita solo sus propias filas— pero
**no exime** `Area_comun/state/TASK_INDEX.json` ni `Area_comun/state/PROJECT_STATE.json`.

Consecuencia (observada en vivo, 2026-06-05): dos agentes que trabajan en paralelo (p.ej. Claude
ratificando TASK-0023 mientras Codex implementa TASK-0027) **no pueden** tener claims activos a la vez,
porque ambos listan esos dos JSON ⇒ el validador marca *overlapping active claims*. El trabajo se
**serializa** por el estado. Cuando el **runtime** (DECISION-0009) empiece a **aplicar** turnos (M1, tras
TASK-0027) cada turno muta estado: la colisión se vuelve constante.

Son **dos problemas distintos**:
1. **Guardrail de coordinación** (validador): trata el archivo como unidad indivisible. *Falso positivo*
   cuando dos agentes tocan **filas distintas**.
2. **Clobber físico**: dos procesos escribiendo el mismo JSON ⇒ *last-writer-wins*. Es independiente del
   guardrail.

## Decisión
Se adopta el modelo de **claims por fila** para los ledgers de estado, **aditivo y opt-in**:

- **`TASK_INDEX.json` y `PROJECT_STATE.json` se tratan como ledgers por fila** (como ya se trata
  `CLAIMS.json`). Un claim puede declarar **qué filas** toca con un selector lógico en el `scope`:
  - `Area_comun/state/TASK_INDEX.json#TASK-0024` — la fila de esa tarea.
  - `Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-0024` — esa entrada de `active_tasks`.
  - `Area_comun/state/PROJECT_STATE.json#<campo>` — un campo de nivel superior (`next_actions`,
    `risks`, `updated_at`, ...).
- **Compatibilidad hacia atrás (conservadora):** un scope **sin** `#selector` (ruta desnuda) = **archivo
  completo** = se solapa con cualquier scope de otro owner sobre ese archivo (comportamiento de hoy).
  El selector `#fila` es **opcional**; los claims históricos no cambian de significado.
- **Regla de solape (guardrail):** para dos claims activos de **distinto owner** sobre el mismo ledger,
  hay conflicto **solo si** referencian la **misma fila** (o uno de ellos es ruta desnuda = todas las
  filas). Filas distintas ⇒ **sin conflicto**. `CLAIMS.json` y `mailbox/**` siguen exentos.
- **Anti-clobber (atomicidad física), separado del guardrail:**
  - En **runtime mode** el **orquestador es el único escritor** del estado (1 turno = 1 commit,
    serializado) ⇒ no hay escrituras concurrentes (DECISION-0009).
  - En **manual mode**, convención: *editar solo las filas declaradas* + *re-leer antes de escribir*
    (el harness ya fuerza re-lectura de archivos modificados). Los escalares compartidos contendidos
    (`updated_at`, `next_actions`) se reclaman con `#campo` o se ceden al escritor único.
- **Alineación con el contrato de turno (SPEC-0026 / TASK-0027):** la invariante *write-allowlist*
  (`changed_paths ⊆ claim`) se extiende a nivel de fila: el orquestador mapea las `transitions` del turno
  a selectores de fila y verifica contra el `scope` del claim del agente.

## Alternativas consideradas
- **B — Eximir TASK_INDEX/PROJECT_STATE como CLAIMS.json (sin comparar filas).** Cambio mínimo pero
  **elimina el guardrail**: dos agentes podrían pisar la **misma** fila sin que el validador lo detecte.
  Descartada: pierde seguridad justo donde el runtime la necesita.
- **C — Solo runtime single-writer.** Resuelve la atomicidad pero **no** desbloquea el modo manual/mixto
  actual (el guardrail seguiría serializando). Se **incorpora** como la pieza de atomicidad de esta
  decisión, no como solución completa.

## Frontera y compatibilidad
- **Neutral de dominio** (es coordinación/tooling, sin términos de negocio).
- **Aditivo ⇒ MINOR** (DECISION-0001): el validador solo **relaja** el solape para filas distintas; no
  introduce fallos nuevos sobre datos existentes (ruta desnuda + ruta desnuda sigue fallando igual que hoy).
- Toca el modelo de coordinación (claim-as-lock, DECISION-0007) y el validador ⇒ requiere esta decisión
  + aprobación humana. Dirección aprobada por el operador (2026-06-05).

## Implementación
Se descompone en **TASK-0028** (impl: gramática de scope + chequeo de solape por fila en
`validate_collaboration_state.py`/`.ps1` con paridad + golden cases + alineación de la write-allowlist del
runtime), especificada en [SPEC-0028](../specs/SPEC-0028-claims-por-fila.md). **Secuenciada después** de
ratificar TASK-0027 (para alinear con el contrato de turno ya estable) y **no concurrente** con TASK-0024
(poda de estado), que también toca el validador.
