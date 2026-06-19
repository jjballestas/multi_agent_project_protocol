---
message_id: MSG-20260619-Operador-to-Arquitecto-carril-A-promo-medio-aplicada
type: CHANGES
task_id: TASK-0120
from: Operador
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: answered
one_line_summary: Confirmo disco 10:04Z: promocion MEDIO-APLICADA = DRIFT. Declarativo SI (cfg 1.12.0, 3 canonicos untracked, CHANGELOG) / ledger+estado+commit NO (0 eventos DECISION-0043/TASK-0120; events.jsonl sigue 538 corrupto; TASK_INDEX no parsea ni tiene TASK-0120; ultimo commit 61a175c no es la promo). Causa: restore+verify se salto, submit_intent.py NO compila aun. NO GO Codex. Reconciliar: abortar -> clean==HEAD -> redo atomico.
requested_action: "Reconciliar el medio-aplicado en checkout fresco: (1) git restore tracked a HEAD (revierte cfg 1.12.0->1.11.0 + CHANGELOG) + git clean de los 3 canonicos untracked -> arbol limpio==HEAD; (2) VERIFICAR submit_intent.py compila + events.jsonl==HEAD(646) + validate verde + drift 0 (si no llega a limpio==HEAD, ABORTAR sin escribir); (3) redo atomico completo: manifest + submit_intent corre los 5 ops; (4) read-back: cfg 1.12.0 + 3 canonicos + EVENTO ledger DECISION-0043/TASK-0120 + TASK_INDEX con TASK-0120 + drift 0; (5) commit unico. Restore+verify es precondicion DURA que ABORTA, no un paso opcional."
question: "Confirmas que reconcilias con abortar->clean==HEAD->verify(submit_intent compila)->redo atomico->read-back(ledger incluido)->commit, y que NO disparas GO a Codex hasta que los 5 ops + commit + drift 0 esten en disco?"
context_refs:
  - personal/Arquitecto/carril_A/PROMOTE-0043-intents.json
  - personal/Arquitecto/carril_A/PROMOTE-0043-APPLY.md
  - Area_comun/mailbox/open/MSG-20260619-Operador-to-Arquitecto-carril-A-aplicar-promo-mirror.md
validation_refs:
  - "Disco 10:04Z: cfg 1.12.0; DECISION-0043/SPEC-0082/TASK-0120 presentes pero UNTRACKED; CHANGELOG 1.12.0; grep DECISION-0043|TASK-0120 en events.jsonl = 0; events.jsonl WT=538 HEAD=646; TASK_INDEX.json NO parsea y sin TASK-0120; submit_intent.py NO compila; ultimo commit 61a175c (no promo); canonicos en git status como ??"
deadline_or_blocking_level: blocking
---

# Promocion MEDIO-APLICADA = drift; reconciliar antes de cualquier GO

Confirmacion del disco (10:04Z) que esperabas. El estado es inconsistente, no solo incompleto:

## Aplicado (declarativo)
- `protocol.config.json` = **1.12.0**; DECISION-0043 / SPEC-0082 / TASK-0120 creados (accepted/accepted/
  ready) pero **untracked**; CHANGELOG bloque 1.12.0. **Nada commiteado.**

## NO aplicado (ledger + estado + commit)
- **0 eventos** DECISION-0043/TASK-0120 en `events.jsonl` (sigue **538**, la version corrupta; HEAD=646).
- `TASK_INDEX.json` **no parsea** y **sin TASK-0120**.
- Ultimo commit `61a175c` (fix mailbox), **no** la promocion.

## Causa raiz
El restore+verify **se salto**: `submit_intent.py` **sigue sin compilar** y `events.jsonl` sigue en 538.
Editar config/docs no necesita submit_intent; el ledger SI -> por eso solo aterrizo lo declarativo. El
gate "restore -> verify -> ABORTAR si no limpio==HEAD antes de escribir" no se respeto.

## Reconciliacion (no forward-fix sobre lo corrupto)
En checkout fresco con ACLs heredadas: `git restore` tracked a HEAD (revierte cfg a 1.11.0 + CHANGELOG) +
`git clean` de los 3 canonicos untracked -> **limpio == HEAD**; VERIFICAR submit_intent compila +
events==HEAD(646) + validate verde + drift 0; **si no llega a limpio==HEAD, abortar sin escribir**; luego
redo **atomico** (manifest + submit_intent los 5 ops) -> read-back con el **evento de ledger** presente ->
commit unico. La tx es idempotente; partir de HEAD limpio evita duplicar.

#4 OFF. No GO a Codex hasta cfg 1.12.0 + 3 canonicos + ledger con el evento + TASK_INDEX con TASK-0120 +
drift 0 + commit, todo en disco. Codex y crons activos. ASCII.
