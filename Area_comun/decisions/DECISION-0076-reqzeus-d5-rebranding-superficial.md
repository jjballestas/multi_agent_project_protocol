---
decision_id: DECISION-0076
title: "REQ-ZEUS D5 - Rebranding white-label superficial (UI/i18n/onboarding + alias env ZEUS_* con shim); sin renombrar binarios/appId (preserva merge upstream); purga de assets de terceros = gate de release aparte"
status: accepted
ratified_at: 2026-06-30
date: 2026-06-30
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [REQ-ZEUS-001, DECISION-0050, DECISION-0075]
scope: product
phase: P2
---

# DECISION-0076 (REQ-ZEUS D5) - Rebranding white-label superficial

> ACCEPTED (operador endoso OPS-115242Z + registro en hub, 2026-06-30). Canonicaliza la D5 de NOVA
> (`.../NOVA/Area_comun/decisions/DECISION-0005-D5-rebranding-superficial.md`).

## Decision
Rebranding **superficial** de Zeus-Aegis sobre el fork de Hermes:
- UI/strings/i18n + copy de onboarding -> "Zeus-Aegis".
- **Alias de variables de entorno visibles** `HERMES_API_URL`->`ZEUS_API_URL`, `HERMES_API_TOKEN`->`ZEUS_API_TOKEN`
  con **shim de compatibilidad** (mismo patron que los fallbacks `CLAUDE_*` existentes).
- **NO renombrar** binarios internos, `appId`, ni paquetes -> preserva la **mergeabilidad con upstream**.

## Restricciones de licencia/marca
- Conservar el aviso MIT de Hermes (NOTICE/LICENSE) en codigo y distribucion.
- El shim de rebrand **NO borra assets**: la purga de los 154 assets de terceros (hermesworld + logos NousResearch)
  es un **gate de release aparte** (build/CI falla si quedan en `dist/`).
- Declarar copyright/licencia propios del codigo del puente (governance-*) -> accion aditiva.

## Razon
Da identidad Zeus sin romper la mergeabilidad con Hermes (reuso, no reescritura) ni incurrir en deuda de mantenimiento.

## Consecuencias
- WS1 (branding) e inventario de "hermes" (TASK-0226 / ex TASK-ZEUS-0002) se ejecutan bajo esta postura; WS3
  (capa de branding + alias + pantalla "Preparando Zeus") la ejecuta.
