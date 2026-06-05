# Session report - Release v0.7.0 (eficiencia de tokens)

- Date: 2026-06-05
- Phase: P2 (Adopcion y expansion)
- Process status: closed (v0.7.0 publicada)
- Ratification: ratified by human (corte aprobado por el operador) — pendiente ratificacion de Codex de la paridad .ps1 de TASK-0025

## 1. In One Sentence
Se publica **v0.7.0**: cierra el track de eficiencia de tokens (cold-start **-75%**) e incluye, aditivo
y off-by-default, el runtime M0 y el modelo de claims por fila.

## 2. What Was Done
- Cierre de **TASK-0025** (frontmatter de mailbox minimo): variante minima en la plantilla + golden
  `minimal_frontmatter`; el validador ya toleraba campos omitidos (sin cambio de codigo ⇒ paridad .ps1
  trivial). Delta frontmatter **-61%** en el ejemplo.
- Corte de release: CHANGELOG `[0.7.0]`, `protocol_version` 0.6.0 → 0.7.0, AGENTS.md y PROJECT_STATE
  actualizados, tag `v0.7.0`.

## 3. SDD Summary
- Specs cubiertas en v0.7.0: SPEC-0023/0024/0025 (tokens), SPEC-0026/0027 (runtime M0), SPEC-0028
  (claims por fila); SPEC-0029/0030 (diseno M1, sin impl).
- Tasks done: TASK-0022/0023/0024/0025/0026/0027/0028/0029.
- Acceptance: medidor 3 escenarios; poda sin perdida + -75%; frontmatter minimo valido + -61%; runtime
  M0 12/12 golden; claims por fila 5/5 golden con paridad.
- Test plans: golden + validador + scan + regresion en los 4 ejemplos; verdes (.py; .ps1 atestiguado por
  CI/Codex salvo donde se indica).
- Desviaciones: TASK-0025 implementada por Claude (Codex fuera, por direccion del operador), sin cambio
  de validador; runtime M1 acota agente real a M2.

## 4. Decisions
- DECISION-0008 (eficiencia de tokens), DECISION-0009 (runtime), DECISION-0011 (claims por fila). Todas
  aditivas/MINOR, neutrales, off-by-default donde aplica.

## 5. Current Project State
- **v0.7.0 publicada**; `protocol_version=0.7.0`; validador + scan + golden verdes; cold-start ~9k tok.
- Done: TASK-0022..0029. Ready: TASK-0030, TASK-0031 (runtime M1, Codex).
- Sin claims activos tras el cierre; sin bloqueos.

## 6. Next Steps
1. **Codex:** TASK-0030 (runtime M1 apply+gate, SPEC-0029) → TASK-0031 (loop, SPEC-0030).
2. **Claude:** revisar 0030/0031; derivar specs/tasks de runtime M2 tras aceptar M1.
3. Proxima poda: archivar la ventana reciente de done.
4. Eventual **v0.8.0**: runtime M1 (apply + loop) cuando cierren 0030/0031.

## 7. What We Need From The Human Owner
- **Push** de los commits + el tag `v0.7.0` al remoto privado (pendiente de tu visto bueno).
- Confirmar que el contenido de v0.7.0 (tokens + runtime M0 + claims por fila) es el alcance deseado.

## 8. Risks Or Ambiguities
- Paridad `.ps1` de TASK-0025 no ejecutada por Claude (deny-rule); trivial por no haber cambio de
  validador; Codex la ratifica al volver.
- Ventana reciente de done en estado caliente; mitiga la proxima poda.

## 9. Communication Status
- Open messages (requiring response): ninguno.
- Active blocks: ninguno.
- Decisions required / human-required: push + tag al remoto (no bloqueante).

## 10. Details
- CHANGELOG `[0.7.0]`; DECISION-0008/0009/0011; SPEC-0023..0030; TASK-0022..0031; reportes de sesion.
- Commits de la sesion: `8c09037` (checkpoint), `9faf0d0` (reporte), + commit de release v0.7.0 + tag.
