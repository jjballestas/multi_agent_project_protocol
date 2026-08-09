---
id: TASK-0351
title: El lazo del runtime reporta ok true y no deja el commit -- exito declarado sin el efecto
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0351-el-lazo-reporta-ok-y-no-commitea.md
created: 2026-08-10
---

# TASK-0351 -- `ok: true` sin commit

Pasos 58 (`runtime_loop_cases`) y 59 (`supervised_autonomy_cases`) del job `validate`, en checkout
limpio a HEAD. Medido por mutacion: **no es la regla de `obstacles`** -- siguen rojos con la regla
neutralizada.

La linea que revienta, en los dos, es la siguiente a la que comprueba el veredicto:

```python
assert result["ok"] is True, result      # PASA
assert git_count(fixture) == before + 1  # FALLA
```

El orquestador **declara exito y no deja el commit**. Sea un defecto de produccion o una fixture
obsoleta, la forma es exactamente el arquetipo que persigue el borrador DECISION-0105: *el
mecanismo reporta exito sin el efecto*. Y esta en el lazo del runtime, no en un verificador.

**Lo primero es decidir de que lado esta el defecto**, y decirlo antes de tocar nada:

- si produccion dejo de commitear y el caso tiene razon -> es un fallo de produccion y hay que
  pararse ahi;
- si el contrato del lazo cambio legitimamente y el caso quedo obsoleto -> se declara que cambio,
  cual y cuando.

**No se ajusta el caso para que pase sin haber respondido a eso.**

Fuera de alcance: los doce rojos de causa `obstacles` (TASK-0347).
