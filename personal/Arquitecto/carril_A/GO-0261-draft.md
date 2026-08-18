---
DRAFT (personal) -- GO de TASK-0261, para encadenar tras 0260 (o segun prioridad del Operador).
No es un MSG del mailbox todavia. Depende de la convencion de bloque de TASK-0258/0262.
---

# GO TASK-0261 -- C3/C4 validate_mailbox exige obstacles + contador de friccion en REPORTE

Unidad 5 de la tabla 0103. maker=Codex, checker=Analista(Opus). risk=medium, estimate=M.

## Consistencia con E7 (nota importante)

E7 partio el sensor de friccion del carril RUNTIME en dos capas (turn_validate autoritativo +
post-gate objetivo = TASK-0286). **El carril SESION (0261) NO tiene ese problema de capa**: el
mailbox no tiene gate/apply, asi que no hay un "gate-red objetivo" que capturar en otra capa. Por
eso C4 declara que en sesion NO existe sensor de friccion y la mitigacion es el `friction_count`
DECLARATIVO. El acceptance de 0261 ya codifica el modelo correcto y NO cambia por E7:
`friction_count > 0 Y obstacles vacio = FAIL`; `friction_count 0 con obstacles vacio = PASA`.

## Que construir (del intake, sin ampliar)

En `scripts/validate_collaboration_state.py` (validate_mailbox), para mensajes `type: REPORTE`
de entrega de unidad gobernada:

- Exigir el bloque `obstacles` bien formado (MISMOS 4 campos + enum que el turn_schema de
  TASK-0258) + un `friction_count` (reintentos / rechazos de gate / correcciones del checker).
- Cruce espejo del carril sesion: `friction_count > 0` Y `obstacles` vacio = FAIL;
  `friction_count 0` con `obstacles` vacio = PASA (lista vacia legitima).

## Guardas duras (out_of_scope del intake)

- **GRANDFATHERING OBLIGATORIO**: la regla aplica SOLO a mensajes con `date` >= fecha de adopcion
  (o marker de version de schema en frontmatter); el historico de `open/`, `answered/`,
  `archived/` NO se pone rojo (validate barre las 3 carpetas). Es acceptance, no opcional -- el
  riesgo es pintar rojo el canal vivo.
- La PLANTILLA del mensaje es TASK-0262 (coordinar el MISMO bloque; 0261 valida, no redacta).
- Sensores automaticos de friccion en sesion FUERA (C4: no existen; el contador es declarativo).
- Reservadas N=6 y fondo intocable FUERA.

## Acceptance y verificacion (del intake)

- REPORTE sin bloque `obstacles` bien formado o sin `friction_count` -> validate exit != 0.
- Los 4 cuadrantes (friccion x obstacles) + el caso grandfathered, todos con el resultado
  esperado; suite de casos mailbox.
- El limite presencia-vs-veracidad documentado donde declara C4.
- validate exit 0 sobre el arbol actual del hub con el historico intacto.
- verification_cmd: validate_collaboration_state.py + runner de casos mailbox (examples/,
  run_*.py) + scan_encoding.py.

## Angulo adversarial para el checker

- Construir un REPORTE con `friction_count: 2` y `obstacles: []` -> debe FAIL.
- Un REPORTE con `friction_count: 0` y `obstacles: []` -> debe PASA (no forzar teatro).
- Un mensaje HISTORICO pre-adopcion sin el bloque -> NO debe enrojecer (grandfathering).
- Confirmar que validate barre las 3 carpetas y que el hub actual queda verde.
