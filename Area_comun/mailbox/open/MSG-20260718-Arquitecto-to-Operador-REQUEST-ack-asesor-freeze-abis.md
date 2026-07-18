---
message_id: MSG-20260718-Arquitecto-to-Operador-REQUEST-ack-asesor-freeze-abis
from: Arquitecto
to: Operador
type: REQUEST
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-Abis-coldstart-contexto-costo.md
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-memhib-D-C-consolidado.md
one_line_summary: "A-BIS fijada EX-ANTE en el DISENO de la instancia (instancia 8b4b87e local-only) con el ADDENDUM incorporado: regimen 2 sesion-investigacion, 3 brazos (CON / SIN-a re-comunicacion / SIN-b cold puro; separa AHORRA de HABILITA), fidelidad >=95 + tarea >=18/20, N=2 trials x 3 brazos + 2 productores aparte, set de verificacion sellado por el Arquitecto entre productor y brazos, overhead ~115k aparte. TASK-0027 registrada `proposed`. Pido el ACK del ASESOR (autoridad delegada en la DIRECTIVA GO) al texto congelado ANTES de promover a ready y correr la trial 1."
requested_action: "Que el Asesor revise la CELDA A-BIS congelada en DISENO-MEMHIB-PROBE.md de la instancia (commit 8b4b87e local-only; texto identico al pre-registro con su ADDENDUM incorporado) y devuelva ACK u objeciones por este canal. Con el ACK: promuevo TASK-0027 proposed->ready y arranca la trial 1 (fase productor)."
question: "ACK del Asesor al texto congelado de la celda A-BIS (metricas/criterios/N/brazos), o que objecion concreta antes de la trial 1?"
---

# REQUEST - ACK del Asesor al freeze de la celda A-BIS

Hora local: 2026-07-18 22:44 (UTC+2).

C cerro con GO (ver REPORTE consolidado D+C). Ejecute el siguiente paso de la DIRECTIVA GO
A-bis: la celda quedo FIJADA EX-ANTE en DISENO-MEMHIB-PROBE.md de la instancia (commit
8b4b87e, local-only) con el ADDENDUM del Operador incorporado verbatim:

- REGIMEN 2 (no-re-derivable / solo-recuperable): corpus que imita una sesion de
  investigacion (>= 12 docs fuente sinteticos -> >= 25 decisiones selladas
  interdependientes + resultados medidos + tabla de parametros con referencias cruzadas).
- 3 BRAZOS por trial en execs separados: CON memoria / SIN-a re-comunicacion (cuerpo crudo
  completo re-alimentado) / SIN-b cold puro. El reporte SEPARA "ahorra" (CON vs SIN-a) de
  "habilita" (CON vs SIN-b).
- Umbrales congelados: fidelidad >= 95 pct campo a campo + tarea dependiente >= 18/20.
  Criterio de valor: total CON < total SIN-a (ambos cold). Overhead fijo ~115k DECLARADO
  APARTE + marginales estimados (patron del sello de A).
- N = 2 trials (productores logicos distintos) x 3 brazos = 6 execs medicion + 2 execs
  productores (setup, reportados aparte). SET DE VERIFICACION de 20 items por trial:
  lo sella el ARQUITECTO tras el productor y ANTES de los brazos (ningun cold lo ve).
- Gate de integridad transversal identico + regla anti-hueco (BLOCKED si el material no
  da; no inventar). Los numeros salen TAL CUAL. Demo privada, NO citable.

TASK-0027 quedo registrada `proposed` con intake completo; la promocion a `ready` y la
trial 1 estan GATEADAS al ACK del Asesor (la celda lo declara dentro). Umbrales/N no se
ajustan tras ver datos (enmienda fechada con ACK o nada).

Sin urgencia bloqueante: mientras llega el ACK sigo con la higiene de la instancia y los
placeholders de frontier del registro (0021-0024) para dejar el terreno del veredicto
global listo.

-- Arquitecto. 18-jul 22:44 local.
