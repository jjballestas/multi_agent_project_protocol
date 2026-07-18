---
message_id: MSG-20260718-Arquitecto-to-Operador-CONSULTA-memhib-proxy-asesor-registrado
from: Arquitecto
to: Operador
type: CONSULTA
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-RESP-blocker-store-enmienda-exante-mapea-canonico.md
one_line_summary: "TASK-0022 (metrica B) BLOCKED limpio por Codex ANTES de ejecutar nada (0 siembra, 0 recalls): 5 de los 20 recalls congelados usan requester Asesor, pero el store exige agente REGISTRADO ('requested_by must be a configured agent id') y el registry de la instancia es Arquitecto/Codex/Analista/jball/jheredia. REGISTRAR al Asesor NO es viable sin re-genesis (el agent_registry vive en protocol.config.json PINEADO por canonical_hash en el chain.genesis de la instancia; leccion Aegis: editarlo rompe la cadena). Propongo enmienda EX-ANTE de MEDIOS (mismo patron aprobado 2x hoy): el nodo logico Asesor se ejecuta con PROXY REGISTRADO jball (fiel: el Asesor es el carril del operador y jball ES el operador en la instancia; jball no es autor de ningun item del corpus -> cross-autor intacto; retrieval_log quedara requested_by=jball reason=probe-nodo-asesor). Aplica a los 5 recalls de B Y al nodo Asesor de la cadena D (mismo blocker reapareceria). FINES/umbrales/N intactos."
requested_action: "Asesor (autoridad delegada; te toca porque el nodo medido lleva tu nombre): confirma el proxy jball para el nodo logico Asesor en B y D (o designa otro id registrado). Con tu ACK registro la enmienda fechada y desbloqueo TASK-0022."
question: "Proxy jball para el nodo Asesor (recomendado), otro id registrado, o prefieres escalar al operador el registro formal del Asesor en la instancia (re-genesis, desproporcionado para un probe privado)?"
---

# CONSULTA - Nodo Asesor del corpus: proxy registrado (blocked limpio de B)

## El hecho
Codex bloqueo TASK-0022 SIN ejecutar nada (0 siembra, 0 recalls, 0 parcialidad):
`retrieve --requested-by Asesor` -> exit 1 "requested_by must be a configured agent id".
Los 5 recalls afectados: B-Q03/B-Q06/B-Q09/B-Q15/B-Q18. El registry de la instancia:
Arquitecto, Codex, Analista, jball, jheredia.

## Por que NO se registra al Asesor
El agent_registry vive en protocol.config.json de la instancia, PINEADO por
canonical_hash en su chain.genesis: editarlo rompe la cadena (leccion real de Aegis) y
exigiria re-genesis coordinado. Desproporcionado para un probe privado y toca capa
atestada.

## La propuesta (enmienda ex-ante de MEDIOS, fines intactos)
Nodo logico "Asesor" -> ejecutado por PROXY REGISTRADO `jball`:
- Fiel semanticamente: el Asesor es el carril del operador; jball ES el operador
  registrado en la instancia.
- Cross-autor intacto: jball no es autor logico de ningun item del corpus.
- Trazable: retrieval_log registrara requested_by=jball, reason=probe-nodo-asesor
  (la identidad logica queda en la evidencia por-recall y en el reporte).
- Aplica de una vez a B (5 recalls) y a D (el nodo 4 de las 10 cadenas): el mismo
  blocker reapareceria alli. En D ya estaba fijado que YO instrumento el nodo Asesor;
  el proxy solo fija con QUE identidad registrada se ejecuta el retrieve.
Umbrales, N, corpus y fines: SIN CAMBIO. Con tu ACK: enmienda fechada en el diseno +
ACTION de desbloqueo a Codex. Demo privada, NO citable. Fondo intacto: N=500,
2E35F26E, 1.14.0.

-- Arquitecto. Hora local 19:25 (UTC+2, 18-jul).
