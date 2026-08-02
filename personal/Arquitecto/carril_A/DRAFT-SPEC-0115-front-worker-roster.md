---
spec_id: SPEC-0115
title: Front Zeus-protocol: formulario de alta de WORKER DE PRODUCTO (no-firmante) + enlace a LLM (Nivel 1 / P4a de TASK-0178), off-by-default
status: draft
owner: Codex
decision: DECISION-0109
relates_to: [DECISION-0109, DECISION-0058, DECISION-0069, DECISION-0107, TASK-0178, REQ-ZEUS-001]
project: Zeus-protocol
date: 2026-08-02
file: Area_comun/specs/SPEC-0115-front-worker-roster.md
---

# SPEC-0115 -- Alta de worker de producto + enlace a LLM (front Zeus-protocol, P4a / Nivel 1)

Operacionaliza DECISION-0109 Nivel 1. El operador da de alta desde el front un WORKER DE PRODUCTO que NO escribe
el ledger (patron Extractor / DECISION-0058), con su propio keypair, y lo enlaza a un LLM (provider/endpoint/
modelo). Off-by-default. Roster FUERA del config pinned. Core neutral (codigo solo en Zeus-protocol; hub/#4 intacto).
NO cubre el Nivel 2 (agente de gobernanza que firma = ceremonia de re-genesis, P4b runbook).

## Arquitectura (hereda 0051/0052/0058/0069)
- **Builder SERVER-SIDE, forma estricta:** el front compone la entrada del roster de workers desde CAMPOS
  validados; el cliente no inyecta forma cruda ni firma. Off-by-default; el roster vive FUERA de protocol.config.json
  (patron extractors.config.json).
- **Keyless / no-firmante (DECISION-0069):** el worker tiene su propio keypair para su trabajo de PRODUCTO, pero
  es keyless respecto al ledger: NO firma ni cierra estado gobernado (guard V2, TASK-0213). Alta != autoridad de firma.

## Criterios de aceptacion
- **AC1 (formulario de alta):** el front tiene un formulario para registrar un worker de producto: campos id,
  provider, endpoint, modelo, capacidades de PRODUCTO. Preview (dry_run) + confirm (sin confirm -> 409). Detras de
  un flag OFF-BY-DEFAULT (fuera del config pinned).
- **AC2 (compose server-side + anti-injection):** al confirmar, el SERVIDOR escribe la entrada canonica en el
  roster de workers (fuera del config pinned) desde los campos validados. El cliente NO inyecta la entrada cruda,
  ni actor, ni nada de firma. Prueba negativa PERMANENTE: forma/campo ajeno o intento de firmar/tocar el ledger
  por esta via -> RECHAZADO (patron 0052).
- **AC3 (frontera keyless, DECISION-0069):** el worker registrado es keyless respecto al ledger; su alta NO le da
  capacidad de firmar/cerrar estado gobernado; si intenta escribir el ledger -> falla cerrado (guard TASK-0213).
  Su trabajo de producto lo verifica y firma un jefe firmante.
- **AC4 (enlace a LLM):** la entrada del worker guarda su config de LLM (provider/endpoint/modelo, p.ej. otro
  local-vlm u Ollama), en el roster fuera del config pinned. Editable/removible por el mismo formulario.
- **AC5 (frontera Nivel 2):** el formulario NO da de alta un agente de gobernanza que firma el ledger (eso es
  ceremonia de re-genesis, P4b runbook). Si el operador pide un firmante, el front a lo sumo recoge datos y marca
  "ceremonia pendiente"; el flip NO ocurre por este formulario.
- **AC6 (fondo intocable + gates):** #4 del hub byte-identico (drift 0); protocol.config.json + agent_registry
  SIN tocar; codigo solo en Zeus-protocol; npm test exit 0 en clon limpio; con flag off el formulario/endpoint es
  inerte (403).

## Alcance de archivos (Zeus-protocol)
- IN: src (endpoint + builder server-side del roster de workers + validacion), public (formulario UI + preview +
  confirm), registro del roster + flag fuera del config pinned, tests (contrato + negativa anti-injection +
  keyless-no-firma + off-by-default).
- OUT: alta de agente de gobernanza/firmante (Nivel 2 = ceremonia); ejecutar/correr el worker; cambios en hub/#4/
  agent_registry/genesis; nuevo INTENT_TYPES.

## Test plan
- Negativa: entrada cruda/campo ajeno desde cliente -> RECHAZADO; intento de firmar/escribir ledger via worker
  keyless -> falla cerrado; sin confirm -> 409; flag off -> inerte.
- Positiva: alta valida -> entrada canonica en el roster (fuera del config pinned) con su LLM config; edicion/baja.
- #4 byte-identico antes/despues; npm test exit 0 clon limpio. Sin browser -> contrato + fixtures.

## DoD
AC1-AC6; off-by-default; anti-injection + keyless probados (negativa permanente); frontera Nivel 2 respetada;
#4 intacto; core neutral; gate maker != checker (Analista + Arquitecto): builder server-side, keyless-no-firma,
frontera Nivel 2, off-by-default. Cierre gobernado.
