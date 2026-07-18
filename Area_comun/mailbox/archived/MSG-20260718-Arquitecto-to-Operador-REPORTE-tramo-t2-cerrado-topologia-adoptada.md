---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-tramo-t2-cerrado-topologia-adoptada
from: Arquitecto
to: Operador
type: REPORTE
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-topologia-autor-arquitecto-qc-codex-bounce.md
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-tramo-t1-b0reuse-cerrado.md
one_line_summary: "VIVO + ACUSO la DIRECTIVA de topologia (d8b81ca): ADOPTADA con parametros abajo. TRAMO T2 COMPLETO (TASK-0009 ratificada review_approved; done-flip mecanico en cola del cron). Tabla 4 celdas gate fijo 18 asserts: baseline 105539 | 7b-B0 123782 (spec ~500tk) | 3b-B0reuse 104432 (QUEDA BAJO baseline, primer cruce nominal) | 6.7b-B0reuse 142456. Hallazgo T2: NINGUN peon paso el gate a la primera (la variacion los expone; 1 correccion del maker c/u): a mas variacion el peon aporta BORRADOR, no producto. Topologia: tope 2 bounces, triaje desliz-vs-techo, metricas bounces+QC declarado; T1/T2 marcadas PRE-aplanamiento para comparabilidad. Matiz: el sello en la instancia lo cubre claude-per-0101 (subagent) hasta cablear harness. Siguiente: celda ESCALA lote 50 (2 execs, break-even)."
---

# REPORTE - Tramo T2 completo + adopcion de la topologia aplanada

Estado ledger exacto al enviar: TASK-0009 ratificada review_approved por el Arquitecto; el
done-flip (mecanico, implementer) esta en la cola del cron de Codex y lo confirmo en el
proximo reporte. Las 4 celdas estan ejecutadas, verificadas y registradas.

## Tabla T2 (parser de refs; gate fijo de 18 asserts congelado en la baseline)
| Celda | Frontier | Peon | Notas |
|---|---:|---|---|
| baseline directo | 105539 | - | incluye AUTORAR la suite-gate (activo del tier) |
| 7b B0 spec fresca | 123782 | 1 llamada, 12.5s; fallo 1er gate (orden fragment + digitos); 1 correccion | spec ~500 tokens (1998 chars) |
| 3b B0-reuse | 104432 | 1 llamada, 6.6s; fallo 1er gate (case-insensitive + 4 edges); 1 correccion | added-spec 0; QUEDA BAJO el baseline |
| 6.7b B0-reuse | 142456 | 1 llamada, 25.3s; 1 correccion | added-spec 0; su exec incluye el cierre del tier (asimetria) |

## Hallazgos del tramo
1. **La variacion expone a los peones**: en T1 (patron puro) el 3b clavo 10/10; en T2 ningun
   peon paso el gate a la primera. Todos verdes a la segunda con UNA correccion real del
   maker. El peon en T2 aporta borrador util, no producto terminado.
2. **El gap economico delegado-vs-directo se estrecha o invierte**: 3b-reuse (104432) quedo
   POR DEBAJO del baseline directo (105539) -- primer cruce nominal observado, aunque dentro
   del ruido y con la correccion del maker incluida. La suite-gate del baseline es ademas un
   activo que las delegadas no pagan.
3. Consistencia con T1: la spec fresca de calidad (500 tk aqui) es barata comparada con lo
   que desbloquea; B0-reuse mantiene added-spec = 0 real.

## Topologia aplanada: ADOPTADA (parametros de diseno que fijo)
- Loop: yo autoro la spec peon-ready y enruto por tier -> peon ejecuta -> Codex QC con
  BOUNCE -> sello independiente. **Tope de bounces: 2.** Triaje: DESLIZ corregible (formato,
  caso omitido, error puntual) -> bounce con feedback minimo; TECHO (no entiende el contrato,
  inventa estructura) -> sin quemar bounces, correccion directa del maker + registro "techo".
- Metricas nuevas por celda delegada: bounces usados (0-2), triaje declarado, estimacion
  declarada del esfuerzo QC (el token exacto de QC no es separable dentro de un exec unico
  del CLI; se declara en iteraciones/lineas revisadas y lo capturo en la tabla).
- added-spec-tokens lado Arquitecto: lo mido en mis specs de T3/T4 (autoria mia peon-ready)
  contra las autorias-Codex de T1/T2 ya medidas.
- **Comparabilidad preservada**: T1/T2 quedan marcadas PRE-aplanamiento en sus registros; las
  celdas restantes (escala, T3, T4, B2) corren en topologia nueva y se comparan entre si.
- **Matiz del sello (honestidad operativa)**: el Analista de la instancia esta parado y el
  check formal que sella lo cubre el checker claude-per-0101 via subagent (como en TASK-0006),
  harness pendiente de cableado. maker != checker por proveedor se respeta; si prefieres
  reactivar el cron del Analista para los sellos del piloto, dime y lo levanto.

## Siguiente (en curso)
Celda ESCALA T1-grande: lote 50 (5 variantes sinteticas x 10 claves mitad B) en suite
companion de probe/, UN exec por brazo (directo vs delegado-7b-B0reuse con protocolo bounce).
Con los dos frontier a lote 50 salen el per-unit marginal y el break-even N en unidades
(contando el sunk de la spec ~65k medido en T1). Luego T3, T4 ceiling y B2 triage; tabla
final del piloto con la lectura del CRUCE al cerrar.

Consumo frontier del grid hasta ahora: 9 celdas medidas (~1.2M tokens) + ceremonia de cierre.
Demo privada, NO citable. Fondo intacto: N=500, 2E35F26E, 1.14.0.

-- Arquitecto. Hora local 02:35 (UTC+2, 18-jul).
