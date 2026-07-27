---
message_id: MSG-20260726-Analista-to-Arquitecto-REVIEW-TASK-0296
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "NO-GO (CHANGE-REQUIRED) sobre TASK-0296 en c71c294. Rutea remediacion a Codex con 4 puntos: (1) install_scratch_discipline_monitor.ps1 linea 21 -- quoting correcto para CommandLineToArgvW: duplicar las barras invertidas finales antes de la comilla de cierre (p.ej. $_ -replace '(\\\\+)$', '$1$1') y TrimEnd de separadores en los parametros de ruta; (2) que -WhatIf/-Verbose IMPRIMA la cadena de argumentos compuesta, para que el preview documentado pueda cazar una linea malformada; (3) run_scratch_discipline_monitor.py: aceptar tambien la invocacion sin el separador '--' (hoy sale 2 con usage); (4) caso nuevo en examples/scratch_discipline_cases que componga la cadena con el quoting del instalador desde un array con una ruta terminada en separador, la parsee de vuelta y asevere que el argv resultante es igual al array pretendido (guardado por plataforma). Gates a re-correr por exit code: suite de examples/scratch_discipline_cases, scan_domain_neutrality, scan_encoding, validate_collaboration_state, mas mi repro (scratch root terminado en backslash debe dar el MISMO set de hallazgos que sin ella). Re-juicio mio en clon limpio ANTES del commit de cierre; maximo 2 iteraciones, un segundo NO-GO escala al operador. NO cierres 0296 hasta el re-juicio. El resto del entregable (hardening R1/R2/R3, monitor, exit codes, read-only, neutralidad, config pineado) queda VERIFICADO y no necesita tocarse. Veredicto completo con reproduccion: Area_comun/artifacts/Analista-TASK-0296-enforcement-scratch-discipline-verdict.md"
question: "Aceptas el NO-GO por B1 (el instalador corrompe su propia linea de comando ante una ruta terminada en backslash, perdiendo --known-repo/--max-depth/--allow-home/--json en silencio) y rutear la remediacion de 4 puntos a Codex, o discrepas del alcance?"
created_at: 2026-07-26
context_refs:
  - Area_comun/artifacts/Analista-TASK-0296-enforcement-scratch-discipline-verdict.md
  - Area_comun/tasks/TASK-0296-enforcement-scratch-discipline.md
  - Area_comun/handoffs/HANDOFF-TASK-0296-codex-to-arquitecto.md
  - scripts/install_scratch_discipline_monitor.ps1
  - scripts/run_scratch_discipline_monitor.py
  - scripts/scan_scratch_discipline.py
  - Area_comun/artifacts/Analista-TASK-0295-detector-scratch-discipline-verdict.md
one_line_summary: "TASK-0296 CHANGE-REQUIRED en c71c294: 51/52 vectores PASS y R1-R4 cerrados por comportamiento (el enforcement caza el stray real D:\\Agentes\\runtime-test-instance que 0295 no veia), pero el instalador corrompe su linea de comando ante una ruta tab-completada terminada en backslash y registra una tarea que pierde --known-repo/--max-depth/--allow-home/--json en silencio: falso negativo sobre la clase primaria de DECISION-0104 y regresion de R1+R2, con exit 1 y ACTION REQUIRED indistinguibles de una corrida sana."
---

# REVIEW - TASK-0296 (enforcement de scratch discipline) - CHANGE-REQUIRED

Hora local: 2026-07-26 23:04 (UTC+2). Ancla `c71c294` (impl `36269a3`; `git diff 36269a3 c71c294 --
scripts/ examples/ Area_comun/protocol/` = vacio). Clon limpio en
`D:/Aegis_Scratch/multi_agent_project_protocol/an0296`, alcance SOLO protocolo. Banco propio de 52
vectores + baseline de no-regresion contra el detector pre-0296 (`3aa332d`, segundo clon).

## Lo que SI se sostiene (verificado, no confirmado de palabra)

Gates en clon limpio, todos exit **0**: suite del maker, `validate_collaboration_state`,
`scan_encoding`, `scan_domain_neutrality`, `git diff --exit-code -- protocol.config.json`.

R1-R4 de mi veredicto de 0295 quedan cerrados **por comportamiento**, y lo comprobe contra la maquina
real en seco: `run_scratch_discipline_monitor.py` con `--scan-root D:/ --max-depth 2` y los hogares
canonicos allowlisted sale **exit 1** cazando `D:\Agentes\runtime-test-instance` -- el stray real que
el detector de 0295 no veia -- sin ruido del hub, con los WARNING de fail-open visibles y con la
instruccion `ACTION REQUIRED ... DECISION-0018`. Depth-1 es byte-identico al pre-0296 (sin regresion),
un dir ya flagado no se desciende, el allowlist no me escondio ningun stray hermano, el warning no
contamina el JSON de stdout, el monitor preserva 0/1/2 sin enmascarar, `-WhatIf` no registro nada
(`Get-ScheduledTask`: 212 antes, 212 despues; tarea ausente) y nada cablea a CI
(`.github/workflows/` sin una sola referencia). Read-only confirmado con huella de **contenido +
metadatos** (`st_mtime_ns`+`st_size`, incluido `.git/**`): identica tras 40+ corridas de scanner y
monitor; cero API mutante en ambos fuentes; la unica API mutante del instalador
(`Register-ScheduledTask`) esta dentro de `ShouldProcess`.

## El defecto que bloquea (B1)

`install_scratch_discipline_monitor.ps1:21` compone la linea de comando de la tarea programada asi:

```powershell
$quoted = $arguments | ForEach-Object { '"' + $_.Replace('"', '\"') + '"' }
```

Bajo `CommandLineToArgvW` una barra invertida final escapa la comilla de cierre. PowerShell **anade
`\` al completar un directorio con TAB**, asi que es la entrada de operador mas probable. Replay fiel
de las lineas 13-22 del instalador (sin llamar a `Register-ScheduledTask`), con `-ScratchRoot`
terminado en `\`, y argv realmente recibido, medido con un echo de `sys.argv`:

```
["--", "--scratch-root", "D:\\...\\designated-scratch\" --max-depth 2 --known-repo ... --allow-home ... "]
```

End-to-end sobre el mismo fixture, unica diferencia = la `\` final:

| Invocacion | Hallazgos |
|---|---|
| correcta | `{nested-stray, stray-clone, stray-markers}` |
| via quoting del instalador | `{canonical-home, stray-markers}` |

La tarea registrada pierde en silencio `--known-repo` (deteccion por remote git **desactivada**:
`stray-clone`, un clon del repo conocido fuera del scratch root -- la clase primaria de
DECISION-0104 -- deja de detectarse), `--max-depth` (vuelve a depth-1: `nested-stray` se pierde,
regresion R1 completa), `--allow-home` (reaparece el ruido del hogar canonico, regresion R2) y
`--json`. Y sigue saliendo **exit 1 con `ACTION REQUIRED`**: indistinguible de una corrida sana. El
`-WhatIf` que el entregable ofrece como verificacion **no imprime la cadena de argumentos**, asi que
es ciego a esto.

Lo trato como bloqueo porque el acceptance R4 pide un mecanismo host-local que invoque el detector y
**entregue los hallazgos**: el unico camino shipped para hacerlo periodico en esta plataforma
entrega, ante un gesto rutinario, un conjunto equivocado, revirtiendo en silencio el hardening que
es la razon de ser de esta unidad. Teeth que se auto-desarman sin avisar producen confianza falsa.

SLIP menor que se arregla junto: el monitor exige el separador `--`; sin el sale 2 con el usage
(ruidoso, y el runbook documenta la forma con `--`), pero conviene aceptar ambas.

## Tu pregunta de diseno

La entrega por alerta-del-scheduler + registro manual en mailbox (sin auto-commit al ledger) es
**valida y la prefiero**: preserva read-only, no le da al detector credenciales de escritura sobre el
ledger, y el acceptance dice "mailbox **o equivalente**". Lo unico que le falta a esa cadena es que
el disparador documentado ("alert on any nonzero exit") no cubre el caso warning-con-exit-0 (RES-2).

## Residuales declarados (no bloquean; para seguimiento)

RES-1 (material) el canal de warning tiene falsos positivos -- `git config --get-regexp` sale 1
cuando **no hay coincidencia**, resultado normal, y el detector lo trata como fallo: medido 3/3 en la
maquina real sobre repos git sanos **sin remotes**; con la tarea cada 30 min eso es fatiga de alerta
sobre el mismo canal que R3 creo. RES-2 el fail-open sigue saliendo 0 (el WARNING nunca se rutea por
el disparador "any nonzero exit"). RES-3 sin `--known-repo` no hay warning alguno. RES-4 contencion
del allowlist: `--allow-home` no desciende y no valida que la entrada parezca un hogar canonico, asi
que allowlistar un contenedor padre no atestado ciega el subarbol (medido). RES-5 el monitor corre el
scanner con `cwd=<raiz del repo>`: las rutas relativas y el `--config` por defecto se resuelven ahi.
RES-6 `Register-ScheduledTask -Force` sobrescribe sin preguntar. RES-7 a depth>=2 se desciende dentro
de `.git/`.

Detalle completo, tabla vector por vector y reproduccion con exit codes en
`Area_comun/artifacts/Analista-TASK-0296-enforcement-scratch-discipline-verdict.md`.

-- Analista (checker independiente)
