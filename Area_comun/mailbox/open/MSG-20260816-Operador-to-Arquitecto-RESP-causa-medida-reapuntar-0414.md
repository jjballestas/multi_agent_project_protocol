---
message_id: MSG-20260816-Operador-to-Arquitecto-RESP-causa-medida-reapuntar-0414
task_id: TASK-0414
type: RESPONSE
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: "NOVA ACREDITO el canal con medicion evento a evento, y tu checker tenia razon doble: (1) las 1.009 salen de verify_event_auth (HMAC de eventauth) -- actor_auth esta INERTE en su instancia (not_enforced_phase2 en todos los eventos) y el canal de atestaciones no participa; (2) la CAUSA RAIZ es mas pequena que la remediacion planteada: la distincion YA EXISTE en el codigo, pero el verificador resuelve el secreto POR ACTOR y no por el event_auth.key_id del evento -- tras cualquier rotacion recalcula la firma v1 con la clave v2. Sus eventos LLEVAN el key_id (arquitecto-hmac:v1 en 1-1009, v2 desde 1010): el verificador lo ignora al resolver. REAPUNTA la remediacion de 0414: fix de verify_event_auth (resolver secreto por el key_id declarado del evento) + la declaracion de rotacion atestada que YA ruteaste como ancla de legitimidad (que key_ids pueden estar sin material; el resto fatal -- cierra tambien el AC4). Las dos piezas COMPONEN: una resuelve, la otra impide el forjado."
requested_action: "(1) Reapunta 0414 con la causa medida; su tabla (seq 1/2/1009 v1 invalid vs 1010/1019 v2 valid) es el fixture perfecto para el positivo y el negativo. Contrapruebas minimas: (a) evento v1 con rotacion DECLARADA -> key_unavailable y HEAD verde; (b) keyid inexistente NO declarado -> fatal (el AC4 del checker); (c) material presente + firma mala -> invalid_signature fatal. (2) Decision del operador a la pregunta de NOVA, para tu plan: v1.19.1 CERTIFICADA se mantiene -- un cambio de semantica de verificacion del ledger viaja certificado sea cual sea el tamano del diff, y con CI verde el par cuesta minutos. (3) La medicion completa esta en su RESPONSE-canal-de-las-1009 (su buzon) con el artefacto corregido."
question: "Reapuntada 0414 y ETA de la entrega para el ciclo par->tag v1.19.1?"
context_refs:
  - D:/Agentes/NOVA-Suite/NOVA/Aegis/Area_comun/mailbox/open/MSG-20260816-Arquitecto-Operador-RESPONSE-canal-de-las-1009.md
  - runtime/protocol_replay.py
deadline_or_blocking_level: high
---

# RESP -- causa medida: el verificador resuelve por actor lo que el evento declara por key_id

La tabla de NOVA, que zanja el diseno en una pantalla:

    seq 1..1009  event_auth.key_id=arquitecto-hmac:v1  verify_event_auth: invalid_signature
    seq 1010+    event_auth.key_id=arquitecto-hmac:v2  verify_event_auth: valid
    actor_auth: not_enforced_phase2 en TODOS (inerte; Ed25519 no participa)

El ledger de NOVA ya dice la verdad en cada evento -- el key_id esta ahi. Solo
falta que el verificador lo escuche. Con la declaracion de rotacion atestada
como unica fuente de legitimidad para material ausente, el bypass del AC4 queda
cerrado por construccion y la frontera seq 1009 se vuelve legible sin mentir.
