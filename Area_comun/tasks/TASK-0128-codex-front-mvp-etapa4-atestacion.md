---
id: TASK-0128
title: Proyecto-front MVP etapa 4 - Vista de atestacion #4 (timeline ledger + boundary T0 + sello pre-T0 + manifest), read-only (DECISION-0049 / SPEC-0086)
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0049, DECISION-0045, DECISION-0047]
created_at: 2026-06-20
---

# TASK-0128 - Proyecto-front MVP etapa 4 (Vista de atestacion #4)

## Objective

Prioridad del operador. Etapa 4 del MVP (SPEC-0086, RF-4 deeper), sobre etapas 1-3 (done). En
`D:\Agentes\Zeus\Zeus-protocol`, **vista READ-ONLY** del **ledger atestado #4**: timeline (seq, actor,
firma VERIFICADA por evento, prev_hash, anclaje) + estado del **boundary T0** + **sello pre-T0** + **manifest**
(`chain_manifest.json` + `pre_t0_provenance`). Diferenciador de tesis hecho visible. Riesgo cero (read-only,
no toca #4, no re-genesis, no agentes nuevos). maker=Codex, checker=Arquitecto.

## Insumo de diseno (design system, verificado por la Analista)

`D:\Agentes\Zeus\Zeus-protocol\design\interface` (commit Zeus-protocol **a445d59**): componentes `timeline`
(atestado), `badges` (3 estados ok/fallo/indeterminado), `canonical-indicator`, pantalla `ledger`. Tokens
dark-first. Citado por hash (insumo del SDD; el codigo/diseno vive en Zeus-protocol).

## Alcance (SPEC-0086 etapa 4, RF-4)

- SOLO LECTURA del canonico (objetos git/origin, NO el working tree). La verificacion de firma/cadena/
  anclaje del front DEBE coincidir con `validate_chain`/`validate_agent_signatures`/`verify_anchor` del
  runtime; el estado de drift == `protocol_state_drift`.
- **Honestidad de estado (criterio de aceptacion, nota Analista):** el `canonical-indicator` y los badges se
  **DERIVAN de la verificacion real**, NO verde estatico -> renderizar WORKING TREE/stale cuando no sea
  canonico o el replay no de exit 0; badge "indeterminado" cuando no se pueda verificar (sin secretos).
- **Guarda PII (DECISION-0040):** el payload de texto libre se muestra REDACTADO ("[redactado - PII de
  tercero]"); el export es PII-free. El front nunca expone PII de terceros.
- Boundary T0 / sello pre-T0 / manifest: mostrar estado (epoca del genesis, pre_t0_provenance sha + commit,
  chain_manifest). Sin escritura (read-only). Codigo solo en Zeus-protocol; CI verde; canal ASCII.

## DoD

SPEC-0086 AC3 (atestacion visible y CORRECTA == runtime), AC1/AC5 (read-only canonico), AC6 (neutralidad/
acoplamiento), AC7 (CI verde), AC9 (determinismo), AC10 (gates protocolo). maker=Codex/checker=Arquitecto;
sin tocar #4/config (epoca 1.14.0). Reporta a in_review con claim file-scoped + submit_intent.

## Verification

- CI del producto verde (node --test); la verificacion de atestacion del front coincide con el runtime
  (firma/cadena/anclaje/drift); el canonical-indicator/badges derivan del estado real (no estatico).
- `validate_collaboration_state.py --root .` (con y sin secretos) + scans del protocolo exit 0; drift 0.
