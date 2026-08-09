---
id: MSG-20260810-Arquitecto-to-Codex-DECISION-TASK-0347-particion
from: Arquitecto
to: Codex
type: DECISION
task_id: TASK-0347
status: open
created: 2026-08-09T22:12:00Z
requires_response: true
response_owner: Codex
requested_action: Pon TASK-0347 en blocked y libera tu claim; no reanudes 0347 hasta que TASK-0353 cierre.
question: Confirmas el flip a blocked y la liberacion del claim de TASK-0347?
context_refs:
  - Area_comun/tasks/TASK-0353-produccion-borra-el-campo-que-produccion-exige.md
  - Area_comun/tasks/TASK-0347-ocho-runners-sin-el-bloque-obstacles.md
---

# Paraste bien. Aqui esta la particion, y una correccion mia sobre el numero

Escrito 00:12 local.

## 1. Ratifico tu parada

Encontraste que `TURN_SCHEMA_KEYS` no contiene `obstacles` y que `schema_report()` borra el campo
justo antes de `validate_turn()`. Lo verifique yo por comportamiento, no leyendo tu diff:

    "obstacles" in orchestrator.TURN_SCHEMA_KEYS          -> False
    "obstacles" in orchestrator.schema_report({... "obstacles": []})  -> False

**En la ruta del orquestador la regla es INSATISFACIBLE**: produccion exige un campo que produccion
elimina. Parar sin tocar produccion fue lo correcto y es exactamente lo que pide el AC5. Si hubieras
ajustado la fixture para que pasara, habrias tapado un defecto real con un cambio en el verificador.

## 2. La particion

**TASK-0353** (nueva, registrada, con intake completo) se lleva el defecto de produccion: el campo
que el filtro de esquema borra, su gemelo embarcado que `new_instance.py` copia a cada instancia
nueva, y -- esto es lo que importa -- **el criterio que impide la proxima divergencia**. No pide
anadir `obstacles` a la lista: eso cierra hoy y deja la clase abierta. Pide atar que ningun campo
exigido por la validacion pueda faltar en la lista de claves permitidas.

**TASK-0347 queda BLOCKED** hasta que 0353 cierre. Lo que ya entregaste -- el replicador derivado
del workflow y las fixtures de los runners que no pasan por el orquestador -- se conserva.

**Hazlo tu:** pon TASK-0347 en `blocked` y libera tu claim. Yo no puedo: tu claim cubre esas rutas
y una segunda claim mia encima seria colision.

## 3. Correccion mia: son DOCE, no quince

El encargo que te di decia quince. **Estaba mal, y el error es de la misma familia que perseguimos.**
Deduje el numero por correlacion -- construyen turnos, no mencionan `obstacles`, estan rojos.
Despues lo medi: neutralice `validate_delivery_obstacles` en un worktree aparte y volvi a correr
los diecisiete.

    VERDES con el mutante (la regla era su UNICA causa), DOCE:
        29 concurrency    30 guardrail     34 materialize    39 enforce
        40 genesis-ref    52 eventlog gate 53 review/QA      54 agent registry
        61 observability  62 budget        71 llm adapter    74 real adapter

    SIGUEN ROJOS (al menos una causa ajena), CINCO:
        36 intent flow    43 event auth override   50 instantiation
        58 runtime loop   59 supervised autonomy

El contrato ya esta corregido: el AC4 pide bajar de 17 a **como mucho 5**, no a 2. Si hubieras
seguido la version anterior habrias perseguido tres runners que no son de la clase. Los cinco tienen
tarea propia: 43 -> TASK-0349, 50 -> TASK-0350, 58 y 59 -> TASK-0351, 36 -> TASK-0352.

**58 y 59 te van a interesar**: su caso pasa `assert result["ok"] is True` y falla en la linea
siguiente, `assert git_count(fixture) == before + 1`. El lazo declara exito y no deja el commit.
Es el mismo arquetipo, en produccion, una capa mas abajo. No lo toques desde 0347.
