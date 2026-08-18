# PROMPT DE INICIO — Arquitecto — 2026-06-27 (post-flip A2, monitoreo dataset TFM)

Eres el **Arquitecto Orquestador** de `multi_agent_project_protocol` (D:\Agentes\multi_agent_project_protocol).
Arranca en frío leyendo: AGENTS.md, CLAUDE.md, `personal/Arquitecto/MEMORY.md` (bloque RESUME de arriba),
y `Area_comun/state/` (CLAIMS.json, mailbox/open/). Reglas vivas: #4 enforce/auth ON; submit_intent = único
escritor; minimal narration (DECISION-0038); maker≠checker; nunca forjar commits de Codex (Co-Authored-By).
Estoy autorizado a ejecutar comandos Bash sin pedir permiso.

## Estado vigente (verificar al arrancar)
- **HEAD 0ac27e3 PUSHED**, v1.14.0 (epoch pinned, DECISION-0047). validate exit 0 esperado.
- **FLIP A2 EJECUTADO EN VIVO**: el override `event-state.runtime.json` (gitignored, raíz del repo) está
  presente → todo `submit_intent` se firma **Ed25519** (no-repudio por agente). Rollback = borrar ese archivo.
- **Cola de trabajo VACÍA.** No arrancar trabajo nuevo sin GO del operador.

## Tarea en curso: MONITOREO DEL DATASET TFM
El operador pidió: *"monitorea el crecimiento del dataset (cuenta eventos ed25519 por agente) y avisa cuando
haya volumen para medir."*
- **Umbral (pre-registro v2.0 FROZEN, atestado #4): ≥500 eventos ed25519 + ≥2 agentes distintos firmando.**
- **Baseline al cerrar la sesión anterior: 3 ed25519, todos `Arquitecto` (el marcador del flip), 1 agente.**
- **AL REANUDAR: re-armar el monitor** (era un background de la sesión previa; el conteo persiste en el ledger).
  Comando para contar ahora:
  ```bash
  cd D:/Agentes/multi_agent_project_protocol
  cat > /tmp/count_ed25519.py <<'PY'
  import json
  ed=0; per={}
  for l in open("runtime/state/events.jsonl",encoding="utf-8"):
      l=l.strip()
      if not l: continue
      try: e=json.loads(l)
      except: continue
      aa=e.get("actor_auth",{}) or {}
      if aa.get("method")=="ed25519":
          ed+=1; a=e.get("actor","?"); per[a]=per.get(a,0)+1
  print(ed, len(per), per)
  PY
  python /tmp/count_ed25519.py
  ```
  Luego re-lanzar el background until-loop que dispara al cumplir ≥500 + ≥2 (ver MEMORY.md).
- **Validación pendiente importante:** el **primer turno ed25519 de Codex/Analista** confirma el cross-signing
  multi-agente en vivo. Si corren turnos y NO firman ed25519, revisar que su runtime vea el override
  (`EVENT_STATE_RUNTIME_CONFIG_PATH` o `event-state.runtime.json` en su root) y tengan su privada en
  `D:/Agentes/protocol-secrets`.
- **Cuando haya volumen:** correr HARNESS (TASK-0191) sobre una COPIA → comparar H1–H3 vs umbrales v2.0 → redactar.

## Realidad a comunicarle al operador
~500 eventos requiere actividad de coordinación real (probablemente varias sesiones) y que un 2º agente trabaje.
Decisión abierta: ¿conducir turnos activamente, esperar el flujo normal, o revisar el N del pre-registro
(cambio de umbral ⇒ pre-registro v2.x ANTES de mirar resultados)?

## Parqueado (no tocar sin GO)
- Hermes UI (DECISION-0064, post-TFM). FLOOR skills Fase 1 (completa). Consola Arquitecto (completa).
- Operador: push de Zeus-protocol al remote (lo bloquea el clasificador; acción del operador).
