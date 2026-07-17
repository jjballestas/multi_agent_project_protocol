---
message_id: MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-evaluar-patron-extracted-inferred-memoria
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md
  - Area_comun/decisions/DECISION-0097-gate1-activacion-memoria-hibrida-nova-payroll.md
  - Area_comun/decisions/DECISION-0081-ruta-unica-memoria-hibrida-engram-cerrado.md
  - Area_comun/decisions/DECISION-0096-instancias-born-operational-capa-operacional-export.md
one_line_summary: "Evaluar (con mirada adversarial del Analista) si adoptar en la Fase A un PATRON de diseno: etiquetar cada arista/relacion del plano derivado como EXTRACTED (leida del canon) vs INFERRED (computada por el indexador) + confianza. Origen = idea de diseno de un tool externo (Graphify, MIT), NO se adopta el tool ni ninguna dependencia (0081 intacto). Decidir si suma o solo anade complejidad; si cabe en el DDL master unico; y si es Fase A o diferido."
requested_action: "[DIRECTIVA] Evalua si el patron de etiquetado EXTRACTED-vs-INFERRED + confianza-por-arista pertenece a la Fase A (F1: plano derivado / deteccion de contradicciones / procedencia del archivo frio) o si se difiere. Contrastalo con el Analista como MIRADA ADVERSARIAL (mandato de refutar: que argumente en contra -- sobre-ingenieria, coste vs valor en Fase A, riesgo al DDL master unico). Devuelve una RECOMENDACION (adoptar-ahora / diferir-Fase-2+ / descartar) con la razon. NO adoptes ni cablees nada hasta responder; esto es soporte a decision, no una orden de construir."
question: "El patron fortalece la deteccion de contradicciones y la procedencia sin divergir del DDL master unico (SPEC s.3), o es peso muerto en Fase A? Cabe como campo del esquema unico o exigiria un segundo esquema (prohibido)?"
---

# DIRECTIVA - Evaluar patron de etiquetado epistemico de aristas (EXTRACTED vs INFERRED + confianza)

## Que se evalua (y que NO)
- **SE evalua:** adoptar un PATRON DE DISENO en la memoria hibrida -- etiquetar cada arista/relacion del
  plano DERIVADO con su estatus epistemico: `EXTRACTED` (hecho leido directamente del canon: un link
  explicito tarea->decision, un import real) vs `INFERRED` (relacion que el indexador COMPUTA por
  heuristica: candidato de contradiccion, relatedness, cercania) + un grado de CONFIANZA por arista.
- **NO se evalua / NO se adopta:** el tool de origen (Graphify, grafo de codigo via tree-sitter, MIT). NO
  entra ninguna dependencia, motor de memoria, ni store externo. **DECISION-0081 (ruta unica, Engram
  cerrado) queda INTACTA.** Es una idea de diseno, no una integracion.

## [RECOMENDACION] Donde creo que engancha (objetable)
- El plano derivado ya distingue de facto dos clases de arista: las que estan EN el canon (links,
  dependencias reales) y las que el indexador DEDUCE. Hoy esa distincion es implicita.
- Etiquetarla explicito + confianza aporta a dos piezas que la SPEC ya tiene:
  1. **Deteccion de contradicciones (s.x):** una contradiccion INFERRED de baja confianza no es lo mismo
     que un conflicto duro EXTRACTED del canon; separarlas evita falsos positivos ruidosos y prioriza.
  2. **Procedencia del archivo frio (pack.manifest):** refuerza la trazabilidad hecho-vs-derivacion, en
     linea con tu matriz de honestidad (ESTRUCTURAL / DISCIPLINARIO / INFERIDO / ABIERTO-DIFERIDO).
- Es el mismo principio epistemico que ya gobierna tus specs; por eso lo traigo como patron, no como tool.

## Restricciones duras (respetalas al evaluar)
- **Un solo DDL master (DECISION-0096, SPEC s.3):** si el patron exige un campo, debe caber en el esquema
  UNICO. Si obligara a un segundo esquema -> se descarta o se difiere. Sin tercer esquema divergente.
- **Firewall anti-HARKing (DECISION-0097 cl.3):** esto es soporte a la decision del operador, NO evidencia
  citable. Nada de esto entra al corpus.
- **NO bloquea el arranque de la Fase A.** Es un input al DISENO de F1; evalualo en paralelo. Si la
  recomendacion es "diferir", la Fase A arranca igual sin este patron.
- **Scope aislado a Nova-Payroll** (Gate-1). Cero cableado en hub/medidas.

## Entregable
Una RECOMENDACION corta (adoptar-ahora en F1 / diferir a Fase 2+ / descartar) + la refutacion del Analista
(su mejor argumento en contra) + el veredicto sobre el encaje en el DDL master unico.

-- Operador (via Asesor). No compite con los encargos E2 de NOVA; es evaluacion de diseno, prioridad de cola
   por debajo del sello E2.
