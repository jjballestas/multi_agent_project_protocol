---
id: TASK-0101
owner: Codex
status: proposed
type: implementation
priority: high
created_at: 2026-06-12
updated_at: 2026-06-12
depends_on: []
relates_to: [DECISION-0029, DECISION-0017, DECISION-0022]
phase: P2
spec_id: SPEC-0070
linked_decisions: [DECISION-0029, DECISION-0017, DECISION-0022, DECISION-0028]
deliverables:
  - runtime/eventlog.py (prev_hash encadenado, off-by-default)
  - examples/golden cases de cadena (alteracion, borrado, reordenamiento detectados)
relevant_files:
  - runtime/eventlog.py
  - runtime/protocol_replay.py
  - protocol.config.json
blocked_by_questions: []
objective: (DECISION-0029 pieza 2a) Anadir encadenado prev_hash al eventlog - hash_n = SHA256(evento_n || hash_{n-1}) - manteniendo el HMAC actual como capa de compatibilidad. Flag propio off-by-default (p.ej. event_state.chain). Hoy la alteracion puntual es detectable (HMAC) pero borrado y reordenamiento NO rompen ninguna verificacion.
expected_output: (1) Campo prev_hash en cada evento bajo flag, genesis bien definido. (2) Verificador de cadena integrado en replay/validate que detecta alteracion, insercion, borrado y reordenamiento. (3) Golden cases que demuestran cada deteccion. (4) Migracion-compatibilidad - log existente sin prev_hash sigue validando en modo legacy; al activar el flag la cadena arranca con un evento ancla. (5) Validador, neutralidad y encoding verdes; sin secretos.
question_to_resolve: Q1 representacion del genesis (hash de protocol.config o constante declarada). Q2 interaccion con prune/archive (DECISION-0014) - como preservar la verificabilidad de la cadena cuando se podan eventos (hash de corte anclado en el archivo).
closure_criterion: prev_hash bajo flag off-by-default; verificador detecta las 4 manipulaciones en golden cases; modo legacy intacto; respuesta a Q2 documentada en la SPEC; handoff con evidencia.
sdd_required: true
---

# TASK-0101 - prev_hash encadenado en el eventlog (DECISION-0029 pieza 2a)

> PROPOSED (Claude 2026-06-12, habilitada por DECISION-0029 aprobada por el operador). Base de la cadena
> de atestacion: TASK-0102 y TASK-0103 dependen de esta. Promover a ready+GO cuando el operador lo
> indique y la SPEC este cerrada.

## Contexto

Ver DECISION-0029 (contexto y decision 2a). El eventlog actual (runtime v0.11.0) firma eventos con HMAC
simetrico y calcula canonical_hash de snapshots, sin encadenado entre eventos: el borrado o reordenamiento
selectivo de eventos no rompe ninguna verificacion. El encadenado es prerrequisito de la firma por agente
(TASK-0102) y del anclaje externo (TASK-0103).
