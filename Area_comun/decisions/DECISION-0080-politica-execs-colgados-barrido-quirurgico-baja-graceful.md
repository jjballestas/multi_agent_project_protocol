---
decision_id: DECISION-0080
title: "Politica de manejo de execs colgados (A: barrido quirurgico) y baja de runtimes de peers (B: baja graceful)"
status: accepted
date: 2026-07-02
deciders: [operador humano, Arquitecto, Analista]
supersedes: []
superseded_by: []
relates_to: [DECISION-0057, DECISION-0018, DECISION-0022, TASK-0235, TASK-0236, REQ-ZEUS-001]
scope: process
phase: P2
---

# DECISION-0080 - Politica de execs colgados (A) y baja graceful de runtimes (B)

## Contexto

El incidente 2026-06-30/07-01 (un exec de cron completo pero colgado retuvo lock/prompt ~14h y trabo la cola) y su
recurrencia 2026-07-02 (npm test colgado en clon limpio + prompt compartido retenido + dos instancias de cron)
obligaron a separar TRES cosas que no son lo mismo, propuestas en `personal/Arquitecto/DISCUSSION-cron-zombie-policy.md`
y sometidas a review adversarial del Analista (veredicto `Area_comun/artifacts/ANALISTA-TASK-0235-cron-policy-AB-veredicto.md`):

- **A. Barrido quirurgico** de un exec colgado (zombie que retiene lock/prompt).
- **B. Baja graceful** de un runtime de peer SANO (ocioso).
- **C. Causa raiz** = hardening del harness -> **YA CERRADA con TASK-0235** (exec-lease), en remediacion/refuerzo con
  TASK-0236 (prompt por-exec, tree-kill, guard de instancia unica, enforcement de lease huerfana).

El Analista dio GO SUSTANTIVO a A y B (los 8 vectores adversariales de la seccion 5 de la DISCUSSION PASAN, algunos
con condicion). Su unico NO-GO fue de cierre canonico por el gate secretless: el HEAD `cc1dac4` fallaba
`validate_collaboration_state.py` en clon limpio por mismatch `.md`/index de TASK-0229 y TASK-0237. Ese drift ya se
corrigio; el HEAD de anclaje de esta decision valida en clon limpio con exit 0.

## Decision

Se **acepta A y B como politica** de la instancia viva, con las siguientes condiciones **NORMATIVAS** (copiadas del
veredicto del Analista; no son detalle de implementacion sino requisito de la politica):

### A. Barrido quirurgico de execs colgados (`scripts/sweep_cron_zombies.py`)
1. **Criterio de kill = lease VENCIDO por `PID + process_start_time_utc`**, NO por posesion de handle. Restart Manager
   queda como forense manual, nunca como autorizacion suficiente de kill. Un holder vivo con deadline futuro -> `skip`
   (`reason=lease_not_expired`). PID reciclado -> `pid_reuse_start_time_mismatch` (no matar).
2. **dry-run por DEFECTO;** matar exige flag explicito.
3. **Kill de ARBOL completo** (`taskkill //PID <pid> //T //F`), no de un solo pid (los hijos esbuild/node/cmd
   sobreviven a un kill de un pid). (Refuerzo TASK-0236.)
4. **Lock global** `.protocol-tmp/cron_zombie_sweeper.lock` que serializa barredores + **re-check bajo lock** antes de
   matar/limpiar (evita carreras entre barredores).
5. **Exclusiones:** `owner_not_target` (no tocar leases de otro owner) y **`checker_owner_excluded`** (no matar el exec
   del checker en curso). **La invocacion operativa DEBE fijar el `checker-owner` real de la ventana** (el default del
   script es `Arquitecto`; barrer al `Analista` desde un contexto donde el checker tambien es Analista sin pasar el
   flag NO lo protege -- riesgo declarado #7).
6. **Deny-list antes del kill:** no matar procesos cuyo cmdline toque `submit_intent`, `git`, `npm test`, `vitest`,
   `node --test`, `validate_collaboration_state.py`, ni si hay rutas dirty bajo claim activa del owner.
7. **Post-kill:** correr `validate_collaboration_state.py` + drift + `scan_encoding.py`. **Si falla -> mensaje
   DECISION-0018 y FRENAR la cola** (no continuar).
8. **On-demand**, cuando aparecen los sintomas (2+ timeouts del monitor con crones vivos, `LOCKED skip`/`LOOP_ERROR`),
   NO en loop ciego.

### B. Baja graceful de un runtime de peer SANO
1. **`stop_after_current_turn`** via el marcador de baja del propio cron: deja de tomar trabajo nuevo, ESPERA al exec
   en curso, libera lock/lease en `finally`. **Nunca force-kill de un runtime sano.**
2. Solo al **cierre real del proceso de coordinacion** (goal cumplido / orden del operador), NO en cada lull de cola.
3. **Mantener 24/7 headless mientras REQ-ZEUS este activo.** El punto de corte objetivo = cierre real de coordinacion
   u orden explicita del operador (no "cola vacia", que en un build activo casi nunca lo esta).

### C. Causa raiz
Cerrada por TASK-0235 (exec-lease: self-heal por PID+start-time con proceso muerto, deadline+kill, liberacion de lock
en `finally`) y en refuerzo por TASK-0236. No es objeto adicional de esta decision.

## Consecuencias

- El barrido de zombies NUNCA es politica automatica ciega; es intervencion gobernada con los guards de arriba. El
  `taskkill` blind `//T` sobre el cron (que fallo en el incidente: no agarra al huerfano y mata execs vivos) queda
  PROHIBIDO como metodo.
- Neutralidad: `scope: process` (operacion de la instancia viva), no toca el core del protocolo ni introduce dominio.
- Guards normativos anclados al veredicto del Analista; su artefacto es la evidencia adversarial de que A/B no matan
  trabajo bueno (vectores #1 y #7).
