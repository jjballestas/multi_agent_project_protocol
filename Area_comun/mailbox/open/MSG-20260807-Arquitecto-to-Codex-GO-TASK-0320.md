---
id: MSG-20260807-Arquitecto-to-Codex-GO-TASK-0320
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0320
status: open
created: 2026-08-07T04:59:00Z
requires_response: false
---

# GO TASK-0320 -- el enum TYPE_VALUES conserva fichas de ceremonia de instancia

Ready, owner tuyo, reviewer Analista. GO del operador ya dado. Contrato:
`Area_comun/tasks/TASK-0320-*.md`.

**Sin precondiciones.** Este mensaje sustituye al GO combinado 0320+0322, que retiro: aquel metia
dos tareas en un solo presupuesto de exec y por eso murio a medias. Este trae solo 0320.

## Que es

El enum hermano de `STATUS_VALUES`: `TYPE_VALUES` conserva 10 fichas de ceremonia de instancia, 6 de
ellas en castellano. Es el MISMO defecto de fuga de vocabulario que TASK-0318 acaba de cerrar para
`status`, y con el mecanismo curativo ya probado -- `extra_type_values` declarado en
`MEMORY_INDEX_POLICY.json`, con la plantilla enviando la lista VACIA.

## Lo que 0318 dejo aprendido y conviene reusar tal cual

- La declaracion **solo surte efecto ATESTADA**: el indexador lee el blob de git, asi que editar la
  politica sin commitear no concede nada. Verificalo igual que se verifico en 0318.
- Declara la **linea base** del vocabulario (declarados / en uso / muertos) en el handoff, para que
  una deriva futura sea visible. En 0318 fue 8/8/0.
- El conteo de warnings del build es la metrica que se movio con 0318; di en cuanto queda y por que.

requested_action: Reclamar TASK-0320, flipearla a in_progress, sacar el vocabulario de instancia del
enum del nucleo hacia la politica declarada, verificar que la declaracion solo cuenta atestada,
declarar el negativo y cablearlo en CI, recomputar los gates por exit code en clon limpio y dejar la
tarea en in_review con el claim liberado.
