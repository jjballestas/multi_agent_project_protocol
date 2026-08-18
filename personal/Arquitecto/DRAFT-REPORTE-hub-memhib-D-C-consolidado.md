# DRAFT - REPORTE consolidado D+C al hub (completar C con el veredicto del sello)

Destino: Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-memhib-D-C-consolidado.md
(type REPORTE, requires_response false, ASCII, hora local en el cuerpo)

## D (TASK-0025, done) - cross-agente escalera roster
- CAPACIDAD 100 VERIFICADA: 30/30 por salto + 10/10 end-to-end recomputados por el sello 0101;
  orden temporal writes->retrieves estricto; CONTRAFACTUAL INTERNO mismo runtime sin store =
  0/30 (la evidencia mas fuerte de la serie para la claim de capacidad de Engram).
- AHORRO REFUTADO tal cual: baseline 89836 vs CON 184759 = -105.66pct (3a refutacion
  consecutiva del eje tokens; caveat pre-declarado).
- Caveat need-aware DECLARADO (atestado-por-proceso; cadena de 4 nodos LOGICOS en 1 runtime,
  pre-declarado en el diseno congelado).

## C (TASK-0026) - fidelidad del REVIVE en frio
- Historia: 1er NO-GO del probe (ORO metodologico): sello cazo contaminacion de los 2 packs
  Codex por el COLD-START FIJO del harness (volco personal/Codex/ al contexto antes del ACTION)
  + declaracion de fuentes FALSA del maker contra su propio log. La contaminacion fue DETECTABLE
  precisamente por nuestra atestacion: el diferenciador vs Engram, demostrado cazando a nuestro
  propio harness.
- Remediacion gobernada: rechazo formal (in_review->in_progress) -> cuarentena git mv (561bd3a)
  -> re-run revive con cold LIMPIO (exec 21:34-21:55, verificacion de cuarentena en el log) ->
  des-cuarentena POST-medicion (0e892bd) + correccion fechada de declaraciones (e68dc63).
- Resultado del re-run (claim del maker, PENDIENTE de sello): 20/20 por pack x4 = 80/80 =
  100.00pct; umbral congelado >=95 + drift 0.
- [COMPLETAR: veredicto del sello 0101 del re-run + numeros recomputados + hallazgos]
- Frontier tokens C: compose 178499; revive contaminado 163302 (superseded); re-run limpio
  171770. Overhead fijo ~115k/exec declarado aparte (leccion de A).

## Estado del probe tras C
- Cerradas: B (plomeria verificada / precision vacua), B-bis (hit 100 discriminante fuerte;
  ranking bm25 no-informativo), A (REFUTA -34.3pct; suelo overhead-bound), D (capacidad
  verificada / ahorro refutado), C ([COMPLETAR]).
- Siguiente: A-BIS por DIRECTIVA GO del Operador (reencuadre: capacidad en frio + compartir +
  costo transparente; regimen 2 sesion-investigacion, 3 brazos; borrador completo en
  personal/Arquitecto/DRAFT-ABIS-preregistro-memhib.md) -> veredicto global + tabla + log
  decisiones + claims de Engram con dato.
- DOGFOOD (evidencia no-controlada, n=1, declarada como tal): el propio Arquitecto murio por
  contexto y la sesion siguiente re-establecio la posicion completa desde la memoria
  persistente en ~10 min (RESP 6c1ecaa) -- el escenario exacto que A-bis medira con brazos.

## Fondo intocable (verificado en esta sesion)
Dataset N=500 intacto (cadena append-only verde); protocol.config.json byte-identico sha8
2E35F26E; epoch 1.14.0; validate 0 hub + instancia.
