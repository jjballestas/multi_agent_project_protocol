---
message_id: MSG-20260620-Operador-to-Arquitecto-confirma-disenador-y-secuencia
type: DECISION
task_id: none
from: Operador
to: Arquitecto
requires_response: false
status: open
one_line_summary: (a) Disenador: id=Disenador, backend=preset claude, min-privilegio (lee Area_comun+design/, escribe solo Zeus-protocol/design/); y SI firma sus propios handoffs de diseno (submit_intent estrecho, solo sus handoffs) - autoria honesta, el dataset muestra SU firma. (b) Secuencia: PRIMERO el endurecimiento badge-honesto (test de comportamiento, pieza chica) y dejarlo AC PERMANENTE; luego etapa5 roster -> onboard Disenador -> etapa6.
requested_action: "Autorar: (1) la pieza chica de endurecimiento badge-honesto = TEST DE COMPORTAMIENTO (inyectar verificacion-runtime que FALLA -> badge NO-verde; todo-valido -> verde), AHORA, antes de etapa5; dejar 'badge behavior test' como AC PERMANENTE de etapa5/6. (2) SDD etapa5 roster (RF-9) con badge-honesto + behavior-test como AC. (3) Plan de ceremonia del onboard del Disenador (re-genesis-boundary gobernado, copia limpia, operador presente, rollback armado) con: id=Disenador, backend=preset claude, keypair propio (publica al registry pinned, privada wrapper-side), tool_policy min-privilegio (lee Area_comun+Zeus-protocol/design/, escribe SOLO Zeus-protocol/design/, NO codigo, submit_intent ESTRECHO solo para sus propios handoffs de diseno), rol = personal/operador/15_Asistente_PROMPT-disenador.md. maker=Codex/checker=Arquitecto."
question: none
context_refs:
  - Area_comun/mailbox/open/MSG-20260620-Arquitecto-to-Operador-confirma-front-completo-disenador.md
  - Area_comun/mailbox/open/MSG-20260620-Analista-to-Arquitecto-TASK-0128-recomendacion.md
  - personal/operador/15_Asistente_PROMPT-disenador.md
deadline_or_blocking_level: normal
---

# Confirmo: badge behavior-test primero; Disenador firma su propio diseno

## (b) Secuencia - APOYO al Analista: endurecer el badge AHORA
El test actual es **string-match** (verifica que el codigo mencione los validadores, NO que el badge se
ponga **no-verde** cuando la verificacion falla). Riesgo: un refactor podria **hardcodear verde y pasar**
= falso verde sobre la propiedad-tesis. Por eso:
- **Pieza chica YA, antes de etapa5:** **test de COMPORTAMIENTO** del badge (inyectar verificacion-runtime
  que FALLA -> badge NO-verde / working_tree/stale/fallo; todo-valido -> verde). Las funciones ya son
  inyectables; coste bajo.
- Dejar **"badge behavior test" como AC PERMANENTE** de etapa5/6: toda pieza nueva de UI queda
  regresion-proof contra la honestidad de estado. Es la propiedad-tesis; no la dejamos a un string-match.
- Luego: **etapa5 roster (RF-9) -> onboard Disenador -> etapa6**, de a una.

## (a) Disenador - confirmado, con AUTORIA HONESTA
- **id:** `Disenador`. **backend:** preset **`claude`** (el CLI disponible; mismo wrapper que el Arquitecto;
  no fijo un model-string que no tenga). **keypair propio** (publica al `agent_registry` pinned; privada
  wrapper-side).
- **tool_policy (min-privilegio):** LEE `Area_comun/` + `Zeus-protocol/design/`; ESCRIBE **solo**
  `Zeus-protocol/design/`; **NO** codigo (otros paths) **NO** estado.
- **FIRMA sus propios handoffs de diseno:** abrele un `submit_intent` **estrecho** -- SOLO para registrar
  **sus** handoffs de diseno (no otros writes al ledger). Razon: #4 es atestacion de **AUTORIA**; el dataset
  debe mostrar la firma del **Disenador** sobre su diseno, no la del Arquitecto en su nombre (eso
  misatribuiria la autoria). El Arquitecto sigue siendo **checker**.
- **rol/prompt:** `personal/operador/15_Asistente_PROMPT-disenador.md` (ajusta la linea "NO submit_intent"
  -> "submit_intent estrecho solo para sus propios handoffs de diseno").

## Onboard = ceremonia
Re-genesis-boundary GOBERNADO, copia limpia (DECISION-0045), **operador PRESENTE**, su propia ventana,
rollback armado. La epoca de #4 cambia al re-genesis (batcheado/gobernado, DECISION-0047). Reporta en
canonico (nuevo firmante en registry, validate exit 0, drift 0). Puedes empezar a disenar el mecanismo del
roster sin esperar la ceremonia (esos datos solo hacen falta para el onboard, que es el primer uso).

#4 epoca 1.14.0 pinned. Una ventana de riesgo a la vez. Canal ASCII.
