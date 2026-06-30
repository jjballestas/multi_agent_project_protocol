# REPORTE DE SELLO — Dataset TFM N=500

- Fecha/hora (UTC): 2026-06-30T00:53Z (sello) · redactado 2026-06-30T01:0xZ
- Autor: Arquitecto · Ratifica: Operador (John Ballestas)
- Estado: **VENTANA CERRADA — corpus sellado en N=500**

## 1. Resumen
El dataset del TFM alcanzó **500 eventos elegibles** y se disparó el `STOP-RULE`. La generación de
eventos quedó **pausada** en el momento exacto de los 500 (aterrizaje exacto, sin overshoot). El corpus
medido es inmutable y queda anclado a un commit y un tag.

## 2. Desglose por agente (firmantes)
| Agente | Eventos elegibles | % |
|---|---|---|
| Arquitecto | 253 | 50.6% |
| Codex | 195 | 39.0% |
| Analista | 52 | 10.4% |
| **Total** | **500 / 500** | 100% |

## 3. Ancla canónica (inmutable)
| Item | Valor |
|---|---|
| Commit del corpus | `e3646ae01fff1f59a5d7882bfd7c8d744ff1c5f9` |
| Tag inmutable | `TFM-dataset-N500` (pusheado a origin) |
| Ledger | `runtime/state/events.jsonl` |
| protocol.config.json (pineado) | sha256 `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354` |

## 4. Criterio de elegibilidad (pre-registrado)
Un evento cuenta al corpus si y solo si: `seq >= 2221` (DATASET_START_SEQ, post-baseline) **y**
`type == "intent.applied"` **y** `actor_auth.method == "ed25519"` (firma per-evento del actor).
Los 500 medidos cumplen los tres al 100% (0 eventos no-firmados dentro de la ventana).

## 5. Doble corroboración del cierre (independiente)
1. Conteo del Arquitecto sobre `events.jsonl`: 500/500 (desglose arriba).
2. Monitor canónico `personal/Arquitecto/monitor_dataset_ed25519.py`:
   "STOP-RULE: 500 eventos elegibles (>=500) desde seq 2221, 3 agentes {Arquitecto: 253, Codex: 195, Analista: 52}. CERRAR VENTANA (no mirar H1-H3 antes)."

Ambos conteos coinciden exactamente.

## 6. Gates en el punto de sello
`validate_collaboration_state.py` exit 0 · `scan_encoding.py` exit 0 · drift 0 · 5 pineados byte-identicos.

## 7. Integridad del pre-registro
- **H1-H3 permanecen CIEGOS** hasta que el Operador congele formalmente el pre-registro v2.0.
- Acción pendiente del Operador: declarar congelado el pre-registro v2.0 (las hipotesis se miden contra
  este corpus de 500 anclado en `TFM-dataset-N500`).

## 8. Estado post-sello (fuera del corpus medido)
A partir de aqui, los eventos nuevos son POST-ventana (no cuentan al corpus). REQ-ZEUS-001 continua su
desarrollo gobernado en el hub. Pendientes inmediatos:
- TASK-0226 (REQ-ZEUS WS1): `changes_requested` — NO-GO del Analista (veredicto en
  `Area_comun/artifacts/ANALISTA-TASK-0226-ws1-branding-veredicto.md`); requiere remediacion de Codex.
- TASK-0225 (Arquitecto-cron): `in_review`.
- TASK-0224 (fix redactor): `review_approved`.

## 9. Trazabilidad
Trayectoria de la sesion: 439 -> 500 (+61) con desarrollo real (Engram, lote del panel, REQ-ZEUS WS1,
ciclos maker!=checker, higiene gobernada). Cierre controlado final: +4 via higiene de mensajes consumidos.
