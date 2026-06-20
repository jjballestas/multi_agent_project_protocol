# DRAFT - TASK-0133: Front - intake gobernado de historias/requisitos (RF-11)

> DRAFT en personal/Arquitecto; NO promovido. Espera ratificacion de DECISION-0051 + extension
> SPEC-0086. maker=Codex / checker=Arquitecto. Codigo en Zeus-protocol (repo producto separado).

- spec: SPEC-0086 (extension RF-11; AC14-AC17 + carry AC11/12/13)
- decision: DECISION-0051 (superficie EXECUTE del operador; intake = task_upsert requirement)
- status propuesto al promover: ready (Codex)
- repo de codigo: D:/Agentes/Zeus/Zeus-protocol
- gobernanza/dataset: este protocolo (Area_comun), atestado #4

## Alcance (de a una pieza)
1. **Wizard de intake (UI):** formulario que estructura titulo, narrativa, intencion de aceptacion
   (lenguaje llano) y proyecto destino; vista de preview con PII redactada antes de confirmar.
2. **Accion gobernada de intake:** agregar a GOVERNED_ACTIONS una accion que arme un intent
   `task_upsert` de un requirement (status proposed, type=requirement, author=Operador), con
   `actorId:"Operador"` (corregir el default "Arquitecto" SOLO para intake), idempotency_key estable.
3. **Cablear EXECUTE real en la UI:** boton + paso de confirmacion visible que envia
   `mode:execute` + `confirm:SUBMIT_INTENT`; mostrar el resultado del runtime. Mantener
   `directLedgerWrites:false`.
4. **Redaccion PII:** reutilizar el redactor de texto libre (safePayloadPreview / equivalente) en
   preview, vista y export; canal ASCII a lo que se escribe.
5. **Handoff intake->SPEC:** el requirement queda en el ledger; el Arquitecto lo consume (no es parte
   del codigo, pero el artefacto debe ser autocontenido: narrativa + intencion de aceptacion).

## DoD
- AC14-AC17 verdes con tests de comportamiento + negativos (sin-confirm-no-escribe; PII redactada).
- Carry AC11/AC12/AC13 verdes.
- node --test verde; CI verde.
- validate exit 0 CON y SIN secretos (clon limpio, DECISION-0046); drift 0; #4 epoca 1.14.0 intacta;
  neutralidad limpia (codigo solo en Zeus-protocol).
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker.
- Commit como Arquitecto con Co-Authored-By: Codex (Codex no forja commits).

## Fuera de alcance
- Otros intent kinds desde el front (sigue cerrado). DEF-PII vivo (TASK-0118 sigue como gate). Roster
  RF-9 (deferida). Captura de PII real viva (gated).
