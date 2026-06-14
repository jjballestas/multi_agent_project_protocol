# Codex Startup Prompt

Prompt corto para pegar al iniciar una sesion nueva:

```text
Lee AGENTS.md y personal/Codex/STARTUP_PROMPT.md.
```

Despues de leerlo, ejecuta este arranque:

REGLA PRIMORDIAL (DECISION-0038): no narrar proceso. No digas "voy a leer", "voy a revisar", "ahora hago"
ni recapitules pasos intermedios. Solo informa cierre, bloqueo con pregunta concreta, fallo/riesgo/cambio
accionable o contenido sustantivo donde el razonamiento sea el entregable.

1. Lee `personal/Codex/Memory.md`.
2. Revisa `git status --short` y no toques cambios ajenos.
3. Revisa `Area_comun/mailbox/open/`.
4. Verifica estado con:

```powershell
git log -5 --oneline
Get-ChildItem -File Area_comun\mailbox\open | Select-Object -ExpandProperty Name
python scripts\validate_collaboration_state.py --root .
python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), indent=2, ensure_ascii=False))"
```

## Estado Esperado

- Refresco: 2026-06-14 Europe/Madrid.
- HEAD observado antes del refresco: `60465f1 chore(ci+coordination): cablea chain_auth_combined en CI + stand-down de Codex`.
- v1.6.0 publicado; TASK-0111 y TASK-0113 cerradas.
- `mailbox/open` puede contener `MSG-20260614-Claude-to-Codex-stand-down-cron.md`; es FYI de parada.
- No hay trabajo no-gated para Codex. No iniciar cron/monitor ni reclamar tareas sin nuevo GO.
- Tareas Codex restantes conocidas: TASK-0095, TASK-0096, TASK-0100 en estado propuesto/gated.
- Mantener off: chain, agent_signatures, anchor, subagents y SA.4, salvo GO explicito.

## Reglas De Arranque

- Estado compartido: solo via runtime/submit_intent o ledger_ops; nunca edicion manual de `Area_comun/state/*.json`.
- Crear claim antes de editar rutas compartidas, incluido mailbox.
- Despues de cada commit Codex, actualizar `personal/Codex/Memory.md`.
- No editar `personal/Claude/` ni `personal/operador/` salvo instruccion explicita.
- Staging siempre por rutas explicitas.
