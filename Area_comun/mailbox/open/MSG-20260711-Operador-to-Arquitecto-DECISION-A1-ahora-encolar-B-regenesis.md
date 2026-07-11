---
message_id: MSG-20260711-Operador-to-Arquitecto-DECISION-A1-ahora-encolar-B-regenesis
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-11
context_refs:
  - Area_comun/mailbox/open/MSG-20260711-Arquitecto-to-Operador-BLOCKER-regenesis-A2-chain-reanchor.md
  - Area_comun/mailbox/open/MSG-20260711-Operador-to-Arquitecto-GO-regenesis-A2-julian-y-speckit-contabilidad.md
one_line_summary: "Decision Orden 1: A1-AHORA (Julian bajo identidad Codex via override runtime, sin tocar config/genesis -> desbloquea onboarding + gate 2-clones hoy) + ENCOLAR B (Codex construye el re-anclaje de cadena para la A2 nominal limpia con jheredia:v1). GUARDRAIL: B debe aterrizar ANTES de la primera unidad de build gobernada de Julian. Orden 2 (kit SPEC-CONT) sigue en paralelo."
requested_action: "Ejecuta A1 ahora: habilita a Julian bajo la identidad Codex via override runtime (Opcion A1 del runbook s.8.4), sin cambio de config ni re-genesis, para desbloquear su onboarding + el gate e2e de 2 clones. Y ENCOLA B a Codex: sellar el segmento operativo actual (seq 672..N) como el pre_t0 seal + escribir un chain.genesis nuevo en N+1 atado al config con jheredia:v1 + soporte del validador para la frontera de epoca-de-config, para la A2 nominal limpia. Corrige el runbook s.8.4 (sobre-declara el tooling A2) cuando B entregue el re-anclaje real."
question: "Confirmas A1 ejecutada (Julian operativo bajo Codex) y B encolada a Codex? Reporta cuando el gate 2-clones quede verde. Recordatorio del guardrail duro abajo."
---

# ACTION - Decision Orden 1: A1-ahora + encolar-B (re-genesis A2)

Recibido tu BLOCKER (diagnostico verificado en codigo: cambiar el config rompe el prev_hash del chain.genesis
y la cascada; regenesis.py no re-ancla la cadena; no hay tooling de re-anclaje; es el problema de seq-2175).
Buen manejo: revertiste limpio (validate 0, b22e49bc, config intacto), sin commitear nada roto ni forjar
historia. Decision del Operador:

## Orden 1 = A1-AHORA + ENCOLAR-B
1. **A1 ahora:** habilita a Julian bajo la identidad Codex via override runtime en su maquina (Opcion A1 del
   runbook s.8.4), SIN cambio de config ni re-genesis. Desbloquea su onboarding y el gate e2e de 2 clones hoy.
2. **Encolar B a Codex:** el re-anclaje de cadena limpio -- sellar seq 672..N como el pre_t0 seal + chain.genesis
   nuevo en N+1 atado al config con jheredia:v1 + soporte del validador para la frontera de epoca-de-config.
   Es el patron pre_t0 que YA existe; trabajo de runtime real, no improvisado.

## GUARDRAIL DURO (study-integrity)
B debe COMPLETAR antes de la primera unidad de build GOBERNADA de Julian (es decir, antes de abrir el build,
post-30-jul). Hasta que B aterrice, el trabajo de Julian es ONBOARDING NO-STUDY bajo Codex (aprender la
metodologia + pasar el gate 2-clones). Su trabajo study-relevant (la evidencia employee-run/transferibilidad =
el build gobernado de Contabilidad) debe nacer bajo su identidad nominal jheredia:v1. Con el build gated a
post-30-jul hay ~19 dias de pista para hacer B bien. No dejes que Julian toque una unidad gobernada atribuible
bajo Codex.

## Pendientes de coordinacion
- El gate 2-clones REAL necesita el clon de Julian operativo: su privada + los secretos HMAC de instancia que
  el Operador distribuye fuera de banda. Tu haces el lado config + paridad de replay local. (Aplica a A1 y B.)
- Follow-up de doc: corrige el runbook s.8.4 (sobre-declara "pubkey + regenesis.py" como A2 valida) cuando B
  entregue el re-anclaje.

## Orden 2 (kit SPEC-CONT): recibido indice + Slice 1 -- sigue
Vi tu entrega del indice + Slice 1 (reportes RO), PREP patron NOVA-SPEC-T-001. Continua por slice (R2-R8) y
reporta la colocacion gobernada (hub Area_comun/specs/nova/ vs ledger de instancia). Ancla el
source_bundle_sha256 de la base congelada (608b4370...) como referencia -- ver mi FYI de base promovida.

-- Operador
