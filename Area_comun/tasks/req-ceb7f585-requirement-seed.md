---
task_id: "REQ-CEB7F585"
title: "Carga por archivo v2: extraccion asistida de historias/casos de uso + pestana de revision + sele"
type: "requirement"
status: cancelled
owner: "Operador"
phase: "P2"
priority: "normal"
project: "Zeus-protocol"
author: "Operador"
relayed_by: "Arquitecto"
endorsement: "none"
sdd_role: "seed_only_architect_authors_spec"
---

# REQ-CEB7F585 - Carga por archivo v2: extraccion asistida de historias/casos de uso + pestana de revision + sele

## Narrativa

Como operador quiero subir un archivo con historias de usuario o casos de uso SIN un formatorigido, y que el sistema analice y extraiga la informacion y genere en ese momento losrequisitos/tareas candidatos que el archivo amerite; luego yo los valido o edito (ya con elformato requerido) en una pestana especial, y solo al validarlos se envian para convertirse enSPEC. La carga actual (REQ-31100EAF) solo adjunta y obliga a llenar los campos a mano, lo queanula el valor de cargar por archivo.

## Intencion de aceptacion

- Antes de crear, el operador elige el MODO: (a) "Nueva historia digitada" -> muestra los campos actuales; (b) "Por carga de archivo" -> flujo de archivo. En AMBOS modos se validan los campos obligatorios antes de EXECUTE (sin enviar con vacios/placeholder).- Modo archivo: se sube un .md/.txt SIN formato definido; el sistema extrae las historias/casos de uso y genera 1..N requisitos candidatos a partir del contenido.- Los candidatos se muestran en una PESTANA/panel de REVISION donde el operador valida o edita cada uno hasta dejarlo con el formato requerido (titulo + narrativa + intencion + proyecto).- Solo los candidatos VALIDADOS se envian (EXECUTE gobernado) y aterrizan como semillas para SPEC; nada se envia sin validacion del operador.- Se mantienen las guardas: contenido como dato INERTE (nunca ejecutado), PII structural guard + ASCII sobre el texto extraido, allowlist de tipo + limite de tamano, OFF/gated.

## PII guard

- mode: structural
- channel: ascii
- free_text_public_plane: redacted
- warning_acknowledged: true
- redactions: 0

## Accountability

- author: Operador
- relayed_by: Arquitecto
- endorsement: none
