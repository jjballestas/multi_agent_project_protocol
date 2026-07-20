# ANALISTA - TASK-0273 deadlock poda-vs-claim (reparto aviso/coordinacion/CI) - veredicto adversarial

Firma: Analista (voz adversarial independiente). Fecha local: 2026-07-20 14:10.
Instruccion canonica: `Area_comun/mailbox/open/MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0273-deadlock-poda.md`.

## Veredicto de cabecera

**GO / OK-CERRABLE.** La respuesta a las tres preguntas del REVIEW: (1) GO; (2) mi medicion
del `--apply` no-op tras el fix es **0.293s / 0.281s** (clon limpio, config viva con
maintenance habilitado, poda no vencida) frente a `--check` 0.377s -- baja de 87-89s a
sub-segundo, con `no_op:true`, `transaction:null` y CERO escrituras de ledger verificadas
por hash; (3) NO logre que el hook dejara pasar un estado invalido: 9/9 escenarios de mi
bateria aguantaron, incluido el ataque combinado (poda vencida + estado invalido staged en
modo full) que la suite del maker no cubria. La frontera se movio exactamente donde la
directiva pedia y en ningun otro sitio: solo la poda ablanda en local; validate, drift de
guia, archivos de juicio y centinela CI siguen abortando identico, y el propio aviso queda
acotado por el CI rojo accionable.

## Ancla canonica y reproduccion

- Implementacion `3062214` (=`51deaf1` re-escrito), entrega HANDOFF-TASK-0273; HEAD del
  protocolo en la pasada: `18e7cfd`.
- Clon limpio `D:/ccv0273` checkout `18e7cfd1c67d0da83fbf7d849283df80df176a64`; todos los
  gates, suites y ataques corridos AHI. SIN PRODUCTO EN ALCANCE por instruccion canonica.
- Suites del maker en el clon (exit codes): `python examples/prune_state_cases/
  run_prune_state_cases.py` EXIT 0; `python examples/runtime_prune_cases/
  run_runtime_prune_cases.py` EXIT 0; `python scripts/test_precommit_hook.py` EXIT 0;
  `python scripts/test_attested_instancing.py` EXIT 0.
- Bateria adversarial propia: sandbox git efimero espejo del fixture del maker con el hook
  REAL del clon (9 escenarios, script reproducible); camino genuino adicional con el
  `prune_state.py` REAL sobre fixture vencido de examples (no stub): `--check` EXIT 1 con
  razones, paso CI simulado EXIT 1 con mensaje accionable, `--apply` real archiva 4 tasks +
  6 claims respetando claim activo y task in_progress, `--check` posterior EXIT 0, `--apply`
  no-op posterior 0.077s.

## Tabla vector por vector (instruccion del Arquitecto)

| # | Vector | Resultado | Evidencia falsable |
|---|--------|-----------|--------------------|
| 1 | Aviso local sin abortar; el resto del hook bloquea igual | **PASA** | S1/S2: poda vencida + cambio valido -> WARNING accionable en stderr + commit EXIT 0 (bounded y full). S3 (ataque central): poda vencida + TASK_INDEX invalido staged en full -> EXIT 1 "collaboration state in staged snapshot is invalid" CON el warning presente; el aviso no enmascara el juicio. S4: invalido solo -> EXIT 1 (baseline identico a ayer). S5: poda vencida + drift de guia staged en bounded -> EXIT 1 "human guide template drift". S7: poda vencida + borrado staged de prune_state.py en full -> EXIT 1 "required judgment file missing". S8: poda vencida + borrado staged del workflow CI en full -> EXIT 1. 9/9 sin escape. |
| 2 | CI exige poda al dia, rojo accionable | **PASA** | Paso nuevo en validate.yml: `if ! prune_state --check` -> "ERROR: protocol state pruning is overdue..." + exit 1. Simulado con fixture REAL vencido: EXIT 1 + mensaje; al dia: EXIT 0. Fail-closed: cualquier exit!=0 del check (incluido crash) pone rojo. Pin sha256 del hook actualizado y verificado: `739d9ead...704e` coincide byte a byte con `.githooks/pre-commit` en HEAD (un pin desactualizado habria dejado CI rojo). |
| 3 | Poda coordinada documentada con precondiciones verificables | **PASA** | `Area_comun/protocol/TASK_PROTOCOL.md` seccion "Coordinated Pruning Checkpoint" (5 pasos: precondiciones read-only separadas -- arbol gobernado limpio + cero claims activos --, diferir si fallan, barrera a peers solo excepcional, apply con identidad Arquitecto via submit_intent en modo runtime, gates + commit explicito antes de reanudar). Espejo en la skill master mailbox-hygiene ("Poda coordinada en el checkpoint"). |
| 4 | Camino no-op barato en --apply | **PASA** | MI medicion en clon (config viva, enabled, no vencida): `--check` 0.377s; `--apply` 0.293s y 0.281s, `mode:noop`, `no_op:true`, `transaction:null`. Verificado con sha256 antes/despues de TASK_INDEX/CLAIMS/PROJECT_STATE/events.jsonl/snapshot.json: CERO bytes escritos; `git status --porcelain` vacio. Contra 89.055s/86.732s pre-fix: mejora ~300x. El early-return evalua assess() ANTES del gate de enforcement, asi que tampoco abre claim ni intent en modo runtime-authoritative (probado en el clon, que ES runtime-tier). |
| 5 | Espejo born-operational + conjunto adoptable | **PASA** | Instancia runtime-tier generada con new_instance.py: hook byte-identico (sha256 `739d9ead...704e`), prune_state.py byte-identico (`a1303550...9de0`), workflow con pin + paso rojo, TASK_PROTOCOL.md con la seccion (linea 310). Instancia attested encapsulada (governance-dir): hook/doc identicos + workflow en raiz de producto con `working-directory: aegis` (las rutas resuelven) + skill mailbox-hygiene con el espejo del checkpoint (linea 181) en aegis/.claude/skills/. |
| 6 | claim-como-lock, validate y drift NO relajados | **PASA** | Diff de 3062214 NO toca validate_collaboration_state.py, protocol_replay.py ni submit_intent.py. Camino vencido de --apply intacto (solo se antepone el early-return): en el fixture real la poda respeta claim activo y task in_progress. S3/S4/S5/S7/S8 prueban que ningun otro juicio del hook ablando. Drift EXIT 0 en clon. |

## Hallazgos residuales declarados (ninguno bloquea el cierre)

- **R1 (aceptado por diseno, declarado):** en local un CRASH de prune_state.py (exit!=0 por
  causa distinta a poda vencida) ayer abortaba el commit y hoy solo avisa. Es coherente con
  el reparto (el hook no distingue exit-codes del check) y el CI es fail-closed ante el
  mismo crash (rojo), pero la deteccion pasa de commit-time a integracion.
- **R2 (endurecimiento simultaneo, vigilar cadencia):** assess() gana un disparador nuevo de
  poda vencida (`next_actions > recent_next_actions=8`, clave ya presente en el config
  pineado). En HEAD esta bajo umbral (`--check` EXIT 0), pero si next_actions crece >8 entre
  checkpoints, la integracion queda roja hasta que el Arquitecto condense: es el mecanismo
  disenado, no un defecto, y conviene tenerlo en la cadencia del checkpoint.
- **R3 (cosmetico):** el JSON del --apply en camino vencido no emite clave `mode` (el no-op
  si emite `mode:noop`); inconsistencia menor de salida, sin efecto de juicio.
- **R4 (cobertura de suite):** el assert de coste no-op del maker solo cubre el fixture
  DISABLED; el caso enabled-no-vencida (el operativo real) lo cubri yo en vivo (0.28-0.29s)
  y post-apply (0.077s). Sugerencia no bloqueante: anadir ese negativo a la suite.
- **R5 (pre-existente, verificado, NO regresion de 0273):** la suite agregada
  runtime_instantiation_cases falla en 2 casos (case_coordination_default_and_flag,
  case_runtime_tier_scaffolds_motor_gates_ci_off) IGUAL en HEAD y en 3062214~1 (diff de
  casos fallidos vacio entre ambos); coincide con lo declarado por el maker en el handoff.
  Merece unidad de mantenimiento propia.

## Gates del protocolo (clon limpio 18e7cfd salvo indicado)

- `python scripts/validate_collaboration_state.py`: vivo (con secretos) EXIT 0; clon (sin
  secretos) EXIT 0.
- `python scripts/scan_encoding.py` EXIT 0; `python scripts/scan_domain_neutrality.py` EXIT 0.
- `python runtime/protocol_replay.py --check-drift` EXIT 0 (drift 0).
- `protocol.config.json` byte-identico vivo/clon sha256
  `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`; epoch 1.14.0 intacta.
- Producto: NOT_RUN por instruccion canonica (SIN PRODUCTO EN ALCANCE).

## Recomendacion de cierre

**OK -> CERRABLE.** La unidad cumple el acceptance completo: reparto aviso/coordinacion/CI
verificado por comportamiento, camino no-op ~300x mas barato con cero escrituras, espejo
born-operational byte-identico en ambos tiers, y ninguna garantia de juicio relajada (9/9
ataques contenidos). R1-R5 declarados; R5 pide unidad de mantenimiento aparte (pre-existente).

---

task_id: TASK-0273
status: in_review
executive_summary: GO / OK-CERRABLE. Los 6 vectores PASAN. No logre colar un estado invalido - 9/9 ataques contenidos, incluido poda-vencida+estado-invalido en full (aborta identico con el warning presente), poda-vencida+drift-de-guia, +borrado-de-prune y +borrado-del-workflow. Mi medicion no-op --apply: 0.293s/0.281s vs --check 0.377s (antes 87-89s, ~300x), no_op true, transaction null, cero bytes de ledger escritos. CI rojo accionable fail-closed con pin sha del hook verificado byte a byte. Espejo born-operational byte-identico en runtime y attested (working-directory correcto). claim-como-lock/validate/drift intactos por diff y por comportamiento. Residuales R1-R5 declarados, ninguno bloquea; R5 (suite instantiation con 2 casos rojos) verificado pre-existente e identico en el commit padre.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0273-deadlock-poda-veredicto.md
gates: clon 18e7cfd validate EXIT 0; encoding EXIT 0; domain EXIT 0; drift EXIT 0; config #4 byte-identica 2E35F26E...354; suites maker prune/runtime-prune/hook/attested-instancing EXIT 0; bateria adversarial 9/9 PASA
next_recommended: Arquitecto ratifica GO y cierra TASK-0273 (task_status done via submit_intent + archivar la instruccion consumida); considerar unidad de mantenimiento para R5 y el negativo de suite de R4.
risks: R1 crash de prune en local se detecta en CI y no en commit-time; R2 el disparador next_actions>8 puede poner CI rojo entre checkpoints si la cadencia de condensacion se descuida; R5 suite runtime_instantiation_cases con 2 casos rojos pre-existentes sin dueno.
