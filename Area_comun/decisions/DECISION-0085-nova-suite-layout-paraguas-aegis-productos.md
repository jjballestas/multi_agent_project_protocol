---
decision_id: DECISION-0085
title: "Layout de la suite Nova: carpeta paraguas NOVA + instancia-metodologia Aegis + repos de producto Nova-X (enmienda a DECISION-0050 para el caso Nova)"
status: accepted
date: 2026-07-03
deciders: [operador humano, Arquitecto]
supersedes: []
supersedes_partial: [DECISION-0050]
superseded_by: []
relates_to: [DECISION-0050, DECISION-0083, GOAL-VISION-NOVA-001, TASK-0230]
phase: P2
scope: product
approval_ref: "Aprobacion directa del Operador (John Ballestas) en sesion interactiva del Arquitecto 2026-07-03 (dale); supersede las ratificaciones ad-hoc de ruta enviadas antes por el asesor (flat NOVA/ y NOVA/nova-budget)."
---

# DECISION-0085 - Layout de la suite Nova (paraguas + Aegis + productos)

> Contexto: F2.1 (TASK-0230) instancio la metodologia en D:/Agentes/Zeus/NOVA (flat, como repo).
> El Operador refino el modelo: NOVA es una carpeta PARAGUAS de la suite, con la instancia de
> metodologia (Aegis) y los productos (Nova-Budget, Nova-Treasury, ...) como repos hermanos
> dentro de ella. Enmienda DECISION-0050 (convencion de repos) para el caso Nova; el core neutral
> del hub y el epoch pineado NO se tocan.

## Decision

1. **Carpeta paraguas.** `D:/Agentes/Zeus/NOVA/` es una CARPETA plana (organizacional), NO un
   repo git. Agrupa la suite Nova en un solo lugar local; el agrupamiento es solo de disco y no
   viaja con los clones.

2. **Instancia de metodologia = `NOVA/Aegis`.** La instancia-protocolo (gobernanza/coordinacion/
   atestacion distribuida del equipo Nova) vive en `D:/Agentes/Zeus/NOVA/Aegis/`, su propio repo
   git, NEUTRAL (sin codigo de dominio; `scan_domain_neutrality` verde). Aegis es la capa que
   APLICA la metodologia sobre la suite -- la version manual de lo que el producto Zeus-Aegis
   (app suspendida, fork de Hermes) generaria automaticamente. Aegis gobierna todos los modulos.

3. **Productos = `NOVA/Nova-X`.** Cada producto de la suite es su PROPIO repo git bajo el
   paraguas: `NOVA/Nova-Budget` (presupuesto), `NOVA/Nova-Treasury` (tesoreria), y los que sigan
   (Accounting, Payroll, ...). El **prefijo `Nova-` es obligatorio**: como cada modulo es un repo
   independiente, su nombre ES su identidad cuando se clona standalone (otra maquina, CI, host
   git); sin prefijo (`Budget` a secas) el repo pierde la pertenencia a la suite. Mismo criterio
   que `Zeus-Aegis`/`Zeus-protocol`.

4. **Creacion lazy con esquema declarado.** Los repos de producto se crean CUANDO arranca su
   desarrollo (Sprint 1 / NOVA-DEV), no antes; pero este esquema queda declarado desde ya para
   que ningun agente improvise la ubicacion. Codex crea el codigo en `NOVA/Nova-X`, NUNCA dentro
   de `NOVA/Aegis` ni en el hub.

5. **Separacion e invariantes (heredados de DECISION-0050, se mantienen).** La separacion que
   importa es POR REPO (gobernanza vs producto), no por carpeta padre: el paraguas no la rompe.
   Acoplamiento unidireccional: Aegis gobierna, los productos se gobiernan, ligados por el trailer
   `Task-Id`. Ningun repo contiene el arbol de otro (nada de repo-dentro-de-repo como working
   tree). Los agentes alcanzan ambos por path (codigo en `NOVA/Nova-X`, gobernanza en `NOVA/Aegis`).

6. **Atestacion del estudio TFM = en el HUB, no en Aegis.** No confundir las dos capas que
   gobiernan: `NOVA/Aegis` = operacion distribuida del dia a dia del equipo Nova; el hub
   `multi_agent_project_protocol` = atestacion/dataset sellado del estudio (CSV, sha256 via
   intents del hub). El estudio NO se mueve a Aegis.

## Consecuencias

- **TASK-0230 (F2.1) se re-alcanza:** la instancia entregada en `NOVA/` flat se REUBICA a
  `NOVA/Aegis/`, y `NOVA/` queda como carpeta paraguas. El handoff, `instance.profile.json` y
  los `.agents/*/config.json` se actualizan a la ruta `NOVA/Aegis`. El OK del Analista sobre el
  layout flat NO cierra 0230; se re-gatea sobre `NOVA/Aegis`.
- Supersede las ratificaciones de ruta previas del asesor (flat `NOVA/` y `NOVA/nova-budget`
  anidado): la ruta canonica de la instancia es `NOVA/Aegis`.
- El futuro Zeus-Aegis (cuando se reactive) debe REPRODUCIR este layout: `NOVA/Aegis` +
  `NOVA/Nova-X`. Este esquema manual es el contrato que la app tendra que honrar.
