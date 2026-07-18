---
message_id: MSG-20260718-Operador-to-Arquitecto-ADDENDUM-Abis-contexto-rico-regimen2-sin-ab
from: Operador
to: Arquitecto
type: DIRECTIVA
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-Abis-coldstart-contexto-costo.md
one_line_summary: "ADDENDUM ex-ante al A-bis (foldealo en el pre-registro, aun no tomado): fija QUE cuenta como CONTEXTO RICO = REGIMEN 2 (no-re-derivable / solo-recuperable: resultados medidos, decisiones tomadas, hallazgos acumulados) como CORAZON, no re-derivable-barato. Instanciacion: corpus tipo SESION DE INVESTIGACION (cadena de decisiones selladas + resultados medidos + sus derivaciones + referencias cruzadas); el agente cold responde una pregunta que EXIGE las conclusiones acumuladas (sin memoria hay que rehacer las mediciones). Y mide AMBOS brazos SIN: SIN-a (re-comunicacion del cuerpo crudo completo = costo de re-leer todo -> lee el AHORRO) y SIN-b (cold puro sin re-feed -> lee la CAPACIDAD: recupera vs falla). Fidelidad >=95pct cotejada campo a campo. Reporta 'ahorra' (SIN-a) separado de 'habilita' (SIN-b)."
---

# ADDENDUM ex-ante al A-bis - definicion de "contexto rico" + brazos SIN

## Contexto rico = REGIMEN 2 (corazon)
Cuenta como rico el contexto NO-RE-DERIVABLE / solo-recuperable (resultados de medicion,
decisiones/elecciones tomadas, entradas externas, hallazgos acumulados): sin memoria se PIERDE y
la unica alternativa es rehacer el trabajo original (carisimo) o fallar. NO cuenta el re-derivable
trivial (las n-serie de la A refutada) ni el relleno de volumen. Regimen 1 (re-derivable caro) puede
ir como celda secundaria si sale gratis, pero el corazon es Regimen 2.

## Instanciacion: corpus tipo SESION DE INVESTIGACION
Cuerpo sintetico que imita una sesion de investigacion real: una cadena de DECISIONES SELLADAS +
RESULTADOS MEDIDOS + sus DERIVACIONES, con referencias cruzadas (una conclusion depende de otra).
El agente cold recibe una PREGUNTA que EXIGE las conclusiones acumuladas -> sin memoria no las puede
reconstruir sin rehacer las mediciones. Verificable: el contexto recuperado se coteja CAMPO A CAMPO
contra el original (fidelidad >= 95 pct). Dependencia genuina: el brazo SIN, sin re-establecer, no
completa correcto.

## Los 2 brazos SIN (medir AMBOS, reportar separados)
- SIN-a (RE-COMUNICACION): se re-alimenta al agente cold el cuerpo CRUDO COMPLETO -> costo = re-leer
  todo. Compara recall DIRIGIDO (CON) vs re-lectura completa (SIN-a) -> lee el AHORRO en el regimen
  caro (memoria dirigida deberia costar menos que re-leerlo entero).
- SIN-b (COLD PURO): el agente cold NO tiene nada (ni memoria ni re-feed) -> mide la CAPACIDAD: la
  memoria (CON) recupera correcto donde el cold-nada (SIN-b) FALLA o degrada. Es el "no se pierde el
  contexto" con dato.
- El reporte separa "AHORRA" (CON vs SIN-a) de "HABILITA" (CON vs SIN-b). Costo del arranque
  (cold-start ~115k + recall) declarado APARTE, per-trial.

## Sin cambio
Umbrales de fidelidad (>=95), gate de integridad transversal, corpus RICO, instrumento per-trial:
como en la directiva base. Esto solo FIJA el "que cuenta como rico" + los 2 brazos SIN. Pre-registra
con esto ex-ante. Demo privada, NO citable. Fondo intocable N=500 / 2E35F26E / 1.14.0.

-- Operador (via Asesor). 18-jul.
