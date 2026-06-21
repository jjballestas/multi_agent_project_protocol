---
message_id: MSG-20260621-Operador-to-Arquitecto-REQ-INGESTION-V2-PRIORIDAD
task_id: none
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Registrar (gobernado) este requerimiento como REQ de Zeus-protocol priority HIGH y autorar su SPEC con PRIORIDAD por encima de lo demas pendiente. Tratarlo como EVOLUCION / supersede de REQ-31100EAF (carga por archivo v1): NO specear la v1 como definitiva. Diagnostico: la v1 solo ADJUNTA el archivo y obliga a llenar Titulo/Narrativa/Intencion a mano (acceptanceIntent vacio -> 400); no extrae nada, anula el valor de cargar por archivo. Seed abajo. Mantener las guardas de ingestion (dato inerte, PII structural + ASCII, allowlist+tamano, OFF/gated)."
question: "Registras esta v2 como REQ priority high y la speceas PRIMERO (antes de los otros pendientes), como evolucion de REQ-31100EAF?"
one_line_summary: "PRIORIDAD #1 del operador: carga por archivo v2 = subir libre (sin formato) -> extraer historias/casos de uso -> generar requisitos candidatos -> pestana de REVISION para validar/editar -> solo validados se envian a SPEC; + selector de modo (digitado vs archivo) validando obligatorios en ambos. Supersede REQ-31100EAF (v1 solo adjunta, no extrae). Registrar high + specear primero."
context_refs:
  - Area_comun/tasks/req-31100eaf-requirement-seed.md
deadline_or_blocking_level: normal
---

# REQ PRIORITARIO - Carga por archivo v2 (extraccion + revision + selector de modo)

Este es mi requerimiento mas importante ahora. Registralo gobernado (priority high) y specealo
PRIMERO. Es la evolucion de la carga por archivo (REQ-31100EAF): la v1 solo adjunta el archivo y
me obliga a llenar los campos a mano (acceptanceIntent vacio -> 400) = no extrae nada. NO la
specees como definitiva.

## Seed

### Titulo
Carga por archivo v2: extraccion asistida de historias/casos de uso + pestana de revision + selector de modo

### Narrativa
Como operador quiero subir un archivo con historias de usuario o casos de uso SIN un formato
rigido, y que el sistema analice y extraiga la informacion y genere en ese momento los
requisitos/tareas candidatos que el archivo amerite; luego yo los valido o edito (ya con el
formato requerido) en una pestana especial, y solo al validarlos se envian para convertirse en
SPEC.

### Intencion de aceptacion
- Antes de crear, el operador elige el MODO: (a) "Nueva historia digitada" -> muestra los campos
  actuales; (b) "Por carga de archivo" -> flujo de archivo. En AMBOS modos se validan los campos
  obligatorios antes de EXECUTE (sin enviar con vacios/placeholder).
- Modo archivo: se sube un .md/.txt SIN formato definido; el sistema extrae las historias/casos
  de uso y genera 1..N requisitos candidatos a partir del contenido.
- Los candidatos se muestran en una PESTANA/panel de REVISION donde el operador valida o edita
  cada uno hasta dejarlo con el formato requerido (titulo + narrativa + intencion + proyecto).
- Solo los candidatos VALIDADOS se envian (EXECUTE gobernado) y aterrizan como semillas para SPEC;
  nada se envia sin validacion del operador.
- Guardas de ingestion intactas: contenido como dato INERTE (nunca ejecutado), PII structural
  guard + ASCII sobre el texto extraido, allowlist de tipo + limite de tamano, OFF/gated.

## Nota de alcance
El paso de extraccion/generacion (analizar el archivo libre -> candidatos) es la pieza grande;
dimensionala en la SPEC. Tengo otros requerimientos pero este es el #1 ahora. Canal ASCII.
