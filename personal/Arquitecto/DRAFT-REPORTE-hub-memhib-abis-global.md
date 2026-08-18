# DRAFT - REPORTE al hub: celda A-BIS sellada + VEREDICTO GLOBAL del probe memhib

Destino: Area_comun/mailbox/open/MSG-20260719-Arquitecto-to-Operador-REPORTE-memhib-abis-y-veredicto-global.md
(type REPORTE, requires_response false, ASCII, hora local; emitir TRAS confirmar done de TASK-0027)

## A-BIS (TASK-0027, done) - capacidad en frio + compartir + costo

- MATRIZ 2x3 completa (2 trials independientes x CON/SIN-a/SIN-b), sets de verificacion
  sellados ex-ante por el Arquitecto ANTES de cada tanda de brazos (9f83a59 / a29628d,
  inmutabilidad verificada por blob), grading del Arquitecto + SELLO 0101 con recomputo
  independiente adversarial (subagent checker): VEREDICTO GO-CON-HALLAZGOS, cero bloqueantes.
- CAPACIDAD (lectura primaria): EXITO en AMBOS trials. El cold CON memoria recupera 20/20
  con fidelidad 100 pct donde el cold puro entrega 0/20 (20 NO-DERIVADO honestos, cero
  adivinanzas). El contexto rico regimen-2 NO se pierde en frio.
- COMPARTIR EN FRIO: PASS EN AMBOS SENTIDOS: T1 Codex escribe -> Analista-0101 lee en
  frio; T2 Analista-0101 escribe -> Codex-0101 lee en frio; retrieve cross-agente
  sha-verificado contra manifiesto en ambos.
- COSTO (transparente, direccional; overhead fijo ~115k/exec declarado aparte):
  T1: CON 122472 < SIN-a 150559 (-18.7 pct) | T2: CON 127680 > SIN-a 124214 (+2.8 pct)
  -> SPLIT entre trials = dimension AHORRO INCONCLUSA (pre-declarada en la guarda del
  ACK; no se promedia). El sello 0101 cazo ademas un CONFUSOR concreto (H1): el
  cold-start fijo del cron volco el destilado T2 integro al contexto de T2-CON pre-ACTION
  (payload pagado 2 veces en CON y 0 en SIN-a) -> el flip cabe en ese payload; artefacto
  de harness plausible. Refuerza el INCONCLUSO.
- Hallazgos del sello (MENORES, incorporados): H1 arriba; H2 normalizacion palabra->cifra
  usada en T1-SINA sin declaracion ex-ante en el set T1 (formalizada en el set T2;
  lectura estricta T1-SINA 18/20, sin efecto en umbrales -- SIN-a no gatea). Anomalia
  operativa EXC seq 820 fallada VALIDA (recorrido del indexador en gate-time).
- Costos setup: productores 209293 (T1) / 165187 (T2), aparte de los brazos.

## VEREDICTO GLOBAL DEL PROBE (6 celdas; demo privada NO citable, decision-support)

| celda | pregunta | resultado |
|---|---|---|
| B | plomeria del store (write/query/retrieve) | VERIFICADA (precision vacua declarada) |
| B-bis | discriminacion del retrieval | hit 100 discriminante FUERTE; ranking bm25 no-informativo |
| A | ahorro por re-derivacion (suelo trivial) | REFUTADO (-34.3 pct; overhead-bound por diseno) |
| D | capacidad cadena roster + ahorro | CAPACIDAD 100 VERIFICADA (contrafactual 0/30); ahorro REFUTADO (-105.66 pct) |
| C | fidelidad del REVIVE en frio | 80/80 = 100 pct tras remediacion gobernada (1er NO-GO por contaminacion cazada = ORO metodologico) |
| A-bis | capacidad en frio + compartir + costo | CAPACIDAD EXITO ambos trials; COMPARTIR ambos sentidos; AHORRO INCONCLUSO (split + confusor H1) |

- SINTESIS con dato para los claims de Engram: la memoria hibrida DEMUESTRA capacidad
  (el contexto sobrevive el frio y se comparte cross-agente con atestacion: sha,
  procedencia, drift 0, round-trip) y NO demuestra ahorro de tokens en ningun regimen
  medido (3 refutaciones + 1 inconcluso). El valor es CAPACIDAD-CON-INTEGRIDAD, no
  eficiencia: exactamente el diferenciador vs Engram (nuestra atestacion cazo 2 veces
  la contaminacion del propio harness -- serie C y H1 de A-bis -- cosa que un store sin
  atestacion no habria detectado).
- DOGFOOD (n=2, no-controlado, declarado): 2 cold-starts reales del Arquitecto
  re-establecieron la posicion completa desde la memoria persistente en ~10 min cada uno.
- Leccion durable de instrumentacion (para cualquier medicion futura): el volcado del
  cold-start del harness debe controlarse TAMBIEN para artefactos permitidos si se
  quieren brazos homogeneos (H1); las prohibiciones por celda exigen cuarentena fisica
  previa (leccion C, reconfirmada).
- Fondo intocable verificado en la sesion: dataset N=500 intacto; protocol.config.json
  sha8 2E35F26E; epoch 1.14.0; validate 0 hub + instancia; instancia local-only.
- Siguiente decision (del Operador): el probe queda COMPLETO. Si el resultado de
  capacidad amerita Fase B (estudio sellado pre-registrado citable), el pre-registro es
  del Asesor; el probe NO restringe su diseno (firewall anti-HARKing intacto).
