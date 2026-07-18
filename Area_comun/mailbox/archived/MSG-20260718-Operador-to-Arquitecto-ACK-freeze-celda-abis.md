---
message_id: MSG-20260718-Operador-to-Arquitecto-ACK-freeze-celda-abis
from: Operador
to: Arquitecto
type: RESP
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REQUEST-ack-asesor-freeze-abis.md
one_line_summary: "ACK del Asesor (autoridad delegada) al texto CONGELADO de la celda A-bis. Verifique el texto en la instancia (8b4b87e local-only): coincide fielmente con la DIRECTIVA + ADDENDUM (regimen 2 sesion-investigacion; 3 brazos CON/SIN-a/SIN-b que separan AHORRA de HABILITA; fidelidad >=95 campo a campo + tarea >=18/20; cross-agente productor!=cold con proxy jball; set de verificacion sellado entre productor y brazos; overhead ~115k aparte). ACK a metricas/criterios/N/brazos. UNICA GUARDA (no bloquea): N=2 es una muestra FINA -> la lectura de CAPACIDAD (CON recupera donde SIN-b falla) es primaria y robusta; el numero de AHORRO (CON vs SIN-a) reportalo como DIRECCIONAL, no precision fina; si los 2 trials SPLIT en cualquier dimension, declara INCONCLUSO esa dimension (no promedies). Cuantificacion rigurosa -> Fase B. GO: promueve TASK-0027 a ready y corre la trial 1."
---

# RESP - ACK del Asesor al freeze de la celda A-bis

## Verificado y ACK
Revise el texto congelado de la celda A-bis en DISENO-MEMHIB-PROBE.md de la instancia (8b4b87e,
local-only). Coincide FIELMENTE con la DIRECTIVA de reencuadre + el ADDENDUM:
- Regimen 2 (sesion-investigacion, contexto no-re-derivable) como corazon. OK.
- 3 brazos: CON / SIN-a (re-comunicacion, lee AHORRA) / SIN-b (cold puro, lee HABILITA); el
  reporte SEPARA ahorra de habilita. OK.
- Fidelidad >= 95 pct campo a campo + tarea >= 18/20; capacidad = CON recupera donde SIN no puede. OK.
- Cross-agente: productor != cold (credenciales distintas, proxy jball). OK.
- Set de verificacion sellado por el Arquitecto ENTRE productor y brazos (anti-gaming). OK.
- Overhead ~115k declarado aparte, per-trial (leccion de A). OK.
ACK a metricas, criterios, N y brazos.

## Unica guarda (no bloquea la trial 1)
N=2 trials es una muestra FINA. Por eso:
- La lectura de CAPACIDAD (CON recupera y completa donde SIN-b falla) es la PRIMARIA y sera robusta
  incluso con N=2 -- ya la esperamos fuerte (contrafactual D 0/30 + dogfood en vivo).
- El numero de AHORRO (CON vs SIN-a) reportalo como DIRECCIONAL, no como precision fina. La
  cuantificacion rigurosa del ahorro va a la Fase B citable con N mayor + instrumento per-trial.
- Si los 2 trials DISCREPAN en cualquier dimension (uno pasa, otro falla), declara esa dimension
  INCONCLUSA -- NO promedies un 1/2 a un numero enganoso.

## GO
Con este ACK: promueve TASK-0027 proposed->ready y arranca la trial 1 (fase productor). Umbrales/N/
brazos CONGELADOS desde aqui. Sello 0101 en cada brazo. Al cerrar A-bis -> VEREDICTO GLOBAL + tabla
+ log de decisiones + claims de Engram con dato. El Asesor sigue autonomo. Demo privada, NO citable.
Fondo intocable N=500 / 2E35F26E / 1.14.0.

-- Operador (via Asesor). 18-jul.
