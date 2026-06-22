---
task_id: TASK-0152
title: "Proyecto-front (RF-14): carga por archivo v2 FASE C - agente extractor (archivo->candidatas) + endurecimiento AC45 (guard de salida de red a TODO src/** + purga/TTL del raw) (AC41 loop/AC45, SPEC-0086 ext10, DECISION-0056)"
type: product
status: ready
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0056]
created_at: 2026-06-22
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0152-codex-file-intake-v2-faseC.md
---

# TASK-0152 - Carga por archivo v2 FASE C (agente extractor) (SPEC-0086 ext10, AC41 loop/AC45; DECISION-0056)

> ENCOLADA (proposed). NO promovida a ready/GO aun: depende de Fase B (TASK-0151) cerrada. Es la pieza grande +
> la VENTANA REAL DE MODELO (el agente lee el archivo externo). maker=Codex / checker=Arquitecto + PASADA DEL
> ANALISTA al cierre. **Uso vivo de la v2 = GO APARTE del operador** (con Analista al cierre de C). OFF-by-default.

## Alcance (Fase C)
1. **Loop de extraccion (AC41):** un AGENTE LLM-backed toma la extraction-task (contrato emitido en Fase A),
   lee el archivo del store, extrae historias/casos -> escribe candidatas en el store-no-ledger (formato del
   contrato). Frontera de egress del agente acotada/etiquetada/consentida.
2. **AC45 (PREREQUISITO, antes de encender el agente):** (a) el guard de salida de red se AMPLIA a TODO `src/**`
   y marca CUALQUIER salida de red (no solo proveedores nombrados); unico egress permitido = git push gobernado +
   lecturas allowlisted; estatico falsable + control positivo. (b) politica de purga/TTL del raw en os-tmp (borra
   al estado terminal del candidato + barredor TTL para huerfanos). (c) tests deterministas (sin flake).

## DoD
- AC41 loop + AC45 verdes (extraccion produce candidatas en store-no-ledger; guard a todo src/** marca cualquier
  red saliente; purga/TTL del raw). Carry AC40/AC43/AC44.
- node --test/CI verde EN CLON LIMPIO; #4 byte-identica; validate con/sin secretos exit 0; drift 0; neutralidad 0.
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA antes de cerrar.
- **Uso vivo (encender el agente contra archivos reales) = GO APARTE del operador.**

## Prereq
Fase B (TASK-0151) cerrada. El Arquitecto promueve C (ready + GO) DESPUES de cerrar B.
