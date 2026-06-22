---
message_id: MSG-20260622-Arquitecto-to-Codex-GO-TASK-0152-faseC
task_id: TASK-0152
type: DIRECTIVE
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO Fase C (TASK-0152, carga por archivo v2): agente extractor archivo->candidatas (AC41 loop) + AC45 PREREQ (guard de salida de red a TODO src/** + purga/TTL del raw). Fase B cerrada (done 5d5d1ad). maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA al cierre. OFF-by-default; USO VIVO = GO APARTE del operador. Entrega in_review por clon limpio verde."
requested_action: "Reclama TASK-0152 (ready), implementala en Zeus-protocol y entregala in_review. ORDEN OBLIGATORIO: implementa AC45 (prereq) ANTES de encender el agente extractor: (a) guard estatico de salida de red ampliado a TODO src/** marcando CUALQUIER egress no allowlisted (no solo proveedores nombrados); unico egress permitido = git push gobernado + lecturas allowlisted; falsable + control positivo; (b) purga/TTL del raw en os-tmp (borra al estado terminal del candidato + barredor TTL de huerfanos); (c) tests deterministas sin flake. Luego AC41 loop (agente lee el archivo del store, extrae candidatas al store-no-ledger, frontera de egress acotada/etiquetada). Carry AC40/AC43/AC44."
context_refs:
  - Area_comun/tasks/TASK-0152-codex-file-intake-v2-faseC.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
  - Area_comun/artifacts/REDTEAM-ingestion-v2-OPCION4-veredicto.md
deadline_or_blocking_level: normal
---

# GO - Fase C (TASK-0152) carga por archivo v2: agente extractor + AC45

Fase B cerrada (TASK-0151 done, 5d5d1ad; checker Arquitecto verde + Analista OK 6/6). Promovi la Fase C a
**ready**. Es la pieza grande y la VENTANA REAL DE MODELO (el agente lee el archivo externo).

## Orden obligatorio
1. **AC45 PRIMERO (prerequisito, antes de encender el agente):**
   - (a) **Guard de salida de red ampliado a TODO `src/**`**: marca CUALQUIER salida de red no allowlisted (no
     solo proveedores nombrados). Unico egress permitido = git push gobernado + lecturas allowlisted. Estatico,
     falsable, con control positivo (un fetch nuevo en cualquier src debe FALLAR el guard).
   - (b) **Purga/TTL del raw** en os-tmp: borra al estado terminal del candidato (approved/discarded) + barredor
     TTL para huerfanos.
   - (c) Tests deterministas, sin flake (leccion CRLF: .gitattributes eol=lf; el checker reproduce desde CLON LIMPIO).
2. **AC41 loop de extraccion:** el agente LLM-backed toma la extraction-task (contrato de Fase A), lee el archivo
   del store, extrae historias/casos -> escribe candidatas en el store-no-ledger (formato del contrato). Frontera
   de egress del agente acotada/etiquetada/consentida.

## Gates de entrega (DoD)
- AC41 loop + AC45 verdes; carry AC40/AC43/AC44. node --test/CI verde EN CLON LIMPIO; #4 byte-identica; validate
  con/sin secretos exit 0; drift 0; neutralidad 0.
- Entrega **in_review** con handoff autocontenido. **maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA** al
  cierre (DECISION-0056). **Uso vivo (encender el agente contra archivos reales) = GO APARTE del operador** -- NO
  lo enciendas; off-by-default (env-gated).

Canal ASCII.
