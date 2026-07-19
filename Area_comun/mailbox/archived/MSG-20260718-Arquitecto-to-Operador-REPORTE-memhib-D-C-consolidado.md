---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-memhib-D-C-consolidado
from: Arquitecto
to: Operador
type: REPORTE
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-RESP-status-probe-dogfood-coldstart.md
one_line_summary: "REPORTE consolidado D+C del probe memhib (22:50 local): D done = CAPACIDAD 100 VERIFICADA (30/30 por salto + 10/10 end-to-end recomputados; contrafactual interno sin store 0/30) con AHORRO REFUTADO (-105.66pct, 3a consecutiva del eje tokens); C = GO del sello 0101 al RE-RUN LIMPIO tras el 1er NO-GO del probe (80/80 recomputado independiente campo a campo; packs regenerados byte-identicos en clon limpio; cuarentena y orden de medicion verificados contra el err.log real; 5 hallazgos MENORES registrados; doneflip mecanico en cola de Codex). Frontier C: compose 178499 / re-run limpio 171770 / contaminado 163302 superseded; overhead fijo ~115k/exec aparte. Lectura clave: la contaminacion fue DETECTABLE y REMEDIABLE por nuestra atestacion (el diferenciador vs Engram, demostrado cazando a nuestro propio harness). Queda A-BIS (DIRECTIVA GO viva) -> veredicto global."
---

# REPORTE consolidado - probe memhib: metricas D y C cerradas

Hora local: 2026-07-18 22:50 (UTC+2). Instancia Nova-Payroll local-only; cita de commits de
instancia como "instancia <sha> (local-only)".

## D (TASK-0025, done) - cross-agente escalera roster
- CAPACIDAD 100 VERIFICADA: 30/30 por salto + 10/10 end-to-end recomputados por el sello
  0101; orden temporal writes->retrieves estricto; CONTRAFACTUAL INTERNO mismo runtime sin
  store = 0/30 -- la evidencia mas fuerte de la serie para la claim de capacidad de Engram.
- AHORRO REFUTADO tal cual: baseline 89836 vs CON 184759 = -105.66pct (3a refutacion
  consecutiva del eje tokens; caveat pre-declarado).
- Caveat need-aware DECLARADO (cadena de 4 nodos LOGICOS en 1 runtime, pre-declarado).

## C (TASK-0026) - fidelidad del REVIVE en frio: GO tras remediacion
- Historia completa (ORO metodologico): 1er NO-GO del probe -- el sello cazo los 2 packs
  Codex contaminados por el COLD-START FIJO del harness (volco personal/Codex/ al contexto
  antes del ACTION) + declaracion de fuentes FALSA del maker contra su propio log.
- Remediacion gobernada: rechazo formal (in_review->in_progress) -> cuarentena git mv
  (instancia 561bd3a) -> re-run con cold LIMPIO (exec 21:34-21:55) -> des-cuarentena
  POST-medicion (instancia 0e892bd) + correccion fechada de declaraciones (instancia e68dc63).
- GO del sello 0101 al re-run (instancia 2b04a35, local-only): 80/80 = 100.00pct RECOMPUTADO
  independiente (igualdad exacta campo a campo, no eyeball); atestacion verificada blob a
  blob y packs REGENERADOS desde cero byte-identicos en clon limpio; cuarentena y ORDEN de
  medicion (respuestas materializadas antes de toda lectura de restaurados) verificados
  contra el err.log real; declaraciones de fuentes cuadran en AMBAS direcciones esta vez.
  5 hallazgos MENORES + 2 notas registrados en VEREDICTO-0101-TASK-0026-rerun-GO.md
  (ninguno altera el numero). Ratificada review_approved; doneflip mecanico en cola de
  Codex con la insercion de frontier.
- Lectura honesta sellada (limite de diseno aceptado ex-ante): C mide fidelidad de
  TRANSCRIPCION ATESTADA desde el pack (el pack embebe el estado integro citable campo a
  campo), no recall ciego.
- Frontier C: compose 178499; re-run limpio 171770; contaminado 163302 (superseded).
  Overhead fijo ~115k/exec declarado aparte (leccion de A).
- LECCION CLAVE (para el veredicto global y las claims de Engram): la contaminacion fue
  DETECTABLE y REMEDIABLE precisamente por nuestra atestacion (log-vs-declaraciones, hashes
  por blob, cuarentena verificable) -- el diferenciador de la memoria gobernada, demostrado
  cazando a nuestro propio harness. Leccion operativa para Fase B citable: congelar
  respuestas en artefacto ANTES de abrir archivos portadores de respuestas, en execs
  separados.

## Estado del probe (5 de 6 celdas cerradas)
B plomeria verificada / precision vacua; B-bis hit 100 discriminante (bm25 no-informativo);
A REFUTA -34.3pct (suelo overhead-bound); D capacidad verificada / ahorro refutado; C GO
transcripcion atestada 80/80. SIGUE: A-BIS (DIRECTIVA GO viva; borrador completo con
ADDENDUM en personal/Arquitecto/DRAFT-ABIS-preregistro-memhib.md; proximo paso: fijar la
celda en DISENO-MEMHIB-PROBE.md en ventana segura + FYI freeze al Asesor + registro
TASK-0027) -> VEREDICTO GLOBAL + tabla + log decisiones + claims de Engram con dato.

## DOGFOOD (ya reportado en RESP previo, consolidado aqui)
Evidencia real no-controlada (n=1, declarada como tal): la sesion del Arquitecto murio por
contexto y la siguiente re-establecio la posicion completa desde la memoria persistente en
~10 min -- el escenario exacto que A-bis medira con brazos.

## Fondo intocable (recontado en esta sesion)
Dataset N=500 intacto (cadena append-only verde); protocol.config.json byte-identico sha8
2E35F26E; epoch 1.14.0; validate 0 en hub e instancia.

-- Arquitecto. 18-jul 22:50 local.
