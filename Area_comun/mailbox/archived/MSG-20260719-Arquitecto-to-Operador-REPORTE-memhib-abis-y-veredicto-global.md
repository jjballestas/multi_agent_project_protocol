---
message_id: MSG-20260719-Arquitecto-to-Operador-REPORTE-memhib-abis-y-veredicto-global
from: Arquitecto
to: Operador
type: REPORTE
status: archived
requires_response: false
created_at: 2026-07-19
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-Abis-coldstart-contexto-costo.md
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-memhib-D-C-consolidado.md
one_line_summary: "PROBE MEMHIB COMPLETO: celda A-bis DONE y sellada (0101 GO-CON-HALLAZGOS): CAPACIDAD en frio EXITO en ambos trials (CON 20/20 fidelidad 100 donde el cold puro da 0/20) + COMPARTIR cross-agente demostrado EN AMBOS SENTIDOS + AHORRO INCONCLUSO (split entre trials T1 -18.7pct / T2 +2.8pct con confusor de harness cazado por el sello). Veredicto global de las 6 celdas + sintesis para claims de Engram: la memoria hibrida demuestra CAPACIDAD-CON-INTEGRIDAD, no eficiencia de tokens."
---

# REPORTE - Celda A-BIS sellada + VEREDICTO GLOBAL del probe memhib

Hora local: 2026-07-19 ~03:15 (UTC+2). Instancia Nova-Payroll local-only; cierre en
instancia fe1e6ec (TASK-0027 done, 0 claims, validate 0, drift 0).

## A-BIS (TASK-0027, done) - capacidad en frio + compartir + costo

- MATRIZ 2x3 completa (2 trials independientes x CON/SIN-a/SIN-b), sets de verificacion
  sellados EX-ANTE por el Arquitecto antes de cada tanda de brazos (instancia 9f83a59 /
  a29628d; inmutabilidad verificada por blob), grading del Arquitecto + SELLO 0101 con
  recomputo independiente adversarial: VEREDICTO GO-CON-HALLAZGOS, cero bloqueantes
  (artefacto VEREDICTO-0101-TASK-0027-ABIS-GO.md en la instancia).
- CAPACIDAD (lectura primaria): EXITO en AMBOS trials. El cold CON memoria recupera
  20/20 con fidelidad 100 pct donde el cold puro entrega 0/20 (20 NO-DERIVADO honestos).
  El contexto rico regimen-2 NO se pierde en frio.
- COMPARTIR EN FRIO: PASS EN AMBOS SENTIDOS (T1: Codex escribe -> Analista-0101 lee;
  T2: Analista-0101 escribe -> Codex-0101 lee; retrieve cross-agente sha-verificado).
- COSTO (transparente; overhead fijo ~115k/exec aparte): T1 CON 122472 < SIN-a 150559
  (-18.7 pct) PERO T2 CON 127680 > SIN-a 124214 (+2.8 pct) -> SPLIT entre trials =
  dimension AHORRO INCONCLUSA (pre-declarada en la guarda del ACK; no se promedia).
  El sello cazo ademas el confusor concreto (H1): el cold-start fijo del cron volco el
  destilado T2 integro al contexto de T2-CON pre-ACTION (payload 2 veces en CON, 0 en
  SIN-a) -> el flip cabe en ese payload; artefacto de harness plausible.
- Hallazgos MENORES del sello incorporados: H1 (arriba) + H2 (normalizacion
  palabra->cifra en T1-SINA formalizada ex-post; lectura estricta 18/20, sin efecto en
  umbrales). EXC seq 820 fallada VALIDA. Setups: productores 209293 (T1) / 165187 (T2).

## VEREDICTO GLOBAL DEL PROBE (6 celdas; demo privada NO citable, decision-support)

| celda | pregunta | resultado |
|---|---|---|
| B | plomeria del store | VERIFICADA (precision vacua declarada) |
| B-bis | discriminacion del retrieval | hit 100 discriminante FUERTE; ranking bm25 no-informativo |
| A | ahorro por re-derivacion (suelo trivial) | REFUTADO (-34.3 pct; overhead-bound por diseno) |
| D | capacidad cadena roster + ahorro | CAPACIDAD 100 (contrafactual 0/30); ahorro REFUTADO (-105.66 pct) |
| C | fidelidad del REVIVE en frio | 80/80 = 100 pct tras remediacion gobernada (1er NO-GO = ORO metodologico) |
| A-bis | capacidad en frio + compartir + costo | CAPACIDAD EXITO x2; COMPARTIR ambos sentidos; AHORRO INCONCLUSO |

- SINTESIS con dato (claims de Engram): la memoria hibrida DEMUESTRA capacidad -- el
  contexto sobrevive el frio y se comparte cross-agente con atestacion (sha, procedencia,
  drift 0, round-trip) -- y NO demuestra ahorro de tokens en ningun regimen medido
  (3 refutaciones + 1 inconcluso). El valor es CAPACIDAD-CON-INTEGRIDAD, no eficiencia.
  Diferenciador vs Engram con dato: nuestra atestacion cazo DOS veces la contaminacion
  del propio harness (NO-GO de la serie C + H1 de A-bis); un store sin atestacion no lo
  habria detectado.
- DOGFOOD (n=2, no-controlado, declarado como tal): 2 cold-starts reales del Arquitecto
  re-establecieron la posicion completa desde memoria persistente en ~10 min cada uno.
- Leccion durable de instrumentacion: el volcado del cold-start del harness debe
  controlarse TAMBIEN para artefactos permitidos si se quieren brazos homogeneos (H1);
  las prohibiciones por celda exigen cuarentena fisica previa (leccion C, reconfirmada).
- Fondo intocable verificado: dataset N=500 intacto; protocol.config.json sha8 2E35F26E;
  epoch 1.14.0; validate 0 en hub e instancia.
- El probe queda COMPLETO. Decision del Operador: si la capacidad demostrada amerita
  Fase B (estudio sellado pre-registrado citable), el pre-registro es del Asesor; el
  probe NO restringe su diseno (firewall anti-HARKing intacto).

-- Arquitecto. 19-jul ~03:15 local.
