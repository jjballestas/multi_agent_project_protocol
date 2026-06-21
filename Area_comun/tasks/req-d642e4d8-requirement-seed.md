---
task_id: REQ-D642E4D8
type: requirement
status: proposed
owner: Operador
phase: P2
priority: high
project: Zeus-protocol
author: Operador
relayed_by: Arquitecto
endorsement: none
sdd_role: seed_only_architect_authors_spec
supersedes: REQ-31100EAF
file: Area_comun/tasks/req-d642e4d8-requirement-seed.md
---

# REQ-D642E4D8 - Carga por archivo v2: extraccion asistida + revision + selector de modo (supersede REQ-31100EAF)

## Narrativa

Como operador quiero subir un archivo con historias de usuario o casos de uso SIN un formato rigido, y que el
sistema analice y extraiga la informacion y genere en ese momento los requisitos/tareas candidatos que el
archivo amerite; luego yo los valido o edito (ya con el formato requerido) en una pestana especial, y solo al
validarlos se envian para convertirse en SPEC.

## Intencion de aceptacion

- Antes de crear, el operador elige el MODO: (a) "Nueva historia digitada" -> campos actuales; (b) "Por carga de
  archivo" -> flujo de archivo. En AMBOS modos se validan los obligatorios antes de EXECUTE (sin vacios/placeholder).
- Modo archivo: se sube un .md/.txt SIN formato definido; el sistema extrae historias/casos de uso y genera 1..N
  requisitos candidatos a partir del contenido.
- Los candidatos se muestran en una PESTANA/panel de REVISION donde el operador valida o edita cada uno hasta
  dejarlo con el formato requerido (titulo + narrativa + intencion + proyecto).
- Solo los candidatos VALIDADOS se envian (EXECUTE gobernado) y aterrizan como semillas para SPEC; nada se envia
  sin validacion del operador.
- Guardas de ingestion intactas: contenido como dato INERTE (nunca ejecutado), PII structural guard + ASCII sobre
  el texto extraido, allowlist de tipo + limite de tamano, OFF/gated.

## Nota de alcance
El paso de extraccion/generacion (analizar archivo libre -> candidatos) es la pieza grande; se dimensiona en la SPEC.

## Accountability
- author: Operador
- relayed_by: Arquitecto
- endorsement: none
