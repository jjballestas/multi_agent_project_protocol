---
message_id: MSG-20260620-Arquitecto-to-Codex-GO-TASK-0133
task_id: TASK-0133
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0133 (ready, maker=Codex): front intake gobernado de historias/requisitos (RF-14). Wizard -> task_upsert requirement via EXECUTE confirmado (actorId=Operador, idempotente); PII estructural+ASCII; no-bypass; construir CONTRA design/interface/components/intake/ (AC13). Ratificado DECISION-0051 + ext SPEC-0086 (AC14-AC17). Codigo en Zeus-protocol; yo checker."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0051-operator-execute-write-surface-front.md
  - Area_comun/tasks/TASK-0133-codex-front-intake-historias.md
  - Area_comun/artifacts/ANALISTA-intake-gobernado-requisitos-diseno.md
  - D:/Agentes/Zeus/Zeus-protocol/design/interface/components/intake/
deadline_or_blocking_level: normal
---

# GO - TASK-0133 front intake gobernado de requisitos (RF-14)

Ratificado por el operador (DECISION-0051 + extension SPEC-0086 RF-14/AC14-AC17). Arranca el build.
maker=Codex / checker=Arquitecto; codigo en Zeus-protocol; reproduccion desde clon limpio.

## Lo esencial
- **Wizard de intake** conforme al diseno YA entregado en `design/interface/components/intake/` (lista,
  wizard-1-capturar, wizard-2-preview, wizard-3-confirmar, wizard-4-resultado, detalle, estados). AC13
  conformidad aplica a esas pantallas.
- **Accion gobernada de intake** -> intent `task_upsert` de un requirement (status proposed,
  type=requirement, author=Operador), `actorId:"Operador"` SOLO para intake, idempotency_key estable.
- **EXECUTE real cableado:** confirmacion visible que declara el writer (runtime/submit_intent.py) +
  `mode:execute`+`confirm:SUBMIT_INTENT`; preview(dry_run) != envio; sin verde sin respuesta real.
  Mantener directLedgerWrites:false.
- **PII ESTRUCTURAL (AC16):** separar lenguaje-llano publicable del payload sensible; redactar/marcar texto
  libre; ASCII en todo string al protocolo; advertir en compose y confirm. NO apoyarse en un detector
  inexistente (TASK-0118/DEF-PII proposed).

## ACs y gates
AC14 (intake->artefacto gobernado, Operador, idempotente), AC15 (EXECUTE exige confirmacion; prueba
negativa sin-confirm-no-escribe), AC16 (PII estructural+ASCII), AC17 (no-bypass) + carry AC11/AC12/AC13.
Gates: node --test/CI verde, npm start ejecutable y la vista intake navega; validate exit 0 CON y SIN
secretos, drift 0, #4 epoca 1.14.0 intacta, neutralidad. Commit como Arquitecto + Co-Authored-By: Codex.

Entrega via submit_intent (in_review) cuando este verde; yo reproduzco como checker y cierro.
