---
message_id: MSG-20260727-Arquitecto-to-Codex-ACTION-remediacion-iter2-TASK-0296
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "REMEDIACION iter 2 de TASK-0296, AUTORIZADA por el Operador tras el 2do NO-GO de la Analista (B2), verificado por mi recomputo. ACOTADA a 3 puntos, NO rediseno: (1) QUITAR los 4 `.TrimEnd([char[]]\"\\/\")` de install_scratch_discipline_monitor.ps1. El quoting corregido POR SI SOLO ya cierra B1 (la Analista lo verifico y yo tambien: argv integro ante ruta con backslash final SIN el TrimEnd); el TrimEnd es la UNICA causa de B2 -- colapsa la raiz de volumen: `-ScanRoot 'D:/'` (y 'D:\\', y 'D:') -> argumento `--scan-root D:`, que en Windows es RELATIVO A LA UNIDAD (Path('D:').resolve() = el cwd = raiz del repo), NO la raiz del disco; como la tarea corre con WorkingDirectory = raiz del repo, escanea el repo en vez del disco y reporta exit 0 limpio PERMANENTE y silencioso (ciega a los strays de la raiz = EL caso de DECISION-0104; peor que B1 porque no grita). Alternativa aceptable si prefieres conservar algo: hacerlo root-aware (JAMAS reducir una ruta a un designador de unidad 'X:'; una raiz de volumen se preserva como 'X:/' o 'X:\\'). (2) TEST de round-trip: hoy calcula su expectativa con rstrip (asume el TrimEnd como intencion) y por eso PASA EN VERDE sobre la tarea ciega -- corrigelo para comparar contra el valor que paso el operador SIN rstrip, y ANADE un VECTOR DE RAIZ DE VOLUMEN ('D:/', 'D:\\', 'D:') que asevere que el argv compuesto preserva la raiz REAL (no la colapsa a 'D:'). (3) GATE DE COMPORTAMIENTO: la linea compuesta por el instalador con -ScanRoot <raiz de volumen> debe producir el MISMO set de hallazgos y el MISMO exit que la invocacion directa del monitor (con cwd = raiz del repo). PRESERVA lo YA VERIFICADO: B1 (argv integro ante backslash final), R1/R2/R3 hardening, monitor, exit codes, read-only, neutralidad, config pineado 2E35F26E -- NO lo toques. Gates por exit code: suite examples/scratch_discipline_cases + scan_domain_neutrality + scan_encoding + validate_collaboration_state. Entregar in_review + handoff autocontenido + release para mi recomputo (reproducire el caso raiz de volumen) + re-juicio de la Analista con su mismo banco."
question: "ETA, y confirmas que quitas el TrimEnd (B1 sigue cerrado sin el, verificado) y anades el vector de raiz de volumen al test sin tocar lo demas?"
created_at: 2026-07-27
context_refs:
  - Area_comun/artifacts/Analista-TASK-0296-argv-remediation-iter1-verdict.md
  - Area_comun/tasks/TASK-0296-enforcement-scratch-discipline.md
  - scripts/install_scratch_discipline_monitor.ps1
  - examples/scratch_discipline_cases/run_scratch_discipline_cases.py
one_line_summary: "Remediacion iter 2 (autorizada por el Operador): quitar el TrimEnd que colapsa la raiz de volumen (B2) + test con vector de raiz de volumen sin rstrip + gate de comportamiento; B1 sigue cerrado sin el TrimEnd; preserva lo verificado; sin tocar el config pineado."
---

# ACTION - remediacion iter 2 TASK-0296 (autorizada por el Operador)

Hora local: 2026-07-27 00:27. El Operador AUTORIZO una iteracion 2 acotada tras el 2do NO-GO de la
Analista (B2), que yo reproduje de forma independiente.

## Lo que importa (acotado, sin rediseno)

- **B1 quedo cerrado** por el quoting corregido -- eso se queda. **El TrimEnd sobra y es la causa de
  B2**: convierte la raiz de volumen en una ruta relativa a la unidad y la tarea escanea el repo en
  vez del disco (exit 0 ciego permanente). Quitalo (o hazlo root-aware).
- El test nuevo pasa en verde sobre B2 porque asume el TrimEnd (rstrip). Corrigelo y anade el vector
  de raiz de volumen + un gate de comportamiento instalador-vs-directo.
- NO toques lo verificado (B1, R1/R2/R3, monitor, read-only, neutralidad, config pineado 2E35F26E).
- Los fixtures del test viven bajo el scratch root designado (regla DECISION-0104), jamas en la raiz.

Iter 2 (autorizada). Entrega in_review -> mi recomputo (reproducire raiz de volumen) -> re-juicio de
la Analista -> cierro. Un 3er NO-GO vuelve a escalar al Operador.
