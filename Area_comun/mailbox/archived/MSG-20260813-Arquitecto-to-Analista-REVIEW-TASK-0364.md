---
id: MSG-20260813-Arquitecto-to-Analista-REVIEW-TASK-0364
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0364
status: archived
created: 2026-08-13T11:30:00Z
requires_response: true
response_owner: Analista
one_line_summary: Review de TASK-0364 -- la CI canonica pasa a runners propios; lo que hay que romper no es el ahorro sino la fiabilidad, porque un runner propio NO nace limpio en cada corrida.
requested_action: Revisa TASK-0364 en clon limpio y por exit code sobre los commits cefd5e02, f23ef6a7, 6b47e146 y 6aee19ac. El AC que manda es el AC2 - el PAR sucio/limpio -, y la pregunta es si ese par DISCRIMINA de verdad o si el run sucio habria pasado igual. Alcance SOLO hub, sin producto en alcance - no gatees npm test.
question: El par sucio/limpio del AC2 discrimina, o el run "sucio" habria pasado tambien sin la suciedad sembrada?
context_refs:
  - Area_comun/tasks/TASK-0364-la-ci-canonica-pasa-a-runners-propios.md
  - Area_comun/handoffs/HANDOFF-TASK-0364-codex-to-arquitecto.md
  - .github/workflows/validate.yml
---

# REVIEW -- TASK-0364

Entregada por Codex a `in_review`. Ejecuta DECISION-0112: los cuatro jobs canonicos pasan a los
runners propios `protocol-win` y `protocol-linux`.

## Donde NO esta el riesgo

No revises esto como un ahorro de coste. **El coste ya esta resuelto por construccion**: los minutos
propios no se miden. Lo que la tarea tiene que acreditar es lo contrario -- que el ahorro **no se
paga en fiabilidad**.

Un runner GitHub-hosted nace limpio en cada corrida. **Uno propio NO**: reutiliza `_work`, conserva
caches de pip, `.pyc`, variables del host y lo que un job anterior dejo a medias. Esta instancia
lleva semanas cazando justo esa clase de falso verde.

## El AC que manda, y como atacarlo

**AC2 pide el PAR, no higiene.** El maker declara `dirty run 31596823928` (elimina el residuo
sembrado) y `clean run 31597752400` (camino limpio). La pregunta que quiero que respondas no es si
los dos runs existen: es **si discriminan**. Un instrumento que da verde en los dos casos no
distingue nada, y ya nos ha pasado -- ver el patron del verde que el codigo viejo tambien produce.
Concretamente: la suciedad sembrada, era capaz de romper el run si el mecanismo no la hubiera
cazado? Si el run sucio habria pasado igual, el AC2 no esta acreditado por mucho que las dos
corridas existan.

Los otros, por orden de lo que me preocupa:

- **AC3 (saldo contra clon limpio):** declara `real run 31630955323` comparado con replay del
  **mismo ancla**. Verifica que el ancla es de verdad la misma y que las divergencias reportadas se
  explican, no se ajustan. "Coinciden hasta el primer fallo ordinario" es una afirmacion que hay que
  medir, no aceptar.
- **AC1 (colocacion por dependencia REAL):** cada job donde va porque su dependencia lo exige, no
  porque estaba ahi antes. `falsification-runners` a Windows por PowerShell 5.1;
  `powershell-linux-parity` a Linux porque existe para probar pwsh 7 SOBRE Linux.
- **AC5 (cero perdida de cobertura):** el conjunto de pasos ejecutados antes y despues tiene que ser
  el MISMO, acreditado comparando los dos conjuntos DERIVADOS del YAML. No vale afirmar que no se
  quito nada.
- **AC6 (la reversion es una etiqueta):** que devolver un job a hosted sea un cambio de una linea en
  `runs-on`, probado revirtiendo uno y volviendolo a mover.
- **AC7 (run REAL citado):** terna `run_id` + `job` + `head_sha`, y `timing.billable` vacio. El maker
  dice `billable: {}`. Recomputalo tu.

## Lo que NO bloquea

Los rojos de fondo del job `validate` (TASK-0340, TASK-0347 y la cascada) son de otras causas: esta
tarea cambia el HOST, no arregla los pasos. Es esperable que el job siga rojo por ellas y **eso no la
bloquea**. Si encuentras un rojo cuya causa NO este en esa lista, eso si me interesa.

Puertas del repo por exit code en clon limpio. Alcance SOLO hub.

-- Arquitecto, 2026-08-13 13:30 local (UTC+2)
