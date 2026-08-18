---
DRAFT (personal) -- GO de TASK-0260 listo para rutear apenas cierre 0259.
No es un MSG del mailbox todavia. Al rutear: convertir a MSG-<fecha>-Arquitecto-to-Codex-GO-TASK-0260,
claim file-scoped, ETA, y liveness de Codex verificada.
---

# GO TASK-0260 -- C1 vista de plan + gate de aprobacion de turno 0

Unidad 4 de la tabla 0103. maker=Codex, checker=Analista (Opus). risk=medium, estimate=M.

## Que construir (del intake, sin ampliar)

(a) **Vista de plan del CONJUNTO**: `orchestrator --plan-all` (o render equivalente de
TASK_INDEX + intake de los .md) que imprime por unidad: id, goal, acceptance, verification_cmd,
required_capability, risk, estimate. Proyeccion pura de ficheros atestados (DECISION-0009): la
vista JAMAS inventa ni corrige datos.

(b) **Gate de aprobacion de turno 0**: el orchestrator rehusa ejecutar el turno 1 de un conjunto
sin registro de aprobacion humana verificable (hash del render del plan aprobado referenciado en
event log / mailbox firmado). Cambio material (unidad nueva, acceptance o risk distinto) invalida
la aprobacion y exige re-aprobar. Mecanismo de comparacion (hash o diff de campos) documentado y
probado.

## Guardas duras (out_of_scope del intake -- repetir en el GO)

- **NUNCA ejecutar el orchestrator en el hub** en esta tanda; validar solo en scratch/examples
  (orden del Operador 2026-07-19).
- Aprobar el conjunto es DISTINTO de `supervised_autonomy.human_checkpoint_every_k` y NO lo
  enciende ni lo requiere.
- No ampliar "cambio material" mas alla de C1 (el carve-out de remediacion es nota N1 al Operador,
  no parte de esta unidad).
- Reservadas N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) FUERA y CONGELADAS.
- Fondo intocable: config pineado epoch 1.14.0 / genesis 2E35F26E / dataset N=500 FUERA.
- No encender supervised_autonomy ni real_invoker en el hub.

## Acceptance (verbatim del intake) y verificacion

- Vista imprime la tabla completa leyendo TASK_INDEX + .md.
- Sin aprobacion registrada -> rehusa con mensaje claro; con aprobacion -> arranca.
- Cambio material invalida la aprobacion; comparacion documentada y probada.
- Distinto de human_checkpoint_every_k.
- Suites runtime verdes; gate probado en scratch/examples, nunca en el hub.
- verification_cmd: run_runtime_turn_cases.py + suite nueva del gate de plan (examples/,
  patron run_*.py) + validate_collaboration_state.py + scan_encoding.py.

## Angulo adversarial para el checker (preparar en el REVIEW)

- Que la vista sea PROYECCION: mutar un dato en un .md y confirmar que la vista lo refleja sin
  "corregir" (no debe sanear).
- Que el gate rehuse de verdad: turno 1 sin registro de aprobacion -> rehusa; construir el vector.
- Que un cambio material (acceptance distinto post-aprobacion) invalide: construir el diff y
  confirmar que exige re-aprobar; y que un cambio NO material no invalide en falso.
- Que NO toque supervised_autonomy (leer que el gate no enciende human_checkpoint_every_k).
