---
message_id: MSG-20260619-Operador-to-Codex-carril-A-reverify
type: REVIEW
task_id: COORD-20260619-CARRIL-A-REVERIFY
from: Operador
to: Codex
status: answered
requires_response: true
response_owner: Codex
one_line_summary: Re-verificacion adversarial de los drafts Carril A actualizados (commit e09a560); confirma que tus 4 objeciones quedan cerradas como estan escritas. NO promover, NO encender.
requested_action: Revisar read-only los 4 drafts actualizados y devolver veredicto (aprobable para promocion / objeciones restantes). No promover por submit_intent ni encender flags sin GO del operador.
question: Quedan cerradas tus 4 objeciones de enforcement como estan escritas en los drafts actualizados, o queda objecion?
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0039-activacion-atestacion-autoria.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0081-activacion-atestacion-autoria.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0040-gate-dataset.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0041-precondicion-acoplamiento-readonly.md
---

# Re-verificacion adversarial Carril A - invariantes de codigo y enforcement

Codex: re-verificacion adversarial de los drafts actualizados (commit e09a560), read-only.
NO promuevas, NO enciendas flags. Confirma o objeta que tus 4 puntos quedan cerrados COMO ESTAN ESCRITOS:

1. A1 provisioning: SPEC-0081 AC1 exige claves HMAC en event_auth.keys antes de event_auth.enabled,
   y anchor_config.remote_url/proof backend antes de anchor_enabled, con smoke que demuestre que
   append_event y el primer anclaje NO fallan tras el provisioning (y fallan sin el). Suficiente?

2. A1 AC3: prueba negativa binaria y bloqueante, con 6 vectores fijos (alteracion / borrado / insercion /
   reordenamiento / llave no registrada / atribucion cruzada) y golden reproducible por vector. El
   manipulation-check 99% queda como gate de SALUD, no de seguridad. Bien definido y enforceable?

3. A2: el invariante de "cero PII" queda acotado al plano estructural (sujeto-por-hash); el predicado /
   texto libre del payload + handoffs / mailbox = control disciplinario; el detector de PII real / exporter
   del plano publicable es la tarea diferida DEF-PII, condicion ANTES de la captura viva (#2/#3), NO
   bloqueo de Carril A. AC4 se verifica por esquema, no por scan_encoding. Cierra tu objecion de enforcement?

4. A3: la verificacion read-only incluye prueba negativa OBJETIVA y registrada (intento de escritura al
   Core rechazado por el SO bajo identidad sin permiso), no solo revision sustantiva / grep. Suficiente?

Nota de alcance: los goldens nuevos (attestation_health_cases, los 6 negativos, smoke de provisioning,
prueba negativa de A3) se EJECUTAN como tu gate de aceptacion en implementacion POST-promocion; ahora
confirma que la SPEC los exige de forma falsable y enforceable. Devuelve veredicto para el GO del operador.
Sin GO del operador no se promueve ni se enciende nada. Canal ASCII.
