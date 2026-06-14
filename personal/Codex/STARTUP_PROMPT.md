# Codex Startup Prompt

Prompt corto para pegar al iniciar una sesion nueva:

```text
Lee AGENTS.md, personal/Codex/STARTUP_PROMPT.md y personal/Codex/Memory.md.
```

Despues de leerlo, ejecuta este arranque:

REGLA PRIMORDIAL (DECISION-0038): no narrar proceso. No digas "voy a leer", "voy a revisar", "ahora hago"
ni recapitules pasos intermedios. Solo informa cierre, bloqueo con pregunta concreta, fallo/riesgo/cambio
accionable o contenido sustantivo donde el razonamiento sea el entregable.

1. Ya debes haber leido `personal/Codex/Memory.md`; si no, leelo antes de tocar estado o mailbox.
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

- Refresco: 2026-06-15 Europe/Madrid.
- HEAD observado antes de este refresco: `823b5b9 chore(personal): renombra areas a la identidad nueva (personal/Claude->Arquitecto, personal/Claude-analista->Analista)`.
- Trio OFF-PILOT cerrado: TASK-0100 done, TASK-0095 done, TASK-0096 done.
- Codex esta en stand-down: no iniciar cron/monitor ni reclamar tareas sin reactivacion explicita del operador.
- El cron local de coordinacion fue detenido; `personal/Codex/coord_cron.stop` puede existir y debe respetarse.
- Reforma de identidad aplicada: dirigirse al arquitecto como `Arquitecto` y a la voz analista como `Analista`.
- El actor tecnico del ledger fue renombrado a `Arquitecto` por re-genesis coordinado; verifica drift antes de cualquier ledger action.
- Mantener off: chain, agent_signatures, anchor, subagents y SA.4, salvo GO explicito.

## Reglas De Arranque

- Estado compartido: solo via runtime/submit_intent o ledger_ops; nunca edicion manual de `Area_comun/state/*.json`.
- Crear claim antes de editar rutas compartidas, incluido mailbox.
- Despues de cada commit Codex, actualizar `personal/Codex/Memory.md`.
- No editar `personal/Arquitecto/`, `personal/Analista/` ni `personal/operador/` salvo instruccion explicita.
- Staging siempre por rutas explicitas.
