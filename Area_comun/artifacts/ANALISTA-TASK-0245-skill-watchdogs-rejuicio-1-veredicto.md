# ANALISTA - TASK-0245 session-watchdogs re-juicio 1

Firma: Analista
Fecha: 2026-07-04

## Veredicto

CAMBIO-REQUERIDO / NO CERRABLE bajo el contrato de ejecucion recibido.

F-0245-01 queda cerrado: el gate `python scripts/test_skills_loader.py` ya es reproducible en clon limpio
del protocolo y no depende de `event-state.runtime.json`. La skill neutral `session-watchdogs` sigue
off-by-default, parametrizada, exportable por `new_instance`, y cargable por el loader read-only.

El bloqueo remanente no esta en F-0245-01 sino en el gate obligatorio de producto pedido para esta pasada:
la instruccion exige clonar `D:/Agentes/Zeus/NOVA/Nova-Budget`, hacer checkout del commit citado y correr
`npm test` ahi, gateando por exit. No hay commit de producto citado en la instruccion canonica de REVIEW, y
el control sobre HEAD local `e3a03a8cf3334c2a84bf54e964319dd08b953b45` falla en la raiz con exit `-4058`
por ausencia de `package.json`. `apps/nova-web` si pasa despues de `npm ci`, pero no lo sustituyo por el
gate raiz sin instruccion canonica corregida.

## Ancla canonica

| Item | Valor |
| --- | --- |
| Protocolo REVIEW | `d5f22eb5aec6ea20e9f5e75bdc8beb7a03e26982` |
| Protocolo remediacion | `75fd96f` |
| Protocolo HEAD limpio pedido | `7a5dfe7` incluido por `d5f22eb` |
| Repo producto | `D:/Agentes/Zeus/NOVA/Nova-Budget` |
| Producto commit citado | Ninguno en la instruccion REVIEW |
| Producto control usado | HEAD local `e3a03a8cf3334c2a84bf54e964319dd08b953b45` |
| Clean clone protocolo | `C:/Users/johnb/AppData/Local/Temp/analista-task0245-20260704063946/protocol` |
| Clean clone producto | `C:/Users/johnb/AppData/Local/Temp/analista-task0245-20260704063946/Nova-Budget` |

## Reproduccion por exit code

| Gate | Exit | Resultado |
| --- | ---: | --- |
| `git clone D:/Agentes/multi_agent_project_protocol <tmp>/protocol` | 0 | PASA |
| `git -C <tmp>/protocol checkout d5f22eb5aec6ea20e9f5e75bdc8beb7a03e26982` | 0 | PASA |
| `python scripts/validate_collaboration_state.py` en clon limpio protocolo | 0 | PASA |
| `python scripts/test_skills_loader.py` en clon limpio protocolo | 0 | PASA; `loaded=["delegate-to-worker"]`, `byte_identical=true` |
| `python examples/skills_loader_cases/run_skills_loader_cases.py` en clon limpio protocolo | 0 | PASA; incluye `AC7-session-watchdogs-registered-neutral-and-loads` |
| `python scripts/scan_domain_neutrality.py` en clon limpio protocolo | 0 | PASA |
| `python scripts/scan_encoding.py` en clon limpio protocolo | 0 | PASA |
| `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1` | 0 | PASA |
| `python -m py_compile scripts/test_skills_loader.py skills/loader.py scripts/new_instance.py` | 0 | PASA |
| Probe propia: habilitar solo `session-watchdogs` en registry temporal y cargar con `skills.loader.load_skills` | 0 | PASA; placeholders requeridos presentes; sin hits `D:/Agentes`, `multi_agent_project_protocol`, `Arquitecto`, `Codex`, `Analista`, `Nova`, `Budget` |
| `python scripts/new_instance.py ... --target <tmp>/generated-instance2 --force` | 0 | PASA |
| Probe propia en instancia generada: habilitar solo `session-watchdogs` y cargar loader read-only | 0 | PASA |
| Drift limpio via `protocol_state_drift(Path("."))` | 0 | PASA; `has_drift=false`, `up_to_seq=3804` |
| `git diff --exit-code 75fd96f -- protocol.config.json` | 0 | PASA |
| `git diff --exit-code 7a5dfe7 -- protocol.config.json` | 0 | PASA |
| `git diff --exit-code d5f22eb -- protocol.config.json` | 0 | PASA |
| `Get-FileHash protocol.config.json -Algorithm SHA256` | 0 | PASA; `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |
| `git clone D:/Agentes/Zeus/NOVA/Nova-Budget <tmp>/Nova-Budget` | 0 | PASA |
| `git -C <tmp>/Nova-Budget checkout e3a03a8cf3334c2a84bf54e964319dd08b953b45` | 0 | PASA como control no citado |
| `npm test` en raiz del clon limpio Nova-Budget | -4058 | SLIPS; no existe `package.json` raiz |
| `npm ci` en `<tmp>/Nova-Budget/apps/nova-web` | 0 | PASA |
| `npm test` en `<tmp>/Nova-Budget/apps/nova-web` | 0 | PASA; 1/1 |
| Vivo: `python scripts/validate_collaboration_state.py` | 0 | PASA |
| Vivo: `python scripts/scan_encoding.py` | 0 | PASA |
| Vivo: `python scripts/scan_domain_neutrality.py` | 0 | PASA |
| Vivo: drift via `protocol_state_drift(Path("."))` | 0 | PASA; `has_drift=false`, `up_to_seq=3804` |

## Tabla vector por vector

| Vector / AC | Estado | Evidencia falsable |
| --- | --- | --- |
| F-0245-01: `scripts/test_skills_loader.py` no depende de archivo local ignorado | PASA | Clon limpio `d5f22eb`, `python scripts/test_skills_loader.py` exit 0. La lista de watched paths ya no exige `event-state.runtime.json`. |
| Skill neutral en `skills/` | PASA | `skills/session-watchdogs.skill.md` existe, frontmatter `neutral_core: true`, loader y scan domain exit 0. |
| Registro off-by-default | PASA | `skills/skills.config.json` contiene `session-watchdogs` con `enabled:false` y `trust_boundary` read-only/no-authority/no-output. |
| Parametrizacion sin literales del dogfooding | PASA | Probe propia cargo la skill y busco `D:/Agentes`, `multi_agent_project_protocol`, `Arquitecto`, `Codex`, `Analista`, `Nova`, `Budget`: hits `[]`. |
| Export via `new_instance` | PASA | Instancia generada en tmp contiene la skill y el loader la resuelve al habilitar solo `session-watchdogs`. |
| Caso de prueba en examples / suite skills | PASA | `examples/skills_loader_cases` exit 0 con `AC7-session-watchdogs-registered-neutral-and-loads`. |
| Protocol config / epoch pineado intacto | PASA | `protocol.config.json` sin diff contra `75fd96f`, `7a5dfe7` y `d5f22eb`; SHA256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. |
| Gate producto obligatorio de esta ejecucion | SLIPS | No hay commit de producto citado; `npm test` en raiz del clon limpio Nova-Budget HEAD local `e3a03a8` exit `-4058`. |

## Hallazgo bloqueante

**WARNING-real F-0245-R1-PRODUCT-GATE:** el contrato de ejecucion exige un gate de producto canonico
(`Nova-Budget` checkout del commit citado, `npm test` en esa raiz, gate por exit), pero la instruccion de
REVIEW no cita commit de producto y la raiz del repo no es paquete npm. Repro: clonar
`D:/Agentes/Zeus/NOVA/Nova-Budget`, checkout `e3a03a8cf3334c2a84bf54e964319dd08b953b45` como control local,
ejecutar `npm test` en la raiz -> exit `-4058`, `ENOENT package.json`.

## Residuales

- No encontre escape nuevo en la garantia propia de TASK-0245.
- `apps/nova-web` pasa `npm ci` + `npm test`, pero queda como evidencia auxiliar hasta que el Arquitecto
  corrija canonicamente el gate de producto o provea un root `package.json`.

## Fix-loop esperado

Iteracion 1 de 2. El owner de la coordinacion debe hacer una de estas dos cosas antes del cierre:

1. Proveer una instruccion REVIEW corregida con commit de producto canonico y gate exacto de producto que
   deba ser vinculante para TASK-0245; o
2. Corregir la instruccion canonica para declarar que TASK-0245 no tiene producto citable y que el gate de
   control aceptado es `apps/nova-web/npm ci` + `apps/nova-web/npm test`, no `npm test` en la raiz.

Despues, re-juicio Analista antes de commit de cierre. Si la misma clase de fallo sobrevive dos iteraciones,
escalar al operador con una pregunta concreta.

task_id: TASK-0245
status: change_required
executive_summary: F-0245-01 queda cerrado por comportamiento en clon limpio: el loader gate ya es reproducible y la skill session-watchdogs mantiene neutralidad, parametrizacion, off-by-default y export via new_instance. TASK-0245 no es cerrable bajo el contrato de esta ejecucion porque no hay commit de producto citado y `npm test` en la raiz del clon limpio Nova-Budget sale exit -4058.
artifacts:
  - path_or_commit: Area_comun/artifacts/ANALISTA-TASK-0245-skill-watchdogs-rejuicio-1-veredicto.md
  - path_or_commit: Area_comun/mailbox/open/MSG-20260704-Arquitecto-to-Analista-REVIEW-TASK-0245-rejuicio-1.md
  - path_or_commit: d5f22eb5aec6ea20e9f5e75bdc8beb7a03e26982
gates:
  - command: python scripts/test_skills_loader.py
    result: PASS
  - command: python examples/skills_loader_cases/run_skills_loader_cases.py
    result: PASS
  - command: python scripts/validate_collaboration_state.py
    result: PASS
  - command: python scripts/scan_encoding.py
    result: PASS
  - command: python scripts/scan_domain_neutrality.py
    result: PASS
  - command: npm test (Nova-Budget root clean clone)
    result: FAIL exit -4058
next_recommended: Corregir canonicamente el gate/ancla de producto para TASK-0245 o proveer root npm test verde; luego pedir re-juicio antes del cierre.
risks: F-0245-01 cerrado; el residual bloqueante es de cierre/gate producto, no de la skill neutral.
