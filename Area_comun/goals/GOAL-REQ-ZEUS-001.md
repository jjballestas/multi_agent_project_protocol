# GOAL-REQ-ZEUS-001 — Productizacion de Zeus-Aegis + metodologia con 4 firmantes

- Estado: active
- Fecha alta: 2026-06-30
- Origen: REQ-ZEUS-001 (D:\Agentes\Ingenas\Budget\02_Analysis\Arquitectura\REQUERIMIENTO_Zeus-Aegis_Productizacion_y_Metodologia.md)
- Gobernado en: HUB (multi_agent_project_protocol). Codigo de producto: D:\Agentes\Zeus\Zeus-Aegis. Instancia-plantilla: NOVA.
- Owner orquestador: Arquitecto · Maker: Codex · Checker: Analista · Aprueba: Operador.
- Decisiones base: DECISION-0001..0005 (NOVA) = D1 tiered / D2 una-por-proyecto / D3 hibrido / D4 hermes-agent MIT / D5 rebrand superficial.

## DoD del goal
Maquina limpia -> instalador unico Zeus -> workspace funcional sin "hermes" visible; gateway+backend auto-provistos;
4 firmantes + maker!=checker operativos; licencias respetadas (2 avisos MIT); cero secretos/PII; TFM intacto;
verificacion e2e con evidencia.

## Modo de ejecucion
- **Autonomia: 24/7 headless** via Arquitecto-cron (TASK-0225) — habilitador, en construccion.
- **Rieles permanentes:** (1) push a main cuando verde [operador ON]; (2) pausar+avisar en N=500 [invariante];
  (3) NO activar #4/F2/Engram/re-genesis sin GO operador [invariante]; (4) NO tocar los 5 pineados [invariante].
- Promocion de tareas **de a una** (DECISION-0020 #7). Narracion minima (DECISION-0038).

## Backlog -> tareas del hub (ver personal/Arquitecto/REQZEUS-backlog-map.md)
- WS1 inventario+plan branding = **TASK-0226** (in_progress, Codex).
- Habilitador 24/7 = **TASK-0225** (Arquitecto-cron) — PRIORIZADO.
- WS5a alta-Analista-NOVA, WS3 branding, WS2 bootstrapper, WS4 backend, WS6 puente UI, WS3.5 instalador, WS7 e2e, WS10 runbooks = por registrar al despejar deps.

## Relacion con el dataset
Aporta al dataset hasta sellar N=500 (faltan ~20). Al sellar: congelar pre-registro v2.0; el goal continua post-ventana.
