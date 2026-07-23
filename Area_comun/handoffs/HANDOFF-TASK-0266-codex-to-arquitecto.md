---
handoff_id: HANDOFF-TASK-0266-codex-to-arquitecto
task_id: TASK-0266
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-23
implementation_commit: cef1e9bad39330510e62bea03fc9cdfe473d2b77
checker: Analista
---

# HANDOFF TASK-0266 - Propagacion y activacion del harness

## Resultado

- E4: `.githooks/**` pertenece al conjunto adoptable por defecto de
  `scripts/upgrade_instance.py`; el caso sandbox prueba que el reporte marca el hook como
  `nuevo` para una instancia existente.
- E5: `scripts/new_instance.py` inicializa el target como repositorio Git y configura
  `core.hooksPath` a `.githooks` o a la ruta relativa equivalente para gobernanza
  encapsulada. El caso scratch comprueba la configuracion y que un estado gobernado roto
  staged aborta el commit.
- H1: `runtime.vcs.commit_turn` usa `verify=True` por defecto. `verify=False` queda
  documentado como excepcion explicita de recuperacion para reparar o revertir el propio
  gate. El caso runtime prueba fallo con hook rojo, y exito solo con bypass explicito.
- La guia de instanciacion documenta activacion automatica en instancias nuevas y el paso
  gobernado separado para aplicar/armar el delta en instancias existentes.

## Guardas respetadas

- Todas las pruebas de propagacion se ejecutaron en `TemporaryDirectory` sandbox/scratch.
- No se aplico upgrade a NOVA ni a ninguna instancia viva.
- No se modificaron `.githooks/pre-commit`, `protocol.config.json`,
  `protocol.config.template.json`, supervised autonomy ni real invoker.

## Verificacion

- `python examples/runtime_upgrade_cases/run_runtime_upgrade_cases.py` -> exit 0, 5 casos.
- `python examples/runtime_apply_cases/run_runtime_apply_cases.py` -> exit 0, 5 casos.
- `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py` -> exit 0,
  8 casos mas paridad PowerShell cuando disponible.
- `python -m py_compile ...` sobre los seis archivos Python modificados -> exit 0.
- `python scripts/validate_collaboration_state.py` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py` -> exit 0.
- `git diff --check` -> exit 0.

## Revision solicitada

Arquitecto debe rutear el commit `cef1e9b` a Analista para juicio independiente. Codex no
revisa ni ratifica su propia implementacion.
