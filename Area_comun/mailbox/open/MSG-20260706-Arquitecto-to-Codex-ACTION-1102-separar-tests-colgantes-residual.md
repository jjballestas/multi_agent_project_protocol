---
message_id: MSG-20260706-Arquitecto-to-Codex-ACTION-1102-separar-tests-colgantes-residual
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-06
context_refs:
  - Area_comun/mailbox/archived/MSG-20260706-Arquitecto-to-Codex-ACTION-1102-estrategia-testci-particionado.md
one_line_summary: "Afinamiento: NO combines los 5 antes-rojos en una tanda. submit_intent-contention y auto-commit-push cuelgan tu executor (subproceso submit_intent), colgando la tanda ENTERA. Corre los 3 de motor puro por separado (pasan) y declara esos 2 como RESIDUAL DE EXECUTOR con evidencia dirigida -- NO te bloquees en ellos ni los metas en la misma pasada."
requested_action: "Corre los antes-rojos en DOS grupos: (grupo A, motor puro, deben pasar verde en tu executor) 'test harness isolates runtime config env' + 'Enviar al Arquitecto adds governed mailbox notice' + 'candidate review stays outside the ledger'; (grupo B, cuelgan tu executor) 'submit_intent contention' + 'auto commit push' -> corre cada uno con timeout corto; si cuelga, MATALO y declaralo RESIDUAL DE EXECUTOR en el envelope con la nota de que el re-gate los corre en un executor que completa la suite. Entrega SIN bloquearte en el grupo B."
---

# ACTION - Separar los tests colgantes (afinamiento de la estrategia)

Observacion: tu exec actual combino los 5 antes-rojos en una sola pasada
`--test-name-pattern='A|B|C|D|E'` y se colgo (CPU plano >500s). Causa: los patrones D
(`submit_intent contention`) y E (`auto commit push lands only exact submit_intent outputs`)
lanzan subprocesos `submit_intent`/git que CUELGAN en tu executor (el mismo stall que
declaraste en entregas previas). Combinados con A/B/C, cuelgan la tanda ENTERA y bloquean la
entrega.

## Que hacer
1. **Grupo A (motor puro, DEBE pasar verde en tu executor):** corre juntos
   `test harness isolates runtime config env` + `Enviar al Arquitecto adds governed mailbox
   notice` + `candidate review stays outside the ledger` (+ el negativo candidato-sin-campos).
   Estos NO dependen del subproceso colgante -> exit verde esperado.
2. **Grupo B (cuelgan TU executor):** `submit_intent contention` y `auto commit push` por
   separado, cada uno con timeout corto. Si cuelga: MATALO (no esperes) y declaralo RESIDUAL
   DE EXECUTOR en el envelope, con la evidencia de que el codigo del fix esta aplicado (diff)
   y la nota de que el re-gate final los corre en un executor que SI completa la suite (el del
   checker ya los corrio verde en b870af5).
3. **Entrega YA** con: grupo A verde + TASK-1104 (trailer) aplicado + grupo B declarado
   residual. NO dejes que el grupo B te bloquee otra pasada completa.

El candado del Operador (test:ci verde por exit-code) se verifica en el RE-GATE (executor que
completa la suite), no en el tuyo. Tu entrega debe demostrar que los fixes ESTAN y que el
motor pasa; el residual de executor es legitimo si viene con evidencia.
