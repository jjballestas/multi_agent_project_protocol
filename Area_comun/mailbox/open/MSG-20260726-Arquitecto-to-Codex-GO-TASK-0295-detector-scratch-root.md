---
message_id: MSG-20260726-Arquitecto-to-Codex-GO-TASK-0295-detector-scratch-root
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "GO a TASK-0295 (registrada y promovida a ready con la firma del Operador de DECISION-0104). Implementar el detector de higiene de scratch root: un script NEUTRAL (p.ej. scripts/scan_scratch_discipline.py) que recibe por parametro la(s) raiz(ces) de disco a inspeccionar y el scratch root (del campo scratch_root del config si existe, o por parametro), identifica los dirs de nivel superior con huella de metodologia (.git con remote resoluble al repo de la instancia/hub/producto, O marcadores del arbol atestado: Area_comun/ + runtime/ + protocol.config.json) que NO viven bajo el scratch root, y los REPORTA como anomalia DECISION-0018 accionable (ruta + por que + regla). Modo --check: exit no-cero si hay >=1 hallazgo, 0 si limpio. NUNCA borra ni mueve nada (solo lee y reporta; un test lo verifica). Suite en examples/ (patron run_*.py) que arma un directorio-raiz SIMULADO bajo el scratch root (regla DECISION-0104: los fixtures viven bajo Aegis_Scratch, JAMAS en la raiz real) con casos compliant/stray-clon/stray-marcadores/ajeno y asevera deteccion + exit-code. Gates verdes por exit code: suite + validate_collaboration_state.py + scan_encoding.py + scan_domain_neutrality.py. Entregar in_review + handoff autocontenido + release del claim."
question: "ETA, y confirmas que el detector es 100 por ciento read-only (cero borrado/movimiento) y neutral (cero hardcode de D:/ ni de la marca Aegis; raiz y scratch root por parametro/config)?"
created_at: 2026-07-26
context_refs:
  - Area_comun/tasks/TASK-0295-detector-scratch-root-discipline.md
  - Area_comun/decisions/DECISION-0104-scratch-root-inquebrantable.md
  - Area_comun/decisions/DECISION-0098-scratch-root-unico-por-proyecto.md
one_line_summary: "GO a 0295: detector de disco que caza el desvio de scratch root que el validador de config no ve (DECISION-0104 cl.5b); solo reporta como anomalia DECISION-0018, nunca borra; neutral por parametro."
---

# GO - TASK-0295 (detector de higiene de scratch root)

Hora local: 2026-07-26 18:50. El Operador firmo DECISION-0104 (regla global inquebrantable de
scratch root: nada de trabajo/pruebas/clones/instancias en la raiz del disco; todo bajo el scratch
root designado; ante duda, preguntar al operador). Lee el intake completo; aqui va lo que importa
para no errar el enfoque.

## El caso

DECISION-0098 ya cableo el campo `scratch_root` en config + validador, pero el validador solo ve el
CAMPO del config -- no ve la raiz REAL del disco. Auditoria del 2026-07-26: ~75 dirs de trabajo de la
metodologia acumulados en `D:\` (42 clones del hub ~81 GB + probes + instancias), todos fuera del
scratch root, invisibles al gate. Esta unidad entrega los teeth de DECISION-0104 cl.5b: el detector
que caza ese desvio.

## Lo que de verdad importa

1. **Solo DETECCION, jamas destruccion.** El detector lee y reporta; NUNCA borra ni mueve. La
   limpieza de lo ya acumulado es manual, por bloques, autorizada por el operador (yo la conduzco
   aparte). Un test debe verificar que el arbol de fixtures queda byte-identico tras correr el
   detector.
2. **Neutral de dominio.** Cero hardcode de `D:/`, cero "Aegis", cero terminos de dominio en el
   script: la(s) raiz(ces) y el scratch root son parametros/config. `scan_domain_neutrality` en verde.
3. **La huella de metodologia** = un `.git` cuyo remote resuelve al repo de la instancia/hub/producto,
   O los marcadores del arbol atestado juntos. Un dir ajeno del usuario (sin huella) NO se flagea.
4. **Los fixtures del test viven BAJO el scratch root** (Aegis_Scratch), nunca en la raiz real: la
   propia unidad respeta la regla que enforcea.

Ciclo gobernado normal: entrega in_review -> yo recompongo por el entrypoint real -> review
adversarial de la Analista en clon limpio -> cierro. Tope 2 iteraciones.
