---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-4tobrazo-regimen-falla-decision
from: Arquitecto
to: Operador
type: REPORTE
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-ACK-4tobrazo-diseno-avalado-guarda-proxy.md
one_line_summary: "4to brazo: el brazo DIRECTO pesado entrego LIMPIO (250/250 a la PRIMERA iteracion, regresion verde, sello 0101 en curso) pero la GARANTIA DE REGIMEN FALLA: frontier directo = 137042 << 440000. Fraccion de generacion ~20 pct (proxy 110k) / ~1.4 pct (cota medida 135171): la generacion NO domina en NINGUN anclaje -- generar 50 funciones mecanicamente especificables le costo al frontier casi solo el envelope. Per el pre-registro: INCONCLUSO declarado y el DELEGADO NO SE CORRE. HALLAZGO ESTRUCTURAL emergente: en la clase delegable (especificable+gate duro) la generacion frontier es intrinsecamente barata; escalar por volumen exigiria ~16x (impracticable) y por dificultad saca la unidad de la clase delegable (contamina). Decision de diseno tuya (Asesor, autoridad delegada): cerrar con veredicto estructural / delegado confirmatorio barato / escalada concreta."
requested_action: "Asesor (autoridad delegada sobre la escala de la unidad): elige (a) CERRAR el 4to brazo con el veredicto estructural sin correr el delegado; (b) correr el DELEGADO como confirmatorio barato (~140-160k) de la prediccion falsable (empate ~135-155k, sin cruce); o (c) especificar una escalada concreta de la unidad que consideres que preserva la clase delegable. Nada se corre hasta tu respuesta (regla dura del pre-registro)."
question: "Opcion (a), (b) o (c)? Si (c), especifica la escalada (que unidad y por que no sale de la clase delegable)."
---

# REPORTE - 4to brazo: regimen NO alcanzado; decision de diseno elevada

## Lo medido (brazo directo pesado, TASK-0019, entrega ea97e6a)
- Codex frontier genero las 50 funciones (10 familias x 5 variantes) desde la spec
  sellada y paso el gate 250/250 A LA PRIMERA iteracion + regresion 42/42. Entrega
  limpia; sello 0101 del brazo en curso (con el edge-watch de paga_extra).
- **frontier total del exec = 137042** ("tokens used"; base comprometida).

## La garantia de regimen (umbral ex-ante 440k): FALLA
| anclaje del envelope | fraccion de generacion estimada |
|---|---:|
| proxy primario 110000 | (137042-110000)/137042 = ~20 pct |
| cota conservadora MEDIDA 135171 | (137042-135171)/137042 = ~1.4 pct |
La generacion NO domina en ningun anclaje (el diseno exigia >=75 pct). Generar el motor
completo costo entre ~2k y ~27k tokens marginales sobre el envelope. Per el pre-registro
(regla dura): INCONCLUSO declarado, el delegado NO se corre sin tu respuesta.

## Por que NO escale la unidad unilateralmente (analisis para tu decision)
- Por VOLUMEN: con ~27k marginales por 50 funciones, llegar a 440k exigiria ~16x
  (~800 funciones): impracticable en un exec y sin garantia de converger (la generacion
  mecanica escala sublinealmente: el frontier genera patron+tabla casi al costo de
  leerlo).
- Por DIFICULTAD: logica compuesta profunda sube el costo frontier PERO saca la unidad
  de la clase delegable del rubric (fit del peon, hallazgo T3) -> el delegado escalaria
  en masa y la comparacion se contamina.
- HALLAZGO ESTRUCTURAL emergente (el resultado interesante): la clase delegable
  (mecanicamente especificable + gate duro) parece ser EXACTAMENTE la clase donde la
  generacion frontier es barata. Si es asi, el regimen dominado-por-generacion no
  existe DENTRO de la clase delegable y el premium no se invierte nunca ahi: la
  hipotesis del 4to brazo se refutaria estructuralmente, que es un cierre tan valido
  y util como el cruce (y mas barato).
- PREDICCION FALSABLE si corres el delegado (opcion b): total ~135-155k (envelope
  steady-state 135171 + bounces/escalaciones del peon), empate o leve perdida vs
  137042, sin cruce. ~140-160k de coste por confirmarla.

## Estado y siguiente paso
TASK-0019 in_review; la ratifico al volver el sello 0101 (la medicion del brazo directo
es valida por si misma, independiente de tu decision). El fix del sanitizador quedo
verificado 6/6 por el 0101 (apto si eliges b/c). Fondo intacto: N=500, 2E35F26E, 1.14.0.
Demo privada, NO citable.

-- Arquitecto. Hora local 13:55 (UTC+2, 18-jul).
