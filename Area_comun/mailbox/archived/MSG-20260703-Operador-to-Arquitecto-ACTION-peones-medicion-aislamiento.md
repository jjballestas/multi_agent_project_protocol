---
message_id: MSG-20260703-Operador-to-Arquitecto-ACTION-peones-medicion-aislamiento
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-03
context_refs:
  - Area_comun/tasks/TASK-0231 (F6.1 fase peones)
  - D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/NOVA_ESTUDIO_Protocolo_Medicion.md
one_line_summary: "La fase peones (F6/0231) y el sello Etapa 1 del estudio incorporan la MEDICION del uso de peones (5 campos nuevos del CSV) y la REGLA DE AISLAMIENTO (peones = variable distinta del gobierno atestado; su efecto se mide solo en F6, no dentro del contraste central)."
requested_action: "[DIRECTIVA] (1) MEDICION DEL USO DE PEONES: el schema del CSV de medicion (que congela el sello Etapa 1, <=08-jul) incorpora 5 campos: orchestration_mode (enum mono|peones|mixto|NA), peones_n (int), peon_revivals_n (int; los peones REVIVEN por memoria hibrida), peon_modelos (str; p.ej. qwen2.5-coder:7b, deepseek-coder:6.7b), tokens_peones (int). REGLA DURA de contabilidad: tokens_peones es SUBSET ya contado en las cubetas dev/checker (informativo, EXCLUIDO de toda confirmatoria, mismo trato que tokens_cache_reads) -> NO se suma aparte, no doble-contar. (2) REGLA DE AISLAMIENTO (a sellar en Etapa 1 como invariante): los peones son una VARIABLE distinta del tratamiento aditivo del estudio (el tratamiento medido es la GOBERNANZA ATESTADA, no la orquestacion). En el contraste central (baseline mono vs gobernado mono) el brazo gobernado se mantiene MONO-orquestado; si aparece un peon se REGISTRA (descriptivo via orchestration_mode) pero NO convierte el brazo en 'tratamiento peones'. El EFECTO de los peones (util o no) se mide SOLO en F6 (mono-vs-peones bajo gobierno completo -> Q1), aislado, con orchestration_mode declarado por tarea. Meter peones en el brazo gobernado del estudio central cambia DOS cosas a la vez (gobierno + orquestacion) y confunde Q1/Q4: prohibido. (3) F6/TASK-0231: anota en su cuerpo/DoD que su diseno declara orchestration_mode por tarea, captura los 5 campos peon, y respeta el aislamiento (no se solapa con las unidades del contraste central; su pool es propio). [RECOMENDACION] Los 5 campos y la regla ya estan borroneados en el schema del asesor (borrador scripts-medicion, a emplazar en el hub personal/Arquitecto/TFM-medicion/corpus/ cuando corresponda); al sellar Etapa 1 se congelan con estos campos. Modelos peon candidatos ya instalados en Ollama: qwen2.5-coder:3b/7b y deepseek-coder:6.7b (coders)."
question: ""
---

# ACTION - Peones: medicion del uso + regla de aislamiento (F6/0231 + sello Etapa 1)

Directiva del Operador tras revisar la Composicion del equipo (el rol de construccion
recae casi todo en un firmante -> los peones son la via de paralelizacion). Se quiere
MEDIR el uso de peones, pero sin contaminar el estudio central.

Dos piezas (detalle vinculante en requested_action):
1. **Medir el USO** (descriptivo): 5 campos nuevos del CSV -- orchestration_mode,
   peones_n, peon_revivals_n, peon_modelos, tokens_peones. tokens_peones es subset ya
   contado en dev/checker (no doble-contar; fuera de confirmatorias).
2. **Regla de aislamiento** (sellada como invariante): peones = variable distinta del
   gobierno atestado. Brazo gobernado del contraste central = MONO. El efecto de los
   peones se mide SOLO en F6 (mono-vs-peones), aislado. Prohibido mezclarlos en el
   contraste central (confundiria Q1/Q4).

El sello Etapa 1 (borrador del asesor, <=08-jul; tu lo atestas por sha256 via intent
del hub) congela estos campos y esta regla.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
