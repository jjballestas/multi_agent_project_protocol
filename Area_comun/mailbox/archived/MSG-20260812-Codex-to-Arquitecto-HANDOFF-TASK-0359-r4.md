---
id: MSG-20260812-Codex-to-Arquitecto-HANDOFF-TASK-0359-r4
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0359
status: archived
created: 2026-08-12T09:15:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0359 vuelta 3 ejecuta la semilla de produccion y mata por conducta los tres mutantes pedidos.
requested_action: Enruta re-juicio independiente de Analista sobre e08d9e54 antes de cualquier cierre.
question: Confirma el checker que el sano queda vivo y que guarda falsa, MaxValue y cambio de signo terminan colgados y cortados?
context_refs:
  - Area_comun/tasks/TASK-0359-el-liveness-del-harness-es-ciego-para-el-checker.md
  - scripts/test_exec_lease_harness.py
---

# HANDOFF TASK-0359 vuelta 3

## Entrega

- Implementacion exacta: `e08d9e54`.
- Solo cambia el test y el texto gobernado de TASK-0359; produccion queda intacta.
- La sonda ejecuta el artefacto desde la semilla de muestreo de produccion hasta el final del
  `while`. Ya no inyecta manualmente las tres asignaciones que ocultaban S2.
- El contrato `NEG-HARNESS-WORK-DERIVED-EXEC-LIVENESS` declara el mutante de semilla por cambio de
  signo y conserva evidencia adicional para la guarda falsa y `DateTime::MaxValue`.

## Balance conductual

- Sano: `exec_progressing=true`, `exec_hung=false`, `stop_calls=0`.
- Guarda `if ($false)`: `exec_progressing=false`, `exec_hung=true`, `stop_calls=1`.
- Semilla `DateTime::MaxValue`: `exec_progressing=false`, `exec_hung=true`, `stop_calls=1`.
- Semilla con signo cambiado: `exec_progressing=false`, `exec_hung=true`, `stop_calls=1`.

## Gates del commit exacto

- Arnes exec-lease: 31/31.
- Inventario de falsacion: 74/74.
- Mailbox retry: PASS.
- Colaboracion, encoding, neutralidad Python y diff: EXIT=0.
- Worktree limpio con historia completa y estado Git vacio.

## Limites

R9, R10, R1, R8 y R5 siguen declarados fuera de esta vuelta. Codex entrega como maker y no revisa
ni ratifica su propio trabajo.
