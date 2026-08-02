---
task_id: TASK-0313
file: Area_comun/tasks/TASK-0313-front-worker-roster.md
title: "Front Zeus-protocol: formulario de alta de worker de producto (no-firmante) + enlace a LLM (SPEC-0115 / DECISION-0109 Nivel 1), off-by-default"
status: done
type: product
owner: Codex
reviewer: Analista
priority: normal
project: Zeus-protocol
spec_id: SPEC-0115
relates_to:
  - DECISION-0109
  - SPEC-0115
  - DECISION-0058
  - DECISION-0069
  - TASK-0178
  - REQ-ZEUS-001
created_at: 2026-08-02
intake:
  type: feature
  goal: >
    Implementar el P4a (Nivel 1) de TASK-0178 en el front Zeus-protocol: un formulario para dar de alta un WORKER
    DE PRODUCTO que NO escribe el ledger (patron Extractor/DECISION-0058), con su keypair, y enlazarlo a un LLM
    (provider/endpoint/modelo). Builder server-side, keyless (DECISION-0069), off-by-default, roster FUERA del
    config pinned. NO cubre Nivel 2 (agente de gobernanza que firma = ceremonia re-genesis, runbook P4b). Codigo
    solo en Zeus-protocol; hub/#4 no se toca.
  acceptance:
    - "AC1 (formulario): alta de worker de producto (id, provider, endpoint, modelo, capacidades de producto) con preview dry_run + confirm (sin confirm -> 409). Detras de flag OFF-BY-DEFAULT (fuera del config pinned)."
    - "AC2 (compose server-side + anti-injection): al confirmar, el SERVIDOR escribe la entrada canonica del roster (fuera del config pinned) desde campos validados; el cliente NO inyecta entrada cruda/actor/firma. Negativa PERMANENTE: forma/campo ajeno o intento de firmar/tocar el ledger por esta via -> RECHAZADO (patron 0052)."
    - "AC3 (frontera keyless, DECISION-0069): el worker es keyless respecto al ledger; su alta NO le da capacidad de firmar/cerrar estado; si intenta escribir el ledger -> falla cerrado (guard TASK-0213)."
    - "AC4 (enlace a LLM): la entrada guarda su config de LLM (provider/endpoint/modelo) en el roster fuera del config pinned; editable/removible por el formulario."
    - "AC5 (frontera Nivel 2): el formulario NO da de alta un agente de gobernanza que firma el ledger (eso es ceremonia re-genesis, runbook P4b). A lo sumo recoge datos + marca ceremonia pendiente; el flip NO ocurre por el formulario."
    - "AC6 (fondo intocable + gates): #4 del hub byte-identico (drift 0); protocol.config.json + agent_registry SIN tocar; codigo solo en Zeus-protocol; npm test exit 0 en clon limpio; con flag off el formulario/endpoint es inerte (403)."
  verification_cmd:
    - "cd D:/Agentes/Zeus/Zeus-protocol && npm test"
  scope_routes:
    - src/server.js
    - public/app.js
    - public/index.html
    - public/styles.css
    - tests/staticContract.test.js
  out_of_scope: >
    Alta de agente de gobernanza/firmante (Nivel 2 = ceremonia re-genesis, runbook P4b); ejecutar/correr el
    worker; cambios en hub/#4/agent_registry/genesis; nuevo INTENT_TYPES; shell/arbitrario.
  risk: medium
  estimate: M
notes: >
  P4a (Nivel 1) de TASK-0178, gobernado por DECISION-0109 (accepted via meta del operador) + SPEC-0115. Repo de
  producto Zeus-protocol. El corazon es el builder server-side + la frontera keyless (el worker NO firma el
  ledger) + la frontera Nivel 2 (un firmante es ceremonia, no formulario). Off-by-default. Gate maker != checker:
  Analista + Arquitecto verifican builder server-side, keyless-no-firma, frontera Nivel 2, off-by-default. Sin
  browser -> por contrato + fixtures.
