---
task_id: TASK-0133
title: "Proyecto-front - intake gobernado de historias/requisitos (RF-14): wizard -> task_upsert requirement via EXECUTE confirmado; PII estructural; conforme al diseno components/intake/"
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0051, DECISION-0040, DECISION-0049, DECISION-0050]
created_at: 2026-06-20
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0133-codex-front-intake-historias.md
---

# TASK-0133 - Front: intake gobernado de historias/requisitos (RF-14)

> maker=Codex / checker=Arquitecto. Codigo en Zeus-protocol (repo producto). Gobernanza/dataset en el
> protocolo. Ratificado: DECISION-0051 + extension SPEC-0086 (RF-14 + AC14-AC17). Construir CONTRA el
> diseno YA entregado por Claude Design en `design/interface/components/intake/`.

## Alcance (de a una pieza)
1. **Wizard de intake (UI)** conforme al diseno `components/intake/` (lista, wizard-1-capturar,
   wizard-2-preview, wizard-3-confirmar, wizard-4-resultado, detalle, estados): estructura titulo,
   narrativa, intencion de aceptacion en lenguaje llano, proyecto destino. Preview (dry_run) distinto del
   envio (execute). Rotulado "Historia/requisito (semilla para SDD)"; nota "el Arquitecto la convierte en
   SPEC con AC+test_plan" (el operador NO firma AC).
2. **Accion gobernada de intake:** agregar a GOVERNED_ACTIONS una accion que arme un intent `task_upsert`
   de un requirement (status proposed, type=requirement, author=Operador), con `actorId:"Operador"`
   (corregir el default "Arquitecto" SOLO para intake), `idempotency_key` estable.
3. **Cablear EXECUTE real en la UI:** boton + paso de confirmacion visible que declara el writer
   (`runtime/submit_intent.py`) y envia `mode:execute` + `confirm:SUBMIT_INTENT`; mostrar el resultado real
   (seq/id, actor); sin verde sin respuesta real del execute. Mantener `directLedgerWrites:false`.
4. **Guarda PII estructural (AC16):** separar lenguaje-llano publicable del payload sensible; redactar/marcar
   texto libre en todo plano publicable/exportable; canal ASCII en todo string escrito al protocolo; advertir
   en compose y confirm. NO depender de un detector inexistente (TASK-0118/DEF-PII proposed).
5. **Handoff intake->SPEC:** el requirement queda en el ledger atestado, autocontenido (narrativa + intencion
   de aceptacion); el Arquitecto lo consume para autorar la SPEC.

## DoD
- AC14-AC17 verdes con tests de comportamiento + negativos (sin-confirm-no-escribe; PII redactada;
  idempotencia; no-bypass). Carry AC11/AC12/AC13 verdes (AC13 conformidad aplica a las pantallas intake).
- `node --test` verde; CI del producto verde; `npm start` ejecutable y la vista de intake navega.
- `validate_collaboration_state` exit 0 CON y SIN secretos (clon limpio, DECISION-0046); drift 0; #4 epoca
  1.14.0 intacta (sin re-genesis); neutralidad limpia (codigo solo en Zeus-protocol; "proyecto destino" =
  dato, no logica de dominio).
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker.
- Commit como Arquitecto con `Co-Authored-By: Codex` (Codex no forja commits).

## Fuera de alcance
- Otros intent kinds desde el front (sigue cerrado). DEF-PII vivo / captura de PII real (TASK-0118 sigue
  gate). Roster RF-9 (deferida). Export del dataset / multi-tenant.
