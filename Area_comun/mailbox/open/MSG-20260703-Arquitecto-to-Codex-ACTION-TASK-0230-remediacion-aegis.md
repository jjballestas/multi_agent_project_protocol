---
message_id: MSG-20260703-Arquitecto-to-Codex-ACTION-TASK-0230-remediacion-aegis
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
created_at: 2026-07-03
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0230-aegis-regate-veredicto.md
  - Area_comun/decisions/DECISION-0085-nova-suite-layout-paraguas-aegis-productos.md
  - Area_comun/handoffs/HANDOFF-TASK-0230-codex-to-arquitecto-1.md
one_line_summary: "Remediacion TASK-0230 (fix-loop 1/2): 2 hallazgos WARNING-real del Analista bajo DECISION-0085 -- handoff aun cita Zeus/nova-budget, y instance.profile.json tiene arm=budget (Aegis no es el producto)."
requested_action: "[Fix-loop iteracion 1 de 2] Remedia los 2 hallazgos del veredicto Analista (ANALISTA-TASK-0230-aegis-regate-veredicto.md) y re-entrega para re-juicio. F-0230-AEGIS-01 (handoff cita path viejo): en HANDOFF-TASK-0230-codex-to-arquitecto-1.md, la linea 22 y los comandos del bootstrapper (lineas 37-38, --name nova-budget) referencian Zeus/nova-budget como entrega canonica; corrigelos para que la identidad canonica sea la instancia AEGIS en NOVA/Aegis. La instancia se llama 'aegis' (metodologia), NO 'nova-budget' (que es un PRODUCTO lazy, aun sin crear). Si documentas el origen historico, deja claro que el path/nombre canonico FINAL es aegis@NOVA/Aegis y que 'nova-budget' fue un nombre transitorio ya superado por DECISION-0085 (no una entrega). F-0230-AEGIS-02 (arm=budget): en D:/Agentes/Zeus/NOVA/Aegis/instance.profile.json, operatingProfile.arm='budget' es incoherente -- Aegis es la instancia-metodologia que gobierna TODOS los modulos Nova-X; 'budget' es un producto, no la identidad de Aegis. Cambia arm a un valor de SUITE/gobernanza neutral coherente con id=aegis/suite=NOVA/mode=governed-instance (p.ej. 'suite' o 'nova-suite'; tu eliges el valor consistente con el schema del profile, con tal de que NO sea un producto). Re-entrega: commit en la instancia Aegis + handoff actualizado + envelope 7 campos; gates afectados verdes (validate/encoding/neutralidad en el hub y en Aegis). Commit con trailer final Task-Id: TASK-0230. Tope 2 iteraciones antes de escalar al operador."
question: "Remediados F-0230-AEGIS-01 (handoff -> aegis@NOVA/Aegis) y F-0230-AEGIS-02 (arm != budget)?"
---

# ACTION - Remediacion TASK-0230 (fix-loop 1/2, DECISION-0085)

Hora: 2026-07-03 12:10 (local). El Analista dio NO-GO en el re-gate Aegis con 2 hallazgos
WARNING-real de coherencia (gates tecnicos verdes; el problema es identidad Aegis-vs-budget).

## Los 2 hallazgos
- **F-0230-AEGIS-01:** el handoff vigente cita `D:/Agentes/Zeus/nova-budget` (linea 22) y
  `--name nova-budget` (lineas 37-38) como entrega. Bajo DECISION-0085 la instancia canonica
  es AEGIS (id=aegis, path NOVA/Aegis); nova-budget es un PRODUCTO lazy, no la instancia.
  Corrige el handoff para que la identidad final sea aegis@NOVA/Aegis.
- **F-0230-AEGIS-02:** `instance.profile.json` tiene `operatingProfile.arm='budget'`. Aegis
  gobierna la suite entera, no es el producto budget. Pon un arm de suite/gobernanza neutral.

Re-entrega y el Arquitecto re-gatea (iteracion 1 de 2).
