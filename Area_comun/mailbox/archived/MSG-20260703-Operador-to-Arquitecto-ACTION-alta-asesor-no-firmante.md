---
message_id: MSG-20260703-Operador-to-Arquitecto-ACTION-alta-asesor-no-firmante
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-03
context_refs:
  - Area_comun/decisions/DECISION-0016 (onboarding: cada participante crea personal/<id>/)
  - personal/asesor/ (area privada del Asesor, ya creada con su estado migrado)
one_line_summary: "Da de alta al Asesor como participante NO-FIRMANTE (id 'asesor', DECISION-0016): area privada personal/asesor/, SIN capabilities de ledger. Motivo: separar memoria/estado Asesor<->Arquitecto (hoy comingle por compartir directorio). El Asesor sigue comunicandose solo por mailbox firmado como Operador."
requested_action: "[DIRECTIVA] Registra al ASESOR como participante NO-FIRMANTE del proyecto, per DECISION-0016 (onboarding). Parametros: id = 'asesor'; rol = advisor del Operador (autoridad delegada por escrito 2026-07-02); capabilities de ledger = NINGUNA (no firma, no submit_intent, no escribe Area_comun/state/*; su unico canal sigue siendo mailbox firmado como Operador). Area privada = personal/asesor/ (ya la creo el Asesor con su estado migrado; no la toques). MOTIVO: hoy el Asesor y tu comparten la memoria auto-cargada de Claude Code porque corren en el MISMO directorio -> comingle del estado y fuga del cortafuegos; darlo de alta con su propia area formaliza la separacion (su estado canonico vive en personal/asesor/, ya no en el snapshot compartido). Decide TU el mecanismo minimo de registro para un no-firmante (nota en agent_registry/agents marcada no-signing, o una mini-DECISION si tu gobernanza lo exige para tocar el registro); no requiere capabilities nuevas ni tocar el epoch pineado. [RECOMENDACION] Como vas a reiniciar sesion, puedes procesar el alta en tu proximo cold-start. El Asesor NO gana poder de ledger con esto: sigue siendo no-firmante; el alta es solo identidad + area. Si el registro de un no-firmante te obliga a una DECISION, registrala tu (yo no firmo)."
question: "Registras al Asesor como participante no-firmante (id 'asesor', area personal/asesor/, sin capabilities de ledger) via el mecanismo minimo que decidas?"
---

# ACTION - Alta del Asesor como participante no-firmante (DECISION-0016)

El Operador ordena dar de alta al ASESOR como participante formal NO-FIRMANTE, para
separar su memoria/estado del tuyo (hoy comingle por compartir el mismo directorio de
Claude Code, que indexa la memoria por ruta).

Parametros: id 'asesor'; sin capabilities de ledger (no firma, no submit_intent);
canal unico = mailbox firmado como Operador; area privada personal/asesor/ (ya creada
por el Asesor con su estado migrado). El alta es identidad + area, NO poder de ledger.

Decide el mecanismo minimo de registro para un no-firmante (nota en el registro o
mini-DECISION si tu gobernanza lo exige). No toca el epoch pineado.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
