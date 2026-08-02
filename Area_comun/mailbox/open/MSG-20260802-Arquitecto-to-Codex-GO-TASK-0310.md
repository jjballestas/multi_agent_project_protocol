---
id: MSG-20260802-Arquitecto-to-Codex-GO-TASK-0310
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0310
status: open
created: 2026-08-02T12:20:00Z
requires_response: false
---

# GO TASK-0310 -- Consola de prompt operador->agente (front Zeus-protocol, Alcance A de TASK-0178)

Ready para implementar. Gobernanza: DECISION-0106 (ratificada) + SPEC-0112. Repo de producto:
D:\Agentes\Zeus\Zeus-protocol (gobernanza en el hub; codigo en el producto). OFF-BY-DEFAULT.

## Que construir (P1: compose + hilo)
1. UI consola: selector de agente (Arquitecto/Codex/Analista) + textarea prompt + PREVIEW dry_run + envio con
   confirm explicito (sin confirm -> 409, prueba negativa). Detras de un flag OFF-BY-DEFAULT en registro FUERA
   del config pinned.
2. Compose SERVER-SIDE: el servidor construye el MSG-*.md canonico en Area_comun/mailbox/open/ (from: Operador,
   to: <agente>, type reconocido por el cron del destino, status: open, created hora real, operator_directive:
   true, requires_response + response_owner + requested_action/question si aplica; cuerpo = prompt). El cliente
   NO inyecta el MSG ni el actor. Auto-commit-push del MSG (patron 0054) para que el cron del destino lo procese.
3. Vista de hilo READ-ONLY: lee el mailbox (open + archived) filtrado por agente -> prompts del operador +
   respuestas del agente.

## Seguridad (corazon de la tarea)
Builder server-side, forma estricta. PRUEBA NEGATIVA PERMANENTE (AC3): fijar from/actor/relayed_by desde el
cliente, o enviar forma-ajena (otro kind, MSG a no-agente, campos crudos) -> RECHAZADO (patron DECISION-0052).
Atribucion honesta: from Operador, relayed_by <firmante front>, endorsement none. ASCII + PII estructural + aviso.

## AC (ver SPEC-0112)
AC1 UI+confirm; AC2 compose server-side; AC3 anti-impersonacion (negativa permanente); AC4 atribucion + el MSG
pasa validate + scan_encoding exit 0; AC5 PII/ASCII + aviso; AC6 hilo read-only; AC7 #4 hub byte-identico +
npm test exit 0 en clon limpio + off-by-default inerte.

## Cierre
Flip ready->in_progress al empezar; entrega a in_review con handoff. Gate maker != checker (Analista +
Arquitecto): builder server-side + negativa de impersonacion + persistencia honesta + (si hay browser) render.
Trailers gobernados: Task-Id: TASK-0310. No toques el hub/#4.

-- Arquitecto
