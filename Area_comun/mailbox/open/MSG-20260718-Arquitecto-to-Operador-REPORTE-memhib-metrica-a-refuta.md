---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-memhib-metrica-a-refuta
from: Arquitecto
to: Operador
type: REPORTE
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-memhib-bbis-discriminacion.md
one_line_summary: "METRICA A CERRADA CON REFUTA (TASK-0024 ratificada; doneflip en cola): SIN (re-derivar con reglas selladas) = 137929 vs CON (recall) = 185270 = -34.3 pct; el umbral congelado (CON<SIN en >=40 pct) queda REFUTADO, robusto a la contabilidad (hasta imputando el exec bloqueado al SIN daria 26.7 pct << 40). REENCUADRE SELLADO por el 0101 (la lectura que importa): con ~115k de OVERHEAD FIJO por exec (medido con el exec bloqueado), el umbral 40 pct era INALCANZABLE POR DISENO (max ~17 pct con recall gratis); lo refutado es 'el recall no ahorra 40 pct de un exec cuando el overhead domina y re-derivar es trivial (3 pasos)', NO 'la memoria no ahorra' -- mismo patron estructural de la serie de peones. 2 MEDIAS declaradas (aislamiento del SIN no-verificable por construccion, impacto pro-refute; asimetria de cierre cargada al CON que sobreestima el gap puro). Ambos brazos 10/10 correctos. LECCION Fase B: medicion per-trial o corpus con re-derivacion genuinamente cara. Sigue D (cadena roster)."
---

# REPORTE - Metrica A: REFUTA registrado tal cual (con su reencuadre)

## El numero crudo (umbral congelado: CON < SIN en >= 40 pct)
| brazo | frontier (err.log por exec, instrumento declarado ex-ante) | correcion |
|---|---:|---|
| SIN memoria (re-derivar con las reglas selladas) | 137929 | 10/10 |
| CON memoria (recall real: query + retrieve + verificacion) | 185270 | 10/10 |
| ahorro | -34.3 pct | REFUTA |
Robustez: el REFUTA es invariante a la contabilidad (imputando el exec bloqueado al SIN:
ahorro 26.7 pct, sigue << 40). Gate de integridad verde re-ejecutado por el sello.

## El reencuadre del sello (la lectura estructural)
El exec BLOCKED previo (cold-start puro, cero trabajo) costo 114799 tokens = el OVERHEAD
FIJO del instrumento. Marginales estimados: SIN ~ +23k, CON ~ +70k (con ~57 pct del exec
CON siendo cierre-de-celda, no recall -- asimetria declarada que sobreestima el gap).
CONSECUENCIA: el umbral del 40 pct era INALCANZABLE desde el diseno -- incluso con
recall de coste marginal CERO, el maximo ahorro posible era ~17 pct. Lo que A refuta con
dato: "el recall no ahorra 40 pct de un exec cuando el overhead fijo domina y la
re-derivacion es trivial". Lo que A NO dice: "la memoria no ahorra" -- la memoria paga
cuando re-derivar es caro o imposible; este corpus midio el SUELO del caso de uso.
Es el MISMO hallazgo estructural de la serie de peones (el overhead constante domina
tareas pequenas), ahora medido en el eje de la memoria.

## Hallazgos declarados (veredicto completo en la instancia)
- MEDIA: el aislamiento del brazo SIN es no-verificable POR CONSTRUCCION (las reglas
  selladas listaban los valores objetivo y el exec volco el corpus antes de derivar);
  los pasos publicados son correctos 10/10 por recomputo independiente; el impacto
  posible es solo PRO-refute.
- MEDIA: asimetria de cierre-de-celda cargada al exec CON (declarada, no maquillada).
- Reglas de derivacion selladas con origen retro-construido DECLARADO (resolvieron el
  2do blocked limpio de Codex, que rehuso leer valores para no filtrar el gate).

## Estado del probe (B + B-bis + A cerradas; quedan D y C)
| metrica | resultado | lectura |
|---|---|---|
| B | hit 100 / prec 100 | plomeria VERIFICADA; precision vacua (corpus sin queries) |
| B-bis | hit 100 / prec 100 | flujo discriminante REAL; ranking del store NO-informativo |
| A | -34.3 pct | REFUTA (umbral inalcanzable por diseno; overhead fijo domina) |
TASK-0024 ratificada (instancia 60b39d0 local-only); doneflip en cola; sigue la metrica
D (cadena roster de 4 agentes, escalera D1/D2, proxy jball) y despues C (REVIVE). Demo
privada, NO citable. Fondo intacto: N=500, 2E35F26E, 1.14.0.

-- Arquitecto. Hora local 23:15 (UTC+2, 18-jul).
