---
message_id: MSG-20260704-Arquitecto-to-Operador-FYI-asiento-coordinacion-build-nova
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: false
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-REQUEST-asiento-coordinacion-build-nova (tu pregunta)
  - Area_comun/decisions/DECISION-0050-repos-arquitectura-acoplamiento.md
  - Area_comun/decisions/DECISION-0085-nova-suite-layout-paraguas-aegis-productos.md
  - Area_comun/decisions/DECISION-0087-nombres-aegis-marca-metodologia.md
one_line_summary: "Regla: AHORA (GOAL-P1 + Sprint 1 del estudio) el asiento de coordinacion del build es el HUB (asiento unico, integridad del estudio, sin costura de atestacion antes del sello). El TARGET maduro es NOVA/Aegis (instancia del equipo); la MIGRACION es el paso de adopcion POST-sello, con regla dual de cross-atestacion. F2 probo el mecanismo, no ordena migrar a mitad del estudio."
requested_action: ""
question: ""
---

# FYI - Asiento de coordinacion del build de Nova (respuesta de arquitectura)

## La tension real (por eso la pregunta es fina)
Hay dos DECISIONes que apuntan distinto y hay que reconciliarlas explicitamente:
- **DECISION-0050 #1/#5:** governance/coordinacion/atestacion SIEMPRE en el protocolo; "la governance de
  TODOS los proyectos vive en el UNICO hub constante; los repos de producto rotan". -> asiento = HUB.
- **DECISION-0085/0087:** cada proyecto tiene su instancia `Aegis/` (ya existe NOVA/Aegis, F2 la construyo
  con governance/coordinacion/atestacion propia via Git). -> asiento = instancia del equipo.

No es contradiccion si se ESCALONA por tiempo y por CAPA. Regla:

## Regla (clara)

1. **AHORA -- ventana del estudio (GOAL-P1 3-8 jul + SPECs Sprint 1 hasta el sello/30-jul): asiento = HUB.**
   Los claims / tasks / mailbox / GOs del build gobernado se coordinan en el hub, donde HOY viven
   `Area_comun/specs/nova/`, el ledger #4 atestado, el corpus de medicion y el sello. Razon dura: el brazo
   GOBERNADO es el TRATAMIENTO que el estudio mide; su atestacion tiene que estar en el mismo #4 que la
   medicion y el sello, en UN solo asiento. Meter una segunda instancia (NOVA/Aegis) a mitad del estudio
   abre una COSTURA de cross-atestacion justo antes del sello (08-jul) = moving-part nueva en el peor
   momento (regla de oro del sello: nada nuevo cerca del sello). Ademas hoy funciona desde el hub.

2. **CODIGO de producto = NOVA/Nova-Budget** (settled, repo propio lazy). Sin multi-root (DECISION-0050).

3. **ESTUDIO / medicion / sello / #4-dataset = HUB** (settled). Es el dataset de investigacion; su lugar es
   Aegis-core/hub por definicion (DECISION-0050 #1: "this is the dataset").

4. **TARGET maduro (a donde VA) = NOVA/Aegis como asiento operativo del equipo Nova.** La vision
   (suite employee-ready, equipos que operan su propia instancia) ES que el build de Nova se coordine en su
   instancia `Aegis/`. F2 ya PROBO ese mecanismo (harness distribuido, clon limpio opera via Git). Pero
   "probar el mecanismo" != "migrar el brazo gobernado del estudio en vuelo".

5. **MIGRACION = paso de adopcion POST-sello, no ahora.** Cuando la Etapa 1 este sellada y medida, el build
   de Nova migra a NOVA/Aegis como la PRIMERA instancia employee-run real -- que es, ademas, la propia
   evidencia de transferibilidad del estudio (la replica employee-run pre-registrada). En ese punto aplica
   la **regla dual de cross-atestacion:**
   - **Hub (Aegis-core):** metodologia canonica + dataset del ESTUDIO/meta (#4 del hub) + sello.
   - **NOVA/Aegis:** #4 OPERATIVO del equipo Nova (sus claims/tasks/mailbox/GOs del build).
   - **Cruce:** el journal de medicion del hub registra, en cada gate, el sha256 de la atestacion de la
     instancia NOVA/Aegis (la instancia atesta su operacion; el hub atesta el estudio que la observa). Una
     linea, verificable por terceros; sin mezclar los dos #4.

## Nota a DECISION-0050/0085 (si lo apruebas)
Conviene una ENMIENDA CORTA que fije el escalonamiento y quite la ambiguedad del #5:
- Aclarar que "hub unico gobierna todo" (0050 #5) aplica a la governance del **ESTUDIO/meta-dataset** y a la
  metodologia canonica (Aegis-core); la governance OPERATIVA de un equipo de producto adoptante vive en su
  instancia `Aegis/` (0085/0087) una vez ADOPTADA, con la regla dual de cross-atestacion de arriba.
- Registrar el TRIGGER de migracion (post-sello Etapa 1) y la regla de cruce sha256.
Puedo redactar esa enmienda (mini-DECISION o addendum a 0050) para tu aprobacion; es frontera -> la decides tu.
No urge para GOAL-P1 (hoy = hub, funciona). La direccion de arriba ya te fija el workflow de VS Code:
gobernanza del build en el hub por ahora; codigo en Nova-Budget; NOVA/Aegis en reserva-probada para post-sello.
