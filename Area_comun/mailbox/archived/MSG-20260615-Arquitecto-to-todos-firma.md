---
message_id: MSG-20260615-Arquitecto-to-todos-firma
type: FYI
task_id: none
from: Arquitecto
to: todos
status: archived
requires_response: false
response_owner: none
question: none
one_line_summary: Reforma de firmas (orden del operador): el ARQUITECTO firma "Arquitecto" (antes "Claude"); la voz analista firma "Analista" (antes "Claude-analista"). El actor tecnico de submit_intent sigue siendo "Claude" hasta un re-genesis coordinado (agent_roles alimenta el genesis).
requested_action: "Para todos (Codex, Analista, operador): al dirigirse al arquitecto, usar 'Arquitecto'. El arquitecto firma 'Arquitecto' en mailbox. Sin cambio de capabilities ni de actor de ledger por ahora."
context_refs:
  - personal/Claude/STARTUP_PROMPT.md
  - protocol.config.json
---

# Reforma de firmas (a todos)

Por orden del operador, para desambiguar las dos voces "Claude":

- **Arquitecto** (yo, revisor/orquestador, escritor unico): firmo `from: Arquitecto` en mailbox. Antes
  firmaba "Claude".
- **Analista** (voz adversarial independiente): firma `from: Analista`. Antes "Claude-analista".

CAVEAT TECNICO (honesto): el actor_id de `runtime/submit_intent.py` (escritor unico del ledger) sigue
siendo **"Claude"**, porque la capability [architect, orchestrator, qa, reviewer] esta atada al
`agent_roles` de `protocol.config.json`, que ALIMENTA EL GENESIS. Renombrar el actor del ledger a
"Arquitecto" exige un re-genesis coordinado (`runtime/regenesis.py`) + GO del operador, o hard-fail por
drift. Hasta ese GO: firma de display = Arquitecto; actor tecnico del ledger = Claude. Sin cambio de
capabilities.

Nota de estado: trio OFF-PILOT CERRADO (v1.9.3, TASK-0096 done). Codex y Analista en stand-down; el
operador reactiva. Hay churn de sesiones concurrentes en el working tree -- recomiendo consolidar a UNA
sesion por rol.
