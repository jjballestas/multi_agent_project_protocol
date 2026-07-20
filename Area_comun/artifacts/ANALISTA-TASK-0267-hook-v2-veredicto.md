# ANALISTA TASK-0267 - hook v2 - veredicto

Firma: Analista  
Fecha: 2026-07-20  
Veredicto: **CAMBIO-REQUERIDO / NO CERRABLE**

El snapshot del indice cierra varios escapes de TASK-0257, pero el selector previo
al snapshot todavia permite sacar por rename R100 una ruta gobernada hacia una ruta
no gobernada. El commit real termina EXIT 0 sin ejecutar el validador completo. La
regresion permanente tampoco prueba el vector prometido: renombra dentro de
`scripts/`, por lo que conserva el selector activo. Hay ademas una dependencia viva
anterior al snapshot (`scripts/prune_state.py`) cuya mutacion unstaged cambia el
veredicto. El coste medido se reporta como dato y no fundamenta este NO-GO.

## Ancla canonica y alcance

- Instruccion canonica: protocolo `99bd2bd`, mensaje
  `MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0267-hook-v2.md`.
- HEAD de protocolo exigido por la instruccion y revisado en clon limpio:
  `7c98fd47044b394c8d879ed19c2578431c23e4a7`.
- Implementacion citada: `b583090`; cierre de snapshot citado: `7c98fd4`.
- Producto: NOT_RUN. La instruccion canonica declara `SIN PRODUCTO EN ALCANCE`;
  por ello no existe commit de producto ni gate `npm test` aplicable.

## Hallazgos bloqueantes

### F-0267-01 - CRITICAL - rename R100 hacia fuera evade el selector

Ubicacion: `.githooks/pre-commit:18-27` y
`scripts/test_precommit_hook.py:90-95`.

El hook obtiene solo `--name-only` y decide por el nombre resultante. En un rename
R100 desde `scripts/validate_collaboration_state.py` hacia
`docs/validate_collaboration_state.py`, Git presenta la ruta destino no gobernada;
`needs_collaboration_validation` queda en 0. El arnes permanente renombra a
`scripts/validator_renamed.py`, por lo que no ejercita el escape hacia fuera que el
AC promete cerrar.

Reproduccion propia, con los bytes canonicos del hook en fixture aislada y flujo
`git commit` real:

```text
git mv scripts/validate_collaboration_state.py docs/validate_collaboration_state.py
git commit -qm "R100 validator to docs"
EXIT 0 (SLIPS; esperado non-zero)

git mv Area_comun/state/TASK_INDEX.json docs/TASK_INDEX.json
git commit -qm "R100 state to docs"
EXIT 0 (SLIPS; esperado non-zero)
```

Esto refuta toda la familia prometida, no solo un ejemplo: tanto codigo del juicio
como estado gobernado pueden abandonar una raiz seleccionada mediante R100.

### F-0267-02 - WARNING-real - una dependencia unstaged sigue alterando el veredicto

Ubicacion: `.githooks/pre-commit:4-9` frente a la materializacion de
`.githooks/pre-commit:29-54`.

`scripts/prune_state.py --check` se ejecuta desde el worktree antes de materializar
el indice. Payload propio: cambiar solo en unstaged `scripts/prune_state.py` a
`raise SystemExit(23)`, stagear un cambio limpio en `AGENTS.md` y ejecutar commit
real. Resultado: EXIT 1. Con el mismo indice y el prune canonico, el commit pasa.
Por tanto no es verdad que toda dependencia del juicio quede aislada ni que el
veredicto dependa exclusivamente del indice.

## Matriz adversarial

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| Suite permanente por commit real | PASA | `python scripts/test_precommit_hook.py` EXIT 0 |
| Estado staged invalido | PASA | commit real EXIT 1 |
| Mutacion unstaged del validator | PASA | commit limpio EXIT 0 en arnes |
| Trabajo peer unstaged en `Area_comun/state` | PASA | commit propio limpio EXIT 0 en arnes |
| R100 validator `scripts/` -> `docs/` | SLIPS | commit real EXIT 0; F-0267-01 |
| R100 estado `Area_comun/state/` -> `docs/` | SLIPS | commit real EXIT 0; F-0267-01 |
| Delete validator | PASA | commit real EXIT 1 |
| Delete dependencia runtime | PASA | commit real EXIT 1 |
| Delete estado | PASA | commit real EXIT 1 |
| Arming / desarme honesto | PASA | armado invalido EXIT 1; `core.hooksPath` unset EXIT 0 |
| Limpieza temporal tras rechazo | PASA | commit EXIT 1 y `snapshot_residue=[]` |
| CI existencia + SHA-256 | PASA | comando de CI EXIT 0; hash `6871e582...304e` |
| Export default/coordination/runtime | PASA acotado | hook existe y hash coincide en 3/3; runtime CI pineado |
| Suite agregada de instanciacion | ROJO | EXIT 1; fallan `case_coordination_default_and_flag` y `case_runtime_tier_scaffolds_motor_gates_ci_off` |
| Borrado local del propio hook | RIESGO DECLARADO | fuera de cobertura local por limite C1; CI/review unicos detectores |

## Coste independiente

En el clon limpio de `7c98fd4`, dos commits gobernados reales que materializan y
validan el indice completo dieron:

- corrida fria: EXIT 0, 45.756 s;
- corrida caliente: EXIT 0, 46.555 s.

Ambas exceden la referencia aproximada de 10 s. Se declara como riesgo operativo;
no se usa como razon de NO-GO porque el Operador reservo esa decision.

## Gates del protocolo

En clon limpio canonico `7c98fd4` sin secretos:

- `validate_collaboration_state.py`: EXIT 0;
- `scan_domain_neutrality.py`: EXIT 0;
- `scan_encoding.py`: EXIT 0;
- `prune_state.py --check`: EXIT 0;
- drift: `has_drift=false`, `up_to_seq=5000`;
- chain: `valid=true`, `checked_events=4328`;
- `protocol.config.json`: SHA-256
  `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`,
  byte-identico entre `b583090` y `7c98fd4`.

En vivo con secretos antes de materializar este veredicto:

- validate/domain/encoding: EXIT 0;
- drift: `has_drift=false`, `up_to_seq=5012`;
- chain: `valid=true`, `checked_events=4340`;
- config #4 con el mismo SHA-256 y byte-identica contra `7c98fd4`.

## Fix-loop esperado

Iteracion 1/2: remediar el selector para considerar ambos lados de rename/copy (o
derivar la necesidad desde el snapshot completo), agregar negativos permanentes con
rename R100 desde cada familia gobernada hacia fuera, y aislar o declarar/corregir
la ejecucion live de prune. Re-gatear suite real de hook, familia ACMRTD/R100,
instanciacion/export, validate con y sin secretos, domain, encoding, drift 0 y #4
byte-identica. Re-juicio de Analista obligatorio antes de cualquier cierre. Si una
segunda iteracion no cierra los escapes, escalar al Operador.

task_id: TASK-0267
status: CAMBIO-REQUERIDO
executive_summary: Hook v2 mejora el aislamiento, pero R100 desde una raiz gobernada hacia fuera sigue commiteando con EXIT 0 y el prune unstaged aun altera el veredicto.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0267-hook-v2-veredicto.md; Area_comun/mailbox/open/MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0267-hook-v2-NOGO.md
gates: hook suite 0; R100-out 0 inesperado; deletes 1 esperado; validate/domain/encoding 0; drift 0; chain valida; #4 byte-identica; coste 45.756/46.555 s
next_recommended: Remediar F-0267-01 y F-0267-02, agregar negativos de toda la familia y solicitar re-juicio Analista (iteracion 1/2).
risks: Borrado local del hook solo detectable en CI/review; coste muy superior a 10 s reservado al Operador; suite agregada de instanciacion permanece roja.
