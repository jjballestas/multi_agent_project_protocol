# runtime/ - Plano de control de orquestacion (opt-in, off by default)

> **Proprietary - All Rights Reserved** (ver `/LICENSE`, DECISION-0010).
> Capa de tooling neutral que orquesta el protocolo file-based. Adoptada por
> [DECISION-0009](../Area_comun/decisions/DECISION-0009-runtime-orquestacion.md); diseno en
> [DISENO-runtime-orquestacion-automatizada.md](../Area_comun/artifacts/DISENO-runtime-orquestacion-automatizada.md).
> **`enabled:false` por defecto:** una instancia sin el bloque `runtime` en `protocol.config` se
> comporta exactamente como hoy (coordinacion manual).

## Estado: M0 (skeleton ejecutable)
Esta carpeta arranca con el contrato de turno y un skeleton read-only: router determinista,
validador de turno y `orchestrator.py --plan`. No invoca agentes ni muta estado.

- `turn_schema.json` - esquema estricto del turn report que un agente devuelve por turno
  (contrato SPEC-0026).
- `context.py` - carga de estado compartida para runtime.
- `router.py` - `select_next(state)` puro y determinista (SPEC-0027).
- `turn_validate.py` - validacion de esquema + write-allowlist + anti-carrera (SPEC-0026).
- `orchestrator.py` - M0 `--plan` dry-run.

## Principios (no negociables, DECISION-0009)
Ficheros = fuente de verdad. 1 turno = 1 commit. Gate por turno + rollback. Gates humanos como
paradas duras. Adapters vendor-neutral. Determinismo en router/transiciones. Claim como lock.

## Neutralidad
`runtime/**` es tooling: se anade a `scan_globs` de neutralidad (no puede introducir terminos de
dominio). El dominio del piloto vive en la instancia, no aqui.
