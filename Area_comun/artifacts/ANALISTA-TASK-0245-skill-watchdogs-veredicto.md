# ANALISTA - TASK-0245 session-watchdogs review

Firma: Analista
Fecha: 2026-07-04
Veredicto: CAMBIO-REQUERIDO / NO CERRABLE

## Ancla canonica

- Protocolo REVIEW HEAD: `984361dcff7225d3dec9c7d1f8b7156fa984a37d`
- Implementacion citada: `6a1cd56ce47f6b4c918aaa4863913e0a0a2c475a`
- Instruccion REVIEW: `Area_comun/mailbox/open/MSG-20260704-Arquitecto-to-Analista-REVIEW-TASK-0245-skill-watchdogs.md`
- Producto: N/A. La instruccion canonica declara "Producto commit citable: NINGUNO" y alcance 100% hub.

## Reproduccion

| Gate | Contexto | Exit | Resultado |
| --- | --- | ---: | --- |
| `git clone D:\Agentes\multi_agent_project_protocol <tmp>; git checkout 984361dcff7225d3dec9c7d1f8b7156fa984a37d` | clon limpio | 0 | PASA |
| `python scripts/validate_collaboration_state.py --root <clone>` | clon limpio sin secretos | 0 | PASA |
| `python scripts/scan_encoding.py --root <clone>` | clon limpio | 0 | PASA |
| `python scripts/scan_domain_neutrality.py --root <clone>` | clon limpio | 0 | PASA |
| `python examples/skills_loader_cases/run_skills_loader_cases.py` | clon limpio | 0 | PASA |
| `python scripts/test_skills_loader.py` | clon limpio | 1 | FALLA: falta `event-state.runtime.json` |
| `python scripts/new_instance.py --source-template <clone> --target <tmp>/generated-instance ... --force` | clon limpio | 0 | PASA |
| probe propio `skills.loader.load_skills` habilitando `session-watchdogs` en instancia generada | instancia generada | 0 | PASA |
| forbidden literal probe sobre `skills/session-watchdogs.skill.md` | clon limpio | 0 | PASA: sin `multi_agent_project_protocol`, `Arquitecto`, `Codex`, `Analista`, `Nova`, `Budget`, `D:/Agentes`, `bot_spot`, `trading` |
| drift + chain probe | clon limpio | 0 | PASA: `has_drift=false`, `up_to_seq=3794`, `checked_events=3122` |
| `git diff --exit-code 6a1cd56 984361d -- protocol.config.json` | canonico | 0 | PASA: byte-identico |

`protocol.config.json` SHA256 en clon limpio: `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.

## Vector por vector

| Vector / AC | Juicio | Evidencia falsable |
| --- | --- | --- |
| Skill neutral en `skills/` y scan domain verde | PASA | `scan_domain_neutrality.py --root <clone>` exit 0; probe de literales prohibidos exit 0. |
| Registro off-by-default | PASA | `skills/skills.config.json` contiene `session-watchdogs`, `enabled:false`, `neutral_core:true`, trust boundary read-only/no-authority/no-output. |
| Patrones parametrizados sin rutas/nombres hardcodeados del dogfooding | PASA | Body usa placeholders `<WORKSPACE_ROOT>`, `<MAILBOX_OPEN_DIR>`, `<STATE_DIR>`, `<RUNTIME_TMP_DIR>`, `<WORKER_IDS>`; probe de literales locales exit 0. |
| `new_instance` exporta `skills/` | PASA | Instancia generada contiene `skills/session-watchdogs.skill.md`; comando exit 0. |
| Loader read-only resuelve la skill en instancia generada | PASA | Probe propio habilito solo `session-watchdogs` en el registry generado y `load_skills(root)` devolvio `has_session_watchdogs:true`, exit 0. |
| Caso de prueba en `examples/` valida carga+neutralidad | PASA | `examples/skills_loader_cases/run_skills_loader_cases.py` exit 0, incluye AC7 `session-watchdogs-registered-neutral-and-loads`. |
| Gates verdes en clon limpio | SLIPS | `scripts/test_skills_loader.py` sale exit 1 en clon limpio porque espera `event-state.runtime.json`, archivo ausente en el arbol git de `984361d`. El mismo gate fue declarado PASS en el handoff, por lo que la entrega no es reproducible desde canonico limpio. |
| Epoch pineado y `protocol.config.json` intactos | PASA | diff `6a1cd56..984361d` sobre `protocol.config.json` exit 0; sha256 estable. |

## Hallazgo bloqueante

F-0245-01 [WARNING-real]: gate de loader no reproducible en clon limpio.

Repro:

```text
git clone D:\Agentes\multi_agent_project_protocol <tmp>\protocol
git -C <tmp>\protocol checkout 984361dcff7225d3dec9c7d1f8b7156fa984a37d
python <tmp>\protocol\scripts\test_skills_loader.py
```

Resultado observado:

```text
AssertionError: missing watched paths: ['event-state.runtime.json']
```

Impacto: el handoff lista `python scripts/test_skills_loader.py PASS`, pero ese gate depende de un archivo local no versionado o no presente en el clon limpio. Bajo la regla de review canonica, un gate declarado como verde debe ser reproducible desde HEAD limpio. No cierro con un gate rojo aunque los AC funcionales especificos de `session-watchdogs` pasen.

## Residuales

- No ejecute `npm test` de Nova-Budget: la instruccion REVIEW canonica declara que TASK-0245 no tiene producto ni commit citable y que el alcance es solo hub (`skills/`, `scripts/new_instance.py`, `examples/`).
- No encontre un escape nuevo en la familia de neutralidad/parametrizacion/export/load: el bloqueo es reproducibilidad del gate limpio, no la semantica de la skill.

## Fix-loop esperado

Remediacion: hacer reproducible `python scripts/test_skills_loader.py` en clon limpio, ya sea versionando/proveyendo el fixture requerido, cambiando el test para no depender de `event-state.runtime.json` local, o corrigiendo el handoff/gate canonico para excluirlo de manera explicita y justificada. Re-gatear validate con y sin secretos, encoding, domain, examples/skills loader, new_instance+loader probe, drift 0 y #4 byte-identica. Re-juicio Analista antes de cualquier cierre; maximo 2 iteraciones antes de escalar al operador si la misma clase de fallo persiste.

task_id: TASK-0245
status: change_required
executive_summary: TASK-0245 no es cerrable porque un gate declarado PASS por el handoff falla en clon limpio canonico. La skill, el registro, la parametrizacion, new_instance y el loader probe pasan, pero `scripts/test_skills_loader.py` depende de `event-state.runtime.json` ausente en el arbol versionado.
artifacts:
  - Area_comun/artifacts/ANALISTA-TASK-0245-skill-watchdogs-veredicto.md
gates:
  - command: python scripts/validate_collaboration_state.py --root <clone>
    result: PASS
  - command: python scripts/scan_encoding.py --root <clone>
    result: PASS
  - command: python scripts/scan_domain_neutrality.py --root <clone>
    result: PASS
  - command: python examples/skills_loader_cases/run_skills_loader_cases.py
    result: PASS
  - command: python scripts/test_skills_loader.py
    result: FAIL
  - command: python scripts/new_instance.py --source-template <clone> --target <tmp>/generated-instance ... --force
    result: PASS
  - command: drift + chain probe
    result: PASS
next_recommended: Codex/Arquitecto deben corregir la reproducibilidad del gate de loader en clon limpio o ajustar el gate canonico, y pedir re-juicio.
risks: Si se cierra asi, el repositorio aceptaria como verde un gate que solo pasa con archivo local no versionado.
