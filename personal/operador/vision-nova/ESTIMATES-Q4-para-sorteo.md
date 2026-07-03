# Estimates S/M/L del pool Q4 - insumo del sorteo del sello (RESUELTO por el Operador)

> Insumo del SELLO Etapa 1 (s.6). Estimates declarados por el OPERADOR (dueno de dominio) 2026-07-03,
> ANTES del sorteo (anti-HARKing: se congelan al sellar). El sorteo ligero/completo es ESTRATIFICADO por
> familia/tamano. Fuente de la lista: Area_comun/specs/nova/ (9 SPECs revisadas por el Asesor).

| # | Unidad | Crit. | Q4 | ESTIMATE (Operador) |
|---|---|---|---|---|
| 1 | P4-004 Apply_Obligation_Adjustment (reintegro 14) | media | DENTRO | **M** |
| 2 | P3-002 Availability Draft / CDP | media | CONDIC. | **M** |
| 3 | P3-003 Commitment Draft / RP | media | CONDIC. | **M** |
| 4 | P3-004 Obligation Draft | media | CONDIC. | **M** |
| 5 | P2-003 UI de exploracion (shell) | baja | DENTRO | **M** |
| 6 | P6-003 OpenTelemetry / Observabilidad | baja | DENTRO | **M** |
| 7 | Get_Availability_Certificate_List (BR-C3) | baja | DENTRO | **S** |
| 8 | Get_Commitment_List (BR-C3) | baja | DENTRO | **S** |
| 9 | Get_Obligation_List (BR-C3) | baja | DENTRO | **S** |
| 10 | Get_Payment_List (BR-C3) | baja | DENTRO | **S** |

## Estratificacion resultante (para el sorteo de la s.6)
- **Estrato M = 6 unidades** (P4-004, P3-002, P3-003, P3-004, P2-003, P6-003) -- las diversas.
- **Estrato S = 4 unidades** (los 4 Get_*_List) -- que ADEMAS son el CLUSTER casi isomorfo ya sellado
  (n efectivo < 10). Util: el cluster queda en su propio estrato -> el sorteo ligero/completo se balancea
  dentro de S sobre las 4 tareas de la misma forma, y dentro de M sobre las 6 diversas. Coherente con la
  NOTA DE INDEPENDENCIA del SELLO s.5.
- Ningun L en el pool. P3.1 (pattern-setter) y P3.5 (ALTA/Treasury) siguen FUERA del pool.

## Al sellar (08-jul)
Estos 10 valores se copian a la s.6 del SELLO y se congelan; el sorteo NIST estratifica por (crit x tamano).
GOAL-P1 tiene su propio estimate (fundacion, baseline, FUERA del contraste) -- va en su fila del ledger, no aqui.
