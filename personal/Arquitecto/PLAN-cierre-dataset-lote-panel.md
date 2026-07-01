> **>>> SUPERADO (2026-07-02) — NO USAR.** El dataset esta SELLADO en N=500 (tag `TFM-dataset-N500` -> e3646ae);
> este plan de "cerrar 61 eventos" quedo obsoleto al alcanzar el sello. Se conserva solo como historico.
> El foco vigente es REQ-ZEUS-001 (ver `personal/Arquitecto/PLAN-REQ-ZEUS-001-reconciliado.md` + `DECISION-0077`).

# PLAN — Cerrar dataset (61 eventos) vía "lote pendientes del panel"

> Draft del Arquitecto. NO escribe ledger todavía. Espera GO del operador.
> Estado verificado 2026-06-29: dataset **439/500 (faltan 61)** — Arquitecto 218 · Codex 177 · **Analista 44**.
> Crons VIVOS y ociosos: Analista pid 57700, Codex pid 56748 (`processable_messages=0`).
> Filtro dataset canónico: `seq>=2221 ∧ type=intent.applied ∧ actor_auth.method=ed25519`.

## Objetivo
Generar ~61 turnos gobernados **reales** (no relleno), **balanceando hacia el Analista** (44),
y dejar que `monitor_dataset_ed25519.py` aplique el STOP-RULE en el evento #500. No mirar H1–H3.

## Mecánica
Cada tarea recorre su ciclo completo → eventos por los 3 firmantes:
`claim(acquire)` → `task_upsert` → `task_status:in_progress` → GO mailbox → Codex implementa
(`claim`/`task_status`) → GO review → **Analista cron** revisa (`claim`/`task_status`/`mailbox_archive`)
→ remediation si NO-GO → `task_status:in_review`→`done` → `claim(release)`.
Rendimiento estimado: ~8–15 eventos/tarea con gate adversarial. 4 tareas ≈ 40–60 eventos.

## Las 4 tareas del lote (specs propuestas — VALIDAR)

### T1 — Zeus-Aegis: vista Estadísticas (stats) completa
- **Owner build:** Codex · **Review:** Analista
- **Scope:** `Zeus-Aegis` panel — pulir `/api/governance/agent-metrics` + vista; añadir
  chip de progreso del dataset (X/500) y costo de tokens real por agente.
- **DoD:** render verde en clon limpio; sin escritura al ledger (F1 read-only); gate Analista GO.

### T2 — Zeus-Aegis: vista "Instanciar proyecto" (read-only)
- **Owner build:** Codex · **Review:** Analista
- **Scope:** vista que muestra el flujo de instanciación atestada (DECISION-0069) en modo
  preparar-comando (genera JSON/cmd, NO ejecuta — F2 sigue gateado).
- **DoD:** read-only; respeta waiver F1; gate Analista GO.

### T3 — Fix redactor de reportes (fechas + hora + dataset)
- **Owner build:** Codex · **Review:** Arquitecto + Analista
- **Scope:** `scripts/generate_human_guide.py` (y/o redactor de reportes): corregir bug de
  fechas; **todo reporte lleva SIEMPRE hora (updated) + estado dataset recontado X/500**.
- **DoD:** reporte de muestra con hora+dataset correctos; gate.

### T4 — Construir + activar Arquitecto-cron
- **Owner build:** Codex · **Review:** Analista
- **Scope:** `personal/Arquitecto/arquitecto_cron.ps1` análogo a los existentes (procesa
  mailbox→Arquitecto). NOTA: el lanzamiento real (.ps1) lo hace el operador (deny-rule harness).
- **DoD:** script presente + runbook de arranque; gate Analista.

## Backlog `ready` legítimo a cerrar por su dueño (NO unilateral)
Vía sus crons, el Analista cierra formalmente sus reviews ya hechos pero no formalizados en ledger:
TASK-0194, 0199, 0201, 0203, 0211, 0215, 0219, 0220, 0221. (Drift trabajo↔lifecycle, DECISION-0018.)
Esto solo: ~9 cierres × varios eventos = puede acercar mucho a 61 **y** sube al Analista.

## Orden de ejecución (al recibir GO)
1. Claim Arquitecto sobre rutas de registro (atómico).
2. `submit_intent --intents` (1 transacción): `task_upsert` T1–T4 + `task_status:ready`.
3. Enqueue GOs (mailbox + intent) a Codex (T1–T4) y a Analista (reviews + cierre backlog).
4. Los crons vivos consumen → eventos. Monitor vigila STOP-RULE.
5. Al llegar a 500: cierre de ventana, reporte humano, NO mirar H1–H3 hasta congelar.

## Riesgos / guardas
- Ledger append-only atestado: ejecutar como **una** transacción atómica con rollback.
- Anti-colisión DECISION-0020: drafts aquí primero; escribir en ventana segura (sin claim del peer).
- Integridad TFM: solo trabajo real; el STOP-RULE corta en 500; H1–H3 ciego hasta el cierre.
