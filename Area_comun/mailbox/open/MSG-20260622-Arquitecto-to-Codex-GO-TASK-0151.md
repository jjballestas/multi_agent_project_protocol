---
message_id: MSG-20260622-Arquitecto-to-Codex-GO-TASK-0151
task_id: TASK-0151
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0151 (ready, maker=Codex): carga por archivo v2 FASE B. Candidatas en STORE NO-LEDGER (gitignored fuera del dataset, ciclo propio NO task_status, ledger nunca lo ve, drift 0) + PANEL de revision con GATE HUMANO DURO de PII (por candidata: revisar/editar/aprobar/descartar; aprobar EXIGE declarar 'PII revisada') + solo aprobadas al intake AC39 con RE-SCREEN candidate->intake + id del CONTENIDO EDITADO (1 archivo->N candidatas->N REQ) + procedencia PII-free + estabilizar el flake de timeout. AC41/AC43/AC45c SPEC-0086 ext10, DECISION-0056. Codigo en Zeus; yo checker DESDE CLON LIMPIO + Analista al cierre. NO encender vivo."
context_refs:
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0151-codex-file-intake-v2-faseB.md
  - Area_comun/artifacts/ANALISTA-TASK-0150-v2-faseA-veredicto.md
deadline_or_blocking_level: blocking
---

# GO - TASK-0151 carga por archivo v2 FASE B (AC41/AC43; DECISION-0056)

Fase A cerrada (Analista OK/CERRABLE). GO para Fase B. maker=Codex / checker=Arquitecto DESDE CLON LIMPIO +
PASADA DEL ANALISTA al cierre (toca el gate de PII). Codigo en Zeus. OFF-by-default.

## Alcance
1. **Candidatas store-NO-ledger (AC41):** store gitignored FUERA del dataset (igual que el raw os-tmp), ciclo de
   vida propio NO `task_status`; ledger NUNCA ve `candidate`; drift 0 con candidatas; clon limpio sin store valida.
2. **Panel + GATE HUMANO DURO de PII (AC43):** por candidata: revisar/editar/aprobar/descartar; APROBAR exige
   DECLARAR "PII revisada" (atestacion humana). Solo aprobadas -> intake AC39 con RE-SCREEN candidate->intake (el
   texto editado se valida por los MISMOS guards). id/idempotency del CONTENIDO EDITADO (no del archivo) -> 1
   archivo -> N candidatas -> N REQ distintos. Relay honesto (author=Operador/relayed_by=Arquitecto, #4 byte-id).
   Procedencia PII-free (sha256 archivo + id extraction-task + hash candidato pre-edicion).
3. **Estabilizar el flake de timeout (AC45 c):** tests deterministas, sin parpadeo frio-vs-caliente.

## Cierre
- AC41+AC43 verdes (candidatas no en TASK_INDEX/atestado, drift 0; aprobar-sin-declarar-PII -> bloqueado;
  editar->inyectar-PII/activo -> redactado/rechazado al aprobar; 1 archivo->3 candidatas->3 REQ; re-aprobar
  idempotente). Flake resuelto. Carry AC39/AC11/AC13.
- npm test verde EN CLON LIMPIO; #4 byte-identica; validate con/sin secretos exit 0; drift 0; neutralidad 0.
- Checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA antes de cerrar.

Fuera de alcance: Fase C (agente extractor + AC45 guard-todo-src + purga/TTL) = TASK-0152 (encolada, GO despues de
cerrar B). Rama "por archivo" del selector GATEADA tras B+C. NO encender vivo (uso vivo = GO aparte del operador).
Entrega in_review con handoff y libera tu claim. Canal ASCII.
