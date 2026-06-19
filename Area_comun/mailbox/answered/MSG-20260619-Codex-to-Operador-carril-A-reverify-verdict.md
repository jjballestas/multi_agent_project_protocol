---
message_id: MSG-20260619-Codex-to-Operador-carril-A-reverify-verdict
type: REVIEW
task_id: COORD-20260619-CARRIL-A-REVERIFY
from: Codex
to: Operador
status: answered
requires_response: false
response_owner: none
one_line_summary: Re-verificacion Codex Carril A: las 4 objeciones de enforcement quedan cerradas como SPEC/DECISION falsables; aprobable para promocion bajo GO del operador, sin encender flags aun.
requested_action: none
context_refs:
  - Area_comun/mailbox/open/MSG-20260619-Operador-to-Codex-carril-A-reverify.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0039-activacion-atestacion-autoria.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0081-activacion-atestacion-autoria.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0040-gate-dataset.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0041-precondicion-acoplamiento-readonly.md
---

# Veredicto Codex - re-verificacion Carril A

Veredicto: **aprobable para promocion bajo GO explicito del operador**. Mis 4 objeciones de enforcement quedan cerradas como estan escritas en los drafts actualizados. No promovi nada y no encendi ningun flag.

## A1 provisioning

**Cerrada.** El draft ya distingue los flags reales: `event_state.chain_enabled`, `event_state.agent_signatures_enabled`, `event_state.anchor_enabled` y `event_auth.enabled` top-level. Tambien registra el estado vivo correcto: #4 OFF, `event_auth.keys` ausente/vacio, `signature_config.public_keys = {}`, `anchor_config.remote_url = ""`.

SPEC-0081 AC1 exige provisioning antes del piloto: public keys por agente, claves HMAC en `event_auth.keys`, remoto/proof backend de anclaje, smoke positivo y casos negativos. Esto cierra el riesgo de `append_event` fallando por `event auth signing key missing` y de primer anclaje fallando por `remote_url=""`.

## A1 seguridad vs salud

**Cerrada.** AC2 queda como salud del instrumento (`>=99%`) con denominador derivado del event log, independiente del firmante. AC3 queda como seguridad binaria, bloqueante, con 6 vectores fijos: alteracion, borrado, insercion, reordenamiento, llave no registrada y atribucion cruzada. La distincion esta bien definida y es testeable por exit-code/golden por vector.

## A2 dos planos / PII

**Cerrada.** El draft ya no sobre-afirma "cero PII" como propiedad estructural del eventlog completo. Queda acotado asi:

- Estructural: sujeto por `canonical_hash`.
- Disciplinario: predicado/payload/handoffs/mailbox pueden contener texto libre hoy; si entrara PII seria anomalia DECISION-0018.
- Detector/exporter DEF-PII: tarea diferida, condicion antes de #2/#3 contra Core vivo o publicacion.

Esto refleja el codigo real: `runtime/state/events.jsonl` admite texto libre en `task_upsert`, `claim.notes`, `title`, `review`, etc.; `scripts/` no tiene detector PII real. Como contrato pre-promocion queda honesto y enforceable por tareas posteriores.

## A3 read-only

**Cerrada.** DECISION-0041 exige evidencia objetiva: intento de escritura al Core rechazado por el SO bajo identidad/montaje sin permiso, mas revision sustantiva de rutas de escritura. Eso convierte el read-only de convencion a gate falsable antes de lectura viva.

## Invariantes

- Escritor unico: no se toca; validador y drift siguen verdes.
- Off-by-default: no se cambia template ni config vivo.
- SemVer/CHANGELOG: quedan como condicion de promocion.
- Neutralidad: Carril A sigue documental/gateado; reglas de dominio quedan fuera del core.

Conclusion: **sin objeciones restantes de codigo-invariante** para promover los drafts como decisiones/SPEC, siempre que la promocion espere GO explicito del operador y la implementacion posterior ejecute los gates nuevos antes de encender #4 o correr #2/#3.
