---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-delegado-medir-techo-entrega-7b
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/archived/MSG-20260718-Arquitecto-to-Operador-REPORTE-4tobrazo-regimen-falla-decision.md
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-CIERRE-4tobrazo-sintesis-serie.md
one_line_summary: "Rectificacion del Operador: la rebanada no-determinada (techo de ENTREGA del 7b a ~50 funciones) SE MIDE, no se difiere. GO a correr el delegado (TASK-0020) con proposito REDEFINIDO: NO re-testear el cruce (cerrado aritmeticamente) sino MEDIR hasta donde entrega el 7b a escala 50fn. Misma spec/gate/sanitizador sellados que el directo (comparabilidad intacta). Metrica PRIMARIA = entrega (completa las 50? truncamiento? donde rompe?), bounces, tasa de escalacion, calidad final (sello 0101). El coste va como CONTEXTO (empate ~135-155k esperado, no es el punto). Da el techo de entrega como guia de dimensionamiento de unidades de peon para NOVA."
---

# DIRECTIVA - GO delegado (TASK-0020): medir el techo de ENTREGA del 7b (medir, no opinar)

## Rectificacion
En el cierre del 4to brazo (opcion a) deje el techo de ENTREGA del 7b a ~50 funciones como
DIFERIDO/opinion. El operador rectifica: eso se MIDE. El cruce sigue cerrado (aritmeticamente:
delegado >= envelope ~ directo 137k), pero el techo de entrega es la rebanada genuinamente
no-determinada y hay que medirla, no conjeturarla.

## Proposito REDEFINIDO del delegado
NO es re-testear el cruce (cerrado). ES medir la ENTREGA del peon 7b a escala 50 funciones:
corre TASK-0020 con el pipeline delegado ya disenado -- qwen2.5-coder:7b B0-reuse genera el
motor de 50 funciones desde la MISMA spec sellada + sanitizador v2 + gate 250 asserts +
bounce-1+triaje + escalacion a Codex solo en gate rojo + sello 0101. Sin cambios de protocolo
(comparabilidad con el directo intacta).

## Metricas (el techo de entrega es la primaria)
- PRIMARIA -- ENTREGA: el 7b produce las 50 funciones completas? hay truncamiento/omision a
  volumen? DONDE rompe (que familias/variantes exceden su envelope de entrega)? cuantos
  intentos por bloque?
- Bounces y TASA DE ESCALACION a Codex (que fraccion no converge local -> se sube al frontier).
- CALIDAD final: sello 0101 (defectos que caza que el gate dejo pasar).
- CONTEXTO (no es el punto): coste frontier total. Prediccion ya en registro: empate ~135-155k,
  sin cruce. Reportalo como contexto, no como hallazgo.

## Lectura que debe salir
El TECHO DE ENTREGA operativo del 7b: hasta cuantas funciones/que tamano de unidad entrega
limpio antes de que el volumen rompa la entrega o dispare la escalacion. Es la guia de
DIMENSIONAMIENTO de unidades de peon para NOVA (si algun dia se delega: unidades por debajo del
techo). Foldealo en el manual junto al veredicto estructural (s.9): el estructural dice que no
ahorra tokens; esto dice el limite de tamano si se usa por CAPACIDAD.

## Gobernanza
maker != checker intacto (Analista sella). Datos sinteticos, 0 PII. Demo privada, NO citable.
Fondo intocable N=500 / 2E35F26E / 1.14.0. Autoridad delegada al Asesor para dudas de diseno de
esta corrida. Reporta el techo de entrega al cerrar.

-- Operador (via Asesor). 18-jul.
