---
decision_id: DECISION-0025
title: Integracion con Agent Teams (Anthropic) via bridge de hooks - Capas A+B (off-by-default, opt-in, neutral)
status: accepted
date: 2026-06-08
ratified_at: 2026-06-08
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0009, DECISION-0017, DECISION-0018, DECISION-0020, DECISION-0021, DECISION-0022, DECISION-0024]
phase: P2
---

# DECISION-0025 - Integracion con Agent Teams via bridge de hooks (Capas A+B)

> ACCEPTED por el operador (2026-06-08), alcance limitado a **Capas A+B** (gate enforcement + audit
> append-only), en **modo sombra** (aditivo, off-by-default, drift benigno). La **Capa C** (mapeo
> autoritativo del ledger) queda **DIFERIDA** a las precondiciones de DECISION-0022. Aprobar esta
> politica NO enciende nada: encender exige claim + implementacion (Codex) + ratificacion (Claude) +
> registro de activacion por instancia. Borrador de diseno del operador:
> `personal/operador/DRAFT-integracion-agent-teams-bridge.md`.

## Contexto

Anthropic distribuye **Agent Teams** (en Claude Code, experimental, off por defecto): un lead que
coordina teammates, cada uno con su contexto, con lista de tareas compartida + claim con file-lock +
mailbox + hooks (`TaskCreated`, `TaskCompleted`, `TeammateIdle`). Es convergente con las primitivas
de este protocolo (lead/teammates, claim como lock, mailbox, gates por turno).

Diferencia clave: Agent Teams guarda su estado en `~/.claude/tasks/{team}/` (efimero, "no editar a
mano", sin resumption de teammates, IDs propios, estados pending/in_progress/completed). Este
protocolo es el ledger **durable, auditable, versionado en git y cross-vendor** (TASK-XXXX, estados
+ SDD, event-sourced). `runtime/submit_intent.py` ya rechaza escrituras que no cumplan
actor+capability, `from`-status valido y claim activo que cubra el scope (gate B.3, DECISION-0022).

Posicionamiento: NO competimos en la capa de coordinacion en vivo (Anthropic la provee mejor y
gratis). El valor defendible es gobernanza/auditoria/cross-vendor/reproducibilidad. Por tanto
**Agent Teams = motor de ejecucion en vivo; este protocolo = ledger encima.** El puente son los
hooks, que reusan los mecanismos existentes.

## Lo que YA existe (no se reconstruye; se compone)

`submit_intent`/`submit_intents` (transaccional + dedup por idempotency_key + rollback), gate B.3,
genesis content-addressed/regenesis, event log + snapshots (DECISION-0017), validadores
(`validate_collaboration_state.py`), scan de neutralidad (`scan_domain_neutrality.py`),
`turn_validate.py`, tool-policy/guardrails/budget. El bridge **reusa todo esto**; solo traduce
eventos de Agent Teams hacia estos mecanismos.

## Decision

**La integracion se distribuye OFF y su activacion es opt-in, por capas, gateada y registrada por
instancia.** El motor en vivo nunca es escritor autoritativo del ledger rico; la autoridad sigue en
`submit_intent` (DECISION-0022 intacta). **Alcance aprobado en esta decision: Capas A y B.**

1. **Off por defecto.** Nuevo bloque `runtime.team_bridge`
   `{enabled:false, layers:[], activation_decision:"", approved_by:"", approved_at:""}`. Sin registro
   valido, una instancia se comporta exactamente como hoy (byte-equivalente).

2. **Capas aprobadas (activables de menor a mayor riesgo):**
   - **A - Gate enforcement (recomendada primero):** los hooks `TaskCompleted`/`TeammateIdle` corren
     los gates existentes (validador + neutralidad [+ `turn_validate` si aplica]) y hacen `exit 2` si
     fallan, de modo que Agent Teams **bloquea** el cierre / mantiene al teammate. No mapea estado;
     extiende los guardrails a cualquier teammate. Riesgo casi nulo.
   - **B - Audit bridge (append-only):** cada evento se anexa a un journal durable
     (`Area_comun/state/team_audit.jsonl`) sin mutar el estado canonico. Rastro auditable, resumible
     en frio desde git. Cubre la limitacion de Agent Teams de "sin resumption / status rezagado".

3. **Capa C - DIFERIDA (no aprobada en esta decision).** El mapeo autoritativo del ledger
   (subject `[TASK-XXXX]` + claim pre-adquirido -> `submit_intent`) queda fuera de alcance hasta
   cumplir la **precondicion dura de DECISION-0022**: ambos loops ya rutean toda transicion por
   `submit_intent` + aprobacion del operador + rollback ensayado. Activar C exige una decision/registro
   adicional. Hasta entonces el bridge en C **degrada a Capa B** (solo audita) y nunca revienta el team.

4. **Idempotencia y fail-closed.** El bridge es idempotente (dedup de `submit_intent` cuando aplique)
   y **nunca debe reventar el team**: ante error de escritura del ledger degrada a audit + notifica
   (consistente con DECISION-0018). Hooks corren en la maquina del lead.

5. **Neutralidad y secretos (AGENTS.md sec.4).** `runtime/team_bridge.py` es tooling neutral: se anade
   a `scan_globs` de neutralidad; no introduce terminos de dominio; sin secretos commiteados.

6. **Reversibilidad.** Apagar = `team_bridge.enabled=false` (o quitar el registro): comportamiento
   actual restaurado, sin migracion retroactiva.

## Versionado y neutralidad (DECISION-0001)

- Aditivo, off-by-default, opt-in, reversible, neutral de dominio => **MINOR**. Mantiene boundaries
  "no secretos" y "aprobacion humana para cambios de boundary".

## Alternativas descartadas

- **Agent Teams como escritor autoritativo directo del ledger:** RECHAZADA (viola gate B.3 /
  DECISION-0022; genera drift).
- **Reimplementar mensajeria/paralelismo en vivo propios:** RECHAZADA (Anthropic ya lo provee mejor y
  gratis; duplicar es reinventar la rueda sin valor diferencial).
- **Mapeo 1:1 automatico sin convencion ni claim:** RECHAZADA (no satisface capability/`from`/claim).
- **Encender Capa C sin precondiciones 0022:** RECHAZADA (rompe el peer loop al primer edit manual);
  por eso C queda diferida en esta decision.

## Aprobacion humana

Otorgada por el operador (2026-06-08) para **Capas A+B** por ser cambio de boundary (AGENTS.md sec.4) y
de compatibilidad de protocolo (CLAUDE.md sec.2). Aprobar la politica NO enciende nada; la activacion
real en la instancia viva es un paso separado registrado en `runtime.team_bridge`.

## Plan de adopcion (post-decision)

- [x] Aprobacion del operador a Capas A+B (2026-06-08).
- [ ] **TASK-0083 / SPEC-0065 (Codex):** implementar `runtime/team_bridge.py` (Capas A+B) + tests
      (recorded fixtures de payloads de hook) + alta en `scan_globs` + bloque `runtime.team_bridge` en
      `protocol.config.template.json` (master) y la instancia viva, off-by-default. Claude revisa
      (adversarial).
- [ ] Activar A+B en la instancia viva (audit + gates) como paso separado registrado. Medir.
- [ ] Capa C: decision/registro adicional solo tras cumplir precondiciones DECISION-0022.
