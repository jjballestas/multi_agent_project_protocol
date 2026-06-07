# Session report - Release v1.0.0 (primer release estable: metodologia distribuible)

- Date: 2026-06-07
- Phase: P2
- Process status: closed
- Ratification: ratified by human (RELEASE v1.0 aprobado expresamente por el operador 2026-06-07) +
  ratified by agents (cada tarea ratificada adversarialmente por Claude; suite golden 28/28 verde)

## 1. In One Sentence

Se publica **v1.0.0**, primer release estable que consolida la metodologia como **producto distribuible**:
contrato de coordinacion + motor runtime N-agente + capa de seguridad/guardrails + wrapper LLM real +
track de adopcion/distribucion, de forma aditiva y neutral de dominio.

## 2. What Was Done

Promocion del protocolo a `1.0.0` (hito de estabilizacion, aprobacion humana per DECISION-0001). Cada pieza
incluida ya fue ratificada adversarialmente por el arquitecto en su cierre. El empaquetado:
- `protocol_version`: 0.10.0 -> **1.0.0** en `protocol.config.json` (el template conserva el placeholder).
- `PROJECT_STATE.json`: `version` 1.0.0 + `released_versions` += `v1.0.0`.
- `CHANGELOG.md`: nueva seccion `[1.0.0]`.
- `AGENTS.md`: Released version -> v1.0.0.
- Tag git `v1.0.0`.

## 3. Alcance incluido (todo DONE y ratificado)

- **Motor (D0) cerrado:** observabilidad N-agente trace_id/spans/summarize_nagent (TASK-0059) + budget/
  deadline A10 (TASK-0060), config-gated y byte-equivalente en off.
- **Seguridad/guardrails (Fase 5):** anti-inyeccion invariante G1 (TASK-0054), tool-policy deny-by-default
  (TASK-0056), firma del envelope / event-auth HMAC (TASK-0057).
- **Wrapper LLM real:** adapter CLI vendor-neutral (presets claude/codex) off-by-default, sin secretos, NO
  autonomia (DECISION-0021, TASK-0062).
- **Distribucion (D2) completa:** tiers coordination/runtime (DECISION-0019, TASK-0058), upgrade tier-aware +
  runtime_version (TASK-0061), docs de adopcion (TASK-0063), versionado del paquete PACKAGE_VERSIONING /
  D2.4 (TASK-0064).
- **Regla anti-colision (DECISION-0020):** formalizada + propagada a AGENTS.md/.template sec.7 + TASK_PROTOCOL.
- **Higiene del prune (SPEC-0051, TASK-0065):** condensa next_actions config-gated, determinista e
  idempotente; cierra el FOLLOW-UP de Capa A.
- **Reporte de inventario HTML** para el operador.

## 4. Quality gates

- Golden runners (python): **28/28 verde**.
- Validador colaboracion py + minimal_instance: verde (solo warnings benignos de FYIs sin requires_response).
- Encoding scan py: limpio. Neutralidad py: exit 0. Prune --check: ok.
- Sin secretos. Neutralidad de dominio intacta.

## 5. Decisions

- DECISION-0020 (ACCEPTED): regla anti-colision para escritura concurrente del ledger (HALLAZGOS #1/#2/#3).
- DECISION-0021 (ACCEPTED, previa): activacion del wrapper LLM real, off-by-default/gateada.

## 6. Pendientes gateados (post-v1.0)

- **Fase B** (SPEC-0039): event-log writer-vivo del **estado del protocolo** (DECISION-0017). ARRANCANDO por
  instruccion del operador (2026-06-07).
- **TASK-0038** (paraguas N-agente): brechas de spec-completa de SPEC-0038. ARRANCANDO por instruccion del
  operador (2026-06-07).
- Fase 7 (release engineering: SBOM/provenance) y autonomia supervisada: siguen gateadas.

## 7. Ratification

Release aprobado por el operador humano (2026-06-07). Codex ratifica el reporte.
