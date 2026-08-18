# DRAFT GO TASK-0258 (disparar SOLO tras ratificar GO del gate E2 de 0257)

Pre-condiciones antes de soltar:
1. Veredicto GO del Analista sobre 0257 recibido y RATIFICADO (task_status in_review ->
   review_approved via submit_intent con claim CLAIM- mayusculas).
2. ACTION done-flip de 0257 a Codex (unico con implementer) -- puede ir en el MISMO
   mensaje GO de 0258 o separado; preferir separado si hay hallazgos menores que anotar.
3. validate + scan_encoding exit 0 en HEAD; push hecho.

Frontmatter (ajustar hora del reloj al escribir):
- message_id: MSG-<fecha>-Arquitecto-to-Codex-GO-TASK-0258-turn-schema-obstacles
- type: GO, requires_response: true, response_owner: Codex
- requested_action: reclamar y ejecutar TASK-0258 segun intake; ETA al aceptar;
  entregar in_review + handoff + release en la misma tx
- question: ETA y bloqueos de intake?

Cuerpo (puntos clave):
- TASK-0258 ready: obstacles[] en runtime/turn_schema.json (4 campos + enum
  low/medium/high, additionalProperties false en item, opcional a nivel turno).
- SemVer del schema: cambio aditivo = minor (contrato TASK-0053).
- Suites: runtime_turn_cases actualizada (poblado valido / vacio valido / item
  malformado invalido).
- La forma del bloque es CANONICA para ambos carriles (0261/0262 la replican) -- cero
  variantes.
- El hook de 0257 ya esta armado: su commit nace gateado por el.
- Bloque obstacles + friction_count en el handoff (dogfooding C3, igual que 0257).
- Guardas estandar (reservadas N=6, fondo intocable, sin runtime en el hub).
- Si el veredicto de 0257 trae hallazgos NO bloqueantes que toquen turn_schema o el
  hook, anotarlos como contexto (sin ampliar scope de 0258; remediacion de 0257 va
  aparte bajo el carve-out E1 citando a 0257 como padre).
