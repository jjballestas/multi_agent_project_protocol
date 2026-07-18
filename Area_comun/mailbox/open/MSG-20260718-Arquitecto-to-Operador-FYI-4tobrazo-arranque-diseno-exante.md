---
message_id: MSG-20260718-Arquitecto-to-Operador-FYI-4tobrazo-arranque-diseno-exante
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-4to-brazo-unidad-pesada-generacion.md
one_line_summary: "DIRECTIVA 4to brazo TOMADA. Pre-registro EX-ANTE en la instancia (DISENO-PESADO-4tobrazo.md, commit 6c3cac6) ANTES de ejecutar. Unidad elegida: MOTOR DE NOMINA SINTETICO (50 funciones = 10 familias x 5 variantes, patron+aritmetica-de-tabla fit-7b, todo sintetico) con gate de 250 asserts deterministas. Estructura: TASK-0018 setup medible (spec+gate+sanitizador-v2 = termino comun, YA en exec) -> TASK-0019 directo -> garantia de regimen (directo >= 440k ~ 4x envelope-proxy 110k; si no llega, DECLARO inconcluso y escalo la unidad ANTES del delegado) -> TASK-0020 delegado (7b B0-reuse + sanitizador + gate + bounce-1 + escalacion; SIN checker LLM local). Sello 0101 en ambos brazos, contabilidad simetrica pre-sello. Si el Asesor objeta unidad/umbral, corrijo por mailbox."
---

# FYI - 4to brazo: arranque con pre-registro ex-ante

## Decisiones de diseno declaradas (autoridad delegada del Asesor reconocida)
- UNIDAD: motor de calculo de recibo de nomina sintetico, 50 funciones (10 familias x 5
  variantes con tablas de parametros DISTINTAS), 5 casos exactos por funcion = gate de
  250 asserts exit-code. Califica al rubric (especificable + gate duro + familia repetida
  + no catastrofica). Dificultad deliberada patron+tabla (dentro del fit del 7b por T3).
- SETUP COMPARTIDO MEDIBLE (TASK-0018): la spec + el gate + el sanitizador v2 los autora
  CODEX en un exec propio -> spec-frontier medida por err.log, termino COMUN a ambos
  brazos (no va al per-brazo). El gate NO se valida contra implementacion de referencia
  (pre-generar la solucion contaminaria el directo): self-check estructural + sello.
- GARANTIA DE REGIMEN (umbral ex-ante): directo_total >= 440000 (~4x envelope-proxy
  110k, que implica generacion >= 3x envelope). Por debajo -> inconcluso declarado +
  escalar la unidad; el delegado NO corre hasta confirmar el regimen. La fraccion
  (directo-110k)/directo se reporta como estimacion declarada.
- Aplicado de una: sanitizador v2 (contrato QC-barato parametrizado), SIN checker LLM
  local, bounce tope 1 + triaje (decode determinista), maker primario qwen2.5-coder:7b;
  maker local mayor solo como celda SECUNDARIA etiquetada previa consulta.
- Leccion 0020 activa: cero writes mios en la instancia bajo claim de Codex.

## Estado
TASK-0018 ready + ACTION en exec (cron vivo). Cadena por tarea: sello 0101 ->
ratificacion -> doneflip -> siguiente (promocion de a una). Reporte por mailbox al
cerrar cada brazo + tabla final + log de decisiones. Demo privada, NO citable. Fondo
intacto: N=500, 2E35F26E, 1.14.0.

-- Arquitecto. Hora local 12:31 (UTC+2, 18-jul).
