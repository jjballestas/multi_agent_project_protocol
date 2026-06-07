---
spec_id: SPEC-0054-faseB3-drift-hard-fail
task_id: TASK-0068
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0017, DECISION-0015, DECISION-0014, DECISION-0011]
relates_to: [SPEC-0039, SPEC-0052, SPEC-0053, SPEC-0038]
---

> Tercera rebanada de la Fase B (SPEC-0039 sec.4). Se monta sobre B.1 (replay/drift, done) y B.2
> (materializacion opt-in, done). Aditivo, triple-gated, off=byte-equivalente. Cambio incompatible del flujo
> manual o del contrato del turno => blocked + DECISION.

# SPEC-0054 - Fase B.3: drift del estado de protocolo como hard-fail (cuando el runtime es el escritor habitual)

## 1. Objetivo

Cerrar el invariante objetivo de la Fase B: `hot *.json == materializa(replay(log))` como **hard-gate**.
Hoy (B.1) el drift es solo WARNING. B.3 lo promueve a **error duro** PERO solo cuando el runtime es el
escritor habitual del estado (no cuando el repo sigue en edicion manual), para no romper el flujo vivo.
Cierra el FOLLOW-UP de Fase 2 (assert_snapshot_matches) extendido al estado de protocolo.

## 2. Gating: la ventana de transicion (SPEC-0039 sec.4)

Se introduce un tercer flag `event_state.enforce` (live + template, **default false**), que se interpreta
como "el runtime es el escritor habitual del estado de protocolo => el drift es un fallo". Jerarquia de
flags (todos default false; cada uno presupone el anterior en sentido operativo):

| Flag | Rebanada | Efecto |
|---|---|---|
| `event_state.enabled` | B.1 | replay/drift observacional; validador emite **WARNING** de drift (con runtime/state). |
| `event_state.materialize` | B.2 | el runtime materializa los *.json desde replay(log) (opt-in, runtime-tier). |
| `event_state.enforce` | **B.3** | el drift pasa de WARNING a **hard-fail** del validador global y aborta el commit del runtime en apply. |

Regla off=byte-equivalente: con `enforce=false` el comportamiento es identico a B.1/B.2 (warning-only). El
repo vivo mantiene `enforce=false` (edicion manual intacta); encenderlo es decision del operador (y exige
haber migrado a materializacion, B.2/B.4).

## 3. Alcance (aditivo, triple-gated, off=byte-equivalente)

1. **Validador global py/.ps1:** cuando `enabled && enforce && runtime/state tiene contenido` y hay drift =>
   `validation.fail(...)` (hard-fail repo-wide) en vez de `warn`. Con `enforce=false` => warning-only (B.1).
   Mensaje claro que liste los paths en drift y como reconciliar (re-materializar / genesis).
2. **Gate en apply (runtime):** ANTES de commitear el turno del runtime, si `enabled && enforce`, correr el
   chequeo de drift del estado de protocolo (reusando `protocol_state_drift`); si hay drift => abortar el
   commit (discard + block), consistente con la atomicidad de apply/TASK-0041 y con el hard-gate de
   control-plane de Fase A (3.2). Con `enforce=false` => comportamiento actual.
3. **Sin nueva maquinaria de estado:** reutiliza `protocol_state_drift`/`materialize_protocol_state` de B.1
   y la materializacion de B.2. B.3 solo cambia la SEVERIDAD (warn->fail) bajo el flag y la cablea en apply.
4. Golden `examples/runtime_protocol_enforce_cases` + CI.

## 4. Limites duros (NO en B.3)

- NO prohibir/migrar la edicion manual del repo vivo (B.4, posible DECISION/MAJOR). B.3 solo HABILITA el
  hard-fail bajo flag; no obliga a nadie a encenderlo.
- NO encender `event_state.enforce` en el repo vivo en esta tarea (queda off).
- NO cambiar el contrato del turn schema ni romper el fallback N=2.
- Cambio incompatible del flujo manual o del contrato => `blocked` + pregunta.

## 5. Tests (golden determinista, sin red)

1. `enforce=true` + drift introducido => validador global **hard-fail** (exit != 0) con paths listados.
2. `enforce=true` + estado coherente (materializado) => validador **pasa**.
3. `enforce=false` (o sin runtime/state) => warning-only / byte-equivalente a B.1 (sin fallo).
4. apply: con `enforce=true` y drift => commit del turno **abortado** (todo-o-nada, sin escritura parcial);
   con coherente => commitea.
5. Combinaciones de flags (enabled/materialize/enforce) coherentes; tier != runtime no fuerza enforce.
6. Regresion: suite runtime + B.1 (replay) + B.2 (materialize) intactos; fallback N=2 byte-equivalente; paridad py/.ps1.

## 6. SemVer

- MINOR (aditivo, triple-gated, off=byte-equivalente; no prohibe edicion manual). La prohibicion/migracion
  del flujo manual (B.4) se evalua aparte y puede ser MAJOR.

## 7. Nota de secuencia

Es la tercera de 4 rebanadas (B.1 done -> B.2 done -> **B.3** -> B.4). Tras B.3, B.4 (migrar/prohibir
edicion manual) probablemente requiera DECISION nueva + evaluacion SemVer (posible MAJOR) + aprobacion humana.
