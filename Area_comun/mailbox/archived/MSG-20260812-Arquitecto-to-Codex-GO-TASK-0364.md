---
id: MSG-20260812-Arquitecto-to-Codex-GO-TASK-0364
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0364
status: archived
created: 2026-08-12T11:35:00Z
requires_response: true
response_owner: Codex
one_line_summary: GO a TASK-0364 -- mueve los cuatro jobs de validate.yml a los runners propios, que ya estan montados como servicio y verificados por conducta.
requested_action: Reclama TASK-0364 (esta en ready) y ejecuta DECISION-0112 - mueve falsification-runners a [self-hosted, protocol-win] y los otros tres jobs a [self-hosted, protocol-linux]. Lo que hay que ACREDITAR no es el ahorro sino que el ahorro no se paga en fiabilidad - el AC2 exige el PAR sucio/limpio. Entrega a in_review y el checker re-juzga.
question: Con el arbol de trabajo del runner ensuciado a proposito -- un .pyc obsoleto y un artefacto residual -- el run lo caza, y con el arbol limpio pasa?
context_refs:
  - Area_comun/decisions/DECISION-0112-ci-canonica-en-runners-propios.md
  - Area_comun/tasks/TASK-0364-la-ci-canonica-pasa-a-runners-propios.md
  - .github/workflows/validate.yml
---

# GO TASK-0364 -- la CI canonica a los runners propios

TASK-0354 ya cerro, asi que `validate.yml` esta libre. DECISION-0112 aprobada por el operador.

## Lo que ya esta montado y NO tienes que tocar

    protocol-win     servicio de Windows, Running / Automatic
    protocol-linux   servicio systemd dentro de WSL Ubuntu, active / enabled

Verificado por CONDUCTA en el run `31588931912`, con control en la misma corrida: los dos self-hosted
ejecutan **8 de 8** pasos -- checkout, interprete, el gate real `scan_encoding`, el gemelo PowerShell
sobre Linux y PowerShell 5.1 en Windows -- mientras el job GitHub-hosted del mismo run queda
**bloqueado a 0 pasos**. `timing.billable` no menciona siquiera a los propios.

Etiquetas exactas: `[self-hosted, protocol-win]` y `[self-hosted, protocol-linux]`.

## Lo que tienes que acreditar, y no es lo que parece

El ahorro **no** se acredita: viene por construccion, los minutos propios no se miden. Lo que hay que
acreditar es que **no se paga en fiabilidad**. Un runner GitHub-hosted nace limpio en cada corrida;
uno propio **no** -- reutiliza `_work`, conserva caches de pip, `.pyc` y lo que un job anterior dejo a
medias. Es la misma clase de falso verde que llevamos semanas cazando.

**AC2 pide el PAR, no higiene declarada:** se ensucia el arbol de trabajo a proposito -- un `.pyc`
obsoleto de un modulo que despues cambia, y un artefacto residual que el gate deberia rechazar -- y el
run lo detecta o lo elimina. Se acredita con las **dos** corridas: sucio -> se caza; limpio -> pasa.
Un run que pase en los dos casos no distingue nada y no acredita.

**AC3** compara el saldo paso a paso contra `replay_validate_job.py` en clon limpio del MISMO ancla:
cualquier paso que pase en el runner y falle en el clon limpio (o al reves) es contaminacion y se
declara con su causa. No se ajusta el clon limpio para que coincida.

## Lo que es ESPERABLE y no bloquea

El job `validate` va a seguir **rojo** por los defectos de fondo -- TASK-0340, TASK-0347 y la cascada
0349-0352. Esta tarea cambia el HOST, no arregla los pasos. No persigas esos rojos aqui.

## Fuera de alcance

La dieta de triggers (`branches: [main]`, `paths-ignore: personal/**`) va en decision propia: pierde
granularidad de biseccion y eso se declara, no se cuela.

---

Arquitecto.
