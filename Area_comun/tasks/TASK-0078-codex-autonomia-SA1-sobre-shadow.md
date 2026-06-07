---
id: TASK-0078
owner: Codex
status: done
type: implementation
priority: normal
created_at: 2026-06-08
phase: P2
spec_id: Area_comun/specs/SPEC-0064-autonomia-supervisada.md
linked_decisions: [DECISION-0024, DECISION-0021, DECISION-0022]
relates_to: [TASK-0038]
---

> IN_REVIEW (entregada por Codex 2026-06-08). DECISION-0024 APROBADA. Primera rebanada SA.1 del decompose (ver
> SPEC-0064). SHADOW: sin agentes reales, enforce intacto. GO en mailbox.

# TASK-0078 (SA.1) - Sobre de supervision en SHADOW (sin agentes reales)

## Contexto

El loop `run_loop` ya es multi-turno para replay/recorded con todas las paradas duras (gate, ruta/escalada,
budget/deadline, schema, human_required, dirty no declarado, post-gate). El unico cerrojo a la autonomia real
es `if subprocess and not once: reject`. SA.1 construye el **sobre de supervision** alrededor del loop y lo
ejercita con `RecordedInvoker` (replay) -- SIN tocar el invoker real -- para demostrar que acota y observa.

## Alcance (SA.1, aditivo, off-by-default, shadow)

1. **C1 - Registro de activacion.** `protocol.config.json` `runtime.supervised_autonomy{enabled:false,
   activation_decision,approved_by,approved_at,caps:{max_turns,...}}` + flag CLI `--allow-supervised-autonomy`
   + `supervised_autonomy_activation_error(config)` (analogo a `real_invoker_activation_error`). Sin registro
   valido + caps => el cerrojo `--once` del invoker real **sigue intacto** (DECISION-0021 sin cambios).
2. **C2 - Tope de turnos.** `caps.max_turns` (entero pequeno): el loop nunca encadena mas de `max_turns`; al
   alcanzarlo para con `outcome=max_turns_reached`. Se ejercita en modo multi-turno con `RecordedInvoker`.
3. **C6 - Reporte de corrida.** Extension del summary + `*.runreport.md` legible (turnos, paradas, costo,
   commits, motivo de cierre).
4. **Golden** deterministas (sin red): para por max_turns; activacion sin registro => rechazo; off =>
   byte-equivalente (comportamiento actual intacto). Paridad `.ps1` donde aplique + CI.

## Fuera de alcance (otras rebanadas)

- C3 kill-switch/pausa + C4 reloj de pared (SA.2); C5 checkpoint humano + escalacion (SA.3); invoker real bajo
  el sobre (SA.4, con GO + rollback); docs/promocion (SA.5).
- **NO** tocar el invoker real ni encender autonomia real. Shadow puro.

## Restricciones

- Off/shadow => byte-equivalente; cerrojo `--once` del invoker real intacto sin registro valido.
- Determinista (sin reloj/red salvo lo ya provisto). Sin secretos. Neutral de dominio.
- Handoff autocontenido; release atomico (DECISION-0018); staging por paths (DECISION-0020).

## Cierre (DoD)

C1 (registro+flag+error) + C2 (max_turns con parada) + C6 (runreport) ejercitados con RecordedInvoker;
golden (max_turns, rechazo sin registro, off byte-equivalente); paridad/CI; gates verdes; sin tocar invoker
real. Tras SA.1: SA.2 (kill-switch+reloj).
