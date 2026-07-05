---
message_id: MSG-20260705-Operador-to-Arquitecto-DIRECTIVA-P4.1-adversarial-ruta-critica-prioriza
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - MSG-20260705-Codex-to-Arquitecto-TASK-0253-F-NOVA-01-retry-4-in-review (pidio rutear el adversarial vs commit 33adb5b)
one_line_summary: "STALL DE RUTA CRITICA detectado por el Asesor: P4.1 (TASK-0253) lleva ~5.5h en in_review (desde 14:30) esperando el adversarial informal 12-puntos -- F-NOVA-01 ya paso (retry-4), solo falta ese gate para cerrar. En esas 5.5h trabajaste gobierno (fix del prune_state que introdujiste + higiene + docs de skill), util pero NO es la ruta critica. PRIORIZA: rutea/corre YA el adversarial informal (sesion separada, vs product commit 33adb5b) -> cierra P4.1 con su fila CLOSE + tokens -> congela el patron ajustes -> abre PAR-1. Si la sesion adversarial esta dormida, activala (DECISION-0057, runtime-only). El gobierno (prune/higiene) es relleno de espera, NO debe desplazar el cierre de P4.1 (piso minimo del 30-jul). No es reproche -- es correccion de prioridad: ruta critica > gobierno."
requested_action: "[DIRECTIVA -- correccion de prioridad, ruta critica] El Asesor detecto un STALL: P4.1 (TASK-0253) esta en in_review desde ~14:30 (hace ~5.5h) esperando el adversarial informal 12-puntos, que es el UNICO paso que falta para cerrarla (F-NOVA-01 ya paso en retry-4). En esas 5.5h avanzaste gobierno (fix del prune_state que tu mismo introdujiste al meter la poda a la higiene, + higiene + docs de skill mailbox-hygiene). Ese gobierno es util PERO es relleno de espera, NO la ruta critica: P4.1 -> PAR-1 es el piso minimo del 30-jul, y no se movio en 5.5h. ACCION AHORA (en este orden): (1) RUTEA/CORRE el adversarial informal 12-puntos de P4.1 en SESION SEPARADA (dev != adversarial) contra el product commit 33adb5b + la evidencia F-NOVA-01 (HANDOFF-TASK-0253-codex-to-arquitecto-7). Si la sesion adversarial esta dormida/no-activa, ACTIVALA tu (DECISION-0057, runtime-only; es una tarea encolada que la necesita). Recordatorio: el adversarial de P4.1 debe cubrir la auth de endpoint (punto 7 del rubric + hallazgo #5 GAP vs DD-01) porque P4.1 es pattern-setter y PAR-1 heredara su patron. (2) Cuando el adversarial apruebe: cierra P4.1 -> in_review->done + CAPTURA la fila CLOSE con tokens_total_atribuibles (err.log ANTES de rotar, medicion_ledger.py --corpus explicito, clave TASK-0253 ya tiene OPEN seq 8). (3) Arranca PAR-1 (P4.2/P4.3 segun sello; BD ya pre-flighteada; SPEC citando los THROW reales). REGLA GENERAL para el resto del turno: el gobierno (prune/higiene/docs) se hace en las VENTANAS DE ESPERA de la ruta critica, NO en lugar de ella; si P4.1 puede avanzar, avanza P4.1 primero. RESPONDE con: (a) adversarial de P4.1 ruteado/corriendo (o su veredicto si ya llego); (b) si la sesion adversarial estaba dormida y la activaste; (c) P4.1 cerrada -> PAR-1 arrancada, o el blocker concreto que lo impida."
question: ""
---

# DIRECTIVA - Prioriza el adversarial de P4.1 (ruta critica parada ~5.5h)

**Stall detectado:** P4.1 (`TASK-0253`) en `in_review` desde ~14:30 (~5.5h) esperando el adversarial
informal 12-puntos -- el unico paso que falta para cerrar (F-NOVA-01 ya paso en retry-4). En esas 5.5h
avanzaste gobierno (fix del `prune_state` + higiene + docs), util pero **relleno de espera, no la ruta critica**.

## Accion ahora (en orden)
1. **Rutea/corre el adversarial informal 12-puntos de P4.1** (sesion separada, vs commit `33adb5b` +
   evidencia F-NOVA-01). Si la sesion adversarial esta dormida, **activala** (DECISION-0057, runtime-only).
   Debe cubrir la **auth de endpoint** (punto 7 + hallazgo #5 GAP) -- P4.1 es pattern-setter, PAR-1 hereda.
2. Adversarial aprueba -> **cierra P4.1** + captura fila CLOSE con tokens (`--corpus` explicito).
3. **Arranca PAR-1** (BD pre-flighteada, SPEC citando THROW reales).

## Regla para el resto del turno
Gobierno (prune/higiene/docs) = en las **ventanas de espera** de la ruta critica, NO en lugar de ella.
Si P4.1 puede avanzar, avanza P4.1 primero. No es reproche -- correccion de prioridad.

## Responde
(a) adversarial ruteado/corriendo/veredicto; (b) sesion adversarial activada?; (c) P4.1 cerrada -> PAR-1, o el blocker.
