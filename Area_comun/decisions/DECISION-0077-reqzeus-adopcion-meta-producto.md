---
decision_id: DECISION-0077
title: "REQ-ZEUS Adopcion - REQ-ZEUS-001 (productizacion Zeus-Aegis + 4 firmantes) adoptado como meta de producto activa, gobernado en el hub como cadena atestada unica; backlog en TASK-02xx con prefijo [REQ-ZEUS-001][WSx]"
status: accepted
ratified_at: 2026-06-30
date: 2026-06-30
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [REQ-ZEUS-001, DECISION-0050, DECISION-0072, DECISION-0073, DECISION-0074, DECISION-0075, DECISION-0076]
scope: product
phase: P2
---

# DECISION-0077 (REQ-ZEUS) - Adopcion de REQ-ZEUS-001 como meta de producto

> ACCEPTED (operador GO explicito 2026-06-30, directiva OPS-115242Z + confirmacion de registro).

## Decision
Se adopta **REQ-ZEUS-001** (productizacion de Zeus-Aegis + metodologia de 4 firmantes) como **meta de producto
activa** (`GOAL-REQ-ZEUS-001`), **gobernada en el HUB** (`multi_agent_project_protocol`) como una **sola cadena
atestada** (DECISION-0050). El codigo de producto vive en `D:/Agentes/Zeus/Zeus-Aegis`; la instancia-plantilla es NOVA.

### Numeracion (reglas del operador)
- **Decisiones D1-D5 = DECISION-0072..0076** en el hub (scope product), NO namespace NOVA-DECISION-* (evita
  fragmentar el ledger). Viven en `Area_comun/decisions/` vivo, NO en los `*.template.*` (neutralidad del master intacta).
- **Backlog de tareas en TASK-02xx** (secuencia del hub): el hard-gate del validador (row-selector de TASK_INDEX)
  solo acepta `TASK-\d{4}`; un namespace `TASK-ZEUS` romperia el scope de los claims y cambiar la regex tocaria el
  core neutral. El agrupamiento de producto va en el **titulo con prefijo `[REQ-ZEUS-001][WSx]`** + campo
  **`relates_to: REQ-ZEUS-001`**, no en el id.

## Reconciliacion (no se tira trabajo)
- TASK-0226 = WS1 (branding inventario+plan) -> done.
- TASK-0222/0223 = WS6 parcial (vistas F1 read-only).
- TASK-0227/0224 = infra. TASK-0225 = habilitador 24/7.
- D1-D5 = DECISION-0072..0076 (registradas). Canonicalizan las NOVA D1-D5.

## Backlog registrado (TASK-02xx, status proposed; se promueve de a una)
- **TASK-0228 [WS5]** alta Analista en NOVA + mapeo rol->agente + wrapper new_instance(4) -- PRIMERO (condiciona owner:Analista).
- TASK-0229 [WS3] branding + alias env + pantalla "Preparando Zeus".
- TASK-0230 [WS2] bootstrapper (gateway+backend+config+lifecycle Electron).
- TASK-0231 [WS4] backend modelos (D3) + bloqueo PII + spike peones (sandbox aparte).
- TASK-0232 [WS3.5] instalador electron-builder firmado + desinstalacion limpia.
- TASK-0234 [WS10] runbooks. (WS7 e2e = owner Analista, se registra tras cerrar WS5.)

## Restricciones (no negociables)
F2 write-through al ledger MEDIDO fuera de alcance; TFM intocable (5 pineados; core neutral no se toca);
piloto de peones en repo sandbox aparte `D:/Agentes/Zeus/piloto-peones`; licencias (2 avisos MIT); sin secretos; sin PII saliente.
