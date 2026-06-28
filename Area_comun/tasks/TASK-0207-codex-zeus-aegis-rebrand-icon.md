---
task_id: TASK-0207
title: "Zeus-Aegis: rebrand visible Hermes->Zeus-Aegis + icono propio (DECISION-0064)"
type: product
status: done
owner: Codex
phase: P2
priority: medium
created_at: 2026-06-28
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064]
file: Area_comun/tasks/TASK-0207-codex-zeus-aegis-rebrand-icon.md
---

# TASK-0207 — Zeus-Aegis: rebrand visible (Hermes→Zeus-Aegis) + icono propio

> GO en espera: NO arrancar hasta cerrar TASK-0206 — una a la vez (DECISION-0020 #7).

## Contexto
Al correr el fork hoy se ve marca **Hermes**: splash "HERMES-AGENT Workspace" + icono anime
(HermesWorld), onboarding "Hermes Workspace / Hermes Agent gateway", título de página, login,
mobile-setup, settings. El operador pidió: **(a)** icono propio Zeus-Aegis, **(b)** que la app
corriendo diga **Zeus-Aegis**, no Hermes. Hay ~180 ocurrencias de "Hermes" en `src`.

## Principio rector (CRÍTICO — leer antes de tocar nada)
Rebrand = **solo texto/branding de cara al usuario**. **NO** renombrar identificadores internos ni
la dependencia externa real, o se rompe la integración:
- **KEEP (no tocar):** env vars `HERMES_API_URL`, `HERMES_API_TOKEN`; el binario/CLI real `hermes`
  y sus comandos (`hermes gateway run`, `hermes --gateway`); nombres de headers/protocolo del
  gateway; nombre de paquete e import paths; claves de i18n. Renombrar esto es bug, no feature.
- **REBRAND (sí cambiar):** el **nombre de producto visible** → `Zeus-Aegis`. Splash/loading,
  `<title>` (use-page-title), onboarding (headings/wizard/steps/tour), login-screen,
  connection-startup/overlay, mobile-prompt (MobileSetupModal/MobilePromptTrigger), settings-dialog
  "about", welcome. Donde el texto visible sea "Hermes Agent Gateway", usar etiqueta neutra
  **"Agent Gateway"** (el binario sigue siendo `hermes`; no afirmar que es un gateway Zeus-Aegis si
  no lo es — honestidad de marca).

Nombre canónico de producto: **Zeus-Aegis** (subtítulo "Workspace" opcional donde el original lo usaba).

## Icono
- **Fuente del arte (ya provista por Arquitecto):** `personal/Arquitecto/zeus-aegis-brand/zeus-aegis-icon.svg`
  (en el repo del PROTOCOLO). Mark: tile redondeado oscuro + égida/escudo azul + rayo dorado.
  Paleta design-system (oro #e3b341, azul #58a6ff, fondo #0d1117). Es un **placeholder** — se puede
  refinar luego; ahora cablearlo.
- Cablear/rasterizar en `vendor/hermes-2.3.0/public/` reemplazando los slots de marca:
  `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`, `claude-icon-192.png`, `claude-icon-512.png`
  (los iconos del PWA manifest), `logo-icon.png`/`logo-icon.jpg`, el logo del splash, y las refs a
  `hermesworld-logo.svg`/`hermesworld-world.png`. Producir los PNG en los tamaños requeridos
  (favicon, 180 apple-touch, 192, 512) — método a discreción de Codex (sharp/resvg vía npx o script
  reproducible incluido).
- `public/manifest.json`: `name`/`short_name` → `Zeus-Aegis`; `icons[]` apuntando a los nuevos
  assets; theme/background acorde a la paleta.

## Fuera de alcance
No tocar `HERMES_API_*`, el binario `hermes` ni comandos del gateway; no rebrand de identificadores
internos; no F2/write-path; no tocar core del protocolo ni baseline TFM. dev script = TASK-0206.

## Criterios de aceptación
- **AC1 (texto visible):** corriendo el fork, splash, `<title>`, onboarding, login y mobile-setup
  dicen **Zeus-Aegis**; cero "Hermes" de cara al usuario en esas pantallas (las 4 capturas del
  operador en `personal/operador/Hermes/Images/` como referencia visual).
- **AC2 (icono):** favicon, app-tile/splash y los iconos del PWA manifest muestran el mark Zeus-Aegis;
  el icono anime ya no aparece.
- **AC3 (integración intacta):** `HERMES_API_URL`/`HERMES_API_TOKEN` siguen funcionando; el puente a
  submit_intent y la lectura del canónico siguen verdes; `pnpm governance:smoke` pasa; el gateway
  arranca igual.
- **AC4 (sin regresión):** `pnpm test` sin nuevos fallos respecto al baseline waivado.
- **AC5 (delta fork):** cambio documentado en SEAMS.md (qué strings/assets, regla KEEP vs REBRAND).
- **AC6 (honestidad):** no se renombró el binario/dependencia externa `hermes`; etiquetas de gateway
  neutras donde aplique.

## Definition of Done
AC1–AC6 verdes; handoff `in_review` a Arquitecto con evidencia: capturas (o salida) de las 4
pantallas mostrando Zeus-Aegis + icono nuevo, salida de `governance:smoke` y `test`, diff de assets/
manifest, nota SEAMS. Commit en Zeus-Aegis como Arquitecto con `Co-Authored-By: Codex`.
