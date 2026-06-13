# Session report - Mitigacion de context rot: DECISION-0030 (slim-views + cold-start) y cierre de onda

- Date: 2026-06-13
- Phase: P2
- Process status: closed
- Ratification: ratified by human
- HEAD: 7e75f47

## 1. In One Sentence

Se aprobo DECISION-0030 (slim-views del estado + politica de cold-start just-in-time) para mitigar el
context rot del runtime, y se cerro la onda de mantenimiento y del pipeline DECISION-0029.

## 2. What Was Done

- **Investigacion** del problema de crecimiento de contexto (docs de Anthropic y OpenAI; revision del repo
  `code-review-graph`). Conclusion: el cuello de botella es cuanto del peso vivo se vuelca al cold-start,
  no falta de un grafo de codigo.
- **DECISION-0030 redactada y ratificada** (accepted, 2026-06-13): vistas derivadas compactas + carga
  just-in-time, con garantias anti-drift y gate de medicion.
- **Mantenimiento sistematico** ejecutado (poda + barrido de mailbox) bajo DECISION-0014, que queda
  ACCEPTED con GO para CI + automatizacion.
- **Pipeline DECISION-0029**: TASK-0101 ratificado (encadenado/firmas/anchor materializados off-by-default
  en `protocol.config.json > event_state`); TASK-0102 y TASK-0103 promovidas a `ready`.
- **Memoria post-commit** actualizada (DECISION-0026).

## 3. SDD Summary

- Specs created or modified: ninguna aun; se encola SPEC-0077+ (contrato de slim-views).
- Tasks implemented against specs: TASK-0101 (pipeline DECISION-0029) ratificado.
- Acceptance criteria satisfied: N/A para DECISION-0030 (fase de diseno); pendientes en su SPEC.
- Test plans executed: validacion de protocolo verde; medicion de cold-start como gate futuro.
- Spec deviations: ninguna.

## 4. Decisions

- **DECISION-0014** - ACCEPTED. Poda sistematica por umbral medido; GO para CI + automatizacion.
- **DECISION-0030** - ACCEPTED. Slim-views + cold-start just-in-time. Target: cold-start < 10k tokens
  (vs ~19.5k actual). Slim-views = derivadas y regenerables (full + archive siguen autoritativos);
  drift-checker extendido; off-by-default con activacion opt-in tras medicion.

## 5. Current Project State

- Estado del protocolo consistente (HEAD 7e75f47): DECISION-0030 en `accepted`; `event_state` del config
  con firmas por agente + anchor off-by-default (TASK-0101).
- DECISION-0029 en ejecucion: 0101 cerrado, 0102/0103 listas para implementar.
- DECISION-0030 entra a la proxima onda (especificacion + implementacion).

## 6. Next Steps

1. SPEC-0077+ (Claude): contrato de cada slim-view (campos exactos, estados calientes), extension del
   drift-checker, ajuste de `coldstart_globs`, golden cases.
2. TASK-0105+ (Codex, tras SPEC): materializacion de slim-views en `materialize_to_disk`, rotacion de
   `events.jsonl`, medicion before/after.
3. Continuar pipeline DECISION-0029: implementar TASK-0102/0103 (ready).

## 7. What We Need From The Human Owner

- Confirmar prioridad relativa entre la onda DECISION-0030 (slim-views) y el resto del pipeline
  DECISION-0029 (0102/0103) para ordenar el backlog.
- GO para encender slim-views una vez la medicion before/after confirme el delta (activacion opt-in).

## 8. Risks Or Ambiguities

- **Drift de slim-views**: mitigado por contrato (materializacion en el mismo ciclo del escritor unico +
  cobertura del drift-checker). Debe verificarse en la SPEC con golden cases.
- **Operacional**: las operaciones de estado del protocolo (`submit_intent`) deben ejecutarse desde VS
  Code; el sandbox de Cowork mantiene un snapshot stale y no es seguro mutar estado desde ahi.

## 9. Communication Status

- Open messages (requiring response): ninguno pendiente al cierre.
- Active blocks: ninguno.
- Decisions required / human-required: priorizacion del backlog (seccion 7).

## 10. Details

- Decisiones: `Area_comun/decisions/DECISION-0030-slim-views-y-cold-start.md`,
  `Area_comun/decisions/DECISION-0014-poda-sistematica.md`,
  `Area_comun/decisions/DECISION-0029-firmantes-cruzados.md`.
- Config: `protocol.config.json` (`event_state`, `token_cost.coldstart_globs`).
- Backlog: SPEC-0077+ (Claude), TASK-0105+ (Codex).
