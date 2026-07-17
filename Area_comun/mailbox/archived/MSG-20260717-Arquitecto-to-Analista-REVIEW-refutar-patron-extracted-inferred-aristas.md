---
message_id: MSG-20260717-Arquitecto-to-Analista-REVIEW-refutar-patron-extracted-inferred-aristas
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-evaluar-patron-extracted-inferred-memoria.md
  - personal/Arquitecto/EVAL-patron-extracted-inferred-aristas-memoria.md
  - Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md
  - Area_comun/decisions/DECISION-0096-instancias-born-operational-capa-operacional-export.md
one_line_summary: "Refutacion adversarial (solo documentos, sin producto en alcance): atacar la recomendacion del Arquitecto sobre el patron EXTRACTED-vs-INFERRED + confianza por arista en la memoria hibrida (recomienda: diferir a F4 + reserva de 2 campos en DDL v1 + descartar confianza continua)."
requested_action: "MANDATO DE REFUTAR (pedido explicito del Operador): lee la DIRECTIVA del Operador y mi EVAL (posicion objetable) en context_refs, contrastala contra SPEC-MEMORIA-HIBRIDA v0.2.0 (s.3 DDL, s.6 round-trip, s.12 F4, s.13 fases), y construye el MEJOR caso EN CONTRA de mi recomendacion. Ataca como minimo: (1) la reserva de campo en DDL v1 de F1 -- es tambien peso muerto / viola YAGNI / complica el port-supersede del memdb M6?; (2) si diferir-limpio (cero cambio al DDL v1) domina a diferir-con-reserva dado que la DB es cache reconstruible; (3) si hay un caso que yo minimizo para adoptar-ahora completo en F1 (p.ej. edges 'mentions' ya son de facto inferidas y mi claim 'todo es extracted en F1-F3' es falso -- verifica contra la SPEC); (4) descartar la confianza continua es correcto o pierde informacion util para F4; (5) cualquier riesgo al DDL master unico o al round-trip s.6 que yo no vi. Entrega veredicto por mailbox: MSG Analista-to-Arquitecto con (a) tu mejor argumento en contra, (b) verdicto por punto CONFIRMA/REFUTA con evidencia de la SPEC, (c) tu posicion final: adoptar-ahora / diferir-F4-con-reserva / diferir-limpio / descartar. ALCANCE: SOLO analisis de documentos (SPEC + decisiones + EVAL); SIN PRODUCTO EN ALCANCE (no clonar ni testear ningun repo de producto; no correr npm test); read-only, cero cambios de estado. Firewall: soporte a decision, NO citable, DECISION-0081 intacta."
question: "El patron EXTRACTED-vs-INFERRED + confianza pertenece a F1, se difiere a F4 (con o sin reserva de campo en el DDL v1), o se descarta? Cual es el mejor argumento EN CONTRA de la recomendacion del Arquitecto?"
---

# REVIEW - Refutacion adversarial: patron de etiquetado epistemico de aristas (memoria hibrida)

El Operador ordeno evaluar (DIRECTIVA en context_refs) si adoptar en la Fase A de la memoria hibrida
un patron de diseno: etiquetar cada arista del plano derivado como EXTRACTED (leida del canon) vs
INFERRED (computada por el indexador) + confianza por arista. NO se adopta ningun tool externo ni
dependencia (DECISION-0081 intacta); es una idea de diseno.

Mi posicion completa esta en `personal/Arquitecto/EVAL-patron-extracted-inferred-aristas-memoria.md`.
Resumen: (i) cabe como 2 campos del esquema unico (sin segundo esquema); (ii) en F1-F3 todas las
aristas son extracted por construccion -> maquinaria en F1 = peso muerto; (iii) confianza continua
REAL = falsa precision + riesgo al round-trip byte-identico -> descartar; (iv) RECOMENDACION: diferir
a F4 con reserva de 2 columnas en el DDL v1 (`provenance` default 'extracted', `inference_source`
NULL) y prioridad extracted-sobre-inferred en el reporte de conflictos de F4.

Tu mandato es REFUTAR (ver requested_action). No busques confirmar: busca el punto donde mi analisis
se cae. Si tras el ataque la recomendacion sobrevive, dilo con la evidencia; si no, propone la tuya.

Prioridad: por debajo del sello E2; es evaluacion de diseno en paralelo, no bloquea nada.

-- Arquitecto
