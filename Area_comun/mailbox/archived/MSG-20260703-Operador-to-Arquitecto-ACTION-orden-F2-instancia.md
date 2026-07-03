---
message_id: MSG-20260703-Operador-to-Arquitecto-ACTION-orden-F2-instancia
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-03
context_refs:
  - Area_comun/decisions/DECISION-0083 (re-alcances F2)
  - Area_comun/tasks/TASK-0230 (F2.1 new_instance)
  - Area_comun/tasks/TASK-0232 (F2.3 harness distribuido)
  - Area_comun/tasks/TASK-0233 (F2.2 e2e distribuida)
  - Area_comun/tasks/TASK-0234 (F2.5 runbook onboarding)
one_line_summary: "F1 cerrada (0244/v1.18.0 done). Arranca F2: promueve de a una las 4 tareas re-alcanzadas (0230->0232->0233->0234) instanciando nova-budget desde el tag v1.18.0, con cosecha gentle-ai nivel B obligatoria."
requested_action: "[DIRECTIVA] (1) Con v1.18.0 taggeada y F1 cerrada, arranca F2 (ventana sem 3, entrega 21-25 jul). F2 es ENTREGA PROTEGIDA (NOVA-ESTUDIO-001 s.4): el estudio/baseline jamas la bloquea; el checkpoint F2-readiness del 19-jul ya esta sellado en el calendario del estudio. (2) Promueve DE A UNA las 4 tareas F2 re-alcanzadas por DECISION-0083 (todas con bloque intake valido, gate 0238 vigente): TASK-0230 [F2.1] new_instance de nova-budget DESDE EL TAG v1.18.0 + perfil de instancia (su cuerpo ya trae la anotacion intake-v2/DoR de DECISION-0084: el TASK_TEMPLATE de la instancia extiende intake con target_user/functional_scope/assets_inputs/tech_constraints/risks_list/priority para type feature/product; timebox 1 dia, el tiempo real es dato del estudio); luego TASK-0232 [F2.3] harness distribuido pull->escribir->push inmediato (claims visibles entre clones) + hosting privado; luego TASK-0233 [F2.2] e2e distribuida (clon limpio opera 1 tarea completa solo via Git, owner Analista, registrar/promover tras F2.1); luego TASK-0234 [F2.5] runbook onboarding remoto (<=1 dia, medido; alimenta HP6). (3) COSECHA GENTLE-AI NIVEL B obligatoria en F2: configs de agente COMMITEADAS en el repo de la instancia (Git es el adapter; NO construir adapters multi-IDE); dry-run + write atomico temp+rename en new_instance; PROHIBIDO 'gentle-ai install' en maquinas Nova (inyecta Engram; reabriria DECISION-0081 y contamina el estudio). (4) Tablero: F2.x con evidencia y sello, como siempre. [RECOMENDACION] El orden 0230->0232->0233->0234 es el natural (la instancia primero); si al instanciar descubres dependencia inversa entre 0232 y 0233, reordena documentando. El nivel C de gentle-ai (merge por secciones, manifiesto, doctor) sigue DIFERIDO a F5."
question: ""
---

# ACTION - Arranca F2 (instancia nova-budget distribuida desde el tag v1.18.0)

F1 quedo cerrada: TASK-0244 (release v1.18.0) esta en `done` con el tag creado
(CHANGELOG + templates sync) y las 7 tareas F1 completas, cada una con su ciclo
adversarial real. Con eso arranca F2, la primera ENTREGA PROTEGIDA de Vision Nova:
instanciar nova-budget desde el tag, montar el harness distribuido por Git y dejar
un runbook de onboarding remoto medido.

El detalle vinculante esta en `requested_action`. Puntos que importan:
- La instancia se crea DESDE EL TAG v1.18.0 (release congelada), no desde HEAD.
- Cosecha gentle-ai NIVEL B obligatoria; nivel C diferido a F5; `gentle-ai install`
  PROHIBIDO en maquinas Nova (contaminaria el estudio via Engram / DECISION-0081).
- Promocion de a una con GO + intake valido; el gate 0238 sigue vigente.

La orden NOVA-DEV (revision adversarial del paquete Ingenas + SPECs gobernadas)
llega por separado a continuacion; la instancia (esta orden) es el camino critico.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
