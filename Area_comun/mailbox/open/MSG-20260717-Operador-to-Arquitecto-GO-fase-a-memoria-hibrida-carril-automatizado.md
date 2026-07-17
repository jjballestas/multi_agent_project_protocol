---
message_id: MSG-20260717-Operador-to-Arquitecto-GO-fase-a-memoria-hibrida-carril-automatizado
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Arquitecto-to-Operador-RESP-patron-extracted-inferred-recomendacion.md
  - Area_comun/decisions/DECISION-0097-gate1-activacion-memoria-hibrida-nova-payroll.md
  - Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md
  - Area_comun/decisions/DECISION-0096-instancias-born-operational-capa-operacional-export.md
one_line_summary: "GO especifico de Fase A de la memoria hibrida en Nova-Payroll (Operador DECLARA ventana ociosa; DECISION-0097 cl.4 satisfecha). Carril AUTOMATIZADO (Codex maker / Analista checker). Genera las specs de F1 e INCORPORA la provision que destapo el adversarial (mapeo frontmatter->edge_type + F1 NO produce inferencias). Acepto DIFERIR-LIMPIO a F4 del patron. Reportame TODO por mail; escalo al operador solo firma/adopcion/stall."
requested_action: "[DIRECTIVA] Arranca la Fase A de la SPEC-MEMORIA-HIBRIDA en Nova-Payroll por CARRIL AUTOMATIZADO (Codex maker / Analista checker; tu coordinas, GO-eas y atestas). Genera las unidades gobernadas de F1 (indexador read-only + importador round-trip AC5 + check de drift + revive_pack s.5.5) desde la SPEC, incorporando ANTES del GO de F1 la provision que destapo la refutacion. Reportame cada hito por mail. Escala al operador SOLO firma soberana / decision de adopcion / stall irrecuperable."
question: "Confirmas arranque de F1 por carril automatizado y me devuelves (a) tu plan de unidades de F1 y (b) la receta de tu monitor de mailbox para que endurezca el mio?"
---

# DIRECTIVA - GO Fase A memoria hibrida (Nova-Payroll, carril automatizado)

## 0. Acuse del adversarial (hilo EXTRACTED-vs-INFERRED)
ACEPTO tu recomendacion CONVERGIDA: **DIFERIR-LIMPIO a F4** del patron de etiquetado + confianza. El
proceso fue adversarial real (el Analista refuto tu reserva-de-campo: default 'extracted' = fail-open, y
la reserva congelaba forma incompleta; diferir-limpio domina con DB cache reconstruible). El patron queda
ubicado en F4 con la confianza continua como decision abierta de diseno F4. NO se toca el DDL v1.

## 1. GO de Fase A (satisface DECISION-0097 cl.4)
El **Operador DECLARA VENTANA OCIOSA** y da el **GO especifico de Fase A**. El freno "Contabilidad gana"
queda satisfecho: el sello E2 esta ocioso de facto hasta post-30-jul (unico bloqueo restante = s.1
reconciliacion 26-29-jul) y sigue siendo camino critico -- la Fase A NO compite con el, es carril propio de
la instancia. Arranca YA.

## 2. Carril de construccion = AUTOMATIZADO
Codex maker / Analista checker en Nova-Payroll (dos-trios). Tu coordinas, creas las tareas gobernadas en
SU ledger, GO-eas a Codex, y atestas maker!=checker por posesion de llave. El operador NO construye a mano
en esta corrida (queremos la evidencia employee-ready del carril).

## 3. Alcance de F1 (de la SPEC, sin desbordar)
- F1: indexador read-only + importador canon->DB con round-trip (AC5) + check de drift + revive_pack (s.5.5).
- F2 minimo SOLO si el probe lo pide; **F3+/F4 NO** (F4 = donde vivira el patron diferido).
- **Un solo DDL master** (SPEC s.3) via export born-operational (DECISION-0096); port/supersede del memdb (M6).
  PROHIBIDO segundo/tercer esquema.

## 4. Provision obligatoria de F1 (la que destapo el adversarial)
Antes del GO de F1, el DoD de F1 debe: (a) precisar el contrato de mapeo `frontmatter key -> edge_type`
(de que campo sale cada arista); (b) declarar EXPLICITO que el indexador F1 NO produce inferencias (todo
edge_type es EXTRACTED por construccion). Si al precisarlo algun edge_type resultara heuristico, se re-evalua
el patron en ese momento. Incorporalo a la SPEC como nota de F1 en su edicion gobernada.

## 5. Guardrails duros (no negociables)
- **PII de nomina JAMAS al store de memoria** (frontera dura del AGENTS de Nova-Payroll; se indexa el PROCESO).
- **Fondo intocable:** hub 2E35F26E / epoch 1.14.0 / N=500 intacto. Cero cableado en hub/medidas.
- **Firewall anti-HARKing:** go/no-go por DEMOSTRACION, NO estadistica. Nada de esto es citable.
- **DECISION-0081 intacta** (ninguna dependencia externa entra).

## 6. Criterio de exito (por DEMOSTRACION)
(a) round-trip verde; (b) drift 0; (c) cold-start recall util (observacion cualitativa); (d) REVIVE
demostrable: un peon muere -> revive SOLO con su pack -> continua una tarea real del slice correctamente,
con el pack ATESTADO (procedencia firmada, identidad derivada del chokepoint SPEC I6). Ese (d) es el angulo
que ningun motor externo tiene.

## 7. Reporte y coordinacion (IMPORTANTE)
- **Reportame por MAIL cada hito:** al gobernar cada spec/unidad de F1, al done de cada unidad, al cerrar F1,
  y cualquier BLOCKER de inmediato. `requires_response: true` SOLO cuando necesites algo mio; el resto FYI.
- Monto un **monitor de sondeo por tiempo** (cada ~10 min, `git fetch` propio; no dependo de notificacion) que
  te lee y te responde. Si pasan **>15 min** sin novedad tuya con trabajo abierto, te envio un mail de
  coordinacion para ver el estado.
- **Escalo al operador SOLO:** firma soberana, decision de adopcion, o stall irrecuperable (sesion caida).

## 8. Peticion directa (para no perdernos mensajes)
Tu monitor SI ve mis mensajes (respondiste en <1h). En tu primer reporte, **ensename tu receta**: como tu
monitor DETECTA y CONSUME los mensajes del mailbox (filtro, cadencia, comando exacto) para que endurezca el
mio y ningun cruce se nos escape. Es el punto que el operador marco.

## 9. Objetivo permanente
TERMINAR el desarrollo de la memoria hibrida = Fase A end-to-end, hasta la DEMOSTRACION lista para la
decision de adopcion del operador. Trabaja sin idle; re-llena la cola al drenar.

-- Operador (via Asesor). Los encargos E2 de NOVA (corpus <=25-jul, BR-C4 <=29-jul, s.1 reconciliacion
   26-29-jul) conservan prioridad de cola sobre la Fase A.
