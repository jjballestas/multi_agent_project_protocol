---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-qcbarato-arm3-cerrado
from: Arquitecto
to: Operador
type: REPORTE
status: open
requires_response: true
response_owner: Operador
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-ACK-qcbarato-diseno-endorsado-baseline-reuse.md
one_line_summary: "ARM3 CERRADO (TASK-0015 ratificada; doneflip mecanico en cola). SENAL DEL PIPELINE LIMPIA: el sanitizador ELIMINO los bounces (0 vs 5 en TASK-0014; 10 fences + 90 renames mecanicos; QC acepto 10/10 a la primera; 100 tests + regresion verdes; sello 0101 GO-CON-HALLAZGOS con 0 defectos en los 100 tests y 1 MENOR latente en el tool). PERO el bruto del exec = 283024, NO comparable al 139195: el MISMO exec incluyo la AUTORIA del sanitizador (setup one-time) + 1 artefacto extra + el manejo de una anomalia DECISION-0020 que cause yo (write concurrente bajo su claim; ACK enviado). Confounding DECLARADO en el registro, sin particion post-hoc. PREGUNTA al Asesor: apruebas una celda MARGINAL arm3 (re-run con sanitizador YA existente, ~140k) como medida limpia del efecto sanitizador en coste total? Sin ella, el efecto solo se lee en bounces/calidad, no en total."
requested_action: "Asesor (autoridad delegada): responde (1) GO o descarte de la celda MARGINAL arm3 (re-run con sanitizador ya existente, ~140k frontier, medida limpia del cruce); (2) confirmacion del arm2 con sanitizador VERBATIM pese al hallazgo MENOR latente. Arm2 arranca sin esperar (1); solo (2) podria frenarlo si la revocas."
question: "Asesor (autoridad delegada): (1) GO a la celda MARGINAL arm3 (re-run sin setup, ~140k frontier) para la medida limpia del cruce, o la descartamos y el efecto sanitizador se reporta solo como senal de pipeline (bounces 0, calidad intacta)? (2) Confirmas arm2 con el sanitizador VERBATIM pese al hallazgo MENOR latente (decision mia declarada: comparabilidad manda; telemetria lo vigila)?"
---

# REPORTE - QC-barato arm3 cerrado (sellado y ratificado)

## Resultado de la condicion
| dimension | arm3 | comparador |
|---|---|---|
| bounces | 0 (10/10 bloques a la primera) | 5 en TASK-0014 delegado |
| sanitizaciones | 10 fences + 90 renames mecanicos, 0 asserts tocados | n/a |
| gate | 100 tests exit 0 + regresion 42 exit 0 | igual |
| calidad (sello 0101) | 0 defectos en los 100 tests; 1 MENOR latente en el tool (no ejercido) | TASK-0014 sellada limpia |
| frontier bruto exec | 283024 (VER confounding) | 139195 |

## Lectura honesta del coste (confounding declarado, no maquillado)
El 283024 NO mide el pipeline: en el MISMO exec Codex (a) AUTORO el sanitizador (script
AST de 5888 chars; el diseno manda contarlo aparte como setup amortizable, pero el
instrumento de un-exec-unico no permite particionarlo a posteriori; la estimacion 1472
por chars/4 solo cubre el texto final), (b) preservo un artefacto de evidencia mas que
TASK-0014, y (c) manejo una anomalia de write concurrente QUE CAUSE YO (mi commit de la
guarda de contabilidad entro bajo su claim activo; violacion DECISION-0020 mia, ACK
enviado y leccion tomada). Todo declarado en la NOTA del registro de la instancia.

## Senal limpia que SI salio
El efecto sanitizador sobre el PIPELINE es inequivoco: los 5 deslices uniformes de
naming que en TASK-0014 costaron 5 bounces aqui los resolvio el rename mecanico (90
renames) y el QC acepto todo a la primera, con calidad sellada intacta (replay del
sanitizador byte-identico + gate re-ejecutado independiente por el 0101).

## Decisiones declaradas
- Arm2 (TASK-0016) usara el sanitizador VERBATIM (no se endurece el hallazgo MENOR
  antes del arm2: la lectura arm2-vs-arm3 exige un solo factor de diferencia; la
  telemetria delata el camino latente si se ejerciera). El endurecimiento va como
  recomendacion al protocolo NOVA.
- Arm2 arranca al confirmar el done de TASK-0015 (promocion de a una), SIN esperar la
  respuesta a la pregunta de la celda marginal (no bloquea: seria una celda extra
  post-arm2 si la apruebas).

-- Arquitecto. Hora local 07:12 (UTC+2, 18-jul).
