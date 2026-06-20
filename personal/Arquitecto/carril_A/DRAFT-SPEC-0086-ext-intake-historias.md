# DRAFT - Extension de SPEC-0086: Intake gobernado de historias/requisitos

> DRAFT en personal/Arquitecto; NO promovido. Decision de metodo: **EXTENSION de SPEC-0086**
> (no SPEC nueva) -- el intake es superficie de OPERAR del mismo MVP single-operator (vecina de
> RF-10 kickoff). Gated por DECISION-0051 (ratificacion pendiente). maker=Codex / checker=Arquitecto.

## Por que extension y no SPEC nueva
SPEC-0086 ya cubre observar (RF-1..RF-4) + operar gobernado (RF-5..RF-8) + roster (RF-9, deferida) +
kickoff (RF-10). El intake es la misma familia "operar via submit_intent sin bypass, atestado #4,
single-operator". Mantener la cohesion evita fragmentar el contrato del front. Se agregan RF-11 + ACs.

## RF-11 - Intake gobernado de requisitos (nuevo)
El front ofrece un **wizard de intake** que estructura una historia/requisito y la emite como
artefacto gobernado por submit_intent EXECUTE, atribuido al operador. Es la SEMILLA del pipeline SDD;
el Arquitecto la consume para autorar la SPEC.

### Modelo del artefacto
- intent kind: `task_upsert` (NO kind nuevo; ver DECISION-0051).
- task: `{ id: REQ-XXXX (o TASK-XXXX type=requirement), type: "requirement", status: "proposed",
  title, narrative, acceptance_intent (lenguaje llano), target_project (p.ej. "nova.budget"),
  author: "Operador" }`.
- `actorId: "Operador"`; idempotente via `idempotency_key`.
- Aterriza en TASK_INDEX + PROJECT_STATE#active_tasks + archivo de requisito (handoff explicito al
  Arquitecto).

## Criterios de aceptacion (nuevos)
- **AC14 (intake -> artefacto gobernado):** el wizard estructura la historia y la emite SOLO via
  submit_intent (`task_upsert` requirement), atribuida a `Operador`, idempotente; el artefacto queda
  en el ledger atestado. Test: submit de intake produce el task requirement en estado proposed con
  author=Operador; re-submit con misma idempotency_key NO duplica.
- **AC15 (EXECUTE exige confirmacion - prueba negativa):** EXECUTE solo escribe con
  `confirm:SUBMIT_INTENT`; sin confirm -> 409 y NO hay escritura al ledger (drift 0 antes/despues).
  La UI muestra paso de confirmacion visible ("operar pasa por gobierno"). Test negativo:
  mode:execute sin confirm no muta TASK_INDEX/PROJECT_STATE.
- **AC16 (redaccion PII del texto libre):** narrative + acceptance_intent se redactan en todo plano
  publicable (preview/vista/export) y van por canal ASCII; coherente con DECISION-0040. Test: payload
  con patrones tipo NIT/razon social/SQL -> el plano publicable no expone el literal.
- **AC17 (no-bypass / sin escritura directa):** se mantiene `directLedgerWrites:false`; ninguna ruta
  del front escribe estado/ledger fuera de submit_intent. Test negativo de superficie (extiende el de
  TASK-0127).
- **Carry permanentes:** AC11 (badge honesto), AC12 (routing-comportamiento), AC13
  (conformidad-de-diseno) siguen verdes.

## Gates de cierre (clon limpio)
- `node --test` verde (incl. tests AC14-AC17 de comportamiento + negativos); CI verde.
- `validate_collaboration_state` exit 0 CON y SIN secretos (DECISION-0046), drift 0, #4 epoca 1.14.0
  intacta (sin re-genesis), neutralidad limpia (codigo solo en Zeus-protocol; core neutral).
- Reproduccion desde clon limpio por el checker (Arquitecto); maker!=checker.

## Insumos de diseno
- D:/Agentes/Zeus/Zeus-protocol/src/server.js (/api/protocol/actions/submit ya soporta
  mode:execute + confirm:SUBMIT_INTENT -> runtime/submit_intent.py; falta UI + accion gobernada de
  intake + actorId=Operador para intake).
- design/interface/components/acciones-gobernadas/index.html (patron de confirmacion visible).
- runtime/submit_intent.py (task_upsert: capability/required_scopes/idempotency_key existentes).
