---
message_id: MSG-20260620-Analista-to-Operador-intake-requisitos-diseno
type: REVIEW
task_id: none
from: Analista
to: Operador
status: open
requires_response: false
response_owner: none
one_line_summary: Requisitos de diseno (lente honestidad/metodologia/neutralidad) para el INTAKE GOBERNADO de historias. 7 puntos falsables (REQUISITO + MODO DE FALLA + honesto). Insumo para Claude Design + la SPEC del Arquitecto; no promueve nada.
requested_action: "Llevar a Claude Design como requisitos que el diseno DEBE honrar; y al Arquitecto como insumo de la SPEC. Ver artefacto."
context_refs:
  - Area_comun/artifacts/ANALISTA-intake-gobernado-requisitos-diseno.md
  - Area_comun/decisions/DECISION-0040-gate-dataset.md
---

# Requisitos de diseno - INTAKE GOBERNADO de historias (voz Analista)

Entregue los requisitos falsables que el diseno de Claude Design DEBE honrar. NO disene UI ni mute estado.
Anclajes verificados por mi: GO en canonico (98410ce); DECISION-0040 canonica; TASK-0118/DEF-PII = proposed
(el detector de PII automatico NO existe aun -> la guarda es estructural, no "el scanner lo atrapa"); el
front ya tiene dry_run vs execute+confirm:SUBMIT_INTENT (el intake reusa ese camino, no crea otro escritor).

Por punto, en el artefacto (REQUISITO / MODO DE FALLA descartado / como se ve honesto):
1. Read vs Write distintos: montar/enviar = escribir -> paso de confirmacion explicito "encola un intent via
   submit_intent"; nada que sugiera escritura directa.
2. Honestidad de estado: preview (dry_run) != envio (execute confirmado); nada verde sin verificacion real;
   indeterminado/cargando/error marcados.
3. Guarda PII innegociable: separar intencion-en-lenguaje-llano (publicable) de payload sensible; redactar/
   marcar texto libre en plano publicable; ASCII; advertir en compose y confirm; NO depender de un scanner
   inexistente. Coherente con DECISION-0040 y el gate TASK-0118/DEF-PII.
4. Roles/SDD visibles: el wizard captura la SEMILLA (requisito), NO una SPEC; el Arquitecto autora la SPEC
   con AC/test_plan despues (el operador no firma AC).
5. Trazabilidad: evento gobernado atribuido al operador; cada envio deja huella (id+seq, idempotente).
6. Neutralidad: el dominio (nova.budget) es solo dato; nada de negocio en el nucleo/design-system neutral.
7. Modos de falla a EVITAR (explicitos): escribir directo el ledger, verde falso, texto crudo expuesto,
   enviar sin confirmacion. El diseno debe demostrar que NINGUNO ocurre.

Nota: el intake debe colgar del patron existente governed-action / "Acciones gobernadas" (un solo writer),
no una superficie nueva de escritura. No promovi, no mute estado, no autore la SPEC.
