# REQ-ZEUS-001 — Mapa de backlog (gobernado en el HUB)

> Gobernanza en el hub (aporta al dataset hasta sellar N=500). Codigo de producto en `D:\Agentes\Zeus\Zeus-Aegis`.
> NOVA = instancia-plantilla del producto para empleados (coordination tier), NO donde se gobierna el build.
> Promocion de a una (DECISION-0020 #7). Decisiones D1-D5 = DECISION-0001..0005 en NOVA/Area_comun/decisions.

| WS | Hub task | Estado | Owner / Review | Depende de | Notas |
|----|----------|--------|----------------|-----------|-------|
| (D1-D5) | — | DONE | Arquitecto | — | DECISION-0001..0005 (NOVA). D4: hermes-agent = MIT (verificado). |
| WS1 inventario + plan branding | **TASK-0226** | ready->in_progress (GO enviado) | Codex / Analista | — | Documento en Zeus-Aegis/docs. Sin tocar codigo del fork. |
| WS5a alta Analista en NOVA + wrapper new_instance(4 agentes) | TASK-0227 (pend.) | por registrar | Codex / Analista | — (independiente) | Wrapper, NO toca el core. Restaura maker!=checker en NOVA. |
| WS3 capa de branding + alias env + pantalla "Preparando Zeus" | TASK-0228 (pend.) | por registrar | Codex / Analista | WS1 | Ejecuta el plan de WS1. |
| WS2 bootstrapper (gateway+backend+config+lifecycle Electron) | TASK-0229 (pend.) | por registrar | Codex / Analista | WS1 | Reusa autoStartGateway existente. hermes-agent MIT -> vendor permitido. |
| WS4 backend modelos (router frontera + peones) + bloqueo PII | TASK-0230 (pend.) | por registrar | Codex / Analista (seguridad) | D3 | Router LiteLLM-style + Ollama. Cero-PII externo. |
| WS6 integracion puente gobernanza desde UI (coordination) | TASK-0231 (pend.) | por registrar | Codex / Analista | WS3, D1 | F1 read-only ya existe; F2 sigue gateado post-N=500. |
| WS3.5 instalador electron-builder firmado | TASK-0232 (pend.) | por registrar | Codex (DevOps) / Analista | WS2, WS3 | Purga de 154 assets de terceros = gate de release. |
| WS7 verificacion e2e en VM limpia | TASK-0233 (pend.) | por registrar | Analista | todo | Checklist licencias (2 MIT) + cero hermes visible + cero PII. |
| WS10 runbooks instalacion/operacion | TASK-0234 (pend.) | por registrar | Arquitecto (Docs) | WS3.5 | — |

## Contribucion al dataset
- Faltan ~20 para N=500. WS1 + lote del panel (0222/0223/0225) cierran la ventana con desarrollo real.
- Al sellar 500: notificar al operador (STOP-RULE), congelar pre-registro v2.0. REQ-ZEUS continua post-ventana en el hub.

## Release publico (post-defensa)
- Export limpio (orphan, sin events.jsonl), purga de assets, scrub de config, 2 avisos MIT, copyright propio, lawyer review.
