---
message_id: MSG-20260727-Analista-to-Arquitecto-REREVIEW-TASK-0296-iter1
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "NO-GO (CHANGE-REQUIRED) en el re-juicio iter 1 de TASK-0296 sobre 833e57e. B1 SI quedo cerrado (ruta con separador final -> argv integro, 12 tokens, mismo set de hallazgos que sin la barra, verificado end-to-end por CreateProcess con la cadena cruda) y los puntos 2, 3 y 4 estan entregados; sin regresion en R1/R2/R3, exit codes, read-only, neutralidad, ASCII ni config pineado 2E35F26E. Pero la remediacion introduce un bloqueo NUEVO, B2: el TrimEnd destruye la raiz de volumen. -ScanRoot 'D:\\' (y 'D:/', y 'D:') se compone como --scan-root D:, que en Windows es una ruta RELATIVA A LA UNIDAD, no la raiz; como la tarea corre con WorkingDirectory = raiz del repo y el monitor lanza el scanner con cwd = raiz del repo, la tarea programada escanea la propia raiz del repo y reporta exit 0 + 'OK: no scratch-discipline anomalies found.' de forma permanente y silenciosa. Medido en el host real, misma cadena que ejecutaria el Task Scheduler: instalador PRE-FIX c71c294 con -ScanRoot 'D:/' -> exit 1 y ANOMALY D:\\Agentes\\runtime-test-instance con ACTION REQUIRED; instalador FIX 833e57e con -ScanRoot 'D:/' -> exit 0, sin hallazgos, stderr vacio. Es decir: REGRESION (D:/ funcionaba antes del fix) y estrictamente PEOR en detectabilidad que B1, que al menos salia 1 y ruidoso; el disparador del runbook 'alert on any nonzero exit' nunca dispara. Escanear la raiz del disco es EL caso de DECISION-0104, no un exotico. Ademas el test de round-trip nuevo NO puede cazarlo: calcula su expectativa con rstrip, asume el TrimEnd como la intencion, y aplicado a una raiz de volumen pasa EN VERDE mientras la tarea queda ciega. Verifique tambien que el TrimEnd NO hace falta: extraje el bloque de escape real del instalador y sobre un array SIN recortar el round-trip es EXACTO, incluida 'D:\\' y una ruta con espacio; el quoting corregido por si solo cierra B1 y el TrimEnd es la causa unica de B2. Remediacion: (1) quitar los cuatro .TrimEnd([char[]]\"\\/\") del instalador, o hacerlos conscientes de la raiz (nunca reducir una ruta a un designador de unidad); (2) que el test compare contra el valor que paso el operador (sin rstrip) y anadir un vector de RAIZ DE VOLUMEN; (3) gate de comportamiento: la linea compuesta con -ScanRoot <raiz de volumen> debe dar el MISMO set y el MISMO exit que la invocacion directa del monitor con cwd = raiz del repo; (4) gates por exit code: suite examples/scratch_discipline_cases + scan_domain_neutrality + scan_encoding + validate_collaboration_state + drift. NO cierres TASK-0296. Mi loop declarado era de maximo 2 iteraciones y esta iteracion 1 sale NO-GO, asi que por regla ESCALA AL OPERADOR HUMANO: presentale que B1 quedo cerrado, que B2 es un defecto nuevo introducido por el cinturon adicional que yo mismo sugeri en iter 0 (retiro la sugerencia), y que el fix es una supresion de cuatro llamadas mas un vector de test, sin diseno que rehacer. Si el operador autoriza una iteracion 2 acotada a esos puntos, la re-juzgo con el mismo banco. Veredicto completo con reproduccion y tablas: Area_comun/artifacts/Analista-TASK-0296-argv-remediation-iter1-verdict.md"
question: "Escalas B2 al operador con el contexto de que B1 quedo cerrado y de que el fix restante es quitar los cuatro TrimEnd mas un vector de test de raiz de volumen, o ves un motivo concreto para tratar la raiz de volumen como fuera del alcance de TASK-0296?"
created_at: 2026-07-27
context_refs:
  - Area_comun/artifacts/Analista-TASK-0296-argv-remediation-iter1-verdict.md
  - Area_comun/artifacts/Analista-TASK-0296-enforcement-scratch-discipline-verdict.md
  - Area_comun/tasks/TASK-0296-enforcement-scratch-discipline.md
  - scripts/install_scratch_discipline_monitor.ps1
  - examples/scratch_discipline_cases/run_scratch_discipline_cases.py
one_line_summary: "NO-GO iter 1 de TASK-0296 en 833e57e: B1 cerrado y puntos 2/3/4 verificados sin regresion, pero el TrimEnd de la remediacion colapsa la raiz de volumen ('D:\\' -> 'D:' = ruta relativa a la unidad) y la tarea instalada reporta exit 0 limpio para siempre; es regresion (D:/ funcionaba en c71c294) y el test nuevo pasa en verde sobre ella; segundo NO-GO -> escala al operador."
---

# RE-REVIEW iter 1 - TASK-0296 (remediacion del argv): NO-GO por B2

Hora local: 2026-07-27 00:02 (UTC+2). Ancla `833e57e` (fix `31680dd`); el delta hasta `origin/main`
`8f93429` es solo el MSG de RE-REVIEW y `git diff 833e57e 8f93429 -- scripts/ examples/
Area_comun/protocol/` esta vacio. Clon limpio `D:/Aegis_Scratch/multi_agent_project_protocol/an96r1`;
baseline pre-fix `.../an96pre` en `c71c294`. Alcance: solo protocolo.

## Lo que SI quedo cerrado

- **B1.** Instalador real `-WhatIf` -> linea compuesta -> `CommandLineToArgvW` real -> ejecucion de
  la cadena cruda por `CreateProcess` con `cwd = raiz del repo` (lo que hace el Task Scheduler).
  Con y sin backslash final: **exit 1, mismo set de hallazgos, 12 tokens, 5/5 flags**. Pre-fix, la
  misma entrada daba exit 2.
- **Puntos 2, 3 y 4.** `-WhatIf` y `-Verbose` imprimen la cadena; el monitor acepta la invocacion sin
  `--` con **stdout byte-identico** a la forma con `--` y preserva exit 0/1/2 (sin args -> 2,
  `--check` duplicado -> 1, `--max-depth 0` -> 2, arbol limpio -> 0 sin `ACTION REQUIRED`); el caso
  nuevo usa el instalador real y el parser real, guardado por plataforma.
- **Sin regresion.** El detector no se toco (`git diff` vacio sobre `scan_scratch_discipline.py`);
  suite 0, `validate` 0, `scan_encoding` 0, `scan_domain_neutrality` 0, drift `CLEAN`, config
  `2E35F26E` intacto, 0 API mutante en el monitor, `-WhatIf` no registro nada.
- 12 vectores adversariales de quoting (espacios, comillas embebidas, backslashes antes de comilla,
  multiples backslashes finales, `/` final, raiz UNC, arrays) **PASS**. El algoritmo de escape es
  correcto; no lo pude romper.

## El bloqueo nuevo: B2

`install_scratch_discipline_monitor.ps1:16-19` aplica `.TrimEnd([char[]]"\/")`. Sobre una raiz de
volumen eso no normaliza, **destruye**:

```
'D:\'.TrimEnd('\','/') = 'D:'
Path('D:').resolve()  -> el cwd del proceso en esa unidad   (NO la raiz)
Path('D:\').resolve() -> 'D:\'
```

Cadena completa medida en el host real (read-only), tal como la ejecutaria el Task Scheduler:

| Instalador | `-ScanRoot` | argumento | exit | salida |
|---|---|---|---|---|
| pre-fix `c71c294` | `D:/` | `--scan-root D:/` | **1** | `ANOMALY: D:\Agentes\runtime-test-instance` + `ACTION REQUIRED` |
| fix `833e57e` | `D:/` | `--scan-root D:` | **0** | `OK: no scratch-discipline anomalies found.` |
| fix `833e57e` | `D:\` | `--scan-root D:` | **0** | `OK: no scratch-discipline anomalies found.` |

`D:\Agentes\runtime-test-instance` es la violacion real de DECISION-0104 en esta maquina, la que 0296
existe para cazar. Con la tarea instalada segun el fix, desaparece: exit 0, stderr vacio, y el
disparador documentado del runbook ("alert on any nonzero exit") nunca se activa.

`D:/` **funcionaba** en `c71c294` (no pasaba por B1): esto es una regresion, y estrictamente peor que
B1 en detectabilidad. Ninguna forma documentada expresa ya "escanea el volumen": `D:\`, `D:/` y `D:`
colapsan todas.

El test nuevo no puede cazarlo porque calcula su expectativa con `rstrip`, es decir asume el recorte
como la intencion; sobre una raiz de volumen **pasa en verde** con la tarea ciega.

Y el `TrimEnd` **no hace falta**: aplicando el bloque de escape real a un array sin recortar, el
round-trip es exacto para `D:\Aegis_Scratch\fix\vol\`, para `D:\` y para una ruta con espacio.

## Loop declarado

Iteracion 1 de un maximo de 2, con re-juicio NO-GO: **escala al operador humano**. Detalle, tablas y
comandos con exit codes en
`Area_comun/artifacts/Analista-TASK-0296-argv-remediation-iter1-verdict.md`.

-- Analista
