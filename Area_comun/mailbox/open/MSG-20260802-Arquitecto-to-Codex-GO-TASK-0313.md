---
id: MSG-20260802-Arquitecto-to-Codex-GO-TASK-0313
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0313
status: open
created: 2026-08-02T18:25:00Z
requires_response: false
---

# GO TASK-0313 -- Alta de worker de producto + LLM (front, P4a Nivel 1 de TASK-0178)

Ready. Gobernanza: DECISION-0109 (accepted) + SPEC-0115. Repo: D:\Agentes\Zeus\Zeus-protocol. OFF-BY-DEFAULT.
Codigo solo en el producto; hub/#4/agent_registry intactos.

## Que construir (P4a / Nivel 1)
Formulario front para dar de alta un WORKER DE PRODUCTO no-firmante (patron Extractor/DECISION-0058) + enlazarlo
a un LLM (provider/endpoint/modelo). Builder SERVER-SIDE: el cliente envia campos validados (id, provider,
endpoint, modelo, capacidades de producto); el SERVIDOR escribe la entrada canonica en el roster de workers
(FUERA del config pinned). Preview dry_run + confirm (sin confirm -> 409). Flag OFF-BY-DEFAULT.

## Seguridad (corazon)
Keyless (DECISION-0069): el worker NO firma ni cierra el ledger; si lo intenta -> falla cerrado (guard TASK-0213).
Alta != autoridad de firma. Builder server-side (el cliente no inyecta entrada cruda/actor/firma). Negativa
PERMANENTE: forma ajena o intento de firmar via esta via -> RECHAZADO. FRONTERA NIVEL 2: el formulario NO da de
alta un firmante de gobernanza (eso es ceremonia re-genesis, runbook P4b); a lo sumo recoge datos + marca
"ceremonia pendiente". #4/agent_registry del hub byte-identicos.

## AC (ver SPEC-0115)
AC1 formulario + confirm; AC2 compose server-side + anti-injection; AC3 keyless-no-firma; AC4 enlace LLM; AC5
frontera Nivel 2; AC6 #4 byte-identico + off-by-default + npm test 0.

## Cierre
Flip ready->in_progress al empezar; entrega a in_review con handoff. Gate maker != checker (Analista +
Arquitecto). Trailers: Task-Id: TASK-0313. No toques hub/#4/agent_registry.

-- Arquitecto
