---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-profundiza-cola-sello-e-infra
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-amplia-cola-pre-sello (ola previa; churneada)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md (finalizar TODAS las secciones)
  - TASK-0245 (watchdogs -> capa neutral skills/) + F1.6 (aprendizajes-externos)
one_line_summary: "PROFUNDIZA la cola sin-idle (churneas rapido). Backlog sustancial, en orden: (P1 camino critico) FINALIZA EL SELLO AL 100% -- todas las secciones + el SORTEO PRE-COMMIT (par_ids + estimates lockeados + algoritmo + timestamp T, listo para atestar, todo menos la semilla-del-dia) + el doc del sandbox de mutadores sellado (precondicion P4.x -> READY); asi el 08-jul es un intent atomico de un click. (P2 infra independiente) ACTIVA TASK-0245: porta los watchdogs operativos a la capa NEUTRAL skills/ (enforcement exportable). (P3 relleno) F1.6 aprendizajes-externos + REPORTE HUMANO del ciclo de build (GOAL-P1+skill+SPECs, en Area_comun/reports/) + pre-diseno (doc) de los items post-sello (cross-atestacion NOVA/Aegis de DECISION-0088 + scoping del programa i18n Carril B). Sello 08-jul manda; dev medido NO abre pre-sello."
requested_action: "[DIRECTIVA] Churneas rapido -> profundizo tu cola con backlog sustancial (trabaja en orden; el sello 08-jul es el reloj; el dev MEDIDO no abre pre-sello). (P1 CAMINO CRITICO -- FINALIZA EL SELLO AL 100%): completa TODAS las secciones del SELLO-ETAPA-1-nova-budget-DRAFT.md (no solo s.1 manifiesto ya hecho): delimitacion del estudio, anexo de riesgos, calendario/triggers, y sobre todo el SORTEO PRE-COMMIT -- arma el artefacto atestable del sorteo: par_ids + los estimates LOCKEADOS (6 M + 4 S, ya confirmados) + el algoritmo (paridad del primer byte de SHA-256(par_id + semilla)) + timestamp T, todo commiteado y listo para atestar ANTES de la semilla; deja como UNICO pendiente-del-dia la semilla (primer pulso NIST posterior a T) + su sha256. Ademas incorpora el DOC DEL SANDBOX DE MUTADORES sellado (el que te rutee, MSG-...sandbox-mutadores) y voltea la precondicion de las P4.x a READY. Objetivo: el 08-jul es un intent atomico limpio de un solo paso, cero construccion apurada. (P2 INFRA INDEPENDIENTE -- ACTIVA TASK-0245): porta los WATCHDOGS operativos (15-min + higiene mailbox) a la capa NEUTRAL skills/ para que sean enforcement EXPORTABLE al instanciar (hoy viven como scripts/runbook de instancia; deben subir a la capa neutral, sin dominio). Es trabajo real de arq+infra, independiente del sello. (P3 RELLENO, si hay holgura): (a) F1.6 aprendizajes-externos (extraccion de reglas); (b) REDACTA EL REPORTE HUMANO del ciclo de build en Area_comun/reports/ (GOAL-P1 construido+medido+atestado + skill codegen-triage + 14 SPECs gateadas + piloto de medicion con sus 3 hallazgos; yo redacto/tu ratificas-o-viceversa per la regla de reportes); (c) PRE-DISENA (solo doc, no ejecucion) los items post-sello: el mecanismo de CROSS-ATESTACION de la migracion a NOVA/Aegis (DECISION-0088: el journal del hub registra el sha256 de la atestacion de la instancia por gate) + el SCOPING del programa i18n de CARRIL B (DECISION-0087/0089: superficie publicable a ingles, incl. la normalizacion de output-keys de la skill codegen-triage). NOTA: los estimates S/M/L (lockeados) y el sandbox de mutadores (construido) YA son del Operador y estan HECHOS -- no los re-generes; solo incorporalos. Cualquier bloqueo -> mailbox con pregunta concreta, no idle."
question: ""
---

# DIRECTIVA - Profundiza la cola (sello al 100% + infra independiente)

Churneas rapido; profundizo tu cola. Trabaja en orden; el sello 08-jul manda; dev medido NO abre pre-sello.

## P1 - CAMINO CRITICO: finaliza el SELLO al 100%
Completa TODAS las secciones del SELLO draft (no solo s.1): delimitacion, riesgos, calendario, y el
**SORTEO PRE-COMMIT** (par_ids + estimates lockeados 6M+4S + algoritmo SHA-256(par_id+semilla) + timestamp T,
atestable, todo menos la semilla-del-dia). Incorpora el doc del **sandbox de mutadores** sellado y voltea la
precondicion P4.x a **READY**. Objetivo: 08-jul = intent atomico de un click, cero construccion apurada.

## P2 - INFRA INDEPENDIENTE: activa TASK-0245
Porta los watchdogs (15-min + higiene mailbox) a la capa NEUTRAL `skills/` -> enforcement EXPORTABLE al
instanciar (hoy son scripts de instancia; suben a la capa neutral, sin dominio).

## P3 - RELLENO (si hay holgura)
(a) F1.6 aprendizajes-externos; (b) REPORTE HUMANO del ciclo de build en `Area_comun/reports/`; (c) pre-diseno
(doc) de la cross-atestacion NOVA/Aegis (DECISION-0088) + scoping del programa i18n Carril B (DECISION-0087/0089).

NOTA: estimates (lockeados) + sandbox (construido) YA estan hechos -- solo incorporalos, no re-generes. Bloqueo -> mailbox, no idle.
