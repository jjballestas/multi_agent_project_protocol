---
artifact_id: ANALISTA-TASK-0230-aegis-regate-veredicto
task_id: TASK-0230
author: Analista
status: change_required
created_at: 2026-07-03
review_target: DECISION-0085 Aegis layout re-gate
---

# Veredicto Analista - TASK-0230 Aegis re-gate

Decision: CAMBIO-REQUERIDO / NO-GO.

Ancla canonica: protocolo HEAD `5f385b5aeae22113268bb286b4e63511f789729a`; instruccion REVIEW `2a68508`; re-deliver protocolo `89b15d1`; producto `D:/Agentes/Zeus/Zeus-protocol` commit `e7c6da4`; instancia `D:/Agentes/Zeus/NOVA/Aegis` commit `ab2b6a2335c5cdb973a77bc955010dfce2bd7dce`; source tag `v1.18.0` commit `c9a442354bb5002b4df3a21e581ef1e891029c58`.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git fetch origin` | EXIT 0 |
| `git status --short` | EXIT 0; dirty tree preexistente ajeno: `.claude/settings.json` y rutas no trackeadas de Arquitecto/operador. No tocado. |
| `python scripts/validate_collaboration_state.py` | EXIT 0; warnings de FYI/ACK archivables, no hard fail. |
| Clean clone `Zeus-protocol` + `git checkout e7c6da4` + `npm test` | EXIT 0; 112 tests, 90 pass, 22 skipped. |
| Payload propio `createNewInstance` en clon limpio | EXIT 0; dry-run default pin `v1.18.0`; write real en tmp desde `c9a4423`; destino existente falla; nombres `NOVA`, `../escape`, `nova_budget`, `a`, `nova..budget`, `-bad` fallan; ref inexistente falla; DoR feature/product cubre positivos y negativos por familia. Residual: `bad-` se acepta. |
| `python scripts/validate_collaboration_state.py` en clon limpio del hub `5f385b5` | EXIT 0 |
| `python scripts/scan_encoding.py` en clon limpio del hub `5f385b5` | EXIT 0 |
| `python scripts/scan_domain_neutrality.py` en clon limpio del hub `5f385b5` | EXIT 0 |
| Drift clon limpio del hub `5f385b5` | `has_drift=false`, `up_to_seq=3507` |
| `python scripts/scan_encoding.py` en hub vivo | EXIT 0 |
| `python scripts/scan_domain_neutrality.py` en hub vivo | EXIT 0 |
| Drift hub vivo | `has_drift=false`, `up_to_seq=3507` |
| `git diff --exit-code c9a4423 -- protocol.config.json` en hub vivo | EXIT 0; byte-identico contra tag `v1.18.0` |
| `python scripts/validate_collaboration_state.py --root D:/Agentes/Zeus/NOVA/Aegis` | EXIT 0 |
| `python scripts/scan_encoding.py --root D:/Agentes/Zeus/NOVA/Aegis` | EXIT 0 |
| `python scripts/scan_domain_neutrality.py --root D:/Agentes/Zeus/NOVA/Aegis` | EXIT 0 |
| Drift Aegis | `has_drift=false`, `up_to_seq=3457` |
| `git -C D:/Agentes/Zeus/NOVA/Aegis diff --exit-code c9a4423 -- protocol.config.json` | EXIT 0; byte-identico contra tag `v1.18.0` |

## Vector por vector

| Vector / AC de la instruccion | Veredicto | Evidencia falsable |
| --- | --- | --- |
| NOVA es carpeta plana y no repo git | PASA | `Test-Path D:/Agentes/Zeus/NOVA/.git` negativo; `Get-ChildItem D:/Agentes/Zeus/NOVA` muestra solo `Aegis`. |
| Aegis es repo git propio | PASA | `git -C D:/Agentes/Zeus/NOVA/Aegis rev-parse HEAD` -> `ab2b6a2335c5cdb973a77bc955010dfce2bd7dce`. |
| Aegis no contiene repo-dentro-de-repo como working tree | PASA | Busqueda de `.git` bajo `NOVA/Aegis` devuelve solo `D:/Agentes/Zeus/NOVA/Aegis/.git`. |
| No hay repos de producto creados aun | PASA | `Get-ChildItem D:/Agentes/Zeus/NOVA` no devuelve `Nova-Budget`, `Nova-Treasury` ni variantes producto. |
| Instancia creada desde tag `v1.18.0` | PASA | Aegis history: `c9a4423` -> `172edcb5` -> `ab2b6a2`; `protocol.config.json` byte-identico a `c9a4423`. Payload propio de bootstrapper escribe desde source commit `c9a442354bb5002b4df3a21e581ef1e891029c58`. |
| `instance.profile.json` y `.agents/*/config.json` apuntan a `NOVA/Aegis` y no al path viejo | PASA | Grep acotado a `instance.profile.json`, `.agents`, `TASK_TEMPLATE.md` devuelve solo `D:/Agentes/Zeus/NOVA/Aegis` para rutas activas. |
| Handoff no debe referenciar el path viejo `Zeus/nova-budget` | SLIPS - WARNING-real | `git grep -n -I -i "D:/Agentes/Zeus/nova-budget\\|Zeus/nova-budget" -- Area_comun/handoffs/HANDOFF-TASK-0230-codex-to-arquitecto-1.md` devuelve linea 22: `Instance created at D:/Agentes/Zeus/nova-budget ...`. La instruccion de review pide explicitamente que el handoff referencie `NOVA/Aegis`, NO el path viejo ni `Zeus/nova-budget`. Uso normal: un cold-start que lea el handoff puede tomar la ruta vieja como parte de la entrega canonica. |
| Perfil Aegis neutral respecto a producto | SLIPS - WARNING-real | `D:/Agentes/Zeus/NOVA/Aegis/instance.profile.json` declara `instance.id=aegis` y `path=NOVA/Aegis`, pero `operatingProfile.arm` sigue en `budget`. Bajo DECISION-0085, Aegis es la instancia-metodologia que gobierna todos los modulos `Nova-X`; `budget` es producto lazy, no identidad de Aegis. |
| Cosecha gentle-ai nivel B: configs de agente commiteadas, Git adapter, no multi-IDE | PASA | `.agents/Analista|Arquitecto|Codex/config.json` trackeados; `adapter=git`, `workspaceRoot=D:/Agentes/Zeus/NOVA/Aegis`, `committedConfig=true`. |
| `gentle-ai install` ausente / Engram prohibido | PASA con residual | Grep de configs y profile no contiene `gentle-ai install`; profile declara `engramInstallAllowed=false`. Residual no bloqueante: la palabra `engram` aparece solo como flag negativo. |
| Hub intacto, epoch pinado, TFM no movida a Aegis | PASA | Hub validate/encoding/neutrality EXIT 0; drift 0; `protocol.config.json` byte-identico a `v1.18.0`; no evidencia de traslado TFM a Aegis. |

## Hallazgos

### F-0230-AEGIS-01 - WARNING-real - Handoff aun contiene path viejo como entrega canonica

El handoff activo `Area_comun/handoffs/HANDOFF-TASK-0230-codex-to-arquitecto-1.md` contiene `D:/Agentes/Zeus/nova-budget` en una linea de entrega. La instruccion de re-gate exigio que el handoff, profile y configs apunten a `NOVA/Aegis`, no a `Zeus/nova-budget`. Esto no es solo historico en un archivo archivado: es el handoff vigente de cierre de TASK-0230.

Remediacion esperada: reemplazar la linea por una formula no ambigua: instancia final en `D:/Agentes/Zeus/NOVA/Aegis`; staging temporal o path anterior no es ruta canonica y no debe ser usado. Si se quiere conservar trazabilidad, moverla a una nota explicita de "historical staging, not canonical path".

### F-0230-AEGIS-02 - WARNING-real - `instance.profile.json` conserva `operatingProfile.arm=budget`

El profile actual de Aegis conserva una identidad de brazo `budget`, heredada del alcance flat `nova-budget`. DECISION-0085 reubica Aegis como instancia-metodologia neutral de la suite, y `Nova-Budget` queda como producto lazy futuro. Este campo actual puede hacer que un agente trate Aegis como instancia de un solo producto.

Remediacion esperada: ajustar el profile a un arm neutral de gobernanza/suite, o registrar explicitamente por decision que `budget` es intencional y no implica producto creado ni dominio dentro de Aegis.

## Residuales no bloqueantes

- El bootstrapper acepta nombre `bad-` como kebab-case. No lo bloqueo porque no rompe root containment, no crea path escape y no fue AC explicito de DECISION-0085.
- Aegis contiene menciones historicas a `nova-budget` heredadas del tag y de decisiones previas. No bloqueo el historico completo porque `scan_domain_neutrality.py --root D:/Agentes/Zeus/NOVA/Aegis` esta verde y la instruccion pidio current handoff/profile/configs como superficie critica.

## Recomendacion

CAMBIO-REQUERIDO. No cierres TASK-0230 hasta que el handoff vigente y el profile queden coherentes con DECISION-0085. Fix-loop esperado: Codex remedia F-0230-AEGIS-01/F-0230-AEGIS-02, re-corre gates Aegis + hub, y Arquitecto pide re-juicio antes del commit de cierre. Maximo 2 iteraciones antes de escalar al operador.

task_id: TASK-0230
status: change_required
executive_summary: NO-GO por dos slips de coherencia DECISION-0085: el handoff vigente aun menciona `D:/Agentes/Zeus/nova-budget`, y el profile de Aegis conserva `operatingProfile.arm=budget`. Los gates tecnicos pasan, pero la evidencia canonica no es cerrable como layout Aegis neutral.
artifacts:
  - path_or_commit: Area_comun/artifacts/ANALISTA-TASK-0230-aegis-regate-veredicto.md
  - path_or_commit: D:/Agentes/Zeus/Zeus-protocol@e7c6da4
  - path_or_commit: D:/Agentes/Zeus/NOVA/Aegis@ab2b6a2335c5cdb973a77bc955010dfce2bd7dce
gates:
  - command: npm test in clean clone of Zeus-protocol at e7c6da4
    result: PASS
  - command: python scripts/validate_collaboration_state.py in hub live and clean clone
    result: PASS
  - command: python scripts/scan_encoding.py in hub live, hub clean clone, and Aegis
    result: PASS
  - command: python scripts/scan_domain_neutrality.py in hub live, hub clean clone, and Aegis
    result: PASS
  - command: drift checks for hub live, hub clean clone, and Aegis
    result: PASS
  - command: git diff --exit-code c9a4423 -- protocol.config.json in hub and Aegis
    result: PASS
next_recommended: Remediate F-0230-AEGIS-01 and F-0230-AEGIS-02, then request Analista re-gate before closure.
risks: If closed as-is, future cold-starts can keep using the obsolete `Zeus/nova-budget` path or treat Aegis as a budget-only product instance.
