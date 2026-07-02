---
message_id: MSG-20260702-Operador-to-Arquitecto-ACTION-higiene-mailbox-cada-5
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-02
context_refs:
  - Area_comun/mailbox/open/
one_line_summary: "Directiva permanente: higiene de mailbox cada 5 mensajes consumidos; open/ solo contiene mensajes vivos."
requested_action: "[DIRECTIVA permanente] (1) REGLA DE CADENCIA: cuando open/ acumule 5 o mas mensajes ya consumidos (respondidos, entregados, acusados o superados), corre un lote de higiene (mailbox_archive via submit_intent, capability orchestrator) en tu siguiente turno; lotes de maximo 5, en ventana idle de peers, en background (lecciones ya conocidas de la skill mailbox-hygiene). (2) open/ debe contener SOLO mensajes vivos: pendientes de respuesta o de consumo. (3) AHORA: en tu proximo turno archiva los ya consumidos, minimo: tu FYI de F0.2 (acusado por la orden F1), el REVIEW del pivote v2 del Analista (consumido por DECISION-0083) y el FYI de higiene del Analista (acusado por el Operador); el FYI del cortafuegos archivable tras leerlo; la ACTION de higiene de Codex sigue VIVA hasta su FYI. (4) Cada lote de higiene se anota en el FYI o commit correspondiente; sin narrar proceso."
question: ""
---

# ACTION - Directiva permanente: higiene de mailbox cada 5 consumidos

Motivo del Operador: open/ acumula mensajes ya cerrados y eso vuelve el canal
ilegible. El mailbox es el panel del Operador: si esta lleno de consumidos, un
mensaje vivo se pierde entre ruido.

Regla simple: 5 consumidos acumulados => lote de higiene en el siguiente turno.
Esta directiva complementa (no sustituye) las reglas duras de la skill
mailbox-hygiene: ASCII, archive solo via mailbox_archive gobernado, lotes de 5,
ventana idle, recuperacion por atomicidad si un lote se corta.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
