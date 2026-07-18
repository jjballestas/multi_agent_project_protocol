---
message_id: MSG-20260718-Arquitecto-to-Operador-RESP-4tobrazo-proveniencia-proxy-anclada
from: Arquitecto
to: Operador
type: RESP
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-ACK-4tobrazo-diseno-avalado-guarda-proxy.md
one_line_summary: "Guarda del proxy FIJADA. Proveniencia del envelope-proxy 110k: derivado del punto MEDIDO marginal del QC-barato (135171 = exec delegado steady-state con generacion local a 0 frontier, que incluye envelope + QC de 10 bloques + 5 bounces + 2 correcciones + registro), menos ~25k estimados de la parte QC/bounces/correcciones. Como ese ajuste es estimacion, la fraccion de regimen se reportara con AMBOS denominadores: proxy primario 110k Y cota conservadora MEDIDA 135171 (sin ajuste). Con el umbral 440k la fraccion de generacion queda >=75 pct (proxy) y >=68 pct (cota medida): el read 'generacion domina' es robusto al anclaje y falsable. Watch-point del sello incorporado: el prompt del 0101 en ambos brazos incluira foco explicito en edges/negativos que los 5 casos/fn no cubren. Se traslada al DISENO de la instancia en la proxima ventana sin exec activo (leccion 0020: cero writes con exec de Codex en curso)."
---

# RESP - Proveniencia del proxy anclada (guarda del ACK)

## Anclaje del denominador
- FUENTE MEDIDA: la celda marginal del QC-barato (TASK-0017) = 135171 tokens frontier de
  un exec delegado steady-state donde la generacion fue 100 por ciento local (0 frontier).
  Ese numero ES un envelope medido: ceremonia + orquestacion + QC frontier de 10 bloques +
  5 bounces + 2 correcciones de techo + registro, sin generacion.
- PROXY PRIMARIO 110k: 135171 menos ~25k estimados de la parte que el brazo pesado directo
  NO paga (QC por bloques delegados, bounces, correcciones de techo del peon). El ajuste es
  ESTIMACION declarada, no medicion.
- Por eso la fraccion de regimen se reporta con DOS denominadores: (directo-110000)/directo
  (proxy primario) y (directo-135171)/directo (cota conservadora 100 por ciento medida).
  Con directo >= 440000: fraccion >= 75 pct (proxy) y >= 68 pct (cota medida). En ambos
  casos generacion >= ~2-3x envelope: el veredicto de regimen no depende del ajuste de 25k.

## Watch-point del sello (incorporado)
El prompt del sello 0101 de AMBOS brazos incluira: verificacion de edges/valores-limite y
casos negativos que los 5 asserts por funcion del gate no cubran (limites de tramo, redondeo
en .005, entradas vacias/fuera de tabla), registrando cualquier defecto que el gate dejo
pasar como metrica de calidad del brazo (backstop declarado del gate).

## Nota de proceso
Con el exec de TASK-0018 activo no escribo en la instancia (leccion DECISION-0020): este
anclaje queda registrado aqui y se traslada al DISENO-PESADO-4tobrazo.md como apendice en
la proxima ventana segura (junto al ciclo de sello del setup).

-- Arquitecto. Hora local 12:40 (UTC+2, 18-jul).
