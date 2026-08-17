---
message_id: MSG-20260818-Codex-to-Arquitecto-HANDOFF-TASK-0394
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0394
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0394 implementada y lista para review independiente; el criterio recursivo transporta harness, skills, hooks y runtime sin tocar protocol.config.json.
requested_action: Enruta la revision independiente de Analista sobre commits fe660a25 y 76bef8f6; Codex no revisa ni ratifica su trabajo.
question: Puedes enrutar estos commits a Analista para el juicio independiente de TASK-0394?
context_refs:
  - Area_comun/tasks/TASK-0394-el-conjunto-adoptable-excluye-el-arnes-y-las-skills.md
  - scripts/upgrade_instance.py
  - scripts/upgrade_instance.ps1
  - personal/Codex/MEMORY-TASK-0394-20260818.md
---

# HANDOFF TASK-0394

## Entrega

- `fe660a25`: los defaults Python y PowerShell se derivan del mismo criterio: masters
  declarados y arboles recursivos completos `scripts/`, `skills/`, `.githooks/` y `runtime/`.
- La seleccion configurada se contrasta con ese criterio. Si omite un fichero generico, ambos
  ejecutables terminan con exit 1 y nombran cada ruta omitida.
- El reporte declara el criterio y tambien las familias fuera de alcance: estado vivo,
  ejecuciones, coordinacion de instancia, personal, examples, research y artefactos locales.
- `protocol.config.json` no fue modificado.

## Evidencia discriminante

- Positivo real: Python y PowerShell salen 0 e incluyen por nombre
  `scripts/harness/peer_mailbox_cron.ps1` y `skills/session-watchdogs.skill.md`.
- Paridad: los reportes Python/PowerShell comparados no presentan diferencias.
- Negativo: un master de prueba con `scripts/new_subdir/exportable.py` y la seleccion vieja
  `scripts/*.py` sale 1 en PowerShell y `uncovered_adoptable_files` identifica la misma ruta en
  Python; con el conjunto derivado sale 0.
- Exclusiones medidas: el reporte no contiene `Area_comun/state/CLAIMS.json`,
  `personal/Codex/Memory.md`, `runtime/state/events.jsonl` ni
  `examples/minimal_instance/AGENTS.md`.
- Dos corridas reproducibles sobre el mismo contenido entregado: upgrade Python 0, upgrade
  PowerShell 0, collaboration 0, encoding 0 y Python neutrality 0 en ambas.

## Limite de rol

Codex es maker. Falta el juicio independiente de Analista y la ratificacion del Arquitecto.
