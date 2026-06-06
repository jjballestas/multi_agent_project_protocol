---
message_id: MSG-20260605-operador-to-Claude-license-propietaria
type: DECISION_REQUIRED
task_id: none
from: operador humano
to: Claude
requires_response: true
response_owner: Claude
subject: LICENSE propietaria (ARR) anadida out-of-band: formalizar + decidir visibilidad del repo
one_line_summary: El operador anadio /LICENSE (propietaria, All Rights Reserved, titular John Jairo Ballestas Payares) en la raiz sin claim; falta gobernarla en el protocolo y alinear el README.
requested_action: Registrar una DECISION de licenciamiento (propietaria/ARR) que enlace /LICENSE; crear el claim correspondiente sobre /LICENSE + README*; y alinear README.md/README_INSTANCIACION.md, que hoy se describen como "reusable template" (contradice ARR). No incluir datos personales sensibles (el NIE NO debe entrar en ningun fichero versionado).
question: Con licencia propietaria, el repo sigue PUBLICO (escaparate, visible-pero-no-usable) o se pasa a PRIVADO?
context_refs:
  - LICENSE
  - README.md
  - README_INSTANCIACION.md
  - Area_comun/decisions/DECISION-0001-versionado.md
changed_refs:
  - LICENSE
validation_refs:
  - none
deadline_or_blocking_level: normal
status: open
---

# LICENSE propietaria (ARR) anadida out-of-band

Delta: el operador humano creo `/LICENSE` (propietaria, *All Rights Reserved*, titular **John Jairo
Ballestas Payares**, contacto john.ballestas@gmail.com) directamente en la raiz, **sin claim** y fuera
del flujo de tareas. Es una decision de politica del operador, no trabajo de implementacion.

Pendiente de gobernanza (lane del arquitecto):
1. **DECISION de licenciamiento** que enlace `/LICENSE` y fije el alcance (propietaria/ARR) - analogo a
   como DECISION-0001 gobierna el versionado.
2. **Claim** sobre `/LICENSE` + `README*` antes de editarlos.
3. **Alinear el mensaje**: `README.md` y `README_INSTANCIACION.md` se venden como *"reusable template"*
   (invitan a copiar); con ARR nadie puede copiar/usar sin acuerdo. Hay que reconciliar el wording.
4. **Privacidad**: el NIE del titular **no** debe figurar en ningun fichero versionado (en `/LICENSE`
   solo va el nombre + email de contacto, por diseno).

No tomo claim ni edito estado yo (canal de operador humano; ademas hay claim activo de Claude sobre el
track de runtime). Adopcion/formalizacion = decision del arquitecto + operador. Una sola pregunta arriba.

## Resolucion del operador (2026-06-05)
**Repo = PRIVADO.** El operador decide pasar el repositorio a privado (licencia propietaria, no
escaparate publico). Queda pendiente para el arquitecto: (1) DECISION de licenciamiento que enlace
`/LICENSE`, (2) claim sobre `/LICENSE` + `README*`, (3) reconciliar el wording "reusable template" del
README con ARR. La pregunta del frontmatter queda respondida: **privado**.
