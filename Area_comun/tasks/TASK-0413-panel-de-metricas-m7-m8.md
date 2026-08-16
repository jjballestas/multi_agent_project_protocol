---
id: TASK-0413
title: Panel de metricas -- M7 cobertura de verificacion y M8 tiempo-mensaje muerto, las dos que no dependen del trailer de actor
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0413-panel-de-metricas-m7-m8.md
created: 2026-08-16
reviewer: Analista
intake:
  type: infra
  goal: >
    D-A de la v3 aprobada. Se entregan PRIMERO M7 y M8 porque son las unicas que NO dependen de la
    derivacion de actor (DECISION-0117); el panel completo M0-M9 llega despues del trailer. Las dos
    tienen especimen medido el 2026-08-16. M7: el job validate corrio 6 de sus ~86 pasos durante DOS
    DIAS y nadie lo vio, porque el job ya estaba rojo por otras causas -- un job rojo absorbe reds
    nuevos gratis. Su ausencia costo el defecto mas caro del dia. M8: el interbloqueo de mensajes sin
    scope resoluble mata encargos en silencio; ese mismo dia un RETRY_EXHAUSTED con attempts 3 dejo
    el trabajo de un maker varado sin que el tablero lo dijera.
  acceptance:
    - "AC1 (M7 con las dos caras): cobertura de verificacion por job y por corrida, publicando el
      RATIO ejecutados sobre declarados Y el CONTADOR ABSOLUTO con suelo historico. El ratio solo no
      vale: si alguien BORRA pasos, declarados baja con ejecutados y el ratio se queda en 100. Se
      acredita con los dos casos: pasos saltados (el ratio cae) y pasos borrados (ratio intacto,
      contador cae)."
    - "AC2 (M8 mide la muerte, no la espera): tiempo-mensaje diferido POR CAUSA
      (active_external_claim, worktree_residue_live, staged_residue_aborted, message_scope_ambiguous)
      contando SOLO lo que termina en defer_terminal o RETRY_EXHAUSTED. Un defer que resuelve es el
      sistema funcionando; contarlo haria que un dia sano pareciera patologico y la metrica se
      ignoraria en dos semanas."
    - "AC3 (jobs intermitentes declarados): M7 marca como INTERMITENTE todo job que en corridas del
      MISMO commit da resultado distinto, y lo EXCLUYE del perfil en vez de promediarlo. Especimen:
      falsification-runners dio 9/0 y 8/1 el mismo dia por TASK-0401."
    - "AC4 (el negativo, por MUTACION): perturbar la fuente -- un job con pasos borrados, un
      retry.json con un defer que resolvio -- debe CAMBIAR el veredicto del panel. Si el panel dice
      lo mismo con la fuente perturbada, no mide."
  verification_cmd:
    - "python scripts/metrics_panel.py --help"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/metrics_panel.py
  out_of_scope:
    - "M0 (derivacion de actor) y todo lo que dependa de el: espera al trailer de DECISION-0117."
    - "M1-M6: entran con el panel completo; aqui solo M7 y M8, que son las que no tienen dependencia."
  risk: low
  estimate: M
---

# TASK-0413 -- las dos metricas que no esperan al trailer

## M7, y por que es la que faltaba

El 2026-08-16 el job `validate` paso de **26 pasos ejecutados a 6** y estuvo asi **dos dias**. No lo
vio nadie porque **el job ya estaba rojo**. Ninguna metrica de latencia, mensajes o re-trabajo lo
habria detectado: hacia falta contar **cuanto se ejecuta**, no cuanto tarda.

Y la trampa que obliga al contador absoluto: **un ratio es ciego al borrado de pasos**. Si se
eliminan verificaciones, declarados baja con ejecutados y el ratio dice 100.

## M8, y por que se mide la muerte y no la espera

Un defer que resuelve es el sistema funcionando. Lo que cuesta es el que **termina en muerte**:
`defer_terminal` o `RETRY_EXHAUSTED`.

## AC3, que salio de un error propio

Se afirmo que un commit tenia "perfil limpio" porque un job dio 9/9. Dio 9/9 **porque el defecto
intermitente no disparo en esa tirada**. Un job intermitente dentro del perfil hace que la
certificacion dependa del azar de la corrida; por eso se declara y se excluye.
