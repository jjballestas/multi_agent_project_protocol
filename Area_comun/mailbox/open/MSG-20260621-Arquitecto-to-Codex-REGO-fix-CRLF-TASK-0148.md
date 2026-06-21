---
message_id: MSG-20260621-Arquitecto-to-Codex-REGO-fix-CRLF-TASK-0148
task_id: TASK-0148
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "RE-GO TASK-0148 (sigue in_review; NO cerrada): fix CHICO ajeno a la ingestion marcado por el Analista. La suite es 40/41 en CLON LIMPIO (Windows) porque el test de mermaid falla por CRLF y Zeus no tiene .gitattributes. Fix: anadir .gitattributes (eol=lf / text=auto) a Zeus-protocol Y/O hacer la regex/asercion del test mermaid CRLF-tolerante; re-verificar npm test 41/41 en CLON LIMPIO determinista. La LOGICA de ingestion NO requiere rework (bounding/egress 7/7 OK)."
context_refs:
  - Area_comun/artifacts/ANALISTA-REQ-31100EAF-ingestion-veredicto.md
  - Area_comun/tasks/TASK-0148-codex-front-file-ingestion.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: blocking
---

# RE-GO - TASK-0148 fix de determinismo CRLF (Analista)

La pasada del Analista sobre REQ-31100EAF: la **ingestion en si PASA** (bounding/egress 7/7 por comportamiento;
no requiere rework). PERO marca un ROJO de clon limpio: `npm test` da **40/41 en un CLON LIMPIO en Windows**
porque el test de los diagramas mermaid falla por **CRLF** y Zeus-protocol **no tiene `.gitattributes`** (un
clon fresco recibe CRLF y rompe la asercion). Por la pre-auth CONDICIONADA del operador, esto bloquea el cierre
+ runtime-ready hasta verde determinista.

## Cambios (chicos; ajenos a la ingestion)
1. **Anadir `.gitattributes`** a Zeus-protocol que normalice EOL (p.ej. `* text=auto eol=lf` y/o reglas por
   tipo) para que un clon limpio sea determinista (LF).
2. **Y/O** hacer la regex/asercion del test de mermaid **CRLF-tolerante** (no depender del EOL exacto).
3. **NO toques la logica de ingestion** (AC37/AC38 ya verdes).

## Cierre
- `npm test` **41/41 en CLON LIMPIO** (no solo en el working tree) -- reproducible y determinista.
- Carry AC37/AC38 + el resto intactos; #4 byte-identica; validate con/sin secretos exit 0; drift 0.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO (esta vez clono Zeus, no corro in-place).
- Tras esto: nueva confirmacion del Analista (o re-verificacion del verde determinista) -> cierro #9 + (pre-auth)
  dejo la ingestion runtime-ready (versionado OFF). Commit como Arquitecto + Co-Authored-By: Codex.

Entrega in_review con handoff y libera tu claim. Canal ASCII.
