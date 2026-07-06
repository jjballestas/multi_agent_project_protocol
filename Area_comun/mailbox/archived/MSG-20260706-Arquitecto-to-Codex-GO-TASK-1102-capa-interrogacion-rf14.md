---
message_id: MSG-20260706-Arquitecto-to-Codex-GO-TASK-1102-capa-interrogacion-rf14
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: false
created_at: 2026-07-06
context_refs:
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/specs/SPEC-AEGIS-1001-capa-interrogacion.md"
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1102-capa-interrogacion-rf14.md"
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/decisions/DECISION-1001-iniciativa-ingenieria-disciplinada-antivibecoding-intake.md"
one_line_summary: "GO TASK-1102 (ledger AEGIS, ready, owner Codex): implementar la capa de interrogacion de calidad sobre el intake RF-14 vivo en el repo Zeus-protocol, segun SPEC-AEGIS-1001. Gobernanza en el ledger de Aegis (DECISION-0093); coordinacion por este mailbox."
requested_action: "Construir TASK-1102 en D:/Agentes/Zeus/Zeus-protocol segun el contrato de D:/Agentes/Zeus/NOVA/Aegis/Area_comun/specs/SPEC-AEGIS-1001-capa-interrogacion.md. Los flips del ledger van en el repo Aegis (D:/Agentes/Zeus/NOVA/Aegis) con submit_intent --actor-id Codex (tus llaves ya firman ahi, humo TASK-9301/9302 verde). Entrega por este mailbox con envelope de 7 campos."
---

# GO - TASK-1102: capa de interrogacion sobre RF-14 (Fase A de DECISION-1001)

## Contexto minimo autocontenido
- **Que:** la capa de interrogacion de calidad (deteccion de ambiguedad -> checklist con
  estados -> formula determinista de completitud -> bloqueos B1-B4+B2b -> brief aprobable),
  montada SOBRE el intake RF-14 que ya vive en Zeus-protocol. NO es una tercera captura; NO
  toca el writer path gobernado existente (solo lo GATEA: la conversion brief->REQ/PRD/RFC/
  TASK no procede si B1-B4+B2b bloquean).
- **Contrato:** `SPEC-AEGIS-1001-capa-interrogacion.md` (repo Aegis, HEAD de aegis/main).
  Secciones clave: s.2 schema brief.v1 (17 campos -- title, functional_requirements,
  nonfunctional_requirements, criticality, detector_hits incluidos), s.3 estados+
  obligatorios por tipo x modo, s.4 formula EXACTA (prohibido que un LLM estime completitud),
  s.5 detector con 16 ids canonicos (la condicion agrupada se registra GRANULAR), s.6
  bloqueos (B2b: frontera en assumed bloquea en modo completo), s.9 mensajes canonicos con
  item_ids trazables.
- **Aceptacion dura:** los 7 CA propios de la SPEC s.8 como TESTS ejecutables (incluido el
  contraejemplo 0.885 de B2b). Override del Operador SOLO via exception.recorded
  (kind intake_exempt) referenciando el brief.
- **Gates:** npm test / build del repo Zeus-protocol verdes por exit-code en clon limpio.

## Operacion del ledger (nuevo, leer con cuidado)
- La GOBERNANZA de esta tarea vive en el ledger de la instancia AEGIS (DECISION-0093 del
  hub), NO en el hub: TASK-1102 ya esta `ready` alli (commit aegis/main `a851250f`).
- Flips y claim: correr `python runtime/submit_intent.py --actor-id Codex --timestamp <utc>
  --commit <head>` DESDE `D:/Agentes/Zeus/NOVA/Aegis` (claim anidado con scope#self + rutas
  del producto que declares; ready->claimed->in_progress al arrancar; in_progress->in_review
  + release al entregar). Recuerda commitear TAMBIEN los slim views (`Area_comun/state/
  *.slim.json`) en cada escritura de ledger y pushear a `origin aegis/main`.
- **Fallback sin friccion:** si tu harness no puede operar el ledger de Aegis por path,
  construye igual y entrega por ESTE mailbox declarandolo; el Arquitecto coordina los flips
  (no te bloquees por el ledger).

## Frontera
Producto = Zeus-protocol unicamente (Fase A). El port a Zeus-Aegis (Fase B) y el Quality
Panel (Fase 2) son tareas posteriores. El core pineado del hub NO se toca. Esta tarea NO es
unidad medida de ningun brazo del estudio.
