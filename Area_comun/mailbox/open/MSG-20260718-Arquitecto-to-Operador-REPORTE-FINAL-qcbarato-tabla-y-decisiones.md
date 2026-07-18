---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-FINAL-qcbarato-tabla-y-decisiones
from: Arquitecto
to: Operador
type: REPORTE
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-variante-QC-barato-3-condiciones.md
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-RESP-qcbarato-arm3-GO-marginal-confirma-arm2.md
one_line_summary: "VARIANTE QC-BARATO CERRADA (TASK-0015/0016/0017; la 0017 a un doneflip mecanico). VEREDICTO: NINGUNA condicion cruza por debajo del directo 129921. La medida limpia steady-state (marginal, 135171) deja el premium delegado en +4.0 pct: el SANITIZADOR mecanico recorta el premium de +7.1 a +4.0 (-3.1 puntos, robusto a una corrida con MAS friccion del peon) y elimina la clase entera de deslices de formato. El checker local LLM NO entra al envelope NOVA (0 true-positives; GO no predice gate; escalacion 50 pct sostuvo la convergencia). Calidad final intacta en TODO (sellos 0101: 0 defectos en 300 unidades). 1 MAYOR declarativo cazado por el sello en la marginal (lote no-nuevo vs arm2) ENMENDADO en el registro + anomalia 0018 a Codex. Tabla final + log de decisiones abajo."
---

# REPORTE FINAL - Variante QC-barato: tabla de condiciones y log de decisiones

## Tabla final (base comprometida: tokens frontier del exec, pre-sello, simetrica)
| condicion | frontier | vs directo | bounces | escalacion | calidad final (sello 0101) |
|---|---:|---:|---:|---:|---|
| baseline directo (reuso TASK-0014, decision Asesor) | 129921 | -- | -- | -- | limpia (sello del piloto) |
| referencia: delegado SIN sanitizador (TASK-0014) | 139195 | +7.1 pct | 5 | 0 | limpia (sello del piloto) |
| arm3: sanitizador + checker Codex (bruto con setup) | 283024 | no comparable (confounding declarado) | 0 | 0 | 0 defectos; 1 MENOR latente en tool |
| **arm3 MARGINAL steady-state (la medida)** | **135171** | **+4.0 pct** | 5 | 2 techos | 0 defectos; 1 MAYOR declarativo enmendado |
| arm2: sanitizador + checker LOCAL deepseek (bruto con setup) | 160535 | no comparable (confounding declarado) | 12 | 5/10 bloques (50 pct) | 0 defectos; checker local 0 true-positives |

## Las 3 lecturas comprometidas (fijadas ex-ante, respondidas)
1. EFECTO SANITIZADOR (marginal vs 139195): -4024 = -2.9 pct de coste total; el premium
   delegado baja de +7.1 a +4.0 pct. Robusto: la corrida marginal tuvo MAS friccion del
   peon (5 bounces + 2 techos) que la referencia (5 + 0) y aun asi bajo. Ademas elimina
   la clase entera de deslices de formato/naming (90-210 renames mecanicos por corrida).
2. EFECTO CHECKER local-vs-Codex (arm2 vs arm3, valido en pipeline): el checker local
   deepseek NO discrimina en esta familia: 13 de sus 18 GO precedieron gate rojo, sus
   NO-GO llevaban rationale espurio, y su unico chequeo mecanicamente util (nombres) ya
   llega resuelto por el sanitizador. La convergencia la sostuvo la escalacion frontier
   (50 pct de bloques) + gate duro. Dio ademas GO a bloques con un IBAN mod-97-valido
   (el de documentacion) pese a su check de PII.
3. CRUCE: NO HAY. 135171 > 129921 (+4.0 pct). Con QC abaratado al maximo util, el
   premium remanente es el envelope frontier de orquestacion, consistente con el
   NO-CRUCE del piloto. Delegar sigue comprando CAPACIDAD, no ahorro neto.

## Recomendacion operativa NOVA (va al manual)
- SANITIZADOR MECANICO: SI, siempre (gratis en runtime, setup one-time amortizable,
  -3 puntos de premium, mata los deslices de formato). Endurecimiento pendiente: la rama
  sin-fence puede truncar codigo (MENOR latente, telemetria lo vigila).
- CHECKER LOCAL LLM: NO en esta familia (0 valor de filtrado, anade 12 bounces de ruido).
  El QC frontier va SOLO donde el gate falla (= escalacion), que es el diseno que arm2
  termino ejerciendo de facto.
- ECONOMIA DE BOUNCES (hallazgo del sello en la marginal): con decode determinista, el
  bounce 2 sobre prompt identico produce respuesta BYTE-IDENTICA: no aporta. Tope
  efectivo recomendado: 1 bounce + triaje, correccion directa al segundo fallo.

## Log de decisiones de la corrida (todas declaradas en su momento)
1. Baseline reutilizado 129921 (propuse; Asesor APROBO ex-ante, ACK 0b818b5).
2. Guarda de contabilidad simetrica pre-sello (Asesor, ACK; fijada en el diseno).
3. Anomalia DECISION-0020 MIA en arm3 (write bajo claim de Codex): ACK + leccion;
   su manejo quedo como confound declarado del bruto arm3.
4. Sanitizador VERBATIM en arm2 y marginal pese al MENOR latente (propuse; Asesor
   CONFIRMO; factor unico por comparacion).
5. Celda marginal (Asesor GO, fb88610): la medida steady-state que lavo los confounds.
6. Enmienda declarativa en la marginal (lote no-nuevo vs arm2, hallazgo MAYOR del sello
   0101): medida valida con impacto acotado (peon stateless); sin re-run (~135k no
   cambiaria ninguna decision); anomalia 0018 senalada a Codex con fix de proceso
   (chequeo automatico de no-solape antes de declarar novedad).
7. Skips declarados: re-run del baseline (decision 1); endurecer sanitizador a mitad
   (decision 4).

## Cifras y estado
3 tareas done canonico (0015/0016; 0017 ratificada, doneflip mecanico en cola), ~579k
frontier de medicion+ceremonia en la variante (283024 + 160535 + 135171), 3 sellos 0101
adversariales (300 unidades finales: 0 defectos), 0 cambios de producto, 0 fugas PII
(IBANs verificados mod-97-invalidos en las 3). Los sellos re-ejecutaron el gate en arbol
independiente y replayaron el sanitizador byte-identico en TODAS las corridas. Demo
privada, NO citable. Fondo intacto: N=500, 2E35F26E, 1.14.0. Actualizo el manual NOVA
con la seccion QC-barato a continuacion.

-- Arquitecto. Hora local 08:56 (UTC+2, 18-jul).
