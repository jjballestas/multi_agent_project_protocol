---
message_id: MSG-20260620-Operador-to-Arquitecto-GO-front-intake-historias
task_id: none
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: "GO (feature nueva, pull real = conducir nova.budget desde el front): dar al front un INTAKE gobernado de historias/requisitos. Modelo elegido = INTAKE -> el ARQUITECTO autora la SPEC (NO autoria directa de SPEC por el operador). El front captura la historia (wizard) y la emite por submit_intent EXECUTE (con confirmacion) como artefacto gobernado de requisito; el Arquitecto la convierte en SPEC con AC+test_plan bajo SDD (maker=Codex/checker, neutralidad, revision adversarial). Guarda PII innegociable (las historias de Budget pueden traer PII de terceros -> ligado a TASK-0118/DECISION-0040). Decide SPEC nueva vs extension de SPEC-0086 y si requiere DECISION previa (nuevo intent kind / superficie de escritura del operador). Drafts para mi ratificacion."
requested_action: "Por el metodo, disena la capacidad 'intake de requisitos' del front. (1) MODELO (elegido por el operador): el operador MONTA la historia/requisito en el front (wizard que la estructura: titulo, narrativa, intencion de aceptacion en lenguaje llano, proyecto destino p.ej. nova.budget) y se envia como INTAKE GOBERNADO por submit_intent. NO es una SPEC: es la semilla. El ARQUITECTO la convierte en SPEC (AC+test_plan, neutralidad, maker=Codex/checker) bajo SDD. Roles intactos: operador = 'que' + GO; Arquitecto = autor de la SPEC. (2) Cablea el camino EXECUTE real del front (hoy solo esta dry_run): el endpoint /api/protocol/actions/submit ya soporta mode:execute + confirm:SUBMIT_INTENT -> runtime/submit_intent.py; falta el boton/confirmacion en la UI. Acota el execute al intake (y a lo que decidas), con paso de confirmacion visible ('operar pasa por gobierno'). El intake aterriza como artefacto gobernado (backlog item type=requirement/story o doc de requisito) atribuido al operador, atomico/idempotente, y el Arquitecto lo consume para autorar la SPEC (handoff explicito). (3) GUARDA PII innegociable: el texto libre de la historia se redacta en cualquier plano publicable y va por canal ASCII a lo que se escribe al protocolo; las historias de nova.budget pueden contener PII de terceros (NIT, razon social, payloads SQL) -> coherente con DECISION-0040 y con TASK-0118/DEF-PII (que sigue como gate antes de captura viva). (4) Por el metodo: decide SPEC nueva vs extension de SPEC-0086, y si introduce un nuevo intent kind o una nueva superficie de escritura del operador -> DECISION primero (CLAUDE.md regla 2). AC: el front no escribe estado/ledger directo (solo submit_intent); execute exige confirmacion (prueba negativa: sin confirm no escribe); redaccion PII del texto libre (test); intake atribuido al operador, idempotente; carry AC11/AC12/AC13 (honestidad/routing/conformidad); validate con/sin secretos exit 0, drift 0, #4 epoca 1.14.0 intacta, neutralidad (codigo solo en Zeus-protocol), node --test/CI verde. maker=Codex / checker=Arquitecto, reproduccion desde clon limpio. Drafts primero para mi ratificacion."
question: "Confirmas el modelo (intake -> tu autoras la SPEC) y autoras el diseno (SPEC nueva o extension + DECISION si aplica)? Reporta los drafts."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0040-gate-dataset.md
  - Area_comun/tasks/TASK-0118-codex-def-pii-detector.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/design/interface/components/acciones-gobernadas/index.html
deadline_or_blocking_level: normal
---

# GO - front: intake gobernado de historias/requisitos (el Arquitecto autora la SPEC)

Pull real: quiero conducir **nova.budget** desde el front, montando historias/requisitos que entren al
pipeline SDD. Modelo elegido (decision del operador): **INTAKE -> el Arquitecto autora la SPEC.** El front
captura la historia; tu la conviertes en SPEC con AC+test_plan. No quiero autorar SPECs yo (preservo la
revision adversarial y la neutralidad que hacen confiable la SPEC).

## Lo que pido (por el metodo)
1. **Wizard de intake** en el front: estructura la historia (titulo, narrativa, intencion de aceptacion en
   lenguaje llano, proyecto destino) y la envia como **artefacto de requisito GOBERNADO** por submit_intent.
   Es la semilla, NO la SPEC.
2. **Cablea el EXECUTE real** (hoy el front solo manda dry_run): el server ya soporta `mode:execute` +
   `confirm:SUBMIT_INTENT` -> `runtime/submit_intent.py`; falta la confirmacion en la UI. Con paso de
   confirmacion visible (operar se ve gobernado). El intake aterriza atribuido al operador, idempotente, y tu
   lo consumes para autorar la SPEC (handoff explicito).
3. **Guarda PII innegociable:** el texto libre de la historia se redacta en plano publicable y va por canal
   ASCII; las historias de Budget pueden traer PII de terceros (NIT, razon social, SQL) -> coherente con
   DECISION-0040; TASK-0118/DEF-PII sigue como gate antes de captura viva.
4. **Decide tu, por el metodo:** SPEC nueva vs extension de SPEC-0086; y si introduce nuevo intent kind /
   nueva superficie de escritura del operador -> DECISION primero.

maker=Codex / checker=Arquitecto. Drafts para mi ratificacion antes de promover. Etapa 5 roster sigue
DEFERIDA. Verifico tu respuesta en canonico. Canal ASCII.
