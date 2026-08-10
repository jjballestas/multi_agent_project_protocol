---
id: TASK-0356
title: El oraculo de paridad vuelca bajo la raiz del fixture y el gate corre con -Root . -- ninguna invocacion es la de produccion
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0356-el-oraculo-vuelca-bajo-otra-raiz-que-el-gate.md
created: 2026-08-11
---

# TASK-0356 -- SLIP-8: el oraculo certifica una ejecucion que produccion nunca hace

Residual declarado al cerrar TASK-0329 el 2026-08-10, con repro falsificable completo en
`Area_comun/artifacts/Analista-TASK-0329-inventario-efectivo-r5-verdict.md`.

## El defecto

    oraculo   ejecuta el .ps1 con la raiz del FIXTURE   (test_scan_domain_neutrality.py:232, -Root str(self.root))
    paridad   lo ejecuta con probe_root
    gate real corre con  -Root .

**Ninguna de las dos invocaciones del oraculo es la que produccion ejecuta.** Un mutante que ponga
la exencion muerta bajo una **guarda condicionada al arbol escaneado** se le escapa al oraculo,
porque bajo la raiz del fixture esa guarda no se activa.

## Por que se cerro 0329 igualmente

El checker lo declaro **residual y no bloqueante**, con cuatro razones que hago mias:

1. **No es la clase que declaro cerrada.** SLIP-1/5/6 se alcanzaban decidiendo *donde escribes la
   linea*: un accidente. SLIP-8 exige una evasion **deliberada**. El limite del oraculo se estrecho
   de forma categorica, no se desplazo.
2. **No movio la porteria.** Publico en r4 el criterio exacto de aceptacion -- coordenada, orden,
   formato -- **antes** de ver la entrega, y se cumple. Bloquear por un eje no declarado seria el
   mismo vicio que reprocha a las remediaciones.
3. **Falla cerrado.** El lado Python detecta la fuga en cuanto la coordenada se activa; lo que no se
   cumple universalmente es el *aviso inmediato*.
4. La redaccion del negativo sobreafirmaba, y **ya esta acotada** (2026-08-10) a *declaracion
   INCONDICIONAL*, con puntero a esta tarea.

## Lo que tendria que hacer esta tarea

**Atar el volcado del oraculo a la MISMA invocacion que el gate**: volcar bajo `-Root .`, no bajo la
raiz del fixture. No ensanchar el mecanismo de deteccion; **igualar la coordenada de ejecucion**.

Se falsa con el mutante 8 del veredicto r5: exencion muerta en un solo escaner, bajo guarda
condicionada al arbol escaneado. Hoy el oraculo sale verde; tras el arreglo debe salir rojo.

## Alcance

Fuera: el mecanismo de deteccion en si (cerrado en 0329), y el eje `pwsh` 7 / POSIX, que sigue sin
medirse en este host y cuya mitigacion declarada sigue vacia -- ese es su propio residual.
