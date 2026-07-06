# PROFILE-NOVA - Disparadores concretos de lentes para la instancia Nova-Budget (Sprint-1-ready, NO CONSTRUIR AUN)

> **ESTADO: DISENO/SPEC, no operado.** Instancia especifica de `Area_comun/protocol/LENS_COVERAGE_GATE.md`
> (mecanismo neutral) para el dominio Nova-Budget. Escribir este profile es prep legitima (DECISION-0092
> seccion B); construir el computo automatico se DIFIERE a Sprint 1 gobernado (post-30-jul).

## 1. Globs/reglas concretas por senal (mapea a la tabla neutral de LENS_COVERAGE_GATE.md s.3)

| Senal neutral | Glob/regla concreta de Nova | Lente |
|---|---|---|
| Superficie de riesgo | El diff toca `src/NOVA.Infrastructure/**/Sql*Gateway.cs` (llamadas a procs mutadores), `SESSION_CONTEXT`/tenant, o cualquier archivo bajo `src/NOVA.Api/Program.cs` que registre auth/autorizacion | R1 |
| Componente compartido por >=2 verticales | El diff toca `BudgetProcedureProblemDetails.Map` (o cualquier switch/mapper compartido entre >=2 carpetas de superficie: `AppropriationModifications/`, `AvailabilityAdjustments/`, `AvailabilityCertificateAnnulments/`, `CommitmentAnnulments/`, etc.) -- esta es EXACTAMENTE la senal que habria disparado el hallazgo #10 (etiquetado cruzado de THROW 50212) por diseno, no por pasada transversal afortunada | R2 |
| Cambia comportamiento observable | El diff anade/modifica un endpoint bajo `src/NOVA.Api/Program.cs` (nueva ruta `Map*`), o cambia el contrato de un DTO en `NOVA.Contracts` | R3 |
| Runtime en produccion | El diff toca un gateway SQL nuevo (`Sql*Gateway.cs` nuevo), un mapeo de error nuevo (nueva entrada en `BudgetProcedureProblemDetails.Map`), o cualquier archivo bajo `NOVA.Infrastructure` que se ejecute en el camino de una mutacion | R4 |
| Handoff pre-revision | Cualquier GO/REVIEW de Arquitecto->Analista o Codex->Arquitecto sobre una unidad NOVA-DEV | R1+R3 minimo |
| Fase post-SDD | Aprobacion de una SPEC-NOVA-* antes de su build (evento "SPEC aprobada, listo para build") | judgment-day, tier alto |

## 2. Ejemplo retrospectivo (auto-calibracion, no vinculante)

Aplicando esta tabla a TASK-0255 (ya cerrada) de forma retrospectiva:
- Toca `SqlAvailabilityCertificateAnnulmentGateway.cs` (gateway nuevo) -> R1 (riesgo) + R4 (runtime).
- Anade endpoint `POST .../annul` -> R3.
- NO toca ningun componente compartido por >=2 verticales de forma nueva en si misma, PERO el hallazgo
  #10 (etiquetado cruzado en `BudgetProcedureProblemDetails.Map`, YA existente y compartido) confirma
  que la regla de R2 (s.1) habria disparado sobre CUALQUIER cambio a ese archivo -- si `SPEC-NOVA-P4-005`
  hubiera declarado `lenses_required` incluyendo R2 por tocar ese switch, el gate de cobertura habria
  exigido revisarlo explicitamente por esa lente, en vez de depender de una pasada transversal.

Este ejercicio es CALIBRACION del diseno (confirma que las reglas de s.1 son observables y habrian
funcionado), no una re-apertura de TASK-0255 ni un cambio retroactivo a su veredicto ya cerrado.

## 3. Umbrales de coste-por-tier (DECISION-0092 seccion A.6 + C.11: modelo de coste SI, framing advisory NO)

Cuando el computo automatico se construya (Sprint 1), el DISPARO debe ser TIERED para no inflar tokens
en un estudio que los MIDE (DECISION-0092, caveat 3 del draft fuente):
- Diff de solo-documentacion (`.md`, `.html` sin cambio de codigo): ninguna lente obligatoria.
- Diff que toca UNA superficie sin componente compartido: R1+R3 (piso minimo de handoff).
- Diff que toca un componente compartido o superficie de runtime nueva: + R2 y/o R4 segun s.1.
- Fase post-SDD de una unidad de criticidad ALTA (ver clasificacion del sello): tier judgment-day.

## 4. Que NO cubre este profile

- No define nuevos checks de calidad; solo indica CUANDO una lente (ya existente como practica) es
  obligatoria para una unidad Nova concreta.
- No cambia el patron congelado de P4.1 ni ninguna SPEC ya cerrada/medida.
- No introduce terminos de este profile al core del protocolo (viven aqui, en `Area_comun/specs/nova/`).
