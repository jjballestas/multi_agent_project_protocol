# runtime/ — Plano de control de orquestación (opt-in, off by default)

> **Proprietary — All Rights Reserved** (ver `/LICENSE`, DECISION-0010).
> Capa de *tooling* neutral que orquesta el protocolo file-based. Adoptada por
> [DECISION-0009](../Area_comun/decisions/DECISION-0009-runtime-orquestacion.md); diseño en
> [DISENO-runtime-orquestacion-automatizada.md](../Area_comun/artifacts/DISENO-runtime-orquestacion-automatizada.md).
> **`enabled:false` por defecto:** una instancia sin el bloque `runtime` en `protocol.config` se
> comporta exactamente como hoy (coordinación manual).

## Estado: M0 (diseño)
Esta carpeta arranca con el **contrato de turno** — la pieza base. Lo demás (orquestador, router,
adapters) se implementa en tareas posteriores (ver DECISION-0009 backlog §7).

- `turn_schema.json` — esquema estricto del *turn report* que un agente devuelve por turno
  (contrato SPEC-0026). El orquestador lo valida, comprueba `changed_paths ⊆ claim`, aplica
  transiciones, corre el gate (validador + scan de neutralidad) y hace **1 turno = 1 commit** (o
  `git revert` + `blocked` si el gate falla).

## Principios (no negociables, DECISION-0009)
Ficheros = fuente de verdad · 1 turno = 1 commit · gate por turno + rollback · gates humanos como
paradas duras · adapters vendor-neutral · determinismo en router/transiciones · claim como lock.

## Neutralidad
`runtime/**` es tooling: se añade a `scan_globs` de neutralidad (no puede introducir términos de
dominio). El dominio del piloto vive en la instancia, no aquí.
