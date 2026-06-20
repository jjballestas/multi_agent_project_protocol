# Codex Startup Prompt

Prompt corto para pegar al iniciar una sesion nueva:

```text
Lee AGENTS.md, personal/Codex/STARTUP_PROMPT.md y personal/Codex/Memory.md antes de actuar.

Regla primordial: no narrar proceso. Solo emitir cierre, bloqueo concreto, fallo/riesgo accionable,
decision requerida o resultado de coordinacion.

Arranque obligatorio:
1. Revisar git status --short y no tocar cambios ajenos.
2. Revisar Area_comun/mailbox/open/.
3. Revisar TASK_INDEX/CLAIMS para tareas activas de Codex y mensajes nuevos dirigidos a Codex.
4. Validar drift antes de cualquier ledger action.
5. Validar estado con:
   - python scripts/scan_encoding.py --root .
   - python scripts/scan_domain_neutrality.py --root .
   - python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), indent=2, ensure_ascii=False))"
   - python scripts/validate_collaboration_state.py --root .

Estado esperado al cierre del 2026-06-20 Europe/Madrid:
- Version/epoch canonico: v1.14.0.
- #4 ON en la instancia: event_auth, chain, agent signatures y anchor habilitados; no asumir OFF-PILOT.
- TASK-0130, TASK-0131 y TASK-0132 estan done; no hay claims activos de Codex.
- Mailbox open esperado: solo .gitkeep (si aparece mensaje nuevo a Codex, procesarlo).
- Drift esperado: has_drift=false, ultimo observado up_to_seq=811.
- Validacion completa verde: encoding OK, neutrality OK, validate_collaboration_state OK; validate sin secretos tambien fue OK en TASK-0132.
- D:/Agentes/Zeus/Zeus-protocol contiene el front MVP T0 cerrado:
  - 58d39fb: selector multi-proyecto read-only + kickoff RF-10 gobernado.
  - 2ca79cc: routing real de 7 vistas (solo un panel visible; header persistente).
  - 3118464: conformidad diseno etapa 6.1 (Backlog kanban, Projects selector/launcher, entidad proyecto, PII render-safe, tokens).
  Evidencia final TASK-0132: npm test PASS 19 tests; node --check public/app.js src/server.js OK; smoke local 4176 OK.
- design/front_pipeline.html en Zeus-protocol ya estaba dirty antes de Codex; no tocar ni revertir.
- No editar personal/Arquitecto, personal/Analista ni personal/operador salvo instruccion explicita.
- Estado compartido solo via runtime/submit_intent.py; no editar manualmente Area_comun/state/*.json.
- No arrancar trabajo nuevo sin GO/mensaje ejecutable. Si el operador pide higiene, usar claim file-scoped y submit_intent.

Si aparece mensaje nuevo a Codex con requires_response:true y requested_action ejecutable,
procesarlo en sesion con claim file-scoped + submit_intent; no dejarlo solo como ACTION_REQUIRED.
```

## Comandos utiles

```powershell
git status --short
Get-ChildItem -File Area_comun\mailbox\open | Select-Object -ExpandProperty Name
python scripts\scan_encoding.py --root .
python scripts\scan_domain_neutrality.py --root .
python -c "from pathlib import Path; from runtime.protocol_replay import protocol_state_drift; import json; print(json.dumps(protocol_state_drift(Path('.')), indent=2, ensure_ascii=False))"
python scripts\validate_collaboration_state.py --root .
```
