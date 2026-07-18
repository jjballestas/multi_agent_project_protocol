---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-variante-QC-barato-3-condiciones
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-FINAL-piloto-cerrado-manual-nova-v1.md
one_line_summary: "GO a la variante QC-barato en 3 condiciones sobre la misma familia comparable al +7%: (1) baseline directo (2) arm3 sanitizador+maker-local+checker-CODEX+gate+Analista (3) arm2 sanitizador+maker-local+checker-LOCAL familia-distinta+gate+Analista+Codex-escalacion. Mide coste + escalacion + CALIDAD (defectos que caza el Analista y el checker dejo pasar). El Asesor tiene autoridad delegada del Operador para resolver dudas de diseno durante la corrida. Demo NO citable."
---

# DIRECTIVA - Variante QC-barato: 3 condiciones (autonoma)

## Objetivo
El piloto cerro en NO-CRUCE: delegar da premium ~+7 pct constante, y ese +7 pct es el QC de
Codex (frontier). Hipotesis: si abaratamos la VERIFICACION (sanitizador + checker no-frontier),
el premium puede cruzar a negativo. FrugalGPT ahorra con scorer BARATO + escalacion; nuestro
primer probe pagaba frontier en el QC de CADA tarea (no era FrugalGPT). Estas 3 condiciones
aplican el metodo probado como corresponde y miden si cruza.

## Diseno (2 factores; misma familia, comparable al +7 pct del grid)
Usa una familia comparable a la de escala/lote-100 (la del +7 pct) para que los numeros sean
contrastables. maker = modelo local; checker de familia DISTINTA al maker (hallazgo T3 de fit:
deepseek fuerte en logica, qwen en formato -> puntos ciegos no solapados).
1. BASELINE DIRECTO -- referencia (frontier hace todo).
2. ARM 3 (conservador): sanitizador pre-gate + maker-local + checker-CODEX (frontier) + gate
   duro claro + Analista sella. AISLA el efecto del sanitizador sobre el brazo de QC fiable.
3. ARM 2 (agresivo): sanitizador pre-gate + maker-local + checker-LOCAL (familia distinta) +
   gate duro claro + Analista sella + Codex SOLO en escalacion (no-go tras tope de bounces).
   Mueve el QC a local gratis; mide si el checker local hace converger el loop.

## Lecturas que deben salir
- Efecto SANITIZADOR = arm3 vs el +7 pct original (mismo checker-Codex, difieren en sanitizador).
- Efecto CHECKER local-vs-Codex = arm2 vs arm3 (mismo sanitizador, difieren en quien revisa).
- Cual (si alguno) CRUZA por debajo del directo, y A QUE CALIDAD.

## Metricas (coste NO es el unico eje)
Por condicion: tokens frontier por unidad; tasa de ESCALACION a Codex (cuantas no convergen
local); numero de bounces; y CALIDAD = defectos que caza el Analista que el checker (local o
Codex) dejo pasar. Un ahorro que baja la calidad NO es ahorro. Reporta las tres dimensiones.

## Gobernanza (no negociable)
maker != checker se preserva: el Analista (frontier, proveedor diverso, DECISION-0101) SIGUE
sellando en las 3 condiciones. El checker local/Codex es el pre-filtro barato de QC, NO
sustituye el sello del Analista. Sin PII al store; fondo intocable N=500 / 2E35F26E / 1.14.0.

## Autoridad y coordinacion
El Operador delega en el Asesor autoridad para resolver dudas de diseno y tomar decisiones
durante esta corrida (par de modelos, tamano de lote, familia exacta, tope de bounces del arm2,
criterio de escalacion). Si tienes una duda, preguntala por mailbox to-Operador y el Asesor
responde con la disciplina de siempre. El Asesor SOLO escala al Operador por: firma soberana,
decision de adopcion, o stall irrecuperable. Reporta por mailbox al cerrar cada condicion.

## Marco
Demo PRIVADA, NO citable (informa NUESTRA decision de si delegar ahorra; si algun dia hay
sellado se re-mide con rigor multi-maquina). Instrumento Codex CLI para el frontier; peones via
Ollama local. Entrega la tabla final de 3 condiciones + el log de decisiones al cierre.

-- Operador (via Asesor). 18-jul.
