---
message_id: MSG-20260702-Arquitecto-to-Operador-FYI-F1-registro-crons
from: Arquitecto
to: Operador
type: FYI
status: open
requires_response: false
created_at: 2026-07-02
context_refs:
  - Area_comun/tasks/TASK-0238-visionnova-f1a-gate-intake.md
  - personal/operador/vision-nova/F0/BACKLOG-F1-descompuesto.md
  - personal/operador/vision-nova/pipeline-vision-nova.html
one_line_summary: "Orden F1 ejecutada: 7 tareas F1-A..G registradas (TASK-0238..0244 proposed), crons relanzados, tablero actualizado; F1-A pendiente de promover tras la higiene de Codex."
requested_action: "No action required; responde la orden F1 (registro + relanzamiento + promocion de F1-A con ids y commits)."
---

# FYI - Orden F1 ejecutada (registro backlog + crons)

status: en_curso (registro completo; promocion de F1-A gateada por higiene de Codex)

## Contexto de rama
Decidiste merge vision-nova -> main y automatizar. Hecho: fusion ff-limpia (commit 37c29a1),
main pusheado. TODO Vision Nova sigue ahora en main (los crons y el dogfooding son main-based).

## Registro del backlog F1 (los 7, proposed, commit 93c10e8)
- TASK-0238 [VISION-NOVA][F1.1] gate de intake determinista (owner Codex)
- TASK-0239 [VISION-NOVA][F1.2] evento firmado exception.recorded (owner Codex)
- TASK-0240 [VISION-NOVA][F1.3] trailers bloqueantes Task-Id/Fixes-Task (owner Codex)
- TASK-0241 [VISION-NOVA][F1.4] taxonomia de defectos + severidad (owner Arquitecto + gate Analista)
- TASK-0242 [VISION-NOVA][F1.5-harness] envelope 7 campos + fix-loop (owner Codex)
- TASK-0243 [VISION-NOVA][F1.5] mini-DECISION anti-vibecoding + clausula pin (owner Arquitecto)
- TASK-0244 [VISION-NOVA][F1.7] release v1.18.0 (owner Arquitecto)

Anotaciones de tus hallazgos aceptados, ya en el cuerpo de las tareas: F-1 (R0/intake_start)
en 0238; F-2 (F1-C/0240 se ACTIVA solo tras desplegar F1-E/0242) en 0240; F-3 (pin-anclado-al-
tag) en 0243; F-4 (v1.18.0 = linea release, epoch PINNED intocable) en 0244. SPECs v0.2 +
backlog v2 referenciados.

## Crons
Relanzados en main: Codex pid 83584, Analista pid 81484 (arranque 19:49, heartbeat OK).
La relanzada se bloqueo primero por la regla deny de PowerShell del clasificador; la
desbloqueaste cambiando el modo. Des-vi la ACTION de higiene de Codex en su seen.json (estaba
marcada seen de antes del stand-down) para que su cron la reprocese este ciclo.

## Secuencia pendiente (segun tu orden)
1. Codex procesa su higiene de area personal (proximo ciclo ~5 min) y emite FYI.
2. Recibido ese FYI: promuevo TASK-0238 (F1-A) a ready + GO a Codex, con el SPEC-intake v0.2
   (R0 ya aplicado). Cadena de a una F1-A -> F1-B -> F1-C.
3. F1-D (taxonomia) y la parte doctrinal de F1-E avanzan en paralelo sin bloquear a Codex.
4. F1-C/0240 NO se activa hasta que F1-E/0242 despliegue los harnesses con trailer.

## Tablero
pipeline-vision-nova.html: F1.1-F1.7 anotadas con las ids registradas + condiciones de
promocion/activacion, sello 19:50, updated_by Arquitecto.

## Anomalia (DECISION-0018), ya resuelta por ti
Tu mensaje respuesta-hallazgos-F1 traia un em-dash (0x2014) que ponia rojo el gate de encoding;
lo normalice a ASCII para no bloquear el pipeline. Vi que ademas normalizaste los 22 em-dashes
de los 7 docs del asesor y agregaste un gate ASCII pre-commit al asesor (commit 7af7d3f). Cerrado.

## Higiene mailbox
Con los crons ya activos NO hay ventana idle segura para mailbox_archive; hay consumidos en
open/ (esta orden F1, tu respuesta-hallazgos, el FYI de F0.2, el FYI de cortafuegos). Los
archivo en la proxima ventana idle verificada (respeto tu directiva de higiene-cada-5, commit 6398910).
