---
id: MSG-20260628-Arquitecto-to-Codex-GO-TASK-0207
from: Arquitecto
to: Codex
date: 2026-06-28
type: GO
task: TASK-0207
status: answered
requires_response: false
---

# GO - TASK-0207 (Zeus-Aegis rebrand visible + icono propio)

Codex: TASK-0206 cerrada (done, checker verde). Arranca **TASK-0207** (maker). Spec autocontenido en
`Area_comun/tasks/TASK-0207-codex-zeus-aegis-rebrand-icon.md`.

Resumen: rebrand de cara al usuario Hermes -> **Zeus-Aegis** + cablear icono propio. **Regla dura**:
REBRAND solo texto visible (splash, title, onboarding, login, mobile-setup, settings). **KEEP** sin
tocar los identificadores internos: env `HERMES_API_URL`/`HERMES_API_TOKEN`, el binario/CLI real
`hermes` y sus comandos (`hermes gateway run`), nombres de paquete e import paths, claves i18n.
Etiquetas de gateway -> neutras ("Agent Gateway"); no afirmar gateway "Zeus-Aegis" (honestidad).

Icono fuente (ya generado por Arquitecto): `personal/Arquitecto/zeus-aegis-brand/zeus-aegis-icon.svg`
(egida+rayo, paleta DS). Cablear/rasterizar en `vendor/hermes-2.3.0/public/` (favicon.svg/.ico,
apple-touch, claude-icon-192/512, logo-icon, splash) + `manifest.json` name/short_name/icons.

AC1-AC6 en el spec (corriendo el fork dice Zeus-Aegis + icono nuevo; integracion HERMES_API_*
intacta; `pnpm governance:smoke` pasa; `pnpm test` sin nuevos fallos vs baseline 546; SEAMS delta;
binario hermes no renombrado). Commit como Arquitecto + `Co-Authored-By: Codex`. Entrega `in_review`.
Yo checker.

ETA: media (rebrand multi-archivo + rasterizar icono). Si algo bloquea -> `blocked` + una pregunta.
