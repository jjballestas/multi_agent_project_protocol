---
task_id: TASK-0178
title: "PENDIENTE (diseno): consola del Arquitecto en el front -- canal conversacional vivo Operador<->Arquitecto que activa el runtime del Arquitecto y transmite su trabajo/reporte (NO el mailbox)"
type: design
status: proposed
owner: Arquitecto
phase: P2
priority: normal
created_at: 2026-06-25
file: Area_comun/tasks/TASK-0178-arquitecto-consola-arquitecto-PENDIENTE.md
---

# TASK-0178 (PENDIENTE) - Consola del Arquitecto en el front

> Requisito del operador (2026-06-25): reemplazar VS Code por el front para coordinar al Arquitecto. NO disenar
> esta sesion -- queda como tarea pendiente para la proxima ventana (orden del operador).

> DISENO ENTREGADO (2026-07-27): ver `Area_comun/artifacts/DESIGN-0178-aegis-front.md`. REENCUADRADO tras
> debate + critica adversarial: el "canal conversacional que activa el runtime" se descarta; en su lugar el
> **Aegis Front** = panel soberano de 3 capas (L1 observacion / L2 asistente no-firmante / L3 firma humana
> consciente), app auto-provisionable, **open-core Apache** (motor+spec), **front-interno-primero** (operar
> instancias propias + gobernar la migracion T0 Access->SQL Server + medir -> dataset propio) con el aparato
> de mercado como fase posterior gateada. Foso = el corpus (no la certificacion, imposible por ISO 17065).
> CODIGO a construir en `Zeus-protocol` bajo `D:/Agentes/Zeus/`, nunca el hub. LISTO PARA CONSTRUIR. Status
> sigue `proposed`; se promueve al arrancar el desarrollo (proxima sesion: goal + revision adversarial del
> primer entregable).

## Que pide el operador
Una interface en el front para HABLAR con el Arquitecto en vivo, como en VS Code: el operador escribe, el
Arquitecto muestra lo que hace y reporta; al enviar un mensaje, el RUNTIME del Arquitecto se ACTIVA. **NO es el
mailbox** (async gobernado) ni la consola de prompts Q2 (operador->agente via mailbox_send): es un **canal
conversacional vivo Operador<->Arquitecto** con streaming del trabajo/reporte.

## Por que es una pieza de arquitectura (a disenar)
Hoy al Arquitecto lo dirige el operador desde VS Code; Codex/Analista los dirige un cron. "Hablarme desde el
front" exige un **puente de runtime del Arquitecto** (wrapper interactivo, como los crons pero en vivo) +
**streaming a la UI**. Conecta con la palanca diferida "front como supervisor siempre-activo". Merece DECISION +
SPEC propias (gobierno del proceso que lanza/dirige runtimes; limites; auditoria).

## Contexto mayor (futuro, NO esta sesion)
El operador describio la **fabrica multi-agente NOVA** (producto municipal/financiero, ~11 roles especializados:
Domain/PO, Legacy Analyst, Solution Architect, Database/Migration, Backend, Frontend UX, AI/MCP, Security, QA,
DevOps, Documentation). Modelo propuesto por el Arquitecto: gobernanza #4 LEAN (architect/implementer/reviewer
firman el ledger) + constructores especializados como agentes de PRODUCTO (clave producto, off-config, US-4), sin
una re-genesis por especialidad. Stack NOVA: VS2026 / .NET 10 ASP.NET Core / SQL Server 2025 / React+TS+Vite /
MCP / OIDC+JWT / Docker+CI/CD+OTel. La consola-del-Arquitecto es lo que el front debe estar listo para soportar.
