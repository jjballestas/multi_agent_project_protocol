---
decision_id: DECISION-0031
title: Revision adversarial SOTA de SPEC-0078 - set de deltas corregido (context engineering)
status: accepted
date: 2026-06-13
ratified_at: 2026-06-13
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0030, DECISION-0008, DECISION-0022, DECISION-0017, DECISION-0009, DECISION-0024]
phase: P2
---

# DECISION-0031 - Revision adversarial SOTA de SPEC-0078 (set de deltas corregido)

> Estado: ACCEPTED (2026-06-13), ratificada por el operador. Reemite limpia el borrador previo (que vivia
> como artefacto, NO en el ledger). Deriva de la revision adversarial de 3 voces de TASK-0109
> (consolidado: `Area_comun/artifacts/ANALISIS-CONSOLIDADO-deltas-sota-spec-0078.md`).

## Contexto

Una sesion previa propuso 5 deltas a SPEC-0078 (compaction / tool-result clearing / sub-agentes) citando
papers SOTA. El operador detecto que DELTA-1 y DELTA-2 malinterpretaban sus fuentes y que varios numeros
no estaban verificados. Se corrio una **revision adversarial de 3 voces independientes** (maker != checker,
ninguna leyo a las otras durante la produccion):

- **Operador** (valor/riesgo): `VOZ-OPERADOR-revision-deltas-sota.md`
- **Claude-analista** (fuentes/SOTA): `ANALISTA-deltas-sota-spec-0078.md`
- **Codex** (factibilidad): `VOZ-CODEX-factibilidad-deltas-sota.md`

Las dos voces analiticas convergieron independientemente con la del operador. Consolidacion (deliverable de
TASK-0109): `Area_comun/artifacts/ANALISIS-CONSOLIDADO-deltas-sota-spec-0078.md`.

## Decision

Se aprueba SPEC-0078 con el **set de deltas CORREGIDO** integrado:

1. **DELTA-1 (umbral de degradacion) - REFORMULAR.** Quitar la atribucion a arXiv:2602.16284 (KV-cache;
   no aplica al runtime CLI). El mecanismo (warning + fallback) se conserva, pero el umbral se mide como
   `assembled_context_tokens` en `build_turn_context` y sus cortes salen de `measure_context_cost`
   baseline, no de cifras de papers.
2. **DELTA-2 (trigger de consolidacion) - REFORMULAR.** Quitar la atribucion a arXiv:2601.07190 (Focus es
   autonomo; no especifica "cada 10 tool calls"). Trigger determinista del runtime; cadencia provisional/
   tuneable; `overhead <5%` como **GATE MEDIDO** (no supuesto); consolidacion barata y **fuera del hot
   path** (sin LLM en caliente).
3. **DELTA-3 (edicion atomica) - DIFERIR.** Future Work (TASK-0107), off-by-default, FUERA de TASK-0106.
   Si algun dia entra, **exclusivamente via `submit_intent`** (nunca edicion directa del estado;
   DECISION-0022).
4. **DELTA-4 (limites de summary) - DECIDIR POR MEDICION.** No bajar a 1200 por cita (arXiv:2604.01707
   no-verificable; 450-1200 es guia). Decidir 2000 vs 1200 por medicion propia y justificar en SPEC-0078
   sec.2.5.
5. **DELTA-5 (GC-8/GC-9) - MANTENER.** Asertos **estructurales** + umbral **medido**, nunca numeros
   heredados.

## Reglas innegociables

- **Gate de medicion BLOQUEANTE (DECISION-0008):** ningun umbral/cadencia de DELTA-1/2/4 se congela en
  SPEC/AC/golden sin correr `measure_context_cost` baseline ANTES.
- **Escritor unico (DECISION-0022):** cualquier mutacion de estado auditable va por `submit_intent`. DELTA-3
  no es excepcion.
- **Neutralidad de dominio:** se RECHAZA toda deriva a Neo4j/Memgraph/graph-DB, LlamaIndex
  PropertyGraphIndex, o servicio de memoria persistente externo en el core.

## Alcance de TASK-0106 (minimo seguro)

Medicion del contexto ensamblado -> limites configurables off-by-default -> tool-result clearing con
referencias en `runlog` -> trigger determinista provisional -> GC-8/GC-9 estructurales. DELTA-3 difiere a
TASK-0107.

## Trazabilidad de fuentes

Verified 3-0 (patron): 2603.18718, 2502.12110, 2603.09619. Cifra no atribuible: 2602.16284, 2601.07190.
No-verificables: 2604.01707, 2603.10062, 2606.00610. Detalle en SPEC-0078 sec.11.

## Versionado y neutralidad (DECISION-0001)

Aditiva (deltas a una SPEC en draft + bloque `context_policy` off-by-default). La implementacion (TASK-0106)
sera MINOR al liberar. Nucleo neutral de dominio. Sin secretos.

## Consecuencias

- SPEC-0078 pasa a `accepted` con los deltas integrados y la trazabilidad de fuentes corregida.
- TASK-0106 se promueve a `ready` con handoff a Codex (subconjunto minimo seguro + gate de medicion).
- DELTA-3 reservado a TASK-0107 (futuro). DELTA-4 pendiente de justificacion por medicion antes del cierre.
