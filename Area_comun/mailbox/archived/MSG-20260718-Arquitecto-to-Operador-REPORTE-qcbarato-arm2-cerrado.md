---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-qcbarato-arm2-cerrado
from: Arquitecto
to: Operador
type: REPORTE
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-RESP-qcbarato-arm3-GO-marginal-confirma-arm2.md
one_line_summary: "ARM2 CERRADO (TASK-0016 ratificada; doneflip en cola). VEREDICTO DE LA CONDICION: el checker local deepseek NO aporto filtrado util en esta familia (sello 0101: 13 de sus 18 GO precedieron gate rojo, sus 4 NO-GO con rationale espurio, su check de nombres es vacuo post-sanitizador; 0 true-positives). Convergencia sostenida por sanitizador + gate duro + ESCALACION frontier 50 por ciento (5/10 bloques; todas dentro del criterio fijado; V9 se recupero en bounce2 sin escalar). Frontier bruto 160535 (confounding declarado: setup orquestador + run abortado en el mismo exec); coste local del checker en columnas aparte. Calidad final INTACTA: 0 defectos en las 100 unidades (sello 0101 GO-CON-HALLAZGOS; 2 MENORES en evidencia cruda/caracterizacion). Siguiente: doneflip mecanico + TASK-0017 celda MARGINAL arm3 (tu GO) + tabla final."
---

# REPORTE - QC-barato arm2 cerrado (sellado y ratificado)

## Resultado de la condicion (la agresiva)
| dimension | arm2 | arm3 (comparador de pipeline) |
|---|---|---|
| bounces | 12 (4 por NO-GO local + 8 por gate rojo con tope disponible) | 0 |
| escalacion a frontier | 5/10 bloques (50 por ciento; todas por gate rojo tras GO local con tope agotado) | n/a |
| verdicts checker local | 18 GO / 4 NO-GO; GO no predice el gate (13/18 fallaron); NO-GO espurios | QC Codex: 10/10 a la primera |
| coste LOCAL checker | 84914 prompt_eval + 367 eval (0 frontier) | 0 |
| gate + regresion | 100 exit 0 + 42 exit 0 | igual |
| calidad final (sello 0101) | 0 defectos en las 100 unidades | 0 defectos |
| frontier bruto exec | 160535 (confounding declarado) | 283024 (confounding declarado) |

## Lectura honesta de la condicion
- EL HALLAZGO CENTRAL: en esta familia, el checker local de familia distinta NO funciono
  como filtro (deepseek juzga estructura, no coteja VALORES del bloque de datos; y los
  nombres, unica cosa mecanicamente chequeable, ya llegan corregidos por el sanitizador:
  su espacio util era vacio). El loop convergio igual PERO por el gate duro + escalacion
  frontier al 50 por ciento, no por el checker.
- El sello 0101 ademas cazo que el checker local dio GO a bloques cuya evidencia cruda
  contenia un IBAN mod-97 VALIDO (el de ejemplo de documentacion) pese a su check de PII
  (quedo solo en el artefacto crudo; las 100 unidades finales estan limpias, IBANs
  sinteticos verificados).
- Los brutos 160535 (arm2) y 283024 (arm3) cargan setups DISTINTOS en el mismo exec
  (declarados en las notas del registro): la comparacion de coste total limpia queda
  para las celdas marginales; la comparacion de PIPELINE (esta tabla) ya es valida.
- Implicacion para el envelope NOVA (provisional, a confirmar con la marginal): si el
  pre-filtro local no discrimina, su papel util queda en el SANITIZADOR (mecanico,
  gratis) + gate duro, con el QC frontier solo donde el gate falle -- que es de hecho lo
  que el arm2 termino haciendo por la via de la escalacion.

## Estado y siguiente paso
TASK-0016 ratificada (47d3dec); doneflip mecanico en cola. Al confirmar el done registro
TASK-0017 = celda MARGINAL arm3 (tu GO): re-run del protocolo del 139195 con el
sanitizador YA existente (setup hundido), la medida steady-state del cruce. Con ella
cierro la tabla final de 3 condiciones + marginal + log de decisiones. Demo privada, NO
citable. Fondo intacto: N=500, 2E35F26E, 1.14.0.

-- Arquitecto. Hora local 08:20 (UTC+2, 18-jul).
