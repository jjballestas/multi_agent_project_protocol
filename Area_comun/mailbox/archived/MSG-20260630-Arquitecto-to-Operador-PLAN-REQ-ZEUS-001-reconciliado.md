---
message_id: MSG-20260630-Arquitecto-to-Operador-PLAN-REQ-ZEUS-001-reconciliado
from: Arquitecto
to: Operador
type: REQUEST
status: archived
requires_response: true
response_owner: Operador
created_at: 2026-06-30
task_id: REQ-ZEUS-001
question: "Aprobar el plan reconciliado REQ-ZEUS-001: (1) gobernanza de D1-D5 se queda en NOVA vs se duplica al hub; (2) namespace TASK-ZEUS-00xx vs 02xx; (3) GO a registrar la DECISION de adopcion + backlog TASK-ZEUS (0007 primero, ninguna owner:Analista antes del alta)?"
context_refs:
  - personal/Arquitecto/PLAN-REQ-ZEUS-001-reconciliado.md
  - Area_comun/goals/GOAL-REQ-ZEUS-001.md
  - MSG-20260630T115242Z-Operador-to-Arquitecto-DIRECTIVA-REQ-ZEUS-001-producto
one_line_summary: "Plan reconciliado REQ-ZEUS-001 listo para aprobacion: D1-D5 ya accepted en NOVA; mapa tareas->WS; backlog TASK-ZEUS; guia de peones en WS4/D3; ETA por fases; 3 dudas concretas."
requested_action: "Revisar personal/Arquitecto/PLAN-REQ-ZEUS-001-reconciliado.md y responder las 3 dudas (s.6) para desbloquear el registro en el hub."
---

# PLAN RECONCILIADO REQ-ZEUS-001 -- para tu aprobacion

Respondo la directiva OPS `115242Z`. Plan completo en `personal/Arquitecto/PLAN-REQ-ZEUS-001-reconciliado.md`.
Resumen ejecutivo:

## Hallazgo clave
Las **D1-D5 YA estan cerradas** (accepted 2026-06-30) en la instancia producto NOVA
(`D:/Agentes/Zeus/NOVA/Area_comun/decisions/DECISION-0001..0006`), y coinciden con tus endosos de la directiva.
Tambien hay una D6 (gate doc-only, ya usada en TASK-0226). Asi que "cerrar D1-D5" esta esencialmente HECHO;
lo que falta es decidir donde se gobiernan (duda 1).

## Reconciliacion (no se tira trabajo)
- TASK-0226 = **TASK-ZEUS-0002 (WS1)** -> done.
- TASK-0222/0223 = **TASK-ZEUS-0008 (WS6)** parcial (vistas F1 read-only) -> in_review/ready.
- TASK-0227 (npm test/boundary, NO era fuga F1) y TASK-0224 = INFRA. TASK-0225 = habilitador 24/7.
- Sin registrar (grueso del producto): WS5 alta-Analista (0007), WS3 branding (0003), WS2 bootstrapper (0004),
  WS4 backend+peones (0005), WS3.5 instalador (0006), WS7 e2e (0009), runbooks (0010).

## Secuencia
Primero **TASK-ZEUS-0007 (alta del Analista en NOVA + wrapper new_instance de 4 firmantes)** porque condiciona
todo lo owner:Analista (el validador rechaza esas tareas sin el alta). Luego WS3/WS2 en paralelo de a una.

## Guia de peones (WS4/D3)
Incorporada: niveles frontera+peon-no-firmante (Qwen2.5-Coder-7B / DeepSeek-Coder-6.7B), codegen-antes-que-LLM,
peon=maker barato fuera del ledger + firmante checker que firma (maker!=checker), gate determinista, y medicion
A/B/C con metrica = tokens del firmante. Piloto en repo SANDBOX aparte `D:/Agentes/Zeus/piloto-peones`.

## Restricciones respetadas
F2-al-ledger-medido fuera de alcance; TFM intocable (5 pineados); licencias MIT (2 avisos); sin PII saliente.

## ETA
Por fases (s.5 del plan): Fase 0 cerrar gates en vuelo; Fase 1 adopcion + 0007 firmantes; Fase 2 branding+bootstrapper;
Fase 3 backend+peones; Fase 4 instalador+e2e+runbooks. Camino critico: WS2 -> WS3.5 -> WS7.

## Necesito tu decision (s.6 del plan) antes de tocar el ledger
1. **D1-D5:** se quedan como decisiones de NOVA (recomiendo; el core neutral no se contamina) o se duplican al hub?
2. **Namespace:** registro el backlog como **TASK-ZEUS-00xx** (recomiendo) o sigo en TASK-02xx?
3. **GO a registrar** en el hub la DECISION de adopcion + backlog TASK-ZEUS (0007 primero; NINGUNA owner:Analista
   antes de cerrar 0007)?
