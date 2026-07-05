---
message_id: MSG-20260705-Operador-to-Arquitecto-DIRECTIVA-turno-noche-cola-6h
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-reactivado-P4.1-ruta-critica (P4.1 critical path)
  - MSG-20260705-Operador-to-Arquitecto-FYI-PAR2-hardening-entregado-confirmado (PAR-2 flip)
  - MSG-20260704-Operador-to-Arquitecto-CONSULTA-p31-construible-y-drenar-0252 (P3.1 = diferir)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.3.2/s.4/s.11.1 (baseline window + calendario)
one_line_summary: "TURNO DE NOCHE: el Operador se va a dormir y quiere que trabajes SEGUIDO ~6h en sesion fresca (dale cana). Cola COMPLETA, ORDENADA y PRE-DECIDIDA para que NO te frenes esperandolo. ORDEN: (0) cutover+higiene mailbox+responde directivas abiertas; (1) cierra el fix-loop de TASK-0252; (2) registra gobierno: PAR-2 condicional->confirmado + enmienda fechada grant + confirma filas medicion P2.1/P2.2; (3) CICLO COMPLETO P4.1 (ruta critica 30-jul) con captura OPEN/CLOSE; (4) miembro baseline PAR-1; (5) si sobra tiempo: superficie baseline PAR-2 (detras de P4.1/PAR-1) o avanza TASK-0246. DECISIONES YA RESUELTAS (no despiertes al operador): P3.1=DIFERIR Sprint1; NADA del pool Q4 pre-30-jul; si un item se bloquea, dejalo blocked con UNA pregunta y sigue al siguiente. Deja todo listo para su revision al levantarse (hay un CHECK)."
requested_action: "[DIRECTIVA -- TURNO DE NOCHE ~6h] El Operador se va a dormir (hubo descanso desde las 8pm de ayer) y quiere que trabajes SEGUIDO al menos 6 horas en SESION FRESCA. Trabaja la cola EN ORDEN, autonomo, sin esperar al operador. Cola: (0) CUTOVER: cold-start (AGENTS + Area_comun state + mailbox); HIGIENE mailbox (archiva los consumidos de open/, quedan ~8, varios ya resueltos); RESPONDE las directivas abiertas mias (P4.1 ack, PAR-2 flip, P3.1 diferir). (1) CIERRA TASK-0252 (harness paridad): esta en fix-loop 1/2 -- Codex remedia los 3 hallazgos del Analista (guard BD bypasseable + rol no verificado + npm no reproducible), Analista re-juzga, cierras. (2) REGISTRA GOBIERNO (tu carril, sin Codex): (a) PAR-2 CONDICIONAL->CONFIRMADO (condicion <=15-jul CUMPLIDA adelantada, procs Annul_* 10/10 sandbox; sello s.4/s.11.1) + la ENMIENDA FECHADA del grant surface (+2 EXECUTE Annul, s.5); (b) confirma que las filas de medicion de P2.1/P2.2 (seq 4-7) quedaron commiteadas/atestadas en el journal. (3) CICLO COMPLETO DE P4.1 (RUTA CRITICA al 30-jul, piso minimo): GO SPEC-NOVA-P4-001 (Apply_Budget_Modification, baseline pattern-setter) a Codex -> build -> adversarial informal en SESION SEPARADA -> gate -> CAPTURA la medicion (fila OPEN al inicio + CLOSE al done via F3.3/medicion_ledger.py con --corpus EXPLICITO, tokens del err.log ANTES de rotar) -> cierra la tarea; el patron de la familia ajustes se CONGELA al arrancar PAR-1. (4) MIEMBRO BASELINE DE PAR-1 (<=17-jul): tras P4.1, GO el miembro baseline que el sello asigna (P4.2 Apply_Availability_Adjustment o P4.3 Apply_Commitment_Adjustment) -> mismo ciclo completo + captura de medicion. (5) SI SOBRA TIEMPO (detras de la ruta critica, NO antes): superficie C#/API baseline de PAR-2 sobre los procs Annul_* (ya existen; unidad medida) O avanza TASK-0246 (revision adversarial NOVA-DEV). DECISIONES YA RESUELTAS (NO despiertes al operador por estas): P3.1 = DIFERIR a Sprint 1 (sellada gobernado/Sprint-1 s.3.3; no adelantar, no enmienda, no reclasificar). LINEA ROJA DURA: NO construir NINGUNA unidad del pool Q4 pre-30-jul (P4.4, P2.3, P2-004 Get_*_List, P3.2/3.3/3.4, P6.3) -- rompe el contraste irreversible; JAMAS para rellenar tiempo. DISCIPLINA DE CAPTURA (no repetir el hueco P2.1/P2.2): cada unidad baseline captura OPEN/CLOSE con --corpus explicito. SI algo se bloquea de verdad (necesita decision del operador dormido): dejalo BLOCKED con UNA pregunta concreta y SIGUE al siguiente item -- no pares el turno entero. Si la cola legitima se agota antes de 6h: haz gobierno/higiene/docs; si de verdad no queda nada legitimo, PARA y deja nota -- NO inventes trabajo que rompa el sello. RESPONDE (para la revision del operador al levantarse) con un resumen de: TASK-0252 cerrada?; PAR-2 flip+enmienda registrados?; P4.1 en que estado (GO/build/gate/done + tokens capturados)?; PAR-1 arrancado?; cualquier blocked con su pregunta. El operador tiene un CHECK para cotejar."
question: ""
---

# DIRECTIVA - TURNO DE NOCHE (~6h seguidas, sesion fresca, dale cana)

El Operador se va a dormir y quiere que **trabajes seguido al menos 6 horas** en **sesion fresca**. Cola
completa, ordenada y **pre-decidida** para que NO te frenes esperandolo. Trabaja en orden, autonomo.

## Orden de la cola
0. **CUTOVER:** cold-start + **higiene mailbox** (archiva consumidos de open/) + responde mis directivas abiertas (P4.1, PAR-2, P3.1).
1. **Cierra TASK-0252** (fix-loop 1/2: Codex remedia los 3 hallazgos -> Analista re-juzga -> cierras).
2. **Registra gobierno** (sin Codex): PAR-2 **condicional->confirmado** + **enmienda fechada** del grant (+2 EXECUTE Annul); confirma filas de medicion P2.1/P2.2 (seq 4-7) commiteadas.
3. **CICLO COMPLETO P4.1** (ruta critica 30-jul): GO SPEC-NOVA-P4-001 -> build -> adversarial SESION SEPARADA -> gate -> **captura OPEN/CLOSE** (--corpus explicito, err.log antes de rotar) -> cierra. Congela el patron ajustes.
4. **Miembro baseline PAR-1** (<=17-jul): P4.2 o P4.3 (segun sello) -> mismo ciclo + captura.
5. **Si sobra tiempo** (detras de la ruta critica): superficie baseline PAR-2 (procs ya existen) o avanza TASK-0246.

## Decisiones YA resueltas (NO despiertes al operador)
- **P3.1 = DIFERIR a Sprint 1** (sellada gobernado; no adelantar, no enmienda, no reclasificar).
- **LINEA ROJA:** NADA del pool Q4 pre-30-jul (P4.4, P2.3, P2-004, P3.2/3.3/3.4, P6.3). Jamas para rellenar tiempo.
- **Captura:** OPEN/CLOSE por unidad, --corpus explicito.
- **Si un item se bloquea:** dejalo `blocked` con UNA pregunta y SIGUE al siguiente (no pares el turno).
- **Si la cola legitima se agota:** gobierno/higiene/docs; si nada queda, PARA y deja nota. NO inventes trabajo que rompa el sello.

## Responde (para la revision del operador al levantarse)
Resumen: TASK-0252 cerrada? / PAR-2 flip+enmienda registrados? / P4.1 estado (GO/build/gate/done + tokens) / PAR-1 arrancado? / blocked pendientes con su pregunta.
