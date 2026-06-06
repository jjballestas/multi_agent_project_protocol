---
spec_id: SPEC-0043-fase5.3-envelope-signing
task_id: TASK-0057
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0015, DECISION-0017, DECISION-0018]
relates_to: [SPEC-0038, SPEC-0039, SPEC-0040]
---

> Rebanada 3 (ultima del nucleo) de la Fase 5 (SPEC-0040 sec.3). SPEC-0038 sec.8.1, D-1 (P0), addenda A1.
> Aditiva, config-gated (firma off por defecto), fallback N=2 byte-equivalente. Aditiva sobre
> runtime/eventlog.py; NO depende de activar Fase B (SPEC-0039). NO requiere DECISION nueva (autorizada por
> DECISION-0015 + OK operador). Cambio incompatible => blocked + DECISION.

# SPEC-0043 - Fase 5.3: autenticacion/atribucion de eventos (firma del envelope)

## 1. Problema

SPEC-0038 sec.8.1 (A1): todo evento/turn_report debe ir firmado/autenticado segun `agent.auth`; un evento
sin firma valida se rechaza y registra como `security.unauthenticated_event` (sin esto el log inmutable no
vale, I7). Hoy `runtime/eventlog.py` no autentica el envelope. La Capa A.6 (TASK-0049) cerro la atribucion
de AUTOR-DE-RECORD desde el estado; falta la capa de AUTENTICIDAD DEL EVENTO (firma).

## 2. Alcance (TASK-0057)

1. **Dos capas de identidad (A1):**
   - (a) **Autenticidad del evento** = sobre firmado en el log (HMAC por agente, clave de bootstrap local).
   - (b) **Autorizacion de protocolo externo** = tokens audience-bound (OAuth/JWT estilo MCP/A2A): SOLO
     estructura/placeholder en `auth` (issuer/audience) para cuando existan agentes/tools externos. NO
     implementar el flujo externo ahora.
2. **Firma del envelope en `runtime/eventlog.py` (aditivo):** al `append`, firmar el evento (HMAC con clave
   por agente desde config/registry); al validar/replay, verificar la firma. Con signing habilitado, un
   evento sin firma valida => **rechazado** + `security.unauthenticated_event`. `trust_boundary` mapea a
   deny-by-default (coherente con 5.1/5.2).
3. **Config-gated:** `event_auth.enabled` off por defecto => byte-equivalente al actual; on => exige firma.
4. **Golden `examples/runtime_event_auth_cases/`** + CI. **Determinismo:** la firma debe ser determinista
   (sin reloj/red) para que el replay reproduzca el mismo hash canonico; mantener negative-replay (A6).

## 3. Invariantes

- **EA1:** con signing on, todo evento aplicado lleva firma valida atribuible al agente; sin firma valida =>
  rechazado + `security.unauthenticated_event` (I7).
- **EA2:** replay determinista: `replay(log)` reproduce el mismo hash canonico de snapshot; negative-replay
  safe (sin invocar red/reloj).
- **EA3:** aditivo/reversible: con `event_auth` off (o ausente) el comportamiento es byte-equivalente al
  actual; fallback N=2 intacto.

## 4. Tests (deterministas, sin red)

1. evento con firma valida => aceptado.
2. evento con firma ausente/alterada (signing on) => rechazado + `security.unauthenticated_event`.
3. replay determinista: mismo hash canonico; negative-replay safe.
4. signing off / ausente => byte-equivalente; fallback N=2 intacto.
5. (placeholder A1 capa-b) `auth` admite issuer/audience sin activar flujo externo (estructura presente,
   no exigida).

## 5. Fuera de alcance

- Flujo OAuth/JWT externo real (solo estructura). Fase B (writer-vivo del estado, SPEC-0039). Fase 6/7.
- Secretos reales: la clave de bootstrap de prueba vive en el golden, NO en el repo vivo.
- Cambio incompatible de contrato => blocked + DECISION.

## 6. SemVer

- MINOR (firma aditiva, config-gated, default off = comportamiento actual).

## 7. Nota de cierre de Fase 5

Con 5.1 (anti-inyeccion) + 5.2 (tool-policy) + 5.3 (firma del envelope), el NUCLEO de la Fase 5
(guardrails / permisos / identidad) queda cubierto. El resto de sec.8 (sandbox de side-effects real) se
activa cuando exista superficie externa real (gateado).
