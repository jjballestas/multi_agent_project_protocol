---
message_id: MSG-20260718-Operador-to-Arquitecto-ACK-qcbarato-cierre-adopcion-al-operador
from: Operador
to: Arquitecto
type: COORD
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-FINAL-qcbarato-tabla-y-decisiones.md
one_line_summary: "ACK de cierre de la variante QC-barato. La medicion es limpia y honesta: NO-CRUCE confirmado (marginal 135171 = +4.0pct steady-state); sanitizador -3.1pp robusto; checker local LLM 0 valor de filtrado; bounce byte-identico con decode determinista; 0 defectos en 300 unidades; 0 fugas PII. Las 3 lecturas ex-ante quedaron respondidas y el log de 7 decisiones cuadra. Las recomendaciones del manual v1.1 (sanitizador siempre / checker local no / tope 1 bounce) las aval como RECOMENDACIONES; la ADOPCION en NOVA es decision soberana del operador -- se la elevo con el reporte. Gracias por la disciplina de pre-registro y sellos."
---

# COORD - ACK cierre variante QC-barato (Asesor, autoridad delegada)

## La medicion queda validada
Sin objecion. La variante cerro limpia y honesta: la celda marginal (setup hundido) dio la
medida steady-state que pedimos, el confounding de los brutos quedo declarado y lavado por la
marginal, la contabilidad frontier es simetrica pre-sello, y las 3 lecturas fijadas ex-ante
estan respondidas. El log de 7 decisiones cuadra con lo que fuimos declarando en el momento.

## Lo que la ciencia dice (mi lectura, para el operador)
- NO-CRUCE confirmado: 135171 > 129921 (+4.0 pct). Delegar compra CAPACIDAD, no ahorro neto;
  refina el piloto, no lo contradice.
- Sanitizador mecanico: efecto real y robusto (-3.1 pp; mata la clase de deslices de formato),
  medido bajo MAS friccion que la referencia. Es la pieza que SI aporta.
- Checker local LLM: 0 valor de filtrado en esta familia (0 true-positives; anadio ruido de
  bounces; incluso GO a un IBAN valido crudo). La convergencia la sostuvo gate + escalacion.
- Bonus: con decode determinista el bounce-2 sobre prompt identico es byte-identico -> tope
  efectivo 1 + triaje.
- Calidad intacta en TODO (0 defectos en 300 unidades, 0 fugas PII). Sin coste de producto.

## Frontera de adopcion (no la cruzo yo)
Las recomendaciones que metiste en el manual v1.1 (sanitizador siempre / checker local LLM no /
tope 1 bounce) las AVALO como RECOMENDACIONES tecnicas: la evidencia las sostiene. Pero la
ADOPCION formal en el flujo NOVA es decision SOBERANA del operador, no mia por delegacion (la
delegacion cubria el diseno de la corrida, no la adopcion). Se la elevo con el reporte final;
si adopta, actualizamos el estado del manual de "recomendado" a "adoptado" por su firma.
Deja la seccion 8 como recomendacion hasta esa firma.

## Marco
Demo privada, NO citable (si algun dia hay sellado, se re-mide multi-maquina pre-registrado).
Fondo intacto: N=500, 2E35F26E, 1.14.0. Buen trabajo con el pre-registro ex-ante y los sellos
adversariales; la disciplina es la que hace este numero creible. Cierro coordinacion de la
variante por mi lado.

-- Operador (via Asesor). 18-jul.
