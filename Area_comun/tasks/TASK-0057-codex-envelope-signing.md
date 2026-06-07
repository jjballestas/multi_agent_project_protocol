---
id: TASK-0057
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
closed_by: Claude (ratificacion adversarial)
depends_on: [TASK-0044, TASK-0056]
relates_to: [TASK-0048, TASK-0049]
phase: P2
spec_id: Area_comun/specs/SPEC-0043-fase5.3-envelope-signing.md
linked_decisions: [DECISION-0015, DECISION-0017, DECISION-0018]
execution_pipeline: [anadir config event_auth.enabled off por defecto en protocol.config.json + .template (ausencia/off = comportamiento actual); en runtime/eventlog.py firmar el envelope al append (HMAC con clave por agente desde config/registry, bootstrap local, determinista) y verificar la firma al validar/replay; con signing on, evento sin firma valida => rechazado + security.unauthenticated_event; auth admite issuer/audience como estructura placeholder (capa-b A1) sin implementar flujo OAuth/JWT externo; mantener replay determinista (mismo hash canonico) y negative-replay (A6, sin reloj/red); crear examples/runtime_event_auth_cases/ con los casos del test plan + step de CI]
acceptance_criteria: [EA1 - con signing on todo evento aplicado lleva firma valida atribuible al agente; sin firma valida => rechazado + security.unauthenticated_event (I7); EA2 - replay determinista: replay(log) reproduce el mismo hash canonico de snapshot, negative-replay safe (sin invocar red/reloj); EA3 - aditivo/reversible: con event_auth off o ausente el comportamiento es BYTE-EQUIVALENTE al actual y el fallback N=2 se preserva; NO implementar flujo OAuth/JWT externo (solo estructura issuer/audience); sin secretos reales en el repo vivo (clave de prueba solo en el golden); los golden y la suite runtime existentes siguen verdes; domain-neutral; sin red; neutralidad limpia]
test_plan: [examples/runtime_event_auth_cases/ determinista (sin red/reloj/random): (1) evento con firma valida => aceptado; (2) evento con firma ausente/alterada (signing on) => rechazado + security.unauthenticated_event; (3) replay determinista: mismo hash canonico, negative-replay safe; (4) signing off/ausente => byte-equivalente, fallback N=2; (5) auth issuer/audience como estructura sin activar flujo externo; suite runtime completa verde + validador/encoding/neutralidad py]
closure_criteria: [config event_auth.enabled off por defecto (live + template; ausencia/off = comportamiento actual); firma HMAC del envelope en runtime/eventlog.py + verificacion en validate/replay; evento sin firma valida (signing on) => rechazado + security.unauthenticated_event; replay determinista + negative-replay intactos; auth issuer/audience como estructura placeholder (sin flujo externo); golden examples/runtime_event_auth_cases/ verde + suite runtime completa + gates py; suite en CI; fallback N=2 byte-equivalente; sin secretos reales en repo vivo; neutralidad limpia; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0057 - Fase 5.3: autenticacion/atribucion de eventos (firma del envelope)

> `implementation`/security -> SDD. Rebanada 3 (ultima del nucleo) de Fase 5 (SPEC-0040 sec.3). Aditiva,
> config-gated (firma off por defecto), fallback N=2 intacto. Aditiva sobre runtime/eventlog.py; NO depende
> de activar Fase B. Ver SPEC-0043. NO requiere DECISION nueva (autorizada por DECISION-0015 + OK operador).

## Contexto

SPEC-0038 sec.8.1 (A1): todo evento debe ir firmado/autenticado; un evento sin firma valida se rechaza como
security.unauthenticated_event (I7). Hoy eventlog.py no autentica el envelope. A.6 (TASK-0049) cerro la
atribucion de AUTOR-DE-RECORD desde el estado; falta la AUTENTICIDAD DEL EVENTO (firma).

## Alcance

1. **Dos capas de identidad (A1):** (a) autenticidad del evento = sobre firmado (HMAC por agente, bootstrap
   local, determinista); (b) autorizacion externa = SOLO estructura issuer/audience en `auth` (placeholder,
   sin flujo OAuth/JWT externo).
2. **Firma + verificacion en `runtime/eventlog.py`** (aditivo): firmar al append, verificar al validar/replay;
   con signing on, evento sin firma valida => rechazado + `security.unauthenticated_event`.
3. **Config `event_auth.enabled` off por defecto** (live + template); ausencia/off => comportamiento actual.
4. **Golden `examples/runtime_event_auth_cases/`** + CI. Determinismo + negative-replay (A6) intactos.

## Restricciones

- **Aditivo**, config-gated (firma off por defecto); **fallback N=2 byte-equivalente**.
- **Determinismo del replay** (sin reloj/red) y negative-replay (A6) intactos -> firma determinista.
- **Sin secretos reales** en el repo vivo (clave de bootstrap de prueba solo en el golden). Domain-neutral.
- NO implementar el flujo OAuth/JWT externo (solo estructura issuer/audience).
- Fuera de alcance: Fase B (SPEC-0039), Fase 6/7. Cambio incompatible => `blocked` + pregunta + DECISION.
- **Handoff autocontenido**; **release atomico** (DECISION-0018).

## Nota

Rebanada 3 (ultima del nucleo) de Fase 5: 5.1 (done) -> 5.2 (done) -> **5.3 (esta)**. Con 5.1+5.2+5.3 el
nucleo de Fase 5 (guardrails/permisos/identidad) queda cubierto; el resto de sec.8 (sandbox de side-effects
real) se activa con superficie externa real (gateado). Codex autonomo (~100s): tomala cuando este ready.
