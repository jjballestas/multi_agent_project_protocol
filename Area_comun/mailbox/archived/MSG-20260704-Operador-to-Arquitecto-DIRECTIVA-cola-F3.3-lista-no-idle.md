---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-cola-F3.3-lista-no-idle
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-sorteo-verificado-camino-optimo-no-standdown (archivada: cola ya ruteada; el sello quedo atestado seq 3831)
  - personal/asesor/DRAFT-SPEC-F3.3-instrumentacion.md (ENTREGABLE NUEVO del Asesor: la SPEC de diseno de F3.3, lista)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.7 (plan Q1-Q5) + s.8/s.10 (schema + reglas)
  - SPEC-0079 / DECISION-0033 (cost-attribution, primitiva a reusar)
one_line_summary: "[DIRECTIVA] MANTENTE SIN IDLE (trabajas rapido). La SPEC de diseno de F3.3 ya esta lista (personal/asesor/DRAFT-SPEC-F3.3-instrumentacion.md): (1) FORMALIZALA a NOVA-SPEC-T-001 y RUTEALA a Codex-maker/Analista-checker AHORA -- es el critical-path para auto-instrumentar el dev medido P2. En PARALELO, mientras Codex construye: (2) coordina/prepara el dev medido P2.1/P2.2 (baseline 3-25 jul; maker Codex + adversarial sesion separada; manual medicion_ledger.py = fallback probado). (3) arma el monitor PAR-2 condicional (hardening <=15-jul, procs Annul_*; si no llegan, registra el trigger de caida). RE-LLENA la cola al cerrarse cada item; no idle entre ellos. El Asesor entrega el draft de F3.2 (aritmetica backlog + Q4 subpotenciado + regla adopcion, para Etapa 2 <=29-jul) en paralelo. Responde: id de la tarea F3.3 a Codex + estado de coordinacion P2 + monitor PAR-2 armado."
requested_action: "[DIRECTIVA] No te dejo sin trabajo -- trabajas rapido, asi que te ruteo la COLA PRIORIZADA COMPLETA y la re-lleno al cerrarse cada item; trabaja los items en PARALELO donde no haya dependencia y no quedes idle entre ellos. (Q1 CRITICAL-PATH, accionable YA) La SPEC de diseno de F3.3 esta LISTA: personal/asesor/DRAFT-SPEC-F3.3-instrumentacion.md (3 eventos + motor: cost.attributed AUTOMATICO por tarea_id reusando la primitiva SPEC-0079/DECISION-0033 -- lee el cumulativo del err.log/STDERR, escribe tokens_total_atribuibles, degradacion por-cubeta a NA sellada, idempotente; defect.reported validado vs schema_defectos v1.0 con detector para la paridad de Q2; manual.intervention -> fila OVERHEAD-FIJO con tag_incidente, aislamiento de teething s.10; study_metrics.py determinista con golden que computa Q1-Q5 del plan s.7). FORMALIZALA a NOVA-SPEC-T-001 y RUTEALA a Codex-maker / Analista-checker AHORA. Debe estar VIVA antes de que abra el dev medido P2 (auto-instrumenta el baseline; manual medicion_ledger.py es el fallback probado, no bloquea). Contrato de aceptacion y traza Q1-Q5 estan en la spec. (Q2 EN PARALELO, sin dependencia de F3.3) mientras Codex construye F3.3, coordina/prepara el DEV MEDIDO P2.1/P2.2 (ventana baseline 3-25 jul): las SPECs P2 ya estan entregadas y verificadas (b3607910); maker Codex + adversarial en SESION SEPARADA; abre con F3.3 lista o con captura manual si no. (Q3 CONDICIONAL, time-boxed) arma el monitor del CHECKPOINT HARDENING PAR-2 (<=15-jul, procs Annul_Availability_Certificate/Annul_Commitment de nova-hardening): si llegan, prepara las SPECs PAR-2; si no llegan al 15-jul, registra el trigger de caida de PAR-2 (coherente con regla 8: el dev nunca crea el proc). (Q4 BACKLOG, re-llenar cuando drenen los de arriba) miembros gobernados de pares (desbloqueo 17-jul, heredan patron congelado P4.1). El Asesor entrega EN PARALELO el draft de F3.2 (aritmetica del backlog + condicionalidad Q4 consolidada + regla de adopcion) para el sello Etapa 2 (<=29-jul); tu lo gobiernas cuando llegue. RECORDATORIO del hallazgo: el sorteo 8/2 hace Q4 subpotenciado -> se declara el poder efectivo (regla sellada), F3.2 lo consolida. RESPONDE con: (a) id de la tarea F3.3 ruteada a Codex; (b) estado de la coordinacion del dev medido P2; (c) confirmacion de que el monitor PAR-2 esta armado. Fondo intocable ya verificado; sello Etapa 1 atestado (seq 3831). Frontera: F3.3 vive en la instancia del estudio, NO en el core neutral (no metas dominio Nova en archivos genericos)."
question: ""
---

# DIRECTIVA - Cola priorizada sin idle (F3.3 lista, entrego la SPEC)

Trabajas rapido: no te dejo sin trabajo. Te ruteo la **cola completa priorizada** y la re-lleno al
cerrarse cada item. Trabaja en **paralelo** donde no haya dependencia; no quedes idle entre items.

## Q1 -- CRITICAL PATH, accionable YA
La **SPEC de diseno de F3.3 esta LISTA**: [DRAFT-SPEC-F3.3-instrumentacion.md](../../personal/asesor/DRAFT-SPEC-F3.3-instrumentacion.md).

- **3 eventos + 1 motor:**
  1. `cost.attributed` AUTOMATICO por `tarea_id` -- REUSA la primitiva aceptada de SPEC-0079/DECISION-0033
     (off-by-default, plano de protocolo). Lee el cumulativo del `err.log`/STDERR, escribe
     `tokens_total_atribuibles`, **degradacion por-cubeta a NA SELLADA** (hallazgo del piloto GOAL-P1),
     idempotente por tarea.
  2. `defect.reported` validado vs `schema_defectos.json` v1.0, con `detector` + `paridad_detector` para la
     serie confirmatoria de Q2.
  3. `manual.intervention` -> fila OVERHEAD-FIJO con `tag_incidente_maquinaria` (aislamiento de teething, s.10).
  4. `study_metrics.py` DETERMINISTA con golden que computa Q1-Q5 del plan s.7 (guard duro NO-inferencial
     en Q3; Q4 esqueleto pre-ventana + subpotenciado declarado).
- **Accion:** FORMALIZA a NOVA-SPEC-T-001 y RUTEA a Codex-maker / Analista-checker AHORA. Debe estar VIVA
  antes de que abra el dev medido P2 (auto-instrumenta el baseline; `medicion_ledger.py` manual = fallback
  probado, no bloquea). Contrato de aceptacion y traza Q1-Q5 en la spec.

## Q2 -- EN PARALELO (sin dependencia de F3.3)
Mientras Codex construye F3.3, coordina/prepara el **dev medido P2.1/P2.2** (ventana baseline 3-25 jul).
SPECs P2 ya entregadas y verificadas (b3607910). Maker Codex + adversarial en SESION SEPARADA. Abre con
F3.3 lista o con captura manual si no.

## Q3 -- CONDICIONAL, time-boxed
Arma el monitor del **checkpoint hardening PAR-2** (<=15-jul, procs `Annul_Availability_Certificate` /
`Annul_Commitment`). Si llegan: prepara las SPECs PAR-2. Si no al 15-jul: registra el trigger de caida
(regla 8: el dev nunca crea el proc).

## Q4 -- BACKLOG (re-llenar al drenar lo de arriba)
Miembros gobernados de pares (desbloqueo 17-jul; heredan el patron congelado de P4.1).

## En paralelo (Asesor)
Entrego el draft de **F3.2** (aritmetica del backlog + condicionalidad Q4 consolidada + regla de adopcion)
para el sello Etapa 2 (<=29-jul); tu lo gobiernas cuando llegue. Recordatorio: el sorteo 8/2 hace Q4
subpotenciado -> se declara el poder efectivo (regla sellada); F3.2 lo consolida.

## Responde con
(a) id de la tarea F3.3 ruteada a Codex; (b) estado de la coordinacion del dev medido P2; (c) confirmacion
de que el monitor PAR-2 esta armado.

Frontera: F3.3 vive en la instancia del estudio, NO en el core neutral. Sello Etapa 1 atestado (seq 3831);
fondo intocable verificado.
