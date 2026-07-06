---
message_id: MSG-20260706-Operador-to-Arquitecto-ACTION-adjudicaciones-1102-lote2
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/mailbox/open/MSG-20260706-Arquitecto-to-Operador-ESCALACION-TASK-1102-doble-nogo.md
  - Area_comun/mailbox/open/MSG-20260706-Arquitecto-to-Operador-LOTE2-PENDIENTE-onboarding-remoto-dba-identidad-anchor.md
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/protocol/RUNBOOK-onboarding-multi-clon-aegis.md"
one_line_summary: "Adjudicaciones del Operador a la ESCALACION 1102 (3) + LOTE2 (3), con candados: 1102 fix-loop 3 solo-tests con re-verificacion del checker; tarea drift si; UI per-item; DBA copia sanitizada; identidad A2 propia (re-genesis SOLO de Aegis, jamas el hub); anchor canonico-solo v1."
requested_action: "Ejecutar las 6 adjudicaciones de abajo. Reportar pickup + ETAs. Las study-criticas llevan candado explicito: (1102-1) el checker re-verifica que los fixtures codifican el contrato CORREGIDO y que el producto queda byte-identico; (1102-3) UI per-item, NO checkbox global; (LOTE2-A) el re-genesis es del config de AEGIS unicamente -- el genesis pineado del hub (epoch 1.14.0) NO se toca; si A2 tocara el hub, difiere y avisa."
question: "Confirmas las 6 y sus candados? Reporta el re-gate de 1102 tras el fix-loop 3, y el lead time del encargo DBA (camino critico)."
---

# ACTION - Adjudicaciones del Operador: ESCALACION 1102 (3) + LOTE2 (3)

El Operador adjudica (acepto las recomendaciones del Asesor con sus candados):

## TASK-1102 (escalacion 3er NO-GO)
1. **Fix-loop 3 ACOTADO a tests: SI, con CANDADO.** Solo actualizar fixtures/tests al contrato nuevo
   (qualityConfirmations en validIntake/contention, happy-path de candidatas con campos+approval, +caso
   negativo); CERO cambios de producto. **Candado (study-integrity):** el checker re-verifica que los
   fixtures codifican el contrato CORREGIDO (no debilitados para pasar) Y que el codigo de producto queda
   BYTE-IDENTICO. Es la diferencia entre arreglar el test y mover la porteria.
2. **Tarea NUEVA para el drift de trailers: SI.** buildAutoCommitMessage emite commits sin Task-Id y el gate
   de trailers del hub aterrizo hoy -> test:ci inalcanzable para cualquier commit del producto. Tarea propia,
   owner Codex, chica. Preexistente, no de 1102.
3. **UI: PER-ITEM, no checkbox global (study-critica).** Un checkbox global que auto-genera 13 confirmaciones
   ES el rubber-stamp que el producto anti-vibecoding existe para impedir (DECISION-1001 s.2: gana verificacion/
   responsabilidad sobre magia automatica). Confirmacion por item, fiel a SPEC s.7. Si hay friccion de UX, se
   resuelve con diseno (revelado progresivo), NO auto-confirmando.

## LOTE2 (onboarding remoto)
5. **Acceso BD remoto: COPIA SANITIZADA local (camino critico, arranca YA).** Si el sandbox tiene datos reales
   de entidades publicas, van SANITIZADOS (sin PII) a la maquina del empleado, con grants patron
   budget_sandbox_verifier. La paridad del estudio se sostiene (es sobre esquema/superficie proc-vista, no
   filas). VPN al sandbox solo si ya es sintetico/no-sensible. Dale el encargo al DBA con su lead time.
6. **(A) Identidad del empleado: A2 (identidad propia), con CANDADO (study-critica).** La transferibilidad/
   employee-run necesita atribucion NOMINAL por humano (A1 bajo Codex/Analista turbia la evidencia). A2:
   estrena `<id>:v1`, su pubkey entra al config. **CANDADO: el re-genesis es del config de AEGIS UNICAMENTE;
   el genesis pineado del HUB (epoch 1.14.0) NO se toca en la ventana sellada.** Si A2 obligara a tocar el hub,
   DIFIERE y avisa (se cae a A1 temporal). Coordina la generacion de llave del empleado en su maquina + el
   re-genesis de Aegis al recibir la pubkey.
7. **(B) Anchoring del clon remoto: CANONICO-SOLO (v1).** El anchor externo es capa secundaria; la atestacion
   primaria es el #4 de Aegis + cross-atestacion ya cableada. Tu maquina ancla; el remoto opera con anchor
   deshabilitado por override. Migra a remoto compartido (GitHub) solo si el audit-trail distribuido se vuelve
   study-relevante mas adelante.

## Frontera
Nada de esto toca el estudio MEDIDO ni el genesis pineado del hub. El segundo humano es variable del estudio
pre-registrada en el sello Etapa 2 (s.4b) -- su onboarding (identidad/acceso) se prepara ahora; su
participacion cuenta desde su pre-registro. Sigue sin idle: TASK-1203 + Contabilidad WS1 en cola.

-- Operador
