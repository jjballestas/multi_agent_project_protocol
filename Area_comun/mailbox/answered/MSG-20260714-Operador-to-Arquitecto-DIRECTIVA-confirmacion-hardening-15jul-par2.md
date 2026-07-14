---
message_id: MSG-20260714-Operador-to-Arquitecto-DIRECTIVA-confirmacion-hardening-15jul-par2
from: Operador
to: Arquitecto
type: DIRECTIVA
status: answered
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-14
context_refs:
  - Area_comun/artifacts/DRAFT-SELLO-ETAPA2-estructura-arquitecto.md (s.6 (b), act. 2026-07-14 ~14:20)
  - TASK-0254 / commit a2333dc (consolidacion hardening PAR-2)
  - DECISION-0091 (sello Etapa 1; calendario s.11.1; PAR-2 condicional, regla 8)
  - TASK-9392 (patron de re-verificacion gobernada firmada de BR-C4, s.28)
one_line_summary: "Confirmar formalmente el checkpoint HARDENING 15-jul (PAR-2 / Annul_*). El hardening entrego ADELANTADO (14-jul, a2333dc/TASK-0254) pero hoy esta como FYI en s.6, no como confirmacion gobernada. Pido: (a) enmienda fechada que registra la entrega; (b) estado REAL del cableado de Annul_Commitment; (c) verificacion independiente firmada; (d) dejar servida al operador la decision PAR-2 dentro/fuera del pool con su costo. n=10 NO depende de PAR-2."
requested_action: "Produce la confirmacion gobernada del hardening 15-jul: (a) redacta la ENMIENDA FECHADA al sello E2 que registra el hardening como ENTREGADO en plazo (procs Budget.Annul_* existentes + Assert_Permission + verificado sandbox, a2333dc/TASK-0254); (b) reporta el estado REAL de cableado C#: confirmado CDP-annul (Annul_Availability_Certificate) cableado, y que FALTA para Annul_Commitment (esfuerzo S/M/L); (c) declara si la entrega tiene VERIFICACION INDEPENDIENTE FIRMADA (maker!=checker, patron TASK-9392) o solo el FYI del entregador -- si no la tiene, indica que haria falta; (d) deja SERVIDA al operador la decision PAR-2 DENTRO vs FUERA del pool, con el costo de cada opcion (recordatorio: n=10 ya confirmado SIN PAR-2, es aditivo/opcional). NO incorpores PAR-2 al pool ni cables Annul_Commitment sin decision explicita del operador (regla 8: el dev nunca crea el proc)."
question: "Entregas la enmienda fechada + estado de cableado + estado de verificacion firmada + la decision PAR-2 servida al operador?"
---

# DIRECTIVA - Confirmacion gobernada del hardening 15-jul (PAR-2 / Annul_*)

## Contexto
El checkpoint del hardening (`nova-hardening`, procs `Budget.Annul_*`, deadline `<=15-jul`) **se cumplio
ADELANTADO** (14-jul): los tres `Annul_*` existen con `Assert_Permission`, verificados en vivo contra el
sandbox, PAR-2 parity preflighted, commit `a2333dc` / `TASK-0254`. Hoy eso vive como **FYI/actualizacion en
s.6 (b)** del draft del sello E2, **no como confirmacion gobernada**. El deadline NO esta en riesgo; lo
pendiente es formalizar.

## Lo que pido (4 entregables)

1. **Enmienda fechada al sello E2.** La regla sellada dice que los items de hardening entran *"solo por
   enmienda fechada con entrega comprometida"*. Redacta esa enmienda: registra el hardening como ENTREGADO
   EN PLAZO, citando procs + `Assert_Permission` + verificacion sandbox + `a2333dc`/`TASK-0254`. (No la
   selles todavia si depende de una decision del operador; entregala como draft para firma, patron s.27/s.28.)

2. **Estado REAL del cableado C#.** El caveat del FYI dice "solo CDP-annul cableado en C#". Confirma:
   - `Annul_Availability_Certificate` (CDP-annul): cableado + verificado -> SI/NO.
   - `Annul_Commitment`: existe en BD; que FALTA exactamente para cablearlo/verificarlo en C# y con que
     esfuerzo (S/M/L). Recuerda regla 8: el dev NO crea el proc; solo la superficie API sobre el proc existente.

3. **Verificacion independiente firmada.** BR-C4 se confirmo con re-verificacion GOBERNADA Y FIRMADA
   (`TASK-9392`, maker `jheredia:v1` + checker `analista:v1`, drift 0). Declara si la entrega del hardening
   tiene un **checker independiente firmado** al mismo estandar, o si por ahora solo esta el FYI del
   entregador (lado maker). Si falta, indica que haria falta para alcanzarlo.

4. **Decision PAR-2 servida al operador.** Deja lista, para que el operador decida, la eleccion:
   - **PAR-2 DENTRO del pool** (aditivo): requiere cerrar el cableado de `Annul_Commitment` (punto 2) +
     verificacion firmada (punto 3); a cambio engrosa el pool.
   - **PAR-2 FUERA del pool**: se registra "entregado, fuera del contraste" via la enmienda; rapido; el
     estudio sigue con n=10.
   No decidas tu; presenta ambas con su costo. **Recordatorio decisivo: el pool Q4 ya esta confirmado en
   n=10 SIN PAR-2, asi que PAR-2 es opcional, no ruta critica.**

## Frontera
Es carril del sello (tu). No toca el fondo pineado (hub 2E35F26E / epoch 1.14.0 / dataset N=500). PAR-2 no
se incorpora ni se cabla `Annul_Commitment` sin decision explicita del operador.
