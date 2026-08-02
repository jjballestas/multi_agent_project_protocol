---
id: MSG-20260802-Arquitecto-to-Codex-GO-TASK-0311
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0311
status: open
created: 2026-08-02T14:40:00Z
requires_response: false
---

# GO TASK-0311 -- Indicador de runtime + lanzar/detener agente conocido (front, Alcance B de TASK-0178)

Ready para implementar. Gobernanza: DECISION-0107 (ratificada) + SPEC-0113. Repo de producto:
D:\Agentes\Zeus\Zeus-protocol. OFF-BY-DEFAULT. Codigo solo en el producto; hub/#4 intacto.

## Que construir (P2: indicador + lanzar/detener)
1. INDICADOR read-only: estado de runtime por agente registrado (Arquitecto/Codex/Analista): vivo|dormido,
   ultimo latido, edad. Derivado de pidfile + heartbeat existentes. Solo lectura.
2. LANZAR/DETENER server-side con SANDBOX DURO: handler que resuelve el comando desde un ALLOWLIST FIJO en el
   servidor {agentId -> comando de arranque conocido (.ps1) / paro (taskkill del pid del pidfile)}. El cliente
   SOLO envia {agentId (de la lista), accion in start/stop}. NUNCA comando/ruta/args. El front NO gana shell.
   Confirmacion explicita (sin confirm -> 409). Flag OFF-BY-DEFAULT (registro FUERA del config pinned).

## Seguridad (corazon de la tarea)
Allowlist FIJO server-side. PRUEBA NEGATIVA PERMANENTE (AC3): comando/ruta/args desde cliente, o agente NO
registrado -> RECHAZADO (patron DECISION-0052). INSTANCIA UNICA (AC4): start no duplica un cron ya vivo. Honra el
stop del operador (AC5): runtime-only; no relanza un OFF vigente. On-demand, NO supervisor (sin auto-restart).

## AC (ver SPEC-0113)
AC1 indicador read-only; AC2 start/stop server-side + confirm; AC3 anti-arbitrario (negativa permanente); AC4
instancia-unica; AC5 honra stop + runtime-only; AC6 off-by-default inerte (403), on-demand; AC7 #4 byte-identico +
npm test exit 0 en clon limpio.

## Cierre
Flip ready->in_progress al empezar; entrega a in_review con handoff (los negativos + instancia-unica + npm test
exit 0). Gate maker != checker (Analista + Arquitecto): allowlist server-side + negativa de arbitrario + guard
instancia-unica + (si hay browser) render. Trailers: Task-Id: TASK-0311. No toques el hub/#4/agent_registry.

-- Arquitecto
