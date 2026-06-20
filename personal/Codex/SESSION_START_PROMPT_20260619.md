# Prompt De Inicio De Sesion - Codex

```text
Lee AGENTS.md, personal/Codex/STARTUP_PROMPT.md y personal/Codex/Memory.md antes de actuar.

Regla primordial: no narrar proceso. Solo emitir cierre, bloqueo concreto, fallo/riesgo accionable,
decision requerida o resultado de coordinacion.

Arranque obligatorio:
1. Revisar git status --short y no tocar cambios ajenos.
2. Revisar Area_comun/mailbox/open/.
3. Revisar TASK_INDEX/CLAIMS para TASK-0117/0118/0119.
4. Validar drift antes de cualquier ledger action:
   python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), indent=2, ensure_ascii=False))"

Estado esperado:
- TASK-0117: in_review; handoff Codex -> Arquitecto entregado.
- TASK-0118: proposed/diferida.
- TASK-0119: done.
- #4 sigue OFF: event_auth.enabled=false, chain_enabled=false, agent_signatures_enabled=false,
  anchor_enabled=false. No piloto y no encendido sin GO posterior explicito.
- Cron/monitor actual detenido por orden del operador. No reiniciar sin GO explicito.

Reglas operativas aprendidas:
- Mensaje nuevo a Codex con requires_response:true y requested_action ejecutable = procesar en sesion:
  claim file-scoped, submit_intent para estado, ejecutar o bloquear con una pregunta concreta, responder/mover
  mensaje.
- Mailbox claims siempre file-scoped a MSG-*.md; nunca directorios del mailbox.
- Estado compartido solo via runtime/submit_intent.py o ledger_ops; nunca editar Area_comun/state/*.json a mano.
- No tocar personal/Arquitecto, personal/Analista ni personal/operador salvo instruccion explicita.
```
