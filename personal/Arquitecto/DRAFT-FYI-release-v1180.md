---
message_id: MSG-20260703-Arquitecto-to-Operador-FYI-release-v1180-y-activacion-trailers
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-03
context_refs:
  - CHANGELOG.md
  - Area_comun/tasks/TASK-0244-visionnova-f1g-release-1180.md
one_line_summary: "Release v1.18.0 tageada (F1 cerrado a falta del gate Analista de 0244); trailers construidos pero INACTIVOS: pido GO para relanzar crons con prompts 0242 y luego activar COMMIT_TRAILERS.json."
requested_action: "Dos GOs operativos: (1) RELANZAR los crons de Codex y Analista (los .ps1 ya llevan los prompts 0242 con envelope+fixloop+trailers; los procesos vivos corren la version anterior; el relanzamiento esta gateado por permisos: yo no puedo ejecutar powershell -File en esta sesion). (2) Con los crons relanzados y emitiendo trailers, autorizar la ACTIVACION del gate de trailers: creare Area_comun/protocol/COMMIT_TRAILERS.json con enabled:true + start_commit=<commit del relanzamiento> (fuera del config pineado; el epoch 1.14.0 no se toca). Orden anti-DoS (F-2): primero (1), despues (2)."
question: "GO para (1) relanzar crons con prompts nuevos y (2) activar trailers con start_commit posterior al relanzamiento?"
---

# FYI - Release v1.18.0 + estado de activacion de trailers

Hora: (se sella al enviar).

## Release
- CHANGELOG v1.18.0 con las 6 entregas F1 (intake gate / exception.recorded / trailers /
  taxonomia / envelope+fixloop / DECISION-0084 DoR).
- Templates sincronizados: AGENTS.template.md s.6.1-6.4 (intake DoR, excepciones auditadas,
  trailers, envelope+fixloop) + HANDOFF_TEMPLATE (regla envelope). TASK_TEMPLATE ya traia
  intake (0238); TASK_PROTOCOL ya traia envelope (0242).
- Gates 3/3 verdes en clon limpio; protocol.config.json byte-identico (sha 2E35F26E...,
  epoch 1.14.0 PINNED; sin diff contra TFM-dataset-N500).
- Tag v1.18.0 creado y pusheado; F2.1 (new_instance nova-budget) consume este tag.
- TASK-0244 va a gate adversarial del Analista (cierre formal de F1 tras su GO).

## Trailers (residual 0242, paso explicito separado)
Construidos y verificados (0240) pero INACTIVOS a proposito: los crons vivos aun corren los
prompts previos a 0242 y no emiten trailers; activar ahora = auto-DoS (F-2). Secuencia
correcta: relanzar crons -> verificar 1 commit de cada peer con trailer -> COMMIT_TRAILERS.json
con start_commit posterior. Pido los dos GOs en requested_action.
