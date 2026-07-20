---
message_id: MSG-20260720-Operador-to-Arquitecto-REQUEST-ventana-N6-julian-entregables-previos
from: Operador
to: Arquitecto
type: REQUEST
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Confirmar si el build-open de Contabilidad puede adelantarse para que Julian (jheredia) construya las 6 unidades MEDIDAS del N=6 en cuanto este disponible, sin esperar al 30-jul: estado real de los entregables previos (corpus E2 <=25-jul, BR-C4 <=29-jul), si dependen de Julian o se desplazan, y que haria falta operativamente para abrir manana. Responder por mailbox; NO arrancar nada sin mi GO."
question: "Los entregables previos permiten adelantar el build-open para que Julian mida en cuanto tenga ventana, o hay una dependencia real que obligue a esperar al 30-jul?"
created_at: 2026-07-20
context_refs:
  - personal/asesor/DRAFT-PREREGISTRO-contabilidad-employee-run.md
one_line_summary: "PREGUNTA SIN GO: Julian tiene disponibilidad proxima y el pre-registro N=6 ya esta SELLADO con prep al 100pct (TASK-9401..9406 ready+reservadas, F3.3 verde, jheredia:v1 operativo), asi que el 30-jul no es puerta de la MEDICION sino del build-open. Se pide estado real de los entregables previos (corpus E2, BR-C4) para saber si se puede adelantar. Nada arranca sin GO del Operador."
---

# REQUEST - se puede adelantar la ventana del N=6?

**Esto es una pregunta, no un GO.** Nada arranca hasta que yo lo firme.

## Por que la hago

Julian tiene disponibilidad proxima, y su tiempo es el unico recurso de este proyecto con
agenda propia: Codex y el Analista son elasticos y no tienen fecha externa; Julian, si.
Si se pierde una ventana suya, no se sabe cuando vuelve.

## Lo que ya esta verificado

- **Pre-registro N=6 SELLADO** + ceremonia s.11 completa, con verificacion independiente
  por un segundo firmante con llave separada.
- **Prep al 100 pct**: TASK-9401..9406 en `ready` y reservadas, **F3.3 verde**, runbook de
  Julian listo.
- **`jheredia:v1` operativo**: llave ed25519 propia, HMAC propio, deploy key en NOVA,
  firmante desde el genesis.
- Y el gate literal del estado: *"gated post-30-jul (**prereq de la 1a unidad MEDIDA, no
  del sello del DISENO**)"*, *"GATED SOLO por el **build-open**"*.

**Lectura:** lo que esta gated no es MEDIR, es que el build de Contabilidad abre despues
de cerrar los entregables previos. Es secuencia operativa, no restriccion cientifica.

**Y el firewall no corre riesgo:** como el pre-registro ya esta sellado, adelantar la
fecha NO permite HARKing -- el diseno esta fijado y las unidades reservadas. No hay nada
que se pueda decidir a posteriori.

## Lo que necesito saber

1. **Estado real de los entregables previos**: corpus E2 (<=25-jul) y BR-C4 (<=29-jul).
   Cerrados, en curso, o en riesgo?
2. **Dependen de Julian?** Si el corpus o BR-C4 consumen su tiempo, medir primero podria
   desplazarlos -- y eso si seria un problema.
3. **Que haria falta operativamente** para abrir el build de Contabilidad en cuanto Julian
   tenga ventana: ceremonia de dos clones (jheredia maker / checker ratifica), disponibilidad
   del checker recien migrado, y cualquier otro prerequisito que yo no vea desde aqui.
4. **Riesgos de adelantar** que tu veas y yo no.

## Nota de agenda que ya detecte

La ceremonia del N=6 exige al **checker**, y el checker acaba de migrar de proveedor
(TASK-0271 done). Su primera carga real fue anoche y salio bien (0270 con 11/11), pero
conviene tenerlo en cuenta al planificar: es el mismo recurso que sostiene la cola de la
0103.

## Guardas

Reservadas N=6 intactas hasta que yo de el GO. Fondo intocable (2E35F26E / epoch 1.14.0 /
N=500). Firewall anti-HARKing intacto. Sin encender supervised_autonomy ni real_invoker.

-- Operador
