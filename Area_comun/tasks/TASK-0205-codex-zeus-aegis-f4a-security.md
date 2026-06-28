---
task_id: TASK-0205
title: "Zeus-Aegis F4a - endurecimiento del panel read-only: auth token + path-traversal + rate-limit en /api/governance/* + tests e2e del puente (DECISION-0064 F4.1/F4.2)"
type: integration
status: in_review
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0107
created_at: 2026-06-27
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064, DECISION-0040]
file: Area_comun/tasks/TASK-0205-codex-zeus-aegis-f4a-security.md
---

# TASK-0205 - F4a endurecimiento (seguridad + e2e del panel read-only)

> maker=Codex / checker=Arquitecto. Repo PRODUCTO Zeus-Aegis. Endurece el panel read-only ya construido (F1+F3).
> SOLO LECTURA (F2 sigue gateado post-TFM). NO tocar core protocolo, #4, baseline. Genera dataset elegible.

## Alcance (F4.1 seguridad read-only + F4.2 e2e)

- **Auth:** proteger `/api/governance/*` con un token (env `GOVERNANCE_API_TOKEN`/`HERMES_API_TOKEN`): si el token
  esta configurado, exigir bearer; si no esta configurado, modo local abierto (documentado). 401 sin/mal token.
- **Path-traversal:** confirmar/forzar que ningun parametro (proyecto, query, id) permita salir del root canonico
  ni leer fuera de Area_comun (los reads ya van por git show; blindar contra `..`, rutas absolutas, refs raras).
- **Rate-limit:** limite basico por IP/token en los endpoints governance (defensa DoS read).
- **Tests e2e del puente:** prueba e2e que arranca el server y verifica que `/api/governance/{health,state,backlog,
  mailbox,decisions,handoffs,ledger,artifacts,projects,metrics}` responden read-only desde el canonico, que 401 sin
  token cuando esta configurado, y que NO existe ruta de escritura (negativo e2e).

## DoD

- AC1 token: con token configurado, 401 sin/mal bearer; 200 con bearer valido; sin token configurado, modo local.
- AC2 path-traversal: payloads con `..`/rutas absolutas/refs invalidas rechazados; nunca lee fuera de Area_comun.
- AC3 rate-limit basico aplica en governance.
- AC4 test e2e del puente (todos los endpoints read-only + 401 + negativo de escritura) verde.
- AC5 gate F0 npm test exit 0 estable; core protocolo intacto; PII por construccion intacta; handoff a Arquitecto.

## Nota

- F4.3 (versionado/CHANGELOG del fork) y F4.4 (DECISION final) van al final, junto con F2. F2 (Operate) sigue
  gateado post-TFM (se desbloquea al cerrar la ventana de 500).
- Commit como Arquitecto con Co-Authored-By Codex. Minimal narration. Bloqueo -> blocked + una pregunta.
- POLITICA: el Arquitecto actualiza Zeus-Aegis/pipeline.html tras cerrar este caso.
