---
id: TASK-0044
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0043]
relates_to: [TASK-0042]
phase: P2
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0015, DECISION-0009, DECISION-0001]
execution_pipeline: [event log append-only JSONL con seq monotono asignado SOLO por el writer + event_schema_version + append atomico (tmp+rename, torn-write safe), aggregate_version por-tarea + idempotency_key por intent (tupla actor/task/transition/attempt/fencing) con dedupe en el writer, claims con lease_until + fencing_token monotono por-aggregate (rechazo de fencing menor registrado), snapshot derivado + compactacion por rango de seq + invariante validador hot==log+snapshot en up_to_seq, golden examples/runtime_eventlog_cases con simulacion de concurrencia y negative replay test]
acceptance_criteria: [seq estrictamente creciente asignado por el writer; append atomico ignora lineas truncadas; aggregate_version por-tarea evita falsos conflictos; idempotency_key duplicado => no-op/exito sin segunda mutacion (incl. cruzando compactacion); lease vencido reclamable por otro con fencing mayor y reporte tardio con fencing menor rechazado (aunque aggregate_version coincida); snapshot reconstruible desde log+snapshot en up_to_seq (mismatch = hard-fail); negative replay test (adapter/tool/red/reloj falso que falla si se invoca) pasa con mismo hash canonico; fallback N=2 y suite runtime previa intactos; sin red]
test_plan: [examples/runtime_eventlog_cases: seq/append-atomico/torn-write; idempotencia duplicada (pre y post compactacion); claim simultaneo + lease vencido + fencing obsoleto; replay reconstruye snapshot (hash) + negative replay; regresion suite runtime verde]
closure_criteria: [event log append-only (seq writer-only + schema version + append atomico) + aggregate_version/idempotency + lease/fencing por-aggregate + snapshot/compactacion + invariante validador + negative replay test; golden verdes; fallback N=2 sin regresion; neutralidad limpia; handoff autocontenido; claim liberado al pasar a in_review]
---

# TASK-0044 - N-agente Fase 2: event log + leases/fencing + idempotencia por-aggregate

> `implementation` -> SDD; implementar contra **SPEC-0038 (congelada)** Fase 2 (sec.13) + addenda
> A3/A5/A6/A7 (gates duros). Segunda fase del runtime N-agente. Aditivo, config-gated, **fallback N=2
> intacto**. Es el corazon de la concurrencia segura para N escritores.

## Alcance (Fase 2)
- **Event log append-only** (D-7/D-11/A5): JSONL con `seq` entero estrictamente creciente **asignado solo
  por el writer**, `event_schema_version`, append atomico (tmp+rename o fsync; lector ignora lineas
  truncadas / torn-write safe). El snapshot (PROJECT_STATE/TASK_INDEX/CLAIMS) es **derivado**.
- **Concurrencia optimista por-aggregate** (D-2/A3): `aggregate_version` por-tarea (no global) +
  `idempotency_key` por intent (tupla `actor/task/transition/attempt/fencing`); duplicado => no-op/exito
  (dedupe en el writer), tambien cruzando compactacion.
- **Leases + fencing** (D-8/A7): claim con `lease_until` + `fencing_token` monotono **por-aggregate**;
  lease vencido => `expired` reclamable por otro elegible con fencing mayor; el writer **rechaza escritura
  con fencing menor** (aunque `aggregate_version` coincida) y registra el rechazo.
- **Snapshot + compactacion** (A5): regenerar snapshot por replay; persistir snapshot cada N eventos con
  `up_to_seq`; compactar el log por rango de `seq` sin borrar historia. **Invariante de validador:** estado
  caliente reproducible desde log+snapshot en `up_to_seq`; mismatch = hard-fail antes de escribir.
- **Negative replay test** (D-12/A6): adapter/tool/red/reloj falso que **falla si se invoca** durante el
  replay; el replay pasa y produce el **mismo hash canonico** de snapshot.

## No-alcance (fases posteriores)
- NO router por capacidad/fairness (Fase 3). NO maquina de estados Review/QA (Fase 4). La **firma/auth de
  eventos (A1/D-1)** aterriza aqui solo como el campo/seam del evento (HMAC local opcional); la politica de
  auth externa (OAuth/JWT) queda condicionada a agentes externos. NO romper N=2.

## Tests
- `examples/runtime_eventlog_cases/`: seq writer-only + append atomico + torn-write; idempotencia duplicada
  (pre/post compactacion); claim simultaneo + lease vencido + fencing obsoleto rechazado; replay
  reconstruye snapshot (hash canonico) + **negative replay**.
- Regresion: suite runtime previa verde; fallback N=2 intacto. Sin red.

## Dogfood
Liveness + handoff-release. ASCII-only en mailbox/state. Paridad .py/.ps1 solo si tocas un validador con
.ps1 (el invariante hot==log+snapshot puede requerir tocar el validador). Te ratifico adversarialmente con
foco en: seq monotono writer-only, idempotencia bajo reintento, fencing por-aggregate, y negative replay.
Si un punto exige decision de politica, `blocked` + 1 pregunta. **Tu area personal ahora es `personal/Codex/`.**
