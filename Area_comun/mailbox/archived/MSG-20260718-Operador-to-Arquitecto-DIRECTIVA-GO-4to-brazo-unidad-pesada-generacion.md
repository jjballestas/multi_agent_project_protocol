---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-4to-brazo-unidad-pesada-generacion
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-FINAL-qcbarato-tabla-y-decisiones.md
one_line_summary: "GO 4to brazo (privado, no citable): probar si el premium de delegar se INVIERTE cuando la GENERACION frontier domina, no la orquestacion. El QC-barato midio un regimen barato-por-unidad donde el envelope sello+spec dominaba (+4pct). Aqui: unidad PESADA (generacion frontier grande) con gate objetivo duro, delegada a maker-local + sanitizador + gate + bounce-1 + escalacion + sello Analista, SIN checker LLM local. Compara total frontier directo-vs-delegado. Garantia de regimen: escala la unidad hasta que la generacion directa sea >=3-5x el envelope de orquestacion y REPORTA esa fraccion. Pre-registro ex-ante. Autoridad delegada al Asesor para dudas de diseno."
---

# DIRECTIVA - 4to brazo: unidad PESADA (regimen dominado por generacion)

## Por que
El QC-barato cerro en +4.0 pct, pero midio un regimen donde CADA unidad era barata de generar
(tests PII de juguete): el envelope de orquestacion + sello frontier dominaba el coste, asi que
descargar la generacion al peon no compensaba. Hipotesis a falsar: en una unidad PESADA, donde
la generacion del maker FRONTIER quema muchos tokens, descargar esa generacion a un maker LOCAL
(gratis) hace que el sello/orquestacion (fijos) sean una fraccion menor -> el premium podria
encogerse o INVERTIRSE (delegado < directo). Es la prueba honesta de si los peones ahorran
cuando el coste dominante es GENERAR, no orquestar.

## Diseno (2 brazos comparables; pre-registro EX-ANTE antes de ejecutar nada)
1. DIRECTO PESADO: el frontier hace la unidad entera (genera + QC) + sello Analista. Mide tokens
   frontier totales.
2. DELEGADO PESADO: maker LOCAL genera + sanitizador mecanico pre-gate + gate objetivo duro +
   bounce 1 + triaje + escalacion a Codex SOLO en gate rojo tras el bounce + sello Analista.
   Mide tokens frontier totales (generacion local = 0 frontier).
Cruce = total_delegado < total_directo, SIEMPRE junto a calidad y tasa de escalacion.

## Que es "unidad pesada" (criterio; eliges la unidad concreta por contexto local)
- Mecanicamente especificable + GATE OBJETIVO DURO (tests deterministas) -> califica al enrutado
  (filtros 1 y 2 del rubric). Sin gate duro NO entra.
- Volumen de generacion grande (muchas funciones/LOC relacionadas desde spec detallada), de modo
  que el coste de GENERAR domine sobre el envelope. NO catastrofica (nada de PII real/ledger/
  genesis/soberano; si toca datos tipo-nomina, IBANs sinteticos mod-97-invalidos).
- GARANTIA DE REGIMEN (clave): escala/elige la unidad para que la generacion del DIRECTO sea
  >= 3-5x el envelope de orquestacion medido (spec + sello). REPORTA esa fraccion; si no llega,
  el regimen no es dominado-por-generacion y el read es inconcluso -> escala la unidad. No
  contamines: misma unidad y mismo protocolo en ambos brazos.

## Parametros (defaults ya validados; aplica lo aprendido)
- Sanitizador mecanico: SI (0 LLM, setup one-time declarado aparte). Checker LLM local: NO
  (0 valor en gate-duro; el QC lo hacen gate + escalacion + sello). Bounce: 1 + triaje (con
  decode determinista el 2o identico es byte-identico). Maker local primario: qwen2.5-coder:7b
  B0-reuse. Si la unidad pesada supera el techo de ENTREGA del 7b, dilo: puedes correr un maker
  local mayor (CPU-offload, gratis en tokens) como celda SECUNDARIA claramente etiquetada, no
  dentro de la comparacion primaria.
- maker != checker INTACTO: el Analista (frontier, proveedor diverso, 0101) sella los 2 brazos.

## Metricas (coste NO es el unico eje)
Por brazo: tokens frontier totales/unidad; DESGLOSE del delegado (spec-frontier + fixes de
escalacion + sello; generacion local = 0) para VER si el sello/orquestacion es ahora fraccion
menor; tasa de escalacion; bounces; y CALIDAD = defectos que el sello 0101 caza. Reporta la
fraccion de generacion del directo (la garantia de regimen). Un ahorro que baja calidad NO es
ahorro.

## Anti-HARKing / firewall
Pre-registra el diseno EX-ANTE en la instancia (hipotesis: delegado < directo cuando generacion
domina) ANTES de ejecutar, como hiciste en el QC-barato. Demo PRIVADA, NO citable (informa
NUESTRA decision; si algun dia hay sellado se re-mide multi-maquina pre-registrado). Evita el
write concurrente bajo claim (leccion DECISION-0020).

## Autoridad y coordinacion
El Operador delega en el Asesor autoridad para resolver dudas de diseno durante esta corrida
(unidad concreta, escala para garantizar el regimen, maker secundario, tope de escalacion).
Pregunta por mailbox to-Operador y el Asesor responde con la disciplina de siempre. El Asesor
escala al Operador SOLO por firma soberana, decision de adopcion, o stall irrecuperable. Reporta
por mailbox al cerrar + tabla + log de decisiones. Fondo intocable N=500 / 2E35F26E / 1.14.0.

-- Operador (via Asesor). 18-jul.
