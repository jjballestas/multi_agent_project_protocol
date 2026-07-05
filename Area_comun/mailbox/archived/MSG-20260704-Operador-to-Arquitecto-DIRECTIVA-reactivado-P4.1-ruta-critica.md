---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-reactivado-P4.1-ruta-critica
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-CONSULTA-p31-construible-y-drenar-0252 (resuelve: P3.1 = OPCION 3 diferir)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.3.2 (baseline 3-25 jul) + s.11.1 (calendario)
  - Area_comun/specs/nova/SPEC-NOVA-P4-001-apply-budget-modification.md (P4.1 baseline pattern-setter)
one_line_summary: "OPERADOR REACTIVO Codex+Analista. Retomamos el pipeline con foco RUTA CRITICA al 30-jul, no relleno de ocio. COLA: (1) PROMUEVE+GO P4.1 (SPEC-NOVA-P4-001, Apply_Budget_Modification, baseline pattern-setter) a Codex YA -- precond sandbox+GRANT ya listas; es piso minimo del 30-jul. (2) Tras P4.1 con patron congelado -> miembro baseline PAR-1 (P4.2/P4.3 segun sello) inicia <=17-jul. (3) TASK-0252 harness = relleno baja prioridad, cuando haya hueco, NO compite con P4.1. (4) P3.1 = OPCION 3 DIFERIR a Sprint 1 (esta sellada gobernado/Sprint-1 s.3.3; no adelantar por evitar idle, no enmienda, no reclasificar). DISCIPLINA DE CAPTURA (critico, no repetir el hueco P2.1/P2.2): cada unidad baseline captura fila OPEN al inicio + CLOSE al done via F3.3/medicion_ledger.py con --corpus EXPLICITO, tokens del err.log ANTES de rotacion. LINEA ROJA: nada del pool Q4 pre-30-jul (P4.4, P2.3, P2-004, P3.2/3.3/3.4, P6.3)."
requested_action: "[DIRECTIVA] El Operador REACTIVO Codex + Analista. Retomamos con foco RUTA CRITICA al 30-jul (no relleno de ocio). Cola priorizada, trabaja en orden: (1) PROMUEVE proposed->ready->GO **P4.1** a Codex YA: SPEC-NOVA-P4-001 (Apply_Budget_Modification), unidad BASELINE pattern-setter de la familia ajustes, EXCLUIDA del contraste, ventana 3-25 jul. Sus precondiciones ya estan: sandbox mutadores sellado (<=14-jul HECHO) + GRANT EXECUTE (HECHO). Es PISO MINIMO VIABLE del 30-jul (s.10): sin P4.1 + miembro baseline PAR-1, el 30-jul dispara STOP-total por SLA. checker_formal=0 (baseline), adversarial informal de 12 puntos en SESION SEPARADA (dev != adversarial). (2) TRAS P4.1 (su patron se CONGELA al arrancar PAR-1): promueve el MIEMBRO BASELINE de PAR-1 (P4.2 Apply_Availability_Adjustment o P4.3 Apply_Commitment_Adjustment, el que el sello asigne al brazo baseline) -- inicia <=17-jul. (3) TASK-0252 (harness paridad exec-vs-endpoint, rol budget_sandbox_verifier / login nova_budget_verifier): relleno de BAJA prioridad, drena cuando haya hueco, NO compite con P4.1. (4) P3.1 = OPCION 3: DIFERIR a Sprint 1. Tenias razon: esta clasificada GOBERNADO/Sprint-1 en el sello (DECISION-0091 s.3.3), NO baseline (mi framing previo fue impreciso: excluida-de-Q4 != baseline). NO la adelantes por evitar idle (causa debil = alteracion post-hoc del pre-registro); NO enmienda, NO reclasificar. Se queda anclando Sprint 1. DISCIPLINA DE CAPTURA DE MEDICION (critico -- no repetir el hueco de P2.1/P2.2): para CADA unidad baseline (P4.1, miembro PAR-1) captura la fila OPEN al inicio y CLOSE al done via F3.3/medicion_ledger.py, con --corpus EXPLICITO apuntando al corpus real (el gotcha que ya detectaste: resuelve relativo al CWD), y lee los tokens del err.log ANTES de que rote. NO diferir a la reconciliacion 26-29 jul. LINEA ROJA (recordatorio): NO construir NINGUNA unidad del pool Q4 pre-30-jul (P4.4, P2.3, P2-004 Get_*_List, P3.2/3.3/3.4, P6.3) -- rompe el contraste irreversible. NOTA nova-hardening: los procs Annul_* (PAR-2, <=15-jul) van en la pista de BD del Operador, FUERA del dev medido (regla 8); el Asesor puede redactar la SPEC de hardening si el Operador lo pide. RESPONDE con: (a) P4.1 GO-eada a Codex (task id); (b) confirmacion de la disciplina de captura OPEN/CLOSE con --corpus explicito; (c) P3.1 diferida (Opcion 3 registrada)."
question: ""
---

# DIRECTIVA - Reactivado: P4.1 ruta critica al 30-jul (no P3.1)

El Operador **reactivo Codex + Analista**. Retomamos con foco **ruta critica al 30-jul**, no relleno.

## Cola priorizada (en orden)
1. **PROMUEVE + GO P4.1 a Codex YA** -- `SPEC-NOVA-P4-001` (Apply_Budget_Modification), baseline
   pattern-setter, ventana 3-25 jul. Precondiciones LISTAS (sandbox sellado + GRANT EXECUTE). Es
   **PISO MINIMO del 30-jul**: sin P4.1 + miembro baseline PAR-1, el 30-jul dispara STOP-total.
   checker_formal=0; adversarial informal en SESION SEPARADA.
2. **Tras P4.1 (patron congelado) -> miembro baseline PAR-1** (P4.2 o P4.3 segun el sello) -- inicia <=17-jul.
3. **TASK-0252** (harness paridad) = relleno BAJA prioridad, cuando haya hueco; NO compite con P4.1.
4. **P3.1 = OPCION 3: DIFERIR a Sprint 1.** Tenias razon: sellada GOBERNADO/Sprint-1 (s.3.3), no baseline.
   No adelantar por evitar idle; no enmienda, no reclasificar. Ancla Sprint 1.

## Disciplina de captura (critico -- no repetir el hueco P2.1/P2.2)
Cada unidad baseline (P4.1, PAR-1): fila **OPEN al inicio + CLOSE al done** via F3.3/`medicion_ledger.py`,
`--corpus` **EXPLICITO** (el gotcha del CWD que ya detectaste), tokens del **err.log ANTES de rotar**. NO
diferir a la reconciliacion 26-29 jul.

## Linea roja
NO construir unidades del pool Q4 pre-30-jul (P4.4, P2.3, P2-004, P3.2/3.3/3.4, P6.3): contraste irreversible.

## nova-hardening (aparte)
Los procs `Annul_*` (PAR-2, <=15-jul) van en la pista de BD del Operador, FUERA del dev medido (regla 8).
El Asesor redacta la SPEC de hardening si el Operador la pide.

## Responde con
(a) P4.1 GO-eada (task id); (b) disciplina de captura OPEN/CLOSE con `--corpus` explicito confirmada;
(c) P3.1 diferida (Opcion 3 registrada).
