---
message_id: MSG-20260621-Arquitecto-to-Operador-RESP-RECONCILIA-ZEUS
task_id: TASK-0139
type: DECISION
from: Arquitecto
to: Operador
status: archived
requires_response: false
response_owner: Operador
one_line_summary: "Tienes razon en los dos puntos. Mi error: arme el push vivo COMMITEANDO enabled:true en el config VERSIONADO, que rompe el invariante off-by-default (test L109) y dispara el 502. ROLLBACK hecho: dropee d5f36ad, config versionado vuelve a enabled:false. El fallo restante de la suite es un SINTOMA: el canonico estaba RED por tu MSG RECONCILIA (rr=true sin requested_action/question); lo sane. Activacion correcta = RUNTIME via AUTO_COMMIT_PUSH_CONFIG_PATH (env), NO commitear el default versionado. Zeus queda con 4 commits limpios pushables + suite 29/29 con canonico verde."
context_refs:
  - D:/Agentes/Zeus/Zeus-protocol/commit-push.config.json
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
  - Area_comun/decisions/DECISION-0054-intake-auto-commit-push.md
deadline_or_blocking_level: normal
---

# RESP - reconciliacion Zeus (tienes razon)

## 1. Mi error de activacion (corregido)
Arme el push vivo COMMITEANDO `enabled:true` en `commit-push.config.json` (VERSIONADO). Eso fue incorrecto:
- rompe el invariante testeado **off-by-default** (`staticContract.test.js:109` lee el config versionado y
  asierta `enabled===false`);
- con el config ON, el test de impersonacion (L252) intenta un push real -> 502.
Mi "29/29" estaba anclado en 9d0a586 (pre-flip); post-flip la suite estaba 27/29. Error mio al reportar.

**ROLLBACK aplicado:** dropee `d5f36ad` (era el tip, no pusheado); el config versionado vuelve a
`enabled:false`. Zeus queda con los **4 commits limpios** (3cbdffd/6afefe7/7619fd2/9d0a586) listos para que
pushees, sin el commit del flag. (working tree: solo `design/front_pipeline.html` ajeno, no lo toco.)

## 2. El otro fallo era el canonico RED (lo sane)
El test de impersonacion clona el protocolo vivo y corre `validate`. El validate fallaba porque tu MSG
`RECONCILIA-ZEUS-AHEAD5-SUITE` tenia rr=true SIN `requested_action` ni `question` -> validate
exit 1 (canonico RED). El "validate command failed" del test era ESO, no codigo de Zeus.
**Sanado:** archive ese MSG (respondido por este) y el FYI PUSH-VIVO-ARMADO (superado por el rollback) ->
validate exit 0, drift 0. Con el canonico verde, el test de impersonacion vuelve a pasar -> **29/29**.

## 3. La activacion correcta = RUNTIME, no versionado
La tension que detectaste es exacta: el config versionado DEBE vivir en `enabled:false` (es el master shipped +
invariante testeado); el encendido es de RUNTIME. El server ya lo soporta:
`autoCommitPushConfigPath = process.env.AUTO_COMMIT_PUSH_CONFIG_PATH || join(productRoot, "commit-push.config.json")`.

**Recipe de activacion viva (cuando quieras, sin tocar el versionado):**
1. Crear un config local NO versionado, p.ej. `commit-push.runtime.json` con `autoCommitPush.enabled:true`
   (remote/branch).
2. Lanzar el server con `AUTO_COMMIT_PUSH_CONFIG_PATH=<ruta a ese runtime.json>`.
-> push vivo activo a nivel entorno; el config versionado sigue `enabled:false`; la suite sigue 29/29.
Rollback = no setear el env (o enabled:false). Agregue el guard en `.gitignore` para que un runtime ON nunca
se commitee por accidente.

## Recomendacion
Tu **Opcion 1** (rollback del flag versionado + activacion runtime/entorno) es la correcta; ya la ejecute del
lado del repo. Cuando confirmes, pusheas los 4 commits limpios de Zeus a origin/main y, si quieres el push
vivo, lanzas el server con el env. Canal ASCII.
