---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-checker-semantics-goalp1
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-arranque-build-goalp1 (mi fraseo owner=Codex-maker/Analista-checker que gatillo tu pregunta)
  - NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md s.2.1 (gate sellado de GOAL-P1) + s.2.2/s.4 (frontera P1 + FRONTERA-FIX)
  - NOVA_ESTUDIO_Protocolo_Medicion.md s.4 (instrumentacion pre-30-jul en categoria propia) + s.6 (defectos frontera P1 = checker_formal fuera de contraste)
one_line_summary: "Respuesta al conflicto que detectaste (schema sellado: baseline => checker_formal=0 vs mi DIRECTIVA owner=Analista-checker): adopta OPCION B (baseline fiel) para la FILA MEDIDA de GOAL-P1. checker_formal=0. Y NO pierdes lo valido de A: su valor (escrutinio formal de P1 + ensayo de la maquinaria gobernada) YA esta sellado en el lugar correcto (frontera P1 read-only 26-29 jul -> FRONTERA-FIX, y el ensayo de maquinaria en categoria propia fuera de Q1). Corrijo mi fraseo generico."
requested_action: "[DIRECTIVA] Adopta la OPCION B (baseline fiel) para GOAL-P1. Concretamente: (1) FILA MEDIDA de GOAL-P1 = Codex maker + gate en ventana = architecture tests + CI verde + adversarial informal de 12 puntos (que corre en AMBOS brazos y NO es el tratamiento); el hub SOLO coordina + atesta; SIN gate formal del Analista sobre el codigo -> checker_formal=0, fiel al schema sellado. El Analista PUEDE validar DoD/evidencia sin que eso cuente como checker_formal. (2) NO pierdes lo valido de A: su preocupacion (escrutinio FORMAL de P1 + ensayar la maquinaria gobernada antes del 30-jul) YA esta cubierta por el diseno sellado -> NO la inyectes como gate vivo. Escrutinio formal de P1 = la REVISION DE FRONTERA P1 sellada (26-29 jul, Analista READ-ONLY, detector=checker_formal, FUERA del contraste de brazos, remediacion a la fila FRONTERA-FIX); ya existe, no toca la fila baseline. (3) Ensayo de la maquinaria gobernada (submit_intent / checker formal / mailbox) end-to-end antes del 30-jul = actividad de ENSAYO SEPARADA, en categoria propia FUERA de Q1 (protocolo de medicion s.4: la instrumentacion pre-30-jul va a categoria propia; el overhead-fijo cuenta desde 30-jul). Corre sobre los artefactos de P1 o un throwaway; NO la escribas como checker_formal en la fila de GOAL-P1. (4) El PILOTO real de GOAL-P1 es validar la CAPTURA DE TOKENS end-to-end (protocolo s.4) = instrumentacion identica en ambos brazos, se valida con B igual. CORRECCION DE MI DIRECTIVA: 'owner=Codex-maker/Analista-checker' fue fraseo generico (regla el Analista es checker-only, no maker); para GOAL-P1 el checker VIVO es el adversarial informal; el Codex-maker/Analista-checker-FORMAL aplica a las tareas GOBERNADAS post-30-jul, no al piloto baseline. Razon de fondo: A meteria el tratamiento (checker formal) en una unidad PRE-tratamiento (el brazo gobernado no existe hasta 30-jul) y ensuciaria si GOAL-P1 es fila baseline o ensayo; B la deja como fila baseline limpia y fiel, y ademas piloto de la medicion."
question: ""
---

# DIRECTIVA - Semantica de checker para GOAL-P1 (adopta B, sin perder A)

Detectaste un conflicto REAL: el schema sellado dice `baseline => checker_formal=0`, pero mi DIRECTIVA
de arranque dijo `owner=Codex-maker/Analista-checker`. Tienes razon en levantarlo. Respuesta:

## Adopta OPCION B (baseline fiel)
La FILA MEDIDA de GOAL-P1: Codex maker + gate en ventana = architecture tests + CI verde + adversarial
informal de 12 puntos (corre en AMBOS brazos, NO es el tratamiento). El hub SOLO coordina + atesta. SIN
gate formal del Analista sobre el codigo -> `checker_formal=0`. La particion s.2.1 YA sella exactamente
ese gate para GOAL-P1. El Analista puede validar DoD/evidencia sin contar como checker_formal.

## No pierdes lo valido de A (esta es la parte fina)
La preocupacion de A -- escrutinio FORMAL de P1 + ensayar la maquinaria gobernada antes del 30-jul -- YA
esta cubierta por el diseno sellado, en el lugar correcto. No hay que inyectarla como gate vivo:

1. **Escrutinio formal de P1** = la REVISION DE FRONTERA P1 sellada (26-29 jul, Analista READ-ONLY,
   `detector=checker_formal`, FUERA del contraste de brazos, remediacion a la fila FRONTERA-FIX). Existe,
   pero es post-ventana y no toca la fila baseline.
2. **Ensayo de la maquinaria gobernada** (submit_intent / checker formal / mailbox) end-to-end antes del
   30-jul = actividad de ENSAYO SEPARADA, en categoria propia FUERA de Q1 (protocolo s.4). Sobre los
   artefactos de P1 o un throwaway; NO como checker_formal en la fila de GOAL-P1.
3. **El piloto real de GOAL-P1** = validar la CAPTURA DE TOKENS end-to-end (protocolo s.4) = instrumentacion
   identica en ambos brazos; se valida con B igual.

## Correccion de mi fraseo
`owner=Codex-maker/Analista-checker` fue generico (regla: el Analista es checker-only, no maker). Para
GOAL-P1 el checker VIVO es el adversarial informal. El `Codex-maker/Analista-checker-FORMAL` aplica a las
tareas GOBERNADAS (post-30-jul), no al piloto.

**Neto:** B deja a GOAL-P1 como fila baseline limpia y fiel al schema sellado, y ademas piloto de la
medicion. A ensuciaria una unidad pre-tratamiento con el tratamiento. Adopta B; el valor de A ya esta sellado.
